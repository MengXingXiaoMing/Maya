# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaAnim as omAnim
import sys
import maya.cmds as cmds
import datetime
import numpy as np

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
        # print(indexArray)
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

        # # 存储所有的变换矩阵
        # transforms = []
        #
        # # 安全地遍历矩阵数组
        # for i in range(maxIndex):
        #     # 跳转到当前元素
        #     if i in indexArray:
        #         transformsHandle.jumpToElement(i)
        #         # 跳转成功，安全地处理数据
        #         dataHandle = transformsHandle.inputValue()
        #         matrixData = dataHandle.data()
        #
        #         if not matrixData.isNull():
        #             matrixFn = om.MFnMatrixData(matrixData)
        #             transforms.append(matrixFn.matrix())
        #     else:
        #         transforms.append([])

        # # 获取绑定姿势矩阵（用于计算相对变换）
        # bindHandle = dataBlock.inputArrayValue(self.bindPreMatrix)
        # if bindHandle.elementCount() > 0:
        #     # 确保只处理有效范围的元素
        #     for i in indexArray:
        #         bindHandle.jumpToElement(i)
        #         bindDataHandle = bindHandle.inputValue()
        #         bindMatrixData = bindDataHandle.data()
        #
        #         if not bindMatrixData.isNull():
        #             bindMatrixFn = om.MFnMatrixData(bindMatrixData)
        #             bindMatrix = bindMatrixFn.matrix()
        #             # 应用绑定姿势矩阵的逆变换来计算相对变换
        #             transforms[i] = bindMatrix * transforms[i]

        # # 遍历几何体中的每个点
        # geomIterator.reset()  # 重置迭代器到起始位置
        # pointIndex = 0



        '''while not geomIterator.isDone():
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
                    # print('weightValue:', weightValue)
                    # print('transforms:', transforms)

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
                    weightListHandle.jumpToElement(pointIndex)'''

        ####################################################
        # 获取 wrapSurface 属性值
        wrapSurfaceArrayHandle = dataBlock.inputArrayValue(self.wrapSurface)
        numWrapSurfaces = wrapSurfaceArrayHandle.elementCount()

        wrapSurfaces = []
        for i in indexArray:
            wrapSurfaceArrayHandle.jumpToElement(i)
            # print(i)
            dataHandle = wrapSurfaceArrayHandle.inputValue()
            surfaceData = dataHandle.data()

            if not surfaceData.isNull():
                surfaceFn = om.MFnNurbsSurface(surfaceData)
                wrapSurfaces.append(surfaceFn)
            else:
                wrapSurfaces.append(None)
        # print('wrapSurfaces:', wrapSurfaces)
        # 获取 baseSurface 属性值
        baseSurfaceArrayHandle = dataBlock.inputArrayValue(self.baseSurface)
        numBaseSurfaces = baseSurfaceArrayHandle.elementCount()
        # print('numBaseSurfaces:', numBaseSurfaces)
        baseSurfaces = []
        for i in indexArray:
            baseSurfaceArrayHandle.jumpToElement(i)
            # print(i)
            dataHandle = baseSurfaceArrayHandle.inputValue()
            surfaceData = dataHandle.data()

            if not surfaceData.isNull():
                surfaceFn = om.MFnNurbsSurface(surfaceData)
                baseSurfaces.append(surfaceFn)
            else:
                baseSurfaces.append(None)

        base_data = []
        geomIterator.reset()  # 重置迭代器到起始位置
        # 获取基础状态的模型点跟随的曲面点uv以及uv点世界坐标
        while not geomIterator.isDone():
            pt = geomIterator.position()
            # print(pt.x, pt.y, pt.z)
            # print(baseSurfaces)
            index, all_uv, all_point, all_distance = self.get_surface_weight(pt, baseSurfaces)
            # print([uv, point, surfaces])
            base_data.append([index, all_uv, all_point, all_distance])
            geomIterator.next()
        geomIterator.reset()  # 重置迭代器到起始位置

        # 计算曲面变形
        i = 0
        geomIterator.reset()  # 重置迭代器到起始位置
        while not geomIterator.isDone():
            # offset = om.MVector()
            # 跳转到当前点的权重数据
            weightListHandle.jumpToElement(i)
            pointWeightsHandle = weightListHandle.inputValue()
            weightsHandle = pointWeightsHandle.child(self.weights)
            weightsArrayHandle = om.MArrayDataHandle(weightsHandle)
            totalWeight = 0.0  # 用于权重归一化检查

            data = base_data[i]
            skinned = geomIterator.position()
            # 计算蒙皮变形效果
            for j in range(len(baseSurfaces)):
                # 检查是否能成功跳转到指定权重要素
                try:
                    weightsArrayHandle.jumpToElement(j)
                    weightValue = weightsArrayHandle.inputValue().asDouble()
                except:
                    weightValue = 0

                # print(weightValue)

                # 线性混合蒙皮公式: 加权求和 (点位置 × 变换矩阵) × 权重值
                if weightValue > 0.0001:  # 忽略极小权重提高性能
                    base_point = data[2][j]
                      # 初始化变形后的点位置
                    # 获取指定UV参数处的点坐标
                    new_point = om.MPoint()
                    u, v = data[1][j]
                    wrapSurfaces[j].getPointAtParam(u, v, new_point, om.MSpace.kWorld)

                    # tempPoint = data[1] * offset
                    # 计算偏移量
                    tempPoint = new_point - base_point
                    skinned += om.MVector(tempPoint * weightValue)
                    totalWeight += weightValue
                    # print('新点：', new_point.x, new_point.y, new_point.z)
                    # print('旧点：', all_point[i][j].x, all_point[i][j].y, all_point[i][j].z)
                    # offset = new_point - data[1]
                    # 获取当前点的权重数据
                    # print('weightValue')
                    # print('num:', j)
                    # 获取节点名称
                    # print(baseSurfaces[j])


            i += 1
            # 安全地前进权重列表句柄
            if i < weightListHandle.elementCount():
                try:
                    weightListHandle.next()
                except:
                    weightListHandle.jumpToElement(i)
            # # 权重归一化处理
            # if totalWeight > 0.0001:
            #     if abs(totalWeight - 1.0) > 0.0001:
            #         skinned = skinned * (1.0 / totalWeight)
            # else:
            #     # 如果没有有效权重，保持原始位置
            #     skinned = data[1]
            # print(skinned.x, skinned.y, skinned.z)
            # 设置点的最终变形位置
            geomIterator.setPosition(skinned)

            geomIterator.next()


    def get_surface_weight(self, position, surfaceFns):
        """计算顶点到曲面的权重（曲面版本）"""
        all_uv = []  # 存储UV参数
        all_point = []  # 存储曲面上最近的点
        all_distance = []
        for surfaceFn in surfaceFns:
            util_u = om.MScriptUtil()
            util_v = om.MScriptUtil()
            paramPtr_u = util_u.asDoublePtr()
            paramPtr_v = util_v.asDoublePtr()
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
        # print(min_index)
        # print(all_uv[min_index])
        # print(all_point[min_index])
        # print(surfaceFns[min_index])
        # print(wrapSurfaces[min_index])

        return min_index, all_uv, all_point, all_distance

    # 节点创建函数
    @classmethod
    def creator(self):
        return ompx.asMPxPtr(surfaceSkinCluster())

    # 节点初始化函数 - 必须正确定义属性
    @classmethod
    def initialize(cls):
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
'''
def create_surface_skin(self):
    # 创建多个NURBS平面
    meshs, surfaces = self.getMeshAndSurface()
    # 创建表面皮肤集群变形器
    for mesh in meshs:
        # print(mesh)
        deform = cmds.deformer(mesh, type="surfaceSkinCluster")
        deform_type = cmds.nodeType(deform, inherited=True)
        if deform_type:
            try:
                size = cmds.getAttr(deform[0] + ".lockWeights",size=1)
            except:
                size = 1
            # print('size', size)
            if size < 1:
                size = 1
            for surface in surfaces:
                self.copy_shape_node(surface)
                if not cmds.objExists(surface + ".lockInfluenceWeights"):
                    cmds.select(surface, replace=True)
                    cmds.addAttr(shortName="liw", longName="lockInfluenceWeights", attributeType="bool")

                shape = cmds.listRelatives(surface, shapes=1) or []
                # print(shape)
                connections = [
                    (surface + ".liw", deform[0] + ".lockWeights[" + str(size - 1) + "]"),
                    (surface + ".worldMatrix[0]", deform[0] + ".matrix[" + str(size - 1) + "]"),
                    (surface + ".objectColorRGB", deform[0] + ".influenceColor[" + str(size - 1) + "]"),
                    (shape[-1] + ".worldSpace[0]", deform[0] + ".baseSurface[" + str(size - 1) + "]"),
                    (shape[0] + ".worldSpace[0]", deform[0] + ".wrapSurface[" + str(size - 1) + "]")
                ]
                for source, target in connections:
                    try:
                        cmds.connectAttr(source, target)
                    except:
                        continue

                # cmds.connectAttr(surface + ".liw", deform+".lockWeights")
                # cmds.connectAttr(surface + ".worldMatrix[0]", deform+".matrix[" + str(i) + "]")
                # cmds.connectAttr(surface + ".objectColorRGB", deform+".influenceColor[" + str(i) + "]")
                # cmds.connectAttr(surface + ".worldSpace[0]", deform+".baseSurface[" + str(i) + "]", force=True)
                # cmds.connectAttr(surface + ".worldSpace[0]", deform+".wrapSurface[" + str(i) + "]", force=True)
                # 获取世界逆矩阵
                m = cmds.getAttr(surface + ".wim")
                # 设置绑定预矩阵
                cmds.setAttr(deform[0] + ".bindPreMatrix[" + str(size - 1) + "]", m, type="matrix")
                size += 1
    cmds.setAttr(deform[0]+".useComponentsMatrix", 1)

    # 设置皮肤集群的最大影响数
    # cmds.skinCluster("surfaceSkinCluster1", edit=True, maximumInfluences=3)
'''