#coding=gbk
import os
import inspect
import pymel.core as pm
import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
file_pathA = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
pm.melGlobals.initVar('string', 'gShelfTopLevel')
currentShelf=str(pm.tabLayout(pm.melGlobals['gShelfTopLevel'], query=1, selectTab=1))
pm.setParent(currentShelf)
pm.shelfButton(sourceType='python',
	image=(file_pathA+'/ControllerIcon.png'),
	label='����������',
	iol=(''),
	command=('import sys\nsys.path.append(r\"'+file_path+'\")\nimport ControllerProcessingWindow\nfrom ControllerProcessingWindow import *\nShowWindow.ZKM_Window()'),
	image1=(file_pathA+'/ControllerIcon.png'),
	annotation='����������')

