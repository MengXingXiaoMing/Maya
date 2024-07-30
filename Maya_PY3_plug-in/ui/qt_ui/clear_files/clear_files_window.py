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

class FlowLayout(QLayout):
    def __init__(self, parent=None, h_spacing=-1, v_spacing=-1, *args, **kwargs):
        super(FlowLayout, self).__init__(parent)
        self._h_spacing = h_spacing
        self._v_spacing = v_spacing

        self.itemList = []

    def __del__(self):
        while self.count():
            self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def smartSpacing(self, pm):
        if not self.parent():
            return -1
        elif isinstance(self.parent(), QWidget):
            return self.parent().style().pixelMetric(pm, None, self.parent())
        else:
            return self.parent().spacing()

    def horizontalSpacing(self):
        return self._h_spacing if self._h_spacing >= 0 else self.smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        return self._v_spacing if self._v_spacing >= 0 else self.smartSpacing(QStyle.PM_LayoutVerticalSpacing)

    def setHorizontalSpacing(self, value):
        self._h_spacing = value

    def setVerticalSpacing(self, value):
        self._v_spacing = value

    def setSpacing(self, value):
        self.setHorizontalSpacing(value)
        self.setVerticalSpacing(value)
        return super().setSpacing(value)

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(
                    QSizePolicy.CheckBox,
                    QSizePolicy.PushButton,
                    Qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton,
                    Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        #self.command = Command()
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('文件清理(Maya'+self.maya_version+')')
        self.create_widgets()
        self.create_layouts()
        self.create_connect()
        self.others_library = OthersLibrary()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version
    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('清理枢轴')
        self.button_2 = QtWidgets.QPushButton('清理所有bs组')
        self.button_3 = QtWidgets.QPushButton('简单模型清理（并不能处理掉所有问题）')
        self.button_4 = QtWidgets.QPushButton('清理动画节点（包括动画层）')

        self.button_5 = QtWidgets.QPushButton('清理显示层')
        self.button_6 = QtWidgets.QPushButton('文件清理')
        self.button_7 = QtWidgets.QPushButton('检查自穿插（需手动修改）')
        self.button_15 = QtWidgets.QPushButton('选择对称点（0.001）')
        self.button_8 = QtWidgets.QPushButton('选择模型中线修复对称')
        self.button_9 = QtWidgets.QPushButton('清理空间名')
        # self.button_10 = QtWidgets.QPushButton('')
        self.button_11 = QtWidgets.QPushButton('清理权重（0.01）')
        self.button_12 = QtWidgets.QPushButton('清理物体点吸附模型后数值为NAN')
        self.button_13 = QtWidgets.QPushButton('清理渲染层（开发中）')
        self.button_14 = QtWidgets.QPushButton('清理渲染层（开发中）')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        scroll_area_1 = QtWidgets.QScrollArea(self)
        scroll_area_1.setWidgetResizable(True)
        scroll_area_1.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area_1.setWidget(QWidget())
        flow_layout_1 = FlowLayout(scroll_area_1.widget())
        flow_layout_1.setSpacing(1)
        flow_layout_1.addWidget(self.button_1)
        flow_layout_1.addWidget(self.button_2)
        flow_layout_1.addWidget(self.button_3)
        flow_layout_1.addWidget(self.button_4)
        flow_layout_1.addWidget(self.button_5)
        flow_layout_1.addWidget(self.button_6)
        flow_layout_1.addWidget(self.button_7)
        flow_layout_1.addWidget(self.button_15)
        flow_layout_1.addWidget(self.button_8)
        flow_layout_1.addWidget(self.button_9)
        # flow_layout_1.addWidget(self.button_10)
        flow_layout_1.addWidget(self.button_11)
        flow_layout_1.addWidget(self.button_12)
        #flow_layout_1.addWidget(self.button_13)

        h_Box_layout_1.addWidget(scroll_area_1)

        # 置顶
        main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(lambda:  self.others_library.cleaning_the_pivot())  # 清理枢轴
        self.button_2.clicked.connect(lambda: self.others_library.clean_up_invalid_BS_groups())  # 清理所有bs和bs组
        self.button_3.clicked.connect(lambda: self.others_library.cleaning_the_model())  # 简单清理模型
        self.button_4.clicked.connect(lambda: self.others_library.cleaning_the_animation_nodes())  # 清理动画节点
        self.button_5.clicked.connect(lambda: self.others_library.cleaning_the_display_layers())  # 清理显示层
        self.button_6.clicked.connect(lambda: self.others_library.cleaning_the_file())  # 文件清理
        self.button_7.clicked.connect(lambda: self.others_library.check_self_intersect())  # 检查自穿插
        self.button_15.clicked.connect(lambda: cmds.select(self.others_library.mirror_point()[2]))  # 选择对称点
        self.button_8.clicked.connect(lambda: self.others_library.fix_symmetry())  # 修复对称
        self.button_9.clicked.connect(lambda: self.others_library.clean_namespace())  # 清理空间名
        self.button_11.clicked.connect(lambda: self.others_library.joint_weight_to_game_specification())  # 清理权重
        self.button_12.clicked.connect(lambda: self.others_library.clean_adsorption_num_nan())  # 清理空间名

    def self_commend(self):
        pass
window = Window()
if __name__ == '__main__':
    window.show()

