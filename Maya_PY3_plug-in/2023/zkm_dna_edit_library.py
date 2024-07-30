#coding=gbk
'''
    ���ߣ����� ��ղ������<https://github.com/MengXingXiaoMing?tab=repositories>
    ����޸�: 2024-07-29
    �汾: 1.0.0
    ����һ������metahuman�ٷ���������⣬�����Ԥ�ƺ��˳��ù��ܣ���ʲô�����������ᣬ�һᾡ������.
    ����Ŀǰ��������ҵ���ҵ��ֻ�ܳ��д�����Ը��»�����ϣ����Ҽ��¡�
'''
import os

import inspect
from sys import path as syspath
from sys import platform

import maya.cmds as cmds
import maya.OpenMaya as om

# import time
# # ��¼��ʼʱ��
# start_time = time.time()

class dna_edit_library():
    def __init__(self):
        # �汾��
        self.maya_version = cmds.about(version=True)
        # ��ǰ�ļ�·��
        self.file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

        self.ROOT_DIR = self.file_path + '/custom_commands/MetaHuman-DNA-Calibration-main'
        self.MAYA_VERSION = self.maya_version  # 2022 or 2023
        self.ROOT_LIB_DIR = f"{self.ROOT_DIR}/lib/Maya{self.MAYA_VERSION}"

        # ������·�����������޸ģ����Ҫ�ĳ�һ���������б���
        # dnaԴ����·��
        self.soure_dna_path = f"{self.ROOT_DIR}/data/mh4/dna_files/Ada_modify.dna"
        # �������ɵ�dna·��
        self.target_dna_path = f"{self.ROOT_DIR}/data/mh4/dna_files/Ada_modify.dna"

        self.load_read_write()

    # �����дdna��
    def load_read_write(self):
        if self.maya_version == '2022' or self.maya_version == '2023':
            if platform == "win32":
                LIB_DIR = f"{self.ROOT_LIB_DIR}/windows"
            elif platform == "linux":
                LIB_DIR = f"{self.ROOT_LIB_DIR}/linux"
            else:
                raise OSError(
                    "OS not supported, please compile dependencies and add value to LIB_DIR"
                )

            # ��Ŀ¼��ӵ�·��
            syspath.insert(0, self.ROOT_DIR)
            syspath.insert(0, LIB_DIR)
            from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter

            # ��Ӷ�ȡ��
            stream = FileStream(self.soure_dna_path, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
            self.reader = BinaryStreamReader(stream, DataLayer_All)
            self.reader.read()

            # ���д���
            stream = FileStream(self.target_dna_path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
            self.writer = BinaryStreamWriter(stream)
            self.writer.setFrom(self.reader)
            print('dna�ѿ��Զ�ȡ��д�롣')
        else:
            cmds.warning("Maya�汾����,��֧��2022��2023�汾���糢���ٱ�İ汾�������޸ġ�")

    # ��ȡ�����ص�ǰѡ��ģ�ͽṹ����
    def get_mesh_structure(self):
        sel = cmds.ls(sl=1)
        shape = cmds.listRelatives(sel, c=1, type='mesh')
        if shape:
            # ѡ����״�ڵ�
            cmds.select(shape)
            # ����MSelectionList���ݴ�ŵ�ǰѡ������
            sel_list = om.MSelectionList()
            # ��ȡ��ǰѡ����䵽sel_list��
            om.MGlobal.getActiveSelectionList(sel_list)
            result = [om.MObject()] * 1
            sel_list.getDependNode(0, result[0])
            # ׼����dep_node_fn����ȡ������ڽڵ����Ϣ
            dep_node_fn = om.MFnDependencyNode(result[0])

            # sel_name = dep_node_fn.name()
            # print(dep_node_fn.name())  # ��ӡ�ڵ�����

            # sel_type = dep_node_fn.typeName()
            # print(dep_node_fn.typeName())  # ��ӡ�ڵ�����

            # ����ȡѡ���б��еĵ�һ��ѡ�����Ŀ������

            # Ϊѡ�еĶ��󴴽�һ���µ�MDagPathʵ��
            dag_path = [om.MDagPath()] * sel_list.length()
            # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
            sel_list.getDagPath(0, dag_path[0])
            # ��ȡ�ڵ�
            node = dag_path[0].node()

            # ���ڵ��Ƿ�Ϊ����
            # node.hasFn(om.MFn.kMesh)

            # ����������򴴽�MFnMesh�����Է�����������
            mesh_fn = om.MFnMesh(node)
            # ��ȡ����Ķ�����
            num_verts = mesh_fn.numVertices()
            # ��ȡ���������
            num_faces = mesh_fn.numPolygons()
            # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

            # ����һ���б����洢����λ��
            vertex_positions = []
            # �������ж��㲢��ȡ���ǵ�λ��
            for i in range(num_verts):
                point = om.MPoint()
                mesh_fn.getPoint(i, point)
                vertex_positions.append([point.x, point.y, point.z])

            # ��ȡ����������
            normals = om.MFloatVectorArray()
            mesh_fn.getVertexNormals(False, normals)
            # ��ȡ���㷨����ֵ����
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])

            # ��ȡuv��
            uv_set = []
            mesh_fn.getUVSetNames(uv_set)

            # ����һ��MFloatArray���洢UV����
            uv_coords_us = om.MFloatArray()
            uv_coords_vs = om.MFloatArray()
            # ����getUVs����������UV�������ƺ�MFloatArray������
            mesh_fn.getUVs(uv_coords_us, uv_coords_vs, uv_set[0])

            # �����沢����
            all_topology = []
            for i in range(num_faces):
                # �����ȡ����
                topology = cmds.polyListComponentConversion(sel[0]+'.f[' + str(i) + ']', tvf=True)
                topology = cmds.ls(topology, fl=1)
                all_uv_num = []
                for j in range(len(topology)):
                    # �����˻�ȡuv
                    uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num.append(num)
                all_topology.append(all_uv_num)

            # ����ѡ��ص�ǰѡ��
            cmds.select(sel)
            print('�ѻ�ȡ��ǰѡ��ģ�ͽṹ���ݡ�')
            # ���ص�ǰѡ������ơ������顢���㷨�����顢�������顢UV��uֵ����UV��vֵ
            return sel[0], vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs
        else:
            cmds.warning('��ѡ��һ���������')

    # ��ģ�ͽṹ����ת����dna���������
    def data_required_for_conversion_into_dna(self, mesh_indices, name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs):
        '''getMeshName = self.reader.getMeshName(mesh_indices)
        print('getMeshName:' + str(getMeshName))'''
        # print('�������ƣ�',name)

        '''getVertexPositionCount = self.reader.getVertexPositionCount(mesh_indices)
        print('getVertexPositionCount:' + str(getVertexPositionCount))
        getVertexPosition = self.reader.getVertexPosition(mesh_indices, 0)
        print('getVertexPosition:' + str(getVertexPosition))'''
        # print('ģ�͵���ֵ��',len(vertex_positions),vertex_positions)

        '''getVertexNormalCount = self.reader.getVertexNormalCount(mesh_indices)
        print('getVertexNormalCount:' + str(getVertexNormalCount))
        getVertexNormal = self.reader.getVertexNormal(mesh_indices, 0)
        print('getVertexNormal:' + str(getVertexNormal))'''
        # print('���㷨����ֵ��',len(vertex_normals),vertex_normals)

        '''getFaceCount = self.reader.getFaceCount(0)
        print('getFaceCount:' + str(getFaceCount))
        getFaceVertexLayoutIndices = self.reader.getFaceVertexLayoutIndices(mesh_indices, 0)
        print('getFaceVertexLayoutIndices:' + str(getFaceVertexLayoutIndices))'''
        # print('���ˣ��棩���ݣ�', len(all_topology), all_topology)

        '''getVertexTextureCoordinateCount = self.reader.getVertexTextureCoordinateCount(mesh_indices)
        print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
        getVertexTextureCoordinate = self.reader.getVertexTextureCoordinate(mesh_indices, 0)
        print('getVertexTextureCoordinate:' + str(getVertexTextureCoordinate))
        getVertexTextureCoordinateUs = self.reader.getVertexTextureCoordinateUs(mesh_indices)
        print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))'''
        # print('UV��uֵ��',len(uv_coords_us),uv_coords_us)

        '''getVertexTextureCoordinateVs = self.reader.getVertexTextureCoordinateVs(mesh_indices)
        print('getVertexTextureCoordinateVs:' + str(len(getVertexTextureCoordinateVs)) + str(getVertexTextureCoordinateVs))'''
        # print('UV��vֵ��', len(uv_coords_vs), uv_coords_vs)

        '''getVertexLayoutCount = self.reader.getVertexLayoutCount(0)
        print('getVertexLayoutCount:' + str(getVertexLayoutCount))'''

        # ��ʼ����[��ָ��,uvָ��,�㷨��ָ��]����
        '''
        �˴�����˵����
            ������ӡģ���ļ��Ļᷢ�ֺ��ң����Ǿ����Ҵ��������ǿ��԰�˳�����еģ�������ģ���ģ�ͽṹ���ݴ�Ż��ҵ��µģ�Ӧ���ǻ�ȡ��ʱ���������
            ȡ�ģ�����ָ��Ҳ���߰���ģ����������ɹ��ɴ����󵼵��������֮Ҫ����Ҫ�ӹٷ������ݿ�ʼ��Ļ�Ҫ����ͷ���׼����
        '''
        p_uv_nor_layout = []
        for i in range(len(uv_coords_us)):
            point = cmds.polyListComponentConversion(name + '.map[' + str(i) + ']', tv=True)
            point = cmds.ls(point, fl=True)
            num = int(point[0].split('[')[1][:-1])
            layout = [num, i, num]
            p_uv_nor_layout.append(layout)
        # print('[��ָ�룬uvָ�룬�㷨��ָ��]���飺',len(p_uv_nor_layout), p_uv_nor_layout)

        # ����uv��ֵ����
        uv = []
        for i in range(len(uv_coords_us)):
            point = [uv_coords_us[i], uv_coords_vs[i]]
            uv.append(point)
        # print('uv��ֵ���飺', len(uv), uv)

        print('�Ѿ�ת���ɱ༭dna�������ݡ�')
        # ����ģ��ָ�룬�����飬�㷨�����飬���ˣ�uv���飬[��ָ��,uvָ��,�㷨��ָ��]����
        return mesh_indices, vertex_positions, vertex_normals, all_topology, uv, p_uv_nor_layout

    # �޸ĵ�λ�á����ߡ�UV����
    def set_point_positions(self, mesh_indices, vertex_positions, vertex_normals, uv, p_uv_nor_layout):
        # ���õ�λ��
        self.writer.setVertexPositions(mesh_indices, vertex_positions)
        # ���õ㷨��
        self.writer.setVertexNormals(mesh_indices, vertex_normals)
        # ���õ�UVλ��
        self.writer.setVertexTextureCoordinates(mesh_indices, uv)
        # ����[��ָ��,uvָ��,�㷨��ָ��]����
        self.writer.setVertexLayouts(mesh_indices, p_uv_nor_layout)
        print(mesh_indices, 'ģ�͵�λ�á����ߡ�UV�����Ը��¡�')

    # ��������
    def set_topology(self, mesh_indices, all_topology):
        # �������ˣ��棩
        self.writer.clearFaceVertexLayoutIndices(mesh_indices)
        # �������ˣ��棩
        for faceIndex in range(len(all_topology)):
            layoutIndices = all_topology[faceIndex]
            self.writer.setFaceVertexLayoutIndices(mesh_indices, faceIndex, layoutIndices)
        print(mesh_indices, '��ǰָ�������Ѹ��¡�')

    # ����bs
    def reset_blendshape(self, mesh_indices):
        # ��ȡbs������bs��Ŀ������ɶ�Ĳ�����ã�bsҲ��ɾ�������õı仯��ֵ����ͺ�
        getBlendShapeTargetCount = self.reader.getBlendShapeTargetCount(mesh_indices)
        # print('getBlendShapeTargetCount:' + str(getBlendShapeTargetCount))
        # getBlendShapeChannelIndex = self.reader.getBlendShapeChannelIndex(mesh_indices, 0)
        # print('getBlendShapeChannelIndex:' + str(getBlendShapeChannelIndex))
        # getBlendShapeTargetDeltaCount = self.reader.getBlendShapeTargetDeltaCount(mesh_indices, 0)
        # print('getBlendShapeTargetDeltaCount:' + str(getBlendShapeTargetDeltaCount))
        # getBlendShapeTargetDelta = self.reader.getBlendShapeTargetDelta(mesh_indices, 0, 0)
        # print('getBlendShapeTargetDelta:' + str(getBlendShapeTargetDelta))
        # getBlendShapeTargetVertexIndices = self.reader.getBlendShapeTargetVertexIndices(mesh_indices, 0)
        # print('getBlendShapeTargetVertexIndices:' + str(getBlendShapeTargetVertexIndices))

        for i in range(getBlendShapeTargetCount):
            # writer.setBlendShapeChannelIndex(mesh_indices, blendShapeTargetIndex, blendShapeChannelIndex)
            self.writer.setBlendShapeTargetDeltas(mesh_indices, i, [])
            self.writer.setBlendShapeTargetVertexIndices(mesh_indices, i, [])
        print(mesh_indices,'����bsƫ����ֵ�Ѿ����á�')

    # ���ù���Ȩ��
    def reset_joint_weight(self,mesh_indices):
        # ��ȡģ�͵�����
        getSkinWeightsCount = self.reader.getSkinWeightsCount(mesh_indices)
        # print('getSkinWeightsCount:' + str(getSkinWeightsCount))
        for j in range(getSkinWeightsCount):
            self.writer.setSkinWeightsJointIndices(mesh_indices, j, [0])
            self.writer.setSkinWeightsValues(mesh_indices, j, [1])
        print('����Ȩ���Ѿ����á�')

    # �༭����Ȩ��
    def edit_joint_weight(self, mesh_indices):
        # ��ȡģ������
        # getMeshCount = self.reader.getMeshCount()
        # print('getMeshCount:' + str(getMeshCount))
        # ��ȡ��������
        getJointCount = self.reader.getJointCount()
        # print('getJointCount:' + str(getJointCount))
        # ��ÿ��ģ�������ʼ�޸�
        # ��ȡģ������
        getMeshName = self.reader.getMeshName(mesh_indices)
        print('getMeshName:' + str(getMeshName))
        # ��ȡ��Ƥ�ڵ�
        history = cmds.listHistory(getMeshName)
        skinClusterName = ''
        for node in history:
            if cmds.nodeType(node) == 'skinCluster':
                skinClusterName = node
                break
        # �Ƴ�����Ӱ��
        cmds.RemoveUnusedInfluences(skinClusterName)
        # ��ȡ��Ӱ��Ĺ���
        source_skin_joint = cmds.skinCluster(getMeshName, q=1, inf=1)
        # print(len(source_skin_joint), source_skin_joint)
        # ��ȡģ�͵�����
        # getSkinWeightsCount = self.reader.getSkinWeightsCount(mesh_indices)
        # print('getSkinWeightsCount:' + str(getSkinWeightsCount))
        # ��ȡģ�͵��б�
        mesh_visit_list = cmds.ls(getMeshName + '.vtx[*]', fl=1)
        # print(len(mesh_visit_list), mesh_visit_list)
        # �����ȡȨ�ش����޸��б�
        clearSkinWeights = self.writer.clearSkinWeights(mesh_indices)
        # print('clearSkinWeights:' + str(clearSkinWeights))
        # ��ȡ��Ӱ��Ĺ��������й����е�ָ��λ��
        joint_index_list = []
        for k in range(getJointCount):
            getJointName = self.reader.getJointName(k)
            for l in range(len(source_skin_joint)):
                if source_skin_joint[l] == getJointName:
                    joint_index_list.append(k)
        # print(len(joint_index_list), joint_index_list)
        # ��ʼ������޸�
        for j in range(len(mesh_visit_list)):
            weight_list = []
            joint_list = []
            # ��ȡÿ��������ĳ�����Ȩ����ֵ
            weight = cmds.skinPercent(skinClusterName, mesh_visit_list[j], q=True, v=True)
            # ������ֵ�Ĺ���������ֵ���ص����б�
            for w in range(len(weight)):
                if weight[w] > 0:
                    joint_list.append(joint_index_list[w])
                    weight_list.append(weight[w])
            self.writer.setSkinWeightsJointIndices(mesh_indices, j, joint_list)
            self.writer.setSkinWeightsValues(mesh_indices, j, weight_list)
        print('���й���Ȩ�ض��Ѹ��¡�')

    # �༭����λ��
    def edit_joint_tr(self):
        getJointCount = self.reader.getJointCount()
        # print('getJointCount:' + str(getJointCount))
        need_write_translate_list = []
        need_write_rotate_list = []
        for i in range(getJointCount):
            # ��ȡ��������
            getJointName = self.reader.getJointName(i)
            # print('getJointName:' + str(getJointName))
            # ��ȡλ����ֵ
            translate = cmds.xform(getJointName, q=True, t=True)
            # print(translate)
            # ��ȡ��ת��ֵ
            rotate = cmds.xform(getJointName, q=True, ro=True)
            # print(rotate)
            # ��ȡ���е���ת��ֵ
            getNeutralJointRotation = self.reader.getNeutralJointRotation(i)
            # print('getJointName:' + str(getNeutralJointRotation))
            # ����λ����ֵ�б�
            need_write_translate_list.append(translate)
            # �ؼ��㲢�����ת��ֵ�б�
            for j in range(0, len(getNeutralJointRotation)):
                getNeutralJointRotation[j] = getNeutralJointRotation[j] + rotate[j]
            need_write_rotate_list.append(getNeutralJointRotation)

        self.writer.setNeutralJointTranslations(need_write_translate_list)
        self.writer.setNeutralJointRotations(need_write_rotate_list)
        print('���й���λ�ö��Ѿ����¡�')

    # ����ǰѡ��ģ��д���bs
    def write_sel_model_to_bs(self,mesh_indices,bs_index,vertex_positions,sel_mesh):
        # getBlendShapeTargetCount = self.reader.getBlendShapeTargetCount(mesh_indices)
        # print('getBlendShapeTargetCount:' + str(getBlendShapeTargetCount))
        # getBlendShapeChannelIndex = self.reader.getBlendShapeChannelIndex(mesh_indices, 0)
        # print('getBlendShapeChannelIndex:' + str(getBlendShapeChannelIndex))
        # getBlendShapeTargetDeltaCount = self.reader.getBlendShapeTargetDeltaCount(mesh_indices, 0)
        # print('getBlendShapeTargetDeltaCount:' + str(getBlendShapeTargetDeltaCount))
        # getBlendShapeTargetDelta = self.reader.getBlendShapeTargetDelta(mesh_indices, 0, 0)
        # print('getBlendShapeTargetDelta:' + str(getBlendShapeTargetDelta))
        vtx = cmds.ls(sel_mesh+'.vtx[*]',fl=1)
        new_vertex_positions = []
        # �������ж���
        for i in range(len(vtx)):
            # ��ȡ���������λ��
            pos = cmds.xform(vtx[i],q=True, ws=True, t=True)

            # ��λ����ӵ��б���
            new_vertex_positions.append(pos)
            # �����һ��ƫ������
        offset_vertices = []
        offset_array = []
        for i in range(len(vertex_positions)):
            x = new_vertex_positions[i][0] - vertex_positions[i][0]
            y = new_vertex_positions[i][1] - vertex_positions[i][1]
            z = new_vertex_positions[i][2] - vertex_positions[i][2]
            xyz = [x,y,z]
            if any(xyz):
                offset_vertices.append(i)
                offset_array.append(xyz)
        self.writer.setBlendShapeTargetDeltas(mesh_indices, bs_index, offset_array)
        self.writer.setBlendShapeTargetVertexIndices(mesh_indices, bs_index, offset_vertices)
        print(mesh_indices, bs_index, '���޸ĵ�ǰָ��λ�õ�bs��')

    # ���ص�ǰָ��������������ҷ�����������
    def load_edit_drver_date(self, base_face):
        all_date = []
        getJointGroupCount = self.reader.getJointGroupCount()  # ��ȡ������ָ��
        # print('����������:' + str(getJointGroupCount))
        getRawControlName = self.reader.getRawControlName(base_face)
        print('��Ҫ�޸ĵĳ�ʼ���飺' + str(base_face))
        print('������������:' + str(getRawControlName))
        # ��ѯ���������Ƿ���Ҫ�޸ĵ�������
        # max = 0
        for j in range(0, getJointGroupCount):  #
            getJointGroupInputIndices = self.reader.getJointGroupInputIndices(j)  # ��ȡ��������������΢����
            # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
            joint_group = []
            base_face_in_joint_group_indices = 0
            for i in range(0, len(getJointGroupInputIndices)):
                if getJointGroupInputIndices[i] == base_face:
                    joint_group = j  # ������
                    base_face_in_joint_group_indices = i  # ��Ҫ�޸ĵĻ��������������б��������ݵ�λ��
                    break
            if joint_group:  # �������������򴴽�������͹����ֵ�
                group_with_values = []
                getJointGroupOutputIndices = self.reader.getJointGroupOutputIndices(j)  # ��ȡ������������������
                # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
                # �������������ֵ�����б�
                joint_value = []
                getJointGroupValues = self.reader.getJointGroupValues(j)  # ��ȡ��������������΢��������������ֵ
                # print('getJointGroupValues:' + str(len(getJointGroupValues)) + str(getJointGroupValues))
                for x in range(0, len(getJointGroupOutputIndices)):
                    ls_list = []
                    for k in range(0, len(getJointGroupInputIndices)):
                        ls_list.append(getJointGroupValues[len(getJointGroupInputIndices) * x + k])
                    joint_value.append(ls_list)
                # print(joint_value)
                # �����޸��б�
                ls_list = [joint_group, joint_value, base_face_in_joint_group_indices]
                group_with_values.append(ls_list)
                all_date.append(group_with_values)
        print('�������ݼ������')
        return all_date

    # д���������
    def write_edit_drver_date(self, all_date):
        getJointCount = self.reader.getJointCount()  # ��ȡ����ָ��
        # print('��������:' + str(getJointCount))
        attr = []
        for j in range(0, getJointCount):
            getJointName = self.reader.getJointName(j)  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
            list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY',
                    'scaleZ']
            for at in list:
                joint_name = getJointName
                ls_list = [j, joint_name, at]
                attr.append(ls_list)
        # print('���й�������:' + str(len(attr)) + str(attr))
        for n in range(0, len(all_date)):
            group_all_date = all_date[n][0]
            joint_group = group_all_date[0]  # ��ȡ����������
            joint_value = group_all_date[1]  # ��ȡ�����Բ�ֵ�ֵ
            base_face_in_joint_group_indices = group_all_date[2]  # ��ȡ����������Ҫ�޸ĵı����������������б����λ��
            getJointGroupInputIndices = self.reader.getJointGroupInputIndices(joint_group)  # ��ȡ��������������΢����
            # ��ȡ�����б��Լ������������
            getJointGroupOutputIndices = self.reader.getJointGroupOutputIndices(joint_group)  # ��ȡ������������������
            for i in range(0, len(getJointGroupOutputIndices)):  # �����������б���
                for j in range(0, len(attr)):  # ���й���������
                    if j == getJointGroupOutputIndices[i]:
                        translate = cmds.xform((attr[j][1]), q=1, t=1)  # ��ȡ��ǰ����λ��
                        getNeutralJointTranslation = self.reader.getNeutralJointTranslation(attr[j][0])  # ��ȡĬ��״̬λ��
                        rotate = cmds.getAttr(attr[j][1] + '.rotate')[0]  # ��ȡ��תֵ
                        now_num = 0
                        base_num = 0
                        if attr[j][2] == 'translateX':
                            now_num = translate[0]
                            base_num = getNeutralJointTranslation[0]
                        if attr[j][2] == 'translateY':
                            now_num = translate[1]
                            base_num = getNeutralJointTranslation[1]
                        if attr[j][2] == 'translateZ':
                            now_num = translate[2]
                            base_num = getNeutralJointTranslation[2]
                        if attr[j][2] == 'rotateX':
                            now_num = rotate[0]
                            base_num = 0
                        if attr[j][2] == 'rotateY':
                            now_num = rotate[1]
                            base_num = 0
                        if attr[j][2] == 'rotateZ':
                            now_num = rotate[2]
                            base_num = 0
                        # print(attr[j][1] + '.' + attr[j][2])
                        # print(now_num)
                        # print(base_num)
                        num = now_num - base_num  # �ؼ���������ֵ
                        joint_value[i][base_face_in_joint_group_indices] = num
                        break
            # ��ʼ�޸�ֵ
            new_values = []
            for i in range(0, len(joint_value)):
                for x in range(0, len(getJointGroupInputIndices)):
                    new_values.append(joint_value[i][x])
            self.writer.setJointGroupValues(joint_group, new_values)  # �޸�����
        print('д���±������')


    # ���ԵĴ���
    def test(self,mesh_indices,sel_mesh):
        getMeshName = self.reader.getMeshName(mesh_indices)
        print('getMeshName:' + str(getMeshName))
        # ��ȡ�����ص�ǰѡ��ģ�ͽṹ����
        cmds.select(getMeshName)
        name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs = self.get_mesh_structure()

        # ��ģ�ͽṹ����ת����dna���������
        mesh_indices, vertex_positions, vertex_normals, all_topology, uv, p_uv_nor_layout = self.data_required_for_conversion_into_dna(mesh_indices, name, vertex_positions, vertex_normals, all_topology,uv_coords_us, uv_coords_vs)
        # ��������
        self.set_topology(mesh_indices, all_topology)
        # �޸ĵ�λ�á����ߡ�UV����
        self.set_point_positions(mesh_indices, vertex_positions, vertex_normals, uv, p_uv_nor_layout)
        # ����bs
        self.reset_blendshape(mesh_indices)
        # �༭����λ��
        self.edit_joint_tr()
        # # ���õ�ǰָ�����Ȩ��
        # self.reset_joint_weight(mesh_indices)
        # �༭����Ȩ��
        self.edit_joint_weight(mesh_indices)

        # # ����ǰģ��д���bs
        # for bs_index, sel_index in zip([0],[0]):
        #     self.write_sel_model_to_bs(mesh_indices, bs_index, vertex_positions,sel_mesh[sel_index])

        # ����������ָ���޸�����
        # for face_drver_index in [191]:
        #     self.write_edit_drver_date(self.load_edit_drver_date(face_drver_index))
        # д��
        self.writer.write()
        print('д����ϣ������dna�鿴Ч����')
dna_edit_library().test(0,['asd'])
# end_time = time.time()
# # ���㲢��ӡ��ʱ
# elapsed_time = end_time - start_time
# print(f"������ʱ: {elapsed_time} ��")
# rl4Embedded_Archetype

