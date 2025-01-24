# -*- coding: utf-8 -*-
import json
import random
import maya.mel as mel
import maya.cmds as cmds
# 获取文件路径
import os
import sys
import inspect
import importlib
import json

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version
# 库添加到系统路径
sys.path.append(library_path)

# 加载曲线编辑
import curve
from curve import *
importlib.reload(curve)

import others_library
from others_library import *
importlib.reload(others_library)

# 加载文本
class CurveControllerEdit:
    def __init__(self):
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
        # 版本号
        self.maya_version = cmds.about(version=True)

        self.curve = CreateAndEditCurve()
        self.other_library = OthersLibrary()
    # ADV改控制器（为了兼容ADV我稍微改下就直接用了）
    def as_swap_curve(self, type, Name, Color, Num):
        Select = cmds.ls(sl=1)
        AllSet = []
        if cmds.objExists('AllSet'):
            cmds.select('AllSet')
            mel.eval('SelectHierarchy;')
            AllSet = cmds.ls(sl=1)
        self.curve.create_curve((self.file_path + '\curve_library'), Name)
        self.modify_vontroller_shape('SoftSelectionSize', 0, 0, 0)
        EndSelect = cmds.ls(sl=1)
        cmds.select(Select, r=1)
        cmds.select(EndSelect, add=1)
        side = ""
        oppositeSide = ""
        allSet = ""
        tempString = []
        tempString2 = []
        tempString3 = []
        sel = cmds.ls(sl=1)
        last = len(sel) - 1
        selShapes = []
        if len(sel) < 2:
            cmds.wraning("Selected both controls to replace, and the new curve to use")

        for i in range(0, len(sel)):
            tempString = cmds.listRelatives(sel[i], s=1)
            selShapes.append(tempString[0])
            '''if mel.gmatch(sel[i], "*Extra*"):
                continue'''

            if not cmds.objExists(selShapes[i]):
                cmds.warning("selected object:\"" + sel[i] + "\" is not a nurbsCurve")

            tempString = cmds.listRelatives(sel[i], s=1)
            '''if mel.objecttype(selShapes[i]) != "nurbsCurve" and cmds.objecttype(selShapes[i]) != "nurbsSurface":
                cmds.warning("selected object:\"" + sel[i] + "\" is not a nurbsCurve")'''

        cmds.select(sel[last])
        mel.eval('DeleteHistory;')
        for i in range(0, len(sel) - 1):
            tempString = cmds.listRelatives(sel[i], s=1)
            tempString3 = []
            if len(tempString):
                tempString3 = cmds.listConnections((tempString[0] + ".v"),
                                                 p=1, s=1, d=0)
                cmds.delete(tempString)

            cmds.duplicate(sel[last], n='tempXform')
            tempString = cmds.listRelatives('tempXform', s=1, f=1)
            for y in range(0, len(tempString)):
                cmds.rename(tempString[y],
                          (sel[i] + "Shape"))

            allSet = "AllSet"
            if cmds.objExists('FaceAllSet'):
                if mel.eval('sets -im FaceAllSet ' + sel[i] + ';'):
                    allSet = "FaceAllSet"

            tempString = cmds.listRelatives('tempXform', s=1)
            for y in range(0, len(tempString)):
                tempString2 = cmds.parent(tempString[y], sel[i], add=1, s=1)
                tempString[y] = tempString2[0]
                rot = cmds.xform(sel[i], q=1, ro=1, ws=1)
                #		if(!(`gmatch $sel[0] "IK*"` || `gmatch $sel[0] "Pole*"` || `gmatch $sel[0] "RootX*"`))
                if not (rot[0] == 0 and rot[1] == 0 and rot[2] == 0):
                    pass
                    # cmds.rotate(-90, -90, 0,(tempString[y] + ".cv[0:9999]"),r=1, os=1)#####
                if sel[i] in AllSet:
                    if cmds.objExists('AllSet'):
                        mel.eval('sets -add ' + allSet + ' ' + tempString[y] + ';')
                    # cmds.sets(tempString[y], add=allSet)

                if tempString3:
                    cmds.catch(mel.eval("connectAttr " + tempString3[0] + " " + tempString[y] + ".v"))

            cmds.delete('tempXform')
        cmds.dgdirty(a=1)
        cmds.delete(EndSelect)
        cmds.select(Select)
        self.curve.change_curve_color(type, Select, Color, Num)

    # 旋转控制器
    def rotation_controller(self, rotate):
        mel.eval('reflectionSetMode none;')
        X = 0.0
        Y = 0.0
        Z = 0.0
        if rotate == "X":
            X = float(90)
            Y = float(0)
            Z = float(0)
        if rotate == "Y":
            X = float(0)
            Y = float(90)
            Z = float(0)
        if rotate == "Z":
            X = float(0)
            Y = float(0)
            Z = float(90)
        self.modify_vontroller_shape("rotate", X, Y, Z)

    # 修改控制器大小
    def modify_vontroller_shape(self, deformation_type, x, y, z):
        cmds.undoInfo(ock=1)
        curve = cmds.ls(sl=1)
        for i in range(0, len(curve)):
            Shape = cmds.listRelatives(curve[i], s=1)
            cmds.select(cl=1)
            cmds.select((Shape[0] + ".cv[0:]"))
            if deformation_type == "translate":
                cmds.move(x, y, z, localSpace=1)
            if deformation_type == "rotate":
                cmds.rotate(x, y, z, r=1)
            if deformation_type == "scale":
                cmds.scale(x, y, z, r=1)
            if deformation_type == "SoftSelectionSize":
                size = cmds.softSelect(q=1, ssd=1)
                shape = cmds.listRelatives(curve[i], c=1, type='nurbsCurve')
                AllNum = cmds.getAttr(shape[0] + '.boundingBox.boundingBoxSize')
                AllNum = max(AllNum)
                num = max(AllNum)
                scale = size / num * 2.14
                cmds.scale((scale), (scale), (scale), r=1)
            cmds.select(cl=1)
        cmds.select(curve)
        cmds.undoInfo(cck=1)

    # 旧版生成控制器
    def old_create_fk(self, controller_group_num, suffix, if_remove_joint, extract_constraints):
        cmds.undoInfo(ock=1)
        mel.eval('SelectHierarchy;')
        joint = cmds.ls(typ='joint', sl=1)
        all = cmds.ls(sl=1)
        if if_remove_joint == True:
            for j in joint:
                if not cmds.listRelatives(j, c=1):
                    joint.remove(j)
        # 建立控制器
        top_grp = []
        curve = []
        for i in range(0, len(joint)):
            cmds.rename(self.curve.create_curve((self.root_path +'\\'+ self.maya_version + '\curve_library'), 'A圆'), (joint[i] + suffix + '_C'))
            sel = cmds.ls(sl=1)
            curve.append(sel[0])
            self.curve.change_curve_color('Index', sel, 0, 18)
            self.modify_vontroller_shape('SoftSelectionSize', 0, 0, 0)
            for j in range(0, controller_group_num):
                mel.eval('doGroup 0 1 1;')
                sel = cmds.ls(sl=1)
                # 建立样条组
                cmds.rename( sel[0], (joint[i] + suffix + '_G'+ str(controller_group_num - j)))
            top_grp.append(sel[0])
            cmds.delete(cmds.parentConstraint(joint[i], (joint[i] + suffix + '_G1')))
        # 进行父化
        for i in range(1, len(joint)):
            parent = cmds.listRelatives(joint[i], p=1)
            joint_parent = cmds.ls(parent,typ='joint')
            if not joint_parent:
                for j in range(0, len(all)):
                    parent = cmds.listRelatives(p=1)
                    joint_parent = cmds.ls(parent,typ='joint')
                    if joint_parent:
                        break
            cmds.parent((joint[i] + suffix + '_G1'), (joint_parent[0] + suffix + '_C'))
        # 进行约束
        if extract_constraints == True:
            cmds.select(cl=1)
            if not cmds.objExists('All_Constraints'):
                cmds.group(em=1,n='All_Constraints')
        for i in range(0, len(joint)):
            parent_constraint = cmds.parentConstraint((joint[i] + suffix + '_C'), joint[i])
            scale_constraint = cmds.scaleConstraint((joint[i] + suffix + '_C'), joint[i])
            if extract_constraints == True:
                cmds.parent(parent_constraint, scale_constraint, 'All_Constraints')
        cmds.undoInfo(cck=1)
    # 切换控制器
    def switch_controllers(self):
        cmds.undoInfo(ock=1)
        show = cmds.getAttr('BaseRoot_Grp.visibility')
        if show == 0:
            cmds.setAttr('BaseRoot_Grp.visibility', 1)
            if cmds.objExists('SkinRootJoint_Grp'):
                cmds.setAttr('SkinRootJoint_Grp.visibility', 0)
            if cmds.objExists('MainSystem_Grp'):
                cmds.setAttr('MainSystem_Grp.visibility', 0)
        else:
            cmds.setAttr('BaseRoot_Grp.visibility', 0)
            if cmds.objExists('SkinRootJoint_Grp'):
                cmds.setAttr('SkinRootJoint_Grp.visibility', 1)
            if cmds.objExists('MainSystem_Grp'):
                cmds.setAttr('MainSystem_Grp.visibility', 1)
        cmds.undoInfo(cck=1)
    # 控制器归位
    def reset_controllers(self):
        cmds.undoInfo(ock=1)
        if cmds.objExists('MainSystem_Grp'):
            FK_controller_sys = cmds.getAttr('MainSystem_Grp.FK_controller_sys')
            FK_controller_sys = FK_controller_sys.replace('\'', '\"')
            FK_controller_sys = json.loads(FK_controller_sys)

            Independence_controller_sys = cmds.getAttr('MainSystem_Grp.Independence_controller_sys')
            Independence_controller_sys = Independence_controller_sys.replace('\'', '\"')
            Independence_controller_sys = json.loads(Independence_controller_sys)

            for i in range(-2,0):
                for str in ['X','Y','Z']:
                    for d in FK_controller_sys:
                        if cmds.objExists(d['FK_sys'][i]):
                            cmds.setAttr(d['FK_sys'][i]+'.translate'+str, 0)
                            cmds.setAttr(d['FK_sys'][i]+'.rotate'+str, 0)
                            cmds.setAttr(d['FK_sys'][i]+'.scale'+str, 1)
                    for d in Independence_controller_sys:
                        if cmds.objExists(d['Independence_sys'][i]):
                            cmds.setAttr(d['Independence_sys'][i]+'.translate'+str, 0)
                            cmds.setAttr(d['Independence_sys'][i]+'.rotate'+str, 0)
                            cmds.setAttr(d['Independence_sys'][i]+'.scale'+str, 1)
                for d in FK_controller_sys:
                    if cmds.objExists(d['FK_sys'][i]):
                        cmds.setAttr(d['FK_sys'][i] + '.visibility', 1)
                for d in Independence_controller_sys:
                    if cmds.objExists(d['Independence_sys'][i]):
                        cmds.setAttr(d['Independence_sys'][i] + '.visibility', 1)
        cmds.undoInfo(cck=1)
    # 控制器镜像
    def mirror_controllers(self,direction):
        cmds.undoInfo(ock=1)
        mirror = 'R'
        if direction == 'RL':
            mirror = 'L'
        try:
            # 获取插件默认生成的部分
            FK_controller_sys = cmds.getAttr('MainSystem_Grp.FK_controller_sys')  # 获取fk控制器系统
            FK_controller_sys = FK_controller_sys.replace('\'', '\"')
            FK_controller_sys = json.loads(FK_controller_sys)

            Independence_controller_sys = cmds.getAttr('MainSystem_Grp.Independence_controller_sys')  # 获取独立控制器系统
            Independence_controller_sys = Independence_controller_sys.replace('\'', '\"')
            Independence_controller_sys = json.loads(Independence_controller_sys)

            curve_type_list = [-9,-19]
            curve_list = [FK_controller_sys,Independence_controller_sys]
            for num in range(0, len(curve_list)):
                all_need_query_nodes = []
                for dict in curve_list[num]:
                    soure = list(dict.values())[0]
                    all_need_query_nodes.append(soure[-1])
                for node in all_need_query_nodes:
                    have_direction = node[curve_type_list[num]]
                    # print(have_direction)
                    mirror_direction = []
                    if have_direction == 'R':
                        mirror_direction = 'L'
                    if have_direction == 'L':
                        mirror_direction = 'R'
                    if mirror_direction == mirror:
                        mirror_curve_name = node[:curve_type_list[num]]+mirror_direction+node[curve_type_list[num]+1:]
                        # print(mirror_curve_name)
                        if cmds.objExists(mirror_curve_name):
                            all_cv = cmds.ls(node+'.cv[*]',fl=1)
                            # print(all_cv)
                            for i in range(0,len(all_cv)):
                                # print(mirror_curve_name+'.cv['+str(i)+']')
                                if cmds.objExists(mirror_curve_name+'.cv['+str(i)+']'):
                                    t = cmds.xform(all_cv[i], q=1, t=1)
                                    cmds.setAttr((mirror_curve_name+'.cv['+str(i)+']'), t[0], t[1], t[2])
            # print(all_need_query_nodes)
            # all_need_query_nodes = []
            # for dict in Independence_controller_sys:
            #     soure = list(dict.values())[0]
            #     all_need_query_nodes.append(soure[-1])
        except:
            pass
        cmds.undoInfo(cck=1)
    # 创建控制器系统
    def create_controllers_system(self, controller_group_num, suffix, if_remove_joint, keep_curve_shape):
        cmds.undoInfo(ock=1)
        try:
            if cmds.objExists('All_ControllerSystem_Grp') and cmds.objExists('BaseRoot_Grp'):
                self.reset_controllers()
                self.other_library.switch_skin_model_hand_influence_state()
                # 删除控制器系统组和蒙皮骨骼组,提取附加的对象p到外面
                reduction_dict_list = []# 保存自定义编辑列表
                reduction_curve_dict_list = []  # 保存需要还原控制器的列表
                reduction_curve_grp_dict_list = []  # 保存需要还原控制器组的列表
                need_delete_curve = []
                #  还原约束所需变量
                # FK_controller_sys = []
                # Independence_controller_sys = []
                all_need_query_nodes = []
                if cmds.objExists('MainSystem_Grp'):
                    # 删除约束组
                    if cmds.objExists('AllConstraintSystem_Grp'):
                        cmds.delete('AllConstraintSystem_Grp')
                    # 判断所需的是否需要在
                    # 获取所有的transform对象
                    all_child = cmds.listRelatives('MainSystem_Grp', c=1, ad=1, type='transform')
                    # 获取插件默认生成的部分
                    FK_controller_sys = cmds.getAttr('MainSystem_Grp.FK_controller_sys')# 获取fk控制器系统
                    FK_controller_sys = FK_controller_sys.replace('\'', '\"')
                    FK_controller_sys = json.loads(FK_controller_sys)

                    Independence_controller_sys = cmds.getAttr('MainSystem_Grp.Independence_controller_sys')# 获取独立控制器系统
                    Independence_controller_sys = Independence_controller_sys.replace('\'', '\"')
                    Independence_controller_sys = json.loads(Independence_controller_sys)

                    need_delete_object = ['MainSystem_Grp', 'Main_controller_Grp', 'Independence_controller_Grp',
                                          'FK_controller_Grp', 'IK_controller_Grp']

                    # 查询所有链接建立列表并断开，查询是否有约束，并且记录还原约束所需的信息


                    for dict in FK_controller_sys:
                        soure = list(dict.values())[0]
                        for s in soure:
                            all_need_query_nodes.append(s)
                    for dict in Independence_controller_sys:
                        soure = list(dict.values())[0]
                        for i in range(0,len(soure)):
                            all_need_query_nodes.append(soure[i])
                    # print(all_need_query_nodes)
                    # for s in all_need_query_nodes:
                    #     reduction_list = []
                    #     parentConstraint = []
                    #     pointConstraint = []
                    #     orientConstraint = []
                    #     aimConstraint = []
                    #     scaleConstraint = []
                    #     Constraint = []
                    #     # all_connect_node = cmds.listConnections('HelmetJ10_R_IndependenceGrp2')
                    #     # all_connect_node = list(dict.fromkeys(all_connect_node))
                    #     # print(all_connect_node)
                    #     all_connect_node = cmds.listConnections(s)
                    #     if all_connect_node:
                    #         seen = set()
                    #         all_connect_node = [x for x in all_connect_node if not (x in seen or seen.add(x))]
                    #         for node in all_connect_node:
                    #             if cmds.objectType(node) == 'parentConstraint':
                    #                 parentConstraint = node
                    #             elif cmds.objectType(node) == 'pointConstraint':
                    #                 pointConstraint = node
                    #             elif cmds.objectType(node) == 'orientConstraint':
                    #                 orientConstraint = node
                    #             elif cmds.objectType(node) == 'aimConstraint':
                    #                 aimConstraint = node
                    #             if cmds.objectType(node) == 'scaleConstraint':
                    #                 scaleConstraint = node
                    #             cmds.setAttr(node+'.nodeState', 2)
                    #         for attribute in ['tx','ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
                    #             have_connect = cmds.listConnections(s + '.'+ attribute, c=1, p=1)
                    #             if have_connect:
                    #                 Constraint.append(have_connect)
                    #                 cmds.disconnectAttr(have_connect[1], have_connect[0])
                    #     if parentConstraint or pointConstraint or orientConstraint or aimConstraint or scaleConstraint or Constraint:
                    #         my_dict = {
                    #             'soure': s,
                    #             'parentConstraint': parentConstraint,
                    #             'pointConstraint': pointConstraint,
                    #             'orientConstraint': orientConstraint,
                    #             'aimConstraint': aimConstraint,
                    #             'scaleConstraint': scaleConstraint,
                    #             'Constraint': Constraint
                    #         }
                    #         reduction_curve_grp_dict_list.append(my_dict)
                    # print(reduction_curve_grp_dict_list)

                    # for fk in FK_controller_sys:
                    #     values_list = list(fk.values())
                    #     need_delete_object = need_delete_object + values_list[0]
                    # for ind in Independence_controller_sys:
                    #     values_list = list(ind.values())
                    #     need_delete_object = need_delete_object + values_list[0]
                    need_extract_grp = [x for x in all_child if x not in all_need_query_nodes]
                    need_extract_grp = [x for x in need_extract_grp if x not in need_delete_object]
                    # print(need_extract_grp)

                    if need_extract_grp:
                        for ex in need_extract_grp:
                            parent = cmds.listRelatives(ex, parent=True)
                            child = cmds.listRelatives(ex, children=True)
                            dict = [{'parent':parent, 'our':ex, 'child': child}]
                            reduction_dict_list.append(dict[0])
                    # 提取对应的组到外面
                    for dict in reduction_dict_list:
                        parent = dict['parent']
                        our = dict['our']
                        child = dict['child']
                        if child:
                            new_child = [x for x in child if x not in all_need_query_nodes]
                            if not new_child:
                                cmds.parent(child, parent)
                        # cmds.parent(our, w=1)
                    if need_extract_grp:
                        cmds.parent(need_extract_grp, w=1)



                    # 获取可能需要保留的控制器
                    for node in all_need_query_nodes:
                        have_connect = cmds.listConnections(node)

                        if have_connect:
                            reduction_curve_dict_list.append(node)
                            parent = cmds.listRelatives(node, parent=True)
                            child = cmds.listRelatives(node, children=True)
                            shape_child = cmds.listRelatives(node, children=True,type='nurbsCurve')
                            if child and shape_child:
                                child = [item for item in child if item not in shape_child]
                            if child:
                                cmds.parent(child,parent)
                            cmds.parent(node,w=1)
                    for fk in FK_controller_sys:
                        cur = fk['FK_sys'][-1]
                        if not cur in reduction_curve_dict_list:
                            reduction_curve_dict_list.append(cur)
                    for ind in Independence_controller_sys:
                        cur = ind['Independence_sys'][-1]
                        if not cur in reduction_curve_dict_list:
                            reduction_curve_dict_list.append(cur)
                    #print(reduction_dict_list)
                    # print(dddd)
                    # 提取所有控制器的形状节点，并且建立字典，后面正常生成完控制器后对其进行替换
                    if keep_curve_shape == True:
                        # 获取插件默认生成的部分
                        for fk in FK_controller_sys:
                            parent = cmds.listRelatives(fk['FK_sys'][-1], p=True)
                            # child = []
                            child = cmds.listRelatives(fk['FK_sys'][-1], c=True)
                            shape_child = cmds.listRelatives(fk['FK_sys'][-1], children=True, type='nurbsCurve')
                            if child and shape_child:
                                child = [item for item in child if item not in shape_child]
                            cur = fk['FK_sys'][-1]
                            if child and parent:
                                cmds.parent(child, parent)
                            # print(cur)
                            if parent:
                                cmds.parent(cur,w=1)
                            need_delete_curve.append(cur)
                        for fk in Independence_controller_sys:
                            parent = cmds.listRelatives(fk['Independence_sys'][-1], p=True)
                            # child = []
                            child = cmds.listRelatives(fk['Independence_sys'][-1], c=True)
                            shape_child = cmds.listRelatives(fk['Independence_sys'][-1], children=True, type='nurbsCurve')
                            if child and shape_child:
                                child = [item for item in child if item not in shape_child]
                            cur = fk['Independence_sys'][-1]
                            if child and parent:
                                cmds.parent(child, parent)
                            if parent:
                                cmds.parent(cur,w=1)
                            need_delete_curve.append(cur)

                        for xyz in ['X', 'Y', 'Z']:
                            for d in FK_controller_sys:
                                cmds.setAttr(d['FK_sys'][-1] + '.translate' + xyz, 0)
                                cmds.setAttr(d['FK_sys'][-1] + '.rotate' + xyz, 0)
                                cmds.setAttr(d['FK_sys'][-1] + '.scale' + xyz, 1)
                            for d in Independence_controller_sys:
                                cmds.setAttr(d['Independence_sys'][-1] + '.translate' + xyz, 0)
                                cmds.setAttr(d['Independence_sys'][-1] + '.rotate' + xyz, 0)
                                cmds.setAttr(d['Independence_sys'][-1] + '.scale' + xyz, 1)
                        for d in FK_controller_sys:
                            cmds.setAttr(d['FK_sys'][-1] + '.visibility', 1)
                        for d in Independence_controller_sys:
                            cmds.setAttr(d['Independence_sys'][-1] + '.visibility', 1)

                    cmds.delete('MainSystem_Grp')

                # 复制基础骨骼，建立蒙皮骨骼

                # 建立控制系统
                if not cmds.objExists('MainSystem_Grp'):
                    cmds.group(em=1, n='MainSystem_Grp', p='All_ControllerSystem_Grp')
                # 建立约束存放组
                if not cmds.objExists('AllConstraintSystem_Grp'):
                    cmds.group(em=1, n='AllConstraintSystem_Grp', p='All_ControllerSystem_Grp')
                # 建立蒙皮骨骼组
                if not cmds.objExists('SkinRootJoint_Grp'):
                    cmds.group(em=1,n='SkinRootJoint_Grp',p='All_ControllerSystem_Grp')
                # 建立总控制器
                if cmds.objExists('Main_controller_Grp'):
                    pass
                else:
                    cmds.group(em=1,n='Main_controller_Grp',p='MainSystem_Grp')
                cmds.setAttr('BaseRoot_Grp.visibility',0)
                ###################################
                # 检查完毕开始创建
                ###################################
                cmds.select('SkinRootJoint_Grp')
                mel.eval('SelectHierarchy;')
                skin_joint = cmds.ls(sl=1, type='joint')
                all_connect_node, Constraint = self.return_constraint(skin_joint + reduction_curve_dict_list, [], [])
                # print(all_connect_node)
                # print(Constraint)
                # 创建蒙皮骨骼
                base_joint,all = self.create_controllers_system_copy_joint_part(suffix)
                # print(all_connect_node)
                # print(Constraint)
                # 开始为蒙皮骨骼创建独立控制器
                Independence_controller = []
                if not cmds.objExists('Independence_controller_Grp'):
                    cmds.group(em=1,n='Independence_controller_Grp',p='MainSystem_Grp')
                cmds.select('SkinRootJoint_Grp')
                mel.eval('SelectHierarchy;')
                skin_joint = cmds.ls(sl=1, type='joint')
                # print('移除骨骼：',if_remove_joint)
                # print(skin_joint)
                if if_remove_joint == True:
                    skin_joint = [j for j in skin_joint if cmds.listRelatives(j, c=1, type='joint')]
                for j in skin_joint:
                    if cmds.objExists(j+'_IndependenceCurve'):
                        cur = [(j+'_IndependenceCurve')]
                        cmds.select(cur)
                        reduction_curve_dict_list.remove(cur[0])
                    else:
                        cur = cmds.circle(c=(0, 0, 0), ch=0, d=1, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(1, 0, 0), n=(j+'_IndependenceCurve'))
                        self.modify_vontroller_shape('SoftSelectionSize', 1, 1, 1)
                        self.curve.change_curve_color('Index', cur, [0,0,0], 20)
                    if (j+'_IndependenceCurve') in need_delete_curve:
                        need_delete_curve.remove((j+'_IndependenceCurve'))
                    grp_str = ''
                    ls_grp = []
                    for g in range(0,controller_group_num):
                        if cmds.objExists(j + '_IndependenceGrp' + str(g + 1)):
                            two_grp = (j + '_IndependenceGrp' + str(g + 1))
                            for attribute,num in zip(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'],[0,0,0,0,0,0,1,1,1,1]):
                                cmds.setAttr(two_grp + '.' + attribute, num)
                        else:
                            two_grp = cmds.group(n=(j + '_IndependenceGrp' + str(g + 1)),em=1)
                        if ls_grp:
                            cmds.parent(two_grp, ls_grp)
                        ls_grp = two_grp
                        grp_str = grp_str +'\"' + (j+'_IndependenceGrp'+str(g+1)) + '\"' + ','

                    cmds.parent((j+'_IndependenceGrp1'),'Independence_controller_Grp')
                    cmds.delete(cmds.parentConstraint(j,(j+'_IndependenceGrp1'),w=1))

                    cmds.parent(cur, (j + '_IndependenceGrp' + str(controller_group_num)))
                    cmds.delete(cmds.parentConstraint(j, cur, w=1))

                    # parentConstraint = cmds.parentConstraint((j + '_IndependenceCurve'), j, w=1)
                    # cmds.parent(parentConstraint, 'AllConstraintSystem_Grp')
                    # scaleConstraint = cmds.scaleConstraint((j + '_IndependenceCurve'), j, mo=1, weight=1)
                    # cmds.parent(scaleConstraint, 'AllConstraintSystem_Grp')
                    # 生成一份Independence控制器字典加总列表里面
                    dict = '{\"Independence_sys\":[' + grp_str + '\"' + cur[0] + '\"' + ']}'
                    dict = json.loads(dict)
                    Independence_controller.append(dict)
                    # Independence_controller.append()

                # 添加字典记录独立控制器系统
                if not cmds.objExists('MainSystem_Grp.Independence_controller_sys'):
                    cmds.addAttr('MainSystem_Grp', ln='Independence_controller_sys', dt='string')
                    cmds.setAttr('MainSystem_Grp.Independence_controller_sys', e=1, keyable=True)
                cmds.setAttr('MainSystem_Grp.Independence_controller_sys', str(Independence_controller), type='string')

                #########################################
                # 为需要添加额外骨骼进行曲面附着，且添加独立控制器
                #########################################
                # print(aaaaa)
                # 开始为蒙皮骨骼创建fk控制器
                if not cmds.objExists('FK_controller_Grp'):
                    cmds.group(em=1,n='FK_controller_Grp',p='MainSystem_Grp')
                FK_controller = []
                for j in skin_joint:
                    if cmds.objExists(j + '_FKCurve'):
                        cur = [(j + '_FKCurve')]
                        cmds.select(cur)
                        reduction_curve_dict_list.remove(cur[0])
                    else:
                        cur = cmds.circle(c=(0, 0, 0), ch=0, d=1, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(1, 0, 0),n=(j + '_FKCurve'))
                        self.modify_vontroller_shape('SoftSelectionSize', 2, 2, 2)
                        self.modify_vontroller_shape('scale', 1.2, 1.2, 1.2)
                        self.curve.change_curve_color('Index', cur, [0, 0, 0], 18)
                    if (j + '_FKCurve') in need_delete_curve:
                        need_delete_curve.remove((j + '_FKCurve'))
                    grp_str = ''
                    ls_grp = []
                    for g in range(0, controller_group_num):
                        if cmds.objExists((j + '_FKGrp' + str(g + 1))):
                            two_grp = (j + '_FKGrp' + str(g + 1))
                            for attribute,num in zip(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'],[0,0,0,0,0,0,1,1,1,1]):
                                cmds.setAttr(two_grp + '.' + attribute, num)
                        else:
                            two_grp = cmds.group(n=(j + '_FKGrp' + str(g + 1)), em=1)
                        if ls_grp:
                            cmds.parent(two_grp,ls_grp)
                        ls_grp = two_grp
                        grp_str = grp_str + '\"' + (j + '_FKGrp' + str(g + 1)) + '\"' + ','

                    cmds.delete(cmds.parentConstraint(j, (j + '_FKGrp1'), w=1))

                    cmds.parent(cur, (j + '_FKGrp' + str(controller_group_num)))
                    cmds.delete(cmds.parentConstraint(j, cur, w=1))

                    cur_str = (j + '_FKCurve')
                    # 生成一份FK控制器字典加总列表里面
                    dict = '{\"FK_sys\":[' + grp_str + '\"' + cur_str + '\"' + ']}'
                    dict = json.loads(dict)
                    FK_controller.append(dict)

                # 父化
                for j in skin_joint:
                    parent = cmds.listRelatives(j, p=1)
                    joint_parent = cmds.ls(parent, typ='joint')
                    if not joint_parent:
                        for i in range(0, len(all)):
                            parent = cmds.listRelatives(p=1)
                            if parent != 'SkinRootJoint_Grp':
                                joint_parent = cmds.ls(parent, typ='joint')
                                if joint_parent:
                                    cmds.parent((j + '_FKGrp1'), (joint_parent[0] + '_FKCurve'))
                            else:
                                break
                    else:
                        cmds.parent((j + '_FKGrp1'), (joint_parent[0] + '_FKCurve'))

                # FK约束独立控制器
                for j in skin_joint:
                    parentConstraint = cmds.parentConstraint((j + '_FKCurve'), (j + '_IndependenceGrp1'), mo=1, weight=1)
                    cmds.parent(parentConstraint,'AllConstraintSystem_Grp')
                    scaleConstraint = cmds.scaleConstraint((j + '_FKCurve'), (j+'_IndependenceGrp1'),mo=1, weight=1)
                    cmds.parent(scaleConstraint,'AllConstraintSystem_Grp')

                cmds.parent((skin_joint[0] + '_FKGrp1'), 'FK_controller_Grp')
                # 添加字典记录独立控制器系统
                if not cmds.objExists('MainSystem_Grp.FK_controller_sys'):
                    cmds.addAttr('MainSystem_Grp', ln='FK_controller_sys', dt='string')
                    cmds.setAttr('MainSystem_Grp.FK_controller_sys', e=1, keyable=True)
                cmds.setAttr('MainSystem_Grp.FK_controller_sys', str(FK_controller), type='string')
                # 开始给IK部分添加ik控制器
                if not cmds.objExists('IK_controller_Grp'):
                    cmds.group(em=1,n='IK_controller_Grp',p='MainSystem_Grp')
                IK_controller = []
                # 查询需要添加ik的骨骼
                for j in range(0, len(skin_joint)):
                    pass
                # 开始为fk添加绳子控制器



                ###########################
                # 开始还原自定义部分
                ###########################

                # 删除多余形状样条
                # if reduction_curve_dict_list:
                #     cmds.delete(reduction_curve_dict_list)
                if need_delete_curve:
                    cmds.delete(need_delete_curve)
                for j in skin_joint:
                    parentConstraint = cmds.parentConstraint((j + '_IndependenceCurve'), j, w=1)
                    cmds.parent(parentConstraint, 'AllConstraintSystem_Grp')
                    scaleConstraint = cmds.scaleConstraint((j + '_IndependenceCurve'), j, mo=1, weight=1)
                    cmds.parent(scaleConstraint, 'AllConstraintSystem_Grp')
                self.reset_controllers()

                if all_connect_node:
                    self.return_constraint([],all_connect_node, Constraint)
                if reduction_dict_list:
                    for reduction_dict in reduction_dict_list:
                        parent = reduction_dict['parent']
                        our = reduction_dict['our']
                        child = reduction_dict['child']
                        if cmds.objExists(parent[0]):
                            # p = cmds.listRelatives(our, parent=True)
                            # if p:
                            # parent = [x for x in parent if x not in p]
                            if our and parent[0] and cmds.objExists(our) and cmds.objExists(parent[0]):
                                cmds.parent(our, parent[0])
                        if child:
                            # c = cmds.listRelatives(our, children=True)
                            # if c:
                            # child = [x for x in child if x not in c]
                            for c in child:
                                if c and our and cmds.objExists(c) and cmds.objExists(our):
                                    cmds.parent(c, our)
                self.other_library.switch_skin_model_hand_influence_state()
            else:
                cmds.error('缺少All_ControllerSystem_Grp组和BaseRoot_Grp组，请导入base.ma。')
            sel = cmds.ls('All_ControllerSystem_Grp', uid=1)
            cmds.setAttr('SkinRootJoint_Grp.visibility', 1)
            print('生成完成。(目前只支持保持父对象约束和缩放约束，还有额外打组)')
        except:
            cmds.warning('生成失败，请检查参数后撤回。(目前只支持保持父对象约束和缩放约束，还有额外打组)')

        cmds.undoInfo(cck=1)

    # 按属性创建蒙皮骨骼
    def create_controllers_system_copy_joint_part(self,other_suffix):
        need_delete_joint_grp = cmds.group(em=1,n='rebuild_need_delete_joint')
        # 获取上次生成的骨骼
        cmds.select('SkinRootJoint_Grp')
        mel.eval('SelectHierarchy')
        rebuild = cmds.ls(sl=1,type='joint')
        cmds.parent(rebuild,need_delete_joint_grp)
        # 获取所有基础骨骼
        cmds.select('SkinRootJoint_Grp')
        mel.eval('SelectHierarchy')
        all = cmds.ls(sl=1)
        cmds.select('BaseRoot_Grp')
        mel.eval('SelectHierarchy')
        base_joint = cmds.ls(sl=1,type='joint')
        base_right_side_joint = []
        base_middle_joint = []
        R_Link_M_joint = []
        # 对骨骼进行分类，在中间的一类，右边的一类，左边的一类
        # 先筛选出在中间且父集没有左右两边的骨骼
        middle_joint = []
        for j in base_joint:
            cmds.select(cl=1)
            translocation = cmds.xform(j, q=1, ws=1, t=1)
            if -0.0000001<translocation[0] and translocation[0]<0.0000001:#如果对象在中间则判断其父对象是否在中间
                parent = cmds.listRelatives(j, p=1)
                translocation = cmds.xform(parent, q=1, ws=1, t=1)
                if -0.0000001<translocation[0] and translocation[0]<0.0000001:#如果父对象还在中间则看看是否是顶组
                    while parent[0] != 'BaseRoot_Grp':#一直循环查询父对象，有一个不在中间就停，直到查到顶组
                        parent = cmds.listRelatives(parent[0], p=1)
                        translocation = cmds.xform(parent, q=1, ws=1, t=1)
                        if translocation[0]<-0.0000001 or translocation[0]>0.0000001:
                            break
                    if parent[0] == 'BaseRoot_Grp':#只要没有查到顶组证明是骨骼不在中心的骨骼链上，那就不用加进中间骨骼列表
                        middle_joint.append(j)
                else:
                    break
        # print(middle_joint)
        # print(aaaaaaa)
        # 查询确定是中间骨骼的的子骨骼
        base_right_side_joint = []
        base_left_side_joint = []
        for j in middle_joint:
            child = cmds.listRelatives(j, c=1,type='joint')
            if child:
                for c in child:
                    translocation = cmds.xform(c, q=1, ws=1, t=1)
                    if translocation[0] >= 0.0000001:
                        base_left_side_joint.append(c)
                    if translocation[0] <= -0.0000001:
                        base_right_side_joint.append(c)
        # 建立左右骨骼对应的所有子集骨骼的字典
        side_dict = []
        for j in base_right_side_joint+base_left_side_joint:
            cmds.select(j)
            mel.eval('SelectHierarchy')
            child_joint = cmds.ls(sl=1, typ='joint')
            child_joint.remove(j)
            dict = {'parent':j,'child':child_joint}
            side_dict.append(dict)
        # 开始生成中间骨骼
        # print(side_dict)
        # print(middle_joint)
        for j in middle_joint:
            suffix = '_M'
            cmds.select(cl=1)
            if cmds.objExists((j + other_suffix + suffix)):
                cmds.select((j + other_suffix + suffix))
                joint = cmds.ls(sl=1)
            else:
                joint = cmds.joint(p=(0, 0, 0), n=(j + other_suffix + suffix))
            # print(joint)
            cmds.delete(cmds.parentConstraint(j, joint, w=1))
            # 进行子化
            parent = cmds.listRelatives(j, p=1)
            if parent[0] == 'BaseRoot_Grp':
                cmds.parent(joint, 'SkinRootJoint_Grp')
                continue
            joint_parent = cmds.ls(parent, typ='joint')
            while not joint_parent: #当joint_parent为空时，证明上层不是骨骼，继续查找上层的上层，直到查到骨骼
                parent = cmds.listRelatives(parent, p=1)
                joint_parent = cmds.ls(parent, typ='joint')
                if parent[0] == 'BaseRoot_Grp': #如果查到顶组也没有那就退出循环
                    break
            if joint_parent:
                cmds.parent(joint, (joint_parent[0] + other_suffix + suffix))

        # 开始按字典生成侧边骨骼
        for sd in side_dict:
            parent = sd['parent']
            child = sd['child']
            #获取完对象开始按顺序创建和父化
            translocation = cmds.xform(parent, q=1, ws=1, t=1)
            if translocation[0] < 0:
                suffix = '_R'
            else:
                suffix = '_L'
            #开始创建骨骼并且父化
            cmds.select(cl=1)
            if cmds.objExists((parent + other_suffix + suffix)):
                cmds.select((parent + other_suffix + suffix))
                joint = cmds.ls(sl=1)
            else:
                joint = cmds.joint(p=(0, 0, 0), n=(parent + other_suffix + suffix))
            cmds.delete(cmds.parentConstraint(parent, joint, w=1))
            middle_joint = cmds.listRelatives(parent, p=1)
            cmds.parent(joint, (middle_joint[0] + other_suffix + '_M'))
            # 进行子化
            for c in child:
                cmds.select(cl=1)
                if cmds.objExists((c + other_suffix + suffix)):
                    cmds.select((c + other_suffix + suffix))
                    joint = cmds.ls(sl=1)
                else:
                    joint = cmds.joint(p=(0, 0, 0), n=(c + other_suffix + suffix))
                cmds.delete(cmds.parentConstraint(c, joint, w=1))
                parent = cmds.listRelatives(c, p=1)
                joint_parent = cmds.ls(parent, typ='joint')
                while not joint_parent:  # 当joint_parent为空时，证明上层不是骨骼，继续查找上层的上层，直到查到骨骼
                    parent = cmds.listRelatives(parent, p=1)
                    joint_parent = cmds.ls(parent, typ='joint')
                    if parent[0] == 'SkinRootJoint_Grp':  # 如果查到顶组也没有那就退出循环(防止无限循环，逻辑上理论这句无效)
                        break
                cmds.parent(joint, (joint_parent[0] + other_suffix + suffix))
        # 查询所有不镜像骨骼，且把对应的生成的骨骼p出去并生成列表
        parent_list = []
        child_list = []
        base_child = []
        all_no_mirror_joint = cmds.ls('*.NoMirror')
        for j in all_no_mirror_joint:
            j = j.split('.')[0]
            j_l = cmds.ls(j + '_L')
            j_r = cmds.ls(j + '_R')
            parent = []
            jon = []
            if j_l:
                jon = j_l
                parent = cmds.listRelatives(j_l, p=1)
            if j_r:
                jon = j_r
                parent = cmds.listRelatives(j_r, p=1)
            if parent:
                base_child.append(j)
                child_list.append(jon)
                parent_list.append(parent[0])
                cmds.parent(jon,w=1)

        # 按对称部分对称
        need_mirror_joint = list(set(base_child) & set(base_right_side_joint + base_left_side_joint))
        need_mirror_joint = list(set(need_mirror_joint) ^ set(base_right_side_joint + base_left_side_joint))#移除左右两遍骨骼种和有不镜像属性的骨骼
        # print(need_mirror_joint)
        for j in need_mirror_joint:
            translocation = cmds.xform(j, q=1, ws=1, t=1)
            soure = '_R'
            tager = 'L'
            if translocation[0] > 0:
                soure = '_L'
                tager = 'R'
            joint = cmds.mirrorJoint(j + other_suffix + soure, mirrorBehavior=1, mirrorYZ=1)
            joint = joint[::-1]

            # cmds.parent(joint,w=1)
            for i in joint:
                if cmds.objExists((i[:-2] + tager)):
                    # print((i[:-2] + tager))
                    cmds.delete(cmds.parentConstraint(i, i[:-2] + tager))
                    parent = cmds.listRelatives(i, p=1)
                    child = cmds.listRelatives(i, c=1)
                    cmds.parent((i[:-2] + tager), parent)
                    if child:
                        cmds.parent(child, (i[:-2] + tager))
                    cmds.delete(i)
                else:
                    cmds.rename(i, (i[:-2] + tager))
        # 按列表p回去
        for p, c in zip(parent_list, child_list):
            cmds.parent(c, p)

        # 清理p出去的骨骼
        cmds.delete(need_delete_joint_grp)

        ###########################################################################################################
        '''for j in base_joint:
            cmds.select(cl=1)
            translocation = cmds.xform(j, q=1, ws=1, t=1)
            suffix = '_M'
            if translocation[0] < 0:
                base_right_side_joint.append(j)
                suffix = '_R'
            if translocation[0] > 0:
                base_right_side_joint.append(j)
                suffix = '_L'
            joint = cmds.joint(p=(0, 0, 0), n=(j + other_suffix + suffix))
            cmds.delete(cmds.parentConstraint(j, joint, w=1))
        for j in base_right_side_joint:
            parent = cmds.listRelatives(j, p=1)
            joint_parent = cmds.ls(parent, typ='joint')
            if not joint_parent:
                for i in range(0, len(all)):
                    parent = cmds.listRelatives(p=1)
                    joint_parent = cmds.ls(parent, typ='joint')
                    if joint_parent:
                        break
            translocation = cmds.xform(joint_parent, q=1, ws=1, t=1)
            if translocation[0] == 0:
                R_Link_M_joint.append(j)
        # 进行父化
        cmds.parent((base_joint[0] + other_suffix + '_M'), 'SkinRootJoint_Grp')
        for i in range(1, len(base_joint)):
            parent = cmds.listRelatives(base_joint[i], p=1)
            joint_parent = cmds.ls(parent, typ='joint')
            if parent == all[0]:
                continue
            if not joint_parent:
                for j in range(0, len(all)):
                    parent = cmds.listRelatives(p=1)
                    joint_parent = cmds.ls(parent, typ='joint')
                    if parent == all[0]:
                        break
                    if joint_parent:
                        break
            base_translocation = cmds.xform(base_joint[i], q=1, ws=1, t=1)
            suffix_s = '_M'
            if base_translocation[0] < 0:
                suffix_s = '_R'
            if base_translocation[0] > 0:
                suffix_s = '_L'
            parent_translocation = cmds.xform(joint_parent, q=1, ws=1, t=1)
            suffix_t = '_M'
            if parent_translocation[0] < 0:
                suffix_t = '_R'
            if parent_translocation[0] > 0:
                suffix_t = '_L'
            cmds.parent((base_joint[i] + other_suffix + suffix_s), (joint_parent[0]+ other_suffix + suffix_t))
        # 选择对应骨骼镜像
        for j in R_Link_M_joint:
            soure = '_R'
            tager = 'L'
            if j[:-1]=='L':
                soure = '_L'
                tager = 'R'
            joint = cmds.mirrorJoint(j + other_suffix + soure, mirrorBehavior=1, mirrorYZ=1)
            for i in joint:
                cmds.rename(i, (i[:-2] + tager))
        # 按属性删除蒙皮骨骼
        for i in range(0, len(base_joint)):
            if cmds.objExists(base_joint[i]+'.NoMirror'):
                translocation = cmds.xform(base_joint[i], q=1, ws=1, t=1)
                if translocation[0] < 0:
                    cmds.delete(base_joint[i] + other_suffix + '_L')
                if translocation[0] > 0:
                    cmds.delete(base_joint[i] + other_suffix + '_R')'''
        #######################################################################################################
        return base_joint,all
    # 按骨骼添加属性(未用)
    def add_addattr_system(self, base_joint, all):
        for i in range(0, len(base_joint)):
            cmds.addAttr(base_joint[i], ln='IK',en=(base_joint[i] + ':IK'))
            cmds.setAttr((base_joint[i] + ':IK'), e=1, keyable=1)
            cmds.addAttr(base_joint[i], ln='FK',en=(base_joint[i] + ':FK'))

    # 添加属性系统
    def delete_addattr_system(self, attribute):
        cmds.undoInfo(ock=1)
        sel = cmds.ls(sl=1)

        if attribute == 'IK':
            if not cmds.objExists(sel[0] + '.IK'):
                if len(sel) > 2:
                    cmds.addAttr(sel[0], ln='IK',en=(sel[0]+':'+sel[1]+':'+sel[2]+':'), at='enum')
                    cmds.setAttr((sel[0]+'.IK'), e=1, keyable=True)
                    cmds.select(sel[0])
                else:
                    cmds.warning('请加载三个骨骼。')
            else:
                cmds.deleteAttr(sel[0], at='IK')
        if attribute == 'NoMirror':
            add = 0
            if not cmds.objExists(sel[0] + '.NoMirror'):
                add = 1
            for s in sel:
                if cmds.objExists(s + '.NoMirror'):
                    if add == 0:
                        cmds.deleteAttr(s, at='NoMirror')
                else:
                    if add == 1:
                        cmds.addAttr(s, ln='NoMirror', at='bool')
                        cmds.setAttr((s + '.NoMirror'), e=1, keyable=True)
                        cmds.setAttr((s + '.NoMirror'), 1)

        if attribute == 'aim':
            if not cmds.objExists(sel[0] + '.aim'):
                cmds.addAttr(sel[0], ln='aim', en='z:-z:y:-y:x:-x:', at='enum')
                cmds.setAttr((sel[0] + '.aim'), e=1, keyable=True)
            else:
                cmds.deleteAttr(sel[0], at='aim')
        if attribute == 'twist':
            if not cmds.objExists(sel[0] + '.twist'):
                if len(sel) > 1:
                    cmds.addAttr(sel[0], ln='twist', en=(sel[0] + ':' + sel[1] + ':'), at='enum')
                    cmds.setAttr((sel[0] + '.twist'), e=1, keyable=True)
                    cmds.addAttr(sel[0], ln='twist_joint_num', dv=2,at='long')
                    cmds.setAttr((sel[0] + '.twist_joint_num'), e=1, keyable=True)
                    cmds.select(sel[0])
                else:
                    cmds.warning('请选择两个骨骼。')
            else:
                cmds.deleteAttr(sel[0], at='twist')
                cmds.deleteAttr(sel[0], at='twist_joint_num')
        if attribute == 'global':
            if not cmds.objExists(sel[0] + '.global'):
                cmds.addAttr(sel[0], ln='global', at='bool')
                cmds.setAttr((sel[0] + '.global'), e=1, keyable=True)
                cmds.setAttr((sel[0] + '.global'), 1)
            else:
                cmds.deleteAttr(sel[0], at='global')
        if attribute == 'rope':
            if not cmds.objExists(sel[0] + '.rope'):
                if len(sel) > 2:
                    text = ''
                    for i in range(len(sel)):
                        text += sel[i] + ':'
                    cmds.addAttr(sel[0], ln='rope', en=text, at='enum')
                    cmds.setAttr((sel[0] + '.rope'), e=1, keyable=True)
                    cmds.addAttr(sel[0], ln='rope_controllers_num', min=6, dv=6, at='long')
                    cmds.setAttr((sel[0] + '.rope_controllers_num'), e=1, keyable=True)
                    cmds.select(sel[0])
                else:
                    cmds.warning('请选择三个骨骼以上。')
            else:
                cmds.deleteAttr(sel[0], at='rope')
                cmds.deleteAttr(sel[0], at='rope_controllers_num')
        cmds.undoInfo(cck=1)

    # 添加选定位数到Notes
    def ZKM_SetNumToNotes(self, sel, factorial):
        notes = ''
        if not sel.hasAttr('notes'):
            for i in range(0, factorial):
                j = str(random.randrange(0, 10, 1))
                notes = notes + j
            sel.addAttr('notes', type='string')
            sel.attr('notes').set(notes)
            note = []
            note.append(notes)
            return note
        else:
            notes = cmds.getAttr(sel + '.notes')
            return notes
        # print (cmds.getAttr(cmds.ls(sl=1)[0] + '.notes'))

    # 选择特定字典的物体名称
    def ZKM_ReturnNotesToModel(self, range, Dictionary, DictionaryProperties, list):
        DictionaryNotes = Dictionary[DictionaryProperties][list]
        Have = 0
        for r in range:
            if cmds.objExists(r):
                if r.hasAttr('notes'):
                    SelNotes = ''
                    SelNotes = SelNotes + (cmds.getAttr(r + '.notes'))
                    SelNotes = SelNotes.encode('utf-8')  # 字符通用码转为字符串
                    if SelNotes == DictionaryNotes:
                        cmds.select(r)
                        Have = 1
                        break
        if Have == 0:
            cmds.select(cl=1)

    # 控制器归零
    def ZKM_ControllerHoming(self):
        cmds.select('ZKM_FK_AllController')
        mel.eval('SelectHierarchy;')
        CurveShape = cmds.ls(sl=1, type='nurbsCurve')
        for Shape in CurveShape:
            parent = cmds.listRelatives(Shape, p=1)
            for t in ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ']:
                try:
                    cmds.setAttr(parent[0] + t, 0)
                except:
                    pass
            for t in ['.scaleX', '.scaleY', '.scaleZ', '.visibility']:
                try:
                    cmds.setAttr(parent[0] + t, 1)
                except:
                    pass
        cmds.select(cl=1)

    # 查询属性是否锁定，解锁并返回列表
    def unLokeAttribute(self, sel):
        re = []
        for t in ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX', '.scaleY',
                  '.scaleZ', '.visibility']:
            if cmds.getAttr(sel + t, lock=1):
                cmds.setAttr(sel + t, lock=0)
                re.append(sel + t)
        return re

    # 切换控制器
    def ZKM_ChuangJianFKSwitch(self, ExtractConstraints):
        self.ZKM_ControllerHoming()
        Now = cmds.parentConstraint('ZKM_FK_Root', q=1, tl=1)
        cmds.select('ZKM_FK_Root')
        mel.eval('SelectHierarchy;')
        joint = cmds.ls(sl=1, type='joint')
        cmds.select(joint)
        if Now:
            cmds.setAttr("ZKM_FK_AllController.visibility", 0)
            for j in joint:
                parentConstraint = []
                scaleConstraint = []
                try:
                    parentConstraint = cmds.parentConstraint(j, wal=1)
                    scaleConstraint = cmds.scaleConstraint(j, wal=1)
                except:
                    pass
                if parentConstraint:
                    cmds.delete(parentConstraint)
                if scaleConstraint:
                    cmds.delete(scaleConstraint)
            cmds.select(cl=1)
        else:
            cmds.setAttr("ZKM_FK_AllController.visibility", 1)
            # 进行约束
            if ExtractConstraints == 1:
                cmds.select(cl=1)
                if not cmds.objExists('ZKM_AllControllerConstraint_Grp'):
                    cmds.rename(mel.eval('doGroup 0 1 1;'), 'ZKM_AllControllerConstraint_Grp')
                    cmds.parent('ZKM_AllControllerConstraint_Grp', 'ZKM_AllFK_TopGrp')
            for i in range(0, len(joint)):
                if cmds.objExists(joint[i] + "_C*"):
                    cmds.parentConstraint((joint[i] + "_C*"), joint[i])
                    cmds.scaleConstraint((joint[i] + "_C*"), joint[i])
                    if ExtractConstraints == 1:
                        cmds.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"),
                                  'ZKM_AllControllerConstraint_Grp')
            cmds.select(cl=1)

    '''    # 检查并清理已经生成的部分
    def ZKM_ChuangJianFK_CheckClean(self,RemoveJoint):

        return joint'''

    # 生成控制器
    def ZKM_ChuangJianFK(self, Name, C_GrpNum, Suffix, RemoveJoint, Colour):
        if cmds.objExists('ZKM_FK_AllController'):
            cmds.setAttr("ZKM_FK_AllController.visibility", 1)
        cmds.select(cl=1)
        cmds.select('ZKM_FK_Root')
        mel.eval('SelectHierarchy;')
        joint = cmds.ls(typ='joint', sl=1)
        if RemoveJoint == True:
            for j in joint:
                q = cmds.listRelatives(j, c=1)
                if len(q) == 0:
                    joint.remove(j)
        # 查询notes是否重复
        '''AllJointNotes = []
        for j in joint:
            sel_notes = cmds.getAttr(j + '.notes')
            AllJointNotes.append(sel_notes)
        AllJointNotesWeightlessnessReduction = set(AllJointNotes)
        AllJointNotes.remove(AllJointNotesWeightlessnessReduction)
        cmds.select(cl=1)
        for j in joint:
            sel_notes = cmds.getAttr(j + '.notes')
            for Notes in AllJointNotes:
                if sel_notes == Notes:
                    cmds.select(j, add=1)'''
        # 清除不需要创建控制器的
        NoCreate = []
        for j in joint:
            if cmds.objExists(j + '.NotGenerate'):
                AttributeName = cmds.getAttr(j + '.NotGenerate')
                Dictionary = {}
                if AttributeName == 0:  # 字符通用码
                    p = cmds.listRelatives(j, p=1)
                    c = cmds.listRelatives(j, c=1)
                    cmds.parent(c, p[0])
                    cmds.parent(j, w=1)
                    Dictionary = {'parent': p, 'self': j, 'child': c}
                    joint.remove(j)
                if AttributeName == 1:  # 字符通用码
                    cmds.select(j)
                    mel.eval('SelectHierarchy;')
                    RemoveJoint = cmds.ls(typ='joint', sl=1)
                    for r in RemoveJoint:
                        try:
                            joint.remove(r)
                        except:
                            pass
                    p = cmds.listRelatives(j, p=1)
                    cmds.parent(j, w=1)
                    Dictionary = {'parent': p, 'self': j, 'child': []}
                NoCreate.append(Dictionary)
        '''查询其他系统打的组并且转移'''

        # 建立独立控制器
        # 建立总控制器组
        cmds.select(cl=1)
        # 创建总字典
        AllDictionary = []
        # 查询是否有创建过，覆盖字典
        HaveAllDictionary = cmds.objExists('ZKM_FK_Root_Grp.notes')
        if HaveAllDictionary and cmds.objExists('ZKM_FK_AllController'):
            # 清理骨骼约束
            cmds.select('ZKM_FK_Root')
            mel.eval('SelectHierarchy;')
            cmds.mel.DeleteConstraints()
            # 修复骨骼note
            Jnt = cmds.ls(typ='joint', sl=1)
            for J in Jnt:
                self.ZKM_SetNumToNotes(J, 32)
            # 将上次生成的通用字符数据转换成字典列表
            HaveAllDictionary = cmds.getAttr('ZKM_FK_Root_Grp.notes')
            HaveAllDictionary = HaveAllDictionary.encode('utf-8')  # 字符通用码转为字符串
            HaveAllDictionary = HaveAllDictionary.split('\n')
            del HaveAllDictionary[-1:]
            for h in range(0, len(HaveAllDictionary)):  # 把字符串列表转换成字典列表
                StrDictionary = eval(HaveAllDictionary[h])
                HaveAllDictionary[h] = StrDictionary
            # 修复所有组的note
            cmds.select('ZKM_FK_Root_G1*')
            RootGrp = cmds.ls(sl=1)
            OldSuffix = RootGrp[0][14:]
            mel.eval('SelectHierarchy;')
            Transform = cmds.ls(typ='transform', sl=1)
            for G in Transform:
                self.ZKM_SetNumToNotes(G, 32)
            # 查询上次生成的样条是否缺失，缺失的话进行补充,没有缺失就进行改名，改成对应骨骼名称的上次生成的结构
            LastGrpNum = HaveAllDictionary[0].get('Grp')  # 获取上次生成打的组
            for Dictionary in HaveAllDictionary:
                self.ZKM_ReturnNotesToModel(joint, Dictionary, 'joint', 0)
                J = cmds.ls(sl=1)
                C_Num = str(Dictionary.get('Curve'))
                self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                C = cmds.ls(sl=1)
                if J:
                    if not C:
                        # 建立基础控制器并改名
                        cmds.rename(self.curve.create_curve(
                            (root_path + '\MayaCommon\CurveShapeWithPicture'), Name), J[0] + "_C" + Suffix)
                        nurbs = cmds.ls(sl=1)
                        self.modify_vontroller_shape('SoftSelectionSize', 0, 0, 0)
                        if not nurbs[0].hasAttr('notes'):
                            nurbs[0].addAttr('notes', type='string')
                        nurbs[0].attr('notes').set(C_Num)  # 按原样修复样条note
                        self.curve.change_curve_color('RGB', nurbs, Colour, 0)
                        cmds.parent(nurbs[0], 'ZKM_FK_Root_C' + OldSuffix)
                        # 建立旧样条组，并将旧32位绝对数还原到修复组中
                        for n in range(0, len(LastGrpNum)):
                            if cmds.objExists(J[0] + "_G" + str((len(LastGrpNum) - n)) + OldSuffix):
                                cmds.select((J[0] + "_G" + str((len(LastGrpNum) - n)) + OldSuffix))
                                TopGrp = cmds.ls(sl=1)
                            else:
                                if n == 0:
                                    cmds.select(nurbs[0])
                                else:
                                    cmds.select(J[0] + "_G" + str((len(LastGrpNum) - n + 1)) + OldSuffix)
                                mel.eval('doGroup 0 1 1;')
                                mel.eval('rename '+(J[0] + "_G" + str((len(LastGrpNum) - n)) + OldSuffix + ';'))
                                TopGrp = cmds.ls(sl=1)
                            if not TopGrp[0].hasAttr('notes'):
                                TopGrp[0].addAttr('notes', type='string')
                            TopGrp[0].attr('notes').set(Dictionary['Grp'][n])  # 按原样修复样条note
                        for n in range(0, len(LastGrpNum) - 1):
                            cmds.parent((J[0] + "_G" + str((len(LastGrpNum) - n)) + OldSuffix),
                                      (J[0] + "_G" + str((len(LastGrpNum) - 1 - n)) + OldSuffix))
                        cmds.parent(nurbs[0], (J[0] + "_G" + str(len(LastGrpNum)) + OldSuffix))
                    else:
                        G_Num = Dictionary.get('Grp')
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                        mel.eval('rename '+ (J[0] + "_C" + OldSuffix) + ';')  # 修复所有存在样条的名称
                        for g in range(0, len(G_Num)):
                            self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Grp', g)
                            G = cmds.ls(sl=1)
                            if not G[0]:
                                cmds.select(J[0] + '_C' + OldSuffix)
                                mel.eval('doGroup 0 1 1;')
                                mel.eval('rename '+ (J[0] + "_G" + str(len(G_Num) - g) + OldSuffix + ';'))
                                TopGrp = cmds.ls(sl=1)
                                if not TopGrp[0].hasAttr('notes'):
                                    TopGrp[0].addAttr('notes', type='string')
                                TopGrp[0].attr('notes').set(Dictionary['Grp'][g])  # 按原样修复样条note
                            else:
                                mel.eval('rename ' + (J[0] + "_G" + str(len(G_Num) - g) + OldSuffix + ';'))  # 修复所有存在样条组的名称
                else:
                    self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                    Cur = cmds.ls(sl=1)
                    AllDelete = []
                    if Cur:
                        Transform.remove(Cur[0])
                        AllDelete.append(Cur)
                    G_Num = Dictionary.get('Grp')
                    for g in range(0, len(G_Num)):
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Grp', g)
                        Grp = cmds.ls(sl=1)
                        if Grp:
                            Transform.remove(Grp[0])
                            AllDelete.append(Grp[0])
                    for D in AllDelete:
                        Parent = cmds.listRelatives(D, p=1)
                        subset = cmds.listRelatives(D, c=1, type='transform')
                        for s in subset:
                            cmds.parent(s, Parent[0])
                        cmds.delete(D)
                    # 此时已经完成了现存原骨骼所有组的新名称旧后缀还原###################################

            # 假如要生成的组数比原本的组少则进行解组
            if C_GrpNum < len(LastGrpNum):
                WantingGrpNum = len(LastGrpNum) - C_GrpNum
                # 查询需解组的组是否存在
                for Dictionary in HaveAllDictionary:
                    for l in range(0, WantingGrpNum):
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Grp', l)
                        sel = cmds.ls(sl=1)
                        if sel:
                            Transform.remove(sel[0])
                            cmds.mel.ungroup()

            # 假如要生成的组数比原本的组多则进行加组
            if C_GrpNum > len(LastGrpNum):
                WantingGrpNum = C_GrpNum - len(LastGrpNum)
                for Dictionary in HaveAllDictionary:
                    for l in range(0, WantingGrpNum):
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                        C = cmds.ls(sl=1)
                        mel.eval('doGroup 0 1 1;')
                        mel.eval('rename ' + (str(C[0][:-2]) + "_G" + str((len(LastGrpNum) + 1 + l)) + OldSuffix) + ';')
                        TopGrp = cmds.ls(sl=1)
                        self.ZKM_SetNumToNotes(TopGrp[0], 32)

            # 修正后缀
            for T in Transform:
                if cmds.objExists(T):
                    if len(OldSuffix) == 0:
                        cmds.rename(T, T + Suffix)
                    if T[-1 * len(OldSuffix):] == OldSuffix:
                        cmds.rename(T, T[:-1 * len(OldSuffix)] + Suffix)

            # 判断是否有添加的骨骼，进行正常生成控制器
            for J in joint:
                if not cmds.objExists(J + "_C" + Suffix):
                    # 建立控制器
                    cmds.rename(self.curve.create_curve(
                        (root_path + '\MayaCommon\CurveShapeWithPicture'), Name), J + "_C" + Suffix)
                    nurbs = cmds.ls(sl=1)
                    self.modify_vontroller_shape('SoftSelectionSize', 0, 0, 0)
                    self.curve.change_curve_color('RGB', nurbs, Colour, 0)
                    self.ZKM_SetNumToNotes(nurbs[0], 32)
                    for j in range(0, C_GrpNum):
                        mel.eval('doGroup 0 1 1;')
                        # 建立样条组
                        mel.eval('rename ' + (J + "_G" + str((C_GrpNum - j)) + Suffix) + ';')
                        Grp = cmds.ls(sl=1)
                        self.ZKM_SetNumToNotes(Grp[0], 32)
            cmds.select(cl=1)
            for J in joint:
                cmds.select(J + "_G1" + Suffix)
                TopGrp = cmds.ls(sl=1)
                cmds.parent(TopGrp[0], 'ZKM_FK_AllController')
            # 创建新字典AllDictionary
            for J in joint:
                J_NumList = []
                J_Num = cmds.getAttr(J + '.notes')
                J_Num = J_Num.encode('utf-8')
                J_NumList.append(J_Num)
                C_NumList = []
                C_Num = cmds.getAttr(J + "_C" + Suffix + '.notes')
                C_Num = C_Num.encode('utf-8')
                C_NumList.append(C_Num)
                G_Num = []
                for i in range(0, C_GrpNum):
                    GrpNum = cmds.getAttr((J + "_G" + str((C_GrpNum - i)) + Suffix + '.notes'))
                    GrpNum = GrpNum.encode('utf-8')
                    G_Num.append(GrpNum)
                Dictionary = {'joint': J_NumList, 'Curve': C_NumList, 'Grp': G_Num}
                AllDictionary.append(Dictionary)
        else:
            cmds.select(cl=1)
            cmds.group(n='ZKM_FK_AllController')
            cmds.parent('ZKM_FK_AllController', 'ZKM_AllFK_TopGrp')
            for J in joint:
                J_nume = []
                # 给骨骼添加32位随机数
                if not J.hasAttr('notes'):
                    self.ZKM_SetNumToNotes(J, 32)
                J_nume.append(cmds.getAttr(J + '.notes').encode('utf-8'))
                # 建立基础控制器并改名
                cmds.rename(self.curve.create_curve(
                    (root_path + '\MayaCommon\CurveShapeWithPicture'), Name), str(J) + "_C" + Suffix)
                nurbs = cmds.ls(sl=1)
                self.modify_vontroller_shape('SoftSelectionSize', 0, 0, 0)
                self.curve.change_curve_color('RGB', nurbs, Colour, 0)
                # 给曲线添加32位随机数
                if not nurbs[0].hasAttr('notes'):
                    self.ZKM_SetNumToNotes(nurbs[0], 32)
                nurbs_nume = []
                nurbs_nume.append(cmds.getAttr(nurbs[0] + '.notes').encode('utf-8'))
                TopGrp_Num = []
                # 循环创建控制器组，且给添加32位随机数
                for j in range(0, C_GrpNum):
                    mel.eval('doGroup 0 1 1;')
                    # 建立样条组
                    mel.eval('rename ' + (str(J) + "_G" + str((C_GrpNum - j)) + Suffix) + ';')
                    Grp = cmds.ls(sl=1)
                    if not Grp[0].hasAttr('notes'):
                        self.ZKM_SetNumToNotes(Grp[0], 32)
                    Grp_Num = cmds.getAttr(Grp[0] + '.notes')
                    TopGrp_Num.append(Grp_Num.encode('utf-8'))
                cmds.parent((str(J) + "_G1" + Suffix), 'ZKM_FK_AllController')
                # 建立骨骼关联字典
                LocalDictionary = {'joint': J_nume, 'Curve': nurbs_nume, 'Grp': TopGrp_Num}
                # 将关联字典添加到总字典
                AllDictionary.append(LocalDictionary)
        # 将总字典添加到骨骼组
        cmds.select('ZKM_FK_Root_Grp')
        RootGrp = cmds.ls(sl=1)
        if not RootGrp[0].hasAttr('notes'):
            RootGrp[0].addAttr('notes', type='string')
        Txt = ''
        for D in AllDictionary:
            Txt = Txt + str(D) + '\n'
        RootGrp[0].attr('notes').set(Txt)

        # 创建控制器查询范围
        cmds.select('ZKM_FK_AllController')
        mel.eval('SelectHierarchy;')
        cmds.select(cl=1)
        NeedDeleteConstraint = []
        for J in joint:  # 开始矫正位置
            for i in range(0, C_GrpNum):
                # 查询是否有约束，有则进行偏移处理
                # 将约束分为位移和旋转两部分
                try:
                    Constraint = cmds.parentConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                    TranslateConstraint = Constraint
                    RotateConstraint = Constraint
                except:
                    try:
                        Constraint = cmds.pointConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                        TranslateConstraint = Constraint
                    except:
                        TranslateConstraint = []
                    try:
                        Constraint = cmds.orientConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                        RotateConstraint = Constraint
                    except:
                        try:
                            Constraint = cmds.aimConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                            RotateConstraint = Constraint
                        except:
                            RotateConstraint = []
                # 开始处理位移和旋转Constraint = cmds.pointConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                # 把定位器p到对应的约束源Constraint = cmds.orientConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                # 获取需要的位移和旋转值赋予到对应约束的偏移值Constraint = cmds.aimConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                # 删除定位器
                if TranslateConstraint:
                    NumLoc = cmds.spaceLocator()
                    parent = cmds.listRelatives(TranslateConstraint, p=1)
                    parent = cmds.listRelatives(parent, p=1)
                    cmds.parent(NumLoc, parent[0])
                    cmds.parentConstraint(J, NumLoc)
                    Num = cmds.getAttr(str(NumLoc) + '.t')
                    cmds.setAttr((str(J) + "_G" + str(i + 1) + Suffix + '.t'), Num)
                    if cmds.ls(TranslateConstraint, type='parentConstraint'):
                        Soure = cmds.parentConstraint(TranslateConstraint, q=1, tl=1)
                        cmds.parentConstraint(Soure, TranslateConstraint, mo=1, e=1)
                    if cmds.ls(TranslateConstraint, type='pointConstraint'):
                        Soure = cmds.pointConstraint(TranslateConstraint, q=1, tl=1)
                        cmds.pointConstraint(Soure, TranslateConstraint, mo=1, e=1)
                    cmds.delete(NumLoc)
                if RotateConstraint:
                    NumLoc = cmds.spaceLocator()
                    parent = cmds.listRelatives(RotateConstraint, p=1)
                    parent = cmds.listRelatives(parent, p=1)
                    cmds.parent(NumLoc, parent[0])
                    cmds.parentConstraint(J, NumLoc)
                    Num = cmds.getAttr(str(NumLoc) + '.r')
                    cmds.setAttr((str(J) + "_G" + str(i + 1) + Suffix + '.r'), Num)
                    if cmds.ls(RotateConstraint, type='parentConstraint'):
                        Soure = cmds.parentConstraint(RotateConstraint, q=1, tl=1)
                        cmds.parentConstraint(Soure, RotateConstraint, mo=1, e=1)
                    if cmds.ls(RotateConstraint, type='orientConstraint'):
                        Soure = cmds.orientConstraint(RotateConstraint, q=1, tl=1)
                        cmds.orientConstraint(Soure, RotateConstraint, mo=1, e=1)
                    if cmds.ls(RotateConstraint, type='aimConstraint'):
                        Soure = cmds.aimConstraint(RotateConstraint, q=1, tl=1)
                        cmds.aimConstraint(Soure, RotateConstraint, mo=1, e=1)
                    cmds.delete(NumLoc)
                ###################################################
                if not (TranslateConstraint and RotateConstraint):
                    NeedDeleteConstraint.append(cmds.parentConstraint(str(J), (str(J) + "_G" + str(i + 1) + Suffix)))
            NeedDeleteConstraint.append(cmds.parentConstraint(str(J), (str(J) + "_C" + Suffix)))
        for D in NeedDeleteConstraint:
            cmds.delete(D)
        # 进行父化
        for i in range(1, len(joint)):
            Parent = cmds.listRelatives(joint[i], p=1)
            cmds.select(Parent)
            jointLX = cmds.ls(typ='joint', sl=1)
            while not jointLX:
                Parent = cmds.listRelatives(p=1)
                cmds.select(Parent, r=1)
                jointLX = cmds.ls(typ='joint', sl=1)
            Parent = cmds.ls(sl=1)
            for j in range(0, len(joint)):
                if joint[j] == Parent[0]:
                    cmds.parent(joint[i] + '_G1' + Suffix, joint[j] + '_C' + Suffix)
                    break
        # 是否提取约束
        ExtractConstraints = cmds.checkBox('WindowControllerProcessingExtractConstraints', q=1, value=1)
        # 进行约束
        if ExtractConstraints == 1:
            cmds.select(cl=1)
            if not cmds.objExists('ZKM_AllControllerConstraint_Grp'):
                cmds.rename(mel.eval('doGroup 0 1 1;'), 'ZKM_AllControllerConstraint_Grp')
                cmds.parent('ZKM_AllControllerConstraint_Grp', 'ZKM_AllFK_TopGrp')
        for i in range(0, len(joint)):
            cmds.parentConstraint((joint[i] + "_C" + Suffix), joint[i])
            cmds.scaleConstraint((joint[i] + "_C" + Suffix), joint[i])
            if ExtractConstraints == 1:
                cmds.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"),
                          'ZKM_AllControllerConstraint_Grp')
        # 还原原本的骨骼
        for NC in NoCreate:
            cmds.parent(NC.get('self'), NC.get('parent')[0])
            if NC.get('child'):
                cmds.parent(NC.get('child'), NC.get('self'))
        # 其他系统 #############################################################################################################
        if cmds.objExists('ZKM_OtherSystem'):
            cmds.setAttr('ZKM_OtherSystem.v', 1)
            cmds.setAttr("ZKM_OtherSystemShape.visibility", 0)
        else:
            cmds.spaceLocator(n='ZKM_OtherSystem')
            cmds.parent('ZKM_OtherSystem', 'ZKM_AllFK_TopGrp')
            cmds.setAttr("ZKM_OtherSystemShape.visibility", 0)
        for n in ['IK', 'SplineIK', 'AIM', 'Wheel', 'Hand', 'foot']:
            if cmds.objExists('ZKM_' + n + '_System'):
                cmds.setAttr('ZKM_' + n + '_System.v', 1)
                cmds.setAttr('ZKM_' + n + '_SystemShape.visibility', 0)
            else:
                cmds.spaceLocator(n='ZKM_' + n + '_System')
                cmds.parent('ZKM_' + n + '_System', 'ZKM_OtherSystem')
                cmds.setAttr('ZKM_' + n + '_SystemShape.visibility', 0)
        cmds.select('ZKM_FK_Root')
        mel.eval('SelectHierarchy;')
        joint = cmds.ls(typ='joint', sl=1)
        '''for j in joint:
            Attribute = cmds.listAttr(userDefined=True)
            if Attribute:
                for At in Attribute:
                    if At == 'IK':# 自带极向量和切换
                        IK_Joint = cmds.attributeQuery('IK', node=j, listEnum=1)
                    if At == 'SplineIK': # 样条IK
                        SplineIK_Joint = cmds.attributeQuery('SplineIK', node=j, listEnum=1)
                    if At == 'AIM': # 眼部朝向
                        SplineIK_Joint = cmds.attributeQuery('SplineIK', node=j, listEnum=1)
                    if At == 'Wheel':# 轮胎驱动
                        pass
                    if At == 'Hand':# 手部驱动
                        SplineIK_Joint = cmds.attributeQuery('Hand', node=j, listEnum=1)
                    if At == 'foot':  # 脚部驱动
                        SplineIK_Joint = cmds.attributeQuery('foot', node=j, listEnum=1)'''

    def ZKM_ChuangJianFK_2(self, Name, C_GrpNum, Suffix, RemoveJoint):
        cmds.select('ZKM_FK_Root')
        mel.eval('SelectHierarchy;')
        joint = cmds.ls(typ='joint', sl=1)
        ALL = cmds.ls(sl=1)
        if RemoveJoint == True:
            for j in joint:
                q = cmds.listRelatives(j, c=1)
                if len(q) == 0:
                    joint.remove(j)
        # 建立独立控制器
        # 建立总控制器组
        cmds.select(cl=1)
        cmds.group(n='ZKM_FK_AllController')
        cmds.parent('ZKM_FK_AllController', 'ZKM_AllFK_TopGrp')
        # 创建总字典
        AllDictionary = []
        for J in joint:
            J_nume = []
            # 给骨骼添加32位随机数
            if not J.hasAttr('notes'):
                self.ZKM_SetNumToNotes(J, 32)
            J_nume.append(cmds.getAttr(J + '.notes'))
            # 建立基础控制器并改名
            cmds.rename(self.curve.create_curve(
                (root_path + '\MayaCommon\CurveShapeWithPicture'), Name), str(J) + "_C" + Suffix)
            nurbs = cmds.ls(sl=1)
            # 给曲线添加32位随机数
            if not nurbs[0].hasAttr('notes'):
                self.ZKM_SetNumToNotes(nurbs[0], 32)
            nurbs_nume = []
            nurbs_nume.append(cmds.getAttr(nurbs[0] + '.notes'))
            TopGrp_Num = []
            # 循环创建控制器组，且给添加32位随机数
            for j in range(0, C_GrpNum):
                Grp_Num = []
                mel.eval('doGroup 0 1 1;')
                # 建立样条组
                cmds.mel.rename(str(J) + "_G" + str((C_GrpNum - j)) + Suffix)
                Grp = cmds.ls(sl=1)
                if not Grp[0].hasAttr('notes'):
                    self.ZKM_SetNumToNotes(Grp[0], 32)
                Grp_Num = cmds.getAttr(Grp[0] + '.notes')
                TopGrp_Num.append(Grp_Num)
            cmds.parent((str(J) + "_G1" + Suffix), 'ZKM_FK_AllController')
            # 建立骨骼关联字典
            LocalDictionary = {'joint': J_nume, 'Curve': nurbs_nume, 'Grp': TopGrp_Num}
            # 将关联字典添加到总字典
            AllDictionary.append(LocalDictionary)
        # 将总字典添加到骨骼组
        cmds.select('ZKM_FK_Root_Grp')
        RootGrp = cmds.ls(sl=1)
        if not RootGrp[0].hasAttr('notes'):
            RootGrp[0].addAttr('notes', type='string')
        Txt = ''
        for D in AllDictionary:
            Txt = Txt + str(D) + '\n'
        RootGrp[0].attr('notes').set(Txt)

        cmds.select('ZKM_FK_AllController')
        mel.eval('SelectHierarchy;')
        AllControllerInformation = cmds.ls(sl=1)
        cmds.select(cl=1)
        # 进行父化
        for i in range(1, len(joint)):
            Parent = cmds.listRelatives(joint[i], p=1)
            cmds.select(Parent)
            jointLX = cmds.ls(typ='joint', sl=1)
            while not jointLX:
                Parent = cmds.listRelatives(p=1)
                cmds.select(Parent, r=1)
                jointLX = cmds.ls(typ='joint', sl=1)
            Parent = cmds.ls(sl=1)
            self.ZKM_ReturnNotesToModel(AllControllerInformation, AllDictionary[i], 'Grp', -1)
            TopGrp = cmds.ls(sl=1)
            for j in range(0, len(joint)):
                self.ZKM_ReturnNotesToModel(AllControllerInformation, AllDictionary[j], 'Curve', 0)
                nurbs = cmds.ls(sl=1)
                if joint[j] == Parent[0]:
                    cmds.parent(TopGrp[0], nurbs[0])
                    break
        # 是否提取约束
        ExtractConstraints = cmds.checkBox('WindowControllerProcessingExtractConstraints', q=1, value=1)
        # 进行约束
        if ExtractConstraints == 1:
            cmds.select(cl=1)
            if not cmds.objExists("ZiJianKZQyveshu"):
                cmds.rename(mel.eval('doGroup 0 1 1;'), "ZiJianKZQyveshu")
        for i in range(0, len(joint)):
            cmds.parentConstraint((joint[i] + "_C" + Suffix), joint[i])
            cmds.scaleConstraint((joint[i] + "_C" + Suffix), joint[i])
            if ExtractConstraints == 1:
                cmds.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"), "ZiJianKZQyveshu")

        t = cmds.getAttr('ZKM_FK_Root_Grp.notes')
        # print (t.split('\n')[0])

    # 还原约束
    def return_constraint(self,need_return_node,all_connect_node, Constraint):
        if not all_connect_node:
            # 断开链接，开启阻断
            all_connect_node = []
            for c in need_return_node:
                for attribute in ['t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz', 'v']:
                    node = cmds.listConnections(c + '.' + attribute)
                    if node:
                        all_connect_node.append(node[0])
            seen = set()
            all_connect_node = [x for x in all_connect_node if not (x in seen or seen.add(x))]
            all_connect_node_ls = []
            for node in all_connect_node:
                node_type = cmds.objectType(node)
                for typ in ['parentConstraint','pointConstraint','orientConstraint','aimConstraint','scaleConstraint']:
                    if node_type == typ:
                        all_connect_node_ls.append(node)
            all_connect_node = all_connect_node_ls
            # print(all_connect_node)
            Constraint = []
            if all_connect_node:
                for node in all_connect_node:
                    if cmds.objectType(node) == 'parentConstraint':
                        cmds.setAttr(node + '.nodeState', 2)
                        constraint_target = cmds.listConnections(node, s=0)
                        seen = set()
                        constraint_target = [x for x in constraint_target if not (x in seen or seen.add(x))]
                        constraint_target.remove(node)
                        if constraint_target:
                            for attribute in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
                                have_connect = cmds.listConnections(constraint_target[0] + '.' + attribute, c=1, p=1)
                                if have_connect:
                                    Constraint.append(have_connect)
                                    cmds.disconnectAttr(have_connect[1], have_connect[0])
                # print(Constraint)
            return all_connect_node, Constraint
        else:
            # print('aaaaaaa')
            # print(all_connect_node)
            # 还原链接关闭阻断
            for node in Constraint:
                if cmds.objExists(node[1]) and cmds.objExists(node[0]):
                    cmds.connectAttr(node[1], node[0], f=1)
            for node in all_connect_node:
                if cmds.objExists(node):
                    if cmds.objectType(node) == 'parentConstraint':
                        soure = cmds.parentConstraint(node, q=1, tl=1)
                        cmds.parentConstraint(soure, node, maintainOffset=1, e=1)
                    # if cmds.objectType(node) == 'pointConstraint':
                    #     cmds.setAttr(node + '.nodeState', 0)
                    # if cmds.objectType(node) == 'aimConstraint':
                    #     cmds.setAttr(node + '.nodeState', 0)
                    # if cmds.objectType(node) == 'orientConstraint':
                    #     cmds.setAttr(node + '.nodeState', 0)
            for node in all_connect_node:
                cmds.setAttr(node + '.nodeState', 0)
