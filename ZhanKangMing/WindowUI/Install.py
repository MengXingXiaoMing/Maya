#coding=gbk
import os
import inspect
import pymel.core as pm
import maya.cmds as mc
import shutil
import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
file_pathA = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
plugin = pm.pluginInfo(q=1, lsp=1)
plugin = plugin[0].split('/')
Text = ''
for T in range(0,len(plugin)-1):
	Text = Text + plugin[T] + '\\'
Text = Text + 'ZKM_plug_in.py'
Text2 = ''
for T in range(0,len(plugin)-1):
	Text2 = Text2 + plugin[T] + '/'
Text2 = Text2 + 'ZKM_plug_in.py'
shutil.copyfile(file_path + '\\ZKM_plug_in.py',Text)
pm.pluginInfo(Text2, edit=1, autoload=True)
pm.loadPlugin('ZKM_plug_in')
