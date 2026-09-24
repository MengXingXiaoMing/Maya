# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class SplineLinkingAndCroppingDisplay(ompx.MPxNode):
    node_name = "SplineLinkingAndCroppingDisplay"
    Uv_id = om.MTypeId(0x00141480 + 63)  # 更新ID防止冲突

    def __init__(self):
        super(SplineLinkingAndCroppingDisplay, self).__init__()

    def compute(self, plug, data_block):
        if plug != self.out_curve and plug != self.out_surface:
            return

        start_point_value = data_block.inputValue(self.start_point).asInt()
        keep_point_value = data_block.inputValue(self.keep_point).asInt()

        link_order_handle = data_block.inputArrayValue(self.link_order)

        in_curve_handle = data_block.inputArrayValue(self.in_curve)
        element_count = in_curve_handle.elementCount()

        if element_count == 0:
            return

        first_degree = 3
        first_form = om.MFnNurbsCurve.kOpen
        is_rational = False

        # 获取当前节点的MObject
        thisNode = self.thisMObject()
        # 创建MFnDependencyNode函数集
        depFn = om.MFnDependencyNode(thisNode)
        # 找到 inCurve 属性
        matrixPlug = depFn.findPlug("inCurve", False)
        # 获取所有存在的索引
        indexArray = om.MIntArray()
        matrixPlug.getExistingArrayAttributeIndices(indexArray)

        # # 获取自定义链接顺序指针并重新组合
        # arrangement_list = []
        # for i in indexArray:
        #     # 跳转到当前元素
        #     link_order_handle.jumpToElement(i)
        #     # 获取当前元素的逻辑索引
        #     # logical_index = link_order_handle.elementIndex()
        #     # 获取当前元素的值
        #     element_handle = link_order_handle.inputValue()
        #     element_value = element_handle.asInt()
        #     # print('当前值', i, '   ', element_value)
        #     list = [i, element_value]
        #     arrangement_list.append(list)
        # # 重新提取储存的顺序值对指针循环顺序进行修改
        # sorted_data = sorted(arrangement_list, key=lambda x: x[1])

        sorted_indices = sorted(
            [idx for idx in indexArray
             if (link_order_handle.jumpToElement(idx),
                 link_order_handle.inputValue().asInt())[1] != -1],
            key=lambda idx: (link_order_handle.jumpToElement(idx),
                             link_order_handle.inputValue().asInt())[1]
        )
        # print('移除-1项')
        # 直接使用排序后的索引处理曲线
        curves_data = []
        for i in sorted_indices:
            in_curve_handle.jumpToElement(i)
            input_data_obj = in_curve_handle.inputValue().data()

            if input_data_obj.hasFn(om.MFn.kNurbsCurve):
                curve_fn = om.MFnNurbsCurve(input_data_obj)

                cvs = om.MPointArray()
                curve_fn.getCVs(cvs, om.MSpace.kWorld)

                knots = om.MDoubleArray()
                curve_fn.getKnots(knots)

                if len(curves_data) == 0:
                    first_degree = curve_fn.degree()
                    first_form = curve_fn.form()

                curves_data.append((cvs, knots, cvs.length()))

                # 检查是否有权重不同的点（Rational）
                for k in range(cvs.length()):
                    if cvs[k].w != 1.0:
                        is_rational = True

        if len(curves_data) == 0:
            return

        # 2. 【核心重构】按严格数学公式生成全局 CVs 和全局 Knots
        combined_cvs = om.MPointArray()
        global_knots = om.MDoubleArray()

        current_knot_val = 0.0
        global_knots.append(current_knot_val)  # 放入第一个节点

        # 头部压紧 (Start Clamp): D-1 个重复值
        for _ in range(first_degree - 1):
            global_knots.append(current_knot_val)

        # 遍历每条线，提取内部间距
        for i, (cvs, knots, num_cvs) in enumerate(curves_data):
            # 合并 CV
            for k in range(num_cvs):
                combined_cvs.append(cvs[k])

            # 提取这段曲线内部真实的形变间距（跳过两端的 Clamp）
            # 内部间距的数量刚好等于 num_cvs - first_degree
            for k in range(first_degree, num_cvs):
                if k < knots.length():
                    delta = max(0.0, knots[k] - knots[k - 1])
                else:
                    delta = 1.0
                current_knot_val += delta
                global_knots.append(current_knot_val)

            # 如果这不是最后一条线，我们需要生成“连接处”的过渡节点
            # 连接处需要 D 个节点来保证平滑且不断裂，步长设为 1.0
            if i < len(curves_data) - 1:
                for _ in range(first_degree):
                    current_knot_val += 1.0
                    global_knots.append(current_knot_val)

        # 尾部压紧 (End Clamp): D-1 个重复值
        for _ in range(first_degree - 1):
            global_knots.append(current_knot_val)

        # ---------------------------------------------------------
        # 此时的 global_knots 长度，在数学上绝对等于 combined_cvs.length() + first_degree - 1
        # 我们用这种“根据跨度重建”的方法，彻底消灭了越界和错位的可能！
        # ---------------------------------------------------------

        # 3. 执行截取逻辑
        num_total_cvs = combined_cvs.length()
        if start_point_value >= num_total_cvs - 1:
            start_point_value = max(0, num_total_cvs - 2)

        actual_end = start_point_value + keep_point_value
        if actual_end > num_total_cvs:
            actual_end = num_total_cvs

        if actual_end - start_point_value < 2:
            return

        cropped_cvs = om.MPointArray()
        for i in range(start_point_value, actual_end):
            cropped_cvs.append(combined_cvs[i])

        # 4. 精确提取对应的 Knot 子集
        num_final_cvs = cropped_cvs.length()
        num_needed_knots = num_final_cvs + first_degree - 1
        final_knots = om.MDoubleArray()

        base_knot_idx = start_point_value
        # 这一步绝对不会越界，因为 global_knots 长度完美匹配总 CV 数
        knot_offset_val = global_knots[base_knot_idx]
        for i in range(num_needed_knots):
            final_knots.append(global_knots[base_knot_idx + i] - knot_offset_val)

        # 5. 创建输出
        curve_data_fn = om.MFnNurbsCurveData()
        output_data_obj = curve_data_fn.create()

        new_curve_fn = om.MFnNurbsCurve()
        new_curve_fn.create(
            cropped_cvs,
            final_knots,
            first_degree,
            first_form,
            is_rational,
            False,
            output_data_obj
        )

        output_handle = data_block.outputValue(self.out_curve)
        output_handle.setMObject(output_data_obj)

        ##############################

        # --- [新增：生成挤出曲面逻辑] ---
        surface_data_fn = om.MFnNurbsSurfaceData()
        output_surf_obj = surface_data_fn.create()

        # 计算曲面的控制点 (2排点：第一排是原曲线CV，第二排是偏移后的CV)
        surface_cvs = om.MPointArray()
        extrusion_dist = 1.0
        up_vector = om.MVector(0, 1, 0)  # 参考向量
        # if output_data_obj:
        for i in range(num_final_cvs):
            # 1. 计算当前点的切线 (近似处理：取前后点向量)
            if i < num_final_cvs - 1:
                tangent = om.MVector(cropped_cvs[i + 1] - cropped_cvs[i])
            else:
                tangent = om.MVector(cropped_cvs[i] - cropped_cvs[i - 1])

            tangent.normalize()

            # 2. 为了防止“翻转”，计算侧向向量 (Side = Tangent x Up)
            # 如果切线太靠近Up轴，换一个参考轴
            side_vec = tangent ^ up_vector
            if side_vec.length() < 0.001:
                side_vec = tangent ^ om.MVector(0, 0, 1)

            side_vec.normalize()
            # 这里的 side_vec 就是挤出方向

            # 第一排点 (原点)
            surface_cvs.append(cropped_cvs[i])
            # 第二排点 (挤出点)
            offset_pt = om.MPoint(cropped_cvs[i].x + side_vec.x * extrusion_dist,
                                  cropped_cvs[i].y + side_vec.y * extrusion_dist,
                                  cropped_cvs[i].z + side_vec.z * extrusion_dist)
            surface_cvs.append(offset_pt)

        # 定义 V 方向的节点 (线性挤出，度数为1)
        v_knots = om.MDoubleArray()
        v_knots.append(0.0)
        v_knots.append(1.0)

        # 创建曲面
        # U方向沿曲线 (first_degree)，V方向线性 (degree 1)
        new_surf_fn = om.MFnNurbsSurface()
        new_surf_fn.create(
            surface_cvs,
            final_knots,  # U方向节点使用曲线的节点
            v_knots,  # V方向节点 [0, 1]
            first_degree,  # U方向度数
            1,  # V方向度数 (线性挤出)
            first_form,  # U方向形式
            om.MFnNurbsSurface.kOpen,  # V方向形式
            is_rational,
            output_surf_obj
        )

        # 输出曲面
        surf_output_handle = data_block.outputValue(self.out_surface)
        surf_output_handle.setMObject(output_surf_obj)
        # ---------------------------

        data_block.setClean(plug)

    # 被链接运行命令
    def connectionMade(self, plug, otherPlug, asSrc):
        """
        当有连接建立时触发。
        plug: 本节点的属性
        otherPlug: 源节点的属性
        asSrc: 是否作为源（我们这里关注的是连入，所以通常为 False）
        """
        # 1. 检查连入的是不是 inCurve 属性
        if plug.attribute() == self.in_curve:
            # 2. 获取当前的索引 (比如 inCurve[3] 的索引就是 3)
            if plug.isElement():
                index = plug.logicalIndex()

                # 3. 找到对应的 link_order[index] 插槽
                # 使用 MFnDependencyNode 来访问当前节点的 plug
                this_node = self.thisMObject()
                dep_node_fn = om.MFnDependencyNode(this_node)
                link_order_plug = dep_node_fn.findPlug(self.link_order, False)

                # 确保 link_order 也是数组，并定位到相同索引
                target_element = link_order_plug.elementByLogicalIndex(index)

                # 4. 设置值为 1
                try:
                    target_element.setInt(index)
                except:
                    pass

                link_order_plug = dep_node_fn.findPlug(self.reverse_curve, False)

                # 确保 link_order 也是数组，并定位到相同索引
                target_element = link_order_plug.elementByLogicalIndex(index)

                # 4. 设置值为 1
                try:
                    target_element.setInt(0)
                except:
                    pass

        return super(SplineLinkingAndCroppingDisplay, self).connectionMade(plug, otherPlug, asSrc)

    def connectionBroken(self, plug, otherPlug, asSrc):
        """
        (可选) 当连接断开时，把 link_order 恢复为 0
        """
        if plug.attribute() == self.in_curve:
            if plug.isElement():
                index = plug.logicalIndex()
                this_node = self.thisMObject()
                dep_node_fn = om.MFnDependencyNode(this_node)
                link_order_plug = dep_node_fn.findPlug(self.link_order, False)
                target_element = link_order_plug.elementByLogicalIndex(index)

                try:
                    target_element.setInt(-1)
                except:
                    pass




        return super(SplineLinkingAndCroppingDisplay, self).connectionBroken(plug, otherPlug, asSrc)

    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
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

        tAttr = om.MFnTypedAttribute()
        cls.in_curve = tAttr.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)
        cls.addAttribute(cls.in_curve)

        cls.out_curve = tAttr.create("outCurve", "oc", om.MFnData.kNurbsCurve)
        tAttr.setWritable(False)
        tAttr.setStorable(False)
        cls.addAttribute(cls.out_curve)

        # 创建 out_surface 属性
        tAttr = om.MFnTypedAttribute()
        cls.out_surface = tAttr.create("outSurface", "os", om.MFnData.kNurbsSurface)
        tAttr.setWritable(False)
        tAttr.setStorable(False)
        cls.addAttribute(cls.out_surface)

        cls.attributeAffects(cls.in_curve, cls.out_curve)
        cls.attributeAffects(cls.start_point, cls.out_curve)
        cls.attributeAffects(cls.keep_point, cls.out_curve)
        cls.attributeAffects(cls.link_order, cls.out_curve)
        cls.attributeAffects(cls.reverse_curve, cls.out_curve)


        cls.attributeAffects(cls.in_curve, cls.out_surface)
        cls.attributeAffects(cls.start_point, cls.out_surface)
        cls.attributeAffects(cls.keep_point, cls.out_surface)
        cls.attributeAffects(cls.link_order, cls.out_surface)
        cls.attributeAffects(cls.reverse_curve, cls.out_surface)

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
    except:
        sys.stderr.write("Failed to register node\n")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    try:
        plugin.deregisterNode(SplineLinkingAndCroppingDisplay.Uv_id)
    except:
        sys.stderr.write("Failed to deregister node\n")