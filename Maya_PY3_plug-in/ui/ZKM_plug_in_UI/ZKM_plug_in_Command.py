#coding=utf-8
import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import importlib
import webbrowser
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-3]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version
# 库添加到系统路径
sys.path.append(library_path)
import others_library
from others_library import *

class ZKM_plug_in_Class():
    def __init__(self):
        self.others_library = OthersLibrary()
        pass
    def open_run_py_window(self,Path,name,Command):
        sys.path.append(Path)
        mel.eval('python(\"import '+name+'\")')
        mel.eval('python(\"importlib.reload( ' + name + ')\")')
        mel.eval('python(\"from '+name+' import *\")')
        mel.eval('python(\"'+Command+'\")')
    def Install_Window(self,Path):
        import maya.app.general.executeDroppedPythonFile as myTempEDPF
        myTempEDPF.executeDroppedPythonFile(Path, "")
        del myTempEDPF
    def AutomaticallySwitchWallpapers(self):
        if cmds.window('AutomaticallySwitchWallpapers_Window', ex=1):
            cmds.deleteUI('AutomaticallySwitchWallpapers_Window')
        cmds.window('AutomaticallySwitchWallpapers_Window', t='文档路径')
        cmds.columnLayout()
        cmds.button()
        cmds.showWindow()
    def open_document(self):
        print('暂时删除，我是个懒狗，自产自销，暂时不提供文档。')
        print('其实后面文档压根没写，要写的话都得补，直接开摆了。')
        #os.system("start explorer Z:\\1.Private folder\\Rig\\zhankangming\\ZhanKangMing\\ZhanKangMing_Documentation\\Documentation.docx")
    def Open_Document_set(self):
        if cmds.window('plug_in_Open_Document_Window', ex=1):
            cmds.deleteUI('plug_in_Open_Document_Window')
        cmds.window('plug_in_Open_Document_Window', t='文档路径')
        cmds.columnLayout()
        cmds.button()
        cmds.showWindow()
    def help(self):
        if cmds.window('plug_in_Help_Window', ex=1):
            cmds.deleteUI('plug_in_Help_Window')
        cmds.window('plug_in_Help_Window', t='帮助窗口')
        cmds.columnLayout()
        cmds.picture(image=file_path+'\\help.png')
        cmds.showWindow()
    def open_web(self):
        mod = int(cmds.getModifiers())
        if mod == 4 :
            self.others_library.open_web(0)
        else:
            self.others_library.open_web(1)
