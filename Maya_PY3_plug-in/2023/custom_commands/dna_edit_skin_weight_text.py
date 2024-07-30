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

# ��¼��ʼʱ��
start_time = time.time()
# �汾��
maya_version = cmds.about(version=True)
#################################################################################################
# ���ֶ��޸�����·��������Ĭ�ϵĻ��Ͳ��ø���
reader = []
writer = []
if maya_version == '2022' or maya_version == '2023':
# �ļ�·��
    file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    # print('·��:',file_path)
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
    print("Maya�汾����,��֧��2022��2023�汾���糢���ٱ�İ汾�������޸ġ�")
#################################################################################################
def edit_joint_weight():
    # ��ȡģ������
    getMeshCount = reader.getMeshCount()
    print('getMeshCount:' + str(getMeshCount))
    # ��ȡ��������
    getJointCount = reader.getJointCount()
    print('getJointCount:' + str(getJointCount))
    # for i in range(getMeshCount):
    #     getMeshName = reader.getMeshName(i)
    #     print('getMeshName:' + str(getMeshName))
    # getMeshIndexListCount = reader.getMeshIndexListCount()
    # print('getMeshIndexListCount:' + str(getMeshIndexListCount))
    # getMeshIndicesForLOD = reader.getMeshIndicesForLOD(0)
    # print('getMeshIndexListCount:' + str(getMeshIndicesForLOD))
    # ��ÿ��ģ�������ʼ�޸�
    for i in range(getMeshCount):
    # for i in [0]:
        # ��ȡģ������
        getMeshName = reader.getMeshName(i)
        print('getMeshName:' + str(getMeshName))
        #��ȡ��Ƥ�ڵ�
        history = cmds.listHistory(getMeshName)
        skinClusterName = ''
        for node in history:
            if cmds.nodeType(node) == 'skinCluster':
                skinClusterName = node
                break
        cmds.RemoveUnusedInfluences(skinClusterName)
        # ��ȡ��Ӱ��Ĺ���
        source_skin_joint = cmds.skinCluster(getMeshName, q=1, inf=1)
        print(len(source_skin_joint), source_skin_joint)
        # ��ȡģ�͵�����
        getSkinWeightsCount = reader.getSkinWeightsCount(i)
        print('getSkinWeightsCount:' + str(getSkinWeightsCount))
        # ��ȡģ�͵��б�
        mesh_visit_list = cmds.ls(getMeshName+'.vtx[*]',fl=1)
        print(len(mesh_visit_list), mesh_visit_list)
        # �����ȡȨ�ش����޸��б�
        clearSkinWeights = writer.clearSkinWeights(i)
        print('clearSkinWeights:' + str(clearSkinWeights))
        # ��ȡ��Ӱ��Ĺ��������й����е�ָ��λ��
        joint_index_list = []
        for k in range(getJointCount):
            getJointName = reader.getJointName(k)
            for l in range(len(source_skin_joint)):
                if source_skin_joint[l] == getJointName:
                    joint_index_list.append(k)
        print(len(joint_index_list), joint_index_list)
        # ��ʼ������޸�
        for j in range(getSkinWeightsCount):
            weight_list = []
            joint_list = []
            # ��ȡÿ��������ĳ�����Ȩ����ֵ
            weight = cmds.skinPercent(skinClusterName, mesh_visit_list[j],  q=True, v=True)
            # ������ֵ�Ĺ���������ֵ���ص����б�
            for w in range(len(weight)):
                if weight[w] > 0:
                    joint_list.append(joint_index_list[w])
                    weight_list.append(weight[w])
            # print(j, '/', getSkinWeightsCount)
            # ��ʼ�����޸�Ȩ��

            # print(joint_list)
            # print(weight_list)
            writer.setSkinWeightsJointIndices(i, j, joint_list)
            writer.setSkinWeightsValues(i, j, weight_list)
        # for j in range(getSkinWeightsCount):
        #     for i in range(getJointCount):
        #         # ��ȡ��������
        #         getJointName = reader.getJointName(i)
        #         print('getJointName:' + str(getJointName))
        #         joint = cmds.skinPercent(skinClusterName, vertexIndex, getJointName, q=True, v=True)

    # getSkinWeightsValues = reader.getSkinWeightsValues(0, 0)
    # print('getSkinWeightsValues:' + str(getSkinWeightsValues))
    # getSkinWeightsJointIndices = reader.getSkinWeightsJointIndices(0, 0)
    # print('getSkinWeightsJointIndices:' + str(getSkinWeightsJointIndices))


    # for i in range(getSkinWeightsCount):
    #     writer.setSkinWeightsValues(0, i, [1])
    #     writer.setSkinWeightsJointIndices(0, i, [0])

    writer.write()  # д������
    print('д�����ļ����')
    print('�Ѿ�ȫ�����У��������dna�鿴Ч��')
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
    # ���������ʹ��dep_node_fn����ȡ������ڽڵ����Ϣ
    print(dep_node_fn.name())  # ��ӡ�ڵ�����
    print(dep_node_fn.typeName())  # ��ӡ�ڵ�����

    # ����һ���յ�MSelectionList����
    selLis = om.MSelectionList()
    # ��ȡ��ǰѡ����䵽selLis��
    om.MGlobal.getActiveSelectionList(selLis)
    # ����ѡ���б��е�ÿ����Ŀ
    for i in range(selLis.length()):
        # Ϊÿ��ѡ�еĶ��󴴽�һ���µ�MDagPathʵ��
        dag_path = [om.MDagPath()] * selLis.length()
        # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
        selLis.getDagPath(i, dag_path[i])
        # ��ȡ�ڵ�
        node = dag_path[i].node()

        # ���ڵ��Ƿ�Ϊ����
        if node.hasFn(om.MFn.kMesh):
            print('������')
            # ����������򴴽�MFnMesh�����Է�����������
            mesh_fn = om.MFnMesh(node)
            # ���ڿ���ʹ��mesh_fn����������صĲ�����
            print(f"Found mesh: {dag_path[i].fullPathName()}")
            # ��ȡ����ӡ����Ķ�����������
            num_verts = mesh_fn.numVertices()
            num_faces = mesh_fn.numPolygons()
            print(f"Mesh has {num_verts} vertices and {num_faces} faces.")
            # ��ȡ�������ͷ�������
            normals = om.MFloatVectorArray()
            mesh_fn.getVertexNormals(False, normals)
            # ������
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
            print(vertex_normals[0])
            # �����沢��ӡ��������
            face_vertices = om.MIntArray()
            mesh_fn.getPolygonVertices(0, face_vertices)
            face_vertex_indices = [face_vertices[j] for j in range(face_vertices.length())]
            print(f"Face {0} vertices: {face_vertex_indices}")
            # for face_idx in range(num_faces):
            #     face_vertices = om.MIntArray()
            #     mesh_fn.getPolygonVertices(face_idx, face_vertices)
            #     face_vertex_indices = [face_vertices[j] for j in range(face_vertices.length())]
            #     print(f"Face {face_idx} vertices: {face_vertex_indices}")
            # uv_coords = om.MFloatArray()
            point = om.MPoint()
            mesh_fn.getPoint(0, point)
            # print(point.x,point.y, point.z)
            # mesh_fn.getUVs(uv_coords, uv_set)
            # print('uv_coords:',uv_coords)
            # points = om.MFloatPointArray()
            # point = om.MPoint(-0.5, 0.0, 0.5)
            # pArray = [0.0, 0.0]
            # x1 = om.MScriptUtil()
            # x1.createFromList(pArray, 0)
            # uvPoint = x1.asFloat2Ptr()
            # print(uvPoint)
            # uv_set = om.MFloatArray()
            # uvReturn = mesh_fn.getUVAtPoint(point, uvPoint, om.MSpace.kWorld, uv_set, None)
            # u, v, face_id = mesh_fn.getUVAtPoint(point[0], om.MSpace.kObject, uv_set)
            # mesh_fn.getPointAtUV(0,  1.0, 1.0, om.MSpace.kObject, uv_set, 0.0)  # ע�⣺���ﲻ��ҪMSpace��������Ϊ����ֻȡһ����
            # ��������ȡ���㣨��Ȼ������ֻ��һ���㣬��������Ȼ��Ҫ���������ʣ�

            # print(om.MPoint(points[0].x, points[0].y, points[0].z))

            # mesh_fn.getUVAtPoint(point, space=om.MSpace.kObject, uvSet='')  # ͨ��ʹ��MSpace.kWorld��MSpace.kObject������ȡ�����������
            # print(uv_coords)
            # vertex_uvs = []
            # for i in range(0, len(uv_coords), 2):
            #     u = uv_coords[i]
            #     v = uv_coords[i + 1]
            #     # ע�⣺�������Ǽ���ÿ�����㶼��һ��UV���꣬���ڴ�������������ȷ�ģ�
            #     # �����������UV������������㹲����ͬ��UV���꣩����˼�����ܲ�������
            #     # ����������£��������Ҫ�����ӵ��߼���ȷ����Щ���㹲��UV��
            #     vertex_uvs.append((i // 2, (u, v)))  # i // 2 ����Ϊ����ÿ�ε�����������ֵ��u��v��
            # print(vertex_uvs)

            # ָ��UV���ϵ����ƣ����û��ָ������Ĭ��Ϊ��һ��UV���ϣ�����еĻ���
            uv_set = []
            mesh_fn.getUVSetNames(uv_set)

            # ����һ��MFloatArray���洢UV����
            uv_coords_1 = om.MFloatArray()
            uv_coords_2 = om.MFloatArray()
            # ����getUVs����������UV�������ƺ�MFloatArray������
            # ע�⣺��Python�У��㲻��Ҫ�������ã���ΪPythonʹ�õ������ô���
            status = mesh_fn.getUVs(uv_coords_1, uv_coords_2, uv_set[0])
            # UV�����ǳɶԳ��ֵģ�u, v��������������Ҫ�ԶԵ���ʽ����������
            num_uvs = uv_coords_1.length()  # ��Ϊÿ��UV�����������꣺u��v
            # for i in range(num_uvs):
            for i in [0,1,12025,12205]:
                u = uv_coords_1[i]
                v = uv_coords_2[i]
                print(f"UV {i}: ({u}, {v})")
        else:
            print(f"Selected item {i} is not a mesh: {dag_path[i].fullPathName()}")

# get_mesh_topology()
###############################################################################################
# selLis = om.MSelectionList()
# om.MGlobal.getActiveSelectionList(selLis)
# result = [om.MObject()] * 1
# selLis.getDependNode(0, result[0])
# dep_node_fn = om.MFnDependencyNode(result[0])
# # ���������ʹ��dep_node_fn����ȡ������ڽڵ����Ϣ
# print(dep_node_fn.name())  # ��ӡ�ڵ�����
# print(dep_node_fn.typeName())  # ��ӡ�ڵ�����

def listSelectionMObj(index=-1):
    selLis = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selLis)
    if(index < 0):
        result = [om.MObject()] * selLis.length()
        for i, obj in enumerate(result):
            selLis.getDependNode(i, obj)
            return result
    else:
        result = [om.MObject()] * 1
        selLis.getDependNode(0, result[0])
        return result
        # get mdagpath
def listSelectionMPath(index=-1):
    selLis = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selLis)
    if(index < 0):
        result = [om.MDagPath()] * selLis.length()
        for i, path in enumerate(result):
            selLis.getDagPath(i, path)
            return result
    else:
        result = [om.MDagPath()] * 1
        selLis.getDagPath(0, result[0])
        return result

# selLis = om.MSelectionList()
# om.MGlobal.getActiveSelectionList(selLis)
# result = [om.MDagPath()] * selLis.length()
# selLis.getDagPath(0, result[0])
# node = result[0].node()
# node.hasFn(om.MFn.kMesh)
# # ����MFnMesh�����Է�����������
# mesh_fn = om.MFnMesh(node)


# # ����һ���յ�MSelectionList����
# selLis = om.MSelectionList()
#
# # ��ȡ��ǰѡ����䵽selLis��
# om.MGlobal.getActiveSelectionList(selLis)
#
# # ����ѡ���б��е�ÿ����Ŀ
# for i in range(selLis.length()):
#     # Ϊÿ��ѡ�еĶ��󴴽�һ���µ�MDagPathʵ��
#     dag_path = [om.MDagPath()] * selLis.length()
#     # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
#     selLis.getDagPath(i, dag_path[i])
#     # ��ȡ�ڵ�
#     node = dag_path[i].node()
#
#     # ���ڵ��Ƿ�Ϊ����
#     if node.hasFn(om.MFn.kMesh):
#         print('������')
#         # ����������򴴽�MFnMesh�����Է�����������
#         mesh_fn = om.MFnMesh(node)
#         # ���ڿ���ʹ��mesh_fn����������صĲ�����
#         print(f"Found mesh: {dag_path[i].fullPathName()}")
#         # ��ȡ����ӡ����Ķ�����������
#         num_verts = mesh_fn.numVertices()
#         num_faces = mesh_fn.numPolygons()
#         print(f"Mesh has {num_verts} vertices and {num_faces} faces.")
#         # ��ѡ�������沢��ӡ��������
#         for face_idx in range(num_faces):
#             face_vertices = om.MIntArray()
#             mesh_fn.getPolygonVertices(face_idx, face_vertices)
#             face_vertex_indices = [face_vertices[j] for j in range(face_vertices.length())]
#             print(f"Face {face_idx} vertices: {face_vertex_indices}")
#         # ...�����������Ӹ����������Ĳ�����
#     else:
#         print(f"Selected item {i} is not a mesh: {dag_path[i].fullPathName()}")

# # ��ȡ����ӡ����Ķ�����������
# num_verts = mesh_fn.numVertices()
# num_faces = mesh_fn.numPolygons()
# print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

# mobj = listSelectionMObj()[0]
# if mobj.hasFn(om.MFn.kDependencyNode):
#     # ת��ΪMFnDependencyNode
#     dep_node_fn = om.MFnDependencyNode(mobj)
#
#     # ���������ʹ��dep_node_fn����ȡ������ڽڵ����Ϣ
#     print(dep_node_fn.name())  # ��ӡ�ڵ�����
#     print(dep_node_fn.typeName())  # ��ӡ�ڵ�����



# ����һ��Mesh���ݽڵ�
# dagPath = om.MDagPath()
# selList = om.MSelectionList()
# selList.add("head_lod0_mesh")  # �滻Ϊ��Ҫ������ģ������
#
# if selList.getDependNode(0,dagPath):
#     pass
#     meshFn = om.MFnMesh(dagPath)
#
#     # ��ȡ������
#     numVertices = meshFn.numVertices()
#     print(f"������: {numVertices}")
#
#     # ��ȡ����
#     numEdges = meshFn.numEdges()
#     print(f"����: {numEdges}")
#
#     # ��ȡ����
#     numFaces = meshFn.numPolygons()
#     print(f"����: {numFaces}")
#
#     # �����Ҫ�������������Ϣ�����������б����Ա���faceIds
#     faceIds = meshFn.getPolygonVertices(0)  # ��0����Ķ���ID�б�
#     print(f"��һ��Ķ���ID: {faceIds}")










# getMeshCount = reader.getMeshCount()
# print('getMeshCount:' + str(getMeshCount))
# # ��ȡ��������
# getJointCount = reader.getJointCount()
# print('getJointCount:' + str(getJointCount))
# for i in range(getMeshCount):
#     print(i)
#     getMeshName = reader.getMeshName(i)
#     print('getMeshName:' + str(getMeshName))
# getMeshName = reader.getMeshName(46)
# print('getMeshName:' + str(getMeshName))



# getMeshName = reader.getMeshName(46)
# mesh_visit_list = cmds.ls(getMeshName+'.vtx[*]',fl=1)
# for v in range(len(mesh_visit_list)):
#     getSkinWeightsJointIndices = reader.getSkinWeightsJointIndices(46, v)
#     print('getSkinWeightsJointIndices:' + str(getSkinWeightsJointIndices))
#     getSkinWeightsValues = reader.getSkinWeights  Values(46, v)
#     print('getSkinWeightsValues:' + str(getSkinWeightsValues))


end_time = time.time()
# ���㲢��ӡ��ʱ
elapsed_time = end_time - start_time
print(f"������ʱ: {elapsed_time} ��")