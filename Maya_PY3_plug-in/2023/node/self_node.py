# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import random



# 2. 节点类定义(变形器)
class SineNode(ompx.MPxDeformerNode):
    # 1. 定义节点名称与ID（ID需全局唯一）
    kPluginNodeTypeName = "spSineNode"
    sineNodeId = om.MTypeId(0x4703)  # 0x8700 是示例ID
    # 声明属性对象
    input = om.MObject()
    output = om.MObject()

    def __init__(self):
        super(SineNode, self).__init__()

    def deform(self, data_block, geo_iter, matrix, multi_index):
        envelope = data_block.inputValue(self.envelope).asFloat()

        if envelope == 0:
            return

        blend_weight = data_block.inputValue(self.input).asFloat()
        if blend_weight == 0:
            return

        target_mesh = data_block.inputValue(self.inMesh).asMesh()
        if target_mesh == 0:
            return

        global_weigh = blend_weight * envelope
        target_points = om.MPointArray()
        target_mesh_fn = om.MFnMesh(target_mesh)  # 获取模型
        target_mesh_fn.getPoints(target_points)  # 获取点




        geo_iter.reset()
        while not geo_iter.isDone():
            source_pt = geo_iter.position()
            target_pt = target_points[geo_iter.index()]

            source_weight = self.weightValue(data_block,multi_index,geo_iter.index())

            final_pt = source_pt + ((target_pt - source_pt) * global_weigh * source_weight)
            geo_iter.setPosition(final_pt)
            geo_iter.next()
        # geo_iter.reset()
        # while not geo_iter.isDone():
        #     if geo_iter.index() % 2 == 0:
        #         pt = geo_iter.position()
        #         pt.y += (2 * envelope)
        #
        #         geo_iter.setPosition(pt)
        #
        #     geo_iter.next()



        # ###############################
        # # 获取当前网格的DAG路径
        # this_node = self.thisMObject()
        # input_attr = ompx.MPxDeformerNode_input  # 获取输入属性
        # input_handle = data_block.outputArrayValue(input_attr)
        # input_handle.jumpToElement(multi_index)
        # input_geom = input_handle.outputValue().child(ompx.cvar.MPxDeformerNode_inputGeom).asMesh()
        #
        # # 创建MFnMesh对象操作UV
        # mesh_fn = om.MFnMesh(input_geom)
        # # 获取uv集s
        # uv_set_name = mesh_fn.getUVSetNames()
        #
        # # 准备批量修改UV数据
        # u_array = om.MFloatArray()
        # v_array = om.MFloatArray()
        # mesh_fn.getUVs(u_array, v_array, uv_set_name[0])
        #
        # # 遍历顶点并修改UV（示例：随机偏移）
        # i = 0.0
        # while not geo_iter.isDone():
        #     uv_index = geo_iter.uvIndex()
        #     if uv_index >= 0:  # 确保UV索引有效
        #         # 随机偏移UV（-0.1到0.1范围）
        #         u_array[uv_index] = i
        #         v_array[uv_index] = i
        #         # 限制在[0,1]范围
        #         u_array[uv_index] = max(0, min(1, u_array[uv_index]))
        #         v_array[uv_index] = max(0, min(1, v_array[uv_index]))
        #         i = i+0.01
        #     geo_iter.next()
        #
        # # 应用新UV数据
        # mesh_fn.setUVs(u_array, v_array, uv_set_name)
        #
        # mesh_fn.updateSurface()  # 更新网格显示

    # # 核心计算逻辑
    # def compute(self, plug, dataBlock):
    #     if plug == self.output:
    #         # 获取输入值
    #         inputHandle = dataBlock.inputValue(self.input)
    #         inputFloat = inputHandle.asFloat()
    #
    #         # 计算正弦结果
    #         result = math.sin(inputFloat) * 10.0
    #
    #         # 输出结果
    #         outputHandle = dataBlock.outputValue(self.output)
    #         outputHandle.setFloat(result)
    #         dataBlock.setClean(plug)  # 标记计算完成

    @classmethod
    def nodeInitializer(cls):
        pass
        # # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        cls.input = nAttr.create("inputaaa", "inValue", om.MFnNumericData.kFloat, 0.0)  # 改用inValue避免冲突
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值
        #
        # # 创建输出属性
        # nAttr = om.MFnNumericAttribute()
        # cls.output = nAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
        # nAttr.setWritable(False)  # 输出属性不可直接修改
        # nAttr.setStorable(False)  # 输出不保存（动态计算）
        #
        # 添加属性到节点
        cls.addAttribute(cls.input)
        # cls.addAttribute(cls.output)
        #
        # # 建立属性关联：输入变化触发输出更新
        # cls.attributeAffects(cls.input, cls.output)
        #
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
        return ompx.asMPxPtr(SineNode())

# 插件加载时执行
def initializePlugin(plugin):
    mplugin = ompx.MFnPlugin(plugin)
    try:
        mplugin.registerNode(
            SineNode.kPluginNodeTypeName,
            SineNode.sineNodeId,
            SineNode.nodeCreator,        # 创建节点的函数
            SineNode.nodeInitializer,     # 初始化属性的函数
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册节点失败: {SineNode.kPluginNodeTypeName}")

    cmds.makePaintable(SineNode.kPluginNodeTypeName,"weights",attrType="multiFloat",shapeMode="deformer")

# 插件卸载时执行
def uninitializePlugin(plugin):
    cmds.makePaintable(SineNode.kPluginNodeTypeName,"weights",remove=True)
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(SineNode.sineNodeId)
    # try:
    #     mplugin.deregisterNode(sineNodeId)
    # except:
    #     sys.stderr.write(f"注销节点失败: {kPluginNodeTypeName}")

# if __name__ == "__main__":
#     plugin_name = 'self_node.py'
#     cmds.evalDeferred('if cmds.pluginInfo("{0}",q=True,loaded=True):cmds.unloadPlugin("{0}")'.format(plugin_name))
#     cmds.evalDeferred('if not cmds.pluginInfo("{0}",q=True,loaded=True):cmds.unloadPlugin("{0}")'.format(plugin_name))
#     cmds.evalDeferred('cmds.polyCube()')
