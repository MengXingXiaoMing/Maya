# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    maya_version_int = maya_version_int - i
    # 库路径
    maya_version = str(maya_version_int)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)

import others_library
importlib.reload(others_library)
from others_library import *

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        self.use_path = cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', q=1, ann=1)
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('帮助(Maya' + self.maya_version + ')')

        self.others_library = OthersLibrary()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        # 库路径
        self.library_path = root_path + '\\' + maya_version


        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    def create_widgets(self):
        # 第一行
        self.button_1 = QtWidgets.QPushButton('访问 up 主页')
        self.button_2 = QtWidgets.QPushButton('访问 up Github')
        self.button_3 = QtWidgets.QPushButton('访问此插件网盘地址，密码zkm1')
        self.button_4 = QtWidgets.QPushButton('打开当前用户文件夹')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        main_layout.addWidget(self.button_1)
        main_layout.addWidget(self.button_2)
        main_layout.addWidget(self.button_3)
        main_layout.addWidget(self.button_4)

        main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(lambda: self.others_library.open_web(1))
        self.button_2.clicked.connect(lambda: self.others_library.open_web(0))
        self.button_3.clicked.connect(lambda: self.others_library.open_web(2))
        self.button_4.clicked.connect(self.open_file_dir)

    #打开文件夹
    def open_file_dir(self):
        os.startfile(os.path.expanduser(self.use_path))

window = Window()
if __name__ == '__main__':
    window.show()

#删除无影响驱动
