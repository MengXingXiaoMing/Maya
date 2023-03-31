#coding=gbk
#��ȡ�ļ�·��
import os
import sys

import inspect
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
from Follicle import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaBS')
from BsConversionDrive import *
# �ļ�����
from FileProcessing import *
# ���Դ���
from Attribute import *
#�򿪲�ͬ�ز�bs���ݴ���
sys.path.append(File_RootDirectory + '\\PresetTemplateFile\\DifferentTopologyTransferBS')
from DifferentTopologyTransferBS.DifferentTopologyTransfer_BS import *
global jobNum
class ZKM_PresetTemplate:
    def __init__(self):
        # ͨ��self���½��Ķ����г�ʼ������
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        # print(self.file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathReversion = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
        self.file_path = file_path
        self.file_pathA = file_pathReversion
    #������ά��ͼ����������
    def CleanWindow(self):
        global jobNum
        try :
            pm.delete('FaceCamera*')
        except:
            pass
        if pm.objExists('FaceTemplate_Grp'):
            pm.delete('FaceTemplate_Grp')
        try:
            self.DeleteScriptJob(jobNum)
        except:
            pass
    #�Զ�ͬ������
    def AutomaticSynchronizationSettings(self):
        with open((self.file_pathA+'/Py_PresetTemplate_Material/AutomaticSynchronization.txt'), 'r') as f:  # ���ļ�
            data = f.read()  # ��ȡ�ļ�
        pm.optionMenu('AutomaticSynchronization', e=1, select=int(data))
        self.AdjustPanelPpresets()
    #�Զ�д��Ԥ��
    def AutomaticSynchronization(self):
        with open((self.file_pathA+'/Py_PresetTemplate_Material/AutomaticSynchronization.txt'), 'w') as f:
            a = str(pm.optionMenu('AutomaticSynchronization', q=1, select=1))
            f.write(a)
        self.AdjustPanelPpresets()
    #�½�ҳ��
    def NewPage(self):
        name = cmds.textFieldGrp('NewFileName', q=1 ,text=1)
        if name:
            file=open((self.file_pathA + '/Py_PresetTemplate_Material/AutomaticSynchronizationSettings/'+name+'.txt'), 'w')
            a0 = pm.optionMenu('LoadBsModelTemplate', q=1, select=1)  # �޸�����ģ��
            a1 = pm.optionMenu('GenerateLocatorScheme', q=1, select=1)  # �޸����붨λ��
            a2 = cmds.checkBox('RemoveKeepmirror', q=1, value=1) # �޸ı��־���
            if a2:
                a2=1
            else:
                a2 = 0
            a3 = pm.optionMenu('ControllerGenerationMethod', q=1, select=1)  # �޸ı��ֳ���
            a4 = cmds.checkBox('AdsorptionSurface', q=1, value=1)  # �޸���������
            if a4:
                a4=1
            else:
                a4 = 0
            a5 = pm.optionMenu('AddAutomatic', q=1, select=1)  # �޸��������
            a6 = pm.optionMenu('LinkBs', q=1, select=1)  # �޸�����bs
            a7 = pm.optionMenu('CustomPanel', q=1, select=1)  # �޸��Զ������
            a8 = pm.optionMenu('CustomPanelLink', q=1, select=1)  # �޸��Զ�������
            a9 = cmds.textFieldGrp('BsIntermediateFrameIntervalSymbol', q=1, text=1)  # bs�м�֡�淶
            a10 = pm.optionMenu('GameSpecifications', q=1, select=1)  # �޸���Ϸ��������
            a11 = pm.optionMenu('FilmSpecifications', q=1, select=1)  # �޸�Ӱ�Ӳ�������
            a12 = pm.optionMenu('CustomModification', q=1, select=1)  # �޸�Ӱ�Ӳ�������
            w = (str(a0)+'\n'+str(a1)+'\n'+str(a2)+'\n'+str(a3)+'\n'+str(a4)+'\n'+str(a5)+'\n'+str(a6)+'\n'+str(a7)+'\n'+str(a8)+'\n'+a9+'\n'+str(a10)+'\n'+str(a11)+'\n'+str(a12))
            file.write(w)
        else:
            pm.error('������ļ����ƣ�')
    #����ҳ��
    def SavePage(self):
        name = pm.optionMenu('AutomaticSynchronization', q=1, value=1)
        if name:
            file=open((self.file_pathA + '/Py_PresetTemplate_Material/AutomaticSynchronizationSettings/'+name+'.txt'), 'w')
            a0 = pm.optionMenu('LoadBsModelTemplate', q=1, select=1)  # �޸�����ģ��
            a1 = pm.optionMenu('GenerateLocatorScheme', q=1, select=1)  # �޸����붨λ��
            a2 = cmds.checkBox('RemoveKeepmirror', q=1, value=1) # �޸ı��־���
            if a2:
                a2=1
            else:
                a2 = 0
            a3 = pm.optionMenu('ControllerGenerationMethod', q=1, select=1)  # �޸ı��ֳ���
            a4 = cmds.checkBox('AdsorptionSurface', q=1, value=1)  # �޸���������
            if a4:
                a4=1
            else:
                a4 = 0
            a5 = pm.optionMenu('AddAutomatic', q=1, select=1)  # �޸��������
            a6 = pm.optionMenu('LinkBs', q=1, select=1)  # �޸�����bs
            a7 = pm.optionMenu('CustomPanel', q=1, select=1)  # �޸��Զ������
            a8 = pm.optionMenu('CustomPanelLink', q=1, select=1)  # �޸��Զ�������
            a9 = cmds.textFieldGrp('BsIntermediateFrameIntervalSymbol', q=1, text=1)  # bs�м�֡�淶
            print(a9)
            a10 = pm.optionMenu('GameSpecifications', q=1, select=1)  # �޸���Ϸ��������
            a11 = pm.optionMenu('FilmSpecifications', q=1, select=1)  # �޸�Ӱ�Ӳ�������
            a12 = pm.optionMenu('CustomModification', q=1, select=1)  # �޸�Ӱ�Ӳ�������
            w = (str(a0)+'\n'+str(a1)+'\n'+str(a2)+'\n'+str(a3)+'\n'+str(a4)+'\n'+str(a5)+'\n'+str(a6)+'\n'+str(a7)+'\n'+str(a8)+'\n'+a9+'\n'+str(a10)+'\n'+str(a11)+'\n'+str(a12))
            file.write(w)
        else:
            pm.error('������ļ����ƣ�')
    #�������Ԥ��
    def AdjustPanelPpresets(self):
        f = open((self.file_pathA+'/Py_PresetTemplate_Material/AutomaticSynchronizationSettings/'+pm.optionMenu('AutomaticSynchronization',q=1, value=1)+'.txt'))  # ����һ���ļ�����
        line = f.readlines()
        f.close()
        pm.optionMenu('LoadBsModelTemplate', e=1, select=int(line[0]))#�޸�����ģ��
        self.ModifyLocPreset('GenerateLocatorScheme')
        pm.optionMenu('GenerateLocatorScheme', e=1, select=int(line[1]))#�޸����붨λ��
        cmds.checkBox('RemoveKeepmirror', e=1, value=int(line[2]))#�޸ı��־���
        pm.optionMenu('ControllerGenerationMethod', e=1, select=int(line[3]))#�޸ı��ֳ���
        cmds.checkBox('AdsorptionSurface', e=1, value=int(line[4]))#�޸���������
        pm.optionMenu('AddAutomatic', e=1, select=int(line[5]))#�޸��������
        pm.optionMenu('LinkBs', e=1, select=int(line[6]))#�޸�����bs
        pm.optionMenu('CustomPanel', e=1, select=int(line[7]))  # �޸��Զ������
        pm.optionMenu('CustomPanelLink', e=1, select=int(line[8]))#�޸��Զ�������
        cmds.textFieldGrp('BsIntermediateFrameIntervalSymbol', e=1,text=line[9][:-1])#bs�м�֡�淶
        pm.optionMenu('GameSpecifications', e=1, select=int(line[10]))#�޸���Ϸ��������
        pm.optionMenu('FilmSpecifications', e=1, select=int(line[11]))#�޸�Ӱ�Ӳ�������
        pm.optionMenu('CustomModification', e=1, select=int(line[12]))#�޸�Ӱ�Ӳ�������
    #����Ӧģ���޸Ķ�λ���ز��б�
    def ModifyLocPreset(self,Name):
        AllButton=(pm.optionMenu('GenerateLocatorScheme',q=1,fullPathName=1))
        cmds.deleteUI(AllButton, control=True)
        file = (self.file_pathA + '/Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial/' + (pm.optionMenu('LoadBsModelTemplate', q=1, value=1)) + '_Programme')
        pm.optionMenu(Name,parent='ChangeRowColumnLayout')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix(file,0,'.ma')):
            pm.menuItem(file, label=file,parent=Name)
        #�޸Ĵ�����
        cmds.iconTextButton('ChangeIconTextButton',e=1,command='os.startfile(\''+self.file_path+'\Py_PresetTemplate_Material\PresetTemplate_TemplateMaterial\\'+str(pm.optionMenu('LoadBsModelTemplate', q=1, value=1))+'_Programme\')')
    #����ģ��
    def LoadEmoticonTemplate(self,FileName,AdditionalPath,Keep):
        if Keep<1:
            if pm.objExists('FaceTemplate_Grp'):
                pm.delete('FaceTemplate_Grp')
        ZKM_FileProcessingClass().ZKM_ImportFile(self.file_path,self.file_pathA,FileName, AdditionalPath,1,'.ma','mayaAscii')
        pm.select('FaceTemplate_Grp')
        pm.select('FaceTemplate_Grp', r=1)

        pm.parent('FaceCamera1','FaceTemplate_Grp')
        #cmds.window('PresetTemplate',edit=True, cc='ZKM_PresetTemplate().CleanWindow()')
        pm.setAttr('FaceTemplate_Grp.translateX',99)
        pm.select('FaceTemplate_Grp')
    #����Ϊģ��
    def AlsVorlageImportieren(self):
        Sel=pm.ls(sl=1)
        sel=str(Sel)
        pm.mel.rename('FaceTemplate_Grp')
        pm.cmds.file((self.file_pathA + '/Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial/' + sel.split('\'')[1] + '.ma'), pr=1, typ='mayaAscii', force=1, options="v=0;", es=1)
        os.makedirs((self.file_path + '\\Py_PresetTemplate_Material\\PresetTemplate_TemplateMaterial\\' + sel.split('\'')[1] + '_Programme'))
    #��ӽű�
    def AddScriptJob(self):
        global jobNum
        jobNum = cmds.scriptJob(e=['SelectionChanged', 'ZKM_PresetTemplate().ScriptJobCommand()'], protected=True)
        jobs = cmds.scriptJob(listJobs=True)
        pm.select(cl=1)
    #����ű�
    def DeleteScriptJob(self,jobNum):
        if jobNum:
            cmds.scriptJob(kill=jobNum, force=True)
    #�ű�ִ�е�����
    def ScriptJobCommand(self):
        if cmds.checkBox('OPorEDScriptJob', q=1,value=1)>0:
            SelParent = pm.listRelatives(p=1)
            if SelParent:
                for Grp in ['FaceTemplate_R', 'FaceTemplate_M', 'FaceTemplate_L']:
                    if SelParent[0] == Grp:
                        sel = pm.ls(sl=1)
                        pm.select('FaceTemplate_LocGrp')
                        pm.mel.eval('SelectHierarchy;')
                        AllLocShape=pm.ls(sl=1,type='locator')
                        for LocShape in AllLocShape:
                            pm.setAttr((LocShape + '.overrideEnabled'),1)
                            pm.setAttr((LocShape + '.overrideColor'), 18)
                        pm.setAttr((sel[0] + 'Shape.overrideEnabled'), 1)
                        pm.setAttr((sel[0] + 'Shape.overrideColor'), 14)
                        pm.select('FaceLoc_'+sel[0])
            if SelParent:
                for Grp in ['FaceLoc_R', 'FaceLoc_M', 'FaceLoc_L']:
                    if SelParent[0] == Grp:
                        sel = pm.ls(sl=1)
                        pm.select('FaceTemplate_LocGrp')
                        pm.mel.eval('SelectHierarchy;')
                        AllLocShape = pm.ls(sl=1, type='locator')
                        for LocShape in AllLocShape:
                            pm.setAttr((LocShape + '.overrideEnabled'), 1)
                            pm.setAttr((LocShape + '.overrideColor'), 18)
                        pm.setAttr((sel[0][8:] + 'Shape.overrideEnabled'), 1)
                        pm.setAttr((sel[0][8:] + 'Shape.overrideColor'), 14)
                        pm.select(sel)
    #���붨λ��
    def ImportLoc(self):
        if pm.objExists('FaceTemplate_LocGrp'):
            pm.delete('FaceTemplate_LocGrp')
        ImportLocFolder = pm.optionMenu('LoadBsModelTemplate', q=1, value=1)
        ImportLoc = pm.optionMenu('GenerateLocatorScheme', q=1, value=1)
        pm.mel.performFileSilentImportAction(self.file_pathA + '/Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial/' + ImportLocFolder + '_Programme/' + ImportLoc + '.ma')
        pm.parent('FaceTemplate_LocGrp','FaceTemplate_Grp')
        #���ݶ�λ��λ�����ɶ�Ӧ��λ���ͽű�
        pm.select(cl=1)
        pm.delete(pm.pointConstraint('FaceTemplate_LocGrp',(pm.group(n='FaceLoc_Grp'))))
        pm.select(cl=1)
        pm.group(n='FaceLoc_R')
        pm.select(cl=1)
        pm.group(n='FaceLoc_M')
        pm.select(cl=1)
        pm.group(n='FaceLoc_L')
        pm.setAttr("FaceLoc_L.scaleX",-1)
        pm.select('FaceLoc_R','FaceLoc_M','FaceLoc_L')
        pm.parent('FaceLoc_R','FaceLoc_M','FaceLoc_L','FaceLoc_Grp')
        for Grp in ['FaceTemplate_R','FaceTemplate_M','FaceTemplate_L']:
            AllLoc=pm.listRelatives(Grp, c=1)
            for Loc in AllLoc:
                print (Loc)
                pm.spaceLocator(p=(0, 0, 0), n=('FaceLoc_' + Loc))
                if pm.listRelatives(Loc, p=1)[0] == Grp:
                    print(Loc)
                    pm.parent(('FaceLoc_' + Loc), ('FaceLoc_'+Grp[-1:]))
                    pm.delete(pm.parentConstraint(Loc, ('FaceLoc_' + Loc)))
                    pm.mel.channelBoxCommand('-freezeAll')
        pm.setAttr('FaceLoc_Grp.translateX',0)
        Colour = cmds.button('ImportLocButton', q=1, bgc=1)
        if Colour[0] == 0:
            cmds.button('ImportLocButton',e=1, bgc=(1,1,1))
        else:
            self.DeleteScriptJob(jobNum)
            cmds.button('ImportLocButton', e=1, bgc=(1, 1, 1))
        pm.setAttr("FaceTemplate_LocGrp.translateX", 0)
        #��ӽű�
        self.AddScriptJob()
        self.SymmetricLink()
    #�Գ�����
    def SymmetricLink(self):
        for sel in (pm.listRelatives('FaceLoc_R', c=1)):
            for Attribute in ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ']:
                AttributeAll = cmds.listConnections((sel[:-1]+'L' + Attribute),p=1)
                if AttributeAll:
                    pm.disconnectAttr(str(AttributeAll[0]), (sel[:-1]+'L' + Attribute))
            if cmds.checkBox('RemoveKeepmirror', q=1, value=1)>0:
                for Attribute in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']:
                    pm.connectAttr((sel+Attribute), (sel[:-1]+'L'+Attribute), f=1)
    #���涨λ���ļ�
    def SaveLocFile(self):
        pm.select('FaceTemplate_LocGrp')
        pm.parent(w=1)
        pm.setAttr("FaceTemplate_LocGrp.translateX", 0)
        NameFile = pm.optionMenu('LoadBsModelTemplate', q=1, value=1)
        ZKM_FileProcessingClass().ZKM_ImportFile(self.file_path,self.file_pathA,'GenerateLocatorScheme', ('Py_PresetTemplate_Material/PresetTemplate_TemplateMaterial/'+NameFile+'_Programme'), 0, '.ma', 'mayaAscii')
        pm.parent('FaceTemplate_LocGrp','FaceTemplate_Grp')
        pm.setAttr("FaceTemplate_LocGrp.translateX", 0)
    #���ɿ�����
    def CreateController(self):
        GetModel = cmds.textFieldButtonGrp('LoadName', q=1, text=1)  # ��ȡģ��
        if not GetModel:
            pm.error('�����ģ��')
        if not 'FaceLoc_Grp':
            pm.error('�뵼�붨λ��')
        JobOPED = cmds.checkBox('OPorEDScriptJob', q=1, value=1)
        cmds.checkBox('OPorEDScriptJob', e=1, value=0)
        OpenLink = cmds.checkBox('RemoveKeepmirror', q=1, value=1)  # �Ƿ������
        if str(OpenLink) == 'True':
            cmds.checkBox('RemoveKeepmirror', e=1, value=0)
            self.SymmetricLink()
        Direction = pm.optionMenu('ControllerGenerationMethod', q=1, sl=1)#�жϳ���
        AdsorptionSurface = cmds.checkBox('AdsorptionSurface', q=1, value=1)#�Ƿ���������
        pm.select(cl=1)
        pm.group(n='Face_Grp')
        pm.select('FaceLoc_Grp')
        pm.mel.eval('SelectHierarchy;')
        AllLocShape = pm.ls(sl=1, type='locator')
        if Direction == 2:
            loc = pm.spaceLocator(p=(0, 0, 0))
            for LocShape in AllLocShape:
                pm.select(LocShape)
                pm.pickWalk(d='up')
                LocShape=pm.ls(sl=1)
                pm.delete(pm.pointConstraint(LocShape,loc))
                pm.delete(pm.parentConstraint(loc,LocShape))
            pm.delete(loc)
        pm.select(AllLocShape)
        pm.pickWalk(d='up')
        Loc = pm.ls(sl=1)
        pm.select('FaceLoc_Head_loc_M','FaceLoc_Jaw_loc_M','FaceLoc_Mouth_loc_M','FaceLoc_Eye_loc_R','FaceLoc_Eye_loc_R',d=1)
        SELA = pm.ls(sl=1)
        ZKM_FollicleClass().ZKM_FollicleConstraint(GetModel,SELA,str(AdsorptionSurface))
        pm.delete('AllFollicle_Grp')
        #����λ�����ɿ�����
        for l in Loc:
            pm.select(cl=1)
            pm.joint(p=(0, 0, 0), n=(l[8:-6] + '_CurveJoint_' + l[-1:]))
            pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.2, tol=0.01, nr=(1, 0, 0), n=(l[8:-6] + '_Curve_' + l[-1:]))
            pm.group(n=(l[8:-6] + '_Group2' + l[-1:]))
            pm.group(n=(l[8:-6] + '_Group1' + l[-1:]))
            pm.parent((l[8:-6] + '_CurveJoint_' + l[-1:]), (l[8:-6] + '_Curve_' + l[-1:]))
            pm.delete(pm.parentConstraint(l, (l[8:-6] + '_Group1' + l[-1:])))
            pm.parent((l[8:-6] + '_Group1' + l[-1:]),'Face_Grp')
            #��Ӿ���ֽ�
            pm.shadingNode('decomposeMatrix', asUtility=1,n=(l[8:-6] + '_Curve_' + l[-1:]+'_decomposeMatrix1'))
            pm.connectAttr((l[8:-6] + '_Curve_' + l[-1:]+'.inverseMatrix'), (l[8:-6] + '_Curve_' + l[-1:]+'_decomposeMatrix1.inputMatrix'), force=1)
            pm.connectAttr((l[8:-6] + '_Curve_' + l[-1:]+'_decomposeMatrix1.outputTranslate'), (l[8:-6] + '_Group2' + l[-1:]+'.translate'), f=1)
            pm.connectAttr((l[8:-6] + '_Curve_' + l[-1:]+'_decomposeMatrix1.outputRotate'), (l[8:-6] + '_Group2' + l[-1:]+'.rotate'), f=1)
            pm.connectAttr((l[8:-6] + '_Curve_' + l[-1:]+'_decomposeMatrix1.outputScale'), (l[8:-6] + '_Group2' + l[-1:]+'.scale'), f=1)

        AllControllerGrp = pm.listRelatives('Face_Grp', c=1)
        pm.select(AllControllerGrp)
        ControllerGrp= pm.ls(sl=1)
        pm.select('Head_Group1M', 'Jaw_Group1M', 'Mouth_Group1M', 'Eye_Group1R','Eye_Group1L', d=1)
        SELB = pm.ls(sl=1)
        ZKM_FollicleClass().ZKM_FollicleConstraint(GetModel,SELB,'True')
        if Direction == 1:
            for ConGrp in ControllerGrp:
                if ConGrp[-1:]=='L':
                    pm.setAttr((ConGrp + '.scaleX'), -1)
                    pm.setAttr((ConGrp + '.scaleY'), -1)
                    pm.setAttr((ConGrp + '.scaleZ'), -1)
        if str(JobOPED) == 'True':
            cmds.checkBox('OPorEDScriptJob', e=1, value=1)
        if str(OpenLink) == 'True':
            cmds.checkBox('RemoveKeepmirror', e=1, value=1)
            self.SymmetricLink()
        pm.setAttr('AllFollicle_Grp.visibility',0)
        pm.setAttr('FaceLoc_Grp.visibility', 0)
    #����������������
    def BsConvertControllerDrive(self):
        AllConstraintGrp = pm.listRelatives('Face_Grp',c=1)
        BS = cmds.textFieldButtonGrp('LoadBS', q=1,text=1)
        bs = BS.split(',')
        ZKM_Bs().ZKM_BsConvertControllerDrive(AllConstraintGrp,bs)
    #����μ������Լ�������
    def SupplementJointController(self):
        pm.select(cl=1)
        pm.group(n='FaceJoint_Grp')
        pm.select('FaceLoc_Grp')
        pm.mel.eval('SelectHierarchy;')
        AllLocShape = pm.ls(sl=1, type='locator')
        pm.select(AllLocShape)
        pm.pickWalk(d='up')
        Loc = pm.ls(sl=1)
        for l in Loc:
            pm.select(cl=1)
            pm.joint(p=(0, 0, 0),n=(l[8:-6] + '_Joint_' + l[-1:]))
            pm.group( n=(l[8:-6] + '_JointGrp_' + l[-1:]))
            pm.joint(p=(0, 0, 0), n=(l[8:-6] + '_GameJoint_' + l[-1:]))
            pm.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=0.1, tol=0.01, nr=(1, 0, 0),n=(l[8:-6] + '_Joint_Curve_' + l[-1:]))
            pm.parent((l[8:-6] + '_GameJoint_' + l[-1:]), (l[8:-6] + '_Joint_Curve_' + l[-1:]))
            pm.select((l[8:-6] + '_Joint_Curve_' + l[-1:]))
            pm.group(n=(l[8:-6] + '_Joint_Group2' + l[-1:]))
            pm.group(n=(l[8:-6] + '_Joint_Group1' + l[-1:]))
            pm.delete(pm.parentConstraint((l[8:-6] + '_Curve_' + l[-1:]), (l[8:-6] + '_JointGrp_' + l[-1:])))
            pm.delete(pm.parentConstraint((l[8:-6] + '_Curve_' + l[-1:]), (l[8:-6] + '_Joint_Group1' + l[-1:])))
            pm.parent((l[8:-6] + '_Joint_Group1' + l[-1:]), (l[8:-6] + '_Curve_' + l[-1:]))
            pm.parent((l[8:-6] + '_JointGrp_' + l[-1:]), 'FaceJoint_Grp')

            pm.connectAttr((l[8:-6] + '_Joint_Curve_' + l[-1:]+'.translate'), (l[8:-6] + '_Joint_' + l[-1:]+'.translate'), f=1)
            pm.connectAttr((l[8:-6] + '_Joint_Curve_' + l[-1:]+'.rotate'), (l[8:-6] + '_Joint_' + l[-1:]+'.rotate'), f=1)
            pm.connectAttr((l[8:-6] + '_Joint_Curve_' + l[-1:]+'.scale'), (l[8:-6] + '_Joint_' + l[-1:]+'.scale'), f=1)
            # ��Ӿ���ֽ�
            pm.shadingNode('decomposeMatrix', asUtility=1, n=(l[8:-6] + '_Joint_' + l[-1:] + '_decomposeMatrix'))
            pm.connectAttr((l[8:-6] + '_Joint_Curve_' + l[-1:] + '.inverseMatrix'),(l[8:-6] + '_Joint_' + l[-1:] + '_decomposeMatrix.inputMatrix'), force=1)
            pm.connectAttr((l[8:-6] + '_Joint_' + l[-1:] + '_decomposeMatrix.outputTranslate'),(l[8:-6] + '_Joint_Group2' + l[-1:] + '.translate'), f=1)
            pm.connectAttr((l[8:-6] + '_Joint_' + l[-1:] + '_decomposeMatrix.outputRotate'),(l[8:-6] + '_Joint_Group2' + l[-1:] + '.rotate'), f=1)
            pm.connectAttr((l[8:-6] + '_Joint_' + l[-1:] + '_decomposeMatrix.outputScale'),(l[8:-6] + '_Joint_Group2' + l[-1:] + '.scale'), f=1)
    #������Բ�����
    def AddAttributesAndAink(self):
        AddAutomaticFileName = pm.optionMenu('AddAutomatic', q=1, value=1)
        LinkBsFileName = pm.optionMenu('LinkBs', q=1, value=1)
        ZKM_FileProcessingClass().ZKM_RunCorrespondingCommand(self.file_pathA+'/Py_PresetTemplate_Material/AutoLinkBsScheme/AddAttributes/'+AddAutomaticFileName)
        ZKM_FileProcessingClass().ZKM_RunCorrespondingCommand(self.file_pathA + '/Py_PresetTemplate_Material/AutoLinkBsScheme/LinkBs/'+LinkBsFileName)
    #�����Զ�������
    def CustomLinks(self):
        AddAutomaticFileName = pm.optionMenu('CustomPanelLink', q=1, value=1)
        ZKM_FileProcessingClass().ZKM_RunCorrespondingCommand(self.file_pathA+'/Py_PresetTemplate_Material/CustomPanel/'+AddAutomaticFileName)
    #������Ϸ�淶��������
    def GameCustomLinks(self):
        AddAutomaticFileName = pm.optionMenu('GameSpecifications', q=1, value=1)
        ZKM_FileProcessingClass().ZKM_RunCorrespondingCommand(self.file_pathA+'/Py_PresetTemplate_Material/BS_IntermediateFrame_GameSpecificationScheme/'+AddAutomaticFileName)
    #����Ӱ�ӹ淶��������
    def FilmCustomLinks(self):
        AddAutomaticFileName = pm.optionMenu('FilmSpecifications', q=1, value=1)
        ZKM_FileProcessingClass().ZKM_RunCorrespondingCommand(self.file_pathA+'/Py_PresetTemplate_Material/BS_IntermediateFrame_FilmSpecificationScheme/'+AddAutomaticFileName)
    #�����Զ����޸�
    def CustomModification(self):
        AddAutomaticFileName = pm.optionMenu('CustomPanelLink', q=1, value=1)
        ZKM_FileProcessingClass().ZKM_RunCorrespondingCommand(self.file_pathA+'/Py_PresetTemplate_Material/CustomModification/'+AddAutomaticFileName)
    #�򿪲�ͬ�ز�����bs����
    def Open_DifferentTopologyTransfer_BS(self):
        ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()
    #ɾ���ޱ仯��������Ӱ���м�֡
    def DeleteN(self):
        ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()


