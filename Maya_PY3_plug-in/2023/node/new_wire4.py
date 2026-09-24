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
class NewWire(ompx.MPxDeformerNode):
    def __init__(self):
        super(NewWire, self).__init__()

    node_name = "NewWire"
    n = 10  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 声明属性
    wireCurve = om.MObject()
    falloffRadius = om.MObject()
    baseCurve = om.MObject()
    bake_baseCurve_point = []
    curvePoints = om.MPointArray()
    totalLength = 0
    # def deform(self, dataBlock, geoIter, matrix, multiIndex):
    #     """核心变形逻辑"""
    #     # 获取封套权重
    #     envelope = dataBlock.inputValue(self.envelope).asFloat()
    #     if envelope < 0.001:
    #         return
    #
    #     # 获取输入曲线
    #     curveHandle = dataBlock.inputValue(self.wireCurve)
    #     curveObj = curveHandle.asNurbsCurve()
    #     if curveObj.isNull():
    #         return
    #
    #     curveFn = om.MFnNurbsCurve(curveObj)
    #     # 1. 重建样条曲线参数化（弧长参数化）
    #     curvePoints = om.MPointArray()
    #     curveFn.getCVs(curvePoints, om.MSpace.kWorld)
    #     arcLengths = self.calculateArcLengths(curvePoints)  # 计算累积弧长
    #     # 2. 构建三次样条函数 [5,7](@ref)
    #     x = np.array([arcLengths[i] for i in range(curvePoints.length())])
    #     y = np.array([[curvePoints[i].x, curvePoints[i].y, curvePoints[i].z]
    #                   for i in range(curvePoints.length())])
    #     splineX = CubicSpline(x, y[:, 0])  # X轴样条
    #     splineY = CubicSpline(x, y[:, 1])  # Y轴样条
    #     splineZ = CubicSpline(x, y[:, 2])  # Z轴样条
    #
    #     # 获取衰减半径
    #     radiusHandle = dataBlock.inputValue(self.falloffRadius)
    #     radius = radiusHandle.asFloat()
    #
    #     # 初始化曲线函数集
    #     curveFn = om.MFnNurbsCurve(curveObj)
    #
    #     totalLength = curveFn.length()  # ? 总弧长
    #
    #     # 2. 创建曲线迭代器
    #     curveIter = om.MItCurveCV(curveObj)
    #
    #     # 3. 存储曲线点位置和u值
    #     curvePoints = om.MPointArray()
    #     while not curveIter.isDone():
    #         point = curveIter.position(om.MSpace.kWorld)
    #         curvePoints.append(point)
    #         curveIter.next()
    #         # 获取U值
    #         closestPoint = om.MPoint()
    #         param = om.MScriptUtil().asDoublePtr()
    #         curveFn.closestPoint(point, closestPoint, param, 0.001, om.MSpace.kWorld)
    #         t = om.MScriptUtil.getDouble(param)  # 曲线参数
    #
    #     # 3. 遍历网格顶点
    #     while not geoIter.isDone():
    #         point = geoIter.position()
    #
    #         # 4. 计算最近曲线点（投影到曲线）
    #         closestPoint = om.MPoint()
    #         param = om.MScriptUtil().asDoublePtr()
    #         curveFn.closestPoint(point, closestPoint, param, 0.001, om.MSpace.kWorld)
    #         t = om.MScriptUtil.getDouble(param)  # 曲线参数
    #
    #         s = curveFn.length(t)
    #
    #         arcPos = s / totalLength  # ? 标准化弧长 [0,1]
    #
    #         # # 5. 计算弧长位置（样条驱动变形核心）
    #         # arcPos = curveFn.findParamFromLength(t)  # 参数→弧长映射
    #         # 沿样条曲线计算目标位置 [3](@ref)
    #         x = float(splineX(arcPos))
    #         y = float(splineY(arcPos))
    #         z = float(splineZ(arcPos))
    #
    #         # x = float(1.0)
    #         # y = float(1.0)
    #         # z = float(1.0)
    #         targetPoint = om.MPoint(x, y, z)
    #         # 6. 改进权重函数（平滑过渡）
    #         distance = point.distanceTo(closestPoint)
    #         weight = self.smoothWeight(distance, radius, envelope)
    #
    #         # 7. 应用形变（向量插值）
    #         offset = (targetPoint - point) * 1
    #         geoIter.setPosition(point + offset)
    #         geoIter.next()

    # 就算好模型点到样条的最近点，然后根据位置缓存好是哪两个点影响，
    # 然后根据对应位置给缓存好两点的权重，再根据样条围成的区域对周围的样条自动算好权重，
    # 最后就是四边面的话就是8个点的权重，然后缓存每个点占总的权重比例，最后把这权重缓存，
    # 读取的时候就直接把对应8个点的位移直接乘以算好的权重给到模型点，为了不是算完上一个算下一个，就按蒙皮一样放一个节点上，一起缓存加更新

    def deform(self, dataBlock, geoIter, matrix, multiIndex):
        # 获取封套权重
        envelope = dataBlock.inputValue(self.envelope).asFloat()
        if envelope == 0.0:
            return

        # 1. 获取输入网格
        in_mesh_handle = dataBlock.inputValue(self.inMesh)
        in_mesh_data = in_mesh_handle.asMesh()
        if in_mesh_data.isNull():
            return
        else:
            print('获取到基础网格')

        # 获取变形曲线
        wire_curveHandle = dataBlock.inputValue(self.wireCurve)
        wire_curveObj = wire_curveHandle.asNurbsCurve()
        # 初始化曲线函数集
        wire_curveFn = om.MFnNurbsCurve(wire_curveObj)
        if wire_curveObj.isNull():
            return
        else:
            print('获取到变形曲线')

        # 获取基础曲线
        base_curveHandle = dataBlock.inputValue(self.baseCurve)
        base_curveObj = base_curveHandle.asNurbsCurve()
        # 初始化曲线函数集
        curveFn = om.MFnNurbsCurve(base_curveObj)
        if base_curveObj.isNull():
            return
        else:
            print('获取到基础曲线')

        '''
        # 获取基础点位置
        # 2. 判断连接是否有效
        base_points = om.MPointArray()
        if base_curveObj.isNull():
            base_points = self.curvePoints
        else:
            print('获取到基础曲线')
            # 4. 连接有效，使用连接的数据，并更新缓存

            # 1. 预计算曲线总长度
            self.totalLength = curveFn.length()
            # 2. 创建曲线迭代器
            curveIter = om.MItCurveCV(base_curveObj)
            # 3. 存储曲线点位置
            self.curvePoints = om.MPointArray()
            while not curveIter.isDone():
                self.curvePoints.append(curveIter.position(om.MSpace.kWorld))
                curveIter.next()
            base_points = self.curvePoints

        # 计算曲线点偏移距离
        if base_points:
            if wire_curveObj.isNull():
                return
            else:
                print('获取到变形曲线')
                # 4. 连接有效，使用连接的数据，并更新缓存
                # 初始化曲线函数集
                # curveFn = om.MFnNurbsCurve(wire_curveObj)
                # 2. 创建曲线迭代器
                curveIter = om.MItCurveCV(wire_curveObj)
                # 3. 存储曲线点位置
                # new_point = om.MPointArray()
                i = 0
                while not curveIter.isDone():
                    point = curveIter.position(om.MSpace.kWorld)
                    # new_point.append(curveIter.position(om.MSpace.kWorld))
                    offset = point - base_points[i]
                    i += 1
                    curveIter.next()
        else:
            print('没有基础点数据')
            '''

        # 计算点权重
        # 使用MFnMesh获取输入网格的完整数据
        inputMeshFn = om.MFnMesh(in_mesh_data)

        # 获取输入网格的所有顶点位置（原始位置，未变形）
        inputPoints = om.MPointArray()
        inputMeshFn.getPoints(inputPoints, om.MSpace.kWorld)
        # print(f"获取到输入网格，顶点数量: {inputPoints.length()}")

        # 遍历网格顶点
        util = om.MScriptUtil()
        paramPtr = util.asDoublePtr()

        all_u = []
        all_point = []  # 曲线上最近的点
        all_weight = []
        # 获取顶点总数
        vertex_count = inputPoints.length()
        # print(f"网格总顶点数: {vertex_count}")
        # 循环遍历每一个顶点
        for i in range(vertex_count):
            point = inputPoints[i]  # 基础模型点
            # 5. 计算最近曲线点
            closestPoint = om.MPoint()
            curveFn.closestPoint(point, closestPoint, paramPtr, 0.001, om.MSpace.kWorld)  # paramPtr是地址
            all_point.append(closestPoint)
            # 准备接收坐标的点
            new_point = om.MPoint()
            # 获取指定参数处的点坐标
            # curveFn.getPointAtParam(paramPtr, new_point, om.MSpace.kWorld)
            # all_point.append(new_point)
            u = util.getDouble(paramPtr)  # 曲线参数
            all_u.append(u)
            # 6. 计算弧长位置
            # s = curveFn.length(t)  # 起点到最近点的弧长
            # arcPos = s / self.totalLength  # 标准化弧长[0,1]

            # 7. 计算影响权重（基于距离）
            distance = point.distanceTo(closestPoint)
            radius = 1
            weight = self.smoothWeight(distance, radius, envelope)
            all_weight.append(weight)

        # -----------------------以上静态部分获取完毕-----------------------
        i = 0
        while not geoIter.isDone():  # 开始循环编辑模型数据
            # 获取点偏移
            # 准备接收坐标的点
            new_point = om.MPoint()
            # 获取指定参数处的点坐标
            wire_curveFn.getPointAtParam(all_u[i], new_point, om.MSpace.kWorld)
            # 获取偏移值
            offset = (new_point - all_point[i]) * all_weight[i] * envelope

            # 7. 应用形变（向量插值）
            geoIter.setPosition(all_point[i] + offset)
            i += 1
            geoIter.next()

    def smoothWeight(self, distance, radius, envelope):
        """基于三次样条的平滑权重函数 [5](@ref)"""
        # 标准化距离 (0~1)
        normalized = distance / radius
        # 三次样条权重核：2t? - 3t? + 1 [5](@ref)
        weight = 2.0 * normalized ** 3 - 3.0 * normalized ** 2 + 1.0
        return weight * envelope

    @classmethod
    def nodeInitializer(cls):
        # 创建曲线属性
        tAttr = om.MFnTypedAttribute()
        cls.wireCurve = tAttr.create("wireCurve", "wc", om.MFnData.kNurbsCurve)
        tAttr.setStorable(True)  # 关键：允许属性被存储
        tAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        cls.addAttribute(cls.wireCurve)

        # 创建曲线属性
        tAttr = om.MFnTypedAttribute()
        cls.baseCurve = tAttr.create("baseCurve", "bc", om.MFnData.kNurbsCurve)
        tAttr.setStorable(True)  # 关键：允许属性被存储
        tAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        cls.addAttribute(cls.baseCurve)

        # 创建输入网格属性
        tAttr = om.MFnTypedAttribute()
        cls.inMesh = tAttr.create("inMesh", "im", om.MFnData.kMesh)
        tAttr.setStorable(True)  # 关键：允许属性被存储
        tAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        cls.addAttribute(cls.inMesh)

        # 创建衰减半径属性
        nAttr = om.MFnNumericAttribute()
        cls.falloffRadius = nAttr.create("falloff", "fo", om.MFnNumericData.kFloat, 5.0)
        nAttr.setMin(0.0)
        nAttr.setStorable(True)  # 关键：允许属性被存储
        nAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        cls.addAttribute(cls.falloffRadius)

        # 创建烘焙权重属性
        nAttr = om.MFnNumericAttribute()
        cls.breakWeight = nAttr.create("break_weight", "bw", om.MFnNumericData.kInt, 0)
        nAttr.setMin(0)
        nAttr.setMax(1)
        nAttr.setStorable(True)  # 关键：允许属性被存储
        nAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        cls.addAttribute(cls.breakWeight)

        # 建立属性依赖
        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.wireCurve, outputGeom)
        cls.attributeAffects(cls.baseCurve, outputGeom)
        cls.attributeAffects(cls.inMesh, outputGeom)
        cls.attributeAffects(cls.falloffRadius, outputGeom)
        cls.attributeAffects(cls.breakWeight, outputGeom)








    # 节点创建器
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(NewWire())

# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            NewWire.node_name,
            NewWire.Uv_id,
            NewWire.nodeCreator,        # 创建节点的函数
            NewWire.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {NewWire.node_name}")

    cmds.makePaintable(NewWire.node_name, "weights", attrType="multiFloat",shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    # cmds.makePaintable(NewWire.node_name, "weights", remove=True)
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(NewWire.Uv_id)