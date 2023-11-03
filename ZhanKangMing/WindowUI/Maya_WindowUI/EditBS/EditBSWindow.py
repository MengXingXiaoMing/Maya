#coding=gbk
import pymel.core as pm
import os
import sys
import inspect

#根目录
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 加载对应后缀文件
sys.path.append(ZKM_RootDirectory+'\\Common\\CommonLibrary')
from LoadCorrespondingSuffixFile import ZKM_FileNameProcessingClass
# 加载文本
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
# 加载命令部分
sys.path.append(File_RootDirectory)
from EditBSCommend import ZKM_EditBSCommend

class ZKM_EditBSWindow():
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        # print(file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
        cur_dirB = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathTop = os.path.join(cur_dirB)  # 获取总位置
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
        self.file_pathTop = file_pathTop
    def ZKM_Window(self):#窗口
        if cmds.window('AddintermediateWindow', ex=1,cc='CleanWindow()'):
            cmds.deleteUI('AddintermediateWindow')
        cmds.window('AddintermediateWindow', t="编辑BS")
        cmds.rowColumnLayout(nc=1, adj=5)
        pm.text(l='链接BS方案')
        cmds.rowColumnLayout(nc=8, adj=5)
        pm.text(l='源以及重映射：')
        pm.optionMenu('EditBSWindow_LinkSoure')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Soure'), 0, '.txt')):
            pm.menuItem(label=file)
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile( r\'' + self.file_path + '\Soure\')')
        pm.text(l='目标：')
        pm.optionMenu('EditBSWindow_LinkTarget')
        for file in (ZKM_FileNameProcessingClass().ZKM_LoadFileNameOfTheCorrespondingSuffix((self.file_path + '\Target'), 0, '.txt')):
            pm.menuItem(label=file)
        cmds.iconTextButton(style='iconOnly', image1='fileNew.png',command='os.startfile(r\'' + self.file_path + '\Target\')')
        pm.setParent('..')
        cmds.rowColumnLayout(nc=2, adj=2)
        pm.optionMenu('EditBSWindow_LinkBSName')
        BS = pm.ls(type='blendShape')
        if not BS:
            pm.menuItem(label='没有检测到BS节点')
        for bs in BS:
            pm.menuItem(label=bs)
        pm.button(l='关联bs',bgc=(1,1,1),c='ZKM_EditBSCommend().LinkBS()')
        pm.setParent('..')
        pm.separator(style="in", height=1)
        pm.separator(style="out", height=1)
        pm.text(l='自动添加bs中间帧')
        cmds.rowColumnLayout(nc=2, adj=5)
        cmds.textFieldButtonGrp('Addintermediate_Soure',cw2=(150,50),bl='加载源',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'Addintermediate_Soure\')')
        cmds.textFieldButtonGrp('Addintermediate_BSName', cw2=(150, 50), bl='加载BS名称',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'Addintermediate_BSName\')')
        cmds.textFieldButtonGrp('Addintermediate_Difference', cw2=(150, 50), bl='区别',bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'Addintermediate_Difference\')')
        cmds.button(l='开始生成', command='ZKM_EditBSCommend().AddBSIntermediateFrame()')
        pm.setParent('..')
        pm.separator(style="in", height=1)
        pm.separator(style="out", height=1)
        pm.text(l='bs中间形态转游戏规范')
        cmds.rowColumnLayout(nc=2, adj=5)
        cmds.textFieldButtonGrp('GameSpecifications_Soure', cw2=(150, 50), bl='加载源',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'GameSpecifications_Soure\')')
        cmds.textFieldButtonGrp('GameSpecifications_BSName', cw2=(150, 50), bl='加载BS名称',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'GameSpecifications_BSName\')')
        pm.setParent('..')
        pm.button(l='给有链接的bs转游戏规范', command='ZKM_EditBSCommend().BSIntermediateFrameToGameSpecifications()')
        pm.separator(style="out", height=1)
        pm.separator(style="in", height=1)
        pm.text(l='烘焙出所有bs')
        cmds.rowColumnLayout(nc=2, adj=5)
        cmds.textFieldButtonGrp('BakeBs_Soure', cw2=(150, 50), bl='加载源',bc='ZKM_AddintermediateWindow().ZKM_LoadText(\'textFieldButtonGrp\' , \'BakeBs_Soure\')')
        cmds.textFieldButtonGrp('BakeBs_BSName', cw2=(150, 50), bl='加载BS名称',bc='ZKM_AddintermediateWindow().ZKM_LoadText(\'textFieldButtonGrp\', \'BakeBs_BSName\')')
        pm.setParent('..')
        pm.button(l='烘焙出所有bs', command='ZKM_EditBSCommend().BakeBs()')

        pm.setParent('..')
        cmds.showWindow()

ShowWindow = ZKM_EditBSWindow()
if __name__ =='__main__':
    ShowWindow.ZKM_Window()

#删除无影响驱动
