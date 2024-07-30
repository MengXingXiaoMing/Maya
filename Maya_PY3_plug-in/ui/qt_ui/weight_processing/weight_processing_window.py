# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

import importlib
import weight_processing_window_command
importlib.reload(weight_processing_window_command)
from weight_processing_window_command import *


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
        self.setWindowTitle('权重处理(Maya'+self.maya_version+')')
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
    def create_widgets(self):
        # 第一行
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

        self.splitter_5 = QtWidgets.QSplitter()
        self.splitter_5.setFixedHeight(1)
        self.splitter_5.setFrameStyle(1)

        # 第六行
        self.button_37 = QtWidgets.QPushButton('为当前选择模型归一化权重')
        self.button_38 = QtWidgets.QPushButton('为当前选择骨骼修复模型移动过远出现抖动的情况(先选跟骨骼)')
        self.button_39 = QtWidgets.QPushButton('选择根骨骼撤回当前修复')


        self.splitter_6 = QtWidgets.QSplitter()
        self.splitter_6.setFixedHeight(1)
        self.splitter_6.setFrameStyle(1)
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
        main_layout.addStretch(1)
        main_layout.addWidget(self.splitter_5)

        # 第六行
        h_Box_layout_12 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_12)
        h_Box_layout_12.addWidget(self.button_37)
        h_Box_layout_12.addWidget(self.button_38)
        h_Box_layout_12.addWidget(self.button_39)


        main_layout.addWidget(self.splitter_6)
        # 置顶

    def create_connect(self):
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

        self.button_37.clicked.connect(self.normalization_joint_weight)  # 为当前选择模型归一化骨骼权重
        self.button_38.clicked.connect(self.matrix_repair_joint_weight_moving_too_far_and_shaking)  # 为当前选择骨骼修复模型移动过远抖动
        self.button_39.clicked.connect(self.select_the_root_joint_to_recall_the_current_matrix_and_repair_joint_weights)  # 选择根骨骼撤回当前矩阵修复骨骼权重

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
    def joint_weight_hammer(self):
        cmds.WeightHammer()
        # print('权重锤')

    # 复制权重
    def normal_copy_joint_weight(self):
        cmds.CopySkinWeights()
        # print('复制权重')

    # 镜像权重
    def mirror_joint_weight(self):
        cmds.MirrorSkinWeights()
        # print('镜像权重')

    # 移动有权重的骨骼
    def move_have_weight_joint(self):
        cmds.MoveSkinJointsTool()
        # print('移动有权重的骨骼')

    # 移除过小权重
    def prune_small_weights(self):
        cmds.PruneSmallWeights()
        # print('移除过小权重')

    # 还原至默认权重
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

window = Window()
if __name__ == '__main__':
    window.show()

