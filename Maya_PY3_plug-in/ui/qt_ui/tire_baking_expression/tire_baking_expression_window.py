# -*- coding: utf-8 -*-
import inspect
import os
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
import ast
import importlib

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

        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('轮胎烘焙表达式(Maya'+self.maya_version+')')

        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()
        self.others_library = OthersLibrary()

        self.create_widgets()
        self.create_layouts()
        self.create_connect()
    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('选择总控样条自动修改adv轮胎表达式（6.220为基准，别的可能失效，改完需检查旋转方向）')

        self.button_2 = QtWidgets.QPushButton('加载总控制器')
        self.line_edit_1 = QtWidgets.QLineEdit()

        self.button_3 = QtWidgets.QPushButton('加载轮胎控制器')
        self.line_edit_2 = QtWidgets.QLineEdit()

        self.button_4 = QtWidgets.QPushButton('加载周长样条')
        self.line_edit_3 = QtWidgets.QLineEdit()

        self.button_5 = QtWidgets.QPushButton('加载输出骨骼（生成后会替换其旋转关联）')
        self.line_edit_4 = QtWidgets.QLineEdit()

        self.button_6 = QtWidgets.QPushButton('按加载内容创建表达式（轮胎控制器和周长样条和输出骨骼的加载顺序要一致）')

        self.button_7 = QtWidgets.QPushButton('不会用点击此处进入up主页寻找用法')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        self.button_8 = QtWidgets.QPushButton('选择总控制器删除adv轮胎表达式，删完需要adv重建才能回到adv默认状态')
        self.button_9 = QtWidgets.QPushButton('删除自定义轮胎表达式，需加载总控制器和轮胎控制器')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)



        # 第一行
        v_Box_layout_1 = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(v_Box_layout_1)
        v_Box_layout_1.addWidget(self.button_1)

        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_1.addLayout(h_Box_layout_1)
        h_Box_layout_1.addWidget(self.line_edit_1)
        h_Box_layout_1.addWidget(self.button_2)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_1.addLayout(h_Box_layout_2)
        h_Box_layout_2.addWidget(self.line_edit_2)
        h_Box_layout_2.addWidget(self.button_3)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_1.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.line_edit_3)
        h_Box_layout_3.addWidget(self.button_4)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_1.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.line_edit_4)
        h_Box_layout_4.addWidget(self.button_5)

        v_Box_layout_1.addWidget(self.button_6)
        v_Box_layout_1.addWidget(self.button_7)

        v_Box_layout_1.addWidget(self.splitter_1)

        v_Box_layout_1.addWidget(self.button_8)
        v_Box_layout_1.addWidget(self.button_9)
        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(self.modify_the_ADV_wheel_expression)
        self.button_2.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_1,['QLineEdit']))
        self.button_3.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_2,['QLineEdit']))
        self.button_4.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_3,['QLineEdit']))
        self.button_5.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_4,['QLineEdit']))
        self.button_6.clicked.connect(self.create_tire)
        self.button_7.clicked.connect(lambda :self.others_library.open_web(1))
        self.button_8.clicked.connect(self.delete_adv_tire)
        self.button_9.clicked.connect(self.delete_self_tire)

    # 修改adv的轮胎表达式
    def modify_the_ADV_wheel_expression(self):
        cmds.undoInfo(ock=1)
        # 获取要删除的节点
        need_delete = []
        # 获取总控制器
        general_controller = cmds.ls(sl=1)
        # 获取所有表达式
        expression = cmds.ls(type='expression')
        # 获取所有疑似车轮表达式的对象
        wheel = cmds.ls('*WheelExpression*')
        # 筛选出轮胎表达式
        wheel_expression = list(set(expression) & set(wheel))
        # 获取表达式输出骨骼
        joint = cmds.listConnections(wheel_expression, d=1, type='joint')
        # 删除adv轮胎表达式
        cmds.delete(wheel_expression)
        # 获取adv其他部分的属性和对象
        # 给总样条添加属性
        cmds.addAttr(general_controller, ln='tire', at='bool')
        cmds.setAttr((general_controller[0] + '.tire'), e=1, channelBox=True, lock=True)
        cmds.addAttr(general_controller, ln='baking_wheels', at='bool')
        cmds.setAttr((general_controller[0] + '.baking_wheels'), e=1, channelBox=True)
        cmds.addAttr(general_controller, ln='start_frame', dv=101, at='long')
        cmds.setAttr((general_controller[0] + '.start_frame'), e=1, channelBox=True)
        cmds.addAttr(general_controller, ln='expression_type', en="tradition:baking:", at="enum")
        cmds.setAttr((general_controller[0] + '.expression_type'), e=1, channelBox=True)

        for j in joint:
            # 拆解出adv源骨骼的名称
            base_joint_name = j[3:]
            # 给样条添加属性
            cmds.addAttr(('FK' + base_joint_name), ln='axial', en='x:y:z:', at='enum')
            cmds.setAttr(('FK' + base_joint_name + '.axial'), e=1, channelBox=True)
            cmds.addAttr(('FK' + base_joint_name), ln='start_num', dv=0, at='double')
            cmds.setAttr(('FK' + base_joint_name + '.start_num'), e=1, keyable=True)
            cmds.addAttr(('FK' + base_joint_name), ln='baking_num', dv=0, at='double')
            cmds.setAttr(('FK' + base_joint_name + '.baking_num'), e=1, keyable=True)
            # 给骨骼添加属性
            cmds.addAttr(('FKX' + base_joint_name), ln='tire', at='bool')
            cmds.setAttr(('FKX' + base_joint_name + '.tire'), e=1, channelBox=True)
            cmds.addAttr(('FKX' + base_joint_name), ln='calculate_tire_num', dv=0, at='double')
            cmds.setAttr(('FKX' + base_joint_name + '.calculate_tire_num'), e=1, keyable=True)
            # 添加骨骼属性代理(代码里给此属性k帧)
            cmds.addAttr(j, proxy=('FK' + base_joint_name + '.baking_num'), longName='baking_wheel')
            # 添加总控制器属性代理
            cmds.addAttr(general_controller, proxy=('FK' + base_joint_name + '.baking_num'), longName=base_joint_name)

            cmds.addAttr('FK' + base_joint_name + '.autoRoll', e=1, softMaxValue=10000000000000000000000000.0, softMinValue=-10000000000000000000000000.0)
            cmds.setAttr('FK' + base_joint_name + '.autoRoll', cb=False, k=True)
            cmds.setAttr('FK' + base_joint_name + '.autoRoll', cb=True, k=False)
            # 建立节点关系
            cmds.connectAttr((general_controller[0] + '.tire'), ('FKX' + base_joint_name + '.tire'), f=1)
            choice_node = cmds.shadingNode('choice', asUtility=1)
            need_delete.append(choice_node)
            cmds.connectAttr((general_controller[0] + '.expression_type'), (choice_node + '.selector'), f=1)
            cmds.connectAttr(('FKX' + base_joint_name + '.calculate_tire_num'), (choice_node + '.input[0]'), f=1)
            cmds.connectAttr(('FK' + base_joint_name + '.baking_num'), (choice_node + '.input[1]'), f=1)
            for i, axial in zip(range(0, 3), ['X', 'Y', 'Z']):
                plusMinusAverage_condition = cmds.shadingNode('condition', asUtility=1)
                need_delete.append(plusMinusAverage_condition)
                cmds.connectAttr(('FK' + base_joint_name + '.axial'), (plusMinusAverage_condition + '.firstTerm'), f=1)
                cmds.setAttr((plusMinusAverage_condition + '.secondTerm'), i)
                cmds.setAttr((plusMinusAverage_condition + '.colorIfFalseR'), 0)
                cmds.connectAttr((choice_node + '.output'), (plusMinusAverage_condition + '.colorIfTrueR'), f=1)
                cmds.connectAttr((plusMinusAverage_condition + '.outColorR'), (j + '.rotate' + axial), f=1)
            # 添加表达式
            cmds.expression(
                s='if(' + general_controller[0] + '.baking_wheels==' + general_controller[0] + '.expression_type){\n'
                    '    int $start=1;\n'
                    '    int $start_frame=' + general_controller[0] + '.start_frame' + ';\n'
                    '    if(frame <= $start_frame)$start=0;\n'
                    '    float $start_num = FK' + base_joint_name + '.start_num;\n'
                    '    if(frame > $start_frame)$start_num=0;\n'
                    '    float $diameter = FK' + base_joint_name + '.diameter;\n'
                    '    float $autoRoll = FK' + base_joint_name + '.autoRoll;\n'
                    '    float $sideAngle=prevPosAngler' + base_joint_name + '.rotateX;\n'
                    '    float $scale = MainScaleMultiplyDivide.input1Y;\n'
                    '    float $prevPosX=FK' + base_joint_name + '.prevPosX;\n'
                    '    float $prevPosY=FK' + base_joint_name + '.prevPosY;\n'
                    '    float $prevPosZ=FK' + base_joint_name + '.prevPosZ;\n'
                    '    prevPosOffset' + base_joint_name + '.translateX=$prevPosX;\n'
                    '    prevPosOffset' + base_joint_name + '.translateY=$prevPosY;\n'
                    '    prevPosOffset' + base_joint_name + '.translateZ=$prevPosZ;\n'
                    '    float $nowPosX=nowPos' + base_joint_name + '.translateX;\n'
                    '    float $nowPosY=nowPos' + base_joint_name + '.translateY;\n'
                    '    float $nowPosZ=nowPos' + base_joint_name + '.translateZ;\n'
                    '    float $distance=`mag<<$nowPosX-$prevPosX,$nowPosY-$prevPosY,$nowPosZ-$prevPosZ>>`;\n'
                    '    float $curRotX=FKX' + base_joint_name + '.calculate_tire_num;\n'
                    '    float $piD = 3.14 * $diameter;\n'
                    '    FKX' + base_joint_name + '.calculate_tire_num=$start_num+$start*($curRotX+($distance/$piD)*360 * $autoRoll * 1 * sin(deg_to_rad($sideAngle)) / $scale);\n'
                    '    FK' + base_joint_name + '.prevPosX=$nowPosX;\n'
                    '    FK' + base_joint_name + '.prevPosY=$nowPosY;\n'
                    '    FK' + base_joint_name + '.prevPosZ=$nowPosZ;\n'
                    '}',
                ae=1, uc='all', o='', n=(base_joint_name + '_WheelExpression'))

        # 添加表达式
        cmds.expression(s='if(' + general_controller[0] + '.baking_wheels==1 && ' + general_controller[0] + '.expression_type==1){\n'
                 '    int $start=1;\n'
                 '    string $car[]=`ls "*.baking_wheels"`;\n'
                 '    int $end_frame = `playbackOptions -q -max`;\n'
                 '    int $now_frame = `currentTime -q`;\n'
                 '    for($i=0;$i<size($car);$i++){\n'
                 '        int $open=`getAttr $car[$i]`;\n'
                 '        if($open==1){\n'
                 '            string $soure[];\n'
                 '            int $numTok=`tokenize $car[$i] "." $soure`;\n'
                 '            float $start_frame=`getAttr ($soure[0]+".start_frame")`;\n'
                 '            if(frame>=$start_frame){\n'
                 '                string $tire[]=`ls ($soure[0]+".tire")`;\n'
                 '                string $tires[]=`listConnections -d 1 $tire[0]`;\n'
                 '                for($j=0;$j<size($tires);$j++){\n'
                 '                    float $tire_num=`getAttr ($tires[$j]+".calculate_tire_num")`;\n'
                 '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
                 '                    setAttr ($tires[$j]+".baking_wheel") $tire_num;\n'
                 '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
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
                      ae=1, uc='all', o='', n=('BakingWheelExpression'))
        cmds.select(general_controller[0])

        cmds.addAttr(general_controller[0], ln='node', dt='string')
        cmds.setAttr(general_controller[0]+'.node', str(need_delete), type='string')

        cmds.undoInfo(cck=1)

    # 从零开始创建轮胎表达式
    def create_tire(self):
        # 获取要删除的节点
        need_delete = []
        surface = cmds.ls(sl=1)
        # 加载总控制器
        self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit'])
        tire_parent_controller = cmds.ls(sl=1)
        # 加载轮子控制器
        self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit'])
        tire_controller = cmds.ls(sl=1)
        # 加载轮子长度
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        tire_perimeter = cmds.ls(sl=1)
        # 加载输出骨骼
        self.maya_common.select_text_target(self.line_edit_4, ['QLineEdit'])
        tire_joint = cmds.ls(sl=1)

        grp = cmds.group(em=1, n='All_Tire_Grp')

        # 给总样条添加属性
        cmds.addAttr(tire_parent_controller, ln='tire', at='bool')
        # cmds.setAttr((tire_parent_controller[0]+'.tire'), e=1, channelBox=True, lock=True)
        cmds.addAttr(tire_parent_controller, ln='baking_wheels', at='bool')
        cmds.setAttr((tire_parent_controller[0] + '.baking_wheels'), e=1, channelBox=True)
        cmds.addAttr(tire_parent_controller, ln='start_frame', dv=101, at='long')
        cmds.setAttr((tire_parent_controller[0] + '.start_frame'), e=1, channelBox=True)
        cmds.addAttr(tire_parent_controller, ln='expression_type', en="tradition:baking:", at="enum")
        cmds.setAttr((tire_parent_controller[0] + '.expression_type'), e=1, channelBox=True)

        ########################################################################################################################
        for i in range(0, len(tire_controller)):
            # 创建烘焙骨骼
            baking_bones = cmds.joint(p=(0, 0, 0), n=(tire_controller[i] + '_baking_joint'))
            cmds.parent(baking_bones, tire_controller[i])
            cmds.setAttr(baking_bones + '.jointOrientX', 0)
            cmds.setAttr(baking_bones + '.jointOrientY', 0)
            cmds.setAttr(baking_bones + '.jointOrientZ', 0)
            cmds.delete(cmds.parentConstraint(tire_controller[i], baking_bones, w=1))
            # 创建
            prePosA = cmds.spaceLocator(p=(0, 0, 0), n=(tire_controller[i] + '_car_bl_prePosLocA'))
            nowPos = cmds.spaceLocator(p=(0, 0, 0), n=(tire_controller[i] + '_car_bl_nowPosLoc'))
            prePos = cmds.spaceLocator(p=(0, 0, 0), n=(tire_controller[i] + '_car_bl_prePosLoc'))
            move_grp = cmds.group(n=(tire_controller[i] + '_Tire'))
            cmds.setAttr(tire_controller[i] + '_car_bl_prePosLoc.visibility', 0)
            cmds.select(nowPos, prePosA)
            Group1 = cmds.group(n=(tire_controller[i] + '_car_bl_locGrp'))
            cmds.setAttr(tire_controller[i] + '_car_bl_locGrp.visibility', 0)

            cmds.addAttr((tire_controller[i]), ln='prePosX', dv=0, at='double')
            # cmds.setAttr((tire_controller[i]+'.prePosX'), e=1, keyable=True)
            cmds.addAttr((tire_controller[i]), ln='prePosY', dv=0, at='double')
            # cmds.setAttr((tire_controller[i]+'.prePosY'), e=1, keyable=True)
            cmds.addAttr((tire_controller[i]), ln='prePosZ', dv=0, at='double')
            # cmds.setAttr((tire_controller[i]+'.prePosZ'), e=1, keyable=True)

            cmds.addAttr((tire_controller[i]), ln='direction_num', dv=0, at='double')
            # cmds.setAttr((tire_controller[i]+'.direction_num'), e=1, keyable=True)

            cmds.select(Group1, move_grp)
            top_grp = cmds.group(n=(tire_controller[i] + 'Tire_Grp'))
            cmds.parent(top_grp, grp)

            cmds.pointConstraint(prePosA, prePos, weight=1)
            cmds.pointConstraint(move_grp, nowPos, weight=1)
            cmds.delete(cmds.pointConstraint(tire_controller[i], top_grp, weight=1))
            curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
            need_delete.append(curveInfo)
            cmds.connectAttr((tire_perimeter[i] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), f=1)

            # 给样条添加属性
            cmds.addAttr(tire_controller[i], ln='running_direction', en='x:y:z:', at='enum')
            cmds.setAttr((tire_controller[i] + '.running_direction'), e=1, channelBox=True)
            cmds.setAttr((tire_controller[i] + '.running_direction'), 2)
            cmds.addAttr(tire_controller[i], ln='axial', en='x:y:z:', at='enum')
            cmds.setAttr((tire_controller[i] + '.axial'), e=1, channelBox=True)
            cmds.addAttr(tire_controller[i], ln='start_num', dv=0, at='double')
            cmds.setAttr((tire_controller[i] + '.start_num'), e=1, keyable=True)
            cmds.addAttr(tire_controller[i], ln='baking_num', dv=0, at='double')
            cmds.setAttr((tire_controller[i] + '.baking_num'), e=1, keyable=True)
            cmds.addAttr(tire_controller[i], ln='magnification', dv=1, at='double')
            cmds.setAttr((tire_controller[i] + '.magnification'), e=1, keyable=True)
            # 给骨骼添加属性
            cmds.addAttr(baking_bones, ln='tire', at='bool')
            # cmds.setAttr((baking_bones + '.tire'), e=1, channelBox=True)
            cmds.addAttr(baking_bones, ln='calculate_tire_num', dv=0, at='double')
            cmds.setAttr((baking_bones + '.calculate_tire_num'), e=1, keyable=True)
            # 添加骨骼属性代理(代码里给此属性k帧)
            cmds.addAttr(baking_bones, proxy=(tire_controller[i] + '.baking_num'), longName='baking_wheel')
            # 添加总控制器属性代理
            cmds.addAttr(tire_parent_controller, proxy=(tire_controller[i] + '.baking_num'), longName=baking_bones)
            # 建立节点关系
            cmds.connectAttr((tire_parent_controller[0] + '.tire'), (baking_bones + '.tire'), f=1)
            choice_node = cmds.shadingNode('choice', asUtility=1)
            need_delete.append(choice_node)
            cmds.connectAttr((tire_parent_controller[0] + '.expression_type'), (choice_node + '.selector'), f=1)
            cmds.connectAttr((baking_bones + '.calculate_tire_num'), (choice_node + '.input[0]'), f=1)
            cmds.connectAttr((tire_controller[i] + '.baking_num'), (choice_node + '.input[1]'), f=1)
            for j, axial in zip(range(0, 3), ['X', 'Y', 'Z']):
                plusMinusAverage_condition = cmds.shadingNode('condition', asUtility=1)
                need_delete.append(plusMinusAverage_condition)
                cmds.connectAttr((tire_controller[i] + '.axial'), (plusMinusAverage_condition + '.firstTerm'), f=1)
                cmds.setAttr((plusMinusAverage_condition + '.secondTerm'), j)
                cmds.setAttr((plusMinusAverage_condition + '.colorIfFalseR'), 0)
                cmds.connectAttr((choice_node + '.output'), (plusMinusAverage_condition + '.colorIfTrueR'), f=1)
                cmds.connectAttr((plusMinusAverage_condition + '.outColorR'), (baking_bones + '.rotate' + axial), f=1)
            choice_node = cmds.shadingNode('choice', asUtility=1)
            need_delete.append(choice_node)
            cmds.connectAttr((tire_controller[i] + '.running_direction'), (choice_node + '.selector'), f=1)
            cmds.connectAttr((tire_controller[i] + '_car_bl_prePosLoc.translateX'), (choice_node + '.input[0]'), f=1)
            cmds.connectAttr((tire_controller[i] + '_car_bl_prePosLoc.translateY'), (choice_node + '.input[1]'), f=1)
            cmds.connectAttr((tire_controller[i] + '_car_bl_prePosLoc.translateZ'), (choice_node + '.input[2]'), f=1)
            cmds.connectAttr((choice_node + '.output'), (tire_controller[i] + '.direction_num'))

            cmds.expression(s=('if('+tire_parent_controller[0]+'.baking_wheels=='+tire_parent_controller[0]+'.expression_type){\n'
                            '   int $start=1;\n'
                            '   int $start_frame='+tire_parent_controller[0]+'.start_frame;\n'
                            '   if(frame <= $start_frame)$start=0;\n'
                            '   float $start_num = '+tire_controller[i]+'.start_num;\n'
                            '   if(frame > $start_frame)$start_num=0;\n'
                            '   float $autoRoll=' + tire_controller[i] + '.magnification;\n'
                            '   float $prePosX=' + tire_controller[i] + '.prePosX;\n'
                            '   float $prePosY=' + tire_controller[i] + '.prePosY;\n'
                            '   float $prePosZ=' + tire_controller[i] + '.prePosZ;\n'
                            '   float $nowPosX=' + tire_controller[i] + '_car_bl_nowPosLoc.translateX;\n'
                            '   float $nowPosY=' + tire_controller[i] + '_car_bl_nowPosLoc.translateY;\n'
                            '   float $nowPosZ=' + tire_controller[i] + '_car_bl_nowPosLoc.translateZ;\n'
                            '   float $dis=`mag(<<$nowPosX,$nowPosY,$nowPosZ>>-<<$prePosX,$prePosY,$prePosZ>>)`;\n'
                            '   ' + tire_controller[i] + '_car_bl_prePosLocA.translateX=$prePosX;\n'
                            '   ' + tire_controller[i] + '_car_bl_prePosLocA.translateY=$prePosY;\n'
                            '   ' + tire_controller[i] + '_car_bl_prePosLocA.translateZ=$prePosZ;\n'
                            '   ' + tire_controller[i] + '.prePosX=$nowPosX;\n'
                            '   ' + tire_controller[i]+ '.prePosY=$nowPosY;\n'
                            '   ' + tire_controller[i] + '.prePosZ=$nowPosZ;\n'
                            '   float $dirPreZ=' + tire_controller[i]+'.direction_num;\n'
                            '   int $dir=1;\n'
                            '   if($dirPreZ<0)$dir=-1;\n'
                            '   float $perimeter=' + curveInfo + '.arcLength;\n'
                            '   float $curRoll=' + baking_bones + '.calculate_tire_num;\n'
                            '   ' + baking_bones + '.calculate_tire_num=$start_num+$start*($curRoll+($dis/$perimeter)*360*$autoRoll*$dir);\n'
                            '}'),
                            ae=1, uc='all', o='', n=(tire_joint[i]+'_WheelExpression'))
            cmds.delete(cmds.pointConstraint(tire_controller[i], move_grp, w=1))
            cmds.parentConstraint(tire_controller[i], move_grp, w=1, mo=1)

            rotateX = cmds.listConnections((tire_joint[i] + '.rotateX'), p=1)
            if rotateX:
                cmds.disconnectAttr(rotateX[0], (tire_joint[i] + '.rotateX'))
            rotateY = cmds.listConnections((tire_joint[i] + '.rotateY'), p=1)
            if rotateY:
                cmds.disconnectAttr(rotateY[0], (tire_joint[i] + '.rotateY'))
            rotateZ = cmds.listConnections((tire_joint[i] + '.rotateZ'), p=1)
            if rotateZ:
                cmds.disconnectAttr(rotateZ[0], (tire_joint[i] + '.rotateZ'))

            cmds.orientConstraint(baking_bones, tire_joint[i], mo=1, weight=1)

            cmds.parent(tire_perimeter[i], grp)
            cmds.setAttr((tire_perimeter[i] + '.visibility'), 0)
            cmds.parentConstraint(tire_controller[i], tire_perimeter[i], w=1)
            cmds.scaleConstraint(tire_controller[i], tire_perimeter[i], w=1)

            cmds.setAttr((tire_controller[i] + '.magnification'), cb=False, k=True)
            cmds.setAttr((tire_controller[i] + '.magnification'), cb=True, k=False)

        # 添加表达式
        cmds.expression(s='if(' + tire_parent_controller[0] + '.baking_wheels==1 && ' + tire_parent_controller[
            0] + '.expression_type==1){\n'
                 '    int $start=1;\n'
                 '    string $car[]=`ls "*.baking_wheels"`;\n'
                 '    int $end_frame = `playbackOptions -q -max`;\n'
                 '    int $now_frame = `currentTime -q`;\n'
                 '    for($i=0;$i<size($car);$i++){\n'
                 '        int $open=`getAttr $car[$i]`;\n'
                 '        if($open==1){\n'
                 '            string $soure[];\n'
                 '            int $numTok=`tokenize $car[$i] "." $soure`;\n'
                 '            float $start_frame=`getAttr ($soure[0]+".start_frame")`;\n'
                 '            if(frame>=$start_frame){\n'
                 '                string $tire[]=`ls ($soure[0]+".tire")`;\n'
                 '                string $tires[]=`listConnections -d 1 $tire[0]`;\n'
                 '                for($j=0;$j<size($tires);$j++){\n'
                 '                    float $tire_num=`getAttr ($tires[$j]+".calculate_tire_num")`;\n'
                 '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
                 '                    setAttr ($tires[$j]+".baking_wheel") $tire_num;\n'
                 '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
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
                      ae=1, uc='all', o='', n=('BakingWheelExpression'))
        cmds.select(tire_parent_controller[0])
        cmds.addAttr(tire_parent_controller[0], ln='node', dt='string')
        cmds.setAttr(tire_parent_controller[0] + '.node', str(need_delete), type='string')


    # 删除轮胎
    def delete_adv_tire(self):
        # 获取总控制器
        general_controller = cmds.ls(sl=1)
        # 获取所有表达式
        expression = cmds.ls(type='expression')
        # 获取所有疑似车轮表达式的对象
        wheel = cmds.ls('*WheelExpression*')
        # 筛选出轮胎表达式
        wheel_expression = list(set(expression) & set(wheel))
        # 获取表达式输出骨骼
        joint = cmds.listConnections(wheel_expression, d=1, type='joint')
        # 删除adv轮胎表达式
        cmds.delete(wheel_expression)
        #删除的属性
        cmds.setAttr((general_controller[0] + '.tire'), l=False)
        cmds.deleteAttr(general_controller[0]+'.tire')
        cmds.deleteAttr(general_controller[0] + '.baking_wheels')
        cmds.deleteAttr(general_controller[0] + '.start_frame')
        cmds.deleteAttr(general_controller[0] + '.expression_type')
        for j in joint:
            # 拆解出adv源骨骼的名称
            base_joint_name = j[3:]
            # 删除属性
            cmds.deleteAttr('FK' + base_joint_name + '.axial')
            cmds.deleteAttr('FK' + base_joint_name + '.start_num')
            cmds.deleteAttr('FK' + base_joint_name + '.baking_num')
            cmds.deleteAttr(j + '.tire')
            cmds.deleteAttr(j + '.calculate_tire_num')
            cmds.deleteAttr(j + '.baking_wheel')
            cmds.deleteAttr(general_controller[0] + '.' + base_joint_name)

        need_delete = cmds.getAttr(general_controller[0] + '.node')
        need_delete = ast.literal_eval(need_delete)

        for d in need_delete:
            try:
                cmds.delete(d)
            except:
                pass
        cmds.deleteAttr(general_controller[0] + '.node')

    def delete_self_tire(self):
        cmds.undoInfo(ock=1)
        # 加载总控制器
        self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit'])
        tire_parent_controller = cmds.ls(sl=1)
        # 加载轮子控制器
        self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit'])
        tire_controller = cmds.ls(sl=1)

        need_delete = cmds.getAttr(tire_parent_controller[0] + '.node')
        need_delete = ast.literal_eval(need_delete)

        for d in need_delete:
            try:
                cmds.delete(d)
            except:
                pass
        cmds.deleteAttr(tire_parent_controller[0] + '.node')

        cmds.delete('All_Tire_Grp')
        # 删除属性
        cmds.setAttr((tire_parent_controller[0] + '.tire'), l=False)
        cmds.deleteAttr(tire_parent_controller[0] + '.tire')
        cmds.deleteAttr(tire_parent_controller[0] + '.baking_wheels')
        cmds.deleteAttr(tire_parent_controller[0] + '.start_frame')
        cmds.deleteAttr(tire_parent_controller[0] + '.expression_type')
        ########################################################################################################################
        for i in range(0, len(tire_controller)):
            # 删除烘焙骨骼
            cmds.delete((tire_controller[i] + '_baking_joint'))
            cmds.deleteAttr(tire_controller[i] + '.prePosX')
            cmds.deleteAttr(tire_controller[i] + '.prePosY')
            cmds.deleteAttr(tire_controller[i] + '.prePosZ')
            cmds.deleteAttr(tire_controller[i] + '.direction_num')
            # 给样条添加属性
            cmds.deleteAttr(tire_controller[i] + '.running_direction')
            cmds.deleteAttr(tire_controller[i] + '.axial')
            cmds.deleteAttr(tire_controller[i] + '.start_num')
            cmds.deleteAttr(tire_controller[i] + '.baking_num')
            cmds.deleteAttr(tire_controller[i] + '.magnification')
            cmds.deleteAttr(tire_parent_controller[0] + '.' + tire_controller[i] + '_baking_joint')
        cmds.delete('*_WheelExpression')
        cmds.delete('BakingWheelExpression')
        cmds.select(cl=1)
        cmds.undoInfo(cck=1)
window = Window()
if __name__ == '__main__':
    window.show()

