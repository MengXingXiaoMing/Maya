# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds


class NewWire(ompx.MPxDeformerNode):
    def __init__(self):
        super(NewWire, self).__init__()

    # 节点标识
    node_name = "NewWire"
    node_id = om.MTypeId(0x00141480)

    # 属性声明 - 严格按照图片结构
    envelope = om.MObject()
    radius = om.MObject()
    curvePairs = om.MObject()
    wireCurve = om.MObject()
    baseCurve = om.MObject()

    def deform(self, dataBlock, geoIter, matrix, multiIndex):
        """
        空的deform方法 - 只用于测试属性结构
        """
        # 不进行任何变形计算，只验证属性连接
        try:
            # 获取基本属性值
            envelope_val = dataBlock.inputValue(self.envelope).asFloat()
            radius_val = dataBlock.inputValue(self.radius).asFloat()

            # 检查曲线对连接
            curve_pairs_handle = dataBlock.inputArrayValue(self.curvePairs)
            num_pairs = curve_pairs_handle.elementCount()

            print(f"NewWire节点执行 - 封套: {envelope_val}, 半径: {radius_val}, 曲线对数量: {num_pairs}")

        except Exception as e:
            print(f"属性检查错误: {e}")

    @classmethod
    def nodeInitializer(cls):
        """
        严格按照图片结构初始化属性
        """
        try:
            # 1. Envelope 属性
            n_attr = om.MFnNumericAttribute()
            cls.envelope = n_attr.create("envelope", "env", om.MFnNumericData.kFloat, 1.0)
            n_attr.setMin(0.0)
            n_attr.setMax(1.0)
            n_attr.setStorable(True)
            n_attr.setKeyable(True)
            cls.addAttribute(cls.envelope)

            # 2. Radius 属性
            n_attr = om.MFnNumericAttribute()
            cls.radius = n_attr.create("radius", "rad", om.MFnNumericData.kFloat, 5.0)
            n_attr.setMin(0.0)
            n_attr.setStorable(True)
            n_attr.setKeyable(True)
            cls.addAttribute(cls.radius)

            # 3. 创建子属性 - Wire Curve (数组)
            t_attr = om.MFnTypedAttribute()
            cls.wireCurve = t_attr.create("wireCurve", "wc", om.MFnData.kNurbsCurve)
            t_attr.setArray(True)
            t_attr.setStorable(True)
            t_attr.setConnectable(True)

            # 4. 创建子属性 - Base Curve (数组)
            t_attr = om.MFnTypedAttribute()
            cls.baseCurve = t_attr.create("baseCurve", "bc", om.MFnData.kNurbsCurve)
            t_attr.setArray(True)
            t_attr.setStorable(True)
            t_attr.setConnectable(True)

            # 5. 创建复合数组属性 Curve Pairs
            compound_attr = om.MFnCompoundAttribute()
            cls.curvePairs = compound_attr.create("curvePairs", "cp")

            # 将子属性添加到复合属性
            compound_attr.addChild(cls.wireCurve)
            compound_attr.addChild(cls.baseCurve)

            # 设置为数组
            compound_attr.setArray(True)
            compound_attr.setStorable(True)
            compound_attr.setConnectable(True)
            cls.addAttribute(cls.curvePairs)

            # 建立属性依赖
            output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
            cls.attributeAffects(cls.envelope, output_geom)
            cls.attributeAffects(cls.radius, output_geom)
            cls.attributeAffects(cls.curvePairs, output_geom)

        except Exception as e:
            raise RuntimeError(f"属性初始化失败: {str(e)}")

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(NewWire())


# 插件初始化
def initializePlugin(plugin):
    plugin_fn = ompx.MFnPlugin(plugin)
    try:
        plugin_fn.registerNode(
            NewWire.node_name,
            NewWire.node_id,
            NewWire.nodeCreator,
            NewWire.nodeInitializer,
            ompx.MPxNode.kDeformerNode
        )
    except:
        raise


def uninitializePlugin(plugin):
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(NewWire.node_id)