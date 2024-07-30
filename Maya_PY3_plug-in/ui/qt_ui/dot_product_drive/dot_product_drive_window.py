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
        self.setWindowTitle('点积驱动(Maya'+self.maya_version+')')
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

        self.button_11 = QtWidgets.QPushButton('选择驱动样条添加驱动定位器')

        self.button_12 = QtWidgets.QPushButton('创建距离驱动器（如果选择距离驱动器控制器则添加其定位器）')



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

        main_layout.addWidget(self.button_11)
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




    def create_model(self, num):
        cone = cmds.cone(n=('dot_cone_'+str(num)), esw=360, ch=0, d=3, hr=2, ut=0, ssw=0, p=(0, -1, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))
        # print(cone)
        cmds.rebuildSurface(cone, rt=0, kc=0, fr=0, ch=0, end=1, sv=4, su=4, kr=0, dir=2, kcp=1, tol=0.01, dv=3,
                            du=3, rpo=1)
        cmds.setAttr(cone[0] + '.scaleX', 10)
        cmds.setAttr(cone[0] + '.scaleY', 10)
        cmds.setAttr(cone[0] + '.scaleZ', 10)
        # cmds.makeIdentity(cone,n=0, s=1, r=1, t=1, apply=True, pn=1)
        cluster = cmds.cluster(cone)
        # print(cluster)
        cmds.setAttr(cluster[1] + '.rotatePivot', 0, 0, 0)
        cmds.setAttr(cluster[1] + '.scalePivot', 0, 0, 0)
        sphere = cmds.sphere(n=('dot_sphere_'+str(num)), esw=360, ch=0, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))
        # print(sphere)
        new_surface = cmds.nurbsBoolean(cone, sphere, ch=1, nsf=1, op=2, n='dot_drver_cluster'+str(num))
        cmds.setAttr(new_surface[0] + '.template', 1)
        # print(new_surface)
        grp_1 = cmds.group(sphere, cluster, n='dot_drver_keep_grp'+str(num))
        cmds.setAttr(grp_1 + '.visibility', 0)
        grp_2 = cmds.group(cone, grp_1, n='dot_drver_grp'+str(num))

        ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_'+str(num)+'_loc0'))
        cmds.setAttr(ls_loc[0] + '.translateX', -10)
        cmds.setAttr(ls_loc[0] + '.translateY', -20)

        shape = cmds.listRelatives(cone, s=1)
        # TypeNurbs = cmds.ls(shape[0], type='nurbsSurface')
        cpom = cmds.createNode('closestPointOnSurface')
        cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)

        pos = cmds.xform(ls_loc[0], q=1, a=1, ws=1, t=1)
        cmds.setAttr((cpom + '.inPositionX'), pos[0])
        cmds.setAttr((cpom + '.inPositionY'), pos[1])
        cmds.setAttr((cpom + '.inPositionZ'), pos[2])
        u = float(cmds.getAttr(cpom + ".parameterU"))
        v = float(cmds.getAttr(cpom + ".parameterV"))
        follicleShape = (ls_loc[0] + '_follicleShape')
        follicle = (ls_loc[0] + '_follicle')
        cmds.createNode('follicle', n=(ls_loc[0] + "_follicleShape"))
        shape = cmds.listRelatives(cone, s=1, type='nurbsSurface')
        cmds.connectAttr((shape[0] + '.worldSpace[0]'), (follicleShape + '.inputSurface'), f=1)
        cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'), f=1)
        cmds.connectAttr((follicleShape + ".outTranslate"), (follicle + ".translate"), f=1)
        # cmds.connectAttr((follicleShape + ".outRotate"), (follicle + ".rotate"), f=1)
        cmds.setAttr((follicleShape + ".parameterU"), u)
        cmds.setAttr((follicleShape + ".parameterV"), v)

        cmds.setAttr(follicle + '.visibility', 0)

        cmds.delete(cpom)

        cmds.delete(ls_loc)

        ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_'+str(num)+'_loc0'))
        curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)],d=1, n=(ls_loc[0] + '_num'))
        cmds.setAttr(curve+".overrideEnabled", 1)
        cmds.setAttr(curve+".overrideDisplayType", 2)
        # cmds.setAttr((curve + '.sx'), 0.0001)
        # cmds.setAttr((curve + '.sy'), 0.0001)
        # cmds.setAttr((curve + '.sz'), 0.0001)
        cmds.addAttr(ls_loc[0], ln='num', dv=1, at='double')
        cmds.setAttr((ls_loc[0] + '.num'), e=1, keyable=True)
        shape = cmds.listRelatives(curve, c=1, type='nurbsCurve')
        paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
        cmds.parent(curve, ls_loc)
        cmds.connectAttr((ls_loc[0] + '.num'),(paramDimension+'.uParamValue'), f=1)

        cmds.setAttr(ls_loc[0] + '.translateY', -1)
        # cmds.setAttr(ls_loc[0] + '.visibility', 0)

        move_grp = cmds.group(em=1, n=('dot_drver_move_grp' + str(num)))
        cmds.parent(ls_loc, new_surface[0], follicle, move_grp)
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
                           d=1, n=('dot_curve_'+str(num)))
        cmds.setAttr((curve + '.tx'), lock=1)
        cmds.setAttr((curve + '.ty'), lock=1)
        cmds.setAttr((curve + '.tz'), lock=1)
        cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleY'), f=1)
        cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleZ'), f=1)
        cmds.addAttr(curve, ln='range', min=-10, max=10, dv=1, at='double')
        cmds.setAttr((curve + '.range'), e=1, keyable=True)
        cmds.connectAttr((curve + '.range'), (cluster[1] + '.scaleY'), f=1)
        cmds.addAttr(curve, ln='num', dv=1, at='double')
        cmds.setAttr((curve + '.num'), e=1, keyable=True)
        cmds.connectAttr((curve + '.num'), (ls_loc[0] + '.num'), f=1)
        grp_3 = cmds.group(em=1, n=(curve + '_grp'))
        cmds.parent(curve, grp_3)
        cmds.parent(grp_3, grp_2)
        cmds.parent(move_grp, curve)

        vectorProduct = cmds.createNode('vectorProduct')
        cmds.setAttr(vectorProduct + '.input1Y', -1)
        cmds.connectAttr((follicle + '.translate'), (vectorProduct + '.input2'), f=1)
        cmds.setAttr(vectorProduct + '.normalizeOutput', 1)

        vectorProduct_2 = cmds.createNode('vectorProduct')
        cmds.setAttr(vectorProduct_2 + '.input1Y', -1)
        cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_2 + '.input2'), f=1)
        cmds.setAttr(vectorProduct_2 + '.normalizeOutput', 1)

        setRange = cmds.createNode('setRange')
        cmds.setAttr(setRange + '.maxX', 1)
        cmds.setAttr(setRange + '.oldMaxX', 1)
        cmds.connectAttr((vectorProduct + '.outputX'), (setRange + '.oldMinX'), f=1)
        cmds.connectAttr((vectorProduct_2 + '.outputX'), (setRange + '.valueX'), f=1)

        cmds.connectAttr((setRange + '.outValueX'), (curve + '.num'), f=1)
        return grp_2, grp_3, curve, ls_loc

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

        top_grp, grp, curve, ls_loc = self.create_model(num)
        cmds.parent(top_grp, all_dot_grp)
        cmds.parentConstraint(drver_joint, grp, weight=1, skipRotate=['x', 'y', 'z'])
        cmds.orientConstraint(drver_joint_parent, grp, offset=(0, 0, 0), weight=1)
        cmds.scaleConstraint(drver_joint, grp, mo=1, weight=1)
        child_joint = cmds.listRelatives(drver_joint, c=1, type='joint')
        cmds.pointConstraint(child_joint[0],ls_loc, weight=1)
        cmds.warning('点积驱动创建完成，请自行构建链接。')


    def connect_attribute(self):
        soure = self.line_edit_3.text()
        target = self.line_edit_4.text()
        Magnification = float(self.line_edit_5.text())
        multiplyDivide = cmds.createNode('multiplyDivide')
        cmds.connectAttr(soure, (multiplyDivide + '.input1X'), f=1)
        cmds.setAttr((multiplyDivide + '.input2X'), Magnification)
        cmds.connectAttr((multiplyDivide + '.outputX'), target, f=1)


    def create_get_num_loc(self):
        sel = cmds.ls(sl=1)
        top_num = sel[0][10:]
        print(top_num)
        all_loc = cmds.ls('dot_'+top_num+'_loc*')
        print(all_loc)
        new_loc = []
        for loc in all_loc:
            child = cmds.listRelatives(loc, c=1, type='locator')
            if child:
                new_loc.append(loc)
        print(new_loc)
        print(new_loc[0][8+len(top_num):])
        num = 0
        if new_loc:
            all_loc_num = []
            for loc in new_loc:
                num = int(loc[8+len(top_num):])
                all_loc_num.append(num)
            # 求最大值
            max_num = max(all_loc_num)
            num = max_num + 1
        cmds.addAttr(sel[0], ln='num'+str(num), dv=1, at='double')
        cmds.setAttr((sel[0] + '.num'+str(num)), e=1, keyable=True)
        ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_'+top_num+'_loc'+str(num)))
        curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)],d=1, n=(ls_loc[0] + '_num'))
        cmds.setAttr(curve + ".overrideEnabled", 1)
        cmds.setAttr(curve + ".overrideDisplayType", 2)
        cmds.addAttr(ls_loc[0], ln='num', dv=1, at='double')
        cmds.setAttr((ls_loc[0] + '.num'), e=1, keyable=True)
        shape = cmds.listRelatives(curve, c=1, type='nurbsCurve')
        paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
        cmds.parent(curve, ls_loc)
        cmds.connectAttr((ls_loc[0] + '.num'),(paramDimension+'.uParamValue'), f=1)

        cmds.parent(ls_loc, ('dot_drver_move_grp'+top_num))

        follicle = ('dot_'+top_num+'_loc0_follicle')
        vectorProduct = cmds.createNode('vectorProduct')
        cmds.setAttr(vectorProduct + '.input1Y', -1)
        cmds.connectAttr((follicle + '.translate'), (vectorProduct + '.input2'), f=1)
        cmds.setAttr(vectorProduct + '.normalizeOutput', 1)

        vectorProduct_2 = cmds.createNode('vectorProduct')
        cmds.setAttr(vectorProduct_2 + '.input1Y', -1)
        cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_2 + '.input2'), f=1)
        cmds.setAttr(vectorProduct_2 + '.normalizeOutput', 1)

        setRange = cmds.createNode('setRange')
        cmds.setAttr(setRange + '.maxX', 1)
        cmds.setAttr(setRange + '.oldMaxX', 1)
        cmds.connectAttr((vectorProduct + '.outputX'), (setRange + '.oldMinX'), f=1)
        cmds.connectAttr((vectorProduct_2 + '.outputX'), (setRange + '.valueX'), f=1)

        cmds.connectAttr((setRange + '.outValueX'), (sel[0] + '.num' + str(num)), f=1)

        cmds.connectAttr((sel[0] + '.num' + str(num)), (ls_loc[0] + '.num'), f=1)
window = Window()
if __name__ == '__main__':
    window.show()
