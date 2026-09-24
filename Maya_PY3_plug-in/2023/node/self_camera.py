# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class SelfCamera(ompx.MPxNode):
    def __init__(self):
        super(SelfCamera, self).__init__()

    node_name = "SelfCamera"
    n = 0  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 属性声明
    inMesh = om.MObject()
    outMesh = om.MObject()
    input = om.MObject()
    targetMesh = om.MObject()

    def compute(self, plug, data_block):
        # 只处理 outMesh 插头
        if plug != SelfCamera.outMesh:
            return

        # 1. 获取输入网格
        in_mesh_handle = data_block.inputValue(SelfCamera.inMesh)
        in_mesh_data = in_mesh_handle.asMesh()

        if in_mesh_data.isNull():
            return

        # 2. 获取目标网格
        target_mesh_handle = data_block.inputValue(SelfCamera.targetMesh)
        target_mesh = target_mesh_handle.asMesh()

        if target_mesh.isNull():
            return

        # 3. 创建输出网格对象
        mesh_data_fn = om.MFnMeshData()
        out_mesh = mesh_data_fn.create()

        # 4. 处理UV变形
        self.process_uv_deform(in_mesh_data, target_mesh, out_mesh, data_block)

        # 5. 设置输出
        output_handle = data_block.outputValue(SelfCamera.outMesh)
        output_handle.setMObject(out_mesh)
        data_block.setClean(plug)  # 标记为"干净"状态

    # in_mesh：输出模型
    # target_mesh：控制uv模型
    def process_uv_deform(self, in_mesh, target_mesh, out_mesh, data_block):
        # 获取输入网格数据
        in_mesh_fn = om.MFnMesh(in_mesh)

        # 获取目标网格点位置
        target_points = om.MPointArray()
        target_mesh_fn = om.MFnMesh(target_mesh)
        target_mesh_fn.getPoints(target_points)

        # 创建输出网格（复制输入网格作为基础）
        in_mesh_fn.copy(in_mesh, out_mesh)
        out_mesh_fn = om.MFnMesh(out_mesh)

        # 获取UV集
        uv_sets = []
        in_mesh_fn.getUVSetNames(uv_sets)

        # 获取原始UV
        u_list = om.MFloatArray()
        v_list = om.MFloatArray()
        in_mesh_fn.getUVs(u_list, v_list, uv_sets[0])

        # 获取权重值
        # input_handle = data_block.inputValue(SelfCamera.input)
        # blend_weight = input_handle.asFloat()
        # envelope = data_block.inputValue(ompx.MPxNode.envelope).asFloat()
        # global_weight = blend_weight * envelope

        # 计算新UV
        for i in range(u_list.length()):
            # 这里简化权重获取，实际应通过顶点索引获取
            source_weight = 1.0

            u = u_list[i] + (target_points[i].x - u_list[i]) * source_weight
            v = v_list[i] + (target_points[i].y - v_list[i]) * source_weight

            u_list.set(u, i)
            v_list.set(v, i)

        # 更新UV
        out_mesh_fn.setUVs(u_list, v_list, uv_sets[0])
        out_mesh_fn.updateSurface()

    @classmethod
    def nodeInitializer(cls):
        # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        cls.input = nAttr.create("inputValue", "inVal", om.MFnNumericData.kFloat, 1.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)

        # 创建输入网格属性
        tAttr = om.MFnTypedAttribute()
        cls.inMesh = tAttr.create("inMesh", "im", om.MFnData.kMesh)
        tAttr.setStorable(True)

        # 创建目标网格属性
        cls.targetMesh = tAttr.create("UVMesh", "tm", om.MFnData.kMesh)
        tAttr.setStorable(True)

        # 创建输出网格属性
        cls.outMesh = tAttr.create("outMesh", "om", om.MFnData.kMesh)
        tAttr.setStorable(False)
        tAttr.setWritable(False)

        # 添加属性
        cls.addAttribute(cls.inMesh)
        cls.addAttribute(cls.outMesh)
        cls.addAttribute(cls.input)
        cls.addAttribute(cls.targetMesh)

        # 设置依赖关系
        cls.attributeAffects(cls.inMesh, cls.outMesh)
        cls.attributeAffects(cls.input, cls.outMesh)
        cls.attributeAffects(cls.targetMesh, cls.outMesh)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(SelfCamera())


# 插件注册保持不变
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            SelfCamera.node_name,
            SelfCamera.Uv_id,
            SelfCamera.nodeCreator,
            SelfCamera.nodeInitializer
        )
    except:
        sys.stderr.write(f"注册节点失败: {SelfCamera.node_name}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(SelfCamera.Uv_id)