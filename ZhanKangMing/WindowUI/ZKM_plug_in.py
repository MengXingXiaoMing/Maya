#coding=gbk
import os
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
	pm.button('MayaWindow_menu_Process_formLayout1_AddButton', parent='flowLayout1', l='小明的盒子')
	showMyMenuCtrl = pm.menu('MayaWindow_menu_Process_Button',parent='MayaWindow', label='小明的盒子')
	pm.menuItem(parent=showMyMenuCtrl, label='改名')
	pm.menuItem(parent=showMyMenuCtrl, label='权重处理')
	pm.menuItem(parent=showMyMenuCtrl, label='控制器处理')
	pm.menuItem(parent=showMyMenuCtrl, label='预置模板')
	pm.menuItem(parent=showMyMenuCtrl, label='所有功能还在添加中')
	pm.menuItem(label="Option")
	pm.menuItem(optionBox=True)
	pm.menuItem(subMenu=True, label="Colors")
	pm.menuItem(label="Blue")
	pm.menuItem(label="Green")
	pm.menuItem(label="Yellow")


