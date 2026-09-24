# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
import math

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
    # 直接判断是否是目录
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
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


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)

        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('体积(Maya' + self.maya_version + ')')
        self.setFixedWidth(400)

        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 库路径
        self.library_path = self.root_path + '\\' + maya_version

        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    def create_widgets(self):
        # 骨骼链
        self.button_1 = QtWidgets.QPushButton('选择骨骼链根骨骼')
        self.line_edit_1 = QtWidgets.QLineEdit('')
        self.button_2 = QtWidgets.QPushButton('加载')

        # 拉伸属性
        self.button_3 = QtWidgets.QPushButton('选择拉伸属性')
        self.line_edit_2 = QtWidgets.QLineEdit('')
        self.button_4 = QtWidgets.QPushButton('加载')

        # 总控制器前缀
        self.label_1 = QtWidgets.QLabel('总控制器前缀:')
        self.line_edit_3 = QtWidgets.QLineEdit('Volume')

        # 生成 / 删除
        self.button_5 = QtWidgets.QPushButton('生成体积')
        self.button_5.setStyleSheet('color:rgb(0,0,0);background:rgb(255,102,102)')
        self.button_6 = QtWidgets.QPushButton('删除体积')
        self.button_6.setStyleSheet('color:rgb(0,0,0);background:rgb(80,80,80)')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        self.label_2 = QtWidgets.QLabel('说明: 拉伸属性为长度拉伸倍率(1为原始长度)；生成后总控制器驱动骨骼 scaleY/scaleZ(径向粗细)。Volume=过渡强度(0-1)，Amplitude=变形幅度(0-2)，Falloff=衰减强度(>1集中中间/<1平缓)，Linearity=线性化(0曲线/1线性)')
        self.label_2.setWordWrap(True)

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.addWidget(self.button_1)
        h_Box_layout_1.addWidget(self.line_edit_1)
        h_Box_layout_1.addWidget(self.button_2)
        h_Box_layout_1.setSpacing(1)

        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_2)
        h_Box_layout_2.addWidget(self.button_3)
        h_Box_layout_2.addWidget(self.line_edit_2)
        h_Box_layout_2.addWidget(self.button_4)
        h_Box_layout_2.setSpacing(1)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_3)
        h_Box_layout_3.addWidget(self.label_1)
        h_Box_layout_3.addWidget(self.line_edit_3)
        h_Box_layout_3.setSpacing(1)

        main_layout.addWidget(self.splitter_1)
        main_layout.addWidget(self.button_5)
        main_layout.addWidget(self.button_6)
        main_layout.addWidget(self.label_2)

        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))

        self.button_3.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit']))
        self.button_4.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))

        self.button_5.clicked.connect(self.create_volume)
        self.button_6.clicked.connect(self.delete_volume)

    # 从根骨骼向下按第一个子骨骼收集成线性骨骼链
    def get_joint_chain(self, root):
        chain = [root]
        current = root
        while True:
            children = cmds.listRelatives(current, c=1, type='joint') or []
            if not children:
                break
            current = children[0]
            chain.append(current)
        return chain

    # 计算每个关节的体积变化分布基础值(两端为0，中间为1)
    # 返回 (曲线版cos平滑衰减, 线性版三角衰减)
    def get_distribution_bases(self, index, count):
        if count <= 2:
            return 1.0, 1.0
        t = float(index) / (count - 1)
        # 曲线分布: cos 平滑衰减
        curve = (1.0 - math.cos(2.0 * math.pi * t)) / 2.0
        # 线性分布: 三角(0->1->0 线性)
        linear = 1.0 - abs(2.0 * t - 1.0)
        return curve, linear

    # 生成体积保持
    def create_volume(self):
        print('生成体积')
        root_text = self.line_edit_1.text().strip()
        stretch_attr = self.line_edit_2.text().strip()
        prefix = self.line_edit_3.text().strip() or 'Volume'

        if not root_text:
            cmds.warning('请先加载骨骼链根骨骼')
            return
        if not stretch_attr or '.' not in stretch_attr:
            cmds.warning('请先加载拉伸属性(格式: 物体.属性)')
            return
        if not cmds.objExists(root_text):
            cmds.warning('骨骼链根骨骼不存在: ' + root_text)
            return
        if cmds.nodeType(root_text) != 'joint':
            cmds.warning('骨骼链根骨骼不是关节: ' + root_text)
            return

        attr_node, attr_name = stretch_attr.split('.', 1)
        if not cmds.objExists(attr_node) or not cmds.attributeQuery(attr_name, node=attr_node, exists=True):
            cmds.warning('拉伸属性不存在: ' + stretch_attr)
            return

        joints = self.get_joint_chain(root_text)
        if len(joints) < 1:
            cmds.warning('未能获取骨骼链')
            return

        need_delete = []

        # 创建总控制器
        master_crv = cmds.circle(n=(prefix + '_Volume_Master_Ctrl'), nr=(0, 1, 0), r=1.0, ch=False)[0]
        master_grp = cmds.group(n=(prefix + '_Volume_Master_Grp'), em=1)
        cmds.parent(master_crv, master_grp)
        pos = cmds.xform(joints[0], q=1, ws=1, t=1)
        cmds.xform(master_grp, ws=1, t=pos)
        cmds.setAttr(master_crv + '.overrideEnabled', 1)
        cmds.setAttr(master_crv + '.overrideColor', 13)
        need_delete.append(master_grp)
        need_delete.append(master_crv)

        # 总控制器控制属性
        # Volume: 有/无体积保持之间的过渡强度(0-1 连续)
        cmds.addAttr(master_crv, ln='Volume', at='double', min=0, max=1, dv=1)
        cmds.setAttr(master_crv + '.Volume', e=1, keyable=True)
        # Amplitude: 有拉伸情况下的变形幅度(0=不变形, 1=标准保持体积, 2=夸张变形)
        cmds.addAttr(master_crv, ln='Amplitude', at='double', min=0, dv=1)
        cmds.setAttr(master_crv + '.Amplitude', e=1, keyable=True)
        # Falloff: 分布衰减强度(1=标准cos衰减, >1更集中中间, <1更平缓均匀)
        cmds.addAttr(master_crv, ln='Falloff', at='double', min=0.1, max=10, dv=1)
        cmds.setAttr(master_crv + '.Falloff', e=1, keyable=True)
        # Linearity: 分布线性化(0=纯曲线衰减, 1=纯线性三角衰减)
        cmds.addAttr(master_crv, ln='Linearity', at='double', min=0, max=1, dv=0)
        cmds.setAttr(master_crv + '.Linearity', e=1, keyable=True)

        # 夹取拉伸值，避免 0 或负数进入幂运算
        stretch_clamp = cmds.createNode('clamp', n=(prefix + '_StretchClamp'))
        need_delete.append(stretch_clamp)
        cmds.connectAttr(stretch_attr, stretch_clamp + '.inputR', f=1)
        cmds.setAttr(stretch_clamp + '.minR', 0.001)
        cmds.setAttr(stretch_clamp + '.maxR', 100000)

        # Amplitude * 0.5
        amp_half = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_AmpHalf'))
        need_delete.append(amp_half)
        cmds.setAttr(amp_half + '.operation', 1)
        cmds.connectAttr(master_crv + '.Amplitude', amp_half + '.input1X', f=1)
        cmds.setAttr(amp_half + '.input2X', 0.5)

        # 取负 -> -Amplitude/2
        exp_neg = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_ExpNeg'))
        need_delete.append(exp_neg)
        cmds.setAttr(exp_neg + '.operation', 1)
        cmds.connectAttr(amp_half + '.outputX', exp_neg + '.input1X', f=1)
        cmds.setAttr(exp_neg + '.input2X', -1)

        # 幂运算: S^(-Amplitude/2)，完整保持体积时的理想径向缩放
        volume_pow = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_VolumePow'))
        need_delete.append(volume_pow)
        cmds.setAttr(volume_pow + '.operation', 3)
        cmds.connectAttr(stretch_clamp + '.outputR', volume_pow + '.input1X', f=1)
        cmds.connectAttr(exp_neg + '.outputX', volume_pow + '.input2X', f=1)

        # delta = T - 1
        delta = cmds.shadingNode('plusMinusAverage', asUtility=1, n=(prefix + '_Delta'))
        need_delete.append(delta)
        cmds.setAttr(delta + '.operation', 1)
        cmds.connectAttr(volume_pow + '.outputX', delta + '.input1D[0]', f=1)
        cmds.setAttr(delta + '.input1D[1]', -1)

        # vol_delta = Volume * delta
        vol_delta = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_VolDelta'))
        need_delete.append(vol_delta)
        cmds.setAttr(vol_delta + '.operation', 1)
        cmds.connectAttr(master_crv + '.Volume', vol_delta + '.input1X', f=1)
        cmds.connectAttr(delta + '.output1D', vol_delta + '.input2X', f=1)

        # 逐个关节应用径向缩放(scaleY / scaleZ)
        count = len(joints)
        for i, joint in enumerate(joints):
            curve_base, linear_base = self.get_distribution_bases(i, count)

            # 曲线分布 ^ Falloff
            curve_pow = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_CurvePow%d' % i))
            need_delete.append(curve_pow)
            cmds.setAttr(curve_pow + '.operation', 3)
            cmds.setAttr(curve_pow + '.input1X', curve_base)
            cmds.connectAttr(master_crv + '.Falloff', curve_pow + '.input2X', f=1)

            # 线性分布 ^ Falloff
            linear_pow = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_LinearPow%d' % i))
            need_delete.append(linear_pow)
            cmds.setAttr(linear_pow + '.operation', 3)
            cmds.setAttr(linear_pow + '.input1X', linear_base)
            cmds.connectAttr(master_crv + '.Falloff', linear_pow + '.input2X', f=1)

            # 线性化混合: dist = mix(curve^f, linear^f, Linearity)
            # 注意: blendColors 的 blender=0 输出 color2, blender=1 输出 color1
            dist_blend = cmds.shadingNode('blendColors', asUtility=1, n=(prefix + '_DistBlend%d' % i))
            need_delete.append(dist_blend)
            cmds.connectAttr(linear_pow + '.outputX', dist_blend + '.color1R', f=1)
            cmds.connectAttr(curve_pow + '.outputX', dist_blend + '.color2R', f=1)
            cmds.connectAttr(master_crv + '.Linearity', dist_blend + '.blender', f=1)

            # vol_delta * dist
            dist_md = cmds.shadingNode('multiplyDivide', asUtility=1, n=(prefix + '_Dist%d' % i))
            need_delete.append(dist_md)
            cmds.setAttr(dist_md + '.operation', 1)
            cmds.connectAttr(vol_delta + '.outputX', dist_md + '.input1X', f=1)
            cmds.connectAttr(dist_blend + '.outputR', dist_md + '.input2X', f=1)

            # 1 + vol_delta * dist
            blend = cmds.shadingNode('plusMinusAverage', asUtility=1, n=(prefix + '_Blend%d' % i))
            need_delete.append(blend)
            cmds.setAttr(blend + '.operation', 1)
            cmds.setAttr(blend + '.input1D[0]', 1)
            cmds.connectAttr(dist_md + '.outputX', blend + '.input1D[1]', f=1)

            for axis in ('Y', 'Z'):
                cmds.connectAttr(blend + '.output1D', joint + '.scale' + axis, f=1)

        # 记录所有创建内容，便于删除
        cmds.addAttr(master_crv, ln='node', dt='string')
        cmds.setAttr(master_crv + '.node', str(need_delete), type='string')

        print('体积保持已生成，总控制器: ' + master_crv)

    # 删除体积保持
    def delete_volume(self):
        print('删除体积')
        sel = cmds.ls(sl=1)
        if not sel:
            cmds.warning('请先选择体积总控制器')
            return
        master = sel[0]
        if not cmds.attributeQuery('node', node=master, exists=True):
            cmds.warning('所选对象不是体积总控制器')
            return
        self.delete_node_attribute(master)

    # 删除 node 属性中记录的所有对象
    def delete_node_attribute(self, obj):
        node = cmds.getAttr(obj + '.node')
        node_list = ast.literal_eval(node)
        for n in node_list:
            if cmds.objExists(n):
                cmds.delete(n)


window = Window()
if __name__ == '__main__':
    window.show()
