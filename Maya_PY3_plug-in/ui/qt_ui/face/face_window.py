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

import zkm_dna_edit_library
from zkm_dna_edit_library import *
importlib.reload(zkm_dna_edit_library)


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

        self.dna_edit_library = DnaEditLibrary()

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

        self.button_4 = QtWidgets.QPushButton('按当前dna创建模型(辅助数据存在则自动添加)')
        self.button_5 = QtWidgets.QPushButton('检查当前模型是否规范(时间)')

        self.button_6 = QtWidgets.QPushButton('按当前dna创建骨骼(没有则创建默认骨骼)')
        self.button_7 = QtWidgets.QPushButton('检查当前骨骼是否规范(时间)')

        self.button_8 = QtWidgets.QPushButton('创建辅助编辑骨骼')
        self.button_9 = QtWidgets.QPushButton('删除辅助骨骼并记录额外偏移数据')
        self.button_10 = QtWidgets.QPushButton('清理骨骼')

        self.Label_3 = QtWidgets.QLabel('权重路径(自动添加缺失骨骼，有则需手动去除):')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_11 = QtWidgets.QPushButton()
        self.button_11.setIcon(QtGui.QIcon(':/fileOpen.png'))
        self.button_12 = QtWidgets.QPushButton('导入权重')
        self.button_13 = QtWidgets.QPushButton('导出权重')

        self.button_14 = QtWidgets.QPushButton('打开不同拓扑传递bs窗口')

        self.button_15 = QtWidgets.QPushButton('按传递结果修改骨骼位置')
        self.button_16 = QtWidgets.QPushButton('骨骼按UV附着表面')
        self.button_17 = QtWidgets.QPushButton('导入bs模型')
        self.button_17.setIcon(QtGui.QIcon(':/fileOpen.png'))

        self.Label_4 = QtWidgets.QLabel('bs名称:')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_18 = QtWidgets.QPushButton('加载')
        self.button_19 = QtWidgets.QPushButton('给bs轮流k帧')
        self.button_20 = QtWidgets.QPushButton('按当前动画烘焙骨骼驱动')


        self.button_21 = QtWidgets.QPushButton('按调整完的驱动烘焙bs')
        self.button_22 = QtWidgets.QPushButton('检查当前骨骼驱动和bs是否完整(暂不提供自定义删改驱动数量)')

        self.Label_5 = QtWidgets.QLabel('输出路径：')
        self.line_edit_5 = QtWidgets.QLineEdit()
        self.button_23 = QtWidgets.QPushButton()
        self.button_23.setIcon(QtGui.QIcon(':/fileOpen.png'))
        self.Label_6 = QtWidgets.QLabel('角色和文件名称：')
        self.line_edit_6 = QtWidgets.QLineEdit()
        self.button_24 = QtWidgets.QPushButton('输出文件')

        self.button_25 = QtWidgets.QPushButton('打开dna读取器')

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

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.Label_2)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_2)
        h_Box_layout_4.setSpacing(1)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.button_3)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_6)
        h_Box_layout_6.addWidget(self.button_4)
        h_Box_layout_6.addWidget(self.button_5)

        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_7)
        h_Box_layout_7.addWidget(self.button_6)
        h_Box_layout_7.addWidget(self.button_7)

        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.button_8)
        h_Box_layout_8.addWidget(self.button_9)
        h_Box_layout_8.addWidget(self.button_10)

        h_Box_layout_9 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_9)
        h_Box_layout_9.addWidget(self.Label_3)
        h_Box_layout_9.addWidget(self.line_edit_3)
        h_Box_layout_9.addWidget(self.button_11)
        h_Box_layout_9.addWidget(self.button_12)
        h_Box_layout_9.addWidget(self.button_13)

        main_layout.addWidget(self.button_14)

        h_Box_layout_10 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_10)
        h_Box_layout_10.addWidget(self.button_15)
        h_Box_layout_10.addWidget(self.button_16)
        h_Box_layout_10.addWidget(self.button_17)

        h_Box_layout_11 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_11)
        h_Box_layout_11.addWidget(self.Label_4)
        h_Box_layout_11.addWidget(self.line_edit_4)
        h_Box_layout_11.addWidget(self.button_18)
        h_Box_layout_11.addWidget(self.button_19)
        h_Box_layout_11.addWidget(self.button_20)

        h_Box_layout_12 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_12)
        h_Box_layout_12.addWidget(self.button_21)
        h_Box_layout_12.addWidget(self.button_22)

        h_Box_layout_13 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_13)
        h_Box_layout_13.addWidget(self.Label_5)
        h_Box_layout_13.addWidget(self.line_edit_5)
        h_Box_layout_13.addWidget(self.button_23)
        h_Box_layout_13.addWidget(self.Label_6)
        h_Box_layout_13.addWidget(self.line_edit_6)
        h_Box_layout_13.addWidget(self.button_24)

        main_layout.addWidget(self.button_25)

        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(self.load_dna)
        self.button_2.clicked.connect(lambda: self.open_file_dialog(self.line_edit_2, 'file',"(*.txt)"))
        self.button_3.clicked.connect(self.help)
        self.button_4.clicked.connect(self.create_model_by_dna)
        self.button_5.clicked.connect(lambda: self.change_button_display(self.button_5, 'model'))
        self.button_6.clicked.connect(self.create_skeleton)
        self.button_7.clicked.connect(lambda: self.change_button_display(self.button_7, 'joint'))
        self.button_8.clicked.connect(self.create_skeleton)
        self.button_9.clicked.connect(self.create_skeleton)
        self.button_10.clicked.connect(self.create_skeleton)
        self.button_22.clicked.connect(lambda: self.change_button_display(self.button_22, 'drver'))
        self.button_23.clicked.connect(lambda: self.open_file_dialog(self.line_edit_5, 'folder', "(*)"))

    # 打开文件选择窗口并将选择赋予给line_edit
    def open_file_dialog(self,line_edit,sel_type,file_type):
        if sel_type == 'file':
            file_path, selected_filter = QtWidgets.QFileDialog.getOpenFileNames(self,"Select File", "", file_type)
            if file_path:
                line_edit.setText(file_path[0])
        if sel_type == 'folder':
            file_path = QtWidgets.QFileDialog.getExistingDirectory(self,"Select File")
            if file_path:
                line_edit.setText(file_path)

    # 加载DNA
    def load_dna(self):
        self.open_file_dialog(self.line_edit_1, 'file', "(*.dna)")
        self.dna_edit_library.load_read(self.line_edit_1.text())
        name = self.dna_edit_library.reader.getName()
        print('你加载的角色名字为：', name)
        self.line_edit_6.setText(name)

    # 按dna数据创建模型
    def create_model_by_dna(self):
        # 设置拓扑
        self.set_topology(mesh_indices, all_topology)
        # 修改点位置、法线、UV坐标
        self.set_point_positions(mesh_indices, vertex_positions, vertex_normals, uv, p_uv_nor_layout)
        print('创建模型')

    # 创建骨骼
    def create_skeleton(self):
        print('创建骨骼')

    # 创建辅助编辑骨骼
    def create_assist_skeleton(self):
        print('创建辅助编辑骨骼')

    # 删除辅助编辑骨骼
    def delete_assist_skeleton(self):
        print('删除辅助编辑骨骼')

    # 复制骨骼并清理dna骨骼
    def copy_skeleton(self):
        print('复制骨骼并清理dna骨骼')

    # 检查当前文件模型数据是否规范
    def check_file_model_data(self):
        num = random.randint(1, 10)
        if num>5:
            return True
        else:
            return False

    # 打开不同拓扑传递bs窗口
    def open_bs_window(self):
        pass

    # 修改按钮显示
    def change_button_display(self, button, query_type):
        if query_type == 'model':
            is_True = self.check_file_model_data()
            if is_True == True:
                now = datetime.now()
                formatted_now = now.strftime("%H:%M:%S")
                button.setText('当前模型已规范('+formatted_now+')')
                button.setStyleSheet('color:rgb(0,0,0);background:rgb(0,255,0)')
            else:
                now = datetime.now()
                formatted_now = now.strftime("%H:%M:%S")
                button.setText('当前模型不规范(' + formatted_now + ')')
                button.setStyleSheet('color:rgb(0,0,0);background:rgb(255,0,0)')
        if query_type == 'joint':
            is_True = self.check_file_model_data()
            if is_True == True:
                now = datetime.now()
                formatted_now = now.strftime("%H:%M:%S")
                button.setText('当前骨骼已规范('+formatted_now+')')
                button.setStyleSheet('color:rgb(0,0,0);background:rgb(0,255,0)')
            else:
                now = datetime.now()
                formatted_now = now.strftime("%H:%M:%S")
                button.setText('当前骨骼不规范(' + formatted_now + ')')
                button.setStyleSheet('color:rgb(0,0,0);background:rgb(255,0,0)')
        if query_type == 'drver':
            is_True = self.check_file_model_data()
            if is_True == True:
                now = datetime.now()
                formatted_now = now.strftime("%H:%M:%S")
                button.setText('当前驱动和bs已规范('+formatted_now+')')
                button.setStyleSheet('color:rgb(0,0,0);background:rgb(0,255,0)')
            else:
                now = datetime.now()
                formatted_now = now.strftime("%H:%M:%S")
                button.setText('当前驱动和bs不规范(' + formatted_now + ')')
                button.setStyleSheet('color:rgb(0,0,0);background:rgb(255,0,0)')

    # 帮助
    def help(self):
        print('help')

window = Window()
if __name__ == '__main__':
    window.show()


# attribute = cmds.channelBox('mainChannelBox', q=1, sma=1)
# print(len(attribute))