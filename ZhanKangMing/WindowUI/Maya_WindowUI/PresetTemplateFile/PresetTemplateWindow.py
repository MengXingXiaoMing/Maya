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
#reload(PresetTemplate)


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
        cmds.button(l='肩部、手肘、手腕骨骼:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveShoulderElbowWristJoint\')')
        cmds.textFieldButtonGrp('WingDriveShoulderElbowWristJoint', cw3=(0, 130, 0), l='', text='', bl='加载骨骼',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveShoulderElbowWristJoint\')')
        cmds.setParent('..')
        cmds.text(l='各个部分朝向样条顺序保持一致')
        cmds.rowColumnLayout(nc=2, adj=6)
        cmds.button(l='初级飞羽样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDrivePrimaryFlyingFeatherCurve\')')
        cmds.textFieldButtonGrp('WingDrivePrimaryFlyingFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDrivePrimaryFlyingFeatherCurve\')')

        cmds.button(l='次级飞羽样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveSecondaryFeatherCurve\')')
        cmds.textFieldButtonGrp('WingDriveSecondaryFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveSecondaryFeatherCurve\')')

        cmds.button(l='三级飞羽样条:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveLevelThreeFlyingFeatherCurve\')')
        cmds.textFieldButtonGrp('WingDriveLevelThreeFlyingFeatherCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveLevelThreeFlyingFeatherCurve\')')
        cmds.button(l='总控初级飞羽占用范围点:',
                    c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveGeneralControlPrimaryFlyingFeatherPoint\')')
        cmds.textFieldButtonGrp('WingDriveGeneralControlPrimaryFlyingFeatherPoint', cw3=(0, 130, 0), l='', text='',
                                bl='加载样条',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveGeneralControlPrimaryFlyingFeatherPoint\')')
        cmds.button(l='总控次级飞羽占用范围点:',
                    c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveGeneralControlSecondaryFeatherPoint\')')
        cmds.textFieldButtonGrp('WingDriveGeneralControlSecondaryFeatherPoint', cw3=(0, 130, 0), l='', text='',
                                bl='加载样条',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveGeneralControlSecondaryFeatherPoint\')')
        cmds.button(l='总控三级飞羽占用范围点:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveGeneralControlLevelThreeFlyingFeatherPoint\')')
        cmds.textFieldButtonGrp('WingDriveGeneralControlLevelThreeFlyingFeatherPoint', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveGeneralControlLevelThreeFlyingFeatherPoint\')')
        cmds.button(l='肩部、手肘、手腕控制器:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveShoulderElbowWristCurve\')')
        cmds.textFieldButtonGrp('WingDriveShoulderElbowWristCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveShoulderElbowWristCurve\')')
        cmds.button(l='肩到手腕控制器链:',c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'WingDriveShoulderWristChainCurve\')')
        cmds.textFieldButtonGrp('WingDriveShoulderWristChainCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveShoulderWristChainCurve\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=1, adj=5)
        #pm.intSliderGrp('KZQDX', l='翼缘覆羽驱动单边骨骼数', min=1, max=10, v=6, f=1, cc="KZQDX", cw3=(120, 20, 100))
        cmds.text(l='控制器对应的末端骨骼保持顺序一致')
        cmds.rowColumnLayout(nc=2, adj=1)
        cmds.textFieldButtonGrp('WingDriveAddAttributeCurve', cw3=(0, 130, 0), l='', text='', bl='加载样条',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDriveAddAttributeCurve\')')
        cmds.button(l='选择样条对应的控制器')
        cmds.button(l='将末端骨骼或者控制器关联到样条', c='ZKM_PresetTemplateWingDrive().PresetTemplateWingAddAttributesCurve()')
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
        cmds.textFieldButtonGrp('WingDrivePrefix',cw3=(0, 200, 50), l='', text='', bl='加载前缀',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'WingDrivePrefix\')')
        cmds.rowColumnLayout(nc=2, adj=2)
        cmds.button(l='生成翅膀驱动')
        cmds.button(l='删除翅膀（需加载前缀）(这页要改底层，请勿使用)',bgc=(1,1,1))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        # 车辆绑定
        child4 = cmds.rowColumnLayout(numberOfColumns=2)
        cmds.rowColumnLayout(nc=2, adj=5)
        PictureFormLayout = cmds.formLayout()
        cmds.picture(
            i=(self.file_pathReversion + "/Py_PresetTemplate_Material/PresetTemplate_PictureMaterial/轮胎自转驱动BGC"))
        PictureFormLayoutHandButton = cmds.button(l='手腕骨骼', bgc=(1, 1, 1))
        PictureFormLayoutThumbButton = cmds.button(l='大拇指', bgc=(1, 1, 1))
        PictureFormLayoutIndexFingerButton = cmds.button(l='食指', bgc=(1, 1, 1))
        PictureFormLayoutMiddleFingerButton = cmds.button(l='中指', bgc=(1, 1, 1))
        PictureFormLayoutRingFingerButton = cmds.button(l='无名指', bgc=(1, 1, 1))
        PictureFormLayoutLittleFingerButton = cmds.button(l='小拇指', bgc=(1, 1, 1))
        PictureFormLayoutSulcusBoneButton = cmds.button(l='钩骨', bgc=(1, 1, 1))
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
        cmds.rowColumnLayout(nc=2, adj=6)
        cmds.button(l='手腕骨骼:', c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ArmDriveWristJoint1\')')
        cmds.textFieldButtonGrp('ArmDriveWristJoint1', cw3=(0, 130, 0), l='', text='', bl='加载骨骼',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'ArmDriveWristJoint1\')')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=6)
        pm.text(l='Go：')
        pm.rowColumnLayout(numberOfColumns=6)
        cmds.radioCollection('PresetTemplateHandDriveSpread1')
        cmds.radioButton('PresetTemplateHandDrive_Spread_X', label="X")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fX', label="-X")
        cmds.radioButton('PresetTemplateHandDrive_Spread_Y', label="Y")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fY', label="-Y")
        cmds.radioButton('PresetTemplateHandDrive_Spread_Z', label="Z")
        cmds.radioButton('PresetTemplateHandDrive_Spread_fZ', label="-Z")
        pm.radioCollection('PresetTemplateHandDriveSpread1', edit=1, select="PresetTemplateHandDrive_Spread_Z")
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')


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

        cmds.tabLayout(tabs, edit=True, tabLabel=[(child1, '表情驱动'), (child2, '手部驱动'), (child3, '翅膀驱动'), (child4, '车辆生成'), (child5, '履带自动'), (child6, '裙子驱动'), (child7, '眼镜嘴巴生成')])

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

def PresetTemplateWingCreateWingDrive():
    #添加基础目标约束部分
    WingDrivePrefix = cmds.textFieldButtonGrp('WingDrivePrefix', q=1, text=1)
    ShoulderElbowWrist = cmds.textFieldButtonGrp('WingDriveShoulderElbowWristJoint', q=1, text=1).split(',')
    Shoulder = ShoulderElbowWrist[0]
    Elbow = ShoulderElbowWrist[1]
    Wrist = ShoulderElbowWrist[2]
    AllGeneralJoint = [Wrist,Elbow,Shoulder]
    PrimaryFlyingFeather = cmds.textFieldButtonGrp('WingDrivePrimaryFlyingFeatherCurve', q=1, text=1).split(',')
    SecondaryFeather = cmds.textFieldButtonGrp('WingDriveSecondaryFeatherCurve', q=1, text=1).split(',')
    LevelThreeFlyingFeather = cmds.textFieldButtonGrp('WingDriveLevelThreeFlyingFeatherCurve', q=1, text=1).split(',')
    GeneralControlPrimaryFlyingFeatherPoint = cmds.textFieldButtonGrp('WingDriveGeneralControlPrimaryFlyingFeatherPoint', q=1, text=1).split(',')
    GeneralControlSecondaryFeatherPoint = cmds.textFieldButtonGrp('WingDriveGeneralControlSecondaryFeatherPoint', q=1, text=1).split(',')
    GeneralControlLevelThreeFlyingFeatherPoint = cmds.textFieldButtonGrp('WingDriveGeneralControlLevelThreeFlyingFeatherPoint', q=1, text=1).split(',')
    GeneralControl = []
    if GeneralControlPrimaryFlyingFeatherPoint:
        GeneralControl = GeneralControlPrimaryFlyingFeatherPoint[0].split('.')
        GeneralControl = pm.listRelatives(GeneralControl[0],p=1)
    if GeneralControlSecondaryFeatherPoint:
        GeneralControl = GeneralControlSecondaryFeatherPoint[0].split('.')
        GeneralControl = pm.listRelatives(GeneralControl[0], p=1)
    if GeneralControlLevelThreeFlyingFeatherPoint:
        GeneralControl = GeneralControlLevelThreeFlyingFeatherPoint[0].split('.')
        GeneralControl = pm.listRelatives(GeneralControl[0], p=1)
    ShoulderWristChain = cmds.textFieldButtonGrp('WingDriveShoulderWristChainCurve', q=1, text=1).split(',')
    AllSecondaryCurve = [PrimaryFlyingFeather,SecondaryFeather,LevelThreeFlyingFeather]
    if Shoulder and Elbow and Wrist:
        AllFeatherControlGrp = []
        j=0
        for Lis in [PrimaryFlyingFeather,SecondaryFeather,LevelThreeFlyingFeather]:
            for C in Lis:
                if pm.objExists(C + '.Joint') and pm.objExists(C + '.Curve'):
                    AllName = pm.attributeQuery('Joint', node=C, listEnum=1)
                    AllJoint = AllName[0].split(':')
                    AllName = pm.attributeQuery('Curve', node=C, listEnum=1)
                    AllCurve = AllName[0].split(':')
                    for i in range(0,len(AllJoint)):
                        #创建对应位置的定位器在曲线上
                        Place = cmds.xform(AllJoint[i], query=True, worldSpace = 1, translation=True)
                        nearestPointOnCurve = pm.createNode("nearestPointOnCurve")
                        shapes = cmds.listRelatives(C)[0]
                        pm.connectAttr((shapes + '.worldSpace[0]'), (nearestPointOnCurve + '.inputCurve'), f=1)
                        pm.setAttr((nearestPointOnCurve+'.inPositionX'), Place[0])
                        pm.setAttr((nearestPointOnCurve+'.inPositionY'), Place[1])
                        pm.setAttr((nearestPointOnCurve+'.inPositionZ'), Place[2])
                        U = pm.getAttr((nearestPointOnCurve + '.parameter'))
                        pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'))
                        pm.setAttr(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc.v',0)
                        pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.2, tol=0.01, nr=(1, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_Curve'))
                        pm.parent((WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'),(WingDrivePrefix + C + AllJoint[i] + '_Curve'))
                        #pm.parentConstraint((C + AllJoint[i] + '_CurveLoc'), (C + AllJoint[i] + '_Curve'))
                        pm.select((WingDrivePrefix + C + AllJoint[i] + '_Curve'))
                        pm.group(n=(WingDrivePrefix + C + AllJoint[i] + '_Grp2'))
                        pm.group(n=(WingDrivePrefix + C + AllJoint[i] + '_Grp1'))
                        Loc = pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C + AllJoint[i] + '_Loc'))
                        pm.setAttr((WingDrivePrefix + C + AllJoint[i] + '_Loc.v'), 0)
                        pm.parentConstraint((WingDrivePrefix + C + AllJoint[i] + '_Loc'),(WingDrivePrefix + C + AllJoint[i] + '_Grp1'),weight=1)
                        motionPath = pm.pathAnimation(Loc,C,upAxis='y', fractionMode=True,
                                                      endTimeU=pm.playbackOptions(query=1, maxTime=1),
                                                      startTimeU=pm.playbackOptions(minTime=1, query=1),
                                                      worldUpObject=AllGeneralJoint[j], worldUpType="objectrotation", inverseUp=False,
                                                      inverseFront=False, follow=True, bank=False, followAxis='x',
                                                      worldUpVector=(0, 1, 0))
                        pm.disconnectAttr((motionPath + "_uValue.output"), (motionPath + ".uValue"))
                        pm.setAttr((motionPath + ".uValue"),U)
                        Parent=pm.listRelatives(AllCurve[i],p=1)
                        pm.select(Parent)
                        pm.rename(pm.mel.doGroup(0, 1, 1),(WingDrivePrefix + C + AllCurve[i] + '_WingAimGrp'))
                        pm.aimConstraint((WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'), (WingDrivePrefix + C + AllCurve[i] + '_WingAimGrp'), weight=1,
                                         upVector=(0, 1, 0), mo=1, worldUpObject=(WingDrivePrefix + C + AllJoint[i] + '_CurveLoc'), worldUpType="objectrotation",
                                         aimVector=(1, 0, 0), worldUpVector=(-1, 0, 0))
                        pm.select(Loc,(WingDrivePrefix + C + AllJoint[i] + '_Grp1'))
                        pm.group(n=(WingDrivePrefix + C + AllJoint[i] + '_Grp'))
                        pm.delete(nearestPointOnCurve)
                    pm.select(cl=1)
                    for i in range(0, len(AllJoint)):
                        pm.select((WingDrivePrefix + C + AllJoint[i] + '_Grp'),add=1)
                    pm.group(n=(WingDrivePrefix + C + 'AllController_Grp'))
                    AllFeatherControlGrp.append((WingDrivePrefix + C + 'AllController_Grp'))
                # 给所有样条点加蔟，约束到最近的总控制曲线上
                shapes = cmds.listRelatives(C)[0]
                pm.select(cl=1)
                pm.select(shapes + '.cv[0:]')
                AllCurvePoint = pm.ls(sl=1,fl=1)
                pm.select(cl=1)
                pm.group(n=(WingDrivePrefix + C + '_WingAllClusterGroup'))
                ClusterGrp = pm.ls(sl=1)
                pm.setAttr((ClusterGrp[0] + ".inheritsTransform"), 0)
                pm.parent(ClusterGrp[0],(WingDrivePrefix + C + 'AllController_Grp'))
                for i in range(0,len(AllCurvePoint)):
                    pm.select(AllCurvePoint[i])
                    pm.mel.newCluster(" -envelope 1")
                    Cluster = pm.ls(sl=1)
                    pm.rename(Cluster,(WingDrivePrefix + C+'_point'+str(i)+'Cluster'))
                    Cluster = pm.ls(sl=1)
                    pm.spaceLocator(p=(0, 0, 0))
                    LSloc = pm.ls(sl=1)
                    pm.delete(pm.pointConstraint(Cluster[0],LSloc))
                    pm.parent(Cluster[0],ClusterGrp[0])
                    Place = pm.xform(str(LSloc[0]), query=True, worldSpace=1, translation=True)
                    nearestPointOnCurve = pm.createNode("nearestPointOnCurve")
                    shapes = pm.listRelatives(GeneralControl)[0]
                    pm.connectAttr((shapes + '.worldSpace[0]'), (nearestPointOnCurve + '.inputCurve'), f=1)
                    pm.setAttr((nearestPointOnCurve + '.inPositionX'), Place[0])
                    pm.setAttr((nearestPointOnCurve + '.inPositionY'), Place[1])
                    pm.setAttr((nearestPointOnCurve + '.inPositionZ'), Place[2])
                    U = pm.getAttr((nearestPointOnCurve + '.parameter'))
                    pm.spaceLocator(p=(0, 0, 0), n=(WingDrivePrefix + C+'_point'+str(i)+'ClusterLoc'))
                    Loc = pm.ls(sl=1)
                    pm.parent(Loc, ClusterGrp[0])
                    motionPath = pm.pathAnimation(Loc, GeneralControl, upAxis='y',
                                                  fractionMode=True,
                                                  endTimeU=pm.playbackOptions(query=1, maxTime=1),
                                                  startTimeU=pm.playbackOptions(minTime=1, query=1),
                                                  worldUpObject=AllGeneralJoint[j], worldUpType="objectrotation",
                                                  inverseUp=False,
                                                  inverseFront=False, follow=True, bank=False, followAxis='x',
                                                  worldUpVector=(0, 1, 0))
                    pm.disconnectAttr((motionPath + "_uValue.output"), (motionPath + ".uValue"))
                    pm.setAttr((motionPath + ".uValue"), U)

                    pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.4, tol=0.01, nr=(1, 0, 0),n=(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve'))
                    pm.group(n=(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp2'))
                    pm.group(n=(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp1'))
                    pm.delete(pm.parentConstraint(Cluster,(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve')))
                    pm.parent(Cluster,(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve'))
                    pm.parent((WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp1'), ClusterGrp[0])
                    pm.parentConstraint((WingDrivePrefix + C+'_point'+str(i)+'ClusterLoc'),(WingDrivePrefix + C + '_point' + str(i) + 'ClusterCurve_Grp1'),mo=1,weight=1)
                    pm.setAttr((WingDrivePrefix + C+'_point'+str(i)+'ClusterLoc.visibility'),0)
                    pm.setAttr((WingDrivePrefix + C+'_point'+str(i)+'Cluster.visibility'), 0)
                    pm.delete(LSloc)
                pm.parent(C,(WingDrivePrefix + C + '_WingAllClusterGroup'))

            j = j + 1
        pm.select(cl=1)
        pm.group(n=(WingDrivePrefix + 'WingAllFeatherControlGroup'))
        for P in AllFeatherControlGrp:
            pm.parent(P, (WingDrivePrefix + 'WingAllFeatherControlGroup'))
        # 给总控制样条所有点加蔟，生成总控制器
        pm.select(GeneralControl, (WingDrivePrefix + 'WingAllFeatherControlGroup'))
        pm.group(n=(WingDrivePrefix + 'WingMainGrp'))
        # 给总控制器所有点加控制器
        k = -1
        for Lis in [GeneralControlPrimaryFlyingFeatherPoint,GeneralControlSecondaryFeatherPoint,GeneralControlLevelThreeFlyingFeatherPoint]:
            for Point in Lis:
                PointNum = Point.split('[')[1][:-1]
                pm.select(Point)
                pm.mel.newCluster(" -envelope 1")
                Cluster = pm.ls(sl=1)
                pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.5, tol=0.01, nr=(1, 0, 0),n=(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Curve'))
                pm.group(n=(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp2'))
                pm.group(n=(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1'))
                pm.delete(pm.parentConstraint(Cluster[0],(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1')))
                pm.parent(Cluster[0],(WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Curve'))
                pm.parentConstraint(ShoulderElbowWrist[k], (WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1'),mo=1)
                pm.parent((WingDrivePrefix + GeneralControl[0] + 'Point' + PointNum + '_Grp1'),(WingDrivePrefix + 'WingMainGrp'))
                pm.setAttr((Cluster[0]+'.visibility'),0)
            k = k - 1
        #添加驱动属性样条
        #建立两条ik链，在手肘位置添加三个蔟，用来控制弯曲幅度和位置，且把属性给到驱动控制器（只修改羽毛部分，因为ADV自带调整）
        #肩部控制器旋转90度，

    else:
        pm.error('请加载肩部、手肘、手腕控制器')

                #将基础目标部分提取成总控制部分


def LTZZQDCK_kssc():
    FFK_C = str(pm.textFieldButtonGrp('LTZZQDCK_JZLTYTFKZQ', q=1, text=1))
    FK_C = str(pm.textFieldButtonGrp('LTZZQDCK_JZLTYTFKKZQ', q=1, text=1))
    QXCD = str(pm.textFieldButtonGrp('LTZZQDCK_JZLTZCQX', q=1, text=1))
    qianzhui = str(pm.textFieldButtonGrp('LTZZQDCK_JZQZ', q=1, text=1))
    if len(FFK_C) < 1:
        pm.select("", r=1)

    if len(FK_C) < 1:
        pm.select("", r=1)

    if len(qianzhui) < 1:
        pm.select("", r=1)

    Luntai_ZouXiang = str(pm.radioCollection('LTZZQDCK_Luntai', q=1, select=1))
    if Luntai_ZouXiang == "LTZZQDCK_Luntai_X":
        Luntai_ZouXiang = "X"

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_fX":
        Luntai_ZouXiang = "X"
        pm.setAttr("qianzhui_LunTai_C.BeiLv", -1)

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_Y":
        Luntai_ZouXiang = "Y"

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_fY":
        Luntai_ZouXiang = "Y"
        pm.setAttr("qianzhui_LunTai_C.BeiLv", -1)

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_Z":
        Luntai_ZouXiang = "Z"

    if Luntai_ZouXiang == "LTZZQDCK_Luntai_fZ":
        Luntai_ZouXiang = "Z"
        pm.setAttr("qianzhui_LunTai_C.BeiLv", -1)

    pm.melGlobals.initVar('string', 'scriptLocationYvZhiWindow')
    pm.mel.performFileSilentImportAction((pm.melGlobals['scriptLocationYvZhiWindow'] + "/CarLunTaiMB.mb"))
    pm.shadingNode('curveInfo', asUtility=1)
    qxxxjd = pm.ls(sl=1)
    pm.connectAttr((QXCD + ".worldSpace[0]"), (qxxxjd[0] + ".inputCurve"),
                   f=1)
    qxcd = float(pm.getAttr(qxxxjd[0] + ".arcLength"))
    pm.select(FK_C, r=1)
    pm.pickWalk(d='up')
    pm.mel.doGroup(0, 1, 1)
    pm.rename(qianzhui + "_LunTai_lianjie")
    pm.mel.doGroup(0, 1, 1)
    pm.rename(qianzhui + "_LunTai_yveshu")
    pm.parent("qianzhui_LunTai_grp", FK_C)
    pm.setAttr("qianzhui_LunTai_grp.rotateZ", 0)
    pm.setAttr("qianzhui_LunTai_grp.translateX", 0)
    pm.setAttr("qianzhui_LunTai_grp.translateY", 0)
    pm.setAttr("qianzhui_LunTai_grp.translateZ", 0)
    pm.setAttr("qianzhui_LunTai_grp.rotateX", 0)
    pm.setAttr("qianzhui_LunTai_grp.rotateY", 0)
    pm.parent("qianzhui_LunTai_grp", "qianzhui_LunTai_Grp")
    pm.connectAttr("qianzhui_Joint.rotateX",
                   (qianzhui + "_LunTai_lianjie" + ".rotate" + Luntai_ZouXiang),
                   f=1)
    pm.parentConstraint('qianzhui_LunTai_C', (qianzhui + "_LunTai_yveshu"),
                        mo=1, weight=1)
    pm.scaleConstraint('qianzhui_LunTai_C', (qianzhui + "_LunTai_yveshu"),
                       weight=1, offset=(1, 1, 1))
    pm.parentConstraint(FFK_C, "qianzhui_LunTai", mo=1, weight=1)
    pm.scaleConstraint(FFK_C, "qianzhui_LunTai", weight=1, offset=(1, 1, 1))
    pm.select('qianzhui_LunTai_Grp', r=1)
    pm.mel.searchReplaceNames("qianzhui", qianzhui, "hierarchy")



