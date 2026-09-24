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

    node_name = "NewWire"
    n = 67  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 声明属性
    wireCurve = om.MObject()
    InfluenceRadius = om.MObject()
    baseCurve = om.MObject()
    bake_baseCurve_point = []
    curvePoints = om.MPointArray()
    totalLength = 0

    def deform(self, dataBlock, geoIter, matrix, multiIndex):
        # 获取封套权重
        self.base_envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        if math.isclose(self.base_envelope, 0.0, abs_tol=1e-5):
            return

        self.radius = dataBlock.inputValue(self.InfluenceRadius).asFloat()

        # 1. 获取输入网格
        input_handle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        input_handle.jumpToElement(multiIndex)
        input_element_handle = input_handle.outputValue()
        input_geom = input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        if input_geom.isNull():
            # print('未获取到基础网格')
            return
        # else:
        #     print('获取到基础网格')

        # 2. 获取复合数组属性中的曲线对
        curve_pairs_handle = dataBlock.inputArrayValue(self.curvePairs)
        num_pairs = curve_pairs_handle.elementCount()

        if num_pairs == 0:
            return

        # 存储所有曲线对的wireCurves和baseCurves数组
        all_curve_arrays = []
        # 遍历每个复合数组元素
        for pair_index in range(num_pairs):
            all_curve_arrays.append([])
            curve_pairs_handle.jumpToArrayElement(pair_index)
            element_handle = curve_pairs_handle.inputValue()  # 获取到对应位置的复合属性

            wire_array_handle = om.MArrayDataHandle(element_handle.child(self.wireCurves))
            # 获取Wire Curve数组的元素数量
            wire_array_count = wire_array_handle.elementCount()
            # print(f"曲线对[{pair_index}]的Wire Curve数组有{wire_array_count}个元素")
            # 遍历Wire Curve数组的每个元素
            wire_curves = []
            for wire_index in range(wire_array_count):
                wire_array_handle.jumpToArrayElement(wire_index)
                wire_element_handle = wire_array_handle.inputValue()

                # 获取连接的NURBS曲线对象
                wire_curve_obj = wire_element_handle.asNurbsCurve()
                if not wire_curve_obj.isNull():
                    # 创建曲线函数集用于操作
                    wire_curve_fn = om.MFnNurbsCurve(wire_curve_obj)
                    wire_curves.append(wire_curve_fn)
                    # print(f"成功获取Wire Curve[{wire_index}]的曲线对象")
                else:
                    print(f"Wire Curve[{wire_index}]未连接有效曲线")

            base_array_handle = om.MArrayDataHandle(element_handle.child(self.baseCurves))
            # 获取Wire Curve数组的元素数量
            base_array_count = base_array_handle.elementCount()
            # print(f"曲线对[{pair_index}]的base Curve数组有{base_array_count}个元素")
            # 遍历base Curve数组的每个元素
            base_curves = []
            for base_index in range(base_array_count):
                base_array_handle.jumpToArrayElement(base_index)
                base_element_handle = base_array_handle.inputValue()

                # 获取连接的NURBS曲线对象
                base_curve_obj = base_element_handle.asNurbsCurve()
                if not base_curve_obj.isNull():
                    # 创建曲线函数集用于操作
                    base_curve_fn = om.MFnNurbsCurve(base_curve_obj)
                    base_curves.append(base_curve_fn)
                    # print(f"成功获取base_curves Curve[{base_index}]的曲线对象")
                else:
                    print(f"base_curves Curve[{base_index}]未连接有效曲线")

            # 获取Base Curve子属性数组
            # base_curves_array = self.get_curve_array_from_compound(element_handle, self.baseCurves, "Base Curve", pair_index)

            if wire_curves and base_curves:
                all_curve_arrays[pair_index] = [wire_curves, base_curves]
                # print(f"成功添加曲线对 {pair_index}: {len(wire_curves)}个Wire曲线, {len(base_curves)}个Base曲线")
        # if all_curve_arrays:
        #     all_curve_arrays = all_curve_arrays[0]
        # print(all_curve_arrays)  # 获取样条对，复合数组包含两个列表，两个列表里存运动样条和基础样条

        # 计算点权重

        inputMeshFn = om.MFnMesh(input_geom)
        # # 使用MFnMesh获取输入网格的完整数据
        # inputMeshFn = om.MFnMesh(in_mesh_data)

        # 获取输入网格的所有顶点位置（原始位置，未变形）
        self.inputPoints = om.MPointArray()
        inputMeshFn.getPoints(self.inputPoints, om.MSpace.kWorld)
        # print(f"获取到输入网格，顶点数量: {inputPoints.length()}")

        # 开始循环建立独立影响的效果
        all_offset = []
        for i in range(len(all_curve_arrays)):
            # print('asd')
            # print(all_curve_arrays[i])
            # print(all_curve_arrays[i][0])
            # print(all_curve_arrays[i][1])
            # 获取范围内样条控制点的权重
            all_u, all_point, all_weights = self.get_weight(all_curve_arrays[i][1])
            # for wire_curveFn, curveFn in zip(all_curve_arrays[i][0], all_curve_arrays[i][1]):
            #     all_point_offset = self.create_independent_deformations(wire_curveFn, curveFn)
            #     all_offset.append(all_point_offset)

            all_point_offset = self.create_independent_deformations(all_curve_arrays[i][0], all_u, all_point, all_weights)
            if all_offset:
                all_offset = [x + y for x, y in zip(all_offset, all_point_offset)]
            else:
                all_offset.append(all_point_offset)

        # print('开始循环修改点')
        i = 0
        # print(all_offset)
        while not geoIter.isDone():  # 开始循环编辑模型数据
            pt_local = geoIter.position()
            offset = all_offset[0][i]
            for j in range(1, len(all_offset)):
                offset += all_offset[j][i]
            # print('a')
            geoIter.setPosition(pt_local + offset)
            # print('d')
            i += 1
            geoIter.next()

    def get_weight(self, curveFns):
        # 遍历网格顶点
        all_u = []
        all_point = []  # 曲线上最近的点
        all_weights = []
        # 获取顶点总数
        vertex_count = self.inputPoints.length()
        # 循环遍历每一个顶点
        for i in range(vertex_count):
            all_distance = []
            ls_point = []
            ls_u = []
            for curveFn in curveFns:
                util = om.MScriptUtil()
                paramPtr = util.asDoublePtr()
                point = self.inputPoints[i]  # 基础模型点
                closestPoint = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kWorld)  # paramPtr是地址
                ls_point.append(closestPoint)

                u = util.getDouble(paramPtr)  # 曲线参数
                ls_u.append(u)
                # 7. 计算影响权重（基于距离）
                distance = point.distanceTo(closestPoint)
                all_distance.append(distance)
                # weight = self.smoothWeight(distance, self.radius, self.base_envelope)
                # all_weight.append(weight)
            all_weight = self.smoothWeights(all_distance, self.radius, self.base_envelope)
            all_u.append(ls_u)
            all_point.append(ls_point)
            all_weights.append(all_weight)
        return all_u, all_point, all_weights  # 所有顶点距离输入线的最近点和对应权重

    def create_independent_deformations(self, wire_curveFn, all_u, all_point, all_weight):
        all_offset = []
        # print(all_u)
        # print(all_point)
        # print(all_weight)
        for i in range(len(all_u)):
            offset = om.MVector()
            for j in range(len(wire_curveFn)):
                # 准备接收坐标的点
                new_point = om.MPoint()
                # 获取指定参数处的点坐标
                u = all_u[i][j]
                # print(wire_curveFn[j])
                wire_curveFn[j].getPointAtParam(u, new_point, om.MSpace.kWorld)
                # 获取偏移值
                # print(all_point[i][j])
                # print(all_weight[i][j])
                offset = offset+(new_point - all_point[i][j]) * all_weight[i][j] * self.base_envelope
            # print('offset:',offset)
            all_offset.append(offset)
        return all_offset

    def smoothWeight(self, distance, radius, envelope):
        """基于三次样条的平滑权重函数，距离超过半径则权重为0"""
        if distance > radius:
            return 0.0

        # 标准化距离 (此时normalized保证在0-1之间)
        normalized = distance / radius
        weight = 2.0 * normalized ** 3 - 3.0 * normalized ** 2 + 1.0

        return weight * envelope

    # 点在多个距离之间分配权重
    def smoothWeights(self, distances, radius, envelope):
        """基于距离的平滑权重计算，距离越小权重越大，所有权重之和为1"""
        if not distances:
            return []

        # 存储每个距离的初始权重
        raw_weights = []
        valid_distances_count = 0

        # 计算每个距离的初始权重
        for distance in distances:
            if distance > radius:
                # 距离超过半径，权重为0
                raw_weights.append(0.0)
            else:
                # 计算标准化距离 (0-1范围)
                normalized = distance / radius

                # 使用三次样条函数计算权重[8](@ref)
                # 这个函数确保距离越小权重越大，在边界处平滑过渡
                weight = 2.0 * normalized ** 3 - 3.0 * normalized ** 2 + 1.0
                raw_weights.append(weight)
                valid_distances_count += 1

        # 如果没有有效距离，返回均匀权重或零权重
        if valid_distances_count == 0:
            # 所有距离都超出半径，返回均匀权重或零权重
            return [0.0] * len(distances)

        # 计算权重总和用于归一化
        total_weight = sum(raw_weights)

        # 归一化权重，确保总和为1
        if total_weight > 0:
            normalized_weights = [weight / total_weight for weight in raw_weights]
        else:
            # 如果所有权重都为0，返回均匀分布
            normalized_weights = [1.0 / len(distances)] * len(distances)

        # 应用封套权重
        final_weights = [weight * envelope for weight in normalized_weights]

        return final_weights

    @classmethod
    def nodeInitializer(cls):
        # 创建复合属性（包含wireCurve和baseCurve）
        compoundAttr = om.MFnCompoundAttribute()
        cls.curvePairs = compoundAttr.create("curvePairs", "cp")

        # 创建曲线属性
        tAttr = om.MFnTypedAttribute()
        cls.wireCurves = tAttr.create("wireCurve", "wc", om.MFnData.kNurbsCurve)
        tAttr.setArray(True)  # 设置为数组属性
        tAttr.setStorable(True)  # 关键：允许属性被存储
        tAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        tAttr.setKeyable(True)
        # cls.addAttribute(cls.wireCurves)

        # 创建曲线属性
        tAttr = om.MFnTypedAttribute()
        cls.baseCurves = tAttr.create("baseCurve", "bc", om.MFnData.kNurbsCurve)
        tAttr.setArray(True)  # 设置为数组属性
        tAttr.setStorable(True)  # 关键：允许属性被存储
        tAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        tAttr.setKeyable(True)
        # tAttr.setIndexMatters(True)  # 索引重要，保持顺序
        # cls.addAttribute(cls.baseCurves)

        # 将子属性添加到复合属性中
        compoundAttr.addChild(cls.wireCurves)
        compoundAttr.addChild(cls.baseCurves)

        # 将复合属性设置为数组
        compoundAttr.setArray(True)
        compoundAttr.setStorable(True)
        compoundAttr.setConnectable(True)
        cls.addAttribute(cls.curvePairs)

        # 创建输入网格属性
        tAttr = om.MFnTypedAttribute()
        cls.inMesh = tAttr.create("inMesh", "im", om.MFnData.kMesh)
        tAttr.setStorable(True)  # 关键：允许属性被存储
        tAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        cls.addAttribute(cls.inMesh)

        # 创建衰减半径属性
        nAttr = om.MFnNumericAttribute()
        cls.InfluenceRadius = nAttr.create("Radius", "Radius", om.MFnNumericData.kFloat, 5.0)
        nAttr.setMin(0.0)
        nAttr.setStorable(True)  # 关键：允许属性被存储
        nAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        nAttr.setKeyable(True)
        cls.addAttribute(cls.InfluenceRadius)

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
        cls.attributeAffects(cls.curvePairs, outputGeom)
        # cls.attributeAffects(cls.wireCurve, outputGeom)
        # cls.attributeAffects(cls.baseCurve, outputGeom)
        cls.attributeAffects(cls.inMesh, outputGeom)
        cls.attributeAffects(cls.InfluenceRadius, outputGeom)
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