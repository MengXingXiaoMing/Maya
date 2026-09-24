# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    # 库路径
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)

# 模型处理
class Model:
    # 按拓扑传递UV
    def transfer_uv(self, soure, target, transfer_method):
        UVsetA = cmds.polyUVSet(soure, q=1, currentUVSet=1)[0]
        UVsetB = cmds.polyUVSet(target, q=1, currentUVSet=1)[0]
        if transfer_method == 0:
            cmds.transferAttributes(soure, target, flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace=UVsetA,
                                    searchMethod=3,
                                    transferNormals=0, transferColors=2, targetUvSpace=UVsetB, colorBorders=1,
                                    sampleSpace=5)
            # cmds.warning('按拓扑传递UV完成')
        if transfer_method == 1:
            cmds.transferAttributes(flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace=str(UVsetA),
                                    searchMethod=3,
                                    transferNormals=0, transferColors=2, targetUvSpace=str(UVsetB), colorBorders=1,
                                    sampleSpace=0)
        cmds.warning('按位置传递UV完成')
        cmds.select(target, r=1)
        cmds.DeleteHistory()

    # 获取并返回当前选择模型结构数据(api 2.0)
    # sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group
    '''def get_mesh_structure_2(self, model_name):
        # 将名称转换为 MObject
        sel = om.MSelectionList()
        sel.add(model_name)
        mobject = sel.getDependNode(0)
        # 检查是否是 transform 节点
        if not mobject.hasFn(om.MFn.kTransform):
            print(f"{model_name} 不是 transform 节点")
            return []

        # 遍历子节点，找到形状节点
        dag_node = om.MFnDagNode(mobject)
        shapes = []
        for i in range(dag_node.childCount()):
            child = dag_node.child(i)
            if child.hasFn(om.MFn.kShape):
                shapes.append(child)
        # print(shapes)

        selectList = om.MGlobal.getActiveSelectionList()
        # print(type(selectList))
        depFn = om.MFnDependencyNode()
        for i in range(selectList.length()):
            # node = selectList.getDependNode(i)
            node = shapes[0]
            type_syr = node.apiTypeStr
            # print("Type: %s" % type_syr)
            if type_syr == "kMesh":
                depFn.setObject(node)

                name = depFn.name()
                # print("Name: %s" % name)

                # 如果是网格，则创建MFnMesh对象以访问网格数据
                mesh_fn = om.MFnMesh(node)
                # 获取网格的顶点数
                num_verts = mesh_fn.numVertices
                # 获取网格的面数
                num_faces = mesh_fn.numPolygons
                # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

                # 创建一个列表来存储顶点位置
                vertex_positions = []
                # 遍历所有顶点并获取它们的位置
                for i in range(num_verts):
                    point = mesh_fn.getPoint(i)
                    vertex_positions.append([point.x, point.y, point.z])
                # print('点：', vertex_positions)

                # 获取平滑组
                # selection_list = om.MSelectionList()
                # selection_list.add(name)
                # dag_path = selection_list.getDagPath(0)
                # line_3 = om.MItMeshEdge(dag_path)
                # smooth_group = []
                # while not line_3.isDone():
                #     # print(line_3.index())
                #     # print(line_3.isSmooth)
                #     if not line_3.isSmooth == True:
                #         smooth_group.append(line_3.index())
                #     line_3.next()

                line = cmds.ls(name + '.e[*]', fl=1)
                smooth_group = []
                for i in range(len(line)):
                    is_smooth = mesh_fn.isEdgeSmooth(i)
                    if is_smooth == False:
                        smooth_group.append(i)

                # mesh_fn.polygonSmoothingGroupID(0)
                # smooth = mesh_fn.getSmoothMeshDisplayOptions()
                # smooth = cmds.polySoftEdge('pCube1.e[0]',q=True,a=True)
                # smooth = cmds.polyInfo('pCube1.f[0]', smoothingGroupID=True)
                # print(smooth)
                # print('平滑组：', smooth.smoothness)

                # 获取线
                # a = [('polySurface1.f[0]'),('polySurface1.f[1]')]
                # dag_path_2 = a[0].getDagPath(0)
                # iterator = om.MItMeshPolygon(dag_path_2)
                # edges = iterator.getEdges()
                # print(edges)

                # 获取顶法线数组
                normals = mesh_fn.getVertexNormals(False)
                # 获取顶点法线数值数组
                vertex_normals = []
                for i in range(num_verts):
                    normal_vec = normals[i]
                    vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
                # print('法线：', vertex_normals)

                # 获取uv集
                uv_set = mesh_fn.getUVSetNames()

                # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
                uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
                # print('U：', uv_coords_us)
                # print('V：', uv_coords_vs)
                # 遍历面并建立
                all_topology = []
                for i in range(num_faces):
                    # 按面获取拓扑
                    topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                    topology = cmds.ls(topology, fl=1)
                    all_uv_num = []
                    for j in range(len(topology)):
                        # 按拓扑获取uv
                        uv = cmds.polyListComponentConversion(topology[j], tv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num.append(num)
                    all_topology.append(all_uv_num)
                # print('拓扑', all_topology)

                all_uv_topology = []
                for i in range(num_faces):
                    # 按面获取拓扑
                    topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                    topology = cmds.ls(topology, fl=1)
                    all_uv_num = []
                    for j in range(len(topology)):
                        # 按拓扑获取uv
                        uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num.append(num)
                    all_uv_topology.append(all_uv_num)
                # 重新选择回当前选择
                # print('已获取当前选择模型结构数据。')
                # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
                return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group'''

    def get_mesh_structure_2(self, model_name):
        # 将名称转换为 MObject
        sel = om.MSelectionList()
        sel.add(model_name)
        mobject = sel.getDependNode(0)
        # 检查是否是 transform 节点
        if not mobject.hasFn(om.MFn.kTransform):
            print(f"{model_name} 不是 transform 节点")
            return []

        # 遍历子节点，找到形状节点
        dag_node = om.MFnDagNode(mobject)
        shape_names = []
        for i in range(dag_node.childCount()):
            child = dag_node.child(i)
            if child.hasFn(om.MFn.kShape):
                # shapes.append(child)
                # 关键：将 MObject 转换为节点名称
                shape_fn = om.MFnDependencyNode(child)
                shape_name = shape_fn.name()
                shape_names.append(shape_name)
                # print(shapes)
                if shape_names:
                    cmds.select(shape_names, replace=True)  # ✅ 替换当前选择

        selectList = om.MGlobal.getActiveSelectionList()
        # print(type(selectList))
        depFn = om.MFnDependencyNode()
        for i in range(selectList.length()):
            node = selectList.getDependNode(i)
            type_syr = node.apiTypeStr
            # print("Type: %s" % type_syr)
            if type_syr == "kMesh":
                depFn.setObject(node)
                # types = om.MGlobal.getFunctionSetList(node)
                name = depFn.name()
                print("Name: %s" % name)

                # 从选择列表中获取第i个被选对象的DAG路径
                dag_path = selectList.getDagPath(0)
                # 获取节点
                node = dag_path.node()
                # 从选择列表中获取第i个被选对象的DAG路径
                # node = selectList.getDagPath(i)

                # 检查节点是否为网格
                # node.hasFn(om.MFn.kMesh)

                # 如果是网格，则创建MFnMesh对象以访问网格数据
                mesh_fn = om.MFnMesh(node)
                # 获取网格的顶点数
                num_verts = mesh_fn.numVertices
                # 获取网格的面数
                num_faces = mesh_fn.numPolygons
                # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

                # 创建一个列表来存储顶点位置
                vertex_positions = []
                # 遍历所有顶点并获取它们的位置
                for i in range(num_verts):
                    point = mesh_fn.getPoint(i)
                    vertex_positions.append([point.x, point.y, point.z])
                # print('点：', vertex_positions)

                # 获取平滑组
                # selection_list = om.MSelectionList()
                # selection_list.add(name)
                # dag_path = selection_list.getDagPath(0)
                # line_3 = om.MItMeshEdge(dag_path)
                # smooth_group = []
                # while not line_3.isDone():
                #     # print(line_3.index())
                #     # print(line_3.isSmooth)
                #     if not line_3.isSmooth == True:
                #         smooth_group.append(line_3.index())
                #     line_3.next()

                line = cmds.ls(name + '.e[*]', fl=1)
                smooth_group = []
                for i in range(len(line)):
                    is_smooth = mesh_fn.isEdgeSmooth(i)
                    if is_smooth == False:
                        smooth_group.append(i)

                # mesh_fn.polygonSmoothingGroupID(0)
                # smooth = mesh_fn.getSmoothMeshDisplayOptions()
                # smooth = cmds.polySoftEdge('pCube1.e[0]',q=True,a=True)
                # smooth = cmds.polyInfo('pCube1.f[0]', smoothingGroupID=True)
                # print(smooth)
                # print('平滑组：', smooth.smoothness)

                # 获取线
                # a = [('polySurface1.f[0]'),('polySurface1.f[1]')]
                # dag_path_2 = a[0].getDagPath(0)
                # iterator = om.MItMeshPolygon(dag_path_2)
                # edges = iterator.getEdges()
                # print(edges)

                # 获取顶法线数组
                normals = mesh_fn.getVertexNormals(False)
                # 获取顶点法线数值数组
                vertex_normals = []
                for i in range(num_verts):
                    normal_vec = normals[i]
                    vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
                # print('法线：', vertex_normals)

                # 获取uv集
                uv_set = mesh_fn.getUVSetNames()

                # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
                uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
                # print('U：', uv_coords_us)
                # print('V：', uv_coords_vs)
                # 遍历面并建立
                all_uv_topology = []
                all_topology = []
                '''
                for i in range(num_faces):
                    # 按面获取拓扑
                    topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                    topology = cmds.ls(topology, fl=1)
                    all_uv_num_1 = []
                    all_uv_num_2 = []
                    for j in range(len(topology)):
                        # 按拓扑获取点
                        uv = cmds.polyListComponentConversion(topology[j], tv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num_1.append(num)
                        # 按拓扑获取uv
                        uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num_2.append(num)

                    all_topology.append(all_uv_num_1)
                    all_uv_topology.append(all_uv_num_2)'''
                # 使用面迭代器遍历
                face_iter = om.MItMeshPolygon(dag_path)
                while not face_iter.isDone():
                    # 获取当前面的顶点索引 [v0, v1, v2, ...]
                    face_vert_indices = face_iter.getVertices()
                    all_topology.append(face_vert_indices)

                    # 获取当前面的UV索引 [uv0, uv1, uv2, ...]
                    face_uv_indices = []
                    for i in range(len(face_vert_indices)):
                        uv_index = face_iter.getUVIndex(i)  # 按顶点顺序获取UV索引
                        face_uv_indices.append(uv_index)
                    all_uv_topology.append(face_uv_indices)

                    face_iter.next()  # 移动到下一个面
                # print('拓扑', all_topology)

                # all_uv_topology = []
                # for i in range(num_faces):
                #     # 按面获取拓扑
                #     topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                #     topology = cmds.ls(topology, fl=1)
                #     all_uv_num = []
                #     for j in range(len(topology)):
                #
                #     all_uv_topology.append(all_uv_num)
                # 重新选择回当前选择
                print('已获取当前选择模型结构数据。')
                # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
                return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group
    # 创建网格
    def creare_mesh(self, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs,all_uv_topology, smooth_group):
        # print(vertex_positions)
        # print(vertex_normals)
        # print(all_topology)
        # print(uv_coords_us)
        # print(uv_coords_vs)
        # print(all_uv_topology)
        # print(smooth_group)
        # 顶点位置
        vertices = vertex_positions
        # 转换为OM类型
        vertex_positions = []
        for vertex in vertices:
            vertex_positions.append(om.MPoint(vertex[0], vertex[1], vertex[2]))

        # 每个面所含的顶点数量
        face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
        for f in all_topology:
            face_counts.append(len(f))

        # 每个面的顶点索引
        face_connects = []
        for face in all_topology:
            for index in face:
                face_connects.append(index)

        # print(vertex_positions)
        # print(face_counts)
        # # print(face_connects)
        # 创建网格
        mesh_fn = om.MFnMesh()
        mesh_obj = mesh_fn.create(vertex_positions, face_counts, face_connects, uv_coords_us, uv_coords_vs)

        # print(all_uv_topology)
        uv_face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
        for f in all_uv_topology:
            uv_face_counts.append(len(f))
        uvIds = [item for sublist in all_uv_topology for item in sublist]
        # print(len(uvIds), uvIds)
        # 设置UV
        mesh_uv = mesh_fn.assignUVs(uv_face_counts, uvIds)

        # 设置法线
        # print(vertex_normals)
        normals = []
        for vertex in vertex_normals:
            normals.append(om.MVector(vertex[0], vertex[1], vertex[2]))
        # print(normals)
        normals_indices = []
        for i in range(len(normals)):
            normals_indices.append(i)
        mesh_fn.setVertexNormals(normals, normals_indices)

        # 设置平滑组
        name = mesh_fn.name()
        # 建立平滑组选集
        smooth_line = []
        if smooth_line:
            for i in smooth_group:
                smooth_line.append(name + '.e[' + str(i) + ']')
            # print('平滑组：',smooth_line)
            # print('平滑组：',smooth_group)
            cmds.polySoftEdge(smooth_line, a=0, ch=0)
        # 冻结当前法线
        cmds.polyNormalPerVertex(name, ufn=1)

        # # 创建一个新的变换节点作为网格的父节点
        # dep_fn = om.MFnDependencyNode()
        # transform_obj = om.MFnTransform().create()
        # dep_fn.setObject(transform_obj)
        #
        # # 将网格附加到变换节点上
        # # 注意：在 Maya 中，网格节点通常不是直接创建的，而是作为变换节点的子节点创建的
        # # 但由于我们使用的是底层 API，这里我们手动创建一个变换节点，并将网格对象附加到它上面
        # # 在 UI 中，这通常是通过在“大纲视图”中拖动网格到变换节点下来完成的
        # # 但在底层 API 中，我们需要使用 MDagModifier 来完成这个操作
        # dag_modifier = om.MDagModifier()
        # dag_modifier.reparentNode(mesh_obj, transform_obj)
        # dag_modifier.doIt()

        # 清理
        # del dag_modifier
        return name

    # 为模型赋予材质
    def assign_material(self, mesh_shape, material_type, have_material):
            # 尝试获取模型的着色组
            shading_groups = cmds.listConnections(mesh_shape[0] + '.instObjGroups', shapes=True) or []
            if not shading_groups:
                # 则创建一个新的着色组
                shading_groups = cmds.shadingNode('shadingEngine', asUtility=1, n=mesh_shape[0] + '_SG')
                # 链接模型和材质组
                cmds.connectAttr((mesh_shape[0] + '.instObjGroups[0]'), (shading_groups + '.dagSetMembers[0]'), force=1)
            else:
                # 如果存在多个着色组，通常我们只关心第一个
                shading_groups = shading_groups[0]
            if have_material:
                shader_name = have_material[0]
            else:
                # 创建一个材质
                shader_name = cmds.shadingNode(material_type, asShader=True, name=mesh_shape[0] + '_material')
                # print(shader_name)
            # 连接材质和着色组
            cmds.connectAttr((shader_name + '.outColor'), (shading_groups + '.surfaceShader'), force=1)
            return shader_name

    # 获取模型uv边界对应的边
    def get_uv_borders(self, objects):
        # 获取所有网格边
        mesh_edges = []
        for obj in objects:
            try:
                edges = cmds.polyListComponentConversion(obj, toEdge=True)
                mesh_edges.extend(cmds.ls(edges, fl=True, l=True))
            except:
                pass

        if not mesh_edges:
            raise RuntimeError("未选中有效网格对象")

        uv_border_edges = []
        # 遍历每条边
        for edge in mesh_edges:
            # 获取该边关联的 UV 点
            edge_uvs = cmds.polyListComponentConversion(edge, toUV=True)
            edge_uvs = cmds.ls(edge_uvs, fl=True) if edge_uvs else []

            # 获取该边关联的面
            edge_faces = cmds.polyListComponentConversion(edge, toFace=True)
            edge_faces = cmds.ls(edge_faces, fl=True) if edge_faces else []

            # 判断逻辑：UV 数量 > 2 或 关联面数 < 2
            if len(edge_uvs) > 2 or len(edge_faces) < 2:
                uv_border_edges.append(edge)

        return uv_border_edges

    # 创建按uv打平的模型
    def create_flattened_model(self, sel):
        sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = self.get_mesh_structure_2(sel)
        # 将模型的点数据转换成uv数据，z轴数值为o
        point = cmds.ls(sel + '.vtx[*]', fl=1)
        uv_with_point = []
        for i in range(len(vertex_positions)):
            uv_points = cmds.polyListComponentConversion(point[i], fromVertex=True, toUV=True)
            uv_points = cmds.filterExpand(uv_points, sm=35)[0]  # 过滤为 UV 组件[4](@ref)
            num = int(uv_points.split('[')[1].split(']')[0])
            list = [i, num]
            uv_with_point.append(list)
            vertex_positions[i][0] = uv_coords_us[num]
            vertex_positions[i][1] = uv_coords_vs[num]
            vertex_positions[i][2] = 0.0
            vertex_normals[i][0] = 0
            vertex_normals[i][1] = 0
            vertex_normals[i][2] = 1


        mesh = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology,
                           smooth_group)
        if cmds.objExists('lambert1'):
            cmds.select(mesh)
            cmds.hyperShade(assign='lambert1')
        print('生成的模型1：', mesh)
        return mesh, uv_with_point

    # 按uv建立模型
    def create_uv_model(self, sel):
        cmds.select(self.get_uv_borders(cmds.ls(sl=1)))
        cmds.undoInfo(ock=1)
        cmds.DetachComponent()
        sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = self.get_mesh_structure_2(sel)
        # 将模型的点数据转换成uv数据，z轴数值为o
        # point = cmds.ls(sel + '.vtx[*]', fl=1)
        for i in range(len(vertex_positions)):
            # uv_points = cmds.polyListComponentConversion(point[i], fromVertex=True, toUV=True)
            # uv_points = cmds.filterExpand(uv_points, sm=35)[0]  # 过滤为 UV 组件[4](@ref)
            # num = int(uv_points.split('[')[1].split(']')[0])
            vertex_positions[i][0] = uv_coords_us[i]
            vertex_positions[i][1] = uv_coords_vs[i]
            vertex_positions[i][2] = 0.0
            vertex_normals[i][0] = 0
            vertex_normals[i][1] = 0
            vertex_normals[i][2] = 1

        mesh = self.creare_mesh(vertex_positions, vertex_normals, all_uv_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group)
        if cmds.objExists('lambert1'):
            cmds.select(mesh)
            cmds.hyperShade(assign='lambert1')
        print('生成的模型1：', mesh)
        return mesh