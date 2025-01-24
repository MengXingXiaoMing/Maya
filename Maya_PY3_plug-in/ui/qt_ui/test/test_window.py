# -*- coding: utf-8 -*-
import inspect
import os
import sys

import random

from datetime import datetime
import maya.mel as mel

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

import importlib
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library = root_path + '\\' + maya_version
# 库添加到系统路径
sys.path.append(library)

print('asdasdasd')


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('表情制作(Maya'+self.maya_version+')')
        self.create_widgets()
        self.create_layouts()
        self.create_connect()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = self.root_path + '\\' + self.maya_version

    dlg_instance = None
    @classmethod
    def show_dialg(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = Window()
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def create_widgets(self):
        # 第一行
        self.Label_1 = QtWidgets.QLabel('模板DNA路径：')

        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_1 = QtWidgets.QPushButton()
        self.button_1.setIcon(QtGui.QIcon(':/fileOpen.png'))


        self.Label_2 = QtWidgets.QLabel('附加txt路径：')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton()
        self.button_2.setIcon(QtGui.QIcon(':/fileOpen.png'))

        self.button_3 = QtWidgets.QPushButton()
        self.button_3.setIcon(QtGui.QIcon(':/help.png'))



    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.setSpacing(1)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.Label_1)
        h_Box_layout_3.addWidget(self.line_edit_1)
        h_Box_layout_3.addWidget(self.button_1)
        h_Box_layout_3.setSpacing(1)
        # h_Box_layout_1.addStretch(1)



        main_layout.addStretch(1)

    def create_connect(self):
        pass

window = Window()
if __name__ == '__main__':
    # try:
    #     window.close()
    #     window.deleteLater()
    # except:
    #     pass
    window.show()


# attribute = cmds.channelBox('mainChannelBox', q=1, sma=1)
# print(len(attribute))