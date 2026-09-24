# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
# 获取文件路径
import os
import inspect

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('链接火车(Maya'+self.maya_version+',仅供引用:SteamTrainBlock_rig，CarriageBlock_rig)')

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
        self.library_path = root_path + '\\' + maya_version


    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('选择路径样条给火车添加路径')
        self.button_2 = QtWidgets.QPushButton('给火车链接第一个车厢')
        self.button_3 = QtWidgets.QPushButton('先选择上一节车厢大控制器，再选下一节车厢大控制器，点击链接车厢')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        v_box_layout = QtWidgets.QVBoxLayout(self.central_widget)
        v_box_layout.setContentsMargins(0, 0, 0, 0)
        v_box_layout.setSpacing(1)

        v_box_layout.addWidget(self.button_1)
        v_box_layout.addWidget(self.button_2)
        v_box_layout.addWidget(self.button_3)


    def create_connect(self):
        self.button_1.clicked.connect(self.commend_1)
        self.button_2.clicked.connect(self.commend_2)
        self.button_3.clicked.connect(self.commend_3)

    # 选择样条运行即可添加路径样条
    def commend_1(self):
        sel = cmds.ls(sl=1)
        if sel:
            shape = cmds.listRelatives(sel, shapes=True, )[0]
            all_an = cmds.ls('SteamTrainBlock_rig:ik_choice.input[*]')
            num = int(all_an[-1].split('[')[-1][:-1])
            cmds.connectAttr(shape + '.worldSpace[0]', 'SteamTrainBlock_rig:ik_choice.input[' + str(num + 1) + ']')
            cmds.setAttr('SteamTrainBlock_rig:anim_globalMove01.curve', num + 1)
            cmds.warning('创建完成')
        else:
            cmds.warning('请选择路径')

    # 第一次添加约束
    def commend_2(self):
        cmds.parentConstraint('SteamTrainBlock_rig:ikParthJ8_loc', 'CarriageBlock_rig:LinkRequiredLoc1', w=1)
        cmds.parentConstraint('SteamTrainBlock_rig:FKBackBodyJ4_M', 'CarriageBlock_rig:FKExtraPropJ44_M', w=1, mo=1)
        cmds.connectAttr('SteamTrainBlock_rig:ik_choice.output', 'CarriageBlock_rig:box_choice.input[1]')
        cmds.setAttr('CarriageBlock_rig:anim_globalMove01.new_curve', 1)
        cmds.warning('创建完成')

    # 后续添加约束
    def commend_3(self):
        sel = cmds.ls(sl=1)
        if len(sel) > 1:
            # 获取空间名称
            spae_name1 = sel[0].split(':')[0]
            spae_name2 = sel[-1].split(':')[0]
            cmds.parentConstraint(spae_name1 + ':ikParthJ3', spae_name2 + ':LinkRequiredLoc1', w=1)
            cmds.parentConstraint(spae_name1 + ':FKPropJ46_M', spae_name2 + ':LinkRequiredLoc', w=1, mo=1)
            cmds.connectAttr('SteamTrainBlock_rig:ik_choice.output', spae_name2 + ':box_choice.input[1]')
            cmds.setAttr(spae_name2 + ':anim_globalMove01.new_curve', 1)
            cmds.warning('创建完成')
        else:
            cmds.warning('请选择两个对象')

window = Window()
if __name__ == '__main__':
    window.show()

