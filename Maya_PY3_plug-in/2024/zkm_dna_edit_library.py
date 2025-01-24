#coding=gbk
'''
    作者：梦星 （詹康明）<https://github.com/MengXingXiaoMing?tab=repositories>
    最后修改: 2024-07-29
    版本: 1.0.0
    这是一个基于metahuman官方库的衍生库，给大家预制好了常用功能，有什么别的需求可以提，我会尽力满足.
    由于目前这个不是我的主业，只能抽空写，所以更新缓慢，希望大家见谅。
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
# # 记录开始时间
# start_time = time.time()


class DnaEditLibrary():
    def __init__(self):
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 当前文件路径
        self.file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

        self.ROOT_DIR = self.file_path + '/custom_commands/MetaHuman-DNA-Calibration-main'
        self.MAYA_VERSION = self.maya_version  # 2022 or 2023
        self.ROOT_LIB_DIR = f"{self.ROOT_DIR}/lib/Maya{self.MAYA_VERSION}"
        self.reader = []
        self.writer = []
        # self.load_read()
        # self.load_write()

    # 载入读dna库
    def load_read(self, suore_path):
        if self.maya_version == '2022' or self.maya_version == '2023':
            # 这两个路径个可自行修改，如果要改成一样的请自行备份
            # dna源数据路径
            self.soure_dna_path = suore_path
            if platform == "win32":
                LIB_DIR = f"{self.ROOT_LIB_DIR}/windows"
            elif platform == "linux":
                LIB_DIR = f"{self.ROOT_LIB_DIR}/linux"
            else:
                raise OSError(
                    "OS not supported, please compile dependencies and add value to LIB_DIR"
                )

            # 将目录添加到路径
            syspath.insert(0, self.ROOT_DIR)
            syspath.insert(0, LIB_DIR)
            from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter

            # 添加读取库
            stream = FileStream(self.soure_dna_path, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
            self.reader = BinaryStreamReader(stream, DataLayer_All)
            self.reader.read()

            print('dna已可以读取。')
        else:
            cmds.warning("Maya版本错误,仅支持2022和2023版本，如尝试再别的版本请自行修改。")

    # 载入写dna库
    def load_write(self, export_path, name):
        if self.maya_version == '2022' or self.maya_version == '2023':
            from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter
            # 重新生成的dna路径
            self.target_dna_path = export_path + '/' + name + '.dna'
            # 添加写入库
            stream = FileStream(self.target_dna_path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
            self.writer = BinaryStreamWriter(stream)
            self.writer.setFrom(self.reader)
            print('dna已可以写入。')
        else:
            cmds.warning("Maya版本错误,仅支持2022和2023版本，如尝试再别的版本请自行修改。")

    # 获取并返回当前选择模型结构数据(api 1.0)
    '''def get_mesh_structure(self):
        sel = cmds.ls(sl=1)
        shape = cmds.listRelatives(sel, c=1, type='mesh')
        if shape:
            # 选择形状节点
            cmds.select(shape)
            # 建立MSelectionList数据存放当前选择数据
            sel_list = om.MSelectionList()
            # 获取当前选择并填充到sel_list中
            om.MGlobal.getActiveSelectionList(sel_list)
            result = [om.MObject()] * 1
            sel_list.getDependNode(0, result[0])
            # 准备用dep_node_fn来获取更多关于节点的信息
            dep_node_fn = om.MFnDependencyNode(result[0])

            # sel_name = dep_node_fn.name()
            # print(dep_node_fn.name())  # 打印节点名称

            # sel_type = dep_node_fn.typeName()
            # print(dep_node_fn.typeName())  # 打印节点类型

            # 仅获取选择列表中的第一个选择的项目的数据

            # 为选中的对象创建一个新的MDagPath实例
            dag_path = [om.MDagPath()] * sel_list.length()
            # 从选择列表中获取第i个被选对象的DAG路径
            sel_list.getDagPath(0, dag_path[0])
            # 获取节点
            node = dag_path[0].node()

            # 检查节点是否为网格
            # node.hasFn(om.MFn.kMesh)

            # 如果是网格，则创建MFnMesh对象以访问网格数据
            mesh_fn = om.MFnMesh(node)
            # 获取网格的顶点数
            num_verts = mesh_fn.numVertices()
            # 获取网格的面数
            num_faces = mesh_fn.numPolygons()
            # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

            # 创建一个列表来存储顶点位置
            vertex_positions = []
            # 遍历所有顶点并获取它们的位置
            for i in range(num_verts):
                point = om.MPoint()
                mesh_fn.getPoint(i, point)
                vertex_positions.append([point.x, point.y, point.z])

            # 获取顶法线数组
            normals = om.MFloatVectorArray()
            mesh_fn.getVertexNormals(False, normals)
            # 获取顶点法线数值数组
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])

            # 获取uv集
            uv_set = []
            mesh_fn.getUVSetNames(uv_set)

            # 创建一个MFloatArray来存储UV坐标
            uv_coords_us = om.MFloatArray()
            uv_coords_vs = om.MFloatArray()
            # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
            mesh_fn.getUVs(uv_coords_us, uv_coords_vs, uv_set[0])

            # 遍历面并建立
            all_topology = []
            for i in range(num_faces):
                # 按面获取拓扑
                topology = cmds.polyListComponentConversion(sel[0]+'.f[' + str(i) + ']', tvf=True)
                topology = cmds.ls(topology, fl=1)
                all_uv_num = []
                for j in range(len(topology)):
                    # 按拓扑获取uv
                    uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num.append(num)
                all_topology.append(all_uv_num)

            # 重新选择回当前选择
            cmds.select(sel)
            print('已获取当前选择模型结构数据。')
            # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
            return sel[0], vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs
        else:
            cmds.warning('请选择一个网格对象。')'''

    # 获取并返回当前选择模型结构数据(api 2.0)
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
                print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

                # 创建一个列表来存储顶点位置
                vertex_positions = []
                # 遍历所有顶点并获取它们的位置
                for i in range(num_verts):
                    point = mesh_fn.getPoint(i)
                    vertex_positions.append([point.x, point.y, point.z])
                # print('点：', vertex_positions)

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
                        uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                        uv = cmds.ls(uv, fl=1)
                        num = int(uv[0].split('[')[1][:-1])
                        all_uv_num.append(num)
                    all_topology.append(all_uv_num)
                # print('拓扑', all_topology)
                # 重新选择回当前选择
                print('已获取当前选择模型结构数据。')
                # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
                return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs

    # 获取默认模型数据
    def get_default_model_data(self, mesh_indices):
        getVertexPositionCount = self.reader.getVertexPositionCount(mesh_indices)
        # print('getVertexPositionCount:' + str(getVertexPositionCount))
        vertex_positions = []
        for i in range(getVertexPositionCount):
            getVertexPosition = self.reader.getVertexPosition(mesh_indices, i)
            vertex_positions.append(getVertexPosition)
        # print('模型点数值：',len(vertex_positions),vertex_positions)

        getVertexNormalCount = self.reader.getVertexNormalCount(mesh_indices)
        # print('getVertexNormalCount:' + str(getVertexNormalCount))
        vertex_normals = []
        for i in range(getVertexNormalCount):
            getVertexNormal = self.reader.getVertexNormal(mesh_indices, i)
            vertex_normals.append(getVertexNormal)
        # print('顶点法线数值：',len(vertex_normals),vertex_normals)

        getFaceCount = self.reader.getFaceCount(0)
        # print('getFaceCount:' + str(getFaceCount))
        all_topology = []
        for i in range(getFaceCount):
            getFaceVertexLayoutIndices = self.reader.getFaceVertexLayoutIndices(mesh_indices, i)
            all_topology.append(getFaceVertexLayoutIndices)
        # print('拓扑（面）数据：', len(all_topology), all_topology)

        # getVertexTextureCoordinateCount = self.reader.getVertexTextureCoordinateCount(mesh_indices)
        # print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
        # getVertexTextureCoordinate = self.reader.getVertexTextureCoordinate(mesh_indices, 0)
        # print('getVertexTextureCoordinate:' + str(getVertexTextureCoordinate))
        getVertexTextureCoordinateUs = self.reader.getVertexTextureCoordinateUs(mesh_indices)
        # print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))
        # print('UV的u值：',len(uv_coords_us),uv_coords_us)

        getVertexTextureCoordinateVs = self.reader.getVertexTextureCoordinateVs(mesh_indices)
        # print('getVertexTextureCoordinateVs:' + str(len(getVertexTextureCoordinateVs)) + str(getVertexTextureCoordinateVs))
        # print('UV的v值：', len(uv_coords_vs), uv_coords_vs)

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

    # 生成对应lod模型数据
    def create_lod_model_data(self, lod_level):
        # 创建基础组
        if not cmds.objExists('head_grp'):
            cmds.group(name='head_grp',em=1)
        if not cmds.objExists('geometry_grp'):
            cmds.group(name='geometry_grp', em=1,p='head_grp')
        # 获取对应LOD模型数据并生成
        getMeshIndexListCount = self.reader.getMeshIndexListCount()
        # print('getMeshIndexListCount:' + str(getMeshIndexListCount))
        for i in range(len(lod_level)):
            for j in range(getMeshIndexListCount):
                if lod_level[i] == j:
                    cmds.group(name='head_lod'+str(j)+'_grp', em=1, p='geometry_grp')
                    # 获取对应LOD的模型指针
                    getMeshIndicesForLOD = self.reader.getMeshIndicesForLOD(j)
                    # print('getMeshIndicesForLOD:' + str(getMeshIndicesForLOD))
                    # 获取dna模型数据
                    vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology = self.get_default_model_data(0)
                    # 按dna数据生成模型
                    # mesh_name = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us,uv_coords_vs, all_uv_topology, [])
                    # for k in getMeshIndicesForLOD:
                    #     # 获取模型名称
                    #     getMeshName = self.reader.getMeshName(k)
                    #     # 获取dna模型数据
                    #     vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology = self.get_default_model_data(k)
                    #     # 按dna数据生成模型
                    #     mesh_name = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, [])
                    #     # cmds.rename(mesh_name, getMeshName)



    # 将模型结构数据转换成dna所需的数据
    def data_required_for_conversion_into_dna(self, mesh_indices, name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs):
        '''getMeshName = self.reader.getMeshName(mesh_indices)
        print('getMeshName:' + str(getMeshName))'''
        # print('对象名称：',name)

        '''getVertexPositionCount = self.reader.getVertexPositionCount(mesh_indices)
        print('getVertexPositionCount:' + str(getVertexPositionCount))
        getVertexPosition = self.reader.getVertexPosition(mesh_indices, 0)
        print('getVertexPosition:' + str(getVertexPosition))'''
        # print('模型点数值：',len(vertex_positions),vertex_positions)

        '''getVertexNormalCount = self.reader.getVertexNormalCount(mesh_indices)
        print('getVertexNormalCount:' + str(getVertexNormalCount))
        getVertexNormal = self.reader.getVertexNormal(mesh_indices, 0)
        print('getVertexNormal:' + str(getVertexNormal))'''
        # print('顶点法线数值：',len(vertex_normals),vertex_normals)

        '''getFaceCount = self.reader.getFaceCount(0)
        print('getFaceCount:' + str(getFaceCount))
        getFaceVertexLayoutIndices = self.reader.getFaceVertexLayoutIndices(mesh_indices, 0)
        print('getFaceVertexLayoutIndices:' + str(getFaceVertexLayoutIndices))'''
        # print('拓扑（面）数据：', len(all_topology), all_topology)

        '''getVertexTextureCoordinateCount = self.reader.getVertexTextureCoordinateCount(mesh_indices)
        print('getVertexTextureCoordinateCount:' + str(getVertexTextureCoordinateCount))
        getVertexTextureCoordinate = self.reader.getVertexTextureCoordinate(mesh_indices, 0)
        print('getVertexTextureCoordinate:' + str(getVertexTextureCoordinate))
        getVertexTextureCoordinateUs = self.reader.getVertexTextureCoordinateUs(mesh_indices)
        print('getVertexTextureCoordinateUs:' + str(len(getVertexTextureCoordinateUs)) + str(getVertexTextureCoordinateUs))'''
        # print('UV的u值：',len(uv_coords_us),uv_coords_us)

        '''getVertexTextureCoordinateVs = self.reader.getVertexTextureCoordinateVs(mesh_indices)
        print('getVertexTextureCoordinateVs:' + str(len(getVertexTextureCoordinateVs)) + str(getVertexTextureCoordinateVs))'''
        # print('UV的v值：', len(uv_coords_vs), uv_coords_vs)

        '''getVertexLayoutCount = self.reader.getVertexLayoutCount(0)
        print('getVertexLayoutCount:' + str(getVertexLayoutCount))'''

        # 开始构建[点指针,uv指针,点法线指针]数组
        '''
        此处额外说明：
            如果你打印模板文件的会发现很乱，但是经过我大量测试是可以按顺序排列的，纯粹是模板的模型结构数据存放混乱导致的，应该是获取的时候不是正向获
            取的，导致指针也乱七八糟的，我甚至怀疑规律存在误导的情况，总之要是你要从官方的数据开始查的话要做好头大的准备。
        '''
        p_uv_nor_layout = []
        for i in range(len(uv_coords_us)):
            point = cmds.polyListComponentConversion(name + '.map[' + str(i) + ']', tv=True)
            point = cmds.ls(point, fl=True)
            num = int(point[0].split('[')[1][:-1])
            layout = [num, i, num]
            p_uv_nor_layout.append(layout)
        # print('[点指针，uv指针，点法线指针]数组：',len(p_uv_nor_layout), p_uv_nor_layout)

        # 创建uv数值数组
        uv = []
        for i in range(len(uv_coords_us)):
            point = [uv_coords_us[i], uv_coords_vs[i]]
            uv.append(point)
        # print('uv数值数组：', len(uv), uv)

        print('已经转化成编辑dna所需数据。')
        # 返回模型指针，点数组，点法线数组，拓扑，uv数组，[点指针,uv指针,点法线指针]数组
        return mesh_indices, vertex_positions, vertex_normals, all_topology, uv, p_uv_nor_layout

    # 修改点位置、法线、UV坐标
    def set_point_positions(self, mesh_indices, vertex_positions, vertex_normals, uv, p_uv_nor_layout):
        # 设置点位置
        self.writer.setVertexPositions(mesh_indices, vertex_positions)
        # 设置点法线
        self.writer.setVertexNormals(mesh_indices, vertex_normals)
        # 设置点UV位置
        self.writer.setVertexTextureCoordinates(mesh_indices, uv)
        # 设置[点指针,uv指针,点法线指针]数组
        self.writer.setVertexLayouts(mesh_indices, p_uv_nor_layout)
        print(mesh_indices, '模型点位置、法线、UV坐标以更新。')

    # 设置拓扑
    def set_topology(self, mesh_indices, all_topology):
        # 清理拓扑（面）
        self.writer.clearFaceVertexLayoutIndices(mesh_indices)
        # 设置拓扑（面）
        for faceIndex in range(len(all_topology)):
            layoutIndices = all_topology[faceIndex]
            self.writer.setFaceVertexLayoutIndices(mesh_indices, faceIndex, layoutIndices)
        print(mesh_indices, '当前指针拓扑已更新。')

    # 重置bs
    def reset_blendshape(self, mesh_indices):
        # 获取bs数量，bs数目和名称啥的不改最好，bs也别删它，不用的变化数值清零就好
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
        print(mesh_indices,'所有bs偏移数值已经重置。')

    # 重置骨骼权重
    def reset_joint_weight(self,mesh_indices):
        # 获取模型点数量
        getSkinWeightsCount = self.reader.getSkinWeightsCount(mesh_indices)
        # print('getSkinWeightsCount:' + str(getSkinWeightsCount))
        for j in range(getSkinWeightsCount):
            self.writer.setSkinWeightsJointIndices(mesh_indices, j, [0])
            self.writer.setSkinWeightsValues(mesh_indices, j, [1])
        print('骨骼权重已经重置。')

    # 编辑骨骼权重
    def edit_joint_weight(self, mesh_indices):
        # 获取模型数量
        # getMeshCount = self.reader.getMeshCount()
        # print('getMeshCount:' + str(getMeshCount))
        # 获取骨骼数量
        getJointCount = self.reader.getJointCount()
        # print('getJointCount:' + str(getJointCount))
        # 对每个模型逐个开始修改
        # 获取模型名称
        getMeshName = self.reader.getMeshName(mesh_indices)
        print('getMeshName:' + str(getMeshName))
        # 获取蒙皮节点
        history = cmds.listHistory(getMeshName)
        skinClusterName = ''
        for node in history:
            if cmds.nodeType(node) == 'skinCluster':
                skinClusterName = node
                break
        # 移除多余影响
        cmds.RemoveUnusedInfluences(skinClusterName)
        # 获取受影响的骨骼
        source_skin_joint = cmds.skinCluster(getMeshName, q=1, inf=1)
        # print(len(source_skin_joint), source_skin_joint)
        # 获取模型点数量
        # getSkinWeightsCount = self.reader.getSkinWeightsCount(mesh_indices)
        # print('getSkinWeightsCount:' + str(getSkinWeightsCount))
        # 获取模型点列表
        mesh_visit_list = cmds.ls(getMeshName + '.vtx[*]', fl=1)
        # print(len(mesh_visit_list), mesh_visit_list)
        # 按点获取权重创建修改列表
        clearSkinWeights = self.writer.clearSkinWeights(mesh_indices)
        # print('clearSkinWeights:' + str(clearSkinWeights))
        # 获取其影响的骨骼在所有骨骼中的指针位置
        joint_index_list = []
        for k in range(getJointCount):
            getJointName = self.reader.getJointName(k)
            for l in range(len(source_skin_joint)):
                if source_skin_joint[l] == getJointName:
                    joint_index_list.append(k)
        # print(len(joint_index_list), joint_index_list)
        # 开始逐个点修改
        for j in range(len(mesh_visit_list)):
            weight_list = []
            joint_list = []
            # 获取每个骨骼在某个点的权重数值
            weight = cmds.skinPercent(skinClusterName, mesh_visit_list[j], q=True, v=True)
            # 将有数值的骨骼和其数值加载到新列表
            for w in range(len(weight)):
                if weight[w] > 0:
                    joint_list.append(joint_index_list[w])
                    weight_list.append(weight[w])
            self.writer.setSkinWeightsJointIndices(mesh_indices, j, joint_list)
            self.writer.setSkinWeightsValues(mesh_indices, j, weight_list)
        print('所有骨骼权重都已更新。')

    # 编辑骨骼位置
    def edit_joint_tr(self):
        getJointCount = self.reader.getJointCount()
        # print('getJointCount:' + str(getJointCount))
        need_write_translate_list = []
        need_write_rotate_list = []
        for i in range(getJointCount):
            # 获取骨骼名称
            getJointName = self.reader.getJointName(i)
            # print('getJointName:' + str(getJointName))
            # 获取位移数值
            translate = cmds.xform(getJointName, q=True, t=True)
            # print(translate)
            # 获取旋转数值
            rotate = cmds.xform(getJointName, q=True, ro=True)
            # print(rotate)
            # 获取已有的旋转数值
            getNeutralJointRotation = self.reader.getNeutralJointRotation(i)
            # print('getJointName:' + str(getNeutralJointRotation))
            # 重组位移数值列表
            need_write_translate_list.append(translate)
            # 重计算并组合旋转数值列表
            for j in range(0, len(getNeutralJointRotation)):
                getNeutralJointRotation[j] = getNeutralJointRotation[j] + rotate[j]
            need_write_rotate_list.append(getNeutralJointRotation)

        self.writer.setNeutralJointTranslations(need_write_translate_list)
        self.writer.setNeutralJointRotations(need_write_rotate_list)
        print('所有骨骼位置都已经更新。')

    # 将当前选择模型写入成bs
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
        # 遍历所有顶点
        for i in range(len(vtx)):
            # 获取顶点的世界位置
            pos = cmds.xform(vtx[i],q=True, ws=True, t=True)

            # 将位置添加到列表中
            new_vertex_positions.append(pos)
            # 计算出一个偏移数组
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
        print(mesh_indices, bs_index, '已修改当前指针位置的bs。')

    # 加载当前指针表情驱动，并且返回驱动数据
    def load_edit_drver_date(self, base_face):
        all_date = []
        getJointGroupCount = self.reader.getJointGroupCount()  # 获取骨骼组指数
        # print('骨骼组数量:' + str(getJointGroupCount))
        getRawControlName = self.reader.getRawControlName(base_face)
        print('需要修改的初始表情：' + str(base_face))
        print('基础表情名称:' + str(getRawControlName))
        # 查询所有组中是否有要修改的主表情
        # max = 0
        for j in range(0, getJointGroupCount):  #
            getJointGroupInputIndices = self.reader.getJointGroupInputIndices(j)  # 获取骨骼组所关联的微表情
            # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
            joint_group = []
            base_face_in_joint_group_indices = 0
            for i in range(0, len(getJointGroupInputIndices)):
                if getJointGroupInputIndices[i] == base_face:
                    joint_group = j  # 骨骼组
                    base_face_in_joint_group_indices = i  # 需要修改的基础表情在属性列表所含数据的位置
                    break
            if joint_group:  # 如果骨骼组存在则创建骨骼组和骨骼字典
                group_with_values = []
                getJointGroupOutputIndices = self.reader.getJointGroupOutputIndices(j)  # 获取骨骼组所关联的属性
                # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
                # 按属性数量拆解值到新列表
                joint_value = []
                getJointGroupValues = self.reader.getJointGroupValues(j)  # 获取骨骼组所关联的微表情所含的属性值
                # print('getJointGroupValues:' + str(len(getJointGroupValues)) + str(getJointGroupValues))
                for x in range(0, len(getJointGroupOutputIndices)):
                    ls_list = []
                    for k in range(0, len(getJointGroupInputIndices)):
                        ls_list.append(getJointGroupValues[len(getJointGroupInputIndices) * x + k])
                    joint_value.append(ls_list)
                # print(joint_value)
                # 建立修改列表
                ls_list = [joint_group, joint_value, base_face_in_joint_group_indices]
                group_with_values.append(ls_list)
                all_date.append(group_with_values)
        print('表情数据加载完毕')
        return all_date

    # 写入表情驱动
    def write_edit_drver_date(self, all_date):
        getJointCount = self.reader.getJointCount()  # 获取骨骼指数
        # print('骨骼数量:' + str(getJointCount))
        attr = []
        for j in range(0, getJointCount):
            getJointName = self.reader.getJointName(j)  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
            list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY',
                    'scaleZ']
            for at in list:
                joint_name = getJointName
                ls_list = [j, joint_name, at]
                attr.append(ls_list)
        # print('所有骨骼属性:' + str(len(attr)) + str(attr))
        for n in range(0, len(all_date)):
            group_all_date = all_date[n][0]
            joint_group = group_all_date[0]  # 获取骨骼组名称
            joint_value = group_all_date[1]  # 获取按属性拆分的值
            base_face_in_joint_group_indices = group_all_date[2]  # 获取骨骼组中需要修改的表情再所关联的所有表情的位置
            getJointGroupInputIndices = self.reader.getJointGroupInputIndices(joint_group)  # 获取骨骼组所关联的微表情
            # 获取属性列表以及其关联的属性
            getJointGroupOutputIndices = self.reader.getJointGroupOutputIndices(joint_group)  # 获取骨骼组所关联的属性
            for i in range(0, len(getJointGroupOutputIndices)):  # 骨骼组中所有表情
                for j in range(0, len(attr)):  # 所有骨骼的属性
                    if j == getJointGroupOutputIndices[i]:
                        translate = cmds.xform((attr[j][1]), q=1, t=1)  # 获取当前骨骼位移
                        getNeutralJointTranslation = self.reader.getNeutralJointTranslation(attr[j][0])  # 获取默认状态位移
                        rotate = cmds.getAttr(attr[j][1] + '.rotate')[0]  # 获取旋转值
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
                        num = now_num - base_num  # 重计算驱动数值
                        joint_value[i][base_face_in_joint_group_indices] = num
                        break
            # 开始修改值
            new_values = []
            for i in range(0, len(joint_value)):
                for x in range(0, len(getJointGroupInputIndices)):
                    new_values.append(joint_value[i][x])
            self.writer.setJointGroupValues(joint_group, new_values)  # 修改数据
        print('写入新表情完毕')

    # 镜像骨骼
    def mirror_joint(self):
        pass

    # 删增骨骼的同时自动修改驱动
    def change_joint(self):
        pass

    # 按模型区别重计算骨骼位置
    def recalculate_joint_position(self):
        pass

    # 按模型区别重计算驱动
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
                print('已获取当前选择模型结构数据。')
                # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
                return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group

    # 创建网格
    def creare_mesh(self, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group):
        print(vertex_positions)
        print(vertex_normals)
        print(all_topology)
        print(uv_coords_us)
        print(uv_coords_vs)
        print(all_uv_topology)
        print(smooth_group)
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
                smooth_line.append(name+'.e['+str(i)+']')
            # print('平滑组：',smooth_line)
            # print('平滑组：',smooth_group)
            cmds.polySoftEdge(smooth_line, a=0, ch=0)
        # 冻结当前法线
        cmds.polyNormalPerVertex(name,ufn=1)


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

    # 简单编辑材质
    def edit_material(self, material_name, color, roughness, transparency):
        # 设置颜色
        if color:
            file_node = self.create_2d_texture()
            cmds.setAttr(file_node + '.fileTextureName', color, type="string")
            cmds.connectAttr((file_node + '.outColor'), (material_name + '.color'), force=1)
        # 设置粗糙度
        if roughness:
            file_node = self.create_2d_texture()
            cmds.setAttr(file_node + '.fileTextureName', color, type="string")
            cmds.connectAttr((file_node + '.outAlpha'), (material_name + '.diffuse'), force=1)
        # 设置透明度
        if transparency:
            file_node = self.create_2d_texture()
            cmds.setAttr(file_node + '.fileTextureName', color, type="string")
            cmds.connectAttr((file_node + '.outColor'), (material_name + '.transparency'), force=1)

    # 创建二维贴图
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

    # 导出材质
    def export_material(self, file_path, type):
        materials = cmds.ls(materials=True)
        materials = [x for x in materials if x not in ['lambert1', 'standardSurface1', 'particleCloud1']]
        print('自定义材质:',materials)
        cmds.select(materials)
        # 导出当前选择
        cmds.file(file_path, pr=1, typ=type, es=1, op='v=0;')  # mayaBinary or mayaAscii
        return materials

    # 导入文件
    def import_file(self, file_path, type):
        cmds.file(file_path, pr=1, ignoreVersion=1, i=1, type=type, namespace=':', importTimeRange='combine', ra=True,
                  mergeNamespacesOnClash=True, options="v=0;")

    # 移除多余材质
    def remove_material(self):
        # 不知道为什么，需要运行两次才有效果
        # 清理材质
        materials = cmds.ls(materials=True)
        materials = [x for x in materials if x not in ['lambert1', 'standardSurface1', 'particleCloud1']]
        # print('自定义材质:', materials)
        # 遍历所有材质
        for mat in materials:
            # 获取与该材质关联的所有节点（这通常包括连接到材质的网格）
            connections = cmds.listConnections(mat, source=False, destination=True,type='shadingEngine')
            if not connections:
                cmds.delete(mat)
        # 清理找色组
        shadingEngine = cmds.ls(type='shadingEngine')
        shadingEngine = [x for x in shadingEngine if x not in ['initialParticleSE', 'initialShadingGroup']]
        # 遍历所有找色组
        for se in shadingEngine:
            # 获取与该材质关联的所有节点（这通常包括连接到材质的网格）
            connections = cmds.listConnections(se, destination=True,type='mesh')
            if not connections:
                cmds.delete(se)
        # print('自定义着色组：',shadingEngine)

    # 清理场景
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

        print('清理场景完成')

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

    # 测试的代码
    def test(self, mesh_indices, sel_mesh):
        self.load_read('D:/Personal/zhankangming/Desktop/MH_text_demo/Ada.dna')
        self.load_write('D:/Personal/zhankangming/Desktop/MH_text_demo', 'Archetype')
        # cmds.select('head_lod0_meshShape')
        # sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = self.get_mesh_structure_2()
        # print('asd')
        # mesh = self.creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group)
        # print('生成的模型：',mesh)
        # shader_name = self.assign_material([mesh], 'lambert', [])
        # print('生成的材质/已有材质：',shader_name)
        #
        # # 编辑生成的材质
        # self.edit_material(shader_name,
        #                    'D:/Personal/zhankangming/Desktop/ZIBLT1KU[[Q_)8XU2XUCMWC.jpg',
        #                    'D:/Personal/zhankangming/Desktop/ZIBLT1KU[[Q_)8XU2XUCMWC.jpg',
        #                    'D:/Personal/zhankangming/Desktop/ZIBLT1KU[[Q_)8XU2XUCMWC.jpg')
        #
        # # 场景清理
        # self.clear_scene()
        #
        # # 导出所有自定义材质
        # print(self.export_material('D:/Personal/zhankangming/Desktop/asddsaga123.ma', 'mayaAscii'))
        #
        # # 导入材质
        # self.import_file('D:/Personal/zhankangming/Desktop/asddsaga123.ma', 'mayaAscii')

        # self.load_read_write()
        # self.assign_material('pCubeShape1', 'lambert1')
        # getMeshName = self.reader.getMeshName(mesh_indices)
        # print('getMeshName:' + str(getMeshName))
        # # 获取并返回当前选择模型结构数据
        # shape = cmds.listRelatives(getMeshName, c=1, type='mesh')
        # cmds.select(shape)
        # name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs = self.get_mesh_structure()
        #
        # # 将模型结构数据转换成dna所需的数据
        # mesh_indices, vertex_positions, vertex_normals, all_topology, uv, p_uv_nor_layout = self.data_required_for_conversion_into_dna(mesh_indices, name, vertex_positions, vertex_normals, all_topology,uv_coords_us, uv_coords_vs)
        # # 设置拓扑
        # self.set_topology(mesh_indices, all_topology)
        # # 修改点位置、法线、UV坐标
        # self.set_point_positions(mesh_indices, vertex_positions, vertex_normals, uv, p_uv_nor_layout)
        # # 重置bs
        # self.reset_blendshape(mesh_indices)
        # # 编辑骨骼位置
        # self.edit_joint_tr()
        # # # 重置当前指针骨骼权重
        # # self.reset_joint_weight(mesh_indices)
        # # 编辑骨骼权重
        # self.edit_joint_weight(mesh_indices)
        #
        # # 将当前模型写入成bs
        # for bs_index, sel_index in zip([0],[0]):
        #     self.write_sel_model_to_bs(mesh_indices, bs_index, vertex_positions,sel_mesh[sel_index])
        #
        # # 按表情驱动指针修改驱动
        # for face_drver_index in [191]:
        #     self.write_edit_drver_date(self.load_edit_drver_date(face_drver_index))
        # # 写入
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
        print('写入完毕，请加载dna查看效果。')

# DnaEditLibrary().test(0,['asd'])

# end_time = time.time()
# # 计算并打印耗时
# elapsed_time = end_time - start_time
# print(f"操作耗时: {elapsed_time} 秒")


