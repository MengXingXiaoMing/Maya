#coding=gbk
import os
import sys
import pymel.core as pm

#仅仅用于加载预置插件,会减慢打开速度,加载后遍可以使用其中内置命令
def initializePlugin(obg):
	LoadPresetPlugIns()
def uninitializePlugin(obj):
	plugin=om.MFnPlugin(obg)
	plugin.deregisterCommand(MatrixComd.kPluginCmdName)
def LoadPresetPlugIns():
	try:
		pm.deleteUI('MayaWindow_menu_Process_Button')
	except:
		pass
	try:
		pm.deleteUI('MayaWindow_menu_Process_formLayout1_AddButton')
	except:
		pass
	FilePath = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
	FilePathBackslash = FilePath.split('\\')
	Text = ''
	for F in FilePathBackslash:
		Text = Text + F + '/'
	pm.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', parent='flowLayout1',i1=FilePath+'\\ZKM_plug_in_UI\\ButtonNomalUI.png',hi=FilePath+'\\ZKM_plug_in_UI\\ButtonMoveInUI.png',
					  c='ZKM_plug_in_Class().Open_web()')
	showMyMenuCtrl = pm.menu('MayaWindow_menu_Process_Button', tearOff=True,parent='MayaWindow', label='梦星盒子')
	pm.menuItem(label='改名',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\Rename\',\'RenameWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label='权重处理',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\WeightProcessing\',\'WeightProcessing\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(subMenu=True, label='控制器处理')
	pm.menuItem(label='《—主窗口ヾ(^▽^*)))',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\ControllerProcessing\',\'ControllerProcessingWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label='属性可视化',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\ControllerProcessing\\ControllerProcessingWindowPictureMaterials\',\'AttributeVisualizationWindow\',\'ZKM_AttributeVisualizationClass().AttributeVisualizationWindow()\')')
	pm.setParent('..', menu=True)
	pm.menuItem(subMenu=True, label='预置模板')
	pm.menuItem(label='《—主窗口ヾ(^▽^*)))',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\',\'PresetTemplateWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label='不同拓补传递BS',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\\DifferentTopologyTransferBS\',\'DifferentTopologyTransfer_BS\',\'ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()\')')
	pm.menuItem(label='SSDR', c='print \'未添加\'')
	pm.setParent('..', menu=True)
	pm.menuItem(label="裙子跟随",
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\SkirtCollision\',\'SkirtCollision\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label="添加中间帧",
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\AddIntermediate\',\'Addintermediate\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label="飘带绳子",
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\Rope\',\'RopeWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(subMenu=True, label='安装到工具栏')
	pm.menuItem(label='改名',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/Rename/Install.py\')')
	pm.menuItem(label='权重处理',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/WeightProcessing/Install.py\')')
	pm.menuItem(label='控制器处理',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/ControllerProcessing/Install.py\')')
	pm.menuItem(label='预置模板',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/PresetTemplateFile/Install.py\')')
	pm.menuItem(label="裙子跟随",
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/SkirtCollision/Install.py\')')
	pm.menuItem(label="添加中间帧",
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/AddIntermediate/Install.py\')')
	pm.setParent('..', menu=True)
	pm.menuItem(divider=True, l='即将添加功能')
	pm.menuItem('ZKM_plug_in_Automatically_switch_wallpapers',checkBox=True, label="自动切换壁纸")
	pm.menuItem(optionBox=True,c='ZKM_plug_in_Class().Help()')
	pm.menuItem(label="动画、驱动曲线")
	pm.menuItem(divider=True, l='功能未完善╮(╯▽╰)╭')
	pm.menuItem(label="打开文档(得先下载,文件很大)", i='fileOpen.png', c='ZKM_plug_in_Class().Open_Document()')
	pm.menuItem(optionBox=True)
	pm.menuItem(label="帮助", i='help.png', c='ZKM_plug_in_Class().Help()')
	pm.menuItem(label="访问UP主页(按住ctrl可进入GitHub))", i='implicitSphere.svg', c='ZKM_plug_in_Class().Open_web()')
	import maya.app.general.executeDroppedPythonFile as myTempEDPF
	myTempEDPF.executeDroppedPythonFile(FilePath + '\\ZKM_plug_in_UI\\ZKM_plug_in_Command.py',"")
	del myTempEDPF
	sys.path.append(FilePath + '\\ZKM_plug_in_UI\\ZKM_plug_in_Command.py')
	pm.mel.eval('python(\"import pymel.core as pm\")')
	pm.mel.eval('python(\"from ZKM_plug_in_Command import *\")')


