# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaAnim as omAnim
import sys
import maya.cmds as cmds
import datetime

# 基础皮肤集群类 - 实现简单的线性混合蒙皮变形器
class surfaceSkinCluster(ompx.MPxSkinCluster):
    node_name = "surfaceSkinCluster"
    # n = 4  # 0-63

    # 使用 datetime 模块，得到浮点数形式的时间戳（秒）
    current_datetime = datetime.datetime.now()
    timestamp_by_datetime = int(current_datetime.timestamp() * 100000) - 176280000000000
    print(f"当前时间戳（秒，datetime.timestamp()）: {timestamp_by_datetime}")
    n = timestamp_by_datetime

    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    # 更改节点ID避免冲突，确保唯一性
    kPluginNodeId = om.MTypeId(target_id)

    # 定义属性
    aMatrix = om.MObject()
    aBindPreMatrix = om.MObject()
    aWeightList = om.MObject()
    aWeights = om.MObject()

    def __init__(self):
        ompx.MPxSkinCluster.__init__(self)

    def deform(self, dataBlock, geomIterator, localToWorldMatrix, multiIndex):
        """
        核心变形方法。对每个顶点应用骨骼变换和权重，计算最终位置。

        参数:
            dataBlock: 节点数据块，包含所有输入属性值
            geomIterator: 几何体顶点迭代器，用于遍历和修改顶点位置
            localToWorldMatrix: 局部空间到世界空间的变换矩阵
            multiIndex: 几何体索引（用于处理多个输入几何体的情况）

        返回: 无返回值。变形结果通过 geomIterator.setPosition() 设置。
        """
        # 获取当前节点的MObject
        thisNode = self.thisMObject()

        # 创建MFnDependencyNode函数集
        depFn = om.MFnDependencyNode(thisNode)

        # 找到 matrix 属性
        matrixPlug = depFn.findPlug("matrix", False)

        # 获取所有存在的索引
        indexArray = om.MIntArray()
        matrixPlug.getExistingArrayAttributeIndices(indexArray)
        print(indexArray)
        # 如果存在索引，取最大值
        if indexArray.length() > 0:
            maxIndex = indexArray[indexArray.length() - 1]+1  # 因为返回的索引数组是升序排列的，所以最后一个最大
            # print("最大索引是: ", maxIndex)
        else:
            maxIndex = 0
            print("没有找到有效索引，请检索节点matrix属性")

        # 获取权重列表数据
        weightListHandle = dataBlock.inputArrayValue(self.weightList)
        if weightListHandle.elementCount() == 0:
            # 没有权重数据 - 无需进行任何操作
            return

        # 获取影响变换矩阵数组
        transformsHandle = dataBlock.inputArrayValue(self.matrix)
        # numTransforms = transformsHandle.elementCount()  # 获取变换矩阵数量
        # print('numTransforms:', numTransforms)
        if transformsHandle.elementCount() == 0:
            return  # 如果没有变换矩阵，直接返回

        # 存储所有的变换矩阵
        transforms = []

        # 安全地遍历矩阵数组
        for i in range(maxIndex):
            # 跳转到当前元素
            if i in indexArray:
                transformsHandle.jumpToElement(i)
                # 跳转成功，安全地处理数据
                dataHandle = transformsHandle.inputValue()
                matrixData = dataHandle.data()

                if not matrixData.isNull():
                    matrixFn = om.MFnMatrixData(matrixData)
                    transforms.append(matrixFn.matrix())
            else:
                transforms.append([])

        # print('transforms1:', transforms)
        # 获取绑定姿势矩阵（用于计算相对变换）
        bindHandle = dataBlock.inputArrayValue(self.bindPreMatrix)
        if bindHandle.elementCount() > 0:
            # 确保只处理有效范围的元素
            for i in indexArray:
                bindHandle.jumpToElement(i)
                bindDataHandle = bindHandle.inputValue()
                bindMatrixData = bindDataHandle.data()

                if not bindMatrixData.isNull():
                    bindMatrixFn = om.MFnMatrixData(bindMatrixData)
                    bindMatrix = bindMatrixFn.matrix()
                    # 应用绑定姿势矩阵的逆变换来计算相对变换
                    transforms[i] = bindMatrix * transforms[i]

        # print('transforms2:', transforms)


        # 遍历几何体中的每个点
        geomIterator.reset()  # 重置迭代器到起始位置
        pointIndex = 0

        # 获取基础状态的模型点跟随的曲面点uv
        # while not geomIterator.isDone():
        #     pass
        #     geomIterator.next()

        while not geomIterator.isDone():
            # 获取点的原始位置[1](@ref)
            pt = geomIterator.position()
            skinned = om.MPoint(0.0, 0.0, 0.0, 0.0)  # 初始化变形后的点位置

            # 获取当前点的权重数据
            # 跳转到当前点的权重数据
            weightListHandle.jumpToElement(pointIndex)
            pointWeightsHandle = weightListHandle.inputValue()
            weightsHandle = pointWeightsHandle.child(self.weights)
            weightsArrayHandle = om.MArrayDataHandle(weightsHandle)

            totalWeight = 0.0  # 用于权重归一化检查

            # 计算蒙皮变形效果
            for i in range(len(transforms)):
                # 检查是否能成功跳转到指定权重要素
                try:
                    weightsArrayHandle.jumpToElement(i)
                    weightValue = weightsArrayHandle.inputValue().asDouble()
                    # print(weightValue)

                    # 线性混合蒙皮公式: 加权求和 (点位置 × 变换矩阵) × 权重值
                    if weightValue > 0.0001:  # 忽略极小权重提高性能
                        tempPoint = pt * transforms[i]
                        skinned += om.MVector(tempPoint * weightValue)
                        totalWeight += weightValue
                except:
                    pass

            # 权重归一化处理
            if totalWeight > 0.0001:
                if abs(totalWeight - 1.0) > 0.0001:
                    skinned = skinned * (1.0 / totalWeight)
            else:
                # 如果没有有效权重，保持原始位置
                skinned = pt
            # print(skinned.x, skinned.y, skinned.z)
            # 设置点的最终变形位置
            geomIterator.setPosition(skinned)

            # 前进到下一个点
            geomIterator.next()
            pointIndex += 1

            # 安全地前进权重列表句柄
            if pointIndex < weightListHandle.elementCount():
                try:
                    weightListHandle.next()
                except:
                    weightListHandle.jumpToElement(pointIndex)

        ####################################################
        # 获取 wrapSurface 属性值
        wrapSurfaceArrayHandle = dataBlock.inputArrayValue(self.wrapSurface)
        numWrapSurfaces = wrapSurfaceArrayHandle.elementCount()

        wrapSurfaces = []
        for i in range(numWrapSurfaces):
            if wrapSurfaceArrayHandle.jumpToElement(i):
                dataHandle = wrapSurfaceArrayHandle.inputValue()
                surfaceData = dataHandle.data()

                if not surfaceData.isNull():
                    surfaceFn = om.MFnNurbsSurface(surfaceData)
                    wrapSurfaces.append(surfaceFn)
                else:
                    # 处理空数据情况
                    wrapSurfaces.append(None)

        # 获取 baseSurface 属性值
        baseSurfaceArrayHandle = dataBlock.inputArrayValue(self.baseSurface)
        numBaseSurfaces = baseSurfaceArrayHandle.elementCount()

        baseSurfaces = []
        for i in range(numBaseSurfaces):
            if baseSurfaceArrayHandle.jumpToElement(i):
                dataHandle = baseSurfaceArrayHandle.inputValue()
                surfaceData = dataHandle.data()

                if not surfaceData.isNull():
                    surfaceFn = om.MFnNurbsSurface(surfaceData)
                    baseSurfaces.append(surfaceFn)
                else:
                    baseSurfaces.append(None)

        # 计算曲面变形




    # 节点创建函数
    @classmethod
    def creator(self):
        return ompx.asMPxPtr(surfaceSkinCluster())

    # 节点初始化函数 - 必须正确定义属性
    @classmethod
    def initialize(cls):
        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.wrapSurface = tAttr.create("wireSurface", "wsu", om.MFnData.kNurbsSurface)  # 改为曲面
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
        cls.attributeAffects(cls.wrapSurface, outputGeom)
        cls.attributeAffects(cls.baseSurface, outputGeom)

# 插件初始化函数
def initializePlugin(obj):
    plugin = ompx.MFnPlugin(obj, "KangmingZhan", "1.0", "Any")

    try:
        print("正在尝试注册surfaceSkinCluster节点")

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