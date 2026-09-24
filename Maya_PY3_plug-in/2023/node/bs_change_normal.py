# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class BsChangeNormal(ompx.MPxNode):
    def __init__(self):
        super(BsChangeNormal, self).__init__()

    node_name = "BsChangeNormal"
    n = 2  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 属性声明
    inMesh = om.MObject()
    outMesh = om.MObject()
    input = om.MObject()
    targetMesh = om.MObject()

    def compute(self, plug, data_block):
        weight_handle = data_block.inputValue(self.input)
        weight_value = weight_handle.asFloat()

        # 只处理 outMesh 插头
        if plug != BsChangeNormal.outMesh:
            return

        # 1. 获取输入网格
        in_mesh_handle = data_block.inputValue(BsChangeNormal.inMesh)
        in_mesh_data = in_mesh_handle.asMesh()

        if in_mesh_data.isNull():
            return

        # 2. 获取目标网格
        target_mesh_handle = data_block.inputValue(BsChangeNormal.targetMesh)
        target_mesh = target_mesh_handle.asMesh()

        # 3. 创建输出网格对象
        mesh_data_fn = om.MFnMeshData()
        out_mesh = mesh_data_fn.create()

        if target_mesh.isNull():
            return
        in_mesh = in_mesh_data

        # 获取输入网格数据
        in_mesh_fn = om.MFnMesh(in_mesh)
        in_points = om.MPointArray()
        in_mesh_fn.getPoints(in_points)  # 获取点
        in_normals = om.MFloatVectorArray()  # 空法线列表
        in_mesh_fn.getNormals(in_normals)  # 获取法线

        # 获取目标网格
        target_mesh_fn = om.MFnMesh(target_mesh)
        target_points = om.MPointArray()
        target_mesh_fn.getPoints(target_points)  # 获取点
        target_normals = om.MFloatVectorArray()
        target_mesh_fn.getNormals(target_normals)  # 获取法线

        # 创建输出网格（复制输入网格作为基础）
        in_mesh_fn.copy(in_mesh, out_mesh)
        out_mesh_fn = om.MFnMesh(out_mesh)

        num_vertices = in_mesh_fn.numVertices()

        new_points = om.MPointArray()
        new_points.setLength(num_vertices)
        # 处理顶点位置插值
        for i in range(num_vertices):
            source_pt = in_points[i]
            target_pt = target_points[i]

            # 位置插值
            final_pt = source_pt + ((target_pt - source_pt) * weight_value)
            new_points.set(final_pt, i)

        # 设置更新后的顶点位置
        out_mesh_fn.setPoints(new_points)

        # 处理法线插值
        new_normals = om.MFloatVectorArray()
        for i in range(num_vertices):
            in_normal = in_normals[i]
            target_normal = target_normals[i]

            # 法线插值
            interpolated_normal = in_normal + ((target_normal - in_normal) * weight_value)
            interpolated_normal.normalize()  # 归一化
            new_normals.append(interpolated_normal)

        # 设置新的法线
        out_mesh_fn.setNormals(new_normals, om.MSpace.kObject)

        # 设置输出网格
        out_mesh_handle = data_block.outputValue(BsChangeNormal.outMesh)
        out_mesh_handle.setMObject(out_mesh)
        data_block.setClean(plug)

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
        cls.targetMesh = tAttr.create("targetMesh", "tm", om.MFnData.kMesh)
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
        return ompx.asMPxPtr(BsChangeNormal())


# 插件注册保持不变
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            BsChangeNormal.node_name,
            BsChangeNormal.Uv_id,
            BsChangeNormal.nodeCreator,
            BsChangeNormal.nodeInitializer
        )
    except:
        sys.stderr.write(f"注册节点失败: {BsChangeNormal.node_name}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(BsChangeNormal.Uv_id)