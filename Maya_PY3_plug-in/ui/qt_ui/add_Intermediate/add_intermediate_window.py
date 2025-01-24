# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
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

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('bs改驱动(Maya' + self.maya_version + ')')

        self.ui_edit = UiEdit()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version

        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    def create_widgets(self):
        # 第一行
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_1 = QtWidgets.QPushButton('加载源（组或者单个模型）')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton('加载bs名称')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_3 = QtWidgets.QPushButton('加载除数字以外的区别')
        self.button_4 = QtWidgets.QPushButton('开始生成')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.setSpacing(1)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.line_edit_1)
        h_Box_layout_3.addWidget(self.button_1)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_2)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.line_edit_3)
        h_Box_layout_5.addWidget(self.button_3)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_6)
        h_Box_layout_6.addWidget(self.button_4)

        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))  # 选择拷贝源按钮
        self.button_3.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))
        self.button_4.clicked.connect(self.create_bs)  # 选择拷贝源按钮

    def create_bs(self):
        base_bs_grp = self.line_edit_1.text()
        bs_name = self.line_edit_2.text()
        specifications = self.line_edit_3.text()
        self.as_specifications_add_bs_intermediate_frame(bs_name, base_bs_grp, specifications)

    def as_specifications_add_bs_intermediate_frame(self, bs_name, base_bs_grp, specifications):
        # 查询按规范对应的bs(末尾数字为000——999，代表0——0.999的bs具体数值)
        cmds.select(base_bs_grp, hierarchy=1)
        BaseMD = cmds.ls(sl=1, type='mesh', long=1)
        AllBsName = cmds.listAttr((bs_name + '.w'), k=True, m=True)
        for i in range(0, len(AllBsName)):
            # 烘焙出对应bs
            for BsNameIntermediateFrame in AllBsName:
                if (AllBsName[i] + specifications) == BsNameIntermediateFrame[:len(AllBsName[i] + specifications)]:
                    num = float(BsNameIntermediateFrame[len(AllBsName[i] + specifications):])
                    while num > 1:
                        num = num / 10.0
                    cmds.setAttr(bs_name + '.' + BsNameIntermediateFrame, 1)
                    cmds.select(base_bs_grp)
                    cmds.duplicate(rr=1)
                    cmds.rename(cmds.ls(sl=1), BsNameIntermediateFrame)
                    sel = cmds.ls(sl=1)
                    cmds.select(sel, hierarchy=1)
                    CopyMD = cmds.ls(sl=1, type='mesh', long=1)
                    # 添加Bs中间帧
                    for j in range(0, len(BaseMD)):
                        cmds.blendShape(bs_name, ibt='absolute', ib=1, e=1, tc=True, t=(BaseMD[j], i, CopyMD[j], num))
                    cmds.setAttr(bs_name + '.' + BsNameIntermediateFrame, 0)
                    cmds.delete(sel)

window = Window()
if __name__ == '__main__':
    window.show()


#删除无影响驱动
