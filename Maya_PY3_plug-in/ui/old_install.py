#coding=gbk
import os
import inspect

import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
# file_path = os.path.join(cur_dir)  # 获取文件路径
# cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
# file_pathA = os.path.join(cur_dirA)  # 获取文件路径A
# print(cur_dir)
# 复制文件到插件管理器
#plugin = pm.pluginInfo(q=1, lsp=1)
# Text2 = cur_dir + 'ZKM_plug_in.py'
# 修改PY文件
class CopyZKMPlugInClass():
    def copy_ZKM_plug_in(self,user_path):
        cur_dirB = ('\\'+'\\').join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        Soure = cur_dir + '\\ZKM_plug_in_UI\\ZKM_plug_in.py'
        Target = cur_dir + '\\ZKM_plug_in.py' 	# 替换后的.txt
        load = []  # 存储
        S = open(Soure,'r')
        if user_path == '':
            cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2])
            user_path = cur_dirA + '/uesr/self'
        print('user_path:',user_path)
        for line in S:
            if 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' in line:
                line_s = line.replace(
                    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', cur_dirB)
            elif 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB' in line:
                line_s = line.replace('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
                                      user_path)
            else:
                line_s = line  # 如果没有匹配项，则保留原行（可选）
            load.append(line_s)
        S.close()
        T = open(Target,'w')
        for line in load:
            T.writelines(line)  # 将替换后的写入新的.txt
        T.close()
#pm.pluginInfo(Text2, edit=1, autoload=True)
#pm.loadPlugin('ZKM_plug_in')
CopyZKMPlugInClass().copy_ZKM_plug_in('')
