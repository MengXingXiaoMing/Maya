# -*- coding: utf-8 -*-
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

import importlib
import controller_processing_window_command
importlib.reload(controller_processing_window_command)
from controller_processing_window_command import *


class FlowLayout(QLayout):
    # this is for 陈逆
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
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        self.file_path_reverse = '/'.join(self.file_path.split('\\'))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = self.root_path + '\\' + self.maya_version
        self.library_path_reverse = '/'.join(self.library_path.split('\\'))

        self.command = Command()
        # self.curve_list = self.command.curve_list()
        # self.button_num = len(self.curve_list)
        self.columns_num = 6
        self.new_button = []
        self.curve_library_path = self.library_path + '\\curve_library\\'
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('控制器处理(Maya'+self.maya_version+')')
        self.setMinimumWidth(50*self.columns_num+30)
        self.height = 740
        self.setMinimumHeight(self.height)

        self.create_widgets()
        self.create_layouts()
        self.create_controller()
        self.create_connect()
    def create_widgets(self):
        # 总模块
        self.scroll_bar_1 = QtWidgets.QScrollBar()
        #height = self.layout_widget.geometry().height()
        # 第一行
        self.Label_1 = QtWidgets.QLabel()
        self.Label_1.setText('控制器大小:')
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.line_edit_1.setFixedWidth(60)
        self.line_edit_1.setText('1.00')
        self.slider_1 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_1.setMinimum(0)
        self.slider_1.setMaximum(200)
        self.slider_1.setValue(100)
        self.button_1 = QtWidgets.QPushButton('缩放至软选择大小')
        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        # 第二行
        self.Label_2 = QtWidgets.QLabel()
        self.Label_2.setFixedWidth(25)
        self.Label_2.setText('轴向:')
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(['X', 'Y', 'Z'])
        self.button_2 = QtWidgets.QPushButton('旋转')
        self.button_3 = QtWidgets.QPushButton('去重名')

        self.splitter_2 = QtWidgets.QSplitter()
        self.splitter_2.setFixedHeight(1)
        self.splitter_2.setFrameStyle(1)

        # 第三行
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_4 = QtWidgets.QPushButton('填写名称上传样条')
        self.scroll_bar_2 = QtWidgets.QScrollBar()


        self.splitter_3 = QtWidgets.QSplitter()
        self.splitter_3.setFixedHeight(1)
        self.splitter_3.setFrameStyle(1)

        # 第四行
        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.addItems(['Index', 'RGB'])
        self.color_button_1 = QtWidgets.QPushButton()
        self.color_button_1.setStyleSheet('background:rgb(100,220,255)')
        self.color_dialog_1 = QtWidgets.QColorDialog()
        self.slider_2 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_2.setMinimum(0)
        self.slider_2.setMaximum(31)
        self.slider_2.setValue(18)
        self.splitter_4 = QtWidgets.QSplitter()
        self.splitter_4.setFixedHeight(1)
        self.splitter_4.setFrameStyle(1)

        # 第五行
        self.Label_3 = QtWidgets.QLabel()
        self.Label_3.setText('骨骼大小:')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.line_edit_3.setText('0.01')
        self.line_edit_3.setFixedWidth(60)
        self.slider_3 = QtWidgets.QSlider(Qt.Horizontal)
        self.Label_4 = QtWidgets.QLabel()
        self.Label_4.setText('控制器组数:')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.line_edit_4.setFixedWidth(60)
        self.line_edit_4.setText('2')
        self.slider_4 = QtWidgets.QSlider(Qt.Horizontal)
        self.checkBox_1 = QtWidgets.QCheckBox()
        self.checkBox_1.setChecked(True)
        self.checkBox_1.setText('忽略末端骨骼')
        self.checkBox_2 = QtWidgets.QCheckBox()
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setText('提取约束')

        self.Label_5 = QtWidgets.QLabel()
        self.Label_5.setText('后缀:')
        self.line_edit_5 = QtWidgets.QLineEdit()
        self.button_5 = QtWidgets.QPushButton('独立创建控制器')
        self.button_5.setStyleSheet('background:rgb(0,0,255)')

        self.comboBox_3 = QtWidgets.QComboBox()
        self.comboBox_3.addItems(self.command.common.load_file_fame_of_the_corresponding_suffix((r'' + self.file_path + '\maya_file'), 1, '.ma'))
        self.button_6 = QtWidgets.QPushButton('导入')
        # self.button_6.setFixedWidth(30)
        self.button_7 = QtWidgets.QPushButton()
        self.button_7.setFixedWidth(30)
        self.button_7.setIcon(QtGui.QIcon(':/fileNew.png'))

        self.comboBox_4 = QtWidgets.QComboBox()
        self.comboBox_4.addItems(['hand', 'tail', 'foot'])
        self.button_8 = QtWidgets.QPushButton('创建(停用)')
        self.comboBox_5 = QtWidgets.QComboBox()
        self.comboBox_5.addItems(['NoMirror'])#['IK', 'NoMirror', 'aim', 'twist', 'global', 'rope']
        self.button_9 = QtWidgets.QPushButton('删/增属性')

        self.button_10 = QtWidgets.QPushButton('切换')
        self.button_10.setStyleSheet('color:rgb(0,0,0);background:rgb(255,255,0)')
        self.button_11 = QtWidgets.QPushButton('归位')
        self.button_11.setStyleSheet('color:rgb(0,0,0);background:rgb(0,255,0)')
        self.checkBox_4 = QtWidgets.QCheckBox()
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setText('保持样条形状')
        self.button_12 = QtWidgets.QPushButton('创建控制器')
        self.button_12.setStyleSheet('color:rgb(0,0,0);background:rgb(255,0,0)')

        self.splitter_5 = QtWidgets.QSplitter()
        self.splitter_5.setFixedHeight(1)
        self.splitter_5.setFrameStyle(1)

        # 第六行
        self.button_13 = QtWidgets.QPushButton('所选中心创建骨骼')
        self.radio_button_1 = QRadioButton()
        self.radio_button_1.setChecked(1)
        self.radio_button_1.move(0, 0)
        self.radio_button_1.setText('X')
        self.radio_button_2 = QRadioButton()
        self.radio_button_2.move(0, 20)
        self.radio_button_2.setText('Y')
        self.radio_button_3 = QRadioButton()
        self.radio_button_3.move(0, 40)
        self.radio_button_3.setText('Z')
        self.button_14 = QtWidgets.QPushButton('镜像骨骼')

        self.line_edit_6 = QtWidgets.QLineEdit()
        self.line_edit_6.setFixedWidth(40)
        self.line_edit_6.setText('2')
        self.slider_5 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_5.setMinimum(2)
        self.slider_5.setMaximum(10)
        self.button_15 = QtWidgets.QPushButton('选择样条创建骨骼')

        self.button_16 = QtWidgets.QPushButton('选择线在中心创建骨骼链')
        self.button_17 = QtWidgets.QPushButton('骨骼转样条')
        self.button_18 = QtWidgets.QPushButton('反转骨骼层次（单链）')
        self.button_33 = QtWidgets.QPushButton('自动父化')
        self.button_19 = QtWidgets.QPushButton('选择样条打印其生成命令')
        self.button_20 = QtWidgets.QPushButton('显影轴向')
        self.button_21 = QtWidgets.QPushButton('显隐骨骼')
        self.button_22 = QtWidgets.QPushButton('隐藏并锁定选择属性')
        self.button_23 = QtWidgets.QPushButton('显示默认属性')

        self.button_24 = QtWidgets.QPushButton('上移自定义的属性')
        self.button_25 = QtWidgets.QPushButton('下移自定义属性属性')

        self.line_edit_7 = QtWidgets.QLineEdit()
        self.button_26 = QtWidgets.QPushButton('替换选择默认属性名称')

        self.line_edit_8 = QtWidgets.QLineEdit()
        self.line_edit_8.setFixedWidth(40)
        self.line_edit_8.setText('2')
        self.slider_6 = QtWidgets.QSlider(Qt.Horizontal)
        self.button_27 = QtWidgets.QPushButton('隔行选线')
        self.button_28 = QtWidgets.QPushButton('隔行选循环边')

        self.line_edit_9 = QtWidgets.QLineEdit()
        self.line_edit_9.setFixedWidth(40)
        self.line_edit_9.setText('2')
        self.slider_7 = QtWidgets.QSlider(Qt.Horizontal)
        self.button_29 = QtWidgets.QPushButton('插入骨骼')

        self.Label_6 = QtWidgets.QLabel()
        self.Label_6.setText('加载毛囊附着模型')
        self.line_edit_10 = QtWidgets.QLineEdit()
        self.button_30 = QtWidgets.QPushButton('加载')
        self.checkBox_3 = QtWidgets.QCheckBox()
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setText('保持原位（父对象约束）')
        self.button_31 = QtWidgets.QPushButton('毛囊附着')

        self.button_32 = QtWidgets.QPushButton('清理无变化驱动')
        self.button_34 = QtWidgets.QPushButton('打直所有驱动')

        self.splitter_6 = QtWidgets.QSplitter()
        self.splitter_6.setFixedHeight(1)
        self.splitter_6.setFrameStyle(1)

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)
        self.main_layout.addStretch(1)

        # 总模块
        self.layout_widget = QWidget(self)
        v_box_layout_1 = QtWidgets.QVBoxLayout(self.layout_widget)
        v_box_layout_1.setContentsMargins(0, 0, 0, 0)
        self.layout_widget.setGeometry(0, 0, 360, 900)

        v_box_layout_1.setSpacing(1)
        # self.main_layout.addWidget(self.scroll_bar_1)

        # 第一行
        h_box_layout_2 = QtWidgets.QHBoxLayout(self)
        v_box_layout_1.addLayout(h_box_layout_2)
        h_box_layout_2.addWidget(self.Label_1)
        h_box_layout_2.addWidget(self.line_edit_1)
        h_box_layout_2.addWidget(self.slider_1)
        h_box_layout_2.addWidget(self.button_1)

        v_box_layout_1.addWidget(self.splitter_1)


        # 第二行
        h_box_layout_3 = QtWidgets.QHBoxLayout(self)
        v_box_layout_1.addLayout(h_box_layout_3)
        h_box_layout_3.addWidget(self.Label_2)
        h_box_layout_3.addWidget(self.comboBox_1)
        h_box_layout_3.addWidget(self.button_2)
        h_box_layout_3.addWidget(self.button_3)

        v_box_layout_1.addWidget(self.splitter_2)

        # 第三行
        v_box_layout_2 = QtWidgets.QVBoxLayout(self)
        v_box_layout_1.addLayout(v_box_layout_2)
        h_box_layout_4 = QtWidgets.QHBoxLayout(self)
        v_box_layout_2.addLayout(h_box_layout_4)
        h_box_layout_4.addWidget(self.line_edit_2)
        h_box_layout_4.addWidget(self.button_4)

        self.h_box_layout_5 = QtWidgets.QHBoxLayout(self)
        v_box_layout_2.addLayout(self.h_box_layout_5)
        v_box_layout_2.addStretch(1)
        # 添加控制器位置

        v_box_layout_1.addWidget(self.splitter_3)

        # 第四行
        h_box_layout_6 = QtWidgets.QHBoxLayout(self)
        v_box_layout_1.addLayout(h_box_layout_6)
        h_box_layout_6.addWidget(self.comboBox_2)
        h_box_layout_6.addWidget(self.color_button_1)
        h_box_layout_6.addWidget(self.slider_2)
        self.color_button_1.setContextMenuPolicy(Qt.CustomContextMenu)
        v_box_layout_1.addWidget(self.splitter_4)

        # 第五行
        v_box_layout_3 = QtWidgets.QVBoxLayout(self)
        v_box_layout_1.addLayout(v_box_layout_3)

        h_box_layout_7 = QtWidgets.QHBoxLayout(self)
        v_box_layout_3.addLayout(h_box_layout_7)
        h_box_layout_7.addWidget(self.Label_3)
        h_box_layout_7.addWidget(self.line_edit_3)
        h_box_layout_7.addWidget(self.slider_3)
        h_box_layout_7.addWidget(self.Label_4)
        h_box_layout_7.addWidget(self.line_edit_4)
        h_box_layout_7.addWidget(self.slider_4)

        h_box_layout_8 = QtWidgets.QHBoxLayout(self)
        v_box_layout_3.addLayout(h_box_layout_8)
        h_box_layout_8.addWidget(self.checkBox_1)
        h_box_layout_8.addWidget(self.checkBox_2)
        h_box_layout_8.addWidget(self.Label_5)
        h_box_layout_8.addWidget(self.line_edit_5)
        h_box_layout_8.addWidget(self.button_5)

        h_box_layout_9 = QtWidgets.QHBoxLayout(self)
        v_box_layout_3.addLayout(h_box_layout_9)
        h_box_layout_9.addWidget(self.comboBox_3)
        h_box_layout_9.addWidget(self.button_6)
        h_box_layout_9.addWidget(self.button_7)

        h_box_layout_10 = QtWidgets.QHBoxLayout(self)
        v_box_layout_3.addLayout(h_box_layout_10)
        h_box_layout_10.addWidget(self.comboBox_4)
        h_box_layout_10.addWidget(self.button_8)
        h_box_layout_10.addWidget(self.comboBox_5)
        h_box_layout_10.addWidget(self.button_9)

        h_box_layout_11 = QtWidgets.QHBoxLayout(self)
        v_box_layout_3.addLayout(h_box_layout_11)
        h_box_layout_11.addWidget(self.button_10)
        h_box_layout_11.addWidget(self.button_11)
        h_box_layout_11.addWidget(self.checkBox_4)
        h_box_layout_11.addWidget(self.button_12)

        v_box_layout_1.addWidget(self.splitter_5)

        # 第六行
        v_box_layout_11 = QtWidgets.QVBoxLayout(self)
        v_box_layout_1.addLayout(v_box_layout_11)

        scroll_area_2 = QtWidgets.QScrollArea(self)
        scroll_area_2.setWidgetResizable(True)
        scroll_area_2.setFixedHeight(200)
        scroll_area_2.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area_2.setWidget(QWidget())
        v_box_layout_11.addWidget(scroll_area_2)
        flow_layout_2 = FlowLayout(scroll_area_2.widget())
        flow_layout_2.setSpacing(1)
        flow_layout_2.addWidget(self.button_13)
        widget_1 = QWidget(self)
        radio_button_h_box_layout_1 = QtWidgets.QHBoxLayout(widget_1)  # 创建一个按钮组
        radio_button_h_box_layout_1.setContentsMargins(0,0,0,0)
        flow_layout_2.addWidget(widget_1)
        radio_button_h_box_layout_1.addWidget(self.radio_button_1, 0)  # 将单选按钮添加到按钮组，组成单选组。
        radio_button_h_box_layout_1.addWidget(self.radio_button_2, 1)
        radio_button_h_box_layout_1.addWidget(self.radio_button_3, 2)
        radio_button_h_box_layout_1.addWidget(self.button_14)

        widget_2 = QWidget(self)
        h_box_layout_18 = QtWidgets.QHBoxLayout(widget_2)
        h_box_layout_18.setSpacing(0)
        h_box_layout_18.setContentsMargins(0, 0, 0, 0)
        flow_layout_2.addWidget(widget_2)
        h_box_layout_18.addWidget(self.line_edit_6)
        h_box_layout_18.addWidget(self.slider_5)
        h_box_layout_18.addWidget(self.button_15)

        flow_layout_2.addWidget(self.button_16)
        flow_layout_2.addWidget(self.button_17)
        flow_layout_2.addWidget(self.button_18)
        flow_layout_2.addWidget(self.button_33)
        flow_layout_2.addWidget(self.button_19)
        flow_layout_2.addWidget(self.button_20)
        flow_layout_2.addWidget(self.button_21)
        flow_layout_2.addWidget(self.button_22)
        flow_layout_2.addWidget(self.button_23)

        widget_3 = QWidget(self)
        h_box_layout_12 = QtWidgets.QHBoxLayout(widget_3)
        h_box_layout_12.setSpacing(0)
        h_box_layout_12.setContentsMargins(0, 0, 0, 0)
        flow_layout_2.addWidget(widget_3)
        h_box_layout_12.addWidget(self.button_24)
        h_box_layout_12.addWidget(self.button_25)

        widget_2 = QWidget(self)
        h_box_layout_13 = QtWidgets.QHBoxLayout(widget_2)
        h_box_layout_13.setSpacing(0)
        h_box_layout_13.setContentsMargins(0, 0, 0, 0)
        flow_layout_2.addWidget(widget_2)
        h_box_layout_13.addWidget(self.line_edit_7)
        h_box_layout_13.addWidget(self.button_26)

        widget_4 = QWidget(self)
        h_box_layout_14 = QtWidgets.QHBoxLayout(widget_4)
        h_box_layout_14.setSpacing(0)
        h_box_layout_14.setContentsMargins(0, 0, 0, 0)
        flow_layout_2.addWidget(widget_4)
        h_box_layout_14.addWidget(self.line_edit_8)
        h_box_layout_14.addWidget(self.slider_6)
        h_box_layout_14.addWidget(self.button_27)
        h_box_layout_14.addWidget(self.button_28)

        widget_5 = QWidget(self)
        h_box_layout_15 = QtWidgets.QHBoxLayout(widget_5)
        h_box_layout_15.setSpacing(0)
        h_box_layout_15.setContentsMargins(0, 0, 0, 0)
        flow_layout_2.addWidget(widget_5)
        h_box_layout_15.addWidget(self.line_edit_9)
        h_box_layout_15.addWidget(self.slider_7)
        h_box_layout_15.addWidget(self.button_29)

        widget_6 = QWidget(self)
        v_box_layout_12 = QtWidgets.QVBoxLayout(widget_6)
        v_box_layout_12.setSpacing(0)
        v_box_layout_12.setContentsMargins(0, 0, 0, 0)
        flow_layout_2.addWidget(widget_6)
        h_box_layout_16 = QtWidgets.QHBoxLayout(self)
        v_box_layout_12.addLayout(h_box_layout_16)
        h_box_layout_16.addWidget(self.Label_6)
        h_box_layout_16.addWidget(self.line_edit_10)
        h_box_layout_16.addWidget(self.button_30)
        h_box_layout_17 = QtWidgets.QHBoxLayout(self)
        v_box_layout_12.addLayout(h_box_layout_17)
        h_box_layout_17.addWidget(self.checkBox_3)
        h_box_layout_17.addWidget(self.button_31)
        flow_layout_2.addWidget(self.button_32)
        flow_layout_2.addWidget(self.button_34)

        v_box_layout_1.addWidget(self.splitter_6)
        # 置顶
        v_box_layout_1.addStretch(1)

    def create_connect(self):
        self.scroll_bar_1.valueChanged.connect(self.automatically_adjust_layout)

        self.line_edit_1.textChanged.connect(lambda: self.modify_UI_values_and_provide_feedback_to_the_slider_1(self.line_edit_1,self.slider_1))  # 修改ui数值反馈给滑块
        self.slider_1.valueChanged.connect(lambda: self.automatically_adjust_the_slider_range_and_return_values_to_ui_1(self.slider_1,self.line_edit_1))  # 自动调整ui范围
        self.button_1.clicked.connect(lambda: self.command.controller.modify_vontroller_shape('SoftSelectionSize', 1, 1, 1))
        self.button_2.clicked.connect(lambda: self.command.controller.rotation_controller(self.comboBox_1.currentText()))
        self.button_3.clicked.connect(self.command.others_library.remove_duplicate_name)
        self.button_4.clicked.connect(self.add_controller)
        self.button_5.clicked.connect(self.independently_creating_controllers)
        self.button_6.clicked.connect(lambda: self.command.common.import_export_file(self.comboBox_3.currentText()[:-3],(r''+ self.file_path_reverse + '/maya_file'),1,'mayaAscii'))
        self.button_7.clicked.connect(lambda: os.startfile(r''+self.file_path + '\maya_file'))
        self.comboBox_2.currentIndexChanged.connect(self.show_or_hide)
        self.slider_2.valueChanged.connect(lambda: self.command.drag_slider_automatically_modify_color_panel(self.slider_2.value(),self.color_button_1))

        self.line_edit_3.textChanged.connect(lambda: self.modify_UI_values_and_provide_feedback_to_the_slider_1(self.line_edit_3,self.slider_3))  # 修改ui数值反馈给滑块
        self.line_edit_3.textChanged.connect(self.scale_joint)
        self.slider_3.valueChanged.connect(lambda: self.automatically_adjust_the_slider_range_and_return_values_to_ui_1(self.slider_3,self.line_edit_3))  # 自动调整ui范围

        self.line_edit_4.textChanged.connect(lambda: self.modify_UI_values_and_provide_feedback_to_the_slider(self.line_edit_4,self.slider_4))  # 修改ui数值反馈给滑块
        self.slider_4.valueChanged.connect(lambda: self.automatically_adjust_the_slider_range_and_return_values_to_ui(self.slider_4,self.line_edit_4))  # 自动调整ui范围

        self.color_button_1.customContextMenuRequested.connect(partial(self.modify_color, self.color_button_1))
        self.color_button_1.clicked.connect(self.change_color)

        self.line_edit_6.textChanged.connect(lambda: self.modify_UI_values_and_provide_feedback_to_the_slider(self.line_edit_6,self.slider_5))  # 修改ui数值反馈给滑块
        self.slider_5.valueChanged.connect(lambda: self.automatically_adjust_the_slider_range_and_return_values_to_ui(self.slider_5,self.line_edit_6))  # 自动调整ui范围

        #self.button_8.clicked.connect(lambda:  self.command.controller.addattr_system(self.comboBox_4.currentText()))  # 创建控制器
        self.button_9.clicked.connect(lambda:  self.command.controller.delete_addattr_system(self.comboBox_5.currentText()))  # 删除控制器
        self.button_10.clicked.connect(self.command.controller.switch_controllers)  # 切换控制器
        self.button_11.clicked.connect(self.command.controller.reset_controllers)  # 归零控制器
        self.button_12.clicked.connect(self.creating_controllers_system) # 创建控制器
        self.button_13.clicked.connect(self.command.others_library.centre_joint) # 在所选线中心建立骨骼链
        self.button_14.clicked.connect(self.mirror_joint)  # 镜像骨骼
        self.button_15.clicked.connect(self.select_curve_create_joint)
        self.button_16.clicked.connect(self.command.others_library.establishing_a_bone_chain_at_the_midline)
        self.button_17.clicked.connect(self.command.others_library.joint_transformation_curve)
        self.button_18.clicked.connect(self.command.others_library.reversa_arrangement)
        self.button_33.clicked.connect(self.command.others_library.automatic_parenting)
        self.button_19.clicked.connect(lambda:  print(self.command.curve.return_curve_command(cmds.ls(sl=1))))
        self.button_20.clicked.connect(self.command.others_library.show_hide_axial)
        self.button_21.clicked.connect(self.command.others_library.set_bone_display)
        self.button_22.clicked.connect(self.command.others_library.hide_selection_properties)
        self.button_23.clicked.connect(self.command.others_library.show_default_properties)
        self.button_24.clicked.connect(lambda: self.command.others_library.get_move_up_dn_attrs_proc(1,[]))
        self.button_25.clicked.connect(lambda: self.command.others_library.get_move_up_dn_attrs_proc(0,[]))
        self.button_26.clicked.connect(lambda: self.command.others_library.modify_default_attribute_names(self.line_edit_7.text()))

        self.line_edit_8.textChanged.connect(lambda: self.modify_UI_values_and_provide_feedback_to_the_slider(self.line_edit_8,self.slider_6))  # 修改ui数值反馈给滑块
        self.slider_6.valueChanged.connect(lambda: self.automatically_adjust_the_slider_range_and_return_values_to_ui(self.slider_6,self.line_edit_8))  # 自动调整ui范围
        self.button_27.clicked.connect(lambda: self.command.others_library.interlaced_line_selection(1,self.line_edit_8.text()))
        self.button_28.clicked.connect(lambda: self.command.others_library.interlaced_line_selection(0, self.line_edit_8.text()))

        self.line_edit_9.textChanged.connect(lambda: self.modify_UI_values_and_provide_feedback_to_the_slider(self.line_edit_9,self.slider_7))  # 修改ui数值反馈给滑块
        self.slider_7.valueChanged.connect(lambda: self.automatically_adjust_the_slider_range_and_return_values_to_ui(self.slider_7,self.line_edit_9))
        self.button_29.clicked.connect(lambda: self.command.others_library.insert_joint(self.line_edit_9.text()))

        self.button_30.clicked.connect(lambda: self.command.ui_edit.load_select_for_ui_text(self.line_edit_10, ['QLineEdit']))
        self.button_31.clicked.connect(lambda: self.command.others_library.follicle_constraint(self.line_edit_10.text(),cmds.ls(sl=1),self.checkBox_3.isChecked()))
        #self.button_32.clicked.connect(lambda: self.open_attribute_visibility_window())
        #self.button_34.clicked.connect(lambda: self.open_attribute_visibility_window())

    # 修改控制器栏宽度
    def resizeEvent(self, event):
        # 窗口大小
        self.new_size = event.size()
        move = self.layout_widget.geometry()
        self.layout_widget.setGeometry(move.x(), move.y(), (self.new_size.width()), move.height())
    # 自动调整控制器栏横向宽度
    def automatically_adjust_layout(self):
        num = self.scroll_bar_1.value()
        move = self.layout_widget.geometry()
        self.layout_widget.setGeometry(0, (num*-1), (self.new_size.width()), (900+(num*1)))
    # 右键处理控制器
    def edit_controller(self,button, point):
        # show context menu
        # create context menu
        self.popMenu = QMenu(self)
        create = self.popMenu.addAction('创建')
        modify = self.popMenu.addAction('修改')
        self.popMenu.addSeparator()
        delete = self.popMenu.addAction('删除')

        create.triggered.connect(partial(self.create_curve, button))
        modify.triggered.connect(partial(self.modify_curve, button))
        delete.triggered.connect(partial(self.delete_curve, button))
        self.popMenu.exec_(button.mapToGlobal(point))

    # 自动调整滑块范围且返回数值给ui
    def automatically_adjust_the_slider_range_and_return_values_to_ui_1(self, soure_ui, target_ui):
        soure_ui_type = 'QSlider'
        num = self.command.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(soure_ui,soure_ui_type)
        target_ui.setText(str(num/100))
        soure_ui.setMinimum(0)
        max_num = soure_ui.maximum()
        if max_num > 1000:
            soure_ui.setMaximum(1000)

    # 修改ui数值反馈给滑块
    def modify_UI_values_and_provide_feedback_to_the_slider_1(self, soure_ui, target_ui):
        num = soure_ui.text()
        num = float(num)
        target_ui_type = 'QSlider'
        target_ui.setValue(num * 100)
        self.command.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(target_ui, target_ui_type)
        sel = cmds.ls(sl=1)
        if sel:
            self.command.controller.modify_vontroller_shape('scale',num,num,num)

    # 创建样条
    def create_curve(self,button):
        self.command.curve.create_curve(self.library_path+'\\curve_library',button.text())
    # 修改样条
    def modify_curve(self,button):
        palette = self.color_button_1.palette()
        background_color = palette.color(self.color_button_1.backgroundRole())
        colour = background_color.getRgbF()
        self.command.controller.as_swap_curve(self.comboBox_2.currentText(),button.text(),colour,self.slider_2.value())
    # 删除样条
    def delete_curve(self,button):
        button.deleteLater()
        os.remove(self.library_path+'\\curve_library\\'+button.text()+'.txt')
        os.remove(self.library_path+'\\curve_library\\'+button.text()+'.jpg')
        print('删除：'+button.text())
    # 修改按钮颜色
    def modify_color(self,button, point):
        text = self.comboBox_2.currentText()
        if text == 'RGB':
            colour = self.color_dialog_1.getColor()
            self.color_button_1.setStyleSheet("QWidget { background-color: %s }"%colour.name())
            palette = self.color_button_1.palette()
            background_color = palette.color(self.color_button_1.backgroundRole())
            # print(background_color.getRgbF())
            # print(background_color.getRgb())

    # 修改颜色滑块显示
    def show_or_hide(self):
        text = self.comboBox_2.currentText()
        if text == 'RGB':
            self.slider_2.setVisible(0)
        else:
            self.slider_2.setVisible(1)

    # 修改控制器颜色
    def change_color(self):
        text = self.comboBox_2.currentText()
        palette = self.color_button_1.palette()
        background_color = palette.color(self.color_button_1.backgroundRole())
        sel = cmds.ls(sl=1)
        curve = []
        for s in sel:
            shape = cmds.listRelatives(s, s=1, type='nurbsCurve')
            if shape:
                curve.append(s)
        colour = background_color.getRgbF()
        num = self.slider_2.value()

        self.command.curve.change_curve_color(text,curve,[colour[0],colour[1],colour[2]],num)

    # 缩放骨骼
    def scale_joint(self):
        cmds.jointDisplayScale(float(self.line_edit_3.text()))

    # 镜像骨骼
    def mirror_joint(self):
        if self.radio_button_1.isChecked():
            self.command.others_library.mirror_joint('X')
        if self.radio_button_2.isChecked():
            self.command.others_library.mirror_joint('Y')
        if self.radio_button_3.isChecked():
            self.command.others_library.mirror_joint('Z')

    # 选择样条创建骨骼
    def select_curve_create_joint(self):
        joint_num = self.slider_5.value()
        self.command.others_library.generate_bone_chain(joint_num)

    # 自动调整滑块范围且返回数值给ui
    def automatically_adjust_the_slider_range_and_return_values_to_ui(self,soure_ui, target_ui):
        soure_ui_type = 'QSlider'
        num = self.command.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(soure_ui, soure_ui_type)
        target_ui.setText(str(num))
        soure_ui.setMinimum(1)
        max_num = soure_ui.maximum()
        if max_num > 10000:
            soure_ui.setMaximum(10000)

    # 修改ui数值反馈给滑块
    def modify_UI_values_and_provide_feedback_to_the_slider(self,soure_ui, target_ui):
        num = soure_ui.text()
        num = float(num)
        target_ui_type = 'QSlider'
        target_ui.setValue(num)
        self.command.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(target_ui, target_ui_type)

    # 打开属性可视化窗口
    def open_attribute_visualization(self):
        pass

    # 独立创建控制器
    def independently_creating_controllers(self):
        controller_group_num = int(self.line_edit_4.text())
        suffix = self.line_edit_5.text()
        if_remove_joint = self.checkBox_1.isChecked()
        extract_constraints = self.checkBox_2.isChecked()
        self.command.controller.old_create_fk(controller_group_num, suffix, if_remove_joint, extract_constraints)

    # 创建控制器系统
    def creating_controllers_system(self):
        # 控制器组数量
        controller_group_num = int(self.line_edit_4.text())
        # 后缀
        suffix = self.line_edit_5.text()
        # 是否移除末端
        if_remove_joint = self.checkBox_1.isChecked()
        # 是否保持控制器形状
        keep_curve_shape = self.checkBox_4.isChecked()
        # 开始创建控制器系统
        self.command.controller.create_controllers_system(controller_group_num, suffix, if_remove_joint,  keep_curve_shape)

    # 打开属性可视化窗口
    def open_attribute_visibility_window(self):
        import attribute_visualization
        importlib.reload(attribute_visualization)
        attribute_visualization.attribute_window.show()

    # 添加控制器
    def add_controller(self):
        self.command.curve.upload_file_by_name(self.line_edit_2.text(), self.library_path_reverse + '/curve_library')
        self.scroll_area_1.deleteLater()
        self.create_controller()

    # 创建控制器
    def create_controller(self):
        self.scroll_area_1 = QtWidgets.QScrollArea(self)
        # self.scroll_area_1.setFixedHeight(400)

        self.scroll_area_1.setWidgetResizable(True)
        self.scroll_area_1.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area_1.setWidget(QWidget())

        self.h_box_layout_5.addWidget(self.scroll_area_1)

        flow_layout_1 = FlowLayout(self.scroll_area_1.widget())
        flow_layout_1.setSpacing(0)

        self.curve_list = self.command.curve_list()
        self.button_num = len(self.curve_list)

        for i in range(self.button_num):
            button = QtWidgets.QToolButton(self)
            button.setAutoRaise(True)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setText(self.curve_list[i])
            # button.setFixedSize(50, 65)
            button.setIcon(QIcon((self.curve_library_path + self.curve_list[i] + '.jpg')))
            button.setIconSize(QSize(50, 50))
            # set button context menu policy
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(partial(self.edit_controller, button))
            flow_layout_1.addWidget(button)
window = Window()
if __name__ == '__main__':
    window.show()

