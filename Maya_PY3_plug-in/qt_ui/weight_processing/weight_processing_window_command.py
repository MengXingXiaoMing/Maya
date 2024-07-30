# -*- coding: utf-8 -*-
import maya.cmds as cmds
# 获取文件路径
import os
import sys
import inspect
import importlib

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version

# 库添加到系统路径
sys.path.append(library_path)

import maya_common
from maya_common import *

import ui_edit
from ui_edit import *

import weight
from weight import *

import others_library
from others_library import *

importlib.reload(maya_common)
importlib.reload(ui_edit)
importlib.reload(weight)
importlib.reload(others_library)

class Command():
    def __init__(self):
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version

        self.maya_common = MayaCommon()
        self.ui_edit = UiEdit()
        self.weight = Weight()
        self.others_library = OthersLibrary()

    # 自动调整滑块范围且返回数值给ui
    def automatically_adjust_the_slider_range_and_return_values_to_ui(self, soure_ui, soure_ui_type):
        num = self.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(soure_ui, soure_ui_type)
        soure_ui.setMinimum(1)
        max_num = soure_ui.maximum()
        if max_num > 10000:
            soure_ui.setMaximum(10000)
        return num




