#coding=gbk
import os
import inspect

import sys
sys.dont_write_bytecode = True
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
# file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
# cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])
# file_pathA = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
# print(cur_dir)
# �����ļ������������
#plugin = pm.pluginInfo(q=1, lsp=1)
# Text2 = cur_dir + 'ZKM_plug_in.py'
# �޸�PY�ļ�
class CopyZKMPlugInClass():
    def copy_ZKM_plug_in(self,user_path):
        cur_dirB = ('\\'+'\\').join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        Soure = cur_dir + '\\ZKM_plug_in_UI\\ZKM_plug_in.py'
        Target = cur_dir + '\\ZKM_plug_in.py' 	# �滻���.txt
        load = []  # �洢
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
                line_s = line  # ���û��ƥ�������ԭ�У���ѡ��
            load.append(line_s)
        S.close()
        T = open(Target,'w')
        for line in load:
            T.writelines(line)  # ���滻���д���µ�.txt
        T.close()
#pm.pluginInfo(Text2, edit=1, autoload=True)
#pm.loadPlugin('ZKM_plug_in')
CopyZKMPlugInClass().copy_ZKM_plug_in('')
