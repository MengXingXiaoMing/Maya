# coding=gbk
import pymel.core as pm
# ��ȡ�ļ�·��
import os
import inspect
import sys
sys.dont_write_bytecode = True
# �����ı�
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-5]))
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaBS')
from BsModelEdit import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaWeight')
from JointWeightProcessing import *
import webbrowser

class ZKM_WindowBsChuLiWindowClass:
    def __init__(self):
        cur_dir = '\\'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
        cur_dirA = '/'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
        file_pathReversion = os.path.join(cur_dirA)  # ��ȡ�ļ�·��A
        # ͨ��self���½��Ķ����г�ʼ������
        self.file_path = file_path
        self.file_pathA = file_pathReversion
    def ZKM_WindowBsChuLi(self):
        if pm.window('WindowBsChuLi', ex=1):
            pm.deleteUI('WindowBsChuLi')
        pm.window('WindowBsChuLi', t="BS����")
        pm.columnLayout()
        pm.rowColumnLayout(nc=2, adj=1)
        pm.rowColumnLayout(nc=1, adj=2)
        pm.rowColumnLayout(nc=6, adj=1)
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_OpenWrap4D()', l="ѡ��ģ�Ϳ�ʼ�����м�̬ģ��(��ѡģ��ģ��)")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().ImportIntermediate()', l="�����м�̬ģ��")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_TransferUV()', l="����UV����ѡ�м�̬ģ�ͣ���ѡĿ��ģ�ͣ�")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_SelectPointCorrectUV()', l="ѡ�������UV(�����ص���ֻ�����ɵ㲿��)")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_TestTemplate()', bgc=(1, 1, 1), l="ģ��")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_UsingHelp()', bgc=(1, 1, 1), l="����")
        pm.setParent('..')
        pm.rowColumnLayout(nc=8, adj=8)
        pm.text(l="���ز�����BS��")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_TransmitSource\')', l="��BS��ģ��:")
        pm.textFieldButtonGrp('BsCL_TransmitSource', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_TransmitSource\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_IntermediateState\')', l="�м�̬ģ��:")
        pm.textFieldButtonGrp('BsCL_IntermediateState', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_IntermediateState\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_TransmitTarget\')', l="BS����Ŀ��:")
        pm.textFieldButtonGrp('BsCL_TransmitTarget', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_TransmitTarget\')')
        pm.rowColumnLayout(nc=8, adj=8)
        pm.button(c='ZKM_WindowBsChuLiWindowClass().TransferDifferentTopologies_BS()', l="����bs")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().UVCopyWeight()', l='UV����Ȩ��')
        pm.setParent('..')
        pm.text(l="�決bs��ģ�ͣ�")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel\')', l="��決ģ��:")
        pm.textFieldButtonGrp('BsCL_BakingModel', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel_BS\')', l="ѡ��BS�ڵ�:")
        pm.textFieldButtonGrp('BsCL_BakingModel_BS', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel_BS\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_BakingBsAttribute\')', l="����BS����:")
        pm.textFieldButtonGrp('BsCL_BakingBsAttribute', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BakingBsAttribute\')')
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BakingBS()', l="�決BS")
        pm.text(l="�ֽ�BS��")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource\')', l="�ֽ�Դģ��:")
        pm.textFieldButtonGrp('BsCL_DecomposeSource', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource_BS\')', l="����BS����:")
        pm.textFieldButtonGrp('BsCL_DecomposeSource_BS', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource_BS\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_DecomposereFerence\')', l="�ֽ�ο�ģ��")
        pm.textFieldButtonGrp('BsCL_DecomposereFerence', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_DecomposereFerence\')')
        pm.button(c='ZKM_WindowBsChuLiWindowClass().DecomposeBS()', l="��ʼ�ֽ�")
        pm.text(l="BSתȨ�أ�")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',"BsCL_BsTransmitWeightModel")', l="��BS��ģ��:")
        pm.textFieldButtonGrp('BsCL_BsTransmitWeightModel', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BsTransmitWeightModel\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',"BsCL_BsTransmitWeightModel_BS")', l="ѡ��BS�ڵ�:")
        pm.textFieldButtonGrp('BsCL_BsTransmitWeightModel_BS', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BsTransmitWeightModel_BS\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',"BsCL_BsTransmitWeightJoint")', l="��������:")
        pm.textFieldButtonGrp('BsCL_BsTransmitWeightJoint', bl="����", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BsTransmitWeightJoint\')')
        pm.button(c='ZKM_WindowBsChuLiWindowClass().HairFollicleAdsorption()', l="��ʼת��")
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.showWindow()

    # ��ģ���ļ�������Wrap4D
    def BsCL_OpenWrap4D(self):
        Sel = pm.ls(sl=1)
        pm.select(Sel[0], r=1)
        pm.mel.eval(
            'file -force -options \"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\" -typ \"OBJexport\" -pr -es (\"' + self.file_pathA + '/WrapPreset/source.obj\");')
        pm.select(Sel[1], r=1)
        pm.mel.eval(
            'file -force -options \"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\" -typ \"OBJexport\" -pr -es (\"' + self.file_pathA + '/WrapPreset/target.obj\");')
        os.startfile(self.file_path + '\\WrapPreset\\WrapTemplate.wrap')

    # �����м�̬ģ��
    def ImportIntermediate(self):
        pm.mel.eval(
            'file -import -type "OBJ"  -ignoreVersion -mergeNamespacesOnClash false -rpr "WrapObject" -options "mo=1"  -pr  -importTimeRange "combine" (\"' + self.file_pathA + '/WrapPreset/WrapObject.obj\");')

    # ���淶����UV
    def BsCL_TransferUV(self):
        Sel = pm.ls(sl=1)
        pm.select(Sel[0])
        UVsetA = pm.polyUVSet(q=1, currentUVSet=1)[0]
        pm.select(Sel[1])
        UVsetB = pm.polyUVSet(q=1, currentUVSet=1)[0]
        pm.select(Sel[0],Sel[1])
        pm.transferAttributes(flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace=str(UVsetA), searchMethod=3,
                              transferNormals=0, transferColors=2, targetUvSpace=str(UVsetB), colorBorders=1, sampleSpace=0)
        pm.select(Sel[1], r=1)
        pm.DeleteHistory()

    # ѡ�������UV
    def BsCL_SelectPointCorrectUV(self):
        Sel = pm.ls(fl=1, sl=1)
        Model = Sel[0].split(".")
        pm.mel.polyPerformAction('polyMapSew', 'e', 0)
        pm.select(cl=1)
        pm.select(Sel, r=1)
        pm.mel.performUnfold(0)
        pm.select(cl=1)
        pm.select(Model[0], r=1)
        pm.DeleteHistory()

    # ����ģ��
    def BsCL_TestTemplate(self):
        os.startfile(self.file_path + '\ZKM_TransferDifferentTopologies_BS.mb')
        print ('\nʹ�ý̳���Ƶ���ӣ�\nhttps://space.bilibili.com/173984578')
        webbrowser.open("https://space.bilibili.com/173984578")

    # ʹ�ð���
    def BsCL_UsingHelp(self):
        os.startfile(self.file_path + '\help.png')
        print ('\nʹ�ý̳���Ƶ���ӣ�\nhttps://space.bilibili.com/173984578')
        webbrowser.open("https://space.bilibili.com/173984578")
    # ��ͬ�ز�����BS
    def TransferDifferentTopologies_BS(self):
        TransmitSource = str(pm.textFieldButtonGrp('BsCL_TransmitSource', q=1, text=1))
        TransmitTarget = str(pm.textFieldButtonGrp('BsCL_TransmitTarget', q=1, text=1))
        IntermediateState = str(pm.textFieldButtonGrp('BsCL_IntermediateState', q=1, text=1))
        ZKM_DifferentTopologiesBSClass().ZKM_TransferDifferentTopologies_BS(TransmitSource, TransmitTarget, IntermediateState)


    # �決BS
    def BakingBS(self):
        BakingModel = str(pm.textFieldButtonGrp('BsCL_BakingModel', q=1, text=1))
        BakingModel_BS = str(pm.textFieldButtonGrp('BsCL_BakingModel_BS', q=1, text=1))
        BakingBsAttribute = str(pm.textFieldButtonGrp('BsCL_BakingBsAttribute', q=1, text=1))
        BakingBsAttributeAll = BakingBsAttribute.split(",")
        ZKM_DifferentTopologiesBSClass().ZKM_BakingBS(BakingModel, BakingModel_BS,BakingBsAttributeAll)

    # �ֽ�BS
    def DecomposeBS(self):
        DecomposeSource = str(pm.textFieldButtonGrp('BsCL_DecomposeSource', q=1, text=1))
        DecomposeSource_BS = str(pm.textFieldButtonGrp('BsCL_DecomposeSource_BS', q=1, text=1))
        DecomposereFerence = str(pm.textFieldButtonGrp('BsCL_DecomposereFerence', q=1, text=1))
        DecomposeSourceAll = DecomposeSource_BS.split(",")
        ZKM_DifferentTopologiesBSClass().ZKM_DecomposeBS(DecomposeSource,DecomposeSourceAll,DecomposereFerence)

    # UV����Ȩ��
    def UVCopyWeight(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp','BsCL_TransmitSource')
        DecomposeSource = pm.ls(sl=1)
        UVsetA = pm.polyUVSet(q=1, currentUVSet=1)[0]
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'BsCL_TransmitTarget')
        DecomposereFerence = pm.ls(sl=1)
        UVsetB = pm.polyUVSet(q=1, currentUVSet=1)[0]
        ZKM_JointWeightProcessingClass().ZKM_CopyWeight('UV', DecomposeSource[0], DecomposereFerence, UVsetA, UVsetB)

    # bsתȨ��
    def HairFollicleAdsorption(self):
        print '��δ����\n'


if __name__ == '__main__':
    ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()
