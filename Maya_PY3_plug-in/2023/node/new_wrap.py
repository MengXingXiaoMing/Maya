# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import random
from scipy.interpolate import CubicSpline
import numpy as np
# cmds.setAttr("nurbsCircleShape2.intermediateObject", 1)
# kPluginNodeId = om.MTypeId(int(time.time() * 1000) % 0x7FFFFF)  # 动态ID
# 2. 节点类定义(变形器)
class NewWrap(ompx.MPxDeformerNode):
    def __init__(self):
        super(NewWrap, self).__init__()

    node_name = "NewWrap"
    n = 36  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 声明属性 - 改为曲面类型
    wireSurface = om.MObject()  # 原来是 wireCurve
    InfluenceRadius = om.MObject()
    baseSurface = om.MObject()  # 原来是 baseCurve
    bake_baseSurface_point = []  # 改为曲面点
    surfacePoints = om.MPointArray()  # 改为曲面点数组
    totalLength = 0
    layer = 0
    attribute_names = []
    surface_weights_list = []

    def deform(self, dataBlock, geoIter, matrix, multiIndex):
        # 获取封套权重
        self.base_envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        if math.isclose(self.base_envelope, 0.0, abs_tol=1e-5):
            return
        # 2. 获取标准权重数据（Maya 内置）
        # standard_weights = self.getStandardWeights(dataBlock, multiIndex)
        # 3. 获取扩展的 weightA 数据
        weight_a_data = self.getWeightAData(dataBlock, multiIndex)

        self.radius = dataBlock.inputValue(self.InfluenceRadius).asFloat()

        # 1. 获取输入网格
        input_handle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        input_handle.jumpToElement(multiIndex)
        input_element_handle = input_handle.outputValue()
        input_geom = input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        if input_geom.isNull():
            print('没有网格')
            return

        # 2. 获取复合数组属性中的曲面对 - 改为surfacePairs
        surface_pairs_handle = dataBlock.inputArrayValue(self.surfacePairs)
        num_pairs = surface_pairs_handle.elementCount()

        if num_pairs == 0:
            print('没有曲面')
            return

        # 存储所有曲面对的wireSurfaces和baseSurfaces数组
        all_surface_arrays = []

        # 遍历每个复合数组元素
        for pair_index in range(num_pairs):
            surface_pairs_handle.jumpToArrayElement(pair_index)
            element_handle = surface_pairs_handle.inputValue()

            # 获取Wire Surface数组
            wire_array_handle = om.MArrayDataHandle(element_handle.child(self.wireSurface))
            wire_array_count = wire_array_handle.elementCount()

            wire_surfaces = []
            for wire_index in range(wire_array_count):
                wire_array_handle.jumpToArrayElement(wire_index)
                wire_element_handle = wire_array_handle.inputValue()

                # 获取连接的NURBS曲面对象 - 改为asNurbsSurface
                wire_surface_obj = wire_element_handle.asNurbsSurface()
                if not wire_surface_obj.isNull():
                    # 创建曲面函数集用于操作 - 改为MFnNurbsSurface
                    wire_surface_fn = om.MFnNurbsSurface(wire_surface_obj)
                    wire_surfaces.append(wire_surface_fn)
                else:
                    print(f"Wire Surface[{wire_index}]未连接有效曲面")

            # 获取Base Surface数组
            base_array_handle = om.MArrayDataHandle(element_handle.child(self.baseSurface))
            base_array_count = base_array_handle.elementCount()

            base_surfaces = []
            for base_index in range(base_array_count):
                base_array_handle.jumpToArrayElement(base_index)
                base_element_handle = base_array_handle.inputValue()

                base_surface_obj = base_element_handle.asNurbsSurface()
                if not base_surface_obj.isNull():
                    base_surface_fn = om.MFnNurbsSurface(base_surface_obj)
                    base_surfaces.append(base_surface_fn)
                else:
                    print(f"Base Surface[{base_index}]未连接有效曲面")

            if wire_surfaces and base_surfaces:
                all_surface_arrays.append([wire_surfaces, base_surfaces])


        # 获取输入网格点
        inputMeshFn = om.MFnMesh(input_geom)
        self.inputPoints = om.MPointArray()
        inputMeshFn.getPoints(self.inputPoints, om.MSpace.kWorld)
        # print(all_surface_arrays)
        # 开始处理曲面变形
        all_offset = []
        for i in range(len(all_surface_arrays)):
            # 获取曲面上点的权重
            all_uv, all_point, all_weights = self.get_surface_weight(all_surface_arrays[i][1])
            # print(all_uv)
            # 创建独立变形
            all_point_offset = self.create_surface_deformations(all_surface_arrays[i][0], all_uv, all_point, all_weights)
            # print('all_offset', all_offset)
            # print('all_point_offset', all_point_offset)
            if self.layer == 0:
                if all_offset:
                    all_offset = [x + y for x, y in zip(all_offset, all_point_offset)]
                else:
                    all_offset.append(all_point_offset)
                    self.layer += 1
            else:
                all_offset.append(all_point_offset)
                pass

        # 应用变形
        i = 0
        while not geoIter.isDone():
            pt_local = geoIter.position()
            offset = all_offset[0][i]
            # print(offset.x, offset.y, offset.z)
            for j in range(1, len(all_offset)):
                offset += all_offset[j][i]
            geoIter.setPosition(pt_local + offset)
            i += 1
            geoIter.next()

    def getWeightAData(self, dataBlock, multiIndex):
        """安全获取 weightA 数据"""
        weights_data = {}
        try:
            # 获取 independentWeightList 数组
            weight_list_handle = dataBlock.outputArrayValue(self.independentWeightList)
            num_elements = weight_list_handle.elementCount()

            if num_elements > 0:
                weight_list_handle.jumpToElement(multiIndex)
                element_handle = weight_list_handle.inputValue()

                # 获取 weightsA 子属性
                weights_handle = element_handle.child(self.weightsA)
                weights_obj = weights_handle.data()

                if not weights_obj.isNull() and weights_obj.hasFn(om.MFn.kDoubleArrayData):
                    weights_array_fn = om.MFnDoubleArrayData(weights_obj)
                    weights_array = weights_array_fn.array()

                    for i in range(weights_array.length()):
                        weights_data[i] = weights_array[i]

        except Exception as e:
            print(f"获取 weightA 数据错误: {e}")

        return weights_data

    def get_surface_weight(self, surfaceFns):
        """计算顶点到曲面的权重（曲面版本）"""
        all_uv = []  # 存储UV参数
        all_point = []  # 存储曲面上最近的点
        all_weights = []

        vertex_count = self.inputPoints.length()

        for i in range(vertex_count):
            all_distance = []
            ls_point = []
            ls_uv = []

            for surfaceFn in surfaceFns:
                util_u = om.MScriptUtil()
                util_v = om.MScriptUtil()
                paramPtr_u = util_u.asDoublePtr()
                paramPtr_v = util_v.asDoublePtr()

                point = self.inputPoints[i]

                # 计算到曲面的最近点 - 曲面使用closestPoint方法
                # closestPoint = om.MPoint()
                closestPoint = surfaceFn.closestPoint(point, paramPtr_u, paramPtr_v, 0.001, om.MSpace.kWorld)

                u = util_u.getDouble(paramPtr_u)
                v = util_v.getDouble(paramPtr_v)
                ls_uv.append((u, v))
                ls_point.append(closestPoint)

                distance = point.distanceTo(closestPoint)
                all_distance.append(distance)

            all_weight = self.smoothWeights(all_distance, self.radius, self.base_envelope)
            all_uv.append(ls_uv)
            all_point.append(ls_point)
            all_weights.append(all_weight)

        return all_uv, all_point, all_weights

    def create_surface_deformations(self, wire_surfaceFn, all_uv, all_point, all_weight):
        """创建基于曲面的独立变形"""
        all_offset = []

        for i in range(len(all_uv)):
            offset = om.MVector()

            for j in range(len(wire_surfaceFn)):
                # 获取指定UV参数处的点坐标
                new_point = om.MPoint()
                u, v = all_uv[i][j]
                wire_surfaceFn[j].getPointAtParam(u, v, new_point, om.MSpace.kWorld)
                # print('新点：', new_point.x, new_point.y, new_point.z)
                # print('旧点：', all_point[i][j].x, all_point[i][j].y, all_point[i][j].z)
                # 计算偏移量
                offset = offset + (new_point - all_point[i][j]) * all_weight[i][j] * self.base_envelope

            all_offset.append(offset)

        return all_offset

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
        # 创建复合属性（包含wireSurface和baseSurface）
        compoundAttr = om.MFnCompoundAttribute()
        cls.surfacePairs = compoundAttr.create("surfacePairs", "sp")  # 改为surfacePairs

        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.wrapSurface = tAttr.create("wireSurface", "ws", om.MFnData.kNurbsSurface)  # 改为曲面
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setConnectable(True)
        tAttr.setKeyable(True)

        # 创建曲面属性 - 改为kNurbsSurface
        tAttr = om.MFnTypedAttribute()
        cls.baseSurface = tAttr.create("baseSurface", "bs", om.MFnData.kNurbsSurface)  # 改为曲面
        tAttr.setArray(True)
        tAttr.setStorable(True)
        tAttr.setConnectable(True)
        tAttr.setKeyable(True)

        # 创建 weightsA 数值数组属性
        n_attr = om.MFnNumericAttribute()
        cls.surfaceWeightList = n_attr.create("weightList", "wl", om.MFnNumericData.kFloat)
        n_attr.setArray(True)
        n_attr.setStorable(True)
        n_attr.setReadable(True)
        n_attr.setWritable(True)
        n_attr.setKeyable(False)
        # 只有数值数组属性需要设置多构建器
        n_attr.setUsesArrayDataBuilder(True)  # 保留这行

        # 将 weightsA 添加到 independentWeightList
        cls.compound_attr.addChild(cls.weightsA)

        # 将子属性添加到复合属性中
        compoundAttr.addChild(cls.wrapSurface)
        compoundAttr.addChild(cls.baseSurface)
        compoundAttr.addChild(cls.surfaceWeightList)
        compoundAttr.setArray(True)
        compoundAttr.setStorable(True)
        compoundAttr.setConnectable(True)
        cls.addAttribute(cls.surfacePairs)  # 改为surfacePairs

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

        # 5. 权重属性配置 (关键修复)
        # 创建 independentWeightList 复合数组
        '''cls.compound_attr = om.MFnCompoundAttribute()
        cls.independentWeightList = cls.compound_attr.create("independentWeightList", "wla")
        cls.compound_attr.setArray(True)
        cls.compound_attr.setStorable(True)
        cls.compound_attr.setReadable(True)
        cls.compound_attr.setWritable(True)'''
        # 复合数组通常不需要设置 setUsesArrayDataBuilder
        # compound_attr.setUsesArrayDataBuilder(True)  # 移除这行

        # # 创建 weightsA 数值数组属性
        # n_attr = om.MFnNumericAttribute()
        # cls.weightsA = n_attr.create("weights0", "w0", om.MFnNumericData.kFloat)
        # n_attr.setArray(True)
        # n_attr.setStorable(True)
        # n_attr.setReadable(True)
        # n_attr.setWritable(True)
        # n_attr.setKeyable(False)
        # # 只有数值数组属性需要设置多构建器
        # n_attr.setUsesArrayDataBuilder(True)  # 保留这行
        #
        # # 将 weightsA 添加到 independentWeightList
        # cls.compound_attr.addChild(cls.weightsA)
        #
        cls.addAttribute(cls.independentWeightList)

        # 建立属性依赖
        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.surfacePairs, outputGeom)
        # cls.attributeAffects(cls.wireCurve, outputGeom)
        # cls.attributeAffects(cls.baseCurve, outputGeom)
        cls.attributeAffects(cls.inMesh, outputGeom)
        cls.attributeAffects(cls.InfluenceRadius, outputGeom)
        cls.attributeAffects(cls.breakWeight, outputGeom)
        cls.attributeAffects(cls.independentWeightList, outputGeom)




    # 添加属性
    def add_attribute(self, ind):
        # 创建 weightsA 数值数组属性
        name = ['weights'+str(ind), 'w'+str(ind)]
        n_attr = om.MFnNumericAttribute()
        weights = n_attr.create(name[0], name[1], om.MFnNumericData.kFloat)
        n_attr.setArray(True)
        n_attr.setStorable(True)
        n_attr.setReadable(True)
        n_attr.setWritable(True)
        n_attr.setKeyable(False)
        # 只有数值数组属性需要设置多构建器
        n_attr.setUsesArrayDataBuilder(True)  # 保留这行

        # 将 weightsA 添加到 independentWeightList
        self.compound_attr.addChild(weights)
        cmds.makePaintable(NewWrap.node_name, name[0], attrType="multiFloat", shapeMode="deformer")
        return [weights, name[0]]

    # 移除绘制
    def remove_drawing(self):
        for name in self.attribute_names:
            cmds.makePaintable(NewWrap.node_name, name, remove=True)

    # 节点创建器
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(NewWrap())

# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            NewWrap.node_name,
            NewWrap.Uv_id,
            NewWrap.nodeCreator,        # 创建节点的函数
            NewWrap.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {NewWrap.node_name}")

    # cmds.makePaintable(NewWrap.node_name, "weights", attrType="multiFloat",shapeMode="deformer")
    cmds.makePaintable(NewWrap.node_name, "weights0", attrType="multiFloat", shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    # cmds.makePaintable(NewWrap.node_name, "weights", remove=True)
    cmds.makePaintable(NewWrap.node_name, "weights0", remove=True)
    NewWrap().remove_drawing()
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(NewWrap.Uv_id)