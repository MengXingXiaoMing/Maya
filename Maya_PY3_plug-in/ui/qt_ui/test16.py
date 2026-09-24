# coding=gbk
# 选择样条运行即可添加路径样条
import maya.cmds as cmds
sel = cmds.ls(sl=1)
if sel:
    shape = cmds.listRelatives(sel, shapes=True,)[0]
    all_an = cmds.ls('SteamTrainBlock_rig:ik_choice.input[*]')
    num = int(all_an[-1].split('[')[-1][:-1])
    cmds.connectAttr(shape+'.worldSpace[0]', 'SteamTrainBlock_rig:ik_choice.input['+str(num+1)+']')
    cmds.setAttr('SteamTrainBlock_rig:anim_globalMove01.curve', num+1)
    cmds.warning('创建完成')
else:
    cmds.warning('请选择路径')



# 第一次添加约束
cmds.parentConstraint('SteamTrainBlock_rig:ikParthJ8_loc', 'CarriageBlock_rig:LinkRequiredLoc1', w=1)
cmds.parentConstraint('SteamTrainBlock_rig:FKBackBodyJ4_M', 'CarriageBlock_rig:FKExtraPropJ44_M', w=1, mo=1)
cmds.connectAttr('SteamTrainBlock_rig:ik_choice.output', 'CarriageBlock_rig:box_choice.input[1]')
cmds.setAttr('CarriageBlock_rig:anim_globalMove01.new_curve', 1)
cmds.warning('创建完成')



# 后续添加约束
sel = cmds.ls(sl=1)
if len(sel)>1:
    # 获取空间名称
    spae_name1 = sel[0].split(':')[0]
    spae_name2 = sel[-1].split(':')[0]
    cmds.parentConstraint(spae_name1+':ikParthJ3', spae_name2+':LinkRequiredLoc1', w=1)
    cmds.parentConstraint(spae_name1+':FKPropJ46_M', spae_name2+':LinkRequiredLoc', w=1, mo=1)
    cmds.connectAttr('SteamTrainBlock_rig:ik_choice.output', spae_name2+':box_choice.input[1]')
    cmds.setAttr(spae_name2+':anim_globalMove01.new_curve', 1)
    cmds.warning('创建完成')
else:
    cmds.warning('请选择两个对象')

