#coding=gbk
import pymel.core as pm
import os
import sys
import inspect

#��Ŀ¼
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# ���ض�Ӧ��׺�ļ�
sys.path.append(ZKM_RootDirectory+'\\Common\\CommonLibrary')
from LoadCorrespondingSuffixFile import ZKM_FileNameProcessingClass
# �����ı�
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
# ���������
sys.path.append(File_RootDirectory)
from EditBSCommend import ZKM_EditBSCommend

class ZKM_EditBSWindow():
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
    def ZKM_Window(self):#����
        if cmds.window('AddintermediateWindow', ex=1,cc='CleanWindow()'):
            cmds.deleteUI('AddintermediateWindow')
        cmds.window('AddintermediateWindow', t="�༭BS")
        cmds.rowColumnLayout(nc=1, adj=5)
        pm.text(l='����BS����')
        cmds.rowColumnLayout(nc=8, adj=5)
        pm.text(l='Դ�Լ���ӳ�䣺')
        pm.optionMenu('EditBSWindow_LinkSoure')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Soure'), 0, '.txt')):
            pm.menuItem(label=file)
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile( r\'' + self.file_path + '\Soure\')')
        pm.text(l='Ŀ�꣺')
        pm.optionMenu('EditBSWindow_LinkTarget')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Target'), 0, '.txt')):
            pm.menuItem(label=file)
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(r\'' + self.file_path + '\Target\')')
        pm.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=2)
        pm.optionMenu('EditBSWindow_LinkBSName')
        BS = pm.ls(type='blendShape')
        if not BS:
            pm.menuItem(label='û�м�⵽BS�ڵ�')
        for bs in BS:
            pm.menuItem(label=bs)
        pm.button(l='����bs',bgc=(1,1,1),c='ZKM_EditBSCommend().LinkBS()')
        pm.setParent('..')
        pm.separator(style="in", height=1)
        pm.separator(style="out", height=1)
        pm.text(l='�Զ����bs�м�֡')
        cmds.rowColumnLayout(nc=2, adj=5)
        cmds.textFieldButtonGrp('Addintermediate_Soure',cw2=(150,50),bl='����Դ',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'Addintermediate_Soure\')')
        cmds.textFieldButtonGrp('Addintermediate_BSName', cw2=(150, 50), bl='����BS����',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'Addintermediate_BSName\')')
        cmds.textFieldButtonGrp('Addintermediate_Difference', cw2=(150, 50), bl='����',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'Addintermediate_Difference\')')
        cmds.button(l='��ʼ����', command='ZKM_EditBSCommend().AddBSIntermediateFrame()')
        pm.setParent('..')
        pm.separator(style="in", height=1)
        pm.separator(style="out", height=1)
        pm.text(l='bs�м���̬ת��Ϸ�淶')
        cmds.rowColumnLayout(nc=2, adj=5)
        cmds.textFieldButtonGrp('GameSpecifications_Soure', cw2=(150, 50), bl='����Դ',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'GameSpecifications_Soure\')')
        cmds.textFieldButtonGrp('GameSpecifications_BSName', cw2=(150, 50), bl='����BS����',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'GameSpecifications_BSName\')')
        pm.setParent('..')
        pm.button(l='�������ӵ�bsת��Ϸ�淶', command='ZKM_EditBSCommend().BSIntermediateFrameToGameSpecifications()')
        pm.separator(style="out", height=1)
        pm.separator(style="in", height=1)
        pm.text(l='�決������bs')
        cmds.rowColumnLayout(nc=2, adj=5)
        cmds.textFieldButtonGrp('BakeBs_Soure', cw2=(150, 50), bl='����Դ',bc='ZKM_AddintermediateWindow().ZKM_LoadText(\'textFieldButtonGrp\' , \'BakeBs_Soure\')')
        cmds.textFieldButtonGrp('BakeBs_BSName', cw2=(150, 50), bl='����BS����',bc='ZKM_AddintermediateWindow().ZKM_LoadText(\'textFieldButtonGrp\', \'BakeBs_BSName\')')
        pm.setParent('..')
        pm.button(l='�決������bs', command='ZKM_EditBSCommend().BakeBs()')

        pm.setParent('..')
        cmds.showWindow()

ShowWindow = ZKM_EditBSWindow()
if __name__ =='__main__':
    ShowWindow.ZKM_Window()

#ɾ����Ӱ������
