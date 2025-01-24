#coding=gbk
import os
import sys
import maya.cmds as cmds
import inspect
FilePath = 'Z:\\1.Private folder\\Rig\\zhankangming\\ZhanKangMing\\Maya_PY3_plug-in\\ui'
sys.path.append(FilePath + '\\ZKM_plug_in_UI')
import ZKM_plug_in_Command
from ZKM_plug_in_Command import *
ZKM_plug_in_user_file_path = r'Z:\1.Private folder\Rig\zhankangming\ZhanKangMing\Maya_PY3_plug-in\user\yangjie'

#�������ڼ���Ԥ�ò��,��������ٶ�,���غ�����ʹ��������������
def initializePlugin(obg):
	sys.path.append(FilePath + '\\ZKM_plug_in_UI')
	cmds.python('import ZKM_plug_in_Command')
	cmds.python('from ZKM_plug_in_Command import *')
	cmds.python('ZKM_plug_in_Class().LoadPresetPlugIns(r\''+ZKM_plug_in_user_file_path+'\')')

def uninitializePlugin(obj):
	plugin=om.MFnPlugin(obg)
	plugin.deregisterCommand(MatrixComd.kPluginCmdName)





