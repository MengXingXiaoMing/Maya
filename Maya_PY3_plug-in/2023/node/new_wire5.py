# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import random
from scipy.interpolate import CubicSpline
import numpy as np

# 2. 节点类定义(变形器)
class NewWire(ompx.MPxDeformerNode):
    def __init__(self):
        super(NewWire, self).__init__()

    node_name = "NewWrap"
    n = 28  # 0-63
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

    def deform(self, dataBlock, geoIter, matrix, multiIndex):
        # 获取封套权重
        envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        if math.isclose(envelope, 0.0, abs_tol=1e-5):
            return

        # 1. 获取输入网格
        input_handle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        input_handle.jumpToElement(multiIndex)
        input_element_handle = input_handle.outputValue()
        input_geom = input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        # in_mesh_handle = dataBlock.inputValue(self.inMesh)
        # in_mesh_data = in_mesh_handle.asMesh()
        if input_geom.isNull():
            print('未获取到基础网格')
            return
        else:
            print('获取到基础网格')

        # 获取变形曲线
        wire_curveHandle = dataBlock.inputValue(self.wireCurve)
        wire_curveObj = wire_curveHandle.asNurbsCurve()
        # 初始化曲线函数集
        wire_curveFn = om.MFnNurbsCurve(wire_curveObj)
        if wire_curveObj.isNull():
            print('未获取到变形曲线')
            return
        else:
            print('获取到变形曲线')

        # 获取基础曲线
        base_curveHandle = dataBlock.inputValue(self.baseCurve)
        base_curveObj = base_curveHandle.asNurbsCurve()
        # 初始化曲线函数集
        curveFn = om.MFnNurbsCurve(base_curveObj)
        if base_curveObj.isNull():
            print('未获取到基础曲线')
            return
        else:
            print('获取到基础曲线')

        # 计算点权重
        # 5. 获取输入几何体

        inputMeshFn = om.MFnMesh(input_geom)
        # # 使用MFnMesh获取输入网格的完整数据
        # inputMeshFn = om.MFnMesh(in_mesh_data)

        # 获取输入网格的所有顶点位置（原始位置，未变形）
        inputPoints = om.MPointArray()
        inputMeshFn.getPoints(inputPoints, om.MSpace.kWorld)
        # print(f"获取到输入网格，顶点数量: {inputPoints.length()}")


        # 遍历网格顶点


        all_u = []
        all_point = []  # 曲线上最近的点
        all_point2 = []  # 曲线上最近的点
        all_new_point = []
        all_mash_point = []
        all_weight = []
        # 获取顶点总数
        vertex_count = inputPoints.length()
        print(f"网格总顶点数: {vertex_count}")
        # 循环遍历每一个顶点
        for i in range(vertex_count):
            util = om.MScriptUtil()
            paramPtr = util.asDoublePtr()
            point = inputPoints[i]  # 基础模型点
            all_mash_point.append([point.x, point.y, point.z])
            # 5. 计算最近曲线点
            # closestPoint = om.MPoint()
            closestPoint = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kWorld)  # paramPtr是地址
            all_point.append(closestPoint)
            all_point2.append([closestPoint.x, closestPoint.y, closestPoint.z])
            u = util.getDouble(paramPtr)  # 曲线参数
            all_u.append(u)
            # 准备接收坐标的点
            new_point = om.MPoint()
            # 获取指定参数处的点坐标
            curveFn.getPointAtParam(u, new_point, om.MSpace.kWorld)
            all_new_point.append([new_point.x,new_point.y,new_point.z])

            # 7. 计算影响权重（基于距离）
            distance = point.distanceTo(closestPoint)
            radius = 0.5
            weight = self.smoothWeight(distance, radius, envelope)
            all_weight.append(weight)
        print('静态部分获取完毕')
        print('最近的U值', all_u)
        print('最近的U值点',all_point)
        print('2最近的U值点', all_point2)
        print('1全部U值取点', all_new_point)
        print('模型基础点', all_mash_point)
        print('权重',all_weight)
        # -----------------------以上静态部分获取完毕-----------------------
        i = 0
        all_geo_pt = []
        all_ls_point = []
        all_offset = []
        while not geoIter.isDone():  # 开始循环编辑模型数据
            pt_local = geoIter.position()
            all_geo_pt.append([pt_local.x,pt_local.y,pt_local.z])
            # 获取点偏移
            # 准备接收坐标的点
            new_point = om.MPoint()
            # 获取指定参数处的点坐标
            wire_curveFn.getPointAtParam(all_u[i], new_point, om.MSpace.kWorld)
            ls_point = [new_point.x, new_point.y, new_point.z]
            all_ls_point.append(ls_point)
            # 获取偏移值
            offset = (new_point - all_point[i]) * all_weight[i] * envelope
            all_offset.append([offset.x,offset.y,offset.z])

            # 7. 应用形变（向量插值）
            geoIter.setPosition(pt_local + offset)
            # print(all_point[i] + offset)
            i += 1
            geoIter.next()
        print(all_ls_point)
        print(all_geo_pt)
        print(all_offset)


    def smoothWeight(self, distance, radius, envelope):
        """基于三次样条的平滑权重函数，距离超过半径则权重为0"""
        if distance > radius:
            return 0.0

        # 标准化距离 (此时normalized保证在0-1之间)
        normalized = distance / radius
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
        nAttr.setKeyable(True)
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