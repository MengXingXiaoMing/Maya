# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import math


class CustomWireDeformer(ompx.MPxDeformerNode):
    """自定义线变形器节点"""

    # 节点属性
    kPluginNodeId = om.MTypeId(0x0456384)  # 唯一节点ID
    dropoff_distance = om.MObject()
    scale = om.MObject()
    envelope = om.MObject()

    def __init__(self):
        ompx.MPxDeformerNode.__init__(self)

    def deform(self, data_block, geom_iter, matrix, multi_index):
        """变形计算的核心方法"""

        # 获取输入属性值
        dropoff_handle = data_block.inputValue(self.dropoff_distance)
        dropoff_value = dropoff_handle.asDouble()

        scale_handle = data_block.inputValue(self.scale)
        scale_value = scale_handle.asFloat()

        envelope_handle = data_block.inputValue(self.envelope)
        envelope_value = envelope_handle.asFloat()

        if envelope_value == 0:
            return  # 封套为0时不进行变形

        # 获取曲线数据（这里需要连接曲线属性）
        # 实际实现中需要添加曲线属性连接和最近点计算逻辑

        # 遍历每个顶点进行计算
        while not geom_iter.isDone():
            if geom_iter.isDone():
                break

            # 获取顶点位置
            point = geom_iter.position()

            # 计算变形效果（示例：简单的Y轴位移）
            weight = self.weightValue(data_block, multi_index, geom_iter.index())

            # 应用变形逻辑
            displacement = om.MVector(0, math.sin(point.x * 0.5) * scale_value, 0)
            new_point = point + displacement * weight * envelope_value

            geom_iter.setPosition(new_point)
            geom_iter.next()

    @classmethod
    def creator(cls):
        return ompx.asMPxPtr(cls())

    @classmethod
    def initialize(cls):
        """初始化节点属性"""

        # 创建数值属性
        n_attr = om.MFnNumericAttribute()

        # 衰减距离属性
        cls.dropoff_distance = n_attr.create("dropoffDistance", "dd",
                                             om.MFnNumericData.kDouble, 10.0)
        n_attr.setKeyable(True)
        n_attr.setMin(0.0)
        n_attr.setMax(100.0)

        # 缩放属性
        cls.scale = n_attr.create("scale", "s",
                                  om.MFnNumericData.kFloat, 1.0)
        n_attr.setKeyable(True)
        n_attr.setMin(-10.0)
        n_attr.setMax(10.0)

        # 封套属性（所有变形器都有）[6](@ref)
        cls.envelope = n_attr.create("envelope", "env",
                                     om.MFnNumericData.kFloat, 1.0)
        n_attr.setKeyable(True)
        n_attr.setMin(0.0)
        n_attr.setMax(1.0)

        # 添加属性
        cls.addAttribute(cls.dropoff_distance)
        cls.addAttribute(cls.scale)
        cls.addAttribute(cls.envelope)

        # 建立属性关联
        output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.dropoff_distance, output_geom)
        cls.attributeAffects(cls.scale, output_geom)
        cls.attributeAffects(cls.envelope, output_geom)


def initializePlugin(mobject):
    """初始化插件"""
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.registerNode("customWireDeformer",
                             CustomWireDeformer.kPluginNodeId,
                             CustomWireDeformer.creator,
                             CustomWireDeformer.initialize,
                             ompx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError("Failed to register node")


def uninitializePlugin(mobject):
    """卸载插件"""
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(CustomWireDeformer.kPluginNodeId)
    except:
        raise RuntimeError("Failed to deregister node")