# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaAnim as omAnim
import sys
import maya.cmds as cmds
import datetime
import numpy as np
import time

# 基础皮肤集群类 - 实现简单的线性混合蒙皮变形器
class basicSkinCluster(ompx.MPxSkinCluster):
    node_name = "basicSkinCluster"
    n = 99  # 0-63

    # 使用 datetime 模块，得到浮点数形式的时间戳（秒）
    # current_datetime = datetime.datetime.now()
    # timestamp_by_datetime = int(current_datetime.timestamp() * 100000) - 176284300000000
    # print(f"当前时间戳（秒，datetime.timestamp()）: {timestamp_by_datetime}")
    # n = timestamp_by_datetime

    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    # 更改节点ID避免冲突，确保唯一性
    kPluginNodeId = om.MTypeId(target_id)

    # 定义属性
    aMatrix = om.MObject()
    aBindPreMatrix = om.MObject()
    aWeightList = om.MObject()
    aWeights = om.MObject()

    break_data = []
    break_weight = []
    # wrapSurfaces = []
    baseSurfaces = []
    def __init__(self):
        ompx.MPxSkinCluster.__init__(self)

    def deform(self, data_block, geom_iter, local_to_world_matrix, geometry_index):
        """修正后的变形函数"""
        print('皮肤节点开始变形')

        # 获取输出几何体
        output_geom_handle = data_block.outputValue(self.outputGeom)
        output_geom_obj = output_geom_handle.asMesh()

        # 使用MFnMesh
        mesh_fn = om.MFnMesh(output_geom_obj)
        points = om.MPointArray()


        # 获取影响变换
        transforms_handle = data_block.inputArrayValue(self.matrix)
        num_transforms = transforms_handle.elementCount()

        if num_transforms == 0:
            return

        # 获取所有变换矩阵
        transforms = []
        for i in range(num_transforms):
            transforms_handle.jumpToArrayElement(i)
            matrix_data_handle = transforms_handle.inputValue()
            matrix_data = om.MFnMatrixData(matrix_data_handle.data())
            transforms.append(matrix_data.matrix())

        # 应用绑定姿势矩阵
        bind_handle = data_block.inputArrayValue(self.bindPreMatrix)
        # if bind_handle.elementCount() > 0:
        transforms1 = []
        for i in range(num_transforms):
            bind_handle.jumpToArrayElement(i)
            bind_matrix_data_handle = bind_handle.inputValue()
            bind_matrix_data = om.MFnMatrixData(bind_matrix_data_handle.data())
            # transforms1.append(transforms[i] * bind_matrix_data.matrix().inverse())
            transforms1.append(transforms[i] * bind_matrix_data.matrix())

        # 获取权重列表
        weight_list_handle = data_block.inputArrayValue(self.weightList)
        if weight_list_handle.elementCount() == 0:
            return
        new_positions = []
        j = 0
        while not geom_iter.isDone():
            # 获取当前顶点位置
            pt = geom_iter.position()
            skinned = om.MPoint(0, 0, 0, 1.0)  # 初始化为零向量，w分量为1

            # 获取当前顶点的权重
            weight_list_handle.jumpToElement(j)
            pointWeightsHandle = weight_list_handle.inputValue()
            weightsHandle = pointWeightsHandle.child(self.weights)
            weightsArrayHandle = om.MArrayDataHandle(weightsHandle)

            # 应用皮肤变形
            total_weight = False
            for i in range(num_transforms):
                try:
                    weightsArrayHandle.jumpToElement(i)
                    weight_value = weightsArrayHandle.inputValue().asDouble()
                except:
                    weight_value = 0

                if weight_value > 0.0001:  # 只处理有影响的权重
                    transformed_point = pt * transforms1[i]
                    skinned += om.MPoint(transformed_point) * weight_value
                    if weight_value > 0:
                        total_weight = True
            j += 1

            # 归一化处理
            if total_weight == True:
                skinned = skinned * (1.0 / total_weight)
            else:
                skinned = pt  # 如果没有权重影响，保持原位置
            # 设置最终位置
            # geom_iter.setPosition(skinned)
            new_positions.append(skinned)
            geom_iter.next()
        # 一次性设置所有顶点位置
        for i, pos in enumerate(new_positions):
            points.append(pos)
        mesh_fn.setPoints(points)
        # 为每个顶点进行变形

    # 节点创建函数
    @classmethod
    def creator(self):
        return ompx.asMPxPtr(basicSkinCluster())

    # 节点初始化函数 - 必须正确定义属性
    @classmethod
    def initialize(cls):
        # 创建烘焙属性
        nAttr = om.MFnNumericAttribute()
        cls.isBreak = nAttr.create("isBreak", "ib", om.MFnNumericData.kInt, 1)
        nAttr.setMin(0)
        nAttr.setMax(1)
        nAttr.setStorable(True)  # 关键：允许属性被存储
        nAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        nAttr.setKeyable(True)
        cls.addAttribute(cls.isBreak)

        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.isBreak, outputGeom)


# 插件初始化函数
def initializePlugin(obj):
    plugin = ompx.MFnPlugin(obj, "KangmingZhan", "1.0", "Any")

    try:
        print("正在尝试注册basicSkinCluster节点")

        result = plugin.registerNode(
            basicSkinCluster.node_name,
            basicSkinCluster.kPluginNodeId,
            basicSkinCluster.creator,
            basicSkinCluster.initialize,
            ompx.MPxNode.kSkinCluster
        )

        print("basicSkinCluster节点注册成功！")
        return result

    except Exception as e:
        error_msg = f"注册basicSkinCluster节点失败: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        om.MGlobal.displayError(error_msg)


# 插件卸载函数
def uninitializePlugin(obj):
    plugin = ompx.MFnPlugin(obj)

    try:
        plugin.deregisterNode(basicSkinCluster.kPluginNodeId)
        print("basicSkinCluster节点注销成功！")
    except Exception as e:
        error_msg = f"注销basicSkinCluster节点失败: {str(e)}"
        print(error_msg)
        om.MGlobal.displayError(error_msg)