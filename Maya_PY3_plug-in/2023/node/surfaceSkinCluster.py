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
class surfaceSkinCluster(ompx.MPxSkinCluster):
    node_name = "surfaceSkinCluster"
    n = 4  # 0-63

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

    def deform(self, dataBlock, geomIterator, localToWorldMatrix, multiIndex):
        # 获取envelope属性值
        envelope_handle = dataBlock.inputValue(self.envelope)
        envelope_value = envelope_handle.asFloat()
        if envelope_value == 0:
            return

        isBreak = dataBlock.inputValue(self.isBreak).asInt()
        if isBreak == 0:
            self.break_data = []

        isBreakWeight = dataBlock.inputValue(self.isBreakWeight).asInt()
        if isBreakWeight == 0:
            self.break_weight = []
        # 获取当前节点的MObject
        thisNode = self.thisMObject()
        # 创建MFnDependencyNode函数集
        depFn = om.MFnDependencyNode(thisNode)
        # 找到 matrix 属性
        matrixPlug = depFn.findPlug("matrix", False)
        # 获取所有存在的索引
        indexArray = om.MIntArray()
        matrixPlug.getExistingArrayAttributeIndices(indexArray)

        # 获取权重列表数据
        weightListHandle = dataBlock.inputArrayValue(self.weightList)
        if weightListHandle.elementCount() == 0:
            # 没有权重数据 - 无需进行任何操作
            return
        # start_time = time.time()
        # 获取 wrapSurface 属性值
        wrapSurfaceArrayHandle = dataBlock.inputArrayValue(self.wrapSurface)
        wrapSurfaces = []
        for i in indexArray:
            wrapSurfaceArrayHandle.jumpToElement(i)

            dataHandle = wrapSurfaceArrayHandle.inputValue()
            surfaceData = dataHandle.data()

            if not surfaceData.isNull():
                surfaceFn = om.MFnNurbsSurface(surfaceData)
                wrapSurfaces.append(surfaceFn)
            else:
                wrapSurfaces.append(None)
        # end_time = time.time()
        # print('获取变形曲面数据运行耗时：', end_time - start_time, '秒')
        # ----------------------------------烘焙uv,基础点，点距离------------------------------------
        # start_time = time.time()
        if not self.break_data:

            # 获取 baseSurface 属性值
            baseSurfaceArrayHandle = dataBlock.inputArrayValue(self.baseSurface)
            baseSurfaces = []
            for i in indexArray:
                baseSurfaceArrayHandle.jumpToElement(i)
                dataHandle = baseSurfaceArrayHandle.inputValue()
                surfaceData = dataHandle.data()
                if not surfaceData.isNull():
                    surfaceFn = om.MFnNurbsSurface(surfaceData)
                    baseSurfaces.append(surfaceFn)
                else:
                    baseSurfaces.append(None)
            self.baseSurfaces = baseSurfaces
            # print('开始烘焙数据')
            base_data = []
            geomIterator.reset()  # 重置迭代器到起始位置
            # 获取基础状态的模型点跟随的曲面点uv以及uv点世界坐标
            while not geomIterator.isDone():
                pt = geomIterator.position()
                # print(pt.x, pt.y, pt.z)
                # print(baseSurfaces)
                index, all_uv, all_point, all_distance = self.get_surface_weight(pt, baseSurfaces)
                # print([uv, point, surfaces])
                base_data.append((index, all_uv, all_point, all_distance))
                geomIterator.next()
            geomIterator.reset()  # 重置迭代器到起始位置
            self.break_data = base_data
        # end_time = time.time()
        # print('获取或生成烘焙数据运行耗时：', end_time - start_time, '秒')
        #----------------------------------烘焙权重数据------------------------------------
        # start_time = time.time()
        i = 0
        if not self.break_weight:
            while not geomIterator.isDone():
                # offset = om.MVector()
                # 跳转到当前点的权重数据
                weightListHandle.jumpToElement(i)
                pointWeightsHandle = weightListHandle.inputValue()
                weightsHandle = pointWeightsHandle.child(self.weights)
                weightsArrayHandle = om.MArrayDataHandle(weightsHandle)
                ls_list =[]
                ls_list2 = []
                # 计算蒙皮变形效果
                for j in range(len(self.baseSurfaces)):
                    # 检查是否能成功跳转到指定权重要素
                    try:
                        weightsArrayHandle.jumpToElement(j)
                        weightValue = weightsArrayHandle.inputValue().asDouble()
                    except:
                        weightValue = 0
                    if weightValue > 0.0001:  # 忽略极小权重提高性能
                        ls_list.append(weightValue)
                        ls_list2.append(j)
                self.break_weight.append((ls_list, ls_list2))
                i += 1
                # 安全地前进权重列表句柄
                if i < weightListHandle.elementCount():
                    try:
                        weightListHandle.next()
                    except:
                        weightListHandle.jumpToElement(i)
                geomIterator.next()
        geomIterator.reset()  # 重置迭代器到起始位置
        # end_time = time.time()
        # print('获取或生成烘焙权重数据运行耗时：', end_time - start_time, '秒')

        # ----------------------------------计算曲面变形------------------------------------
        # start_time = time.time()
        i = 0
        new_point = om.MPoint()
        while not geomIterator.isDone():
            # 跳转到当前点的权重数据
            data = self.break_data[i]
            data_1 = data[1]
            data_2 = data[2]
            skinned = geomIterator.position()
            weight_data = self.break_weight[i]
            # 计算蒙皮变形效果
            # 将长度计算移出内层循环
            loop_count = len(weight_data[1])
            for j in range(loop_count):
                num = weight_data[1][j]
                # 检查是否能成功跳转到指定权重要素
                weightValue = weight_data[0][j]
                # 初始化变形后的点位置
                base_point = data_2[num]
                # 获取指定UV参数处的点坐标
                u, v = data_1[num]
                wrapSurfaces[num].getPointAtParam(u, v, new_point, om.MSpace.kWorld)
                # 计算偏移量
                tempPoint = new_point - base_point
                skinned += om.MVector(tempPoint * weightValue)
            i += 1
            # 设置点的最终变形位置
            geomIterator.setPosition(skinned)
            geomIterator.next()
        # geomIterator.reset()
        # end_time = time.time()
        # print('计算偏移耗时：', end_time - start_time, '秒')

    def get_surface_weight(self, position, surfaceFns):
        """计算顶点到曲面的权重（曲面版本）"""
        all_uv = []  # 存储UV参数
        all_point = []  # 存储曲面上最近的点
        all_distance = []

        util_u = om.MScriptUtil()
        util_v = om.MScriptUtil()
        paramPtr_u = util_u.asDoublePtr()
        paramPtr_v = util_v.asDoublePtr()
        for surfaceFn in surfaceFns:
            # print(surfaceFn)
            # 计算到曲面的最近点 - 曲面使用closestPoint方法
            closestPoint = surfaceFn.closestPoint(position, paramPtr_u, paramPtr_v, 0.001, om.MSpace.kWorld)

            u = util_u.getDouble(paramPtr_u)
            v = util_v.getDouble(paramPtr_v)
            all_uv.append((u, v))
            all_point.append(closestPoint)

            distance = position.distanceTo(closestPoint)
            all_distance.append(distance)

        min_index = np.argmin(all_distance)  # 直接返回最小值的索引

        return min_index, tuple(all_uv), tuple(all_point), tuple(all_distance)

    # 节点创建函数
    @classmethod
    def creator(self):
        return ompx.asMPxPtr(surfaceSkinCluster())

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

        # 创建烘焙权重
        nAttr = om.MFnNumericAttribute()
        cls.isBreakWeight = nAttr.create("isBreakWeight", "ibw", om.MFnNumericData.kInt, 1)
        nAttr.setMin(0)
        nAttr.setMax(1)
        nAttr.setStorable(True)  # 关键：允许属性被存储
        nAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        nAttr.setKeyable(True)
        cls.addAttribute(cls.isBreakWeight)

        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.wrapSurface = tAttr.create("wrapSurface", "wsu", om.MFnData.kNurbsSurface)  # 改为曲面
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setConnectable(True)
        tAttr.setKeyable(True)
        cls.addAttribute(cls.wrapSurface)

        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.baseSurface = tAttr.create("baseSurface", "bsu", om.MFnData.kNurbsSurface)  # 改为曲面
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setConnectable(True)
        tAttr.setKeyable(True)
        cls.addAttribute(cls.baseSurface)

        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.isBreak, outputGeom)
        cls.attributeAffects(cls.isBreakWeight, outputGeom)
        cls.attributeAffects(cls.wrapSurface, outputGeom)
        cls.attributeAffects(cls.baseSurface, outputGeom)

# 插件初始化函数
def initializePlugin(obj):
    plugin = ompx.MFnPlugin(obj, "KangmingZhan", "1.0", "Any")

    try:
        result = plugin.registerNode(
            surfaceSkinCluster.node_name,
            surfaceSkinCluster.kPluginNodeId,
            surfaceSkinCluster.creator,
            surfaceSkinCluster.initialize,
            ompx.MPxNode.kSkinCluster
        )

        print("surfaceSkinCluster节点注册成功！")
        return result

    except Exception as e:
        error_msg = f"注册surfaceSkinCluster节点失败: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        om.MGlobal.displayError(error_msg)


# 插件卸载函数
def uninitializePlugin(obj):
    plugin = ompx.MFnPlugin(obj)

    try:
        plugin.deregisterNode(surfaceSkinCluster.kPluginNodeId)
        print("surfaceSkinCluster节点注销成功！")
    except Exception as e:
        error_msg = f"注销surfaceSkinCluster节点失败: {str(e)}"
        print(error_msg)
        om.MGlobal.displayError(error_msg)