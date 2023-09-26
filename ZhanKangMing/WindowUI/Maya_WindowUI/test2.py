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