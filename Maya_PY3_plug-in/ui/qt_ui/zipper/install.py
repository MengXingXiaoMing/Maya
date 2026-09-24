#coding=gbk
import os
import inspect
import maya.cmds as cmds
import maya.mel as mel
def instal():
	file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))  # 获取文件路径
	file_path_reverse = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))  # 获取文件路径
	gShelfTopLevel = mel.eval('string $my_gShelfTopLevel = $gShelfTopLevel')
	current_shelf = str(cmds.tabLayout(gShelfTopLevel, query=1, selectTab=1))
	cmds.setParent(current_shelf)
	name = '拉链生成'
	Icon = 'pythonFamily.png'
	file = 'zipper_window'
	cmds.shelfButton(sourceType='python',
		image=(Icon),
		label=name,
		iol=(''),
		command=('import sys\nsys.path.append(r\"'+file_path+'\")\nimport '+file+'\nimport importlib\nimportlib.reload('+file+')\nfrom '+file+' import *\nwindow.show()'),
		image1=(Icon),
		annotation=name)
	print(name+' 已安装到当前工具架')
instal()
