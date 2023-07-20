#coding=gbk
import os
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
	pm.button('MayaWindow_menu_Process_formLayout1_AddButton', parent='flowLayout1', l='С���ĺ���')
	showMyMenuCtrl = pm.menu('MayaWindow_menu_Process_Button',parent='MayaWindow', label='С���ĺ���')
	pm.menuItem(parent=showMyMenuCtrl, label='����')
	pm.menuItem(parent=showMyMenuCtrl, label='Ȩ�ش���')
	pm.menuItem(parent=showMyMenuCtrl, label='����������')
	pm.menuItem(parent=showMyMenuCtrl, label='Ԥ��ģ��')
	pm.menuItem(parent=showMyMenuCtrl, label='���й��ܻ��������')
	pm.menuItem(label="Option")
	pm.menuItem(optionBox=True)
	pm.menuItem(subMenu=True, label="Colors")
	pm.menuItem(label="Blue")
	pm.menuItem(label="Green")
	pm.menuItem(label="Yellow")


