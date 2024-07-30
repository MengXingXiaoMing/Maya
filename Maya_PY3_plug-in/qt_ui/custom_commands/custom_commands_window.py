# coding=gbk
import random
import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import os
import sys
import inspect

# �ļ�·��
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# ��·��
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# �汾��
maya_version = cmds.about(version=True)
# ��·��
library_path = root_path + '\\' + maya_version

# ����ӵ�ϵͳ·��
sys.path.append(library_path)
import others_library
from others_library import *
importlib.reload(others_library)




class Window(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("�Զ�������")
        self.setMinimumWidth(300)


class Command():
    def __init__(self):
        # �ļ�·��
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # ��·��
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        self.root_path_reversal = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        # �汾��
        self.maya_version = cmds.about(version=True)
        # ��·��
        self.library_path = self.root_path + '\\' + maya_version
        self.library_path_reversal = self.root_path_reversal + '/' + maya_version

        self.window = Window()

        self.others_library = OthersLibrary()
        self.all_file_type = []
        self.all_file_ui = []
        self.read_base_set()
        #self.command_name_list = self.command_list()
        #self.command_button = []
        #self.need_continue_expanding_ui = []
        #self.trigger_need_continue_expanding_ui = []

    def create_widgets(self):
        self.menu_bar = QtWidgets.QMenuBar()

        self.display_menu = self.menu_bar.addMenu('��ʾ')

        help_menu = self.menu_bar.addMenu('����')

        self.help_action = QtWidgets.QAction('����')
        help_menu.addAction(self.help_action)

        self.Label_1 = QtWidgets.QLabel('·��:')
        self.line_edit_0 = QtWidgets.QLineEdit()  # ·����

        self.Label_2 = QtWidgets.QLabel('�������:')
        self.line_edit_2 = QtWidgets.QLineEdit()  # ��ȿ�
        self.line_edit_2.setMaximumWidth(30)

        self.button_1 = QtWidgets.QPushButton('����')
        self.line_edit_1 = QtWidgets.QLineEdit() # ������

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.tree_widget.setHeaderHidden(True)

        '''self.button_1 = QtWidgets.QPushButton()
        if QtCore.QResource(':/rebuild.png').isValid():
            i = QtGui.QIcon(':/rebuild.png')
            self.button_1.setIcon(i)

        self.button_2 = QtWidgets.QPushButton()
        self.button_2.setText('�½�')

        self.button_3 = QtWidgets.QPushButton()
        if QtCore.QResource(':/fileNew.png').isValid():
            i = QtGui.QIcon(':/fileNew.png')
            self.button_3.setIcon(i)'''

        '''# ���°�ť��ǩΪ����ַ���
        for txt in self.command_name_list:
            button = QtWidgets.QPushButton()
            self.command_button.append(button)
            button.setText(txt)'''

    def create_layouts(self, old_window):
        self.central_widget = QtWidgets.QWidget(old_window)
        old_window.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)


        self.main_layout.setMenuBar(self.menu_bar)

        h_box_layout_1 = QtWidgets.QHBoxLayout()
        h_box_layout_1.addWidget(self.Label_1)
        h_box_layout_1.addWidget(self.line_edit_0,stretch=1)

        h_box_layout_1.addWidget(self.Label_2)
        h_box_layout_1.addWidget(self.line_edit_2)

        h_box_layout_1.addWidget(self.button_1)

        self.main_layout.addLayout(h_box_layout_1)

        self.main_layout.addWidget(self.line_edit_1)
        self.main_layout.addWidget(self.tree_widget)

        '''h_box_layout_2 = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(h_box_layout_2)
        h_box_layout_2.addWidget(self.button_1)
        h_box_layout_2.addWidget(self.button_2)
        h_box_layout_2.addWidget(self.button_3)

        self.scroll_area_1 = QtWidgets.QScrollArea(old_window)

        self.scroll_area_1.setWidgetResizable(True)
        self.scroll_area_1.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area_1.setWidget(QWidget())

        self.main_layout.addWidget(self.scroll_area_1)

        self.flow_layout_1 = FlowLayout(self.scroll_area_1.widget())
        self.flow_layout_1.setSpacing(0)

        self.flow_widget = QtWidgets.QWidget()
        self.v_box_layout_1 = QtWidgets.QVBoxLayout(self.flow_widget)
        self.flow_layout_1.addWidget(self.flow_widget)

        for button in self.command_button:
            self.v_box_layout_1.addWidget(button)'''

    def create_connect(self):
        #self.tree_widget.selectedItems()
        self.tree_widget.itemClicked.connect(self.tree_widget_itemClicked)
        #self.tree_widget.itemSelectionChanged.connect(self.get_current_select)
        self.tree_widget.itemDoubleClicked.connect(self.get_current_select)
        self.button_1.clicked.connect(self.seve_base_set)
        self.line_edit_1.returnPressed.connect(self.ergodic_file)
        self.help_action.triggered.connect(self.help)

    def command_list(self):
        # ��ȡָ��Ŀ¼�µ�����ָ����׺���ļ���
        file_list = []
        list = os.listdir(self.ui_path)  # �����ļ���
        for l in list:
            file_list.append(l)
        return file_list, self.ui_path

    def flie_command_list(self, name, file_path):
        # ��ȡָ��Ŀ¼�µ�����ָ����׺���ļ���
        file_list = []
        file_path = file_path + '/' + str(name)
        # if len(name.split('.')) < 2:
        if os.path.isdir(file_path):
            list = os.listdir(file_path)  # �����ļ���
            for l in list:
                file_list.append(l)
        return file_list, file_path

    def refresh_tree_widget(self):
        self.tree_widget.clear()
        top_level_object_names, file_path = self.command_list()
        for name in top_level_object_names:
            self.continue_iteration_ui = []
            self.now_depth = 1
            item = self.create_item(name, file_path)
            self.tree_widget.addTopLevelItem(item)
        # �ɼ���չ����ui
        #for ui in self.need_continue_expanding_ui:
        #    print(ui.text(0))
        # �����ɼ���չ����ui
        #for ui in self.trigger_need_continue_expanding_ui:
        #    print(ui.text(0))

    def create_item(self, name, file_path):
        item = QtWidgets.QTreeWidgetItem([name])
        item.setData(0, Qt.UserRole, file_path)
        #print(self.now_depth)
        if self.depth < 2:
            self.now_depth = self.depth - 1
        if self.now_depth < self.depth:
            self.now_depth = self.now_depth + 1
            if self.now_depth <= self.depth:
                self.add_chileren(item)
            #if self.now_depth == self.depth - 1 :
            #    self.trigger_need_continue_expanding_ui.extend(ui_list)
            #if self.now_depth > self.depth - 1 :
            #    self.trigger_need_continue_expanding_ui.extend(ui_list)
            #    self.need_continue_expanding_ui.extend(ui_list)
        else:
            self.now_depth = self.now_depth - 1
        self.update_icon(item, name, file_path)
        self.all_file_ui.append(item)
        if not os.path.isdir(file_path + '/' + str(name)):
            type = name.split('.')[-1]
            self.all_file_type.append(type)
            self.all_file_type = list(set(self.all_file_type))
        return item

    def add_chileren(self, item):
        file_path = item.data(0, Qt.UserRole)
        chileren, file_path = self.flie_command_list(item.text(0), file_path)
        if chileren:
            for child in chileren:
                child_item = self.create_item(child, file_path)
                item.addChild(child_item)

    def update_icon(self, item, name, file_path):
        file_icon_provider = QFileIconProvider()
        file_path = file_path + '/' + name
        icon = file_icon_provider.icon(QFileInfo(file_path))
        item.setIcon(0, icon)
    # �������������ļ������ذ�ť
    def show_display_ui(self):
        self.display_ui = []
        for type in self.all_file_type:
            display_shape_action = QtWidgets.QAction(type, checkable=True)
            self.display_ui.append(display_shape_action)
            display_shape_action.setChecked(True)
            self.display_menu.addAction(display_shape_action)
            display_shape_action.toggled.connect(self.display_file_ui)
    # ���ļ�������ʾ
    def display_file_ui(self):
        need_hide = []
        for ui in self.display_ui:
            show = ui.isChecked()
            if show == True:
                type = ui.text()
                need_hide.append(type)
        for ui in self.all_file_ui:
            name = ui.text(0)
            file_path = ui.data(0, Qt.UserRole)
            if not os.path.isdir(file_path + '/' + name):
                if name.split('.')[-1] in need_hide:
                    ui.setHidden(False)
                else:
                    ui.setHidden(True)

    # �����ļ�
    def ergodic_file(self):
        text = self.line_edit_1.text()
        if text:
            for ui in self.all_file_ui:
                name = ui.text(0)
                file_path = ui.data(0, Qt.UserRole)
                if not os.path.isdir(file_path + '/' + name):
                        if text in name:
                            ui.setHidden(False)
                        else:
                            ui.setHidden(True)
        else:
            self.display_file_ui()

    # ���е�ǰѡ��
    def get_current_select(self):
        is_run = False
        selected_items = self.tree_widget.selectedItems()
        file_path = ''
        file_name = ''
        for ui in selected_items:
            file_name = ui.text(0)
            file_path = ui.data(0, Qt.UserRole)
            file = (file_path + '/' + file_name)
            if_file = os.path.isdir(file)
            if if_file == True:
                is_run = True
                continue
            if file_name.split('.')[-1] == 'py':
                # with open(file_path + '/' + file_name,'r', encoding='gbk') as file:
                #     code = file.read()
                #     exec(code, globals())

                # global self_open_file
                # self_open_file = file_path
                # exec(open(file_path + '/' + file_name).read())
                self.others_library.load_source(file_name, (file_path + '/' + file_name))
                is_run = True
                continue
            if file_name.split('.')[-1] == 'mel':
                mel.eval('source "'+file_path + '/' + file_name+'";')
                is_run = True
                continue
        if is_run == False:
            os.startfile(file_path + '/' + file_name)
            cmds.warning(file_path + '/' + file_name +'û�����У���Ĭ�ϴ򿪷�ʽ�򿪡�')

    # ��״�����е�����е�����
    def tree_widget_itemClicked(self):
        self.select_expand_or_collapse_all_projects()
        self.if_continue_iteration()

    # ����ж��Ƿ��������
    def if_continue_iteration(self):
        sel = self.tree_widget.selectedItems()
        for s in sel:
            self.continue_iteration_ui = []
            self.now_depth = 1
            name = s.text(0)
            parent_file_path = s.data(0, Qt.UserRole)
            if s.childCount() == 0:
                chileren, file_path = self.flie_command_list(s.text(0), parent_file_path)
                if chileren:
                    for c in chileren:
                        item = self.create_item(c, file_path)
                        s.addChild(item)

    # ����ǰѡ��ȫ��չ����������
    def select_expand_or_collapse_all_projects(self):
        sel = self.tree_widget.selectedItems()
        expand = 1
        if sel[0].isExpanded():
            expand = 0
        for s in sel:
            self.expand_or_collapse_all_projects([s],expand)
    # ȫ��չ����������
    def expand_or_collapse_all_projects(self,item,expand):
        if QGuiApplication.keyboardModifiers() & Qt.ShiftModifier:
            if item:
                if expand == 0:
                    item[0].setExpanded(False)
                else:
                    item[0].setExpanded(True)
                # �ݹ��չ����������
                for index in range(item[0].childCount()):
                    child_item = item[0].child(index)
                    self.expand_or_collapse_all_projects([child_item],expand)


    # ��·�����浽Ĭ������
    def seve_base_set(self):
        file_path = self.line_edit_0.text()
        iteration_depth = self.line_edit_2.text()
        with open(self.file_path+'\\base_set.txt', 'r', encoding='utf-8') as file:
            # ���ж�ȡ�ļ�����
            lines = file.readlines()
        lines[0]= file_path + '\n'
        lines[1] = iteration_depth + '\n'
        with open(self.file_path+'\\base_set.txt', 'w', encoding='utf-8') as file:
            # д���ı�
            for l in lines:
                file.write(l)
            # ��'with'�����ʱ���ļ����Զ��ر�
        print('д��'+self.file_path+'\\base_set.txt'+'��ϡ�')
        self.read_base_set()
        self.refresh_tree_widget()
    # ��ȡ��������
    def read_base_set(self):
        # ���ļ���ʹ��'r'��ʾ��ȡģʽ
        with open(self.file_path+'\\base_set.txt', 'r', encoding='utf-8') as file:
            # ���ж�ȡ�ļ�����
            lines = file.readlines()
            # ��ӡÿһ��
        if lines:
            file_path = lines[0]
            self.ui_path = file_path[:-1]
            if not os.path.exists(self.ui_path):
                print('�ļ�·�������ڣ����޸�ΪĬ�ϡ�')
                self.ui_path = self.library_path_reversal + '/custom_commands'
            file_path = lines[1]
            if file_path == '\n':
                self.depth = 1
            else:
                self.depth = int(file_path[:-1])
            # try:
            #
            #     self.depth = int(file_path[:-1])
            # except:
            #     self.depth = 1
            try:
                self.depth = int(file_path[:-1])
            except:
                self.depth = 1
                print('������Ȳ����ڣ�������ΪĬ�����ޣ�1����')
            try:
                self.create_set()
            except:
                pass



    def create_set(self):
        self.line_edit_0.setText(self.ui_path)
        self.line_edit_2.setText(str(self.depth))
    def help(self):
        self.others_library.open_web(1)

    def show(self):
        self.create_widgets()
        self.create_layouts(old_window)
        self.create_connect()
        self.refresh_tree_widget()
        self.show_display_ui()
        self.create_set()
        old_window.show(dockable=True, floating=True, area='left')

def is_global_var_defined():
    return 'old_window' in globals()

if not is_global_var_defined():
    global old_window
    old_window = Window()
window = Command()
if __name__ == '__main__':
    window.show()
