# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class SplineLinkingAndCroppingDisplay(ompx.MPxNode):
    node_name = "SplineLinkingAndCroppingDisplay"
    Uv_id = om.MTypeId(0x00141480 + 22)

    def __init__(self):
        super(SplineLinkingAndCroppingDisplay, self).__init__()

    def compute(self, plug, data_block):
        # 仅在输出插件被请求时计算
        if plug != self.out_curve:
            return
        start_point_handle = data_block.inputValue(self.start_point)
        start_point_value = start_point_handle.asInt()

        keep_point_handle = data_block.inputValue(self.keep_point)
        keep_point_value = keep_point_handle.asInt()

        end_point_value = start_point_value + keep_point_value

        # 获取输入数组句柄
        in_curve_handle = data_block.inputArrayValue(self.in_curve)
        element_count = in_curve_handle.elementCount()

        if element_count == 0:
            return

        combined_cvs = om.MPointArray()
        first_degree = 3
        first_form = om.MFnNurbsCurve.kOpen
        is_rational = False
        found_curves_count = 0

        # 1. 提取所有输入曲线的数据
        for i in range(element_count):
            in_curve_handle.jumpToElement(i)
            input_data_obj = in_curve_handle.inputValue().data()

            # 检查数据是否有效
            if input_data_obj.hasFn(om.MFn.kNurbsCurve):
                curve_fn = om.MFnNurbsCurve(input_data_obj)

                current_cvs = om.MPointArray()
                # 在节点内部通常使用 kObject 空间，因为坐标是相对于输入几何体的
                curve_fn.getCVs(current_cvs, om.MSpace.kObject)

                if found_curves_count == 0:
                    first_degree = curve_fn.degree()
                    first_form = curve_fn.form()

                for k in range(current_cvs.length()):
                    combined_cvs.append(current_cvs[k])
                    if current_cvs[k].w != 1.0:
                        is_rational = True

                found_curves_count += 1

        if found_curves_count < 1:
            return

        # 2. 计算节点矢量 (Knots)
        num_cvs = combined_cvs.length()
        if start_point_value >= num_cvs-2:
            start_point_value = num_cvs-2
        if end_point_value >= num_cvs:
            end_point_value = num_cvs
        cropped_cvs = om.MPointArray()
        for i in range(start_point_value, end_point_value):
            cropped_cvs.append(combined_cvs[i])
        num_knots = end_point_value-start_point_value + first_degree - 1
        new_knots = om.MDoubleArray()

        counter = 0.0
        for i in range(num_knots):
            if i < first_degree:
                new_knots.append(0.0)
            elif i <= (num_cvs - 1):
                counter += 1.0
                new_knots.append(counter)
            else:
                new_knots.append(counter + 1.0)

        # 创建一个数据容器对象
        curve_data_fn = om.MFnNurbsCurveData()
        output_data_obj = curve_data_fn.create()

        # 使用该数据容器作为 parent 来创建曲线
        new_curve_fn = om.MFnNurbsCurve()
        new_curve_fn.create(
            cropped_cvs,
            new_knots,
            first_degree,
            first_form,
            is_rational,
            False,
            output_data_obj  # 将生成的几何体放入数据容器
        )

        # 4. 设置输出
        output_handle = data_block.outputValue(self.out_curve)
        output_handle.setMObject(output_data_obj)  # 传递的是数据对象

        data_block.setClean(plug)

    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
        cls.start_point = nAttr.create("startPoint", "sp", om.MFnNumericData.kInt, 0)
        nAttr.setMin(0)
        nAttr.setStorable(True)
        cls.addAttribute(cls.start_point)

        cls.keep_point = nAttr.create("keepPoint", "kp", om.MFnNumericData.kInt, 10)
        nAttr.setStorable(True)
        nAttr.setMin(0)
        cls.addAttribute(cls.keep_point)

        tAttr = om.MFnTypedAttribute()
        # 输入：NurbsCurve 类型数据
        cls.in_curve = tAttr.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)
        cls.addAttribute(cls.in_curve)

        # 输出：NurbsCurve 类型数据
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
    plugin.registerNode(
        SplineLinkingAndCroppingDisplay.node_name,
        SplineLinkingAndCroppingDisplay.Uv_id,
        SplineLinkingAndCroppingDisplay.nodeCreator,
        SplineLinkingAndCroppingDisplay.nodeInitializer,
    )


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(SplineLinkingAndCroppingDisplay.Uv_id)