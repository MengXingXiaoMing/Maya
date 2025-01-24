#coding=gbk
'''
    ���ߣ����� ��ղ������<https://github.com/MengXingXiaoMing?tab=repositories>
    ����޸�: 2024-07-29
    �汾: 1.0.0
    ����һ������metahuman�ٷ���������⣬�����Ԥ�ƺ��˳��ù��ܣ���ʲô�����������ᣬ�һᾡ������.
    ����Ŀǰ��������ҵ���ҵ��ֻ�ܳ��д�����Ը��»�����ϣ����Ҽ��¡�
'''
import os
import sys
import inspect
from sys import path as syspath
from sys import platform

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel
# import time
# # ��¼��ʼʱ��
# start_time = time.time()


class DnaEditLibrary():
    def __init__(self):
        # �汾��
        self.maya_version = cmds.about(version=True)
        # ��ǰ�ļ�·��
        self.file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

        self.ROOT_DIR = self.file_path + '/custom_commands/MetaHuman-DNA-Calibration-main'
        self.MAYA_VERSION = self.maya_version  # 2022 or 2023
        self.ROOT_LIB_DIR = f"{self.ROOT_DIR}/lib/Maya{self.MAYA_VERSION}"
        self.reader = []
        self.writer = []
        # self.load_read()
        # self.load_write()

    # �����dna��
    def load_read(self, suore_path):
        if self.maya_version == '2022' or self.maya_version == '2023':
            # ������·�����������޸ģ����Ҫ�ĳ�һ���������б���
            # dnaԴ����·��
            self.soure_dna_path = suore_path
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

            print('dna�ѿ��Զ�ȡ��')
        else:
            cmds.warning("Maya�汾����,��֧��2022��2023�汾���糢���ٱ�İ汾�������޸ġ�")

    # ����дdna��
    def load_write(self, export_path, name):
        if self.maya_version == '2022' or self.maya_version == '2023':
            from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter
            # �������ɵ�dna·��
            self.target_dna_path = export_path + '/' + name + '.dna'
            # ���д���
            stream = FileStream(self.target_dna_path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
            self.writer = BinaryStreamWriter(stream)
            self.writer.setFrom(self.reader)
            print('dna�ѿ���д�롣')
        else:
            cmds.warning("Maya�汾����,��֧��2022��2023�汾���糢���ٱ�İ汾�������޸ġ�")

    # ��ȡ�����ص�ǰѡ��ģ�ͽṹ����(api 1.0)
    '''def get_mesh_structure(self):
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
            cmds.warning('��ѡ��һ���������')'''

    # ��ȡ�����ص�ǰѡ��ģ�ͽṹ����(api 2.0)
    def get_mesh_structure(self):
        selectList = om.MGlobal.getActiveSelectionList()
        depFn = om.MFnDependencyNode()
        for i in range(selectList.length()):
            node = selectList.getDependNode(i)
            type_syr = node.apiTypeStr
            # print("Type: %s" % type_syr)
            if type_syr == "kMesh":
                depFn.setObject(node)
                # types = om.MGlobal.getFunctionSetList(node)
                name = depFn.name()
                # print("Name: %s" % name)

                # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
                dag_path = selectList.getDagPath(0)
                # ��ȡ�ڵ�
                node = dag_path.node()
                # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
                # node = selectList.getDagPath(i)

                # ���ڵ��Ƿ�Ϊ����
                # node.hasFn(om.MFn.kMesh)

                # ����������򴴽�MFnMesh�����Է�����������
                mesh_fn = om.MFnMesh(node)
                # ��ȡ����Ķ�����
                num_verts = mesh_fn.numVertices
                # ��ȡ���������
                num_faces = mesh_fn.numPolygons
                print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

                # ����һ���б����洢����λ��
                vertex_positions = []
                # �������ж��㲢��ȡ���ǵ�λ��
                for i in range(num_verts):
                    point = mesh_fn.getPoint(i)
                    vertex_positions.append([point.x, point.y, point.z])
                # print('�㣺', vertex_positions)

                # ��ȡ����������
                normals = mesh_fn.getVertexNormals(False)
                # ��ȡ���㷨����ֵ����
                vertex_normals = []
                for i in range(num_verts):
                    normal_vec = normals[i]
                    vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
                # print('���ߣ�', vertex_normals)

                # ��ȡuv��
                uv_set = mesh_fn.getUVSetNames()

                # ����getUVs����������UV�������ƺ�MFloatArray������
                uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
                # print('U��', uv_coords_us)
                # print('V��', uv_coords_vs)
                # �����沢����
                all_topology = []
                for i in range(num_faces):
                    # �����ȡ����
                    topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                    topology = cmds.ls(topology, fl=1)
                    all_uv_num = []
                    for j in range(len(topology)):
                        # �����˻�ȡuv
                        uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num.append(num)
                    all_topology.append(all_uv_num)
                # print('����', all_topology)
                # ����ѡ��ص�ǰѡ��
                print('�ѻ�ȡ��ǰѡ��ģ�ͽṹ���ݡ�')
                # ���ص�ǰѡ������ơ������顢���㷨�����顢�������顢UV��uֵ����UV��vֵ
                return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs

    # ��ȡĬ��ģ������
    def get_default_model_data(self, mesh_indices):
        getVertexPositionCount = self.reader.getVertexPositionCount(mesh_indices)
        # print('getVertexPositionCount:' + str(getVertexPositionCount))
        vertex_positions = []
        for i in range(getVertexPositionCount):
            getVertexPosition = self.reader.getVertexPosition(mesh_indices, i)
            vertex_positions.append(getVertexPosition)
        # print('ģ�͵���ֵ��',len(vertex_positions),vertex_positions)

        getVertexNormalCount = self.reader.getVertexNormalCount(mesh_indices)
        # print('getVertexNormalCount:' + str(getVertexNormalCount))
        vertex_normals = []
        for i in range(getVertexNormalCount):
            getVertexNormal = self.reader.getVertexNormal(mesh_indices, i)
            vertex_normals.append(getVertexNormal)
        # print('���㷨����ֵ��',len(vertex_normals),vertex_normals)

        getFaceCount = self.reader.getFaceCount(0)
        # print('getFaceCount:' + str(getFaceCount))
        all_topology = []
        for i in range(getFaceCount):
            getFaceVertexLayoutIndices = self.reader.getFaceVertexLayoutIndices(mesh_indices, i)
            all_topology.append(getFaceVertexLayoutIndices)
        # print('���ˣ��棩���ݣ�', len(all_topology), all_topology)

        # getVertexTextureCoordinateCount = self.reader.getVertexTextureCoordinateCount(mesh_indices)
        # print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
        # getVertexTextureCoordinate = self.reader.getVertexTextureCoordinate(mesh_indices, 0)
        # print('getVertexTextureCoordinate:' + str(getVertexTextureCoordinate))
        getVertexTextureCoordinateUs = self.reader.getVertexTextureCoordinateUs(mesh_indices)
        # print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))
        # print('UV��uֵ��',len(uv_coords_us),uv_coords_us)

        getVertexTextureCoordinateVs = self.reader.getVertexTextureCoordinateVs(mesh_indices)
        # print('getVertexTextureCoordinateVs:' + str(len(getVertexTextureCoordinateVs)) + str(getVertexTextureCoordinateVs))
        # print('UV��vֵ��', len(uv_coords_vs), uv_coords_vs)

        getVertexLayoutCount = self.reader.getVertexLayoutCount(mesh_indices)
        all_uv_topology = []
        for i in range(getVertexLayoutCount):
            getVertexLayout = self.reader.getVertexLayout(mesh_indices, i)
            all_uv_topology.append(getVertexLayout)
        # print(all_uv_topology)

        # print('getVertexLayoutCount:' + str(getVertexLayoutCount))
        print(vertex_positions)
        print(vertex_normals)
        print(all_topology)
        print(getVertexTextureCoordinateUs)
        print(getVertexTextureCoordinateVs)
        print(all_uv_topology)
        # texture_coordinate_indices = []
        #
        # index_counter = 0
        #
        # for vertices_layout_index_array in dna_faces:
        #     for vertex_layout_index_array in vertices_layout_index_array:
        #         texture_coordinate = texture_coordinates[
        #             coordinate_indices[vertex_layout_index_array]
        #         ]
        #         texture_coordinate_us.append(texture_coordinate.u)
        #         texture_coordinate_vs.append(texture_coordinate.v)
        #         texture_coordinate_indices.append(index_counter)
        #         index_counter += 1
        return vertex_positions, vertex_normals, all_topology, getVertexTextureCoordinateUs, getVertexTextureCoordinateVs, all_uv_topology

    # ���ɶ�Ӧlodģ������
    def create_lod_model_data(self, lod_level):
        # ����������
        if not cmds.objExists('head_grp'):
            cmds.group(name='head_grp',em=1)
        if not cmds.objExists('geometry_grp'):
            cmds.group(name='geometry_grp', em=1,p='head_grp')
        # ��ȡ��ӦLODģ�����ݲ�����
        getMeshIndexListCount = self.reader.getMeshIndexListCount()
        # print('getMeshIndexListCount:' + str(getMeshIndexListCount))
        for i in range(len(lod_level)):
            for j in range(getMeshIndexListCount):
                if lod_level[i] == j:
                    cmds.group(name='head_lod'+str(j)+'_grp', em=1, p='geometry_grp')
                    # ��ȡ��ӦLOD��ģ��ָ��
                    getMeshIndicesForLOD = self.reader.getMeshIndicesForLOD(j)
                    # print('getMeshIndicesForLOD:' + str(getMeshIndicesForLOD))
                    # ��ȡdnaģ������
                    vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology = self.get_default_model_data(0)
                    # ��dna��������ģ��
                    # mesh_name = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us,uv_coords_vs, all_uv_topology, [])
                    # for k in getMeshIndicesForLOD:
                    #     # ��ȡģ������
                    #     getMeshName = self.reader.getMeshName(k)
                    #     # ��ȡdnaģ������
                    #     vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology = self.get_default_model_data(k)
                    #     # ��dna��������ģ��
                    #     mesh_name = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, [])
                    #     # cmds.rename(mesh_name, getMeshName)



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

    # �������
    def mirror_joint(self):
        pass

    # ɾ��������ͬʱ�Զ��޸�����
    def change_joint(self):
        pass

    # ��ģ�������ؼ������λ��
    def recalculate_joint_position(self):
        pass

    # ��ģ�������ؼ�������
    def recalculate_driver(self):
        pass


    def get_mesh_structure_2(self):
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

                # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
                dag_path = selectList.getDagPath(0)
                # ��ȡ�ڵ�
                node = dag_path.node()
                # ��ѡ���б��л�ȡ��i����ѡ�����DAG·��
                # node = selectList.getDagPath(i)

                # ���ڵ��Ƿ�Ϊ����
                # node.hasFn(om.MFn.kMesh)

                # ����������򴴽�MFnMesh�����Է�����������
                mesh_fn = om.MFnMesh(node)
                # ��ȡ����Ķ�����
                num_verts = mesh_fn.numVertices
                # ��ȡ���������
                num_faces = mesh_fn.numPolygons
                # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

                # ����һ���б����洢����λ��
                vertex_positions = []
                # �������ж��㲢��ȡ���ǵ�λ��
                for i in range(num_verts):
                    point = mesh_fn.getPoint(i)
                    vertex_positions.append([point.x, point.y, point.z])
                # print('�㣺', vertex_positions)

                # ��ȡƽ����
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

                line = cmds.ls(name+'.e[*]',fl=1)
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
                # print('ƽ���飺', smooth.smoothness)

                # ��ȡ��
                # a = [('polySurface1.f[0]'),('polySurface1.f[1]')]
                # dag_path_2 = a[0].getDagPath(0)
                # iterator = om.MItMeshPolygon(dag_path_2)
                # edges = iterator.getEdges()
                # print(edges)

                # ��ȡ����������
                normals = mesh_fn.getVertexNormals(False)
                # ��ȡ���㷨����ֵ����
                vertex_normals = []
                for i in range(num_verts):
                    normal_vec = normals[i]
                    vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
                # print('���ߣ�', vertex_normals)

                # ��ȡuv��
                uv_set = mesh_fn.getUVSetNames()

                # ����getUVs����������UV�������ƺ�MFloatArray������
                uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
                # print('U��', uv_coords_us)
                # print('V��', uv_coords_vs)
                # �����沢����
                all_topology = []
                for i in range(num_faces):
                    # �����ȡ����
                    topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                    topology = cmds.ls(topology, fl=1)
                    all_uv_num = []
                    for j in range(len(topology)):
                        # �����˻�ȡuv
                        uv = cmds.polyListComponentConversion(topology[j], tv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num.append(num)
                    all_topology.append(all_uv_num)
                # print('����', all_topology)

                all_uv_topology = []
                for i in range(num_faces):
                    # �����ȡ����
                    topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                    topology = cmds.ls(topology, fl=1)
                    all_uv_num = []
                    for j in range(len(topology)):
                        # �����˻�ȡuv
                        uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num.append(num)
                    all_uv_topology.append(all_uv_num)
                # ����ѡ��ص�ǰѡ��
                print('�ѻ�ȡ��ǰѡ��ģ�ͽṹ���ݡ�')
                # ���ص�ǰѡ������ơ������顢���㷨�����顢�������顢UV��uֵ����UV��vֵ
                return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group

    # ��������
    def creare_mesh(self, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group):
        print(vertex_positions)
        print(vertex_normals)
        print(all_topology)
        print(uv_coords_us)
        print(uv_coords_vs)
        print(all_uv_topology)
        print(smooth_group)
        # ����λ��
        vertices = vertex_positions
        # ת��ΪOM����
        vertex_positions = []
        for vertex in vertices:
            vertex_positions.append(om.MPoint(vertex[0], vertex[1], vertex[2]))

        # ÿ���������Ķ�������
        face_counts = []  # ÿ����Ķ����������ﶼ���ı��Σ����Զ���4
        for f in all_topology:
            face_counts.append(len(f))

        # ÿ����Ķ�������
        face_connects = []
        for face in all_topology:
            for index in face:
                face_connects.append(index)

        # print(vertex_positions)
        # print(face_counts)
        # # print(face_connects)
        # ��������
        mesh_fn = om.MFnMesh()
        mesh_obj = mesh_fn.create(vertex_positions, face_counts, face_connects, uv_coords_us, uv_coords_vs)

        # print(all_uv_topology)
        uv_face_counts = []  # ÿ����Ķ����������ﶼ���ı��Σ����Զ���4
        for f in all_uv_topology:
            uv_face_counts.append(len(f))
        uvIds = [item for sublist in all_uv_topology for item in sublist]
        # print(len(uvIds), uvIds)
        # ����UV
        mesh_uv = mesh_fn.assignUVs(uv_face_counts, uvIds)

        # ���÷���
        # print(vertex_normals)
        normals = []
        for vertex in vertex_normals:
            normals.append(om.MVector(vertex[0], vertex[1], vertex[2]))
        # print(normals)
        normals_indices = []
        for i in range(len(normals)):
            normals_indices.append(i)
        mesh_fn.setVertexNormals(normals, normals_indices)

        # ����ƽ����
        name = mesh_fn.name()
        # ����ƽ����ѡ��
        smooth_line = []
        if smooth_line:
            for i in smooth_group:
                smooth_line.append(name+'.e['+str(i)+']')
            # print('ƽ���飺',smooth_line)
            # print('ƽ���飺',smooth_group)
            cmds.polySoftEdge(smooth_line, a=0, ch=0)
        # ���ᵱǰ����
        cmds.polyNormalPerVertex(name,ufn=1)


        # # ����һ���µı任�ڵ���Ϊ����ĸ��ڵ�
        # dep_fn = om.MFnDependencyNode()
        # transform_obj = om.MFnTransform().create()
        # dep_fn.setObject(transform_obj)
        #
        # # �����񸽼ӵ��任�ڵ���
        # # ע�⣺�� Maya �У�����ڵ�ͨ������ֱ�Ӵ����ģ�������Ϊ�任�ڵ���ӽڵ㴴����
        # # ����������ʹ�õ��ǵײ� API�����������ֶ�����һ���任�ڵ㣬����������󸽼ӵ�������
        # # �� UI �У���ͨ����ͨ���ڡ������ͼ�����϶����񵽱任�ڵ�������ɵ�
        # # ���ڵײ� API �У�������Ҫʹ�� MDagModifier ������������
        # dag_modifier = om.MDagModifier()
        # dag_modifier.reparentNode(mesh_obj, transform_obj)
        # dag_modifier.doIt()

        # ����
        # del dag_modifier
        return name

    # Ϊģ�͸������
    def assign_material(self, mesh_shape, material_type, have_material):
        # ���Ի�ȡģ�͵���ɫ��
        shading_groups = cmds.listConnections(mesh_shape[0] + '.instObjGroups', shapes=True) or []
        if not shading_groups:
            # �򴴽�һ���µ���ɫ��
            shading_groups = cmds.shadingNode('shadingEngine', asUtility=1, n=mesh_shape[0] + '_SG')
            # ����ģ�ͺͲ�����
            cmds.connectAttr((mesh_shape[0] + '.instObjGroups[0]'), (shading_groups + '.dagSetMembers[0]'), force=1)
        else:
            # ������ڶ����ɫ�飬ͨ������ֻ���ĵ�һ��
            shading_groups = shading_groups[0]
        if have_material:
            shader_name = have_material[0]
        else:
            # ����һ������
            shader_name = cmds.shadingNode(material_type, asShader=True, name=mesh_shape[0] + '_material')
            # print(shader_name)
        # ���Ӳ��ʺ���ɫ��
        cmds.connectAttr((shader_name + '.outColor'), (shading_groups + '.surfaceShader'), force=1)
        return shader_name

    # �򵥱༭����
    def edit_material(self, material_name, color, roughness, transparency):
        # ������ɫ
        if color:
            file_node = self.create_2d_texture()
            cmds.setAttr(file_node + '.fileTextureName', color, type="string")
            cmds.connectAttr((file_node + '.outColor'), (material_name + '.color'), force=1)
        # ���ôֲڶ�
        if roughness:
            file_node = self.create_2d_texture()
            cmds.setAttr(file_node + '.fileTextureName', color, type="string")
            cmds.connectAttr((file_node + '.outAlpha'), (material_name + '.diffuse'), force=1)
        # ����͸����
        if transparency:
            file_node = self.create_2d_texture()
            cmds.setAttr(file_node + '.fileTextureName', color, type="string")
            cmds.connectAttr((file_node + '.outColor'), (material_name + '.transparency'), force=1)

    # ������ά��ͼ
    def create_2d_texture(self):
        texture = cmds.shadingNode('file', asTexture=1, isColorManaged=1)
        # Result: file1
        uv = cmds.shadingNode('place2dTexture', asUtility=1)
        # Result: place2dTexture1
        cmds.connectAttr(uv+'.coverage', texture+'.coverage', f=1)
        # Result: Connected place2dTexture1.coverage to file1.coverage.
        cmds.connectAttr(uv+'.translateFrame', texture+'.translateFrame', f=1)
        # Result: Connected place2dTexture1.translateFrame to file1.translateFrame.
        cmds.connectAttr(uv+'.rotateFrame', texture+'.rotateFrame', f=1)
        # Result: Connected place2dTexture1.rotateFrame to file1.rotateFrame.
        cmds.connectAttr(uv+'.mirrorU', texture+'.mirrorU', f=1)
        # Result: Connected place2dTexture1.mirrorU to file1.mirrorU.
        cmds.connectAttr(uv+'.mirrorV', texture+'.mirrorV', f=1)
        # Result: Connected place2dTexture1.mirrorV to file1.mirrorV.
        cmds.connectAttr(uv+'.stagger', texture+'.stagger', f=1)
        # Result: Connected place2dTexture1.stagger to file1.stagger.
        cmds.connectAttr(uv+'.wrapU', texture+'.wrapU', f=1)
        # Result: Connected place2dTexture1.wrapU to file1.wrapU.
        cmds.connectAttr(uv+'.wrapV', texture+'.wrapV', f=1)
        # Result: Connected place2dTexture1.wrapV to file1.wrapV.
        cmds.connectAttr(uv+'.repeatUV', texture+'.repeatUV', f=1)
        # Result: Connected place2dTexture1.repeatUV to file1.repeatUV.
        cmds.connectAttr(uv+'.offset', texture+'.offset', f=1)
        # Result: Connected place2dTexture1.offset to file1.offset.
        cmds.connectAttr(uv+'.rotateUV', texture+'.rotateUV', f=1)
        # Result: Connected place2dTexture1.rotateUV to file1.rotateUV.
        cmds.connectAttr(uv+'.noiseUV', texture+'.noiseUV', f=1)
        # Result: Connected place2dTexture1.noiseUV to file1.noiseUV.
        cmds.connectAttr(uv+'.vertexUvOne', texture+'.vertexUvOne', f=1)
        # Result: Connected place2dTexture1.vertexUvOne to file1.vertexUvOne.
        cmds.connectAttr(uv+'.vertexUvTwo', texture+'.vertexUvTwo', f=1)
        # Result: Connected place2dTexture1.vertexUvTwo to file1.vertexUvTwo.
        cmds.connectAttr(uv+'.vertexUvThree', texture+'.vertexUvThree', f=1)
        # Result: Connected place2dTexture1.vertexUvThree to file1.vertexUvThree.
        cmds.connectAttr(uv+'.vertexCameraOne', texture+'.vertexCameraOne', f=1)
        # Result: Connected place2dTexture1.vertexCameraOne to file1.vertexCameraOne.
        cmds.connectAttr(uv+'.outUV', texture+'.uv')
        # Result: Connected place2dTexture1.outUV to file1.uvCoord.
        cmds.connectAttr(uv+'.outUvFilterSize', texture+'.uvFilterSize')
        # Result: Connected place2dTexture1.outUvFilterSize to file1.uvFilterSize.
        return texture

    # ��������
    def export_material(self, file_path, type):
        materials = cmds.ls(materials=True)
        materials = [x for x in materials if x not in ['lambert1', 'standardSurface1', 'particleCloud1']]
        print('�Զ������:',materials)
        cmds.select(materials)
        # ������ǰѡ��
        cmds.file(file_path, pr=1, typ=type, es=1, op='v=0;')  # mayaBinary or mayaAscii
        return materials

    # �����ļ�
    def import_file(self, file_path, type):
        cmds.file(file_path, pr=1, ignoreVersion=1, i=1, type=type, namespace=':', importTimeRange='combine', ra=True,
                  mergeNamespacesOnClash=True, options="v=0;")

    # �Ƴ��������
    def remove_material(self):
        # ��֪��Ϊʲô����Ҫ�������β���Ч��
        # �������
        materials = cmds.ls(materials=True)
        materials = [x for x in materials if x not in ['lambert1', 'standardSurface1', 'particleCloud1']]
        # print('�Զ������:', materials)
        # �������в���
        for mat in materials:
            # ��ȡ��ò��ʹ��������нڵ㣨��ͨ���������ӵ����ʵ�����
            connections = cmds.listConnections(mat, source=False, destination=True,type='shadingEngine')
            if not connections:
                cmds.delete(mat)
        # ������ɫ��
        shadingEngine = cmds.ls(type='shadingEngine')
        shadingEngine = [x for x in shadingEngine if x not in ['initialParticleSE', 'initialShadingGroup']]
        # ����������ɫ��
        for se in shadingEngine:
            # ��ȡ��ò��ʹ��������нڵ㣨��ͨ���������ӵ����ʵ�����
            connections = cmds.listConnections(se, destination=True,type='mesh')
            if not connections:
                cmds.delete(se)
        # print('�Զ�����ɫ�飺',shadingEngine)

    # ������
    def clear_scene(self):
        file_path = cmds.internalVar(mid=True)
        file_path = file_path + '/scripts/startup/cleanUpScene.mel'

        mel.eval('source "' + file_path + '";')
        mel.eval('deleteEmptyGroups();')
        mel.eval('deleteEmptyLayers("Display");')
        mel.eval('deleteEmptyLayers("Render");')
        mel.eval('deleteUnusedExpressions();')
        mel.eval('deleteUnusedLocators();')
        mel.eval('deleteUnusedPairBlends();')
        mel.eval('deleteUnusedTrax("clips");')
        mel.eval('deleteUnusedTrax("poses");')
        mel.eval('deleteUnusedDeformers();')
        mel.eval('MLdeleteUnused();')
        mel.eval('RNdeleteUnused();')
        mel.eval('deleteUnusedBrushes();')
        mel.eval('deleteUnusedCommon( "groupId", 0, (uiRes("m_cleanUpScene.kDeletingUnusedGroupIDNodes2")) );')
        mel.eval('deleteUnusedInUnusedHierarchy( "nurbsCurve", 0, (uiRes("m_cleanUpScene.kDeletingUnusedNurbsCurves2")));')
        mel.eval('deleteInvalidNurbs(0);')
        mel.eval('string $myTemporaryStringArray[] = {"0"};')
        mel.eval('doRemoveDuplicateShadingNetworks($myTemporaryStringArray,$myTemporaryStringArray);')

        print('���������')

    # def _build(self) -> bool:
    #     self.new_scene()
    #     self.set_filtered_meshes()
    #
    #     self.create_groups()
    #
    #     self.set_units()
    #     self.add_joints()
    #     self.build_meshes()
    #     self.add_ctrl_attributes_on_root_joint()
    #     self.add_animated_map_attributes_on_root_joint()
    #     self.add_key_frames()

    # ���ԵĴ���
    def test(self, mesh_indices, sel_mesh):
        self.load_read('D:/Personal/zhankangming/Desktop/MH_text_demo/Ada.dna')
        self.load_write('D:/Personal/zhankangming/Desktop/MH_text_demo', 'Archetype')
        # cmds.select('head_lod0_meshShape')
        # sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = self.get_mesh_structure_2()
        # print('asd')
        # mesh = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group)
        # print('���ɵ�ģ�ͣ�',mesh)
        # shader_name = self.assign_material([mesh], 'lambert', [])
        # print('���ɵĲ���/���в��ʣ�',shader_name)
        #
        # # �༭���ɵĲ���
        # self.edit_material(shader_name,
        #                    'D:/Personal/zhankangming/Desktop/ZIBLT1KU[[Q_)8XU2XUCMWC.jpg',
        #                    'D:/Personal/zhankangming/Desktop/ZIBLT1KU[[Q_)8XU2XUCMWC.jpg',
        #                    'D:/Personal/zhankangming/Desktop/ZIBLT1KU[[Q_)8XU2XUCMWC.jpg')
        #
        # # ��������
        # self.clear_scene()
        #
        # # ���������Զ������
        # print(self.export_material('D:/Personal/zhankangming/Desktop/asddsaga123.ma', 'mayaAscii'))
        #
        # # �������
        # self.import_file('D:/Personal/zhankangming/Desktop/asddsaga123.ma', 'mayaAscii')

        # self.load_read_write()
        # self.assign_material('pCubeShape1', 'lambert1')
        # getMeshName = self.reader.getMeshName(mesh_indices)
        # print('getMeshName:' + str(getMeshName))
        # # ��ȡ�����ص�ǰѡ��ģ�ͽṹ����
        # shape = cmds.listRelatives(getMeshName, c=1, type='mesh')
        # cmds.select(shape)
        # name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs = self.get_mesh_structure()
        #
        # # ��ģ�ͽṹ����ת����dna���������
        # mesh_indices, vertex_positions, vertex_normals, all_topology, uv, p_uv_nor_layout = self.data_required_for_conversion_into_dna(mesh_indices, name, vertex_positions, vertex_normals, all_topology,uv_coords_us, uv_coords_vs)
        # # ��������
        # self.set_topology(mesh_indices, all_topology)
        # # �޸ĵ�λ�á����ߡ�UV����
        # self.set_point_positions(mesh_indices, vertex_positions, vertex_normals, uv, p_uv_nor_layout)
        # # ����bs
        # self.reset_blendshape(mesh_indices)
        # # �༭����λ��
        # self.edit_joint_tr()
        # # # ���õ�ǰָ�����Ȩ��
        # # self.reset_joint_weight(mesh_indices)
        # # �༭����Ȩ��
        # self.edit_joint_weight(mesh_indices)
        #
        # # ����ǰģ��д���bs
        # for bs_index, sel_index in zip([0],[0]):
        #     self.write_sel_model_to_bs(mesh_indices, bs_index, vertex_positions,sel_mesh[sel_index])
        #
        # # ����������ָ���޸�����
        # for face_drver_index in [191]:
        #     self.write_edit_drver_date(self.load_edit_drver_date(face_drver_index))
        # # д��
        # # self.writer.write()


        getMeshCount = self.reader.getMeshCount()
        print('getMeshCount:' + str(getMeshCount))
        getMeshName = self.reader.getMeshName(0)
        print('getMeshName:' + str(getMeshName))
        getMeshIndexListCount = self.reader.getMeshIndexListCount()
        print('getMeshIndexListCount:' + str(getMeshIndexListCount))
        getMeshIndicesForLOD = self.reader.getMeshIndicesForLOD(0)
        print('getMeshIndicesForLOD:' + str(getMeshIndicesForLOD))

        self.create_lod_model_data([0])
        print('д����ϣ������dna�鿴Ч����')

# DnaEditLibrary().test(0,['asd'])

# end_time = time.time()
# # ���㲢��ӡ��ʱ
# elapsed_time = end_time - start_time
# print(f"������ʱ: {elapsed_time} ��")


