# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    # 库路径
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)


import weight_processing_window_command
importlib.reload(weight_processing_window_command)
from weight_processing_window_command import *

import others_library
from others_library import *
importlib.reload(others_library)

class Withdraw:
    @staticmethod
    def execute(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cmds.undoInfo(ock=1)
            result = func(*args, **kwargs)
            cmds.undoInfo(cck=1)
            return result
        return wrapper
class OverlayButton(QToolButton):
    def __init__(self, icon,offset,scale, parent=None):
        super().__init__(parent)
        self.all_icon = []
        self.offset = offset
        for i,s in zip(icon,scale):
            icon1 = QPixmap(i)  # 图片
            if s[0]!=0 and s[1]!=0:
                icon1 = icon1.scaled(QSize(s[0], s[1]))

            self.all_icon.append(icon1)

    def paintEvent(self, event):
        # 调用基类的 paintEvent 方法绘制默认按钮样式
        super().paintEvent(event)

        # 创建 QPainter 对象
        painter = QPainter(self)
        # 获取按钮的矩形区域
        rect = self.rect()
        # 计算中心点的坐标
        center = rect.center()

        # 绘制第一张图片
        for move,icon in zip(self.offset,self.all_icon):
            painter.drawPixmap(QPoint(move[0]+center.x(), move[1]+center.y()), icon)
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        self.command = Command()
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('权重处理(Maya'+self.maya_version+')(提示，带脚本，运行一些代码建议关闭此窗口)')
        # 提取年月日、时分秒，并转换成数字
        now = datetime.now()
        milliseconds = now.microsecond // 1000  # 将微秒转换为毫
        # 如果你想要一个包含毫秒的字符串表示
        self.time_str = now.strftime("%Y%m%d%H%M%S") + f"{milliseconds:03d}"
        self.setObjectName('ZKM_deform_edit_window' + self.time_str)
        self.deform = []
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
        self.library_path = root_path + '\\' + maya_version

        self.others_library = OthersLibrary()
        # 注册选择变化运行脚本
        self.register_selection_callback()

        self.populate_list_view()

    def create_widgets(self):
        # 第一行
        # 列表视图 - 使用QListWidget更简单
        self.list_widget_1 = QtWidgets.QListWidget()
        # 设置选择模式为单选
        self.list_widget_1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 禁止双击编辑：设置编辑触发器为NoEditTriggers
        self.list_widget_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置选择行为，确保单击即可选择
        self.list_widget_1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)

        # 在 list_widget_2 之前添加模式切换控件



        # 第一行
        # 列表视图 - 使用QListWidget更简单
        self.list_widget_1 = QtWidgets.QListWidget()
        # 设置选择模式为单选
        self.list_widget_1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 禁止双击编辑：设置编辑触发器为NoEditTriggers
        self.list_widget_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置选择行为，确保单击即可选择
        self.list_widget_1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)

        self.list_widget_2 = QtWidgets.QListWidget()
        # 设置选择模式为单选
        # self.list_widget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 修改这里：设置选择模式为多选（支持Shift和Ctrl键）
        self.list_widget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # 禁止双击编辑：设置编辑触发器为NoEditTriggers
        self.list_widget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置选择行为，确保单击即可选择
        self.list_widget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)

        self.button_1 = QtWidgets.QPushButton('选择拷贝源')

        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton('加载')

        self.button_3 = QtWidgets.QPushButton('选择拷贝点')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_4 = QtWidgets.QPushButton('加载')

        self.button_5 = QtWidgets.QPushButton('拷贝点权重')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        # 第二行
        self.button_6 = QtWidgets.QPushButton('移除无权重骨骼')
        self.button_7 = QtWidgets.QPushButton('统一循环边权重')
        self.button_8 = QtWidgets.QPushButton('中线建立骨骼链')

        self.button_9 = QtWidgets.QPushButton(self)
        self.button_9.setFixedSize(50, 50)
        if QtCore.QResource(':/paintSkinWeights.png').isValid():
            i = QtGui.QIcon(':/paintSkinWeights.png')
            self.button_9.setIcon(i)
        self.button_9.setIconSize(QSize(50, 50))
        self.button_10 = QtWidgets.QPushButton(self)
        self.button_10.setFixedSize(50, 50)
        if QtCore.QResource(':/weightHammer.png').isValid():
            i = QtGui.QIcon(':/weightHammer.png')
            self.button_10.setIcon(i)
        self.button_10.setIconSize(QSize(50, 50))
        self.button_11 = QtWidgets.QPushButton(self)
        self.button_11.setFixedSize(50, 50)
        if QtCore.QResource(':/copySkinWeight.png').isValid():
            i = QtGui.QIcon(':/copySkinWeight.png')
            self.button_11.setIcon(i)
        self.button_11.setIconSize(QSize(50, 50))
        self.button_40 = QtWidgets.QPushButton(self)
        self.button_40.setFixedSize(50, 50)
        if QtCore.QResource(':/detachSkin.png').isValid():
            i = QtGui.QIcon(':/detachSkin.png')
            self.button_40.setIcon(i)
        self.button_40.setIconSize(QSize(50, 50))
        self.button_12 = QtWidgets.QPushButton(self)
        self.button_12.setFixedSize(50, 50)
        if QtCore.QResource(':/mirrorSkinWeight.png').isValid():
            i = QtGui.QIcon(':/mirrorSkinWeight.png')
            self.button_12.setIcon(i)
        self.button_12.setIconSize(QSize(50, 50))
        self.button_13 = QtWidgets.QPushButton(self)
        self.button_13.setFixedSize(50, 50)
        if QtCore.QResource(':/moveSkinnedJoint.png').isValid():
            i = QtGui.QIcon(':/moveSkinnedJoint.png')
            self.button_13.setIcon(i)
        self.button_13.setIconSize(QSize(50, 50))
        self.button_14 = QtWidgets.QPushButton(self)
        self.button_14.setFixedSize(50, 50)
        if QtCore.QResource(':/clearCanvas.png').isValid():
            i = QtGui.QIcon(':/clearCanvas.png')
            self.button_14.setIcon(i)
        self.button_14.setIconSize(QSize(50, 50))
        self.button_15 = QtWidgets.QPushButton(self)
        self.button_15.setFixedSize(50, 50)
        if QtCore.QResource(':/rebuild.png').isValid():
            i = QtGui.QIcon(':/rebuild.png')
            self.button_15.setIcon(i)
        self.button_15.setIconSize(QSize(50, 50))

        self.button_16 = QtWidgets.QPushButton('拷贝权重')
        self.button_17 = QtWidgets.QPushButton('对半拷贝权重')

        self.splitter_2 = QtWidgets.QSplitter()
        self.splitter_2.setFixedHeight(1)
        self.splitter_2.setFrameStyle(1)

        # 第三行
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(['后期', '交互'])

        self.Label_1 = QtWidgets.QLabel()
        self.Label_1.setText('平滑次数:')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.line_edit_3.setFixedWidth(50)
        self.line_edit_3.setText('1')
        self.slider_1 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_1.setMinimum(1)
        self.slider_1.setMaximum(10)

        self.button_18 = QtWidgets.QPushButton('平滑权重')

        self.splitter_3 = QtWidgets.QSplitter()
        self.splitter_3.setFixedHeight(1)
        self.splitter_3.setFrameStyle(1)

        #第四行
        self.button_19 = QtWidgets.QPushButton('选择目标模型:')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_20 = QtWidgets.QPushButton('加载')
        self.button_21 = QtWidgets.QPushButton('选择模型合并权重到目标')
        self.button_22 = QtWidgets.QPushButton('导出权重')
        self.button_23 = QtWidgets.QPushButton('导入权重')

        self.splitter_4 = QtWidgets.QSplitter()
        self.splitter_4.setFixedHeight(1)
        self.splitter_4.setFrameStyle(1)
        # self.checkbox = QtWidgets.QCheckBox('Checkbox')

        #第五行
        self.LisLineButtonSize = [50,70]
        self.button_24 = QtWidgets.QToolButton(self)
        self.button_24.setAutoRaise(True)
        self.button_24.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.button_24.setText('选择层次')
        # self.button_24.setFixedSize(50, self.LisLineButtonSize[1])
        if QtCore.QResource(':/menuIconSelect.png').isValid():
            i = QtGui.QIcon(':/menuIconSelect.png')
            self.button_24.setIcon(i)
        self.button_24.setIconSize(QSize(30, 30))

        self.button_25 = QtWidgets.QToolButton(self)
        self.button_25.setAutoRaise(True)
        self.button_25.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/CenterPivot.png').isValid():
            i = QtGui.QIcon(':/CenterPivot.png')
            self.button_25.setIcon(i)
        self.button_25.setIconSize(QSize(50, 50))

        self.button_26 = QtWidgets.QToolButton(self)
        self.button_26.setAutoRaise(True)
        self.button_26.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/DeleteHistory.png').isValid():
            i = QtGui.QIcon(':/DeleteHistory.png')
            self.button_26.setIcon(i)
        self.button_26.setIconSize(QSize(50, 50))

        self.button_27 = QtWidgets.QToolButton(self)
        self.button_27.setAutoRaise(True)
        self.button_27.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/FreezeTransform.png').isValid():
            i = QtGui.QIcon(':/FreezeTransform.png')
            self.button_27.setIcon(i)
        self.button_27.setIconSize(QSize(50, 50))

        self.button_28 = QtWidgets.QToolButton(self)
        self.button_28.setAutoRaise(True)
        self.button_28.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/polyDelEdgeVertex.png').isValid():
            i = QtGui.QIcon(':/polyDelEdgeVertex.png')
            self.button_28.setIcon(i)
        self.button_28.setIconSize(QSize(50, 50))

        self.button_29 = QtWidgets.QToolButton(self)
        self.button_29.setAutoRaise(True)
        self.button_29.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/polySplitEdgeRing.png').isValid():
            i = QtGui.QIcon(':/polySplitEdgeRing.png')
            self.button_29.setIcon(i)
        self.button_29.setIconSize(QSize(50, 50))

        self.button_30 = QtWidgets.QToolButton(self)
        self.button_30.setAutoRaise(True)
        self.button_30.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/polyExtrudeFacet.png').isValid():
            i = QtGui.QIcon(':/polyExtrudeFacet.png')
            self.button_30.setIcon(i)
        self.button_30.setIconSize(QSize(50, 50))

        self.button_31 = QtWidgets.QToolButton(self)
        self.button_31.setAutoRaise(True)
        self.button_31.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/locator.png').isValid():
            i = QtGui.QIcon(':/locator.png')
            self.button_31.setIcon(i)
        self.button_31.setIconSize(QSize(50, 50))

        self.button_32 = QtWidgets.QToolButton(self)
        self.button_32.setAutoRaise(True)
        self.button_32.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/cluster.png').isValid():
            i = QtGui.QIcon(':/cluster.png')
            self.button_32.setIcon(i)
        self.button_32.setIconSize(QSize(50, 50))

        self.button_33 = QtWidgets.QToolButton(self)
        self.button_33.setAutoRaise(True)
        self.button_33.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        self.button_33.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.button_33.setText('S_V')
        if QtCore.QResource(':/kinJoint.png').isValid():
            i = QtGui.QIcon(':/kinJoint.png')
            self.button_33.setIcon(i)
        self.button_33.setIconSize(QSize(50, 50))

        self.button_34 = QtWidgets.QToolButton(self)
        self.button_34.setAutoRaise(True)
        self.button_34.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        self.button_34.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.button_34.setText('S_V')
        if QtCore.QResource(':/channelBoxUseManips.png').isValid():
            i = QtGui.QIcon(':/channelBoxUseManips.png')
            self.button_34.setIcon(i)
        self.button_34.setIconSize(QSize(50, 50))

        self.button_35 = QtWidgets.QToolButton(self)
        self.button_35.setAutoRaise(True)
        self.button_35.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/blendShapeEditor.png').isValid():
            i = QtGui.QIcon(':/blendShapeEditor.png')
            self.button_35.setIcon(i)
        self.button_35.setIconSize(QSize(50, 50))

        self.button_36 = QtWidgets.QToolButton(self)
        self.button_36.setAutoRaise(True)
        self.button_36.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        if QtCore.QResource(':/polyRetopo.png').isValid():
            i = QtGui.QIcon(':/polyRetopo.png')
            self.button_36.setIcon(i)
        self.button_36.setIconSize(QSize(50, 50))

        # self.button_41 = QtWidgets.QToolButton(self)
        # self.button_41.setAutoRaise(True)
        # self.button_41.setFixedSize(self.LisLineButtonSize[0], self.LisLineButtonSize[1])
        # if QtCore.QResource(':/Bool_Shaded.png').isValid():
        #     i = QtGui.QIcon(':/Bool_Shaded.png')
        #     self.button_41.setIcon(i)
        # self.button_41.setIconSize(QSize(50, 50))
        self.button_41 = self.creat_button('', [':/polyCube.png',':/Bool_Shaded.png'],
                            [[-16, -12], [0, -14]], [[30, 30], [0, 0]], [40, 40], [40, 40])  # 导出权重

        self.splitter_5 = QtWidgets.QSplitter()
        self.splitter_5.setFixedHeight(1)
        self.splitter_5.setFrameStyle(1)

        # 第六行
        self.button_37 = QtWidgets.QPushButton('为当前选择模型归一化权重')
        self.button_38 = QtWidgets.QPushButton('为当前选择骨骼修复模型移动过远出现抖动的情况(先选跟骨骼)')
        self.button_39 = QtWidgets.QPushButton('选择根骨骼撤回当前修复')

        self.button_45 = QtWidgets.QPushButton('曲面绑定蒙皮')
        self.button_44 = QtWidgets.QPushButton('添加曲面影响')
        self.button_42 = QtWidgets.QPushButton('移除曲面影响')
        self.button_43 = QtWidgets.QPushButton('复制形状节点')


        self.splitter_6 = QtWidgets.QSplitter()
        self.splitter_6.setFixedHeight(1)
        self.splitter_6.setFrameStyle(1)
    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        h_box_layout = QtWidgets.QHBoxLayout(self.central_widget)
        h_box_layout.setContentsMargins(0, 0, 0, 0)
        h_box_layout.setSpacing(1)

        v_box_layout_0 = QtWidgets.QVBoxLayout(self)



        v_box_layout_0.addWidget(self.list_widget_1)
        v_box_layout_0.addWidget(self.list_widget_2)
        h_box_layout.addLayout(v_box_layout_0)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        h_box_layout.addLayout(main_layout)
        # 列表视图

        # 第一行
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.setSpacing(1)

        # self.list_view = QtWidgets.QListView(self)
        # self.list_model = QtGui.QStandardItemModel(self.list_view)
        # self.list_view.setModel(self.list_model)
        # main_layout.addWidget(self.list_view)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.button_1)
        h_Box_layout_3.addWidget(self.line_edit_1)
        h_Box_layout_3.addWidget(self.button_2)

        # h_Box_layout_1.addStretch(1)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.button_3)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_4)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.button_5)

        main_layout.addWidget(self.splitter_1)
        # 第二行
        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_6)
        h_Box_layout_6.setSpacing(1)

        q_grid_layout_1 = QtWidgets.QGridLayout(self)
        h_Box_layout_6.addLayout(q_grid_layout_1)
        q_grid_layout_1.setColumnStretch(1, 0)
        q_grid_layout_1.addWidget(self.button_6)
        q_grid_layout_1.addWidget(self.button_7)
        q_grid_layout_1.addWidget(self.button_8)

        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_6.addLayout(h_Box_layout_7)
        h_Box_layout_7.addWidget(self.button_9)
        h_Box_layout_7.addWidget(self.button_10)
        h_Box_layout_7.addWidget(self.button_11)
        h_Box_layout_7.addWidget(self.button_40)
        h_Box_layout_7.addWidget(self.button_12)
        h_Box_layout_7.addWidget(self.button_13)
        h_Box_layout_7.addWidget(self.button_14)
        h_Box_layout_7.addWidget(self.button_15)

        v_box_layout_1 = QtWidgets.QVBoxLayout(self)
        h_Box_layout_6.addLayout(v_box_layout_1)
        v_box_layout_1.addWidget(self.button_16)
        v_box_layout_1.addWidget(self.button_17)

        main_layout.addWidget(self.splitter_2)
        # 第三行
        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.comboBox_1)

        h_Box_layout_9 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_8.addLayout(h_Box_layout_9)
        h_Box_layout_9.addWidget(self.Label_1)
        h_Box_layout_9.addWidget(self.line_edit_3)
        h_Box_layout_9.addWidget(self.slider_1)

        h_Box_layout_8.addWidget(self.button_18)

        main_layout.addWidget(self.splitter_3)
        # 第四行
        h_Box_layout_10 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_10)
        h_Box_layout_10.addWidget(self.button_19)
        h_Box_layout_10.addWidget(self.line_edit_4)
        h_Box_layout_10.addWidget(self.button_20)
        h_Box_layout_10.addWidget(self.button_21)
        h_Box_layout_10.addWidget(self.button_22)
        h_Box_layout_10.addWidget(self.button_23)

        main_layout.addWidget(self.splitter_4)

        # 第五行
        h_Box_layout_11 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_11)
        h_Box_layout_11.addWidget(self.button_24)
        h_Box_layout_11.addWidget(self.button_25)
        h_Box_layout_11.addWidget(self.button_26)
        h_Box_layout_11.addWidget(self.button_27)
        h_Box_layout_11.addWidget(self.button_28)
        h_Box_layout_11.addWidget(self.button_29)
        h_Box_layout_11.addWidget(self.button_30)
        h_Box_layout_11.addWidget(self.button_31)
        h_Box_layout_11.addWidget(self.button_32)
        h_Box_layout_11.addWidget(self.button_33)
        h_Box_layout_11.addWidget(self.button_34)
        h_Box_layout_11.addWidget(self.button_35)
        h_Box_layout_11.addWidget(self.button_36)
        h_Box_layout_11.addWidget(self.button_41)
        main_layout.addStretch(1)
        main_layout.addWidget(self.splitter_5)

        # 第六行
        h_Box_layout_12 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_12)
        h_Box_layout_12.addWidget(self.button_37)
        h_Box_layout_12.addWidget(self.button_38)
        h_Box_layout_12.addWidget(self.button_39)

        main_layout.addWidget(self.button_45)
        main_layout.addWidget(self.button_44)
        main_layout.addWidget(self.button_42)
        main_layout.addWidget(self.button_43)

        main_layout.addWidget(self.splitter_6)
        # 置顶


    def create_connect(self):
        # 列表项单击信号连接
        self.list_widget_1.itemClicked.connect(self.on_item_clicked)
        # 列表项选择变化信号连接
        self.list_widget_1.itemSelectionChanged.connect(lambda: self.on_selection_changed(self.list_widget_1))

        self.button_1.clicked.connect(self.select_copy_source)  # 选择拷贝源按钮
        self.button_2.clicked.connect(self.reload_copy_source)  # 加载拷贝源按钮
        self.button_3.clicked.connect(self.select_copy_target)  # 选择拷贝目标按钮
        self.button_4.clicked.connect(self.reload_copy_target)  # 加载拷贝目标按钮
        self.button_5.clicked.connect(self.copy_point_weight)  # 拷贝点权重

        self.button_6.clicked.connect(self.remove_have_not_weight_joint)  # 移除无权重骨骼
        self.button_7.clicked.connect(self.unify_loop_edge_joint_weight)  # 统一循环边权重
        self.button_8.clicked.connect(self.establishing_a_bone_chain_at_the_midline)  # 中线建立骨骼链

        self.button_9.clicked.connect(self.joint_weight_drawing_tool)  # 权重绘制工具
        self.button_10.clicked.connect(self.joint_weight_hammer)  # 权重锤
        self.button_11.clicked.connect(self.normal_copy_joint_weight)  # 复制权重
        self.button_40.clicked.connect(self.cancel_skinning)  # 取消蒙皮
        self.button_12.clicked.connect(self.mirror_joint_weight)  # 镜像权重
        self.button_13.clicked.connect(self.command.others_library.switch_skin_model_hand_influence_state)  # 移动有权重的骨骼
        self.button_14.clicked.connect(self.prune_small_weights)  # 移除过小权重
        self.button_15.clicked.connect(self.reset_weights_to_default)  # 还原至默认权重
        self.button_16.clicked.connect(self.copy_weight)  # 拷贝权重
        self.button_17.clicked.connect(self.half_and_half_copy_weight)  # 对半拷贝权重

        self.line_edit_3.textChanged.connect(self.modify_UI_values_and_provide_feedback_to_the_slider)  # 修改ui数值反馈给滑块
        self.slider_1.valueChanged.connect(self.automatically_adjust_the_slider_range_and_return_values_to_ui)  # 自动调整ui范围
        self.button_18.clicked.connect(self.smooth_joint_weight)  # 平滑权重

        self.button_19.clicked.connect(self.select_target_model)  # 选择目标模型
        self.button_20.clicked.connect(self.reload_target_model)  # 加载目标模型
        self.button_21.clicked.connect(self.select_source_model_merge_joint_weight_to_target)  # 选择源模型合并权重到目标
        self.button_22.clicked.connect(self.export_joint_weight)  # 导出权重
        self.button_23.clicked.connect(self.import_joint_weight)  # 导入权重

        self.button_24.clicked.connect(self.select_levels)  # 选择层次
        self.button_25.clicked.connect(self.center_pivot)  # 居中枢轴
        self.button_26.clicked.connect(self.delete_history)  # 删除历史
        self.button_27.clicked.connect(self.freeze_changes)  # 冻结变换
        self.button_28.clicked.connect(self.delete_segment)  # 删除线
        self.button_29.clicked.connect(self.create_edge_loop)  # 创建循环边
        self.button_30.clicked.connect(self.extrusion)  # 挤出
        self.button_31.clicked.connect(self.create_locator)  # 创建定位器
        self.button_32.clicked.connect(self.create_cluster)  # 创建蔟
        self.button_33.clicked.connect(self.show_or_hide_bones)  # 显影骨骼
        self.button_34.clicked.connect(self.show_hide_axial)  # 显影轴向
        self.button_35.clicked.connect(self.blend_shape_window)  # 混合变形窗口
        self.button_36.clicked.connect(self.anew_topology)  # 重拓补
        self.button_41.clicked.connect(lambda :self.others_library.voxelization())

        self.button_37.clicked.connect(self.normalization_joint_weight)  # 为当前选择模型归一化骨骼权重
        self.button_38.clicked.connect(self.matrix_repair_joint_weight_moving_too_far_and_shaking)  # 为当前选择骨骼修复模型移动过远抖动
        self.button_39.clicked.connect(self.select_the_root_joint_to_recall_the_current_matrix_and_repair_joint_weights)  # 选择根骨骼撤回当前矩阵修复骨骼权重

        self.button_45.clicked.connect(self.create_surface_skin)  # 创建蒙皮
        self.button_44.clicked.connect(self.addSurfaceClusterUse)  # 添加影响
        self.button_42.clicked.connect(self.removeSurfaceClusterUse)  # 移除影响
        self.button_43.clicked.connect(self.copy_shape_node_use)  # 取消

    # 选择拷贝源
    def select_copy_source(self):
        self.command.maya_common.select_text_target(self.line_edit_1,['QLineEdit'])
        # print('选择拷贝源')

    # 加载拷贝源
    def reload_copy_source(self):
        self.command.ui_edit.load_select_for_ui_text(self.line_edit_1,['QLineEdit'])
        # print('加载拷贝源')

    # 选择拷贝目标
    def select_copy_target(self):
        self.command.maya_common.select_text_target(self.line_edit_2, ['QLineEdit'])
        # print('选择拷贝目标')

    # 加载拷贝目标
    def reload_copy_target(self):
        self.command.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit'])
        # print('加载拷贝目标')

    # 拷贝点权重
    def copy_point_weight(self):
        soure = self.line_edit_1.text()
        soure = [soure]
        target = self.line_edit_2.text()
        target = target.split(',')
        if soure and target:
            self.command.weight.base_copy_joint_weight('Normal', soure, target, '', '')
        else:
            cmds.warning('请加载正确的源和点。')
        # print('拷贝点权重')

    # 移除无权重骨骼
    def remove_have_not_weight_joint(self):
        mel.eval('removeUnusedInfluences;')
        # print('移除无权重骨骼')

    # 统一循环边权重
    def unify_loop_edge_joint_weight(self):
        self.command.others_library.uniform_edge_loop_weights()
        # print('统一循环边权重')

    # 中线建立骨骼链
    def establishing_a_bone_chain_at_the_midline(self):
        self.command.others_library.establishing_a_bone_chain_at_the_midline()
        # print('中线建立骨骼链')

    # 权重绘制工具
    def joint_weight_drawing_tool(self):
        cmds.ArtPaintSkinWeightsTool()
        # print('权重绘制工具')

    # 权重锤
    @Withdraw.execute
    def joint_weight_hammer(self):
        cmds.WeightHammer()
        # print('权重锤')

    # 复制权重
    @Withdraw.execute
    def normal_copy_joint_weight(self):
        cmds.CopySkinWeights()
        # print('复制权重')

    # 取消蒙皮
    @Withdraw.execute
    def cancel_skinning(self):
        self.command.weight.cancel_skin()

    # 镜像权重
    def mirror_joint_weight(self):
        cmds.MirrorSkinWeights()
        # print('镜像权重')

    # 移动有权重的骨骼
    @Withdraw.execute
    def move_have_weight_joint(self):
        cmds.MoveSkinJointsTool()
        # print('移动有权重的骨骼')

    # 移除过小权重
    @Withdraw.execute
    def prune_small_weights(self):
        cmds.PruneSmallWeights()
        # print('移除过小权重')

    # 还原至默认权重
    @Withdraw.execute
    def reset_weights_to_default(self):
        cmds.ResetWeightsToDefault()
        print('还原至默认权重')

    # 拷贝权重
    def copy_weight(self):
        self.command.weight.copy_joint_weight()
        print('拷贝权重')

    # 对半拷贝权重
    def half_and_half_copy_weight(self):
        self.command.weight.half_and_half_copy_weight()
        print('对半拷贝权重')

    # 自动调整滑块范围且返回数值给ui
    def automatically_adjust_the_slider_range_and_return_values_to_ui(self):
        soure_ui = self.slider_1
        soure_ui_type = 'QSlider'
        num = self.command.automatically_adjust_the_slider_range_and_return_values_to_ui(soure_ui, soure_ui_type)
        self.line_edit_3.setText(str(num))

    # 修改ui数值反馈给滑块
    def modify_UI_values_and_provide_feedback_to_the_slider(self):
        num = self.line_edit_3.text()
        num = float(num)
        # print(num)
        target_ui = self.slider_1
        target_ui_type = 'QSlider'
        self.command.ui_edit.give_the_value_to_the_slider(num, target_ui, target_ui_type)

    # 平滑权重
    def smooth_joint_weight(self):
        smooth_type = self.comboBox_1.currentText()
        if smooth_type == '后期':
            smooth_type = 1
        else:
            pass
        num = self.slider_1.value()
        self.command.weight.apply_smooth_weight(smooth_type, int(num))

        #self.command.smooth_joint_weight()
        #print('平滑权重')

    # 选择目标模型
    def select_target_model(self):
        self.command.maya_common.select_text_target(self.line_edit_4, ['QLineEdit'])
        # print('选择目标模型')

    # 加载目标模型
    def reload_target_model(self):
        self.command.ui_edit.load_select_for_ui_text(self.line_edit_4, ['QLineEdit'])
        # print('加载目标模型')

    # 选择源模型合并权重到目标
    def select_source_model_merge_joint_weight_to_target(self):
        soure = self.line_edit_4.text()
        self.command.weight.select_source_model_merge_joint_weight_to_target(soure)
        #print('选择源模型合并权重到目标')

    # 导出权重
    def export_joint_weight(self):
        self.command.weight.export_weight(cmds.ls(sl=1))
        print('导出权重')

    # 导入权重
    def import_joint_weight(self):
        self.command.weight.import_weight(cmds.ls(sl=1))
        print('导入权重')

    # 选择层次
    def select_levels(self):
        cmds.SelectHierarchy()
        print('选择层次')

    # 居中枢轴
    def center_pivot(self):
        cmds.CenterPivot()
        print('居中枢轴')

    # 删除历史
    def delete_history(self):
        cmds.DeleteHistory()
        print('删除历史')

    # 冻结变换
    def freeze_changes(self):
        cmds.FreezeTransformations()
        print('冻结变换')

    # 删除线
    def delete_segment(self):
        cmds.DeletePolyElements()
        print('删除线')

    # 创建循环边
    def create_edge_loop(self):
        cmds.SplitEdgeRingTool()
        print('创建循环边')

    # 挤出
    def extrusion(self):
        cmds.polyExtrudeFacet()
        print('挤出')

    # 创建定位器
    def create_locator(self):
        cmds.CreateLocator()
        print('创建定位器')

    # 创建蔟
    def create_cluster(self):
        cmds.cluster()
        print('创建蔟')

    # 显影骨骼
    def show_or_hide_bones(self):
        self.command.others_library.set_bone_display()
        print('显影骨骼')

    # 显影轴向
    def show_hide_axial(self):
        self.command.others_library.show_hide_axial()
        print('显影轴向')

    # 混合变形窗口
    def blend_shape_window(self):
        cmds.ShapeEditor()
        print('混合变形窗口')

    # 重拓补
    def anew_topology(self):
        if self.maya_version == '2018':
            cmds.warning('暂未添加')
        if self.maya_version == '2022':
            cmds.polyRetopo()
        if self.maya_version == '2023':
            cmds.polyRetopo()
        if self.maya_version == '2024':
            cmds.polyRetopo()
        if self.maya_version == '2025':
            cmds.polyRetopo()
        # print('重拓补')

    # 为当前选择模型归一化骨骼权重
    def normalization_joint_weight(self):
        self.command.weight.normalize_weight(cmds.ls(sl=1))
        # print('为当前选择模型归一化骨骼权重')

    # 为当前选择骨骼修复模型移动过远抖动
    def matrix_repair_joint_weight_moving_too_far_and_shaking(self):
        self.command.weight.handling_weight_jitter(cmds.ls(sl=1),1)
        # print('为当前选择骨骼修复模型移动过远抖动')

    # 选择根骨骼撤回当前矩阵修复骨骼权重
    def select_the_root_joint_to_recall_the_current_matrix_and_repair_joint_weights(self):
        self.command.weight.handling_weight_jitter(cmds.ls(sl=1), 0)
         # print('选择根骨骼撤回当前矩阵修复骨骼权重')
    # 创建图片按钮
    def creat_button(self, name, icon, move, scale, lage, icon_lage):
        button = OverlayButton(icon, move, scale)

        if name:
            button.setText(name)
        button.setAutoRaise(True)
        if lage[0]!=0 and lage[1]!=0:
            button.setFixedSize(lage[0], lage[1])
        button.setMaximumSize(999,999)
        # if QtCore.QResource(icon).isValid():
        #     i = QtGui.QIcon(icon)
        #     button.setIcon(i)
        if icon_lage[0]!=0 and icon_lage[1]!=0:
            button.setIconSize(QSize(icon_lage[0], icon_lage[1]))
        return button

    # 脚本命令
    def job_commend(self):
        self.creat_select_deform_list()

    # 注册选择变化事件的回调函数
    def register_selection_callback(self):
        # 创建回调函数
        jobNum = cmds.scriptJob(e=["SelectionChanged", self.job_commend], protected=True, parent='ZKM_deform_edit_window'+self.time_str)
        # print(cmds.scriptJob(listJobs=True))

    def closeEvent(self, event):
        self.deleteLater()  # 标记窗口为待删除
        # super(Window, self).closeEvent(event)
        print("窗口关闭，脚本清理完毕")

    def creat_select_deform_list(self):
        self.populate_list_view()
        # print('选择改变')

    # 创建变形器列表
    def populate_list_view(self):
        sel = cmds.ls(sl=1)
        self.list_widget_1.clear()
        need_deform = []
        if sel:
            deforms = self.list_deformer_hierarchy(sel[0])
            deform_type = []
            for deform in deforms:
                deform_type = cmds.nodeType(deform, inherited=True)
                if deform_type:
                    if deform_type[-1] == 'skinCluster':
                        need_deform.append(deform)
                    elif deform_type[-1] == 'surfaceSkinCluster':
                        need_deform.append(deform)

            """填充列表视图数据"""
            # 获取Maya场景中的几何体
            # geometries = cmds.ls(geometry=True)
            self.list_widget_1.clear()
            if need_deform:
                for geo in need_deform:
                    item = QtWidgets.QListWidgetItem(geo)
                    self.list_widget_1.addItem(item)

                # 自动选择第一项[5](@ref)
                if self.list_widget_1.count() > 0:
                    self.list_widget_1.setCurrentRow(0)
                    # 打印第一项字符
                    first_item = self.list_widget_1.item(0)
                    # print(f"自动选择: {first_item.text()}")

        self.list_widget_2.clear()
        need_deform = []
        if sel:
            deforms = self.list_deformer_hierarchy(sel[-1])
            deform_type = []
            for deform in deforms:
                deform_type = cmds.nodeType(deform, inherited=True)
                if deform_type:
                    if deform_type[-1] == 'skinCluster':
                        need_deform.append(deform)
                    elif deform_type[-1] == 'surfaceSkinCluster':
                        need_deform.append(deform)

            """填充列表视图数据"""
            # 获取Maya场景中的几何体
            # geometries = cmds.ls(geometry=True)
            self.list_widget_2.clear()
            if need_deform:
                for geo in need_deform:
                    item = QtWidgets.QListWidgetItem(geo)
                    self.list_widget_2.addItem(item)

                # 自动选择第一项[5](@ref)
                if self.list_widget_2.count() > 0:
                    self.list_widget_2.setCurrentRow(0)
                    # 打印第一项字符
                    first_item = self.list_widget_2.item(0)
                    # print(f"自动选择: {first_item.text()}")

    def on_item_clicked(self, item):
        """处理列表项单击事件 - 单击时打印字符"""
        # print(f"处理列表项单击事件")
        pass

    def on_selection_changed(self, list_widget):
        """处理选择变化"""
        current_item = list_widget.currentItem()
        if current_item:
            self.deform = current_item.text()
            # print(f"选择已更改1: {self.deform}")

    # 返回变形器列表
    def list_deformer_hierarchy(self, sel):
        # 获取当前选择的模型
        shape = cmds.ls(sel, dag=True, shapes=True)
        if not shape:
            deform = []
        else:
            # 获取选择的模型形状节点
            obj = shape[0]
            # 获取与模型相关的变形器节点
            deform = cmds.listHistory(obj, pruneDagObjects=True, interestLevel=True)
            deform = cmds.ls(deform, type='geometryFilter')  # 过滤出变形器节点
        return deform

    # 添加影响
    def addSurfaceClusterUse(self):
        meshs, surfaces = self.getMeshAndSurface()
        # print(meshs,surfaces)
        # 获取模型是否拥有曲面蒙皮包裹节点
        deforms = self.list_deformer_hierarchy(meshs)
        all_deforms = []
        deform_type = []
        for deform in deforms:
            print(deform)
            deform_type = cmds.nodeType(deform, inherited=True)
            if deform_type:
                if deform_type[-1] == 'surfaceSkinCluster':
                    all_deforms.append(deform)
        self.addSurfaceCluster(meshs, surfaces, all_deforms)
    def addSurfaceCluster(self, meshs, surfaces, all_deforms):
        for mesh in meshs:
            # 获取模型是否拥有曲面蒙皮包裹节点
            deforms = self.list_deformer_hierarchy(mesh)
            deform_type = []
            for deform in deforms:
                # print('deform',deform)
                deform_type = cmds.nodeType(deform, inherited=True)
                if deform_type:
                    if deform_type[-1] == 'surfaceSkinCluster' and deform in all_deforms:
                        try:
                            size = cmds.ls(deform + ".lockWeights[*]")
                        except:
                            pass
                        # print(size)
                        str_num = size[-1].split('[')[-1][:-1]
                        # print('str_num',str_num)
                        size = 1+int(str_num)
                        size += 1
                        if size < 1:
                            size = 1
                        for surface in surfaces:
                            self.copy_shape_node(surface)
                            if not cmds.objExists(surface + ".lockInfluenceWeights"):
                                cmds.select(surface, replace=True)
                                cmds.addAttr(shortName="liw", longName="lockInfluenceWeights", attributeType="bool")
                            shape = cmds.listRelatives(surface, shapes=1) or []
                            # print('shape',shape)
                            # size = cmds.getAttr(deform + ".lockWeights", size=True)
                            connections = [
                                (surface + ".liw", deform + ".lockWeights["+str(size-1)+"]"),
                                (surface + ".worldMatrix[0]", deform + ".matrix["+str(size-1)+"]"),
                                (surface + ".objectColorRGB", deform + ".influenceColor["+str(size-1)+"]"),
                                (shape[-1] + ".worldSpace[0]", deform + ".baseSurface["+str(size-1)+"]"),
                                (shape[0] + ".worldSpace[0]", deform + ".wrapSurface["+str(size-1)+"]")
                            ]
                            for source, target in connections:
                                # try:
                                    # print('connectAttr',source, target)
                                cmds.connectAttr(source, target)
                                # except:
                                #     continue

                            # cmds.connectAttr(surface + ".liw", deform+".lockWeights")
                            # cmds.connectAttr(surface + ".worldMatrix[0]", deform+".matrix[" + str(i) + "]")
                            # cmds.connectAttr(surface + ".objectColorRGB", deform+".influenceColor[" + str(i) + "]")
                            # cmds.connectAttr(surface + ".worldSpace[0]", deform+".baseSurface[" + str(i) + "]", force=True)
                            # cmds.connectAttr(surface + ".worldSpace[0]", deform+".wrapSurface[" + str(i) + "]", force=True)
                            # 获取世界逆矩阵
                            m = cmds.getAttr(surface + ".wim")
                            # 设置绑定预矩阵
                            cmds.setAttr(deform + ".bindPreMatrix[" + str(size - 1) + "]", m, type="matrix")


    # 移除影响
    def removeSurfaceClusterUse(self):
        meshs, surfaces = self.getMeshAndSurface()
        # 获取模型是否拥有曲面蒙皮包裹节点
        deforms = self.list_deformer_hierarchy(meshs)
        all_deforms = []
        deform_type = []
        for deform in deforms:
            # print(deform)
            deform_type = cmds.nodeType(deform, inherited=True)
            if deform_type:
                if deform_type[-1] == 'surfaceSkinCluster':
                    all_deforms.append(deform)
        self.removeSurfaceCluster(meshs, surfaces, all_deforms)
    def removeSurfaceCluster(self, meshs, surfaces, all_deforms):
        for mesh in meshs:
            # 获取模型是否拥有曲面蒙皮包裹节点
            deforms = self.list_deformer_hierarchy(mesh)
            deform_type = []
            for deform in deforms:
                deform_type = cmds.nodeType(deform, inherited=True)
                if deform_type:
                    # print(deform_type)
                    if deform_type[-1] == 'surfaceSkinCluster' and deform in all_deforms:
                        for surface in surfaces:
                            an = self.get_connections_between_nodes(surface, deform)
                            need_an = []
                            for a in an:
                                s = a.split('.')[-1]
                                s = s.split('[')[0]
                                if s in 'matrix':
                                    need_an = a
                                    break
                            # print(need_an)
                            str_num = need_an.split('[')[-1][:-1]
                            # print('str_num',str_num)
                            # print('开始移除',surface)
                            shape = cmds.listRelatives(surface, shapes=1) or []
                            # print('shape',shape)
                            # 方法2：使用循环处理
                            # destinations = cmds.connectionInfo(full_attr, destinationFromSource=True)
                            connections = [
                                (surface + ".liw", deform + '.lockWeights['+str_num+']'),
                                (surface + ".worldMatrix[0]", deform + '.matrix['+str_num+']'),
                                (surface + ".objectColorRGB", deform + '.influenceColor['+str_num+']'),
                                (shape[-1] + ".worldSpace[0]", deform + '.baseSurface['+str_num+']'),
                                (shape[0] + ".worldSpace[0]", deform + '.wrapSurface['+str_num+']')
                            ]
                            for source, target in connections:
                                try:
                                    cmds.disconnectAttr(source, target)
                                except:
                                    continue

    def get_connections_between_nodes(self, node1, node2):
        """获取两个节点之间的所有连接"""
        # 获取 node1 的所有连接
        connections = cmds.listConnections(node1, connections=True, plugs=True)
        if not connections:
            return []

        # 筛选出连接到 node2 的连接
        result = []
        for i in range(0, len(connections), 2):
            source = connections[i]
            destination = connections[i + 1]

            # 检查是否连接到目标节点
            if node2 in source or node2 in destination:
                result.append(destination)

        return result

    # 获取选择的模型和曲面并返回
    def getMeshAndSurface(self):
        sel = cmds.ls(sl=1)
        # 获取形状节点判断类型
        meshs = []
        surfaces = []
        for obj in sel:
            # 获取所有子节点
            children = cmds.listRelatives(obj, shapes=1) or []
            # for child in children:
            # 检查是否是形状节点
            if cmds.nodeType(children[0]) == 'mesh':
                meshs.append(obj)
                # print(f"Mesh shape: {child}")
            else:
                surfaces.append(obj)
                cmds.nodeType(children[0]) == 'nurbsSurface'
                # print(f"NURBS surface shape: {child}")
        return meshs, surfaces

    # 复制形状节点
    def copy_shape_node_use(self, sel):
        sel = cmds.ls(sl=1)
        for s in sel:
            self.copy_shape_node(s)
    def copy_shape_node(self, sel):
        # sel = cmds.ls(sl=1)
        # shape_node = cmds.listRelatives(sel, shapes=True)[0]
        # # 复制形状节点
        # duplicated_shape = cmds.duplicate(shape_node,rr=1,st=1)[0]
        # print(duplicated_shape)
        # # 如果需要将新形状节点连接到特定transform节点
        # target_transform = sel  # 目标transform节点
        # if cmds.objExists(duplicated_shape):
        #     # 获取新形状节点
        #     new_shapes = cmds.listRelatives(duplicated_shape, shapes=True)
        #     if new_shapes:
        #         # 将形状节点parent到目标transform
        #         cmds.parent(new_shapes[0], target_transform, shape=True, add=True)
        #         # 删除多余的transform节点
        #         cmds.delete(duplicated_shape)
        #         cmds.setAttr(new_shapes[0]+".intermediateObject", 1)
        # sel = cmds.ls(sl=1)
        shape_node = cmds.listRelatives(sel, shapes=True)
        # print(shape_node)
        if len(shape_node)>1:
            pass
        else:
            cluster = cmds.cluster(sel)
            cmds.delete(cluster)

    # 创建曲面蒙皮
    # @Withdraw
    def create_surface_skin(self):
        # 创建多个NURBS平面
        meshs, surfaces = self.getMeshAndSurface()
        # 创建表面皮肤集群变形器
        for mesh in meshs:
            # print(mesh)
            deform = cmds.deformer(mesh, type="surfaceSkinCluster")
            deform_type = cmds.nodeType(deform, inherited=True)
            if deform_type:
                try:
                    size = cmds.getAttr(deform[0] + ".lockWeights",size=1)
                except:
                    size = 1
                # print('size', size)
                if size < 1:
                    size = 1
                for surface in surfaces:
                    self.copy_shape_node(surface)
                    if not cmds.objExists(surface + ".lockInfluenceWeights"):
                        cmds.select(surface, replace=True)
                        cmds.addAttr(shortName="liw", longName="lockInfluenceWeights", attributeType="bool")

                    shape = cmds.listRelatives(surface, shapes=1) or []
                    # print(shape)
                    connections = [
                        (surface + ".liw", deform[0] + ".lockWeights[" + str(size - 1) + "]"),
                        (surface + ".worldMatrix[0]", deform[0] + ".matrix[" + str(size - 1) + "]"),
                        (surface + ".objectColorRGB", deform[0] + ".influenceColor[" + str(size - 1) + "]"),
                        (shape[-1] + ".worldSpace[0]", deform[0] + ".baseSurface[" + str(size - 1) + "]"),
                        (shape[0] + ".worldSpace[0]", deform[0] + ".wrapSurface[" + str(size - 1) + "]")
                    ]
                    for source, target in connections:
                        try:
                            cmds.connectAttr(source, target)
                        except:
                            continue

                    # cmds.connectAttr(surface + ".liw", deform+".lockWeights")
                    # cmds.connectAttr(surface + ".worldMatrix[0]", deform+".matrix[" + str(i) + "]")
                    # cmds.connectAttr(surface + ".objectColorRGB", deform+".influenceColor[" + str(i) + "]")
                    # cmds.connectAttr(surface + ".worldSpace[0]", deform+".baseSurface[" + str(i) + "]", force=True)
                    # cmds.connectAttr(surface + ".worldSpace[0]", deform+".wrapSurface[" + str(i) + "]", force=True)
                    # 获取世界逆矩阵
                    m = cmds.getAttr(surface + ".wim")
                    # 设置绑定预矩阵
                    cmds.setAttr(deform[0] + ".bindPreMatrix[" + str(size - 1) + "]", m, type="matrix")
                    size += 1
        cmds.setAttr(deform[0]+".useComponentsMatrix", 1)

        # 设置皮肤集群的最大影响数
        # cmds.skinCluster("surfaceSkinCluster1", edit=True, maximumInfluences=3)
window = Window()
if __name__ == '__main__':
    window.show()

