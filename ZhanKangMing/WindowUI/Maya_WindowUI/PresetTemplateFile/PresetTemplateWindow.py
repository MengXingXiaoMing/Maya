# coding=gbk
# 获取文件路径
import os
import inspect
import sys
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_pathPresetTemplate = os.path.join(cur_dir)  # 获取文件路径
sys.path.append(file_pathPresetTemplate)
# 导入库
import PresetTemplate
from PresetTemplate import *
sys.dont_write_bytecode = True



class PresetTemplateWindowClass:
    def __init__(self):
        # 通过self向新建的对象中初始化属性
        global file_path
        global file_pathA
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        # print(file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
    def PresetTemplateWindow(self):#窗口
        if cmds.window('PresetTemplate', ex=1):
            cmds.deleteUI('PresetTemplate')
            ZKM_PresetTemplate().CleanWindow()
        cmds.window('PresetTemplate',t="预置模板",cc='ZKM_PresetTemplate().CleanWindow()')
        form = cmds.formLayout()
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(form, edit=True,attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))
        # 表情驱动
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

        cmds.button(l='使用帮助', command='os.startfile(\''+self.file_path+'\Help.txt\')')
        cmds.textFieldButtonGrp('LoadName',cw2=(150,10),bl='加载模型',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadName\')')
        cmds.textFieldButtonGrp('LoadBS', cw2=(150,10),bl='加载BS',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadBS\')')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\')')
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=3, adj=4)
        cmds.rowColumnLayout(nc=2, adj=1)
        cmds.button(l='打开不同拓补传递Bs窗口', bgc=(1,1,1),command='ZKM_PresetTemplate().Open_DifferentTopologyTransfer_BS()')
        cmds.button(l='选择模型导为模板', command='ZKM_PresetTemplate().AlsVorlageImportieren()')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=1)
        pm.optionMenu('LoadBsModelTemplate', cc='ZKM_PresetTemplate().ModifyLocPreset(\'GenerateLocatorScheme\')')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial'), 0,'.ma')):
            pm.menuItem(label=file)
        cmds.button(l='载入',command='ZKM_PresetTemplate().LoadEmoticonTemplate(\'LoadBsModelTemplate\',\'Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial\',0)')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\')')
        cmds.rowColumnLayout('ChangeRowColumnLayout',nc=1, adj=1)
        pm.optionMenu('GenerateLocatorScheme')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_pathReversion+'/Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial/'+(pm.optionMenu('LoadBsModelTemplate',q=1, value=1))+'_Programme'),0,'.ma')):
            pm.menuItem(label=file)
        cmds.setParent('..')


        cmds.rowColumnLayout(nc=4, adj=1)
        cmds.button('ImportLocButton',l='导入定位器', command='ZKM_PresetTemplate().ImportLoc()')
        cmds.checkBox('OPorEDScriptJob',label='开关脚本', value=1)
        cmds.checkBox('RemoveKeepmirror',label='移动保持对称', value=1,cc='SymmetricLink()')
        cmds.button(l='保存定位器文件', command='ZKM_PresetTemplate().OpenMouldLoc()')
        cmds.setParent('..')
        cmds.iconTextButton('ChangeIconTextButton',style='iconOnly', image1='fileNew.png',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\')')

        cmds.rowColumnLayout(nc=1, adj=1)
        pm.optionMenu('ControllerGenerationMethod')
        pm.menuItem(label="保持朝向")
        pm.menuItem(label="保持世界")
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=4, adj=2)
        cmds.checkBox('AdsorptionSurface', label='吸附表面', value=1)
        cmds.button(l='生成控制器', command='ZKM_PresetTemplate().CreateController()')
        cmds.button(l='打开SSDR计算权重', bgc=(0,0.8,0.8),command='ZKM_PresetTemplate().CreateController()')
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
        cmds.button(l='添加对应属性以及将控制器自动链接到bs', command='ZKM_PresetTemplate().AddAttributesAndAink()')
        cmds.button(l='控制器转换为驱动', command='ZKM_PresetTemplate().BsConvertControllerDrive()')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\AutoLinkBsScheme\')')

        pm.optionMenu('CustomPanel', label="")
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\CustomPanel'),0, '.ma')):
            pm.menuItem(file, label=file)
        cmds.rowColumnLayout(nc=5, adj=3)
        cmds.button(l='导入自定义面板', command='ZKM_PresetTemplate().ImportFile(\'CustomPanel\',\'Py_PresetTemplate_Material/CustomPanel\',1,\'.ma\',\'mayaAscii\')')
        pm.optionMenu('CustomPanelLink', label="")
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\CustomPanel'),1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='运行自定义链接', command='ZKM_PresetTemplate().RunCorrespondingCommand()')
        cmds.setParent('..')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\CustomPanel\')')
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=4, adj=4)
        cmds.button(l='显示属性', command='ZKM_AttributeClass().ZKM_ShowSelectAllAttributes()')
        cmds.button(l='锁定并隐藏无用属性', command='ZKM_AttributeClass().ZKM_SelHideUselessAttributes()')
        cmds.button(l='补充次级骨骼以及控制器', command='ZKM_PresetTemplate().SupplementJointController()')
        cmds.textFieldGrp('BsIntermediateFrameIntervalSymbol',label='BS中间帧规范',cw2=(70,170))
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=3, adj=1)
        pm.optionMenu('FilmSpecifications')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\BS_IntermediateFrame_FilmSpecificationScheme'), 1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='影视规范修改BS中间帧', command='ZKM_PresetTemplate().FilmCustomLinks()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\BS_IntermediateFrame_FilmSpecificationScheme\')')

        pm.optionMenu('GameSpecifications', label="")
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\BS_IntermediateFrame_GameSpecificationScheme'),1, '.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='UE规范修改BS中间帧', command='ZKM_PresetTemplate().GameCustomLinks()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\BS_IntermediateFrame_GameSpecificationScheme\')')

        pm.optionMenu('CustomModification')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\CustomModification'),1,'.py','.mel')):
            pm.menuItem(file, label=file)
        cmds.button(l='自定义修改', command='ZKM_PresetTemplate().CustomModification()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\CustomModification\')')

        pm.optionMenu('AutomaticSynchronization',cc='AutomaticSynchronization()')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Py_PresetTemplate_Material\AutomaticSynchronizationSettings'),0, '.txt')):
            pm.menuItem(file, label=file)
        cmds.button(l='保存页面', command='ZKM_PresetTemplate().SavePage()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\AutomaticSynchronizationSettings\')')
        cmds.textFieldGrp('NewFileName', label='文件名称')
        cmds.button(l='新建页面', command='ZKM_PresetTemplate().NewPage()')
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png', label='LoadEmoticonTemplate()',command='os.startfile(\'' + self.file_path + '\Py_PresetTemplate_Material\AutomaticSynchronizationSettings\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=3, adj=4)
        cmds.button(l='删除无变化驱动', command='ZKM_PresetTemplate().DeleteUnchangedDrive()')
        cmds.button(l='打直所有驱动', command='ZKM_PresetTemplate().StraightenAllDrives()')
        cmds.button(l='清理多余节点', command='ZKM_PresetTemplate().DeleteUselessNodes()')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        # 手部驱动
        child2 = cmds.rowColumnLayout(nc=1,adj=2)
        cmds.rowColumnLayout(nc=2, adj=5)
        PictureFormLayout=cmds.formLayout()
        cmds.picture(i=(self.file_pathReversion + "/Py_PresetTemplate_Material/PresetTemplate_PictureMaterial/手部驱动BGC.png"))
        PictureFormLayoutHandButton=cmds.button(l='手腕骨骼',bgc=(1,1,1))
        PictureFormLayoutThumbButton=cmds.button(l='大拇指',bgc=(1,1,1))
        PictureFormLayoutIndexFingerButton=cmds.button(l='食指',bgc=(1,1,1))
        PictureFormLayoutMiddleFingerButton=cmds.button(l='中指',bgc=(1,1,1))
        PictureFormLayoutRingFingerButton=cmds.button(l='无名指',bgc=(1,1,1))
        PictureFormLayoutLittleFingerButton = cmds.button(l='小拇指',bgc=(1,1,1))
        PictureFormLayoutSulcusBoneButton = cmds.button(l='钩骨',bgc=(1,1,1))
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
        cmds.button(l='手腕骨骼:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveWristJoint\')')
        cmds.textFieldButtonGrp('ArmDriveWristJoint',cw3=(0,130,0),l='',text='',bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveWristJoint\')')
        cmds.button(l='大拇指样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveThumbCurve\')')
        cmds.textFieldButtonGrp('ArmDriveThumbCurve',cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveThumbCurve\')')
        cmds.button(l='食指样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveIndexFingerCurve\')')
        cmds.textFieldButtonGrp('ArmDriveIndexFingerCurve',cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveIndexFingerCurve\')')
        cmds.button(l='中指样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveMiddleFingerCurve\')')
        cmds.textFieldButtonGrp('ArmDriveMiddleFingerCurve',cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveMiddleFingerCurve\')')
        cmds.button(l='无名指样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveRingFingerCurve\')')
        cmds.textFieldButtonGrp('ArmDriveRingFingerCurve',cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveRingFingerCurve\')')
        cmds.button(l='小拇指样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDrivePinkieCurve\')')
        cmds.textFieldButtonGrp('ArmDrivePinkieCurve',cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDrivePinkieCurve\')')
        cmds.button(l='钩骨样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveUncinateCurve\')')
        cmds.textFieldButtonGrp('ArmDriveUncinateCurve',cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveUncinateCurve\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=3)
        pm.text(l='沟骨朝向：')
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
        pm.text(l='五指朝向：')
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
        pm.text(l='Spread朝向：')
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
        cmds.textFieldButtonGrp('ArmDrivePrefix',cw3=(0, 200, 50), l='', text='', bl='加载前缀',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDrivePrefix\')')
        cmds.rowColumnLayout(nc=2, adj=2)
        cmds.button(l='生成手部驱动',c='ZKM_PresetTemplateHandDrive().PresetTemplateCreateHandDrive()')
        cmds.button(l='删除驱动（需加载前缀）',c='ZKM_PresetTemplateHandDrive().PresetTemplateDeleteHandDrive()')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        # 翅膀驱动
        child3 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.rowColumnLayout(nc=2, adj=7)
        PictureFormLayout1 = cmds.formLayout()
        cmds.picture(
            i=(self.file_pathReversion + "/Py_PresetTemplate_Material/PresetTemplate_PictureMaterial/翅膀驱动BGC.png"))
        PictureFormLayoutWingHandButton = cmds.button(l='手臂驱动', bgc=(1, 1, 1))
        PictureFormLayoutWingMarginButton = cmds.button(l='翼缘覆羽驱动', bgc=(1, 1, 1))
        PictureFormLayoutWingThumbButton = cmds.button(l='大拇指', bgc=(1, 1, 1))
        PictureFormLayoutWingPrimaryButton = cmds.button(l='初级飞羽驱动', bgc=(1, 1, 1))
        PictureFormLayoutWingSecondaryButton = cmds.button(l='次级飞羽驱动', bgc=(1, 1, 1))
        PictureFormLayoutWingThreeButton = cmds.button(l='三级飞羽驱动', bgc=(1, 1, 1))
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
        cmds.button(l='肩部样条:')
        cmds.textFieldButtonGrp('WingDriveShoulderCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveShoulderCurve\')')
        cmds.button(l='手肘样条:')
        cmds.textFieldButtonGrp('WingDriveElbowCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveElbowCurve\')')
        cmds.button(l='手腕样条:')
        cmds.textFieldButtonGrp('WingDriveWristCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveWristCurve\')')
        cmds.button(l='大拇指样条:')
        cmds.textFieldButtonGrp('WingDriveThumbCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveThumbCurve\')')
        cmds.setParent('..')
        cmds.text(l='各个部分朝向样条顺序保持一致')
        cmds.rowColumnLayout(nc=2, adj=6)
        cmds.button(l='初级飞羽样条:')
        cmds.textFieldButtonGrp('WingDrivePrimaryFlyingFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDrivePrimaryFlyingFeatherCurve\')')
        cmds.button(l='次级飞羽样条:')
        cmds.textFieldButtonGrp('WingDriveSecondaryFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveSecondaryFeatherCurve\')')
        cmds.button(l='三级飞羽样条:')
        cmds.textFieldButtonGrp('WingDriveLevelThreeFlyingFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveLevelThreeFlyingFeatherCurve\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=1, adj=5)
        pm.intSliderGrp('KZQDX', l='翼缘覆羽驱动单边骨骼数', min=1, max=10, v=6, f=1, cc="KZQDX", cw3=(120, 20, 100))
        cmds.text(l='控制器对应的末端骨骼保持顺序一致')
        cmds.textFieldButtonGrp(cw3=(0, 200, 0), l='', text='', bl='加载样条')
        cmds.rowColumnLayout(nc=2, adj=1)
        cmds.button(l='将控制器关联到样条')
        cmds.button(l='将末端骨骼关联到样条')
        cmds.button(l='选择样条对应的控制器')
        cmds.button(l='选择样条对应的末端骨骼')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=3)

        pm.text(l='羽毛朝向：')
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
        pm.text(l='Spread朝向：')
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
        cmds.textFieldButtonGrp(cw3=(0, 200, 50), l='', text='', bl='加载前缀')
        cmds.rowColumnLayout(nc=2, adj=2)
        cmds.button(l='生成翅膀驱动')
        cmds.button(l='删除翅膀（需加载前缀）')
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

        cmds.tabLayout(tabs, edit=True, tabLabel=[(child1, '表情驱动'), (child2, '手部驱动'), (child3, '翅膀驱动'), (child4, '轮胎自动'), (child5, '履带自动'), (child6, '裙子驱动'), (child7, '眼镜嘴巴生成')])

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







