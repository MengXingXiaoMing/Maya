#coding=gbk
import os
import pymel.core as pm
import maya.cmds as cmds
#�������ڼ���Ԥ�ò��,��������ٶ�,���غ�����ʹ��������������
def initializePlugin(obg):
	LoadPresetPlugIns()

def uninitializePlugin(obj):
	plugin=om.MFnPlugin(obg)
	plugin.deregisterCommand(MatrixComd.kPluginCmdName)

def LoadPresetPlugIns():
	    if not cmds.commandPort(":4434", query=True):
	    	    cmds.commandPort(name=":4434")
