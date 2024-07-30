# -*- coding: utf-8 -*-
import maya.cmds as cmds
# 获取文件路径
import os
import sys
import inspect
import importlib

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version

# 库添加到系统路径
sys.path.append(library_path)
import common
from common import *

import maya_common
from maya_common import *

import ui_edit
from ui_edit import *

import weight
from weight import *

import others_library
from others_library import *

import curve
from curve import *

import controller
from controller import *

importlib.reload(common)
importlib.reload(maya_common)
importlib.reload(ui_edit)
importlib.reload(weight)
importlib.reload(others_library)
importlib.reload(curve)
importlib.reload(controller)

class Command():
    def __init__(self):
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + self.maya_version

        self.common = Common()
        self.maya_common = MayaCommon()
        self.ui_edit = UiEdit()
        self.weight = Weight()
        self.others_library = OthersLibrary()
        self.curve = CreateAndEditCurve()
        self.controller = CurveControllerEdit()


    def curve_list(self):
        # 获取指定目录下的所有指定后缀的文件名
        curve_list = []
        library_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        library_path = library_path + '/' + self.maya_version + '/curve_library'
        list = os.listdir(library_path)  # 返回文件名
        for l in list:
            if os.path.splitext(l)[1] == '.txt':
                curve_list.append(l.split('.')[0])
        return(curve_list)

    # 拖动滑块自动修改颜色面板
    def drag_slider_automatically_modify_color_panel(self,value,button):
        text = []
        if value ==0:
            text = (120,120,120)
        if value ==1:
            text = (0,0,0)
        if value ==2:
            text = (64,64,64)
        if value ==3:
            text = (153,153,153)
        if value ==4:
            text = (155,0,40)
        if value ==5:
            text = (0,4,96)
        if value ==6:
            text = (0,0,255)
        if value ==7:
            text = (0,70,25)
        if value ==8:
            text = (38,0,67)
        if value ==9:
            text = (200,0,200)
        if value ==10:
            text = (136,72,51)
        if value ==11:
            text = (63,35,31)
        if value ==12:
            text = (151,39,0)
        if value ==13:
            text = (255,0,0)
        if value ==14:
            text = (0,255,0)
        if value ==15:
            text = (0,65,153)
        if value ==16:
            text = (255,255,255)
        if value ==17:
            text = (255,255,0.000)
        if value ==18:
            text = (100,220,255)
        if value ==19:
            text = (67,255,163)
        if value ==20:
            text = (255,176,176)
        if value ==21:
            text = (255,189,131)
        if value ==22:
            text = (255,255,140)
        if value ==23:
            text = (0,153,84)
        if value ==24:
            text = (161,106,48)
        if value ==25:
            text = (158,161,48)
        if value ==26:
            text = (104,161,48)
        if value ==27:
            text = (48,161,93)
        if value ==28:
            text = (48,161,161)
        if value ==29:
            text = (48,103,161)
        if value ==30:
            text = (111,48,161)
        if value ==31:
            text = (160,48,106)
        button.setStyleSheet('background:rgb('+str(text[0])+','+str(text[1])+','+str(text[2])+')')
