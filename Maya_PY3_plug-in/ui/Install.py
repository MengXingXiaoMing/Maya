#coding=gbk
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    # 库路径
    maya_version = str(maya_version_int)
    library_path = root_path + '\\' + maya_version
    maya_version_int = maya_version_int - 1
    print('library_path:',library_path)
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        print(library_path)
        print("文件夹存在")
        break

import general_settings
from general_settings import *
importlib.reload(general_settings)


import others_library
importlib.reload(others_library)
from others_library import *


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        cmds.warning("如果有弹窗，请在弹出的 UAC 窗口中点击 '是' 以授权管理员权限。")
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
        maya_version_int = int(self.maya_version)
        for i in range(30):
            test_version = maya_version_int - i
            # 库路径
            self.maya_version = str(test_version)
            self.library_path = self.root_path + '\\' + self.maya_version
            # 方法2：直接判断是否是目录（更简洁）
            if os.path.isdir(self.library_path):
                # 库添加到系统路径
                sys.path.append(self.library_path)
                maya_version_int = test_version
                # print("文件夹存在")
                break

        # 库路径
        # self.library_path = self.root_path + '\\' + self.maya_version
        print('库路径：',self.library_path)
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
        self.button_1 = QtWidgets.QPushButton('文件复制到选择路径')
        self.button_2 = QtWidgets.QPushButton('更新当前文件夹插件文件')

        self.text_2 = QtWidgets.QLabel('用户文件夹路径：')
        self.line_edit_1 = QtWidgets.QLineEdit(self.root_path+'\\user')
        self.text_3 = QtWidgets.QLabel('文件夹名称：')
        self.line_edit_2 = QtWidgets.QLineEdit('self')
        # self.line_edit_2.setFixedWidth(100)
        self.button_3 = QtWidgets.QPushButton()
        # self.button_3.setMinimumSize(QtCore.QSize(30, 10))
        self.button_3.setIcon(QtGui.QIcon(':/fileOpen.png'))
        self.button_4 = QtWidgets.QPushButton('安装')

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

        # self.v_Box_layout_2 = QtWidgets.QVBoxLayout(self)
        #
        # self.v_Box_layout_2.addWidget(self.text_1)
        # self.v_Box_layout_2.addWidget(self.comboBox_1)
        # self.v_Box_layout_2.addWidget(self.button_1)
        # self.v_Box_layout_2.addWidget(self.button_2)

        # 置顶
        self.main_layout.addStretch(1)
    def create_connect(self):
        self.button_1.clicked.connect(self.install_plugin)
        self.button_2.clicked.connect(self.update_current_folder_files)
        self.button_3.clicked.connect(self.open_file_folder)
        self.button_4.clicked.connect(self.install_new_version)

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
    def update_current_folder_files_old(self):
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
        file_path = self.update_current_folder_files(self.user_path)
        # print(file_path)

        # 构建完整的文件路径
        full_file_path = os.path.join(self.user_path, 'ZKM_plug_in_global_variable.py')

        # 使用open函数创建文件，如果文件不存在则会被创建
        # 'w' 模式表示写入（如果文件已存在则会被覆盖）
        with open(full_file_path, 'w') as new_file:
            # 可选：向文件中写入一些初始Python代码
            new_file.write('ZKM_plug_in_user_file_path = r\''+self.user_path+'\')\n')

        # # 示例用法
        # source = file_path + 'ZKM_plug_in.py'
        # target = plug_in_path +'ZKM_plug_in.py'
        # # 构建 PowerShell 复制命令（兼容路径空格）
        # copy_cmd = f'Copy-Item -Path "{source}" -Destination "{target}" -Force -ErrorAction Stop'
        #
        # # 构建提权命令（以管理员运行 PowerShell）
        # powershell_cmd = f'Start-Process powershell -ArgumentList "-Command {copy_cmd}" -Verb RunAs'
        #
        # try:
        #     # 执行提权复制
        #     subprocess.run(powershell_cmd, shell=True, check=True)
        #     cmds.warning("文件复制成功！请检查插件目录。")
        # except subprocess.CalledProcessError as e:
        #     cmds.error(f"复制失败: 请确保在 UAC 弹窗中点击 '是' 以授权管理员权限。错误代码: {e.returncode}")

        shutil.copy2(file_path + 'ZKM_plug_in.py', plug_in_path +'ZKM_plug_in.py')
        # shutil.copy2(r'D:\scenes\aaa.txt',r'D:\scenes\ddd.txt')

        # 替换反斜杠为正斜杠
        # path_unix = plug_in_path.replace("/", "\\")
        # print(path_unix[:-1])
        # os.environ["MAYA_PLUG_IN_PATH"] = f"{os.environ.get('MAYA_PLUG_IN_PATH', '')}:{path_unix[:-1]}".replace("\\", "/")
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
                # self.main_layout.addLayout(self.v_Box_layout_2)
            elif os.path.exists(self.user_path):
                cmds.warning('当前目录存在，不进行创建。')
            else:
                # try:
                shutil.copytree((self.root_path + r'\user\self'), self.user_path)
                cmds.warning('用户文件夹已创建并复制基本数据')
                # self.main_layout.addLayout(self.v_Box_layout_2)

                # except:
                #     print((self.root_path + r'\user\self'))
                #     print(self.user_path)
                #     cmds.warning('检查目录是否存在')
            path = self.user_path+'\\'
            # 替换反斜杠为正斜杠
            path_unix = path.replace("\\", "/")
            # print(path_unix)
            # self.comboBox_1.addItems([path_unix])
            self.comboBox_1.addItems(self.all_plug_in_path)
        else:
            cmds.warning('请先加载目标路径')

    # 获取maya mod 文件夹并写入mod
    def get_maya_mod_path(self,user_path):
        path = os.environ['MAYA_MODULE_PATH']
        print(path)
        # print(path)
        path = path.split(';')[-1]
        #####################################
        mat_docs_path = os.getenv('MAYA_APP_DIR')
        maya_version = cmds.about(version=True)
        maya_version_path = os.path.join(mat_docs_path, maya_version)
        maya_docs_path_modules = os.path.join(maya_version_path, 'modules')
        file_path = os.path.join(maya_docs_path_modules, 'ZKM_plug_in_mod.mod')
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        # print(path)
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        path = maya_docs_path_modules
        print(path)
        ####################################
        # 构建完整的文件路径
        full_file_path = path +'/ZKM_plug_in_mod.mod'
        full_file_path = full_file_path.replace("/", "\\")
        # 使用open函数创建文件，如果文件不存在则会被创建
        # 'w' 模式表示写入（如果文件已存在则会被覆盖）
        text = ('+ ZKM_plug_in_mod 1.0 ' + user_path +'\n'
                'MAYA_PLUG_IN_PATH +:= \n'
                'MAYA_SCRIPT_PATH +:= ./mel_scripts\n'
                'PYTHONPATH +:= ./python_libs\n')
        with open(full_file_path, 'w') as new_file:
            # 可选：向文件中写入一些初始Python代码
            new_file.write(text)
        #
        # path = os.environ['MAYA_MODULE_PATH']
        # print(path)
        # # print(path)
        # path = path.split(';')[-1]
        # 构建完整的文件路径
        full_file_path = path + '/ZKM_plug_in_library_mod.mod'
        full_file_path = full_file_path.replace("/", "\\")
        # 使用open函数创建文件，如果文件不存在则会被创建
        # 'w' 模式表示写入（如果文件已存在则会被覆盖）
        print('self.library_path:',self.library_path)
        text = ('+ ZKM_plug_in_library_mod 1.0 ' + self.library_path + '\\node' + '\n'
               'MAYA_PLUG_IN_PATH +:= \n'
               'MAYA_SCRIPT_PATH +:= ./mel_scripts\n'
               'PYTHONPATH +:= ./python_libs\n')
        with open(full_file_path, 'w') as new_file:
            # 可选：向文件中写入一些初始Python代码
            new_file.write(text)

    # 写入新文件到用户文件夹
    def update_current_folder_files(self, user_path):
        cur_dirB = ('\\' + '\\').join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[
                                      :-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        Soure = self.file_path + '\\ZKM_plug_in_UI\\ZKM_plug_in.py'
        Target = user_path + '\\ZKM_plug_in.py'  # 替换后的.txt
        load = []  # 存储
        S = open(Soure, 'r', encoding='gbk')
        if user_path == '':
            cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2])
            user_path = cur_dirA + '/uesr/self'
        # print('user_path:', user_path)
        for line in S:
            if 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' in line:
                line_s = line.replace(
                    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
                    cur_dirB)
            elif 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB' in line:
                line_s = line.replace('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
                                      user_path)
            else:
                line_s = line  # 如果没有匹配项，则保留原行（可选）
            load.append(line_s)
        S.close()
        print('修改文件：',Target)
        T = open(Target, 'w')
        for line in load:
            T.writelines(line)  # 将替换后的写入新的.txt
        T.close()

    # 新版本安装
    def install_new_version(self):
        # 创建用户文件夹
        self.create_user_folder()
        # print(self.user_path)
        time.sleep(1)
        # 写入插件文件
        self.update_current_folder_files(self.user_path)
        # 写入mod文件
        self.get_maya_mod_path(self.user_path)
        # print(self.user_path +'\\ZKM_plug_in.py')
        cmds.pluginInfo(self.user_path +'\\ZKM_plug_in.py', edit=1, autoload=True)

        # 目标插件目录（示例路径）
        new_plugin_path = self.user_path.replace("/", "\\")+'/'

        # 获取当前 MAYA_PLUG_IN_PATH 的值
        current_path = os.getenv("MAYA_PLUG_IN_PATH", "")
        # print(current_path)
        path_list = current_path.split(os.pathsep) if current_path else []

        # 添加新路径（避免重复）
        if new_plugin_path not in path_list:
            path_list.append(new_plugin_path)
            updated_path = os.pathsep.join(path_list)
            os.environ["MAYA_PLUG_IN_PATH"] = updated_path  # 更新当前会话环境变量
            # print(f"已添加路径: {new_plugin_path}")

        cmds.loadPlugin('ZKM_plug_in')
        cmds.warning('如果是安装到自定义的已有路径，并且是重复安装的需要重开maya，打开插件管理器，拉到最后把ZKM_plug_in加载和自动加载勾上。')

window = Window()
if __name__ == '__main__':
    window.show()
window.show()
