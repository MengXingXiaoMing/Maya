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

# �ļ�·��
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# ��·��
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# �汾��
maya_version = cmds.about(version=True)
# ��·��
library_path = root_path + '\\' + maya_version

# ����ӵ�ϵͳ·��
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
        # ��ʵ���ϣ���Ӧ��ֱ��ʹ��ԭʼ��Unicode�ַ���
        self.setWindowTitle((u'���Ǻ��ӷ������汾�����װ(Maya' + self.maya_version + u')'))

        # �ļ�·��
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # ��·��
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
        # �汾��
        self.maya_version = cmds.about(version=True)
        self.user_path = ''

        self.others_library = OthersLibrary()
        self.all_plug_in_path = self.get_plug_in_path()
        self.create_widgets()
        self.create_layouts()
        self.create_connect()


    def create_widgets(self):
        # ��һ��
        self.text_1 = QtWidgets.QLabel('���Ʋ����ѡ��·�������û���Զ���װ�ɹ��򵽵�ǰ�ļ����²鿴ZKM_plug_in.py�ļ��Ƿ���£�û���µ�� ���µ�ǰ�ļ��в���ļ�,ZKM_plug_in.py�ļ����������ֶ����Ƶ�����������￪����')
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(self.all_plug_in_path)
        self.button_1 = QtWidgets.QPushButton('�ļ����Ƶ�ѡ��·��')
        self.button_2 = QtWidgets.QPushButton('���µ�ǰ�ļ��в���ļ�')

        self.text_2 = QtWidgets.QLabel('�û��ļ���·����')
        self.line_edit_1 = QtWidgets.QLineEdit(self.root_path+'\\user')
        self.text_3 = QtWidgets.QLabel('�ļ������ƣ�')
        self.line_edit_2 = QtWidgets.QLineEdit('self')
        self.line_edit_2.setFixedWidth(100)
        self.button_3 = QtWidgets.QPushButton()
        self.button_3.setMinimumSize(QtCore.QSize(30, 10))
        self.button_3.setIcon(QtGui.QIcon(':/fileOpen.png'))
        self.button_4 = QtWidgets.QPushButton('�����û��ļ��У�����޷���������user�ļ����µ�self�ļ��е����Լ���Ŀ¼��'
                                              'Ȼ���·���ĵ����Լ����Ƶ�·�����ļ�������������ƵĻ����øģ�')

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

        # �ö�
        self.main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(self.install_plugin)
        self.button_2.clicked.connect(self.update_current_folder_files)
        self.button_3.clicked.connect(self.open_file_folder)
        self.button_4.clicked.connect(self.create_user_folder)

    def get_plug_in_path(self):
        # ��ȡ�Ѽ��صĲ���б�
        loaded_plugins = cmds.pluginInfo(query=True, listPlugins=True)
        # ����һ���ֵ����洢������ƺͿ��ܵ�·��
        all_plugin_paths = []

        # �����Ѽ��صĲ�����������ҵ����ǵ�·������������չ����
        for plugin in loaded_plugins:
            plugin_paths = cmds.pluginInfo(plugin, query=True, p=True)
            # ����·��
            plugin_path = plugin_paths.split('/')
            new_path = ''
            for i in range(0, len(plugin_path) - 1):
                new_path = new_path + plugin_path[i] + '/'
            new_path = [new_path]

            if new_path[0] not in all_plugin_paths:
                # ������ڣ�����ӵ��б���
                all_plugin_paths.append(new_path[0])
        return all_plugin_paths


    # ���µ�ǰ�ļ����ļ�
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
        cmds.warning('����Ѹ���')
        return ls_path

    # �Զ���װ���
    def install_plugin(self):
        plug_in_path = self.comboBox_1.currentText()
        # print(plug_in_path)
        file_path = self.update_current_folder_files()
        # print(file_path)

        # �����������ļ�·��
        full_file_path = os.path.join(self.user_path, 'ZKM_plug_in_global_variable.py')

        # ʹ��open���������ļ�������ļ���������ᱻ����
        # 'w' ģʽ��ʾд�루����ļ��Ѵ�����ᱻ���ǣ�
        with open(full_file_path, 'w') as new_file:
            # ��ѡ�����ļ���д��һЩ��ʼPython����
            new_file.write('ZKM_plug_in_user_file_path = r\''+self.user_path+'\')\n')

        shutil.copy2(file_path + 'ZKM_plug_in.py', plug_in_path +'ZKM_plug_in.py')
        cmds.pluginInfo(plug_in_path +'ZKM_plug_in.py', edit=1, autoload=True)
        cmds.loadPlugin('ZKM_plug_in')
        cmds.warning('����Ѱ�װ')

    # ���ļ���ѡ���ļ��к��·��������д����
    def open_file_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", QDir.homePath())
        if folder_path:
            self.line_edit_1.setText(folder_path)

    # �����û��ļ��в������ļ���·��
    def create_user_folder(self):
        # Ŀ��·��
        target_path = self.line_edit_1.text()
        name = self.line_edit_2.text()
        self.user_path = target_path+'\\'+name
        if target_path:
            if (self.root_path+r'\user\self') == self.user_path:
                cmds.warning('��ǰĿ¼Ϊ����Ա�ļ��У������д�����')
                self.main_layout.addLayout(self.v_Box_layout_2)
            else:
                try:
                    shutil.copytree((self.root_path + r'\user\self'), self.user_path)
                    cmds.warning('�û��ļ����Ѵ��������ƻ�������')
                    self.main_layout.addLayout(self.v_Box_layout_2)
                except:
                    cmds.warning('���Ŀ¼�Ƿ����')

        else:
            cmds.warning('���ȼ���Ŀ��·��')

window = Window()
if __name__ == '__main__':
    window.show()
window.show()
