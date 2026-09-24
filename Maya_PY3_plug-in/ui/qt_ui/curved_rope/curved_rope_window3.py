# -*- coding: utf-8 -*-
import math

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken6 import wrapInstance
import maya.cmds as cmds
import os
import inspect
import importlib
import sys

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

import curve
importlib.reload(curve)
from curve import *

import controller
importlib.reload(controller)
from controller import *

import others_library
importlib.reload(others_library)
from others_library import *

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import common
importlib.reload(common)
from common import *

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
        print(self.root_path)
        # 库路径
        self.library_path = self.root_path + '\\' + maya_version
        # 样条库路径
        self.curve_library_path = self.library_path+ '\curve_library'

        self.curve = CreateAndEditCurve()
        self.curve_library = CreateAndEditCurve()
        self.controller = CurveControllerEdit()
        self.others_library = OthersLibrary()
        self.ui_edit = UiEdit()

        # 开启必要插件
        pluginInfo = cmds.pluginInfo(listPlugins=True, q=True)
        have_matrixNodes = 0
        for p in pluginInfo:
            if 'matrixNodes' == p:
                have_matrixNodes = 1
        if have_matrixNodes == 0:
            cmds.loadPlugin('matrixNodes')
        have_lookdevKit = 0
        for p in pluginInfo:
            if 'lookdevKit' == p:
                have_lookdevKit = 1
        if have_lookdevKit == 0:
            cmds.loadPlugin('lookdevKit')

        self.setWindowTitle('绳子(Maya'+self.maya_version+')')
        self.create_widgets()
        self.create_layouts()
        self.create_connect()
        self.get_rope_num()
        self.get_rope_template()

    def create_widgets(self):
        # 第一行
        self.comboBox_0 = QtWidgets.QComboBox()

        self.button_1 = QtWidgets.QPushButton('测试模板')
        self.button_2 = QtWidgets.QPushButton('中心建立骨骼链')
        self.button_3 = QtWidgets.QPushButton('按骨骼生成样条')
        # self.button_4 = QtWidgets.QPushButton('选择样条创建控制器方向定位骨骼')

        self.line_edit_1 = QtWidgets.QLineEdit()
        self.line_edit_1.setFixedWidth(50)
        self.line_edit_1.setText('50')
        self.slider_1 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_1.setMinimum(1)
        self.slider_1.setMaximum(100)
        self.slider_1.setValue(50)
        self.button_4 = QtWidgets.QPushButton('创建骨骼')

        self.label_1 = QtWidgets.QLabel('根骨骼:')
        self.line_edit_2 = QtWidgets.QLineEdit('')
        self.button_5 = QtWidgets.QPushButton('加载')

        self.button_6 = QtWidgets.QPushButton('矫正轴向')

        self.label_2 = QtWidgets.QLabel('样条:')
        self.line_edit_3 = QtWidgets.QLineEdit('')
        self.button_7 = QtWidgets.QPushButton('加载')
        self.button_10 = QtWidgets.QPushButton('转换为贝塞尔曲线')

        self.line_edit_7 = QtWidgets.QLineEdit()
        self.button_8 = QtWidgets.QPushButton('创建或加载方向骨骼')

        self.check_box_1 = QtWidgets.QCheckBox('独立控制器')

        # self.check_box_2 = QtWidgets.QCheckBox('底层单向FK')
        # self.check_box_3 = QtWidgets.QCheckBox('反转此FK')

        self.label_3 = QtWidgets.QLabel('滑动缩放控制器:')
        self.line_edit_4 = QtWidgets.QLineEdit('0')
        self.line_edit_4.setFixedWidth(50)
        self.slider_2 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_2.setMinimum(1)
        self.slider_2.setMaximum(10)

        # self.check_box_4 = QtWidgets.QCheckBox('底层IK控制器')
        # self.label_4 = QtWidgets.QLabel('底层IK控制器数量倍率:')
        # self.line_edit_5 = QtWidgets.QLineEdit('1')
        # self.line_edit_5.setFixedWidth(50)
        # self.slider_3 = QtWidgets.QSlider(Qt.Horizontal)
        # self.slider_3.setMinimum(1)
        # self.slider_3.setMaximum(10)

        self.check_box_5 = QtWidgets.QCheckBox('拉伸')
        self.check_box_6 = QtWidgets.QCheckBox('收缩')

        self.label_5 = QtWidgets.QLabel('双向fk控制器倍率:')
        self.line_edit_6 = QtWidgets.QLineEdit('0')
        self.line_edit_6.setFixedWidth(50)
        self.slider_4 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_4.setMinimum(1)
        self.slider_4.setMaximum(10)

        self.check_box_7 = QtWidgets.QCheckBox('拖拽控制器')

        self.button_9 = QtWidgets.QPushButton('创建')
        self.button_9.setStyleSheet('color:rgb(0,0,0);background:rgb(255,102,102)')

        self.button_11 = QtWidgets.QPushButton('删除')
        self.button_11.setStyleSheet('color:rgb(0,0,0);background:rgb(80,80,80)')
        self.button_11.setEnabled(False)

        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(['底层单向FK', '底层反向FK'])

        self.button_12 = QtWidgets.QPushButton('补充fk控制器')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        main_layout.addWidget(self.comboBox_0)
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)

        h_Box_layout_1.addWidget(self.button_1)
        h_Box_layout_1.addWidget(self.button_2)
        h_Box_layout_1.addWidget(self.button_3)

        # main_layout.addWidget(self.button_4)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_2)
        h_Box_layout_2.addWidget(self.line_edit_1)
        h_Box_layout_2.addWidget(self.slider_1)
        h_Box_layout_2.addWidget(self.button_4)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.label_1)
        h_Box_layout_3.addWidget(self.line_edit_2)
        h_Box_layout_3.addWidget(self.button_5)

        main_layout.addWidget(self.button_6)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.label_2)
        h_Box_layout_4.addWidget(self.line_edit_3)
        h_Box_layout_4.addWidget(self.button_7)
        h_Box_layout_4.addWidget(self.button_10)

        h_Box_layout_10 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_10)
        h_Box_layout_10.addWidget(self.line_edit_7)
        h_Box_layout_10.addWidget(self.button_8)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_6)
        h_Box_layout_6.addWidget(self.label_3, stretch=0)
        h_Box_layout_6.addWidget(self.line_edit_4, stretch=0)
        h_Box_layout_6.addWidget(self.slider_2, stretch=1)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.check_box_1)



        h_Box_layout_10 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_10)



        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        # h_Box_layout_10.addLayout(h_Box_layout_7)
        # h_Box_layout_7.addWidget(self.label_4, stretch=0)
        # h_Box_layout_7.addWidget(self.line_edit_5, stretch=0)
        # h_Box_layout_7.addWidget(self.slider_3, stretch=1)

        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.check_box_5)
        main_layout.addWidget(self.check_box_6)



        # h_Box_layout_9 = QtWidgets.QHBoxLayout(self)
        # main_layout.addLayout(h_Box_layout_9)
        # h_Box_layout_9.addWidget(self.label_5, stretch=0)
        # h_Box_layout_9.addWidget(self.line_edit_6, stretch=0)
        # h_Box_layout_9.addWidget(self.slider_4, stretch=1)
        # main_layout.addStretch(0)

        main_layout.addWidget(self.check_box_7)
        main_layout.addWidget(self.button_9)
        main_layout.addWidget(self.button_11)

        main_layout.addWidget(self.comboBox_1)
        main_layout.addWidget(self.button_12)




    def create_connect(self):
        self.comboBox_0.currentIndexChanged.connect(self.get_rope_template)
        self.button_1.clicked.connect(self.create_test)
        self.button_2.clicked.connect(self.others_library.establishing_a_bone_chain_at_the_midline)
        self.button_3.clicked.connect(self.others_library.joint_transformation_curve)
        self.line_edit_1.textChanged.connect(lambda: self.adjusting_the_number_of_sliding_controllers(self.slider_1,self.line_edit_1,1))
        self.slider_1.valueChanged.connect(lambda: self.create_joint_num(self.slider_1,self.line_edit_1,1))
        self.button_4.clicked.connect(lambda: self.others_library.generate_bone_chain(int(self.line_edit_1.text())))
        self.button_5.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))
        self.button_6.clicked.connect(self.correct_bone_orientation)
        self.button_7.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))
        self.button_10.clicked.connect(self.convert_to_bezier_curve)
        self.button_8.clicked.connect(self.create_positioning_loc)
        self.line_edit_4.textChanged.connect(lambda: self.adjusting_the_number_of_sliding_controllers(self.slider_2, self.line_edit_4, 0))
        self.slider_2.valueChanged.connect(lambda: self.create_joint_num(self.slider_2, self.line_edit_4, 0))
        # self.line_edit_5.textChanged.connect(lambda: self.adjusting_the_number_of_sliding_controllers(self.slider_3, self.line_edit_5, 1))
        # self.slider_3.valueChanged.connect(lambda: self.create_joint_num(self.slider_3, self.line_edit_5, 1))
        self.line_edit_6.textChanged.connect(lambda: self.adjusting_the_number_of_sliding_controllers(self.slider_4, self.line_edit_6, 1))
        self.slider_4.valueChanged.connect(lambda: self.create_joint_num(self.slider_4, self.line_edit_6, 1))




        self.button_9.clicked.connect(self.create_rope)
        self.button_11.clicked.connect(self.delete_rope)

        self.button_12.clicked.connect(self.create_positive_direction_fk)

    # 按样条创建骨骼链
    def create_joint_num(self,slider,line_edit,min):
        num = self.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(slider, 'QSlider')
        line_edit.setText(str(num))
        if num < min:
            line_edit.setText(str(min))
            slider.setValue(min)
            slider.setMinimum(min)
        if num > 1000000:
            line_edit.setText('1000000')
            slider.setValue(1000000)
            slider.setMaximum(1000000)

    # 调整滑动控制器数量
    def adjusting_the_number_of_sliding_controllers(self,slider,line_edit,min):
        num = int(line_edit.text())
        if num<min:
            num = min
            slider.setValue(num)
            slider.setMinimum(min)
        line_edit.setText(str(num))
        num = self.ui_edit.give_the_value_to_the_slider(num, slider, 'QSlider')

    # 矫正骨骼朝向
    @Withdraw
    def correct_bone_orientation(self):
        sel_joint = cmds.ls(sl=1,type='joint')
        if sel_joint:
            cmds.makeIdentity(sel_joint, apply=True, rotate=True, translate=False, scale=False)
            cmds.joint(sel_joint, e=1, oj='xyz', secondaryAxisOrient='xup', ch=0, zso=1)
            # 选择层次
            cmds.SelectHierarchy(sel_joint, allDescendents=True)
            sel_joint = cmds.ls(sl=1,type='joint')
            cmds.delete(cmds.orientConstraint(sel_joint[-2], sel_joint[-1]))
        joint = self.line_edit_2.text()
        if cmds.objExists(joint):
            cmds.select(joint)
        joint = cmds.ls(sl=1,type='joint')
        if joint:
            cmds.makeIdentity(joint, apply=True, rotate=True, translate=False, scale=False)
            cmds.joint(joint, e=1, oj='xyz', secondaryAxisOrient='xup', ch=0, zso=1)
            # 选择层次
            cmds.SelectHierarchy(joint, allDescendents=True)
            joint = cmds.ls(sl=1, type='joint')
            cmds.delete(cmds.orientConstraint(joint[-2], joint[-1]))

    # 转换成贝塞尔曲线
    @Withdraw
    def convert_to_bezier_curve(self):
        curve = self.line_edit_3.text()
        if cmds.objExists(curve):
            cmds.select(curve)
        curve = cmds.ls(sl=1)
        if curve:
            shape = cmds.listRelatives(curve, s=1)
            if shape:
                cmds.NurbsCurveToBezier(curve)

    # 生成朝向骨骼
    @Withdraw
    def create_positioning_loc(self):
        joint = self.line_edit_7.text()
        if cmds.objExists(joint):
            cmds.select(joint)
        joint = cmds.ls(sl=1, type='joint')
        if not joint:
            Curve = self.line_edit_3.text()
            if Curve:
                cmds.select(Curve + '.cv[*]')
                CurvePoint = cmds.ls(sl=1, fl=1)  # 加载样条点
                CurvePoint.append(CurvePoint[-1])
                Joint = []
                for i in range(0,len(CurvePoint)):
                    cmds.select(CurvePoint[i])
                    Cluster = cmds.cluster()
                    cmds.select(cl=1)
                    joint = cmds.joint(p=(0,0,0))
                    Joint.append(joint)
                    cmds.setAttr((joint + ".displayLocalAxis"), 1)
                    cmds.delete(cmds.pointConstraint(Cluster[1], joint, w=1))
                    cmds.delete(Cluster)
                cmds.setAttr((joint + ".v"), 0)
                for i in range(1,len(CurvePoint)):
                    cmds.parent(Joint[i],Joint[i-1])
                cmds.select(Joint[0])
                cmds.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='zup')
                cmds.curve(p=[(0, 0, 0), (0, 0, 1)], k=[0, 1], d=1)
                ClusterCurve = cmds.ls(sl=1)
                cmds.rebuildCurve(ClusterCurve[0], rt=0, ch=1, end=1, d=1, kr=0, s=(len(CurvePoint)-1), kcp=0, tol=0, kt=0, rpo=1, kep=0)
                cmds.select(ClusterCurve[0] + '.cv[*]')
                ClusterCurvePoint = cmds.ls(sl=1, fl=1)  # 加载样条点
                for i in range(0,len(ClusterCurvePoint)):
                    cmds.select(ClusterCurvePoint[i])
                    Cluster = cmds.cluster()
                    cmds.delete(cmds.pointConstraint(Joint[i],Cluster[1],w=1))
                cmds.select(ClusterCurve)
                cmds.DeleteHistory()
                cmds.delete(cmds.ikHandle(sj=Joint[0], ee=Joint[-1], c=ClusterCurve[0], ccv=False, sol='ikSplineSolver'))
                cmds.delete(ClusterCurve)
                cmds.warning('已经生成完朝向骨骼。')
                self.line_edit_7.setText(Joint[0])
            else:
                cmds.warning('样条不存在')
        else:
            self.line_edit_7.setText(joint[0])

    # 获取当前场景所有绳子,修改UI
    def get_rope_num(self):
        rope = cmds.ls('All_rope_sys_Grp*')
        all_rope_num = []
        if rope:
            max_num = int(rope[-1][16:])+1
            for i in range(max_num+1):
                all_rope_num.append(str(i))
        else:
            all_rope_num = ['0']
        self.comboBox_0.addItems(all_rope_num)

    # 获取当前查询的模板，按模板记录的属性修改创建数值
    def get_rope_template(self):
        top_num = self.comboBox_0.currentText()
        obj = cmds.objExists('All_rope_sys_Grp'+top_num)
        self.line_edit_2.setText('')
        self.line_edit_3.setText('')
        self.line_edit_7.setText('')
        self.check_box_1.setChecked(0)
        self.check_box_5.setChecked(0)
        self.check_box_6.setChecked(0)
        self.check_box_7.setChecked(0)
        self.line_edit_4.setText('0')
        # self.button_9.setVisible(1)
        # self.button_10.setVisible(0)
        self.button_9.setStyleSheet('color:rgb(0,0,0);background:rgb(225,102,102)')
        self.button_9.setEnabled(True)
        self.button_11.setStyleSheet('color:rgb(0,0,0);background:rgb(80,80,80)')
        self.button_11.setEnabled(False)
        if obj:
            obj = ('All_rope_sys_Grp' + top_num)
            if cmds.objExists(obj + '.root_skeleton'):
                text = cmds.getAttr(obj + '.root_skeleton')
                self.line_edit_2.setText(text)
            if cmds.objExists(obj + '.curve'):
                text = cmds.getAttr(obj + '.curve')
                self.line_edit_3.setText(text)
            if cmds.objExists(obj + '.con_toward'):
                text = cmds.getAttr(obj + '.con_toward')
                self.line_edit_7.setText(text)
            if cmds.objExists(obj + '.independence_con'):
                text = cmds.getAttr(obj + '.independence_con')
                if text == 'True':
                    self.check_box_1.setChecked(1)
            if cmds.objExists(obj + '.stretch'):
                text = cmds.getAttr(obj + '.stretch')
                if text == 'True':
                    self.check_box_5.setChecked(1)

            if cmds.objExists(obj + '.slide'):
                text = cmds.getAttr(obj + '.slide')
                if text == 'True':
                    self.check_box_6.setChecked(1)

            if cmds.objExists(obj + '.drag'):
                text = cmds.getAttr(obj + '.drag')
                if text == 'True':
                    self.check_box_7.setChecked(1)

            if cmds.objExists(obj + '.slide_scale'):
                text = cmds.getAttr(obj + '.slide_scale')
                self.line_edit_4.setText(text)

            self.button_9.setStyleSheet('color:rgb(0,0,0);background:rgb(80,80,80)')
            self.button_9.setEnabled(False)
            self.button_11.setStyleSheet('color:rgb(0,0,0);background:rgb(102,225,102)')
            self.button_11.setEnabled(True)

    # 记录创建时候的数值并添加属性记录
    def record_rope_template(self):
        top_num = self.comboBox_0.currentText()
        obj = cmds.objExists('All_rope_sys_Grp'+top_num)
        if obj:
            obj = ('All_rope_sys_Grp' + top_num)

            if not cmds.objExists(obj + '.root_skeleton'):
                cmds.addAttr(obj, ln='root_skeleton', dt='string')
            text = self.line_edit_2.text()
            cmds.setAttr(obj + '.root_skeleton', text, type='string')

            if not cmds.objExists(obj + '.curve'):
                cmds.addAttr(obj, ln='curve', dt='string')
            text = self.line_edit_3.text()
            cmds.setAttr(obj + '.curve', text, type='string')

            if not cmds.objExists(obj + '.con_toward'):
                cmds.addAttr(obj, ln='con_toward', dt='string')
            text = self.line_edit_7.text()
            cmds.setAttr(obj + '.con_toward', text, type='string')

            if not cmds.objExists(obj + '.independence_con'):
                cmds.addAttr(obj, ln='independence_con', dt='string')
            text = self.check_box_1.isChecked()
            cmds.setAttr(obj + '.independence_con', text, type='string')

            if not cmds.objExists(obj + '.stretch'):
                cmds.addAttr(obj, ln='stretch', dt='string')
            text = self.check_box_5.isChecked()
            cmds.setAttr(obj + '.stretch', text, type='string')

            if not cmds.objExists(obj + '.slide'):
                cmds.addAttr(obj, ln='slide', dt='string')
            text = self.check_box_6.isChecked()
            cmds.setAttr(obj + '.slide', text, type='string')

            if not cmds.objExists(obj + '.drag'):
                cmds.addAttr(obj, ln='drag', dt='string')
            text = self.check_box_6.isChecked()
            cmds.setAttr(obj + '.drag', text, type='string')

            if not cmds.objExists(obj + '.slide_scale'):
                cmds.addAttr(obj, ln='slide_scale', dt='string')
            text = self.line_edit_4.text()
            cmds.setAttr(obj + '.slide_scale', text, type='string')

    # 开始创建
    @Withdraw
    def create_rope(self):
        controller_orientation_joint = self.line_edit_7.text()
        if cmds.objExists(controller_orientation_joint):
            cmds.select(controller_orientation_joint)
            cmds.SelectHierarchy()
            # 控制器位置和朝向骨骼
            self.controller_orientation_joint = cmds.ls(sl=1)
            # 样条
            self.base_curve = self.line_edit_3.text()
            joint_chain = self.line_edit_2.text()
            cmds.select(joint_chain)
            cmds.SelectHierarchy()
            # 获取骨骼
            self.joint_chain = cmds.ls(sl=1,type='joint')
            self.top_num = int(self.comboBox_0.currentText())
            # 顶样条名称
            self.top_curve = 'Rope_TotalControl_'+str(self.top_num)+'_Curve'
            curve = self.curve.create_curve(self.library_path + '\curve_library', '四边方向箭')
            cmds.rename(curve, self.top_curve)
            self.top_curve = cmds.ls(sl=1)
            self.curve.change_curve_color('Index', self.top_curve, [0, 0, 0], 13)
            scale = 1.0
            self.controller.modify_vontroller_shape('scale', scale, scale, scale)
            self.controller.rotation_controller('Z')
            cmds.group(self.top_curve, n=self.top_curve[0] + '_Grp2')
            top_grp = cmds.group(n=self.top_curve[0] + '_Grp1')

            self.All_rope_sys_Grp = cmds.group(n='All_rope_sys_Grp' + str(self.top_num), em=1)
            self.record_rope_template()
            cmds.parent(top_grp, self.All_rope_sys_Grp)
            cmds.delete(cmds.parentConstraint(self.controller_orientation_joint[-2], top_grp))

            # 创建蒙皮骨骼
            top_joint, all_skin_joint = self.create_skin_joint()
            cmds.parent(top_joint, self.All_rope_sys_Grp)
            # 创建输出约束对象
            out_obj = all_skin_joint
            # 创建独立控制器
            independent_grp, all_independent_top_grp, all_independent_cur, all_independent_joint = [], [], [], []
            if self.check_box_1.isChecked():
                independent_grp, all_independent_top_grp, all_independent_cur, all_independent_joint = self.create_independent_con()
            # 如果独立控制器存在，则约束蒙皮骨骼
            if all_independent_joint:
                cmds.parent(independent_grp, self.All_rope_sys_Grp)
                for i in range(len(all_skin_joint)):
                    cmds.parentConstraint(all_independent_joint[i], out_obj[i])
                    cmds.scaleConstraint(all_independent_joint[i], out_obj[i])
            if all_independent_top_grp:
                out_obj = all_independent_top_grp

            '''
            # 创建底层FK
            fk_type = self.comboBox_1.currentIndex()
            all_fk_top_grp_list, all_curve_list, all_fk_joint, all_fk_loc = [], [], [], []
            if fk_type > 0:
                all_fk_top_grp_list, all_curve_list, all_fk_joint, all_fk_loc = self.create_positive_direction_fk(fk_type)
                # 列表排列始终保持正向，但是父化顺序可能反向
            # 如果FK控制器存在，且存在独立控制器则约束控制器，则约束独立控制器
            if all_fk_joint:
                for i in range(len(all_fk_joint)):
                    cmds.parentConstraint(all_fk_joint[i], out_obj[i])
            # # 如果FK控制器存在，不存在独立控制器则约束控制器，则约束蒙皮骨骼
            # if all_fk_joint and not all_independent_top_grp:
            #     for i in range(len(all_fk_joint)):
            #         cmds.parentConstraint(all_fk_joint[i], all_skin_joint[i])
            if all_fk_loc:
                out_obj = all_fk_loc
            '''

            # 创建骨骼实际位置传递骨骼
            actual_position_joint, all_position_out_joint, all_rotate_joint = self.create_actual_position_joint()
            # 传统ik骨骼父对象约束实际位置骨骼
            for i in range(len(self.joint_chain)):
                cmds.parentConstraint(self.joint_chain[i], actual_position_joint[i])

            # 创建底层ik控制器样条
            new_curve = cmds.duplicate(self.base_curve, rr=True)
            # 获取底层IK控制器倍率
            # ik_con_magnification = int(self.line_edit_5.text())
            # # print(ik_con_magnification)
            # if ik_con_magnification > 1:
            #     for i in range(ik_con_magnification - 1):
            #         cmds.select(new_curve)
            #         cmds.BezierCurveToNurbs()
            #         commend = self.curve.return_curve_command(new_curve)
            #         cmds.delete(new_curve)
            #         new_curve = mel.eval(commend)
            #         cmds.rebuildCurve(new_curve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=4, d=3, tol=0.01)
            #         cmds.select(new_curve)
            #         cmds.NurbsCurveToBezier()
            new_curve = cmds.rename(new_curve, 'ik_con_' + str(self.top_num) + '_Curve')
            cmds.select(new_curve)
            new_curve = cmds.ls(sl=1)

            # 创建滑动缩放控制器

            rotate_out_obj = all_skin_joint
            if all_independent_joint:
                rotate_out_obj = all_independent_top_grp

            # 创建底层IK控制器
            ik_long_curve_copy ,ik_all_top_grp, all_ik_top_grp, ik_all_con_joint, IK, path_constraint, ik_all_curve, all_rotate_curve = self.create_base_ik_con(new_curve, all_position_out_joint)
            all_need_delete_parentConstraint = []
            for soure, target in zip(ik_all_curve, all_position_out_joint):
                need_delete_parentConstraint = cmds.parentConstraint(soure, target)
                all_need_delete_parentConstraint.append(need_delete_parentConstraint)
            all_need_delete_parentConstraint = all_need_delete_parentConstraint[::3]
            for parentConstraint in all_need_delete_parentConstraint:
                cmds.delete(parentConstraint)
            parentConstraint_all_position_out_joint = all_position_out_joint[::3]
            for curve, joint in zip(all_rotate_curve, parentConstraint_all_position_out_joint):
                cmds.parentConstraint(curve, joint)
            cmds.skinCluster(all_position_out_joint, new_curve[0], mi=1)
            cmds.parent(ik_all_top_grp, self.All_rope_sys_Grp)



            # ik_all_curve = ik_all_curve[::3]
            all_joint_nearestPointOnCurve = self.create_slide_con(new_curve, actual_position_joint, all_rotate_joint, parentConstraint_all_position_out_joint, all_rotate_curve)
            for soure, target in zip(all_rotate_joint, out_obj):
                cmds.parentConstraint(soure, target)

            # 添加拉伸
            if self.check_box_5.isChecked():
                self.create_stretch(new_curve, ik_long_curve_copy, all_position_out_joint, all_skin_joint, all_independent_top_grp)

            # 创建滑动缩放控制器
            self.slide_con_num = int(self.line_edit_4.text())
            if self.slide_con_num > 0:
                self.add_slide_scale_con(self.slide_con_num, all_skin_joint, all_joint_nearestPointOnCurve, all_independent_top_grp, new_curve)

            # 添加收缩
            if self.check_box_6.isChecked():
                self.slide(path_constraint)

            # 添加仅IK约束
            cmds.parentConstraint(self.top_curve, ik_all_top_grp, mo=1)
            cmds.scaleConstraint(self.top_curve, ik_all_top_grp)

            # 按需求添加约束
            # for soure, target in zip(all_rotate_joint, all_fk_loc):
            #     cmds.parentConstraint(soure, target)

                # cmds.dgdirty(a=True)

            # # 按动态权重给动控制器添加约束
            # for soure, target in zip(ik_all_con_joint,all_rotate_joint):
            #     cmds.orientConstraint(soure, target, mo=1, skip=['y', 'z'], weight=1)
            self.drag(all_ik_top_grp)

            # 滑动缩放控制器有fk的情况添加旋转
            self.comboBox_0.addItems(str(self.comboBox_0.count()))
            # cmds.select(self.top_curve)
            self.get_rope_template()
            cmds.select(self.top_curve)
        else:
            cmds.warning('请生成控制器朝向骨骼。')

    # 删除当前绳子
    def delete_rope(self):
        top_num = self.comboBox_0.currentText()
        obj = ('All_rope_sys_Grp' + top_num)

        if cmds.objExists(obj + '.root_skeleton'):
            text = cmds.getAttr(obj + '.root_skeleton')
            cmds.parent(text, w=True)
        if cmds.objExists(obj + '.curve'):
            text = cmds.getAttr(obj + '.curve')
            cmds.parent(text, w=True)
        if cmds.objExists(obj + '.con_toward'):
            text = cmds.getAttr(obj + '.con_toward')
            cmds.parent(text, w=True)

        cmds.delete(obj)
        self.get_rope_template()

    # 创建蒙皮骨骼
    def create_skin_joint(self):
        # 创建输出骨骼
        all_skin_joint = []
        cmds.select(cl=1)
        top_joint = cmds.joint(n='all_rope_'+str(self.top_num)+'_skin_joint')
        cmds.setAttr(top_joint+'.drawStyle', 2)
        # all_skin_joint.append(top_joint)
        for joint in self.joint_chain:
            cmds.select(cl=1)
            joint_out_skin = cmds.joint(n=joint + '_out_skin')
            cmds.delete(cmds.parentConstraint(joint, joint_out_skin))
            cmds.parent(joint_out_skin, top_joint)
            cmds.makeIdentity(
                joint_out_skin,
                apply=True,  # 应用变换到顶点位置
                translate=True,  # 重置平移属性
                rotate=True,  # 重置旋转属性
                scale=True,  # 重置缩放属性
            )
            all_skin_joint.append(joint_out_skin)
        return top_joint, all_skin_joint

    # 创建独立控制器
    def create_independent_con(self):
        all_top_grp = []
        all_cur = []
        all_joint = []
        prefix = 'independent_con_'
        grp = cmds.group(em=1, n=prefix + str(self.top_num) + '_all_Grp')
        for i in range(len(self.joint_chain)):
            curve = self.curve.create_curve(self.library_path + '\curve_library', '正方形')
            cmds.rename(curve, prefix + str(self.top_num) + '_Curve_' + str(i))
            curve = cmds.ls(sl=1)
            all_cur.append(curve)
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 18)
            self.controller.modify_vontroller_shape('scale', 1.0, 1.0, 1.0)
            joint = cmds.joint(n=prefix + str(self.top_num) + '_joint_' + str(i))
            all_joint.append(joint)
            cmds.setAttr(joint + '.visibility', 0)
            # cmds.group(curve, n=prefix + str(self.top_num) + '_Curve_' + str(i) + '_Grp2')
            top_grp = cmds.group(n=prefix + str(self.top_num) + '_Curve_' + str(i) + '_Grp1',em=1)
            cmds.parent(curve, top_grp)
            all_top_grp.append(top_grp)
            cmds.parent(top_grp, grp)
            cmds.delete(cmds.parentConstraint(self.joint_chain[i], top_grp))
        # 添加独立控制器显示影藏
        # 添加显示影藏属性
        cmds.addAttr(self.top_curve, ln='independent_con', at='bool')
        cmds.setAttr(self.top_curve[0] + '.independent_con', e=1, keyable=1)
        cmds.connectAttr(self.top_curve[0] + '.independent_con', grp + '.visibility')
        return grp, all_top_grp, all_cur, all_joint

    # 创建单向fk
    @Withdraw
    def create_positive_direction_fk(self):
        direction = self.comboBox_1.currentIndex()
        top_num = int(self.comboBox_0.currentText())
        FK_con_all_grp = cmds.group(em=1, n='FK_con_all_Grp'+ str(top_num))
        all_independent_con = cmds.ls('independent_con_'+ str(top_num) +'_Curve_*_Grp1', type='transform',  fl=1)
        all_top_grp_list = []
        all_curve_list = []
        all_joint = []
        prefix = 'FK_con_'
        joint_list = self.line_edit_2.text()
        # 选择层次
        cmds.select(joint_list)
        joint_list = cmds.SelectHierarchy(allDescendents=True)
        joint_list = cmds.ls(sl=1, type='joint')
        all_loc = []
        # if direction == 2:
        #     joint_list = self.joint_chain[::-1]  # 步长-1反向遍历
        # print(joint_list)
        for i in range(len(joint_list)):
            curve = self.curve.create_curve(self.library_path + '\curve_library', '正方形')
            cmds.rename(curve, prefix + str(top_num) + '_Curve_' + str(i))
            curve = cmds.ls(sl=1)
            all_curve_list.append(curve)
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 20)
            self.controller.modify_vontroller_shape('scale', 1.4, 1.4, 1.4)
            joint = cmds.joint(n=prefix + str(top_num) + '_joint_' + str(i))
            all_joint.append(joint)
            cmds.setAttr(joint + '.visibility', 0)
            # cmds.group(curve, n=prefix + str(self.top_num) + '_Curve_' + str(i) + '_Grp2')
            top_grp = cmds.group(n=prefix + str(top_num) + '_Curve_' + str(i) + '_Grp1',em=1)
            cmds.parent(curve, top_grp)
            all_top_grp_list.append(top_grp)
            cmds.delete(cmds.parentConstraint(joint_list[i], top_grp))

        if direction == 1:
            all_top_grp_list = all_top_grp_list[::-1]  # 步长-1反向遍历
            all_curve_list = all_curve_list[::-1]  # 步长-1反向遍历

        for i in range(1, len(all_top_grp_list)):
            cmds.parent(all_top_grp_list[i], all_curve_list[i - 1])

        # 创建位移链接定位器
        for i in range(len(joint_list)):
            loc = cmds.spaceLocator(n=prefix + str(top_num) + '_Loc_' + str(i))
            cmds.delete(cmds.parentConstraint(joint_list[i], loc))
            all_loc.append(loc[0])

        if direction == 1:
            all_loc = all_loc[::-1]  # 步长-1反向遍历
        # print(all_loc)
        for i in range(1, len(all_loc)):
            cmds.parent(all_loc[i], all_loc[i - 1])
        for i in range(0, len(all_loc)):
            cmds.connectAttr(all_loc[i] + '.translate', all_top_grp_list[i] + '.translate')
            cmds.connectAttr(all_loc[i] + '.rotate', all_top_grp_list[i] + '.rotate')
            cmds.connectAttr(all_loc[i] + '.scale', all_top_grp_list[i] + '.scale')
        cmds.setAttr(all_loc[0] + '.visibility', 0)

        cmds.parent(all_top_grp_list[0], FK_con_all_grp)
        cmds.parent(all_loc[0], FK_con_all_grp)
        # print(all_curve_list)
        # return all_top_grp_list, all_curve_list, all_joint, all_loc
        # 约束定位器
        for i in range(len(all_loc)):
            cmds.parentConstraint(joint_list[i], all_loc[i])
            child = cmds.listRelatives(all_independent_con[i], c=True, type='parentConstraint')
            cmds.delete(child)
            cmds.parentConstraint(all_curve_list[i], all_independent_con[i], mo=False)
        top_curve = 'Rope_TotalControl_'+str(top_num)+'_Curve'
        cmds.parent(FK_con_all_grp, 'All_rope_sys_Grp'+str(top_num))

        cmds.addAttr(top_curve, ln='FK_con', at='bool')
        cmds.setAttr(top_curve + '.FK_con', e=1, keyable=1)
        cmds.connectAttr(top_curve + '.FK_con', FK_con_all_grp + '.visibility')
        cmds.setAttr(top_curve + '.FK_con', 1)




    # 添加滑动缩放控制器
    def add_slide_scale_con(self, slide_con_num, skin_joint, all_joint_nearestPointOnCurve, all_independent_top_grp, ik_curve):
        # 创建实际输出样条
        cmds.addAttr(self.top_curve[0], ln='slide_scale_con', min=0, max=int(slide_con_num), dv=0, at='long')
        cmds.setAttr((self.top_curve[0] + '.slide_scale_con'), e=1, keyable=True)
        slide_con_grp = cmds.group(n='slide_zoom_all_grp' + str(self.top_num), em=1)
        cmds.select(self.joint_chain[0])
        self.others_library.joint_transformation_curve()
        new_curve = cmds.ls(sl=1)
        cmds.setAttr(new_curve[0] + '.visibility', 0)
        new_curve = cmds.rename(new_curve, 'slide_zoom_' + str(self.top_num) + '_Curve')
        cmds.setAttr(new_curve + '.visibility', 0)
        cmds.rebuildCurve(new_curve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=0, kt=0, s=12, d=3, tol=0.01)
        cmds.select(new_curve)
        new_curve = cmds.ls(sl=1)
        curve_shape = cmds.listRelatives(ik_curve, s=1)
        cmds.skinCluster(self.joint_chain, new_curve, mi=1)
        # 创建滑动缩放控制器
        all_u_curve_grp = []
        for slide_controller_num in range(0, slide_con_num):
            self.curve_library.create_curve(self.curve_library_path, '圆片拉线')
            cmds.rename('slide_zoom_'+ str(self.top_num) +'_curve' + str(slide_controller_num))
            u_curve = cmds.ls(sl=1)
            self.controller.modify_vontroller_shape('scale', 5.0, 5.0, 5.0)
            self.curve_library.change_curve_color('Index', u_curve, [0, 0, 0], 20)

            u_curve_grp = cmds.group(n='slide_zoom_'+str(self.top_num)+'_curve_grp' + str(slide_controller_num), em=1)
            cmds.parent(u_curve[0], u_curve_grp)
            all_u_curve_grp.append(u_curve_grp)
            cmds.addAttr(u_curve[0], ln='uValue', min=0, max=100, dv=0, at='double')
            cmds.setAttr((u_curve[0] + '.uValue'), e=1, keyable=True)
            cmds.addAttr(u_curve[0], ln='slide_range', dv=50, min=0, at='double')
            cmds.setAttr((u_curve[0] + '.slide_range'), e=1, keyable=True)
            cmds.addAttr(u_curve[0], ln='slide_size', min=0, dv=1, at='double')
            cmds.setAttr((u_curve[0] + '.slide_size'), e=1, keyable=True)
            cmds.connectAttr((u_curve[0] + '.slide_size'), (u_curve_grp + '.scaleX'), f=1)
            cmds.connectAttr((u_curve[0] + '.slide_size'), (u_curve_grp + '.scaleY'), f=1)
            cmds.connectAttr((u_curve[0] + '.slide_size'), (u_curve_grp + '.scaleZ'), f=1)

            # 创建控制器显示影藏
            condition = cmds.createNode('condition')
            cmds.connectAttr((self.top_curve[0] + '.slide_scale_con'), (condition + '.firstTerm'))
            cmds.setAttr((condition + '.secondTerm'), slide_controller_num+1)
            cmds.setAttr((condition + '.operation'), 4)
            cmds.connectAttr(condition + '.outColorR', (u_curve_grp + '.visibility'))
            #########################
            path_constraint = self.others_library.path_constraint(ik_curve, u_curve_grp)
            cmds.setAttr(path_constraint + '.worldUpType', 1)
            cmds.connectAttr(self.top_curve[0]+'.xformMatrix', path_constraint + '.worldUpMatrix')

            cmds.setAttr(path_constraint + '.fractionMode', 0)
            u_curve_multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
            cmds.connectAttr((u_curve[0] + '.uValue'), (u_curve_multiplyDivide + '.input1X'), f=1)
            cmds.setAttr((u_curve_multiplyDivide + '.input2X'), 0.01)
            cmds.connectAttr((u_curve_multiplyDivide + '.outputX'), (path_constraint + '.uValue'), f=1)
            # 建立当前弧长
            now_arcLengthDimension = cmds.arcLengthDimension(curve_shape[0] + '.u[0.5]')
            cmds.connectAttr((u_curve_multiplyDivide + '.outputX'), (now_arcLengthDimension + '.uParamValue'), f=1)
            for i in range(0, len(self.joint_chain)):
                # 建立弧长
                arcLengthDimension = cmds.arcLengthDimension(curve_shape[0] + '.u[0.5]')
                cmds.connectAttr((all_joint_nearestPointOnCurve[i]+'.parameter'), (arcLengthDimension + '.uParamValue'))

                # 开始添加缩放计算
                plusMinusAverage = cmds.shadingNode('plusMinusAverage', asUtility=1)
                cmds.setAttr((plusMinusAverage + '.operation'), 2)
                cmds.connectAttr((now_arcLengthDimension + '.arcLength'), (plusMinusAverage + '.input1D[0]'), f=1)
                cmds.connectAttr((arcLengthDimension + '.arcLength'), (plusMinusAverage + '.input1D[1]'), f=1)

                imp_multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
                #################################################################################################
                multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
                cmds.setAttr((multiplyDivide + '.operation'), 2)
                cmds.connectAttr((u_curve[0] + '.slide_range'), (multiplyDivide + '.input1X'), f=1)
                cmds.connectAttr((self.top_curve[0] + '.scaleX'), (multiplyDivide + '.input2X'), f=1)
                cmds.connectAttr((multiplyDivide + '.outputX'), (imp_multiplyDivide + '.input1X'), f=1)
                # cmds.connectAttr((u_curve[0] + '.slide_range'), (imp_multiplyDivide + '.input1X'), f=1)
                #################################################################################################
                cmds.connectAttr((plusMinusAverage + '.output1D'), (imp_multiplyDivide + '.input2X'), f=1)

                out_multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
                cmds.connectAttr((u_curve[0] + '.slide_size'), (out_multiplyDivide + '.input1X'), f=1)
                # 创建驱动节点
                cmds.setDrivenKeyframe((out_multiplyDivide + '.input2X'),
                                       currentDriver=(imp_multiplyDivide + '.outputX'), dv=-100, v=0)
                cmds.setDrivenKeyframe((out_multiplyDivide + '.input2X'),
                                       currentDriver=(imp_multiplyDivide + '.outputX'), dv=0, v=1)
                cmds.setDrivenKeyframe((out_multiplyDivide + '.input2X'),
                                       currentDriver=(imp_multiplyDivide + '.outputX'), dv=100, v=0)
                # 获取最大值
                floatMath = cmds.shadingNode('floatMath', asUtility=1)
                cmds.setAttr((floatMath + '.operation'), 5)
                cmds.connectAttr((out_multiplyDivide + '.outputX'), (floatMath + '.floatA'), f=1)
                #
                # have_floatMath = cmds.listConnections((skin_joint[i] + '.scaleY'), d=False, s=True)
                if not all_independent_top_grp:
                    soure = cmds.listConnections((skin_joint[i] + '.scaleY'), p=1)
                else:
                    soure = cmds.listConnections((all_independent_top_grp[i] + '.scaleY'), p=1)
                cmds.connectAttr(soure[0], (floatMath + '.floatB'), f=1)
                if not all_independent_top_grp:
                    cmds.connectAttr((floatMath + '.outFloat'), (skin_joint[i] + '.scaleY'), f=1)
                    cmds.connectAttr((floatMath + '.outFloat'), (skin_joint[i] + '.scaleZ'), f=1)
                else:
                    cmds.connectAttr((floatMath + '.outFloat'), (all_independent_top_grp[i] + '.scaleY'), f=1)
                    cmds.connectAttr((floatMath + '.outFloat'), (all_independent_top_grp[i] + '.scaleZ'), f=1)
                # print(have_floatMath)
                # if have_floatMath:
                #     new_floatMath = []
                #     while have_floatMath:
                #         new_floatMath = have_floatMath
                #         have_floatMath = cmds.listConnections((have_floatMath[0] + '.floatB'), d=False, s=True)
                #     have_floatMath = new_floatMath
                #     cmds.connectAttr((floatMath + '.outFloat'), (have_floatMath[0] + '.floatB'), f=1)
                # else:
                #     cmds.connectAttr((floatMath + '.outFloat'), (skin_joint[i] + '.scaleY'), f=1)
                #     cmds.connectAttr((floatMath + '.outFloat'), (skin_joint[i] + '.scaleZ'), f=1)

        cmds.parent(all_u_curve_grp, new_curve, slide_con_grp)
        cmds.parent(slide_con_grp, self.All_rope_sys_Grp)

    # 创建额外旋转表达式
    def create_slide_con(self, new_curve, all_joint_out_skin, all_rotate_joint, all_position_out_joint, ik_all_curve):
        # print(ik_all_con_joint)
        # 创建骨骼滑动表达式
        # 获取所有点
        points = cmds.ls(new_curve[0] + '.cv[*]', fl=1)
        points = points[::3]
        ## 先获取每个点的u值
        all_point_u_num = []
        for i in range(len(ik_all_curve)):
            cmds.select(points[i])
            cluster = cmds.cluster()
            loc = cmds.spaceLocator()
            cmds.delete(cmds.parentConstraint(cluster, loc))
            cmds.delete(cluster)
            nearestPointOnCurve = cmds.createNode('nearestPointOnCurve')
            cmds.connectAttr(new_curve[0] + '.worldSpace[0]', nearestPointOnCurve + '.inputCurve')
            decomposeMatrix = cmds.createNode('decomposeMatrix')
            cmds.connectAttr(loc[0] + '.worldMatrix[0]', decomposeMatrix + '.inputMatrix')
            # cmds.connectAttr(ik_all_con_joint[i] + '.worldMatrix[0]', decomposeMatrix + '.inputMatrix')
            cmds.connectAttr(decomposeMatrix + '.outputTranslate', nearestPointOnCurve + '.inPosition')
            num = cmds.getAttr(nearestPointOnCurve + '.result.parameter')
            # text = nearestPointOnCurve + '.result.parameter'
            # all_point_u_num.append(text)
            all_point_u_num.append(num)
            cmds.delete(loc, nearestPointOnCurve, decomposeMatrix)
        # print(all_point_u_num)

        # 创建实时获取骨骼具体位置u值的节点
        all_joint_nearestPointOnCurve = []
        for i in range(len(all_joint_out_skin)):
            nearestPointOnCurve = cmds.createNode('nearestPointOnCurve')
            cmds.connectAttr(new_curve[0] + '.worldSpace[0]', nearestPointOnCurve + '.inputCurve')
            decomposeMatrix = cmds.createNode('decomposeMatrix')
            cmds.connectAttr(all_joint_out_skin[i] + '.worldMatrix[0]', decomposeMatrix + '.inputMatrix')
            cmds.connectAttr(decomposeMatrix + '.outputTranslate', nearestPointOnCurve + '.inPosition')
            all_joint_nearestPointOnCurve.append(nearestPointOnCurve)
        # print(all_joint_nearestPointOnCurve)

        # 添加表达式,统一获取控制器旋转数值，再获取当前骨骼u值在某个范围,然后计算权重乘以旋转数值
        # 按顺序获取u值
        text = '0.0'
        for i in range(1, len(all_point_u_num)-1):
            text = text + ',' + str(all_point_u_num[i])
        text = text + ',1.0'
        # 按顺序获取旋转数值
        rote_text = all_position_out_joint[0] + '.rotateX'
        for i in range(1, len(all_position_out_joint)):
            rote_text = rote_text + ',' + str(all_position_out_joint[i]) + '.rotateX'
        # 创建基础函数
        expression_txt = (
                'float $all_point_u_num_' + str(self.top_num) + '[] = {' + text + '};\n'
                'float $all_curve_rote_num_' + str(self.top_num) + '[] = {' + rote_text + '};\n'
                '//二分查找\n'
                'global proc int findFloatRange(float $targetNum, float $list[]) {\n'
                '    int $left = 0;\n'
                '    int $right = size($list) - 1;\n'
                '    while ($left <= $right) {\n'
                '        int $mid = ($left + $right) / 2;\n'
                '        float $midVal = $list[$mid];\n'
                '        if (($right-$left)<=1) {\n'
                '            return($left);\n'
                '        } else if ($midVal < $targetNum) {\n'
                '            $left = $mid;\n'
                '        } else {\n'
                '            $right = $mid;\n'
                '        }\n'
                '    }\n'
                '}\n'
                'global proc int nearSearch(float $targetNum, float $list[], int $position) {\n'
                '    if($list[$position]<=$targetNum && $list[$position+1]>=$targetNum){\n'
                '        return($position);\n'
                '    }else{\n'
                '        for($i=0;$i<size($list);$i++){\n'
                '            $position = $position+1;\n'
                '            if($list[$position]<=$targetNum && $list[$position+1]>=$targetNum){\n'
                '                return($position);\n'
                '            }\n'
                '        }\n'
                '    }\n'
                '}\n')

        an_num = '$' + all_joint_out_skin[0] + '_u_num'
        an_position = '$' + all_joint_out_skin[0] + '_position'
        an_weight = '$' + all_joint_out_skin[0] + '_weight'
        text = (
                'float ' + an_num + ' = ' + all_joint_nearestPointOnCurve[0] + '.result.parameter;\n'
                'int ' + an_position + ' = findFloatRange(' + an_num + ', $all_point_u_num_' + str(self.top_num) + ');\n'
                'float ' + an_weight + ' = smoothstep(0, 1,((' + an_num + '-$all_point_u_num_' + str(self.top_num) + '[' + an_position + '])/($all_point_u_num_' + str(self.top_num) + '[' + an_position + '+1]-$all_point_u_num_' + str(self.top_num) + '[' + an_position + '])));\n'
                '' + all_rotate_joint[0] + '.rotateX = $all_curve_rote_num_' + str(self.top_num) + '[' + an_position + ']*(1-' + an_weight + ')+$all_curve_rote_num_' + str(self.top_num) + '[' + an_position + '+1]*' + an_weight + ';\n'
        )
        add_text = text
        # expression_txt += add_text
        f_an_position = an_position
        for i in range(1,len(self.joint_chain)):
            an_num = '$' + all_joint_out_skin[i] + '_u_num'
            an_position = '$' + all_joint_out_skin[i] + '_position'
            an_weight = '$' + all_joint_out_skin[i] + '_weight'
            text = (
                    'float ' + an_num + ' = ' + all_joint_nearestPointOnCurve[i] + '.result.parameter;\n'
                    'int ' + an_position + ' = nearSearch('+an_num+', $all_point_u_num_' + str(self.top_num) + ', ' + f_an_position + ');\n'
                    'float ' + an_weight + ' = smoothstep(0, 1,((' + an_num + '-$all_point_u_num_' + str(self.top_num) + '[' + an_position + '])/($all_point_u_num_' + str(self.top_num) + '[' + an_position + '+1]-$all_point_u_num_' + str(self.top_num) + '[' + an_position + '])));\n'
                    '' + all_rotate_joint[i] + '.rotateX = $all_curve_rote_num_' + str(self.top_num) + '[' + an_position + ']*(1-' + an_weight + ')+$all_curve_rote_num_' + str(self.top_num) + '[' + an_position + '+1]*' + an_weight + ';\n'
            )
            add_text += text
            f_an_position = an_position
        expression_txt += add_text
        cmds.expression(s=expression_txt, ae=1, uc='all', o='', n=(self.base_curve + '_expression'))
        # 添加表达式开关
        cmds.addAttr(self.top_curve, ln='close_expression', at='bool')
        cmds.setAttr(self.top_curve[0] + '.close_expression', e=1, keyable=1, channelBox=True)
        condition = cmds.createNode('condition')
        cmds.connectAttr((self.top_curve[0] + '.close_expression'), (condition + '.firstTerm'))
        cmds.setAttr(condition + '.colorIfFalseR', 2)
        cmds.connectAttr((condition + '.outColorR'), (self.base_curve + '_expression.nodeState'))
        return all_joint_nearestPointOnCurve

    # 创建底层IK控制器
    def create_base_ik_con(self, new_curve, all_position_out_joint):
        top_grp_grp = cmds.group(n='ik_con_' + str(self.top_num) + '_All_Grp', em=True)
        all_top_grp = []
        cmds.DeleteHistory()
        # 开始按样条生成控制器
        scale = 2.0
        all_skin_joint = []
        all_curve = []
        cmds.addAttr(self.top_curve, ln='ik_con', at='bool')
        cmds.setAttr(self.top_curve[0] + '.ik_con', e=1, keyable=1)
        for i in range(len(self.controller_orientation_joint)):
            curve = self.curve.create_curve(self.library_path + '\curve_library', '十字星')
            cmds.rename(curve, 'ik_con_' + str(self.top_num) + '_Curve_'+str(i))
            curve = cmds.ls(sl=1)
            all_curve.append(curve[0])
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 18)
            self.controller.modify_vontroller_shape('scale', scale, scale, scale)
            joint = cmds.joint(n='ik_con_' + str(self.top_num) + '_joint_'+str(i))
            cmds.setAttr(joint + '.visibility', 0)
            cmds.group(curve, n='ik_con_' + str(self.top_num) + '_Curve_' + str(i) + '_Grp2')
            base_ik_top_grp = cmds.group(n='ik_con_' + str(self.top_num) + '_Curve_' + str(i) + '_Grp1')
            cmds.delete(cmds.parentConstraint(self.controller_orientation_joint[i], base_ik_top_grp))
            all_skin_joint.append(joint)
            cmds.parent(base_ik_top_grp, top_grp_grp)
            all_top_grp.append(base_ik_top_grp)
        # cmds.skinCluster(all_skin_joint, new_curve[0], mi=1)
        # 创建父化
        # 创建输出骨骼
        # all_joint_out_skin = []
        # for joint in self.joint_chain:
        #     cmds.select(cl=1)
        #     joint_out_skin = cmds.joint(n=joint + '_out_skin')
        #     cmds.pointConstraint(joint, joint_out_skin)
        #     cmds.orientConstraint(joint, joint_out_skin, offset=(0, 0, 0), skip='x', weight=1)
        #     all_joint_out_skin.append(joint_out_skin)
        # # 创建骨骼滑动表达式
        # ## 先获取每个点的u值
        # all_point_u_num = []
        # for i in range(len(points)):
        #     cmds.select(points[i])
        #     cluster = cmds.cluster()
        #     loc = cmds.spaceLocator()
        #     cmds.delete(cmds.parentConstraint(cluster, loc))
        #     cmds.delete(cluster)
        #     nearestPointOnCurve = cmds.createNode('nearestPointOnCurve')
        #     cmds.connectAttr(new_curve[0]+'.worldSpace[0]', nearestPointOnCurve+'.inputCurve')
        #     decomposeMatrix = cmds.createNode('decomposeMatrix')
        #     cmds.connectAttr(loc[0]+'.worldMatrix[0]', decomposeMatrix+'.inputMatrix')
        #     cmds.connectAttr(decomposeMatrix+'.outputTranslate', nearestPointOnCurve+'.inPosition')
        #     num = cmds.getAttr(nearestPointOnCurve+'.result.parameter')
        #     all_point_u_num.append(num)
        #     cmds.delete(loc, nearestPointOnCurve, decomposeMatrix)
        # print(all_point_u_num)
        #
        # # 创建实时获取骨骼具体位置u值的节点
        # all_joint_nearestPointOnCurve = []
        # for i in range(len(all_joint_out_skin)):
        #     nearestPointOnCurve = cmds.createNode('nearestPointOnCurve')
        #     cmds.connectAttr(new_curve[0] + '.worldSpace[0]', nearestPointOnCurve + '.inputCurve')
        #     decomposeMatrix = cmds.createNode('decomposeMatrix')
        #     cmds.connectAttr(all_joint_out_skin[i] + '.worldMatrix[0]', decomposeMatrix + '.inputMatrix')
        #     cmds.connectAttr(decomposeMatrix + '.outputTranslate', nearestPointOnCurve + '.inPosition')
        #     all_joint_nearestPointOnCurve.append(nearestPointOnCurve)
        # print(all_joint_nearestPointOnCurve)
        #
        # # 添加表达式,统一获取控制器旋转数值，再获取当前骨骼u值在某个范围,然后计算权重乘以旋转数值
        # # 按顺序获取u值
        # text = str(all_point_u_num[0])
        # for i in range(1, len(all_point_u_num)):
        #     text = text+','+str(all_point_u_num[i])
        # # 按顺序获取旋转数值
        # rote_text = all_curve[0]+'.rotateX'
        # for i in range(1, len(all_curve)):
        #     rote_text  = rote_text +','+str(all_curve[i])+'.rotateX'
        #
        # expression_txt = (
        #     'float $all_point_u_num_'+str(self.top_num)+'[] = {'+text+'};\n'
        #     'float $all_curve_rote_num_'+str(self.top_num)+'[] = {'+rote_text+'};\n'
        #     '//二分查找\n'
        #     'global proc int findFloatRange(float $targetNum, float $list[]) {\n'
        #     '    int $left = 0;\n'
        #     '    int $right = size($list) - 1;\n'
        #     '    while ($left <= $right) {\n'
        #     '        int $mid = ($left + $right) / 2;\n'
        #     '        float $midVal = $list[$mid];\n'
        #     '        if (($right-$left)<=1) {\n'
        #     '            return($left);\n'
        #     '        } else if ($midVal < $targetNum) {\n'
        #     '            $left = $mid;\n'
        #     '        } else {\n'
        #     '            $right = $mid;\n'
        #     '        }\n'
        #     '    }\n'
        #     '}\n')
        # add_text = ''
        # for i in range(len(self.joint_chain)):
        #     an_num = '$'+all_joint_out_skin[i]+'_u_num'
        #     an_position = '$'+all_joint_out_skin[i]+'_position'
        #     an_weight = '$'+all_joint_out_skin[i]+'_weight'
        #     text = (
        #         'float ' + an_num + ' = ' + all_joint_nearestPointOnCurve[i] + '.result.parameter;\n'
        #         'int '+an_position+' = findFloatRange('+an_num+', $all_point_u_num_'+str(self.top_num)+');\n'
        #         'float '+an_weight+' = (' + an_num + '-$all_point_u_num_'+str(self.top_num)+'['+an_position+'])/($all_point_u_num_'+str(self.top_num)+'['+an_position+'+1]-$all_point_u_num_'+str(self.top_num)+'['+an_position+']);\n'
        #         ''+all_joint_out_skin[i]+'.rotateX = $all_curve_rote_num_'+str(self.top_num)+'['+an_position+']*(1-'+an_weight+')+$all_curve_rote_num_'+str(self.top_num)+'['+an_position+'+1]*'+an_weight+';\n'
        #     )
        #     add_text += text
        # expression_txt += add_text
        # cmds.expression(s=expression_txt, ae=1, uc='all', o='', n=(self.base_curve + '_expression'))
        # 创建ik链并用定位器约束
        # 创建路径约束,用于跟随曲线


        path_constraint_loc = cmds.spaceLocator(n=('path_constraint_loc'+str(self.top_num)))
        cmds.setAttr((path_constraint_loc[0] + '.inheritsTransform'), 0)

        path_constraint = self.others_library.path_constraint(new_curve, path_constraint_loc[0])

        # 创建IK
        # print(self.joint_chain[-1])
        cmds.select(self.joint_chain[0], self.joint_chain[-1], new_curve)
        ik_sys = cmds.ikHandle(ccv=False, sol='ikSplineSolver', roc=False, pcv=False)
        IK = cmds.ls(sl=1)
        cmds.parent(ik_sys[-1], self.joint_chain[-1])
        cmds.parentConstraint(path_constraint_loc, self.joint_chain[0], w=1)

        # 父化
        scale = 1.3
        all_rotate_curve = []
        for i in range(0,len(all_curve),3):
            cmds.connectAttr(self.top_curve[0] + '.ik_con', all_top_grp[i] + '.visibility', f=1)
            self.curve.change_curve_color('Index', [all_curve[i]], [0, 0, 0], 17)
            curve = self.curve.create_curve(self.library_path + '\curve_library', '圆片')
            cmds.rename(curve, 'ik_con_' + str(self.top_num) + '_RotateCurve_' + str(i))
            curve = cmds.ls(sl=1)
            all_rotate_curve.append(curve[0])
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 20)
            self.controller.rotation_controller('Z')
            self.controller.modify_vontroller_shape('scale', scale, scale, scale)
            cmds.delete(cmds.parentConstraint(self.controller_orientation_joint[i], curve))
            cmds.parent(curve, all_curve[i])
            # 添加显示影藏的属性
            cmds.addAttr(all_curve[i], ln='secondary', at='bool')
            cmds.setAttr((all_curve[i] + '.secondary'), e=1, keyable=True)
            cmds.connectAttr((all_curve[i] + '.secondary'), (curve[0] + '.visibility'))
            cmds.setAttr(curve[0] + '.tx', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.ty', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.tz', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.ry', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.rz', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.sx', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.sy', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.sz', lock=True, keyable=False, channelBox=False)
            cmds.setAttr(curve[0] + '.visibility', keyable=False, channelBox=False)
            if i-1 > 0:
                cmds.parent(all_top_grp[i-1],all_curve[i])
                cmds.connectAttr((all_curve[i] + '.secondary'), (all_top_grp[i - 1] + '.visibility'))
            if i+1 < len(all_curve):
                cmds.parent(all_top_grp[i+1],all_curve[i])
                cmds.connectAttr((all_curve[i] + '.secondary'), (all_top_grp[i + 1] + '.visibility'))
        # 创建ik数据组
        joint_chain_grp = cmds.group(n='joint_chain_grp'+str(self.top_num))
        cmds.parent(self.joint_chain[0], joint_chain_grp)
        self.ik_grp = cmds.group(self.base_curve, new_curve, path_constraint_loc, IK, joint_chain_grp, self.controller_orientation_joint[0], n='ik_data_grp'+str(self.top_num))
        cmds.scaleConstraint(self.top_curve, joint_chain_grp, mo=1)
        cmds.parent(self.ik_grp, self.All_rope_sys_Grp)
        cmds.setAttr(self.ik_grp + '.visibility', 0)
        # cmds.setAttr(self.ik_grp + '.visibility', lock=1)
        # 添加IK优化开关
        cmds.addAttr(self.top_curve, ln='break', at='bool')
        cmds.setAttr(self.top_curve[0] + '.break', e=1, keyable=1, channelBox=True)
        for con in all_rotate_curve:
            cmds.connectAttr((self.top_curve[0] + '.break'), (con + '.displayLocalAxis'))
        condition = cmds.createNode('condition')
        cmds.connectAttr((self.top_curve[0] + '.break'), (condition + '.firstTerm'))
        cmds.setAttr(condition + '.colorIfFalseR', 2)
        # shape = cmds.listRelatives(new_curve, s=True)[0]
        # cmds.connectAttr((condition + '.outColorR'), (shape + '.nodeState'))

        long_curve_copy = cmds.duplicate(new_curve, rr=True)
        cmds.parent(long_curve_copy, self.All_rope_sys_Grp)
        cmds.setAttr(long_curve_copy[0] + '.template', 1)
        cmds.connectAttr((self.top_curve[0] + '.break'), (long_curve_copy[0] + '.visibility'))
        cmds.skinCluster(all_position_out_joint, long_curve_copy, mi=1)
        shape = cmds.listRelatives(long_curve_copy, s=True)[0]
        cmds.connectAttr((condition + '.outColorR'), (shape + '.nodeState'))
        shape = cmds.listRelatives(new_curve, s=True)[0]
        cmds.connectAttr((condition + '.outColorR'), (shape + '.nodeState'))

        # 创建位置输出骨骼
        return long_curve_copy, top_grp_grp, all_top_grp, all_skin_joint, IK, path_constraint, all_curve, all_rotate_curve

    # 创建实际位置输出骨骼
    def create_actual_position_joint(self):
        grp = cmds.group(n='actual_position_grp'+str(self.top_num), em=1)
        cmds.setAttr(grp + '.visibility', 0)
        cmds.parent(grp, self.All_rope_sys_Grp)
        grp2 = cmds.group(n='actual_position_rotate_grp' + str(self.top_num), em=1)
        cmds.setAttr(grp2 + '.visibility', 0)
        cmds.parent(grp2, self.All_rope_sys_Grp)
        all_joint = []
        all_rotate_joint = []
        all_out_joint = []
        i = 0
        for j in self.joint_chain:
            cmds.select(cl=1)
            ls_j = cmds.joint(n=(j+'_actual_position_joint'+str(i)), p=(0, 0, 0))
            ls_j2 = cmds.joint(n=(j + '_actual_position_rotate_joint'+str(i)), p=(0, 0, 0))

            cmds.delete(cmds.parentConstraint(j, ls_j, w=1))
            # 冻结变换
            cmds.makeIdentity(ls_j, apply=True, t=1, r=1, s=1)
            cmds.parent(ls_j, grp)

            all_joint.append(ls_j)
            all_rotate_joint.append(ls_j2)

            i += 1
        for j in self.controller_orientation_joint:
            ls_j3 = cmds.joint(n=(j + '_actual_position_out_joint'), p=(0, 0, 0))
            cmds.delete(cmds.parentConstraint(j, ls_j3, w=1))
            cmds.parent(ls_j3, grp2)
            cmds.makeIdentity(ls_j3, apply=True, rotate=True)

            all_out_joint.append(ls_j3)

        return all_joint, all_out_joint, all_rotate_joint

    # 创建拉伸
    def create_stretch(self, long_curve, long_curve_copy, all_position_out_joint, all_skin_joint, all_independent_top_grp):
        # 复制绳子做基础长度
        base_long_curve = cmds.duplicate(self.base_curve, rr=True)
        base_long_curve = cmds.rename(base_long_curve, 'ik_con_' + str(self.top_num) + '_base_Curve')
        cmds.parentConstraint(self.top_curve, base_long_curve, mo=True)
        cmds.scaleConstraint(self.top_curve, base_long_curve, mo=True)
        cmds.select(base_long_curve)
        base_long_curve = cmds.ls(sl=1)
        # cmds.parent(base_long_curve, self.ik_grp)
        base_long_curve_shape = cmds.listRelatives(base_long_curve, s=True)
        base_long_curve_arcLengthDimension = cmds.createNode('arcLengthDimension')
        cmds.setAttr(base_long_curve_arcLengthDimension+'.uParamValue', 1)
        cmds.connectAttr(base_long_curve_shape[0] + '.worldSpace[0]', base_long_curve_arcLengthDimension + '.nurbsGeometry')
        parent = cmds.listRelatives(base_long_curve_arcLengthDimension, p=1)
        cmds.parent(parent, base_long_curve)
        # base_long_curve_curveInfo = cmds.createNode('curveInfo')
        # cmds.connectAttr(base_long_curve_shape[0]+'.worldSpace[0]', base_long_curve_curveInfo+'.inputCurve')
        '''long_curve_copy = cmds.duplicate(long_curve, rr=True)
        cmds.parent(long_curve_copy, self.All_rope_sys_Grp)
        cmds.setAttr(long_curve_copy[0]+'.template', 1)
        cmds.connectAttr((self.top_curve[0] + '.break'), (long_curve_copy[0] + '.visibility'))'''
        # cmds.skinCluster(all_position_out_joint, long_curve_copy, mi=1)
        long_curve_shape = cmds.listRelatives(long_curve_copy, s=True)
        # long_curve_arcLengthDimension = cmds.arcLengthDimension(long_curve_shape[0] + '.u[1.0]')
        long_curve_arcLengthDimension = cmds.createNode('arcLengthDimension')
        cmds.setAttr(long_curve_arcLengthDimension + '.uParamValue', 1)
        cmds.connectAttr(long_curve_shape[0] + '.worldSpace[0]', long_curve_arcLengthDimension + '.nurbsGeometry')
        parent = cmds.listRelatives(long_curve_arcLengthDimension, p=1)
        cmds.parent(parent, long_curve_copy)
        # long_curve_curveInfo = cmds.createNode('curveInfo')
        # cmds.connectAttr(long_curve_shape[0] + '.worldSpace[0]', long_curve_curveInfo + '.inputCurve')
        self.multiplyDivide_stretch = cmds.createNode('multiplyDivide')
        # cmds.connectAttr(base_long_curve_curveInfo + '.arcLength', self.multiplyDivide_stretch + '.input2X')
        # cmds.connectAttr(long_curve_curveInfo + '.arcLength', self.multiplyDivide_stretch + '.input1X')
        cmds.connectAttr(base_long_curve_arcLengthDimension + '.arcLength', self.multiplyDivide_stretch + '.input2X')
        cmds.connectAttr(long_curve_arcLengthDimension + '.arcLength', self.multiplyDivide_stretch + '.input1X')

        cmds.setAttr(self.multiplyDivide_stretch+'.operation', 2)
        # 添加拉伸属性
        cmds.addAttr(self.top_curve, ln='stretch', at='bool')
        cmds.setAttr(self.top_curve[0] + '.stretch', e=1, keyable=1)
        condition = cmds.createNode('condition')
        cmds.setAttr(condition + '.secondTerm', 1)
        cmds.connectAttr(self.top_curve[0] + '.stretch', condition + '.firstTerm')
        cmds.connectAttr(self.multiplyDivide_stretch + '.outputX', condition + '.colorIfTrueR')
        # 添加强制拉伸属性
        cmds.addAttr(self.top_curve, ln='stretch_force',  at='double',  min=0, dv=1)
        cmds.setAttr(self.top_curve[0] + '.stretch_force', e=1, keyable=1)
        stretch_force_multiplyDivide = cmds.createNode('multiplyDivide')
        cmds.connectAttr(condition + '.outColorR', stretch_force_multiplyDivide + '.input2X')
        cmds.connectAttr(self.top_curve[0] + '.stretch_force', stretch_force_multiplyDivide + '.input1X')
        # 添加末端强制收起属性
        all_min_node = []
        cmds.addAttr(self.top_curve, ln='retract_end', at='double',  min=-1*(len(self.joint_chain))+1, dv=0, max=len(self.joint_chain)-1)
        cmds.setAttr(self.top_curve[0] + '.retract_end', e=1, keyable=1)
        # print(self.joint_chain)
        for i in range(1, len(self.joint_chain)):
            # num = cmds.getAttr(self.joint_chain[i] + '.tx')
            setRange = cmds.createNode('setRange')
            cmds.connectAttr(self.top_curve[0] + '.retract_end', setRange + '.valueX')
            cmds.setAttr(setRange + '.maxX', 1)
            # cmds.setAttr(setRange + '.minX', 1)
            cmds.setAttr(setRange + '.oldMinX', i*-1)
            cmds.setAttr(setRange + '.oldMaxX', i*-1+1)
            min_node = cmds.createNode('min')
            all_min_node.append(min_node)
            cmds.connectAttr(setRange + '.outValueX', min_node + '.input[0]')
            # cmds.connectAttr(min_node + '.output', self.joint_chain[i] + '.tx')

        # 反转列表
        # re_joint = self.joint_chain[::-1]
        re_all_min_node = all_min_node[::-1]
        for i in range(0,len(self.joint_chain)-1):
            # num = cmds.getAttr(re_joint[i]+'.tx')
            setRange = cmds.createNode('setRange')
            cmds.connectAttr(self.top_curve[0] + '.retract_end', setRange + '.valueX')
            cmds.setAttr(setRange + '.minX', 1)
            # if i == 0:
            #     cmds.setAttr(setRange + '.maxX', 1)
            cmds.setAttr(setRange + '.oldMinX', i)
            cmds.setAttr(setRange + '.oldMaxX', i+1)
            # soure_an = cmds.listConnections(re_joint[i] + '.tx', s=True,type = 'min')
            cmds.connectAttr(setRange + '.outValueX', re_all_min_node[i] + '.input[1]')

        for i in range(len(self.joint_chain)-1):
            multiplyDivide = cmds.createNode('multiplyDivide')
            cmds.connectAttr(stretch_force_multiplyDivide + '.outputX', multiplyDivide + '.input1X')
            cmds.connectAttr(all_min_node[i] + '.output', multiplyDivide + '.input2X')
            cmds.connectAttr(multiplyDivide + '.outputX', self.joint_chain[i] + '.scaleX')
            if not all_independent_top_grp:
                cmds.connectAttr(multiplyDivide + '.outputX', all_skin_joint[i] + '.scaleX')
            else:
                cmds.connectAttr(multiplyDivide + '.outputX', all_independent_top_grp[i] + '.scaleX')

        # 添加保持体积
        cmds.addAttr((self.top_curve), ln='Volume', min=0, max=10, dv=0, at='double')
        cmds.setAttr((self.top_curve[0] + '.Volume'), e=1, keyable=True)
        setRange = cmds.shadingNode('setRange', asUtility=1)
        cmds.connectAttr((self.top_curve[0] + '.Volume'), (setRange + '.valueX'), f=1)
        cmds.setAttr((setRange + '.oldMaxX'), 10)
        cmds.connectAttr((stretch_force_multiplyDivide + '.outputX'), (setRange + '.minX'), f=1)
        cmds.setAttr((setRange + '.maxX'), 1)
        multiplyDivide_vlume = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide_vlume + '.operation'), 2)
        cmds.connectAttr((setRange + '.outValueX'), (multiplyDivide_vlume + '.input1X'), f=1)
        cmds.connectAttr((stretch_force_multiplyDivide + '.outputX'), (multiplyDivide_vlume + '.input2X'), f=1)
        for i in range(0, len(self.joint_chain)):
            input_range = (0, len(self.joint_chain) - 1)  # 输入范围
            output_range = (0, math.radians(360))  # 输出范围
            input_min, input_max = input_range
            output_min, output_max = output_range
            # 检查输入值是否在输入范围内
            a = (i - input_min) * (output_max - output_min) / (input_max - input_min) + output_min
            cos_value = math.cos(a)
            value = ((cos_value + 1) / 2) * -1 + 1
            cmds.addAttr((all_skin_joint[i]), ln='Volume_num', min=0, max=1, dv=value, at='double')
            cmds.setAttr((all_skin_joint[i] + '.Volume_num'), e=1, keyable=True)
            setRange = cmds.shadingNode('setRange', asUtility=1)
            cmds.connectAttr((all_skin_joint[i] + '.Volume_num'), (setRange + '.valueX'), f=1)
            cmds.connectAttr((multiplyDivide_vlume + '.outputX'), (setRange + '.maxX'), f=1)
            cmds.setAttr((setRange + '.oldMaxX'), 1)
            cmds.setAttr((setRange + '.minX'), 1)

            if not all_independent_top_grp:
                cmds.connectAttr(setRange + '.outValueX', all_skin_joint[i] + '.scaleY')
                cmds.connectAttr(setRange + '.outValueX', all_skin_joint[i] + '.scaleZ')
            else:
                cmds.connectAttr(setRange + '.outValueX', all_independent_top_grp[i] + '.scaleY')
                cmds.connectAttr(setRange + '.outValueX', all_independent_top_grp[i] + '.scaleZ')

    # 添加强制收缩
    def slide(self, path_constraint):
        # 添加滑动属性
        cmds.addAttr(self.top_curve, ln='slide', at='double', min=0, dv=0,max=100)
        cmds.setAttr(self.top_curve[0] + '.slide', e=1, keyable=1)
        multiplyDivide = cmds.createNode('multiplyDivide')
        cmds.connectAttr(self.top_curve[0] + '.slide', multiplyDivide + '.input1X')
        cmds.setAttr(multiplyDivide + '.input2X', 0.01)
        cmds.connectAttr(multiplyDivide + '.outputX', path_constraint + '.uValue')

    # 创建拖拽
    def drag(self, all_ik_top_grp):
        # 创建拖拽样条
        all_point = cmds.ls(self.base_curve+'.cv[*]',fl=1)
        f_point = cmds.xform(all_point[0], q=True, t=True)
        e_point = cmds.xform(all_point[-1], q=True, t=True)
        # print(f_point, e_point)
        drag_curve = cmds.curve(n = 'Rope_drag'+str(self.top_num)+'_Curve',d=1, p=[(f_point[0], f_point[1], f_point[2]), (e_point[0], e_point[1], e_point[2])] )
        cmds.rebuildCurve(drag_curve, rt=0, ch=0, end=1, d=3, kr=0, s=5, kcp=0, tol=0, kt=0, rpo=1, kep=0)
        # 创建拖拽控制器
        scale = 4.0
        all_curve_point = cmds.ls(drag_curve + '.cv[*]',fl=1)
        # print(all_curve_point)
        # print(all_point)
        all_joint = []
        all_top_grp = []
        all_curve = []
        for i in range(len(all_curve_point)):
            cmds.select(all_curve_point[i])
            cluster = cmds.cluster()
            curve = self.curve.create_curve(self.library_path + '\curve_library', '正方形')
            cmds.rename(curve, 'drag_con_' + str(self.top_num) + '_Curve_' + str(i))
            curve = cmds.ls(sl=1)
            all_curve.append(curve[0])
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 18)
            self.controller.modify_vontroller_shape('scale', scale, scale, scale)
            joint = cmds.joint(n='drag_con_' + str(self.top_num) + '_joint_' + str(i))
            cmds.setAttr(joint + '.visibility', 0)
            # all_curve_point = cmds.ls(curve[0] + '.cv[*]')
            all_joint.append(joint)
            cmds.group(curve, n='drag_con_' + str(self.top_num) + '_Curve_' + str(i) + '_Grp2')
            base_drag_top_grp = cmds.group(n='drag_con_' + str(self.top_num) + '_Curve_' + str(i) + '_Grp1')
            all_top_grp.append(base_drag_top_grp)
            cmds.delete(cmds.pointConstraint(cluster, base_drag_top_grp))
            cmds.delete(cmds.orientConstraint(self.controller_orientation_joint[0], base_drag_top_grp))
            # if i>3:
            #     cmds.delete(cmds.orientConstraint(self.controller_orientation_joint[-1], base_drag_top_grp))
            cmds.delete(cluster)
        # 蒙皮

        # 父化
        # print(all_top_grp)
        for i in range(1, 4):
            cmds.parent(all_top_grp[i], all_curve[i-1])
        for i in range(7, 4, -1):
            cmds.parent(all_top_grp[i-1], all_curve[i])
        cmds.select(all_curve[0])
        self.curve.change_curve_color('Index', [all_curve[0]], [0, 0, 0], 17)
        self.controller.modify_vontroller_shape('scale', 1.2, 1.2, 1.2)
        cmds.select(all_curve[-1])
        self.curve.change_curve_color('Index', [all_curve[-1]], [0, 0, 0], 17)
        self.controller.modify_vontroller_shape('scale', 1.2, 1.2, 1.2)

        all_con_grp = cmds.group(all_top_grp[0], all_top_grp[-1], n='drag_con_' + str(self.top_num) + '_all_Grp')
        cmds.parent(all_con_grp, self.All_rope_sys_Grp)
        cmds.parentConstraint(self.top_curve, all_con_grp, mo=1)
        cmds.scaleConstraint(self.top_curve, all_con_grp, mo=1)
        # 创建附着定位器约束控制器
        drag_loc_grp = cmds.group(n='drag_loc_' + str(self.top_num) + '_all_Grp',em=1)
        cmds.setAttr(drag_loc_grp+'.visibility',0)
        all_ik_top_grp = all_ik_top_grp[::3]
        for i in range(len(all_ik_top_grp)):
            loc = cmds.spaceLocator(n='drag_loc_' + str(self.top_num) + '_Curve_' + str(i))
            cmds.delete(cmds.parentConstraint(all_ik_top_grp[i], loc))
            nearestPointOnCurve = cmds.createNode('nearestPointOnCurve')
            cmds.connectAttr(drag_curve + '.worldSpace[0]', nearestPointOnCurve + '.inputCurve')
            decomposeMatrix = cmds.createNode('decomposeMatrix')
            cmds.connectAttr(loc[0] + '.worldMatrix[0]', decomposeMatrix + '.inputMatrix')
            cmds.connectAttr(decomposeMatrix + '.outputTranslate', nearestPointOnCurve + '.inPosition')
            num = cmds.getAttr(nearestPointOnCurve + '.result.parameter')
            path_constraint = self.others_library.path_constraint(drag_curve, loc[0])
            cmds.setAttr(path_constraint + '.uValue', float(num))

            cmds.setAttr(path_constraint + '.worldUpType', 1)
            cmds.connectAttr(self.top_curve[0] + '.xformMatrix', path_constraint + '.worldUpMatrix')

            cmds.delete(nearestPointOnCurve, decomposeMatrix)
            cmds.parentConstraint(loc, all_ik_top_grp[i],mo=1) # skipRotate='x',
            cmds.parent(loc, drag_loc_grp)

        '''all_loc = []
        for i in range(len(all_ik_top_grp)):
            loc = cmds.joint(n='drag_loc_' + str(self.top_num) + '_Curve_' + str(i))
            all_loc.append(loc)
            cmds.delete(cmds.parentConstraint(all_ik_top_grp[i], loc))

            # nearestPointOnCurve = cmds.createNode('nearestPointOnCurve')
            # cmds.connectAttr(drag_curve + '.worldSpace[0]', nearestPointOnCurve + '.inputCurve')
            # decomposeMatrix = cmds.createNode('decomposeMatrix')
            # cmds.connectAttr(loc + '.worldMatrix[0]', decomposeMatrix + '.inputMatrix')
            # cmds.connectAttr(decomposeMatrix + '.outputTranslate', nearestPointOnCurve + '.inPosition')
            # num = cmds.getAttr(nearestPointOnCurve + '.result.parameter')
            # path_constraint = self.others_library.path_constraint(drag_curve, loc)
            # cmds.setAttr(path_constraint + '.uValue', float(num))
            #
            # cmds.setAttr(path_constraint + '.worldUpType', 1)
            # cmds.connectAttr(self.top_curve[0] + '.xformMatrix', path_constraint + '.worldUpMatrix')
            # cmds.delete(path_constraint)

            # cmds.delete(nearestPointOnCurve, decomposeMatrix)

            # cmds.parent(loc, drag_loc_grp)

        # 创建拉伸
        copy_drag_curve = cmds.duplicate(drag_curve)[0]
        copy_drag_curve = cmds.rename(copy_drag_curve, 'copy_' + drag_curve)
        cmds.select(copy_drag_curve)
        copy_drag_curve = cmds.ls(sl=1)
        copy_drag_curve_shape = cmds.listRelatives(copy_drag_curve, s=1)
        base_long_curve_curveInfo = cmds.createNode('curveInfo')
        cmds.connectAttr(copy_drag_curve_shape[0] + '.worldSpace[0]', base_long_curve_curveInfo + '.inputCurve')
        # cmds.skinCluster(all_position_out_joint, long_curve_copy, mi=1)
        long_curve_shape = cmds.listRelatives(drag_curve, s=True)
        long_curve_curveInfo = cmds.createNode('curveInfo')
        cmds.connectAttr(long_curve_shape[0] + '.worldSpace[0]', long_curve_curveInfo + '.inputCurve')
        multiplyDivide = cmds.createNode('multiplyDivide')
        cmds.connectAttr(base_long_curve_curveInfo + '.arcLength', multiplyDivide + '.input1X')
        cmds.connectAttr(long_curve_curveInfo + '.arcLength', multiplyDivide + '.input2X')
        cmds.setAttr(multiplyDivide + '.operation', 2)
        # cmds.skinCluster(all_joint, copy_drag_curve, mi=1)

        for i in range(0, len(all_loc)):
            cmds.parentConstraint(all_loc[i], all_ik_top_grp[i], mo=1)  # skipRotate='x',
        for i in range(1, len(all_loc)):
            # cmds.parent(all_loc[i], all_loc[i - 1])
            cmds.connectAttr(multiplyDivide + '.outputX', all_loc[i - 1] + '.scaleX')
        # cmds.makeIdentity(all_loc[0], apply=True, rotate=True, translate=False, scale=False)
        # cmds.joint(all_loc[0], e=1, oj='xyz', secondaryAxisOrient='xup', ch=0, zso=1)
        # 选择层次
        # cmds.SelectHierarchy(all_loc, allDescendents=True)
        # all_loc = cmds.ls(sl=1, type='joint')
        # cmds.delete(cmds.orientConstraint(all_loc[-2], all_loc[-1]))

        cmds.select(all_loc[0], all_loc[-1], drag_curve)
        ik_sys = cmds.ikHandle(ccv=False, sol='ikSplineSolver', pcv=False, scv=False)
        IK = cmds.ls(sl=1)
        cmds.parent(ik_sys[-1], all_loc[-1])'''


        cmds.parent(drag_curve, drag_loc_grp)
        cmds.parent(drag_loc_grp, self.All_rope_sys_Grp)
        cmds.skinCluster(all_joint, drag_curve, mi=1)

    # 创建滑动缩放
    def create_drag_scale(self):
        pass

    # 创建测试样条与模型
    @Withdraw
    def create_test(self):
        curve = cmds.curve(p=[(-12, 0, 0), (-4, 0, 0), (4, 0, 0), (12, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3)
        cmds.rebuildCurve(curve, rt=0, ch=0, end=1, d=3, kr=0, s=10, kcp=0, tol=0.01, kt=0, rpo=1, kep=1)
        cmds.polyPlane(cuv=2, sy=1, sx=50, h=1, ch=0, w=24, ax=(0, 1, 0))



window = Window()
if __name__ == '__main__':
    window.show()

