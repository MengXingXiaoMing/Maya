#coding=gbk
import pymel.core as pm
import maya.cmds as cmds
from os import listdir
# ��ȡ�ļ�·��
import os
import inspect
import sys
sys.dont_write_bytecode = True
# �����ı�
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))

#�����ı�
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
#Ȩ����
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaWeight')
from JointWeightProcessing import *
#����ģ����
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaModel')
from GenerateModel import *

class ZKM_QvanZhongChuLiWindowClass:
    def __init__(self):
        cur_dir = '\\'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        cur_dirA = '/'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathReversion = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
        # ͨ��self���½��Ķ����г�ʼ������
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
    def ZKM_Window(self):
        if pm.window('WindowQvanZhongChuLiPY', ex=1):
            pm.deleteUI('WindowQvanZhongChuLiPY')

        pm.window('WindowQvanZhongChuLiPY', t='Ȩ�ش���')
        pm.columnLayout()
        pm.rowColumnLayout(nc=1, adj=1)
        pm.rowColumnLayout(nc=3, adj=3)
        pm.rowColumnLayout(nc=2, adj=3)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'XZKBY\')', l='ѡ�񿽱�Դ:')
        pm.textFieldButtonGrp('XZKBY', bl='����', text='', cw3=(0, 100, 65), l='ѡ�񿽱�Դ:',
                              bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'XZKBY\')')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=3)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'XZKBMXHD\')', l='ѡ���追����:')
        pm.textFieldButtonGrp('XZKBMXHD', bl='����', text='', cw3=(0, 100, 65), l='ѡ���追����:',
                              bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'XZKBMXHD\')')
        pm.setParent('..')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_CopyPointWeightApply()', l='������Ȩ��')
        pm.rowColumnLayout(nc=2, adj=2)
        pm.button(c='pm.mel.CopyVertexWeights()', l='���ƶ���Ȩ��')
        pm.button(c='pm.mel.PasteVertexWeights()', l='ճ������Ȩ��')
        pm.button(c='pm.mel.removeUnusedInfluences()', l='�Ƴ���Ȩ�ع���')
        #pm.button(c='ZKM_QvanZhongChuLiCommandsClass().AbsolutePositionMirrorWeight()', l='����λ�þ���Ȩ��(ͣ��)')
        pm.setParent('..')
        pm.rowColumnLayout(nc=7, adj=1)
        pm.iconTextButton(i='paintSkinWeights.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.ArtPaintSkinWeightsTool()', l='')
        pm.iconTextButton(flat=0, style='iconAndTextCentered', i='weightHammer.png', h=45,
                          c='pm.mel.weightHammerVerts()', l='')
        pm.iconTextButton(i='copySkinWeight.png', flat=0, style='iconAndTextCentered', c='pm.mel.CopySkinWeights()',
                          l='')
        pm.iconTextButton(i='mirrorSkinWeight.png', flat=0, style='iconAndTextCentered', c='pm.mel.MirrorSkinWeights()',
                          l='')
        pm.iconTextButton(i='moveSkinnedJoint.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.MoveSkinJointsTool()', l='')
        pm.iconTextButton(i='moveVertexWeights.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.artAttrMoveInfluence()', l='')
        pm.iconTextButton(i='showInfluence.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.artAttrShowInfluences(\'artAttrSkinPaintCtx\')', l='')
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=1)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_CopyModelWeightApply()', l='����Ȩ��(��ѡԴģ��)')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_HalfCopyModelWeightApply()', l='�԰뿽��Ȩ��')
        pm.setParent('..')
        pm.setParent('..')
        pm.rowColumnLayout(nc=3, adj=3)
        pm.optionMenu('NormalizeWeight', label='')
        pm.menuItem(label='����')
        pm.menuItem(label='����')
        pm.optionMenu('NormalizeWeight', edit=1, select=1)
        pm.intSliderGrp('SmoothWeightType', min=1, max=100, cw3=(60, 40, 258), f=1, fieldMaxValue=9999, l='ƽ��������', v=1)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_SmoothWeightApply()', l='ƽ��Ȩ��', w=60)
        pm.setParent('..')
        pm.rowColumnLayout(nc=4, adj=3)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'XZYMX\')', l='ѡ��ԭģ��:')
        pm.textFieldButtonGrp('XZYMX', bl='����', bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'XZYMX\')')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_MergeWeightsToTargetsApply()', l='ѡ��ģ�ͺϲ�Ȩ�ص�Ŀ��')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ExportWeights()', l='����Ȩ��')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ZYQZ\')', l='ѡ��ģ��:')
        pm.textFieldButtonGrp('ZYQZ', bl='����', bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'ZYQZ\')')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().TransferWeights()', l='ת��Ȩ��(��ѡҪת�ƵĹ���)')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ImportWeights()', l='����Ȩ��')
        pm.setParent('..')
        pm.rowColumnLayout(bgc=(0.7, 0.7, 1), adj=2, nc=8)
        pm.textFieldGrp('ModelFace', text='2000', cw2=(80, 70), l='ģ������(����):')
        pm.floatSliderGrp('ReduceDetail', min=1, max=100, cw3=(50, 30, 100), f=1, fieldMaxValue=9999, l='����ϸ��', v=20)
        pm.floatSliderGrp('Smoothness', min=1, max=100, cw3=(50, 40, 100), f=1, fieldMaxValue=9999, l='ƽ���̶�', v=100)
        pm.setParent('..')
        pm.rowColumnLayout(bgc=(0.7, 0.7, 1), adj=1, nc=9)
        
        pm.text(l='��ģ������(������)')
        pm.radioCollection('FKKZQSC_ModelMirror')
        pm.radioButton('None', label='None')
        pm.radioButton('X', label='X��-X')
        pm.radioButton('FX', label='-X��X')
        pm.radioButton('Y', label='Y��-Y')
        pm.radioButton('FY', label='-Y��Y')
        pm.radioButton('Z', label='Z��-Z')
        pm.radioButton('FZ', label='-Z��Z')
        pm.radioCollection('FKKZQSC_ModelMirror', edit=1, select='X')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().GeneratingSimpleModuleApply()', l='���ɼ�ģ(������ģ��)')
        
        pm.setParent('..')
        pm.setParent('..')
        pm.showWindow()
class ZKM_QvanZhongChuLiCommandsClass:
    # ����ѡ��Ϊ�ı�
    def ZKM_LoadText(self, Type, Name):
        ZKM_LoadTextClass().ZKM_LoadText(Type, Name)

    # ѡ���Ӧ�ı�������
    def ZKM_ReadLoadText(self, Type, Name):
        ZKM_ReadTextClass().ZKM_ReadLoadText(Type, Name)

    # ������Ȩ��
    def ZKM_CopyPointWeightApply(self):
        Soure = pm.textFieldButtonGrp('XZKBY', q=1, text=1)
        Target = pm.textFieldButtonGrp('XZKBMXHD', q=1, text=1).split(',')
        ZKM_JointWeightProcessingClass().ZKM_CopyWeight('Normal', Soure, Target, '', '')

    # ����ģ��Ȩ��
    def ZKM_CopyModelWeightApply(self):
        ZKM_JointWeightProcessingClass().ZKM_CopyModelWeightApply()

    # �԰뿽��ģ��Ȩ��
    def ZKM_HalfCopyModelWeightApply(self):
        ZKM_JointWeightProcessingClass().ZKM_HalfCopyModelWeightApply()

    # ƽ��Ȩ��
    def ZKM_SmoothWeightApply(self):
        Model = pm.ls(sl=1)
        NormalizeWeight = int(pm.optionMenu('NormalizeWeight', q=1, select=1))
        CS = pm.intSliderGrp('SmoothWeightType', q=1, v=1)
        ZKM_JointWeightProcessingClass().ZKM_SmoothWeight(Model, NormalizeWeight, CS)

    # ��ģ�ͷ�����������Ȩ�ط�������
    def ZKM_MergeWeightsToTargetsApply(self):
        ModelGrp = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'XZYMX')
        YvanModel = pm.ls(sl=1)
        ZKM_JointWeightProcessingClass().ZKM_MergeWeightsToTargets(YvanModel, ModelGrp)

    # ����Ȩ��
    def ExportWeights(self):
        Model = pm.ls(sl=1)
        MD = []
        for M in Model:
            if pm.mel.findRelatedSkinCluster(M):
                MD.append(M)
                pm.select(M)
                pm.mel.removeUnusedInfluences()
        ZKM_JointWeightProcessingClass().ExportWeight(MD)

    # ����Ȩ��
    def ImportWeights(self):
        Model = pm.ls(sl=1)
        ZKM_JointWeightProcessingClass().ImportWeight(Model)

    # ת��Ȩ��
    def TransferWeights(self):
        Model = str(pm.textFieldButtonGrp('ZYQZ', q=1, text=1))
        ZKM_JointWeightProcessingClass().TransferWeight(Model)

    def GeneratingSimpleModuleApply(self):
        ReduceDetail = float(pm.floatSliderGrp('ReduceDetail', q=1, v=1))
        Smoothness = float(pm.floatSliderGrp('Smoothness', q=1, v=1))
        ModelMirror = str(pm.radioCollection('FKKZQSC_ModelMirror', q=1, select=1))
        FaceNum = float(pm.textFieldGrp('ModelFace', q=1, text=1))
        sel = pm.ls(sl=1)
        ZKM_RegenerateExistingModelClass().GeneratingSimpleModule(sel, FaceNum, ModelMirror, ReduceDetail, Smoothness)

ShowWindow = ZKM_QvanZhongChuLiWindowClass()
if __name__ == '__main__':
    ShowWindow.ZKM_Window()
