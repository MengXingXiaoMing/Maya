# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

model = cmds.ls(sl=1)
all_joint = []
for m in model:
    HaveWeightSoure = pm.mel.findRelatedSkinCluster(m)
    if HaveWeightSoure:
        joint = pm.skinCluster(m, q=1, inf=1)
        all_joint.extend(joint)
cmds.select('C_rootBind_JNT')
top_joint = cmds.ls(sl=1)
all_joint.remove(top_joint[0])
cmds.select(all_joint,add=1)
print(cmds.ls(sl=1))

import json

# 字符串形式的Python列表
str_list = '[{"FK_sys": ["BaseRootJoint_M_FKGrp1", "BaseRootJoint_M_FKGrp2", "BaseRootJoint_M_FKCurve"]}, {"FK_sys": ["joint9_R_FKGrp1", "joint9_R_FKGrp2", "joint9_R_FKCurve"]}]'

# 使用json.loads将字符串解析为Python列表
python_list = json.loads(str_list)

# 打印转换后的Python列表
print(python_list)

if cmds.window('plug_in_Help_Window', ex=1):
    cmds.deleteUI('plug_in_Help_Window')
cmds.window('plug_in_Help_Window', t='帮助窗口')
cmds.columnLayout()
cmds.picture(image='Z:\\1.Private folder\\Rig\\zhankangming\\ZhanKangMing\\Maya_PY3_plug-in\\ui\\ZKM_plug_in_UI\\help.png')
cmds.showWindow()

weights = cmds.skinPercent('skinCluster1', 'pSphere1.vtx[280]', query=True, value=True)
print(weights)
# 获取对应的骨骼列表
influences = cmds.skinCluster('skinCluster1', query=True, influence=True)
print(influences)

# 输出权重信息
for weight, influence in zip(weights, influences):
    print(f"骨骼 {influence} 的权重是 {weight:.4f}")

import maya.cmds as cmds


def clean_render_layers():
    """
    Cleans up all render layers in the current Maya scene,
    leaving only the default render layer.
    """
    # Get the current scene's render setup
    render_setup = cmds.ls(type='renderSetup')
    if render_setup:
        render_setup = render_setup[0]  # Assuming there's only one render setup

        # Get all render layers in the render setup
        render_layers = cmds.ls(render_setup, type='renderLayer')

        # Iterate over all render layers except the default one
        for render_layer in render_layers:
            if render_layer != 'defaultRenderLayer':
                # Delete the render layer
                cmds.delete(render_layer)

                # Print a message to the Maya script editor
        print("Render layers have been cleaned.")
    else:
        print("No render setup found in the scene.")

    # Register the command to Maya's mel command list (optional)


# cmds.mel.eval('global proc string cleanRenderLayers() { python("clean_render_layers()"); }')

# Call the function to clean the render layers
clean_render_layers()


sel = cmds.ls(sl=1)
cube = cmds.polyCube(sz=1, sy=1, sx=1, d=1, cuv=4, h=1, ch=0, w=1, ax=(0, 1, 0))
print(cube[0])
face = cmds.ls(cube[0] + '.f[*]')
cmds.sets(face,name='need_delete_face')
cmds.polyUnite('pCube1','asd', centerPivot=1, ch=0, mergeUVSets=1, name='need_rename_cube')
face = cmds.sets('need_delete_face', q=1)
cmds.delete(face)
cmds.rename('need_rename_cube',sel[0])
cmds.delete('need_delete_face')
cmds.select(sel[0])
mel.eval('DeleteHistory;')




sel = cmds.ls(sl=1)
for s in sel:
    mesh_shape = cmds.listRelatives(s, s=1)
    point = cmds.ls((mesh_shape[0] + '.vtx[*]'), fl=1)
    skin_cluster = cmds.listConnections((mesh_shape[0] + '.inMesh'), d=1)
    SkinJoint = cmds.skinCluster(s, q=1, inf=1)
    for joint in SkinJoint:
        cmds.setAttr((joint + '.liw'), 0)
    # 按骨骼归一化
    for i in range(0,(len(SkinJoint)-1)):
        for p in point:
            weights = cmds.skinPercent(skin_cluster[0], p, query=True, value=True)
            weights_num = round(weights[i], 1)  # 取整数部分
            #print(skin_cluster[0])
            #print(p)
            #print(SkinJoint[i])
            #print(weights_num)
            #print(type(weights_num))
            cmds.skinPercent(skin_cluster[0], p, tv=(SkinJoint[i], weights_num))
        cmds.setAttr((SkinJoint[i] + '.liw'), 1)





    for p in point:
        weights = cmds.skinPercent(skin_cluster[0], p, query=True, value=True)
        max_value = max(weights)
        max_index = weights.index(max_value)
        print(max_value)


        text = ''
        for i in range(0,len(weights)):
            truncated_num = round(weights[0], 1)    # 取整数部分
            text = text + '-tv ' + weights[i] + ' ' + truncated_num + ' '
        # mel.eval('skinPercent '+-tv joint1 0.5 -tv joint2 0.5 +'skinCluster1 pSphere1.vtx[291];')
        pm.skinPercent('skinCluster1', 'pSphere1.vtx[291]', tv=('joint1', 0.5))
        print(weights)
        print(SkinJoint)


def CreateControllerPath(self):  # 创建路径和控制器
    global Attribute
    for Text in Attribute:  # Text=Attribute[0]
        oldNodes = pm.ls()
        pm.mel.performFileSilentImportAction(file_pathA + "/AttributeVisualizationNodeTemplate.mb")  # 导入文件
        newNodes = pm.ls()
        addNodes = [x for x in newNodes if x not in oldNodes]  # 筛选出新增的节点
        Source = str(pm.text('SourceText', q=1, l=1))  # 获取源
        textFieldGrpOld = str(pm.textFieldGrp(Text, q=1, l=1))  # 获取属性
        AttributeDefault = pm.attributeQuery(textFieldGrpOld, node=Source, ld=1)  # 获取默认值
        AttributeType = pm.attributeQuery(textFieldGrpOld, node=Source, attributeType=1)  # 获取属性类型
        AttributeMin = pm.attributeQuery(textFieldGrpOld, node=Source, minExists=1)  # 查询属性是否具有最小值
        AttributeMax = pm.attributeQuery(textFieldGrpOld, node=Source, maxExists=1)  # 查询属性是否具有最大值
        if (AttributeMin == 1):
            AttributeMin = 1
            GetAttributeMin = pm.attributeQuery(textFieldGrpOld, node=Source, min=1)  # 获取属性最大值
            GetAttributeMin = GetAttributeMin[0]
        else:
            AttributeMin = 0
            GetAttributeMin = 0
        if (AttributeMax == 1):
            AttributeMax = 1
            GetAttributeMax = pm.attributeQuery(textFieldGrpOld, node=Source, max=1)  # 获取属性最大值
            GetAttributeMax = GetAttributeMax[0]
        else:
            AttributeMax = 0
            GetAttributeMax = 0

        pm.curve(p=[(-6.847494044e-16, -3.398130212e-17, 1.000234865), (-6.847494044e-16, 0.5001174326, 0.8662283992),
                    (-6.847494044e-16, 0.8662283992, 0.5001174326), (-6.847494044e-16, 1.000234865, -1.581002666e-16),
                    (-6.847494044e-16, 0.8662283992, -0.5001174326), (-6.847494044e-16, 0.5001174326, -0.8662283992),
                    (-6.847494044e-16, -3.398130212e-17, -1.000234865),
                    (-6.847494044e-16, -0.5001174326, -0.8662283992), (-6.847494044e-16, -0.8662283992, -0.5001174326),
                    (-6.847494044e-16, -1.000234865, -1.581002666e-16), (-6.847494044e-16, -0.8662283992, 0.5001174326),
                    (-6.847494044e-16, -0.5001174326, 0.8662283992), (-6.847494044e-16, -3.398130212e-17, 1.000234865),
                    (0.7072730748, -3.398130212e-17, 0.7072730748), (1.000234865, -3.398130212e-17, -1.581002666e-16),
                    (0.7072730748, -3.398130212e-17, -0.7072730748), (-6.847494044e-16, -3.398130212e-17, -1.000234865),
                    (-0.7072730748, -3.398130212e-17, -0.7072730748),
                    (-1.000234865, -3.398130212e-17, -1.581002666e-16), (-0.8662283992, 0.5001174326, -1.581002666e-16),
                    (-0.5001174326, 0.8662283992, -1.581002666e-16), (-6.847494044e-16, 1.000234865, -1.581002666e-16),
                    (0.5001174326, 0.8662283992, -1.581002666e-16), (0.8662283992, 0.5001174326, -1.581002666e-16),
                    (1.000234865, -3.398130212e-17, -1.581002666e-16), (0.8662283992, -0.5001174326, -1.581002666e-16),
                    (0.5001174326, -0.8662283992, -1.581002666e-16), (-6.847494044e-16, -1.000234865, -1.581002666e-16),
                    (-0.5001174326, -0.8662283992, -1.581002666e-16), (-0.8662283992, -0.5001174326, -1.581002666e-16),
                    (-1.000234865, -3.398130212e-17, -1.581002666e-16), (-0.7072730748, -3.398130212e-17, 0.7072730748),
                    (-6.847494044e-16, -3.398130212e-17, 1.000234865)],
                 d=1, n=(Source + '_' + textFieldGrpOld + '_Curve'))
        pm.group(n=(Source + '_' + textFieldGrpOld + '_Curve_Grp'))

        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.ty'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.tz'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.rx'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.ry'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.rz'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.sx'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.sy'),
                   lock=True, channelBox=False, keyable=False)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.sz'),
                   lock=True, channelBox=False, keyable=False)
        pm.connectAttr((Source + '_' + textFieldGrpOld + '_Curve.tx'),
                       'name_decomposeMatrix_Main.Translate', f=1)
        pm.connectAttr((Source + '_' + textFieldGrpOld + '_Curve.inverseMatrix'),
                       'name_decomposeMatrix_Main.inputMatrix', f=1)
        pm.connectAttr('name_decomposeMatrix_Main.OutTranslate',
                       (Source + '_' + textFieldGrpOld + '_Curve_Grp.tx'),
                       f=1)
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.translateX'), 0)  # 设置默认值
        pm.mel.eval("transformLimits -tx" + " " + str(AttributeMin) + " " + str(AttributeMax) + " -etx " + str(
            GetAttributeMin) + " " + str(GetAttributeMax) + " " + (Source + '_' + textFieldGrpOld + '_Curve') + ";")
        pm.transformLimits((Source + '_' + textFieldGrpOld + '_Curve'), etx=(AttributeMin, AttributeMax),
                           tx=(GetAttributeMin, GetAttributeMax))  # 设置最大最小值
        pm.connectAttr((Source + '_' + textFieldGrpOld + '_Curve.translateX'), (Source + '.' + textFieldGrpOld), f=1)
        Normal = pm.getAttr((Source + '.' + textFieldGrpOld), 1)  # 获取默认值
        '''if AttributeMin == 1:
            pm.disconnectAttr('name_Negative_direction_range.output1D', 'name_Negative_direction_condition.colorIfTrueR')
        if AttributeMax == 1:
            pm.disconnectAttr('name_Positive_direction_condition.outColorR', 'name_Negative_direction_condition.colorIfFalseR')'''
        # 对对应控制器进行对应的修改pm.setAttr('name_Negative_direction_condition.colorIfFalseR', 0)
        # print(AttributeType)
        # print(textFieldGrpOld+'AttributeType')

        if (AttributeType == 'double'):  # 浮点
            pm.group((Source + '_' + textFieldGrpOld + '_Curve_Grp'),
                     n=(Source + '_' + textFieldGrpOld + '_Curve_AllGrp'))
        if (AttributeType == 'long' or AttributeType == 'bool' or AttributeType == 'enum'):  # 整形#布尔#字符
            if (AttributeMin == 0):
                GetAttributeMin = -10
            if (AttributeMax == 0):
                GetAttributeMax = 10
            pm.transformLimits((Source + '_' + textFieldGrpOld + '_Curve_Grp'), etx=(1, 1),
                               tx=(GetAttributeMin, GetAttributeMax))

            pm.connectAttr('name_decomposeMatrix_Main.Int', (Source + '_' + textFieldGrpOld + '_Curve_Grp.translateX'),
                           f=1)  # 链接到整数
            pm.select((Source + '_' + textFieldGrpOld + '_Curve'))
            pm.group(n=(Source + '_' + textFieldGrpOld + '_Curve_IntGrp'))
            pm.connectAttr('name_decomposeMatrix_Main.outputTranslateX',
                           (Source + '_' + textFieldGrpOld + '_Curve_IntGrp.translateX'), f=1)  # 链接到创建的int组
            pm.addAttr((Source + '_' + textFieldGrpOld + '_Curve'), ln="int", dv=0, at='long')
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.int'), e=1, keyable=True)
            pm.connectAttr('name_decomposeMatrix_Main.Int', (Source + '_' + textFieldGrpOld + '_Curve.int'),
                           f=1)  # 添加属性并链接
            pm.group((Source + '_' + textFieldGrpOld + '_Curve_Grp'),
                     n=(Source + '_' + textFieldGrpOld + '_Curve_AllGrp'))

        if (AttributeType == 'enum'):  # 字符
            EnumStr = pm.attributeQuery(textFieldGrpOld, node=Source, listEnum=1)
            EnumStr = EnumStr[0]
            pm.select(cl=1)
            pm.group(em=1, n=(Source + '_EnumText' + textFieldGrpOld + '_Curve_Grp'))
            EnumStr = EnumStr.split(":")  # 文件名称
            for EnumText in EnumStr:
                self.EnumCreateTxtCurve(EnumText, textFieldGrpOld)
                pm.parent((Source + '_Enum_' + textFieldGrpOld + EnumText),
                          (Source + '_EnumText' + textFieldGrpOld + '_Curve_Grp'))
            TextLong = 0
            for TrX in range(1, len(EnumStr)):
                # trX = (trX + len(EnumStr[TrX-1]))
                TextLong = (TextLong + len(str(EnumStr[TrX - 1])))
                pm.setAttr((Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '.translateX'),
                           (TextLong * 0.8))  # 设置大小
            for TrX in range(0, len(EnumStr)):
                # 调整颜色
                pm.setAttr((Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '.overrideEnabled'), 1)  # 打开对应的颜色属性
                pm.shadingNode('condition', asUtility=1,
                               n=(Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '_condition'))  # 建立条件
                pm.setAttr((Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '_condition.colorIfFalseR'),
                           2)  # 设置颜色显示
                pm.setAttr((Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '_condition.secondTerm'),
                           TrX)  # 设置值为多少时显示
                pm.connectAttr('name_decomposeMatrix_Main.Int',
                               (Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '_condition.firstTerm'),
                               f=1)  # 链接整形
                pm.connectAttr((Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '_condition.outColorR'),
                               (Source + '_Enum_' + textFieldGrpOld + EnumStr[TrX] + '.overrideDisplayType'),
                               force=1)  # 链接到颜色
            pm.setAttr((Source + '_EnumText' + textFieldGrpOld + '_Curve_Grp.translateY'), 1.5)
            pm.parent((Source + '_EnumText' + textFieldGrpOld + '_Curve_Grp'),
                      (Source + '_' + textFieldGrpOld + '_Curve_AllGrp'))  # 把额外生成的补进组里
        for rename in addNodes:
            pm.select(rename, r=1)
            pm.mel.searchReplaceNames('name', (Source + '_' + textFieldGrpOld), 'selected')
        pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.translateX'), AttributeDefault[0])  # 设置默认值

    RouteMax = ()
    RouteMin = ()
    '''if (AttributeMin == 1):
        RouteMin = GetAttributeMin
    else:
        RouteMin = AttributeDefault
    if (AttributeMax == 1):
        RouteMax = GetAttributeMax
    else:
        RouteMax = AttributeDefault
    if (AttributeMin == 0 and AttributeMax == 1):#判断模式开始创建从默认值到最大值的曲线
        print('asd')
    if (AttributeMin == 1 and AttributeMax == 0):#判断模式开始创建从最小值到默认值的曲线
        print('asd')
    pm.curve(p=[(RouteMin, 0, 0), (RouteMax, 0, 0)], d=1)'''


from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide2.QtGui import QScreen
from PySide2.QtCore import Qt, QPoint
import sys


class PopupWindow(QWidget):
    def __init__(self, parent=None, pos=QPoint()):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
        self.initUI(pos)

    def initUI(self, pos):
        layout = QVBoxLayout(self)
        label = QLabel("Popup Window Near Mouse", self)
        layout.addWidget(label)

        # 将窗口移动到指定的位置
        self.move(pos)
        self.show()


def create_popup_near_mouse():
    # 获取鼠标的屏幕坐标
    cursor = QApplication.primaryScreen().mapFromGlobal(QApplication.desktop().cursor().pos())

    # 计算窗口位置以确保它在屏幕上可见
    screen_geometry = QApplication.primaryScreen().geometry()
    window_width = 200
    window_height = 100
    x = max(0, cursor.x() - window_width // 2)
    y = max(0, cursor.y() - window_height // 2)
    x = min(x, screen_geometry.width() - window_width)
    y = min(y, screen_geometry.height() - window_height)

    # 创建并显示窗口
    popup = PopupWindow(pos=QPoint(x, y))


# 创建应用并运行
app = QApplication(sys.argv)

# 假设在某个事件（如按钮点击）中调用 create_popup_near_mouse 函数
create_popup_near_mouse()

sys.exit(app.exec_())