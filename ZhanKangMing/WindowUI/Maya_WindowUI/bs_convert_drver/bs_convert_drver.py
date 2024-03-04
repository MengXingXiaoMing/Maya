#coding=gbk
import os
import sys
import inspect
import pymel.core as pm
#根目录
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

# 加载文本
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *

class ZKM_BsConvertDrverWindow():
    def ZKM_Window(self):#窗口
        if pm.window('bs_convert_drver_window', ex=1,cc='CleanWindow()'):
            pm.deleteUI('bs_convert_drver_window')
        pm.window('bs_convert_drver_window', t='bs转驱动')
        pm.rowColumnLayout(nc=1, adj=5)
        pm.text(l='请先运行adv')
        pm.textFieldButtonGrp('face_bs_grp', bl='表情bs基础组',text='face_base',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'face_bs_grp\')')
        pm.textFieldButtonGrp('face', bl='加载脸',text='face_base|face',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'face\')')
        pm.textFieldButtonGrp('tongue', bl='加载舌头',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'tongue\')')
        pm.textFieldButtonGrp('upper_teeth', bl='加载上牙',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'upper_teeth\')')
        pm.textFieldButtonGrp('lower_teeth', bl='加载下牙',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'lower_teeth\')')
        pm.textFieldButtonGrp('controller', bl='加载需要做驱动的控制器',
                              text='ChinCrease_M,Lip_L,Lip_R,lowerLip_M,upperLip_M,LipRegion_M,SmileBulge_L,SmilePull_L,lowerLipA_L,cornerLip_L,upperLipC_L,upperLipB_L,lowerLip_L,upperLip_L,lowerLipC_L,lowerLipB_L,upperLipA_L,SmileBulge_R,SmilePull_R,lowerLip_R,upperLip_R,lowerLipC_R,lowerLipB_R,lowerLipA_R,cornerLip_R,upperLipC_R,upperLipB_R,upperLipA_R,Jaw_M,NoseCorner_R,NoseUnder_M,NoseCorner_L',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'controller\')')
        pm.button(l='为所有控制器创建无效果驱动', command='ZKM_BsConvertDrverWindow().create_normal_drver()')
        #pm.button(l='清理下眼皮驱动', command='ZKM_BsConvertDrverWindow().clear()')
        pm.button(l='创建基础BS', command='ZKM_BsConvertDrverWindow().create_base_bs()')
        pm.textFieldButtonGrp('face_bs_name', bl='加载bs名称',
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'face_bs_name\')')
        pm.rowColumnLayout(nc=4, adj=3)
        pm.optionMenu('bs_convert_drver_window_bs_name_OptionMenu')
        pm.menuItem(label='m_a')
        pm.menuItem(label='m_e')
        pm.menuItem(label='m_i')
        pm.menuItem(label='m_o')
        pm.menuItem(label='m_u')
        pm.menuItem(label='m_m')
        pm.menuItem(label='m_r')
        pm.menuItem(label='m_f')
        cmds.checkBox('bs_convert_drver_window_automatic_adjustment_of_oral_cavity', label='自动调整口腔内部')
        pm.button(l='转到驱动', command='ZKM_BsConvertDrverWindow().drver()')
        pm.button(l='删除所有驱动组', command='ZKM_BsConvertDrverWindow().delete_normal_drver()')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=1)
        pm.button(l='创建当前选择创建驱动', bgc=(1, 1, 1), command='ZKM_BsConvertDrverWindow().create_drver()')
        pm.button(l='创建当前选择添加bs', bgc=(1, 1, 1), command='ZKM_BsConvertDrverWindow().create_bs()')
        pm.setParent('..')
        pm.setParent('..')
        pm.showWindow()
    def create_normal_drver(self):
        pm.mel.eval('asGoToBuildPose bodySetup;if (`objExists FaceControlSet`)asGoToBuildPose faceSetup;')
        soure_attribute = ['ctrlPhonemes_M.aaa','ctrlPhonemes_M.eh','ctrlPhonemes_M.iee','ctrlPhonemes_M.ohh',
                           'ctrlPhonemes_M.uuu','ctrlPhonemes_M.mbp','ctrlPhonemes_M.fff','ctrlPhonemes_M.rrr']
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'controller')
        pm.select('Tongue0_M','upperTeeth_M','lowerTeeth_M',add=1)
        controller = pm.ls(sl=1)
        for c in controller:
            if not pm.objExists(c+'_DrverGrp'):
                pm.select(c)
                pm.mel.doGroup(0, 1, 1)
                pm.mel.rename(c+'_DrverGrp')
            for s in soure_attribute:
                for z in ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ']:
                    loke = pm.getAttr((c + '.' + z), l=True)
                    if not loke:
                        pm.setAttr(s, 10)
                        pm.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=s)
                        pm.setAttr(s,0)
                        pm.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=s)

    def delete_normal_drver(self):
        pm.mel.eval('asGoToBuildPose bodySetup;if (`objExists FaceControlSet`)asGoToBuildPose faceSetup;')
        soure_attribute = ['ctrlPhonemes_M.aaa', 'ctrlPhonemes_M.eh', 'ctrlPhonemes_M.iee', 'ctrlPhonemes_M.ohh',
                           'ctrlPhonemes_M.uuu', 'ctrlPhonemes_M.mbp', 'ctrlPhonemes_M.fff', 'ctrlPhonemes_M.rrr']
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'controller')
        pm.select('Tongue0_M', 'upperTeeth_M', 'lowerTeeth_M', add=1)
        controller = pm.ls(sl=1)
        for c in controller:
            if pm.objExists(c + '_DrverGrp'):
                P = pm.listRelatives((c + '_DrverGrp'), p=1)
                C = pm.listRelatives((c + '_DrverGrp'), c=1)
                pm.parent(C[0],P[0])

                pm.delete((c + '_DrverGrp'))

    def clear(self):
        pm.keyframe('SDKCheekRaiser_L_translateY1', valueChange=0, index=1, absolute=1)
        pm.keyframe('SDKCheekRaiser_R_translateY1', valueChange=0, index=1, absolute=1)
        pm.keyframe('bwctrlMouthCorner_L_translateX_input_4_', valueChange=0, index=1, absolute=1)
        pm.keyframe('bwctrlMouthCorner_R_translateX_input_4_', valueChange=0, index=1, absolute=1)
        pm.keyframe('bwctrlCheek_R_translateY_input_2_', valueChange=0, index=1, absolute=1)
        pm.keyframe('bwctrlCheek_L_translateY_input_2_', valueChange=0, index=1, absolute=1)
        pm.keyframe('SDKlowerLid_L_translateY1', valueChange=0, index=1, absolute=1)
        pm.keyframe('SDKCheekRaiser_R_translateY2', valueChange=0, index=1, absolute=1)
        pm.keyframe('SDKCheekRaiser_L_translateY2', valueChange=0, index=1, absolute=1)
        pm.keyframe('SDKlowerLid_R_translateY1', valueChange=0, index=1, absolute=1)

    def create_base_bs(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_grp')
        face_bs_grp = pm.ls(sl=1)
        pm.select(face_bs_grp)
        pm.duplicate(rr=1)
        pm.mel.rename('base_bs')
        pm.select(face_bs_grp, add=1)
        bs = pm.blendShape('base_bs', face_bs_grp)
        pm.textFieldButtonGrp('face_bs_name', e=1,text=bs[0])
        pm.delete('base_bs')

    def drver(self):
        pm.mel.eval('asGoToBuildPose bodySetup;if (`objExists FaceControlSet`)asGoToBuildPose faceSetup;')
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_grp')
        face_bs_grp = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face')
        face = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'tongue')
        tongue = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'upper_teeth')
        upper_teeth = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'lower_teeth')
        lower_teethe = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'controller')
        controller = pm.ls(sl=1)
        bs_name = pm.optionMenu('bs_convert_drver_window_bs_name_OptionMenu', q=1, v=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_name')
        face_bs_name = pm.ls(sl=1)
        pm.setAttr("ctrlPhonemes_M.lntd", 0)
        pm.setAttr("ctrlPhonemes_M.aaa", 0)
        pm.setAttr("ctrlPhonemes_M.eh", 0)
        pm.setAttr("ctrlPhonemes_M.ahh", 0)
        pm.setAttr("ctrlPhonemes_M.ohh", 0)
        pm.setAttr("ctrlPhonemes_M.uuu", 0)
        pm.setAttr("ctrlPhonemes_M.iee", 0)
        pm.setAttr("ctrlPhonemes_M.rrr", 0)
        pm.setAttr("ctrlPhonemes_M.www", 0)
        pm.setAttr("ctrlPhonemes_M.sss", 0)
        pm.setAttr("ctrlPhonemes_M.fff", 0)
        pm.setAttr("ctrlPhonemes_M.tth", 0)
        pm.setAttr("ctrlPhonemes_M.mbp", 0)
        pm.setAttr("ctrlPhonemes_M.ssh", 0)
        pm.setAttr("ctrlPhonemes_M.schwa", 0)
        pm.setAttr("ctrlPhonemes_M.gk", 0)

        try:
            pm.setAttr("m_i.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_r.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_f.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_a.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_o.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_u.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_u.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_m.visibility", 0)
        except:
            pass
        try:
            pm.setAttr("m_e.visibility", 0)
        except:
            pass


        if bs_name == 'm_a':
            pm.setAttr('ctrlPhonemes_M.aaa', 10)
            pm.setAttr("m_a.visibility", 1)
        if bs_name == 'm_e':
            pm.setAttr('ctrlPhonemes_M.eh', 10)
            pm.setAttr("m_e.visibility", 1)
        if bs_name == 'm_i':
            pm.setAttr('ctrlPhonemes_M.iee', 10)
            pm.setAttr("m_i.visibility", 1)
        if bs_name == 'm_o':
            pm.setAttr('ctrlPhonemes_M.ohh', 10)
            pm.setAttr("m_o.visibility", 1)
        if bs_name == 'm_u':
            pm.setAttr('ctrlPhonemes_M.uuu', 10)
            pm.setAttr("m_u.visibility", 1)
        if bs_name == 'm_m':
            pm.setAttr('ctrlPhonemes_M.mbp', 10)
            pm.setAttr("m_m.visibility", 1)
        if bs_name == 'm_r':
            pm.setAttr('ctrlPhonemes_M.rrr', 10)
            pm.setAttr("m_r.visibility", 1)
        if bs_name == 'm_f':
            pm.setAttr('ctrlPhonemes_M.fff', 10)
            pm.setAttr("m_f.visibility", 1)
        modify = cmds.checkBox('bs_convert_drver_window_automatic_adjustment_of_oral_cavity', q=1,v=1)
        if modify:
            # 开始修改上下牙和舌头的位置
            oral_cavity = []
            oral_cavity.append(tongue[0])
            oral_cavity.append(upper_teeth[0])
            oral_cavity.append(lower_teethe[0])
            for oc in oral_cavity:
                pm.select(oc)
                absolute_name = oc.split('|')
                select_name = bs_name
                for i in range(1, len(absolute_name)):
                    select_name = select_name + '|' + absolute_name[i]

                pm.select(select_name, add=1)
                all_tongue = pm.ls(sl=1)
                shape = pm.listRelatives(all_tongue[0], s=1)
                pm.createNode('closestPointOnMesh', n=('cpom'))
                pm.connectAttr((shape[0] + '.outMesh'), ('cpom' + '.inMesh'), f=1)
                pm.spaceLocator(p=(0, 0, 0))
                loc = pm.ls(sl=1)
                pm.parentConstraint(all_tongue[0],loc,weight=1)
                #pm.geometryConstraint(all_tongue[0],loc,weight=1)
                xform = pm.getAttr(loc[0]+'.t')
                pm.setAttr(('cpom.inPositionX'), xform[0])
                pm.setAttr(('cpom.inPositionY'), xform[1])
                pm.setAttr(('cpom.inPositionZ'), xform[2])
                u = float(pm.getAttr('cpom.parameterU'))
                v = float(pm.getAttr('cpom.parameterV'))
                pm.delete(loc)
                pm.delete('cpom')
                for i in range(0, len(all_tongue)):
                    shape = pm.listRelatives(all_tongue[i], s=1)
                    pm.createNode('follicle', n=('follicleShape' + str(i)))
                    pm.connectAttr((shape[0] + '.outMesh'), ('follicleShape' + str(i) + '.inputMesh'), f=1)
                    pm.connectAttr((shape[0] + '.worldMatrix[0]'),
                                   ('follicleShape' + str(i) + '.inputWorldMatrix'), f=1)
                    pm.connectAttr(('follicleShape' + str(i) + '.outTranslate'),
                                   ('follicle' + str(i) + '.translate'), f=1)
                    pm.connectAttr(('follicleShape' + str(i) + '.outRotate'),
                                   ('follicle' + str(i) + '.rotate'),
                                   f=1)
                    pm.setAttr(('follicleShape' + str(i) + '.parameterU'), u)
                    pm.setAttr(('follicleShape' + str(i) + '.parameterV'), v)
                    pm.spaceLocator(p=(0, 0, 0), n=('Loc' + str(i)))
                    pm.delete(pm.parentConstraint('follicle' + str(i), ('Loc' + str(i)), w=1))
                    pm.delete('follicle' + str(i))

                c_name = []
                if oc == tongue[0]:
                    c_name = 'Tongue0_M'
                if oc == upper_teeth[0]:
                    c_name = 'upperTeeth_M'
                if oc == lower_teethe[0]:
                    c_name = 'lowerTeeth_M'
                pm.spaceLocator(p=(0, 0, 0), n=(c_name + '_Loc'))
                pm.delete(pm.parentConstraint(c_name, c_name+'_Loc', w=1))
                pm.parentConstraint('Loc0', c_name+'_Loc', w=1, mo=1)
                parentConstraint_1 = pm.parentConstraint(c_name+'_Loc', c_name, w=1, dr=1,mo=1)
                pm.parentConstraint('Loc1', 'Loc0', w=1)
                pm.delete(parentConstraint_1)
                pm.delete('Loc0', 'Loc1', c_name+'_Loc')

    def create_drver(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_grp')
        face_bs_grp = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face')
        face = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'tongue')
        tongue = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'upper_teeth')
        upper_teeth = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'lower_teeth')
        lower_teethe = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'controller')
        controller = pm.ls(sl=1)
        bs_name = pm.optionMenu('bs_convert_drver_window_bs_name_OptionMenu',q=1,v=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_name')
        face_bs_name = pm.ls(sl=1)

        attribute = ''
        if bs_name == 'm_a':
            attribute = 'ctrlPhonemes_M.aaa'
        if bs_name == 'm_e':
            attribute = 'ctrlPhonemes_M.eh'
        if bs_name == 'm_i':
            attribute = 'ctrlPhonemes_M.iee'
        if bs_name == 'm_o':
            attribute = 'ctrlPhonemes_M.ohh'
        if bs_name == 'm_u':
            attribute = 'ctrlPhonemes_M.uuu'
        if bs_name == 'm_m':
            attribute = 'ctrlPhonemes_M.mbp'
        if bs_name == 'm_r':
            attribute = 'ctrlPhonemes_M.rrr'
        if bs_name == 'm_f':
            attribute = 'ctrlPhonemes_M.fff'
        # 生成驱动
        pm.select(controller,'Tongue0_M', 'upperTeeth_M', 'lowerTeeth_M')
        all_controller = pm.ls(sl=1)
        for c in all_controller:
            for z in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']:
                # 获取旧驱动数值
                old_num = pm.getAttr((c + '_DrverGrp.' + z))
                # 获取控制器数值
                new_num = pm.getAttr((c + '.' + z))
                # 两者相加后控制器数值归零，驱动组数值为加完的数值，然后设置关键帧
                new_num = old_num + new_num
                loke = pm.getAttr((c + '.' + z), l=True)
                if not loke:
                    pm.setAttr((c + '.' + z), 0)
                    pm.setAttr(attribute, 0)
                    pm.setAttr((c + '_DrverGrp.' + z), 0)
                    pm.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=attribute)
                    pm.setAttr(attribute, 10)
                    pm.setAttr((c + '_DrverGrp.' + z), new_num)
                    pm.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=attribute)

        if bs_name == 'm_a':
            pm.setAttr('ctrlPhonemes_M.aaa', 10)
        if bs_name == 'm_e':
            pm.setAttr('ctrlPhonemes_M.eh', 10)
        if bs_name == 'm_i':
            pm.setAttr('ctrlPhonemes_M.iee', 10)
        if bs_name == 'm_o':
            pm.setAttr('ctrlPhonemes_M.ohh', 10)
        if bs_name == 'm_u':
            pm.setAttr('ctrlPhonemes_M.uuu', 10)
        if bs_name == 'm_m':
            pm.setAttr('ctrlPhonemes_M.mbp', 10)
        if bs_name == 'm_r':
            pm.setAttr('ctrlPhonemes_M.rrr', 10)
        if bs_name == 'm_f':
            pm.setAttr('ctrlPhonemes_M.fff', 10)

    def create_bs(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_grp')
        face_bs_grp = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face')
        face = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'tongue')
        tongue = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'upper_teeth')
        upper_teeth = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'lower_teeth')
        lower_teethe = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'controller')
        controller = pm.ls(sl=1)
        bs_name = pm.optionMenu('bs_convert_drver_window_bs_name_OptionMenu', q=1, v=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_name')
        face_bs_name = pm.ls(sl=1)
        # 查询别名
        name = []
        w_name = []
        if pm.objExists(face_bs_name[0]):
            all_bs_name = pm.aliasAttr(face_bs_name[0], q=1)
            for i in range(0, len(all_bs_name)):
                if i % 2 == 0:
                    name.append(all_bs_name[i])
                else:
                    w_name.append(all_bs_name[i])
        # 如果名称存在则删除
        num = []
        for i in range(0, len(name)):
            if name[i] == 'base_bs':
                num = int(w_name[i][-2:-1])
                break
        for i in range(0, len(name)):
            if name[i] == bs_name:
                pm.mel.blendShapeDeleteTargetGroup(face_bs_name[0], int(w_name[i][-2:-1]))
        # 修改基础bs别名
        pm.setAttr(face_bs_name[0] + '.base_bs', 1)
        pm.aliasAttr(bs_name, (face_bs_name[0] + '.base_bs'))
        # 打开编辑
        pm.sculptTarget(face_bs_name[0], e=1, target=num)
        # 开始矫正位置
        pm.select(face)
        absolute_name = face[0].split('|')
        select_name = bs_name
        for i in range(1, len(absolute_name)):
            select_name = select_name + '|' + absolute_name[i]
        pm.select(select_name, add=1)
        sel = pm.ls(sl=1)
        pm.select(sel[0] + ".vtx[*]")
        sel_A = pm.ls(fl=1, sl=1)
        pm.select(sel[1] + ".vtx[*]")
        sel_B = pm.ls(fl=1, sl=1)
        for i in range(0, len(sel_A)):
            a = pm.xform(sel_A[i], q=1, ws=1, t=1)
            b = pm.xform(sel_B[i], q=1, ws=1, t=1)
            pm.select(sel_A[i])
            pm.move((b[0] - a[0]), (b[1] - a[1]), (b[2] - a[2]), r=1)
        # 关闭编辑
        pm.sculptTarget(face_bs_name[0], e=1, target=num)
        # 添加bs驱动
        multiplyDivide = pm.shadingNode('multiplyDivide', asUtility=1)
        pm.setAttr((multiplyDivide + '.input2X'), 0.1)
        attribute = ''
        if bs_name == 'm_a':
            attribute = 'ctrlPhonemes_M.aaa'
        if bs_name == 'm_e':
            attribute = 'ctrlPhonemes_M.eh'
        if bs_name == 'm_i':
            attribute = 'ctrlPhonemes_M.iee'
        if bs_name == 'm_o':
            attribute = 'ctrlPhonemes_M.ohh'
        if bs_name == 'm_u':
            attribute = 'ctrlPhonemes_M.uuu'
        if bs_name == 'm_m':
            attribute = 'ctrlPhonemes_M.mbp'
        if bs_name == 'm_r':
            attribute = 'ctrlPhonemes_M.rrr'
        if bs_name == 'm_f':
            attribute = 'ctrlPhonemes_M.fff'
        pm.connectAttr(attribute, (multiplyDivide + '.input1X'), f=1)
        pm.connectAttr((multiplyDivide + '.outputX'), (face_bs_name[0] + '.' + bs_name), f=1)
        # 创建静止bs
        pm.mel.eval('asGoToBuildPose bodySetup;if (`objExists FaceControlSet`)asGoToBuildPose faceSetup;')
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_grp')
        face_bs_grp = pm.ls(sl=1)
        pm.select(face_bs_grp)
        pm.duplicate(rr=1)
        pm.mel.rename('base_bs')
        pm.select(face_bs_grp, add=1)
        pm.blendShape(face_bs_name[0], e=1, t=(face_bs_grp[0], num+1, 'base_bs', 1))
        pm.delete('base_bs')

        if bs_name == 'm_a':
            pm.setAttr('ctrlPhonemes_M.aaa', 10)
        if bs_name == 'm_e':
            pm.setAttr('ctrlPhonemes_M.eh', 10)
        if bs_name == 'm_i':
            pm.setAttr('ctrlPhonemes_M.iee', 10)
        if bs_name == 'm_o':
            pm.setAttr('ctrlPhonemes_M.ohh', 10)
        if bs_name == 'm_u':
            pm.setAttr('ctrlPhonemes_M.uuu', 10)
        if bs_name == 'm_m':
            pm.setAttr('ctrlPhonemes_M.mbp', 10)
        if bs_name == 'm_r':
            pm.setAttr('ctrlPhonemes_M.rrr', 10)
        if bs_name == 'm_f':
            pm.setAttr('ctrlPhonemes_M.fff', 10)
ShowWindow = ZKM_BsConvertDrverWindow()
if __name__ =='__main__':
    ShowWindow.ZKM_Window()
    pass

#删除无影响驱动
