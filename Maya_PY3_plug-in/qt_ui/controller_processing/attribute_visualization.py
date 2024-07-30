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

import others_library
from others_library import *
importlib.reload(others_library)


class AttributeWindow(QtWidgets.QDialog):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            attribute_window.close()
            attribute_window.deleteLater()
        except:
            pass
        super(AttributeWindow, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('属性可视化(Maya'+self.maya_version+')')
        self.setMinimumWidth(300)
        self.others_library = OthersLibrary()

        self.create_widgets()
        self.create_layouts()
        self.create_connect()
    def create_widgets(self):
        # 总模块
        self.scroll_bar_1 = QtWidgets.QScrollBar()
        #height = self.layout_widget.geometry().height()
        # 第一行
        self.button_1 = QtWidgets.QPushButton('加载具体属性')
        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        self.Label_1 = QtWidgets.QLabel()
        self.Label_1.setText('原名称 ')
        self.splitter_2 = QtWidgets.QSplitter()
        self.splitter_2.setFixedHeight(1)
        self.splitter_2.setFrameStyle(1)

        self.Label_2 = QtWidgets.QLabel()
        self.Label_2.setText('目标名称')
        self.splitter_3 = QtWidgets.QSplitter()
        self.splitter_3.setFixedHeight(1)
        self.splitter_3.setFrameStyle(1)

        self.Label_3 = QtWidgets.QLabel()
        self.Label_3.setText('可视化名称')
        self.splitter_4 = QtWidgets.QSplitter()
        self.splitter_4.setFixedHeight(1)
        self.splitter_4.setFrameStyle(1)

        self.button_2 = QtWidgets.QPushButton('转换')
        self.button_2.setVisible(0)
        self.line_edit_1 = QtWidgets.QLineEdit()




    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addStretch(0)

        h_box_layout_1 = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(h_box_layout_1)
        h_box_layout_1.addWidget(self.button_1)

        h_box_layout_2 = QtWidgets.QHBoxLayout(self)
        self.main_layout.addWidget(self.splitter_1)
        self.main_layout.addLayout(h_box_layout_2)

        v_box_layout_1 = QtWidgets.QVBoxLayout(self)
        v_box_layout_1.addWidget(self.Label_1)
        v_box_layout_1.addWidget(self.splitter_2)

        v_box_layout_2 = QtWidgets.QVBoxLayout(self)
        v_box_layout_2.addWidget(self.Label_2)
        v_box_layout_2.addWidget(self.splitter_3)

        v_box_layout_3 = QtWidgets.QVBoxLayout(self)
        v_box_layout_3.addWidget(self.Label_3)
        v_box_layout_3.addWidget(self.splitter_4)

        h_box_layout_2.addLayout(v_box_layout_1)
        h_box_layout_2.addLayout(v_box_layout_2)
        h_box_layout_2.addLayout(v_box_layout_3)

        self.v_box_layout_4 = QtWidgets.QVBoxLayout(self)
        v_box_layout_1.addLayout(self.v_box_layout_4)

        self.v_box_layout_5 = QtWidgets.QVBoxLayout(self)
        v_box_layout_2.addLayout(self.v_box_layout_5)

        self.v_box_layout_6 = QtWidgets.QVBoxLayout(self)
        v_box_layout_3.addLayout(self.v_box_layout_6)

        self.main_layout.addWidget(self.button_2)
        self.main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(self.load_attribute)
        self.button_2.clicked.connect(self.transfer_attribute)

    def load_attribute(self):
        self.button_2.setVisible(1)
        for need_delete_widget in [self.v_box_layout_4,self.v_box_layout_5,self.v_box_layout_6]:
            while need_delete_widget.count():
                item = need_delete_widget.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        self.new_name = []
        self.show_curve = []
        sel = cmds.ls(sl=1)
        self.button_1.setText(sel[0])
        self.attribute = cmds.channelBox('mainChannelBox', q=1, sma=1)
        for at in self.attribute:
            Label_ = QtWidgets.QLabel()
            Label_.setText(at)
            Label_.setMinimumHeight(20)
            self.v_box_layout_4.addWidget(Label_)

            line_edit_a1 = QtWidgets.QLineEdit()
            line_edit_a1.setText(at)
            line_edit_a1.setMinimumHeight(20)
            self.v_box_layout_5.addWidget(line_edit_a1)

            line_edit_a2 = QtWidgets.QLineEdit()
            line_edit_a2.setText(at)
            line_edit_a2.setMinimumHeight(20)
            self.v_box_layout_6.addWidget(line_edit_a2)

            self.new_name.append(line_edit_a1)
            self.show_curve.append(line_edit_a2)
    def transfer_attribute(self):
        for i in range(len(self.new_name)):
            attribute = self.attribute[i]
            new_name = self.new_name[i].text()
            show_curve = self.show_curve[i].text()
            curve = self.others_library.create_str_shape_curve(show_curve)
            print('原名称：'+attribute+'  属性名称：'+new_name+'  样条形状：'+show_curve+'\n')

attribute_window = AttributeWindow()

