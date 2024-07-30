#coding=gbk
import os
import sys
import maya.cmds as cmds
import inspect
FilePath = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
sys.path.append(FilePath + '\\ZKM_plug_in_UI')
import ZKM_plug_in_Command
from ZKM_plug_in_Command import *

#仅仅用于加载预置插件,会减慢打开速度,加载后遍可以使用其中内置命令
def initializePlugin(obg):
	sys.path.append(FilePath + '\\ZKM_plug_in_UI')
	cmds.python('import ZKM_plug_in_Command')
	cmds.python('from ZKM_plug_in_Command import *')

	LoadPresetPlugIns()
def uninitializePlugin(obj):
	plugin=om.MFnPlugin(obg)
	plugin.deregisterCommand(MatrixComd.kPluginCmdName)
def LoadPresetPlugIns():
	# MAYA版本
	maya_version = cmds.about(version=True)
	FilePathBackslash = FilePath.split('\\')
	Text = ''
	for F in FilePathBackslash:
		Text = Text + F + '/'
	try:
		cmds.deleteUI('MayaWindow_menu_Process_Button')
	except:
		pass
	try:
		cmds.deleteUI('MayaWindow_menu_Process_formLayout1_AddButton')
	except:
		pass
	cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', parent='flowLayout1',i1=FilePath+'\\ZKM_plug_in_UI\\ButtonNomalUI.png',hi=FilePath+'\\ZKM_plug_in_UI\\ButtonMoveInUI.png',
					  c='ZKM_plug_in_Class().open_web()')
	showMyMenuCtrl = cmds.menu('MayaWindow_menu_Process_Button', tearOff=True,parent='MayaWindow', label='梦星盒子')
	cmds.menuItem(label='文件清理',
				c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\clear_files\',\'clear_files_window\',\'window.show()\')')
	cmds.menuItem(label='权重处理',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\weight_processing\',\'weight_processing_window\',\'window.show()\')')
	cmds.menuItem(label='控制器处理',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\controller_processing\',\'controller_processing_window\',\'window.show()\')')
	# cmds.menuItem(subMenu=True, label='控制器处理')
	# cmds.menuItem(label='《—主窗口ヾ(^▽^*)))',
	# 			c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\controller_processing\',\'controller_processing_window\',\'window.show()\')')
	# cmds.menuItem(label='属性可视化(未开发)',c='')
	# cmds.setParent('..', menu=True)
	cmds.menuItem(label='BS编辑',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\bs_edit\',\'bs_edit_window\',\'window.show()\')')
	cmds.menuItem(label='新轮胎表达式',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\tire_baking_expression\',\'tire_baking_expression_window\',\'window.show()\')')
	cmds.menuItem(label='曲面绳子',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\curved_rope\',\'curved_rope_window\',\'window.show()\')')
	cmds.menuItem(label='自定义命令',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\custom_commands\',\'custom_commands_window\',\'window.show()\')')
	cmds.menuItem(label='驱动器',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\disk_drive\',\'disk_drive_window\',\'window.show()\')')
	'''cmds.menuItem(subMenu=True, label='预置模板')
	cmds.menuItem(label='《—主窗口ヾ(^▽^*)))',
				c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\',\'PresetTemplateWindow\',\'ShowWindow.ZKM_Window()\')')
	cmds.menuItem(label='不同拓补传递BS',
				c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\\DifferentTopologyTransferBS\',\'DifferentTopologyTransfer_BS\',\'ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()\')')
	cmds.menuItem(label='SSDR', c='print (\'未添加\')')
	cmds.setParent('..', menu=True)'''
	cmds.setParent('..', menu=True)
	cmds.menuItem(divider=True, l='即将添加功能')
	cmds.menuItem('ZKM_plug_in_Automatically_switch_wallpapers',checkBox=True, label="自动切换壁纸")
	cmds.menuItem(optionBox=True,c='ZKM_plug_in_Class().help()')
	cmds.menuItem(divider=True, l='功能未完善╮(╯▽╰)╭')
	cmds.menuItem(label="打开文档(我是懒狗，压根没写哈哈哈)", i='fileOpen.png', c='ZKM_plug_in_Class().open_document()')
	cmds.menuItem(optionBox=True)
	cmds.menuItem(label="帮助(目前为空)", i='help.png', c='ZKM_plug_in_Class().help()')
	cmds.menuItem(label="访问UP主页(按住ctrl可进入GitHub))", i='implicitSphere.svg', c='ZKM_plug_in_Class().open_web()')




