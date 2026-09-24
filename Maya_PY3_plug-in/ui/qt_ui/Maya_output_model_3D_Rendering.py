# coding=gbk
import maya.cmds as cmds
import maya.mel as mel
maya_useNewAPI = True
import maya.api.OpenMaya as om
import mmap
import os
import pickle


def write_to_shared_memory(data,shared_file=os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem.bin")):
    # 使用pickle序列化数据（更可靠）
    data_bytes = pickle.dumps(data)
    data_size = len(data_bytes)
    total_size = 4 + data_size  # 头部4字节 + 数据本身

    print(f"数据大小: {data_size} 字节, 需要分配: {total_size} 字节")

    with open(shared_file, "wb") as f:
        # 分配足够的空间：头部4字节 + 数据本身
        f.write(b'\x00' * total_size)

    with open(shared_file, "r+b") as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            # 确保有足够空间
            if len(mm) < total_size:
                raise ValueError(f"内存映射大小不足: {len(mm)} < {total_size}")

            mm.seek(0)
            # 写入数据长度（4字节）
            mm.write(data_size.to_bytes(4, byteorder='big'))
            # 写入实际数据
            mm.write(data_bytes)
            mm.flush()

    print(f"数据写入成功，总共写入 {total_size} 字节")
# 获取maya模型数据
def get_mesh_structure1(model_name):
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
                cmds.select(shape_names, replace=True)  # ? 替换当前选择

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
            vertices = vertex_positions
            normal_list = [list(mintarray) for mintarray in all_topology]
            faces = normal_list
            list1 = uv_coords_us
            list2 = uv_coords_vs
            combined_list = list(zip(list1, list2))
            return vertices, faces, combined_list
            # return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group

def get_mesh_structure(model_name):
    # 将名称转换为 MObject
    # 1. 通过名称获取 MObject
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

    # 创建选择列表获取形状节点的MObject
    shape_sel = om.MSelectionList()
    shape_sel.add(shape_names[0])
    shape_mobject = shape_sel.getDependNode(0)
    # 获取DAG路径用于面迭代器
    dag_path = om.MDagPath.getAPathTo(shape_mobject)

    # 如果是网格，则创建MFnMesh对象以访问网格数据
    mesh_fn = om.MFnMesh(shape_mobject)
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

    print('已获取当前选择模型结构数据。')
    # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
    vertices = vertex_positions
    normal_list = [list(mintarray) for mintarray in all_topology]
    faces = normal_list
    list1 = uv_coords_us
    list2 = uv_coords_vs
    combined_list = list(zip(list1, list2))
    return vertices, faces, combined_list, vertex_normals
    # return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group
# name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = get_mesh_structure('pSphere1')
vertices, faces, combined_list, vertex_normals= get_mesh_structure('pPlane1')  #pPlane1 Gauntlet11
vertices_1, faces_1, combined_list_1, vertex_normals_1= get_mesh_structure('pSphere1')
print(vertices, faces, combined_list)
write_to_shared_memory([vertices, faces, combined_list, vertex_normals], shared_file=os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pPlane1', "model_data.bin"))
write_to_shared_memory([vertices_1, faces_1, combined_list_1, vertex_normals_1], shared_file=os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pSphere1', "model_data.bin"))