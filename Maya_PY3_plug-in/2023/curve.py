# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
# 获取文件路径
import os
import sys
import inspect
import importlib
import maya.OpenMaya as OpenMaya
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version
# 库添加到系统路径
sys.path.append(library_path)

class CreateAndEditCurve:
    # 填写样条名称上传
    def upload_file_by_name(self,name, file):
        Curve = cmds.ls(sl=1)
        if Curve:
            if os.path.exists(file + '/' + name + '.jpg'):
                os.remove(file + '/' + name + '.jpg')
            if os.path.exists(file + '/' + name + '.txt'):
                os.remove(file + '/' + name + '.txt')
            ShowGrid = 0
            if cmds.optionVar(query='showGrid') == 1:
                mel.eval('ToggleGrid;')
                ShowGrid = 1
            cmds.select(cl=1)
            shape = cmds.listRelatives(Curve[0], s=1, type='nurbsCurve')
            cmds.select(shape)
            mel.eval('FrameSelectedInAllViews;')
            mel.eval('HideUnselectedObjects;')
            cmds.playblast(compression="jpg", format='image', viewer=0, frame=float(cmds.currentTime(q=1)),
                         widthHeight=(550, 550),percent=25,
                         filename=(file + '/' + name))
            cmds.select(shape)
            mel.eval('ShowLastHidden;')

            os.rename((file + '/' + name + '.0000.jpg'), (file + '/' + name + '.jpg'))

            file = open((file + '/' + name + '.txt'), 'w')
            shape = cmds.listRelatives(Curve[0], s=1, type='nurbsCurve')
            CurveDegree = cmds.getAttr(shape[0] + '.degree')
            CurveForm = cmds.getAttr(shape[0] + '.form')
            text = ''
            text = self.return_curve_command(Curve)
            file.write(text)
            if ShowGrid == 1:
                mel.eval('ToggleGrid;')
            cmds.select(Curve)
        else:
            cmds.error('请选择样条')

    # 返回生成此样条的命令
    def return_curve_command(self,curve):
        cmds.select((curve[0] + ".cv[0:]"), r=1)
        Point = cmds.ls(fl=1, sl=1)
        shape = cmds.listRelatives(curve[0], s=1, type='nurbsCurve')
        curveDegree = cmds.getAttr(shape[0] + '.degree')
        curveForm = cmds.getAttr(shape[0] + '.form')
        AllP = ''
        if curveForm == 2:
            AllP = AllP + '-per on '
        for i in range(0, len(Point)):
            X = str(cmds.getAttr(shape[0] + ".controlPoints[" + str(i) + "].xValue"))
            Y = str(cmds.getAttr(shape[0] + ".controlPoints[" + str(i) + "].yValue"))
            Z = str(cmds.getAttr(shape[0] + ".controlPoints[" + str(i) + "].zValue"))
            Txt = ('-p ' + X + ' ' + Y + ' ' + Z + ' ')
            AllP = AllP + Txt
        if curveForm == 2:
            for i in range(0, curveDegree):
                X = str(cmds.getAttr(shape[0] + ".controlPoints[" + str(i) + "].xValue"))
                Y = str(cmds.getAttr(shape[0] + ".controlPoints[" + str(i) + "].yValue"))
                Z = str(cmds.getAttr(shape[0] + ".controlPoints[" + str(i) + "].zValue"))
                Txt = ('-p ' + X + ' ' + Y + ' ' + Z + ' ')
                AllP = AllP + Txt

        C1 = str(curve[0])
        sel1 = OpenMaya.MSelectionList()  # 创建空的选择列表
        sel1.add(C1)  # 把元素添加到选择列表
        selPath1 = OpenMaya.MDagPath()  # 创建空地址路径
        sel1.getDagPath(0, selPath1)  # 将sel的第0个赋予到地址selPath（C的地址给到selPath）

        address1 = OpenMaya.MFnNurbsCurve(selPath1)  # 将具体地址的样条给到nnn
        array1 = OpenMaya.MDoubleArray()  # 创建一空的个双阵列
        address1.getKnots(array1)  # 获取curve1的所有点k值给到array阵列

        AllK = ''
        for i in array1:
            Txt = ('-k ' + str(i) + ' ')
            AllK = AllK + Txt
        Print = ('curve -d ' + str(curveDegree) + ' ' + AllP + ' ' + AllK + ';')
        return Print

    # 创建样条
    # ZKM_CreateAndEditCurveClass().create_curve('X:\script\proj_sw7\Rig\ZhanKangMing\ZhanKangMing\Maya\MayaCommon\CurveShapeWithPicture','T')
    def create_curve(self,File,Name):
        with open(File + '\\' + Name + '.txt') as f:
            contents = f.readlines()
        mel.eval(contents[0])

    # 修正样条形状名称
    # ZKM_CreateAndEditCurveClass().ZKM_FixSplineShapeName(['nurbsCircle1'])
    def ZKM_FixSplineShapeName(self,curve):
        for C in curve:
            shape = cmds.listRelatives(C, s=1, type='nurbsCurve')
            cmds.rename(shape, (C + 'Shape'))

    # 选中改颜色
    def change_curve_color(self, colour_type, sel, color, num):
        if colour_type == 'RGB':
            for s in sel:
                shape = cmds.listRelatives(s, s=1, type='nurbsCurve')
                #cmds.setAttr(shape[0] + ".overrideEnabled", 0)
                #cmds.color(str(shape[0]), rgb=(Color[0], Color[1], Color[2]))
                cmds.setAttr(shape[0] + ".overrideEnabled", 1)
                cmds.setAttr(shape[0] + ".overrideDisplayType", 0)
                cmds.setAttr(shape[0] + '.overrideRGBColors', 1)
                cmds.setAttr(shape[0] + '.overrideColorR', color[0])
                cmds.setAttr(shape[0] + '.overrideColorG', color[1])
                cmds.setAttr(shape[0] + '.overrideColorB', color[2])
        if colour_type == 'Index':
            for s in sel:
                shape = cmds.listRelatives(s, s=1, type='nurbsCurve')
                # cmds.setAttr(shape[0] + ".overrideEnabled", 0)
                # cmds.color(str(shape[0]), rgb=(Color[0], Color[1], Color[2]))
                cmds.setAttr(shape[0] + ".overrideEnabled", 1)
                cmds.setAttr(shape[0] + ".overrideDisplayType", 0)
                cmds.setAttr(shape[0] + '.overrideRGBColors', 0)
                cmds.setAttr(shape[0] + '.overrideColor', num)

