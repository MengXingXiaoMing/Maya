# coding=gbk
import maya.cmds as cmds
import random
import pymel.core as pm
import os
import sys
import inspect
import pymel.core as pm
J = pm.ls(sl=1)[0]
Suffix = ''
for i in range(0, 2):
    # 查询是否有约束，有则进行偏移处理
    # 将约束分为位移和旋转两部分
    try:
        Constraint = pm.parentConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
        TranslateConstraint = Constraint
        RotateConstraint = Constraint
    except:
        try:
            Constraint = pm.pointConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
            TranslateConstraint = Constraint
        except:
            TranslateConstraint = []
        try:
            Constraint = pm.orientConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
            RotateConstraint = Constraint
        except:
            try:
                Constraint = pm.aimConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                RotateConstraint = Constraint
            except:
                RotateConstraint = []
    # 开始处理位移和旋转
    # 把定位器p到对应的约束源
    # 获取需要的位移和旋转值赋予到对应约束的偏移值
    # 删除定位器
    if TranslateConstraint:
        NumLoc = pm.spaceLocator()
        parent = pm.listRelatives(TranslateConstraint, p=1)
        parent = pm.listRelatives(parent, p=1)
        pm.parent(NumLoc,parent[0])
        pm.parentConstraint(J,NumLoc)
        Num = pm.getAttr(str(NumLoc) + '.t')
        pm.setAttr((str(J) + "_G" + str(i + 1) + Suffix + '.t'), Num)
        if pm.ls(TranslateConstraint,type = 'parentConstraint'):
            Soure = pm.parentConstraint(TranslateConstraint, q=1, tl=1)
            pm.parentConstraint(Soure, TranslateConstraint, mo=1, e=1)
            '''SoureT = pm.listConnections(str(TranslateConstraint) + ".target[*].targetTranslate", s=True, scn=True,d=False)
            n = 0
            pm.spaceLocator(p=(0, 0, 0))
            locT = pm.ls(sl=1)
            pm.delete(pm.parentConstraint(J, locT))
            for ST in SoureT:
                # 建立定位器被对应的骨骼约束
                pm.parent(locT,ST)
                TX = pm.getAttr(locT[0] + '.translateX')
                TY = pm.getAttr(locT[0] + '.translateY')
                TZ = pm.getAttr(locT[0] + '.translateZ')
                pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetTranslateX', TX)
                pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetTranslateY', TY)
                pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetTranslateZ', TZ)
                n = n + 1
            pm.delete(locT)'''
        if pm.ls(TranslateConstraint, type='pointConstraint'):
            Soure = pm.pointConstraint(TranslateConstraint, q=1, tl=1)
            pm.pointConstraint(Soure, TranslateConstraint, mo=1, e=1)
        pm.delete(NumLoc)
    if RotateConstraint:
        NumLoc = pm.spaceLocator()
        parent = pm.listRelatives(RotateConstraint, p=1)
        parent = pm.listRelatives(parent, p=1)
        pm.parent(NumLoc, parent[0])
        pm.parentConstraint(J, NumLoc)
        Num = pm.getAttr(str(NumLoc) + '.r')
        pm.setAttr((str(J) + "_G" + str(i + 1) + Suffix + '.r'), Num)
        if pm.ls(RotateConstraint, type='parentConstraint'):
            Soure = pm.parentConstraint(RotateConstraint, q=1, tl=1)
            pm.parentConstraint(Soure, RotateConstraint, mo=1, e=1)
            '''SoureR = pm.listConnections(str(RotateConstraint) + ".target[*].targetRotate", s=True, scn=True, d=False)
            n = 0
            pm.spaceLocator(p=(0, 0, 0))
            locR = pm.ls(sl=1)
            pm.delete(pm.parentConstraint(J, locR))
            for ST in SoureR:
                # 建立定位器被对应的骨骼约束
                pm.parent(locR, ST)
                TX = pm.getAttr(locR[0] + '.rotateX')
                TY = pm.getAttr(locR[0] + '.rotateY')
                TZ = pm.getAttr(locR[0] + '.rotateZ')
                pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetRotateX', TX)
                pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetRotateY', TY)
                pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetRotateZ', TZ)
                n = n + 1
            pm.delete(locR)'''
        if pm.ls(RotateConstraint, type='orientConstraint'):
            Soure = pm.orientConstraint(RotateConstraint, q=1, tl=1)
            pm.orientConstraint(Soure, RotateConstraint, mo=1, e=1)
        if pm.ls(RotateConstraint, type='aimConstraint'):
            Soure = pm.orientConstraint(RotateConstraint, q=1, tl=1)
            pm.orientConstraint(Soure, RotateConstraint, mo=1, e=1)
        pm.delete(NumLoc)
    ###################################################




'''pos_1 = pm.xform( 'locator1', q=1, ws=1, t=1)
pos_2 = pm.xform( 'locator2', q=1, ws=1, t=1)
print pos_1
print pos_2
pos = [(a+b)/2 for (a, b) in zip(pos_1, pos_2)]
print pos
print pm.xform( 'joint3_G2', q=1, ws=1, t=1)
offset = [a-b for (a, b) in zip(pm.xform( 'joint3_G2', q=1, ws=1, t=1), pos)]
print offset
pm.xform('joint3_G2', ws=1, t=pos)
pm.move(offset[0], offset[1], offset[2], 'joint3_G2', r=1)'''



Constraint = pm.parentConstraint('nurbsCircle2', wal=1)
print Constraint






sel=pm.ls(sl=1,fl=1)
pm.mel.SelectEdgeRingSp()
Sel = pm.ls(sl=1,fl=1)
i = 0
while 1:
    if not (i < len(Sel)):
        break
    pm.select(Sel[i], r=1)
    pm.mel.performSelContiguousEdges(0)
    pm.mel.ConvertSelectionToVertices()
    Point=pm.ls(sl=1,fl=1)
    pm.select(Point[0])
    pm.mel.CopyVertexWeights()
    pm.select(Point)
    pm.mel.PasteVertexWeights()
    i = i + len(sel)


pm.mel.polySelectEdgesEveryN("edgeLoop", 1)

sel=pm.ls(sl=1,fl=1)
pm.mel.ConvertSelectionToVertices()
point = pm.ls(sl=1,fl=1)
pm.select(point[0])
for i in range(0,len(point)):
    pm.select(point[i])
    pm.mel.CopyVertexWeights()
    pm.mel.polySelectEdgesEveryN("edgeLoop", 1)
    SelA=pm.ls(sl=1,fl=1)
    pm.select(list(set(SelA).difference(set(sel))))
    pm.mel.SelectEdgeLoopSp()
    pm.mel.ConvertSelectionToVertices()
    LoopPoint = pm.ls(sl=1,fl=1)
    pm.select(LoopPoint)
    pm.mel.PasteVertexWeights()


sel = pm.ls(sl=1, fl=1)
pm.mel.ConvertSelectionToVertices()
point = pm.ls(sl=1, fl=1)
pm.select(point[0])
J = []
for i in range(0, len(point)):
    pm.select(point[i])
    pm.mel.polySelectEdgesEveryN("edgeLoop", 1)
    SelA = pm.ls(sl=1, fl=1)
    pm.select(list(set(SelA).difference(set(sel))))
    pm.mel.SelectEdgeLoopSp()
    pm.mel.ConvertSelectionToVertices()
    LoopPoint = pm.ls(sl=1, fl=1)
    pm.select(LoopPoint)
    cluster = pm.cluster()
    pm.select(cl=1)
    joint = pm.joint(p=(0,0,0))
    pm.delete(pm.pointConstraint(cluster, joint, w=1))
    pm.delete(cluster)
    if i > 0:
        pm.parent(joint,J)
    J = joint





pm.mel.SelectEdgeRingSp()
Sel = pm.ls(sl=1,fl=1)
i = 0
while 1:
    if not (i < len(Sel)):
        break
    pm.select(Sel[i], r=1)
    pm.mel.performSelContiguousEdges(0)
    pm.mel.ConvertSelectionToVertices()
    Point=pm.ls(sl=1,fl=1)
    pm.select(Point[0])
    pm.mel.CopyVertexWeights()
    pm.select(Point)
    pm.mel.PasteVertexWeights()
    i = i + len(sel)










import pymel.core as pm
sel = pm.ls(sl=1)
multMatrix = pm.shadingNode('multMatrix', asUtility=1)
Matrix = pm.listConnections((sel[0]+'.worldMatrix[0]'), p=1)
for M in Matrix:
    pm.connectAttr((multMatrix + '.matrixSum'), M, force=1)
pm.connectAttr((sel[0]+'.worldMatrix[0]'), (multMatrix+'.matrixIn[0]'), force=1)
pm.connectAttr((sel[0]+'.worldInverseMatrix[0]'), (multMatrix+'.matrixIn[1]'), force=1)
for i in range(1,len(sel)):
    multMatrix = pm.shadingNode('multMatrix', asUtility=1)
    Matrix = pm.listConnections((sel[i]+'.worldMatrix[0]'), p=1)
    for M in Matrix:
        pm.connectAttr((multMatrix + '.matrixSum'), M, force=1)
    pm.connectAttr((sel[i] + '.worldMatrix[0]'), (multMatrix + '.matrixIn[0]'), force=1)
    pm.connectAttr((sel[0]+'.worldInverseMatrix[0]'), (multMatrix+'.matrixIn[1]'), force=1)









import pymel.core as pm
AllJoint = pm.ls(sl=1)



ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *

ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_SoureDrver')
HipJoint = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_DrverTarget')
Curve = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_Skirt_Edge')
RangeCurve = pm.ls(sl=1)
axial = ''
DirectionNum = 1
Axial = pm.textFieldButtonGrp('WindowSkirtCollision_Axial', q=1, text=1)
Direction = [1, -1, 1, -1, 1, -1]
AxialList = [u'x', u'-x', u'y', u'-y', u'z', u'-z']
AxialList_2 = ['X', 'X', 'Y', 'Y', 'Z', 'Z']
for i in range(0, len(AxialList)):
    if Axial == AxialList[i]:
        axial = AxialList_2[i]
        DirectionNum = Direction[i]

Hip = HipJoint[0]
Cur = Curve[0]
pm.select(HipJoint[0])

FollowLocGrp = pm.group(em=1,n=HipJoint[0]+'_'+HipJoint[1]+'_FollowLocGrp')

'''for Hip in HipJoint:'''
pm.spaceLocator(p=(0, 0, 0), n=(Cur + '_' + Hip + '_FollowSkirtLoc'))
#pm.setAttr((Cur + '_' + Hip + 'FollowSkirtLoc.visibility'), 0)
pm.parent((Cur + '_' + Hip + '_FollowSkirtLoc'),FollowLocGrp)
pathAnimation = pm.pathAnimation(RangeCurve[0],(Cur + '_' + Hip + '_FollowSkirtLoc'))
print pathAnimation
pm.select(cl=1)
SubitemJoint = pm.listRelatives(Hip, c=1)
J_A = pm.joint(p=(0, 0, 0),n=(Hip+'_'+SubitemJoint[0]+'_JointA'))
J_B = pm.joint(p=(0, 0, 0),n=(Hip+'_'+SubitemJoint[0]+'_JointB'))
pm.select(J_A)
J_C = pm.joint(p=(0, 0, 0),n=(Hip+'_'+SubitemJoint[0]+'_JointC'))
J_D = pm.joint(p=(0, 0, 0),n=(Hip+'_'+SubitemJoint[0]+'_JointD'))
pm.delete(pm.parentConstraint(Hip,(Hip+'_'+SubitemJoint[0]+'_JointA'),w=1))
pm.delete(pm.parentConstraint(SubitemJoint[0],(Hip+'_'+SubitemJoint[0]+'_JointB'),w=1))
pm.delete(pm.parentConstraint(Hip,(Hip+'_'+SubitemJoint[0]+'_JointC'),w=1))
pm.delete(pm.parentConstraint(SubitemJoint[0],(Hip+'_'+SubitemJoint[0]+'_JointD'),w=1))
pm.pointConstraint(Hip,(Hip+'_'+SubitemJoint[0]+'_JointA'),w=1)
pm.aimConstraint((Cur + '_' + Hip + '_FollowSkirtLoc'),(Hip+'_'+SubitemJoint[0]+'_JointA'),weight=1,
                 upVector=(0, 0, -1), worldUpObject=(Cur + '_' + Hip + '_FollowSkirtLoc'),worldUpType="objectrotation",
                 offset=(0, 0, 0), aimVector=(1, 0, 0), worldUpVector=(0, 0, -1))
pm.aimConstraint(SubitemJoint,(Hip+'_'+SubitemJoint[0]+'_JointC'),weight=1,
                 upVector=(0, 0, -1), worldUpObject=(Hip+'_'+SubitemJoint[0]+'_JointB'), worldUpType="object",
                 offset=(0, 0, 0), aimVector=(1, 0, 0))

decomposeMatrix = pm.shadingNode('decomposeMatrix', asUtility=1)
pm.connectAttr((SubitemJoint[0]+'.worldMatrix[0]'), (decomposeMatrix+'.inputMatrix'), force=1)
nearestPointOnCurve = pm.shadingNode('nearestPointOnCurve', asUtility=1)
pm.connectAttr((decomposeMatrix+'.outputTranslate'), (nearestPointOnCurve+'.inPosition'), force=1)
CurveShape = pm.listRelatives(RangeCurve, c=1,type='nurbsCurve')
print CurveShape
pm.connectAttr((CurveShape[0]+'.worldSpace[0]'), (nearestPointOnCurve+'.inputCurve'), force=1)
pm.connectAttr((nearestPointOnCurve+'.parameter'), (pathAnimation+'.uValue'), f=1)

'''pm.shadingNode('decomposeMatrix', asUtility=1)
pm.connectAttr('Hip_R_HipPart1_R_JointD.worldMatrix[0]', 'decomposeMatrix32.inputMatrix', force=1)


pm.shadingNode('distanceBetween', asUtility=1)
pm.connectAttr('decomposeMatrix32.outputTranslate', 'distanceBetween1.point1', force=1)
pm.connectAttr('decomposeMatrix32.outputTranslate', 'distanceBetween1.point1', force=1)'''




'''    for Cur in Curve:'''
if not pm.objExists((Cur + '_SikrtCollision_Grp')):
    pm.select(Cur)
    pm.pickWalk(d='up')
    pm.mel.doGroup(0, 1, 1)
    pm.mel.rename(Cur + '_SikrtCollision_Grp')
else:
    pm.select((Cur + '_SikrtCollision_Grp'))
SikrtCollisionGrp = pm.ls(sl=1)
'''if not pm.objExists((SikrtCollisionGrp[0] + '.remapValue')):
    pm.addAttr(SikrtCollisionGrp[0], ln='remapValue', dv=0, at='double')
    pm.setAttr((SikrtCollisionGrp[0] + '.remapValue'), e=1, keyable=True)'''
pm.spaceLocator(p=(0, 0, 0), n=(Cur + '_' + Hip + 'FollowHipLoc'))
#pm.setAttr((Cur + '_' + Hip + 'FollowHipLoc.visibility'), 0)
pm.parent((Cur + '_' + Hip + 'FollowHipLoc'),FollowLocGrp)
pm.delete(pm.parentConstraint( Cur,(Cur + '_' + Hip + 'FollowHipLoc'),w=1))


distanceBetween = pm.shadingNode('distanceBetween', asUtility=1)
pm.connectAttr((Cur + '_' + Hip + 'FollowHipLoc.translate'), (distanceBetween + '.point1'), f=1)
pm.connectAttr((Cur + '_' + Hip + '_FollowSkirtLoc.translate'), (distanceBetween + '.point2'),f=1)

multiplyDivide_1 = pm.shadingNode('multiplyDivide', asUtility=1)
pm.setAttr((multiplyDivide_1 + '.operation'), 2)
pm.setAttr((multiplyDivide_1 + '.input1X'), 1)
pm.connectAttr((distanceBetween + '.distance'), (multiplyDivide_1 + '.input2X'), f=1)

multiplyDivide_2 = pm.shadingNode('multiplyDivide', asUtility=1)
pm.setAttr((multiplyDivide_2 + '.operation'), 2)
pm.connectAttr((multiplyDivide_1 + '.outputX'), (multiplyDivide_2 + '.input1X'), f=1)
pm.setAttr((multiplyDivide_2 + '.input2X'), pm.getAttr((multiplyDivide_2 + '.input1X')))

remapValue = pm.shadingNode('remapValue', asUtility=1)
pm.connectAttr((multiplyDivide_2 + '.outputX'), (remapValue + '.inputValue'), f=1)
pm.addAttr(remapValue, ln='remapValue', dv=0, at='double')
pm.setAttr((remapValue + '.remapValue'), e=1, keyable=True)
#pm.connectAttr((SikrtCollisionGrp[0] + '.remapValue'), (remapValue + '.remapValue'), f=1)
multiplyDivide_3 = pm.shadingNode('multiplyDivide', asUtility=1)
pm.connectAttr((remapValue + '.outValue'), (multiplyDivide_3 + '.input1X'), f=1)
pm.connectAttr((J_C + '.rotateY'), (multiplyDivide_3 + '.input2X'), f=1)

multiplyDivide_4 = pm.shadingNode('multiplyDivide', asUtility=1)
pm.connectAttr((multiplyDivide_3+'.outputX'), (multiplyDivide_4 + '.input1X'), f=1)
pm.addAttr(Cur, ln='Magnification', dv=DirectionNum, at='double')
pm.setAttr((Cur + '.' + 'Magnification'), e=1, keyable=True)
pm.connectAttr((Cur + '.' + 'Magnification'), (multiplyDivide_4 + '.input2X'), f=1)

clamp = pm.shadingNode('clamp', asUtility=1)
pm.setAttr((clamp+'.maxR'), 180)
pm.connectAttr((multiplyDivide_4+'.outputX'), (clamp+'.inputR'), f=1)
pm.connectAttr((clamp+'.outputR'), (Cur + '_SikrtCollision_Grp.rotate'+axial), f=1)

pm.addAttr(Cur, ln=(Hip + 'InputMin'), dv=0.8, at='double')
pm.setAttr((Cur + '.' + Hip + 'InputMin'), e=1, keyable=True)
pm.connectAttr((Cur + '.' + Hip + 'InputMin'), (remapValue + '.inputMin'), f=1)
################################################################



pm.addAttr(Cur, ln=Hip + 'InputMax', dv=2, at='double')
pm.setAttr((Cur + '.' + Hip + 'InputMax'), e=1, keyable=True)
pm.connectAttr((Cur + '.' + Hip + 'InputMax'), (remapValue + '.inputMax'), f=1)

pm.addAttr(Cur, ln=Hip + 'OutputMin', dv=0, at='double')
pm.setAttr((Cur + '.' + Hip + 'OutputMin'), e=1, keyable=True)
pm.connectAttr((Cur + '.' + Hip + 'OutputMin'), (remapValue + '.outputMin'), f=1)
pm.addAttr(Cur, ln=Hip + 'OutputMax', dv=90, at='double')
pm.setAttr((Cur + '.' + Hip + 'OutputMax'), e=1, keyable=True)
pm.connectAttr((Cur + '.' + Hip + 'OutputMax'), (remapValue + '.outputMax'), f=1)

'''for Cur in Curve:'''
AllRemapValue = pm.listConnections((Cur + '_SikrtCollision_Grp'), s=1, d=1, scn=1)
print AllRemapValue
LinkCondition = []
for i in range(1, len(AllRemapValue)):
    print i
    condition = pm.shadingNode('condition', asUtility=1)
    pm.select(AllRemapValue[i - 1])
    type = pm.ls(sl=1, type='condition')
    if type:
        pm.connectAttr((AllRemapValue[i - 1] + '.outColorR'), (condition + '.firstTerm'), f=1)
        pm.connectAttr((AllRemapValue[i - 1] + '.outColorR'), (condition + '.colorIfTrueR'), f=1)
    else:
        pm.connectAttr((AllRemapValue[i - 1] + '.outValue'), (condition + '.firstTerm'), f=1)
        pm.connectAttr((AllRemapValue[i - 1] + '.outValue'), (condition + '.colorIfTrueR'), f=1)
    pm.connectAttr((AllRemapValue[i] + '.outValue'), (condition + '.secondTerm'), f=1)
    pm.setAttr((condition + '.operation'), 2)
    pm.connectAttr((AllRemapValue[i] + '.outValue'), (condition + '.colorIfFalseR'), f=1)
    AllRemapValue[i] = condition
    LinkCondition = condition
multiplyDivide_3 = pm.shadingNode('multiplyDivide', asUtility=1)

pm.addAttr(Cur, ln='Magnification', dv=DirectionNum, at='double')
pm.setAttr((Cur + '.' + 'Magnification'), e=1, keyable=True)
if LinkCondition:
    pm.connectAttr((LinkCondition[0] + '.outColorR'), (multiplyDivide_3 + '.input1X'), f=1)
else:
    pm.connectAttr((AllRemapValue[0] + '.outValue'), (multiplyDivide_3 + '.input1X'), f=1)
pm.connectAttr((Cur + '.' + 'Magnification'), (multiplyDivide_3 + '.input2X'), f=1)
pm.connectAttr((multiplyDivide_3 + '.outputX'), (Cur + '_SikrtCollision_Grp.rotate' + axial), f=1)