#coding=gbk
import os
import inspect
import maya.cmds as cmds
import maya.mel as mel
def instal():
	file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))  # ��ȡ�ļ�·��
	file_path_reverse = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))  # ��ȡ�ļ�·��
	gShelfTopLevel = mel.eval('string $my_gShelfTopLevel = $gShelfTopLevel')
	current_shelf = str(cmds.tabLayout(gShelfTopLevel, query=1, selectTab=1))
	cmds.setParent(current_shelf)
	name = 'Ȩ�ش���'
	Icon = 'pythonFamily.png'
	file = 'scroll_window'
	cmds.shelfButton(sourceType='python',
		image=(Icon),
		label=name,
		iol=(''),
		command=('import sys\nsys.path.append(r\"'+file_path+'\")\nimport '+file+'\nimport importlib\nimportlib.reload('+file+')\nfrom '+file+' import *\nwindow.show()'),
		image1=(Icon),
		annotation=name)
	print(name+' �Ѱ�װ��')
instal()
