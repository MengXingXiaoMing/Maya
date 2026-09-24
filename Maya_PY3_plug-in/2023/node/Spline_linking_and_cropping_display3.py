# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class SplineLinkingAndCroppingDisplay(ompx.MPxNode):
    node_name = "SplineLinkingAndCroppingDisplay"
    Uv_id = om.MTypeId(0x00141480 + 31)  # 更新ID防止冲突

    def __init__(self):
        super(SplineLinkingAndCroppingDisplay, self).__init__()

    def compute(self, plug, data_block):
        if plug != self.out_curve:
            return

        # 1. 获取基础截取参数
        start_point_value = data_block.inputValue(self.start_point).asInt()
        keep_point_value = data_block.inputValue(self.keep_point).asInt()

        in_curve_handle = data_block.inputArrayValue(self.in_curve)
        element_count = in_curve_handle.elementCount()

        if element_count == 0:
            return

        combined_cvs = om.MPointArray()
        global_knots = om.MDoubleArray()

        first_degree = 3
        first_form = om.MFnNurbsCurve.kOpen
        is_rational = False
        found_curves_count = 0
        knot_offset = 0.0

        # 2. 遍历并拼接原始数据
        for i in range(element_count):
            in_curve_handle.jumpToElement(i)
            input_data_obj = in_curve_handle.inputValue().data()

            if input_data_obj.hasFn(om.MFn.kNurbsCurve):
                curve_fn = om.MFnNurbsCurve(input_data_obj)

                # 提取 CVs
                current_cvs = om.MPointArray()
                curve_fn.getCVs(current_cvs, om.MSpace.kWorld)

                # 提取原始 Knots
                current_knots = om.MDoubleArray()
                curve_fn.getKnots(current_knots)

                if found_curves_count == 0:
                    first_degree = curve_fn.degree()
                    first_form = curve_fn.form()
                    # 第一条线：保留所有 Knot
                    for k in range(current_knots.length()):
                        global_knots.append(current_knots[k])
                else:
                    # 后续样条：为了修复连接处，跳过开头的 (degree-1) 个重复节点
                    # 这样连接处的节点多重度就不会超过 degree
                    last_knot_in_global = global_knots[global_knots.length() - 1]

                    # 移除当前全局序列末尾多余的重复节点（保留一个作为衔接）
                    for _ in range(first_degree - 1):
                        if global_knots.length() > 0:
                            global_knots.remove(global_knots.length() - 1)

                    # 获取新样条的起始偏移（使其从上一条线的结尾开始）
                    start_knot_val = current_knots[0]

                    # 拼接新样条的节点，跳过开头的 (degree-1) 个
                    for k in range(first_degree - 1, current_knots.length()):
                        normalized_knot = current_knots[k] - start_knot_val
                        global_knots.append(normalized_knot + last_knot_in_global)

                # 合并 CVs
                for k in range(current_cvs.length()):
                    combined_cvs.append(current_cvs[k])
                    if current_cvs[k].w != 1.0:
                        is_rational = True

                found_curves_count += 1

        if found_curves_count < 1:
            return

        # 3. 处理截取逻辑
        num_total_cvs = combined_cvs.length()
        if start_point_value >= num_total_cvs - 1:
            start_point_value = max(0, num_total_cvs - 2)

        actual_end = start_point_value + keep_point_value
        if actual_end > num_total_cvs:
            actual_end = num_total_cvs

        cropped_cvs = om.MPointArray()
        for i in range(start_point_value, actual_end):
            cropped_cvs.append(combined_cvs[i])

        # 4. 截取对应的 Knot 序列
        # 数量公式：N_cvs + Degree - 1
        num_final_cvs = cropped_cvs.length()
        num_needed_knots = num_final_cvs + first_degree - 1
        final_knots = om.MDoubleArray()

        # 从全局节点序列中根据 CV 偏移提取
        base_knot_idx = start_point_value
        if base_knot_idx + num_needed_knots <= global_knots.length():
            knot_offset_val = global_knots[base_knot_idx]
            for i in range(num_needed_knots):
                final_knots.append(global_knots[i + base_knot_idx] - knot_offset_val)
        else:
            # 如果索引溢出（极端情况），回退到均匀节点生成以防崩溃
            for i in range(num_needed_knots):
                if i < first_degree:
                    final_knots.append(0.0)
                elif i <= (num_final_cvs - 1):
                    final_knots.append(float(i - first_degree + 1))
                else:
                    final_knots.append(float(num_final_cvs - first_degree))

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
        data_block.setClean(plug)

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
        nAttr.setArray(True)
        nAttr.setStorable(True)
        cls.addAttribute(cls.link_order)

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

        cls.attributeAffects(cls.in_curve, cls.out_curve)
        cls.attributeAffects(cls.start_point, cls.out_curve)
        cls.attributeAffects(cls.keep_point, cls.out_curve)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(SplineLinkingAndCroppingDisplay())


def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(SplineLinkingAndCroppingDisplay.node_name, SplineLinkingAndCroppingDisplay.Uv_id,
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