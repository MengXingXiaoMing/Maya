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

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import model
from model import *
importlib.reload(model)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        #self.command = Command()
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('文件清理+小功能(Maya'+self.maya_version+')')
        self.ui_edit = UiEdit()
        self.model = Model()

        self.create_widgets()
        self.create_layouts()
        self.create_connect()
        self.others_library = OthersLibrary()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version



    def create_widgets(self):
        # 第一行
        self.button_001 = QtWidgets.QPushButton('清理枢轴')
        self.button_002 = QtWidgets.QPushButton('清理所有bs组')
        self.button_003 = QtWidgets.QPushButton('简单模型清理（并不能处理掉所有问题）')
        self.button_004 = QtWidgets.QPushButton('清理动画节点（包括动画层）')

        self.button_005 = QtWidgets.QPushButton('清理显示层')
        self.button_006 = QtWidgets.QPushButton('文件清理')
        self.button_007 = QtWidgets.QPushButton('检查自穿插（需手动修改）')
        self.button_008 = QtWidgets.QPushButton('选择对称点（0.001）')
        self.button_009 = QtWidgets.QPushButton('选择模型中线修复对称')
        self.button_010 = QtWidgets.QPushButton('清理空间名')
        self.button_011 = QtWidgets.QPushButton('清理权重（0.01）')
        self.button_012 = QtWidgets.QPushButton('清理物体点吸附模型后数值为NAN')
        # self.button_013 = QtWidgets.QPushButton('清理渲染层（开发中）')
        # self.button_014 = QtWidgets.QPushButton('清理渲染层（开发中）')
        self.button_013 = QtWidgets.QPushButton('旧版模型对称（保证至少有一对面是对称的，且有中线）')
        self.button_014 = QtWidgets.QPushButton('选择uv边界线')
        self.button_015 = QtWidgets.QPushButton('按uv切割模型并按uv打平模型且建立uv变形表达式(加表达式时巨卡，生成后的模型有刷新属性，自己写个表达式链接给那刷新属性就能刷新)')
        self.button_016 = QtWidgets.QPushButton('按uv建立模型')
        self.button_017 = QtWidgets.QPushButton('建立Uv变形平面')

        # self.splitter_1 = QtWidgets.QSplitter()
        # self.splitter_1.setFixedHeight(1)
        # self.splitter_1.setFrameStyle(1)

    def create_layouts(self):
        # 创建滚动区域
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)  # 关键：允许内容部件调整大小
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(scroll_area)  # 将滚动区域设置为主窗口的中央部件

        # 创建内容部件
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        main_layout = QtWidgets.QVBoxLayout(content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        splitter = QtWidgets.QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        scroll_area_2, Widget_1, h_Box_layout_11 = self.ui_edit.create_ui_with_auto_slider(splitter)
        h_Box_layout_11.setSpacing(1)
        h_Box_layout_11.addWidget(self.button_001)
        h_Box_layout_11.addWidget(self.button_002)
        h_Box_layout_11.addWidget(self.button_003)
        h_Box_layout_11.addWidget(self.button_004)
        h_Box_layout_11.addWidget(self.button_005)
        h_Box_layout_11.addWidget(self.button_006)
        h_Box_layout_11.addWidget(self.button_007)
        h_Box_layout_11.addWidget(self.button_008)
        h_Box_layout_11.addWidget(self.button_009)
        h_Box_layout_11.addWidget(self.button_010)
        h_Box_layout_11.addWidget(self.button_011)
        h_Box_layout_11.addWidget(self.button_012)
        h_Box_layout_11.addWidget(self.button_013)
        # for i in range(100):
        #     button_015 = QtWidgets.QPushButton('按uv切割模型并按uv打平模型')
        #     h_Box_layout_11.addWidget(button_015)
        #flow_layout_1.addWidget(self.button_13)

        scroll_area_3, Widget_2, h_Box_layout_12 = self.ui_edit.create_ui_with_auto_slider(splitter)
        h_Box_layout_12.addWidget(self.button_014)
        h_Box_layout_12.addWidget(self.button_015)
        h_Box_layout_12.addWidget(self.button_016)



        # 置顶
        main_layout.addStretch(1)

    def create_connect(self):
        self.button_001.clicked.connect(lambda:  self.others_library.cleaning_the_pivot())  # 清理枢轴
        self.button_002.clicked.connect(lambda: self.others_library.clean_up_invalid_BS_groups())  # 清理所有bs和bs组
        self.button_003.clicked.connect(lambda: self.others_library.cleaning_the_model())  # 简单清理模型
        self.button_004.clicked.connect(lambda: self.others_library.cleaning_the_animation_nodes())  # 清理动画节点
        self.button_005.clicked.connect(lambda: self.others_library.cleaning_the_display_layers())  # 清理显示层
        self.button_006.clicked.connect(lambda: self.others_library.cleaning_the_file())  # 文件清理
        self.button_007.clicked.connect(lambda: self.others_library.check_self_intersect())  # 检查自穿插
        self.button_008.clicked.connect(lambda: cmds.select(self.others_library.mirror_point()[2]))  # 选择对称点
        self.button_009.clicked.connect(lambda: self.others_library.fix_symmetry())  # 修复对称
        self.button_010.clicked.connect(lambda: self.others_library.clean_namespace())  # 清理空间名
        self.button_011.clicked.connect(lambda: self.others_library.joint_weight_to_game_specification())  # 清理权重
        self.button_012.clicked.connect(lambda: self.others_library.clean_adsorption_num_nan())  # 物体吸附数值为nan
        self.button_013.clicked.connect(lambda: self.others_library.fix_symmetry_2())  # 修复对称2

        self.button_014.clicked.connect(lambda: cmds.select(self.model.get_uv_borders(cmds.ls(sl=1))))  # 选择uv边缘
        self.button_015.clicked.connect(self.mesh_to_uv)  # 按uv切割模型并生成打平模型（所有分离的线和uv匹配）
        self.button_016.clicked.connect(lambda: cmds.select(self.model.create_uv_model(cmds.ls(sl=1)[0]))) # 按uv切割模型并生成打平模型（所有分离的线和uv匹配）


    # 按uv切割模型并生成打平模型（所有分离的线和uv匹配）,且建立uv变形
    def mesh_to_uv(self):
        cmds.undoInfo(ock=1)
        sel = cmds.ls(sl=1)
        cmds.select(self.model.get_uv_borders(cmds.ls(sl=1)))
        cmds.DetachComponent()
        model, uv_with_point = self.model.create_flattened_model(sel[0])
        # 添加属性
        cmds.addAttr(model, ln='refresh', at='double', dv=0)
        an = model + '.refresh'
        cmds.setAttr(an, e=1, keyable=True)
        x = 0
        for s in sel:
            shape = cmds.listRelatives(s, c=1, type='mesh')
            point = cmds.ls(model + '.vtx[*]', fl=1)
            expression_txt = 'float $refresh = ' + an + ';\n'
            for i in range(len(point)):
                # uv_points = cmds.polyListComponentConversion(point[i], fromVertex=True, toUV=True)
                # uv_points = cmds.filterExpand(uv_points, sm=35)[0]  # 过滤为 UV 组件[4](@ref)
                # num = int(uv_points.split('[')[1].split(']')[0])
                num = uv_with_point[i][1]
                # xform = cmds.xform(point[i], q=1, t=1, ws=1)
                # plusMinusAverage = cmds.createNode('plusMinusAverage')
                txt = 'float $xform'+str(x)+'[] = `xform -q -t -a  "' + point[i] + '"`;\n'
                for me in shape:
                    txt += '' + me + '.uvSet[0].uvSetPoints[' + str(num) + '].uvSetPointsU = $xform'+str(x)+'[0];\n'
                    txt += '' + me + '.uvSet[0].uvSetPoints[' + str(num) + '].uvSetPointsV = $xform'+str(x)+'[1];\n'
                x += 1
                expression_txt += txt
                print(s,x)
                # print(uv_points)
            cmds.expression(s=expression_txt, ae=1, uc='all', o='')
            cmds.polySoftEdge(s, a=180, ch=1)

        cmds.undoInfo(cck=1)
    def self_commend(self):
        pass

window = Window()
if __name__ == '__main__':
    window.show()

