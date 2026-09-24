# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds






# 2. 节点类定义(变形器)
class UvDeform(ompx.MPxDeformerNode):
    # 1. 定义节点名称与ID（ID需全局唯一）
    kPluginNodeTypeName = "UvDeform"
    UvDeformId = om.MTypeId(0x8751)  # 0x8700 是示例ID
    # 声明属性对象
    input = om.MObject()

    def __init__(self):
        super(UvDeform, self).__init__()

    # data_block：数据容器，存储节点所有输入/输出属性值
    # geo_iter：几何体迭代器，遍历当前网格顶点
    # matrix：当前变形实例的世界变换矩阵
    # multi_index：当前处理的几何体实例索引
    def deform(self, data_block, geo_iter, matrix, multi_index):
        envelope = data_block.inputValue(self.envelope).asFloat()  # 封套权重（0~1）
        if envelope == 0:
            return

        blend_weight = data_block.inputValue(self.input).asFloat()  # 混合权重
        if blend_weight == 0:
            return

        target_mesh = data_block.inputValue(self.inMesh).asMesh()  # 目标模型
        if target_mesh == 0:
            return

        global_weigh = blend_weight * envelope # 混合权重
        # 获取目标控制模型点数据
        target_points = om.MPointArray()
        target_mesh_fn = om.MFnMesh(target_mesh)  # 获取模型
        target_mesh_fn.getPoints(target_points)  # 获取点

        # 获取输入几何体
        input_handle = data_block.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        input_handle.jumpToElement(multi_index)
        input_element_handle = input_handle.outputValue()
        input_geom = input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()

        # 创建MFnMesh对象
        mesh_fn = om.MFnMesh(input_geom)  # 自身的模型
        # 获取UV集名称
        uv_sets = []
        mesh_fn.getUVSetNames(uv_sets)

        # 获取uv集
        u_list = om.MFloatArray()
        v_list = om.MFloatArray()
        mesh_fn.getUVs(u_list, v_list, uv_sets[0])

        # 计算新的UV值
        # geo_iter.reset()  # 重置模型
        for i in range(len(u_list)):
            source_weight = self.weightValue(data_block, multi_index, i)  # 绘制的权重
            target_pt = target_points[i] # 目标顶点位置
            # print(target_pt[0],target_pt[1])
            u = target_pt[0]+(target_pt[0] - u_list[i]) * global_weigh * source_weight
            v = target_pt[1]+(target_pt[1] - v_list[i]) * global_weigh * source_weight
            # u = target_pt[0]
            # v = target_pt[1]
            u_list[i] = u
            v_list[i] = v


        # 设置回网格
        mesh_fn.setUVs(om.MFloatArray(u_list), om.MFloatArray(v_list), uv_sets[0])
        # ===== 仅添加以下4行代码 ===== #
        mesh_fn.updateSurface()  # 强制更新网格数据结构
        data_block.outputValue(self.outputGeom).setClean()  # 标记输出几何体为"干净"状态
        if not cmds.about(batch=True):  # 非批处理模式下刷新视图
            cmds.refresh(cv=True, force=True)  # 强制刷新当前视图




    @classmethod
    def nodeInitializer(cls):
        pass
        # # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        cls.input = nAttr.create("inputaaa", "inValue", om.MFnNumericData.kFloat, 1.0)  # 改用inValue避免冲突
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值

        # 添加属性到节点
        cls.addAttribute(cls.input)

        # 创建输入Mesh属性
        tAttr = om.MFnTypedAttribute()
        cls.inMesh = tAttr.create("inMesh", "im", om.MFnData.kMesh)
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值

        # 创建输出Mesh属性
        cls.outMesh = tAttr.create("outMesh", "om", om.MFnData.kMesh)
        tAttr.setStorable(False)  # 动态计算，不存储
        tAttr.setWritable(False)  # 禁止用户直接修改

        # 添加属性并建立依赖
        cls.addAttribute(cls.inMesh)
        cls.addAttribute(cls.outMesh)
        # cls.attributeAffects(cls.inMesh, cls.outMesh)  # 输入变化触发输出更新[5,9](@ref)
        output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.inMesh, output_geom)  # 输入变化触发输出更新[5,9](@ref)
        cls.attributeAffects(cls.input, output_geom)  # 输入变化触发输出更新[5,9](@ref)


    # 节点创建器
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(UvDeform())

# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            UvDeform.kPluginNodeTypeName,
            UvDeform.UvDeformId,
            UvDeform.nodeCreator,        # 创建节点的函数
            UvDeform.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {UvDeform.kPluginNodeTypeName}")

    cmds.makePaintable(UvDeform.kPluginNodeTypeName,"weights",attrType="multiFloat",shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    cmds.makePaintable(UvDeform.kPluginNodeTypeName,"weights",remove=True)
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(UvDeform.UvDeformId)
