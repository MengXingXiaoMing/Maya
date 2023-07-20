#coding=gbk
import os
import pymel.core as pm
import maya.cmds as cmds
#仅仅用于加载预置插件,会减慢打开速度,加载后遍可以使用其中内置命令
def initializePlugin(obg):
	LoadPresetPlugIns()

def uninitializePlugin(obj):
	plugin=om.MFnPlugin(obg)
	plugin.deregisterCommand(MatrixComd.kPluginCmdName)

def LoadPresetPlugIns():
	    if not cmds.commandPort(":4434", query=True):
	    	    cmds.commandPort(name=":4434")
