#coding=gbk
import os
import inspect
class filePath:
    def file_path(self):
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        return file_path
    def file_pathReversion(self):
        cur_dir_Reversion = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path_Reversion = os.path.join(cur_dir_Reversion)  # ��ȡ�ļ�·��A
        return file_path_Reversion
