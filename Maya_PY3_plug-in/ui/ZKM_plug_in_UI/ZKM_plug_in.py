#coding=gbk
import os
import sys
import maya.cmds as cmds
import inspect
FilePath = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
sys.path.append(FilePath + '\\ZKM_plug_in_UI')
import ZKM_plug_in_Command
from ZKM_plug_in_Command import *

#�������ڼ���Ԥ�ò��,��������ٶ�,���غ�����ʹ��������������
def initializePlugin(obg):
	sys.path.append(FilePath + '\\ZKM_plug_in_UI')
	cmds.python('import ZKM_plug_in_Command')
	cmds.python('from ZKM_plug_in_Command import *')

	LoadPresetPlugIns()
def uninitializePlugin(obj):
	plugin=om.MFnPlugin(obg)
	plugin.deregisterCommand(MatrixComd.kPluginCmdName)
def LoadPresetPlugIns():
	# MAYA�汾
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
	showMyMenuCtrl = cmds.menu('MayaWindow_menu_Process_Button', tearOff=True,parent='MayaWindow', label='���Ǻ���')
	cmds.menuItem(label='�ļ�����',
				c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\clear_files\',\'clear_files_window\',\'window.show()\')')
	cmds.menuItem(label='Ȩ�ش���',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\weight_processing\',\'weight_processing_window\',\'window.show()\')')
	cmds.menuItem(label='����������',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\controller_processing\',\'controller_processing_window\',\'window.show()\')')
	# cmds.menuItem(subMenu=True, label='����������')
	# cmds.menuItem(label='���������کd(^��^*)))',
	# 			c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\controller_processing\',\'controller_processing_window\',\'window.show()\')')
	# cmds.menuItem(label='���Կ��ӻ�(δ����)',c='')
	# cmds.setParent('..', menu=True)
	cmds.menuItem(label='BS�༭',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\bs_edit\',\'bs_edit_window\',\'window.show()\')')
	cmds.menuItem(label='����̥���ʽ',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\tire_baking_expression\',\'tire_baking_expression_window\',\'window.show()\')')
	cmds.menuItem(label='��������',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\curved_rope\',\'curved_rope_window\',\'window.show()\')')
	cmds.menuItem(label='�Զ�������',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\custom_commands\',\'custom_commands_window\',\'window.show()\')')
	cmds.menuItem(label='������',
				  c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\disk_drive\',\'disk_drive_window\',\'window.show()\')')
	'''cmds.menuItem(subMenu=True, label='Ԥ��ģ��')
	cmds.menuItem(label='���������کd(^��^*)))',
				c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\',\'PresetTemplateWindow\',\'ShowWindow.ZKM_Window()\')')
	cmds.menuItem(label='��ͬ�ز�����BS',
				c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\\DifferentTopologyTransferBS\',\'DifferentTopologyTransfer_BS\',\'ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()\')')
	cmds.menuItem(label='SSDR', c='print (\'δ���\')')
	cmds.setParent('..', menu=True)'''
	cmds.setParent('..', menu=True)
	cmds.menuItem(divider=True, l='������ӹ���')
	cmds.menuItem('ZKM_plug_in_Automatically_switch_wallpapers',checkBox=True, label="�Զ��л���ֽ")
	cmds.menuItem(optionBox=True,c='ZKM_plug_in_Class().help()')
	cmds.menuItem(divider=True, l='����δ���ƨr(�s���t)�q')
	cmds.menuItem(label="���ĵ�(����������ѹ��ûд������)", i='fileOpen.png', c='ZKM_plug_in_Class().open_document()')
	cmds.menuItem(optionBox=True)
	cmds.menuItem(label="����(ĿǰΪ��)", i='help.png', c='ZKM_plug_in_Class().help()')
	cmds.menuItem(label="����UP��ҳ(��סctrl�ɽ���GitHub))", i='implicitSphere.svg', c='ZKM_plug_in_Class().open_web()')




