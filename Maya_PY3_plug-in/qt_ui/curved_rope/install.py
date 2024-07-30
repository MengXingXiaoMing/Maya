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
	name = '文件清理'
	Icon = 'curved_rope_Icon.png'
	file = 'curved_rope_window'
	cmds.shelfButton(sourceType='python',
		image=(file_path_reverse+'/'+Icon),
		label=name,
		iol=(''),
		command=('import sys\nsys.path.append(r\"'+file_path+'\")\nimport '+file+'\nimport importlib\nimportlib.reload('+file+')\nfrom '+file+' import *\nwindow.show()'),
		image1=(file_path_reverse + '/'+Icon),
		annotation=name)
	print(name+' 已安装。')
instal()