#coding=gbk
import maya.api.OpenMaya as om
import sys
import maya.cmds as cmds
import inspect
FilePath = 'Z:\\1.Private folder\\Rig\\zhankangming\\ZhanKangMing\\Maya_PY3_plug-in_2025\\ui'
sys.path.append(FilePath + '\\ZKM_plug_in_UI')
import ZKM_plug_in_Command
from ZKM_plug_in_Command import *
ZKM_plug_in_user_file_path = r'Z:\1.Private folder\Rig\zhankangming\ZhanKangMing\Maya_PY3_plug-in_2025\user\zkm2025'

# 声明使用新版API（必需！）
def maya_useNewAPI():
    pass

def initializePlugin(plugin):
    try:
        plugin_fn = om.MFnPlugin(
            plugin,
            vendor="ZhanKangMing",  # 开发者名称
            version="1.0.0"  # 版本号
        )
        cmds.python('import ZKM_plug_in_Command')
        cmds.python('from ZKM_plug_in_Command import *')
        cmds.python('ZKM_plug_in_Class().LoadPresetPlugIns(r\'' + ZKM_plug_in_user_file_path + '\')')

    except Exception as e:
        om.MGlobal.displayError(f"初始化失败: {str(e)}")

def uninitializePlugin(plugin):
    # plugin_fn = om.MFnPlugin(plugin)
    try:
        cmds.deleteUI('MayaWindow_menu_Process_Button')
    except:
        pass
    try:
        cmds.deleteUI('MayaWindow_menu_Process_formLayout1_AddButton')
    except:
        pass