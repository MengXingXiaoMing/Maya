# -*- coding: utf-8 -*-
import inspect
import os

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

import inspect
import importlib

import ui_edit
from ui_edit import *
importlib.reload(ui_edit)

import maya_common
from maya_common import *
importlib.reload(maya_common)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('驱动器(Maya'+self.maya_version+')')
        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()

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
    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('选择驱动骨骼')

        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton('加载')

        self.button_3 = QtWidgets.QPushButton('选择驱动骨骼父对象')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_4 = QtWidgets.QPushButton('加载')

        self.button_5 = QtWidgets.QPushButton('创建驱动控制')

        self.button_6 = QtWidgets.QPushButton('选择链接源')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_7 = QtWidgets.QPushButton('加载')

        self.button_8 = QtWidgets.QPushButton('选择链接目标')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_9 = QtWidgets.QPushButton('加载')

        self.text_1 = QtWidgets.QLabel('倍率')
        self.line_edit_5 = QtWidgets.QLineEdit('1')

        self.button_10 = QtWidgets.QPushButton('链接')

        self.button_11 = QtWidgets.QPushButton('选择点积驱动样条添加驱动定位器')

        self.button_12 = QtWidgets.QPushButton('创建球形距离驱动器（如果选择其控制器则添加其定位器）')
        self.button_13 = QtWidgets.QPushButton('选择物体创建不规则物体距离驱动器（如果选择以创建过此驱动的物体则添加其定位器）')
        self.button_14 = QtWidgets.QPushButton('选择物体删除其关联的不规则物体距离驱动器')



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

        h_Box_layout_2.addWidget(self.button_5)
        h_Box_layout_2.addWidget(self.button_11)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_2)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.button_6)
        h_Box_layout_5.addWidget(self.line_edit_3)
        h_Box_layout_5.addWidget(self.button_7)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_6)
        h_Box_layout_6.addWidget(self.button_8)
        h_Box_layout_6.addWidget(self.line_edit_4)
        h_Box_layout_6.addWidget(self.button_9)

        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_7)
        h_Box_layout_7.addWidget(self.text_1)
        h_Box_layout_7.addWidget(self.line_edit_5)
        h_Box_layout_7.addWidget(self.button_10)

        main_layout.addWidget(self.button_12)
        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.button_13)
        h_Box_layout_8.addWidget(self.button_14)
        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(lambda :self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))
        self.button_3.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit']))
        self.button_4.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))
        self.button_5.clicked.connect(self.create_drver)
        self.button_6.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit']))
        self.button_7.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))
        self.button_8.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_4, ['QLineEdit']))
        self.button_9.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_4, ['QLineEdit']))
        self.button_10.clicked.connect(self.connect_attribute)
        self.button_11.clicked.connect(self.create_get_num_loc)
        self.button_12.clicked.connect(self.create_distance_drver)
        self.button_13.clicked.connect(self.create_irregular_object_weight)
        self.button_14.clicked.connect(self.delete_irregular_range_driver)

    # 创建点积驱动基础
    def create_model(self, num):
        curve = cmds.curve(n='dot_drver'+str(num),p=[(0, -2, 0), (0, 0, 0), (0, -2, 0)], k=[0, 1, 2], d=1)

        all_cluster_grp = []
        all_loc = []
        for i in [0, 2]:
            cluster = cmds.cluster(curve + '.cv[' + str(i) + ']')
            grp = cmds.group(cluster,n=cluster[0] + '_grp')
            all_cluster_grp.append(grp)
            cmds.setAttr(grp + '.rotatePivot', 0, 0, 0)
            cmds.setAttr(grp + '.scalePivot', 0, 0, 0)
            loc = cmds.spaceLocator(n=('dot_drver' + str(num) + '_t_loc' +str(i)), p=(0, 0, 0))[0]
            cmds.setAttr(loc + '.ty', -2)
            all_loc.append(loc)
            cmds.pointConstraint(cluster[1], loc, offset=(0, 0, 0), weight=1)
            if i == 0:
                cmds.setAttr(grp + '.rz', 30)
            else:
                cmds.setAttr(grp + '.rz', 10)

        cone = cmds.revolve(curve, esw=360, ch=1, ulp=1, degree=3, ut=0, ssw=0, s=8, tol=0.01, ax=(0, 1, 0), rn=0, po=0)
        # print(cone)
        sphere = cmds.sphere(n=('dot_sphere_' + str(num)), esw=360, ch=0, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1,
                             tol=0.01, nsp=4, ax=(0, 1, 0))
        # print(sphere)
        new_surface = cmds.nurbsBoolean(cone[0], sphere, ch=1, nsf=1, op=2, n='dot_drver_cluster' + str(num))
        # print(new_surface)
        cmds.setAttr(new_surface[0] + '.template', 1)
        # 建立数值定位器
        ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_' + str(num) + '_loc0'))
        num_curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(ls_loc[0] + '_num'))
        cmds.setAttr(num_curve + ".overrideEnabled", 1)
        cmds.setAttr(num_curve + ".overrideDisplayType", 2)
        # cmds.setAttr((curve + '.sx'), 0.0001)
        # cmds.setAttr((curve + '.sy'), 0.0001)
        # cmds.setAttr((curve + '.sz'), 0.0001)
        cmds.addAttr(ls_loc[0], ln='num', dv=1, at='double')
        cmds.setAttr((ls_loc[0] + '.num'), e=1, keyable=True)
        shape = cmds.listRelatives(num_curve, c=1, type='nurbsCurve')
        paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
        cmds.parent(num_curve, ls_loc)
        cmds.connectAttr((ls_loc[0] + '.num'), (paramDimension + '.uParamValue'), f=1)
        cmds.setAttr(ls_loc[0] + '.translateY', -1)

        grp_1 = cmds.group(curve, all_cluster_grp, all_loc, cone, sphere, n='dot_count_' + str(num) + '_Grp')
        cmds.setAttr(grp_1 + '.visibility', 0)
        # 建立控制器
        curve = cmds.curve(p=[(0.0, 0.0, 0.0), (1.3246660753366768e-16, -1.0151220316349963, 0.0),
                              (0.0399518620411479, -1.0205214288941349, 0.0),
                              (0.07719707184685853, -1.03594916120812, 0.0),
                              (0.1092661723850182, -1.0603803444126723, 0.0),
                              (0.13369754874488846, -1.0924495608444404, 0.0),
                              (0.14912501063975567, -1.1296946933878147, 0.0),
                              (0.15452572135840073, -1.169646602968543, 0.0), (0.0, -1.1696465940573089, 0.0),
                              (1.3246660753366768e-16, -1.0151220316349963, 0.0),
                              (-0.0399518620411479, -1.0205214288941349, 0.0),
                              (-0.07719707184685853, -1.03594916120812, 0.0),
                              (-0.1092661723850182, -1.0603803444126723, 0.0),
                              (-0.13369754874488846, -1.0924495608444404, 0.0),
                              (-0.14912501063975567, -1.1296946933878147, 0.0),
                              (-0.15452572135840073, -1.169646602968543, 0.0),
                              (-0.14912501063975567, -1.2095984560975157, 0.0),
                              (-0.13369754874488846, -1.24684366590469, 0.0),
                              (-0.1092661723850182, -1.2789127664433722, 0.0),
                              (-0.07719707184685853, -1.3033441428048105, 0.0),
                              (-0.0399518620411479, -1.3187716046981095, 0.0),
                              (1.7031435161511713e-16, -1.3241723154157095, 0.0),
                              (0.0399518620411479, -1.3187716046981095, 0.0),
                              (0.07719707184685853, -1.3033441428048105, 0.0),
                              (0.1092661723850182, -1.2789127664433722, 0.0),
                              (0.13369754874488846, -1.24684366590469, 0.0),
                              (0.14912501063975567, -1.2095984560975157, 0.0),
                              (0.15452572135840073, -1.169646602968543, 0.0),
                              (-0.15452572135840073, -1.169646602968543, 0.0), (0.0, -1.1696465940573089, 0.0),
                              (1.7031435161511713e-16, -1.3241723154157095, 0.0)],
                           k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
                              16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0],
                           d=1, n=('dot_curve_' + str(num)))
        cmds.setAttr((curve + '.tx'), lock=1)
        cmds.setAttr((curve + '.ty'), lock=1)
        cmds.setAttr((curve + '.tz'), lock=1)
        cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleY'), f=1)
        cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleZ'), f=1)

        cmds.addAttr(curve, ln='range', min=0.1, max=179.9, dv=30, at='double')
        cmds.setAttr((curve + '.range'), e=1, keyable=True)
        cmds.connectAttr((curve + '.range'), (all_cluster_grp[0] + '.rotateZ'), f=1)

        cmds.addAttr(curve, ln='inside_range', min=0.1, max=179.9, dv=0.1, at='double')
        cmds.setAttr((curve + '.inside_range'), e=1, keyable=True)
        cmds.connectAttr((curve + '.inside_range'), (all_cluster_grp[1] + '.rotateZ'), f=1)

        cmds.addAttr(curve, ln='num', dv=1, at='double')
        cmds.setAttr((curve + '.num'), e=1, keyable=True)
        cmds.connectAttr((curve + '.num'), (ls_loc[0] + '.num'), f=1)

        cmds.parent(new_surface[0], ls_loc, curve)

        grp_2 = cmds.group(em=1, n=(curve + '_grp'))
        cmds.parent(curve, grp_2)
        grp_3 = cmds.group(grp_1, grp_2, n='dot_drver_grp' + str(num))

        vectorProduct_2 = cmds.createNode('vectorProduct')
        cmds.setAttr(vectorProduct_2 + '.input1Y', -1)

        cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_2 + '.input2'), f=1)
        cmds.setAttr(vectorProduct_2 + '.normalizeOutput', 1)

        setRange = cmds.createNode('setRange')
        cmds.setAttr(setRange + '.maxX', 1)
        cmds.setAttr(setRange + '.oldMaxX', 1)

        all_vectorProduct = []
        for fo in all_loc:
            vectorProduct = cmds.createNode('vectorProduct')
            cmds.setAttr(vectorProduct + '.input1Y', -1)
            cmds.connectAttr((fo + '.translate'), (vectorProduct + '.input2'), f=1)
            cmds.setAttr(vectorProduct + '.normalizeOutput', 1)
            all_vectorProduct.append(vectorProduct)
        cmds.connectAttr((all_vectorProduct[0] + '.outputX'), (setRange + '.oldMinX'), f=1)
        cmds.connectAttr((all_vectorProduct[1] + '.outputX'), (setRange + '.oldMaxX'), f=1)

        cmds.connectAttr((vectorProduct_2 + '.outputX'), (setRange + '.valueX'), f=1)

        cmds.connectAttr((setRange + '.outValueX'), (curve + '.num'), f=1)

        return grp_3, grp_2, ls_loc

    # 创建点积驱动
    def create_drver(self):
        drver_joint = self.line_edit_1.text()
        drver_joint_parent = self.line_edit_2.text()
        all_dot_grp = 'All_dot_drver_grp'
        if not cmds.objExists(all_dot_grp):
            cmds.group(n=all_dot_grp, em=1)
        all_grp = cmds.ls('dot_drver_grp*')
        num = 0
        if all_grp:
            all_grp_num = []
            for grp in all_grp:
                num = int(grp[13:])
                all_grp_num.append(num)
            # 求最大值
            max_num = max(all_grp_num)
            num = max_num + 1

        top_grp, grp, ls_loc = self.create_model(num)
        cmds.parent(top_grp, all_dot_grp)

        if drver_joint:
            cmds.pointConstraint(drver_joint, grp, offset=(0, 0, 0), weight=1)
            cmds.scaleConstraint(drver_joint, grp, mo=1, weight=1)
            child_joint = cmds.listRelatives(drver_joint, c=1, type='joint')
            if child_joint:
                cmds.pointConstraint(child_joint[0], ls_loc, weight=1)
        if drver_joint_parent:
            cmds.orientConstraint(drver_joint_parent, grp, offset=(0, 0, 0), weight=1)
        cmds.select(ls_loc)
        cmds.warning('点积驱动创建完成，请自行构建链接,如果缺少加载则不运行部分约束。')

    # 简单链接属性
    def connect_attribute(self):
        soure = self.line_edit_3.text()
        target = self.line_edit_4.text()
        Magnification = float(self.line_edit_5.text())
        multiplyDivide = cmds.createNode('multiplyDivide')
        cmds.connectAttr(soure, (multiplyDivide + '.input1X'), f=1)
        cmds.setAttr((multiplyDivide + '.input2X'), Magnification)
        cmds.connectAttr((multiplyDivide + '.outputX'), target, f=1)

    # 添加点积驱动额外定位器
    def create_get_num_loc(self):
        sel = cmds.ls(sl=1)
        top_num = sel[0][10:]
        # print(top_num)
        all_loc = cmds.ls('dot_' + top_num + '_loc*')
        # print(all_loc)
        new_loc = []
        for loc in all_loc:
            child = cmds.listRelatives(loc, c=1, type='locator')
            if child:
                new_loc.append(loc)
        # print(new_loc)
        # print(new_loc[0][8+len(top_num):])
        num = 0
        if new_loc:
            all_loc_num = []
            for loc in new_loc:
                num = int(loc[8 + len(top_num):])
                all_loc_num.append(num)
            # 求最大值
            max_num = max(all_loc_num)
            num = max_num + 1

        if num != 0:
            cmds.addAttr(sel[0], ln='num' + str(num), dv=1, at='double')
            cmds.setAttr((sel[0] + '.num' + str(num)), e=1, keyable=True)

            ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_' + top_num + '_loc' + str(num)))
            curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(ls_loc[0] + '_num'))
            cmds.setAttr(curve + '.overrideEnabled', 1)
            cmds.setAttr(curve + '.overrideDisplayType', 2)
            cmds.addAttr(ls_loc[0], ln='num', dv=1, at='double')
            cmds.setAttr((ls_loc[0] + '.num'), e=1, keyable=True)
            shape = cmds.listRelatives(curve, c=1, type='nurbsCurve')
            paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
            cmds.parent(curve, ls_loc)
            cmds.connectAttr((ls_loc[0] + '.num'), (paramDimension + '.uParamValue'), f=1)

            cmds.parent(ls_loc, sel)

            all_range_loc = [('dot_drver' + top_num + '_t_loc0'), ('dot_drver' + top_num + '_t_loc2')]
            vectorProduct_1 = cmds.listConnections(all_range_loc[0], d=1, s=1, type='vectorProduct')
            vectorProduct_2 = cmds.listConnections(all_range_loc[1], d=1, s=1, type='vectorProduct')

            vectorProduct_3 = cmds.createNode('vectorProduct')
            cmds.setAttr(vectorProduct_3 + '.input1Y', -1)
            cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_3 + '.input2'), f=1)
            cmds.setAttr(vectorProduct_3 + '.normalizeOutput', 1)

            setRange = cmds.createNode('setRange')
            cmds.setAttr(setRange + '.maxX', 1)
            cmds.connectAttr((vectorProduct_1[0] + '.outputX'), (setRange + '.oldMinX'), f=1)
            cmds.connectAttr((vectorProduct_2[0] + '.outputX'), (setRange + '.oldMaxX'), f=1)
            cmds.connectAttr((vectorProduct_3 + '.outputX'), (setRange + '.valueX'), f=1)

            cmds.connectAttr((setRange + '.outValueX'), (sel[0] + '.num' + str(num)), f=1)
            cmds.connectAttr((sel[0] + '.num' + str(num)), (ls_loc[0] + '.num'), f=1)
            cmds.select(ls_loc)
            cmds.warning('创建完成')
        else:
            cmds.warning('请选择驱动控制器')

    # 创建距离判断基础部分
    def create_distance_drver(self):
        sel = cmds.ls(sl=1)
        all_range_grp = cmds.ls('distance_drver*_curve')

        if not sel or (not sel[0] in all_range_grp):
            num = 0
            all_num = []
            grp = cmds.ls('range_grp_*')
            if grp:
                for g in grp:
                    num = int(g[10:])
                    all_num.append(num)
                # 求最大值
                max_num = max(all_num)
                num = max_num + 1
            loc_num = 0
            # 创建距离显示曲面
            sphere_1 = cmds.sphere(n=('range_sphere1_' + str(num)), esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8,
                                   r=1,
                                   tol=0.01, nsp=4, ax=(0, 1, 0))
            cmds.setAttr(sphere_1[0] + '.template', 1)
            sphere_2 = cmds.sphere(n=('range_sphere2_' + str(num)), esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8,
                                   r=1,
                                   tol=0.01, nsp=4, ax=(0, 1, 0))
            cmds.setAttr(sphere_2[0] + '.template', 1)
            curve = cmds.curve(n=('distance_drver' + str(num) + '_curve'),
                               p=[(-3.7551395312306146e-17, 1.1053200580606237, -7.566895313483482e-16),
                                  (0.5526600290326463, 0.9572348032834932, -7.566895313483482e-16),
                                  (0.9572348032834932, 0.5526600290326463, -7.566895313483482e-16),
                                  (1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16),
                                  (0.9572348032834932, -0.5526600290326463, -7.566895313483482e-16),
                                  (0.5526600290326463, -0.9572348032834932, -7.566895313483482e-16),
                                  (-3.7551395312306146e-17, -1.1053200580606237, -7.566895313483482e-16),
                                  (-0.5526600290326463, -0.9572348032834932, -7.566895313483482e-16),
                                  (-0.9572348032834932, -0.5526600290326463, -7.566895313483482e-16),
                                  (-1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16),
                                  (-0.9572348032834932, 0.5526600290326463, -7.566895313483482e-16),
                                  (-0.5526600290326463, 0.9572348032834932, -7.566895313483482e-16),
                                  (-3.7551395312306146e-17, 1.1053200580606237, -7.566895313483482e-16),
                                  (-3.7551395312306146e-17, 0.7815795502970119, 0.7815795502970119),
                                  (-3.7551395312306146e-17, -1.7471036244928595e-16, 1.1053200580606237),
                                  (-3.7551395312306146e-17, -0.7815795502970119, 0.7815795502970119),
                                  (-3.7551395312306146e-17, -1.1053200580606237, -7.566895313483482e-16),
                                  (-3.7551395312306146e-17, -0.7815795502970119, -0.7815795502970119),
                                  (-3.7551395312306146e-17, -1.7471036244928595e-16, -1.1053200580606237),
                                  (0.5526600290326463, -1.7471036244928595e-16, -0.9572348032834932),
                                  (0.9572348032834932, -1.7471036244928595e-16, -0.5526600290326463),
                                  (1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16),
                                  (0.9572348032834932, -1.7471036244928595e-16, 0.5526600290326463),
                                  (0.5526600290326463, -1.7471036244928595e-16, 0.9572348032834932),
                                  (-3.7551395312306146e-17, -1.7471036244928595e-16, 1.1053200580606237),
                                  (-0.5526600290326463, -1.7471036244928595e-16, 0.9572348032834932),
                                  (-0.9572348032834932, -1.7471036244928595e-16, 0.5526600290326463),
                                  (-1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16),
                                  (-0.9572348032834932, -1.7471036244928595e-16, -0.5526600290326463),
                                  (-0.5526600290326463, -1.7471036244928595e-16, -0.9572348032834932),
                                  (-3.7551395312306146e-17, -1.7471036244928595e-16, -1.1053200580606237),
                                  (-3.7551395312306146e-17, 0.7815795502970119, -0.7815795502970119),
                                  (-3.7551395312306146e-17, 1.1053200580606237, -7.566895313483482e-16)],
                               k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
                                  16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0,
                                  30.0, 31.0, 32.0], d=1)
            cmds.addAttr(curve, ln='range0', min=0, dv=0.01, at='double')
            cmds.setAttr((curve + '.range0'), e=1, keyable=True)
            cmds.addAttr(curve, ln='range1', min=0, dv=1, at='double')
            cmds.setAttr((curve + '.range1'), e=1, keyable=True)

            cmds.connectAttr((curve + '.range1'), (curve + '.scaleX'), f=1)
            cmds.connectAttr((curve + '.range1'), (curve + '.scaleY'), f=1)
            cmds.connectAttr((curve + '.range1'), (curve + '.scaleZ'), f=1)

            cmds.connectAttr((curve + '.range0'), (sphere_1[1] + '.radius'), f=1)
            cmds.connectAttr((curve + '.range1'), (sphere_2[1] + '.radius'), f=1)

            distanceDimShape, loc_2 = self.create_distance_count(num,loc_num,curve)

            grp_1 = cmds.group(sphere_1, sphere_2, distanceDimShape, curve, loc_2, n=('range_grp_' + str(num)))
            cmds.parentConstraint(curve, sphere_1, mo=1, w=1)
            cmds.parentConstraint(curve, sphere_2, mo=1, w=1)
            if cmds.objExists('All_range_drver_grp'):
                cmds.parent(grp_1, 'All_range_drver_grp')
            else:
                cmds.group(grp_1, n='All_range_drver_grp')
            cmds.select(curve)
        else:
            num = int(sel[0][14:-6])
            all_num = []
            all_range_loc_grp = cmds.ls('distance_drver' + str(num) + '_loc1_*', type='locator')
            for loc in all_range_loc_grp:
                n = int(loc[20 + len(str(num)):-5])
                all_num.append(n)
            # 求最大值
            max_num = max(all_num)
            loc_num = max_num + 1
            # print(loc_num)
            curve = sel[0]

            distanceDimShape, loc_2 = self.create_distance_count(num, loc_num, curve)

            cmds.parent(distanceDimShape, loc_2, ('range_grp_' + str(num)))
            cmds.select(loc_2)
        cmds.warning('创建完成')

    # 创建距离判断计算部分
    def create_distance_count(self,num,loc_num,curve):
        setRange = cmds.createNode('setRange')
        cmds.setAttr((setRange + '.minX'), 1)
        cmds.connectAttr((curve + '.range0'), (setRange + '.oldMinX'), f=1)
        cmds.connectAttr((curve + '.range1'), (setRange + '.oldMaxX'), f=1)
        # 创建距离判断
        loc_1 = cmds.spaceLocator(n='distance_drver' + str(num) + '_loc0_' + str(loc_num))[0]
        cmds.setAttr((loc_1 + '.visibility'), 0)
        loc_2 = cmds.spaceLocator(n='distance_drver' + str(num) + '_loc1_' + str(loc_num))[0]
        distanceDimShape = cmds.createNode('distanceDimShape')
        cmds.setAttr((distanceDimShape + '.visibility'), 0)
        print(distanceDimShape)
        cmds.connectAttr((loc_1 + '.worldPosition[0]'), (distanceDimShape + '.startPoint'), f=1)
        cmds.connectAttr((loc_2 + '.worldPosition[0]'), (distanceDimShape + '.endPoint'), f=1)

        cmds.connectAttr((distanceDimShape + '.distance'), (setRange + '.valueX'), f=1)

        cmds.addAttr(curve, ln='num' + str(loc_num), dv=0, at='double')
        cmds.setAttr((curve + '.num' + str(loc_num)), e=1, keyable=True)
        cmds.addAttr(loc_2, ln='num', dv=0, at='double')
        cmds.setAttr((loc_2 + '.num'), e=1, keyable=True)

        cmds.connectAttr((setRange + '.outValueX'), (curve + '.num' + str(loc_num)), f=1)
        cmds.connectAttr((setRange + '.outValueX'), (loc_2 + '.num'), f=1)

        # 添加数值显示
        self.create_num_show([loc_2])
        # num_curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(loc_2 + '_num'))
        # cmds.setAttr(num_curve + ".overrideEnabled", 1)
        # cmds.setAttr(num_curve + ".overrideDisplayType", 2)
        # shape = cmds.listRelatives(num_curve, c=1, type='nurbsCurve')
        # paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
        # cmds.parent(num_curve, loc_2)
        # cmds.connectAttr((loc_2 + '.num'), (paramDimension + '.uParamValue'), f=1)

        # 整理文件
        cmds.delete(cmds.pointConstraint(curve, loc_1))
        cmds.parent(loc_1, curve)
        return distanceDimShape, loc_2



    # 创建不规则物体动态权重
    def create_irregular_object_weight(self):
        # 创建不规则形状驱动定位器
        sel = cmds.ls(sl=1)
        have_range = cmds.objExists(sel[0] + '.range')
        if have_range == True: #如果物体有范围显示，则增加定位器
            loc_0, loc_2, distanceDimShape = self.create_distance_show(sel)
            distanceDimShape=cmds.listRelatives(distanceDimShape,p=1)
            cmds.parent(loc_0, loc_2, distanceDimShape, (sel[0] + '_irregular_object_drver_grp'))
        else:
            cmds.addAttr(sel[0], ln='range', min=0.001, dv=1, at='double')
            cmds.setAttr((sel[0] + '.range'), e=1, keyable=True)
            loc_0, loc_2, distanceDimShape = self.create_distance_show(sel)
            distanceDimShape = cmds.listRelatives(distanceDimShape, p=1)
            # 添加范围指示器
            sel_shape = cmds.listRelatives(sel, c=1, type='mesh')
            if sel_shape:
                sel_copy = self.create_mesh_range_indicator(sel, sel_shape)
                cmds.group(sel_copy, loc_0, loc_2, distanceDimShape, n=sel[0] + '_irregular_object_drver_grp')
            else:
                cmds.group(loc_0, loc_2, distanceDimShape, n=sel[0] + '_irregular_object_drver_grp')
        cmds.select(loc_2)
        cmds.warning('mesh有大致范围显示，曲面没有范围显示，mesh可以缩放，但是其范围指示器不跟随缩放，如有需要请自行调整。')

    # 创建数值显示
    def create_num_show(self, sel):
        # 添加数值显示
        num_curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(sel[0] + '_num'))
        cmds.setAttr(num_curve + ".overrideEnabled", 1)
        cmds.setAttr(num_curve + ".overrideDisplayType", 2)
        shape = cmds.listRelatives(num_curve, c=1, type='nurbsCurve')
        paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
        cmds.parent(num_curve, sel[0])
        cmds.connectAttr((sel[0] + '.num'), (paramDimension + '.uParamValue'), f=1)

    # 创建距离计算
    def create_distance_show(self, sel):
        # 计算定位器添加的数量数值
        all_loc = cmds.ls(sel[0]+'_drver_num_loc*',type='locator')
        num = 0
        if all_loc:
            all_loc_num = []
            for loc in all_loc:
                num = int(loc[len(sel[0])+14:-5])
                all_loc_num.append(num)
            # 求最大值
            max_num = max(all_loc_num)
            num = max_num + 1

        loc_0 = cmds.spaceLocator(n=sel[0] + '_follow_surface0_locA'+str(num))[0]

        loc_1 = cmds.spaceLocator(n=sel[0] + '_follow_surface0_locB'+str(num))[0]
        cmds.parent(loc_1, loc_0)
        cmds.geometryConstraint(sel, loc_0, weight=1)
        cmds.normalConstraint(sel, loc_0, worldUpType="vector", aimVector=(1, 0, 0), upVector=(0, 1, 0), weight=1,
                              worldUpVector=(0, 1, 0))
        loc_2 = cmds.spaceLocator(n=sel[0] + '_drver_num_loc'+str(num))[0]
        cmds.pointConstraint(loc_2, loc_0, weight=1)
        cmds.pointConstraint(loc_2, loc_1, weight=1)
        # 创建点积计算，判断是否在法线正方向
        vectorProduct_1 = cmds.createNode('vectorProduct')
        cmds.setAttr(vectorProduct_1 + '.input1X', 1)
        cmds.connectAttr((loc_1 + '.translate'), (vectorProduct_1 + '.input2'), f=1)
        cmds.setAttr(vectorProduct_1 + '.normalizeOutput', 1)

        # 创建距离计算
        setRange = cmds.createNode('setRange')
        cmds.setAttr((setRange + '.minX'), 1)
        cmds.connectAttr((sel[0] + '.range'), (setRange + '.oldMaxX'), f=1)
        # 创建距离判断
        cmds.setAttr((loc_0 + '.visibility'), 0)
        distanceDimShape = cmds.createNode('distanceDimShape')
        cmds.setAttr((distanceDimShape + '.visibility'), 0)

        cmds.connectAttr((loc_0 + '.worldPosition[0]'), (distanceDimShape + '.startPoint'), f=1)
        cmds.connectAttr((loc_2 + '.worldPosition[0]'), (distanceDimShape + '.endPoint'), f=1)

        cmds.connectAttr((distanceDimShape + '.distance'), (setRange + '.valueX'), f=1)

        cmds.addAttr(sel[0], ln='num'+str(num), dv=0, at='double')
        cmds.setAttr((sel[0] + '.num'+str(num)), e=1, keyable=True)

        cmds.addAttr(loc_2, ln='num', dv=0, at='double')
        cmds.setAttr((loc_2 + '.num'), e=1, keyable=True)

        # 创建点积判断
        condition = cmds.createNode('condition')
        cmds.setAttr((condition + '.operation'), 2)

        cmds.connectAttr((vectorProduct_1 + '.outputX'), (condition + '.firstTerm'), f=1)
        cmds.connectAttr((setRange + '.outValueX'), (condition + '.colorIfTrueR'), f=1)

        cmds.connectAttr((condition + '.outColorR'), (sel[0] + '.num'+str(num)), f=1)
        cmds.connectAttr((condition + '.outColorR'), (loc_2 + '.num'), f=1)
        # 添加数值显示
        self.create_num_show([loc_2])
        return loc_0, loc_2, distanceDimShape

    # 创建mesh范围指示器
    def create_mesh_range_indicator(self, sel,sel_shape):
        sel_copy = cmds.duplicate(sel, rr=1)
        sel_copy_shape = cmds.listRelatives(sel_copy, c=1, type='mesh')
        cmds.connectAttr((sel_shape[0] + '.outMesh'), (sel_copy_shape[0] + '.inMesh'), f=1)
        polyExtrudeFacet = cmds.polyExtrudeFacet(sel_copy, divisions=1, off=0, taper=1, pvy=-1, pvx=-1, pvz=-1, thickness=0,
                                                 twist=0,
                                                 smoothingAngle=30, keepFacesTogether=1, constructionHistory=1)
        cmds.connectAttr((sel[0] + '.range'), (polyExtrudeFacet[0] + '.thickness'), f=1)
        cmds.parentConstraint(sel, sel_copy, w=1)

        cmds.setAttr(sel_copy[0] + '.template', 1)
        cmds.displaySmoothness(sel_copy, pointsWire=16, polygonObject=3, pointsShaded=4, divisionsV=3, divisionsU=3)
        return sel_copy

    # 删除不规则范围驱动器
    def delete_irregular_range_driver(self):
        sel = cmds.ls(sl=1)
        if cmds.objExists(sel[0] + '_irregular_object_drver_grp'):
            cmds.delete(sel[0] + '_irregular_object_drver_grp')
            all_attrs = cmds.listAttr(sel, keyable=True, multi=True, scalar=True, userDefined=True) or []
            for attr in all_attrs:
                cmds.deleteAttr(sel[0] + '.' + attr)

window = Window()
if __name__ == '__main__':
    window.show()
