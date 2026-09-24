# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import random
# from scipy.interpolate import CubicSpline
import numpy as np

# 2. 节点类定义(变形器)
class NewWire(ompx.MPxDeformerNode):
    def __init__(self):
        super(NewWire, self).__init__()

    node_name = "NewWire"
    n = 44  # 0-63
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

    # def process_curve_array(self, array_handle):
    #     """处理曲线数组，提取所有曲线对象"""
    #     curves = []
    #
    #     try:
    #         # 获取MObject并检查是否有效
    #         array_obj = array_handle.data()
    #         if array_obj.isNull():
    #             return curves
    #
    #         # 使用MFnArrayAttrsData处理数组数据
    #         if array_obj.hasFn(om.MFn.kArrayAttrsData):
    #             array_data_fn = om.MFnArrayAttrsData(array_obj)
    #
    #             # 获取NURBS曲线数组
    #             curve_array = array_data_fn.nurbsCurves()
    #             if not curve_array.isNull():
    #                 for i in range(curve_array.length()):
    #                     curve_obj = curve_array[i]
    #                     if not curve_obj.isNull():
    #                         curve_fn = om.MFnNurbsCurve(curve_obj)
    #                         curves.append(curve_fn)
    #
    #     except Exception as e:
    #         print(f"处理曲线数组时出错: {e}")
    #
    #     return curves
    #
    # def get_curve_array_from_compound(self, compound_handle, attribute, attribute_name, pair_index):
    #     """
    #     从复合属性中获取曲线数组 - 修复版
    #     """
    #     curves = []
    #
    #     try:
    #         # 获取子属性的数组句柄 (如 wireCurves)
    #         # 修复：直接检查MDataHandle的有效性，不使用isNull()
    #         array_handle = compound_handle.child(attribute)
    #
    #         # 修复：检查MDataHandle是否有效
    #         # 注意：MDataHandle没有isNull()方法，我们需要用其他方式检查
    #         try:
    #             # 尝试获取数据对象来检查句柄是否有效
    #             array_obj = array_handle.data()
    #
    #             # 如果数据对象为空，说明句柄无效
    #             if array_obj.isNull():
    #                 print(f"曲线对 {pair_index} 的 {attribute_name} 数据对象为空")
    #                 return curves
    #
    #         except Exception as e:
    #             print(f"曲线对 {pair_index} 的 {attribute_name} 数组句柄无效: {e}")
    #             return curves
    #
    #         # 获取数组数据对象
    #         array_obj = array_handle.data()
    #
    #         # 处理数组数据
    #         if array_obj.hasFn(om.MFn.kArrayAttrsData):
    #             array_data_fn = om.MFnArrayAttrsData(array_obj)
    #             curve_array = array_data_fn.nurbsCurves()
    #
    #             if not curve_array.isNull():
    #                 for i in range(curve_array.length()):
    #                     curve_obj = curve_array[i]
    #                     if not curve_obj.isNull() and curve_obj.hasFn(om.MFn.kNurbsCurve):
    #                         curve_fn = om.MFnNurbsCurve(curve_obj)
    #                         curves.append(curve_fn)
    #                         print(f"曲线对 {pair_index} 的 {attribute_name}[{i}] 添加成功")
    #                     else:
    #                         print(f"曲线对 {pair_index} 的 {attribute_name}[{i}] 曲线对象无效")
    #             else:
    #                 print(f"曲线对 {pair_index} 的 {attribute_name} 曲线数组为空")
    #         else:
    #             # 如果不是数组属性，尝试作为单个曲线处理
    #             if not array_obj.isNull() and array_obj.hasFn(om.MFn.kNurbsCurve):
    #                 curve_fn = om.MFnNurbsCurve(array_obj)
    #                 curves.append(curve_fn)
    #                 print(f"曲线对 {pair_index} 的 {attribute_name} 作为单个曲线添加成功")
    #
    #     except Exception as e:
    #         print(f"从曲线对 {pair_index} 获取 {attribute_name} 时出错: {e}")
    #
    #     return curves

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
        # in_mesh_handle = dataBlock.inputValue(self.inMesh)
        # in_mesh_data = in_mesh_handle.asMesh()
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
            print(f"曲线对[{pair_index}]的Wire Curve数组有{wire_array_count}个元素")
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
                    print(f"成功获取Wire Curve[{wire_index}]的曲线对象")
                else:
                    print(f"Wire Curve[{wire_index}]未连接有效曲线")

            base_array_handle = om.MArrayDataHandle(element_handle.child(self.baseCurves))
            # 获取Wire Curve数组的元素数量
            base_array_count = base_array_handle.elementCount()
            print(f"曲线对[{pair_index}]的base Curve数组有{base_array_count}个元素")
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
                    print(f"成功获取base_curves Curve[{base_index}]的曲线对象")
                else:
                    print(f"base_curves Curve[{base_index}]未连接有效曲线")

            # 获取Base Curve子属性数组
            # base_curves_array = self.get_curve_array_from_compound(element_handle, self.baseCurves, "Base Curve", pair_index)

            if wire_curves and base_curves:
                all_curve_arrays[pair_index] = [wire_curves, base_curves]
                print(f"成功添加曲线对 {pair_index}: {len(wire_curves)}个Wire曲线, {len(base_curves)}个Base曲线")
        # if all_curve_arrays:
        #     all_curve_arrays = all_curve_arrays[0]
        print(all_curve_arrays)

        '''
        # 获取变形曲线
        wire_curveHandle = dataBlock.inputValue(self.wireCurve)
        wire_curveObj = wire_curveHandle.asNurbsCurve()
        # 初始化曲线函数集
        wire_curveFn = om.MFnNurbsCurve(wire_curveObj)
        if wire_curveObj.isNull():
            # print('未获取到变形曲线')
            return
        # else:
        #     print('获取到变形曲线')

        # 获取基础曲线
        base_curveHandle = dataBlock.inputValue(self.baseCurve)
        base_curveObj = base_curveHandle.asNurbsCurve()
        # 初始化曲线函数集
        curveFn = om.MFnNurbsCurve(base_curveObj)
        if base_curveObj.isNull():
            # print('未获取到基础曲线')
            return
        # else:
        #     print('获取到基础曲线')
        '''

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
            print('asd')
            print(all_curve_arrays[i])
            print(all_curve_arrays[i][0])
            print(all_curve_arrays[i][1])
            for wire_curveFn, curveFn in zip(all_curve_arrays[i][0], all_curve_arrays[i][1]):
                all_point_offset = self.create_independent_deformations(wire_curveFn, curveFn)
                all_offset.append(all_point_offset)

        print('开始循环修改点')
        i = 0
        while not geoIter.isDone():  # 开始循环编辑模型数据
            pt_local = geoIter.position()
            offset = all_offset[0][i]
            for j in range(1, len(all_offset)):
                offset += all_offset[j][i]

            geoIter.setPosition(pt_local + offset)
            i += 1
            geoIter.next()

    def create_independent_deformations(self, wire_curveFn, curveFn):
        # 遍历网格顶点
        all_u = []
        all_point = []  # 曲线上最近的点
        # all_point2 = []  # 曲线上最近的点
        # all_new_point = []
        # all_mash_point = []
        all_weight = []
        # 获取顶点总数
        vertex_count = self.inputPoints.length()
        # print(f"网格总顶点数: {vertex_count}")
        # 循环遍历每一个顶点
        for i in range(vertex_count):
            util = om.MScriptUtil()
            paramPtr = util.asDoublePtr()
            point = self.inputPoints[i]  # 基础模型点
            # all_mash_point.append([point.x, point.y, point.z])
            # 5. 计算最近曲线点
            # closestPoint = om.MPoint()
            closestPoint = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kWorld)  # paramPtr是地址
            all_point.append(closestPoint)
            # all_point2.append([closestPoint.x, closestPoint.y, closestPoint.z])
            u = util.getDouble(paramPtr)  # 曲线参数
            all_u.append(u)
            # 准备接收坐标的点
            # new_point = om.MPoint()
            # 获取指定参数处的点坐标
            # curveFn.getPointAtParam(u, new_point, om.MSpace.kWorld)
            # all_new_point.append([new_point.x,new_point.y,new_point.z])

            # 7. 计算影响权重（基于距离）
            distance = point.distanceTo(closestPoint)
            weight = self.smoothWeight(distance, self.radius, self.base_envelope)
            all_weight.append(weight)
        # print('静态部分获取完毕')
        # print('最近的U值', all_u)
        # print('最近的U值点',all_point)
        # print('2最近的U值点', all_point2)
        # print('1全部U值取点', all_new_point)
        # print('模型基础点', all_mash_point)
        # print('权重',all_weight)
        # -----------------------以上静态部分获取完毕-----------------------
        # i = 0
        # all_geo_pt = []
        # all_ls_point = []
        all_offset = []
        for i in range(len(all_u)):
        # while not geoIter.isDone():  # 开始循环编辑模型数据
            # pt_local = geoIter.position()
            # all_geo_pt.append([pt_local.x,pt_local.y,pt_local.z])
            # 获取点偏移
            # 准备接收坐标的点
            new_point = om.MPoint()
            # 获取指定参数处的点坐标
            wire_curveFn.getPointAtParam(all_u[i], new_point, om.MSpace.kWorld)
            # ls_point = [new_point.x, new_point.y, new_point.z]
            # all_ls_point.append(ls_point)
            # 获取偏移值
            offset = (new_point - all_point[i]) * all_weight[i] * self.base_envelope
            all_offset.append(offset)
            # print(offset.x, offset.y, offset.z)

            # 7. 应用形变（向量插值）
            # geoIter.setPosition(pt_local + offset)
            # print(all_point[i] + offset)
            # i += 1
            # geoIter.next()
        # print(all_ls_point)
        # print(all_geo_pt)
        # print(all_offset)
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