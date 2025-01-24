# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
# 获取文件路径
import os
from os import listdir
import sys
import inspect
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




# 权重相关
class Weight:
    # 基础拷贝权重
    def base_copy_joint_weight(self, copy_way, soure, target, soure_uv_set, target_uv_set):
        # str copy_way 有Normal和UV两种方式
        # list soure
        # list target
        # str soure_uv_set
        # str target_uv_set
        if copy_way and soure and target:
            source_skin_joint = []
            try:
                source_skin_joint = cmds.skinCluster(soure, q=1, inf=1)
            except:
                pass

            if source_skin_joint:
                # source_shape = cmds.listRelatives(soure, s=1)
                # source_skin_cluster = cmds.listConnections((source_shape[0] + '.inMesh'), d=1)
                if type(soure) == list:
                    source_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + soure[0] + '\");')
                else:
                    source_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + soure + '\");')
            else:
                source_skin_cluster = []
            if len(target[0].split('.')) == 1:
                target_type = 'Model'
            else:
                target_type = 'Point'

            if source_skin_cluster:
                # 先进行添加影响和蒙皮
                if target_type == 'Model':
                    for t in target:
                        target_skin_cluster = []
                        try:
                            target_skin_cluster = mel.eval('findRelatedSkinCluster(\"'+t+'\");')
                            # target_shape = cmds.listRelatives(t, s=1)
                            # target_skin_cluster = cmds.listConnections((target_shape[0] + '.inMesh'), d=1)
                        except:
                            pass
                        if target_skin_cluster:
                            cmds.skinCluster(target_skin_cluster,e=1,ub=1)
                        cmds.skinCluster(t,source_skin_joint,tsb=1)
                target_model = ''
                if target_type == 'Point':
                    target_model = target[0].split('.')[0]
                    target_skin_cluster = []
                    try:
                        target_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + target_model + '\");')
                        # target_shape = cmds.listRelatives(target_model, s=1)
                        # target_skin_cluster = cmds.listConnections((target_shape[0] + '.inMesh'), d=1)
                    except:
                        pass
                    if target_skin_cluster:
                        targetJoint = cmds.skinCluster(target_model, q=1, inf=1)
                        joint = [i for i in source_skin_joint if i not in targetJoint]
                        if joint:
                            for j in joint:
                                cmds.skinCluster(target_skin_cluster, e=1, ai=j, wt=0)
                    else:
                        cmds.skinCluster(target_model,source_skin_joint, tsb=1)

                # 进行拷贝权重
                if copy_way == 'Normal':
                    if target_type == 'Model':
                        for t in target:
                            cmds.select(soure, t)
                            target_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + t + '\");')
                            cmds.copySkinWeights(ss=source_skin_cluster, surfaceAssociation='closestPoint',
                                               influenceAssociation='oneToOne', noMirror=1, ds=target_skin_cluster)

                            # cmds.copySkinWeights(surfaceAssociation='closestPoint',
                            #                      influenceAssociation='oneToOne', noMirror=1)
                    if target_type == 'Point':
                        cmds.select(soure, target)
                        target_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + target_model + '\");')
                        cmds.copySkinWeights(ss=source_skin_cluster, surfaceAssociation='closestPoint',
                                             influenceAssociation='oneToOne', noMirror=1,selectedComponents=1,
                                             ds=target_skin_cluster)
                if copy_way == 'UV':
                    if target_uv_set and target_uv_set:
                        if target_type == 'Model':
                            for T in target:
                                cmds.select(soure, T)
                                target_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + T + '\");')
                                cmds.copySkinWeights(ss=source_skin_cluster, surfaceAssociation='closestPoint',
                                                     uvSpace=(soure_uv_set, target_uv_set),
                                                     noMirror=1, influenceAssociation=['closestJoint', 'oneToOne'],
                                                     ds=target_skin_cluster)
                        if target_type == 'Point':
                            cmds.select(soure, target)
                            target_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + target + '\");')
                            cmds.copySkinWeights(ss=source_skin_cluster, surfaceAssociation='closestPoint',
                                                 uvSpace=(soure_uv_set, target_uv_set),
                                                 noMirror=1, influenceAssociation=['closestJoint', 'oneToOne'],
                                                 ds=target_skin_cluster)
                    else:
                        print('请加载uv选集')
            else:
                print('源没有骨骼蒙皮')

    # 拷贝模型权重
    def copy_joint_weight(self):
        sel = cmds.ls(sl=1)
        self.base_copy_joint_weight('Normal', sel[0], sel[1:], '', '')

    # 对半拷贝权重
    def half_and_half_copy_weight(self):
        all_sel = cmds.ls(sl=1)
        print(all_sel)
        print(len(all_sel) / 2)
        first_half = all_sel[:int(len(all_sel) / 2)]
        print(first_half)
        latter_half = all_sel[int(len(all_sel) / 2):]
        cmds.select(first_half)
        cmds.SelectHierarchy()
        first_half_mesh = cmds.ls(type="mesh", sl=1)
        cmds.select(latter_half)
        cmds.SelectHierarchy()
        latter_half_mesh = cmds.ls(type="mesh", sl=1)
        if len(first_half_mesh) == len(latter_half_mesh):
            for i in range(0, len(first_half_mesh)):
                cmds.select(first_half_mesh[i], r=1)
                cmds.pickWalk(d='up')
                s = cmds.ls(sl=1)
                cmds.select(latter_half_mesh[i], r=1)
                cmds.pickWalk(d='up')
                t = cmds.ls(sl=1)
                cmds.select(s, t)
                self.copy_joint_weight()
        else:
            cmds.cmds.mel.error("请加载偶数的选择")

    # 底层平滑权重
    def base_smooth_weight(self, model, normalize_weight, num):
        cmds.undoInfo(ock=1)
        for m in model:
            if normalize_weight == 1:
                cmds.skinCluster(e=1, nw=2)
            else:
                cmds.skinCluster(e=1, nw=1)
            joint = cmds.skinCluster(m,q=1, inf=1)
            for i in range(0, len(joint)):
                mel.eval('artSkinInflListChanging ' + joint[i] + ' 1;')
                mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
                sel = cmds.currentCtx()
                for J in range(0, num):
                    cmds.artAttrSkinPaintCtx(sel, e=1, opacity=1, clear=1)
        cmds.undoInfo(cck=1)

    # 平滑权重应用
    def apply_smooth_weight(self, normalize_weight, num):
        sel = cmds.ls(sl=1)
        model = []
        if len(sel[0].split('.')) == 1:
            for s in sel:
                shape = cmds.listRelatives(s, s=1)
                model.append(shape[0])
        else:
            shape = sel[0].split('.')
            model.append(shape[0])

        mel.eval('ArtPaintSkinWeightsTool;')
        mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')
        self.base_smooth_weight(model, normalize_weight, num)
        cmds.select(sel)

    # 选择源模型合并权重到目标
    def select_source_model_merge_joint_weight_to_target(self, soure):
        cmds.undoInfo(ock=1)
        sel = cmds.ls(sl=1)
        new_model = []
        for s in sel:
            cmds.select(s)
            cmds.duplicate(rr=1)
            new_sel = cmds.ls(sl=1)
            new_model.append(new_sel[0])
        for s, n in zip(sel, new_model):
            cmds.select(s, n)
            self.copy_joint_weight()
        cmds.polyUniteSkinned(new_model, ch=0, mergeUVSets=1, centerPivot=1)
        merged_models = cmds.ls(sl=1)
        for i in new_model:
            cmds.delete(i)
        cmds.select(merged_models, soure)
        self.copy_joint_weight()
        cmds.delete(merged_models)
        cmds.undoInfo(cck=1)

    # 导出权重
    def export_weight(self, Model):
        # 查询当前Maya安装路径
        MAYA_VERSION = cmds.about(version=True)[:4]
        # MayaPath = os.environ['HOME'] + "/maya/" + MAYA_VERSION
        # 查询并建立临时文件夹
        try:
            wight_file_path = cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', q=1,ann=1)
            print(wight_file_path)
            path = wight_file_path + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder'
        except:
            path = file_path + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder'
        path_split = path.split('\\')
        MayaPath = path_split[0]
        for i in range(1, len(path_split)):
            MayaPath = MayaPath + '/' + path_split[i]
        # if not os.path.exists(path):
        #     os.makedirs(path)
        # 清理与即将生成的文件重名的文件
        #print (MayaPath + '/scratch_file/MayaWeightExportImportWeightProvisionalFolder')
        if any(name.endswith(('.xml')) for name in
               os.listdir(path + '\\')):
            my_path = (path + '\\')
            for file_name in listdir(my_path):
                if file_name.endswith('.xml'):
                    os.remove(my_path + file_name)
                if file_name.endswith('.txt'):
                    os.remove(my_path + file_name)
        # 按名字创建文本
        for MD in Model:
            SkinCluster = mel.eval('findRelatedSkinCluster '+MD+';')
            if not SkinCluster:
                break
        for MD in Model:
            SkinCluster = mel.eval('findRelatedSkinCluster '+MD+';')
            if SkinCluster:
                Joint = cmds.skinCluster(MD, q=1, inf=1)
                file = open((path + '\\' + MD + '.txt'), "w")
                for Jon in Joint:
                    file.write(Jon + '\n')
                file.close()
                mel.eval('deformerWeights -export -deformer \"' + SkinCluster + '\" -path \"' + MayaPath + '/' + '\" \"' + MD + '.xml\";')
        print('\n如果要查询，下面是路径：' + '\n' + str(path) + '\n')

    # 导入权重
    # noinspection PyTypeChecker
    def import_weight(self, Model):
        # 查询当前Maya安装路径
        # MAYA_VERSION = cmds.about(version=True)[:4]
        # MayaPath = os.environ['HOME'] + "/maya/" + MAYA_VERSION
        try:
            wight_file_path = cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', q=1,ann=1)
            # print(wight_file_path)
            path = wight_file_path + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder'
        except:
            path = file_path + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder'
        # 查询临时文件夹
        # AllPath = file_path.split('/')
        # path = AllPath[0]
        # for i in range(1, len(AllPath)):
        #     path = path + '\\' + AllPath[i]
        # MayaPath = file_path
        if not os.path.exists(path):
            print('\n没有找到本插件的权重存放文件夹，请先导出权重。\n如果要查询，下面是路径：' + '\n' + str(
                path) + '\n')
        else:
            AllNodes = cmds.ls(type='joint')
            for MD in Model:
                if not os.path.exists(path + '\\'+ MD + ".xml"):
                    print('\n如果没有找到本插件的权重存放文件夹，请先导出权重。\n如果要查询，下面是路径：' + '\n' + str(path) + '\\'+ str(MD) + ".xml"+'\n')
                else:

                    fo = open(path + "\\" + MD + ".txt", "r")
                    lines = [l.split() for l in fo if l.strip()]
                    fo.close()
                    for i in range(0, len(lines)):
                        lines[i] = str(lines[i])[2:-2]
                    addJoint = [x for x in lines if x not in AllNodes]  # 筛选出需要补充创建的骨骼
                    for J in addJoint:  # 补充骨骼
                        cmds.select(cl=1)
                        cmds.joint(p=(0, 0, 0), n=J)
                    try:
                        HaveSkinCluster = mel.eval('findRelatedSkinCluster '+MD+';')  # 查询是否有蒙皮节点
                    except:
                        HaveSkinCluster = []

                    if HaveSkinCluster:
                        cmds.select(MD, r=1)
                        shapes = cmds.listRelatives(MD, shapes=1)
                        cmds.skinCluster(shapes[0], e=1, ub=1)
                    cmds.select(MD)
                    cmds.select(lines, add=1)
                    cmds.skinCluster(tsb=1)
                    cmds.select(MD)
                    SkinCluster = mel.eval('findRelatedSkinCluster '+MD+';')  # 查询蒙皮节点
                    cmds.deformerWeights((MD + ".xml"),
                                       path=(path + "\\"), im=1,
                                       method="index", deformer=SkinCluster)
                    cmds.skinCluster(SkinCluster, forceNormalizeWeights=1, e=1)
                    #print('\n如果要查询，下面是路径：' + '\n' + str(path) + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder\n如果没有导入请确认是否重名或者名称不一样\n')
        cmds.refresh()

    # 归一化权重
    def normalize_weight(self, Model):
        for MD in Model:
            SkinCluster = mel.eval('findRelatedSkinCluster '+MD+';')  # 查询蒙皮节点
            cmds.skinCluster(SkinCluster, forceNormalizeWeights=1, e=1)

    # 处理权重矩阵，使低版本maya模型移动过远产生点抖动的问题
    def handling_weight_jitter(self, sel, switch):
        cmds.undoInfo(ock=1)
        if switch == 1:
            multMatrix = cmds.shadingNode('multMatrix', asUtility=1)
            Matrix = cmds.listConnections((sel[0] + '.worldMatrix[0]'), p=1)
            for M in Matrix:
                cmds.connectAttr((multMatrix + '.matrixSum'), M, force=1)
            cmds.connectAttr((sel[0] + '.worldMatrix[0]'), (multMatrix + '.matrixIn[0]'), force=1)
            cmds.connectAttr((sel[0] + '.worldInverseMatrix[0]'), (multMatrix + '.matrixIn[1]'), force=1)
            for i in range(1, len(sel)):
                multMatrix = cmds.shadingNode('multMatrix', asUtility=1)
                Matrix = cmds.listConnections((sel[i] + '.worldMatrix[0]'), p=1, type='skinCluster')
                for M in Matrix:
                    target = cmds.skinCluster(M.split('.')[0], q=1, g=1)
                    if target:
                        if not cmds.ls(target[0], type='mesh'):
                            Matrix.remove(M)
                for M in Matrix:
                    cmds.connectAttr((multMatrix + '.matrixSum'), M, force=1)
                cmds.connectAttr((sel[i] + '.worldMatrix[0]'), (multMatrix + '.matrixIn[0]'), force=1)
                cmds.connectAttr((sel[0] + '.worldInverseMatrix[0]'), (multMatrix + '.matrixIn[1]'), force=1)
        else:
            Matrix = cmds.listConnections((sel[0] + '.worldInverseMatrix[0]'), d=1, type='multMatrix')
            for i in range(0, len(Matrix)):
                Soure = cmds.listConnections((Matrix[i] + '.matrixIn[0]'), p=1)
                Target = cmds.listConnections((Matrix[i] + '.matrixSum'), p=1)
                if Target:
                    for T in Target:
                        cmds.connectAttr(Soure[0], T, force=1)
                cmds.delete(Matrix[i])
        cmds.undoInfo(cck=1)




