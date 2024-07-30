# -*- coding: utf-8 -*-
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

import model
importlib.reload(model)
from model import *

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import weight
importlib.reload(weight)
from weight import *

import blendshape
importlib.reload(blendshape)
from blendshape import *

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
        self.setWindowTitle('BS编辑（仅开发了UI）(Maya'+self.maya_version+')')

        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()
        self.others_library = OthersLibrary()
        self.ui_edit = UiEdit()
        self.weight = Weight()
        self.blendshape = BlendshapeEdit()
        self.folder_name = 'wrap_preset'
        self.model = Model()

        self.create_widgets()
        self.create_layouts()
        self.create_connect()
    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('创建中间态模型（需要有wrap3d）')
        self.button_2 = QtWidgets.QPushButton('导入中间态模型')
        self.button_36 = QtWidgets.QPushButton('按拓扑传递UV')
        self.button_3 = QtWidgets.QPushButton('传递给目标模型UV')
        self.button_4 = QtWidgets.QPushButton('选择点修正UV')
        self.button_5 = QtWidgets.QPushButton('导入模板')
        self.button_6 = QtWidgets.QPushButton('帮助')

        self.Label_1 = QtWidgets.QLabel()
        self.Label_1.setText('异拓扑传递变形：')

        self.button_7 = QtWidgets.QPushButton('含变形的模型：')
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.button_8 = QtWidgets.QPushButton('加载')

        self.button_9 = QtWidgets.QPushButton('中间态模型：')
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.button_10 = QtWidgets.QPushButton('加载')

        self.button_11 = QtWidgets.QPushButton('变形传递目标：')
        self.line_edit_3 = QtWidgets.QLineEdit()
        self.button_12 = QtWidgets.QPushButton('加载')

        self.button_13 = QtWidgets.QPushButton('传递变形')
        self.button_14 = QtWidgets.QPushButton('UV复制权重')

        self.Label_2 = QtWidgets.QLabel()
        self.Label_2.setText('烘焙模型：')

        self.button_15 = QtWidgets.QPushButton('需烘焙模型/组：')
        self.line_edit_4 = QtWidgets.QLineEdit()
        self.button_16 = QtWidgets.QPushButton('加载')

        self.button_17 = QtWidgets.QPushButton('具体BS属性：')
        self.line_edit_5 = QtWidgets.QLineEdit()
        self.button_18 = QtWidgets.QPushButton('加载')

        #self.line_edit_6 = QtWidgets.QLineEdit()
        self.button_19 = QtWidgets.QPushButton(self)
        if QtCore.QResource(':/paintBlendshape.png').isValid():
            i = QtGui.QIcon(':/paintBlendshape.png')
            self.button_19.setIcon(i)
        self.button_19.setIconSize(QSize(25, 25))
        self.button_19.setMaximumHeight(23)
        self.button_20 = QtWidgets.QPushButton('烘焙当前范围帧')

        self.Label_5 = QtWidgets.QLabel()
        self.Label_5.setText('BS轮流输出数值:')
        self.line_edit_7 = QtWidgets.QLineEdit()
        self.line_edit_7.setText('1')
        self.button_21 = QtWidgets.QPushButton('自动加帧')

        self.Label_3 = QtWidgets.QLabel()
        self.Label_3.setText('三轴分解BS：')

        self.button_22 = QtWidgets.QPushButton('分解源模型：')
        self.line_edit_8 = QtWidgets.QLineEdit()
        self.button_23 = QtWidgets.QPushButton('加载')

        self.button_24 = QtWidgets.QPushButton('具体BS属性：')
        self.line_edit_9 = QtWidgets.QLineEdit()
        self.button_25 = QtWidgets.QPushButton('加载')

        self.button_26 = QtWidgets.QPushButton('分解参考模型：')
        self.line_edit_10 = QtWidgets.QLineEdit()
        self.button_27 = QtWidgets.QPushButton('加载')

        self.button_28 = QtWidgets.QPushButton('开始分解')

        self.Label_4 = QtWidgets.QLabel()
        self.Label_4.setText('BS转权重：')

        self.button_29 = QtWidgets.QPushButton('含BS的模型：')
        self.line_edit_11 = QtWidgets.QLineEdit()
        self.button_30 = QtWidgets.QPushButton('加载')

        self.button_31 = QtWidgets.QPushButton('选择BS节点：')
        self.line_edit_12 = QtWidgets.QLineEdit()
        self.button_32 = QtWidgets.QPushButton('加载')

        self.button_33 = QtWidgets.QPushButton('脸部骨骼：')
        self.line_edit_13 = QtWidgets.QLineEdit()
        self.button_34 = QtWidgets.QPushButton('加载')

        self.button_35 = QtWidgets.QPushButton('开始转换（暂未开发）')

        #self.button_36 = QtWidgets.QPushButton('开始转换（暂未开发）')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # 第一行
        h_box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_box_layout_1)
        h_box_layout_1.addWidget(self.button_1)
        h_box_layout_1.addWidget(self.button_2)
        h_box_layout_1.addWidget(self.button_36)
        h_box_layout_1.addWidget(self.button_3)
        h_box_layout_1.addWidget(self.button_4)
        h_box_layout_1.addWidget(self.button_5)
        h_box_layout_1.addWidget(self.button_6)

        h_Box_layout_2 = QtWidgets.QGridLayout(self)
        main_layout.addLayout(h_Box_layout_2)

        h_Box_layout_2.addWidget(self.Label_1, 0, 0)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3, 0, 1)
        h_Box_layout_3.addWidget(self.button_7)
        h_Box_layout_3.addWidget(self.line_edit_1)
        h_Box_layout_3.addWidget(self.button_8)

        h_Box_layout_4 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_4, 0, 2)
        h_Box_layout_4.addWidget(self.button_9)
        h_Box_layout_4.addWidget(self.line_edit_2)
        h_Box_layout_4.addWidget(self.button_10)

        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_5, 0, 3)
        h_Box_layout_5.addWidget(self.button_11)
        h_Box_layout_5.addWidget(self.line_edit_3)
        h_Box_layout_5.addWidget(self.button_12)

        h_Box_layout_6 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_6, 0, 4)
        h_Box_layout_6.addWidget(self.button_13)
        h_Box_layout_6.addWidget(self.button_14)

        h_Box_layout_2.addWidget(self.Label_2, 1, 0)

        h_Box_layout_7 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_7, 1, 1)
        h_Box_layout_7.addWidget(self.button_15)
        h_Box_layout_7.addWidget(self.line_edit_4)
        h_Box_layout_7.addWidget(self.button_16)

        h_Box_layout_8 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_8, 1, 2)
        h_Box_layout_8.addWidget(self.button_17)
        h_Box_layout_8.addWidget(self.line_edit_5)
        h_Box_layout_8.addWidget(self.button_18)

        h_Box_layout_9 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_9, 1, 4)
        h_Box_layout_9.addWidget(self.button_19)
        #h_Box_layout_9.addWidget(self.line_edit_6)
        h_Box_layout_9.addWidget(self.button_20)


        h_Box_layout_10 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_10, 1, 3)
        h_Box_layout_10.addWidget(self.Label_5)
        h_Box_layout_10.addWidget(self.line_edit_7)
        h_Box_layout_10.addWidget(self.button_21)

        h_Box_layout_2.addWidget(self.Label_3, 2, 0)

        h_Box_layout_11 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_11, 2, 1)
        h_Box_layout_11.addWidget(self.button_22)
        h_Box_layout_11.addWidget(self.line_edit_8)
        h_Box_layout_11.addWidget(self.button_23)

        h_Box_layout_12 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_12, 2, 2)
        h_Box_layout_12.addWidget(self.button_24)
        h_Box_layout_12.addWidget(self.line_edit_9)
        h_Box_layout_12.addWidget(self.button_25)

        h_Box_layout_13 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_13, 2, 3)
        h_Box_layout_13.addWidget(self.button_26)
        h_Box_layout_13.addWidget(self.line_edit_10)
        h_Box_layout_13.addWidget(self.button_27)

        h_Box_layout_14 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_14, 2, 4)
        h_Box_layout_14.addWidget(self.button_28)

        '''h_Box_layout_2.addWidget(self.Label_4, 3, 0)

        h_Box_layout_15 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_15, 3, 1)
        h_Box_layout_15.addWidget(self.button_29)
        h_Box_layout_15.addWidget(self.line_edit_11)
        h_Box_layout_15.addWidget(self.button_30)

        h_Box_layout_16 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_16, 3, 2)
        h_Box_layout_16.addWidget(self.button_31)
        h_Box_layout_16.addWidget(self.line_edit_12)
        h_Box_layout_16.addWidget(self.button_32)

        h_Box_layout_17 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_17, 3, 3)
        h_Box_layout_17.addWidget(self.button_33)
        h_Box_layout_17.addWidget(self.line_edit_13)
        h_Box_layout_17.addWidget(self.button_34)

        h_Box_layout_18 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_18, 3, 4)
        h_Box_layout_18.addWidget(self.button_35)'''

        h_Box_layout_19 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_19)
        #h_Box_layout_19.addWidget(self.button_36)

        main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(self.open_wrap)  # 打开wrap模板文件
        self.button_2.clicked.connect(self.import_intermediate)  # 导入中间态模型
        self.button_36.clicked.connect(self.topology_transfer_uv)  # 按规范传递UV
        self.button_3.clicked.connect(self.position_transfer_uv)  # 按规范传递UV
        self.button_4.clicked.connect(self.select_point_correct_uv)  # 选点修正UV
        self.button_5.clicked.connect(self.test_Template)  # 打开模板
        self.button_6.clicked.connect(self.help)  # 帮助
        self.button_7.clicked.connect(lambda :self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit']))  # 选择含变形的模型
        self.button_8.clicked.connect(lambda :self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))  # 加载含变形的模型
        self.button_9.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_2, ['QLineEdit']))  # 选择中间态模型
        self.button_10.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))  # 加载中间态模型
        self.button_11.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_3, ['QLineEdit']))  # 选择变形传递目标
        self.button_12.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))  # 加载变形传递目标
        self.button_13.clicked.connect(self.transfer_deformation)  # 传递变形
        self.button_14.clicked.connect(self.copy_weights_by_uv)  # UV复制权重
        self.button_15.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_4, ['QLineEdit']))  # 选择含变形的模型
        self.button_16.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_4, ['QLineEdit']))  # 加载含变形的模型
        self.button_17.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_5, ['QLineEdit']))  # 选择中间态模型
        self.button_18.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_5, ['QLineEdit']))  # 加载中间态模型
        self.button_21.clicked.connect(self.bs_auto_k_frame)  # bs自动k帧
        self.button_19.clicked.connect(self.darw_bs_weight)  # 绘制bs权重
        self.button_20.clicked.connect(self.back_frame)  # 烘焙当前范围帧

        self.button_22.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_8, ['QLineEdit']))  # 选择含变形的模型
        self.button_23.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_8, ['QLineEdit']))  # 加载含变形的模型
        self.button_24.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_9, ['QLineEdit']))  # 选择中间态模型
        self.button_25.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_9, ['QLineEdit']))  # 加载中间态模型
        self.button_26.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_10, ['QLineEdit']))  # 选择变形传递目标
        self.button_27.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_10, ['QLineEdit']))  # 加载变形传递目标
        self.button_28.clicked.connect(self.split_bs)


    # 打开模板文件，进入Wrap4D
    def open_wrap(self):
        sel = cmds.ls(sl=1)
        cmds.select(sel[0], r=1)
        mel.eval('file -force -options \"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\" -typ \"OBJexport\" -pr -es (\"' + self.file_path_reverse + '/'+self.folder_name+'/source.obj\");')
        cmds.select(sel[1], r=1)
        mel.eval('file -force -options \"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\" -typ \"OBJexport\" -pr -es (\"' + self.file_path_reverse + '/'+self.folder_name+'/target.obj\");')
        os.startfile(self.file_path + '\\' + self.folder_name + '\\wrap_template.wrap')
        cmds.warning('文件如果打开后没效果请进wrap界面手动加载，以下是文件路径：\n' + self.file_path + '\\' + self.folder_name + '\\wrap_template.wrap')

    # 导入中间态模型
    def import_intermediate(self):
        mel.eval('file -import -type "OBJ"  -ignoreVersion -mergeNamespacesOnClash false -rpr "WrapObject" -options "mo=1"  -pr  -importTimeRange "combine" (\"' + self.file_path_reverse + '/'+self.folder_name+'/WrapObject.obj\");')
        cmds.warning('导入中间态模型')

    # 按拓扑传递UV
    def topology_transfer_uv(self):
        sel = cmds.ls(sl=1)
        self.model.transfer_uv(sel[0],sel[1],0)

    # 世界位置传递UV
    def position_transfer_uv(self):
        sel = cmds.ls(sl=1)
        self.model.transfer_uv(sel[0], sel[1], 1)

    # 选择点修正UV
    def select_point_correct_uv(self):
        sel = cmds.ls(fl=1, sl=1)
        model = sel[0].split(".")
        mel.eval('polyPerformAction polyMapSew e 0;')
        cmds.u3dUnfold(sel, rs=0, ite=1, bi=1, p=0, ms=1024, tf=1)
        cmds.select(cl=1)
        cmds.select(model[0], r=1)
        cmds.DeleteHistory()
        cmds.warning('UV修正完成')

    # 测试模板
    def test_Template(self):
        mel.eval('file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;"  -pr  -importFrameRate true  -importTimeRange "override" "' + self.file_path_reverse + '/template.ma";')

    # 使用帮助
    def help(self):
        if QGuiApplication.keyboardModifiers() & Qt.ControlModifier:
            web = self.others_library.open_web(1)
            print('\n使用教程视频链接：\n'+web)
        print('按住ctrl点击帮助可打开使用教程视频链接。\n'
              '1.先选模板模型，再选要编辑的模型开始创建中间态模型（需要有wrap3d，模板里都给设置好了，包裹完了在里面直接按默认的导出就可以了）。\n'
              '2.导入中间态模型。\n'
              '3.先选源模型，再选中间态模型开始按拓扑传递UV（其实就是导入的中间态模型要有个uv）。\n'
              '4.先选中间态模型，再选目标模型开始传递UV（让他俩uv基本一致，不然无法按uv来进行变形传递）。\n'
              '5.选择点修正UV（只修改点飞出去的，一般要修自穿插的位置，例如嘴部，整体修到没有重叠就好了）。\n')

    # 不同拓扑传递变形
    def transfer_deformation(self):
        transmit_source = self.line_edit_1.text()  # 含变形模型
        intermediate_state = self.line_edit_2.text()  # 中间态模型
        transmit_target = self.line_edit_3.text()  # 变形传递目标
        self.blendshape.transfer_different_topologies_bs(transmit_source, transmit_target, intermediate_state)

    # 按UV复制权重
    def copy_weights_by_uv(self):
        transmit_source = self.line_edit_1.text()  # 含变形模型
        transmit_target = self.line_edit_3.text()  # 变形传递目标
        soure_ui = cmds.polyUVSet(transmit_source, q=1, auv=1)
        target_ui = cmds.polyUVSet(transmit_target, q=1, auv=1)
        self.weight.base_copy_joint_weight('UV', transmit_source, [transmit_target], soure_ui[0], target_ui[0])

    # 加载的bs自动k帧
    def bs_auto_k_frame(self):
        bs_name = self.line_edit_5.text()
        bs_name = bs_name.split(',')
        num = float(self.line_edit_7.text())
        self.blendshape.bs_auto_k_frame(bs_name, num)

    # 绘制bs权重
    def darw_bs_weight(self):
        mel.eval('ArtPaintBlendShapeWeightsTool;')

    # 烘焙当前范围帧
    def back_frame(self):
        model = self.line_edit_4.text()
        self.blendshape.back_frame(model)

    # 分解bs
    def split_bs(self):
        soure = self.line_edit_8.text()
        bs = self.line_edit_9.text()
        bs = bs.split(',')
        target = self.line_edit_10.text()
        self.blendshape.split_bs(soure, bs, target)

window = Window()
if __name__ == '__main__':
    window.show()

