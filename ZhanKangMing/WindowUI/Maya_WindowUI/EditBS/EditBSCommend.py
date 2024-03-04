#coding=gbk
import maya.cmds as cmds
import pymel.core as pm
import os
import sys
import inspect
#��Ŀ¼
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# �����ı�
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaBS')
from BsAddIntermediateFramesAccordingSpecifications import *

class ZKM_EditBSCommend():
    def __init__(self):
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
    def LinkBS(self):
        SoureDictionary = pm.optionMenu('EditBSWindow_LinkSoure', q=1, v=1)
        SoureDictionary = SoureDictionary.encode('utf-8')
        Target = pm.optionMenu('EditBSWindow_LinkTarget', q=1, v=1)
        Target = Target.encode('utf-8')
        BSName = pm.optionMenu('EditBSWindow_LinkBSName', q=1, v=1)
        f = open(self.file_pathReversion + '/Soure/'+SoureDictionary+'.txt')  # ����һ���ļ�����
        SoureDictionaryLine = f.readlines()
        f.close()
        f = open(self.file_pathReversion + '/Target/' + Target + '.txt')  # ����һ���ļ�����
        TargetLine = f.readlines()
        f.close()
        # ��ʼ����
        for i in range(0,len(TargetLine)):
            if pm.objExists(BSName+'.'+TargetLine[i]):
                Soure = eval(SoureDictionaryLine[i])
                soure = Soure['soure']
                mapping = Soure['mapping']
                remapValue = pm.shadingNode('remapValue', asUtility=1)
                pm.setAttr(remapValue+'.inputMin',mapping[0])
                pm.setAttr(remapValue + '.inputMax', mapping[1])
                pm.setAttr(remapValue + '.outputMin', mapping[2])
                pm.setAttr(remapValue + '.outputMax', mapping[3])
                pm.connectAttr(soure, remapValue+'.inputValue', f=1)
                pm.connectAttr(remapValue + '.outValue', BSName+'.'+TargetLine[i], f=1)

    def AddBSIntermediateFrame(self):
        BSName = cmds.textFieldButtonGrp('Addintermediate_BSName', q=1, text=1)
        Soure = cmds.textFieldButtonGrp('Addintermediate_Soure', q=1, text=1)
        Difference = cmds.textFieldButtonGrp('Addintermediate_Difference', q=1, text=1)
        ZKM_BsIntermediateFrame().ZKM_AsSpecificationsAddBSIntermediateFrame(BSName, Soure, Difference)

    def BSIntermediateFrameToGameSpecifications(self):
        BSName = cmds.textFieldButtonGrp('GameSpecifications_BSName', q=1, text=1)
        Soure = cmds.textFieldButtonGrp('GameSpecifications_Soure', q=1, text=1)
        ZKM_BsIntermediateFrame().ZKM_BSIntermediateFrameConversionSpecification(Soure, BSName)

    def BakeBs(self):
        BSName = cmds.textFieldButtonGrp('BakeBs_BSName', q=1, text=1)
        Soure = cmds.textFieldButtonGrp('BakeBs_Soure', q=1, text=1)
        ZKM_BsIntermediateFrame().ZKM_BakeBsBackDictionary(Soure, BSName)