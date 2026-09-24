# coding=gbk
import maya.OpenMaya as om
import maya.cmds as cmds

sel = cmds.ls(sl=1)
for s in sel:
    parent = cmds.listRelatives(s, p=1, type='joint')
    loc = cmds.spaceLocator(n=s + '_loc')[0]
    cmds.delete(cmds.parentConstraint(s, loc))
    if parent:
        cmds.parent(loc, parent[0] + '_loc')
    new_name = s + '_FKGrp1'
    if cmds.objExists(new_name):
        cmds.connectAttr(loc + '.tx', new_name + '.tx')
        cmds.connectAttr(loc + '.ty', new_name + '.ty')
        cmds.connectAttr(loc + '.tz', new_name + '.tz')

        cmds.connectAttr(loc + '.rx', new_name + '.rx')
        cmds.connectAttr(loc + '.ry', new_name + '.ry')
        cmds.connectAttr(loc + '.rz', new_name + '.rz')

        cmds.connectAttr(loc + '.sx', new_name + '.sx')
        cmds.connectAttr(loc + '.sy', new_name + '.sy')
        cmds.connectAttr(loc + '.sz', new_name + '.sz')


sel = cmds.ls(sl=1)
for s in sel:
    # print(s[:-2])
    # print(s[-2:])
    # loc = s + '_loc'
    loc = s[:-2] + '_self' + s[-2:] + '_loc'
    if cmds.objExists(loc):
        cmds.parentConstraint(s, loc, mo=1, w=1)
        cmds.scaleConstraint(s, loc)






sel = cmds.ls(sl=1)
cmds.select(cl=1)
for s in sel:
    try:
        cmds.select(s + '_FKGrp1', add=1)
    except:
        pass


for s in sel:
    try:
        cmds.connectAttr(s + '_loc.tx', s + '_FKGrp1.tx')
        cmds.connectAttr(s + '_loc.ty', s + '_FKGrp1.ty')
        cmds.connectAttr(s + '_loc.tz', s + '_FKGrp1.tz')

        cmds.connectAttr(s + '_loc.rx', s + '_FKGrp1.rx')
        cmds.connectAttr(s + '_loc.ry', s + '_FKGrp1.ry')
        cmds.connectAttr(s + '_loc.rz', s + '_FKGrp1.rz')

        cmds.connectAttr(s + '_loc.sx', s + '_FKGrp1.sx')
        cmds.connectAttr(s + '_loc.sy', s + '_FKGrp1.sy')
        cmds.connectAttr(s + '_loc.sz', s + '_FKGrp1.sz')
    except:
        pass

for s in sel:
    cmds.parentConstraint(s, s + '_loc.sz')

for s in sel:
    try:
        print(s[2:])
        print(s + '_loc')
        print(cmds.objExists(s[2:-2]))
        print(cmds.objExists(s + '_loc'))
        cmds.scaleConstraint(s[2:-2], s + '_loc')
    except:
        pass

for s in sel:
    try:
        print(s[2:])
        print(s + '_loc')
        print(cmds.objExists(s[2:-2]))
        print(cmds.objExists(s + '_loc'))
        cmds.parentConstraint(s[2:-2], s + '_loc',mo=1)
    except:
        pass

for s in sel:
    try:
        cmds.connectAttr(s + '_loc.tx', s + '_FKGrp1.tx')
        cmds.connectAttr(s + '_loc.ty', s + '_FKGrp1.ty')
        cmds.connectAttr(s + '_loc.tz', s + '_FKGrp1.tz')

        cmds.connectAttr(s + '_loc.rx', s + '_FKGrp1.rx')
        cmds.connectAttr(s + '_loc.ry', s + '_FKGrp1.ry')
        cmds.connectAttr(s + '_loc.rz', s + '_FKGrp1.rz')

        cmds.connectAttr(s + '_loc.sx', s + '_FKGrp1.sx')
        cmds.connectAttr(s + '_loc.sy', s + '_FKGrp1.sy')
        cmds.connectAttr(s + '_loc.sz', s + '_FKGrp1.sz')
    except:
        pass

sel = cmds.ls(sl=1)
for s in sel:
    cmds.parentConstraint(s+'_AC', s, mo=1)
    cmds.scaleConstraint(s+'_AC', s, mo=1)

sel = cmds.ls(sl=1)
sel2 = cmds.ls(sl=1)
print(sel)
print(sel2)
for s, s2 in zip(sel, sel2):
    print(s,s2)
    cmds.connectAttr(s + '.tx', s2 + '_FKGrp1.tx')
    cmds.connectAttr(s + '.ty', s2 + '_FKGrp1.ty')
    cmds.connectAttr(s + '.tz', s2 + '_FKGrp1.tz')

    cmds.connectAttr(s + '.rx', s2 + '_FKGrp1.rx')
    cmds.connectAttr(s + '.ry', s2 + '_FKGrp1.ry')
    cmds.connectAttr(s + '.rz', s2 + '_FKGrp1.rz')

    cmds.connectAttr(s + '.sx', s2 + '_FKGrp1.sx')
    cmds.connectAttr(s + '.sy', s2 + '_FKGrp1.sy')
    cmds.connectAttr(s + '.sz', s2 + '_FKGrp1.sz')
    print('aaa')

import maya.cmds as cmds
sel = cmds.ls(sl=1)
self_list = []
for s in sel:
    downstream_nodes = cmds.listConnections(s + '.translateX', s=False, d=True)
    # print(type(downstream_nodes))
    if downstream_nodes != None:
        # print(downstream_nodes)
        downstream_nodes = downstream_nodes[0]
        self_list.append([s, downstream_nodes])
print(self_list)


lists = [['J_Ankle_R_R_loc', 'J_Ankle_R_R_FKGrp1'], ['J_MiddleFinger3_R_R_loc', 'J_MiddleFinger3_R_R_FKGrp1'], ['J_ThumbFinger3_R_R_loc', 'J_ThumbFinger3_R_R_FKGrp1'], ['J_Shoulder_R_R_loc', 'J_Shoulder_R_R_FKGrp1'], ['J_Hip_R_R_loc', 'J_Hip_R_R_FKGrp1'], ['J_HipTop_R_L_loc', 'J_HipTop_R_L_FKGrp1'], ['J_MiddleFingerTop_R_L_loc', 'J_MiddleFingerTop_R_L_FKGrp1'], ['J_RingFinger1_R_R_loc', 'J_RingFinger1_R_R_FKGrp1'], ['J_ThumbFinger3_R_L_loc', 'J_ThumbFinger3_R_L_FKGrp1'], ['BaseRootJoint_M_loc', 'BaseRootJoint_M_FKGrp1'], ['J_IndexFinger1_R_R_loc', 'J_IndexFinger1_R_R_FKGrp1'], ['J_Wrist_R_L_loc', 'J_Wrist_R_L_FKGrp1'], ['J_RingFinger3_R_R_loc', 'J_RingFinger3_R_R_FKGrp1'], ['J_Knee_R_R_loc', 'J_Knee_R_R_FKGrp1'], ['J_Ankle_R_L_loc', 'J_Ankle_R_L_FKGrp1'], ['J_ThumbFinger2_R_L_loc', 'J_ThumbFinger2_R_L_FKGrp1'], ['J_Scapula1_R_L_loc', 'J_Scapula1_R_L_FKGrp1'], ['J_IndexFinger3_R_L_loc', 'J_IndexFinger3_R_L_FKGrp1'], ['J_Knee_R_L_loc', 'J_Knee_R_L_FKGrp1'], ['J_ThumbFinger1_R_R_loc', 'J_ThumbFinger1_R_R_FKGrp1'], ['J_Shoulder_R_L_loc', 'J_Shoulder_R_L_FKGrp1'], ['J_Root_M_M_loc', 'J_Root_M_M_FKGrp1'], ['J_MiddleFinger1_R_L_loc', 'J_MiddleFinger1_R_L_FKGrp1'], ['J_Hip_R_L_loc', 'J_Hip_R_L_FKGrp1'], ['J_MiddleFinger2_R_R_loc', 'J_MiddleFinger2_R_R_FKGrp1'], ['J_IndexFinger2_R_L_loc', 'J_IndexFinger2_R_L_FKGrp1'], ['J_Tiptoe_L_loc', 'J_Tiptoe_L_FKGrp1'], ['J_IndexFinger1_R_L_loc', 'J_IndexFinger1_R_L_FKGrp1'], ['J_ThumbFinger2_R_R_loc', 'J_ThumbFinger2_R_R_FKGrp1'], ['J_Elbow_R_L_loc', 'J_Elbow_R_L_FKGrp1'], ['J_IndexFingerTop_R_L_loc', 'J_IndexFingerTop_R_L_FKGrp1'], ['J_IndexFinger3_R_R_loc', 'J_IndexFinger3_R_R_FKGrp1'], ['J_RingFingerTop_R_R_loc', 'J_RingFingerTop_R_R_FKGrp1'], ['J_Tiptoe_R_loc', 'J_Tiptoe_R_FKGrp1'], ['J_ThumbFinger1_R_L_loc', 'J_ThumbFinger1_R_L_FKGrp1'], ['J_Heel_R_loc', 'J_Heel_R_FKGrp1'], ['J_HipTop_R_R_loc', 'J_HipTop_R_R_FKGrp1'], ['J_RingFinger3_R_L_loc', 'J_RingFinger3_R_L_FKGrp1'], ['J_RingFingerTop_R_L_loc', 'J_RingFingerTop_R_L_FKGrp1'], ['J_IndexFinger2_R_R_loc', 'J_IndexFinger2_R_R_FKGrp1'], ['J_RingFinger2_R_R_loc', 'J_RingFinger2_R_R_FKGrp1'], ['J_MiddleFingerTop_R_R_loc', 'J_MiddleFingerTop_R_R_FKGrp1'], ['J_RingFinger1_R_L_loc', 'J_RingFinger1_R_L_FKGrp1'], ['J_Elbow_R_R_loc', 'J_Elbow_R_R_FKGrp1'], ['J_Head_M_M_loc', 'J_Head_M_M_FKGrp1'], ['J_Heel_L_loc', 'J_Heel_L_FKGrp1'], ['J_MiddleFinger3_R_L_loc', 'J_MiddleFinger3_R_L_FKGrp1'], ['J_Scapula_R_L_loc', 'J_Scapula_R_L_FKGrp1'], ['J_Wrist_R_R_loc', 'J_Wrist_R_R_FKGrp1'], ['J_Scapula_R_R_loc', 'J_Scapula_R_R_FKGrp1'], ['J_IndexFingerTop_R_R_loc', 'J_IndexFingerTop_R_R_FKGrp1'], ['J_MiddleFinger2_R_L_loc', 'J_MiddleFinger2_R_L_FKGrp1'], ['J_Scapula1_R_R_loc', 'J_Scapula1_R_R_FKGrp1'], ['J_MiddleFinger1_R_R_loc', 'J_MiddleFinger1_R_R_FKGrp1'], ['J_RingFinger2_R_L_loc', 'J_RingFinger2_R_L_FKGrp1']]
for list in lists:
    try:
        cmds.connectAttr(list[0] + '.tx', list[1] + '.tx')
        cmds.connectAttr(list[0] + '.ty', list[1] + '.ty')
        cmds.connectAttr(list[0] + '.tz', list[1] + '.tz')

        cmds.connectAttr(list[0] + '.rx', list[1] + '.rx')
        cmds.connectAttr(list[0] + '.ry', list[1] + '.ry')
        cmds.connectAttr(list[0] + '.rz', list[1] + '.rz')

        cmds.connectAttr(list[0] + '.sx', list[1] + '.sx')
        cmds.connectAttr(list[0] + '.sy', list[1] + '.sy')
        cmds.connectAttr(list[0] + '.sz', list[1] + '.sz')
    except:
        pass


lists = [
#前半
['R_thumb03_CTL','FKThumbFinger3_R'],
['R_thumb02_CTL','FKThumbFinger2_R'],
['R_thumb01_CTL','FKThumbFinger1_R'],

['R_index03_CTL','FKIndexFinger3_R'],
['R_index02_CTL','FKIndexFinger2_R'],
['R_index01_CTL','FKIndexFinger1_R'],

['R_middle03_CTL','FKMiddleFinger3_R'],
['R_middle02_CTL','FKMiddleFinger2_R'],
['R_middle01_CTL','FKMiddleFinger1_R'],

['R_pinky03_CTL','FKRingFinger3_R'],
['R_pinky02_CTL','FKRingFinger2_R'],
['R_pinky01_CTL','FKRingFinger1_R'],

['R_wristFK_CTL','FKWrist_R'],
['R_elbowFK_CTL','FKElbow_R'],
['R_shoulder_CTL','FKShoulder_R'],
['R_shoulderFK_CTL','FKScapula1_R'],
['R_clavicle_CTL','FKScapula_R'],

['R_thighFK_CTL','FKHip_R'],
['R_kneeFK_CTL','FKKnee_R'],
['R_ankleFK_CTL','FKAnkle_R'],
# ['R_heel_CTL','FKHeel2_R'],

# 中心
['C_root_CTL','FKHead_M'],
['C_pelvis_CTL','HipSwinger_M'],

# 后半
['L_thumb03_CTL','FKThumbFinger3_L'],
['L_thumb02_CTL','FKThumbFinger2_L'],
['L_thumb01_CTL','FKThumbFinger1_L'],

['L_index03_CTL','FKIndexFinger3_L'],
['L_index02_CTL','FKIndexFinger2_L'],
['L_index01_CTL','FKIndexFinger1_L'],

['L_middle03_CTL','FKMiddleFinger3_L'],
['L_middle02_CTL','FKMiddleFinger2_L'],
['L_middle01_CTL','FKMiddleFinger1_L'],

['L_pinky03_CTL','FKRingFinger3_L'],
['L_pinky02_CTL','FKRingFinger2_L'],
['L_pinky01_CTL','FKRingFinger1_L'],

['L_wristFK_CTL','FKWrist_L'],
['L_elbowFK_CTL','FKElbow_L'],
['L_shoulder_CTL','FKShoulder_L'],
['L_shoulderFK_CTL','FKScapula1_L'],
['L_clavicle_CTL','FKScapula_L'],

['L_thighFK_CTL','FKHip_L'],
['L_kneeFK_CTL','FKKnee_L'],
['L_ankleFK_CTL','FKAnkle_L'],
# ['L_heel_CTL','FKHeel2_L'],
]
for lis in lists:
    cmds.rename(lis[1],lis[0])


sel = cmds.ls(sl=1)
for s in sel:
    cmds.select(cl=1)
    parent = cmds.listRelatives(s, p=1, type='joint')
    joint = cmds.joint(p=(0,0,0), n=s + '_FKJ')
    cmds.delete(cmds.parentConstraint(s, joint))
    if parent:
        cmds.parent(joint, parent[0] + '_FKJ')



sel = cmds.ls(sl=1)
for s in sel:
    parent = cmds.listRelatives(s, p=1, type='joint')
    loc = cmds.spaceLocator(n=s + '_loc')[0]
    cmds.delete(cmds.parentConstraint(s, loc))
    if parent:
        cmds.parent(loc, parent[0] + '_loc')


sel = cmds.ls(sl=1)
for s in sel:
    # print(s[:-2])
    # print(s[-2:])
    # loc = s + '_loc'
    loc = s + '_loc'
    grp = s[:-2] + '_FKJ' + s[-2:] + '_FKGrp1'
    if cmds.objExists(loc) and cmds.objExists(grp):
        # cmds.parentConstraint(s, loc, mo=1, w=1)
        # cmds.scaleConstraint(s, loc)

        cmds.connectAttr(loc + '.tx', grp + '.tx')
        cmds.connectAttr(loc + '.ty', grp + '.ty')
        cmds.connectAttr(loc + '.tz', grp + '.tz')

        cmds.connectAttr(loc + '.rx', grp + '.rx')
        cmds.connectAttr(loc + '.ry', grp + '.ry')
        cmds.connectAttr(loc + '.rz', grp + '.rz')

        cmds.connectAttr(loc + '.sx', grp + '.sx')
        cmds.connectAttr(loc + '.sy', grp + '.sy')
        cmds.connectAttr(loc + '.sz', grp + '.sz')

sel = cmds.ls(sl=1)
for s in sel:
    # print(s[:-2])
    # print(s[-2:])
    # loc = s + '_loc'
    loc = s + '_loc'
    grp = s[:-2] + '_FKJ' + s[-2:] + '_FKGrp1'
    if cmds.objExists(loc) and cmds.objExists(grp):

        cmds.disconnectAttr(loc + '.tx', grp + '.tx')
        cmds.disconnectAttr(loc + '.ty', grp + '.ty')
        cmds.disconnectAttr(loc + '.tz', grp + '.tz')

        cmds.disconnectAttr(loc + '.rx', grp + '.rx')
        cmds.disconnectAttr(loc + '.ry', grp + '.ry')
        cmds.disconnectAttr(loc + '.rz', grp + '.rz')

        cmds.disconnectAttr(loc + '.sx', grp + '.sx')
        cmds.disconnectAttr(loc + '.sy', grp + '.sy')
        cmds.disconnectAttr(loc + '.sz', grp + '.sz')


sel = cmds.ls(sl=1)
for s in sel:
    shapes = cmds.listRelatives(s, shapes=True, type='nurbsCurve')
    cmds.connectAttr('drver_curve.base_ctr',shapes[0]+'.visibility')
    print(shapes)


sel = cmds.ls(sl=1)
name = ''
for s in sel:
    name = name +':'+ s[:-4]
print(name[1:])
cmds.addAttr("EyeJ2_R_FKCurve", ln="facialType", at='enum', en=name[1:], k=True)
cmds.addAttr("EyeJ2_L_FKCurve", ln="facialType", at='enum', en=name[1:], k=True)
cmds.addAttr("JawJ_M_FKCurve", ln="facialType", at='enum', en=name[1:], k=True)
for s in sel:
    name = name +':'+ s[:-4]



sel = cmds.ls(sl=1)
for i in range(27):
    condition = cmds.createNode('condition')
    print(condition)
    cmds.setAttr(condition + '.colorIfFalseR', 0)
    cmds.setAttr(condition + '.colorIfTrueR', 1)
    cmds.setAttr(condition + '.secondTerm', i)
    cmds.connectAttr('EyeJ2_L_FKCurve.facialType', condition + '.firstTerm')
    cmds.connectAttr(condition + '.outColorR', 'choice1.input[' + str(i) + ']')


