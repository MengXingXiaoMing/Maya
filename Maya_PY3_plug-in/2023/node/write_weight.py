# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds


class NewWrap(ompx.MPxDeformerNode):
    """NewWrap 变形器节点 - 支持多层级权重绘制"""

    def __init__(self):
        super(NewWrap, self).__init__()

    # 节点基本信息
    node_name = "NewWrap"
    n = 124  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    node_id = om.MTypeId(target_id)

    # 属性声明 - 与图片中的结构完全匹配
    radius = om.MObject()
    surfacePairs = om.MObject()
    weights = om.MObject()
    weightsA = om.MObject()

    def deform(self, dataBlock, geoIter, matrix, multiIndex):
        """
        变形计算 - 安全稳定的实现
        """
        try:
            # 1. 获取标准封套权重（使用变形器内置封套）
            envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
            if math.isclose(envelope, 0.0, abs_tol=1e-5):
                return

            # 2. 获取自定义半径属性
            radius_val = dataBlock.inputValue(self.radius).asFloat()
            if radius_val <= 0.0:
                return

            # 3. 安全获取输入几何体
            input_geom = self.getInputGeometry(dataBlock, multiIndex)
            if input_geom.isNull():
                return

            # 4. 获取曲面对数据
            surface_pairs = self.getSurfacePairs(dataBlock)
            if not surface_pairs:
                return

            # 5. 获取权重数据
            weights_data = self.getWeightsData(dataBlock, multiIndex)

            # 6. 应用变形
            self.applyDeformation(geoIter, input_geom, surface_pairs, weights_data, envelope, radius_val)

        except Exception as e:
            # 安全错误处理，避免Maya崩溃
            print(f"NewWrap变形器安全错误: {e}")

    def getInputGeometry(self, dataBlock, multiIndex):
        """安全获取输入几何体"""
        try:
            input_handle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
            input_handle.jumpToElement(multiIndex)
            input_element_handle = input_handle.outputValue()
            return input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        except:
            return om.MObject()  # 返回空对象

    def getSurfacePairs(self, dataBlock):
        """安全获取曲面对数据"""
        surface_pairs = []
        try:
            pairs_handle = dataBlock.inputArrayValue(self.surfacePairs)
            num_pairs = pairs_handle.elementCount()

            for i in range(num_pairs):
                pairs_handle.jumpToArrayElement(i)
                element_handle = pairs_handle.inputValue()

                # 这里可以添加具体的曲面处理逻辑
                pair_data = {
                    'index': i,
                    'weight_index': i  # 每个pair对应一个权重索引
                }
                surface_pairs.append(pair_data)

        except Exception as e:
            print(f"获取曲面对数据错误: {e}")

        return surface_pairs

    def getWeightsData(self, dataBlock, multiIndex):
        """安全获取权重数据"""
        weights_data = {}
        try:
            weights_handle = dataBlock.outputArrayValue(self.weights)
            weights_handle.jumpToElement(multiIndex)
            weights_element_handle = weights_handle.outputValue()

            weights_obj = weights_element_handle.data()
            if not weights_obj.isNull() and weights_obj.hasFn(om.MFn.kDoubleArrayData):
                weights_array_fn = om.MFnDoubleArrayData(weights_obj)
                weights_array = weights_array_fn.array()

                for i in range(weights_array.length()):
                    weights_data[i] = weights_array[i]

        except Exception as e:
            print(f"获取权重数据错误: {e}")

        return weights_data

    def applyDeformation(self, geoIter, input_geom, surface_pairs, weights_data, envelope, radius):
        """应用变形计算 - 安全稳定的实现"""
        try:
            # 获取输入网格点
            mesh_fn = om.MFnMesh(input_geom)
            input_points = om.MPointArray()
            mesh_fn.getPoints(input_points, om.MSpace.kWorld)

            vertex_index = 0
            geoIter.reset()

            while not geoIter.isDone():
                if vertex_index >= input_points.length():
                    break

                current_pos = geoIter.position()
                total_offset = om.MVector(0, 0, 0)

                # 对每个surfacePair计算影响
                for pair_data in surface_pairs:
                    pair_index = pair_data['index']
                    weight_index = pair_data['weight_index']

                    # 获取该pair的权重
                    pair_weight = weights_data.get(weight_index, 1.0)

                    if pair_weight > 0:
                        # 计算单个pair的变形偏移
                        pair_offset = self.calculatePairOffset(
                            current_pos, pair_index, radius, envelope
                        )

                        # 应用权重
                        weighted_offset = pair_offset * pair_weight
                        total_offset += om.MVector(weighted_offset.x, weighted_offset.y, weighted_offset.z)

                # 安全应用变形
                if total_offset.length() > 0.001:
                    new_position = current_pos + total_offset
                    geoIter.setPosition(new_position)

                vertex_index += 1
                geoIter.next()

        except Exception as e:
            print(f"应用变形错误: {e}")

    def calculatePairOffset(self, position, pair_index, radius, envelope):
        """计算单个曲面对的变形偏移 - 示例逻辑"""
        # 安全计算偏移量
        try:
            angle = pair_index * math.pi / 3
            distance_factor = min(1.0, position.length() / radius) if radius > 0 else 0

            offset_x = math.cos(angle) * distance_factor * envelope * 0.1
            offset_y = math.sin(angle) * distance_factor * envelope * 0.1
            offset_z = math.sin(angle * 2) * distance_factor * envelope * 0.05

            return om.MPoint(offset_x, offset_y, offset_z)
        except:
            return om.MPoint(0, 0, 0)

    @classmethod
    def nodeInitializer(cls):
        """节点属性初始化 - 与图片结构完全匹配"""
        try:
            # 1. 半径属性 (Radius)
            n_attr = om.MFnNumericAttribute()
            cls.radius = n_attr.create("radius", "rad", om.MFnNumericData.kFloat, 5.0)
            n_attr.setMin(0.0)
            n_attr.setKeyable(True)
            n_attr.setStorable(True)
            cls.addAttribute(cls.radius)

            # 2. 曲面对属性 (Surface Pairs) - 复合数组
            compound_attr = om.MFnCompoundAttribute()
            cls.surfacePairs = compound_attr.create("surfacePairs", "sp")

            # 创建子属性
            t_attr = om.MFnTypedAttribute()
            wire_surface = t_attr.create("wireSurface", "ws", om.MFnData.kNurbsSurface)
            t_attr.setArray(True)

            t_attr = om.MFnTypedAttribute()
            base_surface = t_attr.create("baseSurface", "bs", om.MFnData.kNurbsSurface)
            t_attr.setArray(True)

            # 添加到复合属性
            compound_attr.addChild(wire_surface)
            compound_attr.addChild(base_surface)
            compound_attr.setArray(True)
            cls.addAttribute(cls.surfacePairs)

            # 3. 权重属性 (Weights) - 多权重数组
            n_attr = om.MFnNumericAttribute()
            cls.weights = n_attr.create("weights", "w", om.MFnNumericData.kDouble)
            n_attr.setArray(True)
            n_attr.setUsesArrayDataBuilder(True)
            cls.addAttribute(cls.weights)

            # 3. 权重属性 (WeightsA) - 多权重数组
            n_attr = om.MFnNumericAttribute()
            cls.weightsA = n_attr.create("weightsA", "wA", om.MFnNumericData.kDouble)
            n_attr.setArray(True)
            n_attr.setUsesArrayDataBuilder(True)
            n_attr.setReadable(True)  # 确保可读
            n_attr.setWritable(True)  # 确保可写
            n_attr.setStorable(True)  # 确保可存储
            n_attr.setKeyable(False)  # 权重属性通常不可键控
            n_attr.setHidden(False)  # 确保不隐藏（默认就是False）
            cls.addAttribute(cls.weightsA)  # 确保已添加到节点

            # 建立属性依赖
            output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
            cls.attributeAffects(cls.radius, output_geom)
            cls.attributeAffects(cls.surfacePairs, output_geom)
            cls.attributeAffects(cls.weights, output_geom)
            cls.attributeAffects(cls.weightsA, output_geom)

            print("NewWrap节点属性初始化成功")

        except Exception as e:
            print(f"节点属性初始化失败: {e}")
            raise

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(NewWrap())


def initializePlugin(plugin):
    """插件初始化 - 安全稳定的注册"""
    try:
        plugin_fn = ompx.MFnPlugin(plugin)

        # 注册节点
        plugin_fn.registerNode(
            NewWrap.node_name,
            NewWrap.node_id,
            NewWrap.nodeCreator,
            NewWrap.nodeInitializer,
            ompx.MPxNode.kDeformerNode
        )

        # 注册为可绘制权重
        cmds.makePaintable(NewWrap.node_name, "weights", attrType="multiFloat", shapeMode="deformer")
        cmds.makePaintable(NewWrap.node_name, "weightsA", attrType="multiFloat", shapeMode="deformer")

        print(f"成功注册节点: {NewWrap.node_name}")

    except Exception as e:
        print(f"插件初始化失败: {e}")


def uninitializePlugin(plugin):
    """插件卸载"""
    try:
        cmds.makePaintable(NewWrap.node_name, "weights", remove=True)
        cmds.makePaintable(NewWrap.node_name, "weightsA", remove=True)
        plugin_fn = ompx.MFnPlugin(plugin)
        plugin_fn.deregisterNode(NewWrap.node_id)
        print(f"成功卸载节点: {NewWrap.node_name}")
    except Exception as e:
        print(f"插件卸载失败: {e}")