# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import random
import numpy as np
from scipy.interpolate import CubicSpline

# 2. 节点类定义(变形器)
class PointPositionAssociationBS(ompx.MPxDeformerNode):
    def __init__(self):
        super(BsChangeNormal, self).__init__()

    node_name = "BsChangeNormal"
    n = 6  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    def deform(self, data_block, geo_iter, matrix, multi_index):
        envelope = data_block.inputValue(self.envelope).asFloat()
        if envelope == 0:
            return

        blend_weight = data_block.inputValue(self.bend_weight).asFloat()
        if blend_weight == 0:
            return

        soure_mesh = data_block.inputValue(self.soureMesh).asMesh()
        if soure_mesh.isNull():
            return

        target_mesh = data_block.inputValue(self.targetMesh).asMesh()
        if target_mesh.isNull():
            return

        global_weight = blend_weight * envelope  # 获取基本权重
        # 获取当前网格的 MFnMesh 对象
        input_handle = data_block.outputArrayValue(self.input)
        input_handle.jumpToElement(multi_index)
        input_element_handle = input_handle.outputValue()
        input_geom = input_element_handle.child(self.inputGeom).asMesh()

        mesh_fn = om.MFnMesh(input_geom)  # 创建 MFnMesh 对象

        # imput_geom = input_element_handle.child(self.inputGeom).asMesh()
        target_mesh_fn = om.MFnMesh(target_mesh)  # 获取模型

        target_points = om.MPointArray()
        target_mesh_fn.getPoints(target_points)  # 获取点

        new_normals = om.MFloatVectorArray()  # 空法线列表
        target_mesh_fn.getNormals(new_normals)  # 获取法线
        target_normals = om.MFloatVectorArray()
        target_mesh_fn.getNormals(target_normals)  # 获取法线

        geo_iter.reset()
        while not geo_iter.isDone():
            source_weight = self.weightValue(data_block, multi_index, geo_iter.index())  # 获取绘制的权重

            source_pt = geo_iter.position()
            target_pt = target_points[geo_iter.index()]  # 获取点
            final_pt = source_pt + ((target_pt - source_pt) * global_weight * source_weight)
            geo_iter.setPosition(final_pt)
            ###################
            source_normal = om.MFloatVector(geo_iter.normal())
            target_normal = target_normals[geo_iter.index()]  # 获取法线
            target_normal = om.MFloatVector(target_normal)
            # print(source_normal)
            # print(target_normal)
            # 获取法线数组 (对象空间)
            final_normal = source_normal + ((target_normal - source_normal) * global_weight * source_weight)
            print(final_normal)
            #
            # final_normal.normalize()  # 归一化为单位向量
            # 将计算好的新法线存储到数组中
            new_normals.set(final_normal, geo_iter.index())
            #
            # geo_iter.setNormal(final_normal)

            geo_iter.next()
        mesh_fn.setNormals(new_normals, om.MSpace.kObject)

    @classmethod
    def nodeInitializer(cls):
        # # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        cls.bend_weight = nAttr.create("bendWeight", "inValue", om.MFnNumericData.kFloat, 0.0)  # 改用inValue避免冲突
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值

        # 创建输入Mesh属性
        nAttr = om.MFnTypedAttribute()
        cls.soureMesh = nAttr.create("soureMesh", "sMesh", om.MFnData.kMesh)
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值

        # 创建输入Mesh属性
        nAttr = om.MFnTypedAttribute()
        cls.targetMesh = nAttr.create("targetMesh", "tMesh", om.MFnData.kMesh)
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值

        # 创建输出Mesh属性
        cls.outMesh = nAttr.create("outMesh", "om", om.MFnData.kMesh)
        nAttr.setStorable(False)  # 动态计算，不存储
        nAttr.setWritable(False)  # 禁止用户直接修改

        # 添加属性并建立依赖
        cls.addAttribute(cls.bend_weight)
        cls.addAttribute(cls.soureMesh)
        cls.addAttribute(cls.targetMesh)
        cls.addAttribute(cls.outMesh)
        # cls.attributeAffects(cls.inMesh, cls.outMesh)  # 输入变化触发输出更新[5,9](@ref)
        output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.bend_weight, output_geom)  # 输入变化触发输出更新[5,9](@ref)
        cls.attributeAffects(cls.soureMesh, output_geom)  # 输入变化触发输出更新[5,9](@ref)
        cls.attributeAffects(cls.targetMesh, output_geom)  # 输入变化触发输出更新[5,9](@ref)


    # 节点创建器
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(BsChangeNormal())

# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            BsChangeNormal.node_name,
            BsChangeNormal.Uv_id,
            BsChangeNormal.nodeCreator,        # 创建节点的函数
            BsChangeNormal.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {BsChangeNormal.node_name}")

    cmds.makePaintable(BsChangeNormal.node_name, "weights", attrType="multiFloat",shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    # cmds.makePaintable(BsChangeNormal.node_name, "weights", remove=True)
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(BsChangeNormal.Uv_id)