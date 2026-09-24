# coding=gbk
from maya import cmds

sel = cmds.ls(sl=1)

for s in sel:
    # 添加属性
    cmds.addAttr(s, ln="follow_world",  at='bool')
    cmds.setAttr(s+'.follow_world', e=1, keyable=1)
    parent = cmds.listRelatives(s, p=1)
    parent = cmds.listRelatives(parent, p=1)
    print(parent)
    parentConstraint = cmds.parentConstraint('Main', parent, w=1, mo=1)
    cmds.connectAttr(s+'.follow_world', parentConstraint[0]+'.MainW0')


