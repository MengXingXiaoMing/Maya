#coding=gbk
import os
import inspect
import pymel.core as pm
import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_path = os.path.join(cur_dir)  # 获取文件路径
cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
file_pathA = os.path.join(cur_dirA)  # 获取文件路径A
pm.melGlobals.initVar('string', 'gShelfTopLevel')
currentShelf=str(pm.tabLayout(pm.melGlobals['gShelfTopLevel'], query=1, selectTab=1))
pm.setParent(currentShelf)
print (file_pathA+'/SkirtFollowIcon.png')
pm.shelfButton(sourceType='python',
	image=('bsd-add.png'),
	label='自动添加中间帧',
	iol=(''),
	command=('import sys\nsys.path.append(r\"'+file_path+'\")\nimport Addintermediate\nfrom Addintermediate import *\nShowWindow.ZKM_Window()'),
	image1=('bsd-add.png'),
	annotation='自动添加中间帧')
