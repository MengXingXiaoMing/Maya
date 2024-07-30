# -*- coding: utf-8 -*-
import math

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
        self.library_path = self.root_path + '\\' + maya_version
        # 样条库路径
        self.curve_library_path = self.library_path+ '\curve_library'

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


    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('测试模板')
        self.button_2 = QtWidgets.QPushButton('中心建立骨骼链')
        self.button_3 = QtWidgets.QPushButton('按骨骼生成样条')
        self.button_4 = QtWidgets.QPushButton('选择样条创建控制器方向定位骨骼')

        self.line_edit_1 = QtWidgets.QLineEdit()
        self.line_edit_1.setFixedWidth(50)
        self.line_edit_1.setText('50')
        self.slider_1 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_1.setMinimum(1)
        self.slider_1.setMaximum(100)
        self.slider_1.setValue(50)
        self.button_5 = QtWidgets.QPushButton('创建骨骼')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        self.slider_2 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_2.setMinimum(0)
        self.slider_2.setMaximum(4)
        self.slider_2.setValue(0)
        self.button_6 = QtWidgets.QPushButton('创建基础')
        self.button_6.setStyleSheet('color:rgb(0,0,0);background:rgb(255,102,102)')
        self.label_1 = QtWidgets.QLabel('请记得矫正骨骼轴向')

        self.splitter_2 = QtWidgets.QSplitter()
        self.splitter_2.setFixedHeight(1)
        self.splitter_2.setFrameStyle(1)

        self.label_2 = QtWidgets.QLabel('骨骼')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_7 = QtWidgets.QPushButton('加载')

        self.label_3 = QtWidgets.QLabel('样条')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_8 = QtWidgets.QPushButton('加载')

        #self.label_4 = QtWidgets.QLabel('一端拖拽控制器数：')
        #self.line_edit_4 = QtWidgets.QLineEdit()
        #self.line_edit_4.setFixedWidth(30)
        #self.line_edit_4.setText('4')
        #self.slider_3 = QtWidgets.QSlider(Qt.Horizontal)
        #self.slider_3.setMinimum(1)
        #self.slider_3.setMaximum(10)

        self.label_5 = QtWidgets.QLabel('滑动缩放控制器数：')
        self.line_edit_5 = QtWidgets.QLineEdit()
        self.line_edit_5.setFixedWidth(30)
        self.line_edit_5.setText('1')
        self.slider_3 = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_3.setMinimum(1)
        self.slider_3.setMaximum(10)

        self.label_6 = QtWidgets.QLabel('前缀')
        self.line_edit_6 = QtWidgets.QLineEdit('Rope_')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)

        h_Box_layout_1.addWidget(self.button_1)
        h_Box_layout_1.addWidget(self.button_2)
        h_Box_layout_1.addWidget(self.button_3)

        main_layout.addWidget(self.button_4)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_2)
        h_Box_layout_2.addWidget(self.line_edit_1)
        h_Box_layout_2.addWidget(self.slider_1)
        h_Box_layout_2.addWidget(self.button_5)

        main_layout.addWidget(self.splitter_1)

        v_box_layout_1 = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(v_box_layout_1)
        v_box_layout_1.addWidget(self.slider_2)
        v_box_layout_1.addWidget(self.button_6)
        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        v_box_layout_1.addLayout(h_Box_layout_3)
        h_Box_layout_3.addStretch(1)
        h_Box_layout_3.addWidget(self.label_1)
        h_Box_layout_3.addStretch(1)
        main_layout.setStretchFactor(v_box_layout_1, 2)

        main_layout.addWidget(self.splitter_2)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.label_2)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_7)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.label_3)
        h_Box_layout_5.addWidget(self.line_edit_3)
        h_Box_layout_5.addWidget(self.button_8)

        # h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        # main_layout.addLayout(h_Box_layout_6)
        # h_Box_layout_6.addWidget(self.label_4)
        # h_Box_layout_6.addWidget(self.line_edit_4)
        # h_Box_layout_6.addWidget(self.slider_3)

        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.label_5)
        h_Box_layout_8.addWidget(self.line_edit_5)
        h_Box_layout_8.addWidget(self.slider_3)

        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_7)
        h_Box_layout_7.addWidget(self.label_6)
        h_Box_layout_7.addWidget(self.line_edit_6)

        # 置顶
        #main_layout.addStretch(0)

    def create_connect(self):
        self.button_1.clicked.connect(self.create_test)
        self.button_2.clicked.connect(self.others_library.create_centre_joint)
        self.button_3.clicked.connect(self.others_library.joint_transformation_curve)
        self.button_4.clicked.connect(self.create_positioning_loc)
        self.slider_1.valueChanged.connect(self.create_joint_num)
        self.button_5.clicked.connect(lambda :self.others_library.generate_bone_chain(int(self.line_edit_1.text())))
        self.slider_2.valueChanged.connect(self.implementation_progress)
        self.button_6.clicked.connect(self.create_rope)
        self.button_7.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_2,['QLineEdit']))
        self.button_8.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_3,['QLineEdit']))
        self.slider_3.valueChanged.connect(self.adjusting_the_number_of_sliding_controllers)

    # 按样条创建骨骼链
    def create_joint_num(self):
        num = self.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(self.slider_1, 'QSlider')
        self.line_edit_1.setText(str(num))
        if num < 1:
            self.line_edit_1.setText('1')
            self.slider_1.setValue(1)
            self.slider_1.setMinimum(0)
        if num > 1000000:
            self.line_edit_1.setText('1000000')
            self.slider_1.setValue(1000000)
            self.slider_1.setMaximum(1000000)

    # 自动调整按钮
    def implementation_progress(self):
        step = self.slider_2.value()
        txt = ""
        Text = ["创建基础", ",添加拉伸",",添加收缩", ",添加FK", ",添加拖拽"]
        for i in range(0, len(Text)):
            if step >= i:
                txt = txt + Text[i]
                self.button_6.setText(txt)

    # 调整滑动控制器数量
    def adjusting_the_number_of_sliding_controllers(self):
        num = self.ui_edit.automatically_adjust_the_slider_range_and_return_the_value(self.slider_3, 'QSlider')
        if num<1:
            num = 1
            self.slider_3.setValue(num)
            self.slider_3.setMinimum(1)
        self.line_edit_5.setText(str(num))

    # 生成朝向骨骼
    def create_positioning_loc(self):
        Curve = cmds.ls(sl=1)
        cmds.select(Curve[0] + '.cv[*]')
        CurvePoint = cmds.ls(sl=1, fl=1)  # 加载样条点
        CurvePoint.append(CurvePoint[-1])
        Joint = []
        for i in range(0,len(CurvePoint)):
            cmds.select(CurvePoint[i])
            Cluster = cmds.cluster()
            cmds.select(cl=1)
            joint = cmds.joint(p=(0,0,0),n='LocJoint_'+ str(i))
            Joint.append(joint)
            cmds.setAttr(('LocJoint_' + str(i) + ".displayLocalAxis"), 1)
            cmds.delete(cmds.pointConstraint( Cluster[1], joint, w=1))
            cmds.delete(Cluster)
        cmds.setAttr(('LocJoint_' + str(len(CurvePoint)-1) + ".v"), 0)
        for i in range(1,len(CurvePoint)):
            cmds.parent(('LocJoint_'+ str(i)),('LocJoint_'+ str(i-1)))
        cmds.select('LocJoint_0')
        cmds.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='zup')
        cmds.curve(p=[(0, 0, 0), (0, 0, 1)], k=[0, 1], d=1)
        ClusterCurve = cmds.ls(sl=1)
        cmds.rebuildCurve(ClusterCurve[0], rt=0, ch=1, end=1, d=1, kr=0, s=(len(CurvePoint)-1), kcp=0, tol=0, kt=0, rpo=1, kep=0)
        cmds.select(ClusterCurve[0] + '.cv[*]')
        ClusterCurvePoint = cmds.ls(sl=1, fl=1)  # 加载样条点
        for i in range(0,len(ClusterCurvePoint)):
            cmds.select(ClusterCurvePoint[i])
            Cluster = cmds.cluster()
            cmds.delete(cmds.pointConstraint(('LocJoint_'+ str(i)),Cluster[1],w=1))
        cmds.select(ClusterCurve)
        cmds.DeleteHistory()
        cmds.delete(cmds.ikHandle(sj=Joint[0], ee=Joint[-1], c=ClusterCurve[0], ccv=False, sol='ikSplineSolver'))
        cmds.delete(ClusterCurve)
        cmds.warning('已经生成完朝向骨骼。')

    # 开始创建
    def create_rope(self):
        if cmds.objExists('LocJoint_0'):
            cmds.undoInfo(ock=1)

            step = self.slider_2.value()  # 步骤
            joint = self.line_edit_2.text()  # 加载顶骨骼
            self.curve = self.line_edit_3.text()  # 加载样条
            self.slide_zoom = int(self.line_edit_5.text())  # 加载滑动控制器数量
            self.prefix = self.line_edit_6.text()  # 加载前缀


            # 重载骨骼
            cmds.select(joint)
            cmds.SelectHierarchy()
            self.joint = cmds.ls(sl=1, type='joint')

            # 获取样条点
            cmds.select(self.curve + '.cv[*]')
            self.curve_point = cmds.ls(sl=1, fl=1) # 加载样条点

            self.drag_controllers_num = int(len(self.curve_point))//2  # 加载一段控制器数量

            # 顶组名称
            self.top_grp = self.prefix + 'TotalControl'
            top_grp_curve = self.top_grp + '_Curve'

            # 创建基础
            if step > -1:
                self.create_base()
                cmds.addAttr(top_grp_curve, ln='_000', en='█████:', at='enum', nn="█████████████")
                cmds.setAttr(top_grp_curve+'._000', e=1, keyable=True)
                for i in range(0,4):
                    self.others_library.get_move_up_dn_attrs_proc(1, [top_grp_curve+'._000'])
                cmds.addAttr(top_grp_curve, ln="_001", en="█████:", at="enum", nn="█████████████")
                cmds.setAttr(top_grp_curve+'._001', e=1, keyable=True)
                for i in range(0, 2):
                    self.others_library.get_move_up_dn_attrs_proc(1, [top_grp_curve+'._001'])
            # 添加拉伸s
            if step > 0:
                self.add_stretch()
                cmds.addAttr(top_grp_curve, ln="_002", en="█████:", at="enum", nn="█████████████")
                cmds.setAttr(top_grp_curve+'._002', e=1, keyable=True)
                for i in range(0,5):
                    self.others_library.get_move_up_dn_attrs_proc(0, [top_grp_curve+'.Basic_IK'])
            # 添加收缩
            if step > 1:
                self.add_contract()
                for i in range(0,4):
                    self.others_library.get_move_up_dn_attrs_proc(1, [top_grp_curve+'.Contract'])
            # 添加FK
            if step > 2:
                cmds.addAttr(top_grp_curve, ln="_003", en="█████:", at="enum", nn="█████████████")
                cmds.setAttr(top_grp_curve+'._003', e=1, keyable=True)
                self.add_fk()
            # 添加拖拽
            if step > 3:
                self.add_drag()
                for i in range(0,4):
                    self.others_library.get_move_up_dn_attrs_proc(1, [top_grp_curve+'.IK_Drag'])
                for i in range(0,4):
                    self.others_library.get_move_up_dn_attrs_proc(1, [top_grp_curve+'.IK_DragSecondary'])
            if cmds.objExists(top_grp_curve+'._000'):
                cmds.setAttr(top_grp_curve+'._000', lock=True)
            if cmds.objExists(top_grp_curve+'._001'):
                cmds.setAttr(top_grp_curve+'._001', lock=True)
            if cmds.objExists(top_grp_curve+'._002'):
                cmds.setAttr(top_grp_curve+'._002', lock=True)
            if cmds.objExists(top_grp_curve+'._003'):
                cmds.setAttr(top_grp_curve+'._003', lock=True)
            cmds.delete('LocJoint_0')
            cmds.select(top_grp_curve)
            cmds.undoInfo(cck=1)
        else:
            cmds.warning('请生成控制器朝向骨骼。')

    ############################################################################################################################
    # 命令部分
    # 创建基础
    def create_base(self):
        # 创建基础
        all_base_controller_grp = cmds.group(em=1, n=(self.prefix + 'All_BaseController_Grp'))
        # 创建基础控制器
        i = 0
        for point in self.curve_point:
            cmds.select(point)
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            self.curve_library.create_curve(self.curve_library_path,'正方形')
            self.controller.modify_vontroller_shape('scale', 1.5, 1.5, 1.5)
            cmds.rename((self.prefix + str(i) + '_BaseController'))
            total_control = cmds.ls(sl=1)
            self.curve_library.change_curve_color('Index', total_control, [0,0,0], 18)
            cmds.group(n=(self.prefix + str(i) + '_BaseController_Grp2'))
            TopGrp = cmds.group(n=(self.prefix + str(i) + '_BaseController_Grp1'))
            cmds.delete(cmds.parentConstraint(('LocJoint_'+str(i)), TopGrp, w=1))
            cmds.parent(Cluster[1], total_control[0])
            cmds.parent(TopGrp, all_base_controller_grp)
            i = i + 1

        # 创建路径约束,用于跟随曲线
        path_constraint_loc = cmds.spaceLocator(n=(self.prefix + 'path_constraint_loc'))
        cmds.setAttr((path_constraint_loc[0] + '.inheritsTransform'), 0)

        self.path_constraint = self.others_library.path_constraint(self.curve, path_constraint_loc[0])
        # 创建IK
        cmds.select(self.joint[0], self.joint[-1], self.curve)
        cmds.ikHandle(ccv=False, sol='ikSplineSolver', roc=False, pcv=False, n=(self.prefix + 'ikHandle'))
        IK = cmds.ls(sl=1)
        cmds.parentConstraint(path_constraint_loc, self.joint[0], w=1)
        # 创建曲面
        cmds.extrude(self.curve, upn=1, dl=3, ch=0, rotation=0, length=0.01, scale=1, et=0, rn=False, po=0, n=(self.curve + '_Surface'))
        surface = cmds.ls(sl=1)
        cmds.setAttr(surface[0]+'.visibility',0)
        # 创建控制曲面的蔟
        for i in range(0, len(self.curve_point)):
            cmds.select(surface[0] + '.cv[' + str(i) + '][0:*]')
            cluster = cmds.cluster()
            cmds.setAttr((cluster[1] + '.v'), 0)
            cmds.parent(cluster[1], (self.prefix + str(i) + '_BaseController'))
        # 重建曲面
        rebuildSurface = cmds.rebuildSurface(surface, rt=0, kc=0, fr=0, ch=1, end=1, sv=1, su=(len(self.curve_point) - 1) * 3, kr=0, dir=2, kcp=0, tol=0.01, dv=3, du=3, rpo=1, n=(self.curve[0] + '_Surface'))

        # 创建毛囊附着表面跟随骨骼
        all_joint_follicle_grp = cmds.group(em=1, n=(self.prefix + 'All_JointFollicle_Grp'))
        shape = cmds.listRelatives(surface, s=1)
        curve_shape = cmds.listRelatives(self.curve, s=1)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((curve_shape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)

        copy_curve = cmds.duplicate(self.curve)
        copy_curve_shape = cmds.listRelatives(copy_curve[0], s=1)
        copy_curve_curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((copy_curve_shape[0] + '.worldSpace[0]'), (copy_curve_curveInfo + '.inputCurve'), force=1)
        for i in range(0, len(self.joint)):
            cpom = cmds.createNode('closestPointOnSurface', n=(self.joint[i] + 'closestPointOnSurface'))
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
            decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
            cmds.connectAttr((self.joint[i] + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
            cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
            follicleShape = cmds.createNode('follicle', n=(self.joint[i] + '_follicleShape'))
            follicle = cmds.listRelatives(follicleShape, p=1)
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (self.joint[i] + '_follicleShape' + '.inputSurface'), f=1)
            cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (self.joint[i] + '_follicleShape' + '.inputWorldMatrix'),f=1)
            cmds.connectAttr((self.joint[i] + '_follicleShape' + ".outTranslate"),
                             (self.joint[i] + '_follicle' + '.translate'),f=1)
            cmds.connectAttr((self.joint[i] + '_follicleShape' + ".outRotate"),
                             (self.joint[i] + '_follicle' + ".rotate"), f=1)
            cmds.connectAttr((cpom + '.parameterU'), (self.joint[i] + '_follicle' + '.parameterU'), f=1)
            cmds.setAttr((self.joint[i] + '_follicle' + '.parameterV'), 0)
            cmds.select(cl=1)
            skin_joint = cmds.joint(p=(0, 0, 0), n=(self.joint[i] + 'SkinJoint'))
            cmds.delete(cmds.parentConstraint(follicle[0], skin_joint))
            cmds.parent(follicle[0], all_joint_follicle_grp)
        # 创建滑动缩放控制器
        all_u_curve_grp = []
        # 创建总控制器
        self.curve_library.create_curve(self.curve_library_path, '四边方向箭')
        self.controller.modify_vontroller_shape('scale', 0.5, 0.5, 0.5)
        self.controller.modify_vontroller_shape('rotate', 0, 90, 90)
        cmds.rename((self.prefix + 'TotalControl_Curve'))
        total_control = cmds.ls(sl=1)
        self.curve_library.change_curve_color('Index', total_control, [0, 0, 0], 13)
        cmds.group(n=(self.prefix + 'TotalControl_Grp2'))
        cmds.group(n=(self.prefix + 'TotalControl_Grp1'))

        for slide_controller_num in range(0,self.slide_zoom):
            self.curve_library.create_curve(self.curve_library_path, '圆片拉线')
            cmds.rename(self.prefix + 'slide_zoom_curve' + str(slide_controller_num))
            u_curve = cmds.ls(sl=1)
            self.controller.modify_vontroller_shape('scale', 5.0, 5.0, 5.0)
            self.curve_library.change_curve_color('Index', u_curve, [0, 0, 0], 20)

            u_curve_grp = cmds.group(n='slide_zoom_curve_grp' + str(slide_controller_num),em=1)
            cmds.parent(u_curve[0], u_curve_grp)
            all_u_curve_grp.append(u_curve_grp)
            cmds.addAttr(u_curve[0], ln='uValue', min=0, max=100, dv=0, at='double')
            cmds.setAttr((u_curve[0] + '.uValue'), e=1, keyable=True)
            cmds.addAttr(u_curve[0], ln='slide_range',  dv=50, min=0, at='double')
            cmds.setAttr((u_curve[0] + '.slide_range'), e=1, keyable=True)
            cmds.addAttr(u_curve[0], ln='slide_size',  dv=1, min=0, at='double')
            cmds.setAttr((u_curve[0] + '.slide_size'), e=1, keyable=True)
            cmds.connectAttr((u_curve[0] + '.slide_size'), (u_curve_grp + '.scaleX'), f=1)
            cmds.connectAttr((u_curve[0] + '.slide_size'), (u_curve_grp + '.scaleY'), f=1)
            cmds.connectAttr((u_curve[0] + '.slide_size'), (u_curve_grp + '.scaleZ'), f=1)

            path_constraint = self.others_library.path_constraint(self.curve, u_curve_grp)
            cmds.setAttr(path_constraint + '.fractionMode',0)
            u_curve_multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
            cmds.connectAttr((u_curve[0] + '.uValue'), (u_curve_multiplyDivide + '.input1X'), f=1)
            cmds.setAttr((u_curve_multiplyDivide + '.input2X'),0.01)
            cmds.connectAttr((u_curve_multiplyDivide + '.outputX'), (path_constraint + '.uValue'), f=1)
            # 建立当前弧长
            now_arcLengthDimension = cmds.arcLengthDimension(curve_shape[0] + '.u[0.5]')
            cmds.connectAttr((u_curve_multiplyDivide + '.outputX'), (now_arcLengthDimension + '.uParamValue'), f=1)
            for i in range(0, len(self.joint)):
                # 建立弧长
                arcLengthDimension = cmds.arcLengthDimension(curve_shape[0] + '.u[0.5]')
                cmds.connectAttr((self.joint[i] + '_follicle' + '.parameterU'), (arcLengthDimension + '.uParamValue'), f=1)
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
                cmds.connectAttr((total_control[0] + '.scaleX'), (multiplyDivide + '.input2X'), f=1)
                cmds.connectAttr((multiplyDivide + '.outputX'), (imp_multiplyDivide + '.input1X'), f=1)
                #cmds.connectAttr((u_curve[0] + '.slide_range'), (imp_multiplyDivide + '.input1X'), f=1)
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
                cmds.setAttr((floatMath+'.operation'),5)
                cmds.connectAttr((out_multiplyDivide + '.outputX'), (floatMath+'.floatA'), f=1)

                have_floatMath = cmds.listConnections((self.joint[i] + 'SkinJoint.scaleY'), d=False, s=True)

                if have_floatMath:
                    new_floatMath = []
                    while have_floatMath:
                        new_floatMath = have_floatMath
                        have_floatMath = cmds.listConnections((have_floatMath[0] + '.floatB'), d=False, s=True)
                    have_floatMath = new_floatMath
                    cmds.connectAttr((floatMath+'.outFloat'), (have_floatMath[0]+'.floatB'), f=1)
                else:
                    cmds.connectAttr((floatMath+'.outFloat'), (self.joint[i] + 'SkinJoint.scaleY'), f=1)
                    cmds.connectAttr((floatMath+'.outFloat'), (self.joint[i] + 'SkinJoint.scaleZ'), f=1)

        for i in range(0, len(self.joint)):
            cmds.parentConstraint((self.joint[i] + '_follicle'), (self.joint[i] + 'SkinJoint'), mo=1, w=1)

        # 整理文件
        cmds.group(copy_curve[0], path_constraint_loc[0], self.joint[0], self.curve, IK[0], n=(self.prefix + 'SpineIkSys_Grp'))
        cmds.group((self.joint[0] + 'SkinJoint'), n=(self.prefix + self.joint[0] + '_SkinJoint_Grp'))
        for i in range(1, len(self.joint)):
            cmds.parent((self.joint[i] + 'SkinJoint'), (self.prefix + self.joint[0] + '_SkinJoint_Grp'))
        cmds.setAttr(self.prefix + self.joint[0] + '_SkinJoint_Grp.useOutlinerColor', True)
        cmds.setAttr(self.prefix + self.joint[0] + '_SkinJoint_Grp.outlinerColor', 1, 0, 0)
        cmds.group(surface[0], all_joint_follicle_grp, n=(self.prefix + 'follicleAttachmentSys_Grp'))
        cmds.group(all_base_controller_grp, (self.prefix + self.joint[0] + '_SkinJoint_Grp'), (self.prefix + 'SpineIkSys_Grp'),
                   (self.prefix + 'follicleAttachmentSys_Grp'), n=(self.prefix + 'BasicPart_Grp'))
        # 创建总控制
        cmds.delete(cmds.parentConstraint((self.prefix + str(len(self.curve_point) - 1) + '_BaseController'),
                                          (self.prefix + 'TotalControl_Grp1'), w=1))
        cmds.parentConstraint((self.prefix + 'TotalControl_Curve'), (self.prefix + 'BasicPart_Grp'), mo=1, w=1)
        cmds.scaleConstraint((self.prefix + 'TotalControl_Curve'), (self.prefix + 'BasicPart_Grp'), mo=1)
        cmds.setAttr((self.curve + '.inheritsTransform'), 0)
        cmds.setAttr((self.prefix + 'follicleAttachmentSys_Grp.inheritsTransform'), 0)

        all_slide_zoom_grp = cmds.group(n=(self.prefix + 'All_Slide_Zoom_Grp'),em=1)
        cmds.parent(all_u_curve_grp,all_slide_zoom_grp)

        all_grp = cmds.group(all_slide_zoom_grp, (self.prefix + 'TotalControl_Grp1'), (self.prefix + 'BasicPart_Grp'), n=(self.prefix + 'All_Grp'))
        cmds.setAttr((self.prefix + 'SpineIkSys_Grp.v'), 0)
        cmds.setAttr((self.prefix + 'All_JointFollicle_Grp.v'), 0)
        cmds.setAttr((self.prefix + 'All_Grp.inheritsTransform'), 0)



        #添加精度优化属性
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='Accuracy', min=1, dv=3, at='long')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.Accuracy'), e=1, keyable=True)
        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.Accuracy'), (multiplyDivide + '.input1X'), force=1)
        cmds.setAttr((multiplyDivide + '.input2X'), (len(self.curve_point) - 1))
        cmds.connectAttr((multiplyDivide + '.outputX'), (rebuildSurface[1] + '.spansU'), force=1)

        # 添加优化
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='optimize', at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.optimize'), e=1, keyable=True)
        shadingNode = cmds.shadingNode('condition', asUtility=1)
        cmds.setAttr((shadingNode+'.colorIfFalseR'), 2)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.optimize'), (shadingNode + '.firstTerm'), force=1)
        cmds.connectAttr((shadingNode + '.outColorR'), (shape[0] + '.nodeState'), force=1)

        #创建优化曲面
        cmds.extrude(self.curve, upn=1, dl=3, ch=0, rotation=0, length=1, scale=1, et=0, rn=False, po=0)
        surface = cmds.ls(sl=1)
        cmds.parent(surface[0], (self.prefix + 'follicleAttachmentSys_Grp'))
        cmds.select(surface[0] + '.cv[0:][0]')
        point = cmds.ls(sl=1, fl=1)

        #创建控制曲面的蔟
        for i in range(0, len(point)):
            cmds.select(surface[0] + '.cv[' + str(i) + '][0:*]')
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            cmds.delete(cmds.parentConstraint((self.prefix + str(i) + '_BaseController'), Cluster[1], weight=1))
            cmds.parent(Cluster[1], (self.prefix + str(i) + '_BaseController'), )
        rebuildSurface = cmds.rebuildSurface(surface, rt=0, kc=0, fr=0, ch=1, end=1, sv=1, su=(len(self.joint) - 1) * 3, kr=0,
                                             dir=2, kcp=0, tol=0.01, dv=3, du=3, rpo=1)
        cmds.connectAttr((multiplyDivide + '.outputX'), (rebuildSurface[1] + '.spansU'), force=1)

        cmds.connectAttr((self.prefix + 'TotalControl_Curve.optimize'), (surface[0] + '.visibility'), force=1)
        cmds.setAttr((surface[0] + '.overrideEnabled'), 1)
        cmds.setAttr((surface[0] + '.overrideDisplayType'), 2)

        #添加底层控制器显示隐藏
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='Basic_IK', at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.Basic_IK'), e=1, keyable=True)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.Basic_IK'), (self.prefix + 'All_BaseController_Grp.visibility'), force=1)

        # 添加滑动缩放控制器显示隐藏
        cmds.addAttr(total_control[0], ln='Slide_Zoom', at='bool')
        cmds.setAttr((total_control[0] + '.Slide_Zoom'), e=1, keyable=True)
        cmds.connectAttr((total_control[0] + '.Slide_Zoom'),
                         (all_slide_zoom_grp + '.visibility'), force=1)

    # 添加拉伸
    def add_stretch(self):
        # 添加拉伸
        curve_shape = cmds.listRelatives(self.curve, s=1)
        cmds.select(cmds.duplicate(self.curve, rr=1))
        copy_curve = cmds.ls(sl=1)
        copy_curve_shape = cmds.listRelatives(copy_curve, s=1)
        copy_curve_shape_child = cmds.listRelatives(copy_curve_shape[0], c=1, f=1)
        cmds.delete(copy_curve_shape_child)
        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide + '.operation'), 2)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((curve_shape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1X'), f=1)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((copy_curve_shape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input2X'), f=1)
        # 添加拉伸开关
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='stretch', at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.stretch'), e=1, keyable=True)
        #
        #cmds.connectAttr((self.prefix + 'TotalControl_Curve.stretch'), (self.prefix+'slide_zoom_curve.stretch'), f=1)
        #
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='StretchMagnification', dv=1, at='double')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.StretchMagnification'), e=1, keyable=True)
        condition = cmds.shadingNode('condition', asUtility=1)
        cmds.connectAttr((multiplyDivide + '.outputX'), (condition + '.colorIfFalseR'), f=1)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.stretch'), (condition + '.firstTerm'), f=1)
        cmds.setAttr((condition + '.colorIfTrueR'), 1)
        multiplyDivide_stretch = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.connectAttr((condition + '.outColorR'), (multiplyDivide_stretch + '.input1X'), f=1)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.StretchMagnification'), (multiplyDivide_stretch + '.input2X'),f=1)
        for i in range(0, len(self.joint)):
            cmds.connectAttr((multiplyDivide_stretch + '.outputX'), (self.joint[i] + '.scaleX'), f=1)
            cmds.connectAttr((multiplyDivide_stretch + '.outputX'), (self.joint[i] + 'SkinJoint.scaleX'), f=1)
        cmds.setAttr(copy_curve[0] + '.inheritsTransform', 1)
        # 添加保持体积
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='Volume', min=0, max=10,dv=0, at='double')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.Volume'), e=1, keyable=True)
        setRange = cmds.shadingNode('setRange', asUtility=1)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.Volume'), (setRange + '.valueX'), f=1)
        cmds.setAttr((setRange + '.oldMaxX'), 10)
        cmds.connectAttr((multiplyDivide_stretch + '.outputX'), (setRange + '.minX'), f=1)
        cmds.setAttr((setRange + '.maxX'), 1)
        multiplyDivide_vlume = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide_vlume + '.operation'), 2)
        cmds.connectAttr((setRange + '.outValueX'), (multiplyDivide_vlume + '.input1X'), f=1)
        cmds.connectAttr((multiplyDivide_stretch + '.outputX'), (multiplyDivide_vlume + '.input2X'), f=1)
        for i in range(0, len(self.joint)):
            input_range = (0, len(self.joint)-1)  # 输入范围
            output_range = (0, math.radians(360))  # 输出范围
            input_min, input_max = input_range
            output_min, output_max = output_range
            # 检查输入值是否在输入范围内
            a = (i - input_min) * (output_max - output_min) / (input_max - input_min) + output_min
            cos_value = math.cos(a)
            value = ((cos_value+1)/2)*-1+1
            cmds.addAttr((self.joint[i] + 'SkinJoint'), ln='Volume_num', min=0, max=1, dv=value, at='double')
            cmds.setAttr((self.joint[i] + 'SkinJoint.Volume_num'), e=1, keyable=True)
            setRange = cmds.shadingNode('setRange', asUtility=1)
            cmds.connectAttr((self.joint[i] + 'SkinJoint.Volume_num'), (setRange + '.valueX'), f=1)
            cmds.connectAttr((multiplyDivide_vlume + '.outputX'), (setRange + '.maxX'), f=1)
            cmds.setAttr((setRange + '.oldMaxX'), 1)
            cmds.setAttr((setRange + '.minX'), 1)



            have_floatMath = cmds.listConnections((self.joint[i] + 'SkinJoint.scaleY'), d=False, s=True)
            new_floatMath = []
            while have_floatMath:
                new_floatMath = have_floatMath
                have_floatMath = cmds.listConnections((have_floatMath[0] + '.floatB'), d=False, s=True)
            have_floatMath = new_floatMath
            cmds.connectAttr((setRange + '.outValueX'), (have_floatMath[0] + '.floatB'), f=1)

    # 添加收缩
    def add_contract(self):
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='Contract', dv=0, max=100, min=-100, at='double')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.Contract'), e=1, keyable=True)

        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide + '.input2X'), -0.01)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.Contract'), (multiplyDivide + '.input1X'), f=1)
        cmds.connectAttr((multiplyDivide + '.outputX'), (self.path_constraint + '.uValue'), f=1)

        # 建立反向ik且建立毛囊
        cmds.select(cmds.duplicate(self.curve, rr=1))
        cmds.rename(cmds.ls(sl=1),(self.curve+'_reverse'))
        reverse_curve = cmds.ls(sl=1)

        CopyCurveShape = cmds.listRelatives(reverse_curve, s=1)
        CopyCurveShape_child = cmds.listRelatives(CopyCurveShape[0], c=1, f=1)
        cmds.delete(CopyCurveShape_child)

        cmds.reverseCurve(reverse_curve[0], ch=0, rpo=1)
        #reverse_curve = cmds.ls(sl=1)
        for i in range(0,len(self.joint)):
            cmds.select(cl=1)
            cmds.joint(p=(0,0,0),n=(self.joint[len(self.joint)-1-i] + '_Reverse'))
            cmds.delete(cmds.parentConstraint(self.joint[len(self.joint)-1-i],(self.joint[len(self.joint)-1-i] + '_Reverse'),w=1))
            if i > 0:
                cmds.parent((self.joint[len(self.joint)-1-i] + '_Reverse'),(self.joint[len(self.joint)-i] + '_Reverse'))
        cmds.parent((self.joint[len(self.joint)-1] + '_Reverse'),(self.prefix + 'SpineIkSys_Grp'))

        # 创建路径约束
        path_constraint_loc = cmds.spaceLocator(n=(self.prefix + 'path_constraint_Reverse_loc'))
        cmds.setAttr((self.prefix + 'path_constraint_Reverse_loc.inheritsTransform'), 0)
        cmds.parent(path_constraint_loc[0], (self.prefix + 'SpineIkSys_Grp'))
        path_constraint_reverse = self.others_library.path_constraint(reverse_curve, path_constraint_loc[0])
        # 创建IK
        cmds.select((self.joint[0] + '_Reverse'), (self.joint[-1] + '_Reverse'), reverse_curve)
        cmds.ikHandle(ccv=False, sol='ikSplineSolver', roc=False, pcv=False, n=(self.prefix + 'Reverse_ikHandle'))
        IK = cmds.ls(sl=1)
        cmds.parentConstraint(path_constraint_loc, (self.joint[-1] + '_Reverse'), w=1)
        cmds.parent(IK[0],(self.prefix + 'SpineIkSys_Grp'))

        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide + '.input2X'), 0.01)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.Contract'), (multiplyDivide + '.input1X'), f=1)
        cmds.connectAttr((multiplyDivide + '.outputX'), (path_constraint_reverse + '.uValue'), f=1)

        shape = cmds.listRelatives((self.curve+'_Surface'), s=1)

        for i in range(0, len(self.joint)):
            cpom = cmds.createNode('closestPointOnSurface',n=(self.joint[i] + '_Reverse_closestPointOnSurface'))
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
            decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
            cmds.connectAttr((self.joint[i] + '_Reverse.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
            cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)

            condition = cmds.shadingNode('condition', asUtility=1)
            cmds.connectAttr((self.prefix + 'TotalControl_Curve.Contract'), (condition + '.firstTerm'), f=1)
            cmds.setAttr((condition+'.operation'), 2)
            cmds.connectAttr((self.joint[i] + 'closestPointOnSurface.parameterU'), (condition+'.colorIfFalseR'), f=1)
            cmds.connectAttr((cpom + '.parameterU'), (condition+'.colorIfTrueR'), f=1)
            cmds.connectAttr((condition+'.outColorR'), (self.joint[i] + '_follicleShape.parameterU'), f=1)
        # print reverse_curve
        cmds.select(reverse_curve[0] + '.cv[*]')
        curve_point = cmds.ls(sl=1, fl=1)  # 加载样条点
        for i in range(0,len(curve_point)):
            cmds.select(curve_point[i])
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            cmds.parent(Cluster[1],(self.prefix + str(len(curve_point)-1-i) + '_BaseController'))
        multiplyDivideStretch = cmds.listConnections((self.joint[0] + '.scaleX'), p=1)
        # print multiplyDivideStretch
        for i in range(0, len(self.joint)):
            cmds.connectAttr(multiplyDivideStretch[0], (self.joint[i] + '_Reverse.scaleX'), f=1)

    # 添加FK
    def add_fk(self):
        FK_List = []
        for i in range(0, len(self.curve_point)):
            FK_List.append(i)
        for i in range(0, len(self.curve_point) - 1):
            FK_List.append(len(self.curve_point) - i - 2)

        j = 0
        All_TopGrp = []
        for i in FK_List:
            r = 2
            if j >= (len(self.curve_point)-1):
                r = 1
            FKCurve = cmds.circle(c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=r, tol=0.01,
                                  nr=(1,0,0),
                                  n=(self.prefix + 'FKController' + str(j)))
            cmds.setAttr((self.prefix + 'FKController' + str(j) + 'Shape.overrideEnabled'), 1)
            sel = cmds.ls(sl=1)
            self.curve_library.change_curve_color('Index', sel , [0, 0, 0], 20)
            if j >= (len(self.curve_point)-1):
                self.curve_library.change_curve_color('Index', sel, [0, 0, 0], 21)
                Shape = cmds.listRelatives(FKCurve[0], s=1)
                cmds.select((Shape[0] + ".cv[0:]"))
                # cmds.scale(0.8, 0.8, 0.8, r=1)
            cmds.select(FKCurve)
            cmds.group(n=(self.prefix + 'FKController_Grp2_' + str(j)))
            TopGrp = cmds.group(n=(self.prefix + 'FKController_Grp1_' + str(j)))
            All_TopGrp.append(TopGrp)
            cmds.delete(cmds.parentConstraint((self.prefix + str(FK_List[j]) + '_BaseController'), TopGrp, w=1))

            if j > 0:
                cmds.parent((self.prefix + 'FKController_Grp1_' + str(j)),
                            (self.prefix + 'FKController' + str(j - 1)))
            if j > (len(self.curve_point)-2):
                cmds.parentConstraint((self.prefix + 'FKController' + str(j)),
                                      (self.prefix + str(FK_List[j]) + '_BaseController_Grp1'), w=1)
            j = j + 1
        j = 0
        All_Loc = []
        for i in FK_List:
            if j < (len(self.curve_point) - 1):
                cmds.spaceLocator(p=(0, 0, 0), n=(self.prefix + 'Loc' + str(j)))
                cmds.setAttr((self.prefix + 'Loc' + str(j) + '.v'), 0)
                Loc = cmds.ls(sl=1)
                All_Loc.append(Loc)
                cmds.parent(Loc, (self.prefix + 'FKController_Grp1_' + str(len(self.curve_point) - 1)))
                cmds.delete(cmds.parentConstraint((self.prefix + 'FKController_Grp1_' + str(j), Loc[0]), w=1))
                cmds.connectAttr((Loc[0] + '.translate'),
                                 (self.prefix + 'FKController_Grp1_' + str(len(FK_List) - 1 - j) + '.translate'), f=1)
                cmds.connectAttr((Loc[0] + '.rotate'),
                                 (self.prefix + 'FKController_Grp1_' + str(len(FK_List) - 1 - j) + '.rotate'), f=1)
                if cmds.objExists((self.prefix + 'Loc' + str(j - 1))):
                    cmds.parent((self.prefix + 'Loc' + str(j - 1)), (self.prefix + 'Loc' + str(j)))
                cmds.parentConstraint((self.prefix + 'FKController' + str(j)), All_Loc[j], w=1)
            j = j + 1
        cmds.parent((self.prefix + 'FKController_Grp1_0'), (self.prefix + 'All_Grp'))
        cmds.parentConstraint((self.prefix + 'TotalControl_Curve'), (self.prefix + 'FKController_Grp1_0'), mo=1, w=1)
        cmds.scaleConstraint((self.prefix + 'TotalControl_Curve'), (self.prefix + 'FKController_Grp1_0'), mo=1)
        #添加fk的显示隐藏
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='FK_ShowA',at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.FK_ShowA'), e=1,keyable=True)

        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='FK_ShowB', at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.FK_ShowB'), e=1, keyable=True)
        for i in range(0, (len(self.curve_point)*2-1)):
            if i < (len(self.curve_point)-1):
                cmds.connectAttr((self.prefix + 'TotalControl_Curve.FK_ShowA'), (self.prefix + 'FKController' + str(i) + 'Shape.overrideVisibility'), force=1)
            else:
                cmds.connectAttr((self.prefix + 'TotalControl_Curve.FK_ShowB'), (self.prefix + 'FKController' + str(i) + 'Shape.overrideVisibility'), force=1)

    # 添加拖拽
    def add_drag(self):
        # 修改FK
        FK_Curve = cmds.curve(p=[(0, 0, 0), (0.2, 0, 0), (0.8, 0, 0), (1, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3,
                              n=(self.prefix + 'FKSize'))
        cmds.addAttr((self.prefix + 'FKSize'), ln='FK_SizeA', dv=0.7, at='double')
        cmds.setAttr((self.prefix + 'FKSize.FK_SizeA'), e=1, keyable=True)
        cmds.addAttr((self.prefix + 'FKSize'), ln='FK_SizeB', dv=0.5, at='double')
        cmds.setAttr((self.prefix + 'FKSize.FK_SizeB'), e=1, keyable=True)
        cmds.setAttr((FK_Curve + '.v'), 0)
        cmds.parent(FK_Curve, (self.prefix + 'TotalControl_Curve'))

        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((FK_Curve + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)

        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1X'), f=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1Y'), f=1)
        cmds.connectAttr((self.prefix + 'FKSize.FK_SizeB'), (multiplyDivide + '.input2Y'), f=1)
        cmds.connectAttr((self.prefix + 'FKSize.FK_SizeA'), (multiplyDivide + '.input2X'), f=1)
        for i in range(0, (len(self.curve_point) * 2 - 1)):
            CopyCurveShape = cmds.listRelatives((self.prefix + 'FKController' + str(i)), s=1)

            makeNurbCircle = cmds.listConnections(CopyCurveShape[0] + '.create')
            if i > (len(self.curve_point) - 1):
                cmds.connectAttr((multiplyDivide + '.outputY'), (makeNurbCircle[0] + '.radius'), f=1)

            else:
                cmds.connectAttr((multiplyDivide + '.outputX'), (makeNurbCircle[0] + '.radius'), f=1)

        cmds.delete((self.prefix + 'FKController_Grp1_0_parentConstraint1'),
                    (self.prefix + 'FKController_Grp1_0_scaleConstraint1'))
        # 拖拽控制器总数量
        Drag_Curve = cmds.curve(p=[(0, 0, 0), (0.2, 0, 0), (0.8, 0, 0), (1, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3, n=self.prefix + self.curve + '_DragCurve')
        drag_curve_shape = cmds.listRelatives(Drag_Curve, s=1)

        cmds.rebuildCurve(Drag_Curve, rt=0, ch=0, end=1, d=3, kr=0, s=(self.drag_controllers_num-1)*2-1, kcp=0, tol=0, kt=0, rpo=1, kep=0)




        cmds.select(Drag_Curve)
        cmds.duplicate(rr=1)
        a = cmds.ls(sl=1)
        # 创建曲面
        # cmds.extrude(Drag_Curve, upn=0, dl=1, ch=0, rotation=0, length=1, scale=1, et=0, rn=True,po=0)
        cmds.extrude(a, upn=1, dl=3, ch=0, rotation=0, length=0.01, scale=1, et=0, rn=False, po=0)
        Surface = cmds.ls(sl=1)
        cmds.rebuildSurface(Surface[0], rt=0, kc=0, fr=0, ch=0, end=1, sv=1, su=(self.drag_controllers_num-1)*2-1, kr=0, dir=2, kcp=0, tol=0,
                          dv=3, du=3, rpo=1)
        #Surface = cmds.ls(sl=1)
        #cmds.DeleteHistory()
        cmds.delete(a)


        cmds.select(Drag_Curve + '.cv[0:]')
        drag_curve_point = cmds.ls(sl=1, fl=1)
        Num = []
        all_drag_cluster = []
        for i in range(0, self.drag_controllers_num):
            Num.append(i)
        for i in range(-1 * self.drag_controllers_num, 0):
            Num.append(len(self.curve_point) + i)
        for i in range(0, self.drag_controllers_num):
            cmds.select(drag_curve_point[i])
            Drag_Cluster = cmds.cluster()
            cmds.setAttr(Drag_Cluster[1]+'.v',0)
            all_drag_cluster.append(Drag_Cluster[1])
            cmds.delete(cmds.parentConstraint((self.prefix + str(Num[i]) + '_BaseController_Grp1'), Drag_Cluster[1], w=1))
        for i in range(0, self.drag_controllers_num):
            cmds.select(drag_curve_point[len(drag_curve_point)-i-1])
            Drag_Cluster = cmds.cluster()
            cmds.setAttr(Drag_Cluster[1] + '.v', 0)
            all_drag_cluster.append(Drag_Cluster[1])
            cmds.delete(cmds.parentConstraint((self.prefix + str(Num[len(drag_curve_point)-i-1]) + '_BaseController_Grp1'), Drag_Cluster[1], w=1))
        cmds.select(Drag_Curve)
        cmds.rebuildCurve(Drag_Curve, rt=0, ch=0, end=1, d=3, kr=0, s=len(self.curve_point)*10, kcp=0, tol=0, kt=0, rpo=1,
                          kep=0)
        #cmds.DeleteHistory()
        cmds.group(em=1,n=(self.prefix + 'all_drag_locator_grp'))
        all_curve_loc = []
        for i in range(0, len(self.curve_point)):
            num_list = cmds.xform(self.curve_point[i], q=1, t=1, wd=1)
            cpom = cmds.createNode('nearestPointOnCurve')
            cmds.connectAttr((drag_curve_shape[0] + '.worldSpace[0]'), (cpom + '.inputCurve'), f=1)
            cmds.setAttr(cpom + '.inPosition', num_list[0], num_list[1], num_list[2])
            loc = cmds.spaceLocator(p=(0, 0, 0), n=self.prefix + str(i) + '_drag_locator')
            all_curve_loc.append(loc[0])
            motion_path = self.others_library.path_constraint(Drag_Curve,loc[0])
            cmds.setAttr(motion_path + '.fractionMode', 0)
            num = cmds.getAttr(cpom + '.parameter')
            #cmds.connectAttr((cpom + '.parameter'), (motion_path + ".uValue"), f=1)
            cmds.setAttr((motion_path + ".uValue"), num)
            cmds.parent(loc[0],(self.prefix + 'all_drag_locator_grp'))
            cmds.delete(cpom)


        cmds.select(self.curve_point[:self.drag_controllers_num], self.curve_point[-1 * self.drag_controllers_num:])
        drag_curve_point = cmds.ls(sl=1, fl=1)
        NumList = []
        for i in range(0, self.drag_controllers_num):
            NumList.append(i)
        for i in range(-1 * self.drag_controllers_num, 0):
            NumList.append(len(self.curve_point) + i)
        # 创建基础控制器
        i = 0
        for point in drag_curve_point[0:self.drag_controllers_num * 2]:
            cmds.select(point)
            Num = 17
            Radius = 6
            if i > 0 and i < self.drag_controllers_num*2-1:
                Radius = 4
                Num = 6
            self.curve_library.create_curve(self.curve_library_path,'正方形')
            self.controller.modify_vontroller_shape('scale', 1, Radius, Radius)
            cmds.rename((self.prefix + str(i) + '_DragController'))
            circle = cmds.ls(sl=1)

            cmds.setAttr((self.prefix + str(i) + '_DragController.overrideEnabled'),1)
            self.curve_library.change_curve_color('Index', circle, [0, 0, 0], Num)
            cmds.group(n=(self.prefix + str(i) + '_DragController_Grp2'))
            TopGrp = cmds.group(n=(self.prefix + str(i) + '_DragController_Grp1'))
            cmds.delete(cmds.parentConstraint(('LocJoint_'+str(NumList[i])), TopGrp, w=1))

            i = i + 1

        # cmds.move(0, 0, -0.5, r=1, os=1, wd=1)
        # cmds.makeIdentity(apply=True, t=1)
        # 创建控制曲面的蔟
        for i in range(0, len(drag_curve_point)):
            cmds.select(Surface[0] + '.cv[' + str(i) + '][0:*]')
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            cmds.delete(cmds.parentConstraint((self.prefix + str(i) + '_DragController'), Cluster[1], weight=1))
            cmds.parent(Cluster[1], (self.prefix + str(i) + '_DragController'))

        # 创建毛囊附着表面
        All_DragFollicle_Grp = cmds.group(em=1, n=(self.prefix + 'All_DragFollicle_Grp'))
        All_DragLoc_Grp = cmds.group(em=1, n=(self.prefix + 'All_DragLoc_Grp'))
        shape = cmds.listRelatives(Surface, s=1)
        for i in range(0, len(self.curve_point)):
            cpom = cmds.createNode('closestPointOnSurface')
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
            decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
            #cmds.connectAttr((self.prefix + str(i) + '_BaseController.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'),
            #                 force=1)
            cmds.connectAttr((self.prefix + str(i) + '_drag_locator.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'),force=1)

            cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
            follicleShape = cmds.createNode('follicle', n=(self.prefix + str(i) + '_BaseController_Grp1' + '_follicleShape'))
            follicle = cmds.listRelatives(follicleShape, p=1)
            cmds.connectAttr((shape[0] + '.worldSpace[0]'),
                             (self.prefix + str(i) + '_BaseController_Grp1_follicleShape.inputSurface'), f=1)
            cmds.connectAttr((shape[0] + '.worldMatrix[0]'),
                             (self.prefix + str(i) + '_BaseController_Grp1_follicleShape.inputWorldMatrix'), f=1)
            cmds.connectAttr((self.prefix + str(i) + '_BaseController_Grp1_follicleShape.outTranslate'),
                             (self.prefix + str(i) + '_BaseController_Grp1_follicle.translate'), f=1)
            cmds.connectAttr((self.prefix + str(i) + '_BaseController_Grp1_follicleShape.outRotate'),
                             (self.prefix + str(i) + '_BaseController_Grp1_follicle.rotate'), f=1)
            #cmds.setAttr((self.prefix + str(i) + '_BaseController_Grp1_follicle.parameterU'),
            #             cmds.getAttr((cpom + '.parameterU')))
            #cmds.setAttr((self.prefix + str(i) + '_BaseController_Grp1_follicle.parameterV'),
            #             cmds.getAttr((cpom + '.parameterV')))
            cmds.connectAttr((cpom + '.parameterU'),(self.prefix + str(i) + '_BaseController_Grp1_follicle.parameterU'), f=1)
            cmds.connectAttr((cpom + '.parameterV'),(self.prefix + str(i) + '_BaseController_Grp1_follicle.parameterV'), f=1)

            cmds.select(cl=1)
            cmds.parent(follicle[0], All_DragFollicle_Grp)
            cmds.spaceLocator(p=(0, 0, 0), n=(self.prefix + 'DragLoc' + str(i)))
            cmds.parent((self.prefix + 'DragLoc' + str(i)), (self.prefix + 'All_DragLoc_Grp'))
            cmds.delete(cmds.parentConstraint((self.prefix + 'FKController' + str(i)), (self.prefix + 'DragLoc' + str(i)), w=1))
            cmds.parentConstraint(follicle[0], (self.prefix + 'DragLoc' + str(i)), mo=1, w=1)
            # cmds.delete(cpom, decomposeMatrix)
        for i in range(0, len(self.curve_point) - 1):
            cmds.parent((self.prefix + 'DragLoc' + str(i + 1)), (self.prefix + 'DragLoc' + str(i)))
        for i in range(0, len(self.curve_point)):
            cmds.connectAttr((self.prefix + 'DragLoc' + str(i) + '.translate'),
                             (self.prefix + 'FKController_Grp1_' + str(i) + '.translate'), f=1)
            cmds.connectAttr((self.prefix + 'DragLoc' + str(i) + '.rotate'),
                             (self.prefix + 'FKController_Grp1_' + str(i) + '.rotate'), f=1)
        # 整理文件
        for i in range(0, self.drag_controllers_num):
            cmds.parent(all_drag_cluster[i],self.prefix + str(i) + '_DragController')
            cmds.parent(all_drag_cluster[self.drag_controllers_num+i], self.prefix + str(self.drag_controllers_num*2-i-1) + '_DragController')

        #cmds.delete(Drag_Curve)
        for i in range(1, self.drag_controllers_num * 2):
            if i < self.drag_controllers_num+1:
                cmds.parent((self.prefix + str(i) + '_DragController_Grp1'), (self.prefix + str(i - 1) + '_DragController'))
            else:
                cmds.parent((self.prefix + str(i - 1) + '_DragController_Grp1'), (self.prefix + str(i) + '_DragController'))
        for i in range(1, self.drag_controllers_num * 2):
            if i > 2 and i < (self.drag_controllers_num * 2 - 3):
                print((self.drag_controllers_num * 2 - 2))
                cmds.setAttr((self.prefix + str(i) + '_DragController_Grp1.translateX'),
                             (cmds.getAttr((self.prefix + str(i) + '_DragController_Grp1.translateX'))) * 0.01)
                cmds.setAttr((self.prefix + str(i) + '_DragController_Grp1.translateY'),
                             (cmds.getAttr((self.prefix + str(i) + '_DragController_Grp1.translateY'))) * 0.01)
                cmds.setAttr((self.prefix + str(i) + '_DragController_Grp1.translateZ'),
                             (cmds.getAttr((self.prefix + str(i) + '_DragController_Grp1.translateZ'))) * 0.01)
        cmds.group((self.prefix + 'all_drag_locator_grp'),Surface,Drag_Curve, All_DragFollicle_Grp, All_DragLoc_Grp, n=(self.prefix + 'All_DragFollicleAttachment_Grp'))
        cmds.group((self.prefix + 'All_DragFollicleAttachment_Grp'), (self.prefix + '0_DragController_Grp1'),
                   (self.prefix + str(self.drag_controllers_num * 2 - 1) + '_DragController_Grp1'),
                   n=(self.prefix + 'All_Drag_Grp'))
        cmds.parent((self.prefix + 'All_Drag_Grp'), (self.prefix + 'All_Grp'))
        cmds.setAttr((self.prefix + 'All_DragFollicleAttachment_Grp.inheritsTransform'), 0)
        cmds.setAttr((self.prefix + 'All_DragFollicleAttachment_Grp.v'), 0)
        cmds.parentConstraint((self.prefix + 'TotalControl_Curve'), (self.prefix + 'All_Drag_Grp'), mo=1, w=1)
        cmds.scaleConstraint((self.prefix + 'TotalControl_Curve'), (self.prefix + 'All_Drag_Grp'), mo=1)
        # 添加拖拽的显示隐藏
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='IK_Drag', at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.IK_Drag'), e=1, keyable=True)
        cmds.connectAttr((self.prefix + 'TotalControl_Curve.IK_Drag'), (self.prefix + 'All_Drag_Grp.visibility'), force=1)
        cmds.addAttr((self.prefix + 'TotalControl_Curve'), ln='IK_DragSecondary', at='bool')
        cmds.setAttr((self.prefix + 'TotalControl_Curve.IK_DragSecondary'), e=1, keyable=True)
        for i in range(1, (self.drag_controllers_num * 2-1)):
            cmds.connectAttr((self.prefix + 'TotalControl_Curve.IK_DragSecondary'), (self.prefix + str(i) + '_DragController.overrideVisibility'), force=1)
    ##########'''#############################################################

    # 创建测试样条与模型
    def create_test(self):
        curve = cmds.curve(p=[(-12, 0, 0), (-4, 0, 0), (4, 0, 0), (12, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3)
        cmds.rebuildCurve(curve, rt=0, ch=0, end=1, d=3, kr=0, s=10, kcp=0, tol=0.01, kt=0, rpo=1, kep=1)
        cmds.polyPlane(cuv=2, sy=1, sx=50, h=1, ch=0, w=24, ax=(0, 1, 0))
window = Window()
if __name__ == '__main__':
    window.show()

