# coding=utf-8
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds


class CollisionDeformer(ompx.MPxDeformerNode):
    # 节点元数据
    kPluginNodeName = "spCollisionDeformer"
    kPluginNodeId = om.MTypeId(0x87001)

    # 属性定义
    collider_mesh = om.MObject()
    max_distance = om.MObject()
    strength = om.MObject()
    use_normals = om.MObject()

    # 空间加速结构缓存
    intersector_cache = {}

    def __init__(self):
        super(CollisionDeformer, self).__init__()

    def deform(self, data_block, geo_iter, world_matrix, multi_index):
        # 1. 获取基础属性
        envelope = data_block.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        if math.isclose(envelope, 0.0, abs_tol=1e-5):
            return

        # 2. 获取自定义属性
        max_dist_data = data_block.inputValue(self.max_distance)
        max_distance = max_dist_data.asFloat()

        strength_data = data_block.inputValue(self.strength)
        strength = strength_data.asFloat()

        use_normals_data = data_block.inputValue(self.use_normals)
        use_normals = use_normals_data.asBool()

        # 3. 获取碰撞体网格
        collider_handle = data_block.inputValue(self.collider_mesh)
        collider_obj = collider_handle.asMesh()
        if collider_obj.isNull():
            return

        # 4. 准备空间加速结构
        mesh_fn = om.MFnMesh(collider_obj)
        mesh_dag = om.MDagPath.getAPathTo(collider_obj)

        # 使用缓存优化性能[4](@ref)
        if mesh_dag not in self.intersector_cache:
            intersector = om.MMeshIntersector()
            intersector.create(collider_obj, world_matrix.inverse())
            self.intersector_cache[mesh_dag] = intersector
        else:
            intersector = self.intersector_cache[mesh_dag]

        # 5. 获取输入几何体
        input_handle = data_block.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        input_handle.jumpToElement(multi_index)
        input_element_handle = input_handle.outputValue()
        input_geom = input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()

        # 6. 获取法线数据
        normals = om.MFloatVectorArray()
        if use_normals:
            mesh_fn = om.MFnMesh(input_geom)
            mesh_fn.getVertexNormals(False, normals)

        # 7. 顶点变形处理
        inverse_world_matrix = world_matrix.inverse()
        point_on_mesh = om.MPointOnMesh()

        geo_iter.reset()
        while not geo_iter.isDone():
            # 获取顶点权重和位置
            weight = self.weightValue(data_block, multi_index, geo_iter.index())
            pt_world = geo_iter.position() * world_matrix

            # 碰撞检测[4](@ref)
            if intersector.getClosestPoint(pt_world, point_on_mesh, max_distance):
                # 计算碰撞方向
                collision_point = point_on_mesh.getPoint()
                collision_normal = point_on_mesh.getNormal()

                # 计算偏移向量
                if use_normals:
                    vertex_normal = om.MVector(normals[geo_iter.index()]) * world_matrix
                    vertex_normal.normalize()
                    offset_dir = vertex_normal
                else:
                    offset_dir = om.MVector(collision_point - pt_world).normal()

                # 计算衰减因子
                distance = point_on_mesh.distance()
                falloff = 1.0 - (distance / max_distance)

                # 应用变形
                offset = offset_dir * strength * falloff * weight * envelope
                new_pt_world = pt_world + offset
                new_pt_local = new_pt_world * inverse_world_matrix
                geo_iter.setPosition(new_pt_local)

            geo_iter.next()

        # 清理过期缓存
        self.cleanup_cache()

    def cleanup_cache(self):
        # 每帧清理超过5秒未使用的缓存
        current_time = om.MTime()
        current_time.setUIUnit(om.MTime.uiUnit())
        to_remove = [k for k, v in self.intersector_cache.items()
                     if current_time.value() - v.last_used > 5.0]
        for key in to_remove:
            del self.intersector_cache[key]

    @classmethod
    def nodeInitializer(cls):
        # 1. 碰撞体网格属性
        tAttr = om.MFnTypedAttribute()
        cls.collider_mesh = tAttr.create("colliderMesh", "col", om.MFnData.kMesh)
        tAttr.setReadable(True)
        tAttr.setWritable(True)
        tAttr.setStorable(True)
        cls.addAttribute(cls.collider_mesh)

        # 2. 最大距离属性
        nAttr = om.MFnNumericAttribute()
        cls.max_distance = nAttr.create("maxDistance", "maxDist", om.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.01)
        nAttr.setMax(10.0)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.max_distance)

        # 3. 变形强度属性
        cls.strength = nAttr.create("strength", "str", om.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(-1.0)
        nAttr.setMax(1.0)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.strength)

        # 4. 法线方向开关
        cls.use_normals = nAttr.create("useNormals", "uNorm", om.MFnNumericData.kBoolean, True)
        cls.addAttribute(cls.use_normals)

        # 5. 属性关联
        output_geom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.collider_mesh, output_geom)
        cls.attributeAffects(cls.max_distance, output_geom)
        cls.attributeAffects(cls.strength, output_geom)
        cls.attributeAffects(cls.use_normals, output_geom)

        # 6. 封套关联
        envelope_attr = ompx.cvar.MPxGeometryFilter_envelope
        cls.attributeAffects(envelope_attr, output_geom)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(CollisionDeformer())


def initializePlugin(plugin):
    plugin_fn = ompx.MFnPlugin(plugin, "Autodesk", "1.0", "Any")
    try:
        plugin_fn.registerNode(
            CollisionDeformer.kPluginNodeName,
            CollisionDeformer.kPluginNodeId,
            CollisionDeformer.nodeCreator,
            CollisionDeformer.nodeInitializer,
            ompx.MPxNode.kDeformerNode
        )
    except:
        sys.stderr.write(f"注册碰撞变形器失败: {CollisionDeformer.kPluginNodeName}")
        raise

    # 启用权重绘制
    cmds.makePaintable(
        CollisionDeformer.kPluginNodeName,
        "weights",
        attrType="multiFloat",
        shapeMode="deformer"
    )


def uninitializePlugin(plugin):
    # 移除权重绘制支持
    cmds.makePaintable(
        CollisionDeformer.kPluginNodeName,
        "weights",
        remove=True
    )
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(CollisionDeformer.kPluginNodeId)