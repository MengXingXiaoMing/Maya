# coding=gbk
import math
import time
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
import os
import inspect
import importlib
import sys

class CustomPlainTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super(CustomPlainTextEdit, self).__init__(parent)

    def keyPressEvent(self, key_event):
        print('Key Pressed:{0}'.format(key_event.text()))

        ctrl = key_event.modifiers() == QtCore.Qt.ControlModifier
        print('ctrl:', ctrl)
        shift = key_event.modifiers() == QtCore.Qt.ShiftModifier
        print('shift:', shift)
        alt = key_event.modifiers() == QtCore.Qt.AltModifier
        print('alt:', alt)

        ctrl_alt = key_event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
        print('ctrl_alt:', ctrl_alt)

        key = key_event.key()
        if key == QtCore.Qt.Key_A:
            print('A key was pressed')
        elif key == QtCore.Qt.Key_Return:
            print('Return key was pressed')
        elif key == QtCore.Qt.Key_Enter:
            print('Enter key was pressed')

        super(CustomPlainTextEdit, self).keyPressEvent(key_event)

    def keyReleaseEvent(self, key_event):
        print('Key Release:{0}'.format(key_event.text()))
        super(CustomPlainTextEdit, self).keyReleaseEvent(key_event)

class MoveableWidget(QtWidgets.QWidget):
    def __init__(self, x, y, width, height, color, parent=None):
        super(MoveableWidget, self).__init__(parent)

        self.setFixedSize(width, height)
        self.move(x, y)

        self.move_color = QtCore.Qt.yellow
        self.color = color
        self.orginal_color = color

        self.move_enabled = False

    def mousePressEvent(self, mouse_event):
        print('Mouse Pressed(选择)')

        self.color = QtCore.Qt.yellow
        if mouse_event.button() == QtCore.Qt.LeftButton and mouse_event.modifiers() == QtCore.Qt.ControlModifier:
            self.initial_pos = self.pos()
            self.global_pos = mouse_event.globalPos()
            self.move_enabled = True



    def mouseReleaseEvent(self, mouse_event):
        print('Mouse Released')
        self.color = self.base_color
        if self.move_enabled:
            self.move_enabled = False


    def mouseDoubleClickEvent(self, mouse_event):
        print('Mouse Double Clicked')

        # if self.color == self.orginal_color:
        #     self.color = QtCore.Qt.yellow
        # else:
        #     self.color = self.orginal_color
        #
        # self.update()

    def mouseMoveEvent(self, mouse_event):
        print('Mouse Moved')

        if self.move_enabled:
            diff = mouse_event.globalPos() - self.global_pos
            self.move(self.initial_pos + diff)

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.fillRect(paint_event.rect(), self.color)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        # maya版本
        self.maya_version = cmds.about(version=True)
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = self.root_path + '\\' + self.maya_version
        # 样条库路径
        self.curve_library_path = self.library_path+ '\curve_library'

        self.setWindowTitle('绳子(Maya'+self.maya_version+')')
        self.create_widgets()
        self.create_layouts()

        self.setMinimumSize(400,400)
        self.test_in_progress = False
    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('进度条')
        self.button_1.clicked.connect(self.run_progress_test)
        self.button_2 = QtWidgets.QPushButton('进度条2')
        self.button_2.clicked.connect(self.run_progress_test2)
        self.button_3 = QtWidgets.QPushButton('创建方块')
        self.button_3.clicked.connect(self.vis_button)

        self.plain_text = CustomPlainTextEdit()

        self.progress_bar = QtWidgets.QProgressBar(self)

        # self.progress_bar.setVisible(0)
        # self.progress_bar.setTextVisible(0)

        self.progress_bar_label = QtWidgets.QLabel('进度：', self)

        # self.progress_bar_label.setVisible(0)
        # self.progress_bar_label.move(10, 10)

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.red_widget = MoveableWidget(10, 10, 24, 24, QtCore.Qt.red, self.central_widget)
        self.blue_widget = MoveableWidget(300, 300, 24, 24, QtCore.Qt.blue, self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)

        # h_Box_layout_1.addWidget(self.button_1)
        # h_Box_layout_1.addWidget(self.button_2)
        # h_Box_layout_1.addWidget(self.button_3)
        # main_layout.addWidget(self.progress_bar_label)
        # main_layout.addWidget(self.progress_bar)
        #
        # main_layout.addWidget(self.plain_text)
    def run_progress_test(self):
        number_of_operations = 50

        progress_dialog = QtWidgets.QProgressDialog("Running test...", "Cancel", 0, number_of_operations, self)
        progress_dialog.setWindowTitle("Progress Dialog Test")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()

        QtCore.QCoreApplication.processEvents()

        for i in range(1, number_of_operations + 1):
            progress_dialog.setLabelText("Operation " + str(i) + " of " + str(number_of_operations))
            progress_dialog.setValue(i)
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()

        progress_dialog.close()
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.setMinimumDuration(1)

    def run_progress_test2(self):
        if self.test_in_progress:
            return
        number_of_operation = 30
        self.progress_bar.setRange(0, number_of_operation)
        self.progress_bar.setVisible(1)
        self.progress_bar_label.setVisible(1)
        self.progress_bar_label.setText("Operation 0 of " + str(number_of_operation))
        self.test_in_progress = True
        # self.update_visibility()
        for i in range(1, number_of_operation + 1):
            if not self.test_in_progress:
                break
            self.progress_bar_label.setText("进度： " + str(i) + " → " + str(number_of_operation))
            self.progress_bar.setValue(i)
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
        # self.progress_bar.setVisible(0)
        self.test_in_progress = False

    def vis_button(self):
        vis = self.button_1.isVisible()
        print(vis)
        if vis == True:
            self.button_1.setVisible(0)
        else:
            self.button_1.setVisible(1)
        cmds.polySphere()





window = Window()
if __name__ == '__main__':
    window.show()








