#coding=gbk
import pymel.core as cmds
import os
import sys
import inspect

#��Ŀ¼
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# �����ı�
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaCurve')
from CreateAndEditCurve import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from AutomaticModificationUIRange import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaOthersLibrary')
from IndependentSmallFunctions import *

class ZKM_RopeWindow():
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathReversion = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
        cur_dirB = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathTop = os.path.join(cur_dirB)  # ��ȡ��λ��
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
        self.file_pathTop = file_pathTop
    def ZKM_Window(self):# ����
        if cmds.window('ZKM_RopeWindow', ex=1):
            cmds.deleteUI('ZKM_RopeWindow')
        cmds.window('ZKM_RopeWindow', t="����Ʈ��")
        cmds.rowColumnLayout(nc=1, adj=5)
        cmds.rowColumnLayout(nc=3, adj=3)
        cmds.button(c='ZKM_RopeWindow().Test()', bgc=(0.5, 0.8, 0.8), l='����ģ��')
        cmds.button(c='ZKM_IndependentSmallfunctions().CreateJointByEdgeLoop()', bgc=(0.5, 0.8, 0.8), l='���Ľ���������')
        cmds.button(c='ZKM_IndependentSmallfunctions().JointTransformationCurve()', bgc=(0.5, 0.8, 0.8), l='������������')
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=2)
        pm.intSliderGrp('RopeWindow_InsertBone', fmx=9999999, min=1,
                        cc='ZKM_AutomaticModificationUIRangeClass().ZKM_IntSlider_Max_Edit_Controller(\'WindowControllerProcessingInsertBone\')',
                        max=10, cw3=(0, 40, 140), f=1, l="��������", v=50)
        pm.button(c='ZKM_IndependentSmallfunctions().GenerateBoneChain(pm.intSliderGrp(\'RopeWindow_InsertBone\', q=1, v=1))', l="��������")
        cmds.setParent('..')
        cmds.intSlider('ZKM_RopeWindow_EditCreateRopeButton', bgc=(1, 0.4, 0.4), min=0, cc='ZKM_RopeWindow().ImplementationProgress()', max=4, value=0, step=1)
        cmds.button('ZKM_RopeWindow_CreateRopeButton', h=30, bgc=(1, 0.4, 0.4), c='ZKM_RopeWindow().Create()', l='��������')#���������죬��ק
        cmds.rowColumnLayout(nc=3, adj=2,h=1)
        cmds.textFieldGrp('ZKM_RopeWindow_Differensce', cw2=(45, 30), text='1',l='���ȱ���')
        cmds.button(l='������������',bgc=(0.5, 0.8, 0.8))
        cmds.button(l="������������",bgc=(0.5, 0.8, 0.8))
        cmds.setParent('..')
        cmds.textFieldButtonGrp('ZKM_RopeWindow_AddJoint', cw3=(60,150, 50), bl='����',l='���ع���',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'ZKM_RopeWindow_AddJoint\')')
        cmds.textFieldButtonGrp('ZKM_RopeWindow_AddCurve', cw3=(60, 150, 50), bl='����', l='��������',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'ZKM_RopeWindow_AddCurve\')')
        cmds.textFieldButtonGrp('ZKM_RopeWindow_Prefix', cw3=(60, 150, 50), bl='����', l='����ǰ׺',text='Rope_',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'ZKM_RopeWindow_Prefix\')')
        cmds.rowColumnLayout(nc=2, adj=5,h=1)
        cmds.checkBox('ZKM_RopeWindow_CreateRoute',label='����·��')
        cmds.textFieldGrp('ZKM_RopeWindow_RouteMagnification',cw2=(65, 110), l=('·�����ȱ���'), text=5)
        cmds.checkBox('ZKM_RopeWindow_ReplaceShrinkage', label='�滻����')
        cmds.textFieldButtonGrp('ZKM_RopeWindow_AdditionalSplines', cw3=(43, 100, 5), bl='����', l='��������',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'ZKM_RopeWindow_AdditionalSplines\')')
        cmds.checkBox('ZKM_RopeWindow_CreateRouste', label='�ر�����')
        cmds.textFieldButtonGrp('ZKM_RopeWindow_NotStretchBones', cw3=(55, 88, 10), bl='����', l='���������',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'ZKM_RopeWindow_NotStretchBones\')')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.showWindow()
    #�Զ�������ť
    def ImplementationProgress(self):
        ShuLiang = int(pm.intSlider('ZKM_RopeWindow_EditCreateRopeButton', q=1, v=1))
        Txt = ""
        Text = ["��������", ",��������",",��������", ",����FK", ",������ק"]
        for i in range(0, len(Text)):
            if ShuLiang >= i:
                Txt = Txt + Text[i]
                pm.button('ZKM_RopeWindow_CreateRopeButton', e=1, l=Txt)
    def Create(self):
        pm.loadPlugin('matrixNodes')
        Step = cmds.intSlider('ZKM_RopeWindow_EditCreateRopeButton', q=1,value=1)
        Joint = cmds.textFieldButtonGrp('ZKM_RopeWindow_AddJoint', q=1, text=1)  # ���ض�����
        Curve = cmds.textFieldButtonGrp('ZKM_RopeWindow_AddCurve', q=1, text=1)  # ��������
        Prefix = cmds.textFieldButtonGrp('ZKM_RopeWindow_Prefix', q=1, text=1)  # ����ǰ׺
        cmds.select(Joint)
        cmds.SelectHierarchy()
        Joint = cmds.ls(sl=1, type='joint')
        cmds.select(Curve + '.cv[*]')
        CurvePoint = cmds.ls(sl=1, fl=1) # ����������

        Cluster = []
        Num = []
        for i in range(-1, 1):
            cmds.select(CurvePoint[i])
            C = cmds.cluster()
            num = cmds.getAttr(C[1] + '.rotatePivot')
            Num.append(num)
            Cluster.append(C[1])

        Num = list(set(Num[0]) - set(Num[1]))
        Num = [abs(Num[0][0]),abs(Num[0][1]),abs(Num[0][2])]

        SurfaceDirection = [0, 0, 1]
        if Num[1] > Num[2]:
            SurfaceDirection = [0, 1, 0]
        if Num[2] > Num[0]:
            SurfaceDirection = [1, 0, 0]
        cmds.delete(Cluster)

        #��������
        if Step > -1:
            self.CreateBase(Prefix,Curve,CurvePoint,Joint,SurfaceDirection)
        # ��������
        if Step > 0:
            self.AddStretch(Prefix, Curve, CurvePoint, Joint)
        # ��������
        if Step > 1:
            self.AddContract(Prefix,Curve,CurvePoint,Joint)
        # ����FK
        if Step > 2:
            self.AddFK(Prefix,Curve,CurvePoint,Joint,SurfaceDirection)
        # ������ק
        if Step > 3:
            self.AddDrag(Prefix,Curve,CurvePoint,Joint,SurfaceDirection)

    ############################################################################################################################
    # �����
    # ��������
    def CreateBase(self,Prefix,Curve,CurvePoint,Joint,SurfaceDirection):
        # ��������
        All_BaseController_Grp = cmds.group(em=1, n=(Prefix + 'All_BaseController_Grp'))
        # ��������������
        i = 0
        for Point in CurvePoint:
            cmds.select(Point)
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            BaseCurve = cmds.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(SurfaceDirection[2],SurfaceDirection[1],SurfaceDirection[0]),
                                    n=(Prefix + str(i) + '_BaseController'))
            ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor('Index', BaseCurve, [0,0,0], 18)
            cmds.group(n=(Prefix + str(i) + '_BaseController_Grp2'))
            TopGrp = cmds.group(n=(Prefix + str(i) + '_BaseController_Grp1'))
            cmds.delete(cmds.parentConstraint(Cluster[1], TopGrp, w=1))
            cmds.parent(Cluster[1], BaseCurve[0])
            cmds.parent(TopGrp, All_BaseController_Grp)
            i = i + 1
        # ����IK
        cmds.select(Joint[0], Joint[-1], Curve)
        cmds.ikHandle(ccv=False, sol='ikSplineSolver',n=(Prefix + '_ikHandle'))
        IK = cmds.ls(sl=1)
        # ��������
        cmds.extrude(Curve, upn=0, dl=1, ch=0, rotation=0, d=SurfaceDirection, length=1, scale=1, et=0, rn=True, po=0)
        Surface = cmds.ls(sl=1)
        #cmds.move(0, 0, -0.5, r=1, os=1, wd=1)
        #cmds.makeIdentity(apply=True, t=1)
        # ���������������
        for i in range(0, len(CurvePoint)):
            cmds.select(Surface[0] + '.cv[' + str(i) + '][0:*]')
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            cmds.parent(Cluster[1], (Prefix + str(i) + '_BaseController'))
        # �ؽ�����
        pm.rebuildSurface("extrudedSurface1", rt=0, kc=0, fr=0, ch=1, end=1, sv=1, su=len(Joint)*3, kr=0, dir=2, kcp=0, tol=0.01,dv=3, du=3, rpo=1)
        # ����ë�Ҹ��ű���������
        All_JointFollicle_Grp = cmds.group(em=1, n=(Prefix + 'All_JointFollicle_Grp'))
        shape = cmds.listRelatives(Surface, s=1)
        for i in range(0, len(Joint)):
            cpom = cmds.createNode('closestPointOnSurface',n=(Joint[i] + 'closestPointOnSurface'))
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
            decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
            cmds.connectAttr((Joint[i] + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
            cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
            follicleShape = cmds.createNode('follicle', n=(Joint[i] + '_follicleShape'))
            follicle = cmds.listRelatives(follicleShape, p=1)
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (Joint[i] + '_follicleShape' + '.inputSurface'), f=1)
            cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (Joint[i] + '_follicleShape' + '.inputWorldMatrix'), f=1)
            cmds.connectAttr((Joint[i] + '_follicleShape' + ".outTranslate"), (Joint[i] + '_follicle' + '.translate'),
                             f=1)
            cmds.connectAttr((Joint[i] + '_follicleShape' + ".outRotate"), (Joint[i] + '_follicle' + ".rotate"), f=1)
            #cmds.setAttr((Joint[i] + '_follicle' + '.parameterU'), cmds.getAttr((cpom + '.parameterU')))
            cmds.connectAttr((cpom + '.parameterU'), (Joint[i] + '_follicle' + '.parameterU'), f=1)
            cmds.setAttr((Joint[i] + '_follicle' + '.parameterV'),0)
            #cmds.connectAttr((cpom + '.parameterV'), (Joint[i] + '_follicle' + '.parameterV'), f=1)
            cmds.select(cl=1)
            joint = cmds.joint(p=(0, 0, 0), n=(Joint[i] + 'SkinJoint'))
            cmds.delete(cmds.parentConstraint(follicle[0], joint))
            '''if i > 0:
                cmds.parent(joint, (Joint[i - 1] + 'SkinJoint'))'''
            cmds.parent(follicle[0], All_JointFollicle_Grp)

        #cmds.select(Joint[0] + 'SkinJoint')
        #cmds.makeIdentity(apply=True, t=1)
        #cmds.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
        for i in range(0, len(Joint)):
            cmds.parentConstraint((Joint[i] + '_follicle'), (Joint[i] + 'SkinJoint'), mo=1, w=1)

        # cmds.setAttr((Prefix + Joint[0] + '_SkinJoint_Grp.v'), 0)

        # �����ļ�
        cmds.group(Joint[0], Curve, IK[0], n=(Prefix + 'SpineIkSys_Grp'))
        cmds.group((Joint[0] + 'SkinJoint'), n=(Prefix + Joint[0] + '_SkinJoint_Grp'))
        for i in range(1, len(Joint)):
            cmds.parent((Joint[i] + 'SkinJoint'),(Prefix + Joint[0] + '_SkinJoint_Grp'))
        cmds.setAttr('Rope_'+Joint[0]+'_SkinJoint_Grp.useOutlinerColor', True)
        cmds.setAttr('Rope_'+Joint[0]+'_SkinJoint_Grp.outlinerColor', 1, 0, 0)
        cmds.group(Surface[0], All_JointFollicle_Grp, n=(Prefix + 'follicleAttachmentSys_Grp'))
        cmds.group(All_BaseController_Grp, (Prefix + Joint[0] + '_SkinJoint_Grp'), (Prefix + 'SpineIkSys_Grp'),
                   (Prefix + 'follicleAttachmentSys_Grp'),n=(Prefix + 'BasicPart_Grp'))
        # �����ܿ���
        BaseCurve = cmds.circle(c=(0, 0, 0), ch=0, d=5, ut=0, sw=360, s=8, r=5, tol=0.01, nr=(SurfaceDirection[2],SurfaceDirection[1],SurfaceDirection[0]),
                                n=(Prefix + 'TotalControl_Curve'))
        ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor('Index', BaseCurve, [0, 0, 0], 13)
        cmds.group(n=(Prefix + 'TotalControl_Grp2'))
        cmds.group(n=(Prefix + 'TotalControl_Grp1'))
        cmds.delete(cmds.parentConstraint((Prefix + str(len(CurvePoint) - 1) + '_BaseController'),
                                          (Prefix + 'TotalControl_Grp1'), w=1))
        cmds.parentConstraint((Prefix + 'TotalControl_Curve'), (Prefix + 'BasicPart_Grp'), mo=1, w=1)
        cmds.scaleConstraint((Prefix + 'TotalControl_Curve'), (Prefix + 'BasicPart_Grp'), mo=1)
        cmds.setAttr((Curve + '.inheritsTransform'), 0)
        cmds.setAttr((Prefix + 'follicleAttachmentSys_Grp.inheritsTransform'), 0)

        cmds.group((Prefix + 'TotalControl_Grp1'), (Prefix + 'BasicPart_Grp'), n=(Prefix + 'All_Grp'))
        cmds.setAttr((Prefix + 'SpineIkSys_Grp.v'), 0)
        cmds.setAttr((Prefix + 'follicleAttachmentSys_Grp.v'), 0)

        '''#����ǰ����������
        for i in range(0,len(Joint)):
            pass
        CurveShape = cmds.listRelatives(Curve, s=1)
        cmds.select(cmds.duplicate(Curve, rr=1))
        CopyCurve = cmds.ls(sl=1)
        CopyCurveShape = cmds.listRelatives(CopyCurve, s=1)
        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide + '.operation'), 2)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((CurveShape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1X'), f=1)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((CopyCurveShape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input2X'), f=1)
        for i in range(0, len(Joint)):
            cmds.connectAttr((multiplyDivide + '.outputX'), (Joint[i] + '.scaleX'), f=1)
            cmds.connectAttr((multiplyDivide + '.outputX'), (Joint[i] + 'SkinJoint.scaleX'), f=1)
        cmds.setAttr(CopyCurve[0] + '.inheritsTransform', 1)'''
    # ��������
    def AddStretch(self, Prefix, Curve, CurvePoint, Joint):
        # ��������
        CurveShape = cmds.listRelatives(Curve, s=1)
        cmds.select(cmds.duplicate(Curve, rr=1))
        CopyCurve = cmds.ls(sl=1)
        CopyCurveShape = cmds.listRelatives(CopyCurve, s=1)
        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide + '.operation'), 2)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((CurveShape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1X'), f=1)
        curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
        cmds.connectAttr((CopyCurveShape[0] + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)
        cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input2X'), f=1)
        # �������쿪��
        cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='stretch', at='bool')
        cmds.setAttr((Prefix + 'TotalControl_Curve.stretch'), e=1, keyable=True)
        cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='StretchMagnification', dv=1, at='double')
        cmds.setAttr((Prefix + 'TotalControl_Curve.StretchMagnification'), e=1, keyable=True)
        condition = cmds.shadingNode('condition', asUtility=1)
        cmds.connectAttr((multiplyDivide + '.outputX'), (condition + '.colorIfFalseR'), f=1)
        cmds.connectAttr((Prefix + 'TotalControl_Curve.stretch'), (condition + '.firstTerm'), f=1)
        cmds.setAttr((condition + '.colorIfTrueR'), 1)
        multiplyDivideStretch = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.connectAttr((condition + '.outColorR'), (multiplyDivideStretch + '.input1X'), f=1)
        cmds.connectAttr((Prefix + 'TotalControl_Curve.StretchMagnification'), (multiplyDivideStretch + '.input2X'),
                         f=1)
        for i in range(0, len(Joint)):
            cmds.connectAttr((multiplyDivideStretch + '.outputX'), (Joint[i] + '.scaleX'), f=1)
            cmds.connectAttr((multiplyDivideStretch + '.outputX'), (Joint[i] + 'SkinJoint.scaleX'), f=1)
        cmds.setAttr(CopyCurve[0] + '.inheritsTransform', 1)
    # ��������
    def AddContract(self,Prefix,Curve,CurvePoint,Joint):
        cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='Contract', dv=0, max=100, min=-100, at='double')
        cmds.setAttr((Prefix + 'TotalControl_Curve.Contract'), e=1, keyable=True)
        multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
        cmds.setAttr((multiplyDivide + '.input2X'), 0.01)
        cmds.connectAttr((Prefix + 'TotalControl_Curve.Contract'), (multiplyDivide + '.input1X'), f=1)
        for i in range(0, len(Joint)):
            plusMinusAverage = cmds.shadingNode('plusMinusAverage', asUtility=1)
            cmds.connectAttr((multiplyDivide + '.outputX'), (plusMinusAverage + '.input1D[0]'), f=1)
            #cmds.setAttr((plusMinusAverage + '.input1D[1]'), cmds.getAttr(Joint[i] + '_follicleShape.parameterU'))
            cmds.connectAttr((Joint[i] + 'closestPointOnSurface.parameterU'), (plusMinusAverage + '.input1D[1]'), f=1)
            cmds.connectAttr((plusMinusAverage + '.output1D'), (Joint[i] + '_follicleShape.parameterU'), f=1)
    # ����FK
    def AddFK(self,Prefix,Curve,CurvePoint,Joint,SurfaceDirection):
        FK_List = []
        for i in range(0, len(CurvePoint)):
            FK_List.append(i)
        for i in range(0, len(CurvePoint) - 1):
            FK_List.append(len(CurvePoint) - i - 2)

        j = 0
        All_TopGrp = []
        for i in FK_List:
            FKCurve = cmds.circle(c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=2, tol=0.01,
                                  nr=(SurfaceDirection[2],SurfaceDirection[1],SurfaceDirection[0]),
                                  n=(Prefix + 'FKController' + str(j)))
            sel = cmds.ls(sl=1)
            ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor('Index', sel , [0, 0, 0], 20)
            if j >= (len(CurvePoint)):
                ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor('Index', sel, [0, 0, 0], 21)
                Shape = cmds.listRelatives(FKCurve[0], s=1)
                cmds.select((Shape[0] + ".cv[0:]"))
                cmds.scale(0.8, 0.8, 0.8, r=1)
            cmds.select(FKCurve)
            cmds.group(n=(Prefix + 'FKController_Grp2_' + str(j)))
            TopGrp = cmds.group(n=(Prefix + 'FKController_Grp1_' + str(j)))
            All_TopGrp.append(TopGrp)
            cmds.delete(cmds.parentConstraint((Prefix + str(FK_List[j]) + '_BaseController'), TopGrp, w=1))

            if j > 0:
                cmds.parent((Prefix + 'FKController_Grp1_' + str(j)),
                            (Prefix + 'FKController' + str(j - 1)))
            if j > (len(CurvePoint)-2):
                cmds.parentConstraint((Prefix + 'FKController' + str(j)),
                                      (Prefix + str(FK_List[j]) + '_BaseController_Grp1'), w=1)
            j = j + 1
        j = 0
        All_Loc = []
        for i in FK_List:
            if j < (len(CurvePoint) - 1):
                cmds.spaceLocator(p=(0, 0, 0), n=(Prefix + 'Loc' + str(j)))
                cmds.setAttr((Prefix + 'Loc' + str(j) + '.v'), 0)
                Loc = cmds.ls(sl=1)
                All_Loc.append(Loc)
                cmds.parent(Loc, (Prefix + 'FKController_Grp1_' + str(len(CurvePoint) - 1)))
                cmds.delete(cmds.parentConstraint((Prefix + 'FKController_Grp1_' + str(j), Loc[0]), w=1))
                cmds.connectAttr((Loc[0] + '.translate'),
                                 (Prefix + 'FKController_Grp1_' + str(len(FK_List) - 1 - j) + '.translate'), f=1)
                cmds.connectAttr((Loc[0] + '.rotate'),
                                 (Prefix + 'FKController_Grp1_' + str(len(FK_List) - 1 - j) + '.rotate'), f=1)
                if cmds.objExists((Prefix + 'Loc' + str(j - 1))):
                    cmds.parent((Prefix + 'Loc' + str(j - 1)), (Prefix + 'Loc' + str(j)))
                cmds.parentConstraint((Prefix + 'FKController' + str(j)), All_Loc[j], w=1)
            j = j + 1
        cmds.parent((Prefix + 'FKController_Grp1_0'), (Prefix + 'All_Grp'))
        cmds.parentConstraint((Prefix + 'TotalControl_Curve'), (Prefix + 'FKController_Grp1_0'), mo=1, w=1)
        cmds.scaleConstraint((Prefix + 'TotalControl_Curve'), (Prefix + 'FKController_Grp1_0'), mo=1)
    # ������ק
    def AddDrag(self,Prefix,Curve,CurvePoint,Joint,SurfaceDirection):
        #�޸�FK
        FK_Curve = cmds.curve(p=[(0, 0, 0), (0.25, 0, 0), (0.75, 0, 0), (1, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3)
        cmds.setAttr((FK_Curve + '.v'),0)
        cmds.parent(FK_Curve,(Prefix + 'TotalControl_Curve'))
        for i in range(0,((len(CurvePoint)-1)*2)):
            CopyCurveShape = cmds.listRelatives((Prefix + 'FKController' + str(i)), s=1)
            curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
            cmds.connectAttr((FK_Curve + '.worldSpace[0]'), (curveInfo + '.inputCurve'), force=1)

            multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
            cmds.connectAttr((curveInfo + '.arcLength'), (multiplyDivide + '.input1X'), f=1)

            cmds.setAttr((multiplyDivide + '.input2X'), 2.5)
            makeNurbCircle = cmds.listConnections(CopyCurveShape[0]+'.create')
            cmds.connectAttr((multiplyDivide + '.outputX'), (makeNurbCircle[0] + '.radius'), f=1)

            if i > (len(CurvePoint) - 2):
                cmds.setAttr((multiplyDivide + '.input2X'), 2)

        cmds.delete((Prefix + 'FKController_Grp1_0_parentConstraint1'),(Prefix + 'FKController_Grp1_0_scaleConstraint1'))
        Cluster = []
        Num = []
        for i in range(-2, 2):
            cmds.select(CurvePoint[i])
            C = cmds.cluster()
            num = cmds.getAttr(C[1] + '.rotatePivot')
            Num.append(num)
            Cluster.append(C[1])
        Drag_Curve = cmds.curve(p=[(Num[1][0][0],Num[1][0][1],Num[1][0][2]), (Num[0][0][0],Num[0][0][1],Num[0][0][2]),
                                   (Num[3][0][0],Num[3][0][1],Num[3][0][2]), (Num[2][0][0],Num[2][0][1],Num[2][0][2])], k=[0, 0, 0, 1, 1, 1], d=3)
        cmds.delete(Cluster)
        cmds.select(Drag_Curve + '.cv[0:]')
        Drag_CurvePoint = cmds.ls(sl=1, fl=1)
        # ��������������
        i = 0
        for Point in Drag_CurvePoint[0:4]:
            cmds.select(Point)
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            Num = 17
            Radius = 4
            if i == 1 or i == 2:
                Radius = 3
                Num = 6
            circle = cmds.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=Radius, tol=0.01, nr=(SurfaceDirection[2],SurfaceDirection[1],SurfaceDirection[0]),
                                    n=(Prefix + str(i) + '_DragController'))
            ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor('Index', circle, [0, 0, 0], Num)
            cmds.group(n=(Prefix + str(i) + '_DragController_Grp2'))
            TopGrp = cmds.group(n=(Prefix + str(i) + '_DragController_Grp1'))
            cmds.delete(cmds.parentConstraint(Cluster[1], TopGrp, w=1))
            '''if i < 2:
                cmds.delete(cmds.parentConstraint((Prefix + '0_BaseController'), TopGrp, w=1))
            else:
                cmds.delete(cmds.parentConstraint((Prefix + str(len(CurvePoint) - 1) + '_BaseController'), TopGrp, w=1))'''
            cmds.delete(Cluster)
            # cmds.parent(TopGrp,All_BaseController_Grp)
            i = i + 1
        # ��������
        cmds.extrude(Drag_Curve, upn=0, dl=1, ch=0, rotation=0, d=SurfaceDirection, length=1, scale=1, et=0, rn=True, po=0)
        Surface = cmds.ls(sl=1)
        #cmds.move(0, 0, -0.5, r=1, os=1, wd=1)
        #cmds.makeIdentity(apply=True, t=1)
        # ���������������
        for i in range(0, len(Drag_CurvePoint)):
            cmds.select(Surface[0] + '.cv[' + str(i) + '][0:*]')
            Cluster = cmds.cluster()
            cmds.setAttr((Cluster[1] + '.v'), 0)
            cmds.delete(cmds.parentConstraint((Prefix + str(i) + '_DragController'),Cluster[1],w=1))
            cmds.parent(Cluster[1], (Prefix + str(i) + '_DragController'))
        # ����ë�Ҹ��ű���
        All_DragFollicle_Grp = cmds.group(em=1, n=(Prefix + 'All_DragFollicle_Grp'))
        All_DragLoc_Grp = cmds.group(em=1, n=(Prefix + 'All_DragLoc_Grp'))
        shape = cmds.listRelatives(Surface, s=1)
        for i in range(0, len(CurvePoint)):
            cpom = cmds.createNode('closestPointOnSurface')
            cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
            decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
            cmds.connectAttr((Prefix + str(i) + '_BaseController.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'),
                             force=1)
            cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
            follicleShape = cmds.createNode('follicle', n=(Prefix + str(i) + '_BaseController_Grp1' + '_follicleShape'))
            follicle = cmds.listRelatives(follicleShape, p=1)
            cmds.connectAttr((shape[0] + '.worldSpace[0]'),
                             (Prefix + str(i) + '_BaseController_Grp1_follicleShape.inputSurface'), f=1)
            cmds.connectAttr((shape[0] + '.worldMatrix[0]'),
                             (Prefix + str(i) + '_BaseController_Grp1_follicleShape.inputWorldMatrix'), f=1)
            cmds.connectAttr((Prefix + str(i) + '_BaseController_Grp1_follicleShape.outTranslate'),
                             (Prefix + str(i) + '_BaseController_Grp1_follicle.translate'), f=1)
            cmds.connectAttr((Prefix + str(i) + '_BaseController_Grp1_follicleShape.outRotate'),
                             (Prefix + str(i) + '_BaseController_Grp1_follicle.rotate'), f=1)
            cmds.setAttr((Prefix + str(i) + '_BaseController_Grp1_follicle.parameterU'),
                         cmds.getAttr((cpom + '.parameterU')))
            cmds.setAttr((Prefix + str(i) + '_BaseController_Grp1_follicle.parameterV'),
                         cmds.getAttr((cpom + '.parameterV')))
            cmds.select(cl=1)
            cmds.parent(follicle[0], All_DragFollicle_Grp)
            cmds.spaceLocator(p=(0, 0, 0), n=(Prefix + 'DragLoc' + str(i)))
            cmds.parent((Prefix + 'DragLoc' + str(i)), (Prefix + 'All_DragLoc_Grp'))
            cmds.delete(cmds.parentConstraint((Prefix + 'FKController' + str(i)), (Prefix + 'DragLoc' + str(i)), w=1))
            cmds.parentConstraint(follicle[0], (Prefix + 'DragLoc' + str(i)), mo=1, w=1)
            cmds.delete(cpom, decomposeMatrix)
        for i in range(0, len(CurvePoint) - 1):
            cmds.parent((Prefix + 'DragLoc' + str(i + 1)), (Prefix + 'DragLoc' + str(i)))
        for i in range(0, len(CurvePoint)):
            cmds.connectAttr((Prefix + 'DragLoc' + str(i) + '.translate'),
                             (Prefix + 'FKController_Grp1_' + str(i) + '.translate'), f=1)
            cmds.connectAttr((Prefix + 'DragLoc' + str(i) + '.rotate'),
                             (Prefix + 'FKController_Grp1_' + str(i) + '.rotate'), f=1)
        # �����ļ�
        cmds.delete(Drag_Curve)
        cmds.parent((Prefix + '1_DragController_Grp1'), (Prefix + '0_DragController'))
        cmds.parent((Prefix + '2_DragController_Grp1'), (Prefix + '3_DragController'))
        cmds.group(Surface, All_DragFollicle_Grp, All_DragLoc_Grp, n=(Prefix + 'All_DragFollicleAttachment_Grp'))
        cmds.group((Prefix + 'All_DragFollicleAttachment_Grp'), (Prefix + '0_DragController_Grp1'),
                   (Prefix + '3_DragController_Grp1'),
                   n=(Prefix + 'All_Drag_Grp'))
        cmds.parent((Prefix + 'All_Drag_Grp'), (Prefix + 'All_Grp'))
        cmds.setAttr((Prefix + 'All_DragFollicleAttachment_Grp.inheritsTransform'), 0)
        cmds.setAttr((Prefix + 'All_DragFollicleAttachment_Grp.v'), 0)
        cmds.parentConstraint((Prefix + 'TotalControl_Curve'), (Prefix + 'All_Drag_Grp'), mo=1, w=1)
        cmds.scaleConstraint((Prefix + 'TotalControl_Curve'), (Prefix + 'All_Drag_Grp'), mo=1)

    ############################################################################################################################
    # ��������������ģ��
    def Test(self):
        curve = pm.curve(p=[(-12, 0, 0), (-4, 0, 0), (4, 0, 0), (12, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3)
        pm.rebuildCurve(curve, rt=0, ch=1, end=1, d=3, kr=0, s=10, kcp=0, tol=0.01, kt=0, rpo=1, kep=1)
        pm.polyPlane(cuv=2, sy=1, sx=50, h=1, ch=0, w=24, ax=(0, 1, 0))

ShowWindow = ZKM_RopeWindow()
if __name__ =='__main__':
    ShowWindow.ZKM_Window()