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
        self.setWindowTitle('拉链生成(Maya' + self.maya_version + ')')

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 库路径
        self.library_path = library_path

        self.ui_edit = UiEdit()
        self.curve = CreateAndEditCurve()
        self.controller = CurveControllerEdit()

        # 顶层组名
        self.top_name = 'Zipper_all_Grp_'

        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    def create_widgets(self):
        # 对象A
        self.label_1 = QtWidgets.QLabel('对象A：')
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_1 = QtWidgets.QPushButton('加载')

        # 对象B
        self.label_2 = QtWidgets.QLabel('对象B：')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_2 = QtWidgets.QPushButton('加载')

        # 生成
        self.button_3 = QtWidgets.QPushButton('生成拉链')

        # 使用说明
        self.label_3 = QtWidgets.QLabel('按顺序选择对象后点击“加载”（对象A、对象B数量需一致，任意类型均可），再点“生成拉链”。')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)

        h_box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_box_layout_1)
        h_box_layout_1.addWidget(self.label_1)
        h_box_layout_1.addWidget(self.line_edit_1)
        h_box_layout_1.addWidget(self.button_1)

        h_box_layout_2 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_box_layout_2)
        h_box_layout_2.addWidget(self.label_2)
        h_box_layout_2.addWidget(self.line_edit_2)
        h_box_layout_2.addWidget(self.button_2)

        main_layout.addWidget(self.button_3)
        main_layout.addWidget(self.label_3)

    def create_connect(self):
        self.button_1.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))
        self.button_3.clicked.connect(self.generate)

    # 获取下一个可用编号
    def _get_next_num(self):
        num = 0
        while cmds.objExists(self.top_name + str(num)):
            num += 1
        return num

    # 获取对象世界坐标
    def _get_ws_pos(self, obj):
        return cmds.xform(obj, q=True, ws=True, t=True)

    # 从ui文本解析对象列表（按选择顺序，任意类型均可）
    def _parse_chain(self, text):
        if not text:
            return []
        names = [n.strip() for n in text.split(',') if n.strip()]
        objs = []
        for n in names:
            if cmds.objExists(n):
                objs.append(n)
            else:
                cmds.warning('对象不存在: ' + n)
                return []
        return objs

    # 计算总控制器缩放
    def _compute_scale(self, chain_a, chain_b):
        total = 0.0
        count = 0
        for chain in (chain_a, chain_b):
            for i in range(1, len(chain)):
                p0 = self._get_ws_pos(chain[i - 1])
                p1 = self._get_ws_pos(chain[i])
                total += math.dist(p0, p1)
                count += 1
        if count == 0:
            return 1.0
        avg = total / count
        return max(avg * 0.5, 0.001)

    # 创建总控制器并添加全部控制属性
    def _create_master_controller(self, top_num, chain_a, chain_b):
        self.curve.create_curve(self.library_path + r'\curve_library', '圆朝向')
        ctrl = cmds.ls(sl=1)[0]
        self.curve.change_curve_color('Index', [ctrl], [0, 0, 0], 17)
        ctrl = cmds.rename(ctrl, 'Zipper_Top_ctrl_C_%d' % top_num)

        scale = self._compute_scale(chain_a, chain_b)
        cmds.select(ctrl)
        self.controller.modify_vontroller_shape('scale', scale, scale, scale)

        grp2 = cmds.group(n='Zipper_Top_ctrl_Grp2_%d' % top_num, em=1)
        grp1 = cmds.group(n='Zipper_Top_ctrl_Grp1_%d' % top_num, em=1)
        cmds.parent(grp2, grp1)
        cmds.parent(ctrl, grp2)

        # 位置置于两条链首端的中间
        p0 = self._get_ws_pos(chain_a[0])
        p1 = self._get_ws_pos(chain_b[0])
        mid = [(a + b) / 2.0 for a, b in zip(p0, p1)]
        cmds.xform(grp1, ws=1, t=mid)

        self._add_master_attrs(ctrl)
        return grp1, ctrl

    # 给总控制器添加全部权重算法属性
    def _add_master_attrs(self, ctrl):
        attrs = [
            ('clamp', 'double', 1.0, None, None),
            ('base_weight', 'double', 1.0, None, None),
            ('number_objects', 'long', -1, None, None),
            ('time', 'double', 0.0, None, None),
            ('frequency', 'double', 0.1, None, None),
            ('range', 'double', 1.0, None, None),
            ('shrink_remapping', 'double', 1.0, 0.0, 1.0),
            ('front_shrink', 'double', 0.0, None, None),
            ('front_shrink_magnification', 'double', 0.0, None, None),
            ('back_shrink', 'double', 0.0, None, None),
            ('back_shrink_magnification', 'double', 0.0, None, None),
        ]
        for name, typ, dv, mn, mx in attrs:
            if not cmds.objExists(ctrl + '.' + name):
                kwargs = {'ln': name, 'at': typ, 'dv': dv}
                if mn is not None:
                    kwargs['min'] = mn
                if mx is not None:
                    kwargs['max'] = mx
                cmds.addAttr(ctrl, **kwargs)
            cmds.setAttr(ctrl + '.' + name, e=1, keyable=1)

    # 为单个输出骨骼创建脊柱权重表达式，驱动其矩阵混合权重
    def _create_zipper_expression(self, top_num, i, n, ctrl, joint, blend):
        fi = float(i)
        fn = float(n)
        lines = [
            'float $zClamp = %s.clamp;' % ctrl,
            'float $zBase = %s.base_weight;' % ctrl,
            'float $zTime = %s.time;' % ctrl,
            'float $zFreq = %s.frequency;' % ctrl,
            'float $zRange = %s.range * 0.01;' % ctrl,
            'float $zShrink = %s.shrink_remapping;' % ctrl,
            'float $zFShrink = %s.front_shrink;' % ctrl,
            'float $zFMag = %s.front_shrink_magnification;' % ctrl,
            'float $zBShrink = %s.back_shrink;' % ctrl,
            'float $zBMag = %s.back_shrink_magnification;' % ctrl,
            'float $zOff = %s.offset;' % joint,
            'float $zN = %s;' % fn,
            'if (%s.number_objects >= 0) $zN = %s.number_objects;' % (ctrl, ctrl),
            'if ($zN < 1.0) $zN = 1.0;',
            'float $zFIn = clamp(0.0, 1.5707963, (1.5707963 / $zN) * ($zFShrink + %s) * $zFMag);' % fi,
            'float $zFF = clamp(0.0, 1.0, sin($zFIn) * (1.0 - $zShrink) + $zShrink);',
            'float $zBIn = clamp(0.0, 1.5707963, (1.5707963 / $zN) * ($zBShrink + $zN - %s - 1.0) * $zBMag);' % fi,
            'float $zBF = clamp(0.0, 1.0, sin($zBIn) * (1.0 - $zShrink) + $zShrink);',
            'float $zOut = clamp(0.0 - $zClamp, $zClamp, $zFF * $zBF * $zBase * sin($zFreq * $zTime * 6.2831853 + $zRange * %s + $zOff));' % fi,
            'float $zWB = 1.0 - clamp(0.0, 1.0, $zOut);',
            '%s.target[0].weight = $zWB;' % blend,
        ]
        expr = '\n'.join(lines)
        name = 'Zipper_expr_%d_%d' % (top_num, i)
        if cmds.objExists(name):
            cmds.delete(name)
        cmds.expression(s=expr, n=name)

    # 生成拉链
    @Withdraw
    def generate(self):
        chain_a = self._parse_chain(self.line_edit_1.text())
        chain_b = self._parse_chain(self.line_edit_2.text())
        if not chain_a or not chain_b:
            cmds.warning('请先分别加载对象A和对象B。')
            return
        if len(chain_a) != len(chain_b):
            cmds.warning('对象A和对象B的数量不一致（%d vs %d），无法一一对应。' % (len(chain_a), len(chain_b)))
            return

        n = len(chain_a)
        top_num = self._get_next_num()
        top_grp = self.top_name + str(top_num)
        cmds.group(n=top_grp, em=1)

        # 创建总控制器
        ctrl_grp, ctrl = self._create_master_controller(top_num, chain_a, chain_b)
        cmds.parent(ctrl_grp, top_grp)

        # 创建输出骨骼，用矩阵混合驱动位移与旋转（避免约束翻转）
        output_joints = []
        for i in range(n):
            cmds.select(cl=1)
            joint = cmds.joint(n='Zipper_output_J_%d_%d' % (top_num, i))
            # 每个骨骼单独的偏移量属性（对应 all_offset）
            cmds.addAttr(joint, ln='offset', at='double', dv=0.0)
            cmds.setAttr(joint + '.offset', e=1, keyable=1)

            # 矩阵混合节点：对象A世界矩阵 -> inputMatrix，对象B世界矩阵 -> target[0].targetMatrix
            blend = cmds.createNode('blendMatrix', n='Zipper_blendMatrix_%d_%d' % (top_num, i))
            decomp = cmds.createNode('decomposeMatrix', n='Zipper_decomposeMatrix_%d_%d' % (top_num, i))

            cmds.connectAttr(chain_a[i] + '.worldMatrix[0]', blend + '.inputMatrix', f=1)
            cmds.connectAttr(chain_b[i] + '.worldMatrix[0]', blend + '.target[0].targetMatrix', f=1)

            cmds.connectAttr(blend + '.outputMatrix', decomp + '.inputMatrix', f=1)
            cmds.connectAttr(decomp + '.outputTranslate', joint + '.translate', f=1)
            cmds.connectAttr(decomp + '.outputRotate', joint + '.rotate', f=1)

            self._create_zipper_expression(top_num, i, n, ctrl, joint, blend)
            output_joints.append(joint)

        out_grp = cmds.group(output_joints, n='Zipper_output_J_%d_all_skin_joint' % top_num)
        cmds.parent(out_grp, top_grp)

        cmds.select(ctrl)
        cmds.warning('拉链生成完毕，总控制器: %s' % ctrl)


window = Window()
if __name__ == '__main__':
    window.show()
