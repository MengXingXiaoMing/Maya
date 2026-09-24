#coding=gbk
import maya.api.OpenMaya as om
import maya.cmds as cmds

# 获取并返回当前选择模型结构数据
# 调用函数
# get_depend_nodes_from_selection()
def get_mesh_structure():
    selectList = om.MGlobal.getActiveSelectionList()
    depFn = om.MFnDependencyNode()
    for i in range(selectList.length()):
        node = selectList.getDependNode(i)
        type_syr = node.apiTypeStr
        print("Type: %s" % type_syr)
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
            print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

            # 创建一个列表来存储顶点位置
            vertex_positions = []
            # 遍历所有顶点并获取它们的位置
            for i in range(num_verts):
                point = mesh_fn.getPoint(i)
                vertex_positions.append([point.x, point.y, point.z])
            print('点：',vertex_positions)

            # 获取顶法线数组
            normals = mesh_fn.getVertexNormals(False)
            # 获取顶点法线数值数组
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
            print('法线：',vertex_normals)

            # 获取uv集
            uv_set = mesh_fn.getUVSetNames()

            # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
            uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
            print('U：', uv_coords_us)
            print('V：', uv_coords_vs)
            # 遍历面并建立
            all_topology = []
            for i in range(num_faces):
                # 按面获取拓扑
                topology = cmds.polyListComponentConversion(name+'.f[' + str(i) + ']', tvf=True)
                topology = cmds.ls(topology, fl=1)
                all_uv_num = []
                for j in range(len(topology)):
                    # 按拓扑获取uv
                    uv = cmds.polyListComponentConversion(topology[j], tv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num.append(num)
                all_topology.append(all_uv_num)
            print('拓扑', all_topology)
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
            return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology
cmds.select('pCubeShape1')
sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology = get_mesh_structure()

# 创建网格
def creare_mesh(name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology):
    # 立方体的顶点位置
    vertices = vertex_positions

    # 转换为OM类型
    vertex_positions = []
    for vertex in vertices:
        vertex_positions.append(om.MPoint(vertex[0], vertex[1], vertex[2]))


    # 将面定义转换为MIntArray
    face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
    for f in all_topology:
        face_counts.append(len(f))

    # face_vertex_counts = om.MIntArray()  # 所有面的顶点总数
    # for face in faces:
    #     face_vertex_counts.append(len(face))

    face_connects = []
    for face in all_topology:
        for index in face:
            face_connects.append(index)

    print(vertex_positions)
    print(face_counts)
    print(face_connects)
    # 创建网
    mesh_fn = om.MFnMesh()
    # 定义每个面的顶点索引（多边形连接）
    # 注意：Maya中的多边形是顺时针或逆时针定义的，取决于法线的方向
    mesh_obj = mesh_fn.create(vertex_positions, face_counts, face_connects, uv_coords_us, uv_coords_vs)

    print(all_uv_topology)
    uv_face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
    for f in all_uv_topology:
        uv_face_counts.append(len(f))
    uvIds = [item for sublist in all_uv_topology for item in sublist]
    print(len(uvIds),uvIds)

    mesh_uv = mesh_fn.assignUVs(uv_face_counts, uvIds)

    # # 使用cmds创建一个默认材质
    # shader_name = cmds.shadingNode('blinn', asShader=True, name='my_default_material')

    # 尝试获取模型的着色组
    # shading_groups = cmds.listConnections(name + '.instObjGroups', shapes=True) or []
    # 将材质连接到着色组的surfaceShader属性
    # if not cmds.isConnected('lambert1.outColor', shading_group + '.surfaceShader'):
    #     cmds.connectAttr('lambert1.outColor', shading_group + '.surfaceShader', force=True)
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

creare_mesh(sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology)


import maya.api.OpenMaya as om
line = cmds.ls(('pConeShape1.e[*]'), fl=True)
# 获取球体的 MObject
for i in range(len(line)):
    selection_list = om.MSelectionList()
    selection_list.add(line[i])
    dag_path = selection_list.getDagPath(0)
    line_3 = om.MItMeshEdge(dag_path)
    print(line_3.isSmooth)

import maya.api.OpenMaya as om
selection_list = om.MSelectionList()
selection_list.add('pCone1')
dag_path = selection_list.getDagPath(0)
line_3 = om.MItMeshEdge(dag_path)
while not line_3.isDone():
    print(line_3.index())
    line_3.next()
    print(line_3.isSmooth)

# 获取网格函数集
mesh_fn = om.MFnMesh(dag_path.node())
# 遍历所有边
num_edges = mesh_fn.numEdges()
for i in range(num_edges):
    # 这里我们其实不能直接获取边的 MDagPath，但我们可以获取边的索引
    # 如果你需要处理每条边，可以直接在这里操作
    edge_index = i




print(line)
dag_path = line.getDagPath(0)


class File:
    def read(self):
        print("Reading from base File class")


class SpecialFile(File):
    def read(self):
        # 首先调用父类的 read 方法
        super().read()
        # 然后执行一些额外的操作
        print("Reading additional content from SpecialFile")

    # 创建一个 SpecialFile 的实例


sf = SpecialFile()
# 调用其 read 方法
sf.read()





cunt = int(-1.001 / -0.01)
print(cunt)

num = 3.14959
truncated_num = (num * 100) // 1  # 乘以100，取整（//是整除运算符）
truncated_num /= 100  # 再除以100

print(truncated_num)  # 输出: 3.14
########################################################################################
cmds.undoInfo(ock=1)
sel = cmds.ls(sl=1)
for s in sel:
    mesh_shape = cmds.listRelatives(s, s=1)
    point = cmds.ls((mesh_shape[0] + '.vtx[*]'), fl=1)
    skin_cluster = cmds.listConnections((mesh_shape[0] + '.inMesh'), d=1)
    SkinJoint = cmds.skinCluster(s, q=1, inf=1)
    for joint in SkinJoint:
        cmds.setAttr((joint + '.liw'), 0)
    # 按骨骼归一化
    for p in point:
        all_skin = []
        edit_num = 0.0
        for i in range(0, (len(SkinJoint))):
            weights = cmds.skinPercent(skin_cluster[0], p, query=True, value=True)
            if weights != 0:
                weights_num = round(weights[i], 2)  # 取小数点后一位
                add_num = weights[i] - weights_num
                edit_num = edit_num + add_num

                unit = 0.01
                if edit_num < 0:
                    unit = -0.01
                cunt = int(edit_num / unit)
                if cunt > 0:
                    weights_num = weights_num + unit
                    edit_num = edit_num - unit
                all_skin.append((SkinJoint[i], weights_num))
        num = 1
        for j in range(0, (len(all_skin))):
            num = num - all_skin[j][1]
        all_skin[-1] = (all_skin[-1][0], all_skin[-1][1] + num)
        cmds.skinPercent(skin_cluster[0], p, tv=all_skin)
    cmds.skinCluster(skin_cluster[0], forceNormalizeWeights=1, e=1)
cmds.warning('骨骼权重清理为小数点后一位清理完成。')
cmds.undoInfo(cck=1)



def list_deformer_hierarchy(node):
    # 获取节点的变形历史，只包括变形器节点
    history = cmds.listHistory(node, gl=1,pdo=1)
    if not history:
        return []
    return history
# 使用示例
node_name = "pCube1"  # 替换为你的目标节点名称
deformer_hierarchy = list_deformer_hierarchy(node_name)
print("变形器层级:")
for deformer in deformer_hierarchy:
    print(deformer)






import maya.mel as mel

cmds.select('joint1')
cmds.SelectHierarchy()
sel_0 = cmds.ls(sl=1)
cmds.select('joint1')
cmds.duplicate(rr=1)
cmds.SelectHierarchy()
sel_2 = cmds.ls(sl=1)
cmds.select('joint1')
cmds.SelectHierarchy()
sel_1 = cmds.ls(sl=1)
for i in range(len(sel_1)):
    cmds.select(sel_2[len(sel_1)-1-i])
    mel.eval('rename '+sel_0[len(sel_0)-1-i]+'_copy;')

import time
# 定义一个函数，其运行时间将被测量
def some_function_to_measure():
    # 这里可以是你想要测量的任何代码
    # 例如，一个循环，一些计算，或者其他操作
    # j = []
    # for i in range(100):
    #     n = n = cmds.group(em=1)
    #     if j:
    #         cmds.parent(n, j)
    #     j = n
    cmds.playblast(fp=4, clearCache=1, showOrnaments=1, sequenceTime=0, format='avi', percent=50, viewer=1, quality=70,
                 compression="none")

# 记录开始时间
start_time = time.time()

# 调用要测量的函数
some_function_to_measure()

# 记录结束时间
end_time = time.time()

# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time:.6f} seconds to complete.")


import time
# 定义一个函数，其运行时间将被测量
def some_function_to_measure():
    # 这里可以是你想要测量的任何代码
    # 例如，一个循环，一些计算，或者其他操作
    j = []
    for i in range(10000):
        n = cmds.group(em=1)
        if j:
            cmds.parent(n, j)
        j = n


# 记录开始时间
start_time = time.time()

# 调用要测量的函数
some_function_to_measure()

# 记录结束时间
end_time = time.time()

# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time:.6f} seconds to complete.")

import time
# 定义一个函数，其运行时间将被测量
def some_function_to_measure():
    # 这里可以是你想要测量的任何代码
    # 例如，一个循环，一些计算，或者其他操作
    cmds.duplicate(rr=1)

# 记录开始时间
start_time = time.time()

# 调用要测量的函数
some_function_to_measure()

# 记录结束时间
end_time = time.time()

# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time:.6f} seconds to complete.")



from time import perf_counter
from  maya import cmds
from  maya.api import OpenMaya as om

st = perf_counter()
dag_mod = om.MDagModifier()
a = om.MObject.kNullObj
for _ in range(1000):
    a = dag_mod.createNode('transform', a)
dag_mod.doIt()
print(perf_counter()-st)









from maya.api import OpenMaya as om
dag_mod = om.MDagModifier()
parent_node = om.MObject.kNullObj
new_node = dag_mod.createNode('transform', parent_node)





















#
print('创建履带')
# 获取要删除的节点
need_delete = []

# 加载轮子长度
# self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit'])
cmds.select('nurbsCircle1')
track_perimeter = cmds.ls(sl=1)
# 加载输出骨骼
# self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit'])
cmds.select('joint4')
track_joint = cmds.ls(sl=1)
cmds.SelectHierarchy()
joint = cmds.ls(sl=1)
# 加载总控制器
# self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
cmds.select('joint1_C')
track_parent_controller = cmds.ls(sl=1)
# 加载轮子控制器
# self.maya_common.select_text_target(self.line_edit_4, ['QLineEdit'])
cmds.select('joint2_C')
track_controller = cmds.ls(sl=1)

grp = cmds.group(em=1, n='All_track_Grp')

# 给总样条添加属性
cmds.addAttr(track_parent_controller, ln='track', at='bool')
# cmds.setAttr((track_parent_controller[0]+'.track'), e=1, channelBox=True, lock=True)
cmds.addAttr(track_parent_controller, ln='baking_tracks', at='bool')
cmds.setAttr((track_parent_controller[0] + '.baking_tracks'), e=1, channelBox=True)
cmds.addAttr(track_parent_controller, ln='start_frame', dv=101, at='long')
cmds.setAttr((track_parent_controller[0] + '.start_frame'), e=1, channelBox=True)
cmds.addAttr(track_parent_controller, ln='expression_type', en="tradition:baking:", at="enum")
cmds.setAttr((track_parent_controller[0] + '.expression_type'), e=1, channelBox=True)

########################################################################################################################
# for i in range(0, len(track_controller)):
i = 0
# 创建烘焙骨骼
baking_bones = cmds.joint(p=(0, 0, 0), n=(track_controller[i] + '_baking_joint'))
cmds.parent(baking_bones, track_controller[i])
cmds.setAttr(baking_bones + '.jointOrientX', 0)
cmds.setAttr(baking_bones + '.jointOrientY', 0)
cmds.setAttr(baking_bones + '.jointOrientZ', 0)
cmds.delete(cmds.parentConstraint(track_controller[i], baking_bones, w=1))
# 创建
prePosA = cmds.spaceLocator(p=(0, 0, 0), n=(track_controller[i] + '_car_bl_prePosLocA'))
nowPos = cmds.spaceLocator(p=(0, 0, 0), n=(track_controller[i] + '_car_bl_nowPosLoc'))
prePos = cmds.spaceLocator(p=(0, 0, 0), n=(track_controller[i] + '_car_bl_prePosLoc'))
move_grp = cmds.group(n=(track_controller[i] + '_track'))
cmds.setAttr(track_controller[i] + '_car_bl_prePosLoc.visibility', 0)
cmds.select(nowPos, prePosA)
Group1 = cmds.group(n=(track_controller[i] + '_car_bl_locGrp'))
cmds.setAttr(track_controller[i] + '_car_bl_locGrp.visibility', 0)

cmds.addAttr((track_controller[i]), ln='prePosX', dv=0, at='double')
# cmds.setAttr((track_controller[i]+'.prePosX'), e=1, keyable=True)
cmds.addAttr((track_controller[i]), ln='prePosY', dv=0, at='double')
# cmds.setAttr((track_controller[i]+'.prePosY'), e=1, keyable=True)
cmds.addAttr((track_controller[i]), ln='prePosZ', dv=0, at='double')
# cmds.setAttr((track_controller[i]+'.prePosZ'), e=1, keyable=True)

cmds.addAttr((track_controller[i]), ln='direction_num', dv=0, at='double')
# cmds.setAttr((track_controller[i]+'.direction_num'), e=1, keyable=True)

cmds.select(Group1, move_grp)
top_grp = cmds.group(n=(track_controller[i] + 'track_Grp'))
cmds.parent(top_grp, grp)

cmds.pointConstraint(prePosA, prePos, weight=1)
cmds.pointConstraint(move_grp, nowPos, weight=1)
cmds.delete(cmds.pointConstraint(track_controller[i], top_grp, weight=1))
curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
need_delete.append(curveInfo)
cmds.connectAttr((track_perimeter[i] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), f=1)

# 给样条添加属性
cmds.addAttr(track_controller[i], ln='running_direction', en='x:y:z:', at='enum')
cmds.setAttr((track_controller[i] + '.running_direction'), e=1, channelBox=True)
cmds.setAttr((track_controller[i] + '.running_direction'), 2)
cmds.addAttr(track_controller[i], ln='axial', en='x:y:z:', at='enum')
cmds.setAttr((track_controller[i] + '.axial'), e=1, channelBox=True)
cmds.addAttr(track_controller[i], ln='start_num', dv=0, at='double')
cmds.setAttr((track_controller[i] + '.start_num'), e=1, keyable=True)
cmds.addAttr(track_controller[i], ln='baking_num', dv=0, at='double')
cmds.setAttr((track_controller[i] + '.baking_num'), e=1, keyable=True)
cmds.addAttr(track_controller[i], ln='magnification', dv=1, at='double')
cmds.setAttr((track_controller[i] + '.magnification'), e=1, keyable=True)
# 给骨骼添加属性
cmds.addAttr(baking_bones, ln='track', at='bool')
# cmds.setAttr((baking_bones + '.track'), e=1, channelBox=True)
cmds.addAttr(baking_bones, ln='calculate_track_num', dv=0, at='double')
cmds.setAttr((baking_bones + '.calculate_track_num'), e=1, keyable=True)
# 添加骨骼属性代理(代码里给此属性k帧)
cmds.addAttr(baking_bones, proxy=(track_controller[i] + '.baking_num'), longName='baking_track')
# 添加总控制器属性代理
cmds.addAttr(track_parent_controller, proxy=(track_controller[i] + '.baking_num'), longName=baking_bones)
# 建立节点关系
cmds.connectAttr((track_parent_controller[0] + '.track'), (baking_bones + '.track'), f=1)
# choice_node = cmds.shadingNode('choice', asUtility=1)
# need_delete.append(choice_node)
# cmds.connectAttr((track_parent_controller[0] + '.expression_type'), (choice_node + '.selector'), f=1)
# cmds.connectAttr((baking_bones + '.calculate_track_num'), (choice_node + '.input[0]'), f=1)
# cmds.connectAttr((track_controller[i] + '.baking_num'), (choice_node + '.input[1]'), f=1)
# for j, axial in zip(range(0, 3), ['X', 'Y', 'Z']):
#     plusMinusAverage_condition = cmds.shadingNode('condition', asUtility=1)
#     need_delete.append(plusMinusAverage_condition)
#     cmds.connectAttr((track_controller[i] + '.axial'), (plusMinusAverage_condition + '.firstTerm'), f=1)
#     cmds.setAttr((plusMinusAverage_condition + '.secondTerm'), j)
#     cmds.setAttr((plusMinusAverage_condition + '.colorIfFalseR'), 0)
#     cmds.connectAttr((choice_node + '.output'), (plusMinusAverage_condition + '.colorIfTrueR'), f=1)
#     cmds.connectAttr((plusMinusAverage_condition + '.outColorR'), (baking_bones + '.rotate' + axial), f=1)
# choice_node = cmds.shadingNode('choice', asUtility=1)
# need_delete.append(choice_node)
# cmds.connectAttr((track_controller[i] + '.running_direction'), (choice_node + '.selector'), f=1)
# cmds.connectAttr((track_controller[i] + '_car_bl_prePosLoc.translateX'), (choice_node + '.input[0]'), f=1)
# cmds.connectAttr((track_controller[i] + '_car_bl_prePosLoc.translateY'), (choice_node + '.input[1]'), f=1)
# cmds.connectAttr((track_controller[i] + '_car_bl_prePosLoc.translateZ'), (choice_node + '.input[2]'), f=1)
# cmds.connectAttr((choice_node + '.output'), (track_controller[i] + '.direction_num'))

cmds.expression(s=('if('+track_parent_controller[0]+'.baking_tracks=='+track_parent_controller[0]+'.expression_type){\n'
                    '   int $start=1;\n'
                    '   int $start_frame='+track_parent_controller[0]+'.start_frame;\n'
                    '   if(frame <= $start_frame)$start=0;\n'
                    '   float $start_num = '+track_controller[i]+'.start_num;\n'
                    '   if(frame > $start_frame)$start_num=0;\n'
                    '   float $autoRoll=' + track_controller[i] + '.magnification;\n'
                    '   float $prePosX=' + track_controller[i] + '.prePosX;\n'
                    '   float $prePosY=' + track_controller[i] + '.prePosY;\n'
                    '   float $prePosZ=' + track_controller[i] + '.prePosZ;\n'
                    '   float $nowPosX=' + track_controller[i] + '_car_bl_nowPosLoc.translateX;\n'
                    '   float $nowPosY=' + track_controller[i] + '_car_bl_nowPosLoc.translateY;\n'
                    '   float $nowPosZ=' + track_controller[i] + '_car_bl_nowPosLoc.translateZ;\n'
                    '   float $dis=`mag(<<$nowPosX,$nowPosY,$nowPosZ>>-<<$prePosX,$prePosY,$prePosZ>>)`;\n'
                    '   ' + track_controller[i] + '_car_bl_prePosLocA.translateX=$prePosX;\n'
                    '   ' + track_controller[i] + '_car_bl_prePosLocA.translateY=$prePosY;\n'
                    '   ' + track_controller[i] + '_car_bl_prePosLocA.translateZ=$prePosZ;\n'
                    '   ' + track_controller[i] + '.prePosX=$nowPosX;\n'
                    '   ' + track_controller[i]+ '.prePosY=$nowPosY;\n'
                    '   ' + track_controller[i] + '.prePosZ=$nowPosZ;\n'
                    '   float $dirPreZ=' + track_controller[i]+'.direction_num;\n'
                    '   int $dir=1;\n'
                    '   if($dirPreZ<0)$dir=-1;\n'
                    '   float $perimeter=' + curveInfo + '.arcLength;\n'
                    '   float $curRoll=' + baking_bones + '.calculate_track_num;\n'
                    '   ' + baking_bones + '.calculate_track_num=($start_num+$start*($curRoll+$dis/$perimeter*$autoRoll*$dir))%1;\n'
                    '}'),
                    ae=1, uc='all', o='', n=(track_perimeter[i]+'_trackExpression'))

cmds.delete(cmds.pointConstraint(track_controller[i], move_grp, w=1))
cmds.parentConstraint(track_controller[i], move_grp, w=1, mo=1)

# rotateX = cmds.listConnections((track_joint[i] + '.rotateX'), p=1)
# if rotateX:
#     cmds.disconnectAttr(rotateX[0], (track_joint[i] + '.rotateX'))
# rotateY = cmds.listConnections((track_joint[i] + '.rotateY'), p=1)
# if rotateY:
#     cmds.disconnectAttr(rotateY[0], (track_joint[i] + '.rotateY'))
# rotateZ = cmds.listConnections((track_joint[i] + '.rotateZ'), p=1)
# if rotateZ:
#     cmds.disconnectAttr(rotateZ[0], (track_joint[i] + '.rotateZ'))

# cmds.orientConstraint(baking_bones, track_joint[i], mo=1, weight=1)

# cmds.parent(track_perimeter[i], grp)
# cmds.setAttr((track_perimeter[i] + '.visibility'), 0)
# cmds.parentConstraint(track_controller[i], track_perimeter[i], w=1)
# cmds.scaleConstraint(track_controller[i], track_perimeter[i], w=1)

# 创建定位器拖动骨骼链
motion_loc = cmds.spaceLocator(n=track_controller[i] + '_motion_loc')[0]
cmds.parent(motion_loc, grp)
motionPath = 'motionPath3'


choice = cmds.createNode('choice')
cmds.connectAttr(track_parent_controller[0]+'.expression_type', choice+'.selector', f=1)

cmds.setDrivenKeyframe(choice+'.input[0]',
                       currentDriver=baking_bones+'.calculate_track_num', dv=0, v=0)
cmds.setDrivenKeyframe(choice+'.input[0]',
                       currentDriver=baking_bones+'.calculate_track_num', dv=1, v=1)
motionPath_drver_node = cmds.listConnections((motionPath + '.uValue'))
cmds.keyTangent(motionPath_drver_node,itt='linear', ott='linear')
cmds.select(motionPath_drver_node)
cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
mel.eval('doSetInfinity \"-pri cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
cmds.select(motionPath_drver_node)
cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
mel.eval('doSetInfinity \"-poi cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
cmds.connectAttr(baking_bones+'.calculate_track_num', choice+'.input[0]', force=1)


cmds.setDrivenKeyframe(choice+'.input[1]',
                       currentDriver=(baking_bones+'.baking_track'), dv=0, v=0)
cmds.setDrivenKeyframe(choice+'.input[1]',
                       currentDriver=(baking_bones+'.baking_track'), dv=1, v=1)
motionPath_drver_node = cmds.listConnections((motionPath + '.uValue'))
cmds.keyTangent(motionPath_drver_node,itt='linear', ott='linear')
cmds.select(motionPath_drver_node)
cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
mel.eval('doSetInfinity \"-pri cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
cmds.select(motionPath_drver_node)
cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
mel.eval('doSetInfinity \"-poi cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
cmds.connectAttr(baking_bones+'.baking_track', choice+'.input[1]', f=1)



cmds.setDrivenKeyframe((motionPath + '.uValue'),
                       currentDriver=(choice + '.output'), dv=0, v=0)
cmds.setDrivenKeyframe((motionPath + '.uValue'),
                       currentDriver=(choice + '.output'), dv=1, v=1)
motionPath_drver_node = cmds.listConnections((motionPath + '.uValue'))
cmds.keyTangent(motionPath_drver_node,itt='linear', ott='linear')
cmds.select(motionPath_drver_node)
cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
mel.eval('doSetInfinity \"-pri cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
cmds.select(motionPath_drver_node)
cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
mel.eval('doSetInfinity \"-poi cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')


cmds.select(track_joint[0], joint[-1], track_perimeter[i])
cmds.ikHandle(ccv=False, sol='ikSplineSolver', roc=False, pcv=False)
IK = cmds.ls(sl=1)

cmds.pointConstraint(motion_loc, track_joint[0], w=1)
track_joint_grp = cmds.group(track_joint[0],n=track_controller[i] + '_track_joint_grp',)

cmds.parent(IK, track_joint_grp, top_grp)
cmds.parentConstraint(track_controller[i],track_joint_grp,w=1,mo=1)


cmds.setAttr((track_controller[i] + '.magnification'), cb=True, k=False)

# 添加表达式
cmds.expression(s='if(' + track_parent_controller[0] + '.baking_tracks==1 && ' + track_parent_controller[
    0] + '.expression_type==1){\n'
         '    int $start=1;\n'
         '    string $car[]=`ls "*.baking_tracks"`;\n'
         '    int $end_frame = `playbackOptions -q -max`;\n'
         '    int $now_frame = `currentTime -q`;\n'
         '    for($i=0;$i<size($car);$i++){\n'
         '        int $open=`getAttr $car[$i]`;\n'
         '        if($open==1){\n'
         '            string $soure[];\n'
         '            int $numTok=`tokenize $car[$i] "." $soure`;\n'
         '            float $start_frame=`getAttr ($soure[0]+".start_frame")`;\n'
         '            if(frame>=$start_frame){\n'
         '                string $track[]=`ls ($soure[0]+".track")`;\n'
         '                string $tracks[]=`listConnections -d 1 $track[0]`;\n'
         '                for($j=0;$j<size($tracks);$j++){\n'
         '                    float $track_num=`getAttr ($tracks[$j]+".calculate_track_num")`;\n'
         '                    setKeyframe ($tracks[$j]+".baking_track");\n'
         '                    setAttr ($tracks[$j]+".baking_track") $track_num;\n'
         '                    setKeyframe ($tracks[$j]+".baking_track");\n'
         '                }\n'
         '            }\n'
         '        }\n'
         '    }\n'
         '    if($end_frame==$now_frame){\n'
         '        for($i=0;$i<size($car);$i++){\n'
         '            setAttr $car[$i] 0;\n'
         '        }\n'
         '    }\n'
         '}\n',
                ae=1, uc='all', o='', n=('BakingtrackExpression'))
cmds.select(track_parent_controller[0])
cmds.addAttr(track_parent_controller[0], ln='node', dt='string')
cmds.setAttr(track_parent_controller[0] + '.node', str(need_delete), type='string')

# 添加拉伸
cmds.select(track_perimeter[i])
cmds.duplicate(rr=1)
base_long_curve = cmds.ls(sl=1)

curveInfo_bsee_long = cmds.shadingNode('curveInfo', asUtility=1)
need_delete.append(curveInfo_bsee_long)
cmds.connectAttr((base_long_curve[0] + '.worldSpace[0]'), (curveInfo_bsee_long + '.inputCurve'), f=1)
# 计算拉伸
multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1.input1X'), f=1)
cmds.connectAttr((curveInfo_bsee_long + '.arcLength'), (multiplyDivide + '.input2.input2X'), f=1)
cmds.setAttr((multiplyDivide + '.operation'), 2)
for j in joint:
    cmds.connectAttr((multiplyDivide + '.outputX'), (j + '.scaleX'), f=1)
cmds.parent(base_long_curve[0], top_grp)
cmds.parentConstraint(track_parent_controller[0], base_long_curve[0], mo=1)
cmds.scaleConstraint(track_controller[0], base_long_curve[0], mo=1)






# 初始位置
target = 'nurbsCircle2'
node = 'nurbsCircle2_pointConstraint1'
start_offset = (0,0,0)
now_offset = cmds.getAttr(node+'.offset')[0]
print(now_offset)
old_tx = cmds.getAttr(target+'.t')[0]
print(old_tx)

# 移动控制器
now_tx = cmds.getAttr(target+'.t')[0]
print(now_tx)


curve = ['nurbsCircle3_parentConstraint1']




# 先提取所有的额外约束
curve = ['nurbsCircle1','nurbsCircle2','nurbsCircle3']
all_connect_node = []
for c in curve:
    for attribute in ['t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz', 'v']:
        node = cmds.listConnections(c + '.' + attribute)
        if node:
            all_connect_node.append(node[0])
seen = set()
all_connect_node = [x for x in all_connect_node if not (x in seen or seen.add(x))]
print(all_connect_node)
Constraint = []
for node in all_connect_node:
    if cmds.objectType(node) == 'parentConstraint':
        cmds.setAttr(node + '.nodeState', 2)
        constraint_target = cmds.listConnections(node,s=0)
        seen = set()
        constraint_target = [x for x in constraint_target if not (x in seen or seen.add(x))]
        constraint_target.remove(node)
        if constraint_target:
            for attribute in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
                have_connect = cmds.listConnections(constraint_target[0] + '.' + attribute, c=1, p=1)
                if have_connect:
                    Constraint.append(have_connect)
                    cmds.disconnectAttr(have_connect[1], have_connect[0])
print(Constraint)

for node in Constraint:
    cmds.connectAttr(node[1], node[0], f=1)
for node in all_connect_node:
    if cmds.objectType(node) == 'parentConstraint':
        soure = cmds.parentConstraint(node,q=1,tl=1)
        cmds.parentConstraint(soure, node, maintainOffset=1, e=1)
    # if cmds.objectType(node) == 'pointConstraint':
    #     cmds.setAttr(node + '.nodeState', 0)
    # if cmds.objectType(node) == 'aimConstraint':
    #     cmds.setAttr(node + '.nodeState', 0)
    # if cmds.objectType(node) == 'orientConstraint':
    #     cmds.setAttr(node + '.nodeState', 0)
for node in all_connect_node:
    cmds.setAttr(node + '.nodeState', 0)

constraint_target = cmds.listConnections('joint3')
seen = set()
constraint_target = [x for x in constraint_target if not (x in seen or seen.add(x))]
print(constraint_target)


cmds.copyDeformerWeights(ss='pCube1', sa="closestPoint", dd='blendShape1', ds='pPlane2', sd='blendShape2') #sa="closestPoint",
cmds.copyDeformerWeights(ss='pCube2', sd='cluster5', nm=1, ds='pCube1', dd='cluster6')
cmds.copyDeformerWeights(ss='pCube1', ds='pCube1', sd='blendShape1', mirrorMode='YZ', mirrorInverse = True)
# 获取当前选择的对象列表
selection = cmds.ls(selection=True, flatten=True)
# 假设我们只处理一个对象（可以扩展为处理多个对象）
obj = selection[0]
# 获取对象的历史节点
history = cmds.listHistory(obj)
print(history)



# 获取当前选择的模型
selected_objects = cmds.ls(selection=True, dag=True, shapes=True)

if not selected_objects:
    cmds.warning("请选择一个模型。")
else:
    # 遍历选择的模型
    obj=selected_objects[0]
    print(obj)
    # 获取与模型相关的变形器节点
    deformers = cmds.listHistory(obj, pruneDagObjects=True, interestLevel=True)
    deformers = cmds.ls(deformers, type='geometryFilter')  # 过滤出变形器节点

    if deformers:
        print(f"模型 '{obj}' 包含的变形器节点:")
        for deformer in deformers:
            print(f" - {deformer}")
    else:
        print(f"模型 '{obj}' 不包含变形器节点。")




# 定义回调函数
def aaa():
    print('aaaaa')
    # window.creat_select_deform_list()

# 检查窗口是否存在
if not cmds.window('ZKM_deform_edit_window', exists=True):
    print("窗口 'ZKM_deform_edit_window' 不存在！")
else:
    # 注册脚本作业
    jobNum = cmds.scriptJob(
        e=["SelectionChanged", aaa],  # 直接传递函数对象
        protected=True,  # 防止脚本作业被删除
        parent='ZKM_deform_edit_window'  # 绑定到指定窗口
    )

    # 检查脚本作业是否注册成功
    if jobNum:
        print(f"脚本作业注册成功，ID: {jobNum}")
    else:
        print("脚本作业注册失败！")


def model_history_changed():
    print("Model history has changed!")

script_job_id = cmds.scriptJob(event=["DGEvaluate", model_history_changed])

import maya.OpenMaya as OpenMaya
# 定义回调函数
def on_command_executed(client_data):
    print("命令被触发")
callback_id = OpenMaya.MEventMessage.addEventCallback("CommandExecuted", on_command_executed)

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import Qt

# 创建 QTreeWidget
tree_widget = QTreeWidget()
tree_widget.setHeaderLabels(["名称"])

# 添加项目
item = QTreeWidgetItem(tree_widget)
item.setText(0, "项目 1")

# 启用编辑功能
item.setFlags(item.flags() | Qt.ItemIsEditable)




from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 第一行
        v_Box_layout_1 = QVBoxLayout(self)
        main_layout.addLayout(v_Box_layout_1)
        v_Box_layout_1.setSpacing(1)

        grid_layout_2 = QGridLayout(self)
        v_Box_layout_1.addLayout(grid_layout_2)

        # 设置第二行的拉伸因子为 1，使其最大化
        grid_layout_2.setRowStretch(0, 0)  # 第一行不拉伸
        grid_layout_2.setRowStretch(1, 1)  # 第二行拉伸
        grid_layout_2.setRowStretch(2, 0)  # 第三行不拉伸

        # 添加一些示例控件
        label_1 = QLabel("Label 1")
        label_2 = QLabel("Label 2")
        label_3 = QLabel("Label 3")
        label_4 = QLabel("Label 4")
        label_5 = QLabel("Label 5")

        # 将控件添加到网格布局中
        grid_layout_2.addWidget(label_1, 0, 0)
        grid_layout_2.addWidget(label_2, 0, 1)
        grid_layout_2.addWidget(label_3, 1, 0)
        grid_layout_2.addWidget(label_4, 1, 1)
        grid_layout_2.addWidget(label_5, 2, 0)

        # 设置控件的大小策略
        label_1.setSizePolicy(QLabel.Expanding, QLabel.Expanding)
        label_2.setSizePolicy(QLabel.Expanding, QLabel.Expanding)
        label_3.setSizePolicy(QLabel.Expanding, QLabel.Expanding)
        label_4.setSizePolicy(QLabel.Expanding, QLabel.Expanding)
        label_5.setSizePolicy(QLabel.Expanding, QLabel.Expanding)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


print(cmds.blendShape('blendShape1',e=1,md=0,mt=[0,0],sa='X'))

cmds.blendShape(
    'blendShape1',
    edit=True,
    # mirror=1,                      # 开启镜像模式
    mirrorDirection=1,             # 镜像方向（0=X, 1=Y, 2=Z）
    symmetryAxis='X',              # 对称轴
    # sourceAttribute='X',           # 源属性轴
    # topologyCheck=0                # 关闭拓扑检查（慎用）
)

import maya.cmds as cmds

# 镜像混合变形权重
cmds.mirrorBlendShapeWeights(
    'blendShape1',  # 混合变形节点名称
    mirrorAxis="X", # 镜像轴（X/Y/Z）
    sourceSide="L", # 源侧标记（如顶点名包含 "L"）
    destinationSide="R", # 目标侧标记
    topToBottom=0,  # 是否镜像上下方向（0 为关闭）
    leftToRight=1   # 开启左右镜像
)

cmds.copyBlendShapeWeights(
    sourceShape='blendShape1',  # 源混合变形节点
    destinationShape='blendShape1',  # 目标混合变形节点
    sourceTarget='L_target',  # 源目标名称
    destinationTarget='R_target'  # 目标名称
)


import maya.cmds as cmds

# 镜像混合变形权重
cmds.mirrorBlendShapeWeights(
    'blendShape1',  # 混合变形节点名称
    mirrorAxis="X", # 镜像轴（X/Y/Z）
    sourceSide="L", # 源侧标记（如顶点名包含 "L"）
    destinationSide="R", # 目标侧标记
    topToBottom=0,  # 是否镜像上下方向（0 为关闭）
    leftToRight=1   # 开启左右镜像
)


cmds.copyBlendShapeWeights(
    sourceShape='blendShape1',  # 源混合变形节点
    destinationShape='blendShape1',  # 目标混合变形节点
    sourceTarget='L_smile',  # 源目标名称
    destinationTarget='R_smile'  # 目标名称
)

cmds.setAttr("blendShape1.pCube2.inputTargetGroup[0].targetWeights[0]", 0)



import maya.cmds as cmds

def mirror_blend_shape_weights(blend_shape_node, base_index, target_index, mirror_axis='X'):
    """
    镜像混合变形权重
    :param blend_shape_node: 混合变形节点名称（如 'blendShape1'）
    :param base_index: 基础形状的索引
    :param target_index: 目标形状的索引
    :param mirror_axis: 镜像轴（'X', 'Y', 'Z'）
    """
    # 设置镜像轴
    cmds.blendShape(blend_shape_node, edit=True, symmetryAxis=mirror_axis)

    # 镜像目标形状
    cmds.blendShape(
        blend_shape_node,
        edit=True,
        mirrorTarget=[(base_index, target_index)]  # 镜像基础形状和目标形状
    )

    print(f"镜像完成：基础形状索引 {base_index}，目标形状索引 {target_index}，镜像轴 {mirror_axis}")

# 示例调用
blend_shape_node = 'blendShape1'  # 混合变形节点名称
base_index = 0  # 基础形状索引
target_index = 1  # 目标形状索引
mirror_axis = 'X'  # 镜像轴

mirror_blend_shape_weights(blend_shape_node, base_index, target_index, mirror_axis)

print(cmds.aliasAttr('blendShape1.w[2]',q=1))
target_count = cmds.blendShape('blendShape1', query=True, weightCount=True)
print(target_count)

import maya.cmds as cmds

def mirror_all_blend_shape_weights(blend_shape_node, mirror_axis='X'):
    """
    镜像混合变形节点中的所有目标形状
    :param blend_shape_node: 混合变形节点名称
    :param mirror_axis: 镜像轴（'X', 'Y', 'Z'）
    """
    # 获取混合变形节点的目标形状数量
    target_count = cmds.blendShape(blend_shape_node, query=True, weightCount=True)

    # 遍历所有目标形状并镜像
    for target_index in range(target_count):
        cmds.blendShape(
            blend_shape_node,
            edit=True,
            mirrorTarget=[(0, target_index)]  # 镜像基础形状和目标形状
        )

    # 设置镜像轴
    cmds.blendShape(blend_shape_node, edit=True, symmetryAxis=mirror_axis)

    print(f"镜像完成：共镜像 {target_count} 个目标形状，镜像轴 {mirror_axis}")

# 示例调用
blend_shape_node = 'blendShape1'  # 混合变形节点名称
mirror_axis = 'X'  # 镜像轴

mirror_all_blend_shape_weights(blend_shape_node, mirror_axis)


def new_maya_base_copy_joint_weight(copy_way, soure, target, soure_skin, target_skin, soure_uv_set,target_uv_set):
    # str copy_way 有Normal和UV两种方式
    # list soure
    # list target
    # str soure_uv_set
    # str target_uv_set
    if copy_way and soure and target and soure_skin:
        print('asdasd')
        # 获取源骨骼影响
        source_skin_joint = cmds.skinCluster(soure_skin, q=1, inf=1)

        # 判断目标选的是模型还是点
        for tar in target:
            pass
        if len(target[0].split('.')) == 1:
            target_type = 'Model'
        else:
            target_type = 'Point'
        # 先进行添加影响和蒙皮
        if target_type == 'Model':
            for i in range(len(target)):
                target_skin_cluster = target_skin[i]
                if target_skin_cluster:
                    cmds.skinCluster(target_skin_cluster, e=1, ub=1)
                cmds.skinCluster(target[i], source_skin_joint, tsb=1)
        if target_type == 'Point':
            target_model = target[0].split('.')[0]
            target_skin_cluster = target_skin
            if target_skin_cluster:
                targetJoint = cmds.skinCluster(target_model, q=1, inf=1)
                joint = [i for i in source_skin_joint if i not in targetJoint]
                if joint:
                    for j in joint:
                        cmds.skinCluster(target_skin_cluster, e=1, ai=j, wt=0)
            else:
                cmds.skinCluster(target_model, source_skin_joint, tsb=1)
                # cmds.skinCluster('joint3','pCube1', ignoreSelected=0,mul=1)
        print('aaa')
        # 进行拷贝权重
        if copy_way == 'Normal':
            if target_type == 'Model':
                for i in range(len(target)):
                    print('Model')
                    cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestComponent', influenceAssociation='oneToOne', noMirror=1, ds=target_skin[i])
            if target_type == 'Point':
                print('Point')
                cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestComponent', influenceAssociation='oneToOne', noMirror=1, ds=target_skin)
        if copy_way == 'UV':
            if target_uv_set and target_uv_set:
                if target_type == 'Model':
                    for i in range(len(target)):
                        cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestComponent',uvSpace=(soure_uv_set, target_uv_set), influenceAssociation='oneToOne', noMirror=1, ds=target_skin[i])
                if target_type == 'Point':
                    cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestComponent',uvSpace=(soure_uv_set, target_uv_set), influenceAssociation='oneToOne', noMirror=1, ds=target_skin)
            else:
                print('请加载uv选集')
        # else:
        #     print('源没有骨骼蒙皮')
    else:
        cmds.warning('请确认是否有拷贝源和目标列表和源蒙皮。')

new_maya_base_copy_joint_weight('Normal', 'pCube1', ['pCube2'], 'skinCluster4', ['skinCluster7'], '', '')



cmds.copySkinWeights(ss='skinCluster4', surfaceAssociation='closestComponent', influenceAssociation='oneToOne', noMirror=1, ds='skinCluster3')





print(cmds.listConnections('cluster5.message', d=True))
set_members = cmds.sets('cluster6Set', query=True)


import maya.cmds as cmds
# 选择变形器
deformer = cmds.ls(selection=True, type='deformer')
print(deformer)
# 获取变形器输出几何体
affected_geometry = cmds.listConnections(deformer + '.outputGeometry')

# 列出集合内元素
for geo in affected_geometry:
    elements = cmds.ls(geo, long=True)
    print("Geometry: {}".format(geo))
    for element in elements:
        print("Element: {}".format(element))

set_members = cmds.sets('cluster6Set', query=True)
print(set_members)

name_1 = 'a_'
name_2 = 'b_'
name_3 = 'c_'
num_indicator = 3
deform_name = 'blendShape2'

targets = cmds.ls(deform_name + '.inputTarget[0].inputTargetGroup[*]')
# print(targets)
# print(cmds.aliasAttr(parent_item.text(0)+'.w[0]', q=1))
blendshape_targets = cmds.listAttr(deform_name + '.w', m=True)
for i in range(len(blendshape_targets)):
    if not name_2:
        name_2 = blendshape_targets[i]
    text = ''
    if num_indicator == 0:
        text = str(i) + name_1 + name_2 +name_3
    if num_indicator == 1:
        text = name_1 + str(i) + name_2 + name_3
    if num_indicator == 2:
        text = name_1 + name_2 + str(i) + name_3
    if num_indicator == 3:
        text = name_1 + name_2 +name_3 + str(i)
    for target in targets:
        target = target.split('[')[-1][:-1]
        # print(target)
        name = cmds.aliasAttr(deform_name + '.w[' + target + ']', q=1)
        if name == blendshape_targets[i]:
            cmds.aliasAttr(text,deform_name+'.w[' + str(i) + ']')


import maya.cmds as cmds

# 获取当前聚焦的面板
current_panel = cmds.getPanel(withFocus=True)

# 检查面板类型是否为Blend Shape编辑器
if cmds.getPanel(typeOf=current_panel) == 'blendShapeEditor':
    # 查询选中的Blend Shape节点
    selected_bs = cmds.blendShapeEditor(current_panel, query=True, selectedBlendShape=True)
    if selected_bs:
        print("当前选择的BlendShape节点:", selected_bs[0])
    else:
        print("未选择任何BlendShape节点。")
else:
    print("当前聚焦的面板不是Blend Shape编辑器。")



def read_weight(obj,deform,bs_name):
    if bs_name:
        # 获取bs选集
        set = cmds.listConnections(deform + '.message', d=True, type='objectSet')
        set_obj = cmds.ls(cmds.sets(set, q=True),fl=1)
        weight_list = []

        for i in range(len(set_obj)):
            an = cmds.ls(deform+'.inputTarget[0].baseWeights['+str(i)+']')
            weight = cmds.getAttr(an)
            weight_list.append(weight)
    else:
        weight_list = cmds.percent(deform, obj, q=1, v=1)
    print(weight_list)
read_weight('pCube5','blendShape4','group2')

print(blendshape_targets)










import maya.api.OpenMaya as OpenMaya


rich_selection = OpenMaya.MGlobal.getRichSelection(True)
#print(point)
# 将软选择转换为选择列表
selection_list = OpenMaya.MSelectionList()
selection_list = rich_selection.getSelection()

# 遍历选择列表中的组件
iter = OpenMaya.MItSelectionList(selection_list, OpenMaya.MFn.kMeshVertComponent)
# 获取当前组件的 DAG 路径和对象
dag_path = OpenMaya.MDagPath()
component = OpenMaya.MObject()
dag_path = iter.getDagPath()

# 确保路径指向形状节点（例如：pCubeShape）
dag_path.extendToShape()  # 关键步骤！

# 创建单索引组件函数集（顶点组件）
fn_component = OpenMaya.MFnSingleIndexedComponent(component)

# 获取顶点索引和权重
elements = OpenMaya.MIntArray()
weights = OpenMaya.MDoubleArray()
elements = fn_component.getElements()
fn_component.getWeights(dag_path, weights)

# 遍历所有顶点
for i in range(elements.length()):
    vertex_index = elements[i]
    vertex_name = "{}.vtx[{}]".format(dag_path.fullPathName(), vertex_index)
    soft_selection[vertex_name] = weights[i]

iter.next()




# from __future__ import unicode_literals, print_function, division
import maya.api.OpenMaya as om

# 创建一个 MRichSelection 对象
rich_sel = om.MGlobal.getRichSelection(0)

# 获取软选择列表
soft_sel = rich_sel.getSelection()

# 遍历软选择中的元素并获取权重
iter = om.MItSelectionList(soft_sel, om.MFn.kMeshVertComponent)
while not iter.isDone():
    dag_path, component = iter.getComponent()
    print(dag_path.fullPathName())
    mesh_fn = om.MFnMesh(dag_path)

    # 创建一个 MFnSingleIndexedComponent 对象, 用于操作组件
    mfn_component = om.MFnSingleIndexedComponent(component)
    # 获取每个组件的id
    elements = mfn_component.getElements()
    for i in range(len(elements)):
        # 获取每个组件的权重
        weight = mfn_component.weight(i).influence
        print("Vertex Index: {}, Weight: {}".format(elements[i], weight))
    iter.next()

import maya.cmds as cmds


def get_selected_shape_editor_targets():
    # 获取当前聚焦的面板
    current_panel = cmds.getPanel(withFocus=True)
    print(current_panel)
    cmds.deleteUI(current_panel)
    # 检查是否是BlendShape编辑器（即图中的Shape Editor）
    # if cmds.getPanel(typeOf=current_panel) != 'blendShapeEditor':
    #     cmds.warning("当前面板不是Shape Editor！")
    #     return []

    # 获取选中的BlendShape节点
    # selected_bs = cmds.blendShapeEditor(current_panel, query=True, selectedConnection=True)
    # if not selected_bs:
    #     cmds.warning("未选择BlendShape节点！")
    #     return []

    blend_shape_node = 'blendShape2'

    # 获取用户在编辑器中选中的目标体索引
    selected_indices = cmds.blendShapeEditor(current_panel, query=True, slc=True)
    if not selected_indices:
        cmds.warning("未选择任何目标体！")
        return []

    # 获取BlendShape节点所有目标体的别名（即图中显示的pSphere5、blendShape2等名称）
    target_aliases = cmds.listAttr(f"{blend_shape_node}.w", multi=True) or []

    # 通过索引获取选中的名称
    selected_names = []
    for idx in selected_indices:
        if idx < len(target_aliases):
            alias = cmds.aliasAttr(f"{blend_shape_node}.{target_aliases[idx]}", query=True)
            selected_names.append(alias)

    return selected_names


# 使用示例
selected_targets = get_selected_shape_editor_targets()
if selected_targets:
    print("当前选择的BlendShape目标体名称:", selected_targets)
else:
    print("未选择任何目标体。")


import maya.cmds as cmds
parent_ui = cmds.getPanel(withFocus=True)
print(parent_ui)
def get_ui_children(parent_ui):
    # 检查父控件是否存在
    if not cmds.control(parent_ui, exists=True):
        return []

    # 获取直接子控件列表
    children = cmds.layout(parent_ui, query=True, childArray=True) or []
    return children
def get_all_ui_children(parent_ui, include_nested=True):
    children = []
    direct_children = get_ui_children(parent_ui)
    for child in direct_children:
        children.append(child)
        # 递归获取子控件的子控件
        if include_nested:
            nested_children = get_all_ui_children(child, include_nested=True)
            children.extend(nested_children)
    return children
a = get_ui_children(get_all_ui_children)
print(a)
cmds.deleteUI(a)




def generic_mapping(x, input_min, input_max, output_min, output_max):
    return

# 示例：将 [10, 20] 映射到 [5, -2]
print(generic_mapping(12, 10, 20, 5, -2))  # 输出 1.5





















sel = cmds.ls(sl=1)
cmds.select(sel[:-1])
joint = cmds.ls(sl=1)
mesh = sel[-1]
print(joint)
print(mesh)
for j in joint:
    grp = cmds.group(n=j + '_secondary_grp', em=1)
    curve = cmds.circle(c=(0, 0, 0) ,nr=(0, 1, 0), sw=360, r=1 ,d=3 ,ut=0 ,tol=0.01 ,s=8 ,ch=0, n=j+'_secondary' )
    cmds.parent(curve, grp)
    cmds.delete(cmds.orientConstraint(j, grp))
    # cmds.delete(cmds.pointConstraint(j, grp))
    grp_j = cmds.group(n=j + '_joint_grp', em=1)
    cmds.delete(cmds.parentConstraint(j, grp_j))
    cmds.parent(j, grp_j)
    grp_j2 = cmds.group(n=j + '_joint_grp2', em=1)
    cmds.delete(cmds.parentConstraint(j, grp_j2))
    cmds.parent(grp_j, grp_j2)
    # 创建附着
    proximityPin = cmds.createNode('proximityPin')
    cmds.select(mesh)
    cmds.delete(cmds.cluster())
    shape_nodes = cmds.listRelatives(mesh, shapes=True, fullPath=True)
    cmds.connectAttr(shape_nodes[0]+'.worldMesh[0]', proximityPin + '.deformedGeometry')
    cmds.connectAttr(shape_nodes[-1]+'.outMesh', proximityPin+'.originalRailCurve')
    cmds.connectAttr(proximityPin+'.outputMatrix[0]', grp+'.offsetParentMatrix')
    matrix = cmds.getAttr(j+'.worldMatrix[0]')
    # print(matrix[-4])
    composeMatrix_matrix = cmds.createNode('composeMatrix')
    cmds.connectAttr(composeMatrix_matrix+'.outputMatrix', proximityPin+'.inputMatrix[0]')
    cmds.setAttr(composeMatrix_matrix + '.inputTranslateX', matrix[-4])
    cmds.setAttr(composeMatrix_matrix + '.inputTranslateY', matrix[-3])
    cmds.setAttr(composeMatrix_matrix + '.inputTranslateZ', matrix[-2])

    # 创建逆矩阵除缩放归位
    decomposeMatrix = cmds.createNode('decomposeMatrix')
    cmds.connectAttr(curve[0]+'.inverseMatrix', decomposeMatrix+'.inputMatrix')
    composeMatrix = cmds.createNode('composeMatrix')
    cmds.connectAttr(decomposeMatrix + '.outputQuat', composeMatrix + '.inputQuat')
    cmds.connectAttr(decomposeMatrix + '.outputRotate', composeMatrix + '.inputRotate')
    cmds.connectAttr(decomposeMatrix + '.outputShear', composeMatrix + '.inputShear')
    cmds.connectAttr(decomposeMatrix + '.outputTranslate', composeMatrix + '.inputTranslate')
    cmds.connectAttr(composeMatrix+'.outputMatrix', curve[0]+'.offsetParentMatrix')

    # 链接
    cmds.setAttr(grp + '.tx',0)
    cmds.setAttr(grp + '.ty', 0)
    cmds.setAttr(grp + '.tz', 0)
    cmds.connectAttr(curve[0] + '.t', grp_j + '.t')
    cmds.connectAttr(curve[0] + '.r', grp_j + '.r')
    cmds.connectAttr(curve[0] + '.s', grp_j + '.s')












