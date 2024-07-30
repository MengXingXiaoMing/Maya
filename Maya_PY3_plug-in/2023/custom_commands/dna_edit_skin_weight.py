#coding=gbk
from os import makedirs
from os import path as ospath
import maya.cmds as cmds
from sys import path as syspath
from sys import platform
import os
import inspect
import maya.OpenMaya as om

import time

# 记录开始时间
start_time = time.time()
# 版本号
maya_version = cmds.about(version=True)
#################################################################################################
# 请手动修改以下路径，都是默认的话就不用改了
reader = []
writer = []
if maya_version == '2022' or maya_version == '2023':
# 文件路径
    file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    # print('路径:',file_path)
    ROOT_DIR = file_path + '/MetaHuman-DNA-Calibration-main'
    MAYA_VERSION = maya_version  # 2022 or 2023
    ROOT_LIB_DIR = f"{ROOT_DIR}/lib/Maya{MAYA_VERSION}"
    if platform == "win32":
        LIB_DIR = f"{ROOT_LIB_DIR}/windows"
    elif platform == "linux":
        LIB_DIR = f"{ROOT_LIB_DIR}/linux"
    else:
        raise OSError(
            "OS not supported, please compile dependencies and add value to LIB_DIR"
        )
    # Adds directories to path
    syspath.insert(0, ROOT_DIR)
    syspath.insert(0, LIB_DIR)
    from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter

    flie = f"{ROOT_DIR}/data/mh4/dna_files/Ada.dna"
    stream = FileStream(flie, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    flie = f"{ROOT_DIR}/data/mh4/dna_files/Ada_modify.dna"
    stream = FileStream(flie, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
else:
    print("Maya版本错误,仅支持2022和2023版本，如尝试再别的版本请自行修改。")
#################################################################################################
def edit_joint_weight():
    # 获取模型数量
    getMeshCount = reader.getMeshCount()
    print('getMeshCount:' + str(getMeshCount))
    # 获取骨骼数量
    getJointCount = reader.getJointCount()
    print('getJointCount:' + str(getJointCount))
    # 对每个模型逐个开始修改
    for i in range(getMeshCount):
    # for i in [0]:
        # 获取模型名称
        getMeshName = reader.getMeshName(i)
        print('getMeshName:' + str(getMeshName))
        #获取蒙皮节点
        history = cmds.listHistory(getMeshName)
        skinClusterName = ''
        for node in history:
            if cmds.nodeType(node) == 'skinCluster':
                skinClusterName = node
                break
        cmds.RemoveUnusedInfluences(skinClusterName)
        # 获取受影响的骨骼
        source_skin_joint = cmds.skinCluster(getMeshName, q=1, inf=1)
        print(len(source_skin_joint), source_skin_joint)
        # 获取模型点数量
        getSkinWeightsCount = reader.getSkinWeightsCount(i)
        print('getSkinWeightsCount:' + str(getSkinWeightsCount))
        # 获取模型点列表
        mesh_visit_list = cmds.ls(getMeshName+'.vtx[*]',fl=1)
        print(len(mesh_visit_list), mesh_visit_list)
        # 按点获取权重创建修改列表
        clearSkinWeights = writer.clearSkinWeights(i)
        print('clearSkinWeights:' + str(clearSkinWeights))
        # 获取其影响的骨骼在所有骨骼中的指针位置
        joint_index_list = []
        for k in range(getJointCount):
            getJointName = reader.getJointName(k)
            for l in range(len(source_skin_joint)):
                if source_skin_joint[l] == getJointName:
                    joint_index_list.append(k)
        print(len(joint_index_list), joint_index_list)
        # 开始逐个点修改
        for j in range(getSkinWeightsCount):
            weight_list = []
            joint_list = []
            # 获取每个骨骼在某个点的权重数值
            weight = cmds.skinPercent(skinClusterName, mesh_visit_list[j],  q=True, v=True)
            # 将有数值的骨骼和其数值加载到新列表
            for w in range(len(weight)):
                if weight[w] > 0:
                    joint_list.append(joint_index_list[w])
                    weight_list.append(weight[w])
            writer.setSkinWeightsJointIndices(i, j, joint_list)
            writer.setSkinWeightsValues(i, j, weight_list)
# edit_joint_weight()
print('###################################')
getMeshCount = reader.getMeshCount()
print('getMeshCount:' + str(getMeshCount))
getMeshName = reader.getMeshName(0)
print('getMeshName:' + str(getMeshName))
getMeshIndexListCount = reader.getMeshIndexListCount()
print('getMeshIndexListCount:' + str(getMeshIndexListCount))
getVertexPositionCount = reader.getVertexPositionCount(0)
print('getVertexPositionCount:' + str(getVertexPositionCount))
getVertexPosition = reader.getVertexPosition(0,0)
print('getVertexPosition:' + str(getVertexPosition))
getVertexTextureCoordinateCount = reader.getVertexTextureCoordinateCount(0)
print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
getVertexTextureCoordinate = reader.getVertexTextureCoordinate(0,2)
print('getVertexTextureCoordinate:2' + str(getVertexTextureCoordinate))
getVertexTextureCoordinate = reader.getVertexTextureCoordinate(0,12025)
print('getVertexTextureCoordinate:12025' + str(getVertexTextureCoordinate))
getVertexTextureCoordinateUs = reader.getVertexTextureCoordinateUs(0)
print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))
getVertexTextureCoordinateVs = reader.getVertexTextureCoordinateVs(0)
print('getVertexTextureCoordinateVs:' + str(getVertexTextureCoordinateVs))
getVertexNormalCount = reader.getVertexNormalCount(0)
print('getVertexNormalCount:' + str(getVertexNormalCount))
getVertexNormal = reader.getVertexNormal(0,0)
print('getVertexNormal:' + str(getVertexNormal))
getVertexLayoutCount = reader.getVertexLayoutCount(0)
print('getVertexLayoutCount:' + str(getVertexLayoutCount))
getVertexLayout = reader.getVertexLayout(0,0)
print('getVertexLayout:' + str(getVertexLayout))
getVertexLayout = reader.getVertexLayout(0,12071)
print('getVertexLayout:' + str(getVertexLayout))
getVertexLayout = reader.getVertexLayout(0,24177)
print('getVertexLayout:' + str(getVertexLayout))
getVertexLayoutPositionIndices = reader.getVertexLayoutPositionIndices(0)
print('getVertexLayoutPositionIndices:' + str(len(getVertexLayoutPositionIndices)) + str(getVertexLayoutPositionIndices))
print(getVertexLayoutPositionIndices[12071])
print(getVertexLayoutPositionIndices[24177])
getVertexLayoutTextureCoordinateIndices = reader.getVertexLayoutTextureCoordinateIndices(0)
print('getVertexLayoutTextureCoordinateIndices:' + str(len(getVertexLayoutTextureCoordinateIndices)) + str(getVertexLayoutTextureCoordinateIndices))
print(getVertexLayoutTextureCoordinateIndices[12071])
print(getVertexLayoutTextureCoordinateIndices[24177])
getVertexLayoutNormalIndices = reader.getVertexLayoutNormalIndices(0)
print('getVertexLayoutNormalIndices:' + str(getVertexLayoutNormalIndices))
print(getVertexLayoutNormalIndices[12071])
print(getVertexLayoutNormalIndices[24177])
getFaceCount = reader.getFaceCount(0)
print('getFaceCount:' + str(getFaceCount))
getFaceVertexLayoutIndices = reader.getFaceVertexLayoutIndices(0,0)
print('getFaceVertexLayoutIndices:' + str(getFaceVertexLayoutIndices))
getMaximumInfluencePerVertex = reader.getMaximumInfluencePerVertex(0)
print('getMaximumInfluencePerVertex:' + str(getMaximumInfluencePerVertex))
getBlendShapeTargetCount = reader.getBlendShapeTargetCount(0)
print('getBlendShapeTargetCount:' + str(getBlendShapeTargetCount))
getBlendShapeChannelIndex = reader.getBlendShapeChannelIndex(0,0)
print('getBlendShapeChannelIndex:' + str(getBlendShapeChannelIndex))
getBlendShapeTargetDeltaCount = reader.getBlendShapeTargetDeltaCount(0,0)
print('getBlendShapeTargetDeltaCount:' + str(getBlendShapeTargetDeltaCount))
getBlendShapeTargetDelta = reader.getBlendShapeTargetDelta(0,0,0)
print('getBlendShapeTargetDelta:' + str(getBlendShapeTargetDelta))
getBlendShapeTargetVertexIndices = reader.getBlendShapeTargetVertexIndices(0,0)
print('getBlendShapeTargetVertexIndices:' + str(len(getBlendShapeTargetVertexIndices)) + str(getBlendShapeTargetVertexIndices))
def get_mesh_topology():
    selLis = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selLis)
    result = [om.MObject()] * 1
    selLis.getDependNode(0, result[0])
    dep_node_fn = om.MFnDependencyNode(result[0])
    # 现在你可以使用dep_node_fn来获取更多关于节点的信息
    print(dep_node_fn.name())  # 打印节点名称
    print(dep_node_fn.typeName())  # 打印节点类型

    # 创建一个空的MSelectionList对象
    selLis = om.MSelectionList()
    # 获取当前选择并填充到selLis中
    om.MGlobal.getActiveSelectionList(selLis)
    # 遍历选择列表中的每个项目
    for i in range(selLis.length()):
        # 为每个选中的对象创建一个新的MDagPath实例
        dag_path = [om.MDagPath()] * selLis.length()
        # 从选择列表中获取第i个被选对象的DAG路径
        selLis.getDagPath(i, dag_path[i])
        # 获取节点
        node = dag_path[i].node()
        # 检查节点是否为网格
        if node.hasFn(om.MFn.kMesh):
            print('是网格')
            # 如果是网格，则创建MFnMesh对象以访问网格数据
            mesh_fn = om.MFnMesh(node)
            # 现在可以使用mesh_fn进行网格相关的操作了
            print(f"Found mesh: {dag_path[i].fullPathName()}")
            # 获取并打印网格的顶点数和面数
            num_verts = mesh_fn.numVertices()
            num_faces = mesh_fn.numPolygons()
            print(f"Mesh has {num_verts} vertices and {num_faces} faces.")
            # 获取顶点数和法线数组
            normals = om.MFloatVectorArray()
            mesh_fn.getVertexNormals(False, normals)
            # 打包结果
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
            print(vertex_normals[0])
            # 遍历面并打印顶点索引
            face_vertices = om.MIntArray()
            mesh_fn.getPolygonVertices(0, face_vertices)
            face_vertex_indices = [face_vertices[j] for j in range(face_vertices.length())]
            print(f"Face {0} vertices: {face_vertex_indices}")

            uv_set = []
            mesh_fn.getUVSetNames(uv_set)

            # 创建一个MFloatArray来存储UV坐标
            uv_coords_1 = om.MFloatArray()
            uv_coords_2 = om.MFloatArray()
            # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
            # 注意：在Python中，你不需要传递引用，因为Python使用的是引用传递
            status = mesh_fn.getUVs(uv_coords_1, uv_coords_2, uv_set[0])
            # UV坐标是成对出现的（u, v），所以我们需要以对的形式来访问它们
            num_uvs = uv_coords_1.length()  # 因为每个UV点有两个坐标：u和v
            # for i in range(num_uvs):
            for i in [0,1,12025,12205]:
                u = uv_coords_1[i]
                v = uv_coords_2[i]
                print(f"UV {i}: ({u}, {v})")
        else:
            print(f"Selected item {i} is not a mesh: {dag_path[i].fullPathName()}")
def set_md(meshIndex):
    set_point_positions(meshIndex)
    writer.setMaximumInfluencePerVertex(meshIndex, maxInfluenceCount)
    writer.clearSkinWeights(meshIndex)
    writer.setSkinWeightsValues(meshIndex, vertexIndex, weights)
    writer.setSkinWeightsJointIndices(meshIndex, vertexIndex, jointIndices)
    writer.clearBlendShapeTargets(meshIndex)
    writer.setBlendShapeChannelIndex(meshIndex, blendShapeTargetIndex, blendShapeChannelIndex)
    writer.setBlendShapeTargetDeltas(meshIndex, blendShapeTargetIndex, deltas)
    writer.setBlendShapeTargetVertexIndices(meshIndex, blendShapeTargetIndex, vertexIndices)
def set_point_positions(meshIndex):
    # 设置点位置
    writer.setVertexPositions(meshIndex, positions)
    # 设置点UV位置
    writer.setVertexTextureCoordinates(meshIndex, textureCoordinates)
    # 设置点法线
    writer.setVertexNormals(meshIndex, normals)
    # 设置点、uv点、点法线排列
    writer.setVertexLayouts(meshIndex, layouts)
    # 清理拓扑（面）
    writer.clearFaceVertexLayoutIndices(meshIndex)
    # 设置拓扑（面）
    writer.setFaceVertexLayoutIndices(meshIndex, faceIndex, layoutIndices)
    pass
def create_dna():

    # writer.write()  # 写入数据
    print('写入新文件完毕')
    print('已经全部运行，请加载新dna查看效果')
create_dna()
###############################################################################################
end_time = time.time()
# 计算并打印耗时
elapsed_time = end_time - start_time
print(f"操作耗时: {elapsed_time} 秒")