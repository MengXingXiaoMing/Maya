# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys
import maya.mel as mel


class selfIK(ompx.MPxNode):
    def __init__(self):
        super(selfIK, self).__init__()

    node_name = "selfIK"
    Uv_id = om.MTypeId(0x00141480 + 206)  # 6

    def compute(self, plug, data_block):
        # print('实行了计算')
        pass

    @classmethod
    def nodeInitializer(cls):
        # 获取样条对象
        tAttr = om.MFnTypedAttribute()
        cls.inCurve = tAttr.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        cls.addAttribute(cls.inCurve)

        # 获取骨骼间距
        nAttr = om.MFnNumericAttribute()
        cls.radius = nAttr.create("radius", "ras", om.MFnNumericData.kfloat, 0)
        nAttr.setArray(True)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.radius)



        nAttr = om.MFnNumericAttribute()
        cls.select = nAttr.create("select", "sel", om.MFnNumericData.kInt, 0)
        nAttr.setArray(True)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.select)

        cls.commend_read_int = nAttr.create("commendReadInt", "cri", om.MFnNumericData.kInt, 0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setMin(0)
        cls.addAttribute(cls.commend_read_int)

        # 添加布尔属性 ifPy
        cls.if_py = nAttr.create("ifPy", "ifpy", om.MFnNumericData.kBoolean, 0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.if_py)

        # 添加布尔属性 ifShape
        cls.if_shape = nAttr.create("ifShape", "ifshape", om.MFnNumericData.kBoolean, 0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.if_shape)

        tAttr = om.MFnTypedAttribute()
        cls.text_input = tAttr.create("textInput", "txt", om.MFnData.kString)
        stringData = om.MFnStringData().create("")
        tAttr.setDefault(stringData)
        tAttr.setStorable(True)
        tAttr.setKeyable(True)
        tAttr.setWritable(True)
        tAttr.setReadable(True)
        cls.addAttribute(cls.text_input)

        tAttr = om.MFnTypedAttribute()
        cls.in_data = tAttr.create("in_data", "indata", om.MFnData.kAny)
        tAttr.setArray(True)
        tAttr.setConnectable(True)
        tAttr.setUsesArrayDataBuilder(True)
        tAttr.setKeyable(True)
        cls.addAttribute(cls.in_data)

        tAttr = om.MFnTypedAttribute()
        cls.out_data = tAttr.create("out_data", "outdata", om.MFnData.kAny)
        tAttr.setConnectable(True)
        tAttr.setWritable(True)
        cls.addAttribute(cls.out_data)

        cls.attributeAffects(cls.in_data, cls.out_data)
        cls.attributeAffects(cls.select, cls.out_data)
        cls.attributeAffects(cls.if_shape, cls.out_data)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(selfIK())


def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.1.0")

    try:
        plugin.registerNode(
            selfIK.node_name,
            selfIK.Uv_id,
            selfIK.nodeCreator,
            selfIK.nodeInitializer,
        )
        # 创建属性编辑器模板
        print(f"成功注册节点: {selfIK.node_name}")

    except Exception as e:
        sys.stderr.write(f"注册节点失败: {selfIK.node_name}, 错误: {str(e)}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(selfIK.Uv_id)