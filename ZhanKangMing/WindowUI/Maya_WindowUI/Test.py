# coding=gbk
import maya.cmds as cmds
import random
import pymel.core as pm
import os
import sys
import inspect
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

