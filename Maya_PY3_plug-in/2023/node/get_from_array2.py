# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class GetFromArray(ompx.MPxDeformerNode):
    def __init__(self):
        super(GetFromArray, self).__init__()

    node_name = "GetFromArray"
    n = 39  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    def deform(self, data_block, geoIter, matrix, multiIndex):
        # 获取 select 属性值
        select_handle = data_block.inputValue(self.select)
        select_value = select_handle.asInt()
        print(
            select_value
        )


    @classmethod
    def nodeInitializer(cls):
        # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        cls.select = nAttr.create("select", "sel", om.MFnNumericData.kInt, 1)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setMin(0)
        cls.addAttribute(cls.select)

        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.out_data = tAttr.create("out_data", "outdata", om.MFnData.kAny)  # 改为曲面
        tAttr.setConnectable(True)
        tAttr.setWritable(True)  # 确保可写
        cls.addAttribute(cls.out_data)

        cls.attributeAffects(cls.select, cls.out_data)
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(GetFromArray())


# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            GetFromArray.node_name,
            GetFromArray.Uv_id,
            GetFromArray.nodeCreator,        # 创建节点的函数
            GetFromArray.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {GetFromArray.node_name}")

    cmds.makePaintable(GetFromArray.node_name, "weights", attrType="multiFloat", shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    # cmds.makePaintable(GetFromArray.node_name, "weights", remove=True)
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(GetFromArray.Uv_id)