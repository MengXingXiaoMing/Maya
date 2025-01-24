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
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))

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

    def LoadPresetPlugIns(self,ZKM_plug_in_user_file_path):
        # MAYA版本
        maya_version = cmds.about(version=True)
        FilePathBackslash = self.root_path.split('\\')
        Text = ''
        for F in FilePathBackslash:
            Text = Text + F + '/'
        try:
            cmds.deleteUI('MayaWindow_menu_Process_Button')
        except:
            pass
        try:
            cmds.deleteUI('MayaWindow_menu_Process_formLayout1_AddButton')
        except:
            pass
        # aa= cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', q=1,ann=1)
        # print(aa)
        cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', parent='flowLayout1',i1=self.root_path+'\\ZKM_plug_in_UI\\ButtonNomalUI.png',hi=self.root_path+'\\ZKM_plug_in_UI\\ButtonMoveInUI.png',
                          c='ZKM_plug_in_Class().open_web()',ann=ZKM_plug_in_user_file_path)
        showMyMenuCtrl = cmds.menu('MayaWindow_menu_Process_Button', tearOff=True,parent='MayaWindow', label='梦星盒子')
        cmds.menuItem(label='文件清理',
                    c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\clear_files\',\'clear_files_window\',\'window.show()\')')
        cmds.menuItem(label='权重处理',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\weight_processing\',\'weight_processing_window\',\'window.show()\')')
        cmds.menuItem(label='控制器处理',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\controller_processing\',\'controller_processing_window\',\'window.show()\')')
        # cmds.menuItem(subMenu=True, label='控制器处理')
        # cmds.menuItem(label='《—主窗口ヾ(^▽^*)))',
        # 			c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\qt_ui\\controller_processing\',\'controller_processing_window\',\'window.show()\')')
        # cmds.menuItem(label='属性可视化(未开发)',c='')
        # cmds.setParent('..', menu=True)
        cmds.menuItem(label='BS编辑',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\bs_edit\',\'bs_edit_window\',\'window.show()\')')
        cmds.menuItem(label='新轮胎表达式',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\tire_baking_expression\',\'tire_baking_expression_window\',\'window.show()\')')
        cmds.menuItem(label='履带',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\track\',\'track_window\',\'window.show()\')')
        cmds.menuItem(label='曲面绳子',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\curved_rope\',\'curved_rope_window\',\'window.show()\')')
        cmds.menuItem(label='自定义命令',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\custom_commands\',\'custom_commands_window\',\'window.show()\')')
        cmds.menuItem(label='驱动器',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\disk_drive\',\'disk_drive_window\',\'window.show()\')')
        cmds.menuItem(label='自动添加中间帧',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\add_Intermediate\',\'add_intermediate_window\',\'window.show()\')')
        cmds.menuItem(label='bs加驱动',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\bs_convert_drver\',\'bs_convert_drver_window\',\'window.show()\')')
        cmds.menuItem(label='手动加驱动裙子',
                      c='ZKM_plug_in_Class().open_run_py_window(r\'' + self.root_path + '\\qt_ui\\skirt_drver\',\'skirt_drver_window\',\'window.show()\')')
        '''cmds.menuItem(subMenu=True, label='预置模板')
        cmds.menuItem(label='《—主窗口ヾ(^▽^*)))',
                    c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\',\'PresetTemplateWindow\',\'ShowWindow.ZKM_Window()\')')
        cmds.menuItem(label='不同拓补传递BS',
                    c='ZKM_plug_in_Class().open_run_py_window(r\'' + FilePath + '\\Maya_WindowUI\\PresetTemplateFile\\DifferentTopologyTransferBS\',\'DifferentTopologyTransfer_BS\',\'ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()\')')
        cmds.menuItem(label='SSDR', c='print (\'未添加\')')
        cmds.setParent('..', menu=True)'''
        cmds.setParent('..', menu=True)
        cmds.menuItem(divider=True, l='')
        # cmds.menuItem('ZKM_plug_in_Automatically_switch_wallpapers',checkBox=True, label="自动切换壁纸")
        # cmds.menuItem(optionBox=True,c='ZKM_plug_in_Class().help()')
        # cmds.menuItem(divider=True, l='功能未完善╮(╯▽╰)╭')
        cmds.menuItem(label="打开文档(我是懒狗，压根没写哈哈哈)", i='fileOpen.png', c='ZKM_plug_in_Class().open_document()')
        cmds.menuItem(optionBox=True)
        cmds.menuItem(label="帮助(目前为空)", i='help.png', c='ZKM_plug_in_Class().help()')
        cmds.menuItem(label="访问UP主页(按住ctrl可进入GitHub))", i='implicitSphere.svg', c='ZKM_plug_in_Class().open_web()')
