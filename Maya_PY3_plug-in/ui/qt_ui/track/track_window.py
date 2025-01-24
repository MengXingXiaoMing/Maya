# -*- coding: utf-8 -*-
import ast

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
import math
import os
import sys
import inspect
import importlib
import maya.mel as mel
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

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import maya_common
importlib.reload(maya_common)
from maya_common import *

import others_library
importlib.reload(others_library)
from others_library import *

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('履带(Maya' + self.maya_version + ')')

        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()
        self.others_library = OthersLibrary()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version

        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    def create_widgets(self):
        # 第一行
        self.button_0 = QtWidgets.QPushButton('按选择样条创建曲面')

        self.button_1 = QtWidgets.QPushButton('选择闭合样条')
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton('加载')

        self.button_19 = QtWidgets.QPushButton('选择样条对应的曲面')
        self.line_edit_8 = QtWidgets.QLineEdit()
        self.button_20 = QtWidgets.QPushButton('加载')

        self.button_3 = QtWidgets.QPushButton('选择骨骼链根骨骼')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_4 = QtWidgets.QPushButton('加载')

        self.button_5 = QtWidgets.QPushButton('选择总控制器')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_6 = QtWidgets.QPushButton('加载')

        self.button_7 = QtWidgets.QPushButton('选择履带控制器')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_8 = QtWidgets.QPushButton('加载')

        self.button_9 = QtWidgets.QPushButton('开始生成')
        self.button_10 = QtWidgets.QPushButton('选择总控制器删除履带')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        self.button_11 = QtWidgets.QPushButton('ADV选择闭合样条')
        self.line_edit_5 = QtWidgets.QLineEdit('nurbsCircle1,nurbsCircle2')
        self.button_12 = QtWidgets.QPushButton('加载')

        self.button_13 = QtWidgets.QPushButton('ADV选择样条对应的曲面')
        self.line_edit_6 = QtWidgets.QLineEdit('extrudedSurface1,extrudedSurface2')
        self.button_14 = QtWidgets.QPushButton('加载')

        self.button_15 = QtWidgets.QPushButton('ADV选择骨骼链根骨骼')
        self.line_edit_7 = QtWidgets.QLineEdit('bbbb,aaaa')
        self.button_16 = QtWidgets.QPushButton('加载')

        self.button_21 = QtWidgets.QPushButton('ADV选择总控制器')
        self.line_edit_9 = QtWidgets.QLineEdit('Main')
        self.button_22 = QtWidgets.QPushButton('加载')

        self.button_23 = QtWidgets.QPushButton('ADV选择履带控制器')
        self.line_edit_10 = QtWidgets.QLineEdit('FKfrontWheel_R,FKfrontWheel_L')
        self.button_24 = QtWidgets.QPushButton('加载')

        self.button_17 = QtWidgets.QPushButton('ADV轮胎转成履带(还没写)')
        self.button_18 = QtWidgets.QPushButton('删除ADV轮胎转成履带(还没写)')

        # self.comboBox_99 = QtWidgets.QComboBox()
        # self.comboBox_99.addItems(['后期', '交互'])
        # self.button_99 = QtWidgets.QPushButton()
        # self.button_99.setMinimumSize(QtCore.QSize(30, 30))
        # self.button_99.setIcon(QtGui.QIcon(':/fileOpen.png'))


    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.addWidget(self.button_0)
        h_Box_layout_1.setSpacing(1)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3)
        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_3.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.button_1)
        h_Box_layout_4.addWidget(self.line_edit_1)
        h_Box_layout_4.addWidget(self.button_2)
        h_Box_layout_4.setSpacing(1)
        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_3.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.button_19)
        h_Box_layout_5.addWidget(self.line_edit_8)
        h_Box_layout_5.addWidget(self.button_20)
        h_Box_layout_5.addWidget(self.button_3)
        h_Box_layout_5.addWidget(self.line_edit_2)
        h_Box_layout_5.addWidget(self.button_4)
        h_Box_layout_5.setSpacing(1)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_6)

        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_6.addLayout(h_Box_layout_7)
        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_7.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.button_7)
        h_Box_layout_8.addWidget(self.line_edit_4)
        h_Box_layout_8.addWidget(self.button_8)
        h_Box_layout_8.setSpacing(1)
        h_Box_layout_9 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_7.addLayout(h_Box_layout_9)
        h_Box_layout_9.addWidget(self.button_5)
        h_Box_layout_9.addWidget(self.line_edit_3)
        h_Box_layout_9.addWidget(self.button_6)
        h_Box_layout_9.setSpacing(1)

        h_Box_layout_1.addWidget(self.button_9)
        h_Box_layout_1.addWidget(self.button_10)

        h_Box_layout_1.addWidget(self.splitter_1)

        h_Box_layout_10 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_10)

        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_10.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.button_11)
        h_Box_layout_8.addWidget(self.line_edit_5)
        h_Box_layout_8.addWidget(self.button_12)
        h_Box_layout_8.setSpacing(1)
        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_10.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.button_13)
        h_Box_layout_8.addWidget(self.line_edit_6)
        h_Box_layout_8.addWidget(self.button_14)
        h_Box_layout_8.setSpacing(1)
        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_10.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.button_15)
        h_Box_layout_8.addWidget(self.line_edit_7)
        h_Box_layout_8.addWidget(self.button_16)
        h_Box_layout_8.setSpacing(1)

        h_Box_layout_11 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_11)
        h_Box_layout_12 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_11.addLayout(h_Box_layout_12)
        h_Box_layout_12.addWidget(self.button_21)
        h_Box_layout_12.addWidget(self.line_edit_9)
        h_Box_layout_12.addWidget(self.button_22)
        h_Box_layout_12.setSpacing(1)
        h_Box_layout_13 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_11.addLayout(h_Box_layout_13)
        h_Box_layout_13.addWidget(self.button_23)
        h_Box_layout_13.addWidget(self.line_edit_10)
        h_Box_layout_13.addWidget(self.button_24)
        h_Box_layout_13.setSpacing(1)

        h_Box_layout_1.addWidget(self.button_17)
        h_Box_layout_1.addWidget(self.button_18)

        main_layout.addStretch(1)

    def create_connect(self):
        self.button_0.clicked.connect(self.create_curved)

        self.button_1.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))

        self.button_19.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_8, ['QLineEdit']))
        self.button_20.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_8, ['QLineEdit']))

        self.button_3.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit']))
        self.button_4.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))

        self.button_5.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit']))
        self.button_6.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))

        self.button_7.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_4, ['QLineEdit']))
        self.button_8.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_4, ['QLineEdit']))

        self.button_9.clicked.connect(self.create_track)
        self.button_10.clicked.connect(self.delete_track)
        #
        self.button_11.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_5, ['QLineEdit']))
        self.button_12.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_5, ['QLineEdit']))

        self.button_13.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_6, ['QLineEdit']))
        self.button_14.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_6, ['QLineEdit']))

        self.button_15.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_7, ['QLineEdit']))
        self.button_16.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_7, ['QLineEdit']))

        self.button_21.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_9, ['QLineEdit']))
        self.button_22.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_9, ['QLineEdit']))

        self.button_23.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_10, ['QLineEdit']))
        self.button_24.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_10, ['QLineEdit']))

        self.button_17.clicked.connect(self.create_adv_track)
        self.button_18.clicked.connect(self.delete_adv_track)

    # 创建曲面
    def create_curved(self):
        sel = cmds.ls(sl=1)
        cmds.extrude(sel, upn=1, dl=3, ch=0, rotation=0, length=1, scale=1, et=0, rn=False, po=0,)
        cmds.rebuildSurface("extrudedSurface1", rt=0, kc=0, fr=0, ch=0, end=1, sv=4, su=4, kr=0, dir=2, kcp=1, tol=0.01,
                        dv=3, du=1, rpo=1)

    # 创建履带
    def create_track(self):
        print('创建履带')
        # 获取要删除的节点
        need_delete = []

        # 加载轮子长度
        self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit'])
        # cmds.select('nurbsCircle1,nurbsCircle2')
        track_perimeter = cmds.ls(sl=1)
        # 加载解除曲面
        self.maya_common.select_text_target(self.line_edit_8, ['QLineEdit'])
        # cmds.select('extrudedSurface1,extrudedSurface2')
        track_curved = cmds.ls(sl=1)
        # 加载输出骨骼
        self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit'])
        # cmds.select('bbbb,aaaa')
        track_joint = cmds.ls(sl=1)
        joint = []
        for each in track_joint:
            cmds.select(each)
            cmds.SelectHierarchy()
            joint_ls = cmds.ls(sl=1)
            joint.append(joint_ls)
        # 加载总控制器
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        # cmds.select('joint2_C,joint105_C')
        track_parent_controller = cmds.ls(sl=1)
        # 加载轮子控制器
        self.maya_common.select_text_target(self.line_edit_4, ['QLineEdit'])
        # cmds.select('joint2_C')
        track_controller = cmds.ls(sl=1)

        grp = cmds.group(em=1, n='All_track_Grp')
        need_delete.append(grp)
        # 给总样条添加属性
        cmds.addAttr(track_parent_controller, ln='track', at='bool')
        need_delete.append(track_parent_controller[0] + '.track')
        cmds.addAttr(track_parent_controller, ln='track_joint', at='bool')
        need_delete.append(track_parent_controller[0]+'.track_joint')
        # cmds.setAttr((track_parent_controller[0]+'.track'), e=1, channelBox=True, lock=True)
        cmds.addAttr(track_parent_controller, ln='baking_tracks', at='bool')
        cmds.setAttr((track_parent_controller[0] + '.baking_tracks'), e=1, channelBox=True)
        need_delete.append(track_parent_controller[0] + '.baking_tracks')
        cmds.addAttr(track_parent_controller, ln='start_frame', dv=101, at='long')
        cmds.setAttr((track_parent_controller[0] + '.start_frame'), e=1, channelBox=True)
        need_delete.append(track_parent_controller[0] + '.start_frame')
        cmds.addAttr(track_parent_controller, ln='expression_type', en="tradition:baking:", at="enum")
        cmds.setAttr((track_parent_controller[0] + '.expression_type'), e=1, channelBox=True)
        need_delete.append(track_parent_controller[0] + '.expression_type')
        cmds.select(track_parent_controller[0])
        cmds.addAttr(track_parent_controller[0], ln='node', dt='string')
        need_delete.append(track_parent_controller[0] + '.node')


        # 添加地面碰撞
        collision_grp = cmds.group(track_perimeter, track_curved, n='All_collision_grp')
        cmds.parent(collision_grp, grp)
        box_range = cmds.xform(collision_grp, q=1, bb=1)
        # print(box_range)
        collision_conter = cmds.xform(collision_grp, q=True, ws=True, sp=True)
        # print(collision_conter)
        # 创建接触面
        w_max = box_range[4] - box_range[0]
        h_max = box_range[5] - box_range[2]
        collision_plane = cmds.polyPlane(w=w_max * 2, h=h_max * 2, sx=w_max * 20, sy=h_max * 20, ax=(0, 1, 0), cuv=2, ch=0,
                       n='track_collision_plane')
        # print(collision_plane)
        cmds.setAttr(collision_plane[0] + '.tx', collision_conter[0])
        cmds.setAttr(collision_plane[0] + '.tz', collision_conter[2])
        # cmds.channelBoxCommand(freezeTranslate=1)
        cmds.makeIdentity(collision_plane, apply=True, t=True, n=0)
        # 创建碰撞
        collision_node = mel.eval('cMuscle_makeMuscle(0);')
        # print(collision_node)
        cmds.setAttr(collision_node[0] + '.draw', 1)
        cmds.setAttr(collision_node[0] + '.fat', 0)
        cmds.parent(collision_plane,collision_grp)
        cmds.parentConstraint(track_parent_controller, collision_plane, w=1, mo=1)
        cmds.scaleConstraint(track_parent_controller, collision_plane, w=1, mo=1)
        # 添加平面显示隐藏属性和开启碰撞属
        cmds.addAttr(track_parent_controller, ln='collision_plane', at='bool')
        cmds.setAttr((track_parent_controller[0] + '.collision_plane'), e=1, channelBox=True)
        need_delete.append(track_parent_controller[0] + '.collision_plane')
        cmds.addAttr(track_parent_controller, ln='Constrain_Fat', dv=0, at='double')
        cmds.setAttr((track_parent_controller[0] + '.Constrain_Fat'), e=1, keyable=True)
        need_delete.append(track_parent_controller[0] + '.Constrain_Fat')
        cmds.addAttr(track_parent_controller, ln='collision', at='bool')
        cmds.setAttr((track_parent_controller[0] + '.collision'), e=1, channelBox=True)
        need_delete.append(track_parent_controller[0] + '.collision')
        top_condition = cmds.shadingNode('condition', asUtility=1)
        cmds.connectAttr((track_parent_controller[0] + '.collision'), (top_condition + '.firstTerm'))
        cmds.setAttr((top_condition + '.colorIfTrueR'), 2)
        cmds.setAttr((top_condition + '.colorIfFalseR'), 0)


        ########################################################################################################################
        for i in range(0, len(track_controller)):
            # 创建烘焙骨骼
            cmds.select(cl=1)
            baking_bones = cmds.joint(p=(0, 0, 0), n=(track_controller[i] + '_baking_joint'))
            need_delete.append(baking_bones)
            cmds.parent(baking_bones, track_controller[i])
            cmds.setAttr(baking_bones + '.jointOrientX', 0)
            cmds.setAttr(baking_bones + '.jointOrientY', 0)
            cmds.setAttr(baking_bones + '.jointOrientZ', 0)
            cmds.delete(cmds.parentConstraint(track_controller[i], baking_bones, w=1))
            # 创建
            prePosA = cmds.spaceLocator(p=(0, 0, 0), n=(track_controller[i] + '_car_bl_prePosLocA'))
            nowPos = cmds.spaceLocator(p=(0, 0, 0), n=(track_controller[i] + '_car_bl_nowPosLoc'))
            prePos = cmds.spaceLocator(p=(0, 0, 0), n=(track_controller[i] + '_car_bl_prePosLoc'))
            move_grp = cmds.group(n=(track_controller[i] + '_track'))
            cmds.setAttr(track_controller[i] + '_car_bl_prePosLoc.visibility', 0)
            cmds.select(nowPos, prePosA)
            Group1 = cmds.group(n=(track_controller[i] + '_car_bl_locGrp'))
            cmds.setAttr(track_controller[i] + '_car_bl_locGrp.visibility', 0)

            cmds.addAttr((track_controller[i]), ln='prePosX', dv=0, at='double')
            # cmds.setAttr((track_controller[i]+'.prePosX'), e=1, keyable=True)
            need_delete.append(track_controller[i]+'.prePosX')
            cmds.addAttr((track_controller[i]), ln='prePosY', dv=0, at='double')
            # cmds.setAttr((track_controller[i]+'.prePosY'), e=1, keyable=True)
            need_delete.append(track_controller[i] + '.prePosY')
            cmds.addAttr((track_controller[i]), ln='prePosZ', dv=0, at='double')
            # cmds.setAttr((track_controller[i]+'.prePosZ'), e=1, keyable=True)
            need_delete.append(track_controller[i] + '.prePosZ')

            cmds.addAttr((track_controller[i]), ln='direction_num', dv=0, at='double')
            # cmds.setAttr((track_controller[i]+'.direction_num'), e=1, keyable=True)
            need_delete.append(track_controller[i]+'.direction_num')

            cmds.select(Group1, move_grp)
            top_grp = cmds.group(n=(track_controller[i] + 'track_Grp'))
            cmds.parent(top_grp, grp)

            cmds.pointConstraint(prePosA, prePos, weight=1)
            cmds.pointConstraint(move_grp, nowPos, weight=1)
            cmds.delete(cmds.pointConstraint(track_controller[i], top_grp, weight=1))
            curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
            # need_delete.append(curveInfo)
            cmds.connectAttr((track_perimeter[i] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), f=1)

            # 给样条添加属性
            cmds.addAttr(track_controller[i], ln='running_direction', en='x:y:z:', at='enum')
            cmds.setAttr((track_controller[i] + '.running_direction'), e=1, channelBox=True)
            cmds.setAttr((track_controller[i] + '.running_direction'), 2)
            need_delete.append((track_controller[i] + '.running_direction'))
            cmds.addAttr(track_controller[i], ln='axial', en='x:y:z:', at='enum')
            cmds.setAttr((track_controller[i] + '.axial'), e=1, channelBox=True)
            need_delete.append((track_controller[i] + '.axial'))
            cmds.addAttr(track_controller[i], ln='start_num', dv=0, at='double')
            cmds.setAttr((track_controller[i] + '.start_num'), e=1, keyable=True)
            need_delete.append((track_controller[i] + '.start_num'))
            cmds.addAttr(track_controller[i], ln='baking_num', dv=0, at='double')
            cmds.setAttr((track_controller[i] + '.baking_num'), e=1, keyable=True)
            need_delete.append((track_controller[i] + '.baking_num'))
            cmds.addAttr(track_controller[i], ln='magnification', dv=1, at='double')
            cmds.setAttr((track_controller[i] + '.magnification'), e=1, keyable=True)
            need_delete.append((track_controller[i] + '.magnification'))
            # 给骨骼添加属性
            cmds.addAttr(baking_bones, ln='track', at='bool')
            # need_delete.append((baking_bones + '.track'))
            # cmds.setAttr((baking_bones + '.track'), e=1, channelBox=True)
            cmds.addAttr(baking_bones, ln='calculate_track_num', dv=0, at='double')
            cmds.setAttr((baking_bones + '.calculate_track_num'), e=1, keyable=True)
            # need_delete.append((baking_bones + '.calculate_track_num'))
            # 添加骨骼属性代理(代码里给此属性k帧)
            cmds.addAttr(baking_bones, proxy=(track_controller[i] + '.baking_num'), longName='baking_track')
            # need_delete.append((baking_bones + '.baking_track'))
            # 添加总控制器属性代理
            cmds.addAttr(track_parent_controller, proxy=(track_controller[i] + '.baking_num'), longName=baking_bones)
            need_delete.append((track_parent_controller[0] + '.' + baking_bones))
            # 建立节点关系
            cmds.connectAttr((track_parent_controller[0] + '.track'), (baking_bones + '.track'), f=1)
            # choice_node = cmds.shadingNode('choice', asUtility=1)
            # need_delete.append(choice_node)
            # cmds.connectAttr((track_parent_controller[0] + '.expression_type'), (choice_node + '.selector'), f=1)
            # cmds.connectAttr((baking_bones + '.calculate_track_num'), (choice_node + '.input[0]'), f=1)
            # cmds.connectAttr((track_controller[i] + '.baking_num'), (choice_node + '.input[1]'), f=1)
            # for j, axial in zip(range(0, 3), ['X', 'Y', 'Z']):
            #     plusMinusAverage_condition = cmds.shadingNode('condition', asUtility=1)
            #     need_delete.append(plusMinusAverage_condition)
            #     cmds.connectAttr((track_controller[i] + '.axial'), (plusMinusAverage_condition + '.firstTerm'), f=1)
            #     cmds.setAttr((plusMinusAverage_condition + '.secondTerm'), j)
            #     cmds.setAttr((plusMinusAverage_condition + '.colorIfFalseR'), 0)
            #     cmds.connectAttr((choice_node + '.output'), (plusMinusAverage_condition + '.colorIfTrueR'), f=1)
            #     cmds.connectAttr((plusMinusAverage_condition + '.outColorR'), (baking_bones + '.rotate' + axial), f=1)
            choice_node = cmds.shadingNode('choice', asUtility=1)
            need_delete.append(choice_node)
            cmds.connectAttr((track_controller[i] + '.running_direction'), (choice_node + '.selector'), f=1)
            cmds.connectAttr((track_controller[i] + '_car_bl_prePosLoc.translateX'), (choice_node + '.input[0]'), f=1)
            cmds.connectAttr((track_controller[i] + '_car_bl_prePosLoc.translateY'), (choice_node + '.input[1]'), f=1)
            cmds.connectAttr((track_controller[i] + '_car_bl_prePosLoc.translateZ'), (choice_node + '.input[2]'), f=1)
            cmds.connectAttr((choice_node + '.output'), (track_controller[i] + '.direction_num'))

            expression_node = cmds.expression(s=('if(' + track_parent_controller[0] + '.baking_tracks==' + track_parent_controller[0] + '.expression_type){\n'
                                '   int $start=1;\n'
                                '   int $start_frame=' + track_parent_controller[0] + '.start_frame;\n'
                                '   if(frame <= $start_frame)$start=0;\n'
                                '   float $start_num = ' + track_controller[i] + '.start_num;\n'
                                '   if(frame > $start_frame)$start_num=0;\n'
                                '   float $autoRoll=' + track_controller[i] + '.magnification;\n'
                                '   float $prePosX=' +track_controller[i] + '.prePosX;\n'
                                '   float $prePosY=' + track_controller[i] + '.prePosY;\n'
                                '   float $prePosZ=' +track_controller[i] + '.prePosZ;\n'
                                '   float $nowPosX=' + track_controller[i] + '_car_bl_nowPosLoc.translateX;\n'
                                '   float $nowPosY=' + track_controller[i] + '_car_bl_nowPosLoc.translateY;\n'
                                '   float $nowPosZ=' +track_controller[i] + '_car_bl_nowPosLoc.translateZ;\n'
                                '   float $dis=`mag(<<$nowPosX,$nowPosY,$nowPosZ>>-<<$prePosX,$prePosY,$prePosZ>>)`;\n'
                                '   ' + track_controller[i] + '_car_bl_prePosLocA.translateX=$prePosX;\n'
                                '   ' + track_controller[i] + '_car_bl_prePosLocA.translateY=$prePosY;\n'
                                '   ' + track_controller[i] + '_car_bl_prePosLocA.translateZ=$prePosZ;\n'
                                '   ' + track_controller[i] + '.prePosX=$nowPosX;\n'
                                '   ' + track_controller[i] + '.prePosY=$nowPosY;\n'
                                '   ' +track_controller[i] + '.prePosZ=$nowPosZ;\n'
                                '   float $dirPreZ=' + track_controller[i] + '.direction_num;\n'
                                '   int $dir=1;\n'
                                '   if($dirPreZ<0)$dir=-1;\n'
                                '   float $perimeter=' + curveInfo + '.arcLength;\n'
                                '   float $curRoll=' + baking_bones + '.calculate_track_num;\n'
                                '   ' + baking_bones + '.calculate_track_num=$start_num+$start*($curRoll+$dis/$perimeter*$autoRoll*$dir);\n'
                                '}'),
                                ae=1, uc='all', o='', n=(track_perimeter[i] + '_trackExpression'))
            need_delete.append(expression_node)
            cmds.delete(cmds.pointConstraint(track_controller[i], move_grp, w=1))
            cmds.parentConstraint(track_controller[i], move_grp, w=1, mo=1)

            # rotateX = cmds.listConnections((track_joint[i] + '.rotateX'), p=1)
            # if rotateX:
            #     cmds.disconnectAttr(rotateX[0], (track_joint[i] + '.rotateX'))
            # rotateY = cmds.listConnections((track_joint[i] + '.rotateY'), p=1)
            # if rotateY:
            #     cmds.disconnectAttr(rotateY[0], (track_joint[i] + '.rotateY'))
            # rotateZ = cmds.listConnections((track_joint[i] + '.rotateZ'), p=1)
            # if rotateZ:
            #     cmds.disconnectAttr(rotateZ[0], (track_joint[i] + '.rotateZ'))

            # cmds.orientConstraint(baking_bones, track_joint[i], mo=1, weight=1)

            # cmds.parent(track_perimeter[i], grp)
            # cmds.setAttr((track_perimeter[i] + '.visibility'), 0)
            # cmds.parentConstraint(track_controller[i], track_perimeter[i], w=1)
            # cmds.scaleConstraint(track_controller[i], track_perimeter[i], w=1)

            # 创建定位器拖动骨骼链
            motion_loc = cmds.spaceLocator(n=track_controller[i] + '_motion_loc')[0]
            cmds.setAttr(motion_loc + '.visibility', 0)
            cmds.parent(motion_loc, grp)
            motionPath = self.others_library.path_constraint(track_perimeter[i], motion_loc)

            choice = cmds.createNode('choice')
            cmds.connectAttr(track_parent_controller[0] + '.expression_type', choice + '.selector', f=1)

            cmds.setDrivenKeyframe(choice + '.input[0]',
                                   currentDriver=baking_bones + '.calculate_track_num', dv=0, v=0)
            cmds.setDrivenKeyframe(choice + '.input[0]',
                                   currentDriver=baking_bones + '.calculate_track_num', dv=1, v=1)
            motionPath_drver_node = cmds.listConnections(choice + '.input[0]')
            cmds.keyTangent(motionPath_drver_node, itt='linear', ott='linear')
            cmds.select(motionPath_drver_node)
            cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
            mel.eval('doSetInfinity \"-pri cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
            cmds.select(motionPath_drver_node)
            cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
            mel.eval('doSetInfinity \"-poi cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
            # cmds.connectAttr(baking_bones + '.calculate_track_num', choice + '.input[0]', force=1)

            cmds.setDrivenKeyframe(choice + '.input[1]',
                                   currentDriver=(baking_bones + '.baking_track'), dv=0, v=0)
            cmds.setDrivenKeyframe(choice + '.input[1]',
                                   currentDriver=(baking_bones + '.baking_track'), dv=1, v=1)
            motionPath_drver_node = cmds.listConnections(choice + '.input[1]')
            cmds.keyTangent(motionPath_drver_node, itt='linear', ott='linear')
            cmds.select(motionPath_drver_node)
            cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
            mel.eval('doSetInfinity \"-pri cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
            cmds.select(motionPath_drver_node)
            cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
            mel.eval('doSetInfinity \"-poi cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
            # cmds.connectAttr(baking_bones + '.baking_track', choice + '.input[1]', f=1)

            cmds.setDrivenKeyframe((motionPath + '.uValue'),
                                   currentDriver=(choice + '.output'), dv=0, v=0)
            cmds.setDrivenKeyframe((motionPath + '.uValue'),
                                   currentDriver=(choice + '.output'), dv=1, v=1)
            motionPath_drver_node = cmds.listConnections((motionPath + '.uValue'))
            cmds.keyTangent(motionPath_drver_node, itt='linear', ott='linear')
            cmds.select(motionPath_drver_node)
            cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
            mel.eval('doSetInfinity \"-pri cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')
            cmds.select(motionPath_drver_node)
            cmds.selectKey(motionPath_drver_node, add=1, k=1, f=(0.0, 1.0))
            mel.eval('doSetInfinity \"-poi cycle\" graphEditor1GraphEd \"bufferCurve useSmoothness\";')

            cmds.select(track_joint[i], joint[i][-1], track_perimeter[i])
            cmds.ikHandle(ccv=False, sol='ikSplineSolver', roc=False, pcv=False)
            IK = cmds.ls(sl=1)
            cmds.setAttr(IK[0] + '.visibility', 0)

            cmds.pointConstraint(motion_loc, track_joint[i], w=1)
            track_joint_grp = cmds.group(track_joint[i], n=track_controller[i] + '_track_joint_grp')
            cmds.setAttr(track_joint_grp + '.visibility', 0)

            cmds.parent(IK, track_joint_grp, top_grp)
            cmds.parentConstraint(track_controller[i], track_joint_grp, w=1, mo=1)

            cmds.setAttr((track_controller[i] + '.magnification'), cb=True, k=False)



            # 添加拉伸
            cmds.select(track_perimeter[i])
            cmds.duplicate(rr=1)
            base_long_curve = cmds.ls(sl=1)

            base_long_curve_grp = cmds.group(base_long_curve, n=base_long_curve[0] + '_grp')
            cmds.setAttr(base_long_curve_grp + '.visibility', 0)

            curveInfo_bsee_long = cmds.shadingNode('curveInfo', asUtility=1)
            # need_delete.append(curveInfo_bsee_long)
            cmds.connectAttr((base_long_curve[0] + '.worldSpace[0]'), (curveInfo_bsee_long + '.inputCurve'), f=1)
            # 计算拉伸
            scale_multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
            cmds.connectAttr((curveInfo + '.arcLength'), (scale_multiplyDivide + '.input1.input1X'), f=1)
            cmds.connectAttr((curveInfo_bsee_long + '.arcLength'), (scale_multiplyDivide + '.input2.input2X'), f=1)
            cmds.setAttr((scale_multiplyDivide + '.operation'), 2)
            for j in joint[i]:
                cmds.connectAttr((scale_multiplyDivide + '.outputX'), (j + '.scaleX'), f=1)
            cmds.parent(base_long_curve_grp, top_grp)
            cmds.parentConstraint(track_parent_controller[0], base_long_curve_grp, mo=1)
            cmds.scaleConstraint(track_controller[0], base_long_curve_grp, mo=1)


            # 添加毛囊存放组和蒙皮骨骼存放组
            all_skin_joint_grp = cmds.group(em=1, n=(track_controller[i] + '_grp'))
            # cmds.setAttr((all_skin_joint_grp + '.visibility'), 0)
            all_joint_follicle_grp = cmds.group(em=1, n=(track_curved[i] + '_grp'))
            cmds.parent(all_skin_joint_grp, all_joint_follicle_grp,top_grp)
            cmds.setAttr((all_joint_follicle_grp + '.visibility'), 0)
            # 添加输出骨骼
            for j in joint[i]:
                shape = cmds.listRelatives(track_curved[i],s=1)
                cmds.select(cl=1)
                # 创建骨骼
                # 创建骨骼带动毛囊附着曲面
                cpom = cmds.createNode('closestPointOnSurface', n=(j + 'closestPointOnSurface'))
                cmds.connectAttr((track_curved[i] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
                decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
                cmds.connectAttr((j + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
                cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
                follicleShape = cmds.createNode('follicle', n=(j + '_follicleShape'))
                follicle = cmds.listRelatives(follicleShape, p=1)
                cmds.connectAttr((shape[0] + '.worldSpace[0]'), (j + '_follicleShape' + '.inputSurface'), f=1)
                cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (j + '_follicleShape' + '.inputWorldMatrix'), f=1)
                cmds.connectAttr((j + '_follicleShape' + ".outTranslate"),
                                 (j + '_follicle' + '.translate'), f=1)
                cmds.connectAttr((j + '_follicleShape' + ".outRotate"),
                                 (j + '_follicle' + ".rotate"), f=1)
                cmds.connectAttr((cpom + '.parameterU'), (j + '_follicle' + '.parameterU'), f=1)
                cmds.connectAttr((cpom + '.parameterV'), (j + '_follicle' + '.parameterV'), f=1)
                # cmds.setAttr((j + '_follicle' + '.parameterV'), 0)
                cmds.select(cl=1)
                skin_joint = cmds.joint(p=(0, 0, 0), n=(j + '_SkinJoint'))
                cmds.parent(skin_joint,all_skin_joint_grp)
                cmds.pointConstraint(follicle[0], skin_joint)
                cmds.delete(cmds.orientConstraint(j, skin_joint))
                cmds.orientConstraint(follicle[0], skin_joint)
                cmds.connectAttr((scale_multiplyDivide + '.outputX'), (skin_joint + '.scaleX'), f=1)
                cmds.parent(follicle[0], all_joint_follicle_grp)

            # 创建定位器碰撞
            collision_loc_grp = cmds.group(n=track_controller[i]+'_Collision_loc_grp', em=1)
            cmds.setAttr(collision_loc_grp+'.visibility',0)
            cmds.parent(collision_loc_grp,collision_grp)

            curve_point = cmds.ls(track_perimeter[i] + '.cv[*]', fl=1)
            for sel in [track_curved[i]]:
                point_loc = []
                cmds.setAttr(sel+'.visibility',0)
                point = cmds.ls(sel+'.cv[*]',fl=1)
                point_loc = point_loc+point
                # print(point_loc)
                for p in range(0,len(point_loc)):
                    cluster = cmds.cluster(point_loc[p])
                    loc = cmds.spaceLocator(n=sel+'_'+str(p)+'_loc')
                    # print(loc)
                    node = mel.eval('cMuscle_rigKeepOutSel();')
                    cmds.setAttr(node[0] + '.inDirectionX', 0)
                    cmds.setAttr(node[0] + '.inDirectionY', 1)

                    cmds.select(cl=1)
                    out_joint = cmds.joint(n=sel+'_'+str(p)+'_out_joint')
                    cmds.addAttr(out_joint, ln='baking_track_joint', at='bool')
                    cmds.setAttr((out_joint + '.baking_track_joint'), e=1, keyable=1)
                    # cmds.addAttr(node[-1], ln='baking_track_joint_target', at='bool')
                    # cmds.setAttr((node[-1] + '.baking_track_joint_target'), e=1, keyable=1)
                    # cmds.addAttr(track_parent_controller, ln='Constrain_Fat', dv=0, at='long')
                    # cmds.setAttr((node[-1] + '.baking_track_joint_target'), e=1, keyable=1)
                    # 添加总控制器属性代理
                    cmds.addAttr(track_parent_controller, proxy=(out_joint + '.translateY'), longName=out_joint)
                    cmds.connectAttr((track_parent_controller[0] + '.track_joint'),(out_joint + '.baking_track_joint'))
                    need_delete.append(track_parent_controller[0] + '.'+ out_joint)
                    cmds.parent(out_joint, node[0])
                    cmds.parent(node[-1],out_joint)
                    # print(node)
                    cmds.delete(cmds.parentConstraint(cluster[1], loc, weight=1))
                    cmds.parent(loc[0], collision_loc_grp)
                    cmds.select(loc, collision_plane)
                    mel.eval('cMuscle_keepOutAddRemMuscle(1);')
                    cmds.parent(cluster[1], node[-1])
                    # parentConstraint = cmds.parentConstraint(out_joint, cluster[1], weight=1)
                    # cmds.connectAttr((track_parent_controller[0] + '.expression_type'), (parentConstraint[0]+'.'+out_joint+'W0'))
                    # 计算距离
                    obj_position = cmds.xform(point_loc[p], query=True, translation=True, worldSpace=True)
                    for cp in curve_point:
                        target_position = cmds.xform(cp, query=True, translation=True, worldSpace=True)
                        # print(obj_position)
                        distance = math.sqrt((obj_position[0] - target_position[0]) ** 2 +
                                             (obj_position[1] - target_position[1]) ** 2 +
                                             (obj_position[2] - target_position[2]) ** 2)
                        if distance<0.0001 :
                            curve_cluster = cmds.cluster(cp)
                            cmds.parent(curve_cluster[1], node[-1])
                            break

            cmds.parentConstraint(track_controller[i], collision_loc_grp, weight=1, mo=1)
            cmds.scaleConstraint(track_controller[i], collision_loc_grp, weight=1, mo=1)

        cmds.connectAttr((track_parent_controller[0] + '.collision_plane'), (collision_plane[0] + '.visibility'))
        cmds.connectAttr((top_condition + '.outColorR'), (collision_node[0] + '.nodeState'))
        cmds.connectAttr((track_parent_controller[0] + '.Constrain_Fat'), (collision_node[0] + '.fat'))



        # 添加烘焙表达式
        baking_expression = cmds.expression(
            s =  'if(' + track_parent_controller[0] + '.baking_tracks==1 && ' + track_parent_controller[0] + '.expression_type==1){\n'
                 '    int $start=1;\n'
                 '    string $car[]=`ls "*.baking_tracks"`;\n'
                 '    int $end_frame = `playbackOptions -q -max`;\n'
                 '    int $now_frame = `currentTime -q`;\n'
                 '    for($i=0;$i<size($car);$i++){\n'
                 '        int $open=`getAttr $car[$i]`;\n'
                 '        if($open==1){\n'
                 '            string $soure[];\n'
                 '            int $numTok=`tokenize $car[$i] "." $soure`;\n'
                 '            float $start_frame=`getAttr ($soure[0]+".start_frame")`;\n'
                 '            if(frame>=$start_frame){\n'
                 '                string $track[]=`ls ($soure[0]+".track")`;\n'
                 '                string $tracks[]=`listConnections -d 1 $track[0]`;\n'
                 '                for($j=0;$j<size($tracks);$j++){\n'
                 '                    float $track_num=`getAttr ($tracks[$j]+".calculate_track_num")`;\n'
                 '                    setKeyframe ($tracks[$j]+".baking_track");\n'
                 '                    setAttr ($tracks[$j]+".baking_track") $track_num;\n'
                 '                    setKeyframe ($tracks[$j]+".baking_track");\n'
                 '                }\n'
                 '                string $track_joints[]=`listConnections -d 1 ($soure[0]+".track_joint")`;\n'
                 '                for($k=0;$k<size($track_joints);$k++){\n'
                 '                    string $child[]=`listRelatives -c $track_joints[$k]`;\n'
                 '                    float $num = `getAttr ($child[0]+".translateY")`;\n'
                 '                    setKeyframe ($track_joints[$k]+".translateY");\n'
                 '                    setAttr ($track_joints[$k]+".translateY") $num;\n'
                 '                    setKeyframe ($track_joints[$k]+".translateY");\n'
                 '                }\n'
                 '            }\n'
                 '        }\n'
                 '    }\n'
                 '    if($end_frame==$now_frame){\n'
                 '        for($i=0;$i<size($car);$i++){\n'
                 '            setAttr $car[$i] 0;\n'
                 '        }\n'                                                                                                                                                                                                                                                                                                                                           
                                                                                                             
                 '    }\n'
                 '}\n',
            ae=1, uc='all', o='', n=('BakingtrackExpression'))
        need_delete.append(baking_expression)
        cmds.setAttr(track_parent_controller[0] + '.node', str(need_delete), type='string')
    # 删除履带
    def delete_track(self):
        print('删除履带')
        # 加载总控制器
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        # cmds.select('joint2_C,joint105_C')
        track_parent_controller = cmds.ls(sl=1)
        self.delete_node_attribute(track_parent_controller[0])

    # 创建履带
    def create_adv_track(self):
        print('创建adv履带')

        pass

    # 删除履带
    def delete_adv_track(self):
        print('删除adv履带')
        # 加载总控制器
        sel = cmds.ls(sl=1)
        self.delete_node_attribute(sel[0])


    # 删除node属性中的所有对象
    def delete_node_attribute(self,obj):
        node = cmds.getAttr(obj + '.node')
        node = ast.literal_eval(node)
        for n in node:
            attribute = n.split('.')
            # print(attribute)
            if len(attribute) == 1:
                cmds.delete(n)
            else:
                cmds.deleteAttr(n)
            # print(n)



window = Window()
if __name__ == '__main__':
    window.show()


#删除无影响驱动
