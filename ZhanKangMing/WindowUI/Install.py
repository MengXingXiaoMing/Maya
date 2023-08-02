#coding=gbk
import os
import inspect
import pymel.core as pm
import maya.cmds as mc
import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_path = os.path.join(cur_dir)  # 获取文件路径
cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
file_pathA = os.path.join(cur_dirA)  # 获取文件路径A

# 复制文件到插件管理器
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
# 修改PY文件
cur_dirB = ('\\'+'\\').join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
print cur_dirB
Soure = file_path + '\\ZKM_plug_in_UI\\ZKM_plug_in.py'
Target = Text 	# 替换后的.txt
load = []  # 存储
S = open(Soure,'r')
for line in S:
    line_s = line.replace('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
                          cur_dirB )
    load.append(line_s)
S.close()
T = open(Target,'w')
for line in load:
    T.writelines(line)  # 将替换后的写入新的.txt
T.close()
pm.pluginInfo(Text2, edit=1, autoload=True)
pm.loadPlugin('ZKM_plug_in')

