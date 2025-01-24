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
            writer.setSkinWeightsJointIndices(i, j, joint_list)
            writer.setSkinWeightsValues(i, j, weight_list)
# edit_joint_weight()
# print('###################################')
# getMeshCount = reader.getMeshCount()
# print('getMeshCount:' + str(getMeshCount))
# getMeshName = reader.getMeshName(0)
# print('getMeshName:' + str(getMeshName))
# getMeshIndexListCount = reader.getMeshIndexListCount()
# print('getMeshIndexListCount:' + str(getMeshIndexListCount))
# getVertexPositionCount = reader.getVertexPositionCount(0)
# print('getVertexPositionCount:' + str(getVertexPositionCount))
# getVertexPosition = reader.getVertexPosition(0,0)
# print('getVertexPosition:' + str(getVertexPosition))
# getVertexTextureCoordinateCount = reader.getVertexTextureCoordinateCount(0)
# print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
# getVertexTextureCoordinate = reader.getVertexTextureCoordinate(0,2)
# print('getVertexTextureCoordinate:2' + str(getVertexTextureCoordinate))
# getVertexTextureCoordinate = reader.getVertexTextureCoordinate(0,12025)
# print('getVertexTextureCoordinate:12025' + str(getVertexTextureCoordinate))
# getVertexTextureCoordinateUs = reader.getVertexTextureCoordinateUs(0)
# print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))
# getVertexTextureCoordinateVs = reader.getVertexTextureCoordinateVs(0)
# print('getVertexTextureCoordinateVs:' + str(getVertexTextureCoordinateVs))
# getVertexNormalCount = reader.getVertexNormalCount(0)
# print('getVertexNormalCount:' + str(getVertexNormalCount))
# getVertexNormal = reader.getVertexNormal(0,0)
# print('getVertexNormal:' + str(getVertexNormal))
# getVertexLayoutCount = reader.getVertexLayoutCount(0)
# print('getVertexLayoutCount:' + str(getVertexLayoutCount))
# getVertexLayout = reader.getVertexLayout(0,0)
# print('getVertexLayout:' + str(getVertexLayout))
# getVertexLayout = reader.getVertexLayout(0,12071)
# print('getVertexLayout:' + str(getVertexLayout))
# getVertexLayout = reader.getVertexLayout(0,24177)
# print('getVertexLayout:' + str(getVertexLayout))
# getVertexLayoutPositionIndices = reader.getVertexLayoutPositionIndices(0)
# print('getVertexLayoutPositionIndices:' + str(len(getVertexLayoutPositionIndices)) + str(getVertexLayoutPositionIndices))
# print(getVertexLayoutPositionIndices[12071])
# print(getVertexLayoutPositionIndices[24177])
# getVertexLayoutTextureCoordinateIndices = reader.getVertexLayoutTextureCoordinateIndices(0)
# print('getVertexLayoutTextureCoordinateIndices:' + str(len(getVertexLayoutTextureCoordinateIndices)) + str(getVertexLayoutTextureCoordinateIndices))
# print(getVertexLayoutTextureCoordinateIndices[12071])
# print(getVertexLayoutTextureCoordinateIndices[24177])
# getVertexLayoutNormalIndices = reader.getVertexLayoutNormalIndices(0)
# print('getVertexLayoutNormalIndices:' + str(getVertexLayoutNormalIndices))
# print(getVertexLayoutNormalIndices[12071])
# print(getVertexLayoutNormalIndices[24177])
# getFaceCount = reader.getFaceCount(0)
# print('getFaceCount:' + str(getFaceCount))
# getFaceVertexLayoutIndices = reader.getFaceVertexLayoutIndices(0,0)
# print('getFaceVertexLayoutIndices:' + str(getFaceVertexLayoutIndices))
# getMaximumInfluencePerVertex = reader.getMaximumInfluencePerVertex(0)
# print('getMaximumInfluencePerVertex:' + str(getMaximumInfluencePerVertex))
# getBlendShapeTargetCount = reader.getBlendShapeTargetCount(0)
# print('getBlendShapeTargetCount:' + str(getBlendShapeTargetCount))
# getBlendShapeChannelIndex = reader.getBlendShapeChannelIndex(0,0)
# print('getBlendShapeChannelIndex:' + str(getBlendShapeChannelIndex))
# getBlendShapeTargetDeltaCount = reader.getBlendShapeTargetDeltaCount(0,0)
# print('getBlendShapeTargetDeltaCount:' + str(getBlendShapeTargetDeltaCount))
# getBlendShapeTargetDelta = reader.getBlendShapeTargetDelta(0,0,0)
# print('getBlendShapeTargetDelta:' + str(getBlendShapeTargetDelta))
# getBlendShapeTargetVertexIndices = reader.getBlendShapeTargetVertexIndices(0,0)
# print('getBlendShapeTargetVertexIndices:' + str(len(getBlendShapeTargetVertexIndices)) + str(getBlendShapeTargetVertexIndices))
# ��ȡģ�ͽṹ
def get_mesh_structure():
    sel = cmds.ls(sl=1)
    shape = cmds.listRelatives(sel, c=1, type='mesh')
    if shape:
        cmds.select(shape)
        sel_list = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(sel_list)
        result = [om.MObject()] * 1
        sel_list.getDependNode(0, result[0])
        dep_node_fn = om.MFnDependencyNode(result[0])
        # ���������ʹ��dep_node_fn����ȡ������ڽڵ����Ϣ
        sel_name = dep_node_fn.name()
        # print(dep_node_fn.name())  # ��ӡ�ڵ�����
        # sel_type = dep_node_fn.typeName()
        # print(dep_node_fn.typeName())  # ��ӡ�ڵ�����
        # ����һ���յ�MSelectionList����
        sel_list = om.MSelectionList()
        # ��ȡ��ǰѡ����䵽selLis��
        om.MGlobal.getActiveSelectionList(sel_list)
        # ����ѡ���б��е�ÿ����Ŀ
        for i in range(sel_list.length()):
            # Ϊÿ��ѡ�еĶ��󴴽�һ���µ�MDagPathʵ��
            dag_path = [om.MDagPath()] * sel_list.length()
            # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
            sel_list.getDagPath(i, dag_path[i])
            # ��ȡ�ڵ�
            node = dag_path[i].node()
            # ���ڵ��Ƿ�Ϊ����
            # node.hasFn(om.MFn.kMesh)
            # print('������')
            # ����������򴴽�MFnMesh�����Է�����������
            mesh_fn = om.MFnMesh(node)
            # ���ڿ���ʹ��mesh_fn����������صĲ�����
            # print(f"Found mesh: {dag_path[i].fullPathName()}")
            # ��ȡ����ӡ����Ķ�����������
            num_verts = mesh_fn.numVertices()
            num_faces = mesh_fn.numPolygons()
            # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")
            # ����һ���б����洢����λ��
            vertex_positions = []
            # �������ж��㲢��ȡ���ǵ�λ��
            for i in range(num_verts):
                point = om.MPoint()
                mesh_fn.getPoint(i, point)
                vertex_positions.append([point.x, point.y, point.z])
            # ��ȡ�������ͷ�������
            normals = om.MFloatVectorArray()
            mesh_fn.getVertexNormals(False, normals)
            # ������
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
            # print(vertex_normals[0]) # ������ֵ
            # uuvv = []
            # for i in range(num_verts):
            #     ls_uv = cmds.polyListComponentConversion(sel[0] + '.vtx[' + str(i) + ']', tuv=True)
            #     ls_uv = cmds.ls(ls_uv, fl=1)
            #     for ls in ls_uv:
            #         num = int(ls.split('[')[1][:-1])
            #         uuvv.append(num)
            # print(len(uuvv),uuvv)
            # print(0,uuvv[2])
            # print(1,uuvv[12205])
            # print(795,uuvv[222])
            # print(910,uuvv[223])

            # print(f"Face {0} vertices: {face_vertex_indices}")
            uv_set = []
            mesh_fn.getUVSetNames(uv_set)
            # ����һ��MFloatArray���洢UV����
            uv_coords_us = om.MFloatArray()
            uv_coords_vs = om.MFloatArray()
            # ����getUVs����������UV�������ƺ�MFloatArray������
            # ע�⣺��Python�У��㲻��Ҫ�������ã���ΪPythonʹ�õ������ô���
            mesh_fn.getUVs(uv_coords_us, uv_coords_vs, uv_set[0])

            # �����沢��ӡ��������
            # face_vertices = om.MIntArray()
            # mesh_fn.getPolygonVertices(0, face_vertices)
            all_topology_indices = []
            face_vertex_layout_indices = []
            for i in range(num_faces):
                # face_vertices = om.MIntArray()
                # mesh_fn.getPolygonVertices(i, face_vertices)
                topology = cmds.polyListComponentConversion(sel[0]+'.f[' + str(i) + ']', tvf=True)
                topology = cmds.ls(topology, fl=1)
                all_uv = []
                for j in range(len(topology)):
                    uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv.append(num)
                face_vertex_layout_indices.append(all_uv)
                # all_num = []
                # for j in range(len(topology)):
                #     num = int(topology[j].split('[')[1][:-1])
                #     all_num.append(num)
                # for j in range(len(all_num)):
                #     if not all_num[j] in all_topology_indices:
                #         all_topology_indices.append(all_num[j])
                    # all_topology_indices.append(all_num[j])

            cmds.select(sel)
            # ���ص�ǰѡ������ơ����͡�ģ�͵������������������㷨����ֵ�����ˡ�UV��uֵ����UV��vֵ
            return sel[0], vertex_positions, vertex_normals, all_topology_indices,face_vertex_layout_indices, uv_coords_us, uv_coords_vs
    else:
        cmds.warning('��ѡ��һ���������')
# ��ģ�ͽṹ����ת����dna���������
def data_required_for_conversion_into_dna(mesh_indices):
    name, vertex_positions, vertex_normals, all_topology_indices,face_vertex_layout_indices, uv_coords_us , uv_coords_vs = get_mesh_structure()
    getMeshName = reader.getMeshName(mesh_indices)
    print('getMeshName:' + str(getMeshName))
    print('�������ƣ�',name)
    getVertexPositionCount = reader.getVertexPositionCount(mesh_indices)
    print('getVertexPositionCount:' + str(getVertexPositionCount))
    getVertexPosition = reader.getVertexPosition(mesh_indices, 0)
    print('getVertexPosition:' + str(getVertexPosition))
    print('ģ�͵���ֵ��',len(vertex_positions),vertex_positions)
    # # ���õ�λ��
    # writer.setVertexPositions(meshIndex, positions)
    getVertexNormalCount = reader.getVertexNormalCount(mesh_indices)
    print('getVertexNormalCount:' + str(getVertexNormalCount))
    for num in [0, 1, 2, 3, 4, 5, 6, 7]:
        getVertexNormal = reader.getVertexNormal(mesh_indices, num)
        print('getVertexNormal:' + str(getVertexNormal))
    print('���㷨����ֵ��',len(vertex_normals),vertex_normals)
    # ���õ㷨��
    # writer.setVertexNormals(meshIndex, normals)
    getFaceCount = reader.getFaceCount(0)
    print('getFaceCount:' + str(getFaceCount))
    for num in [0, 1, 2, 3, 4,5,6,7]:
        getFaceVertexLayoutIndices = reader.getFaceVertexLayoutIndices(mesh_indices, num)
        print('getFaceVertexLayoutIndices:' + str(getFaceVertexLayoutIndices))
    print('���ˣ��棩����ָ�룺', len(all_topology_indices), all_topology_indices)
    print('���ˣ��棩���ݣ�', len(face_vertex_layout_indices), face_vertex_layout_indices)

    # �������ˣ��棩
    # writer.clearFaceVertexLayoutIndices(meshIndex)
    # �������ˣ��棩
    # writer.setFaceVertexLayoutIndices(meshIndex, faceIndex, layoutIndices)
    getVertexTextureCoordinateCount = reader.getVertexTextureCoordinateCount(mesh_indices)
    print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
    getVertexTextureCoordinate = reader.getVertexTextureCoordinate(mesh_indices, 0)
    print('getVertexTextureCoordinate:' + str(getVertexTextureCoordinate))
    getVertexTextureCoordinateUs = reader.getVertexTextureCoordinateUs(mesh_indices)
    print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))
    print('UV��uֵ��',len(uv_coords_us),uv_coords_us)
    getVertexTextureCoordinateVs = reader.getVertexTextureCoordinateVs(mesh_indices)
    print('getVertexTextureCoordinateVs:' + str(len(getVertexTextureCoordinateVs)) + str(getVertexTextureCoordinateVs))
    print('UV��vֵ��',len(uv_coords_vs),uv_coords_vs)
    # for num in [0, 1, 2, 3, 4, 5, 6, 7,12025]:
    #     print(getVertexTextureCoordinateUs[num],getVertexTextureCoordinateVs[num])
    #     print(uv_coords_us[num], uv_coords_vs[num])
    #     print()
    # ���õ�UVλ��
    # writer.setVertexTextureCoordinates(meshIndex, textureCoordinates)
    getVertexLayoutCount = reader.getVertexLayoutCount(0)
    print('getVertexLayoutCount:' + str(getVertexLayoutCount))
    # for num in range(getVertexLayoutCount):
    #     getVertexLayout = reader.getVertexLayout(mesh_indices, num)
    #     if getVertexLayout[0] == 2965:
    #         print(num)
    #         print(getVertexLayout)
    print('###########')
    # for num in range(0, getVertexLayoutCount):
    #     getVertexLayout = reader.getVertexLayout(mesh_indices, num)
    #     print(getVertexLayout)
    #     try :
    #         print(all_topology_indices[num])
    #     except:
    #         print('none')
    # print()
    # print('getVertexLayout:' + str(all_topology_indices[910]) + str(reader.getVertexLayout(mesh_indices, 910)))
    print()
    # for num in range(0,getVertexLayoutCount):
    #     getVertexLayout = reader.getVertexLayout(mesh_indices, num)
    #     # if all_topology_indices[num] == getVertexLayout[0]:
    #     print('getVertexLayout:', num, all_topology_indices[num], str(getVertexLayout))

    # print('getVertexLayout:' + str(all_topology_indices[910]) + str(reader.getVertexLayout(mesh_indices, 910)))
    print()
    for num in range(0,10):
        getVertexLayout = reader.getVertexLayout(mesh_indices, num)
        print('getVertexLayout:' + str(num) + str(getVertexLayout))
    print()
    for num in range(getVertexLayoutCount-7, getVertexLayoutCount):
        getVertexLayout = reader.getVertexLayout(mesh_indices, num)
        print('getVertexLayout:' + str(getVertexLayout))
    print()
    max = 0
    for num in range(getVertexLayoutCount):
        getVertexLayout = reader.getVertexLayout(mesh_indices, num)
        if getVertexLayout[0]> max:
            max = getVertexLayout[0]
    print('getVertexLayout[*][0](max):' + str(max+1))
    max = 0
    for num in range(getVertexLayoutCount):
        getVertexLayout = reader.getVertexLayout(mesh_indices, num)
        if getVertexLayout[1] > max:
            max = getVertexLayout[1]
    print('getVertexLayout[*][1](max):' + str(max+1))
    max = 0
    for num in range(getVertexLayoutCount):
        getVertexLayout = reader.getVertexLayout(mesh_indices, num)
        if getVertexLayout[2] > max:
            max = getVertexLayout[2]
    print('getVertexLayout[*][2](max):' + str(max+1))
    lst = []
    for num in range(getVertexLayoutCount):
        getVertexLayout = reader.getVertexLayout(mesh_indices, num)
        lst.append(getVertexLayout[1])
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    # print('�ظ�Ԫ�أ�',[item for item, count in count_dict.items() if count > 1])
    # a_1 = []
    # a_2 = []
    # for num in range(getVertexLayoutCount):
    #     getVertexLayout = reader.getVertexLayout(mesh_indices, num)
    #     a_1.append(getVertexLayout[0])
    #     a_2.append(getVertexLayout[0])
    # print(max([x for x in a_1]))
    # print(max([x for x in a_2]))

    # list = []
    # for i in range(getVertexLayoutCount):
    #     getVertexLayout = reader.getVertexLayout(mesh_indices, i)
    #     list.append(getVertexLayout[2])
    # seen = set()
    # duplicates = []
    # for item in list:
    #     if item in seen:
    #         if item not in duplicates:
    #             duplicates.append(item)
    #     else:
    #         seen.add(item)
    #         # ��Ҫ����һ�����б�����uָ�롢vָ�롢����ָ��
    # print(duplicates)

    uv_layout = []

    for i in range(len(uv_coords_us)):
        ls_uv = cmds.polyListComponentConversion(name + '.map[' + str(i) + ']', tv=True)
        ls_uv = cmds.ls(ls_uv, fl=True)
        num = int(ls_uv[0].split('[')[1][:-1])
        # getVertexLayout = reader.getVertexLayout(mesh_indices, i)
        layout = [num, i, num]
        print(layout)
        uv_layout.append(layout)
    # ʹ��sort()��������ָ��keyΪlambda�������ú����������б�����һ��Ԫ��
    # uv_layout.sort(key=lambda x: x[-1])
    uv = []
    for i in range(len(uv_coords_us)):
        ls_uv = [uv_coords_us[i], uv_coords_vs[i]]
        uv.append(ls_uv)
        # point = cmds.polyListComponentConversion(name+'.vtx['+str(i)+']', tuv=True)
        # point = cmds.ls(point, fl=1)
        # # print(point)
        # for j in range(len(point)):
        #     point_num = int(point[j].split('[')[1][:-1])
        #     # print(i, point_num)
        #     layout = [point_num,point_num,i]
        #     uv_num_list = [uv_coords_us[i], uv_coords_vs[i]]
        #     uv_layout.append(layout)
        #     uv.append(uv_num_list)
    print(len(uv_layout),uv_layout)
    # for num in range(24040,24050):
    #     print('uv_layout:' + str(num) + str(uv_layout[num]))
    print()
    # for num in range(len(uv_layout)-7, len(uv_layout)):
    #     print('uv_layout:' + str(uv_layout[num]))
    print()
    getVertexTextureCoordinate = reader.getVertexTextureCoordinate(mesh_indices, 0)
    print('getVertexTextureCoordinate:' + str(getVertexTextureCoordinate))
    # for i in range(len(uv_coords_us)):
    #     point = cmds.polyListComponentConversion(name+'.map['+str(i)+']', tv=True)
    #     point = cmds.polyListComponentConversion(name + '.map[' + str(i) + ']', tv=True)
    #     point_num = int(point[0].split('[')[1][:-1])
    #     # print(i, point_num)
    #     layout = [i,i,point_num]
    #     uv_num_list = [uv_coords_us[i], uv_coords_vs[i]]
    #     uv_layout.append(layout)
    #     uv.append(uv_num_list)

    # uv_layout.sort(key=lambda x: x[-1])
    # print(uv_layout)
    # writer.setVertexLayouts(meshIndex, layouts)

    # UV�����ǳɶԳ��ֵģ�u, v��������������Ҫ�ԶԵ���ʽ����������
    # num_uvs = uv_coords_us.length()  # ��Ϊÿ��UV�����������꣺u��v
    # for i in range(num_uvs):
    for i in [0, 1, 2, 3, 4]:
        u = uv_coords_us[i]
        v = uv_coords_vs[i]
        print(f"UV {i}: ({u}, {v})")

    # writer.setBlendShapeTargetDeltas(meshIndex, blendShapeTargetIndex, deltas)
    # writer.setBlendShapeTargetVertexIndices(meshIndex, blendShapeTargetIndex, vertexIndices)
    return vertex_positions, vertex_normals, all_topology_indices,face_vertex_layout_indices, uv, uv_layout
# def set_md(meshIndex):
#     set_point_positions(meshIndex)
#     writer.setMaximumInfluencePerVertex(meshIndex, maxInfluenceCount)
#     writer.clearSkinWeights(meshIndex)
#     writer.setSkinWeightsValues(mesh_indices, vertexIndex, weights)
#     writer.setSkinWeightsJointIndices(mesh_indices, vertexIndex, jointIndices)
# �޸ĵ�λ�á����ߡ�UV����
def set_point_positions(mesh_indices, positions, normals, uv, uv_layouts):
    # ���õ�λ��
    writer.setVertexPositions(mesh_indices, positions)
    # ���õ㷨��
    writer.setVertexNormals(mesh_indices, normals)
    # # # ���õ�UVλ��
    writer.setVertexTextureCoordinates(mesh_indices, uv)
    # # ����[24049��λ��ָ��,24408uvָ��,24049���㷨��ָ��]
    # �滻��������д��
    writer.setVertexLayouts(mesh_indices, uv_layouts)
# ��������
def clean_topology(mesh_indices, all_topology_indices):
    # writer.clearMeshes()
    # for i in range(1,50):
    #     writer.deleteMesh(i)
    # �������ˣ��棩
    writer.clearFaceVertexLayoutIndices(mesh_indices)
    # �������ˣ��棩
    for faceIndex in range(len(all_topology_indices)):
        layoutIndices = all_topology_indices[faceIndex]
        writer.setFaceVertexLayoutIndices(mesh_indices, faceIndex, layoutIndices)
# ����bs
def reset_blendshape(mesh_indices):
    # writer.clearBlendShapeTargets(mesh_indices)
    getBlendShapeTargetCount = reader.getBlendShapeTargetCount(mesh_indices)
    print('getBlendShapeTargetCount:' + str(getBlendShapeTargetCount))
    getBlendShapeChannelIndex = reader.getBlendShapeChannelIndex(mesh_indices, 0)
    print('getBlendShapeChannelIndex:' + str(getBlendShapeChannelIndex))
    getBlendShapeTargetDeltaCount = reader.getBlendShapeTargetDeltaCount(mesh_indices, 0)
    print('getBlendShapeTargetDeltaCount:' + str(getBlendShapeTargetDeltaCount))
    getBlendShapeTargetDelta = reader.getBlendShapeTargetDelta(mesh_indices, 0, 0)
    print('getBlendShapeTargetDelta:' + str(getBlendShapeTargetDelta))
    for i in range(getBlendShapeTargetCount):
        # writer.setBlendShapeChannelIndex(mesh_indices, blendShapeTargetIndex, blendShapeChannelIndex)
        writer.setBlendShapeTargetDeltas(mesh_indices, i, [0.0,0.0,0.0])
        writer.setBlendShapeTargetVertexIndices(mesh_indices, i, [0])
def create_dna(mesh_indices):
    vertex_positions, vertex_normals, all_topology_indices,face_vertex_layout_indices, uv, uv_layout = data_required_for_conversion_into_dna(mesh_indices)
    # clean_topology(mesh_indices, face_vertex_layout_indices)
    set_point_positions(mesh_indices, vertex_positions, vertex_normals, uv, uv_layout)
    writer.write()  # д������
    print('д�����ļ����')
    print('�Ѿ�ȫ�����У��������dna�鿴Ч��')
create_dna(0)
###############################################################################################
end_time = time.time()
# ���㲢��ӡ��ʱ
elapsed_time = end_time - start_time
print(f"������ʱ: {elapsed_time} ��")
# for num in [0, 1, 2, 3, 4,5,6,7]:
#     point = cmds.polyListComponentConversion('head_lod0_mesh.f['+str(num)+']', tvf=True)
#     point = cmds.ls(point, fl=1)
#     print(point)
#     for i in range(len(point)):
#         uv = cmds.polyListComponentConversion(point[i], tuv=True)
#         uv = cmds.ls(uv, fl=1)
#         print(uv)
#
#     print()
# name = 'head_lod0_mesh'
# getVertexLayoutCount = reader.getVertexLayoutCount(0)
# print('getVertexLayoutCount:' + str(getVertexLayoutCount))
# for num in range(getVertexLayoutCount):
#     getVertexLayout = reader.getVertexLayout(0, num)
#     ls_uv = cmds.polyListComponentConversion(name + '.vtx[' + str(getVertexLayout[0]) + ']', tuv=True)
#     ls_uv = cmds.ls(ls_uv, fl=1)
#     if len(ls_uv) > 1:
#         print('getVertexLayout:',ls_uv,num,getVertexLayout)

# name = 'head_lod0_mesh'
# for num in range(0,10):
#     getVertexLayout = reader.getVertexLayout(0, num)
#     point = cmds.polyListComponentConversion(name + '.f[' + str(getVertexLayout[0]) + ']', te=True)
#     point = cmds.ls(point, fl=1)
#     print('getVertexLayout:', point)
#     ls_uv = cmds.polyListComponentConversion(name + '.f[' + str(getVertexLayout[0]) + ']', tuv=True)
#     ls_uv = cmds.ls(ls_uv, fl=1)
#     print('getVertexLayout:',ls_uv)
#     point = cmds.polyListComponentConversion(name + '.f[' + str(getVertexLayout[0]) + ']', tv=True)
#     point = cmds.ls(point, fl=1)
#     print('getVertexLayout:', point)
#     point = cmds.polyListComponentConversion(name + '.f[' + str(getVertexLayout[0]) + ']', tvf=True)
#     point = cmds.ls(point, fl=1)
#     print('getVertexLayout:', point)
#     point = cmds.polyListComponentConversion(name + '.f[' + str(getVertexLayout[0]) + ']', uvs=True)
#     point = cmds.ls(point, fl=1)
#     print('getVertexLayout:', point)
#     point = cmds.polyListComponentConversion(name + '.f[' + str(getVertexLayout[0]) + ']', vfa=True)
#     point = cmds.ls(point, fl=1)
#     print('getVertexLayout:', point)
mesh_indices = 0
getBlendShapeTargetCount = reader.getBlendShapeTargetCount(mesh_indices)
print('getBlendShapeTargetCount:' + str(getBlendShapeTargetCount))
getBlendShapeChannelIndex = reader.getBlendShapeChannelIndex(mesh_indices, 0)
print('getBlendShapeChannelIndex:' + str(getBlendShapeChannelIndex))
getBlendShapeTargetDeltaCount = reader.getBlendShapeTargetDeltaCount(mesh_indices, 0)
print('getBlendShapeTargetDeltaCount:' + str(getBlendShapeTargetDeltaCount))
getBlendShapeTargetDelta = reader.getBlendShapeTargetDelta(mesh_indices, 0, 0)
print('getBlendShapeTargetDelta:' + str(getBlendShapeTargetDelta))
getBlendShapeTargetVertexIndices = reader.getBlendShapeTargetVertexIndices(mesh_indices, 0)
print('getBlendShapeTargetVertexIndices:',len(getBlendShapeTargetVertexIndices),str(getBlendShapeTargetVertexIndices))
