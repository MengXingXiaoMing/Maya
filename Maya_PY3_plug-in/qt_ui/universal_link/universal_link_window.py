# -*- coding: utf-8 -*-
import os

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

import inspect



class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('通用链接器(Maya'+self.maya_version+')')
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = self.root_path + '\\' + self.maya_version

        self.namespaces = cmds.namespaceInfo(lon=True, r=True)
        self.namespaces.insert(0, '')
        self.namespaces.remove('UI')
        self.namespaces.remove('shared')
        # print(self.namespaces)

        self.soure = []
        self.link_num = []
        self.target = []

        self.create_widgets()
        self.create_layouts()
        self.create_connect()

        # print(self.soure)
        # print(self.link_num)
        # print(self.target)

    def create_widgets(self):
        # 第一行
        self.label_1 = QtWidgets.QLabel('源')
        self.label_1.setAlignment(Qt.AlignCenter)
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(self.read_file(self.file_path+'\\soure'))
        self.comboBox_4 = QtWidgets.QComboBox()
        self.comboBox_4.addItems(self.namespaces)

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setOrientation(Qt.Vertical)
        self.splitter_1.setFixedWidth(1)
        self.splitter_1.setFrameStyle(1)

        self.label_2 = QtWidgets.QLabel('数值')
        self.label_2.setAlignment(Qt.AlignCenter)
        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.addItems(self.read_file(self.file_path+'\\link_num'))
        self.comboBox_5 = QtWidgets.QComboBox()
        self.comboBox_5.addItems([])

        self.splitter_2 = QtWidgets.QSplitter()
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter_2.setFixedWidth(1)
        self.splitter_2.setFrameStyle(1)

        self.label_3 = QtWidgets.QLabel('目标')
        self.label_3.setAlignment(Qt.AlignCenter)
        self.comboBox_3 = QtWidgets.QComboBox()
        self.comboBox_3.addItems(self.read_file(self.file_path+'\\target'))
        self.comboBox_6 = QtWidgets.QComboBox()
        self.comboBox_6.addItems(self.namespaces)

        self.button_1 = QtWidgets.QPushButton('链接（如果目标或者源缺失则跳过那项）')

        self.button_2 = QtWidgets.QPushButton()
        self.button_2.setIcon(QtGui.QIcon(':/fileNew.png'))

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)


        # 第一行
        scroll_area_4 = QtWidgets.QScrollArea(self)
        scroll_area_4.setWidgetResizable(True)
        scroll_area_4.setFixedHeight(210)
        scroll_area_4.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area_4.setWidget(QWidget())
        scroll_area_4.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area_4)

        widget_0 = QWidget(self)
        widget_0.setContentsMargins(0, 0, 0, 0)
        scroll_area_4.setWidget(widget_0)

        h_Box_layout_1 = QtWidgets.QHBoxLayout(widget_0)
        h_Box_layout_1.setContentsMargins(0, 0, 0, 0)
        h_Box_layout_1.setSpacing(1)
        # main_layout.addLayout(h_Box_layout_1)

        v_Box_layout_1 = QtWidgets.QVBoxLayout()
        h_Box_layout_1.addLayout(v_Box_layout_1)
        v_Box_layout_1.addWidget(self.label_1)
        v_Box_layout_1.addWidget(self.comboBox_1)
        v_Box_layout_1.addWidget(self.comboBox_4)
        h_Box_layout_1.setStretchFactor(v_Box_layout_1, 1)

        h_Box_layout_1.addWidget(self.splitter_1)
        h_Box_layout_1.setStretchFactor(self.splitter_1, 0)

        v_Box_layout_2 = QtWidgets.QVBoxLayout()
        h_Box_layout_1.addLayout(v_Box_layout_2)
        v_Box_layout_2.addWidget(self.label_2)
        v_Box_layout_2.addWidget(self.comboBox_2)
        v_Box_layout_2.addWidget(self.comboBox_5)
        h_Box_layout_1.setStretchFactor(v_Box_layout_2, 1)

        h_Box_layout_1.addWidget(self.splitter_2)
        h_Box_layout_1.setStretchFactor(self.splitter_2, 0)

        v_Box_layout_3 = QtWidgets.QVBoxLayout()
        h_Box_layout_1.addLayout(v_Box_layout_3)
        v_Box_layout_3.addWidget(self.label_3)
        v_Box_layout_3.addWidget(self.comboBox_3)
        v_Box_layout_3.addWidget(self.comboBox_6)
        h_Box_layout_1.setStretchFactor(v_Box_layout_3, 1)
        # h_Box_layout_1.addStretch(1)

        self.v_Box_layout_4 = QtWidgets.QVBoxLayout()
        # scroll_area_1.setWidget(widget_1)
        self.refresh_layout(self.comboBox_1, 'soure',self.v_Box_layout_4)

        self.v_Box_layout_5 = QtWidgets.QVBoxLayout()
        # scroll_area_2.setWidget(widget_2)
        self.refresh_layout(self.comboBox_2, 'link_num',self.v_Box_layout_5)
        self.v_Box_layout_5.addStretch(1)

        self.v_Box_layout_6 = QtWidgets.QVBoxLayout()
        # scroll_area_3.setWidget(widget_3)
        self.refresh_layout(self.comboBox_3, 'target',self.v_Box_layout_6)
        self.v_Box_layout_6.addStretch(1)

        v_Box_layout_1.addLayout(self.v_Box_layout_4)
        v_Box_layout_2.addLayout(self.v_Box_layout_5)
        v_Box_layout_3.addLayout(self.v_Box_layout_6)

        h_Box_layout_2 = QtWidgets.QHBoxLayout()
        main_layout.addLayout(h_Box_layout_2)
        h_Box_layout_2.addWidget(self.button_1)
        h_Box_layout_2.setStretchFactor(self.button_1, 1)
        h_Box_layout_2.addWidget(self.button_2)
        h_Box_layout_2.setStretchFactor(self.button_2, 0)

        main_layout.addStretch(1)

    def create_connect(self):
        self.comboBox_1.currentIndexChanged.connect(lambda :self.refresh_layout(self.comboBox_1, 'soure', self.v_Box_layout_4))
        self.comboBox_2.currentIndexChanged.connect(lambda :self.refresh_layout(self.comboBox_2, 'link_num', self.v_Box_layout_5))
        self.comboBox_3.currentIndexChanged.connect(lambda :self.refresh_layout(self.comboBox_3, 'target', self.v_Box_layout_6))
        self.button_1.clicked.connect(self.link)
        self.button_2.clicked.connect(lambda: os.startfile(r''+self.file_path))
    # 读取文件
    def read_file(self,folder_path):
        all_file = []
        # 遍历文件夹内的所有文件
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                all_file.append(file_name)
        return all_file

    # 读取当前文件内容按行返回
    def read_all_file(self,file_path):
        text_list = []
        # 打开并读取txt文件
        with open(file_path, 'r') as file:
            # 逐行处理
            for line in file:
                # 打印每一行
                text_list.append(line.strip())
        return text_list

    # 删除控件内的所有元素
    def delete_layout_items(self,layout):
        if layout.count():
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self.delete_layout_items(sub_layout)
                        sub_layout.deleteLater()

    # 刷新当前控件
    def refresh_layout(self,layout,add_path,parent):
        self.delete_layout_items(parent)
        file = layout.currentText()
        file_path = self.file_path+'\\'+add_path+'\\'+file
        text = self.read_all_file(file_path)
        if add_path == 'soure':
            self.soure = text
            # print(self.soure)
        elif add_path == 'target':
            self.target = text
            # print(self.target)
        elif add_path == 'link_num':
            self.link_num = text
            # print(self.link_num)
        for i in range(len(text)):
            label_0 = QtWidgets.QLabel('('+str(i)+')')
            label_0.setAlignment(Qt.AlignCenter)
            label_1 = QtWidgets.QLabel(text[i])
            label_1.setAlignment(Qt.AlignCenter)
            h_Box_layout = QtWidgets.QHBoxLayout(self)
            if add_path == 'soure' or add_path == 'link_num':
                h_Box_layout.addStretch(1)
            h_Box_layout.addWidget(label_0)
            if add_path == 'link_num':
                label_0.setVisible(0)
                # h_Box_layout.addStretch(1)
            h_Box_layout.addWidget(label_1)
            if add_path == 'target' or add_path == 'link_num':
                h_Box_layout.addStretch(1)
            parent.addLayout(h_Box_layout)
        parent.addStretch(1)

    # 按目前设置进行链接
    def link(self):
        soure_spacename = self.comboBox_4.currentText()
        target_spacename = self.comboBox_6.currentText()
        self.link_attribute(soure_spacename, self.soure, self.link_num, target_spacename, self.target)

    # 链接属性
    def link_attribute(self,soure_spacename, soure, link_num, target_spacename, target):
        cmds.undoInfo(ock=1)
        if soure_spacename:
            soure_spacename = soure_spacename + ':'
        if target_spacename:
            target_spacename = target_spacename + ':'
        for i in range(len(soure)):
            if i < len(link_num) and i < len(target):
                soure_name = soure_spacename + soure[i]
                target_name = target_spacename + target[i]
                have_soure = cmds.listConnections(target_name, p=1)
                if have_soure:
                    cmds.disconnectAttr(have_soure[0], target_name)
                if cmds.objExists(soure_name) and cmds.objExists(target_name):
                    num_list = link_num[i].split(',')
                    if len(num_list)>1:
                        num = num_list[0].split(':')
                        setRange = cmds.shadingNode('setRange', asUtility=1)
                        cmds.setAttr(setRange + ".oldMinX", float(num[0]))
                        cmds.setAttr(setRange + ".oldMaxX", float(num[1]))
                        num = num_list[1].split(':')
                        cmds.setAttr(setRange + ".minX", float(num[0]))
                        cmds.setAttr(setRange + ".maxX", float(num[1]))
                        cmds.connectAttr(soure_name, (setRange + '.valueX'), force=1)
                        cmds.connectAttr((setRange + '.outValueX'), target_name, force=1)
                    else:
                        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
                        cmds.setAttr(multiplyDivide + ".input2X", float(num_list[0]))
                        cmds.connectAttr(soure_name, (multiplyDivide + '.input1X'), force=1)
                        cmds.connectAttr((multiplyDivide + '.outputX'), target_name, force=1)
        cmds.warning('链接完成')
        cmds.undoInfo(cck=1)
window = Window()
if __name__ == '__main__':
    window.show()
