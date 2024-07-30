# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance

import maya.cmds as cmds
# 获取文件路径
import os
import sys
import inspect
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

#加载文本
class MayaCommon:
    def select_text_target(self, soure_ui, soure_ui_type):
        if soure_ui_type[0] == 'QLineEdit':
            text = soure_ui.text()
            all_name = text.split(',')
            all_select = []
            for sel in all_name:
                name = sel.split('.')
                all_select.append(name[0])
            cmds.select(all_select)
