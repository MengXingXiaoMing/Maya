# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
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
#加载文本
import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import controller
importlib.reload(controller)
from controller import *

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        # 但实际上，你应该直接使用原始的Unicode字符串
        self.setWindowTitle((u'裙子驱动(Maya' + self.maya_version + u')'))

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = self.root_path + '\\' + self.maya_version

        self.curve = CreateAndEditCurve()
        self.controller = CurveControllerEdit()

        self.create_widgets()
        self.create_layouts()
        self.create_connect()


    def create_widgets(self):
        # 第一行
        # file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(QPixmap(self.file_path+'/image.png'))

        self.button_1 = QtWidgets.QPushButton('选择总控制器')
        self.line_edit_1 = QtWidgets.QLineEdit('Main')
        self.button_2 = QtWidgets.QPushButton('加载总控制器')

        self.button_3 = QtWidgets.QPushButton('选择Root骨骼')
        self.line_edit_2 = QtWidgets.QLineEdit('Root_M')
        self.button_4 = QtWidgets.QPushButton('加载Root骨骼')

        self.button_5 = QtWidgets.QPushButton('选择裙子控制器')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_6 = QtWidgets.QPushButton('加载裙子控制器')

        self.button_7 = QtWidgets.QPushButton('选择裙子末端骨骼')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_8 = QtWidgets.QPushButton('加载裙子末端骨骼')

        self.button_13 = QtWidgets.QPushButton('选择驱动源骨骼')
        self.line_edit_5 = QtWidgets.QLineEdit('Hip_R,Hip_L')
        self.button_14 = QtWidgets.QPushButton('加载驱动源骨骼')

        self.button_9 = QtWidgets.QPushButton('生成预置驱动')
        self.text_1 = QtWidgets.QLabel('修改完驱动后再生成驱动开关')
        self.button_10 = QtWidgets.QPushButton('生成驱动开关')
        self.text_2 = QtWidgets.QLabel('下面是删除部分')
        self.button_11 = QtWidgets.QPushButton('按加载删除驱动开关')
        self.button_12 = QtWidgets.QPushButton('按当前加载删除预置驱动')
    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        main_layout.addWidget(self.label)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_2)
        h_Box_layout_2.addWidget(self.button_1)
        h_Box_layout_2.addWidget(self.line_edit_1)
        h_Box_layout_2.addWidget(self.button_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.button_3)
        h_Box_layout_3.addWidget(self.line_edit_2)
        h_Box_layout_3.addWidget(self.button_4)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.button_5)
        h_Box_layout_4.addWidget(self.line_edit_3)
        h_Box_layout_4.addWidget(self.button_6)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.button_7)
        h_Box_layout_5.addWidget(self.line_edit_4)
        h_Box_layout_5.addWidget(self.button_8)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_6)
        h_Box_layout_6.addWidget(self.button_13)
        h_Box_layout_6.addWidget(self.line_edit_5)
        h_Box_layout_6.addWidget(self.button_14)

        main_layout.addWidget(self.button_9)
        main_layout.addWidget(self.text_1)
        main_layout.addWidget(self.button_10)
        main_layout.addWidget(self.text_2)
        main_layout.addWidget(self.button_11)
        main_layout.addWidget(self.button_12)
        # 置顶
        main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(lambda :self.select_text(self.line_edit_1))
        self.button_2.clicked.connect(lambda :self.load_text(self.line_edit_1))

        self.button_3.clicked.connect(lambda: self.select_text(self.line_edit_2))
        self.button_4.clicked.connect(lambda: self.load_text(self.line_edit_2))

        self.button_5.clicked.connect(lambda: self.select_text(self.line_edit_3))
        self.button_6.clicked.connect(lambda: self.load_text(self.line_edit_3))

        self.button_7.clicked.connect(lambda: self.select_text(self.line_edit_4))
        self.button_8.clicked.connect(lambda: self.load_text(self.line_edit_4))

        self.button_13.clicked.connect(lambda: self.select_text(self.line_edit_5))
        self.button_14.clicked.connect(lambda: self.load_text(self.line_edit_5))

        self.button_9.clicked.connect(self.create_drve)  # 生成预置驱动
        self.button_10.clicked.connect(self.create_drve_switch)  # 生成预置驱动
        self.button_11.clicked.connect(self.delete_drve_switch)  # 生成预置驱动
        self.button_12.clicked.connect(self.delete_drve)  # 生成预置驱动
    def load_text(self,name):
        sel = cmds.ls(sl=1, fl=1)
        # 建立具体的文本
        all_sel = str(sel[0])
        if len(sel) > 1:
            for i in range(1, len(sel)):
                all_sel = all_sel + ',' + sel[i]
        name.setText(all_sel)
    def select_text(self,name):
        text = name.text()
        all_text = text.split(',')
        cmds.select(all_text)

    # 生成预置驱动
    def create_drve(self):
        cmds.undoInfo(ock=1)
        self.select_text(self.line_edit_1)
        main = cmds.ls(sl=1, fl=1)
        self.select_text(self.line_edit_2)
        root = cmds.ls(sl=1, fl=1)
        self.select_text(self.line_edit_3)
        skirt = cmds.ls(sl=1, fl=1)
        self.select_text(self.line_edit_4)
        end_joint = cmds.ls(sl=1, fl=1)
        self.select_text(self.line_edit_5)
        hip_joint = cmds.ls(sl=1, fl=1)
        # print (main,root,skirt,end_joint)
        # 创建跟随组
        all_aim_constraint_group = []
        for cur in skirt:
            cmds.select(cur)
            parent_c = cmds.listRelatives(cur, p=1)
            parent_p = cmds.listRelatives(parent_c, p=1)
            aim_constraint_group = cmds.group(n='aim_constraint_'+cur, em=1)
            all_aim_constraint_group.append(aim_constraint_group)
            cmds.delete(cmds.parentConstraint(cur, aim_constraint_group, w=1))
            cmds.parent(aim_constraint_group, parent_p)
            cmds.parent(parent_c, aim_constraint_group)

        # 创建总跟随控制器组
        ls_loc = cmds.spaceLocator(n='ls_loc')[0]
        for joint in end_joint:
            cmds.pointConstraint(joint, ls_loc, w=1)
        top_cur = cmds.curve(n='top_aim_constraint_soure_curve',
                   p=[(2.29906764589e-16, 3.75466240143, -3.75466240143),
                    (1.99089155166e-32, 5.30989449024, -3.25137264563e-16),
                    (-2.29906764589e-16, 3.75466240143, 3.75466240143),
                    (-3.25137264563e-16, 2.75265868031e-16, 5.30989449024),
                    (-2.29906764589e-16, -3.75466240143, 3.75466240143),
                    (-3.25692221629e-32, -5.30989449024, 5.31895762691e-16),
                    (2.29906764589e-16, -3.75466240143, -3.75466240143),
                    (3.25137264563e-16, -7.24108436827e-16, -5.30989449024),
                    (2.29906764589e-16, 3.75466240143, -3.75466240143),
                    (1.99089155166e-32, 5.30989449024, -3.25137264563e-16),
                    (-2.29906764589e-16, 3.75466240143, 3.75466240143)],
                 k=[-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], d=3, per=True)
        self.curve.change_curve_color('Index', [top_cur], [1, 1, 1], 13)
        self.controller.modify_vontroller_shape('scale', 0.5, 0.5, 0.5)
        self.controller.rotation_controller('X')
        top_cur_grp_2 = cmds.group(n='top_aim_constraint_soure_curve_grp2')
        top_cur_grp_1 = cmds.group(n='top_aim_constraint_soure_curve_grp1')
        cmds.delete(cmds.parentConstraint(ls_loc, top_cur_grp_1, w=1))
        cmds.delete(ls_loc)

        # 添加切换属性
        cmds.addAttr(top_cur, ln='follow', at='enum', en='body:word', k=True)
        cmds.setAttr((top_cur + '.follow'), e=1, keyable=True)
        parentConstraint = cmds.parentConstraint(root,top_cur_grp_1, w=1, mo=1)
        cmds.parentConstraint(main, top_cur_grp_1, w=1, mo=1)
        cmds.setDrivenKeyframe((parentConstraint[0] + '.'+root[0]+'W0'),
                               currentDriver=(top_cur + '.follow'), dv=0, v=1)
        cmds.setDrivenKeyframe((parentConstraint[0] + '.' + root[0] + 'W0'),
                               currentDriver=(top_cur + '.follow'), dv=1, v=0)
        cmds.setDrivenKeyframe((parentConstraint[0] + '.' + main[0] + 'W1'),
                               currentDriver=(top_cur + '.follow'), dv=0, v=1)
        cmds.setDrivenKeyframe((parentConstraint[0] + '.' + main[0] + 'W1'),
                               currentDriver=(top_cur + '.follow'), dv=1, v=0)
        cmds.scaleConstraint(main, top_cur_grp_1, w=1, mo=1)

        all_aim_constraint_soure = []
        for i in range(len(end_joint)):
            cur = cmds.curve(n='aim_constraint_soure_' + end_joint[i] + '_curve',
                             p=[(3.94758581432, -3.94758581432, -3.94758581432),
                                (3.94758581432, 3.94758581432, -3.94758581432),
                                (3.94758581432, 3.94758581432, 3.94758581432),
                                (3.94758581432, -3.94758581432, 3.94758581432),
                                (3.94758581432, -3.94758581432, -3.94758581432),
                                (-3.94758581432, -3.94758581432, -3.94758581432),
                                (-3.94758581432, 3.94758581432, -3.94758581432),
                                (-3.94758581432, 3.94758581432, 3.94758581432),
                                (-3.94758581432, -3.94758581432, 3.94758581432),
                                (-3.94758581432, -3.94758581432, -3.94758581432),
                                (3.94758581432, -3.94758581432, -3.94758581432),
                                (3.94758581432, 3.94758581432, -3.94758581432),
                                (-3.94758581432, 3.94758581432, -3.94758581432),
                                (-3.94758581432, 3.94758581432, 3.94758581432),
                                (3.94758581432, 3.94758581432, 3.94758581432),
                                (3.94758581432, -3.94758581432, 3.94758581432),
                                (-3.94758581432, -3.94758581432, 3.94758581432)],
                             k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
                                16.0], d=1)
            self.curve.change_curve_color('Index', [cur], [1, 1, 1], 13)
            self.controller.modify_vontroller_shape('scale', 0.05, 0.05, 0.05)
            cur_grp_2 = cmds.group(n='aim_constraint_soure_'+ end_joint[i] +'_curve_grp2', em=1)
            cur_grp_1 = cmds.group(n='aim_constraint_soure_' + end_joint[i] + '_curve_grp1', em=1)
            cmds.parent(cur_grp_1, top_cur)
            cmds.parent(cur_grp_2, cur_grp_1)
            cmds.parent(cur, cur_grp_2)
            cmds.delete(cmds.parentConstraint(end_joint[i], cur_grp_1,w=1))
            cmds.aimConstraint(cur, all_aim_constraint_group[i], weight=1, upVector=(0, 1, 0), mo=1, worldUpObject=cur,
                             worldUpType="objectrotation", aimVector=(1, 0, 0), worldUpVector=(0, 1, 0))
            all_aim_constraint_soure.append(cur)

        # 创建默认驱动组
        all_drver_group = []
        have_drver_group = []
        for cur in skirt:
            for i in range(0,3):
                cmds.select(cur)
                parent_c = cmds.listRelatives(cur, p=1)
                parent_p = cmds.listRelatives(parent_c, p=1)
                aim_constraint_group = cmds.group(n='skirt_drver'+str(i)+'_' + cur, em=1)
                all_drver_group.append(aim_constraint_group)
                if i == 1:
                    have_drver_group.append(aim_constraint_group)
                if i < 2:
                    cmds.delete(cmds.pointConstraint(cur, aim_constraint_group, w=1))
                else:
                    cmds.delete(cmds.parentConstraint(cur, aim_constraint_group, w=1))
                cmds.parent(aim_constraint_group, parent_p)
                cmds.parent(parent_c, aim_constraint_group)
        for k in range(len(hip_joint)):
            if k == 0:
                for i in range(len(have_drver_group)):
                    if i == 0:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=60, v=-30)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=-10)

                    if i == 1:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=60, v=-60)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=-30)

                    if i == 2:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=-60)

                    if i == 3:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-60, v=60)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=-30)

                    if i == 4:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-60, v=30)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=-10)
            else:
                for i in range(len(have_drver_group)):
                    if i == 0:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=60, v=-30)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=10)
                    if i == 7:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=60, v=-60)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=30)
                    if i == 6:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=60)

                    if i == 5:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-60, v=60)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=30)

                    if i == 4:
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateX'),
                                               currentDriver=(hip_joint[k] + '.rotateZ'), dv=-60, v=30)

                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-10, v=0)
                        cmds.setDrivenKeyframe((have_drver_group[i] + '.rotateZ'),
                                               currentDriver=(hip_joint[k] + '.rotateY'), dv=-60, v=10)

        # 添加后面要撤回修改的属性
        loc = cmds.spaceLocator(n=main[0]+'_skirt_dete_loc')[0]
        cmds.setAttr(loc+'.v', 0)
        cmds.parent(loc, 'top_aim_constraint_soure_curve_grp1')
        cmds.addAttr(loc, ln='all_aim_constraint_group', dt='string')
        text = ''
        for i in range(len(all_aim_constraint_group)):
            text = text + all_aim_constraint_group[i] + ','
        cmds.setAttr(loc+'.all_aim_constraint_group', text, type='string')

        cmds.addAttr(loc, ln='all_drver_group', dt='string')
        text = ''
        for i in range(len(all_drver_group)):
            text = text + all_drver_group[i] + ','
        cmds.setAttr(loc+'.all_drver_group', text, type='string')
        cmds.warning(u'创建预置驱动完成,请手动修改驱动，或者在三个驱动组中添加自己的驱动组。')
        cmds.undoInfo(cck=1)
    # 生成驱动开关
    def create_drve_switch(self):
        cmds.undoInfo(ock=1)
        self.select_text(self.line_edit_3)
        skirt = cmds.ls(sl=1, fl=1)
        # 查询所有驱动组
        for cur in skirt:
            cmds.addAttr(cur,ln='drver', max=1, dv=1, at='double', min=0)
            cmds.setAttr((cur+'.drver'),e=1, keyable=True)
            have_drver_group = []
            top_grp = 'skirt_drver0_' + cur
            end_grp = 'skirt_drver2_' + cur
            add_grp = [end_grp]
            while add_grp[0] != top_grp :
                have_drver_group.append(add_grp[0])
                add_grp = cmds.listRelatives(add_grp[0], p=1)
            # 查询所有有关联的驱动属性
            for group in have_drver_group:
                for at in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX',
                           'scaleY', 'scaleZ']:
                    attr = cmds.listConnections(group + '.' + at, d=1, p=1, c=1, scn=1)
                    if attr:
                        multiplyDivide = cmds.createNode('multiplyDivide')
                        cmds.connectAttr((cur + '.drver'), (multiplyDivide + '.input1X'), f=1)
                        cmds.connectAttr(attr[1], (multiplyDivide + '.input2X'), f=1)
                        cmds.connectAttr((multiplyDivide + '.outputX'), attr[0], f=1)
        cmds.warning(u'创建驱动开关完成。')
        cmds.undoInfo(cck=1)
    # 按加载删除驱动开关
    def delete_drve_switch(self):
        cmds.undoInfo(ock=1)
        self.select_text(self.line_edit_3)
        skirt = cmds.ls(sl=1, fl=1)
        # 查询所有驱动组
        for cur in skirt:
            cmds.deleteAttr(cur, at='drver')
            have_drver_group = []
            top_grp = 'skirt_drver0_' + cur
            end_grp = 'skirt_drver2_' + cur
            add_grp = [end_grp]
            while add_grp[0] != top_grp:
                have_drver_group.append(add_grp[0])
                add_grp = cmds.listRelatives(add_grp[0], p=1)
            # 查询所有有关联的驱动属性
            for group in have_drver_group:
                for at in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX',
                           'scaleY', 'scaleZ']:
                    attr = cmds.listConnections(group + '.' + at, d=1, p=1, scn=1)
                    if attr:
                        node = attr[0].split('.')[0]
                        attr = cmds.listConnections(node + '.input2X', d=1, p=1, scn=1)
                        node = cmds.listConnections(group + '.' + at, d=1, p=1)
                        cmds.disconnectAttr(node[0], (group + '.' + at))
                        cmds.connectAttr(attr[0], (group + '.' + at), f=1)
        cmds.warning(u'删除驱动开关完成。')
        cmds.undoInfo(cck=1)

    # 按当前加载删除预置驱动
    def delete_drve(self):
        cmds.undoInfo(ock=1)
        self.select_text(self.line_edit_1)
        main = cmds.ls(sl=1, fl=1)

        all_drver_group = cmds.getAttr(main[0]+'_skirt_dete_loc.all_drver_group')  # 获取fk控制器系统
        all_drver_group = all_drver_group.split(',')
        for group in all_drver_group:
            if group:
                parent = cmds.listRelatives(group, p=1)
                child = cmds.listRelatives(group, c=1)
                cmds.parent(child, parent)
                cmds.delete(group)

        all_aim_constraint_group = cmds.getAttr(main[0]+'_skirt_dete_loc.all_aim_constraint_group')  # 获取fk控制器系统
        all_aim_constraint_group = all_aim_constraint_group.split(',')
        for group in all_aim_constraint_group:
            if group:
                parent = cmds.listRelatives(group, p=1)
                child = cmds.listRelatives(group, c=1)
                cmds.parent(child, parent)
                cmds.delete(group)

        # cmds.deleteAttr(main[0]+'_skirt_dete_loc', at='all_drver_group')
        # cmds.deleteAttr(main[0]+'_skirt_dete_loc', at='all_aim_constraint_group')
        cmds.delete('top_aim_constraint_soure_curve_grp1',main[0]+'_skirt_dete_loc')
        cmds.warning(u'删除驱动预置驱动完成。')
        cmds.undoInfo(cck=1)

window = Window()
if __name__ == '__main__':
    window.show()
window.show()
