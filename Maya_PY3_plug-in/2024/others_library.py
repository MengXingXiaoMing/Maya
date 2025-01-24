# -*- coding: utf-8 -*-
import importlib

import maya.cmds as cmds
import maya.mel as mel
# 获取文件路径
import os
import sys
import inspect
import webbrowser
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




# 杂项
class OthersLibrary:
    # 打开网页
    def open_web(self,num):
        web = ''
        if num == 0 :
            web = 'https://github.com/MengXingXiaoMing?tab=repositories'
        if num == 1:
            web = 'https://space.bilibili.com/173984578?spm_id_from=333.1007.0.0'
        webbrowser.open(web)
        return web
    # 去除重复名称
    def remove_duplicate_name(self):
        all_name = cmds.ls()
        duplicate_name = []
        for name in all_name:
            duplicate = name.split('|')
            if len(duplicate) > 1:
                duplicate_name.append(name)
        cmds.undoInfo(ock=1)
        if duplicate_name:
            for i in range(0, len(duplicate_name)):
                num = []
                base_name = []
                name = duplicate_name[len(duplicate_name) - i - 1].split('|')[-1]
                for j in range(0, len(name)):
                    if name[len(name) - 1 - j].isdigit() == False:
                        num = name[len(name) - j:]
                        base_name = name[:len(name) - j]
                        break
                cmds.select('*|' + base_name + '*')
                name_list = cmds.ls(sl=1)
                all_num = []
                for name in name_list:
                    for j in range(0, len(name)):
                        if name[len(name) - 1 - j].isdigit() == False:
                            num = name[len(name) - j:]
                            if num:
                                all_num.append(int(num))
                            break
                cmds.rename(duplicate_name[len(duplicate_name) - i - 1], (str(base_name) + str(max(all_num) + 1)))
            cmds.warning('已经去除重复名称')
        else:
            cmds.warning('没有重名DAG')
        cmds.undoInfo(cck=1)

    # 显隐轴向
    def show_hide_axial(self):
        cmds.undoInfo(ock=1)
        sel = cmds.ls(sl=1)
        for i in range(0, len(sel)):
            Ture = int(cmds.getAttr(sel[i] + ".displayLocalAxis"))
            if Ture < 1:
                cmds.setAttr((sel[i] + ".displayLocalAxis"), 1)
            else:
                cmds.setAttr((sel[i] + ".displayLocalAxis"), 0)

        cmds.undoInfo(cck=1)
    # 生成骨骼链
    def generate_bone_chain(self, num):
        cmds.undoInfo(ock=1)
        nurbs = cmds.ls(sl=1)
        cmds.spaceLocator(p=(0, 0, 0), n="LocatorSC")
        cmds.select("LocatorSC", r=1)
        cmds.select(nurbs, tgl=1)
        cmds.pathAnimation(upAxis='x', fractionMode=True, endTimeU=cmds.playbackOptions(query=1, maxTime=1),
                         startTimeU=cmds.playbackOptions(minTime=1, query=1), worldUpType="vector", inverseUp=False,
                         inverseFront=False, follow=True, bank=False, followAxis='y', worldUpVector=(0, 1, 0))
        LuJingJieDian = cmds.listConnections("LocatorSC.rx", s=1, d=0)
        cmds.disconnectAttr((LuJingJieDian[0] + "_uValue.output"), (LuJingJieDian[0] + ".uValue"))
        cmds.select(cl=1)
        for i in range(0, num + 1):
            number = 1.0 / num * i
            cmds.setAttr((LuJingJieDian[0] + ".uValue"), number)
            joint = cmds.joint(p=(0, 0, 0))
            cmds.delete(cmds.pointConstraint("LocatorSC", joint))
        cmds.delete("LocatorSC")

        cmds.undoInfo(cck=1)
    # 镜像骨骼
    def mirror_joint(self, axial):
        sel = cmds.ls(sl=1)
        for i in range(0, len(sel)):
            cmds.select(cl=1)
            joint = cmds.joint(p=(0, 0, 0))
            cmds.delete(cmds.pointConstraint(sel[i], joint, weight=1))
            if axial == "X":
                Num = float(cmds.getAttr(joint+".translateX"))
                cmds.setAttr(joint+".translateX", (Num * (-1)))
                cmds.select(sel[i], r=1)
                cmds.mirrorJoint(mirrorBehavior=1, mirrorYZ=1)
            if axial == "Y":
                Num = float(cmds.getAttr(joint+".translateY") * (-1))
                cmds.setAttr(joint+".translateY", Num)
                cmds.select(sel[i], r=1)
                cmds.mirrorJoint(mirrorBehavior=1, mirrorXZ=1)
            if axial == "Z":
                Num = float(cmds.getAttr(joint+".translateZ") * (-1))
                cmds.setAttr(joint+".translateZ", Num)
                cmds.select(sel[i], r=1)
                cmds.mirrorJoint(mirrorXY=1, mirrorBehavior=1)
            sel_a = cmds.ls(sl=1)
            cmds.delete(cmds.pointConstraint(joint, sel_a, weight=1))
            cmds.delete(joint)

    # 把所选线单独转化为样条
    def ChangeLineToSpline(self):
        Lint = cmds.ls(fl=1, sl=1)
        ModelName = []
        numTokens = ModelName = Lint[0].split(".")
        for i in range(0, len(Lint)):
            cmds.select(Lint[i])
            cmds.polyToCurve(conformToSmoothMeshPreview=0, degree=1, form=2)
            cmds.mel.rename("LingShiLint" + str(i))
            if i > 0:
                cmds.parent(("LingShiLintShape" + str(i)),
                          "LingShiLint0", s=1, add=1)
                cmds.delete("LingShiLint" + str(i))
        cmds.select('LingShiLint0', r=1)
        cmds.mel.CenterPivot()
        cmds.mel.rename(ModelName[0] + "Cur")

    # 在所选中心创建骨骼
    def centre_joint(self):
        cmds.undoInfo(ock=1)
        cluster = cmds.cluster()
        cmds.select(cl=1)
        joint = cmds.joint(p=(0, 0, 0))
        cmds.delete(cmds.parentConstraint(cluster[1], joint, weight=1))
        cmds.delete(cluster)
        cmds.undoInfo(cck=1)

    # 在中心建立骨骼链
    def create_centre_joint(self):
        cmds.undoInfo(ock=1)
        mel.eval('ConvertSelectionToVertices;')
        sel = cmds.ls(fl=1, sl=1)
        OldJoint = ''
        NewJoint = ''
        for i in range(0, len(sel)):
            cmds.select(sel[i], r=1)
            mel.eval('PolySelectConvert 2;')
            new_sel = cmds.ls(sl=1, fl=1)
            new_sel = [x for x in new_sel if x not in sel]
            cmds.select(new_sel[0])
            mel.eval('SelectContiguousEdges;')
            self.centre_joint()
            joint = cmds.ls(sl=1)
            OldJoint = NewJoint
            NewJoint = joint
            if len(OldJoint) != 0:
                cmds.parent(NewJoint, OldJoint)

        cmds.undoInfo(cck=1)

    # 自动父化
    def automatic_parenting(self):
        sel = cmds.ls(sl=1)
        cmds.undoInfo(ock=1)
        for i in range(0, (len(sel)-1)):
            cmds.parent(sel[i + 1], sel[i])
        cmds.undoInfo(cck=1)

    # 反转层次
    def reversa_arrangement(self):
        mel.eval('SelectHierarchy;')
        select = cmds.ls(sl=1)
        for i in range(1, len(select)):
            cmds.parent(select[i], w=1)
        for i in range(0, (len(select) - 1)):
            cmds.parent(select[i], select[i + 1])

    # 骨骼转样条
    def joint_transformation_curve(self):
        mel.eval('SelectHierarchy;')
        select = cmds.ls(sl=1)
        CurveP = ""
        for i in range(0, len(select)):
            cmds.spaceLocator(p=(0, 0, 0), n="LS_Loc")
            cmds.pointConstraint(select[i], "LS_Loc", weight=1)
            TX = str(cmds.getAttr("LS_Loc.translateX"))
            TY = str(cmds.getAttr("LS_Loc.translateY"))
            TZ = str(cmds.getAttr("LS_Loc.translateZ"))
            CP = (" -p " + TX + " " + " " + TY + " " + TZ)
            CurveP = CurveP + CP
            cmds.delete("LS_Loc")
        mel.eval("curve -d 3" + CurveP)

    # 插入骨骼
    def insert_joint(self,joint_num):
        sel = cmds.ls(sl=1)
        interval = 1.0/(float(joint_num)+1.0)
        all_joint = []
        all_joint.append(sel[0])
        cmds.undoInfo(ock=1)
        for i in range(1, int(joint_num)+1):
            cmds.select(cl=1)
            joint = cmds.joint(p=(0,0,0))
            pointConstraint = cmds.pointConstraint(sel[0], joint, weight=1)
            cmds.pointConstraint(sel[1], joint, weight=1)
            cmds.setAttr((pointConstraint[0] + '.' + sel[0] + 'W0'), 1 - (i * interval))
            cmds.setAttr((pointConstraint[0] + '.' + sel[1] + 'W1'), i * interval)
            cmds.delete(pointConstraint)
            all_joint.append(joint)
        all_joint.append(sel[1])
        for i in range(0, len(all_joint)):
            cmds.parent(all_joint[i+1],all_joint[i])
        cmds.undoInfo(cck=1)

    # 偏移属性
    def get_move_up_dn_attrs_proc(self, updn, objet_attrs):
        if objet_attrs:
            attrs = []
            objs = [objet_attrs[0].split(".")[0]]
            for at in objet_attrs:
                attrs.append(at.split(".")[-1])
            pass
        else:
            objs = cmds.ls(sl=1)
            attrs = cmds.channelBox('mainChannelBox', q=1, sma=1)
        ex = 0
        for j in range(0, len(objs)):
            obj = objs[j]
            for i in range(0, len(attrs)):
                attr = attrs[i]
                ex = int(cmds.objExists(obj + "." + attr))
                if ex == 0:
                    continue

                udAttrs = cmds.listAttr(obj, ud=1, u=1)
                index = -1
                for a in range(0, len(udAttrs)):
                    if attr == udAttrs[a]:
                        index = int(a)

                if index == -1:
                    continue

                indexUp = index - 1
                if indexUp < 0:
                    indexUp = index

                upAttr = udAttrs[indexUp]
                if updn == 1:
                    if index == 0:
                        continue

                    cmds.deleteAttr(obj + "." + upAttr)
                    cmds.undo()
                    for aa in range((index + 1), len(udAttrs)):
                        cmds.deleteAttr(obj + "." + udAttrs[aa])
                        cmds.undo()

                if updn == 0:
                    cmds.deleteAttr(obj + "." + attr)
                    cmds.undo()
                    dnSize = len(attrs)
                    for aa in range((index + dnSize + 1), len(udAttrs)):
                        cmds.deleteAttr(obj + "." + udAttrs[aa])
                        cmds.undo()

    # 隐藏选择属性
    def hide_selection_properties(self):
        QvDongYvan = cmds.ls(sl=1)
        LianJieYvan = cmds.channelBox('mainChannelBox', q=1, sma=1)
        for i in range(0, len(LianJieYvan)):
            cmds.setAttr((QvDongYvan[0] + "." + LianJieYvan[i]),
                       channelBox=False, keyable=False)

    # 显示默认属性
    def show_default_properties(self):
        QvDongYvan = cmds.ls(sl=1)
        LianJieYvan = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        for j in range(0, len(QvDongYvan)):
            for i in range(0, len(LianJieYvan)):
                cmds.setAttr((QvDongYvan[j] + "." + LianJieYvan[i]), k=True)

    # 修改默认属性名称
    def modify_default_attribute_names(self,name):
        sel = cmds.ls(sl=1)
        attrs = cmds.channelBox('mainChannelBox', q=1, sma=1)
        cmds.aliasAttr(name, sel[0]+'.'+attrs[0])

    # 隔行选线
    def interlaced_line_selection(self, select_type, num):
        if select_type == 1:
            mel.eval('polySelectEdgesEveryN \"edgeRing\" '+num+';')
        else:
            mel.eval('polySelectEdgesEveryN \"edgeLoop\" ' + num + ';')

    # 统一循环边骨骼权重
    def uniform_edge_loop_weights(self):
        sel = cmds.ls(sl=1, fl=1)
        cmds.ConvertSelectionToVertices()
        point = cmds.ls(sl=1, fl=1)
        soure = point[0].split('.')[0]

        source_skin_joint = []
        try:
            source_skin_joint = cmds.skinCluster(soure, q=1, inf=1)
        except:
            pass

        if source_skin_joint:
            source_shape = cmds.listRelatives(soure, s=1)
            source_skin_cluster = cmds.listConnections((source_shape[0] + '.inMesh'), d=1)
            for i in range(0, len(point)):
                cmds.select(point[i])
                soure_weight = cmds.skinPercent(source_skin_cluster[0], point[i], q=1, value=1)
                cmds.ConvertSelectionToEdges()
                s = cmds.ls(sl=1, fl=1)
                cmds.select(list(set(s).difference(set(sel))))
                s = cmds.ls(sl=1, fl=1)
                cmds.select(s[0])
                cmds.SelectEdgeLoopSp()
                cmds.ConvertSelectionToVertices()
                loop_point = cmds.ls(sl=1, fl=1)
                transformValue = []
                for i in range(0, len(source_skin_joint)):
                    new_list = [source_skin_joint[i], soure_weight[i]]
                    transformValue.append(new_list)
                cmds.skinPercent(source_skin_cluster[0], loop_point,
                                 transformValue=transformValue)
        else:
            cmds.warning('源没有蒙皮。')

    # 显影骨骼
    def set_bone_display(self):
        joint = []
        try:
            joint = cmds.ls(sl=1,typ="joint")
        except:
            pass
        if not joint:
            joint = cmds.ls(typ="joint")
        joint_type = int(cmds.getAttr(joint[0] + ".drawStyle"))
        if joint_type == 0:
            for i in range(0, len(joint)):
                cmds.setAttr((joint[i] + ".drawStyle"), 2)
        else:
            for i in range(0, len(joint)):
                cmds.setAttr((joint[i] + ".drawStyle"), 0)

    # 按循环边中心创建骨骼
    def establishing_a_bone_chain_at_the_midline(self):
        sel = cmds.ls(sl=1, fl=1)
        mel.eval('ConvertSelectionToVertices;')
        point = cmds.ls(sl=1, fl=1)
        first_point = []
        # 获取端点
        for p in point:
            cmds.select(p)
            mel.eval('GrowLoopPolygonSelectionRegion;')
            s = cmds.ls(sl=1, fl=1)
            cmds.select(list(set(s) & (set(point))))
            s = cmds.ls(sl=1, fl=1)
            if len(s) < 3:
                first_point = p
                break
        old_point = []
        previous_one_joint = []
        next_joint = []

        for i in range(0, len(point)):
            if i == 0:
                cmds.select(first_point)
            else:
                cmds.select(next_joint)
            new_select_joint = cmds.ls(sl=1, fl=1)
            mel.eval('ConvertSelectionToVertexPerimeter;')
            s = cmds.ls(sl=1, fl=1)
            cmds.select(list(set(s) & (set(point))))
            s = cmds.ls(sl=1, fl=1)
            cmds.select(list(set(s).difference(set(new_select_joint))))
            s = cmds.ls(sl=1, fl=1)
            cmds.select(list(set(s).difference(set(old_point))))
            old_point.append(new_select_joint[0])
            next_joint = cmds.ls(sl=1, fl=1)

            cmds.select(new_select_joint)
            mel.eval('ConvertSelectionToEdges;')
            s = cmds.ls(sl=1, fl=1)
            cmds.select(list(set(s).difference(set(sel))))
            s = cmds.ls(sl=1, fl=1)
            cmds.select(s[0])
            mel.eval('SelectEdgeLoopSp;')
            mel.eval('ConvertSelectionToVertices;')
            loop_point = cmds.ls(sl=1, fl=1)
            cmds.select(loop_point)
            cluster = cmds.cluster()
            cmds.select(cl=1)
            joint = cmds.joint(p=(0, 0, 0))
            cmds.delete(cmds.pointConstraint(cluster, joint, w=1))
            cmds.delete(cluster)

            if i > 0:
                cmds.parent(joint, previous_one_joint)
            previous_one_joint = joint

    # 毛囊约束
    def follicle_constraint(self, model, sel, keep):
        cmds.undoInfo(ock=1)
        cmds.select(cl=1)
        if not cmds.objExists('AllFollicle_Grp'):
            cmds.group(em=1,n='AllFollicle_Grp')
        shape = cmds.listRelatives(model, s=1)
        TypeMesh = cmds.ls(shape[0], type='mesh')
        if TypeMesh:
            cmds.createNode('closestPointOnMesh', n=("cpom"))
            cmds.connectAttr((shape[0] + '.outMesh'), ('cpom' + '.inMesh'), f=1)
        TypeNurbs = cmds.ls(shape[0], type='nurbsSurface')
        if TypeNurbs:
            cmds.createNode('closestPointOnSurface', n=("cpom"))
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), ('cpom' + '.inputSurface'), f=1)
        cmds.spaceLocator(p=(0, 0, 0), n=("Loc"))
        for i in range(0, len(sel)):
            cmds.delete(cmds.pointConstraint(sel[i], "Loc", weight=1, offset=(0, 0, 0)))
            pos = cmds.xform(("Loc"), q=1, a=1, ws=1, t=1)
            cmds.setAttr(("cpom" + ".inPositionX"), pos[0])
            cmds.setAttr(("cpom" + ".inPositionY"), pos[1])
            cmds.setAttr(("cpom" + ".inPositionZ"), pos[2])
            u = float(cmds.getAttr("cpom" + ".parameterU"))
            v = float(cmds.getAttr("cpom" + ".parameterV"))
            cmds.createNode('follicle', n=(sel[i] + "_follicleShape"))
            if TypeMesh:
                shape = cmds.listRelatives(model, s=1, type='mesh')
                cmds.connectAttr((shape[0] + ".outMesh"), (sel[i] + "_follicleShape" + ".inputMesh"), f=1)
                cmds.connectAttr((shape[0] + ".worldMatrix[0]"),
                               (sel[i] + "_follicleShape" + ".inputWorldMatrix"), f=1)
            if TypeNurbs:
                shape = cmds.listRelatives(model, s=1, type='nurbsSurface')
                cmds.connectAttr((shape[0] + '.worldSpace[0]'), (sel[i] + '_follicleShape' + '.inputSurface'), f=1)
                cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (sel[i] + '_follicleShape' + '.inputWorldMatrix'),
                               f=1)
            cmds.connectAttr((sel[i] + "_follicleShape" + ".outTranslate"), (sel[i] + "_follicle" + ".translate"),
                           f=1)
            cmds.connectAttr((sel[i] + "_follicleShape" + ".outRotate"), (sel[i] + "_follicle" + ".rotate"), f=1)
            cmds.setAttr((sel[i] + "_follicleShape" + ".parameterU"), u)
            cmds.setAttr((sel[i] + "_follicleShape" + ".parameterV"), v)
            if keep == True:
                if not i == 'FaceLoc_head_loc_M':
                    cmds.parentConstraint((sel[i] + "_follicle"), sel[i], mo=1, weight=1)
            else:
                cmds.parentConstraint((sel[i] + "_follicle"), sel[i], weight=1)
            if cmds.objExists('AllFollicle_Grp'):
                cmds.parent((sel[i] + "_follicle"), 'AllFollicle_Grp')
        cmds.delete("Loc")
        cmds.delete("cpom")
        cmds.undoInfo(cck=1)
        # ZKM_FollicleClass().ZKM_FollicleConstraint('bace_bs_Mesh',['nurbsCircle1','nurbsCircle2'],'Ture')

    # 切换蒙皮模型手影响状态
    def switch_skin_model_hand_influence_state(self):
        all_head = cmds.headsUpDisplay(q=1, lh=1)
        # need_occupy = []
        # for s in all_head:
        #     selecct = cmds.headsUpDisplay(s, q=1, section=1)
        #     block = cmds.headsUpDisplay(s, q=1, block=1)
        #     vis = cmds.headsUpDisplay(s, q=1, vis=1)
        #     date = [selecct,block, vis]
        #     if vis == 0:
        #         need_occupy.append(date)
        skin = cmds.ls(type='skinCluster')
        # print(need_occupy)
        if 'HUD_self_head' in all_head:
            # mel.eval('moveJointsMode 0;')
            for s in skin:
                cmds.skinCluster(s, moveJointsMode=0, e=1)
            cmds.headsUpDisplay('HUD_self_head', rem=1)
            print('蒙皮已经解除锁定')
        else:
            # mel.eval('moveJointsMode 1;')
            for s in skin:
                cmds.skinCluster(s, moveJointsMode=1, e=1)
            try:
                cmds.headsUpDisplay(rp=[2,5])
            except:
                pass
            cmds.headsUpDisplay('HUD_self_head', section=2, block=5, blockSize='medium', label='蒙皮已禁用', labelFontSize='large')

    # 以下是清理模型 #
    # 清理枢轴
    def cleaning_the_pivot(self):
        sel = cmds.ls()
        for i in range(0, len(sel)):
            if cmds.objExists(sel[i] + ".displayRotatePivot"):
                cmds.setAttr((sel[i] + ".displayRotatePivot"), 0)
            if cmds.objExists(sel[i] + ".displayScalePivot"):
                cmds.setAttr((sel[i] + ".displayScalePivot"), 0)
            if cmds.objExists(sel[i] + ".displayHandle"):
                cmds.setAttr((sel[i] + ".displayHandle"), 0)
            if cmds.objExists(sel[i] + ".displayLocalAxis"):
                cmds.setAttr((sel[i] + ".displayLocalAxis"), 0)
        cmds.warning('清理枢轴完成')

    # 清理所有bs组
    def clean_up_invalid_BS_groups(self):
        blendShape = cmds.ls(type='blendShape')
        cmds.delete(blendShape)
        attribute = cmds.ls('shapeEditorManager.blendShapeDirectory[*]')
        for i in range(0, len(attribute)):
            cmds.removeMultiInstance(attribute[i], b=True)
        cmds.warning('清理bs完成')

    # 简单模型清理
    def cleaning_the_model(self):
        cmds.undoInfo(ock=1)
        sel = cmds.ls(sl=1)
        # 清理模型显示
        cmds.polyOptions(ae=1, cm='diffuse', uvt=0, dcv=0, cs=0, gl=1, suv=4, duv=0, dn=0, bc=1, dce=0, db=0,
                         din=(0, 0, 0, 0), dc=0, dv=0, dw=0, dt=0, dmb=0, mb='overwrite', dif=1, sv=3, facet=1,
                         sn=0.4,
                         sb=3, bcv=1)
        mel.eval('updateSMPAttrs(0, 0, 2, 0, 1, 1, 0, 1, 0, 0, 1);')
        # 重置模型显示
        cmds.PolyDisplayReset()
        # maya自带模型清理
        mel.eval(
            'polyCleanupArgList 4 { "1","1","1","0","1","1","1","0","1","1e-05","1","1e-05","0","1e-05","0","1","1","1" };')
        cmds.select(sel)
        mel.eval('DeleteHistory;')
        ffd = cmds.lattice(divisions=(2, 2, 2), ldv=(2, 2, 2), objectCentered=True)
        cmds.select(ffd[1])
        mel.eval('DeleteHistory;')
        cmds.delete(ffd)
        cmds.warning('简单清理模型完成。')
        cmds.select(sel)
        cmds.undoInfo(cck=1)

    # 清理动画节点
    def cleaning_the_animation_nodes(self):
        animCurveTU = cmds.ls(type='animCurveTU')
        animCurveTL = cmds.ls(type='animCurveTL')
        animCurveTA = cmds.ls(type='animCurveTA')
        animLayer = cmds.ls(type='animLayer')
        cmds.delete(animCurveTU, animCurveTL, animCurveTA, animLayer)
        cmds.warning('清理动画节点完成')

    # 清理显示层
    def cleaning_the_display_layers(self):
        displayLayer = cmds.ls(type='displayLayer')
        # 删除displayLayer列表中defaultLayer的元素
        displayLayer.remove('defaultLayer')
        if displayLayer:
            cmds.delete(displayLayer)

    # 文件清理
    def cleaning_the_file(self):
        sel = cmds.ls(sl=1)
        soure_file_node = str(len(cmds.ls()))
        if sel:
            # 导出当前选择
            cmds.select(sel)
            # 获取当前文件的路径
            current_file_path = cmds.file(q=True, loc=True)
            try:
                current_file_path = current_file_path.decode('utf-8')
            except:
                pass
            cmds.file((current_file_path[:-3] + '_Clear.mb'), pr=1, typ="mayaBinary", force=1, options="v=0;", es=1)
            cmds.file((current_file_path[:-3] + '_Clear.mb'), ignoreVersion=1, typ="mayaBinary", options="v=0;",
                      o=1, f=1)
            all_node = cmds.ls()
            cmds.warning('清理文件完成,原有' + soure_file_node + '个节点，现有' + str(len(all_node)) + '个节点。')
        else:
            cmds.warning('请先选择要保留的文件')

    # 检查自穿插
    def check_self_intersect(self):
        mel.eval('SelectHierarchy;')
        sel = cmds.ls(sl=1, type='mesh')
        pfxToonNode = 'pfxToonCollisionDetectShape'
        if not cmds.objExists('pfxToonCollisionDetectShape'):
            pfxToonNode = cmds.createNode('pfxToon', n='pfxToonCollisionDetectShape')
        cmds.setAttr(pfxToonNode + '.drawAsMesh', 1)
        cmds.setAttr(pfxToonNode + '.profileLines', 0)
        cmds.setAttr(pfxToonNode + '.creaseLines', 0)
        cmds.setAttr(pfxToonNode + '.intersectionLines', 1)
        cmds.setAttr(pfxToonNode + '.displayPercent', 100)
        cmds.setAttr(pfxToonNode + '.intersectionColor', 1, 0, 0, type='double3')
        cmds.setAttr(pfxToonNode + '.selfIntersect', 1)
        i = 0
        for s in sel:
            cmds.connectAttr(s + '.outMesh', pfxToonNode + '.inputSurface[' + str(i) + '].surface', f=True)
            cmds.connectAttr(s + '.worldMatrix[0]', pfxToonNode + '.inputSurface[' + str(i) + '].inputWorldMatrix',
                             f=True)
            i += 1
    # 查询对称点
    def mirror_point(self):
        sel = cmds.ls(sl=1)
        all_point = cmds.ls(sel[0] + '.vtx[*]', fl=1)
        point_dic_list = []
        for p in all_point:
            pos = cmds.xform(p, q=1, ws=1, t=1)
            dic = {'point': p, 'num': pos}
            point_dic_list.append(dic)
        range_num = 0.001
        mirror_point = []
        while point_dic_list:
            p_1_dic = point_dic_list.pop()
            if (0 - range_num) <= p_1_dic['num'][0] <= (0 + range_num):
                mirror_point.append(p_1_dic['point'])
            else:
                for p_2_dic in point_dic_list:
                    if (-1 * p_1_dic['num'][0] - range_num) <= p_2_dic['num'][0] <= (-1 * p_1_dic['num'][0] + range_num):
                        if (p_1_dic['num'][1] - range_num) <= p_2_dic['num'][1] <= (p_1_dic['num'][1] + range_num):
                            if (p_1_dic['num'][2] - range_num) <= p_2_dic['num'][2] <= (p_1_dic['num'][2] + range_num):
                                mirror_point.append(p_1_dic['point'])
                                mirror_point.append(p_2_dic['point'])
                                point_dic_list.remove(p_2_dic)
        return sel, all_point, mirror_point

    # 修复对称
    def fix_symmetry(self):
        '''# 判断必须插件是否获取
        pluginInfo = cmds.pluginInfo(listPlugins=True, q=True)
        have_meshReorder = 0
        for p in pluginInfo:
            if 'meshReorder' == p:
                have_meshReorder = 1
        if have_meshReorder == 0:
            cmds.loadPlugin('meshReorder')
        # 关闭基础设置
        mel.eval('reflectionSetMode none;')
        sel, all_point, mirror_point = self.mirror_point()
        if len(mirror_point) > 3:
            cmds.refresh()
            cmds.select(mirror_point, r=1)
            mel.eval('ConvertSelectionToFaces;')
            # 获取对称的面
            mirror_face = cmds.ls(sl=1,fl=1)
            # 在对称的面中查询四个坐标的x轴都在z轴负方向上
            l_one_face_point = []
            for f in mirror_face:
                cmds.select(f)
                mel.eval('ConvertSelectionToVertices;')
                correction_point_sequence_point = cmds.ls(sl=1, fl=1)
                i = 0
                for p in correction_point_sequence_point:
                    pos = cmds.xform(p, q=1, ws=1, t=1)
                    if pos[0] >= 0:
                        i = 1
                        break
                if i == 0:
                    # 选择需要矫正点序列的一半点
                    l_one_face_point = correction_point_sequence_point
                    break
            cmds.select(l_one_face_point)
            mel.eval('reflectionSetMode objectx;')
            r_one_face_point = []
            for i in range(0, 3):
                cmds.select(l_one_face_point[i], sym=1, r=1)
                two_point = cmds.ls(sl=1, fl=1)
                other_point = [item for item in two_point if item not in l_one_face_point[i]]
                if other_point:
                    r_one_face_point.append(other_point[0])
            mel.eval('reflectionSetMode none;')
            # 拆解数字
            r_one_face_point_num = []
            for i in range(0, 3):
                r_one_face_point_num.append(r_one_face_point[i].split('[')[-1][:-1])
            # 复制模型
            cmds.select(sel)
            cmds.duplicate(rr=1)
            copy_model = cmds.ls(sl=1, fl=1)
            cmds.setAttr((copy_model[0] + '.scaleX'), -1)
            cmds.makeIdentity(n=0, s=1, r=1, t=1, apply=True, pn=1)
            shape = cmds.listRelatives(copy_model[0], s=1)
            cmds.meshRemap(l_one_face_point[0], l_one_face_point[1], l_one_face_point[2],
                           (shape[0] + '.vtx[' + r_one_face_point_num[0] + ']'),
                           (shape[0] + '.vtx[' + r_one_face_point_num[1] + ']'),
                           (shape[0] + '.vtx[' + r_one_face_point_num[2] + ']'))
            # 查询x轴负方向点
            all_point_L = []
            for p in all_point:
                pos = cmds.xform(p, q=1, ws=1, t=1)
                if pos[0] > 0:
                    all_point_L.append(p)
            # 建立混合变形
            blendShape = cmds.blendShape(copy_model[0], all_point_L, frontOfChain=1, tc=0)
            cmds.setAttr((blendShape[0] + '.' + copy_model[0]), 1)
            cmds.select(sel)
            mel.eval('DeleteHistory;')
            cmds.delete(copy_model)
            cmds.select(sel)
            ffd = cmds.lattice(divisions=(2, 2, 2), ldv=(2, 2, 2), objectCentered=True)
            cmds.select(ffd[1])
            mel.eval('DeleteHistory;')
            cmds.delete(ffd)
            cmds.select(sel)
            cmds.warning('对称修复完成。')
        else:
            cmds.warning('模型至少需要有一个三角面对称。')'''
        cmds.undoInfo(ock=1)
        '''sel_f = cmds.ls(sl=1, fl=1)
        mesh = sel_f[0].split('.')[0]
        cmds.select(mesh)
        mesh = cmds.ls(sl=1)
        copy_mesh = cmds.duplicate(mesh)

        cmds.setAttr(mesh[0] + '.rotatePivot', 0, 0, 0)
        cmds.setAttr(mesh[0] + '.scalePivot', 0, 0, 0)
        cmds.select(mesh[0] + '.f[*]')
        cmds.scale(1e-05, 0, 0, r=1, ws=1)

        blendShape = cmds.blendShape(copy_mesh, mesh)

        cmds.setAttr(blendShape[0] + '.' + copy_mesh[0], 1)
        cmds.select(cl=1)
        cmds.symmetricModelling(sel_f[0], e=1, ts=True)
        cmds.select(sel_f)
        cmds.blendShape(blendShape[0] + '.' + copy_mesh[0], ss=0, md=1, sa="x", e=1, mt=(0, 0))
        cmds.select(mesh)
        cmds.DeleteHistory()
        cmds.delete(copy_mesh)
        cmds.symmetricModelling(s=0)'''
        sel_f = cmds.ls(sl=1, fl=1)
        mesh = [sel_f[0].split('.')[0]]
        point = cmds.ls(mesh[0] + '.vtx[*]', fl=1)
        r_point = []
        for p in point:
            pos = cmds.xform(p, q=1, ws=1, t=1)
            if pos[0] < 0.001:
                r_point.append(p)
        str_r_point = str(r_point)[1:-2]
        new_s = str_r_point.replace("'", "\"")
        for f in sel_f:
            cmds.select(f)
            common = ('activateTopoSymmetry("' + f + '", {' + new_s + '"}, {"' + mesh[0] + '"}, "facet", "dR_symmetrize", 1);')
            mel.eval(common)
        cmds.select(cl=1)
        cmds.undoInfo(cck=1)

    # 清理空间名
    def clean_namespace(self):
        namespace = cmds.namespaceInfo(lon=True, r=1)
        namespace = [x for x in namespace if x not in ['UI', 'shared']]
        for i in range(0, len(namespace)):
            cmds.namespace(removeNamespace=namespace[len(namespace) - i - 1], mergeNamespaceWithRoot=1)
        cmds.warning('清理命名空间完成。')

    # 清理点吸附数值为nan的模型
    def clean_adsorption_num_nan(self):
        cmds.undoInfo(ock=1)
        sel = cmds.ls(sl=1)
        cube = cmds.polyCube(sz=1, sy=1, sx=1, d=1, cuv=4, h=1, ch=0, w=1, ax=(0, 1, 0))
        face = cmds.ls(cube[0] + '.f[*]')
        cmds.sets(face, name='need_delete_face')
        cmds.polyUnite(cube[0], sel[0], centerPivot=1, ch=0, mergeUVSets=1, name='need_rename_cube')
        face = cmds.sets('need_delete_face', q=1)
        cmds.delete(face)
        cmds.rename('need_rename_cube', sel[0])
        cmds.delete('need_delete_face')
        cmds.select(sel[0])
        mel.eval('DeleteHistory;')
        cmds.warning('清理吸附数值为nan的模型完成。')
        cmds.undoInfo(cck=1)

    # 骨骼权重规范为游戏规范（0.01）
    def joint_weight_to_game_specification(self):
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

    # 独立生成指定名称字符形状样条
    def create_str_shape_curve(self,text):
        cmds.undoInfo(ock=1)
        top_grp = cmds.textCurves(t=text)
        cmds.duplicate()
        sel = cmds.ls(sl=1)
        cmds.delete(top_grp[0])
        mel.eval('SelectHierarchy;')
        mel.eval('FreezeTransformations')

        shape = cmds.ls(sl=1,type='nurbsCurve')
        grp = cmds.ls(sl=1, type='transform')
        cmds.parent(shape,sel[0],s=1,add=1)
        cmds.delete(grp[1:])
        cmds.undoInfo(cck=1)

        return grp[0]

    # 路径约束
    def path_constraint(self,curve,follow_target):
        shape = cmds.listRelatives(curve, s=1)
        motion_path = cmds.shadingNode('motionPath', asUtility=1)
        cmds.connectAttr((shape[0] + '.worldSpace[0]'), (motion_path + '.geometryPath'), f=1)
        cmds.setAttr(motion_path + '.fractionMode', 1)
        cmds.setAttr(motion_path + '.follow', 1)
        cmds.setAttr(motion_path + '.sideTwist', l=False)
        cmds.setAttr(motion_path + '.upTwist', l=False)
        cmds.setAttr(motion_path + '.frontTwist', l=False)
        cmds.setAttr(motion_path + '.frontAxis', 0)
        cmds.setAttr(motion_path + '.upAxis', 1)
        cmds.connectAttr((motion_path + '.message'), (follow_target + '.specifiedManipLocation'), f=1)
        for axle in ['X', 'Y', 'Z']:
            addDoubleLinear = cmds.shadingNode('addDoubleLinear', asUtility=1)
            cmds.connectAttr((follow_target + '.transMinusRotatePivot' + axle), (addDoubleLinear + '.input1'), f=1)
            if axle == 'X':
                cmds.connectAttr((motion_path + '.xCoordinate'), (addDoubleLinear + '.input2'), f=1)
            if axle == 'Y':
                cmds.connectAttr((motion_path + '.yCoordinate'), (addDoubleLinear + '.input2'), f=1)
            if axle == 'Z':
                cmds.connectAttr((motion_path + '.zCoordinate'), (addDoubleLinear + '.input2'), f=1)
            cmds.connectAttr((addDoubleLinear + '.output'), (follow_target + '.translate' + axle), f=1)
            cmds.connectAttr((motion_path + '.rotate' + axle), (follow_target + '.rotate' + axle), f=1)
        return motion_path

    # Author:D-Key 陈逆
    def load_source(self,name,location):
        version = float('%d.%d' % sys.version_info[:2])
        if version < 3.4:
            from imp import load_source
            return load_source(name,location)
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location(name,location)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module