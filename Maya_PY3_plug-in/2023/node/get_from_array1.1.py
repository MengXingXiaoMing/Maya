# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class GetFromArray(ompx.MPxNode):
    def __init__(self):
        super(GetFromArray, self).__init__()

    node_name = "GetFromArray"
    n = 38  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    def compute(self, plug, data_block):
        # 只在输出属性需要计算时执行
        # if plug != GetFromArray.out_data:
        #     return

        # 获取 select 属性值
        select_handle = data_block.inputValue(self.select)
        select_value = select_handle.asInt()

        # 获取输入数组
        in_data_handle = data_block.inputArrayValue(self.in_data)

        # 计算实际索引 (确保在有效范围内)
        element_count = in_data_handle.elementCount()
        if element_count == 0:
            return

        # 限制索引在有效范围内
        if select_value >= element_count:
            select_value = element_count - 1

        # 跳转到指定索引
        in_data_handle.jumpToElement(select_value)

        # 获取该元素的数据
        input_handle = in_data_handle.inputValue()
        input_data = input_handle.data()

        # # 检查数据是否为空
        # if input_data.isNull():
        #     # 空数据，输出空
        #     output_handle = data_block.outputValue(GetFromArray.out_data)
        #     null_obj = om.MObject()  # 创建一个空的 MObject
        #     output_handle.setMObject(null_obj)
        #     data_block.setClean(plug)
        #     return

        # 设置输出数据
        try:
            output_handle = data_block.outputValue(self.out_data)
            output_handle.setMObject(input_data)
        except:
            return
        # 标记为已计算
        data_block.setClean(plug)

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
        cls.in_data = tAttr.create("in_data", "indata", om.MFnData.kAny)  # 改为曲面
        tAttr.setArray(True)
        tAttr.setConnectable(True)
        tAttr.setUsesArrayDataBuilder(True)  # 重要：启用数组数据构建器
        # tAttr.setIndexMatters(True)  # 确保索引重要
        cls.addAttribute(cls.in_data)

        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.out_data = tAttr.create("out_data", "outdata", om.MFnData.kAny)  # 改为曲面
        tAttr.setConnectable(True)
        tAttr.setWritable(True)  # 确保可写
        cls.addAttribute(cls.out_data)

        cls.attributeAffects(cls.in_data, cls.out_data)
        cls.attributeAffects(cls.select, cls.out_data)
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(GetFromArray())


# 插件注册保持不变
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            GetFromArray.node_name,
            GetFromArray.Uv_id,
            GetFromArray.nodeCreator,
            GetFromArray.nodeInitializer
        )
    except:
        sys.stderr.write(f"注册节点失败: {GetFromArray.node_name}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(GetFromArray.Uv_id)