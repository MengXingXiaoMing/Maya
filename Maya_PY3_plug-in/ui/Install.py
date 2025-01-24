#coding=gbk
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
import os
import sys
import inspect
import importlib
import maya.mel as mel
import shutil

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version

# 库添加到系统路径
sys.path.append(library_path)

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
        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        # 但实际上，你应该直接使用原始的Unicode字符串
        self.setWindowTitle((u'梦星盒子服务器版本插件安装(Maya' + self.maya_version + u')'))

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
        # 版本号
        self.maya_version = cmds.about(version=True)
        self.user_path = ''

        self.others_library = OthersLibrary()
        self.all_plug_in_path = self.get_plug_in_path()
        self.create_widgets()
        self.create_layouts()
        self.create_connect()


    def create_widgets(self):
        # 第一行
        self.text_1 = QtWidgets.QLabel('复制插件到选择路径，如果没有自动安装成功则到当前文件夹下查看ZKM_plug_in.py文件是否更新，没更新点击 更新当前文件夹插件文件,ZKM_plug_in.py文件更新了则手动复制到插件管理器里开启。')
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(self.all_plug_in_path)
        self.button_1 = QtWidgets.QPushButton('文件复制到选择路径')
        self.button_2 = QtWidgets.QPushButton('更新当前文件夹插件文件')

        self.text_2 = QtWidgets.QLabel('用户文件夹路径：')
        self.line_edit_1 = QtWidgets.QLineEdit(self.root_path+'\\user')
        self.text_3 = QtWidgets.QLabel('文件夹名称：')
        self.line_edit_2 = QtWidgets.QLineEdit('self')
        self.line_edit_2.setFixedWidth(100)
        self.button_3 = QtWidgets.QPushButton()
        self.button_3.setMinimumSize(QtCore.QSize(30, 10))
        self.button_3.setIcon(QtGui.QIcon(':/fileOpen.png'))
        self.button_4 = QtWidgets.QPushButton('创建用户文件夹（如果无法创建则复制user文件夹下的self文件夹到你自己的目录，'
                                              '然后把路径改到你自己复制的路径，文件夹名称你仅复制的话不用改）')

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)

        v_Box_layout_1 = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(v_Box_layout_1)
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_1.addLayout(h_Box_layout_1)
        h_Box_layout_1.addWidget(self.text_2)
        h_Box_layout_1.addWidget(self.line_edit_1)
        h_Box_layout_1.addWidget(self.text_3)
        h_Box_layout_1.addWidget(self.line_edit_2)
        h_Box_layout_1.addWidget(self.button_3)
        v_Box_layout_1.addWidget(self.button_4)

        self.v_Box_layout_2 = QtWidgets.QVBoxLayout(self)
        #
        self.v_Box_layout_2.addWidget(self.text_1)
        self.v_Box_layout_2.addWidget(self.comboBox_1)
        self.v_Box_layout_2.addWidget(self.button_1)
        self.v_Box_layout_2.addWidget(self.button_2)

        # 置顶
        self.main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(self.install_plugin)
        self.button_2.clicked.connect(self.update_current_folder_files)
        self.button_3.clicked.connect(self.open_file_folder)
        self.button_4.clicked.connect(self.create_user_folder)

    def get_plug_in_path(self):
        # 获取已加载的插件列表
        loaded_plugins = cmds.pluginInfo(query=True, listPlugins=True)
        # 创建一个字典来存储插件名称和可能的路径
        all_plugin_paths = []

        # 遍历已加载的插件，并尝试找到它们的路径（不考虑扩展名）
        for plugin in loaded_plugins:
            plugin_paths = cmds.pluginInfo(plugin, query=True, p=True)
            # 重组路径
            plugin_path = plugin_paths.split('/')
            new_path = ''
            for i in range(0, len(plugin_path) - 1):
                new_path = new_path + plugin_path[i] + '/'
            new_path = [new_path]

            if new_path[0] not in all_plugin_paths:
                # 如果不在，则添加到列表中
                all_plugin_paths.append(new_path[0])
        return all_plugin_paths


    # 更新当前文件夹文件
    def update_current_folder_files(self):
        new_file_path = self.file_path.split('/')
        ls_path = ''
        file_name = 'old_install.py'
        for i in range(0, len(new_file_path)):
            ls_path = ls_path + new_file_path[i] + '\\'
        # self.others_library.load_source(file_name, (ls_path + file_name))
        # cmds.python('copy_ZKM_plug_in(\''+self.user_path+'\')')
        sys.path.append(self.file_path)
        cmds.python('import old_install')
        cmds.python('from old_install import *')
        # print('CopyZKMPlugInClass().copy_ZKM_plug_in(r\''+self.user_path+'\')')
        cmds.python('CopyZKMPlugInClass().copy_ZKM_plug_in(r\''+self.user_path+'\')')
        cmds.warning('插件已更新')
        return ls_path

    # 自动安装插件
    def install_plugin(self):
        plug_in_path = self.comboBox_1.currentText()
        # print(plug_in_path)
        file_path = self.update_current_folder_files()
        # print(file_path)

        # 构建完整的文件路径
        full_file_path = os.path.join(self.user_path, 'ZKM_plug_in_global_variable.py')

        # 使用open函数创建文件，如果文件不存在则会被创建
        # 'w' 模式表示写入（如果文件已存在则会被覆盖）
        with open(full_file_path, 'w') as new_file:
            # 可选：向文件中写入一些初始Python代码
            new_file.write('ZKM_plug_in_user_file_path = r\''+self.user_path+'\')\n')

        shutil.copy2(file_path + 'ZKM_plug_in.py', plug_in_path +'ZKM_plug_in.py')
        cmds.pluginInfo(plug_in_path +'ZKM_plug_in.py', edit=1, autoload=True)
        cmds.loadPlugin('ZKM_plug_in')
        cmds.warning('插件已安装')

    # 打开文件夹选择文件夹后把路径给到填写区域
    def open_file_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", QDir.homePath())
        if folder_path:
            self.line_edit_1.setText(folder_path)

    # 创建用户文件夹并复制文件到路径
    def create_user_folder(self):
        # 目标路径
        target_path = self.line_edit_1.text()
        name = self.line_edit_2.text()
        self.user_path = target_path+'\\'+name
        if target_path:
            if (self.root_path+r'\user\self') == self.user_path:
                cmds.warning('当前目录为管理员文件夹，不进行创建。')
                self.main_layout.addLayout(self.v_Box_layout_2)
            else:
                try:
                    shutil.copytree((self.root_path + r'\user\self'), self.user_path)
                    cmds.warning('用户文件夹已创建并复制基本数据')
                    self.main_layout.addLayout(self.v_Box_layout_2)
                except:
                    cmds.warning('检查目录是否存在')

        else:
            cmds.warning('请先加载目标路径')

window = Window()
if __name__ == '__main__':
    window.show()
window.show()
