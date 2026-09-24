# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import sys
import math


class SplineLinkingAndCroppingDisplay(ompx.MPxNode):
    node_name = "SplineLinkingAndCroppingDisplay"
    # 更新ID防止冲突
    Uv_id = om.MTypeId(0x00141480 + 5)

    def __init__(self):
        super(SplineLinkingAndCroppingDisplay, self).__init__()

    def compute(self, plug, data_block):
        if plug != self.out_curve and plug != self.out_surface:
            return

        # --- 读取基础输入属性 ---
        start_point_value = data_block.inputValue(self.start_point).asInt()
        keep_point_value = data_block.inputValue(self.keep_point).asInt()

        # 读取基础旋转角度属性 (角度制)
        base_rotation_angle = data_block.inputValue(self.rotation).asDouble()

        # 获取数组句柄
        offset_parent_handle = data_block.inputArrayValue(self.offset_point)
        link_order_handle = data_block.inputArrayValue(self.link_order)
        reverse_curve_handle = data_block.inputArrayValue(self.reverse_curve)
        curve_rotation_handle = data_block.inputArrayValue(self.curve_rotation)
        in_curve_handle = data_block.inputArrayValue(self.in_curve)

        if in_curve_handle.elementCount() == 0:
            return

        # --- 初始化核心数据 ---
        first_degree = 3
        first_form = om.MFnNurbsCurve.kOpen
        is_rational = False

        # --- 获取逻辑索引并排序 ---
        thisNode = self.thisMObject()
        depFn = om.MFnDependencyNode(thisNode)
        matrixPlug = depFn.findPlug("inCurve", False)
        indexArray = om.MIntArray()
        matrixPlug.getExistingArrayAttributeIndices(indexArray)

        # 获取自定义链接顺序指针并重新组合，移除-1项
        try:
            sorted_indices = sorted(
                [idx for idx in indexArray
                 if (link_order_handle.jumpToElement(idx),
                     link_order_handle.inputValue().asInt())[1] != -1],
                key=lambda idx: (link_order_handle.jumpToElement(idx),
                                 link_order_handle.inputValue().asInt())[1]
            )
        except:
            sorted_indices = []

        if not sorted_indices:
            return

        # --- 遍历并同步处理 曲线数据 和 偏移数据 ---
        curves_data = []
        for i in sorted_indices:
            # 获取反转属性
            reverse_curve_handle.jumpToElement(i)
            need_reverse = reverse_curve_handle.inputValue().asInt()

            # 获取该曲线的独立旋转角度
            try:
                curve_rotation_handle.jumpToElement(i)
                curve_rot = curve_rotation_handle.inputValue().asDouble()
            except:
                curve_rot = 0.0

            # 获取样条数据
            in_curve_handle.jumpToElement(i)
            input_data_obj = in_curve_handle.inputValue().data()

            if input_data_obj.hasFn(om.MFn.kNurbsCurve):
                curve_fn = om.MFnNurbsCurve(input_data_obj)

                # 1. 获取原始CV数据
                cvs = om.MPointArray()
                curve_fn.getCVs(cvs, om.MSpace.kWorld)
                num_cvs_orig = cvs.length()

                knots = om.MDoubleArray()
                curve_fn.getKnots(knots)

                # 2. 获取对应的 offsetValues 数组
                current_offsets = []
                try:
                    offset_parent_handle.jumpToElement(i)
                    child_handle = offset_parent_handle.inputValue().child(self.offset_values)
                    inner_array_handle = om.MArrayDataHandle(child_handle)

                    for j in range(inner_array_handle.elementCount()):
                        inner_array_handle.jumpToElement(j)
                        current_offsets.append(inner_array_handle.inputValue().asDouble())
                except:
                    pass  # 如果没有数据，保持空列表，下面会自动补齐

                # 3. 核心：强制对齐 offset 长度与 CV 数量
                # 如果用户手动删减了 offset 数组，或者还没初始化好，必须强制对齐，否则后面会越界
                if len(current_offsets) < num_cvs_orig:
                    current_offsets.extend([0.0] * (num_cvs_orig - len(current_offsets)))
                elif len(current_offsets) > num_cvs_orig:
                    current_offsets = current_offsets[:num_cvs_orig]

                # 4. 手动反转逻辑 (CV、Knot 和 offset 必须同步反转)
                if need_reverse == 1:
                    # 反转 CVs
                    reversed_cvs = om.MPointArray()
                    reversed_cvs.setLength(num_cvs_orig)
                    for j in range(num_cvs_orig):
                        reversed_cvs.set(cvs[num_cvs_orig - 1 - j], j)
                    cvs = reversed_cvs

                    # 反转 Knots
                    num_knots = knots.length()
                    reversed_knots = om.MDoubleArray()
                    reversed_knots.setLength(num_knots)
                    max_knot = knots[num_knots - 1]
                    for j in range(num_knots):
                        reversed_knots.set(max_knot - knots[num_knots - 1 - j], j)
                    knots = reversed_knots

                    # 反转 offset 数组
                    current_offsets.reverse()

                # 记录第一条线的信息作为基准
                if len(curves_data) == 0:
                    first_degree = curve_fn.degree()
                    first_form = curve_fn.form()

                # 将 offset 数据和曲线旋转也存入元组中传递给下一个阶段
                curves_data.append((cvs, knots, cvs.length(), current_offsets, curve_rot))

                # 检查是否为有理曲线
                if not is_rational:
                    for k in range(cvs.length()):
                        if cvs[k].w != 1.0:
                            is_rational = True
                            break

        if not curves_data:
            return

        # --- 合并 CVs、Knots 和 Offsets ---
        combined_cvs = om.MPointArray()
        global_knots = om.MDoubleArray()
        combined_offsets = []  # 用于存储合并后的全局 offset

        current_knot_val = 0.0
        global_knots.append(current_knot_val)

        # 头部压紧 (Start Clamp)
        for _ in range(first_degree - 1):
            global_knots.append(current_knot_val)

        for i, (cvs, knots, num_cvs, offsets, curve_rot) in enumerate(curves_data):
            # 合并 CV 和 Offset (绝对的一一对应)
            # 将曲线独立旋转叠加到每个CV的offset中，最终旋转 = 全局rotation + 曲线rotation + CV offset
            for k in range(num_cvs):
                combined_cvs.append(cvs[k])
                combined_offsets.append(offsets[k] + curve_rot)

            # 提取内部节点间距
            for k in range(first_degree, num_cvs):
                if k < knots.length():
                    delta = max(0.0, knots[k] - knots[k - 1])
                else:
                    delta = 1.0
                current_knot_val += delta
                global_knots.append(current_knot_val)

            # 生成“连接处”过渡节点
            if i < len(curves_data) - 1:
                for _ in range(first_degree):
                    current_knot_val += 1.0
                    global_knots.append(current_knot_val)

        # 尾部压紧 (End Clamp)
        for _ in range(first_degree - 1):
            global_knots.append(current_knot_val)

        # --- 执行截取逻辑 ---
        num_total_cvs = combined_cvs.length()
        if start_point_value >= num_total_cvs - 1:
            start_point_value = max(0, num_total_cvs - 2)

        actual_end = start_point_value + keep_point_value
        if actual_end > num_total_cvs:
            actual_end = num_total_cvs

        if actual_end - start_point_value < 2:
            return

        cropped_cvs = om.MPointArray()
        cropped_offsets = []  # 截取后的 offset
        for i in range(start_point_value, actual_end):
            cropped_cvs.append(combined_cvs[i])
            cropped_offsets.append(combined_offsets[i])  # 同步截取

        # --- 精确提取对应的 Knot 子集 ---
        num_final_cvs = cropped_cvs.length()
        num_needed_knots = num_final_cvs + first_degree - 1
        final_knots = om.MDoubleArray()

        base_knot_idx = start_point_value
        knot_offset_val = global_knots[base_knot_idx]
        for i in range(num_needed_knots):
            final_knots.append(global_knots[base_knot_idx + i] - knot_offset_val)

        # --- 创建输出曲线 ---
        curve_data_fn = om.MFnNurbsCurveData()
        output_curve_obj = curve_data_fn.create()

        new_curve_fn = om.MFnNurbsCurve()
        new_curve_fn.create(
            cropped_cvs,
            final_knots,
            first_degree,
            first_form,
            is_rational,
            False,
            output_curve_obj
        )

        output_handle = data_block.outputValue(self.out_curve)
        output_handle.setMObject(output_curve_obj)

        # --- 生成挤出曲面逻辑 ---
        if plug == self.out_surface:
            surface_data_fn = om.MFnNurbsSurfaceData()
            output_surf_obj = surface_data_fn.create()

            surface_cvs = om.MPointArray()
            extrusion_dist = 1.0
            up_vector = om.MVector(0, 1, 0)

            for i in range(num_final_cvs):
                # 1. 计算切线 (Tangent)
                if i < num_final_cvs - 1:
                    tangent = om.MVector(cropped_cvs[i + 1] - cropped_cvs[i])
                else:
                    tangent = om.MVector(cropped_cvs[i] - cropped_cvs[i - 1])

                if tangent.length() < 0.0001:
                    if i > 0: tangent = om.MVector(cropped_cvs[i] - cropped_cvs[i - 1])

                tangent.normalize()

                # 2. 计算侧向向量
                dot = tangent * up_vector
                if abs(dot) > 0.999:
                    side_vec = tangent ^ om.MVector(0, 0, 1)
                else:
                    side_vec = tangent ^ up_vector

                side_vec.normalize()

                # 3. 计算最终旋转角度：基础属性旋转 + 该点专属偏移值
                # 这里我们默认 offsetValues 里填的也是角度值
                point_offset_angle = cropped_offsets[i]
                total_angle_deg = base_rotation_angle + point_offset_angle

                # 转换为弧度
                total_angle_rad = math.radians(total_angle_deg)

                # 4. 应用旋转
                if abs(total_angle_rad) > 0.0001:
                    quat = om.MQuaternion(total_angle_rad, tangent)
                    rot_matrix = quat.asMatrix()
                    rotated_side_vec = side_vec * rot_matrix
                    final_side_vec = rotated_side_vec.normal()
                else:
                    final_side_vec = side_vec

                # 第一排点 (原曲线点)
                surface_cvs.append(cropped_cvs[i])

                # 第二排点 (挤出点)
                offset_pt = om.MPoint(
                    cropped_cvs[i].x + final_side_vec.x * extrusion_dist,
                    cropped_cvs[i].y + final_side_vec.y * extrusion_dist,
                    cropped_cvs[i].z + final_side_vec.z * extrusion_dist
                )
                surface_cvs.append(offset_pt)

            # 定义 V 方向的节点 (线性挤出)
            v_knots = om.MDoubleArray()
            v_knots.append(0.0)
            v_knots.append(1.0)

            # 创建曲面
            new_surf_fn = om.MFnNurbsSurface()
            try:
                new_surf_fn.create(
                    surface_cvs,
                    final_knots,
                    v_knots,
                    first_degree,
                    1,
                    first_form,
                    om.MFnNurbsSurface.kOpen,
                    is_rational,
                    output_surf_obj
                )

                surf_output_handle = data_block.outputValue(self.out_surface)
                surf_output_handle.setMObject(output_surf_obj)
            except:
                sys.stderr.write("Failed to create complex surface\n")

        data_block.setClean(plug)

    # ---------------- 保持不变的辅助函数 ----------------
    def connectionMade(self, plug, otherPlug, asSrc):
        if plug.attribute() == self.in_curve:
            if plug.isElement():
                index = plug.logicalIndex()
                this_node = self.thisMObject()
                dep_node_fn = om.MFnDependencyNode(this_node)

                # 设置 link_order
                link_order_plug = dep_node_fn.findPlug(self.link_order, False)
                try:
                    target_element = link_order_plug.elementByLogicalIndex(index)
                    target_element.setInt(index)
                except:
                    pass

                # 设置 reverse_curve
                reverse_curve_plug = dep_node_fn.findPlug(self.reverse_curve, False)
                try:
                    target_element = reverse_curve_plug.elementByLogicalIndex(index)
                    target_element.setInt(0)
                except:
                    pass

                # 设置 offset_point 默认值
                in_curve_plug = dep_node_fn.findPlug(self.in_curve, False)
                curve_element_plug = in_curve_plug.elementByLogicalIndex(index)
                curve_obj = curve_element_plug.asMObject()
                cv_count = 0
                if curve_obj.hasFn(om.MFn.kNurbsCurve):
                    curve_fn = om.MFnNurbsCurve(curve_obj)
                    cv_count = curve_fn.numCVs()

                if cv_count > 0:
                    offset_point_plug = dep_node_fn.findPlug(self.offset_point, False)
                    offset_element_plug = offset_point_plug.elementByLogicalIndex(index)
                    offset_values_plug = offset_element_plug.child(self.offset_values)
                    offset_values_plug.setNumElements(cv_count)
                    for j in range(cv_count):
                        try:
                            element_plug = offset_values_plug.elementByLogicalIndex(j)
                            element_plug.setDouble(0.0)  # 初始化旋转角度为 0.0
                        except:
                            pass

                # 初始化该曲线的独立旋转角度为 0.0
                curve_rotation_plug = dep_node_fn.findPlug(self.curve_rotation, False)
                try:
                    cr_element = curve_rotation_plug.elementByLogicalIndex(index)
                    cr_element.setDouble(0.0)
                except:
                    pass

        return super(SplineLinkingAndCroppingDisplay, self).connectionMade(plug, otherPlug, asSrc)

    def connectionBroken(self, plug, otherPlug, asSrc):
        if plug.attribute() == self.in_curve:
            if plug.isElement():
                index = plug.logicalIndex()
                this_node = self.thisMObject()
                dep_node_fn = om.MFnDependencyNode(this_node)
                link_order_plug = dep_node_fn.findPlug(self.link_order, False)
                try:
                    target_element = link_order_plug.elementByLogicalIndex(index)
                    target_element.setInt(-1)
                except:
                    pass
        return super(SplineLinkingAndCroppingDisplay, self).connectionBroken(plug, otherPlug, asSrc)

    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
        tAttr = om.MFnTypedAttribute()
        cAttr = om.MFnCompoundAttribute()

        # 基础属性
        cls.start_point = nAttr.create("startPoint", "sp", om.MFnNumericData.kInt, 0)
        nAttr.setMin(0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.start_point)

        cls.keep_point = nAttr.create("keepPoint", "kp", om.MFnNumericData.kInt, 100)
        nAttr.setStorable(True)
        nAttr.setMin(1)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.keep_point)

        # 全局基础旋转属性
        cls.rotation = nAttr.create("rotation", "rot", om.MFnNumericData.kDouble, 0.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.rotation)

        # 数组属性
        cls.link_order = nAttr.create("linkOrder", "lo", om.MFnNumericData.kInt, 0)
        nAttr.setMin(-1)
        nAttr.setArray(True)
        nAttr.setStorable(True)
        cls.addAttribute(cls.link_order)

        cls.reverse_curve = nAttr.create("reverseCurve", "rc", om.MFnNumericData.kInt, 0)
        nAttr.setMin(0)
        nAttr.setMax(1)
        nAttr.setArray(True)
        nAttr.setStorable(True)
        cls.addAttribute(cls.reverse_curve)

        # 每条曲线的独立旋转角度 (与全局rotation叠加)
        cls.curve_rotation = nAttr.create("curveRotation", "crot", om.MFnNumericData.kDouble, 0.0)
        nAttr.setArray(True)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.curve_rotation)

        # 复合数组属性 (用于存储每个控制点的偏转角度)
        cls.offset_values = nAttr.create("offsetValues", "ovs", om.MFnNumericData.kDouble, 0.0)
        nAttr.setArray(True)
        nAttr.setStorable(True)

        cls.offset_point = cAttr.create("offsetPoint", "ofp")
        cAttr.setArray(True)
        cAttr.addChild(cls.offset_values)
        cAttr.setStorable(True)
        cls.addAttribute(cls.offset_point)

        # 输入输出属性
        cls.in_curve = tAttr.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)
        cls.addAttribute(cls.in_curve)

        cls.out_curve = tAttr.create("outCurve", "oc", om.MFnData.kNurbsCurve)
        tAttr.setWritable(False)
        tAttr.setStorable(False)
        cls.addAttribute(cls.out_curve)

        cls.out_surface = tAttr.create("outSurface", "os", om.MFnData.kNurbsSurface)
        tAttr.setWritable(False)
        tAttr.setStorable(False)
        cls.addAttribute(cls.out_surface)

        # 依赖关系
        input_list_for_curve = [cls.in_curve, cls.start_point, cls.keep_point,
                                cls.link_order, cls.reverse_curve]
        for attr in input_list_for_curve:
            cls.attributeAffects(attr, cls.out_curve)

        input_list_for_surface = [cls.in_curve, cls.start_point, cls.keep_point,
                                  cls.link_order, cls.reverse_curve, cls.offset_point,
                                  cls.rotation, cls.curve_rotation]
        for attr in input_list_for_surface:
            cls.attributeAffects(attr, cls.out_surface)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(SplineLinkingAndCroppingDisplay())


def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(SplineLinkingAndCroppingDisplay.node_name,
                            SplineLinkingAndCroppingDisplay.Uv_id,
                            SplineLinkingAndCroppingDisplay.nodeCreator,
                            SplineLinkingAndCroppingDisplay.nodeInitializer)
        print("SplineLinkingAndCroppingDisplay节点注册成功！")
    except:
        sys.stderr.write("注册节点失败\n")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    try:
        plugin.deregisterNode(SplineLinkingAndCroppingDisplay.Uv_id)
        print("SplineLinkingAndCroppingDisplay节点注销成功！")
    except:
        sys.stderr.write("注销节点失败\n")