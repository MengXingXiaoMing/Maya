# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import random



# 2. 节点类定义(变形器)
class SineNode(ompx.MPxDeformerNode):
    # 1. 定义节点名称与ID（ID需全局唯一）
    kPluginNodeTypeName = "spSineNode"
    sineNodeId = om.MTypeId(0x4004)  # 0x8700 是示例ID

    MAX_ANGLE = 0.5 *3.1415926
    def __init__(self):
        super(SineNode, self).__init__()

    def deform(self, data_block, geo_iter, world_matrix, multi_index):
        envelope = data_block.inputValue(self.envelope).asFloat()  # 封套权重（0~1）
        if envelope == 0:
            return

        max_distance = data_block.inputValue(self.max_distance).asFloat()  # 最大影响距离
        if max_distance == 0:
            return

        target_postance = data_block.inputValue(self.target_position).asFloatVector()  # 目标点（世界坐标）
        target_postance = om.MPoint(target_postance)*world_matrix.inverse()  ## 世界坐标 → 局部坐标
        target_postance = om.MFloatVector(target_postance)  ## 转为向量类型


        input_handle = data_block.outputArrayValue(self.input)  # 控制柄
        input_handle.jumpToElement(multi_index)
        input_element_handle = input_handle.outputValue()

        input_geom = input_element_handle.child(self.inputGeom).asMesh()
        mesh_fn = om.MFnMesh(input_geom)

        normals = om.MFloatVectorArray()
        mesh_fn.getVertexNormals(False, normals)

        # inverse_world_matrix = world_matrix.inverse()  #

        geo_iter.reset()
        while not geo_iter.isDone():
            pt_local = geo_iter.position()  # 当前顶点（局部坐标）
            # pt_world = pt_local * world_matrix

            # target_vector = target_postance - om.MFloatVector(pt_world)
            target_vector = target_postance - om.MFloatVector(pt_local)  # 目标方向向量

            distance = target_vector.length()  # 到目标点的距离
            if distance <= max_distance:  # 在影响范围内
                # normal = om.MVector(normals[geo_iter.index()]) * world_matrix
                # normal = om.MFloatVector(normal)
                normal = om.MFloatVector(normals[geo_iter.index()])  # 顶点法线（局部坐标）

                angle = normal.angle(target_vector)  # 法线与目标向量的夹角
                if angle <= self.MAX_ANGLE: # 角度小于阈值（如90°）
                    offset = target_vector * ((max_distance - distance)/max_distance)  # 计算偏移量

                    # new_pt_world = pt_world + om.MVector(offset)
                    # new_pt_local = new_pt_world * inverse_world_matrix

                    # geo_iter.setPosition(new_pt_local)
                    geo_iter.setPosition(pt_local + om.MVector(offset))  # 应用偏移



            geo_iter.next()








    @classmethod
    def nodeInitializer(cls):
        numeric_attr = om.MFnNumericAttribute()

        cls.max_distance = numeric_attr.create("maximumDistance", "maxDist", om.MFnNumericData.kFloat, 1.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        # numeric_attr.setMax(1.0)

        cls.target_position = numeric_attr.createPoint("targetPosition", "targetPos")
        numeric_attr.setKeyable(True)

        cls.addAttribute(cls.max_distance)
        cls.addAttribute(cls.target_position)

        output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.max_distance, output_geom)
        cls.attributeAffects(cls.target_position, output_geom)







    # 节点创建器
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(SineNode())

# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            SineNode.kPluginNodeTypeName,
            SineNode.sineNodeId,
            SineNode.nodeCreator,        # 创建节点的函数
            SineNode.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {SineNode.kPluginNodeTypeName}")

    cmds.makePaintable(SineNode.kPluginNodeTypeName,"weights",attrType="multiFloat",shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    cmds.makePaintable(SineNode.kPluginNodeTypeName,"weights",remove=True)
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(SineNode.sineNodeId)
