# coding=gbk
# ��ȡ�ļ�·��
import os
import inspect
import sys
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
file_pathPresetTemplate = os.path.join(cur_dir)  # ��ȡ�ļ�·��
sys.path.append(file_pathPresetTemplate)
# �����
import PresetTemplate
from PresetTemplate import *
sys.dont_write_bytecode = True



class PresetTemplateWindowClass:
    def __init__(self):
        # ͨ��self���½��Ķ����г�ʼ������
        global file_path
        global file_pathA
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        # print(file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathReversion = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
    def PresetTemplateWindow(self):#����
        if cmds.window('PresetTemplate', ex=1):
            cmds.deleteUI('PresetTemplate')
            ZKM_PresetTemplate().CleanWindow()
        cmds.window('PresetTemplate',t="Ԥ��ģ��",cc='ZKM_PresetTemplate().CleanWindow()')
        form = cmds.formLayout()
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(form, edit=True,attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))
        # ��������
        child1 = cmds.rowColumnLayout(nc=2,adj=2)
        cmds.formLayout()
        cmds.paneLayout('modelPanel_paneLayout',w=400, h=400)

        modelPanelEditor = cmds.modelPanel(p='modelPanel_paneLayout')
        cmds.setParent('..')
        modelPanelCamera = cmds.camera(n='FaceCamera1',position=(0, 0, 20))
        cmds.modelPanel(modelPanelEditor, edit=True, camera=modelPanelCamera[0])

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=1, adj=5)
        cmds.rowColumnLayout(nc=4, adj=1)

        cmds.button(l='ʹ�ð���', command='os.startfile(\''+self.file_path+'\Help.txt\')')
        cmds.textFieldButtonGrp('LoadName',cw2=(150,10),bl='����ģ��',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadName\')')
        cmds.textFieldButtonGrp('LoadBS', cw2=(150,10),bl='����BS',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadBS\')')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\')')
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=3, adj=4)
        cmds.rowColumnLayout(nc=2, adj=1)
        cmds.button(l='�򿪲�ͬ�ز�����Bs����', bgc=(1,1,1),command='ZKM_PresetTemplate().Open_DifferentTopologyTransfer_BS()')
        cmds.button(l='ѡ��ģ�͵�Ϊģ��', command='ZKM_PresetTemplate().AlsVorlageImportieren()')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=1)
        pm.optionMenu('LoadBsModelTemplate', cc='ZKM_PresetTemplate().ModifyLocPreset(\'GenerateLocatorScheme\')')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial'), 0,'.ma')):
            pm.menuItem(label=file)
        cmds.button(l='����',command='ZKM_PresetTemplate().LoadEmoticonTemplate(\'LoadBsModelTemplate\',\'Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial\',0)')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\')')
        cmds.rowColumnLayout('ChangeRowColumnLayout',nc=1, adj=1)
        pm.optionMenu('GenerateLocatorScheme')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_pathReversion+'/Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial/'+(pm.optionMenu('LoadBsModelTemplate',q=1, value=1))+'_Programme'),0,'.ma')):
            pm.menuItem(label=file)
        cmds.setParent('..')


        cmds.rowColumnLayout(nc=4, adj=1)
        cmds.button('ImportLocButton',l='���붨λ��', command='ZKM_PresetTemplate().ImportLoc()')
        cmds.checkBox('OPorEDScriptJob',label='���ؽű�', value=1)
        cmds.checkBox('RemoveKeepmirror',label='�ƶ����ֶԳ�', value=1,cc='SymmetricLink()')
        cmds.button(l='���涨λ���ļ�', command='ZKM_PresetTemplate().OpenMouldLoc()')
        cmds.setParent('..')
        cmds.iconTextButton('ChangeIconTextButton',style='iconOnly', image1='fileNew.png',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\')')

        cmds.rowColumnLayout(nc=1, adj=1)
        pm.optionMenu('ControllerGenerationMethod')
        pm.menuItem(label="���ֳ���")
        pm.menuItem(label="��������")
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=4, adj=2)
        cmds.checkBox('AdsorptionSurface', label='��������', value=1)
        cmds.button(l='���ɿ�����', command='ZKM_PresetTemplate().CreateController()')
        cmds.button(l='��SSDR����Ȩ��', bgc=(0,0.8,0.8),command='ZKM_PresetTemplate().CreateController()')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',vis=0)

        cmds.rowColumnLayout(nc=2, adj=1)
        pm.optionMenu('AddAutomatic')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path+'\Py_PresetTemplate_Material\AutoLinkBsScheme\AddAttributes'),1, '.py','.mel')):
            pm.menuItem(file, label=file)
        pm.optionMenu('LinkBs')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\AutoLinkBsScheme\LinkBs'), 1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=1)
        cmds.button(l='��Ӷ�Ӧ�����Լ����������Զ����ӵ�bs', command='ZKM_PresetTemplate().AddAttributesAndAink()')
        cmds.button(l='������ת��Ϊ����', command='ZKM_PresetTemplate().BsConvertControllerDrive()')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\AutoLinkBsScheme\')')

        pm.optionMenu('CustomPanel', label="")
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\CustomPanel'),0, '.ma')):
            pm.menuItem(file, label=file)
        cmds.rowColumnLayout(nc=5, adj=3)
        cmds.button(l='�����Զ������', command='ZKM_PresetTemplate().ImportFile(\'CustomPanel\',\'Py_PresetTemplate_Material/CustomPanel\',1,\'.ma\',\'mayaAscii\')')
        pm.optionMenu('CustomPanelLink', label="")
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\CustomPanel'),1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='�����Զ�������', command='ZKM_PresetTemplate().RunCorrespondingCommand()')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\CustomPanel\')')
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=4, adj=4)
        cmds.button(l='��ʾ����', command='ZKM_AttributeClass().ZKM_ShowSelectAllAttributes()')
        cmds.button(l='������������������', command='ZKM_AttributeClass().ZKM_SelHideUselessAttributes()')
        cmds.button(l='����μ������Լ�������', command='ZKM_PresetTemplate().SupplementJointController()')
        cmds.textFieldGrp('BsIntermediateFrameIntervalSymbol',label='BS�м�֡�淶',cw2=(70,170))
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=3, adj=1)
        pm.optionMenu('FilmSpecifications')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\BS_IntermediateFrame_FilmSpecificationScheme'), 1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='Ӱ�ӹ淶�޸�BS�м�֡', command='ZKM_PresetTemplate().FilmCustomLinks()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\BS_IntermediateFrame_FilmSpecificationScheme\')')

        pm.optionMenu('GameSpecifications', label="")
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\BS_IntermediateFrame_GameSpecificationScheme'),1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='UE�淶�޸�BS�м�֡', command='ZKM_PresetTemplate().GameCustomLinks()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\BS_IntermediateFrame_GameSpecificationScheme\')')

        pm.optionMenu('CustomModification')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\CustomModification'),1,'.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='�Զ����޸�', command='ZKM_PresetTemplate().CustomModification()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\CustomModification\')')

        pm.optionMenu('AutomaticSynchronization',cc='AutomaticSynchronization()')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\AutomaticSynchronizationSettings'),0, '.txt')):
            pm.menuItem(file, label=file)
        cmds.button(l='����ҳ��', command='ZKM_PresetTemplate().SavePage()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\AutomaticSynchronizationSettings\')')
        cmds.textFieldGrp('NewFileName', label='�ļ�����')
        cmds.button(l='�½�ҳ��', command='ZKM_PresetTemplate().NewPage()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\AutomaticSynchronizationSettings\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=3, adj=4)
        cmds.button(l='ɾ���ޱ仯����', command='ZKM_PresetTemplate().DeleteUnchangedDrive()')
        cmds.button(l='��ֱ��������', command='ZKM_PresetTemplate().StraightenAllDrives()')
        cmds.button(l='�������ڵ�', command='ZKM_PresetTemplate().DeleteUselessNodes()')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        # �ֲ�����
        child2 = cmds.rowColumnLayout(nc=1,adj=2)
        cmds.rowColumnLayout(nc=2, adj=5)
        PictureFormLayout=cmds.formLayout()
        cmds.picture(i=(self.file_pathReversion + "/Py_PresetTemplate_Material/PresetTemplate_PictureMaterial/�ֲ�����BGC.png"))
        PictureFormLayoutHandButton=cmds.button(l='�������',bgc=(1,1,1))
        PictureFormLayoutThumbButton=cmds.button(l='��Ĵָ',bgc=(1,1,1))
        PictureFormLayoutIndexFingerButton=cmds.button(l='ʳָ',bgc=(1,1,1))
        PictureFormLayoutMiddleFingerButton=cmds.button(l='��ָ',bgc=(1,1,1))
        PictureFormLayoutRingFingerButton=cmds.button(l='����ָ',bgc=(1,1,1))
        PictureFormLayoutLittleFingerButton = cmds.button(l='СĴָ',bgc=(1,1,1))
        PictureFormLayoutSulcusBoneButton = cmds.button(l='����',bgc=(1,1,1))
        cmds.setParent('..')
        pm.formLayout(PictureFormLayout,
                      edit=1,
                      attachPosition=[(PictureFormLayoutHandButton, "top", 190, 0),
                                      (PictureFormLayoutThumbButton, "top", 220, 0),
                                      (PictureFormLayoutIndexFingerButton, "top", 240, 0),
                                      (PictureFormLayoutMiddleFingerButton, "top", 190, 0),
                                      (PictureFormLayoutRingFingerButton, "top", 140, 0),
                                      (PictureFormLayoutLittleFingerButton, "top", 110, 0),
                                      (PictureFormLayoutSulcusBoneButton, "top", 165, 0)],
                      attachForm=[(PictureFormLayoutHandButton, "left", 10),
                                  (PictureFormLayoutThumbButton, "left", 50),
                                  (PictureFormLayoutIndexFingerButton, "left", 200),
                                  (PictureFormLayoutMiddleFingerButton, "left", 210),
                                  (PictureFormLayoutRingFingerButton, "left", 200),
                                  (PictureFormLayoutLittleFingerButton, "left", 180),
                                  (PictureFormLayoutSulcusBoneButton, "left", 60)])
        cmds.rowColumnLayout(nc=1, adj=5)
        cmds.rowColumnLayout(nc=2,adj=6)
        cmds.button(l='�������:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveWristJoint\')')
        cmds.textFieldButtonGrp('ArmDriveWristJoint',cw3=(0,130,0),l='',text='',bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveWristJoint\')')
        cmds.button(l='��Ĵָ����:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveThumbCurve\')')
        cmds.textFieldButtonGrp('ArmDriveThumbCurve',cw3=(0, 130, 0), l='', text='', bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveThumbCurve\')')
        cmds.button(l='ʳָ����:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveIndexFingerCurve\')')
        cmds.textFieldButtonGrp('ArmDriveIndexFingerCurve',cw3=(0, 130, 0), l='', text='', bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveIndexFingerCurve\')')
        cmds.button(l='��ָ����:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveMiddleFingerCurve\')')
        cmds.textFieldButtonGrp('ArmDriveMiddleFingerCurve',cw3=(0, 130, 0), l='', text='', bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveMiddleFingerCurve\')')
        cmds.button(l='����ָ����:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveRingFingerCurve\')')
        cmds.textFieldButtonGrp('ArmDriveRingFingerCurve',cw3=(0, 130, 0), l='', text='', bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveRingFingerCurve\')')
        cmds.button(l='СĴָ����:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDrivePinkieCurve\')')
        cmds.textFieldButtonGrp('ArmDrivePinkieCurve',cw3=(0, 130, 0), l='', text='', bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDrivePinkieCurve\')')
        cmds.button(l='��������:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveUncinateCurve\')')
        cmds.textFieldButtonGrp('ArmDriveUncinateCurve',cw3=(0, 130, 0), l='', text='', bl='���ع���',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveUncinateCurve\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=3)
        pm.text(l='���ǳ���')
        pm.rowColumnLayout(numberOfColumns=6)
        cmds.radioCollection('PresetTemplateHandDriveGougu')
        cmds.radioButton('PresetTemplateHandDrive_Gougu_X', label="X")
        cmds.radioButton('PresetTemplateHandDrive_Gougu_fX', label="-X")
        cmds.radioButton('PresetTemplateHandDrive_Gougu_Y', label="Y")
        cmds.radioButton('PresetTemplateHandDrive_Gougu_fY', label="-Y")
        cmds.radioButton('PresetTemplateHandDrive_Gougu_Z', label="Z")
        cmds.radioButton('PresetTemplateHandDrive_Gougu_fZ', label="-Z")
        pm.radioCollection('PresetTemplateHandDriveGougu', edit=1, select="PresetTemplateHandDrive_Gougu_X")
        cmds.setParent('..')
        pm.text(l='��ָ����')
        pm.rowColumnLayout(numberOfColumns=6)
        cmds.radioCollection('PresetTemplateHandDriveWuZhi')
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_X', label="X")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_fX', label="-X")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_Y', label="Y")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_fY', label="-Y")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_Z', label="Z")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_fZ', label="-Z")
        pm.radioCollection('PresetTemplateHandDriveWuZhi', edit=1, select="PresetTemplateHandDrive_WuZhi_Y")
        cmds.setParent('..')
        pm.text(l='Spread����')
        pm.rowColumnLayout(numberOfColumns=6)
        cmds.radioCollection('PresetTemplateHandDriveSpread')
        cmds.radioButton('PresetTemplateHandDrive_Spread_X', label="X")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fX', label="-X")
        cmds.radioButton('PresetTemplateHandDrive_Spread_Y', label="Y")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fY', label="-Y")
        cmds.radioButton('PresetTemplateHandDrive_Spread_Z', label="Z")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fZ', label="-Z")
        pm.radioCollection('PresetTemplateHandDriveSpread', edit=1, select="PresetTemplateHandDrive_Spread_Z")
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.textFieldButtonGrp('ArmDrivePrefix',cw3=(0, 200, 50), l='', text='', bl='����ǰ׺',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDrivePrefix\')')
        cmds.rowColumnLayout(nc=2, adj=2)
        cmds.button(l='�����ֲ�����',c='ZKM_PresetTemplateHandDrive().PresetTemplateCreateHandDrive()')
        cmds.button(l='ɾ�������������ǰ׺��',c='ZKM_PresetTemplateHandDrive().PresetTemplateDeleteHandDrive()')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        # �������
        child3 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.rowColumnLayout(nc=2, adj=7)
        PictureFormLayout1 = cmds.formLayout()
        cmds.picture(
            i=(self.file_pathReversion + "/Py_PresetTemplate_Material/PresetTemplate_PictureMaterial/�������BGC.png"))
        PictureFormLayoutWingHandButton = cmds.button(l='�ֱ�����', bgc=(1, 1, 1))
        PictureFormLayoutWingMarginButton = cmds.button(l='��Ե��������', bgc=(1, 1, 1))
        PictureFormLayoutWingThumbButton = cmds.button(l='��Ĵָ', bgc=(1, 1, 1))
        PictureFormLayoutWingPrimaryButton = cmds.button(l='������������', bgc=(1, 1, 1))
        PictureFormLayoutWingSecondaryButton = cmds.button(l='�μ���������', bgc=(1, 1, 1))
        PictureFormLayoutWingThreeButton = cmds.button(l='������������', bgc=(1, 1, 1))
        cmds.setParent('..')
        pm.formLayout(PictureFormLayout1,
                      edit=1,
                      attachPosition=[(PictureFormLayoutWingHandButton, "top", 120, 0),
                                      (PictureFormLayoutWingMarginButton, "top", 30, 0),
                                      (PictureFormLayoutWingThumbButton, "top", 30, 0),
                                      (PictureFormLayoutWingPrimaryButton, "top", 300, 0),
                                      (PictureFormLayoutWingSecondaryButton, "top", 320, 0),
                                      (PictureFormLayoutWingThreeButton, "top", 360, 0)],
                      attachForm=[(PictureFormLayoutWingHandButton, "left", 10),
                                  (PictureFormLayoutWingMarginButton, "left", 15),
                                  (PictureFormLayoutWingThumbButton, "left", 370),
                                  (PictureFormLayoutWingPrimaryButton, "left", 540),
                                  (PictureFormLayoutWingSecondaryButton, "left", 250),
                                  (PictureFormLayoutWingThreeButton, "left", 80)])
        cmds.rowColumnLayout(nc=1, adj=5)
        cmds.rowColumnLayout(nc=2, adj=4)
        cmds.button(l='�粿����:')
        cmds.textFieldButtonGrp('WingDriveShoulderCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveShoulderCurve\')')
        cmds.button(l='��������:')
        cmds.textFieldButtonGrp('WingDriveElbowCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveElbowCurve\')')
        cmds.button(l='��������:')
        cmds.textFieldButtonGrp('WingDriveWristCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveWristCurve\')')
        cmds.button(l='��Ĵָ����:')
        cmds.textFieldButtonGrp('WingDriveThumbCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveThumbCurve\')')
        cmds.setParent('..')
        cmds.text(l='�������ֳ�������˳�򱣳�һ��')
        cmds.rowColumnLayout(nc=2, adj=6)
        cmds.button(l='������������:')
        cmds.textFieldButtonGrp('WingDrivePrimaryFlyingFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDrivePrimaryFlyingFeatherCurve\')')
        cmds.button(l='�μ���������:')
        cmds.textFieldButtonGrp('WingDriveSecondaryFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveSecondaryFeatherCurve\')')
        cmds.button(l='������������:')
        cmds.textFieldButtonGrp('WingDriveLevelThreeFlyingFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='��������',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveLevelThreeFlyingFeatherCurve\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=1, adj=5)
        pm.intSliderGrp('KZQDX', l='��Ե�����������߹�����', min=1, max=10, v=6, f=1, cc="KZQDX", cw3=(120, 20, 100))
        cmds.text(l='��������Ӧ��ĩ�˹�������˳��һ��')
        cmds.textFieldButtonGrp(cw3=(0, 200, 0), l='', text='', bl='��������')
        cmds.rowColumnLayout(nc=2, adj=1)
        cmds.button(l='������������������')
        cmds.button(l='��ĩ�˹�������������')
        cmds.button(l='ѡ��������Ӧ�Ŀ�����')
        cmds.button(l='ѡ��������Ӧ��ĩ�˹���')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=3)

        pm.text(l='��ë����')
        pm.rowColumnLayout(numberOfColumns=6)
        cmds.radioCollection('PresetTemplateHandDriveWuZhi2')
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_X2', label="X")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_fX2', label="-X")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_Y2', label="Y")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_fY2', label="-Y")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_Z2', label="Z")
        cmds.radioButton('PresetTemplateHandDrive_WuZhi_fZ2', label="-Z")
        pm.radioCollection('PresetTemplateHandDriveWuZhi2', edit=1, select="PresetTemplateHandDrive_WuZhi_Y2")
        cmds.setParent('..')
        pm.text(l='Spread����')
        pm.rowColumnLayout(numberOfColumns=6)
        cmds.radioCollection('PresetTemplateHandDriveSpread3')
        cmds.radioButton('PresetTemplateHandDrive_Spread_X3', label="X")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fX3', label="-X")
        cmds.radioButton('PresetTemplateHandDrive_Spread_Y3', label="Y")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fY3', label="-Y")
        cmds.radioButton('PresetTemplateHandDrive_Spread_Z3', label="Z")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fZ3', label="-Z")
        pm.radioCollection('PresetTemplateHandDriveSpread3', edit=1, select="PresetTemplateHandDrive_Spread_Z3")
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.textFieldButtonGrp(cw3=(0, 200, 50), l='', text='', bl='����ǰ׺')
        cmds.rowColumnLayout(nc=2, adj=2)
        cmds.button(l='���ɳ������')
        cmds.button(l='ɾ����������ǰ׺��')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')




        child4 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button()
        cmds.button()
        cmds.button()
        cmds.setParent('..')

        child5 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button()
        cmds.button()
        cmds.button()
        cmds.setParent('..')

        child6 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button()
        cmds.button()
        cmds.button()
        cmds.setParent('..')
        #########################################
        child7 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button()
        cmds.button()
        cmds.button()
        cmds.setParent('..')

        cmds.tabLayout(tabs, edit=True, tabLabel=[(child1, '��������'), (child2, '�ֲ�����'), (child3, '�������'), (child4, '��̥�Զ�'), (child5, '�Ĵ��Զ�'), (child6, 'ȹ������'), (child7, '�۾��������')])

        cmds.showWindow()
if __name__ =='__main__':
    global file_path
    global file_pathA
    try:
        ZKM_PresetTemplate().DeleteScriptJob(jobNum)
    except:
        pass
    PresetTemplateWindowClass().PresetTemplateWindow()
    PresetTemplate.ZKM_PresetTemplate().AutomaticSynchronizationSettings()



def PresetTemplateCreateWingDrive():

    pass







