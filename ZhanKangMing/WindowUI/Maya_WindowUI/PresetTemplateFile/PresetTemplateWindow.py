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
    ################################
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
        cmds.button(l='ɾ���ޱ仯����', command='ZKM_PresetTemplate().OpenMouldLoc()')
        cmds.button(l='��ֱ��������', command='ZKM_PresetTemplate().OpenMouldLoc()')
        cmds.button(l='�������ڵ�', command='ZKM_PresetTemplate().OpenMouldLoc()')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
    ################################
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
        cmds.button(l='�������:')
        cmds.textFieldButtonGrp(cw3=(0,130,0),l='',text='',bl='���ع���')
        cmds.button(l='��Ĵָ����:')
        cmds.textFieldButtonGrp(cw3=(0, 130, 0), l='', text='', bl='���ع���')
        cmds.button(l='ʳָ����:')
        cmds.textFieldButtonGrp(cw3=(0, 130, 0), l='', text='', bl='���ع���')
        cmds.button(l='��ָ����:')
        cmds.textFieldButtonGrp(cw3=(0, 130, 0), l='', text='', bl='���ع���')
        cmds.button(l='����ָ����:')
        cmds.textFieldButtonGrp(cw3=(0, 130, 0), l='', text='', bl='���ع���')
        cmds.button(l='СĴָ����:')
        cmds.textFieldButtonGrp(cw3=(0, 130, 0), l='', text='', bl='���ع���')
        cmds.button(l='��������:')
        cmds.textFieldButtonGrp(cw3=(0, 130, 0), l='', text='', bl='���ع���')
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
        cmds.textFieldButtonGrp(cw3=(0, 200, 50), l='', text='', bl='����ǰ׺')
        cmds.rowColumnLayout(nc=2, adj=2)
        cmds.button(l='�����ֲ�����')
        cmds.button(l='ɾ�������������ǰ׺��')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
    #########################################
        child3 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button()
        cmds.button()
        cmds.button()
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

        cmds.tabLayout(tabs, edit=True, tabLabel=[(child1, '��������'), (child2, '�ֲ�����'), (child3, '�������'), (child4, '��̥�Զ�'), (child5, '�Ĵ��Զ�'), (child6, 'ȹ������')])

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






