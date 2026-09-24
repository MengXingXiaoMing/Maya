# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    # 库路径
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)
# 添加正确的 PySide2 导入

for i in range(30):
    maya_version_int = maya_version_int - i
    # 库路径
    maya_version = str(maya_version_int)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)

#加载文本
class MayaCommon:
    def select_text_target(self, soure_ui, soure_ui_type):
        if soure_ui_type[0] == 'QLineEdit':
            text = soure_ui.text()
            all_name = text.split(',')
            cmds.select(all_name)