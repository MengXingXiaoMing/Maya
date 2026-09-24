#coding=gbk
from maya import cmds
cmds.SelectHierarchy()
meshs = cmds.ls(sl=1, type='mesh')
print(meshs)
loc = cmds.spaceLocator()[0]
print(loc)
# 假设已选中模型
for mesh in meshs:
    # 方法1：列出模型的历史记录，并过滤出skinCluster节点
    print(mesh)
    transform = cmds.listRelatives(mesh, p=1)[0]
    print(transform)
    deforms = cmds.listHistory(transform, pruneDagObjects=True, interestLevel=True)

    if deforms:
        print(deforms)
        skinClusters = []
        for deform in deforms:
            if cmds.nodeType(deform) == 'skinCluster':
                skinClusters.append(deform)
        print(skinClusters)
        if skinClusters:
            for skin in skinClusters:
                cmds.setAttr(skin+'.relativeSpaceMode',  2)
                cmds.connectAttr(loc+'.worldMatrix[0]', skin+'.relativeSpaceMatrix')

            cmds.connectAttr(loc+'.worldMatrix[0]', transform+'.offsetParentMatrix')




from maya import cmds
sel = cmds.ls(sl=1)
for s in sel:
    cmds.connectAttr('a_' + s + '.translate', s + '.translate')
    cmds.connectAttr('a_' + s + '.rotate', s + '.rotate')
    cmds.connectAttr('a_' + s + '.scale', s + '.scale')





sel = cmds.ls(sl=1)
sel = sel[1::2]
for s in sel:
    try:
        parent = cmds.listRelatives(s, p=1)
        child = cmds.listRelatives(s, c=1)
        cmds.parent(child, parent)
        cmds.delete(s)
    except:
        pass


