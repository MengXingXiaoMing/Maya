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
# channelBox -e -remove "ffd1" "mainChannelBox";

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
        self.setWindowTitle('通用附着版卷轴(Maya'+self.maya_version+')')
        # 提取年月日、时分秒，并转换成数字
        now = datetime.now()
        milliseconds = now.microsecond // 1000  # 将微秒转换为毫
        # 如果你想要一个包含毫秒的字符串表示
        self.time_str = now.strftime("%Y%m%d%H%M%S") + f"{milliseconds:03d}"
        self.setObjectName('ZKM_deform_edit_window' + self.time_str)
        self.deform = []
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

        self.others_library = OthersLibrary()
        self.curve = CreateAndEditCurve()
        self.controller = CurveControllerEdit()



    def create_widgets(self):
        # 第一行
        # 列表视图 - 使用QListWidget更简单
        self.list_widget_1 = QtWidgets.QListWidget()
        # 设置选择模式为单选
        self.list_widget_1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 禁止双击编辑：设置编辑触发器为NoEditTriggers
        self.list_widget_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置选择行为，确保单击即可选择
        self.list_widget_1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)

        # 在 list_widget_2 之前添加模式切换控件

        # 第一行
        # 列表视图 - 使用QListWidget更简单
        self.list_widget_1 = QtWidgets.QListWidget()
        # 设置选择模式为单选
        self.list_widget_1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 禁止双击编辑：设置编辑触发器为NoEditTriggers
        self.list_widget_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置选择行为，确保单击即可选择
        self.list_widget_1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)

        self.list_widget_2 = QtWidgets.QListWidget()
        # 设置选择模式为单选
        # self.list_widget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 修改这里：设置选择模式为多选（支持Shift和Ctrl键）
        self.list_widget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # 禁止双击编辑：设置编辑触发器为NoEditTriggers
        self.list_widget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置选择行为，确保单击即可选择
        self.list_widget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.txt1 = QtWidgets.QLabel('按顺序选择骨骼点击创建，自行处理总控制器和约束总组')

        self.button_2 = QtWidgets.QPushButton('创建卷曲')


    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        h_box_layout = QtWidgets.QHBoxLayout(self.central_widget)
        h_box_layout.setContentsMargins(0, 0, 0, 0)
        h_box_layout.setSpacing(1)

        v_box_layout_0 = QtWidgets.QVBoxLayout(self)



        # v_box_layout_0.addWidget(self.list_widget_1)
        # v_box_layout_0.addWidget(self.list_widget_2)
        h_box_layout.addLayout(v_box_layout_0)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        h_box_layout.addLayout(main_layout)
        # 列表视图

        # 第一行
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(h_Box_layout_1)
        h_Box_layout_1.setSpacing(1)

        # self.list_view = QtWidgets.QListView(self)
        # self.list_model = QtGui.QStandardItemModel(self.list_view)
        # self.list_view.setModel(self.list_model)
        # main_layout.addWidget(self.list_view)

        h_Box_layout_2 = QtWidgets.QVBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)

        h_Box_layout_3 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_2.addLayout(h_Box_layout_3)
        main_layout.addWidget(self.txt1)

        main_layout.addWidget(self.button_2)
        # 置顶

    def create_connect(self):
        self.button_2.clicked.connect(self.create)  # 选择拷贝源按钮

    @Withdraw
    def  create (self):
        # 默认参数
        use_reverse = True
        amplitude_forward = 100.0
        decay_forward = 0.0
        axis_forward = 2  # Z
        amplitude_reverse = -100.0
        decay_reverse = 0.0
        axis_reverse = 2  # Z

        sel = cmds.ls(sl=1)
        re_all_curve = []
        reverse = False
        top_curve = cmds.circle(ch=0, n='scroll_top_curve')

        re_all_curve, all_grp1, all_loc, independence_controller, root_bone, top_grp = self.create_scroll(
            sel, re_all_curve, reverse, top_curve,
            amplitude=amplitude_forward,
            decay=decay_forward,
            axis=axis_forward
        )
        group1 = cmds.group(em=1, name='scroll_group')
        cmds.parent(all_grp1 [0], all_loc[0], group1)
        cmds.select(cl=1)

        if use_reverse:
            sel = re_all_curve
            reverse = True
            se_re_all_curve, se_all_grp1, se_all_loc, se_independence_controller, se_root_bone, se_top_grp = self.create_scroll(
                sel, re_all_curve, reverse, top_curve,
                amplitude=amplitude_reverse,
                decay=decay_reverse,
                axis=axis_reverse
            )
            group2 = cmds.group(em=1, name='scroll_group_reverse')
            cmds.parent(se_all_grp1 [0], se_all_loc [0], group2)
            group = cmds.group(em=1, name='scroll_all_group')
            cmds.parent(group1, group2, group)
            if se_top_grp:
                cmds.parent(se_top_grp, group)
            
        else:
            cmds.rename(group1, 'scroll_all_group')
        
    def create_scroll(self, sel, re_all_curve, reverse, top_curve, amplitude=100.0, decay=100.0, axis=2):
        cmds.select(cl=1)
        all_grp1 = []
        all_grp2 = []
        all_curve = []
        all_loc = []


        # 创建总控制器
        if reverse == False:
            move_an = 'move_Forward'
            add_text = '_'
            color_num = 17
            radius = 1
        else:
            sel = sel[::-1]
            move_an = 'move_reverse'
            add_text = '_F_'
            color_num = 18
            radius = 0.5

        cmds.addAttr(top_curve, ln=move_an, at='double', min=0, max=len(sel),  dv=0)
        cmds.setAttr(top_curve[0]+'.'+move_an, e=1, keyable=1)

        # 根据方向创建振幅倍率、递减系数和轴向选择属性
        suffix = 'Forward' if not reverse else 'reverse'
        amplitude_attr = 'amplitude_' + suffix
        decay_attr = 'decay_' + suffix
        axis_attr = 'axis_' + suffix
        cmds.addAttr(top_curve, ln=amplitude_attr, at='double', dv=100)
        cmds.setAttr(top_curve[0]+'.'+amplitude_attr, e=1, keyable=1)
        cmds.addAttr(top_curve, ln=decay_attr, at='double', min=0)
        cmds.setAttr(top_curve[0]+'.'+decay_attr, e=1, keyable=1)
        cmds.addAttr(top_curve, ln=axis_attr, at='enum', en='X:Y:Z', dv=2)
        cmds.setAttr(top_curve[0]+'.'+axis_attr, e=1, keyable=1)
        # 使用 UI 传入的初始值
        cmds.setAttr(top_curve[0]+'.'+amplitude_attr, amplitude)
        cmds.setAttr(top_curve[0]+'.'+decay_attr, decay)
        cmds.setAttr(top_curve[0]+'.'+axis_attr, axis)

        # 创建正向控制器
        for i in range(len(sel)):
            # 创建控制器
            curve = cmds.circle(ch=1, r=radius, nr=(1,0,0), name=sel[i]+add_text+'curve')
            # 修改控制器颜色
            self.curve.change_curve_color('Index', [curve[0]], 0, color_num)
            # 每个 FK 控制器上添加驱动旋转数值属性
            cmds.addAttr(curve, ln='drive', at='double', dv=60, min=0)
            cmds.setAttr(curve[0]+'.drive', e=1, keyable=1)
            grp2 = cmds.group(em=1, name=sel[i]+add_text+'grp2')
            cmds.parent(curve[0],grp2)
            grp1 = cmds.group(em=1, name=sel[i]+add_text+'grp1')
            cmds.parent(grp2,grp1)
            print(grp1)
            print(sel[i])
            cmds.delete(cmds.parentConstraint(sel[i],grp1))
            all_grp1.append(grp1)
            all_grp2.append(grp2)
            all_curve.append(curve)
            re_all_curve.append(curve[0])
            # 创建定位器
            loc = cmds.spaceLocator(name=sel[i]+add_text+'_loc')
            cmds.parentConstraint(sel[i],loc)
            all_loc.append(loc[0])
        cmds.setAttr(all_loc[0]+'.visibility', 0)

        # 添加显示隐藏属性
        cmds.addAttr(top_curve, ln=move_an+'_FK_controller', at='bool')
        cmds.setAttr(top_curve[0]+'.'+move_an+'_FK_controller', e=1, keyable=1)
        cmds.setAttr(top_curve[0]+'.'+move_an+'_FK_controller', 1)
        cmds.connectAttr(top_curve[0]+'.'+move_an+'_FK_controller', all_grp1[0]+'.visibility')
        # 父化
        for i in range(1, len(sel)):
            cmds.parent(all_grp1[i], all_curve[i-1][0])
            cmds.parent(all_loc[i], all_loc[i-1])

        # 添加过渡
        for i in range(len(sel)):
            # 创建重映射驱动
            setRange = cmds.createNode("setRange")
            cmds.connectAttr(top_curve[0]+'.'+move_an, setRange+".valueX")
            for x in ['.t','.r','.s']:
                remapValue = cmds.createNode("remapValue")
                an = remapValue+'.color[0].color_Color'
                cmds.connectAttr(all_loc[i]+x, an)
                cmds.connectAttr(remapValue+'.outColor', all_grp1[i]+x)
                cmds.connectAttr(setRange+'.outValueX', remapValue+".inputValue")
                for j in [['x','R'],['y','G'],['z','B']]:
                    num = cmds.getAttr(all_loc[i]+x+j[0])
                    cmds.setAttr(remapValue+'.color[1].color_Color'+j[1],num)
                # 链接重映射
                cmds.setAttr(setRange+".maxX", 1)
                cmds.setAttr(setRange+".oldMinX", len(sel)-1-i)
                cmds.setAttr(setRange+".oldMaxX", len(sel)-i)
            
            # 旋转驱动（每个 FK 控制器独立的 drive 属性）
            # mult_node.input1X = setRange.outValueX（0→1 激活比例）
            # mult_node.input2X = 控制器 drive 属性
            mult_node = cmds.createNode('multiplyDivide', name=sel[i]+add_text+'curl_amp')
            cmds.connectAttr(setRange+'.outValueX', mult_node+'.input1X')
            cmds.connectAttr(all_curve[i][0]+'.drive', mult_node+'.input2X')

            # 递减：输出 = 驱动值 - 递减量
            # 末尾关节减 0，向前依次加码（len(sel)-1-i）
            # 递减量 × setRange.outValueX（激活比例）避免初始预旋转
            decay_mult_node = cmds.createNode('multiplyDivide', name=sel[i]+add_text+'curl_decay')
            cmds.connectAttr(top_curve[0]+'.'+decay_attr, decay_mult_node+'.input1X')
            cmds.setAttr(decay_mult_node+'.input2X', len(sel) - 1 - i)

            effective_decay = cmds.createNode('multiplyDivide', name=sel[i]+add_text+'curl_eff_decay')
            cmds.connectAttr(decay_mult_node+'.outputX', effective_decay+'.input1X')
            cmds.connectAttr(setRange+'.outValueX', effective_decay+'.input2X')

            pma_node = cmds.createNode('plusMinusAverage', name=sel[i]+add_text+'curl_sub')
            cmds.setAttr(pma_node+'.operation', 2)  # subtract
            cmds.connectAttr(mult_node+'.outputX', pma_node+'.input1D[0]')
            cmds.connectAttr(effective_decay+'.outputX', pma_node+'.input1D[1]')

            # 钳制：不小于 0，防止负旋转
            clamp_node = cmds.createNode('clamp', name=sel[i]+add_text+'curl_clamp')
            cmds.connectAttr(pma_node+'.output1D', clamp_node+'.inputR')
            cmds.setAttr(clamp_node+'.minR', 0)
            cmds.setAttr(clamp_node+'.maxR', 999999)

            # 倍率：钳制后 × amplitude * 0.01
            amp_scale_node = cmds.createNode('multiplyDivide', name=sel[i]+add_text+'curl_amp_scale')
            cmds.connectAttr(top_curve[0]+'.'+amplitude_attr, amp_scale_node+'.input1X')
            cmds.setAttr(amp_scale_node+'.input2X', 0.01)

            amp_out_node = cmds.createNode('multiplyDivide', name=sel[i]+add_text+'curl_amp_out')
            cmds.connectAttr(clamp_node+'.outputR', amp_out_node+'.input1X')
            cmds.connectAttr(amp_scale_node+'.outputX', amp_out_node+'.input2X')
            
            # 根据轴向枚举路由到对应 rotate 属性（实时切换）
            for axis_idx, axis_name in enumerate(['X', 'Y', 'Z']):
                cond = cmds.createNode('condition', name=sel[i]+add_text+'curl_axis_'+axis_name)
                cmds.setAttr(cond+'.operation', 0)  # 等于
                cmds.connectAttr(top_curve[0]+'.'+axis_attr, cond+'.firstTerm')
                cmds.setAttr(cond+'.secondTerm', axis_idx)
                cmds.connectAttr(amp_out_node+'.outputX', cond+'.colorIfTrueR')
                cmds.setAttr(cond+'.colorIfFalseR', 0)
                cmds.connectAttr(cond+'.outColorR', all_grp2[i]+'.rotate'+axis_name)
        
        # 添加独立控制器（仅在反向时创建）
        independence_controller = []
        root_bone = None
        top_grp = None
        if reverse != False:
            # 创建总骨骼
            cmds.select(cl=1)
            root_bone = cmds.joint(name='scroll_reverse_root')
            cmds.setAttr(root_bone+'.drawStyle', 2)
            #创建总控制器组
            top_grp = cmds.group(em=1, name='scroll_reverse_top_grp')
            # 添加显示隐藏属性
            cmds.addAttr(top_curve, ln='independence_controller', at='bool')
            cmds.setAttr(top_curve[0]+'.independence_controller', e=1, keyable=1)
            cmds.setAttr(top_curve[0]+'.independence_controller', 1)
            cmds.connectAttr(top_curve[0]+'.independence_controller', top_grp+'.visibility')
            for i in range(len(sel)):
                # 创建半径 0.3 的独立控制器
                curve = cmds.circle(ch=0, r=0.3, nr=(1,0,0), name=sel[i]+'_'+str(i)+'_curve')
                self.curve.change_curve_color('Index', [curve[0]], 0, color_num+2)
                grp2 = cmds.group(em=1, name=sel[i]+'_'+str(i)+'_grp1')
                cmds.parent(curve[0], grp2)
                grp1 = cmds.group(em=1, name=sel[i]+'_'+str(i)+'_grp2')
                cmds.parent(grp2, grp1)
                cmds.parentConstraint(all_curve[i][0], grp1)
                cmds.scaleConstraint(all_curve[i][0], grp1)
                # cmds.parent(grp1, all_curve[i][0])
                cmds.parent(grp1, top_grp)
                independence_controller.append(grp1)

                # 创建独立骨骼并挂到总骨骼下
                cmds.select(cl=1)
                bone = cmds.joint(name=sel[i]+'_'+str(i)+'_bone')
                cmds.parent(bone, root_bone)
                # 独立控制器约束对应骨骼
                cmds.parentConstraint(curve[0], bone)
                cmds.scaleConstraint(curve[0], bone)
            

        return re_all_curve, all_grp1, all_loc, independence_controller, root_bone, top_grp




    
    # 独立控制器


window = Window()
if __name__ == '__main__':
    window.show()

