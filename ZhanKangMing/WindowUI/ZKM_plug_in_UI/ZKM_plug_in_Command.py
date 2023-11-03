#coding=gbk
import os
import sys
import pymel.core as pm
import webbrowser
class ZKM_plug_in_Class():
    def Open_RunPY_Window(self,Path,name,Command):
        sys.path.append(Path)
        #print (Path)
        #print 'python(\"import '+name+'\")'
        pm.mel.eval('python(\"import '+name+'\")')
        #print 'python(\"from ' + name + ' import *\")'
        pm.mel.eval('python(\"from '+name+' import *\")')
        pm.mel.eval('python(\"'+Command+'\")')
    def Install_Window(self,Path):
        import maya.app.general.executeDroppedPythonFile as myTempEDPF
        myTempEDPF.executeDroppedPythonFile(Path, "")
        del myTempEDPF
    def AutomaticallySwitchWallpapers(self):
        if pm.window('AutomaticallySwitchWallpapers_Window', ex=1):
            pm.deleteUI('AutomaticallySwitchWallpapers_Window')
        pm.window('AutomaticallySwitchWallpapers_Window', t='文档路径')
        pm.columnLayout()
        pm.button()
        pm.showWindow()
    def Open_Document(self):
        os.system("start explorer Z:\\1.Private folder\\Rig\\zhankangming\\ZhanKangMing\\ZhanKangMing_Documentation\\Documentation.docx")
    def Open_Document_set(self):
        if pm.window('plug_in_Open_Document_Window', ex=1):
            pm.deleteUI('plug_in_Open_Document_Window')
        pm.window('plug_in_Open_Document_Window', t='文档路径')
        pm.columnLayout()
        pm.button()
        pm.showWindow()
    def Help(self):
        if pm.window('plug_in_Help_Window', ex=1):
            pm.deleteUI('plug_in_Help_Window')
        pm.window('plug_in_Help_Window', t='帮助窗口')
        pm.columnLayout()
        pm.button()
        pm.showWindow()
    def Open_web(self):
        mod = int(pm.getModifiers())
        if mod == 4 :
            webbrowser.open('https://github.com/MengXingXiaoMing?tab=repositories')
        else:
            webbrowser.open('https://space.bilibili.com/173984578?spm_id_from=333.1007.0.0')
