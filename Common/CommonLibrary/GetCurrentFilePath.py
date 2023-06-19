#coding=gbk
import os
import inspect
class filePath:
    def file_path(self):
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        return file_path
    def file_pathReversion(self):
        cur_dir_Reversion = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path_Reversion = os.path.join(cur_dir_Reversion)  # 获取文件路径A
        return file_path_Reversion
