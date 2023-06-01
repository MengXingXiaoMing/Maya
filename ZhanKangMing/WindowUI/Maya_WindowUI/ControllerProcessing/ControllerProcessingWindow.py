#coding=gbk
import maya.OpenMaya as OpenMaya
import pymel.core as pm
import random
import os
import sys
import inspect
import maya.cmds as cmds

#��Ŀ¼
sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
#���ؼ����ļ�������غ�׺���ļ����ƣ�ȡ����ֵ��
sys.path.append(ZKM_RootDirectory+'\\Common\\CommonLibrary')
from LoadCorrespondingSuffixFile import *
# �����ı�
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
# ë��Լ��
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaCommon')
class PresetTemplateWindowClass:
    def __init__(self):
        # ͨ��self���½��Ķ����г�ʼ������
        global file_path
        global file_pathA
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        # print(file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathReversion = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
        cur_dirB = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathTop = os.path.join(cur_dirB)  # ��ȡ��λ��
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
        self.file_pathTop = file_pathTop
    def WindowControllerProcessing(self):
        if pm.window('WindowControllerProcessingA', ex=1):
            pm.deleteUI('WindowControllerProcessingA')
        pm.window('WindowControllerProcessingA', s=1, t="����������")
        pm.rowColumnLayout(nc=2)
        pm.formLayout("WindowControllerProcessingFrom",w=295,h=820)
        pm.rowColumnLayout("WindowControllerProcessingWindow", nc=1, adj=8)
        pm.rowColumnLayout(nc=2, adj=2)
        pm.floatSliderGrp('WindowControllerProcessingControllerSizeFloatSliderGrp', fmx=9999999, min=0.1,
                          cc='ScaleController()', max=2, cw3=(55, 40, 92),f=1, l="��������С", v=1.00)
        pm.button(c='ModifyControllerShapeTRS(\'SoftSelectionSize\', 0, 0, 0)', l="��������ѡ���С")
        pm.setParent('..')
        pm.rowColumnLayout(cs=[(1, 3), (2, 10), (4, 10)], nc=4, adj=8)
        pm.text(l="����")
        pm.rowColumnLayout(columnWidth=[(1, 40), (2, 40), (3, 40)], numberOfColumns=6)
        pm.radioCollection('WindowControllerProcessingControllerOrientation')
        pm.radioButton('X', label="X")
        pm.radioButton('Y', label="Y")
        pm.radioButton('Z', label="Z")
        pm.radioCollection('WindowControllerProcessingControllerOrientation', edit=1, select="X")
        pm.setParent('..')
        pm.button(c='RotationController()', l="��ת")
        pm.checkBox('WindowControllerProcessingIgnoreEndBones_checkBox', value=1, label="����ĩ�˹���")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=8)
        # ��������״��
        pm.rowColumnLayout(nc=2, adj=2)
        pm.textFieldButtonGrp('WindowControllerProcessingUploadControllerFile', bl="��д�����ϴ�����", text="", cw3=(0, 100, 0), l='',
                              bc='GenerateRefreshWindow(\''+self.file_pathTop+'/Maya/MayaCommon/CurveShapeWithPicture\')')
        pm.button(l='ɾ����ѡ����',c='DeleteSelectedCurve(\''+self.file_pathTop+'/Maya/MayaCommon/CurveShapeWithPicture\')')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=1)
        pm.formLayout('WindowControllerProcessingAllControllerFormLayout',h=220)
        pm.rowColumnLayout('WindowControllerProcessingAllControllerFlowLayout',nc=5)
        pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection')
        AllTxtFile = os.listdir(self.file_pathTop+'\Maya\MayaCommon\CurveShapeWithPicture')  # �����ļ���
        for i in AllTxtFile:
            if os.path.splitext(i)[1] == '.txt':
                Name = os.path.splitext(i)[0]
                pm.iconTextRadioButton(Name,w=55,h=55,i1=(self.file_pathTop+'\Maya\MayaCommon\CurveShapeWithPicture'+"\\"+Name+'.jpg'),iol=Name)
        pm.setParent('..')
        pm.setParent('..')
        pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection',e=1,
                                   sl=pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, cia=1)[0])
        WindowControllerProcessingAllControllerSliderLineMax = len(AllTxtFile)/5/2*55-165
        if WindowControllerProcessingAllControllerSliderLineMax<0:
            WindowControllerProcessingAllControllerSliderLineMax=0.01
        pm.floatScrollBar("WindowControllerProcessingAllControllerSliderLine", hr=0, max=WindowControllerProcessingAllControllerSliderLineMax, min=0,
                          cc='Slider(\'WindowControllerProcessingAllControllerSliderLine\',\'WindowControllerProcessingAllControllerFlowLayout\',\'WindowControllerProcessingAllControllerFormLayout\',-1)')
        pm.setParent('..')
        # �Ŀ���������ɫ
        pm.button(c='asSwapCurve()', l="�Ŀ�����")
        pm.rowColumnLayout(nc=3, adj=4)
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',rgb=(0.127, 0.715, 1.000),cw2=(25,0))
        pm.intSlider('WindowControllerProcessingChangeCurveColor_intSlider',max=31, step=1, value=17, min=0,w=215,cc='DragSliderAutomaticallyModifyColorPanel()')
        pm.button(c='ChangeCurveColor()', l="����ɫ")
        pm.setParent('..')
        pm.intSliderGrp('WindowControllerProcessingNumberControllerGroups', min=1, max=10, cw3=(60, 40, 160), f=1, l="����������:", v=2)
        # ��д��׺�ʹ������
        pm.rowColumnLayout(nc=3, adj=8)
        pm.textFieldGrp('WindowControllerProcessingSuffix', text="", cw2=(25, 110), l="��׺")
        pm.rowColumnLayout(columnWidth=[(1, 27), (2, 27), (3, 27)], numberOfColumns=5)
        pm.radioCollection('WindowControllerProcessingJointMirror')
        pm.radioButton('X', label="X")
        pm.radioButton('Y', label="Y")
        pm.radioButton('Z', label="Z")
        pm.radioCollection('WindowControllerProcessingJointMirror', edit=1, select="X")
        pm.setParent('..')
        pm.button(c='MirrorJoint()', l="�������")
        pm.setParent('..')
        # �����ʼ����
        pm.rowColumnLayout(nc=2, adj=8)
        pm.intSliderGrp('WindowControllerProcessingJointNum', fmx=9999999, min=1, cc='IntSlider_Max_Edit_Controller(\'WindowControllerProcessingJointNum\')', max=100,
                        cw3=(0, 40, 140), f=1, l="", v=50)
        pm.button(c='GenerateBoneChain()', l="ѡ��������������")
        pm.setParent('..')
        pm.rowColumnLayout(cs=(2, 5), nc=3, adj=8)
        pm.button(c=lambda *args: pm.mel.detectionOfTheSameNameMain(), bgc=(0, 0.8, 0.8), l="ȥ���ظ�����")
        pm.checkBox('WindowControllerProcessingExtractConstraints', value=0, label="��ȡԼ��")
        pm.button('CHUANGJIANFK', c='ChuangJianFK()', l="ѡ����������ʼ����������")
        pm.setParent('..')
        pm.setParent('..')
        pm.flowLayout(wrap=1,columnSpacing=3,h=500)
        pm.button('CENTREJOINT', c='CreateCentreJoint()', l="����ѡ�����ߴ��̹���")
        pm.button(c=lambda *args: pm.mel.GetCurvePoint(), l="��ȡ��������ֵ")
        pm.button(c='ShowAxial()', l="��������")
        pm.button(c='JointTransformationCurve()', l="����ת����")
        pm.button(c=lambda *args: pm.mel.CreateCentreJoint(), l="�����߽���������")
        pm.button(c='ReversalArrangement()', l="��ת������Σ�������")
        pm.rowColumnLayout( adj=8, nc=3)
        pm.intSliderGrp('WindowControllerProcessingInterval', fmx=9999999, min=1, cc='IntSlider_Max_Edit_Controller(\'WindowControllerProcessingInterval\')', max=10,cw3=(0, 40, 100), f=1, l="", v=2)
        pm.button(c='InterlacedLineSelection("edgeRing")', l="����ѡ��")
        pm.button(c='InterlacedLineSelection("edgeLoop")', l="����ѡѭ����")
        pm.setParent('..')

        pm.rowColumnLayout(nc=2, adj=2, w=290)
        pm.intSliderGrp('WindowControllerProcessingInsertBone', fmx=9999999, min=1, cc='IntSlider_Max_Edit_Controller(\'WindowControllerProcessingInsertBone\')', max=10, cw3=(0, 40, 140),f=1, l="��������", v=5)
        pm.button(c='InsertJoint()', l="�������")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=2, w=290)
        pm.textFieldButtonGrp('WindowControllerProcessing_HairFollicleConstraint_MD', bl="����", text="", cw3=(50, 205, 0), l=("����ģ��"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'WindowControllerProcessing_HairFollicleConstraint_MD\')')
        pm.rowColumnLayout(columnWidth=(1, 125), numberOfColumns=2)
        pm.checkBox('HairFollicleConstraint_KeepPlace_checkBox', value=1, label="����ԭλ(������Լ��)")
        pm.button(c=lambda *args: pm.mel.HairFollicleAdsorption(), l="ë�Ҹ���(ѡ����Ҫ���������)")
        pm.setParent('..')
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=3, w=290)
        pm.textFieldButtonGrp('WindowControllerProcessing_LoadSourceProperties', bl="����", text="", cw3=(60, 195, 0), l=("����Դ����:"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'WindowControllerProcessing_LoadSourceProperties\')')
        pm.textFieldButtonGrp('WindowControllerProcessing_LoadTargetProperties', bl="����", text="", cw3=(70, 185, 0), l=("����Ŀ������:"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'WindowControllerProcessing_LoadTargetProperties\')')
        pm.rowColumnLayout(numberOfColumns=3)
        pm.textFieldGrp('LJBL', text="1", cw2=(25, 45), l=("����"))
        pm.button(c='LinkProperty()', l="����")
        pm.button(c=lambda *args: pm.mel.AttributeVisualizationWindow(), bgc=(1, 1, 0), l="�����Կ��ӻ�����(���ɺ��Ծ���)")
        pm.setParent('..')
        pm.rowColumnLayout( nc=2, adj=2,cw=(1,140))
        pm.button(c='gtMoveUpDnAttrsProc(1)', l="��������")
        pm.button(c='HideSelectionProperties()', l="����ѡ������")
        pm.button(c='gtMoveUpDnAttrsProc(0)', l="��������")
        pm.button(c='ShowDefaultProperties()', l="��ʾĬ������")
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.floatScrollBar("WindowControllerProcessingWindowSliderLine", hr=0, max=820,
                          cc='Slider(\'WindowControllerProcessingWindowSliderLine\',\'WindowControllerProcessingWindow\',\'WindowControllerProcessingFrom\',-1)', min=0)
        pm.showWindow()


# ��������
def Slider(SliderLine,Window,From,Num):
    num = pm.floatScrollBar(SliderLine, q=1, v=1)
    pm.formLayout(From,edit=1,attachPosition=(Window, "top", (num * Num), 0),attachForm=(Window, "left", 0))

# �Զ�����������Χ
def FloatSlider_Max_Edit_Controller(floatSlider):
    ShuLiang = float(pm.floatSliderGrp(floatSlider, q=1, v=1))
    ShuLiangMax = float(pm.floatSliderGrp(floatSlider, q=1, max=1))
    ShuLiangMaxA = 0.0
    ShuLiangMaxA = ShuLiangMax / 4.0
    if ShuLiang < ShuLiangMaxA:
        pm.floatSliderGrp(floatSlider, max=(ShuLiangMaxA * 2), e=1, fmx=9999999)
    ShuLiangMaxB = 0.0
    ShuLiangMaxB = ShuLiangMax / 4.0 * 3.0
    if ShuLiang > ShuLiangMaxB:
        pm.floatSliderGrp(floatSlider, max=(ShuLiangMaxB * 2), e=1, fmx=9999999)
def IntSlider_Max_Edit_Controller(intSlider):
    ShuLiang = int(pm.intSliderGrp(intSlider, q=1, v=1))
    ShuLiangMax = int(pm.intSliderGrp(intSlider, q=1, max=1))
    ShuLiangMaxA = 0
    ShuLiangMaxA = ShuLiangMax / 4
    if ShuLiang < ShuLiangMaxA:
        pm.intSliderGrp(intSlider, max=(ShuLiangMaxA * 2), e=1, fmx=9999999)
    ShuLiangMaxB = 0
    ShuLiangMaxB = ShuLiangMax / 4 * 3
    if ShuLiang > ShuLiangMaxB:
        pm.intSliderGrp(intSlider, max=(ShuLiangMaxB * 2), e=1, fmx=9999999)

# ���ɲ�ˢ��
def GenerateRefreshWindow(File):
    Name = pm.textFieldButtonGrp('WindowControllerProcessingUploadControllerFile', q=1, text=1)
    if Name:
        UploadFileByName(Name,File)
        PresetTemplateWindowClass().WindowControllerProcessing()
    else:
        pm.error('����д��������')
# ɾ����ѡ����
def DeleteSelectedCurve(File):
    Name = pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, sl=1)
    os.remove(File + '/' + Name + '.txt')
    os.remove(File + '/' + Name + '.jpg')
    PresetTemplateWindowClass().WindowControllerProcessing()
# ��д���������ϴ�
def UploadFileByName(Name,File):
    Curve =pm.ls(sl=1)
    if Curve:
        if os.path.exists(File+'/'+Name+'.jpg'):
            os.remove(File+'/'+Name+'.jpg')
        if os.path.exists(File+'/'+Name+'.txt'):
            os.remove(File+'/'+Name+'.txt')
        ShowGrid = 0
        if pm.optionVar(query='showGrid') == 1:
            pm.mel.ToggleGrid()
            ShowGrid = 1
        pm.select(cl=1)
        shape = pm.listRelatives(Curve[0], s=1, type='nurbsCurve')
        pm.select(shape)
        pm.mel.FrameSelectedWithoutChildren()
        #pm.isolateSelect('modelPanel4', state=1)
        pm.mel.HideUnselectedObjects()
        pm.playblast(compression="jpg", format='image', viewer=0, frame=float(pm.currentTime(q=1)),widthHeight=(110, 110),
                     filename=(File+'/'+Name))
        #pm.isolateSelect('modelPanel4', state=0)
        pm.select(shape)
        pm.mel.ShowLastHidden()

        os.rename((File+'/'+Name+'.0000.jpg'), (File+'/'+Name+'.jpg'))

        file=open((File+'/'+Name+'.txt'), 'w')
        shape = pm.listRelatives(Curve[0],s=1,type='nurbsCurve')
        CurveDegree = pm.getAttr(shape[0]+'.degree')
        CurveForm = pm.getAttr(shape[0] + '.form')
        text = ''
        text = ReturnCurveCommand(Curve)
        file.write(text)
        if ShowGrid == 1:
            pm.mel.ToggleGrid()
        pm.select(Curve)
    else:
        pm.error('��ѡ������')
# �������ɴ�����������
def ReturnCurveCommand(Curve):
    pm.select((Curve[0] + ".cv[0:]"),r=1)
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
        for i in range(0, 3):
            X = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].xValue"))
            Y = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].yValue"))
            Z = str(pm.getAttr(shape[0] + ".controlPoints[" + str(i) + "].zValue"))
            Txt = ('-p ' + X + ' ' + Y + ' ' + Z + ' ')
            AllP = AllP + Txt

    C1 = str(Curve[0])
    sel1 = OpenMaya.MSelectionList()  # �����յ�ѡ���б�
    sel1.add(C1)  # ��Ԫ����ӵ�ѡ���б�
    selPath1 = OpenMaya.MDagPath()  # �����յ�ַ·��
    sel1.getDagPath(0, selPath1)  # ��sel�ĵ�0�����赽��ַselPath��C�ĵ�ַ����selPath��

    address1 = OpenMaya.MFnNurbsCurve(selPath1)  # �������ַ����������nnn
    array1 = OpenMaya.MDoubleArray()  # ����һ�յĸ�˫����
    address1.getKnots(array1)  # ��ȡcurve1�����е�kֵ����array����

    AllK = ''
    for i in array1:
        Txt = ('-k ' + str(i) + ' ')
        AllK = AllK + Txt
    Print = ('curve -d '+str(CurveDegree)+' '+AllP+' '+AllK+';')
    return Print
# ��������
def CreateCurve():
    Name = pm.iconTextRadioCollection('WindowControllerProcessingAllControllerIconTextRadioCollection', q=1, sl=1)
    with open(PresetTemplateWindowClass().file_pathTop+'\Maya\MayaCommon\CurveShapeWithPicture'+"\\"+Name+'.txt') as f:
        contents = f.readlines()
    pm.mel.eval(contents[0])
# ����������״����
def FixSplineShapeName(Curve):
    shape = pm.listRelatives(Curve[0], s=1, type='nurbsCurve')
    pm.rename(shape,(Curve[0]+'Shape'))

# ѡ�и���ɫ
def ChangeCurveColor():
    Sel = pm.ls(sl=1)
    Color = pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',q=1,rgb=1)
    for s in Sel:
        shape = pm.listRelatives(Sel[0], s=1, type='nurbsCurve')
        pm.setAttr(s+".overrideEnabled", 0)
        pm.setAttr(shape[0]+".overrideEnabled", 0)
        pm.color(s, rgb=(Color[0], Color[1], Color[2]))
# �϶������Զ��޸���ɫ���
def DragSliderAutomaticallyModifyColorPanel():
    value = pm.intSlider('WindowControllerProcessingChangeCurveColor_intSlider', q=1, value=1)
    if value ==0:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.188,0.188,0.188))
    if value ==1:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.000,0.000))
    if value ==2:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.051,0.051,0.051))
    if value ==3:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.319,0.319,0.319))
    if value ==4:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.328,0.000,0.021))
    if value ==5:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.001,0.117))
    if value ==6:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.000,1.000))
    if value ==7:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.061,0.010))
    if value ==8:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.019,0.000,0.056))
    if value ==9:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.577,0.000,0.577))
    if value ==10:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.254,0.065,0.033))
    if value ==11:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.050,0.017,0.014))
    if value ==12:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.319,0.019,0.000))
    if value ==13:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,0.000,0.000))
    if value ==14:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,1.000,0.000))
    if value ==15:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.053,0.319))
    if value ==16:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,1.000,1.000))
    if value ==17:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,1.000,0.000))
    if value ==18:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.127,0.716,1.000))
    if value ==19:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.056,1.000,0.366))
    if value ==20:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,0.434,0.434))
    if value ==21:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.776,0.413,0.191))
    if value ==22:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(1.000,1.000,0.125))
    if value ==23:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.000,0.319,0.089))
    if value ==24:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.356,0.144,0.030))
    if value ==25:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.342,0.356,0.030))
    if value ==26:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.138,0.356,0.030))
    if value ==27:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.030,0.356,0.109))
    if value ==28:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.030,0.356,0.356))
    if value ==29:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.030,0.136,0.356))
    if value ==30:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.159,0.030,0.356))
    if value ==31:
        pm.colorSliderGrp('WindowControllerProcessingChangeCurveColor_colorSliderGrp',e=1, rgb=(0.356,0.030,0.144))
# ADV�Ŀ�������Ϊ�˼���ADV����΢���¾�ֱ�����ˣ�
def asSwapCurve():
    Select = pm.ls(sl=1)
    CreateCurve()
    ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
    EndSelect = pm.ls(sl=1)
    pm.select(Select, r=1)
    pm.select(EndSelect, add=1)
    side = ""
    oppositeSide = ""
    allSet = ""
    tempString = []
    tempString2 = []
    tempString3 = []
    sel = pm.ls(sl=1)
    last = len(sel) - 1
    selShapes = []
    if len(sel) < 2:
        pm.pm.mel.error("Selected both controls to replace, and the new curve to use")

    for i in range(0, len(sel)):
        tempString = pm.listRelatives(sel[i], s=1)
        selShapes.append(tempString[0])
        if pm.mel.gmatch(sel[i], "*Extra*"):
            continue

        if not pm.objExists(selShapes[i]):
            pm.pm.mel.error("selected object:\"" + sel[i] + "\" is not a nurbsCurve")

        tempString = pm.listRelatives(sel[i], s=1)
        if pm.objectType(selShapes[i]) != "nurbsCurve" and pm.objectType(selShapes[i]) != "nurbsSurface":
            pm.pm.mel.error("selected object:\"" + sel[i] + "\" is not a nurbsCurve")

    pm.select(sel[last])
    pm.mel.DeleteHistory()
    for i in range(0, len(sel) - 1):
        tempString = pm.listRelatives(sel[i], s=1)
        tempString3 = []
        if len(tempString):
            tempString3 = pm.listConnections((tempString[0] + ".v"),
                                             p=1, s=1, d=0)
            pm.delete(tempString)

        pm.duplicate(sel[last], n='tempXform')
        tempString = pm.listRelatives('tempXform', s=1, f=1)
        for y in range(0, len(tempString)):
            pm.rename(tempString[y],
                      (sel[i] + "Shape"))

        allSet = "AllSet"
        if pm.objExists('FaceAllSet'):
            if pm.mel.eval('sets -im FaceAllSet '+sel[i]+';'):
                allSet = "FaceAllSet"

        tempString = pm.listRelatives('tempXform', s=1)
        for y in range(0, len(tempString)):
            tempString2 = pm.parent(tempString[y], sel[i], add=1, s=1)
            tempString[y] = tempString2[0]
            rot = pm.xform(sel[i], q=1, ro=1, ws=1)
            #		if(!(`gmatch $sel[0] "IK*"` || `gmatch $sel[0] "Pole*"` || `gmatch $sel[0] "RootX*"`))
            if not (rot[0] == 0 and rot[1] == 0 and rot[2] == 0):
                cmds.rotate(-90, -90, 0,
                          (tempString[y] + ".cv[0:9999]"),
                          r=1, os=1)

            if pm.objExists('AllSet'):
                pm.mel.eval('sets -add '+allSet+' '+tempString[y]+';')
                #cmds.sets(tempString[y], add=allSet)

            if tempString3:
                pm.catch(pm.mel.eval("connectAttr " + tempString3[0] + " " + tempString[y] + ".v"))

        pm.delete('tempXform')
    pm.dgdirty(a=1)
    pm.delete(EndSelect)
    pm.select(Select)
    ChangeCurveColor()

# ���ſ�����
def ScaleController():
    Scale = float(pm.floatSliderGrp('WindowControllerProcessingControllerSizeFloatSliderGrp', q=1, v=1))
    ModifyControllerShapeTRS("scale", Scale, Scale, Scale)
    FloatSlider_Max_Edit_Controller('WindowControllerProcessingControllerSizeFloatSliderGrp')

# ��ת������
def RotationController():
    Rotate = str(pm.radioCollection('WindowControllerProcessingControllerOrientation', q=1, select=1))
    X = 0.0
    Y = 0.0
    Z = 0.0
    if Rotate == "X":
        X = float(90)
        Y = float(0)
        Z = float(0)
    if Rotate == "Y":
        X = float(0)
        Y = float(90)
        Z = float(0)
    if Rotate == "Z":
        X = float(0)
        Y = float(0)
        Z = float(90)
    ModifyControllerShapeTRS("rotate", X, Y, Z)

# �޸Ŀ�������С
def ModifyControllerShapeTRS(Type, X, Y, Z):
    Curve = pm.ls(sl=1)
    for i in range(0, len(Curve)):
        shap = pm.listRelatives(Curve[i], s=1)
        pm.select(cl=1)
        for j in range(0, len(shap)):
            pm.select((shap[j] + ".cv[0:]"),add=1)
        if Type == "translate":
            pm.move((X), (Y), (Z),localSpace=1)
        if Type == "rotate":
            pm.rotate((X), (Y), (Z),r=1)
        if Type == "scale":
            pm.scale((X), (Y), (Z),r=1)
        if Type == "SoftSelectionSize":
            size = pm.softSelect(q=1,ssd=1)
            AllNum = pm.getAttr(Curve[i]+'.boundingBox.boundingBoxSize')
            num = max(AllNum)
            Scale = size/num*2.14
            pm.scale((Scale), (Scale), (Scale), r=1)
        pm.select(cl=1)
    pm.select(Curve)

# ���ɿ�����
def ChuangJianFK():
    pm.mel.SelectHierarchy()
    joint = pm.ls(typ='joint', sl=1)
    ALL = pm.ls(sl=1)
    #�Ƴ�������
    RemoveJoint = pm.checkBox('WindowControllerProcessingIgnoreEndBones_checkBox', q=1, v=1)
    if RemoveJoint == True:
        for j in joint:
            q = pm.listRelatives(j,c=1)
            if len(q) == 0:
                joint.remove(j)
    #����������
    TopGrp = []
    C_GrpNum = int(pm.intSliderGrp('WindowControllerProcessingNumberControllerGroups', q=1, v=1))#��������ֵ
    Suffix = str(pm.textFieldGrp('WindowControllerProcessingSuffix', q=1, text=1))#��ȡ��׺

    nurbs = []
    for i in range(0, len(joint)):
        pm.rename(CreateCurve(),joint[i] + "_C")
        nurbs.append(joint[i] + "_C")
        for j in range(0, C_GrpNum):
            pm.mel.doGroup(0, 1, 1)
            #����������
            pm.mel.rename(joint[i] + "_G" + str((C_GrpNum - j)) + Suffix)
        TopGrp.append(joint[i] + "_G1" + Suffix)
        pm.delete(pm.pointConstraint(joint[i],(joint[i] + "_G1" + Suffix)))
        pm.delete(pm.orientConstraint(joint[i], (joint[i] + "_G1" + Suffix)))
    # ���и���
    for i in range(1, len(joint)):
        Parent = pm.listRelatives(joint[i],p=1)
        pm.select(Parent)
        jointLX = pm.ls(typ='joint', sl=1)
        if not jointLX:
            for k in range(0, len(ALL)):
                Parent = pm.listRelatives(p=1)
                pm.select(Parent, r=1)
                jointLX = pm.ls(typ='joint', sl=1)
                if jointLX:
                    break
        Parent = pm.ls(sl=1)
        for j in range(0, len(joint)):
            if joint[j] == Parent[0]:
                pm.parent(TopGrp[i], nurbs[j])
                break
    # �Ƿ���ȡԼ��
    ExtractConstraints = pm.checkBox('WindowControllerProcessingExtractConstraints', q=1, value=1)
    #����Լ��
    if ExtractConstraints == 1:
        pm.select(cl=1)
        if not pm.objExists("ZiJianKZQyveshu"):
            pm.rename(pm.mel.doGroup(0, 1, 1),"ZiJianKZQyveshu")
    for i in range(0, len(joint)):
        pm.parentConstraint((joint[i] + "_C"),joint[i])
        pm.scaleConstraint((joint[i] + "_C"),joint[i])
        if ExtractConstraints == 1:
            pm.parent((joint[i] + "_scaleConstraint1"),(joint[i] + "_parentConstraint1"),"ZiJianKZQyveshu")

# ��������
def ShowAxial():
    Sel = pm.ls(sl=1)
    for i in range(0, len(Sel)):
        Ture = int(pm.getAttr(Sel[i] + ".displayLocalAxis"))
        if Ture < 1:
            pm.setAttr((Sel[i] + ".displayLocalAxis"),
                       1)


        else:
            pm.setAttr((Sel[i] + ".displayLocalAxis"),
                       0)


# ���ɹ�����
def GenerateBoneChain():
    Nurbs = pm.ls(sl=1)
    ShuLiang = pm.intSliderGrp('WindowControllerProcessingJointNum', q=1, v=1)
    pm.spaceLocator(p=(0, 0, 0), n="LocatorSC")
    pm.select("LocatorSC", r=1)
    pm.select(Nurbs, tgl=1)
    pm.pathAnimation(upAxis='x', fractionMode=True, endTimeU=pm.playbackOptions(query=1, maxTime=1),
                     startTimeU=pm.playbackOptions(minTime=1, query=1), worldUpType="vector", inverseUp=False,
                     inverseFront=False, follow=True, bank=False, followAxis='y', worldUpVector=(0, 1, 0))
    LuJingJieDian = pm.listConnections("LocatorSC.rx", s=1, d=0)
    pm.disconnectAttr((LuJingJieDian[0] + "_uValue.output"), (LuJingJieDian[0] + ".uValue"))
    pm.select(cl=1)
    for i in range(0, ShuLiang + 1):
        number = 1.0 / ShuLiang * i
        pm.setAttr((LuJingJieDian[0] + ".uValue"),number)
        pm.joint(p=(0, 0, 0), n=("Joint" + str(i)))
        pm.delete(pm.pointConstraint("LocatorSC",("Joint" + str(i))))
    pm.delete("LocatorSC")

# �������
def MirrorJoint():
    Sel = pm.ls(sl=1)
    ChaoXiangh = str(pm.radioCollection('WindowControllerProcessingJointMirror', q=1, select=1))
    pm.select(cl=1)
    pm.joint(p=(0, 0, 0), n="Mirror_joint")
    for i in range(0, len(Sel)):
        pm.delete(pm.pointConstraint(Sel[i], "Mirror_joint", weight=1))
        if ChaoXiangh == "X":
            Num = float(pm.getAttr("Mirror_joint.translateX"))
            pm.setAttr("Mirror_joint.translateX",(Num * (-1)))
            pm.select(Sel[i], r=1)
            pm.mirrorJoint(mirrorBehavior=1, mirrorYZ=1)
        if ChaoXiangh == "Y":
            Num = float(pm.getAttr("Mirror_joint.translateY") * (-1))
            pm.setAttr("Mirror_joint.translateY", Num)
            pm.select(Sel[i], r=1)
            pm.mirrorJoint(mirrorBehavior=1, mirrorXZ=1)
        if ChaoXiangh == "Z":
            Num = float(pm.getAttr("Mirror_joint.translateZ") * (-1))
            pm.setAttr("Mirror_joint.translateZ", Num)
            pm.select(Sel[i], r=1)
            pm.mirrorJoint(mirrorXY=1, mirrorBehavior=1)
        sel = pm.ls(sl=1)
        pm.delete(pm.pointConstraint("Mirror_joint", sel[0], weight=1))
    pm.delete("Mirror_joint")

# �����Ľ���������
def CreateCentreJoint():
    pm.mel.SelectEdgeRingSp()
    ele = pm.ls(fl=1, sl=1)
    skip = []
    OldJoint = ""
    NewJoint = ""
    for i in range(0, len(ele)):
        if ele[i] in skip:
            continue
        pm.select(ele[i], r=1)
        pm.mel.performSelContiguousEdges(0)
        newEle = pm.ls(fl=1, sl=1)
        skip = skip + newEle
        pm.polyToCurve(conformToSmoothMeshPreview=1, degree=1, form=2)
        Curve = pm.ls(sl=1)
        pm.mel.CenterPivot()
        pm.select(cl=1)
        joint = str(pm.joint(p=(0, 0, 0)))
        OldJoint = NewJoint
        NewJoint = joint
        pm.pointConstraint(Curve[0], joint, weight=1, offset=(0, 0, 0))
        pm.delete(Curve)
        if len(OldJoint) != 0:
            pm.parent(NewJoint, OldJoint)

# ��ת���
def ReversalArrangement():
    pm.mel.SelectHierarchy()
    Select = pm.ls(sl=1)
    for i in range(1, len(Select)):
        pm.parent(Select[i], w=1)
    for i in range(0, (len(Select) - 1)):
        pm.parent(Select[i], Select[i + 1])

# ����ת����
def JointTransformationCurve():
    pm.mel.SelectHierarchy()
    Select = pm.ls(sl=1)
    CurveP = ""
    for i in range(0, len(Select)):
        pm.spaceLocator(p=(0, 0, 0), n="LS_Loc")
        pm.pointConstraint(Select[i], "LS_Loc", weight=1)
        TX = str(pm.getAttr("LS_Loc.translateX"))
        TY = str(pm.getAttr("LS_Loc.translateY"))
        TZ = str(pm.getAttr("LS_Loc.translateZ"))
        CP = (" -p " + TX + " " + " " + TY + " " + TZ)
        CurveP = CurveP + CP
        pm.delete("LS_Loc")
    pm.mel.eval("curve -d 3" + CurveP)
# �������
def InsertJoint():
    #pm.undoInfo(st=1,ock=1,infinity=1)
    Sel = pm.ls(sl=1)
    # ��ѯ������������
    JointNum = pm.intSliderGrp('WindowControllerProcessingInsertBone', q=1, v=1) -1
    pm.curve(p=[(0, 0, 0), (0, 0, 1)], d=1)
    Curve = pm.ls(sl=1)
    pm.select((Curve[0] + ".cv[0]"),r=1)
    pm.mel.newCluster(" -envelope 1")
    Cluster1 = pm.ls(sl=1)
    pm.select((Curve[0] + ".cv[1]"),r=1)
    pm.mel.newCluster(" -envelope 1")
    Cluster2 = pm.ls(sl=1)
    pm.delete(pm.pointConstraint(Sel[0], Cluster1[0], weight=1, offset=(0, 0, 0)))
    pm.delete(pm.pointConstraint(Sel[1], Cluster2[0], weight=1, offset=(0, 0, 0)))
    pm.select(cl=1)
    pm.spaceLocator(p=(0, 0, 0), n=("LS_Loc"))
    pm.select(Curve[0], tgl=1)
    pm.pathAnimation(upAxis='x', fractionMode=True, endTimeU=pm.playbackOptions(query=1, maxTime=1),
                     startTimeU=pm.playbackOptions(minTime=1, query=1), worldUpType="vector", inverseUp=False,
                     inverseFront=False, follow=True, bank=False, followAxis='y', worldUpVector=(0, 1, 0))
    LuJingJieDian = pm.listConnections(("LS_Loc.rx"),s=1, d=0)
    pm.disconnectAttr((LuJingJieDian[0] + "_uValue.output"), (LuJingJieDian[0] + ".uValue"))
    pm.select(cl=1)
    for i in range(1, JointNum):
        number = 1.0 / JointNum * i
        pm.setAttr((LuJingJieDian[0] + ".uValue"),number)
        pm.joint(p=(0, 0, 0), n=(str(Sel[0]) + str(Sel[1]) + "_Joint" + str(i)))
        pm.delete(pm.pointConstraint("LS_Loc", (str(Sel[0]) + str(Sel[1]) + "_Joint" + str(i)),weight=1))
    pm.delete("LS_Loc")
    pm.parent((str(Sel[0]) + str(Sel[1]) + "_Joint1"),Sel[0])
    pm.parent(Sel[1],(str(Sel[0]) + str(Sel[1]) + "_Joint" + str((JointNum - 1))))
    pm.delete(Curve, Cluster1, Cluster2)
    #pm.undoInfo(cck=1)

# ƫ������
def gtMoveUpDnAttrsProc(updn):
    objs = pm.ls(sl=1)
    attrs = pm.channelBox('mainChannelBox', q=1, sma=1)
    ex = 0
    for j in range(0, len(objs)):
        obj = objs[j]
        for i in range(0, len(attrs)):
            attr = attrs[i]
            ex = int(pm.objExists(obj + "." + attr))
            if ex == 0:
                continue

            udAttrs = pm.listAttr(obj, ud=1, u=1)
            index = -1
            for a in range(0, len(udAttrs)):
                if attr == udAttrs[a]:
                    index = int(a)

            if index == -1:
                continue

            indexUp = index - 1
            if indexUp < 0:
                indexUp = index

            upAttr = udAttrs[indexUp]
            if updn == 1:
                if index == 0:
                    continue

                pm.deleteAttr(obj + "." + upAttr)
                pm.undo()
                for aa in range((index + 1), len(udAttrs)):
                    pm.deleteAttr(obj + "." + udAttrs[aa])
                    pm.undo()

            if updn == 0:
                pm.deleteAttr(obj + "." + attr)
                pm.undo()
                dnSize = len(attrs)
                for aa in range((index + dnSize + 1), len(udAttrs)):
                    pm.deleteAttr(obj + "." + udAttrs[aa])
                    pm.undo()

# ����ѡ������
def HideSelectionProperties():
    QvDongYvan = pm.ls(sl=1)
    LianJieYvan = pm.channelBox('mainChannelBox', q=1, sma=1)
    for i in range(0, len(LianJieYvan)):
        pm.setAttr((QvDongYvan[0] + "." + LianJieYvan[i]),
                   channelBox=False, keyable=False)

# ��ʾĬ������
def ShowDefaultProperties():
    QvDongYvan = pm.ls(sl=1)
    LianJieYvan = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for j in range(0, len(QvDongYvan)):
        for i in range(0, len(LianJieYvan)):
            pm.setAttr((QvDongYvan[j] + "." + LianJieYvan[i]),k=True)

#����ѡ��
def InterlacedLineSelection(MS):
    pm.mel.polySelectEdgesEveryN(MS, pm.intSliderGrp('WindowControllerProcessingInterval', q=1, v=1))

# ��������
def LinkProperty():
    TextField_MB = str(pm.textFieldButtonGrp('WindowControllerProcessing_LoadTargetProperties', q=1, text=1))
    TextField_Y = str(pm.textFieldButtonGrp('WindowControllerProcessing_LoadSourceProperties', q=1, text=1))
    pm.shadingNode('multiplyDivide', asUtility=1, n=(TextField_MB + "_multiplyDivide"))
    multiplyDivide = pm.ls(sl=1)
    pm.connectAttr(TextField_Y,(multiplyDivide[0] + ".input1X"),f=1)
    pm.connectAttr((multiplyDivide[0] + ".outputX"),TextField_MB, f=1)
    Num = float(pm.textFieldGrp('LJBL', q=1, text=1))
    pm.setAttr((multiplyDivide[0] + ".input2X"),Num)



if __name__ == '__main__':
    PresetTemplateWindowClass().WindowControllerProcessing()