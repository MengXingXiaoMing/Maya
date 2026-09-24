# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
import importlib
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    # 库路径
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)


def Withdraw(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # 修正参数空格问题
        cmds.undoInfo(ock=1)  # 开启撤销块
        cmds.ogs(p=1)
        exception_info = None
        result = []
        try:
            result = func(*args, **kwargs)  # 正确缩进
        except Exception as e:  # 缩进对齐try
            # 捕获异常并保存信息
            exception_info = sys.exc_info()
        finally:
            # 无论是否异常都会执行
            cmds.undoInfo(cck=1)  # 关闭撤销块
            cmds.ogs(p=1)
            # print('撤销块已关闭')

        # 重新抛出异常
        if exception_info:
            error_type, error_value, traceback = exception_info
            # 重新抛出原始异常（保持堆栈信息）
            error_type = type(error_value)
            formatted_traceback = format_exception(error_type, error_value, traceback)
            cmds.warning(''.join(formatted_traceback))
            # raise error_value.with_traceback(traceback)
        return result

    return wrapper
# 权重相关
class Weight:
    # 取消蒙皮
    def cancel_skin(self):
        sel = cmds.ls(sl=1)
        source_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + sel[0] + '\");')
        # print(source_skin_cluster)
        source_skin_joint = cmds.skinCluster(source_skin_cluster, q=1, inf=1)
        # print(source_skin_joint)
        # source_skin_joint=source_skin_joint[:100]
        restore = []
        for j in source_skin_joint:
            layer = cmds.ls(j, long=True)
            layer_num = len(layer[0].split("|"))
            if layer_num % 100 == 0:
                parent = cmds.listRelatives(j, p=True)
                cmds.parent(j, w=True)
                p_s = [parent, j]
                restore.append(p_s)
                # print(layer_num)
        cmds.select(sel)
        cmds.DetachSkin()
        for p, j in restore:
            cmds.parent(j, p)
        cmds.select(sel)

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
                            targetJoint = cmds.skinCluster(t, q=1, inf=1)
                            joint = [i for i in source_skin_joint if i not in targetJoint]
                            if joint:
                                for j in joint:
                                    cmds.skinCluster(target_skin_cluster, e=1, ai=j, wt=0)
                        else:
                            cmds.skinCluster(t, source_skin_joint, tsb=1)
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
                        cmds.skinCluster(target_model, source_skin_joint, tsb=1)

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
                        try:
                            cmds.copySkinWeights(ss=source_skin_cluster, surfaceAssociation='closestPoint',
                                                 influenceAssociation='oneToOne', noMirror=1, selectedComponents=1,
                                                 ds=target_skin_cluster)
                        except:
                            cmds.copySkinWeights(surfaceAssociation='closestPoint',
                                                 influenceAssociation='oneToOne', noMirror=1,
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


    def new_maya_base_copy_joint_weight(self,copy_way, soure, target, soure_skin, target_skin, soure_uv_set, target_uv_set):
        # str copy_way 有Normal和UV两种方式
        # list soure
        # list target
        # str soure_uv_set
        # str target_uv_set
        if copy_way and soure and target and soure_skin:
            # 获取源骨骼影响
            source_skin_joint = cmds.skinCluster(soure_skin, q=1, inf=1)
            # 判断目标选的是模型还是点
            if len(target[0].split('.')) == 1:
                target_type = 'Model'
            else:
                target_type = 'Point'
            # 先进行添加影响和蒙皮
            if target_type == 'Model':
                # print(target)
                for i in range(len(target_skin)):
                    target_skin_cluster = target_skin[i]
                    if target_skin_cluster:
                        # print(target_skin[i])
                        targetJoint = cmds.skinCluster(target_skin[i], q=1, inf=1)
                        joint = [i for i in source_skin_joint if i not in targetJoint]
                        joint_re = [i for i in targetJoint if i not in source_skin_joint]
                        if joint:
                            # print(source_skin_joint)
                            # print(targetJoint)
                            # print(joint)
                            for j in joint:
                                # print(target_skin_cluster, j)
                                cmds.skinCluster(target_skin_cluster, e=1, ai=j, wt=0)
                        if joint:
                            for j in joint_re:
                                cmds.skinCluster(target_skin_cluster, e=1, ri=j)

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
                    cmds.warning('没有找到目标模型的skinCluster')
            # 进行拷贝权重
            if copy_way == 'Normal':
                if target_type == 'Model':
                    for i in range(len(target)):
                        # print(soure_skin,target_skin[i])
                        cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestPoint',
                                             influenceAssociation='closestJoint', noMirror=1, ds=target_skin[i])
                if target_type == 'Point':
                    cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestPoint',
                                         influenceAssociation='closestJoint', noMirror=1, ds=target_skin)
            if copy_way == 'UV':
                if target_uv_set and target_uv_set:
                    if target_type == 'Model':
                        for i in range(len(target)):
                            cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestPoint',
                                                 uvSpace=(soure_uv_set, target_uv_set), influenceAssociation='closestJoint',
                                                 noMirror=1, ds=target_skin[i])
                    if target_type == 'Point':
                        cmds.copySkinWeights(ss=soure_skin, surfaceAssociation='closestPoint',
                                             uvSpace=(soure_uv_set, target_uv_set), influenceAssociation='closestJoint',
                                             noMirror=1, ds=target_skin)
                else:
                    print('请加载uv选集')
        else:
            cmds.warning('请确认是否有拷贝源和目标列表和源蒙皮。')

    # 拷贝模型权重
    def copy_joint_weight(self):
        sel = cmds.ls(sl=1)
        self.base_copy_joint_weight('Normal', sel[0], sel[1:], '', '')

    # 对半拷贝权重
    def half_and_half_copy_weight(self):
        all_sel = cmds.ls(sl=1)
        # print(all_sel)
        # print(len(all_sel) / 2)
        first_half = all_sel[:int(len(all_sel) / 2)]
        # print(first_half)
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
        # MAYA_VERSION = cmds.about(version=True)[:4]
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
            for file_name in os.listdir(my_path):
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
            for MD in Model:
                AllNodes = cmds.ls(type='joint')
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
    @Withdraw
    def handling_weight_jitter(self, sel, switch):
        # cmds.undoInfo(ock=1)
        if switch == 1:
            multMatrix = cmds.shadingNode('multMatrix', asUtility=1)
            Matrix = cmds.listConnections((sel[0] + '.worldMatrix[0]'), p=1, type='skinCluster')
            for M in Matrix:
                cmds.connectAttr((multMatrix + '.matrixSum'), M, force=1)
            cmds.connectAttr((sel[0] + '.worldMatrix[0]'), (multMatrix + '.matrixIn[0]'), force=1)
            cmds.connectAttr((sel[0] + '.worldInverseMatrix[0]'), (multMatrix + '.matrixIn[1]'), force=1)
            for i in range(1, len(sel)):
                multMatrix = cmds.shadingNode('multMatrix', asUtility=1)
                Matrix = cmds.listConnections((sel[i] + '.worldMatrix[0]'), p=1, type='skinCluster')
                # print(Matrix)
                # for M in Matrix:
                #     target = cmds.skinCluster(M.split('.')[0], q=1, g=1)
                #     if target:
                #         if not cmds.ls(target[0], type='mesh'):
                #             Matrix.remove(M)
                print(Matrix)
                if Matrix:
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
        # cmds.undoInfo(cck=1)


    def get_current_paint_skin_cluster(self):
        """
        针对 Maya 2025 蒙皮笔刷面板获取当前选中的真实蒙皮节点名
        """
        # 控件名称根据你的日志确定为 'skinClusterPaintList'
        list_control = 'skinClusterPaintList'

        # 1. 优先尝试从 UI 列表控件获取
        if cmds.textScrollList(list_control, q=True, exists=True):
            # 获取选中的显示名称列表
            selected_items = cmds.textScrollList(list_control, q=True, selectItem=True)

            if selected_items:
                # 还原真实节点名：将日志中的 " → " (u'\u2192') 换回 "|"
                # 即使没有层级符号，replace 也不影响普通字符串
                display_name = selected_items[0]
                real_skin_cluster = display_name.replace(u' \u2192 ', '|')
                return real_skin_cluster

        # 2. 如果 UI 获取不到，使用上下文查询（注意：必须是 artAttrSkinPaintCtx）
        ctx = "artSkinPaintContext"
        if cmds.contextInfo(ctx, ex=True):
            try:
                # 查询笔刷当前绑定的 skinCluster
                active_sc = cmds.artAttrSkinPaintCtx(ctx, q=True, skinCluster=True)
                if active_sc:
                    return active_sc
            except Exception as e:
                print(f"上下文查询失败: {e}")

        return None

    def get_closest_vertex(self):
        # 1. 获取选中的模型
        selection = cmds.ls(sl=True, long=True)
        if not selection:
            cmds.warning("请先选中一个多边形模型！")
            return

        # 2. 获取视口并处理坐标翻转
        active_view = omui.M3dView.active3dView()
        view_ptr = active_view.widget()
        widget = shiboken6.wrapInstance(int(view_ptr), QtWidgets.QWidget)

        global_pos = QtGui.QCursor.pos()
        local_pos = widget.mapFromGlobal(global_pos)

        _, _, _, vheight = active_view.viewport()
        final_x = int(local_pos.x())
        final_y = int(vheight - local_pos.y())

        # 3. 转换射线
        ray_source = om.MPoint()
        ray_direction = om.MVector()
        active_view.viewToWorld(final_x, final_y, ray_source, ray_direction)

        found = False
        for obj in selection:
            try:
                sel_list = om.MSelectionList()
                sel_list.add(obj)
                dag_path = sel_list.getDagPath(0)

                if not dag_path.hasFn(om.MFn.kMesh):
                    dag_path.extendToShape()

                fn_mesh = om.MFnMesh(dag_path)

                # --- A. 射线检测获取表面坐标和所在的 Face ID ---
                hit_info = fn_mesh.closestIntersection(
                    om.MFloatPoint(ray_source),
                    om.MFloatVector(ray_direction),
                    om.MSpace.kWorld,
                    999999.0,
                    True
                )

                if hit_info:
                    hit_point = om.MPoint(hit_info[0])
                    face_id = hit_info[2]  # 获取碰撞点所在的三角面/多边形 ID

                    # --- B. 寻找该面上最近的顶点 ---
                    # 获取该多边形包含的所有顶点索引
                    face_vertices = fn_mesh.getPolygonVertices(face_id)

                    closest_vtx_id = -1
                    min_dist = float('inf')

                    for vtx_id in face_vertices:
                        # 获取顶点坐标
                        vtx_pos = fn_mesh.getPoint(vtx_id, space=om.MSpace.kWorld)
                        # 计算到点击点的距离
                        dist = hit_point.distanceTo(vtx_pos)

                        if dist < min_dist:
                            min_dist = dist
                            closest_vtx_id = vtx_id

                    # 4. 格式化输出
                    if closest_vtx_id != -1:
                        full_vertex_name = f"{obj}.vtx[{closest_vtx_id}]"
                        # print("-" * 50)
                        # print(f"鼠标点击位置: {hit_point.x:.4f}, {hit_point.y:.4f}, {hit_point.z:.4f}")
                        # print(f"最近顶点名称: {full_vertex_name}")
                        # print(f"距离差值: {min_dist:.6f}")
                        # print("-" * 50)
                        found = True
                        return [[hit_point.x, hit_point.y, hit_point.z], full_vertex_name, min_dist]
                        # break
            except Exception as e:
                print(f"处理失败: {e}")
                continue

        if not found:
            print("未击中任何模型表面。")
            return None

    # 获取当前点当前蒙皮权重
    def get_max_weight_influence(self, point, skin_cluster):
        # 2. 获取该点的所有权重值
        # transformValues=True 会返回 (骨骼名, 权重值) 的对子
        weights = cmds.skinPercent(skin_cluster, point, query=True, value=True)
        influences = cmds.skinCluster(skin_cluster, q=True, inf=True)
        # print(weights,influences)
        # 3. 将骨骼名与权重值一一对应
        weight_map = dict(zip(influences, weights))

        # 4. 找到权重最大的骨骼
        max_influence = max(weight_map, key=weight_map.get)
        max_value = weight_map[max_influence]

        return max_influence, max_value

    # 绘制最近点最大权重骨骼
    def draw_near_point_max_skin_weight_joint(self):
        mel.eval("ArtPaintSkinWeightsTool;")
        list = self.get_closest_vertex()
        skin = self.get_current_paint_skin_cluster()
        if list and skin:
            inf_name, val = result = self.get_max_weight_influence(list[1], skin)
            mel.eval(
                'artSkinInflListChanging \"' + inf_name + '\" 1;''artSkinInflListChanged artAttrSkinPaintCtx;refreshAE;')


class SurfaceWeight:
    pass

