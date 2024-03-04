#coding=gbk
import pymel.core as pm
import sys
sys.path.append(r'Z:\1.Private folder\Rig\zhankangming\ZhanKangMing\ZhanKangMing\Maya\MayaWeight')
# 加载文本
from JointWeightProcessing import *
#导出权重
pm.select('geo_GRP')
pm.mel.SelectHierarchy()
mesh = pm.ls(sl=1,type='mesh')
pm.select(mesh)
pm.pickWalk(d='up')
sel_mesh = pm.ls(sl=1)
ZKM_JointWeightProcessingClass().ExportWeight(sel_mesh)
#新建新骨骼
pm.select("Root_M", r=1)
pm.duplicate(rr=1)
pm.mel.SelectHierarchy()
sel = pm.ls(sl=1)
for i in range(0, len(sel)):
    pm.select(sel[-1*i])
    buffer = sel[-1*i].split("|")
    pm.rename(sel[-1*i],buffer[-1] + "_Copy")
pm.rename("Root_M1_Copy", "Root_M_Copy")
pm.setAttr("Root_M_Copy.inheritsTransform", 0)
#链接骨骼
pm.select("Root_M")
pm.mel.SelectHierarchy()
sel_1 = pm.ls(sl=1)
pm.select("Root_M_Copy")
pm.mel.SelectHierarchy()
sel_2 = pm.ls(sl=1)
for i in range(0, len(sel_1)):
    pm.connectAttr((sel_1[i] + ".translate"), (sel_2[i] + ".translate"),f=1)
    pm.connectAttr((sel_1[i] + ".rotate"), (sel_2[i] + ".rotate"),f=1)
    pm.connectAttr((sel_1[i] + ".scale"), (sel_2[i] + ".scale"),f=1)
#约束模型组
pm.parentConstraint('Main','geo_GRP',mo=1, weight=1)
pm.scaleConstraint('Main','geo_GRP',mo=1, weight=1)
#将旧骨骼改名
for i in range(0, len(sel_1)):
    pm.rename(sel_1[i],sel_1[i]+'_old')
for i in range(0, len(sel_2)):
    pm.rename(sel_2[i],sel_2[i][:-5])
ZKM_JointWeightProcessingClass().ImportWeight(sel_mesh)





#表情修改
sel_md = pm.ls(sl=1)
ZKM_JointWeightProcessingClass().ExportWeight(sel_md)
AllFace = ['Eye_R','Eye_L','upperTeethJoint_M','lowerTeethJoint_M']
for sel in AllFace:
    parent = pm.listRelatives(sel,parent=1)
    str_sel = str(sel)
    pm.rename(sel,sel+'_Old')
    pm.select(cl=1)
    pm.joint(p=(0, 0, 0),n=str_sel)
    grp = pm.mel.doGroup(0, 1, 1)
    pm.rename(grp,str_sel+'_Grp')
    pm.connectAttr((sel+'_Old.translate'), (str_sel + '.translate'), f=1)
    pm.connectAttr((sel+'_Old.rotate'), (str_sel + '.rotate'), f=1)
    pm.connectAttr((sel+'_Old.scale'), (str_sel + '.scale'), f=1)
    pm.delete(pm.parentConstraint(parent,str_sel+'_Grp'))
    pm.delete(pm.scaleConstraint(parent, str_sel + '_Grp'))


Tongue = ['Tongue0Joint_M','Tongue1Joint_M','Tongue2Joint_M','Tongue3Joint_M']
for sel in Tongue:
    parent = pm.listRelatives(sel, parent=1)
    str_sel = str(sel)
    pm.rename(sel, sel + '_Old')
    pm.select(cl=1)
    pm.joint(p=(0, 0, 0),n=str_sel)
    grp = pm.mel.doGroup(0, 1, 1)
    pm.rename(grp, str_sel + '_Grp')
    pm.connectAttr((sel + '_Old.translate'), (str_sel + '.translate'), f=1)
    pm.connectAttr((sel + '_Old.rotate'), (str_sel + '.rotate'), f=1)
    pm.connectAttr((sel + '_Old.scale'), (str_sel + '.scale'), f=1)
    pm.delete(pm.parentConstraint(parent, str_sel + '_Grp'))
    pm.delete(pm.scaleConstraint(parent, str_sel + '_Grp'))
pm.parent('Tongue1Joint_M_Grp','Tongue0Joint_M_Grp')
pm.parent('Tongue2Joint_M_Grp','Tongue1Joint_M_Grp')
pm.parent('Tongue3Joint_M_Grp','Tongue2Joint_M_Grp')
pm.disconnectAttr('Tongue0Joint_M_Old.translate', 'Tongue0Joint_M.translate')
pm.disconnectAttr('lowerTeethJoint_M_Old.translate', 'lowerTeethJoint_M.translate')
pm.disconnectAttr('upperTeethJoint_M_Old.translate', 'upperTeethJoint_M.translate')
ZKM_JointWeightProcessingClass().ImportWeight(sel_md)
pm.parentConstraint('Head_M_old','SkinAttachMesh',mo=1, weight=1)
pm.scaleConstraint('Head_M_old','SkinAttachMesh',mo=1, weight=1)
pm.parentConstraint('Head_M_old','eye_all',mo=1, weight=1)
pm.scaleConstraint('Head_M_old','eye_all',mo=1, weight=1)




pm.mel.eval('CBunlockAttr \"tongue.tx\";')
pm.mel.eval('CBunlockAttr \"tongue.ty\";')
pm.mel.eval('CBunlockAttr \"tongue.tz\";')
pm.mel.eval('CBunlockAttr \"tongue.rx\";')
pm.mel.eval('CBunlockAttr \"tongue.ry\";')
pm.mel.eval('CBunlockAttr \"tongue.rz\";')
pm.mel.eval('CBunlockAttr \"tongue.sx\";')
pm.mel.eval('CBunlockAttr \"tongue.sy\";')
pm.mel.eval('CBunlockAttr \"tongue.sz\";')


pm.parentConstraint('Tongue1_M','tongue',mo=1, weight=1)

#coding=gbk
import pymel.core as pm
#按顺序选择链接源骨骼
sel_1 = pm.ls(sl=1)
#按顺序选择链接目标骨骼
sel_2 = pm.ls(sl=1)
for i in range(0, len(sel_1)):
    pm.connectAttr((sel_1[i]+'.translate'), (sel_2[i] + '.translate'), f=1)
    pm.connectAttr((sel_1[i]+'.rotate'), (sel_2[i] + '.rotate'), f=1)
    pm.connectAttr((sel_1[i]+'.scale'), (sel_2[i] + '.scale'), f=1)




























# 自动生成初级翅膀
sel = pm.select(ls=1)
pm.select(sel[0])
Curve = pm.select(ls=1)
pm.select(sel[1:])
Joint = pm.select(sl=1)

nearestPointOnCurve = pm.createNode("nearestPointOnCurve")
shapes = cmds.listRelatives(C)[0]
pm.connectAttr((shapes + '.worldSpace[0]'), (nearestPointOnCurve + '.inputCurve'), f=1)
pm.setAttr((nearestPointOnCurve+'.inPositionX'), Place[0])
pm.setAttr((nearestPointOnCurve+'.inPositionY'), Place[1])
pm.setAttr((nearestPointOnCurve+'.inPositionZ'), Place[2])
U = pm.getAttr((nearestPointOnCurve + '.parameter'))
pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'))































def PresetTemplateWingCreateWingDrive():
    #添加基础目标约束部分
    WingDrivePrefix = cmds.textFieldButtonGrp('WingDrivePrefix', q=1, text=1)
    ShoulderElbowWrist = cmds.textFieldButtonGrp('WingDriveShoulderElbowWristJoint', q=1, text=1).split(',')
    Shoulder = ShoulderElbowWrist[0]
    Elbow = ShoulderElbowWrist[1]
    Wrist = ShoulderElbowWrist[2]
    AllGeneralJoint = [Wrist,Elbow,Shoulder]
    PrimaryFlyingFeather = cmds.textFieldButtonGrp('WingDrivePrimaryFlyingFeatherCurve', q=1, text=1).split(',')
    SecondaryFeather = cmds.textFieldButtonGrp('WingDriveSecondaryFeatherCurve', q=1, text=1).split(',')
    LevelThreeFlyingFeather = cmds.textFieldButtonGrp('WingDriveLevelThreeFlyingFeatherCurve', q=1, text=1).split(',')
    GeneralControlPrimaryFlyingFeatherPoint = cmds.textFieldButtonGrp('WingDriveGeneralControlPrimaryFlyingFeatherPoint', q=1, text=1).split(',')
    GeneralControlSecondaryFeatherPoint = cmds.textFieldButtonGrp('WingDriveGeneralControlSecondaryFeatherPoint', q=1, text=1).split(',')
    GeneralControlLevelThreeFlyingFeatherPoint = cmds.textFieldButtonGrp('WingDriveGeneralControlLevelThreeFlyingFeatherPoint', q=1, text=1).split(',')
    GeneralControl = []
    if GeneralControlPrimaryFlyingFeatherPoint:
        GeneralControl = GeneralControlPrimaryFlyingFeatherPoint[0].split('.')
        GeneralControl = pm.listRelatives(GeneralControl[0],p=1)
    if GeneralControlSecondaryFeatherPoint:
        GeneralControl = GeneralControlSecondaryFeatherPoint[0].split('.')
        GeneralControl = pm.listRelatives(GeneralControl[0], p=1)
    if GeneralControlLevelThreeFlyingFeatherPoint:
        GeneralControl = GeneralControlLevelThreeFlyingFeatherPoint[0].split('.')
        GeneralControl = pm.listRelatives(GeneralControl[0], p=1)
    ShoulderWristChain = cmds.textFieldButtonGrp('WingDriveShoulderWristChainCurve', q=1, text=1).split(',')
    AllSecondaryCurve = [PrimaryFlyingFeather,SecondaryFeather,LevelThreeFlyingFeather]
    if Shoulder and Elbow and Wrist:
        AllFeatherControlGrp = []
        j=0
        for Lis in [PrimaryFlyingFeather,SecondaryFeather,LevelThreeFlyingFeather]:
            for C in Lis:
                if pm.objExists(C + '.Joint') and pm.objExists(C + '.Curve'):
                    AllName = pm.attributeQuery('Joint', node=C, listEnum=1)
                    AllJoint = AllName[0].split(':')
                    AllName = pm.attributeQuery('Curve', node=C, listEnum=1)
                    AllCurve = AllName[0].split(':')
                    for i in range(0,len(AllJoint)):
                        #创建对应位置的定位器在曲线上
                        Place = cmds.xform(AllJoint[i], query=True, worldSpace = 1, translation=True)
                        nearestPointOnCurve = pm.createNode("nearestPointOnCurve")
                        shapes = cmds.listRelatives(C)[0]
                        pm.connectAttr((shapes + '.worldSpace[0]'), (nearestPointOnCurve + '.inputCurve'), f=1)
                        pm.setAttr((nearestPointOnCurve+'.inPositionX'), Place[0])
                        pm.setAttr((nearestPointOnCurve+'.inPositionY'), Place[1])
                        pm.setAttr((nearestPointOnCurve+'.inPositionZ'), Place[2])
                        U = pm.getAttr((nearestPointOnCurve + '.parameter'))
                        pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'))
                        pm.setAttr(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc.v',0)
                        pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.2, tol=0.01, nr=(1, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_Curve'))
                        pm.parent((WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'),(WingDrivePrefix + C + AllJoint[i] + '_Curve'))
                        #pm.parentConstraint((C + AllJoint[i] + '_CurveLoc'), (C + AllJoint[i] + '_Curve'))
                        pm.select((WingDrivePrefix + C + AllJoint[i] + '_Curve'))
                        pm.group(n=(WingDrivePrefix + C + AllJoint[i] + '_Grp2'))
                        pm.group(n=(WingDrivePrefix + C + AllJoint[i] + '_Grp1'))
                        Loc = pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_Loc'))
                        pm.setAttr((WingDrivePrefix + C + AllJoint[i] + '_Loc.v'), 0)
                        pm.parentConstraint((WingDrivePrefix + C + AllJoint[i] + '_Loc'),(WingDrivePrefix + C + AllJoint[i] + '_Grp1'),weight=1)
                        motionPath = pm.pathAnimation(Loc,C,upAxis='y', fractionMode=True,
                                                      endTimeU=pm.playbackOptions(query=1, maxTime=1),
                                                      startTimeU=pm.playbackOptions(minTime=1, query=1),
                                                      worldUpObject=AllGeneralJoint[j], worldUpType="objectrotation", inverseUp=False,
                                                      inverseFront=False, follow=True, bank=False, followAxis='x',
                                                      worldUpVector=(0, 1, 0))
                        pm.disconnectAttr((motionPath + "_uValue.output"), (motionPath + ".uValue"))
                        pm.setAttr((motionPath + ".uValue"),U)
                        Parent=pm.listRelatives(AllCurve[i],p=1)
                        pm.select(Parent)
                        pm.rename(pm.mel.doGroup(0, 1, 1),(WingDrivePrefix + C + AllCurve[i] + '_WingAimGrp'))
                        pm.aimConstraint((WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'), (WingDrivePrefix + C + AllCurve[i] + '_WingAimGrp'), weight=1,
                                         upVector=(0, 1, 0), mo=1, worldUpObject=(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'), worldUpType="objectrotation",
                                         aimVector=(1, 0, 0), worldUpVector=(-1, 0, 0))
                        pm.select(Loc,(WingDrivePrefix + C + AllJoint[i] + '_Grp1'))
                        pm.group(n=(WingDrivePrefix + C + AllJoint[i] + '_Grp'))
                        pm.delete(nearestPointOnCurve)
                    pm.select(cl=1)
                    for i in range(0, len(AllJoint)):
                        pm.select((WingDrivePrefix + C + AllJoint[i] + '_Grp'),add=1)
                    pm.group(n=(WingDrivePrefix + C + 'AllController_Grp'))
                    AllFeatherControlGrp.append((WingDrivePrefix + C + 'AllController_Grp'))
                # 给所有样条点加蔟，约束到最近的总控制曲线上
                shapes = cmds.listRelatives(C)[0]
                pm.select(cl=1)
                pm.select(shapes + '.cv[0:]')
                AllCurvePoint = pm.ls(sl=1,fl=1)
                pm.select(cl=1)
                pm.group(n=(WingDrivePrefix + C + '_WingAllClusterGroup'))
                ClusterGrp = pm.ls(sl=1)
                pm.setAttr((ClusterGrp[0] + ".inheritsTransform"), 0)
                pm.parent(ClusterGrp[0],(WingDrivePrefix + C + 'AllController_Grp'))
                for i in range(0,len(AllCurvePoint)):
                    pm.select(AllCurvePoint[i])
                    pm.mel.newCluster(" -envelope 1")
                    Cluster = pm.ls(sl=1)
                    pm.rename(Cluster,(WingDrivePrefix + C+'_point'+str(i)+'Cluster'))
                    Cluster = pm.ls(sl=1)
                    pm.spaceLocator(p=(0, 0, 0))
                    LSloc = pm.ls(sl=1)
                    pm.delete(pm.pointConstraint(Cluster[0],LSloc))
                    pm.parent(Cluster[0],ClusterGrp[0])
                    Place = pm.xform(str(LSloc[0]), query=True, worldSpace=1, translation=True)
                    nearestPointOnCurve = pm.createNode("nearestPointOnCurve")
                    shapes = pm.listRelatives(GeneralControl)[0]
                    pm.connectAttr((shapes + '.worldSpace[0]'), (nearestPointOnCurve + '.inputCurve'), f=1)
                    pm.setAttr((nearestPointOnCurve + '.inPositionX'), Place[0])
                    pm.setAttr((nearestPointOnCurve + '.inPositionY'), Place[1])
                    pm.setAttr((nearestPointOnCurve + '.inPositionZ'), Place[2])
                    U = pm.getAttr((nearestPointOnCurve + '.parameter'))
                    pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C+'_point'+str(i)+'ClusterLoc'))
                    Loc = pm.ls(sl=1)
                    pm.parent(Loc, ClusterGrp[0])
                    motionPath = pm.pathAnimation(Loc, GeneralControl, upAxis='y',
                                                  fractionMode=True,
                                                  endTimeU=pm.playbackOptions(query=1, maxTime=1),
                                                  startTimeU=pm.playbackOptions(minTime=1, query=1),
                                                  worldUpObject=AllGeneralJoint[j], worldUpType="objectrotation",
                                                  inverseUp=False,
                                                  inverseFront=False, follow=True, bank=False, followAxis='x',
                                                  worldUpVector=(0, 1, 0))
                    pm.disconnectAttr((motionPath + "_uValue.output"), (motionPath + ".uValue"))
                    pm.setAttr((motionPath + ".uValue"), U)

                    pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.4, tol=0.01, nr=(1, 0, 0),n=(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve'))
                    pm.group(n=(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp2'))
                    pm.group(n=(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp1'))
                    pm.delete(pm.parentConstraint(Cluster,(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve')))
                    pm.parent(Cluster,(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve'))
                    pm.parent((WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp1'), ClusterGrp[0])
                    pm.parentConstraint((WingDrivePrefix + C+'_point'+str(i)+'ClusterLoc'),(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp1'),mo=1,weight=1)
                    pm.setAttr((WingDrivePrefix + C+'_point'+str(i)+'ClusterLoc.visibility'),0)
                    pm.setAttr((WingDrivePrefix + C+'_point'+str(i)+'Cluster.visibility'), 0)
                    pm.delete(LSloc)
                pm.parent(C,(WingDrivePrefix + C + '_WingAllClusterGroup'))

            j = j + 1
        pm.select(cl=1)
        pm.group(n=(WingDrivePrefix + 'WingAllFeatherControlGroup'))
        for P in AllFeatherControlGrp:
            pm.parent(P, (WingDrivePrefix + 'WingAllFeatherControlGroup'))
        # 给总控制样条所有点加蔟，生成总控制器
        pm.select(GeneralControl, (WingDrivePrefix + 'WingAllFeatherControlGroup'))
        pm.group(n=(WingDrivePrefix + 'WingMainGrp'))
        # 给总控制器所有点加控制器
        k = -1
        for Lis in [GeneralControlPrimaryFlyingFeatherPoint,GeneralControlSecondaryFeatherPoint,GeneralControlLevelThreeFlyingFeatherPoint]:
            for Point in Lis:
                PointNum = Point.split('[')[1][:-1]
                pm.select(Point)
                pm.mel.newCluster(" -envelope 1")
                Cluster = pm.ls(sl=1)
                pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.5, tol=0.01, nr=(1, 0, 0),n=(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Curve'))
                pm.group(n=(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp2'))
                pm.group(n=(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1'))
                pm.delete(pm.parentConstraint(Cluster[0],(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1')))
                pm.parent(Cluster[0],(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Curve'))
                pm.parentConstraint(ShoulderElbowWrist[k], (WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1'),mo=1)
                pm.parent((WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1'),(WingDrivePrefix + 'WingMainGrp'))
                pm.setAttr((Cluster[0]+'.visibility'),0)
            k = k - 1
        #添加驱动属性样条
        #建立两条ik链，在手肘位置添加三个蔟，用来控制弯曲幅度和位置，且把属性给到驱动控制器（只修改羽毛部分，因为ADV自带调整）
        #肩部控制器旋转90度，

    else:
        pm.error('请加载肩部、手肘、手腕控制器')

                #将基础目标部分提取成总控制部分

def LTZZQDCK_kssc():
    FFK_C = str(pm.textFieldButtonGrp('LTZZQDCK_JZLTYTFKZQ', q=1, text=1))
    FK_C = str(pm.textFieldButtonGrp('LTZZQDCK_JZLTYTFKKZQ', q=1, text=1))
    QXCD = str(pm.textFieldButtonGrp('LTZZQDCK_JZLTZCQX', q=1, text=1))
    qianzhui = str(pm.textFieldButtonGrp('LTZZQDCK_JZQZ', q=1, text=1))
    if len(FFK_C) < 1:
        pm.select("", r=1)

    if len(FK_C) < 1:
        pm.select("", r=1)

    if len(qianzhui) < 1:
        pm.select("", r=1)

    Luntai_ZouXiang = str(pm.radioCollection('LTZZQDCK_Luntai', q=1, select=1))
    if Luntai_ZouXiang == "LTZZQDCK_Luntai_X":
        Luntai_ZouXiang = "X"

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_fX":
        Luntai_ZouXiang = "X"
        pm.setAttr("qianzhui_LunTai_C.BeiLv", -1)

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_Y":
        Luntai_ZouXiang = "Y"

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_fY":
        Luntai_ZouXiang = "Y"
        pm.setAttr("qianzhui_LunTai_C.BeiLv", -1)

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_Z":
        Luntai_ZouXiang = "Z"

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_fZ":
        Luntai_ZouXiang = "Z"
        pm.setAttr("qianzhui_LunTai_C.BeiLv", -1)

    pm.melGlobals.initVar('string', 'scriptLocationYvZhiWindow')
    pm.mel.performFileSilentImportAction((pm.melGlobals['scriptLocationYvZhiWindow'] + "/CarLunTaiMB.mb"))
    pm.shadingNode('curveInfo', asUtility=1)
    qxxxjd = pm.ls(sl=1)
    pm.connectAttr((QXCD + ".worldSpace[0]"), (qxxxjd[0] + ".inputCurve"),
                   f=1)
    qxcd = float(pm.getAttr(qxxxjd[0] + ".arcLength"))
    pm.select(FK_C, r=1)
    pm.pickWalk(d='up')
    pm.mel.doGroup(0, 1, 1)
    pm.mel.rename(qianzhui + "_LunTai_lianjie")
    pm.mel.doGroup(0, 1, 1)
    pm.mel.rename(qianzhui + "_LunTai_yveshu")
    pm.parent("qianzhui_LunTai_grp", FK_C)
    pm.setAttr("qianzhui_LunTai_grp.rotateZ", 0)
    pm.setAttr("qianzhui_LunTai_grp.translateX", 0)
    pm.setAttr("qianzhui_LunTai_grp.translateY", 0)
    pm.setAttr("qianzhui_LunTai_grp.translateZ", 0)
    pm.setAttr("qianzhui_LunTai_grp.rotateX", 0)
    pm.setAttr("qianzhui_LunTai_grp.rotateY", 0)
    pm.parent("qianzhui_LunTai_grp", "qianzhui_LunTai_Grp")
    pm.connectAttr("qianzhui_Joint.rotateX",
                   (qianzhui + "_LunTai_lianjie" + ".rotate" + Luntai_ZouXiang),
                   f=1)
    pm.parentConstraint('qianzhui_LunTai_C', (qianzhui + "_LunTai_yveshu"),
                        mo=1, weight=1)
    pm.scaleConstraint('qianzhui_LunTai_C', (qianzhui + "_LunTai_yveshu"),
                       weight=1, offset=(1, 1, 1))
    pm.parentConstraint(FFK_C, "qianzhui_LunTai", mo=1, weight=1)
    pm.scaleConstraint(FFK_C, "qianzhui_LunTai", weight=1, offset=(1, 1, 1))
    pm.select('qianzhui_LunTai_Grp', r=1)
    pm.mel.searchReplaceNames("qianzhui", qianzhui, "hierarchy")


















































































