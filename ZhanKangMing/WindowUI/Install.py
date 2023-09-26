#coding=gbk
import os
import inspect
import pymel.core as pm
import maya.cmds as mc
import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
file_pathA = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A

# �����ļ������������
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
# �޸�PY�ļ�
cur_dirB = ('\\'+'\\').join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
print cur_dirB
Soure = file_path + '\\ZKM_plug_in_UI\\ZKM_plug_in.py'
Target = Text 	# �滻���.txt
load = []  # �洢
S = open(Soure,'r')
for line in S:
    line_s = line.replace('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
                          cur_dirB )
    load.append(line_s)
S.close()
T = open(Target,'w')
for line in load:
    T.writelines(line)  # ���滻���д���µ�.txt
T.close()
pm.pluginInfo(Text2, edit=1, autoload=True)
pm.loadPlugin('ZKM_plug_in')

