# coding=gbk
import pymel.core as pm
import os
import maya.OpenMaya as OpenMaya
class ZKM_CreateAndEditCurveClass:
    # 填写样条名称上传
    # ZKM_CreateAndEditCurveClass().ZKM_UploadFileByName('a', 'X:/script/proj_sw7/Rig/ZhanKangMing/ZhanKangMing/Maya/MayaCommon/CurveShapeWithPicture')
    def ZKM_UploadFileByName(self,Name, File):
        Curve = pm.ls(sl=1)
        if Curve:
            if os.path.exists(File + '/' + Name + '.jpg'):
                os.remove(File + '/' + Name + '.jpg')
            if os.path.exists(File + '/' + Name + '.txt'):
                os.remove(File + '/' + Name + '.txt')
            ShowGrid = 0
            if pm.optionVar(query='showGrid') == 1:
                pm.mel.ToggleGrid()
                ShowGrid = 1
            pm.select(cl=1)
            shape = pm.listRelatives(Curve[0], s=1, type='nurbsCurve')
            pm.select(shape)
            pm.mel.FrameSelectedInAllViews()
            pm.mel.HideUnselectedObjects()
            pm.playblast(compression="jpg", format='image', viewer=0, frame=float(pm.currentTime(q=1)),
                         widthHeight=(550, 550),percent=25,
                         filename=(File + '/' + Name))
            pm.select(shape)
            pm.mel.ShowLastHidden()

            os.rename((File + '/' + Name + '.0000.jpg'), (File + '/' + Name + '.jpg'))

            file = open((File + '/' + Name + '.txt'), 'w')
            shape = pm.listRelatives(Curve[0], s=1, type='nurbsCurve')
            CurveDegree = pm.getAttr(shape[0] + '.degree')
            CurveForm = pm.getAttr(shape[0] + '.form')
            text = ''
            text = self.ZKM_ReturnCurveCommand(Curve)
            file.write(text)
            if ShowGrid == 1:
                pm.mel.ToggleGrid()
            pm.select(Curve)
        else:
            pm.error('请选择样条')

    # 返回生成此样条的命令
    # print (ZKM_CreateAndEditCurveClass().ZKM_ReturnCurveCommand(['nurbsCircle1']))
    def ZKM_ReturnCurveCommand(self,Curve):
        pm.select((Curve[0] + ".cv[0:]"), r=1)
        Point = pm.ls(fl=1, sl=1)
        shape = pm.listRelatives(Curve[0], s=1, type='nurbsCurve')
        CurveDegree = pm.getAttr(shape[0] + '.degree')
        CurveForm = pm.getAttr(shape[0] + '.form')
        AllP = ''
        if CurveForm == 2:
            AllP = AllP + '-per on '
        for i in range(0, len(Point)):
            X = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].xValue"))
            Y = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].yValue"))
            Z = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].zValue"))
            Txt = ('-p ' + X + ' ' + Y + ' ' + Z + ' ')
            AllP = AllP + Txt
        if CurveForm == 2:
            for i in range(0, CurveDegree):
                X = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].xValue"))
                Y = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].yValue"))
                Z = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].zValue"))
                Txt = ('-p ' + X + ' ' + Y + ' ' + Z + ' ')
                AllP = AllP + Txt

        C1 = str(Curve[0])
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
        Print = ('curve -d ' + str(CurveDegree) + ' ' + AllP + ' ' + AllK + ';')
        return Print

    # 创建样条
    # ZKM_CreateAndEditCurveClass().ZKM_CreateCurve('X:\script\proj_sw7\Rig\ZhanKangMing\ZhanKangMing\Maya\MayaCommon\CurveShapeWithPicture','T')
    def ZKM_CreateCurve(self,File,Name):
        with open(File + '\\' + Name + '.txt') as f:
            contents = f.readlines()
        pm.mel.eval(contents[0])

    # 修正样条形状名称
    # ZKM_CreateAndEditCurveClass().ZKM_FixSplineShapeName(['nurbsCircle1'])
    def ZKM_FixSplineShapeName(self,Curve):
        for C in Curve:
            shape = pm.listRelatives(C, s=1, type='nurbsCurve')
            pm.rename(shape, (C + 'Shape'))

    # 选中改颜色
    # ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(['nurbsCircle1'],[1,1,1])
    def ZKM_ChangeCurveColor(self,Sel,Color):
        for s in Sel:
            shape = pm.listRelatives(Sel[0], s=1, type='nurbsCurve')
            pm.setAttr(str(s) + ".overrideEnabled", 0)
            pm.setAttr(shape[0] + ".overrideEnabled", 0)
            pm.color(str(s), rgb=(Color[0], Color[1], Color[2]))

