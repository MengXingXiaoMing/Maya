#coding=gbk
import os
import sys
import pymel.core as pm

#�������ڼ���Ԥ�ò��,��������ٶ�,���غ�����ʹ��������������
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
	showMyMenuCtrl = pm.menu('MayaWindow_menu_Process_Button', tearOff=True,parent='MayaWindow', label='���Ǻ���')
	pm.menuItem(label='����',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\Rename\',\'RenameWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label='Ȩ�ش���',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\WeightProcessing\',\'WeightProcessing\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(subMenu=True, label='����������')
	pm.menuItem(label='���������کd(^��^*)))',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\ControllerProcessing\',\'ControllerProcessingWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label='���Կ��ӻ�',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\ControllerProcessing\\ControllerProcessingWindowPictureMaterials\',\'AttributeVisualizationWindow\',\'ZKM_AttributeVisualizationClass().AttributeVisualizationWindow()\')')
	pm.setParent('..', menu=True)
	pm.menuItem(subMenu=True, label='Ԥ��ģ��')
	pm.menuItem(label='���������کd(^��^*)))',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\',\'PresetTemplateWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label='��ͬ�ز�����BS',
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\\DifferentTopologyTransferBS\',\'DifferentTopologyTransfer_BS\',\'ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()\')')
	pm.menuItem(label='SSDR', c='print \'δ���\'')
	pm.setParent('..', menu=True)
	pm.menuItem(label="ȹ�Ӹ���",
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\SkirtCollision\',\'SkirtCollision\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label="����м�֡",
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\AddIntermediate\',\'Addintermediate\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(label="Ʈ������",
				c='ZKM_plug_in_Class().Open_RunPY_Window(r\'' + FilePath + '\\Maya_WindowUI\\Rope\',\'RopeWindow\',\'ShowWindow.ZKM_Window()\')')
	pm.menuItem(subMenu=True, label='��װ��������')
	pm.menuItem(label='����',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/Rename/Install.py\')')
	pm.menuItem(label='Ȩ�ش���',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/WeightProcessing/Install.py\')')
	pm.menuItem(label='����������',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/ControllerProcessing/Install.py\')')
	pm.menuItem(label='Ԥ��ģ��',
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/PresetTemplateFile/Install.py\')')
	pm.menuItem(label="ȹ�Ӹ���",
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/SkirtCollision/Install.py\')')
	pm.menuItem(label="����м�֡",
				c='ZKM_plug_in_Class().Install_Window(r\'' + Text + 'Maya_WindowUI/AddIntermediate/Install.py\')')
	pm.setParent('..', menu=True)
	pm.menuItem(divider=True, l='������ӹ���')
	pm.menuItem('ZKM_plug_in_Automatically_switch_wallpapers',checkBox=True, label="�Զ��л���ֽ")
	pm.menuItem(optionBox=True,c='ZKM_plug_in_Class().Help()')
	pm.menuItem(label="��������������")
	pm.menuItem(divider=True, l='����δ���ƨr(�s���t)�q')
	pm.menuItem(label="���ĵ�(��������,�ļ��ܴ�)", i='fileOpen.png', c='ZKM_plug_in_Class().Open_Document()')
	pm.menuItem(optionBox=True)
	pm.menuItem(label="����", i='help.png', c='ZKM_plug_in_Class().Help()')
	pm.menuItem(label="����UP��ҳ(��סctrl�ɽ���GitHub))", i='implicitSphere.svg', c='ZKM_plug_in_Class().Open_web()')
	import maya.app.general.executeDroppedPythonFile as myTempEDPF
	myTempEDPF.executeDroppedPythonFile(FilePath + '\\ZKM_plug_in_UI\\ZKM_plug_in_Command.py',"")
	del myTempEDPF
	sys.path.append(FilePath + '\\ZKM_plug_in_UI\\ZKM_plug_in_Command.py')
	pm.mel.eval('python(\"import pymel.core as pm\")')
	pm.mel.eval('python(\"from ZKM_plug_in_Command import *\")')


