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

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import maya_common
importlib.reload(maya_common)
from maya_common import *

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
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('改驱动加bs(Maya' + self.maya_version + ')')

        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version

        # 开启必要插件
        pluginInfo = cmds.pluginInfo(listPlugins=True, q=True)
        if not 'invertShape' in pluginInfo:
                cmds.loadPlugin('invertShape')


        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    def create_widgets(self):
        # 第一行
        self.Label_1 = QtWidgets.QLabel()
        self.Label_1.setText('先启动ADV')
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.line_edit_1.setText('face_base')
        self.button_1 = QtWidgets.QPushButton('表情bs组')

        self.line_edit_2 = QtWidgets.QLineEdit()
        self.line_edit_2.setText('face_base|face')
        self.button_2 = QtWidgets.QPushButton('加载需变形部分')

        self.line_edit_3 = QtWidgets.QLineEdit()
        self.line_edit_3.setText('ChinCrease_M,Lip_L,Lip_R,lowerLip_M,upperLip_M,LipRegion_M,SmileBulge_L,SmilePull_L,lowerLipA_L,cornerLip_L,upperLipC_L,upperLipB_L,lowerLip_L,upperLip_L,lowerLipC_L,lowerLipB_L,upperLipA_L,SmileBulge_R,SmilePull_R,lowerLip_R,upperLip_R,lowerLipC_R,lowerLipB_R,lowerLipA_R,cornerLip_R,upperLipC_R,upperLipB_R,upperLipA_R,Jaw_M,NoseCorner_R,NoseUnder_M,NoseCorner_L,Tongue0_M, upperTeeth_M, lowerTeeth_M')
        self.button_5 = QtWidgets.QPushButton('加载需要做驱动的控制器')
        self.button_8 = QtWidgets.QPushButton('选择当前加载的控制器')

        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_10 = QtWidgets.QPushButton('创建bs(如果有请自行填写，层级移动到最底端)')

        self.button_6 = QtWidgets.QPushButton('创建无驱动效果驱动组')
        self.button_7 = QtWidgets.QPushButton('删除无驱动效果驱动组')

        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(['无', 'm_a', 'm_e', 'm_i', 'm_o', 'm_u', 'm_m', 'm_r', 'm_f'])
        self.button_3 = QtWidgets.QPushButton('按当前调整修改驱动')

        self.button_4 = QtWidgets.QPushButton('自动查询需要添加的bs进行bs')
        self.button_9 = QtWidgets.QPushButton('选择等待移动点模型和参考模型，点击后将移动源模型点到参考模型，如果是bs请打开bs编辑')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        main_layout.addWidget(self.Label_1)

        # 第一行
        h_Box_layout_1 = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.setSpacing(1)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.line_edit_1)
        h_Box_layout_3.addWidget(self.button_1)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_4)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_2)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_6)
        h_Box_layout_6.addWidget(self.line_edit_3)
        h_Box_layout_6.addWidget(self.button_5)
        h_Box_layout_6.addWidget(self.button_8)

        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_8)
        h_Box_layout_8.addWidget(self.line_edit_4)
        h_Box_layout_8.addWidget(self.button_10)


        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_7)
        h_Box_layout_7.addWidget(self.button_6)
        h_Box_layout_7.addWidget(self.button_7)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.comboBox_1)
        h_Box_layout_5.addWidget(self.button_3)


        main_layout.addWidget(self.button_4)
        main_layout.addWidget(self.button_9)

        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))
        self.comboBox_1.currentIndexChanged.connect(self.automatically_switch_display)
        self.button_3.clicked.connect(self.create_drver)
        self.button_4.clicked.connect(self.create_bs_driver)

        self.button_5.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))
        self.button_8.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit']))

        self.button_10.clicked.connect(self.create_bs_node)

        self.button_6.clicked.connect(self.create_normal_drver)
        self.button_7.clicked.connect(self.delete_normal_drver)

        self.button_9.clicked.connect(self.move_point_to_target)
        # asDsEdit Edit ctrlPhonemes_M aaa 0;
        # // Result: scriptEditorPanel1Window|scriptEditorPanel1|formLayout97|formLayout99|paneLayout2|cmdScrollFieldReporter1
        # asDsEditApply;

    # 除ADV控制器归零
    def controller_zeroing(self,name):
        if name == '无':
            for n in ['aaa', 'eh', 'iee', 'ohh', 'uuu', 'mbp', 'rrr', 'fff']:
                cmds.setAttr('ctrlPhonemes_M.' + n, 0)
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        controller = cmds.ls(sl=1)
        for c in controller:
            for a in ['tx','ty', 'tz','rx', 'ry', 'rz']:
                lock = cmds.getAttr(c + '.'+a,l=1)
                if lock == 0:
                    cmds.setAttr(c + '.'+a, 0)
            for a in ['sx', 'sy', 'sz']:
                lock = cmds.getAttr(c + '.'+a,l=1)
                if lock == 0:
                    cmds.setAttr(c + '.'+a, 1)

    # 自动切换显示
    def automatically_switch_display(self):
        cmds.undoInfo(ock=1)
        name = self.comboBox_1.currentText()
        print(name)
        for n, m in zip(['m_a', 'm_e', 'm_i', 'm_o', 'm_u', 'm_m', 'm_r', 'm_f'],
                        ['aaa', 'eh', 'iee', 'ohh', 'uuu', 'mbp', 'rrr', 'fff']):
            if n == name:
                #mel.eval('asGoToBuildPose faceSetup;')
                self.controller_zeroing('无')
                if cmds.objExists('ctrlPhonemes_M.' + m):
                    cmds.setAttr('ctrlPhonemes_M.' + m, 10)
                if cmds.objExists(n + ".visibility"):
                    cmds.setAttr(n + ".visibility", 1)
            else:
                cmds.setAttr(n + ".visibility", 0)
        if name == '无':
            #mel.eval('asGoToBuildPose faceSetup;')
            self.controller_zeroing('无')
            pass

        cmds.undoInfo(cck=1)
    # 自动切换显示
    def automatically_switch_edit_display(self):
        cmds.undoInfo(ock=1)
        name = self.comboBox_1.currentText()
        if name != '无':
            isEnabled = self.comboBox_1.isEnabled()
            if isEnabled == True:
                for n,m in zip(['m_a', 'm_e', 'm_i', 'm_o', 'm_u', 'm_m', 'm_r', 'm_f'],
                               ['aaa', 'eh', 'iee', 'ohh', 'uuu', 'mbp', 'rrr', 'fff']):
                    if n == name:
                        mel.eval('asDsEdit Edit ctrlPhonemes_M '+m+' 0;')
                self.comboBox_1.setEnabled(False)
                self.button_3.setText('正在编辑：'+name)
                self.button_3.setStyleSheet('color:rgb(0,0,0);background:rgb(0,255,0)')
                cmds.warning('开始编辑')
            else:
                #mel.eval('asDsEditApply;')
                self.controller_zeroing('无')
                for n,m in zip(['m_a', 'm_e', 'm_i', 'm_o', 'm_u', 'm_m', 'm_r', 'm_f'],
                               ['aaa', 'eh', 'iee', 'ohh', 'uuu', 'mbp', 'rrr', 'fff']):
                    if n == name:
                        if cmds.objExists('ctrlPhonemes_M.' + m):
                            cmds.setAttr('ctrlPhonemes_M.'+m, 10)
                self.comboBox_1.setEnabled(True)
                self.button_3.setText('开始修改')
                self.button_3.setStyleSheet('')
                cmds.warning('编辑完毕')
        else:
            cmds.warning('请先选择一个表情选项')

        cmds.undoInfo(cck=1)


    # 创建bs节点
    def create_bs_node(self):
        base_grp = self.line_edit_1.text()
        need_replace = self.line_edit_2.text()
        need_replace = need_replace.split(',')
        # need_replace = cmds.ls(need_replace, long=True)
        # 创建基础bs
        cmds.select(base_grp)
        copy = cmds.duplicate(rr=1)
        bs = cmds.blendShape(copy, base_grp, frontOfChain=1)
        cmds.delete(copy)
        print((bs))
        cmds.select(base_grp)
        cmds.SelectHierarchy()
        meshs = cmds.ls(sl=1, type='mesh')
        for mesh in meshs:
            deform = cmds.listHistory(mesh, pruneDagObjects=True, interestLevel=True)
            deform = cmds.ls(deform, type='geometryFilter')  # 过滤出变形器节点
            print(deform)
            cmds.reorderDeformers(deform[-1], bs[0], mesh)
            pass
        self.line_edit_4.setText(bs[0])

    # 自动查询并添加bs
    def create_bs_driver(self):
        cmds.undoInfo(ock=1)
        base_grp = self.line_edit_1.text()
        need_replace = self.line_edit_2.text()
        need_replace = need_replace.split(',')
        # need_replace = cmds.ls(need_replace, long=True)
        # 创建基础bs
        # cmds.select(base_grp)
        # copy = cmds.duplicate(rr=1)
        # bs = cmds.blendShape(copy, base_grp, frontOfChain=1)
        bs = [self.line_edit_4.text()]
        # cmds.delete(copy)
        bs_position = 0
        for n, m in zip(['m_a', 'm_e', 'm_i', 'm_o', 'm_u', 'm_m', 'm_r', 'm_f'],
                        ['aaa', 'eh', 'iee', 'ohh', 'uuu', 'mbp', 'rrr', 'fff']):
            if cmds.objExists(n):
                bs_position = bs_position + 1
                # 表情控制器归位
                #mel.eval('asGoToBuildPose faceSetup;')
                self.controller_zeroing('无')
                # 创建规范组
                new_bs_grp = cmds.duplicate(base_grp, n=m)
                # 移动对应表情控制器
                cmds.setAttr('ctrlPhonemes_M.'+m, 10)
                # 判断哪些是要替换的进行替换
                base_child = cmds.listRelatives(base_grp, c=1)
                for i in range(0, len(base_child)):
                    for j in range(0, len(need_replace)):
                        absolute_name = need_replace[j].split('|')
                        if base_child[i] == absolute_name[-1]:
                            shape_base = cmds.listRelatives(new_bs_grp[0] + '|' + absolute_name[-1], c=1, type='mesh',
                                                            fullPath=1)
                            cmds.delete(shape_base)
                            # 生成bs模型
                            # print(base_grp + '|' + absolute_name[-1])
                            # print(new_bs_grp[0] + '|' + absolute_name[-1])
                            inverted_mesh = cmds.invertShape((base_grp + '|' + absolute_name[-1]),
                                                             (n + '|' + absolute_name[-1]))
                            shape = cmds.listRelatives(inverted_mesh, c=1, type='mesh', fullPath=1)

                            cmds.parent(shape, new_bs_grp[0] + '|' + absolute_name[-1], s=1, add=1)
                            cmds.delete(inverted_mesh)

                # 属性数值归零
                cmds.setAttr('ctrlPhonemes_M.'+m, 0)

                # 清理模型
                cmds.select(new_bs_grp[0])
                lattice = cmds.lattice(divisions=(2, 5, 2), ldv=(2, 2, 2), objectCentered=True)
                cmds.DeleteHistory()
                cmds.delete(lattice)

                # 创建新bs
                cmds.blendShape(bs, e=1, t=(base_grp, bs_position, new_bs_grp[0], 1))
                cmds.delete(new_bs_grp[0])

                # 添加bs驱动
                multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
                cmds.setAttr((multiplyDivide + '.input2X'), 0.1)

                cmds.connectAttr('ctrlPhonemes_M.'+m, (multiplyDivide + '.input1X'), f=1)
                cmds.connectAttr((multiplyDivide + '.outputX'), (bs[0] + '.' + m), f=1)
        cmds.undoInfo(cck=1)

    # 创建无驱动效果组
    def create_normal_drver(self):
        cmds.undoInfo(ock=1)
        #mel.eval('asGoToBuildPose bodySetup;if (`objExists FaceControlSet`)asGoToBuildPose faceSetup;')
        self.controller_zeroing('无')
        soure_attribute = ['ctrlPhonemes_M.aaa','ctrlPhonemes_M.eh','ctrlPhonemes_M.iee','ctrlPhonemes_M.ohh',
                           'ctrlPhonemes_M.uuu','ctrlPhonemes_M.mbp','ctrlPhonemes_M.fff','ctrlPhonemes_M.rrr']
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        controller = cmds.ls(sl=1)
        for c in controller:
            if not cmds.objExists(c+'_DrverGrp'):
                cmds.select(c)
                mel.eval('doGroup 0 1 1;')
                sel = cmds.ls(sl=1)
                cmds.rename(sel,c+'_DrverGrp')
            for s in soure_attribute:
                for z in ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ']:
                    loke = cmds.getAttr((c + '.' + z), l=True)
                    if not loke:
                        cmds.setAttr(s, 10)
                        cmds.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=s)
                        cmds.setAttr(s,0)
                        cmds.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=s)
        cmds.undoInfo(cck=1)

    # 删除无驱动效果组
    def delete_normal_drver(self):
        cmds.undoInfo(ock=1)
        #mel.eval('asGoToBuildPose bodySetup;if (`objExists FaceControlSet`)asGoToBuildPose faceSetup;')
        self.controller_zeroing('无')
        soure_attribute = ['ctrlPhonemes_M.aaa', 'ctrlPhonemes_M.eh', 'ctrlPhonemes_M.iee', 'ctrlPhonemes_M.ohh',
                           'ctrlPhonemes_M.uuu', 'ctrlPhonemes_M.mbp', 'ctrlPhonemes_M.fff', 'ctrlPhonemes_M.rrr']
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        controller = cmds.ls(sl=1)
        for c in controller:
            if cmds.objExists(c + '_DrverGrp'):
                P = cmds.listRelatives((c + '_DrverGrp'), p=1)
                C = cmds.listRelatives((c + '_DrverGrp'), c=1)
                cmds.parent(C[0],P[0])
                cmds.delete((c + '_DrverGrp'))
        cmds.undoInfo(cck=1)

    # 创建驱动
    def create_drver(self):
        cmds.undoInfo(ock=1)
        self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit'])
        face_bs_grp = cmds.ls(sl=1)
        self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit'])
        face = cmds.ls(sl=1)
        self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit'])
        controller = cmds.ls(sl=1)
        bs_name = self.comboBox_1.currentText()
        print(bs_name)
        attribute = ''
        if bs_name == 'm_a':
            attribute = 'ctrlPhonemes_M.aaa'
        if bs_name == 'm_e':
            attribute = 'ctrlPhonemes_M.eh'
        if bs_name == 'm_i':
            attribute = 'ctrlPhonemes_M.iee'
        if bs_name == 'm_o':
            attribute = 'ctrlPhonemes_M.ohh'
        if bs_name == 'm_u':
            attribute = 'ctrlPhonemes_M.uuu'
        if bs_name == 'm_m':
            attribute = 'ctrlPhonemes_M.mbp'
        if bs_name == 'm_r':
            attribute = 'ctrlPhonemes_M.rrr'
        if bs_name == 'm_f':
            attribute = 'ctrlPhonemes_M.fff'
        # 生成驱动
        cmds.select(controller)
        all_controller = cmds.ls(sl=1)
        for c in all_controller:
            for z in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']:
                # 获取旧驱动数值
                old_num = cmds.getAttr((c + '_DrverGrp.' + z))
                # 获取控制器数值
                new_num = cmds.getAttr((c + '.' + z))
                # 两者相加后控制器数值归零，驱动组数值为加完的数值，然后设置关键帧
                new_num = old_num + new_num
                loke = cmds.getAttr((c + '.' + z), l=True)
                if not loke:
                    cmds.setAttr((c + '.' + z), 0)
                    cmds.setAttr(attribute, 0)
                    cmds.setAttr((c + '_DrverGrp.' + z), 0)
                    cmds.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=attribute)
                    cmds.setAttr(attribute, 10)
                    cmds.setAttr((c + '_DrverGrp.' + z), new_num)
                    cmds.setDrivenKeyframe((c + '_DrverGrp.' + z), currentDriver=attribute)

        if bs_name == 'm_a':
            cmds.setAttr('ctrlPhonemes_M.aaa', 10)
        if bs_name == 'm_e':
            cmds.setAttr('ctrlPhonemes_M.eh', 10)
        if bs_name == 'm_i':
            cmds.setAttr('ctrlPhonemes_M.iee', 10)
        if bs_name == 'm_o':
            cmds.setAttr('ctrlPhonemes_M.ohh', 10)
        if bs_name == 'm_u':
            cmds.setAttr('ctrlPhonemes_M.uuu', 10)
        if bs_name == 'm_m':
            cmds.setAttr('ctrlPhonemes_M.mbp', 10)
        if bs_name == 'm_r':
            cmds.setAttr('ctrlPhonemes_M.rrr', 10)
        if bs_name == 'm_f':
            cmds.setAttr('ctrlPhonemes_M.fff', 10)
        cmds.undoInfo(cck=1)

    @Withdraw
    # 将选择模型点挪动到目标模型
    def move_point_to_target(self):
        sel = cmds.ls(sl=1)
        soure = sel[0]
        target = sel[1]
        # 获取所有顶点
        soure_vertices = cmds.ls(f"{soure}.vtx[*]", flatten=True)
        soure_vertex_positions = []
        for vertex in soure_vertices:
            # 获取顶点的世界坐标
            position = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
            soure_vertex_positions.append(position)
        targe_vertices = cmds.ls(f"{target}.vtx[*]", flatten=True)
        targe_vertex_positions = []
        for vertex in targe_vertices:
            # 获取顶点的世界坐标
            position = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
            targe_vertex_positions.append(position)

        offset = []
        for position1, position2 in zip(soure_vertex_positions, targe_vertex_positions):
            position = [(position2[0] - position1[0]),(position2[1] - position1[1]),(position2[2] - position1[2])]
            offset.append(position)

        # for vertex, position in zip(soure_vertices, targe_vertex_positions):
        #     cmds.xform(vertex, translation=position, worldSpace=True)

        for vertex, position in zip(soure_vertices, offset):
            cmds.move(position[0], position[1], position[2], vertex, relative=True, objectSpace=True, worldSpaceDistance=True)
        cmds.warning('强行移动模型点完毕。')


window = Window()
if __name__ == '__main__':
    window.show()

#删除无影响驱动
