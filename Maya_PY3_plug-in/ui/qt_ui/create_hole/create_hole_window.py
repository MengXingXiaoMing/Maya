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


import others_library
from others_library import *
importlib.reload(others_library)

import maya_common
from maya_common import *
importlib.reload(maya_common)

import ui_edit
from ui_edit import *
importlib.reload(ui_edit)

import curve
from curve import *
importlib.reload(curve)

import controller
from controller import *
importlib.reload(controller)


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('创建洞(Maya'+self.maya_version+')')


        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = self.root_path + '\\' + maya_version

        self.other_library = OthersLibrary()
        self.maya_common = MayaCommon()
        self.ui_edit = UiEdit()
        self.curve = CreateAndEditCurve()
        self.controller = CurveControllerEdit()


        self.top_name = 'Hole_all_Grp_'
        self.create_widgets()
        self.create_layouts()
        self.create_connect()

        self.create_hole_ui()
        self.load_data()
    def create_widgets(self):
        # 第一行
        # self.button_0 = QtWidgets.QPushButton('选择并加载当前主控制器存储的数据继续创建（不选择则创建新的）')
        self.comboBox_0 = QtWidgets.QComboBox()

        self.Label_1 = QtWidgets.QLabel('跟随骨骼：')
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_1 = QtWidgets.QPushButton('加载')

        self.Label_2 = QtWidgets.QLabel('整体跟随对象：')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton('加载')

        self.check_box_1 = QtWidgets.QCheckBox('洞上边缘')
        self.check_box_2 = QtWidgets.QCheckBox('洞下边缘')
        self.button_3 = QtWidgets.QPushButton('创建洞基础')

        self.button_4 = QtWidgets.QPushButton('帮助')
        #
        # self.label_1 = QtWidgets.QLabel('创建额外边缘')
        # self.label_1.setAlignment(QtCore.Qt.AlignCenter)  # 设置文本居中

        # self.comboBox_1 = QtWidgets.QComboBox()
        # self.comboBox_1.addItems(['0'])
        # self.check_box_3 = QtWidgets.QCheckBox('额外洞上边缘')
        # self.button_5 = QtWidgets.QPushButton('选择额外上边缘样条')
        # self.check_box_4 = QtWidgets.QCheckBox('额外洞下边缘')
        # self.button_6 = QtWidgets.QPushButton('选择额外下边缘样条')
        # self.button_7 = QtWidgets.QPushButton('创建额外洞边缘')

        self.button_8 = QtWidgets.QPushButton('选择总控制器创建驱动组并选择')
        self.button_9 = QtWidgets.QPushButton('选择总控制器删除驱动组')
        self.button_10 = QtWidgets.QPushButton('选择洞闭合驱动目标')

        self.button_11 = QtWidgets.QPushButton('选择两个边缘骨骼对应数量和排列方向完全相同的总控制器创建拉链')

        self.button_12 = QtWidgets.QPushButton('选择曲面和对应控制器创建附着控制器')
        self.button_13 = QtWidgets.QPushButton('选择删除附着控制器关联')

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

        v_Box_layout_2 = QtWidgets.QVBoxLayout(self)
        h_Box_layout_1.addLayout(v_Box_layout_2)
        v_Box_layout_2.addWidget(self.comboBox_0)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_2.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.Label_1)
        h_Box_layout_3.addWidget(self.line_edit_1)
        h_Box_layout_3.addWidget(self.button_1)
        h_Box_layout_3.setSpacing(1)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_2.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.Label_2)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_2)
        h_Box_layout_4.setSpacing(1)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_2.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.check_box_1)
        h_Box_layout_5.addWidget(self.check_box_2)

        v_Box_layout_2.addWidget(self.button_3)
        # v_Box_layout_2.addWidget(self.button_4)

        splitter = QtWidgets.QSplitter(Qt.Vertical)
        splitter.setContentsMargins(0, 0, 0, 0)
        v_Box_layout_2.addWidget(splitter)

        Widget_1 = QtWidgets.QWidget()
        splitter.addWidget(Widget_1)
        v_Box_layout_3 = QtWidgets.QVBoxLayout(Widget_1)
        v_Box_layout_3.setContentsMargins(0, 0, 0, 0)
        v_Box_layout_3.addWidget(self.button_8)
        v_Box_layout_3.addWidget(self.button_9)
        v_Box_layout_3.addWidget(self.button_11)
        v_Box_layout_3.addWidget(self.button_4)
        # v_Box_layout_3.addWidget(self.label_1)
        # v_Box_layout_3.addWidget(self.comboBox_1)
        #
        # h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        # v_Box_layout_3.addLayout(h_Box_layout_6)
        # h_Box_layout_6.addWidget(self.check_box_3)
        # h_Box_layout_6.addWidget(self.button_5)
        #
        # h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        # v_Box_layout_3.addLayout(h_Box_layout_7)
        # h_Box_layout_7.addWidget(self.check_box_4)
        # h_Box_layout_7.addWidget(self.button_6)
        # v_Box_layout_3.addWidget(self.button_7)

        v_Box_layout_3.setSpacing(1)

        Widget_2 = QtWidgets.QWidget()
        splitter.addWidget(Widget_2)
        v_Box_layout_4 = QtWidgets.QVBoxLayout(Widget_2)
        v_Box_layout_4.setContentsMargins(0, 0, 0, 0)


        # v_Box_layout_4.addWidget(self.button_10)
        v_Box_layout_4.addWidget(self.button_12)
        v_Box_layout_4.addWidget(self.button_13)
        v_Box_layout_4.setSpacing(1)


        main_layout.addStretch(1)

    def create_connect(self):
        # self.button_0.clicked.connect(self.get_and_create_hole_grp)  # 选择拷贝源按钮
        self.comboBox_0.currentIndexChanged.connect(self.load_data)
        self.button_1.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))  # 加载骨骼
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))  # 加载朝向跟随
        self.button_3.clicked.connect(self.create_hole)  # 创建基础
        self.button_4.clicked.connect(lambda: self.other_library.open_help(self.file_path))  # 帮助
        self.button_8.clicked.connect(self.create_driver_grp_and_select)
        self.button_9.clicked.connect(self.delete_driver_grp)
        self.button_11.clicked.connect(self.create_new_output_bone)  # 创建拉链
        self.button_12.clicked.connect(self.create_attach)  # 创建拉链
        self.button_13.clicked.connect(self.delete_attach)  # 创建拉链

        self.Restore_command_association()

    # 加载数据并更新ui
    def load_data(self):
        self.Disconnect_command_association()
        top_num = int(self.comboBox_0.currentText())
        # print(top_num)
        # joint = self.line_edit_1.text()
        # top_parent = self.line_edit_2.text()
        top_grp = self.top_name + str(top_num)
        self.line_edit_1.setText('')
        self.line_edit_2.setText('')
        self.check_box_1.setChecked(False)
        self.check_box_2.setChecked(False)
        if cmds.objExists(top_grp):
            if cmds.objExists(top_grp + '.follow_joint'):
                follow_joint = cmds.getAttr(top_grp+'.follow_joint')
                self.line_edit_1.setText(follow_joint)

            if cmds.objExists(top_grp + '.follow_obj'):
                follow_obj = cmds.getAttr(top_grp + '.follow_obj')
                self.line_edit_2.setText(follow_obj)

            if cmds.objExists('Hole_up_surface_' + str(top_num)):
                self.check_box_1.setChecked(True)

            if cmds.objExists('Hole_dn_surface_' + str(top_num)):
                self.check_box_2.setChecked(True)

            # FK_controller_sys = cmds.getAttr('MainSystem_Grp.FK_controller_sys')  # 获取fk控制器系统
            # FK_controller_sys = FK_controller_sys.replace('\'', '\"')
            # FK_controller_sys = json.loads(FK_controller_sys)



        self.Restore_command_association()

    # 切换ui
    def switch_ui(self):
        self.Disconnect_command_association()
        top_num = int(self.comboBox_0.currentText())
        # joint = self.line_edit_1.text()
        # top_parent = self.line_edit_2.text()
        top_grp = self.top_name + str(top_num)
        if cmds.objExists(top_grp):
            if cmds.objExists(top_grp + '.follow_joint'):
                follow_joint = cmds.getAttr(top_grp + '.follow_joint')
                self.line_edit_1.setText(follow_joint)

            if cmds.objExists(top_grp + '.follow_obj'):
                follow_obj = cmds.getAttr(top_grp + '.follow_obj')
                self.line_edit_2.setText(follow_obj)

            if cmds.objExists('Hole_up_surface_' + str(top_num)):
                self.check_box_1.setChecked(True)

            if cmds.objExists('Hole_dn_surface_' + str(top_num)):
                self.check_box_2.setChecked(True)

            # FK_controller_sys = cmds.getAttr('MainSystem_Grp.FK_controller_sys')  # 获取fk控制器系统
            # FK_controller_sys = FK_controller_sys.replace('\'', '\"')
            # FK_controller_sys = json.loads(FK_controller_sys)

        self.Restore_command_association()

    # 断开命令关联
    def Disconnect_command_association(self):
        self.check_box_1.stateChanged.disconnect(self.load_or_delete_up_edge_hole)
        self.check_box_2.stateChanged.disconnect(self.load_or_delete_dn_edge_hole)

    # 恢复命令关联
    def Restore_command_association(self):
        self.check_box_1.stateChanged.connect(self.load_or_delete_up_edge_hole)  # 创建或删除上边缘
        self.check_box_2.stateChanged.connect(self.load_or_delete_dn_edge_hole)  # 创建或删除上边缘

    # 获取有第几个洞组
    def get_and_create_hole_grp(self):
        all_hole_grp = cmds.ls(self.top_name+'*')
        num = 0
        if all_hole_grp:
            all_num = []
            for grp in all_hole_grp:
                num = int(grp.split('_')[-1])
                all_num.append(num)
            num = max(all_num)
        # cmds.group(n=name + str(num),em=1)
        print('有', num, '个洞组')
        return num

    # 创建总个数+1的ui
    def create_hole_ui(self):
        num = self.get_and_create_hole_grp()
        for i in range(num+2):
            self.comboBox_0.addItems([str(i)])

    # 加载或删除洞上边缘
    def load_or_delete_up_edge_hole(self):
        top_num = int(self.comboBox_0.currentText())
        other_edge = 'Hole_dn_edge_'+str(top_num)
        if cmds.objExists(other_edge):
            self.create_up_dn_edge_surface(self.check_box_1, 'up', [other_edge])
        else:
            self.create_up_dn_edge_surface(self.check_box_1, 'up', [])

    # 加载或删除洞下边缘
    def load_or_delete_dn_edge_hole(self):
        top_num = int(self.comboBox_0.currentText())
        other_edge = 'Hole_up_edge_' + str(top_num)
        if cmds.objExists(other_edge):
            self.create_up_dn_edge_surface(self.check_box_2, 'dn', [other_edge])
        else:
            self.create_up_dn_edge_surface(self.check_box_2, 'dn', [])

    # 创建上下边缘曲面
    def create_up_dn_edge_surface(self, check_box, add_name, other_edge):
        sel = cmds.ls(sl=1, fl=1)
        center_joint = self.line_edit_1.text()
        if_create = check_box.isChecked()
        top_num = int(self.comboBox_0.currentText())
        top_grp_name = self.top_name + str(top_num)
        if not cmds.objExists(top_grp_name):
            cmds.group(n=top_grp_name, em=1)

        # print(top_num)
        name_list = []
        for txt in ['_edge_', '_surface_']:
            name = 'Hole_' +add_name+ txt + str(top_num)
            if if_create == False:
                name = 'Hole_' +add_name+ txt + str(top_num)
                if cmds.objExists(name):
                    cmds.delete(name)
            name_list.append(name)
        else:
            if sel and sel[0].split('.')[-1].split('[')[0] == 'e':
                cmds.select(sel)
                curve = cmds.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, ch=0, n=name_list[0])
                # 判断是否反转
                reversal = False
                if other_edge and cmds.objExists(other_edge[0]):
                    # 获取上下朝向是否一致
                    curve_shape = cmds.listRelatives(other_edge[0], s=1)
                    closest_point = self.get_nearest_point(curve, curve_shape[0]+'.cv[0]')
                    num = int(closest_point.split('[')[-1][:-1])
                    if num != 0:
                        reversal = True
                        cmds.reverseCurve(curve, ch=1, rpo=1)
                cmds.parent(curve, top_grp_name)
                cmds.select(sel)
                curve = cmds.polyToCurve(form=2, degree=3, conformToSmoothMeshPreview=1, ch=0)
                cmds.rebuildCurve(curve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=4, d=3, tol=0.01)

                if reversal == True:
                    cmds.reverseCurve(curve, ch=1, rpo=1)

                cmds.select(curve)
                cmds.nurbsCurveToBezier()
                shape = cmds.listRelatives(curve, s=1, type='nurbsCurve')
                cmds.setAttr(shape[0] + '.dispCV', 1)
                surface = cmds.revolve(curve, ch=0, po=3, rn=0, ssw=0, esw=0.1, ut=0, tol=0.01, degree=1, s=1, ulp=1,
                                       ax=(1, 0, 0), n=name_list[1])

                cmds.delete(curve)
                for i in range(13):
                    follow_point = surface[0] + '.cv[' + str(i) + '][0]'
                    point = surface[0] + '.cv[' + str(i) + '][1]'
                    follow_cluster = cmds.cluster(follow_point)
                    cluster = cmds.cluster(point)
                    # print(cluster)
                    cmds.select(cl=1)
                    joint_1 = cmds.joint(p=(0, 0, 0))
                    joint_2 = cmds.joint(p=(0, 0, 0))
                    cmds.delete(cmds.pointConstraint(center_joint, joint_1))
                    cmds.delete(cmds.pointConstraint(follow_cluster, joint_2))
                    cmds.select(joint_1)
                    cmds.joint(e=1, oj='xyz', secondaryAxisOrient='xup', ch=0, zso=1)
                    cmds.pointConstraint(joint_2, cluster)
                    cmds.setAttr(joint_1 + '.sx', 1.1)
                    cmds.select(surface)
                    mel.eval('DeleteHistory;')
                    cmds.delete(cluster[1], joint_1)
                cmds.parent(surface, top_grp_name)
                # 按样条挤出后根据中心骨骼调整朝向
                print('曲面生成完毕', )
            else:
                self.Disconnect_command_association()
                check_box.setChecked(False)
                self.Restore_command_association()
                cmds.warning('请选择线')

    # 创建基础洞
    @Withdraw
    def create_hole(self):
        top_num = int(self.comboBox_0.currentText())
        top_grp = self.top_name + str(top_num)
        have_up_surface = self.check_box_1.isChecked()
        have_dn_surface = self.check_box_2.isChecked()
        follow_joint = self.line_edit_1.text()
        follow_obj = self.line_edit_2.text()
        add_item_text=self.comboBox_0.itemText(self.comboBox_0.count() - 1)
        self.comboBox_0.addItems([str(int(add_item_text)+1)])
        if have_up_surface == True and have_dn_surface == True and follow_joint and follow_obj:
            follow_joint_an = top_grp + '.follow_joint'
            if not cmds.objExists(follow_joint_an):
                cmds.addAttr(top_grp, ln='follow_joint', dt='string')
                cmds.setAttr(follow_joint_an, e=1, keyable=True)
            cmds.setAttr(follow_joint_an, follow_joint, type='string')
            follow_obj_an = top_grp + '.follow_obj'
            if not cmds.objExists(follow_obj_an):
                cmds.addAttr(top_grp, ln='follow_obj', dt='string')
                cmds.setAttr(follow_obj_an, e=1, keyable=True)
            cmds.setAttr(follow_obj_an, follow_obj, type='string')

            up_surface = 'Hole_up_surface_' + str(top_num)
            dn_surface = 'Hole_dn_surface_' + str(top_num)
            cmds.setAttr(up_surface + '.visibility', 0)
            cmds.setAttr(dn_surface + '.visibility', 0)

            up_j = self.create_bone_by_point(top_num, follow_joint, up_surface + '.cv[6][0]', 'up_joint_', up_surface, 0)
            dn_j = self.create_bone_by_point(top_num, follow_joint, dn_surface + '.cv[6][0]', 'dn_joint_', dn_surface, 0)
            side_F_updn_j = self.create_bone_by_point(top_num, follow_joint, up_surface + '.cv[0][0]', 'sd_F_joint_updn_', up_surface, 1)
            side_E_updn_j = self.create_bone_by_point(top_num, follow_joint, up_surface + '.cv[12][0]', 'sd_E_joint_updn_', up_surface, 1)

            cmds.select(cl=1)
            center_j = cmds.joint(n='center_joint_' + str(top_num))
            center_end_j = cmds.joint(n='center_joint_End_' + str(top_num))
            cmds.pointConstraint(follow_joint, center_j)
            cmds.delete(cmds.pointConstraint(up_j[1], dn_j[1], center_end_j))
            center_j = [center_j,center_end_j]
            cmds.setAttr(center_j[0] + '.visibility', 0)

            cmds.joint(center_j, e=1, zso=1, oj='xyz', sao='yup')
            ## 方向约束
            i = 0
            for joint, obj in zip([center_j, up_j, dn_j, side_F_updn_j, side_E_updn_j],
                                 [up_j[1], center_end_j, center_end_j, center_end_j, center_end_j]):
                cmds.select(cl=1)
                copy_j = cmds.joint()
                cmds.delete(cmds.pointConstraint(joint[1], copy_j))
                cmds.delete(cmds.aimConstraint(copy_j, joint[0], offset=(0, 0, 0), weight=1, aimVector=(1, 0, 0),
                                               upVector=(0, 1, 0), worldUpType='object', worldUpObject=obj))
                ## 冻结变换
                cmds.makeIdentity(joint, apply=True, r=1, n=0)
                cmds.delete(copy_j)
                if i > 0:
                    cmds.parent(joint[0], center_j[0])
                i = i + 1

            # 创建根骨骼方向约束
            for joint, num in zip([center_j, up_j, dn_j, side_F_updn_j, side_E_updn_j],[0, 0, 180, 90, -90]):
                cmds.delete(cmds.orientConstraint(center_j[0], joint[1]))
                ## 冻结变换
                cmds.makeIdentity(joint[1], apply=True, r=1, n=0)
                cmds.setAttr(joint[1] + '.rotateX', num)
                cmds.makeIdentity(joint[1], apply=True, r=1, n=0)

            skin_list = self.create_normal_weight_list()
            side_F_up_j, side_E_up_j = self.create_up_down_hole(top_num, follow_joint, '_joint_up_', up_surface,
                                     up_j,
                                     center_j,
                                     [side_F_updn_j, side_E_updn_j],
                                     skin_list)

            # new_skin = []
            # for skin in skin_list:
            #     ls_skin = []
            #     ls_skin.append(skin[0])
            #     ls_skin.append(skin[2])
            #     ls_skin.append(skin[1])
            #     new_skin.append(ls_skin)
            side_F_dn_j, side_E_dn_j = self.create_up_down_hole(top_num, follow_joint, '_joint_dn_', dn_surface,
                                     dn_j,
                                     center_j,
                                     [side_F_updn_j, side_E_updn_j],
                                     skin_list)
            # 父化边缘骨骼
            cmds.parent(side_F_up_j[0], side_F_dn_j[0], side_F_updn_j[0])
            cmds.parent(side_E_up_j[0], side_E_dn_j[0], side_E_updn_j[0])

            # 获取包围盒大小，设定控制器缩放值
            box_min = cmds.getAttr(top_grp+'.boundingBoxMin')[0]
            box_max = cmds.getAttr(top_grp+'.boundingBoxMax')[0]
            base_num = (box_max[0]-box_min[0]+box_max[1]-box_min[1]+box_max[2]-box_min[2])/3
            # print(base_num)
            scale = base_num/1.5001384715239192*0.02
            skin_up_surface, up_grp = self.create_attach_controller(top_num, up_surface, 'up', up_j, side_F_updn_j, side_E_updn_j, center_j, scale, 0)
            # print(skin_up_surface)
            skin_dn_surface, dn_grp = self.create_attach_controller(top_num, dn_surface, 'dn', up_j, side_F_updn_j, side_E_updn_j, center_j, scale, 1)

            up_edge = 'Hole_up_edge_' + str(top_num)
            dn_edge = 'Hole_dn_edge_' + str(top_num)
            cmds.setAttr(up_edge + '.visibility', 0)
            cmds.setAttr(dn_edge + '.visibility', 0)

            up_edge_grp = self.create_out_ctr(top_num, 'up', up_edge, skin_up_surface, center_j, scale * 0.8, 0)
            dn_edge_grp = self.create_out_ctr(top_num, 'dn', dn_edge, skin_dn_surface, center_j, scale * 0.8, 1)

            scale = base_num / 1.5001384715239192 * 1.0
            # 创建总控制器
            all_center_ctr = self.create_top_controller('Hole_center_Top', '', top_num,'圆片', scale, center_j, 'Z', 1, [1.5, 0.0, 0.0], 13)

            # 创建上下控制器
            all_up_ctr = self.create_top_controller('Hole_up_Top', '', top_num, '圆朝向', scale, up_j, 'Z', 2, [1.2, 0.0, 0.0], 13)
            all_up_end_ctr = self.create_top_controller('Hole_up_end_Top', '', top_num, '圆朝向', scale, [up_j[1], up_j[0]], 'Z', 0, [1.2, 0.0, 0.0], 13)
            cmds.parent(all_up_end_ctr[0], all_up_ctr[2])

            all_dn_ctr = self.create_top_controller('Hole_dn_Top', '', top_num, '圆朝向', scale, dn_j, 'Z', 2, [1.2, 0.0, 0.0],13)
            all_dn_end_ctr = self.create_top_controller('Hole_dn_end_Top', '', top_num, '圆朝向', scale, [dn_j[1], dn_j[0]], 'Z', 0, [1.2, 0.0, 0.0], 13)
            cmds.parent(all_dn_end_ctr[0], all_dn_ctr[2])

            # 创建侧面控制器并添加次级影藏
            ## F部分
            all_F_updn_ctr = self.create_top_controller('Hole_F_updn_Top', '', top_num, '圆朝向', scale, side_F_updn_j, 'Z', 2, [1.2, 0.0, 0.0], 13)
            all_F_updn_end_ctr = self.create_top_controller('Hole_F_updn_end_Top', '', top_num, '圆朝向', scale, [side_F_updn_j[1], side_F_updn_j[1]], 'Z', 0, [0.05, 0.0, 0.0], 13)
            cmds.parent(all_F_updn_end_ctr[0], all_F_updn_ctr[2])

            all_F_up_ctr = self.create_top_controller('Hole_F_up_Top', '', top_num, '圆朝向', scale * 0.8, side_F_up_j, 'Z', 3, [1.1, 0.0, 0.1], 17)
            all_F_up_end_ctr = self.create_top_controller('Hole_F_up_end', '', top_num, '圆朝向', scale * 0.8, [side_F_up_j[1], side_F_up_j[1]], 'Z', 0, [0.0, 0.0, -0.1], 6)
            cmds.parent(all_F_up_end_ctr[0], all_F_up_ctr[2])
            cmds.parent(all_F_up_ctr[0], all_F_updn_ctr[2])

            all_F_dn_ctr = self.create_top_controller('Hole_F_dn_Top', '', top_num, '圆朝向', scale * 0.8, side_F_dn_j, 'Z', 3, [1.1, 0.0, -0.1], 17)
            all_F_dn_end_ctr = self.create_top_controller('Hole_F_dn_end_Top', '', top_num, '圆朝向', scale * 0.8, [side_F_dn_j[1], side_F_dn_j[1]], 'Z', 0, [0.0, 0.0, 0.1], 6)
            cmds.parent(all_F_dn_end_ctr[0], all_F_dn_ctr[2])
            cmds.parent(all_F_dn_ctr[0], all_F_updn_ctr[2])

            ## E部分
            all_E_updn_ctr = self.create_top_controller('Hole_E_updn_Top', '', top_num, '圆朝向', scale, side_E_updn_j,'Z', 2, [1.2, 0.0, 0.0], 13)
            all_E_updn_end_ctr = self.create_top_controller('Hole_E_updn_end_Top', '', top_num, '圆朝向', scale,[side_E_updn_j[1], side_E_updn_j[1]], 'Z', 0,[0.05, 0.0, 0.0], 13)
            cmds.parent(all_E_updn_end_ctr[0], all_E_updn_ctr[2])

            all_E_up_ctr = self.create_top_controller('Hole_E_up_Top', '', top_num, '圆朝向', scale * 0.8, side_E_up_j,'Z', 3, [1.1, 0.0, -0.1], 17)
            all_E_up_end_ctr = self.create_top_controller('Hole_E_up_end', '', top_num, '圆朝向', scale * 0.8,[side_E_up_j[1], side_E_up_j[1]], 'Z', 0, [0.0, 0.0, 0.1], 6)
            cmds.parent(all_E_up_end_ctr[0], all_E_up_ctr[2])
            cmds.parent(all_E_up_ctr[0], all_E_updn_ctr[2])

            all_E_dn_ctr = self.create_top_controller('Hole_E_dn_Top', '', top_num, '圆朝向', scale * 0.8, side_E_dn_j,'Z', 3, [1.1, 0.0, 0.1], 17)
            all_E_dn_end_ctr = self.create_top_controller('Hole_E_dn_end_Top', '', top_num, '圆朝向', scale * 0.8,[side_E_dn_j[1], side_E_dn_j[1]], 'Z', 0, [0.0, 0.0, -0.1], 6)
            cmds.parent(all_E_dn_end_ctr[0], all_E_dn_ctr[2])
            cmds.parent(all_E_dn_ctr[0], all_E_updn_ctr[2])

            # 创建影响驱动属性并约束关联
            self.create_secondary([all_F_updn_ctr, all_F_updn_end_ctr], [[all_F_up_ctr, all_F_up_end_ctr], [all_F_dn_ctr, all_F_dn_end_ctr]])
            self.create_secondary([all_E_updn_ctr, all_E_updn_end_ctr], [[all_E_up_ctr, all_E_up_end_ctr], [all_E_dn_ctr, all_E_dn_end_ctr]])
            self.create_secondary_top([all_F_updn_ctr, all_F_updn_end_ctr], [[all_F_up_ctr, all_F_up_end_ctr], [all_F_dn_ctr, all_F_dn_end_ctr]])
            self.create_secondary_top([all_E_updn_ctr, all_E_updn_end_ctr], [[all_E_up_ctr, all_E_up_end_ctr], [all_E_dn_ctr, all_E_dn_end_ctr]])

            # 约束输出骨骼
            cmds.parentConstraint(all_up_ctr[3],up_j[0])
            cmds.parentConstraint(all_up_end_ctr[3], up_j[1])
            cmds.parentConstraint(all_dn_ctr[3], dn_j[0])
            cmds.parentConstraint(all_dn_end_ctr[3], dn_j[1])

            cmds.parentConstraint(all_F_up_end_ctr[3], side_F_up_j[1])
            cmds.parentConstraint(all_F_dn_end_ctr[3], side_F_dn_j[1])
            cmds.parentConstraint(all_E_up_end_ctr[3], side_E_up_j[1])
            cmds.parentConstraint(all_E_dn_end_ctr[3], side_E_dn_j[1])

            # 清理层级结构
            top_ctr_grp = cmds.group(all_center_ctr[0], all_up_ctr[0], all_dn_ctr[0], all_F_updn_ctr[0], all_E_updn_ctr[0], n='Hole_top_ctrl_all_grp_' + str(top_num))
            middle_ctr_grp = cmds.group(up_grp, dn_grp, n='Hole_updn_all_grp_'+ str(top_num))
            out_ctr_grp = cmds.group(up_edge_grp, dn_edge_grp, n='Hole_updn_edge_ctrl_all_Grp_'+ str(top_num))

            all_ctr_grp = cmds.group(top_ctr_grp, middle_ctr_grp, out_ctr_grp, n='Hole_all_ctrl_Grp_'+ str(top_num))
            cmds.parent(all_ctr_grp, top_grp)
            # 创建整体旋转约束
            cmds.parentConstraint(follow_obj, top_ctr_grp, mo=1)
            cmds.orientConstraint(follow_obj, middle_ctr_grp, mo=1)
            cmds.orientConstraint(follow_obj, out_ctr_grp, mo=1)
            cmds.scaleConstraint(follow_obj, top_ctr_grp, mo=1)
            cmds.scaleConstraint(follow_obj, middle_ctr_grp, mo=1)
            cmds.scaleConstraint(follow_obj, out_ctr_grp, mo=1)
            cmds.parentConstraint(all_center_ctr[2], all_up_ctr[0], mo=1)
            cmds.parentConstraint(all_center_ctr[2], all_dn_ctr[0], mo=1)
            # 创建底层显示影藏属性
            cmds.addAttr(all_center_ctr[2], ln="end_ctr", at='bool')
            cmds.setAttr((all_center_ctr[2] + '.end_ctr'), e=1, keyable=1)
            cmds.connectAttr((all_center_ctr[2] + '.end_ctr'), (out_ctr_grp + '.visibility'))
            # 创建中间控制器按比例约束
            follow_joint_parentConstraint = cmds.parentConstraint(follow_joint, all_center_ctr[0], mo=1)
            cmds.parentConstraint(follow_obj, all_center_ctr[0], mo=1)
            cmds.addAttr(all_center_ctr[2], ln="follow", at='double', min=0, max=10, dv=1)
            cmds.setAttr((all_center_ctr[2] + '.follow'), e=1, keyable=1)
            plusMinusAverage = cmds.createNode('plusMinusAverage')
            cmds.setAttr(plusMinusAverage+'.operation', 2)
            cmds.setAttr(plusMinusAverage+'.input1D[0]', 10)
            cmds.connectAttr((all_center_ctr[2] + '.follow'), plusMinusAverage+'.input1D[1]')
            multiplyDivide = cmds.createNode('multiplyDivide')
            cmds.connectAttr((all_center_ctr[2] + '.follow'), multiplyDivide+'.input1X')
            cmds.connectAttr(plusMinusAverage+'.output1D', multiplyDivide+'.input1Y')
            cmds.setAttr(multiplyDivide+'.input2X', 0.1)
            cmds.setAttr(multiplyDivide+'.input2Y', 0.1)
            cmds.connectAttr(multiplyDivide+'.outputX', follow_joint_parentConstraint[0]+'.'+follow_joint+'W0')
            cmds.connectAttr(multiplyDivide+'.outputY', follow_joint_parentConstraint[0]+'.'+follow_obj+'W1')
            # 创建总的缩放
            cmds.scaleConstraint(follow_joint, all_center_ctr[0])
        else:
            cmds.warning('请加载骨骼、跟随对象，创建上下洞边缘。')

    # 按先后选择的主控制器创建拉链效果，且创建新输出骨骼
    @Withdraw
    def create_new_output_bone(self):
        sel = cmds.ls(sl=1)
        # 创建输出骨骼，并且创建约束
        f_top_num = sel[0].split('_')[-1]
        f_joint_up = cmds.ls('Hole_up_edge_J_' + f_top_num + '_*')
        f_joint_dn = cmds.ls('Hole_dn_edge_J_' + f_top_num + '_*')
        e_top_num = sel[1].split('_')[-1]
        e_joint_up = cmds.ls('Hole_up_edge_J_' + e_top_num + '_*')
        e_joint_dn = cmds.ls('Hole_dn_edge_J_' + e_top_num + '_*')

        # 添加属性
        cmds.addAttr(sel[1], ln='up_follow', at='double', dv=100)
        cmds.setAttr((sel[1] + '.up_follow'), e=1, keyable=1)
        cmds.addAttr(sel[1], ln='dn_follow', at='double', dv=100)
        cmds.setAttr((sel[1] + '.dn_follow'), e=1, keyable=1)

        cmds.addAttr(sel[1], ln='up_range', at='double', dv=1)
        cmds.setAttr((sel[1] + '.up_range'), e=1, keyable=1)
        cmds.addAttr(sel[1], ln='dn_range', at='double', dv=1)
        cmds.setAttr((sel[1] + '.dn_range'), e=1, keyable=1)

        skin_up_j = []
        # skin_up_j_parentConstraint = []
        skin_dn_j = []
        # skin_dn_j_parentConstraint = []
        for i in range(len(f_joint_up)):
            cmds.select(cl=1)
            joint = cmds.joint(n='Hole_up_edge_J_' + f_top_num + 'and' + e_top_num + '_' + str(i))
            skin_up_j.append(joint)
            cmds.addAttr(joint, ln='offset', at='double', dv=i)
            cmds.setAttr((joint + '.offset'), e=1, keyable=1)
            parentConstraint = cmds.parentConstraint(f_joint_up[i], joint)
            # print(parentConstraint)
            cmds.parentConstraint(e_joint_up[i], joint)

            # # 创建驱动节点
            plusMinusAverage = cmds.shadingNode('plusMinusAverage', asUtility=1)
            cmds.connectAttr((sel[1] + '.up_follow'), plusMinusAverage+'.input1D[0]')
            cmds.setAttr(plusMinusAverage+'.input1D[1]', 10*i)

            multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
            cmds.connectAttr(plusMinusAverage+'.output1D', multiplyDivide+'.input1X')
            cmds.connectAttr((sel[1] + '.up_range'), multiplyDivide+'.input2X')

            cmds.setDrivenKeyframe((parentConstraint[0]+'.'+f_joint_up[i]+'W0'),
                                   currentDriver=(multiplyDivide + '.outputX'), dv=0, v=0)
            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + f_joint_up[i] + 'W0'),
                                   currentDriver=(multiplyDivide + '.outputX'), dv=10*len(f_joint_up), v=1)

            cmds.connectAttr(plusMinusAverage + '.output1D', multiplyDivide + '.input1Y')
            cmds.connectAttr((sel[1] + '.up_range'), multiplyDivide + '.input2Y')
            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + e_joint_up[i] + 'W1'),
                                   currentDriver=(multiplyDivide + '.outputY'), dv=10*len(f_joint_up), v=0)
            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + e_joint_up[i] + 'W1'),
                                   currentDriver=(multiplyDivide + '.outputY'), dv=0, v=1)
        for i in range(len(f_joint_dn)):
            cmds.select(cl=1)
            joint = cmds.joint(n='Hole_up_edge_J_' + f_top_num + 'and' + e_top_num + '_' + str(i))
            skin_dn_j.append(joint)
            cmds.addAttr(joint, ln='offset', at='double', dv=i)
            cmds.setAttr((joint + '.offset'), e=1, keyable=1)
            parentConstraint = cmds.parentConstraint(f_joint_dn[i], joint)
            # print(parentConstraint)
            cmds.parentConstraint(e_joint_dn[i], joint)

            # # 创建驱动节点
            plusMinusAverage = cmds.shadingNode('plusMinusAverage', asUtility=1)
            cmds.connectAttr((sel[1] + '.dn_follow'), plusMinusAverage + '.input1D[0]')
            cmds.setAttr(plusMinusAverage + '.input1D[1]', 10 * i)

            multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
            cmds.connectAttr(plusMinusAverage + '.output1D', multiplyDivide + '.input1X')
            cmds.connectAttr((sel[1] + '.dn_range'), multiplyDivide + '.input2X')

            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + f_joint_dn[i] + 'W0'),
                                   currentDriver=(multiplyDivide + '.outputX'), dv=0, v=0)
            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + f_joint_dn[i] + 'W0'),
                                   currentDriver=(multiplyDivide + '.outputX'), dv=10 * len(f_joint_dn), v=1)

            cmds.connectAttr(plusMinusAverage + '.output1D', multiplyDivide + '.input1Y')
            cmds.connectAttr((sel[1] + '.dn_range'), multiplyDivide + '.input2Y')
            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + e_joint_dn[i] + 'W1'),
                                   currentDriver=(multiplyDivide + '.outputY'), dv=10 * len(f_joint_dn), v=0)
            cmds.setDrivenKeyframe((parentConstraint[0] + '.' + e_joint_dn[i] + 'W1'),
                                   currentDriver=(multiplyDivide + '.outputY'), dv=0, v=1)

        skin_grp = cmds.group(skin_up_j, skin_dn_j, n='Hole_up_edge_J_' + f_top_num + 'and' + e_top_num + '_all_skin_joint')
        follow_obj = cmds.getAttr('Hole_all_Grp_' + f_top_num + '.follow_obj')
        cmds.scaleConstraint(follow_obj, skin_grp)



        # 在首选的输出骨骼上创建滑动权重

    # 选择总控制器为其以及子对象创建驱动组并选择，如果已有驱动组则选择驱动组
    @Withdraw
    def create_driver_grp_and_select(self):
        sel = cmds.ls(sl=1)
        top_num = sel[0].split('_')[-1]
        ctrl = ['Hole_up_Top_ctrl_C_' + top_num,
                'Hole_up_end_Top_ctrl_C_' + top_num,
                'Hole_up_ctrl_C_' + top_num + '_*',
                'Hole_up_edge_ctrl_C_' + top_num + '_*',

                'Hole_dn_Top_ctrl_C_' + top_num,
                'Hole_dn_end_Top_ctrl_C_' + top_num,
                'Hole_dn_ctrl_C_' + top_num + '_*',
                'Hole_dn_edge_ctrl_C_' + top_num + '_*',

                'Hole_F_updn_Top_ctrl_C_' + top_num,
                'Hole_F_up_Top_ctrl_C_' + top_num,
                'Hole_F_dn_Top_ctrl_C_' + top_num,
                'Hole_F_updn_end_Top_ctrl_C_' + top_num,
                'Hole_F_up_end_ctrl_C_' + top_num,
                'Hole_F_dn_end_Top_ctrl_C_' + top_num,

                'Hole_E_updn_Top_ctrl_C_' + top_num,
                'Hole_E_up_Top_ctrl_C_' + top_num,
                'Hole_E_dn_Top_ctrl_C_' + top_num,
                'Hole_E_updn_end_Top_ctrl_C_' + top_num,
                'Hole_E_up_end_ctrl_C_' + top_num,
                'Hole_E_dn_end_Top_ctrl_C_' + top_num,
                ]
        cmds.select(ctrl)
        sel = cmds.ls(sl=1)
        all_drver_grp = []
        for s in sel:
            if not cmds.objExists(s + '_drver_grp'):
                child = cmds.listRelatives(s, p=1)
                parent = cmds.listRelatives(child, p=1)
                drver_grp = cmds.group(n=s + '_drver_grp', em=1)
                cmds.delete(cmds.parentConstraint(parent[0], drver_grp))
                cmds.parent(drver_grp, parent)
                cmds.parent(child, drver_grp)
            all_drver_grp.append(s + '_drver_grp')
        cmds.select(all_drver_grp)

    # 删除驱动组
    @Withdraw
    def delete_driver_grp(self):
        sel = cmds.ls(sl=1)
        top_num = sel[0].split('_')[-1]
        ctrl = ['Hole_up_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_up_end_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_up_ctrl_C_' + top_num + '_*' + '_drver_grp',
                'Hole_up_edge_ctrl_C_' + top_num + '_*' + '_drver_grp',

                'Hole_dn_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_dn_end_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_dn_ctrl_C_' + top_num + '_*' + '_drver_grp',
                'Hole_dn_edge_ctrl_C_' + top_num + '_*' + '_drver_grp',

                'Hole_F_updn_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_F_up_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_F_dn_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_F_updn_end_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_F_up_end_ctrl_C_' + top_num + '_drver_grp',
                'Hole_F_dn_end_Top_ctrl_C_' + top_num + '_drver_grp',

                'Hole_E_updn_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_E_up_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_E_dn_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_E_updn_end_Top_ctrl_C_' + top_num + '_drver_grp',
                'Hole_E_up_end_ctrl_C_' + top_num + '_drver_grp',
                'Hole_E_dn_end_Top_ctrl_C_' + top_num + '_drver_grp',
                ]
        cmds.select(ctrl)
        sel = cmds.ls(sl=1)
        for s in sel:
            if cmds.objExists(s):
                child = cmds.listRelatives(s, c=1)
                parent = cmds.listRelatives(s, p=1)
                cmds.parent(child, parent)
                cmds.delete(s)

    # 创建显示隐藏属性，并父化且链接根骨骼位移
    def create_secondary(self, parent, child):
        # 创建次级联动
        cmds.addAttr(parent[1][2], ln="secondary", at='bool')
        cmds.setAttr((parent[1][2] + '.secondary'), e=1, keyable=1)
        for c in child:
            loc = cmds.spaceLocator(n=c[1][0]+'_loc')[0]
            cmds.setAttr(loc+'.visibility', 0)
            grp = cmds.group(n=c[1][0]+'_loc_grp')
            cmds.parent(grp, c[0][0])
            cmds.delete(cmds.parentConstraint(c[0][0], grp))
            cmds.delete(cmds.parentConstraint(c[1][0], loc))
            cmds.connectAttr(loc + '.translate', c[1][0] + '.translate')
            cmds.connectAttr(loc + '.rotate', c[1][0] + '.rotate')
            cmds.parentConstraint(parent[1][2], loc)
            shape = cmds.listRelatives(c[1][2], s=1)[0]
            cmds.connectAttr(parent[1][2] + '.secondary', shape + '.visibility')

    # 创建显示隐藏属性，并父化且链接根骨骼位移
    def create_secondary_top(self, parent, child):
        cmds.addAttr(parent[0][2], ln="secondary", at='bool')
        cmds.setAttr((parent[0][2] + '.secondary'), e=1, keyable=1)
        for c in child:
            shape = cmds.listRelatives(c[0][2], s=1)[0]
            # print(shape)
            cmds.connectAttr(parent[0][2] + '.secondary', shape + '.visibility')

    # 创建顶层控制器
    def create_top_controller(self,base_name, addname, top_num, ctr_type, scale, soure_obj, rote_axial, frequency, tx_mag_list, colour):
        # 创建上下控制器
        grp1, grp2, curve, joint = self.create_controller(base_name, addname, top_num, ctr_type, scale)
        cmds.delete(cmds.parentConstraint(soure_obj[0], grp1))
        cmds.select(curve)
        for i in range(frequency):
            self.controller.rotation_controller(rote_axial)
        tx = cmds.getAttr(soure_obj[1] + '.translateX')
        cmds.select(curve)
        self.controller.modify_vontroller_shape('translate', tx * tx_mag_list[0], tx * tx_mag_list[1], tx * tx_mag_list[2])
        self.curve.change_curve_color('Index', [curve], [0, 0, 0], colour)
        return [grp1, grp2, curve, joint]

    # 获取对象离样条最近的点
    def get_nearest_point(self, curve, target_obj):
        # print(curve,target_obj)
        target_obj_pos = cmds.xform(target_obj, query=True, translation=True, worldSpace=True)
        # print(target_obj_pos)
        # print(target_obj_pos)
        closest_point = None
        min_distance = float('inf') # 正无穷大
        # 获取所有控制点
        control_points = cmds.ls(curve[0] + '.cv[*]', flatten=True)
        for cv in control_points:
            pos = cmds.xform(cv, query=True, translation=True, worldSpace=True)
            # print(pos)
            distance = math.dist(pos, target_obj_pos)
            if distance < min_distance:
                min_distance = distance
                closest_point = cv
        return closest_point

    # 根据点创建骨骼
    def create_bone_by_point(self, top_num, follow_joint, point, name, surface, attachment):
        ## 创建上边缘骨骼
        cmds.select(cl=1)
        joint = cmds.joint(n=name + str(top_num))
        end_joint = cmds.joint(n=name + 'End_' + str(top_num))
        cmds.delete(cmds.pointConstraint(follow_joint, joint))
        up_cluster = cmds.cluster(point)
        cmds.delete(cmds.pointConstraint(up_cluster, end_joint))
        cmds.delete(up_cluster)
        if attachment == 1:
            parentConstraint, grp = self.other_library.attachment_surface(surface, end_joint, end_joint, 1)
            cmds.delete(parentConstraint, grp)
        cmds.joint(joint, e=1, zso=1, oj='xyz', sao='yup')
        return [joint,end_joint]

    # 创建默认权重列表
    def create_normal_weight_list(self):
        # 基础权重列表
        base_skin_list = [[0.0, 0.0, 1.0],
                          [0.34, 0.0, 0.66],
                          [0.6, 0.0, 0.4],
                          [0.78, 0.0, 0.22],
                          [0.94, 0.0, 0.06],
                          [1.0, 0.0, 0.0],
                          [1.0, 0.0, 0.0]]
        reverse_List = []
        for i in range(-2, -7, -1):
            ls_list = base_skin_list[i]
            reverse_List.append([ls_list[0], ls_list[2], ls_list[1]])
        for list in reverse_List:
            base_skin_list.append(list)
        ## 重复权重
        skin_list = []
        for list in base_skin_list:
            skin_list.append(list)
            skin_list.append(list)
        return skin_list

    # 创建单向边缘
    def create_up_down_hole(self, top_num, follow_joint, add_name, surface, toward_j, center_j, side_joint, skin_list):
        # # 复制边缘骨骼总控制器
        # 复制边缘骨骼
        side_F_j_all = cmds.duplicate(side_joint[0], rr=1, renameChildren=1)
        side_F_j_all_child = cmds.listRelatives(side_F_j_all, c=1, type='joint')
        side_F_j = cmds.rename(side_F_j_all[0], 'sd_F' + add_name + str(top_num))
        side_F_end_j = cmds.rename(side_F_j_all_child, 'sd_F' + add_name + 'End_' + str(top_num))
        # 复制边缘骨骼
        side_E_j_all = cmds.duplicate(side_joint[1], rr=1, renameChildren=1)
        side_E_j_all_child = cmds.listRelatives(side_E_j_all, c=1, type='joint')
        side_E_j = cmds.rename(side_E_j_all[0], 'sd_E' + add_name + str(top_num))
        side_E_end_j = cmds.rename(side_E_j_all_child, 'sd_E' + add_name + 'End_' + str(top_num))

        # 导入默认权重
        ## 蒙皮side_F_end_up_j
        skin = cmds.skinCluster(toward_j[1], side_F_end_j, side_E_end_j, surface, tsb=1)
        surface_shape = cmds.listRelatives(surface, s=True)
        surface_point = cmds.ls(surface_shape[0] + '.cv[*][*]', fl=1)

        # print(skin_list)
        for point, skin_num in zip(surface_point, skin_list):
            cmds.skinPercent(skin[0], point,
                             tv=[(toward_j[1], skin_num[0]), (side_E_end_j,skin_num[1]), (side_F_end_j,  skin_num[2])])
        return [side_F_j,side_F_end_j], [side_E_j,side_E_end_j]

    # 创建附着控制器
    def create_attach_controller(self, top_num, surface, add_name, up_j, side_F_updn_j, side_E_updn_j, center_j, scale, reversal):
        # 创建附着的控制器，首尾各俩独立的，中间三个贝塞尔控制器
        shape = cmds.listRelatives(surface, s=True)
        surface_point = cmds.ls(shape[0] + '.cv[*][0]', fl=1)
        # 复制曲面
        copy_surface = cmds.duplicate(surface, rr=1, renameChildren=1)
        copy_surface = cmds.rename(copy_surface, 'Hole_' + add_name + '_copy_surface_' + str(top_num))

        all_grp = []
        all_cur = []
        all_joint = []
        all_loc = []
        first_loc = []
        # 为每个点创建控制器和附着定位器
        for i in range(len(surface_point)):
            cluster = cmds.cluster(surface_point[i])
            # curve = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)
            rotate = [0,0,0]
            if i == 0 or i == len(surface_point) - 1:
                self.curve.create_curve(self.library_path + '\curve_library', '馒头')
                scale_now = scale * 10
                rotate = [0, 90, 0]
                if reversal == 1:
                    rotate = [0, 90, 180]
            else:
                self.curve.create_curve(self.library_path + '\curve_library','A圆')
                scale_now = scale * 1
            curve = cmds.ls(sl=1)
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 17)
            curve = cmds.rename(curve, 'Hole_'+add_name+'_ctrl_C_' + str(top_num) + '_' + str(i))
            all_cur.append(curve)
            joint = cmds.joint(n='Hole_'+add_name+'_J_' + str(top_num) + '_' + str(i))
            cmds.setAttr(joint + '.visibility', 0)
            all_joint.append(joint)
            # cmds.parent(joint, curve)
            cmds.select(curve)
            self.controller.modify_vontroller_shape('scale', scale_now, scale_now, scale_now)
            self.controller.modify_vontroller_shape('rotate', rotate[0], rotate[1], rotate[2])
            grp2 = cmds.group(n='Hole_'+add_name+'_ctrl_Grp2_' + str(top_num) + '_' + str(i), em=1)
            grp1 = cmds.group(n='Hole_'+add_name+'_ctrl_Grp1_' + str(top_num) + '_' + str(i))
            cmds.parent(curve, grp2)
            cmds.delete(cmds.pointConstraint(cluster, grp1))
            cmds.delete(cmds.orientConstraint(center_j[0], grp1))
            loc = cmds.spaceLocator(n='Hole_'+add_name+'_loc_' + str(top_num) + '_' + str(i))
            cmds.setAttr(loc[0] + '.visibility', 0)
            cmds.delete(cmds.parentConstraint(cluster, loc, w=1))
            cmds.delete(cmds.orientConstraint(center_j[0], loc))
            # parentConstraint, grp = self.other_library.attachment_surface(surface, loc[0], loc[0], 1)
            parent, all_follicle, parentConstraint = self.other_library.follicle_constraint(surface, [loc[0]], True)
            print(parent)

            cmds.delete(parentConstraint)
            # cmds.delete(cmds.orientConstraint(center_j[0], loc))
            # cmds.pointConstraint(grp, loc, mo=1)
            cmds.pointConstraint(all_follicle, loc)
            orientConstraint = cmds.orientConstraint(all_follicle, loc, mo=1)

            # cmds.addAttr(curve, ln='orient', at='bool')
            # cmds.setAttr(curve + '.orient', e=1, keyable=True)
            # cmds.connectAttr(curve + '.orient', orientConstraint[0] + '.' + grp + 'W0')
            first_loc.append(all_follicle[0])
            all_grp.append(grp1)
            all_loc.append(loc)
            cmds.delete(cluster)
        cmds.parent(parent, self.top_name + str(top_num))
        cmds.setAttr(parent + '.visibility', 0)
        # cmds.select('aaa')
        # 按固定顺序父化定位器和控制器组
        cmds.addAttr(all_cur[3],ln="secondary_controller",  at='bool')
        cmds.setAttr(all_cur[3]+'.secondary_controller', e=1, keyable=True)
        self.curve.change_curve_color('Index', [all_cur[3]], [0, 0, 0], 13)
        cmds.addAttr(all_cur[6], ln="secondary_controller", at='bool')
        cmds.setAttr(all_cur[6] + '.secondary_controller', e=1, keyable=True)
        self.curve.change_curve_color('Index', [all_cur[6]], [0, 0, 0], 13)
        cmds.addAttr(all_cur[9], ln="secondary_controller", at='bool')
        cmds.setAttr(all_cur[9] + '.secondary_controller', e=1, keyable=True)
        self.curve.change_curve_color('Index', [all_cur[9]], [0, 0, 0], 13)

        for i in range(len(all_loc)):
            if i < 2 or i > len(all_loc)-3:
                cmds.parent(all_grp[i], all_loc[i])
            if i in [2, 4]:
                cmds.parent(all_grp[i], all_cur[3])
                cmds.parent(all_loc[i], all_loc[3])
                cmds.connectAttr(all_cur[3] + '.secondary_controller',all_grp[i] + '.visibility')
            if i in [5, 7]:
                cmds.parent(all_grp[i], all_cur[6])
                cmds.parent(all_loc[i], all_loc[6])
                cmds.connectAttr(all_cur[6] + '.secondary_controller', all_grp[i] + '.visibility')
            if i in [8, 10]:
                cmds.parent(all_grp[i], all_cur[9])
                cmds.parent(all_loc[i], all_loc[9])
                cmds.connectAttr(all_cur[9] + '.secondary_controller', all_grp[i] + '.visibility')

        for i in range(len(surface_point)):
            orientConstraint = cmds.orientConstraint(first_loc[i], all_loc[i], mo=1)
            cmds.addAttr(all_cur[i], ln='orient', at='bool')
            cmds.setAttr(all_cur[i] + '.orient', e=1, keyable=True)
            cmds.connectAttr(all_cur[i] + '.orient', orientConstraint[0] + '.' + first_loc[i] + 'W0')

        # cmds.parent(all_grp[3], all_loc[3])
        # cmds.parent(all_grp[6], all_loc[6])
        # cmds.parent(all_grp[9], all_loc[9])
        for i in range(len(all_loc)):
            cmds.connectAttr(all_loc[i][0]+'.translate', all_grp[i]+'.translate')
            cmds.connectAttr(all_loc[i][0] + '.rotate', all_grp[i] + '.rotate')
        grp = cmds.group(all_loc[0], all_loc[1], all_loc[3], all_loc[6], all_loc[9], all_loc[11], all_loc[12],
                   all_grp[0], all_grp[1], all_grp[3], all_grp[6], all_grp[9], all_grp[11], all_grp[12],
                   center_j[0], n='Hole_'+add_name+'_all_grp_' + str(top_num))

        ## 蒙皮
        skin = cmds.skinCluster(all_joint, copy_surface, tsb=1)
        copy_surface_shape = cmds.listRelatives(copy_surface, s=True)
        copy_surface_point = cmds.ls(copy_surface_shape[0] + '.cv[*][*]', fl=1)
        # print(copy_surface_point)
        # print(skin_list)
        skin_list = []
        for i in range(len(all_joint)):
            skin_list.append(0.0)
        # print(skin_list)
        for i in range(len(all_joint)):
            new_skin = []
            for j in range(len(skin_list)):
                if j == i:
                    new_skin.append(1.0)
                else:
                    new_skin.append(skin_list[j])
            all_list = []
            for j in range(len(all_joint)):
                all_list.append((all_joint[j], new_skin[j]))
            cmds.skinPercent(skin[0], copy_surface_point[i*2], tv=all_list)
            cmds.skinPercent(skin[0], copy_surface_point[i*2+1], tv=all_list)
        return copy_surface, grp



        ## 创建纯附着控制器

    # 获取样条点并创建附着曲面的控制器和骨骼
    def create_out_ctr(self, top_num, add_name, curve, surface, center_j, scale, reversal):
        name = 'Hole_'+add_name+'_edge_'
        curve_point = cmds.ls(curve + '.cv[*]', fl=1)
        all_grp = cmds.group(em=1,n=name+'ctrl_all_Grp_' + str(top_num))
        for i in range(len(curve_point)):
            cluster = cmds.cluster(curve_point[i])
            rotate = [0, 0, 0]
            if i == 0 or i == len(curve_point) - 1:
                self.curve.create_curve(self.library_path + '\curve_library', '馒头')
                scale_now = scale * 10
                rotate = [0, 90, 0]
                if reversal == 1:
                    rotate = [0, 90, 180]
            else:
                self.curve.create_curve(self.library_path + '\curve_library', 'A圆')
                scale_now = scale * 1
            curve = cmds.ls(sl=1)
            self.curve.change_curve_color('Index', curve, [0, 0, 0], 18)
            curve = cmds.rename(curve, name + 'ctrl_C_' + str(top_num) + '_' + str(i))
            # all_cur.append(curve)
            joint = cmds.joint(n=name + 'J_' + str(top_num) + '_' + str(i))
            # all_joint.append(joint)
            # cmds.parent(joint, curve)
            cmds.select(curve)
            self.controller.modify_vontroller_shape('scale', scale_now, scale_now, scale_now)
            self.controller.modify_vontroller_shape('rotate', rotate[0], rotate[1], rotate[2])
            grp2 = cmds.group(n=name + 'ctrl_Grp2_' + str(top_num) + '_' + str(i))
            grp1 = cmds.group(n=name + 'ctrl_Grp1_' + str(top_num) + '_' + str(i))
            cmds.delete(cmds.pointConstraint(cluster, grp1))
            cmds.delete(cmds.orientConstraint(center_j[0], grp1))
            # cmds.select(cl=1)
            # parentConstraint, grp = self.other_library.attachment_surface(surface, grp1, grp1, 1)
            parent, all_follicle, parentConstraint = self.other_library.follicle_constraint(surface, [grp1], True)

            # cmds.setAttr(grp + '.visibility', 0)
            cmds.delete(parentConstraint)
            # cmds.pointConstraint(grp, grp1)
            # orientConstraint = cmds.orientConstraint(grp, grp1, mo=1)
            cmds.pointConstraint(all_follicle, grp1)
            orientConstraint = cmds.orientConstraint(all_follicle, grp1, mo=1)

            cmds.addAttr(curve, ln='orient', at='bool')
            cmds.setAttr(curve + '.orient', e=1, keyable=True)
            # cmds.connectAttr(curve + '.orient', orientConstraint[0] + '.' + grp + 'W0')
            cmds.connectAttr(curve + '.orient', orientConstraint[0] + '.' + all_follicle[0] + 'W0')
            cmds.delete(cluster)
            cmds.parent(grp1, all_grp)
        cmds.parent(parent, self.top_name + str(top_num))
        cmds.setAttr(parent + '.visibility', 0)
        return all_grp

    # 创建控制器
    def create_controller(self, name, add_name, top_num,  curve_type, scale):
        self.curve.create_curve(self.library_path + '\curve_library', curve_type)
        curve = cmds.ls(sl=1)
        self.curve.change_curve_color('Index', curve, [0, 0, 0], 17)
        curve = cmds.rename(curve, name + '_ctrl_C_' + str(top_num) + add_name)
        joint = cmds.joint(n=name + '_J_' + str(top_num) + add_name)
        cmds.setAttr(joint + '.visibility', 0)
        # cmds.parent(joint, curve)
        cmds.select(curve)
        self.controller.modify_vontroller_shape('scale', scale, scale, scale)
        grp2 = cmds.group(n=name + '_ctrl_Grp2_' + str(top_num) + add_name, em=1)
        grp1 = cmds.group(n=name + '_ctrl_Grp1_' + str(top_num) + add_name)
        cmds.parent(curve, grp2)
        return grp1, grp2, curve, joint

    # 选择曲面和对应控制器创建附着
    @Withdraw
    def create_attach(self):
        sel = cmds.ls(sl=1)
        # 获取选择的控制器最后的数值
        top_num = sel[0].split('_')[-1]
        # print(top_num)
        # 获取包围盒大小，设定控制器缩放值
        top_grp = self.top_name + str(top_num)
        box_min = cmds.getAttr(top_grp + '.boundingBoxMin')[0]
        box_max = cmds.getAttr(top_grp + '.boundingBoxMax')[0]
        base_num = (box_max[0] - box_min[0] + box_max[1] - box_min[1] + box_max[2] - box_min[2]) / 3
        # print(base_num)
        scale = base_num / 9.39318231179574 * 0.6
        # 创建控制器位置的附着控制器
        attach_cur = self.curve.create_curve(self.library_path + '\curve_library','球')
        cmds.rename(attach_cur, sel[0] + '_attach_curve')
        attach_cur = cmds.ls(sl=1)
        self.curve.change_curve_color('Index', attach_cur, [0, 0, 0], 17)
        self.controller.modify_vontroller_shape('scale', scale, scale, scale)
        attach_loc_grp = cmds.group(n=sel[0] + '_attach_loc_grp')
        cmds.delete(cmds.parentConstraint(sel[0], attach_loc_grp))
        cmds.delete(cmds.geometryConstraint(sel[1], attach_loc_grp))
        cmds.geometryConstraint(sel[1], attach_cur)
        # 创建法线约束旋转控制器
        normal_cur = self.curve.create_curve(self.library_path + '\curve_library', '球')
        cmds.rename(normal_cur, sel[0] + '_normal_cur_curve')
        normal_cur = cmds.ls(sl=1)
        self.curve.change_curve_color('Index', normal_cur, [0, 0, 0], 18)
        self.controller.modify_vontroller_shape('scale', scale*0.8, scale*0.8, scale*0.8)
        normal_cur_grp = cmds.group(n=sel[0] + '_normal_cur_grp')
        cmds.delete(cmds.parentConstraint(sel[0], normal_cur_grp))
        cmds.parent(normal_cur_grp, attach_cur)
        cmds.normalConstraint(sel[1], normal_cur_grp, weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType='vector', worldUpVector=(0, 1, 0))

        # 创建数值链接组链接
        connect_loc = cmds.spaceLocator(n=sel[0] + '_attach_connect_loc')
        cmds.setAttr(connect_loc[0] + '.visibility', 0)
        parent_1 = cmds.listRelatives(sel[0], p=1)
        parent_2 = cmds.listRelatives(parent_1, p=1)
        cmds.delete(cmds.parentConstraint(parent_1, connect_loc))
        cmds.parent(connect_loc,parent_2)
        connect_grp = cmds.group(n=sel[0] + '_attach_connect_grp', em=1)
        cmds.delete(cmds.parentConstraint(parent_1, connect_grp))
        cmds.parent(connect_grp, parent_2)
        cmds.parent(parent_1, connect_grp)
        cmds.parentConstraint(normal_cur, connect_loc, mo=1)
        cmds.connectAttr(connect_loc[0] + '.translate', connect_grp + '.translate')
        cmds.connectAttr(connect_loc[0] + '.rotate', connect_grp + '.rotate')
        cmds.connectAttr(connect_loc[0] + '.scale', connect_grp + '.scale')
        # 父化
        cmds.parent(attach_loc_grp, top_grp)
        follow_obj = cmds.getAttr(top_grp + '.follow_obj')
        cmds.parentConstraint(follow_obj, attach_loc_grp, mo=1)
        cmds.scaleConstraint(follow_obj, attach_loc_grp, mo=1)
        cmds.parentConstraint(follow_obj, sel[1], mo=1)
        cmds.scaleConstraint(follow_obj, sel[1], mo=1)
        cmds.select(attach_cur)
        # 创建父控制器链接
        parent = cmds.listRelatives(parent_2, p=1)
        parent_3 = cmds.listRelatives(parent, p=1)
        parent_3 = cmds.listRelatives(parent_3, p=1)
        connect_loc = cmds.spaceLocator(n=sel[0] + '_attach_connect_loc1')
        cmds.setAttr(connect_loc[0] + '.visibility', 0)
        grp = cmds.group(connect_loc, n=sel[0] + '_attach_connect_loc1_grp')
        parent_connect_grp = cmds.group(n=sel[0] + '_attach_connect_parent_grp', em=1)
        cmds.delete(cmds.parentConstraint(sel[0], parent_connect_grp))
        cmds.parent(parent_connect_grp, parent_2)
        cmds.parent(connect_grp, parent_connect_grp)
        cmds.delete(cmds.parentConstraint(sel[0], grp))
        cmds.parentConstraint(parent, connect_loc, mo=1)
        cmds.parent(grp, parent_3)
        cmds.connectAttr(connect_loc[0] + '.translate', parent_connect_grp + '.translate')
        cmds.connectAttr(connect_loc[0] + '.rotate', parent_connect_grp + '.rotate')
        cmds.connectAttr(connect_loc[0] + '.scale', parent_connect_grp + '.scale')

    # 选择附着控制器删除并清理关联
    @Withdraw
    def delete_attach(self):
        sel = cmds.ls(sl=1)
        # 获取原选择控制器名称
        sour_cur = sel[0][:-13]
        parent = cmds.listRelatives(sel[0], p=1)
        cmds.delete(parent)
        cmds.delete(sour_cur + '_attach_connect_loc')
        cmds.delete(sour_cur + '_attach_connect_loc1_grp')
        grp = sour_cur + '_attach_connect_grp'
        parent = cmds.listRelatives(grp, p=1)
        child = cmds.listRelatives(grp, c=1)
        cmds.parent(child, parent)
        cmds.delete(grp)
        grp = sour_cur + '_attach_connect_parent_grp'
        parent = cmds.listRelatives(grp, p=1)
        child = cmds.listRelatives(grp, c=1)
        cmds.parent(child, parent)
        cmds.delete(grp)


window = Window()
if __name__ == '__main__':
    window.show()


# 添加骨骼属性代理(代码里给此属性k帧)
# cmds.addAttr('joint7', proxy=('joint8.translateX'), longName='txxx')
# sel = cmds.ls(sl=1)
# print(len(sel))