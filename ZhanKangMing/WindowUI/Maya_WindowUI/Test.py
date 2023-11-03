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





























