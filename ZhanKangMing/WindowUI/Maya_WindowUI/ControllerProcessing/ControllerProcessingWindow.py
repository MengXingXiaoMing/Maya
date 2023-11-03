#coding=gbk
import maya.OpenMaya as OpenMaya
import pymel.core as pm
import random
import os
import sys
import inspect
import maya.cmds as cmds

#根目录
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
# UI拖动
from SliderEdit import *
# 加载文本
from LoadText import *
# 自动调整UI
from AutomaticModificationUIRange import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaCurve')
# 加载曲线编辑
from CreateAndEditCurve import *
# 毛囊约束
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaCommon')
from Follicle import *
from FileProcessing import *
# 独立功能
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaOthersLibrary')
from IndependentSmallFunctions import *
# 加载对应后缀文件
sys.path.append(ZKM_RootDirectory+'\\Common\\CommonLibrary')
from LoadCorrespondingSuffixFile import *
# 属性可视化
sys.path.append(File_RootDirectory + '\\ControllerProcessingWindowPictureMaterials')
from AttributeVisualizationWindow import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaController')
# 加载曲线编辑
from CurveControllerEdit import *


'''
from CurveControllerEdit import *
import CurveControllerEdit
reload(CurveControllerEdit)
from CreateAndEditCurve import *
import CreateAndEditCurve
reload(CreateAndEditCurve)
from IndependentSmallFunctions import *
import IndependentSmallFunctions
reload(IndependentSmallFunctions)
'''

class ZKM_ControllerPresetTemplateWindowClass:
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        # print(file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
        cur_dirB = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathTop = os.path.join(cur_dirB)  # 获取总位置
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
        self.file_pathTop = file_pathTop
    def ZKM_Window(self):
        if pm.window('WindowControllerProcessing', ex=1):
            pm.deleteUI('WindowControllerProcessing')
        pm.window('WindowControllerProcessing', s=1, t="控制器处理")
        pm.rowColumnLayout(nc=2)
        pm.formLayout("WindowControllerProcessingFrom",w=303,h=820)
        pm.rowColumnLayout("WindowControllerProcessingWindow", nc=1, adj=8)
        pm.rowColumnLayout(nc=2, adj=2)
        pm.floatSliderGrp('WindowControllerProcessingControllerSizeFloatSliderGrp', fmx=9999999, min=0.1,
                          cc='ZKM_ControllerPresetTemplateCommand().ScaleController()', max=2, cw3=(55, 40, 92),f=1, l="控制器大小", v=1.00)
        pm.button(c='ZKM_CurveControllerEditClass().ZKM_ModifyControllerShapeTRS(\'SoftSelectionSize\', 0, 0, 0)', l="缩放至软选择大小")
        pm.setParent('..')
        pm.rowColumnLayout(cs=[(1, 3), (2, 10), (4, 10)], nc=4, adj=8)
        pm.text(l="轴向")
        pm.rowColumnLayout(columnWidth=[(1, 40), (2, 40), (3, 40)], numberOfColumns=6)
        pm.radioCollection('WindowControllerProcessingControllerOrientation')
        pm.radioButton('X', label="X")
        pm.radioButton('Y', label="Y")
        pm.radioButton('Z', label="Z")
        pm.radioCollection('WindowControllerProcessingControllerOrientation', edit=1, select="X")
        pm.setParent('..')
        pm.button(c='ZKM_ControllerPresetTemplateCommand().RotationController()', l="旋转")
        pm.button(c='ZKM_ControllerPresetTemplateCommand().detectionOfTheSameNameMain()', bgc=(0, 0.8, 0.8), l="去除重复名称节点")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=8)
        # 控制器形状组
        pm.rowColumnLayout(nc=2, adj=2)
        pm.textFieldButtonGrp('WindowControllerProcessingUploadControllerFile', bl="填写名称上传样条", text="", cw3=(0, 100, 0), l='',
                              bc='ZKM_ControllerPresetTemplateCommand().GenerateRefreshWindow(\''+self.file_pathTop+'/Maya/MayaCommon/CurveShapeWithPicture\')')
        pm.button(l='删除所选样条',c='ZKM_ControllerPresetTemplateCommand().DeleteSelectedCurve(\''+self.file_pathTop+'/Maya/MayaCommon/CurveShapeWithPicture\')')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=1,cw=(1,1))
        AllTxtFile = os.listdir(self.file_pathTop+'\Maya\MayaCommon\CurveShapeWithPicture')  # 返回文件名
        WindowControllerProcessingAllControllerSliderLineMax = (len(AllTxtFile)/5/2*74-400)/10
        if WindowControllerProcessingAllControllerSliderLineMax<=0:
            WindowControllerProcessingAllControllerSliderLineMax=0.01
        pm.floatScrollBar("WindowControllerProcessingAllControllerSliderLine", hr=0, max=WindowControllerProcessingAllControllerSliderLineMax, min=0,
                          cc='ZKM_SliderClass().ZKM_Slider(\'WindowControllerProcessingAllControllerSliderLine\',\'WindowControllerProcessingAllControllerFlowLayout\',\'WindowControllerProcessingAllControllerFormLayout\',-10)')
        pm.formLayout('WindowControllerProcessingAllControllerFormLayout',h=400)
        pm.rowColumnLayout('WindowControllerProcessingAllControllerFlowLayout',nc=5)
        pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection')
        for i in AllTxtFile:
            if os.path.splitext(i)[1] == '.txt':
                Name = os.path.splitext(i)[0]
                pm.rowColumnLayout(nc=1, adj=2)
                pm.iconTextRadioButton(Name,w=55,h=55,i=(self.file_pathTop + '\Maya\MayaCommon\CurveShapeWithPicture' + "\\" + Name + '.jpg'),st="iconOnly",ann=Name)
                pm.text(l=Name)
                pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection',e=1,
                                   sl=pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, cia=1)[0])

        pm.setParent('..')
        # 改控制器和颜色
        pm.button(c='ZKM_ControllerPresetTemplateCommand().asSwapCurve()', l="改控制器")
        pm.rowColumnLayout(nc=4, adj=4)
        pm.optionMenu('WindowControllerProcessingChangeCurveColor_OptionMenu')
        pm.menuItem(label="Index")
        pm.menuItem(label="RGB")
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',rgb=(0.127, 0.715, 1.000),cw2=(25,0))
        pm.intSlider('WindowControllerProcessingChangeCurveColor_intSlider',max=31, step=1, value=18, min=0,w=145,cc='ZKM_ControllerPresetTemplateCommand().DragSliderAutomaticallyModifyColorPanel()')
        pm.button(c='ZKM_ControllerPresetTemplateCommand().ChangeCurveColor()', l="改颜色")
        pm.setParent('..')
        pm.intSliderGrp('WindowControllerProcessingNumberControllerGroups', min=1, max=10, cw3=(60, 40, 170), f=1, l="控制器组数:", cc='ZKM_AutomaticModificationUIRangeClass().ZKM_IntSlider_Max_Edit_Controller(\'WindowControllerProcessingNumberControllerGroups\')',v=2)
        # 填写后缀和处理骨骼
        pm.rowColumnLayout(nc=3, adj=8)
        pm.textFieldGrp('WindowControllerProcessingSuffix', text="", cw2=(25, 130), l="后缀")
        pm.rowColumnLayout(columnWidth=[(1, 27), (2, 27), (3, 27)], numberOfColumns=5)
        pm.radioCollection('WindowControllerProcessingJointMirror')
        pm.radioButton('X', label="X")
        pm.radioButton('Y', label="Y")
        pm.radioButton('Z', label="Z")
        pm.radioCollection('WindowControllerProcessingJointMirror', edit=1, select="X")
        pm.setParent('..')
        pm.button(c='ZKM_IndependentSmallfunctions().MirrorJoint(str(pm.radioCollection(\'WindowControllerProcessingJointMirror\', q=1, select=1)))', l="镜像骨骼")
        pm.setParent('..')
        # 清理后开始生成
        pm.rowColumnLayout(nc=2, adj=8)
        pm.intSliderGrp('WindowControllerProcessingJointNum', fmx=9999999, min=1, cc='ZKM_AutomaticModificationUIRangeClass().ZKM_IntSlider_Max_Edit_Controller(\'WindowControllerProcessingJointNum\')', max=100,
                        cw3=(0, 40, 150), f=1, l="", v=50)
        pm.button(c='ZKM_IndependentSmallfunctions().GenerateBoneChain(pm.intSliderGrp(\'WindowControllerProcessingJointNum\', q=1, v=1))', l="选择样条创建骨骼")
        pm.setParent('..')
        pm.rowColumnLayout(cs=(2, 5), nc=4, adj=3)
        pm.checkBox('WindowControllerProcessingIgnoreEndBones_checkBox',w=85, value=1, label="忽略末端骨骼")
        pm.checkBox('WindowControllerProcessingExtractConstraints', value=1, label="提取约束")
        pm.button(c='ZKM_CurveControllerEditClass().ZKM_ChuangJianFKPreconditions()',bgc=(1,0,0), l="创基础")
        pm.button(c='ZKM_ControllerPresetTemplateCommand().OldChuangJianFK()', bgc=(0.4, 0, 0), l="独立创建控制器")
        pm.setParent('..')
        pm.rowColumnLayout(cs=(2, 5), nc=3, adj=1)
        pm.optionMenu('WindowControllerProcessingImportFile')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\ControllerProcessingWindowModel'), 0, '.mb')):
            pm.menuItem(label=file)
        pm.button(c='ZKM_ControllerPresetTemplateCommand().ImportFile()', l="导入", bgc=(1, 1, 1))
        pm.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(r\''+self.file_path + '\ControllerProcessingWindowModel'+'\')')
        pm.setParent('..')
        pm.rowColumnLayout(cs=(2, 5), nc=4, adj=1)
        pm.optionMenu('WindowControllerProcessingCreateModel', w=90,cc='ZKM_ControllerPresetTemplateCommand().ModifyAccessoryUI()')
        pm.menuItem(label="hand")
        pm.menuItem(label="foot")
        pm.button(c='ZKM_ControllerPresetTemplateCommand().CreateModel()', l="创建", bgc=(1, 1, 1))
        pm.rowColumnLayout('WindowControllerProcessingCreateModel_rowColumnLayout',adj=1, nc=1)
        pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', w=115)
        ZKM_ControllerPresetTemplateCommand().ModifyAccessoryUI()
        pm.setParent('..')
        pm.button(c='ZKM_ControllerPresetTemplateCommand().AddAttribute(\'WindowControllerProcessingCreateModel_Attribute\')', l="删/增属性", bgc=(1, 1, 1))
        pm.setParent('..')
        pm.rowColumnLayout(cs=(2, 5), nc=2, adj=1)
        pm.floatSliderGrp('WindowControllerProcessingControllerJointSize', fmx=9999999, min=0.1, max=2, cw3=(45, 40, 92), f=1,l="骨骼大小", v=1.00,cc='ZKM_ControllerPresetTemplateCommand().JointScale()')
        pm.button('ShowHideJoint_Button',c='ZKM_ControllerPresetTemplateCommand().ShowHideJoint()', l="隐藏所有骨骼", bgc=(1, 1, 1))
        pm.setParent('..')
        pm.rowColumnLayout(cs=(2, 5), nc=4, adj=4)
        pm.rowColumnLayout(cs=(2, 5), nc=2, adj=1,w=152)
        pm.optionMenu('WindowControllerProcessingAddAttributeOptionMenu')
        pm.menuItem(label="IK")
        pm.menuItem(label="SplineIK")
        pm.menuItem(label="AIM")
        pm.menuItem(label="Wheel")
        pm.menuItem(label="NotGenerate")
        pm.menuItem(label="Global")


        pm.button(c='ZKM_ControllerPresetTemplateCommand().AddAttribute(\'WindowControllerProcessingAddAttributeOptionMenu\')', l="A/D属性", bgc=(1, 1, 1))
        pm.setParent('..')
        pm.button(c='ZKM_CurveControllerEditClass().ZKM_ChuangJianFKSwitch(pm.checkBox(\'WindowControllerProcessingExtractConstraints\', q=1,value=1))',bgc=(1, 1, 0), l="切换")
        pm.button(c='ZKM_CurveControllerEditClass().ZKM_ControllerHoming()', bgc=(0, 1, 0), l="归位")
        pm.button('CHUANGJIANFK', c='ZKM_ControllerPresetTemplateCommand().ChuangJianFK()', bgc=(1, 1, 1), l="创建控制器")
        pm.setParent('..')
        pm.setParent('..')
        pm.flowLayout(wrap=1,columnSpacing=3,h=500)
        pm.button(c='ZKM_IndependentSmallfunctions().CentreJoint()', l="在所选线中心创建骨骼")
        pm.button(c='print (ZKM_CreateAndEditCurveClass().ZKM_ReturnCurveCommand(pm.ls(sl=1)))', l="获取样条点数值")
        pm.button(c='ZKM_IndependentSmallfunctions().ShowAxial()', l="显隐轴向")
        pm.button(c='ZKM_IndependentSmallfunctions().JointTransformationCurve()', l="骨骼转样条")
        pm.button(c='ZKM_IndependentSmallfunctions().CreateCentreJoint()', l="在中线建立骨骼链")
        pm.button(c='ZKM_IndependentSmallfunctions().ReversalArrangement()', l="反转骨骼层次（单链）")
        pm.rowColumnLayout( adj=8, nc=3)
        pm.intSliderGrp('WindowControllerProcessingInterval', fmx=9999999, min=1, cc='ZKM_AutomaticModificationUIRangeClass().ZKM_IntSlider_Max_Edit_Controller(\'WindowControllerProcessingInterval\')', max=10,cw3=(0, 40, 100), f=1, l="", v=2)
        pm.button(c='ZKM_IndependentSmallfunctions().InterlacedLineSelection("edgeRing",pm.intSliderGrp(\'WindowControllerProcessingInterval\', q=1, v=1))', l="隔行选线")
        pm.button(c='ZKM_IndependentSmallfunctions().InterlacedLineSelection("edgeLoop",pm.intSliderGrp(\'WindowControllerProcessingInterval\', q=1, v=1))', l="隔行选循环边")
        pm.setParent('..')

        pm.rowColumnLayout(nc=2, adj=2, w=300)
        pm.intSliderGrp('WindowControllerProcessingInsertBone', fmx=9999999, min=1, cc='ZKM_AutomaticModificationUIRangeClass().ZKM_IntSlider_Max_Edit_Controller(\'WindowControllerProcessingInsertBone\')', max=10, cw3=(0, 40, 140),f=1, l="插入数量", v=5)
        pm.button(c='ZKM_IndependentSmallfunctions().InsertJoint()', l="插入骨骼")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=2, w=290)
        pm.textFieldButtonGrp('WindowControllerProcessing_HairFollicleConstraint_MD', bl="加载", text="", cw3=(50, 205, 0), l=("加载模型"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'WindowControllerProcessing_HairFollicleConstraint_MD\')')
        pm.rowColumnLayout(columnWidth=(1, 125), numberOfColumns=2)
        pm.checkBox('HairFollicleConstraint_KeepPlace_checkBox', value=1, label="保持原位(父对象约束)")
        pm.button(c='ZKM_ControllerPresetTemplateCommand().HairFollicleAdsorption()', l="毛囊附着(选择需要跟随的物体)")
        pm.setParent('..')
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=3, w=300)
        pm.textFieldButtonGrp('WindowControllerProcessing_LoadSourceProperties', bl="加载", text="", cw3=(60, 195, 0), l=("加载源属性:"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'WindowControllerProcessing_LoadSourceProperties\')')
        pm.textFieldButtonGrp('WindowControllerProcessing_LoadTargetProperties', bl="加载", text="", cw3=(70, 185, 0), l=("加载目标属性:"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'WindowControllerProcessing_LoadTargetProperties\')')
        pm.rowColumnLayout(numberOfColumns=3)
        pm.textFieldGrp('LJBL', text="1", cw2=(25, 45), l=("倍率"))
        pm.button(c='ZKM_ControllerPresetTemplateCommand().LinkProperty()', l="链接")
        pm.button(c='ZKM_AttributeVisualizationClass().AttributeVisualizationWindow()', bgc=(1, 1, 0), l="打开属性可视化窗口(生成忽略警告)")
        pm.setParent('..')
        pm.rowColumnLayout( nc=2, adj=2,cw=(1,140))
        pm.button(c='ZKM_IndependentSmallfunctions().gtMoveUpDnAttrsProc(1)', l="上移属性")
        pm.button(c='ZKM_IndependentSmallfunctions().HideSelectionProperties()', l="隐藏选择属性")
        pm.button(c='ZKM_IndependentSmallfunctions().gtMoveUpDnAttrsProc(0)', l="下移属性")
        pm.button(c='ZKM_IndependentSmallfunctions().ShowDefaultProperties()', l="显示默认属性")
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.floatScrollBar("WindowControllerProcessingWindowSliderLine", hr=0, max=28,
                          cc='ZKM_SliderClass().ZKM_Slider(\'WindowControllerProcessingWindowSliderLine\',\'WindowControllerProcessingWindow\',\'WindowControllerProcessingFrom\',-30)', min=0)
        pm.showWindow()
class ZKM_ControllerPresetTemplateCommand:
    # 生成控制器并刷新窗口
    def GenerateRefreshWindow(self,File):
        Name = pm.textFieldButtonGrp('WindowControllerProcessingUploadControllerFile', q=1, text=1)
        if Name:
            pm.melGlobals.initVar('string', 'gMainWindow')
            WH = pm.window(pm.melGlobals['gMainWindow'], q=1, widthHeight=1)
            pm.window(pm.melGlobals['gMainWindow'], edit=1, widthHeight=(1100, 1100))
            ZKM_CreateAndEditCurveClass().ZKM_UploadFileByName(Name,File)
            ShowWindow.ZKM_Window()
            pm.window(pm.melGlobals['gMainWindow'], edit=1, widthHeight=(WH[0], WH[1]))
        else:
            pm.error('请填写样条名称')
    # 删除所选样条
    def DeleteSelectedCurve(self,File):
        Name = pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, sl=1)
        os.remove(File + '/' + Name + '.txt')
        os.remove(File + '/' + Name + '.jpg')
        ShowWindow.ZKM_Window()
    # 选中改颜色
    def ChangeCurveColor(self):
        Sel = pm.ls(sl=1)
        Type = pm.optionMenu('WindowControllerProcessingChangeCurveColor_OptionMenu',q=1,v=1)
        Color = pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',q=1,rgb=1)
        Num = pm.intSlider('WindowControllerProcessingChangeCurveColor_intSlider',q=1,value=1)
        ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(str(Type),Sel,Color,Num)

    # 拖动滑块自动修改颜色面板
    def DragSliderAutomaticallyModifyColorPanel(self):
        value = pm.intSlider('WindowControllerProcessingChangeCurveColor_intSlider', q=1, value=1)
        if value ==0:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.188,0.188,0.188))
        if value ==1:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.000,0.000))
        if value ==2:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.051,0.051,0.051))
        if value ==3:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.319,0.319,0.319))
        if value ==4:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.328,0.000,0.021))
        if value ==5:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.001,0.117))
        if value ==6:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.000,1.000))
        if value ==7:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.061,0.010))
        if value ==8:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.019,0.000,0.056))
        if value ==9:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.577,0.000,0.577))
        if value ==10:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.254,0.065,0.033))
        if value ==11:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.050,0.017,0.014))
        if value ==12:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.319,0.019,0.000))
        if value ==13:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,0.000,0.000))
        if value ==14:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,1.000,0.000))
        if value ==15:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.053,0.319))
        if value ==16:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,1.000,1.000))
        if value ==17:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,1.000,0.000))
        if value ==18:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.127,0.716,1.000))
        if value ==19:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.056,1.000,0.366))
        if value ==20:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,0.434,0.434))
        if value ==21:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.776,0.413,0.191))
        if value ==22:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,1.000,0.125))
        if value ==23:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.319,0.089))
        if value ==24:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.356,0.144,0.030))
        if value ==25:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.342,0.356,0.030))
        if value ==26:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.138,0.356,0.030))
        if value ==27:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.030,0.356,0.109))
        if value ==28:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.030,0.356,0.356))
        if value ==29:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.030,0.136,0.356))
        if value ==30:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.159,0.030,0.356))
        if value ==31:
            pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.356,0.030,0.144))

    # 改控制器
    def asSwapCurve(self):
        Name = pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, sl=1)
        Type = pm.optionMenu('WindowControllerProcessingChangeCurveColor_OptionMenu', q=1, v=1)
        print 'Type'
        Color = pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp', q=1, rgb=1)
        Num = pm.intSlider('WindowControllerProcessingChangeCurveColor_intSlider', q=1, value=1)
        ZKM_CurveControllerEditClass().ZKM_asSwapCurve(str(Type),Name, Color,Num)

    # 缩放控制器
    def ScaleController(self):
        Scale = float(pm.floatSliderGrp('WindowControllerProcessingControllerSizeFloatSliderGrp', q=1, v=1))
        ZKM_CurveControllerEditClass().ZKM_ModifyControllerShapeTRS("scale", Scale, Scale, Scale)
        ZKM_AutomaticModificationUIRangeClass().ZKM_FloatSlider_Max_Edit_Controller('WindowControllerProcessingControllerSizeFloatSliderGrp')

    # 旋转控制器
    def RotationController(self):
        Rotate = str(pm.radioCollection('WindowControllerProcessingControllerOrientation', q=1, select=1))
        ZKM_CurveControllerEditClass().ZKM_RotationController(Rotate)
    # 生成控制器
    def ChuangJianFK(self):
        Name = pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, sl=1)
        C_GrpNum = int(pm.intSliderGrp('WindowControllerProcessingNumberControllerGroups', q=1, v=1))  # 样条组数值
        Suffix = str(pm.textFieldGrp('WindowControllerProcessingSuffix', q=1, text=1))  # 获取后缀
        Colour = pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',q=1, rgb=1)
        # 移除根骨骼
        RemoveJoint = pm.checkBox('WindowControllerProcessingIgnoreEndBones_checkBox', q=1, v=1)
        ZKM_CurveControllerEditClass().ZKM_ChuangJianFK(Name, C_GrpNum, Suffix, RemoveJoint,Colour)
    # 旧版生成控制器
    def OldChuangJianFK(self):
        Name = pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, sl=1)
        C_GrpNum = int(pm.intSliderGrp('WindowControllerProcessingNumberControllerGroups', q=1, v=1))  # 样条组数值
        Suffix = str(pm.textFieldGrp('WindowControllerProcessingSuffix', q=1, text=1))  # 获取后缀
        Colour = pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp', q=1, rgb=1)
        # 移除根骨骼
        RemoveJoint = pm.checkBox('WindowControllerProcessingIgnoreEndBones_checkBox', q=1, v=1)
        ZKM_CurveControllerEditClass().ZKM_OldChuangJianFK(Name, C_GrpNum, Suffix, RemoveJoint, Colour)
    # 毛囊附着
    def HairFollicleAdsorption(self):
        MD = pm.textFieldButtonGrp('WindowControllerProcessing_HairFollicleConstraint_MD', q=1, text=1)
        Sel = pm.ls(sl=1)
        Keep = str(pm.checkBox('HairFollicleConstraint_KeepPlace_checkBox', q=1 , value=1))
        ZKM_FollicleClass().ZKM_FollicleConstraint(MD,Sel,Keep)
    # 链接属性
    def LinkProperty(self):
        TextField_MB = str(pm.textFieldButtonGrp('WindowControllerProcessing_LoadTargetProperties', q=1, text=1))
        TextField_Y = str(pm.textFieldButtonGrp('WindowControllerProcessing_LoadSourceProperties', q=1, text=1))
        pm.shadingNode('multiplyDivide', asUtility=1, n=(TextField_MB + "_multiplyDivide"))
        multiplyDivide = pm.ls(sl=1)
        pm.connectAttr(TextField_Y, (multiplyDivide[0] + ".input1X"), f=1)
        pm.connectAttr((multiplyDivide[0] + ".outputX"), TextField_MB, f=1)
        Num = float(pm.textFieldGrp('LJBL', q=1, text=1))
        pm.setAttr((multiplyDivide[0] + ".input2X"), Num)

    # 去除重复命名物体
    def detectionOfTheSameNameMain(self):
        ZKM_RootDirectory = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        print '别人写的，这种我就不重新写了'
        pm.mel.eval('source \"'+ZKM_RootDirectory+'/Outside/去除重复的物体名.mel\";')

    # 添加特定属性
    def AddAttribute(self,name):
        AttributeName = pm.optionMenu(name,q=1,v=1)
        sel = pm.ls(sl=1,type='joint')
        Text = ''
        for T in sel:
            Text = Text + T+':'
        if sel:
            if AttributeName == u'NotGenerate':#字符通用码
                Attribute = pm.listAttr(sel[0],userDefined=True)
                if pm.objExists((sel[0] + '.notes')):
                    Attribute.remove('notes')
                if pm.objExists((sel[0] + '.NotGenerate')):
                    Attribute.remove('NotGenerate')
                for An in Attribute:
                    if pm.objExists((sel[0] + '.'+An)):
                        pm.catch(lambda: pm.deleteAttr(sel[0], attribute=An))
                if pm.objExists((sel[0] + '.NotGenerate')):
                    pm.catch(lambda: pm.deleteAttr(sel[0], attribute="NotGenerate"))
                else:
                    pm.addAttr(sel[0], ln='NotGenerate', en='self:subset:', at='enum')
                    pm.setAttr((sel[0] + '.NotGenerate'), e=1, keyable=True)
                    pm.select(sel[0])
            else:
                if pm.objExists((sel[0] + '.NotGenerate')):
                    pm.catch(lambda: pm.deleteAttr(sel[0], attribute="NotGenerate"))
                for Name in [u'IK',u'Cup',u'SplineIK', u'AIM', u'Wheel',u'Global']:
                    if AttributeName == Name:  # 字符通用码
                        if pm.objExists((sel[0] + '.' + Name)):
                            pm.catch(lambda: pm.deleteAttr(sel[0], attribute=Name))
                        else:
                            pm.addAttr(sel[0], ln=Name, en=Text, at='enum')
                            pm.setAttr((sel[0] + '.' + Name), e=1, keyable=True)
                            pm.select(sel[0])

                for Name in [u'Wrist',u'Cup',u'PinkyFinger', u'RingFinger', u'MiddleFinger', u'IndexFinger', u'ThumbFinger']:
                    if AttributeName == Name:  # 字符通用码
                        if pm.objExists((sel[0] + '.' + Name)):
                            pm.catch(lambda: pm.deleteAttr(sel[0], attribute=Name))
                        else:
                            pm.addAttr(sel[0], ln=Name, en=Text, at='enum')
                            pm.setAttr((sel[0] + '.' + Name), e=1, keyable=True)
                            pm.select(sel[0])

                for Name in [u'Foot',u'Heel',u'Tiptoe', u'ToesFront', u'ToesBack', u'Ankle']:
                    if AttributeName == Name:  # 字符通用码
                        if pm.objExists((sel[0] + '.' + Name)):
                            pm.catch(lambda: pm.deleteAttr(sel[0], attribute=Name))
                        else:
                            pm.addAttr(sel[0], ln=Name, en=Text, at='enum')
                            pm.setAttr((sel[0] + '.' + Name), e=1, keyable=True)
                            pm.select(sel[0])

    # 骨骼整体缩放
    def JointScale(self):
        pm.jointDisplayScale(pm.floatSliderGrp('WindowControllerProcessingControllerJointSize',q=1,v=1))
        ZKM_AutomaticModificationUIRangeClass().ZKM_FloatSlider_Max_Edit_Controller('WindowControllerProcessingControllerJointSize')

    # 骨骼显示隐藏
    def ShowHideJoint(self):
        Text = pm.button('ShowHideJoint_Button', q=1, l=1)
        Joint = pm.ls(typ="joint")
        if Text == u'隐藏所有骨骼':
            for i in range(0, len(Joint)):
                pm.setAttr((Joint[i] + ".drawStyle"), 2)
            pm.button('ShowHideJoint_Button', e=1, l='显示所有骨骼',bgc=(0.6,0.6,0.6))
        if Text == u'显示所有骨骼':
            for i in range(0, len(Joint)):
                pm.setAttr((Joint[i] + ".drawStyle"), 0)
            pm.button('ShowHideJoint_Button', e=1, l='隐藏所有骨骼',bgc=(1,1,1))

    # 导入文件
    def ImportFile(self):
        cur_dir = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dir)  # 获取文件路径A
        name = pm.optionMenu('WindowControllerProcessingImportFile',q=1,v=1)
        #name = name.encode('utf-8')
        ZKM_FileProcessingClass().ZKM_ImportFile(name, (file_pathReversion + '/ControllerProcessingWindowModel'), 1, 'mayaBinary')

    # 创建部件模板
    def CreateModel(self):
        AttributeName = pm.optionMenu('WindowControllerProcessingCreateModel', q=1, v=1)
        if AttributeName == u'hand':#字符通用码
            #创建骨骼
            pm.select(cl=1)
            AllJoint = []
            wrist = pm.joint(p=(0, 0, 0), n='Wrist')
            AllJoint.append(wrist)
            pm.joint(p=(-1, 0, 0), n='WristEnd')
            pm.select(wrist)
            Cup = pm.joint(p=(-1, 0, -1), n='Cup')
            AllJoint.append(Cup)
            pm.joint(Cup, sao='yup', zso=1, e=1, oj='xyz')
            AllName = ['PinkyFinger', 'RingFinger', 'MiddleFinger', 'IndexFinger', 'ThumbFinger']
            for i in range(1, 5):
                if i > 1:
                    pm.select(wrist)
                else:
                    pm.select(Cup)
                for n in range(4, 8):
                    finger = pm.joint(p=(-n, 0, i - 2), n=AllName[i] + str(n - 3))
                    AllJoint.append(finger)
            pm.select(Cup)
            for n in range(4, 8):
                finger = pm.joint(p=(-n, 0, -2), n=AllName[0] + str(n - 3))
                AllJoint.append(finger)
            pm.select(wrist)
            pm.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
            pm.select(AllJoint[0])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=1)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(AllJoint[0],AllJoint[1])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=2)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(AllJoint[0],AllJoint[18:22])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=3)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(AllJoint[0], AllJoint[2:6])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=4)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(AllJoint[0], AllJoint[6:10])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=5)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(AllJoint[0], AllJoint[10:14])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=6)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(AllJoint[0], AllJoint[14:18])
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=7)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=1)


        if AttributeName == u'foot':#字符通用码
            #创建骨骼
            pm.select(cl=1)
            foot = pm.joint(p=(0, 2, 0), n='Foot')
            pm.joint(p=(0, 1, 0), n='FootEnd')
            pm.select(foot)
            Heel = pm.joint(p=(0, 0, -1), n='Heel')
            Tiptoe = pm.joint(p=(0, 0, 3), n='Tiptoe')
            ToesFront = pm.joint(p=(0, 0.5, 2), n='ToesFront')
            pm.joint(p=(0, 0, 3), n='ToesFrontEnd')
            pm.select(Tiptoe)
            ToesBack = pm.joint(p=(0, 0.5, 2), n='ToesBack')
            Ankle = pm.joint(p=(0, 2, 0), n='Ankle')
            pm.joint(p=(0, 0, 0), n='AnkleEnd')
            pm.select(foot)
            pm.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
            pm.select(foot)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=1)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(foot,Heel)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=2)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(foot,Tiptoe)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=3)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(foot,ToesFront)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=4)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(foot,ToesBack)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=5)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.select(foot,Ankle)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=6)
            self.AddAttribute('WindowControllerProcessingCreateModel_Attribute')
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', e=1, sl=1)

    # 修改配件UI
    def ModifyAccessoryUI(self):
        AttributeName = pm.optionMenu('WindowControllerProcessingCreateModel', q=1, v=1)
        if AttributeName == u'hand':#字符通用码
            #创建骨骼
            cmds.deleteUI('WindowControllerProcessingCreateModel_Attribute', control=True)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', w=115,p='WindowControllerProcessingCreateModel_rowColumnLayout')
            pm.menuItem(label="Wrist")
            pm.menuItem(label="Cup")
            pm.menuItem(label="PinkyFinger")
            pm.menuItem(label="RingFinger")
            pm.menuItem(label="MiddleFinger")
            pm.menuItem(label="IndexFinger")
            pm.menuItem(label="ThumbFinger")
        if AttributeName == u'foot':#字符通用码
            cmds.deleteUI('WindowControllerProcessingCreateModel_Attribute', control=True)
            pm.optionMenu('WindowControllerProcessingCreateModel_Attribute', w=115,p='WindowControllerProcessingCreateModel_rowColumnLayout')
            pm.menuItem(label="Foot")
            pm.menuItem(label="Heel")
            pm.menuItem(label="Tiptoe")
            pm.menuItem(label="ToesFront")
            pm.menuItem(label="ToesBack")
            pm.menuItem(label="Ankle")


ShowWindow = ZKM_ControllerPresetTemplateWindowClass()
ShowWindow.ZKM_Window()