# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
# from PySide6.QtCore import Signal, Qt, QObject, QEvent
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    # 库路径
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
        # print("文件夹存在")
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)

# import maya.app.general.artAttrSkinJointMenuUpdater as skinUpdater

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import weight
importlib.reload(weight)
from weight import *

import model
importlib.reload(model)
from model import *

class CustomDelegate(QStyledItemDelegate):
    # 定义信号，参数为 (旧文本, 新文本, 是否被用户编辑)
    editingFinished = Signal(str, str, QTreeWidgetItem)

    def createEditor(self, parent, option, index):
        # 创建默认编辑器（例如 QLineEdit）
        editor = super().createEditor(parent, option, index)
        self.old_text = index.data()  # 保存编辑前的文本
        self.current_item = None  # 初始化当前项
        if isinstance(parent, QTreeWidget):
            self.current_item = parent.itemFromIndex(index)  # 获取当前项
        return editor

    def setModelData(self, editor, model, index):
        # 获取新文本
        new_text = editor.text()
        # 发送信号（旧文本、新文本、对应的项）
        self.editingFinished.emit(self.old_text, new_text, self.current_item)
        # 调用父类方法完成数据保存
        super().setModelData(editor, model, index)

class MyTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Column 1"])
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)  # 启用内部拖拽
        self.setSortingEnabled(False)
        self.expandAll()
        self._selected_items_before_drag = []
        # self.setMaximumHeight(99999)
        # 连接 itemChanged 信号
        # self.itemChanged.connect(self.on_item_changed)

        # 连接 itemDoubleClicked 信号
        self.original_text = []
        # self.itemDoubleClicked.connect(self.on_item_double_clicked)

        # self.itemSelectionChanged.connect(self.on_selection_changed)
        # 保存上次选择的项
        # self.last_selected_item = None

        # 设置自定义委托
        self.delegate = CustomDelegate()
        self.setItemDelegate(self.delegate)
        # 连接信号
        self.delegate.editingFinished.connect(self.on_edit_finished)

    def on_edit_finished(self, old_text, new_text, item):
        if old_text != new_text:
            # print(f"用户编辑完成: {old_text} -> {new_text}")
            if old_text and cmds.objExists(old_text) and old_text != new_text:
                cmds.rename(old_text, new_text)
                for i in range(window.list_widget_1.topLevelItemCount()):
                    item = window.list_widget_1.topLevelItem(i)  # 从 0 开始移除并获取项
                    # print(item.text(0))
                    if item.text(0) == old_text:
                        item.setText(0, new_text)

                for i in range(window.list_widget_2.topLevelItemCount()):
                    item = window.list_widget_2.topLevelItem(i)  # 从 0 开始移除并获取项
                    # print(item.text(0))
                    if item.text(0) == old_text:
                        item.setText(0, new_text)

                for i in range(window.list_widget_3.topLevelItemCount()):
                    item = window.list_widget_3.topLevelItem(i)  # 从 0 开始移除并获取项
                    # print(item.text(0))
                    if item:
                        for i in range(item.childCount()):
                            text = item.child(i).text(0)
                            if text == old_text:
                                item.child(i).setText(0, new_text)

                # sel = cmds.ls(sl=1)
                # cmds.select(sel)
    # def on_item_double_clicked(self, item, column):
    #         # 在编辑开始前保存原始文本
    #         self.original_text = item.text(column)
    #         # print(self.original_text)
    #         # print(f"编辑前的文本: {self.original_text}")
    #         # 开始编辑模式
    #         print('double_clicked:',self.original_text)
    #         # item.setFlags(item.flags() | Qt.ItemIsEditable)
    #         # item.editItem(item, column)
    #         # item.setFlags(item.flags() | Qt.ItemIsEditable)
            # self.editItem(item, column)
    # def on_item_changed(self, item, column):
    #     # cmds.undoInfo(ock=1)
    #     # 获取修改后的文本
    #     new_text = item.text(column)
    #     # print(new_text)
    #     # print(f"修改前的文本: {self.original_text}")
    #     # print(f"修改后的文本: {new_text}")
    #
    #     # if cmds.objExists(new_text):
    #     #     # 恢复原始文本
    #     #     item.setText(column, self.original_text)
    #     #     # 显示警告（这里假设 cmds.warning 是有效的函数）
    #     #     cmds.warning('该名称已存在，请重新命名！')
    #     # item.setText(0, new_text)
    #     if self.original_text and cmds.objExists(self.original_text) and self.original_text!=new_text:
    #         # uid = cmds.ls(self.original_text, uid=1)
    #         # print(self.original_text,new_text)
    #         # new_name = cmds.ls(uid)
    #         # item.setText(0, new_name[0])
    #         cmds.rename(self.original_text, new_text)
    #         for i in range(window.list_widget_1.topLevelItemCount()):
    #             item=window.list_widget_1.topLevelItem(i)  # 从 0 开始移除并获取项
    #             # print(item.text(0))
    #             if item.text(0) == self.original_text:
    #                 item.setText(0,new_text)
    #
    #         for i in range(window.list_widget_2.topLevelItemCount()):
    #             item=window.list_widget_2.topLevelItem(i)  # 从 0 开始移除并获取项
    #             # print(item.text(0))
    #             if item.text(0) == self.original_text:
    #                 item.setText(0,new_text)
    #
    #
    #         for i in range(window.list_widget_3.topLevelItemCount()):
    #             item=window.list_widget_3.topLevelItem(i)  # 从 0 开始移除并获取项
    #             # print(item.text(0))
    #             if item:
    #                 for i in range(item.childCount()):
    #                     text = item.child(i).text(0)
    #                     if text == self.original_text:
    #                         item.child(i).setText(0,new_text)
    #
    #         # sel = cmds.ls(sl=1)
    #         # cmds.select(sel)
    #     print(new_text)
    #     # if self.original_text != new_text:
    #     #     cmds.rename(self.original_text, new_text)
    #     # # 更新原始文本
    #     # self.original_text = []
    #     # cmds.undoInfo(cck=1)
    # def on_selection_changed(self):
    #     # 获取当前选中的项目
    #     selected_items = self.selectedItems()


    # def restore_last_selection(self):
    #     # 恢复上次选择的项
    #     if self.last_selected_item:
    #         for i in range(self.topLevelItemCount()):
    #             item = self.topLevelItem(i)
    #             if item.text(0) == self.last_selected_item:
    #                 self.setCurrentItem(item)
    #                 self.setItemSelected(item, True)
    #                 break

    # def currentChanged(self, current, previous):
    #     dragged_items = self.selectedItems()
    #     print(dragged_items)
    #     if dragged_items:
    #         print(dragged_items[0].text(0))

    def startDrag(self, supportedActions):
        maya_version = int(cmds.about(version=True))
        if maya_version < 2025:
            # 记录拖放前的选择
            self._selected_items_before_drag = [self.topLevelItem(i) for i in range(self.topLevelItemCount()) if
                                                self.isItemSelected(self.topLevelItem(i))]
            super().startDrag(supportedActions)
        else:
            # 使用 selectedItems() 方法获取所有选中的项
            self._selected_items_before_drag = self.selectedItems()

            super().startDrag(supportedActions)

    def dropEvent(self, event):
        # 获取拖拽的目标位置
        target_item = self.itemAt(event.pos())
        # print("Dropped on item:", target_item.text(0))
        dragged_items = self.selectedItems()
        self.clearSelection()
        # dragged_items_txt = dragged_items[0].text(0)
        # print("Dragged items:", dragged_items[0].text(0))
        # 获取所有顶级项
        items = []
        for i in range(self.topLevelItemCount()):
            items.append(self.topLevelItem(i))  # 从 0 开始移除并获取项
        target_index = 0
        dragged_index = 0
        for i in range(0,len(items)):
            if target_item == items[i]:
                target_index = i
            if dragged_items[0] == items[i]:
                dragged_index = i
        items.pop(dragged_index)
        # 在目标位置插入对象
        # print(target_index)
        items.insert(target_index, dragged_items[0])
        # items.insert(0, items[-1])
        # 按新顺序添加项
        # for item in items:
        #     self.addTopLevelItem(item)
        # 获取表头标签
        header_labels = self.headerItem().text(0)
        # for i in range(0,len(items)):
        #     print(items[i].text(0))
        # print('aaaa')
        # print(items[target_index].text(0))
        # print(items[target_index-1].text(0))
        cmds.reorderDeformers(items[target_index-1].text(0), items[target_index].text(0), header_labels)

        # if self.label.geometry().contains(event.pos()):
        #     event.acceptProposedAction()
        #     self.label.setText(f"Dropped: {event.mimeData().text()}")
        # else:
        #     # If the drop position is outside the label, call the base class's dropEvent
        super().dropEvent(event)

        # 使用 QTimer 来延迟到下一个事件循环迭代时恢复选择
        # QTimer.singleShot(0, self.restoreSelection)

        window.creat_select_deform_list()
        # self.setCurrentItem(self.topLevelItem(i))
        maya_version = int(cmds.about(version=True))
        if maya_version < 2025:
            self.setItemSelected(self.topLevelItem(target_index), True)
        else:
            # 遍历所有项，匹配标识符
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                identifier = item.data(0, Qt.UserRole)  # 与记录时一致
                if i == target_index:
                    item.setSelected(True)
        # sel = cmds.ls(sl=1)
        # cmds.select(sel)
        # # 获取所有顶级项
        # items = []
        # for i in range(self.topLevelItemCount()):
        #     items.append(self.takeTopLevelItem(0))  # 从 0 开始移除并获取项
        # for i in range(len(items)):
        #     if items[i].text(0) == dragged_items_txt:
        #         self.setCurrentItem(items[i])

        # NoteRole = Qt.UserRole + 1  # 定义一个自定义角色
        # self.setData(0, NoteRole, "This is a note for the item")
        # # 检索备注
        # note = self.data(0, NoteRole)
        # print(note)

    def restoreSelection(self):
        # 清除当前选择
        self.clearSelection()
        # 恢复之前的选择
        for item in self._selected_items_before_drag:
            # 由于拖放可能改变了项目的顺序或位置，我们需要重新查找并选择它们
            # 这里我们假设所有项目仍然是顶级项目，并且没有嵌套结构
            for i in range(self.topLevelItemCount()):
                if self.topLevelItem(i).text(0) == item.text(0):  # 通过文本比较来找到相同的项目
                    self.setCurrentItem(self.topLevelItem(i))
                    self.setItemSelected(self.topLevelItem(i), True)
                    break

class MyTreeWidget_2(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(['Column 1'])
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)  # 启用内部拖拽
        self.setSortingEnabled(False)
        self.expandAll()
        self._selected_items_before_drag = []
        self.setMaximumHeight(99999)
        # 连接 itemChanged 信号
        # self.itemChanged.connect(self.on_item_changed)

        # 连接 itemDoubleClicked 信号
        self.original_text = []
        # self.itemDoubleClicked.connect(self.on_item_double_clicked)
        # 设置选择模式为允许多项选择
        # self.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.itemSelectionChanged.connect(self.on_selection_changed)
        # 保存上次选择的项
        # self.last_selected_item = None
        # 设置选择模式为ContiguousSelection
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)  #可按住shift多选
        self.itemSelectionChanged.connect(self.creat_select_deform_list)
        # 连接信号到槽函数
        self.itemClicked.connect(self.reselect)

        # 设置上下文菜单策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 设置自定义委托
        self.delegate = CustomDelegate()
        self.setItemDelegate(self.delegate)
        # 连接信号
        self.delegate.editingFinished.connect(self.on_edit_finished)

        self.model = Model()



    def on_edit_finished(self, old_text, new_text, item):
        if old_text != new_text:
            if old_text and cmds.objExists(old_text) and old_text != new_text:
                cmds.rename(old_text, new_text)
                for i in range(window.list_widget_1.topLevelItemCount()):
                    item = window.list_widget_1.topLevelItem(i)  # 从 0 开始移除并获取项
                    if item.text(0) == old_text:
                        item.setText(0, new_text)

                for i in range(window.list_widget_2.topLevelItemCount()):
                    item = window.list_widget_2.topLevelItem(i)  # 从 0 开始移除并获取项
                    if item.text(0) == old_text:
                        item.setText(0, new_text)

                for i in range(window.list_widget_3.topLevelItemCount()):
                    item=window.list_widget_3.topLevelItem(i)  # 从 0 开始移除并获取项
                    if item:
                        for i in range(item.childCount()):
                            text = item.child(i).text(0)
                            if text == old_text:
                                item.child(i).setText(0,new_text)

    def show_context_menu(self, position):
        # 获取当前点击的项
        item = self.itemAt(position)
        if not item:
            return  # 如果没有点击到项，则不显示菜单
        date = item.data(0, Qt.UserRole)
        self.setCurrentItem(item)
        if date:
            # 创建右键菜单
            menu = QMenu(self)

            # 添加菜单项
            action1 = QAction('记录模型和权重数据(不包括蒙皮)', self)
            menu.addAction(action1)
            action2 = QAction('读取信息生成模型', self)
            menu.addAction(action2)
            action3 = QAction('将当前选择对象所含变形器且也在组内的所有变形器统一复制权重', self)
            menu.addAction(action3)
            action4 = QAction('将当前选择对象所含变形器在组内的权重全部归一', self)
            menu.addAction(action4)
            action5 = QAction('删除记录的数据', self)
            menu.addAction(action5)
            action6 = QAction('将选择蒙皮拷贝到组内所有蒙皮', self)
            menu.addAction(action6)
            action7 = QAction('将组内所有蒙皮拷贝到当前选择蒙皮', self)
            menu.addAction(action7)

            # 连接菜单项的点击事件
            action1.triggered.connect(lambda: self.on_action_triggered(item, 0))
            action2.triggered.connect(lambda: self.on_action_triggered(item, 1))
            action3.triggered.connect(lambda: self.on_action_triggered(item, 2))
            action4.triggered.connect(lambda: self.on_action_triggered(item, 3))
            action5.triggered.connect(lambda: self.on_action_triggered(item, 4))
            action6.triggered.connect(lambda: self.on_action_triggered(item, 5))
            action7.triggered.connect(lambda: self.on_action_triggered(item, 6))
            self.setCurrentItem(item)
            # 显示菜单
            menu.exec_(self.viewport().mapToGlobal(position))

    def on_action_triggered(self, item, function_type):
        node = item.text(0)
        if function_type == 0:
            if cmds.objExists(node + '.vertex_positions') and cmds.objExists(
                    node + '.vertex_normals') and cmds.objExists(node + '.all_topology') and cmds.objExists(
                    node + '.uv_coords_us') and cmds.objExists(node + '.uv_coords_vs') and cmds.objExists(
                    node + '.all_uv_topology') and cmds.objExists(node + '.smooth_group') and cmds.objExists(node + '.weight_list'):
                # cmds.warning('数据存在')
                cmds.warning('数据已存在')
            else:
                # 记录模型和权重数据
                items = window.list_widget_1.selectedItems()
                if items:
                    sel = cmds.ls(sl=1)[0]
                    text = items[0].text(0)
                    # print(text)
                    items_parent = []
                    if items:
                        item_1 = items[0].text(0)
                        items_parent = items[0].parent()
                    parent_is_bs_1 = False
                    items_parent_text = ''
                    if items_parent:
                        items_parent_text = items_parent.text(0)
                        if cmds.nodeType(items_parent_text) == 'blendShape':
                            parent_is_bs_1 = True
                    item_1_type = []
                    if text:
                        if cmds.objExists(text):
                            item_1_type = cmds.nodeType(text)
                    if item_1_type == 'skinCluster':
                        cmds.warning('skinCluster不被记录')
                        weight_list = []
                    elif item_1_type == 'blendShape':
                        weight_list, bs_list = window.read_weight(sel, text, text)
                        # cluster = self.create_skin(self.obj_1, weight_list, ['reversal'])
                        # self.set_deform_weight(self.obj_1, self.obj_1, item_1, cluster, [], 1)
                    elif parent_is_bs_1 == True:
                        weight_list, bs_list = window.read_weight(sel, items_parent_text, 'bs.'+text)
                        # cluster = self.create_skin(self.obj_1, weight_list, ['reversal'])
                        # self.set_deform_weight(self.obj_1, self.obj_1, items_parent_text, cluster, items_parent_text, 1)
                    else:
                        weight_list, bs_list = window.read_weight(sel, text, [])
                    if weight_list:
                        # print(sel)
                        sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = self.model.get_mesh_structure_2(sel)
                        all_topology = self.mintarray_list_to_python_list(all_topology)

                        for list,an in zip(
                                [vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology,smooth_group,weight_list],
                                ['vertex_positions', 'vertex_normals', 'all_topology', 'uv_coords_us', 'uv_coords_vs','all_uv_topology', 'smooth_group', 'weight_list']):
                            cmds.addAttr(node, ln=an, dt='string')
                            cmds.setAttr(node+'.'+an, e=1, keyable=True)
                            cmds.setAttr(node+'.'+an, str(list), type='string')
                else:
                    cmds.warning('没有找到权重')
        if cmds.objExists(node + '.vertex_positions') and cmds.objExists(
                node + '.vertex_normals') and cmds.objExists(node + '.all_topology') and cmds.objExists(
            node + '.uv_coords_us') and cmds.objExists(node + '.uv_coords_vs') and cmds.objExists(
            node + '.all_uv_topology') and cmds.objExists(node + '.smooth_group') and cmds.objExists(
            node + '.weight_list') and function_type <= 4:
            if function_type == 1:
                # 读取信息生成模型
                mesh ,cluster = self.read_data_to_create_a_model(node)
                # print(mesh)

            elif function_type == 2:
                sel = cmds.ls(sl=1)
                mesh, cluster = self.read_data_to_create_a_model(node)
                self.copy_weight(sel,item,mesh, cluster)

            elif function_type == 3:
                sel = cmds.ls(sl=1)
                mesh, cluster = self.read_data_to_create_a_model(node)
                cmds.delete(cluster)
                cluster = cmds.cluster(mesh)
                self.copy_weight(sel,item,mesh ,cluster)

            elif function_type == 4:
                # 删除记录的数据
                for an in ['vertex_positions', 'vertex_normals', 'all_topology', 'uv_coords_us', 'uv_coords_vs',
                         'all_uv_topology', 'smooth_group', 'weight_list']:
                    if cmds.objExists(node + '.' + an):
                        cmds.deleteAttr(node, at=an)
                cmds.warning('数据已经删除')
        else:
            cmds.warning('数据不存在')

        if function_type == 5:
            get = self.copy_skinweight('o_m')
            if get == True:
                cmds.warning('一对多拷贝完成')

        if function_type == 6:
            get = self.copy_skinweight('m_o')
            if get == True:
                cmds.warning('多对一拷贝完成')

    # 读取数据创建模型
    def read_data_to_create_a_model(self,node):
        # 读取信息生成模型
        mesh = []
        cluster = []
        if cmds.objExists(node + '.vertex_positions')and cmds.objExists(
                        node + '.vertex_normals') and cmds.objExists(node + '.all_topology') and cmds.objExists(
                    node + '.uv_coords_us') and cmds.objExists(node + '.uv_coords_vs') and cmds.objExists(
                    node + '.all_uv_topology') and cmds.objExists(node + '.smooth_group') and cmds.objExists(
                    node + '.weight_list'):

            vertex_positions = []
            vertex_normals = []
            all_topology = []
            uv_coords_us = []
            uv_coords_vs = []
            all_uv_topology = []
            smooth_group = []
            weight_list = []
            # 获取插件默认生成的部分
            all_list = [vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs,
                        all_uv_topology, smooth_group, weight_list]
            all_an = ['vertex_positions', 'vertex_normals', 'all_topology', 'uv_coords_us', 'uv_coords_vs',
                      'all_uv_topology', 'smooth_group', 'weight_list']

            for i in range(len(all_list)):
                list = cmds.getAttr(node + '.' + all_an[i])  # 获取数据
                list = list.replace('\'', '\"')
                list = json.loads(list)
                if all_an[i] == 'all_topology':
                    self.python_list_to_mintarray_list(list)
                all_list[i] = list

            mesh = self.model.creare_mesh(all_list[0], all_list[1], all_list[2], all_list[3], all_list[4], all_list[5],
                                          all_list[6])

            self.model.assign_material([mesh], [], ['lambert1'])
            # print(mesh)
            # 创建权重
            cluster = window.create_skin(mesh, all_list[-1], ['copy'])
        else:
            cmds.warning('数据不存在')
        return mesh, cluster

    @staticmethod
    def mintarray_list_to_python_list(mintarray_list):
        """
        将MIntArray列表转换为传统Python列表

        参数:
            mintarray_list: 包含MIntArray对象的列表

        返回:
            list: 传统Python嵌套列表
        """
        if not isinstance(mintarray_list, list):
            raise TypeError("输入必须是列表类型")

        python_list = []
        for item in mintarray_list:
            if isinstance(item, om.MIntArray):
                # 将MIntArray转换为Python列表
                python_list.append(list(item))
            elif isinstance(item, (list, tuple)):
                # 如果已经是列表或元组，直接添加
                python_list.append(list(item))
            else:
                raise TypeError(f"列表元素必须是MIntArray、列表或元组类型，实际类型: {type(item)}")

        return python_list

    @staticmethod
    def python_list_to_mintarray_list(python_list):
        """
        将传统Python列表转换为MIntArray列表

        参数:
            python_list: 传统Python嵌套列表

        返回:
            list: 包含MIntArray对象的列表
        """
        if not isinstance(python_list, list):
            raise TypeError("输入必须是列表类型")

        mintarray_list = []
        for item in python_list:
            if isinstance(item, om.MIntArray):
                # 如果已经是MIntArray，直接添加
                mintarray_list.append(item)
            elif isinstance(item, (list, tuple)):
                # 将列表或元组转换为MIntArray
                mintarray_list.append(om.MIntArray(item))
            else:
                raise TypeError(f"列表元素必须是MIntArray、列表或元组类型，实际类型: {type(item)}")

        return mintarray_list

    # 复制权重
    def copy_weight(self,sel,item ,mesh, cluster):
        # 将组内所有变形器统一复制权重
        node = item.text(0)
        all_child = cmds.listConnections(node + '.input1D', source=True, destination=True)
        # print(all_child)
        transform = cmds.listRelatives(mesh, p=1)
        # print(transform)
        items_parent_text_1 = ''
        items_parent_text_2 = ''
        parent_is_bs_1 = False

        for deform in all_child:
            parent_is_bs_2 = False
            for s in sel:
                ls_deform = window.list_deformer_hierarchy(s)
                if deform in ls_deform:
                    window.copy_weight_commend(cluster[0], deform, parent_is_bs_1, parent_is_bs_2, transform[0], s,
                                               items_parent_text_1, items_parent_text_2)
                    break
        cmds.delete(transform)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            modifiers = QApplication.keyboardModifiers()
            if modifiers & Qt.ControlModifier:
                self.setSelectionMode(QAbstractItemView.MultiSelection)
                self.ctrlKeyPressed = True
                # self.clearSelection()  # 清除所有现有选择
                index_under_mouse = self.indexAt(event.pos())
                if index_under_mouse.isValid():
                    item = self.itemFromIndex(index_under_mouse)
                    if item:
                        if item.isSelected():
                            item.setSelected(False)
                        else:
                            item.setSelected(True)
                        self.last_selected_index = index_under_mouse
            else:
                self.ctrlKeyPressed = False
                self.setSelectionMode(QAbstractItemView.ContiguousSelection)
                super().mousePressEvent(event)

    def creat_select_deform_list(self):
        window.creat_select_deform_list()

    def reselect(self):
        sel = cmds.ls(sl=1)
        if sel:
            cmds.select(cl=1)
            cmds.select(sel)

    def startDrag(self, supportedActions):
        maya_version = int(cmds.about(version=True))
        if maya_version<2025:
            # 记录拖放前的选择
            self._selected_items_before_drag = [self.topLevelItem(i) for i in range(self.topLevelItemCount()) if
                                                self.isItemSelected(self.topLevelItem(i))]
            super().startDrag(supportedActions)
        else:
            # 使用 selectedItems() 方法获取所有选中的项
            self._selected_items_before_drag = self.selectedItems()

            super().startDrag(supportedActions)

    def dropEvent(self, event):
        # 获取拖拽的目标位置
        target_item = self.itemAt(event.pos())
        # print("Dropped on item:", target_item.text(0))
        dragged_items = self.selectedItems()
        # dragged_items_txt = dragged_items[0].text(0)
        # print("Dragged items:", dragged_items[0].text(0))
        # 获取所有顶级项
        items = []
        for i in range(self.topLevelItemCount()):
            items.append(self.topLevelItem(i))  # 从 0 开始移除并获取项
        if_continue = 1
        for i in range(len(dragged_items)):
            if dragged_items[i] in items:
                cmds.warning('选择了组')
                if_continue = 0
                break
        if if_continue == 1: # 如果没有选择到组则继续
            if target_item in items:
                # print("Dropped on item:", target_item.text(0))
                # super().dropEvent(event)
                all_select_text = []
                for i in range(len(dragged_items)):
                    text = dragged_items[i].text(0)
                    all_select_text.append(text)
                    pass
                # target_item.setParent(dragged_items[0])
                # 将拖拽的项添加到目标项的子项中
                target_child = target_item.childCount()
                target_remove_child = []
                # 获取重复项
                for dragged_item in dragged_items:
                    for i in range(target_child):
                        text = target_item.child(i).text(0)
                        if text in all_select_text:
                            # target_item.removeChild(target_item.child(i))
                            target_remove_child.append(target_item.child(i))
                            # dragged_items.remove(dragged_item)

                # 从目标移除重复项
                for dragged_item in dragged_items:
                    node = dragged_item.text(0)
                    for item in target_remove_child:
                        soure_an = cmds.listConnections(node + '.envelope', p=1)
                        soure_node = cmds.listConnections(node + '.envelope', s=1)
                        # print(soure_node)
                        # print(target_item.text(0))
                        # print('\n')
                        # print(soure)
                        for i in range(len(soure_node)):
                            if soure_node[i] == target_item.text(0):
                                # print(node+'.envelope',soure_an[i])
                                cmds.disconnectAttr(node + '.envelope', soure_an[i])
                        target_item.removeChild(item)

                # 从源移除
                for dragged_item in dragged_items:
                    # 如果 dragged_item 已经有父项，需要先从其父项中移除
                    node = dragged_item.text(0)
                    soure = dragged_item.parent().text(0)
                    # 断开链接con = cmds.listConnections(connections[i]+'.input3D[0].input3Dx')
                    soure_an = cmds.listConnections(node + '.envelope', p=1)
                    soure_node = cmds.listConnections(node + '.envelope', s=1)
                    # print(soure)
                    for i in range(len(soure_node)):
                        if soure_node[i] == soure:
                            # print(node+'.envelope',soure_an[i])
                            cmds.disconnectAttr(node+'.envelope', soure_an[i])
                    if dragged_item.parent():
                        dragged_item.parent().removeChild(dragged_item)# 从父项移除

                # 添加到目标
                for dragged_item in dragged_items:
                    node = dragged_item.text(0)
                    target_item.addChild(dragged_item)  # 添加到目标项的子项中
                    input1D_value = cmds.getAttr(target_item.text(0) + ".input1D", multiIndices=True)
                    if not input1D_value:
                        input1D_value = [0]
                    cmds.connectAttr(node + '.envelope',
                                     (target_item.text(0) + '.input1D[' + str(input1D_value[-1] + 1) + ']'))

                #
                # for i in range(target_item.childCount()):
                #     text = target_item.child[i].text(0)
                #     if text in all_select_text:
                #         self.removeChild(target_item.child[i])

            else:
                cmds.warning('请拖拽到组')
                pass
        else:
            pass
            # super().dropEvent(event)

    def restoreSelection(self):
        # 清除当前选择
        self.clearSelection()
        # 恢复之前的选择
        for item in self._selected_items_before_drag:
            # 由于拖放可能改变了项目的顺序或位置，我们需要重新查找并选择它们
            # 这里我们假设所有项目仍然是顶级项目，并且没有嵌套结构
            for i in range(self.topLevelItemCount()):
                if self.topLevelItem(i).text(0) == item.text(0):  # 通过文本比较来找到相同的项目
                    self.setCurrentItem(self.topLevelItem(i))
                    self.setItemSelected(self.topLevelItem(i), True)
                    break

    # 拷贝蒙皮权重
    def copy_skinweight(self, copy_way):
        # 获取视窗选择
        dragged_items = window.list_widget_1.selectedItems()
        dragged_items_text = ''
        if dragged_items:
            dragged_items_text1 = dragged_items[0].text(0)
            skin_clusters = cmds.ls(dragged_items_text1, type='skinCluster')
            if skin_clusters:
                dragged_items_text = dragged_items_text1
        # 获取组选择
        layer_items = window.list_widget_3.selectedItems()
        all_child_item_text = []
        if layer_items:
            for layer_item in layer_items:
                if layer_item.data(0, Qt.UserRole):
                    for i in range(0, layer_item.childCount()):
                        child_item = layer_item.child(i)  # 遍历子项
                        child_item_text = child_item.text(0)
                        skin_clusters = cmds.ls(child_item_text, type='skinCluster')
                        if skin_clusters:
                            all_child_item_text.append(child_item_text)
        if dragged_items_text and all_child_item_text:
            print(dragged_items_text)
            print(all_child_item_text)
            #按拷贝方式进行拷贝
            if copy_way  ==  'o_m':
                window.weight.new_maya_base_copy_joint_weight('Normal', dragged_items_text, all_child_item_text, dragged_items_text, all_child_item_text, '', '')
            if copy_way  ==  'm_o':
                # 获取蒙皮影响的形状节点
                mesh = []
                for sk in all_child_item_text:
                    meshes_deformed_by_skin = cmds.deformer(sk, query=True, geometry=True)
                    mesh.append(meshes_deformed_by_skin[0])
                sel = mesh
                new_model = []
                for s in sel:
                    cmds.select(s)
                    cmds.duplicate(rr=1)
                    new_sel = cmds.ls(sl=1)
                    new_model.append(new_sel[0])
                for s, n, s_skin in zip(sel, new_model, all_child_item_text):
                    s = cmds.listRelatives(s, p=1)
                    # print('s:', s,n)
                    # 为目标模型创建蒙皮
                    targetJoint = cmds.skinCluster(s, q=1, inf=1)
                    # print(targetJoint)
                    # 创建skinCluster节点
                    skin_cluster = cmds.skinCluster(targetJoint, n,
                                                    skinMethod=0,  # 经典线性蒙皮
                                                    dropoffRate=1.0)[0] # 权重衰减率
                    window.weight.new_maya_base_copy_joint_weight('Normal', s, [n], s_skin, [skin_cluster], '', '')
                cmds.polyUniteSkinned(new_model, ch=0, mergeUVSets=1, centerPivot=1)
                merged_models = cmds.ls(sl=1)
                for i in new_model:
                    cmds.delete(i)
                s_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + merged_models[0] + '\");')
                # print(s_skin_cluster)
                window.weight.new_maya_base_copy_joint_weight('Normal', merged_models, [dragged_items_text], s_skin_cluster, [dragged_items_text], '', '')
                cmds.delete(merged_models)
            return True
        else:
            cmds.warning('请选择源和目标。')
            return False

class OverlayButton(QToolButton):
    def __init__(self, icon,offset,scale, parent=None):
        super().__init__(parent)
        self.all_icon = []
        self.offset = offset
        for i,s in zip(icon,scale):
            icon1 = QPixmap(i)  # 图片
            if s[0]!=0 and s[1]!=0:
                icon1 = icon1.scaled(QSize(s[0], s[1]))

            self.all_icon.append(icon1)

    def paintEvent(self, event):
        # 调用基类的 paintEvent 方法绘制默认按钮样式
        super().paintEvent(event)

        # 创建 QPainter 对象
        painter = QPainter(self)
        # 获取按钮的矩形区域
        rect = self.rect()
        # 计算中心点的坐标
        center = rect.center()

        # 绘制第一张图片
        for move,icon in zip(self.offset,self.all_icon):
            painter.drawPixmap(QPoint(move[0]+center.x(), move[1]+center.y()), icon)

    # 在OverlayButton类中定义
    doubleClicked = Signal()

    # 在mouseDoubleClickEvent中发射
    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass

        super(Window, self).__init__(parent)
        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('变形器层级编辑(Maya' + self.maya_version + ')(跑别的代码记得关闭此窗口，窗口带脚本影响效率和撤回)')
        # self.resize(750, 250)
        # 提取年月日、时分秒，并转换成数字
        now = datetime.now()
        milliseconds = now.microsecond // 1000  # 将微秒转换为毫
        # 如果你想要一个包含毫秒的字符串表示
        self.time_str = now.strftime("%Y%m%d%H%M%S") + f"{milliseconds:03d}"
        # self.time_str = f"{year}{month:02d}{day:02d}{hour:02d}{minute:02d}{second:02d}"
        # print(self.time_str)
        self.setObjectName('ZKM_deform_edit_window'+self.time_str)

        self.ui_edit = UiEdit()
        self.model = Model()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))

        # 库路径
        self.library_path = root_path + '\\' + maya_version

        self.controller_file_path = cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', q=1, ann=1)
        # print('deform_edit_',self.controller_file_path)
        self.icon_name = ['smoothSkin.png', 'blendShape.png', 'lattice.png', 'cluster.png', 'deltaMush.png', 'tension.png', 'solidify.png',
                     'proximityWrap.png', 'wrap.png', 'shrinkwrap.png', 'morph.png', 'wire.png', 'wrinkle.png', 'sculpt.png', 'textureDeformer.png',
                     'softMod.png','jiggleDeformer.png']

        self.deform_types = ['skinCluster', 'blendShape', 'ffd', 'cluster', 'deltaMush', 'tension', 'solidify',
                        'proximityWrap', 'wrap', 'shrinkwrap', 'morph', 'wire', 'wrinkle', 'sculpt', 'textureDeformer',
                        'softMod','jiggle']

        self.icon_name_1 = ['bendNLD.png','flareNLD.png','sineNLD.png','squashNLD.png','twistNLD.png','waveNLD.png','textureDeformer.png']
        self.deform_types_1 = ['deformBend','deformFlare','deformSine','deformSquash','deformTwist','deformWave','textureDeformer']

        self.loc_name = 'deform_edit_window_loc'
        self.loc_layer_date_name = 'deform_edit_window_loc_layer'
        self.weight = Weight()
        self.obj_1 = []
        self.obj_2 = []

        self.create_widgets()
        self.create_layouts()
        self.create_connect()
        # 注册选择变化运行脚本
        self.register_selection_callback()
        self.creat_date_loc()
        cmds.select(cmds.ls(sl=1))

    def create_widgets(self):
        # 第一行
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItems(['将当前选择物体变形器的',
                                  '将当前选择物体变形器不在组内的',
                                  '将当前选择物体变形器没有加到任意组内的',
                                  ])
        self.comboBox_3 = QtWidgets.QComboBox()
        self.comboBox_3.addItems(['all'])
        self.comboBox_3.addItems(self.deform_types)
        self.comboBox_3.addItems(self.deform_types_1)

        # self.comboBox_1.setMaximumHeight(30)
        self.button_1 = QtWidgets.QPushButton()
        # self.button_2 = QtWidgets.QPushButton()
        self.list_widget_1 = MyTreeWidget()
        self.list_widget_1.setHeaderLabel('')

        # self.button_1.setMinimumSize(QtCore.QSize(30, 30))
        # self.button_1.sizeHint().setHeight(3)
        self.list_widget_2 = MyTreeWidget()
        self.list_widget_2.setHeaderLabel('')

        # self.button_1.setIcon(QtGui.QIcon(':/fileOpen.png'))
        self.button_1.setText('添加到选择组')
        # self.button_1.setMaximumSize(QtCore.QSize(80, 30))
        self.Label_1 = QtWidgets.QLabel('变形器显示层')
        self.Label_1.setAlignment(Qt.AlignCenter)
        self.checkBox_1 = QtWidgets.QCheckBox("编辑模式", self)

        self.icon_button_14 = self.creat_button('', [':/rebuild.png'],
                                               [[-9, -9]], [[0, 0]], [0, 0], [0, 0])  #

        self.list_widget_3 = MyTreeWidget_2()
        self.list_widget_3.setHeaderLabel('')
        self.icon_button_15 = self.creat_button('', [':/moveButtonUp.png'],
                                                [[-9, -9]], [[0, 0]], [0, 0], [0, 0])  # 绘制权重
        self.icon_button_16 = self.creat_button('', [':/moveButtonDown.png'],
                                                [[-9, -9]], [[0, 0]], [0, 0], [0, 0])  # 绘制权重

        self.icon_button_1 = self.creat_button('',[':/paintSkinWeights.png',':paintSetMembership.png'],
                                               [[-18, -13], [-13, -15]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 绘制权重
        self.icon_button_2 = self.creat_button('', [':/addSkinInfluence.png', ':/copySkinWeight.png'],
                                               [[-8, -15], [-21, -13]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 拷贝权重
        # self.icon_button_2.setVisible(False)
        self.icon_button_3 = self.creat_button('', [':/copySkinWeight.png'],
                                               [[-15, -15]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 复制权重
        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.addItems(['-X→X', 'X→-X', '-Y→Y', 'Y→-Y', '-Z→Z', 'Z→-Z'])
        self.icon_button_4 = self.creat_button('', [':/mirrorSkinWeight.png'],
                                               [[-15, -15]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 镜像权重
        self.icon_button_5 = self.creat_button('', [':/reverse.svg', ':/reloadReference.png'],
                                               [[-16, -16], [-8, -8]], [[35, 35],[0, 0]], [40, 40], [40, 40])  # 反转权重
        self.icon_button_17 = self.creat_button('', [':/SoftSelect.png'],
                                                [[-14, -14]], [[30, 30]], [40, 40], [40, 40])  # 绘制权重
        self.icon_button_12 = self.creat_button('', [':/deformImportWeights.png'],
                                                [[-14, -14]], [[0, 0]], [40, 40], [40, 40])  # 导入变形器权重
        self.icon_button_13 = self.creat_button('', [':/deformExportWeights.png'],
                                                [[-14, -14]], [[0, 0]], [40, 40], [40, 40])  # 导出变形器权重
        self.icon_button_6 = self.creat_button('', [':/importSmoothSkin.png', ':/info'],
                                               [[-14, -14], [-15, -5]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 导入权重
        self.icon_button_7 = self.creat_button('', [':/exportSmoothSkin.png', ':/info'],
                                               [[-14, -14], [-15, -4]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 导出权重


        self.icon_button_8 = self.creat_button('', [':/newLayerEmpty.png'],
                                               [[-10, -10]], [[0, 0]], [30, 0], [0, 0])  # 添加层级
        self.icon_button_9 = self.creat_button('', [':/newLayerEmpty.png', ':/delete.png'],
                                               [[-10, -10], [-1, -11]], [[30, 0], [13, 13]], [0, 0], [0, 0])  # 删除层级
        self.icon_button_10 = self.creat_button('', [':/newPCM.png'],
                                                [[-10, -10]], [[0, 0]], [0, 0], [30, 0])  # 添加元素
        self.icon_button_11 = self.creat_button('', [':/deletePCM.png'],
                                                [[-10, -10]], [[0, 0]], [30, 0], [0, 0])  # 删除元素

        self.icon_button_18 = self.creat_button('', [':/copySkinWeight.png', ':teCompDup.png'],
                                               [[-18, -13], [-10, -15]], [[0, 0], [0, 0]], [40, 40], [40, 40])  # 绘制权重
    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        # main_layout.setStretch(0, 1)
        # self.menu_bar = QtWidgets.QMenuBar()
        # self.main_layout.setMenuBar(self.menu_bar)
        # 第一行

        grid_layout_2 = QtWidgets.QGridLayout(self)
        main_layout.addLayout(grid_layout_2)

        # containerWidget_1 = QWidget(self)
        v_Box_layout_1 = QtWidgets.QVBoxLayout(self)
        grid_layout_2.addLayout(v_Box_layout_1, 0, 0, 1, 2)
        v_Box_layout_1.setContentsMargins(0, 0, 0, 0)
        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_1.addLayout(h_Box_layout_5)
        h_Box_layout_5.setContentsMargins(0, 0, 0, 0)
        h_Box_layout_5.addWidget(self.comboBox_1, stretch=1)
        h_Box_layout_5.addWidget(self.comboBox_3, stretch=0)
        h_Box_layout_5.addWidget(self.button_1, stretch=0)
        # h_Box_layout_5.addWidget(self.button_2)
        v_Box_layout_1.addStretch(1)

        v_Box_layout_8 = QtWidgets.QVBoxLayout(self)
        grid_layout_2.addLayout(v_Box_layout_8, 1, 0)
        v_Box_layout_8.addWidget(self.list_widget_1)


        v_Box_layout_4 = QtWidgets.QVBoxLayout(self)
        # grid_layout_2.addWidget(self.button_1, 0, 1)
        grid_layout_2.addLayout(v_Box_layout_4, 1, 1)
        v_Box_layout_4.addWidget(self.list_widget_2)  # ,stretch=1
        # v_Box_layout_4.setSpacing(1)
        # v_Box_layout_4.setStretch(0, 1)


        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        grid_layout_2.addLayout(h_Box_layout_1, 0, 2)
        h_Box_layout_1.addWidget(self.Label_1, stretch=1)
        h_Box_layout_1.addWidget(self.checkBox_1, stretch=0)
        h_Box_layout_1.addWidget(self.icon_button_14, stretch=0)

        v_Box_layout_5 = QtWidgets.QVBoxLayout(self)
        grid_layout_2.addLayout(v_Box_layout_5, 1, 2)
        h_Box_layout_5 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_5.addLayout(h_Box_layout_5)
        h_Box_layout_5.addWidget(self.list_widget_3)
        v_Box_layout_8 = QtWidgets.QVBoxLayout(self)
        h_Box_layout_5.addLayout(v_Box_layout_8)
        vline_0 = QtWidgets.QFrame()
        vline_0.setFrameShape(QFrame.HLine)  # 设置为竖线
        # vline.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
        v_Box_layout_8.addWidget(vline_0)
        v_Box_layout_8.addWidget(self.icon_button_15)
        vline_1 = QtWidgets.QFrame()
        vline_1.setFrameShape(QFrame.HLine)  # 设置为竖线
        # vline.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
        v_Box_layout_8.addWidget(vline_1)
        v_Box_layout_8.addWidget(self.icon_button_16)
        vline_3 = QtWidgets.QFrame()
        vline_3.setFrameShape(QFrame.HLine)  # 设置为竖线
        # vline.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
        v_Box_layout_8.addWidget(vline_3)

        # 设置行伸缩因子
        grid_layout_2.setRowStretch(0, 0)  # 第一行
        grid_layout_2.setRowStretch(1, 10)  # 第二行（较大的伸缩因子）
        grid_layout_2.setRowStretch(2, 0)  # 第三行

        v_Box_layout_6 = QtWidgets.QVBoxLayout(self)
        grid_layout_2.addLayout(v_Box_layout_6, 2, 0, 2, 2)
        v_Box_layout_6.setContentsMargins(0, 0, 0, 0)
        h_Box_layout_1 = QtWidgets.QHBoxLayout(self)
        v_Box_layout_6.addLayout(h_Box_layout_1)
        h_Box_layout_1.setContentsMargins(0, 0, 0, 0)
        # v_Box_layout_6.addLayout(h_Box_layout_1)
        h_Box_layout_1.addWidget(self.icon_button_1)
        h_Box_layout_1.addWidget(self.icon_button_2)
        h_Box_layout_1.addWidget(self.icon_button_3)
        h_Box_layout_1.addWidget(self.icon_button_18)
        h_Box_layout_2 = QtWidgets.QHBoxLayout(self)
        h_Box_layout_1.addLayout(h_Box_layout_2)
        vline_4 = QtWidgets.QFrame()
        vline_4.setFrameShape(QFrame.VLine)  # 设置为竖线
        h_Box_layout_2.addWidget(vline_4)
        h_Box_layout_2.addWidget(self.comboBox_2)
        h_Box_layout_2.addWidget(self.icon_button_4)
        vline_5 = QtWidgets.QFrame()
        vline_5.setFrameShape(QFrame.VLine)  # 设置为竖线
        h_Box_layout_2.addWidget(vline_5)
        h_Box_layout_1.addWidget(self.icon_button_5)
        h_Box_layout_1.addWidget(self.icon_button_17)
        h_Box_layout_1.addWidget(self.icon_button_12)
        h_Box_layout_1.addWidget(self.icon_button_13)
        h_Box_layout_1.addWidget(self.icon_button_6)
        h_Box_layout_1.addWidget(self.icon_button_7)


        vline_2 = QtWidgets.QFrame()
        vline_2.setFrameShape(QFrame.VLine)  # 设置为竖线
        # vline.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
        h_Box_layout_1.addWidget(vline_2)

        splitter = QtWidgets.QSplitter(Qt.Vertical)
        splitter.setContentsMargins(0, 0, 0, 0)
        grid_layout_2.addWidget(splitter, 2, 2)

        Widget_1 = QtWidgets.QWidget()
        h_Box_layout_3 = QtWidgets.QHBoxLayout(Widget_1)
        h_Box_layout_3.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(Widget_1)
        h_Box_layout_3.addWidget(self.icon_button_8)
        h_Box_layout_3.addWidget(self.icon_button_9)
        Widget_2 = QtWidgets.QWidget()
        h_Box_layout_4 = QtWidgets.QHBoxLayout(Widget_2)
        h_Box_layout_4.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(Widget_2)
        h_Box_layout_4.addWidget(self.icon_button_10)
        h_Box_layout_4.addWidget(self.icon_button_11)

        # grid_layout_2.setSpacing(0)





        # main_layout.addStretch(1)

    def create_connect(self):
        self.button_1.clicked.connect(self.add_to_selection_grp)
        # self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_2, ['QLineEdit']))  # 选择拷贝源按钮
        # self.button_3.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_3, ['QLineEdit']))
        # self.button_4.clicked.connect(self.create_bs)  # 选择拷贝源按钮
        self.checkBox_1.clicked.connect(self.creat_select_deform_list)
        self.icon_button_14.clicked.connect(self.rebuild_date_loc)
        self.icon_button_1.clicked.connect(self.edit_weight)
        self.icon_button_2.clicked.connect(self.duplicate_weight)
        self.icon_button_3.clicked.connect(self.copy_weight)
        self.icon_button_4.clicked.connect(self.mirror_deformer_weight)
        self.icon_button_5.clicked.connect(self.reversal_deformer_weight)
        self.icon_button_17.clicked.connect(self.set_soft_weight)
        self.icon_button_12.clicked.connect(self.import_weight_data)
        self.icon_button_13.clicked.connect(self.output_weight_data)

        self.icon_button_8.clicked.connect(self.add_deform_edit_layer)
        self.icon_button_9.clicked.connect(self.delete_deform_edit_layer)
        self.icon_button_10.clicked.connect(self.add_sub_item)
        self.icon_button_11.clicked.connect(self.delete_sub_item)


        self.icon_button_15.clicked.connect(lambda: self.move_layer(-1))
        self.icon_button_16.clicked.connect(lambda: self.move_layer(1))

        self.icon_button_18.clicked.connect(self.copy_deform_an)
        # 正确：使用信号
        self.icon_button_18.doubleClicked.connect(self.copy_deform_an2)

        self.icon_button_6.clicked.connect(self.select_file)
        self.icon_button_7.clicked.connect(self.create_weight_json_file)


    '''def add_item(self, text, icon_type):
        # 设置背景颜色
        item = QtWidgets.QTreeWidgetItem()
        # item.setBackgroundColor(0, QtGui.QColor(0, 0, 0))
        self.list_widget_1.addTopLevelItem(item)
        item.setText(0,text)
        item.visible = False
        icon = QtGui.QIcon(':/empty.png')
        for name in ['smoothSkin', 'blendShape', 'lattice', 'cluster', 'deltaMush', 'tension', 'solidify',
                     'proximityWrap', 'wrap', 'shrinkwrap', 'morph', 'wire', 'wrinkle', 'sculpt', 'textureDeformer',
                     'softMod']:
            if icon_type == name:
                icon = QtGui.QIcon(':/'+name+'.png')
                break
        item.setIcon(0, icon)
        if icon_type == '':
            item.setFlags(Qt.ItemIsEnabled)

        # # 创建根项
        # root = QTreeWidgetItem(self.list_widget_1, ['Root'])
        #
        # # 创建子项
        # child = QTreeWidgetItem(root, ['Child'])
        #
        # # 创建 QLabel 并设置为子项的描述列
        # label = QLabel("Description for Child Item")
        # self.list_widget_1.setItemWidget(child, 1, label)
        # # 设置子项无法被选择
        # child.setFlags(Qt.ItemIsEnabled)'''

    # 创建选择列表
    def creat_select_deform_list(self):
        # print('aaa')
        sel = cmds.ls(sl=True,fl=1)

        i_edit = self.checkBox_1.isChecked()
        layer_items = self.list_widget_3.selectedItems()
        all_child_item_text = []
        if layer_items:
            for layer_item in layer_items:
                if layer_item.data(0, Qt.UserRole):
                # node = layer_item.text(0)
                # child_connections = cmds.listConnections(node + '.input1D', source=True, destination=True)
                # print(child_connections)
                # all_child_item_text = child_connections
                #     print(layer_item.text(0))
                    for i in range(0,layer_item.childCount()):
                        child_item = layer_item.child(i)  # 遍历子项
                        child_item_text = child_item.text(0)
                        all_child_item_text.append(child_item_text)
        # self.list_widget_1.setHeaderLabels('asdfas')
        # selected_texts = [item.text(0) for item in self.list_widget_1.selectedItems()]
        # print(selected_texts)
        dragged_items = self.list_widget_1.selectedItems()
        # print(dragged_items)
        dragged_items_text = ''
        if dragged_items:
            dragged_items_text = dragged_items[0].text(0)
            # print(dragged_items[0].text(0))
        old_name = self.list_widget_1.headerItem().text(0)
        items = self.creat_select_deform_list_1(sel, self.icon_name, self.deform_types)
        new_name = self.list_widget_1.headerItem().text(0)
        if dragged_items and old_name == new_name:
            for i in range(0, len(items)):
                # print(items[i].text(0),dragged_items_text)
                if items[i].text(0) == dragged_items_text:
                    # print('aaaaaaaaa')
                    self.list_widget_1.setCurrentItem(items[i])
                    # self.list_widget_1.setCurrentItem(items[i])
        if items and i_edit:
            for item in items:
                text = item.text(0)
                if not text in all_child_item_text:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)


        dragged_items = self.list_widget_2.selectedItems()
        # print(dragged_items)
        dragged_items_text = ''
        if dragged_items:
            dragged_items_text = dragged_items[0].text(0)
            # print(dragged_items[0].text(0))
        old_name = self.list_widget_2.headerItem().text(0)
        items = self.creat_select_deform_list_2(sel, self.icon_name, self.deform_types)
        new_name = self.list_widget_2.headerItem().text(0)
        if dragged_items and old_name == new_name:
            for i in range(0, len(items)):
                # print(items[i].text(0),dragged_items_text)
                if items[i].text(0) == dragged_items_text:
                    # print('aaaaaaaaa')
                    self.list_widget_2.setCurrentItem(items[i])
        if items and i_edit:
            for item in items:
                text = item.text(0)
                if not text in all_child_item_text:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)

        # if self.obj_1 and self.obj_2 and self.obj_1 != self.obj_2:
        #     self.icon_button_2.setVisible(True)
        # else:
        #     self.icon_button_2.setVisible(False)
    def creat_select_deform_list_1(self,sel,icon_name,deform_types):
        first_sel = []
        self.list_widget_1.setHeaderLabel('')
        self.list_widget_1.clear()
        all_point = []
        if len(sel) > 0:
            first_sel = sel[0]
            name = first_sel.split('.')
            point_name = []
            if len(name) != 1:
                first_sel = name[0]
                for obj in sel:
                    ls_name = obj.split('.')
                    if ls_name[0] == name[0]:
                        point_name.append(obj)
            if point_name:
                all_point = point_name[0]
                for i in range(1, len(point_name)):
                    all_point = all_point + ',' + point_name[i]
            if all_point:
                self.list_widget_1.setHeaderLabel(all_point)
                self.obj_1 = point_name
            elif first_sel:
                self.list_widget_1.setHeaderLabel(first_sel)
                self.obj_1 = first_sel
        first_deform = self.list_deformer_hierarchy(first_sel)
        items = self.create_deformer_button(first_deform, icon_name, deform_types, self.list_widget_1)
        # if dragged_items:
        #     for i in range(len(first_deform)):
        #         if dragged_items[0].text(0) == first_deform[i]:
        #             self.list_widget_1.setCurrentItem(items[i])
        # if icon_type == '':
        #     item.setFlags(Qt.ItemIsEnabled)
        return items

    def creat_select_deform_list_2(self,sel,icon_name,deform_types):
        end_sel = []
        self.list_widget_2.setHeaderLabel('')
        self.list_widget_2.clear()
        all_point = []
        if len(sel) > 0:
            end_sel = sel[-1]
            name = end_sel.split('.')
            point_name = []
            if len(name) != 1:
                end_sel = name[0]
                for obj in sel:
                    ls_name = obj.split('.')
                    if ls_name[0] == name[0]:
                        point_name.append(obj)
            if point_name:
                all_point = point_name[0]
                for i in range(1, len(point_name)):
                    all_point = all_point + ',' + point_name[i]
        if all_point:
            self.list_widget_2.setHeaderLabel(all_point)
            self.obj_2 = point_name
            # print(type(self.obj_2))
        elif end_sel:
            self.list_widget_2.setHeaderLabel(end_sel)
            self.obj_2 = end_sel
            # print(type(self.obj_2))
        # print(self.obj_2)
        end_deform = self.list_deformer_hierarchy(end_sel)
        items = self.create_deformer_button(end_deform, icon_name, deform_types, self.list_widget_2)

        return items

    # 创建变形器按钮
    def create_deformer_button(self,end_deform,icon_name,deform_types,target):
        # cmds.undoInfo(ock=1)
        if end_deform:
            # print(end_deform)
            items = []
            for deform in end_deform:
                item = QtWidgets.QTreeWidgetItem()
                # 启用编辑功能
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                if target:
                    target.addTopLevelItem(item)
                item.setText(0, deform)
                # 保存修改前的文本
                # self.original_text = item.text(0)
                item.visible = False
                icon = QtGui.QIcon(':/empty.png')
                is_over = False
                for name, deform_type in zip(icon_name, deform_types):
                    if cmds.objExists(deform):
                        for icon_type in cmds.nodeType(deform, inherited=True):
                            if icon_type == deform_type:
                                icon = QtGui.QIcon(':/' + name)
                                if deform_type == 'blendShape':
                                    self.create_bs_subset(item,deform)
                                is_over = True
                                break
                            if icon_type == 'nonLinear':
                                for name_1, deform_type_1 in zip(self.icon_name_1, self.deform_types_1):
                                    connected_node = cmds.listConnections(deform+'.matrix', source=True)
                                    # connected_node = cmds.listConnections('flare1.matrix', source=True)
                                    shape_nodes = cmds.listRelatives(connected_node, shapes=True)
                                    # print(shape_nodes)
                                    for icon_type in cmds.nodeType(shape_nodes[0], inherited=True):
                                        if icon_type == deform_type_1:
                                            icon = QtGui.QIcon(':/' + name_1)
                                            is_over = True
                                            break
                item.setIcon(0, icon)
                items.append(item)
            return items

        # cmds.undoInfo(cck=1)

    # 创建bs子集
    def create_bs_subset(self, parent_item,deform_name):
        targets = cmds.ls(deform_name+'.inputTarget[0].inputTargetGroup[*]')
        # print(targets)
        # print(cmds.aliasAttr(parent_item.text(0)+'.w[0]', q=1))
        for target in targets:
            target = target.split('[')[-1][:-1]
            # print(target)
            name = cmds.aliasAttr(deform_name+'.w['+target+']', q=1)
            items = self.create_deformer_button([name], 'blendShape.png', 'blendShape', [])
            icon = QtGui.QIcon(':/blendShape.png')
            items[0].setIcon(0, icon)
            items[0].setFlags(items[0].flags() & ~Qt.ItemIsDragEnabled)
            parent_item.addChild(items[0])

    # 返回变形器列表
    def list_deformer_hierarchy(self,sel):
        # 获取当前选择的模型
        shape = cmds.ls(sel, dag=True, shapes=True)
        if not shape:
            deform = []
        else:
            # 获取选择的模型形状节点
            obj = shape[0]
            # 获取与模型相关的变形器节点
            deform = cmds.listHistory(obj, pruneDagObjects=True, interestLevel=True)
            deform = cmds.ls(deform, type='geometryFilter')  # 过滤出变形器节点
        return deform

    # 脚本命令
    def job_commend(self):
        self.creat_select_deform_list()

    # 注册选择变化事件的回调函数
    def register_selection_callback(self):
        # 创建回调函数
        jobNum = cmds.scriptJob(e=["SelectionChanged", self.job_commend], protected=True, parent='ZKM_deform_edit_window'+self.time_str)
        # print(cmds.scriptJob(listJobs=True))

    def closeEvent(self, event):
        self.deleteLater()  # 标记窗口为待删除
        # super(Window, self).closeEvent(event)
        print("窗口关闭，脚本清理完毕")

    # 创建记录层级定位器
    def creat_date_loc(self):
        if not cmds.objExists(self.loc_name):
            loc = cmds.spaceLocator(name=self.loc_name)
            cmds.setAttr(loc[0] + '.visibility', 0)
        if not cmds.objExists(self.loc_layer_date_name):
            node = cmds.createNode('choice',n=self.loc_layer_date_name)
            cmds.connectAttr(self.loc_name+'.visibility',node+'.selector')
            cmds.connectAttr(node + '.output', self.loc_name + '.template')
        self.creat_deformer_UI()

    # 重构层级节点并且还原链接
    def rebuild_date_loc(self):
        ls = cmds.ls(self.loc_layer_date_name + '.input[*]')
        connections = []
        if ls:
            connections = cmds.listConnections(self.loc_layer_date_name + '.input[*]', source=True, destination=True)
            # print(connections)
        con_lis = []
        if connections:
            for i in range(len(connections)):
                ls = cmds.ls(connections[i]+'.input1D[*]')
                if ls:
                    con = cmds.listConnections(connections[i]+'.input1D[*]',  p=1)
                    # con = cmds.listConnections('plusMinusAverage2.input1D[*]',  p=1)
                    # print(con)
                else:
                    con = []
                con_lis.append(con)
                    # cmds.disconnectAttr(self.loc_layer_date_name+'.input['+str(i)+']', con[0])
            for i in range(len(connections)):
                if cmds.objExists(connections[i]):
                    cmds.delete(connections[i])
            node = cmds.createNode('choice', n=self.loc_layer_date_name)
            cmds.connectAttr(self.loc_name + '.visibility', node + '.selector')
            for i in range(len(connections)):
                node = cmds.createNode('plusMinusAverage',n=connections[i])
                cmds.connectAttr(self.loc_layer_date_name+'.input['+str(i)+']',connections[i]+'.input3D[0].input3Dx')
                for j in range(len(con_lis[i])):
                    # print(con_lis[i])
                    cmds.connectAttr(con_lis[i][j],node + '.input1D['+str(j)+']')
            cmds.warning('已完全重建分类节点')

    # 创建层级UI
    def creat_deformer_UI(self):
        self.list_widget_3.setHeaderLabel(self.loc_name)
        self.list_widget_3.clear()
        # 创建已有变形器列表
        ls = cmds.ls(self.loc_layer_date_name+'.input[*]')
        connections = []
        if ls:
            connections = cmds.listConnections(self.loc_layer_date_name+'.input[*]', source=True, destination=True)
        # print(connections)
        # 打断所有链接并重新链接
        # print(connections)
        if connections:
            for i in range(len(connections)):
                con = cmds.listConnections(connections[i]+'.input3D[0].input3Dx', c=1, p=1)
                # print(con)
                cmds.disconnectAttr(con[1], con[0])
            for i in range(len(connections)):
                cmds.connectAttr(self.loc_layer_date_name+'.input['+str(i)+']',connections[i]+'.input3D[0].input3Dx')

            for node in connections:
                items = self.create_deformer_button([node], ['plusMinusAverage.svg'], ['plusMinusAverage'], self.list_widget_3)
                for item in items:
                    item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
                    # item.childCount = 0
                child_connections = cmds.listConnections(node+'.input1D', source=True, destination=True)
                # print(child_connections)
                if child_connections:
                    for child_node in child_connections:
                        new_items = self.create_deformer_button([child_node], self.icon_name, self.deform_types, [])
                        items[0].addChild(new_items[0])
                        # new_items[0].childCount = 0
                items[0].setData(0, Qt.UserRole, 'plusMinusAverage')
                items[0].setFlags(items[0].flags() & ~Qt.ItemIsDragEnabled)# ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled
                # print('plusMinusAverage')

    # 移层级
    def move_layer(self,num):
        layer_items = self.list_widget_3.selectedItems()
        if layer_items:
            item = layer_items[0]
            # print(item.text(0))
            data = item.data(0, Qt.UserRole)

            # parent = item.parent()
            # print(parent)
            if data:
                items = []
                for i in range(self.list_widget_3.topLevelItemCount()):
                    items.append(self.list_widget_3.topLevelItem(i))  # 从 0 开始移除并获取项
                # for item in items:
                #     print(item.text(0))
                # 获取移动指针
                dragged_index = 0
                for i in range(0, len(items)):
                    if items[i] == item:
                        dragged_index = i
                target_index = dragged_index+num
                # print(dragged_index)

                if target_index >= 0:
                    items.pop(dragged_index)
                    # 在目标位置插入对象
                    # print(target_index)
                    items.insert(target_index, item)
                    # for item in items:
                    #     print(item.text(0))
                        # self.list_widget_3.addTopLevelItem(item)
                    # 按新顺序添加项
                    for i in range(len(items)):
                        self.list_widget_3.takeTopLevelItem(i)

                    # 按新顺序添加项
                    for i in range(len(items)):
                        # print(items[i].text(0))
                        self.list_widget_3.insertTopLevelItem(i,items[i])
                    self.list_widget_3.setItemSelected(item, True)

                    # 按新顺序重新链接
                    connections = cmds.listConnections(self.loc_layer_date_name+'.input[*]',
                                                       source=True, destination=True)
                    if connections:
                        for i in range(len(connections)):
                            con = cmds.listConnections(connections[i] + '.input3D[0].input3Dx', c=1, p=1)
                            # print(con)
                            cmds.disconnectAttr(self.loc_layer_date_name+'.input[' + str(i) + ']', con[0])
                    for i in range(len(items)):
                        cmds.connectAttr(self.loc_layer_date_name+'.input[' + str(i) + ']',
                                         items[i].text(0) + '.input3D[0].input3Dx')

            else:
                cmds.warning('请选择一个顶组件')
        else:
            cmds.warning('请选择至少一个节点')

    # 创建图片按钮
    def creat_button(self, name, icon, move, scale, lage, icon_lage):
        button = OverlayButton(icon, move, scale)

        if name:
            button.setText(name)
        button.setAutoRaise(True)
        if lage[0]!=0 and lage[1]!=0:
            button.setFixedSize(lage[0], lage[1])
        button.setMaximumSize(999,999)
        # if QtCore.QResource(icon).isValid():
        #     i = QtGui.QIcon(icon)
        #     button.setIcon(i)
        if icon_lage[0]!=0 and icon_lage[1]!=0:
            button.setIconSize(QSize(icon_lage[0], icon_lage[1]))
        return button


    # 添加变形器显示层UI
    # 添加编辑层
    def add_deform_edit_layer(self):
        # 创建加减节点
        sel = cmds.ls(sl=1)
        node = cmds.createNode('plusMinusAverage')
        cmds.select(sel)
        ls = cmds.ls(self.loc_layer_date_name+'.input[*]')
        connections = []
        if ls:
            connections = cmds.listConnections(self.loc_layer_date_name+'.input[*]', source=True, destination=True)
        # print(connections)
        num = '0'
        if connections:
            num = str(len(connections))
        cmds.connectAttr(self.loc_layer_date_name+'.input['+num+']', node + '.input3D[0].input3Dx')
        items = self.create_deformer_button([node], ['plusMinusAverage.svg'], ['plusMinusAverage'], self.list_widget_3)
        for item in items:
            item.setData(0, Qt.UserRole, 'plusMinusAverage')
            # customContextMenuRequested.connect(partial(self.edit_controller, item))
            # cmds.connectAttr('deform_edit_window_locShape.worldPosition[' + str(len(connections)) + '].worldPositionX',
            #                  node + '.input3D[0].input3Dx')

    # 删除变形器显示层UI
    def delete_deform_edit_layer(self):
        items = self.list_widget_3.selectedItems()
        if items:
            for item in reversed(items):
                parent = item.parent()
                if parent:
                    # 如果项目有父项目，则从父项目中移除它
                    index = parent.indexOfChild(item)
                    parent.takeChild(index)
                    item.deleteLater()  # 或者简单地使用 del item（但通常不需要，因为 takeChild 已经断开了连接）
                else:
                    # 如果项目是顶级项目，则从 QTreeWidget 中移除它
                    index = self.list_widget_3.indexOfTopLevelItem(item)
                    self.list_widget_3.takeTopLevelItem(index)
                    # item.deleteLater()  # 清理内存
                cmds.delete(item.text(0))

    # 添加子项
    def add_sub_item(self):
        items = self.list_widget_1.selectedItems()
        item_3 = []
        if items:
            item_1 = items[0].text(0)
            item_3.append(item_1)
        items = self.list_widget_2.selectedItems()
        if items:
            item_2 = items[0].text(0)
            item_3.append(item_2)
        if len(item_3)>1:
            # print(item_3[0])
            if item_3[0]==item_3[1]:
                item_3 = [item_3[0]]
        items = self.list_widget_3.selectedItems()
        text =[]
        if items:
            text = items[0].data(0, Qt.UserRole)
        # print(text)
        # print(item_3)
        # print(items[0].text(0))
        self.add_sub_item2(text,items,item_3)

    # 添加子项提取
    def add_sub_item2(self,text,items,item_3):
        if text:
            if items and item_3:
                ls_list = item_3
                for i in range(items[0].childCount()):
                    child_item = items[0].child(i) # 遍历子项
                    child_item_text = child_item.text(0)
                    if child_item_text in item_3:
                        ls_list.remove(child_item_text)
                new_items = self.create_deformer_button(ls_list, self.icon_name, self.deform_types, [])
                if ls_list:
                    i = 0
                    for item in new_items:
                        items[0].addChild(item)
                        input1D_value = cmds.getAttr(items[0].text(0)+".input1D", multiIndices=True)
                        if not input1D_value:
                            input1D_value = [0]
                        # cmds.connectAttr(item_3[0] + '.envelope', items[0].text(0) + '.input1D['+str(input1D_value[-1]+1) + ']', force=True)
                        cmds.connectAttr(ls_list[i] + '.envelope',
                                         items[0].text(0) + '.input1D[' + str(input1D_value[-1] + 1) + ']', force=True)
                        i=i+1
                else:
                    cmds.warning('都已存在')
        else:
            cmds.warning('请选择父层级')
                    # for item in item_3:
                #     pass
        # if items:
        #     for item in items:
        # # 创建子项
        # sub_item = QTreeWidgetItem(parent_item, [text])
        # # 将子项添加到父项
        # parent_item.addChild(sub_item)
        # # 刷新显示
        # self.update()

    # 删除子项
    def delete_sub_item(self):
        items = self.list_widget_3.selectedItems()
        for item in items:
            parent = item.parent()
            text = item.data(0,Qt.UserRole)
            if not text:
                # print('移除：', item.text(0))
                connections = cmds.listConnections(item.text(0)+'.envelope', p=1, type='plusMinusAverage')
                # connections = cmds.listConnections('blendShape1.envelope', p=1,type='plusMinusAverage')
                if connections:
                    for con in connections:
                        node = con.split('.')[0]
                        # print(node)
                        if node == parent.text(0):
                            cmds.disconnectAttr(item.text(0)+'.envelope', con)
                parent.takeChild(parent.indexOfChild(item))

        # self.creat_deformer_UI()

    # 编辑权重
    def edit_weight(self):
        items = self.list_widget_1.selectedItems()
        if items:
            items = items[0]
            items_parent = items.parent()
            # print(items_parent)
            items = items.text(0)
            if items_parent:
                items_parent_text = items_parent.text(0)
                if cmds.nodeType(items_parent_text) == 'blendShape':
                    node_type = cmds.nodeType(items_parent_text)
                    mel.eval('PaintTextureDeformerWeightsTool;')
                    mel.eval('artSetToolAndSelectAttr( \"artAttrCtx\", \"' + node_type + '.' + items_parent_text + '.baseWeights\" );')
            else:
                if items and cmds.objExists(items):
                    if cmds.nodeType(items) == 'skinCluster':
                        mel.eval('ArtPaintSkinWeightsTool;')
                        selectedItems = [items]
                        # print(selectedItems)
                        self.onSkinClusterSelected(selectedItems)
                    elif cmds.nodeType(items) == 'blendShape':
                        node_type = cmds.nodeType(items)
                        mel.eval('PaintTextureDeformerWeightsTool;')
                        mel.eval('artSetToolAndSelectAttr( \"artAttrCtx\", \"'+node_type+'.'+items+'.baseWeights\" );')
                    else:
                        try:
                            node_type = cmds.nodeType(items)
                            mel.eval('PaintTextureDeformerWeightsTool;')
                            mel.eval('artSetToolAndSelectAttr( \"artAttrCtx\", \"' + node_type + '.' + items + '.weights\" );')
                        except:
                            pass
        else:
            cmds.warning('请在首个大纲选择变形器节点。')

    def updateSkinClusterList(self):
        # 获取所有 skinCluster 节点
        skinClusters = cmds.ls(type="skinCluster") or []

        # 清理并更新列表（用 → 替换层级符号）
        cmds.textScrollList("skinClusterList", edit=True, removeAll=True)
        for sc in skinClusters:
            displayName = sc.replace("|", " → ")  # 处理层级
            cmds.textScrollList("skinClusterList", e=True, append=displayName)

    def onSkinClusterSelected(self,selectedItems):
        # 获取选中的显示名称并还原真实节点名
        # selectedItems = cmds.textScrollList("skinClusterList", q=True, selectItem=True) or []
        # selectedItems = self.list_widget_1.selectedItems()
        if not selectedItems:
            return

        selectedDisplay = selectedItems[0]
        realSkinCluster = selectedDisplay.replace(" → ", "|")

        # 确保节点存在
        if not cmds.objExists(realSkinCluster):
            cmds.warning(f"SkinCluster {realSkinCluster} no longer exists!")
            self.updateSkinClusterList()
            return

        # 更新关节菜单
        try:
            skinUpdater.scw.artAttrSkinJointMenuCallBack([realSkinCluster])
        except:
            pass  # 防止旧版 Maya 兼容问题

        # 触发影响列表更新（模拟原生行为）
        influences = cmds.skinCluster(realSkinCluster, q=True, influence=True)
        for jnt in influences:
            mel.eval('artSkinInflListChanging \"' + jnt + '\" 0;')
            mel.eval('artSkinInflListChanging \"' + jnt + '\" 1;')
            # cmds.artSkinInflListChanging(jnt, 0)
            # cmds.artSkinInflListChanging(jnt, 1)
        # print(influences[0])
        mel.eval('artSkinInflListChanging \"' + influences[0] + '\" 1;''artSkinInflListChanged artAttrSkinPaintCtx;refreshAE;')
        # cmds.artSkinInflListChanged("artAttrSkinPaintCtx")
        # mel.eval('refreshAE;')  # 刷新属性编辑器

    # 复制权重（只有选择两个对象才显示）
    def duplicate_weight(self):
        sel = cmds.ls(sl=1)
        item_3 = []
        items = self.list_widget_1.selectedItems()
        item_1 = []
        items_parent=[]
        if items:
            item_1 = items[0].text(0)
            item_3.append(item_1)
            items_parent = items[0].parent()
        # print(items_parent)
        parent_is_bs_1 = False
        if items_parent:
            items_parent_text = items_parent.text(0)
            if cmds.nodeType(items_parent_text) == 'blendShape':
                parent_is_bs_1 = True
        items = self.list_widget_2.selectedItems()
        item_2 = []
        items_parent = []
        if items:
            item_2 = items[0].text(0)
            item_3.append(item_2)
            items_parent = items[0].parent()
        # print(items_parent)
        parent_is_bs_2 = False
        if items_parent:
            items_parent_text = items_parent.text(0)
            if cmds.nodeType(items_parent_text) == 'blendShape':
                parent_is_bs_2 = True
        # items = self.list_widget_3.selectedItems()
        # text = items[0].data(0, Qt.UserRole)
        bs_sk = 0
        # print(bs_sk)
        item_1_type = []
        item_2_type = []
        if item_1:
            if cmds.objExists(item_1):
                item_1_type = cmds.nodeType(item_1)
        if item_2:
            if cmds.objExists(item_2):
                item_2_type = cmds.nodeType(item_2)
        if item_1 and item_2 :
            # print(item_1,item_2)
            bs_sk = 1
            if item_1_type == 'skinCluster' and item_2_type == item_1_type:
                # 都是蒙皮则默认复制权重
                print('复制蒙皮权重')
                # print(self.obj_1, self.obj_2, item_1, [item_2])
                self.weight.new_maya_base_copy_joint_weight('Normal', self.obj_1, [self.obj_2], item_1, [item_2], '', '')
            elif (item_1_type == 'skinCluster' or item_2_type == 'skinCluster') and item_1_type != item_2_type:
                cmds.warning('蒙皮蔟不可和其他变形器权重公用。')
            else:
                if parent_is_bs_1 == True or parent_is_bs_2 == True or item_1_type == 'blendShape' or item_2_type == 'blendShape':
                    cmds.warning('bs无法转移')
        if bs_sk == 0:
            if item_1 and not item_2 and bs_sk == 0 and item_1_type != 'skinCluster' and item_1_type != 'blendShape' and parent_is_bs_1 == False:
                # 既不是bs也不是蒙皮的情况
                # 自带复制权重sets -fe cluster6Set pCube2.vtx[0:7] ;
                print('默认通用变形器权重')
                # set = cmds.listConnections(item_1+'.message', d=True,type='objectSet')
                set = cmds.deformer(item_1, q=1, cmp=1)
                # print(set)
                # set_members = cmds.sets('cluster6Set', query=True)
                # print(self.obj_2)
                # print(type(self.obj_2))
                if type(self.obj_2) == list:
                    # cmds.sets(self.obj_2, fe=set[0])
                    cmds.deformer(item_1,e=1, geometry = self.obj_2)
                    obj = self.obj_2[0].split('.')[0]
                    # print(obj)
                    cmds.copyDeformerWeights(ss=self.obj_1, sd=item_1, nm=1, ds=obj, dd=item_1,surfaceAssociation='closestPoint', )
                else:
                    add_set = cmds.ls(self.obj_2+'.vtx[*]')
                    # cmds.sets(add_set, fe=set[0])
                    cmds.deformer(item_1, e=1, geometry=add_set)
                    cmds.copyDeformerWeights(ss=self.obj_1, sd=item_1, nm=1, ds=self.obj_2, dd=item_1,surfaceAssociation='closestPoint', )
                cmds.select(sel)
            else:
                if item_1_type == 'blendShape' or parent_is_bs_1 == True:
                    cmds.warning('bs无法转移')
                else:
                    cmds.warning('可能是暂未记录（请无视）')


    # 复制权重(不同转移)
    def copy_weight(self):
        sel = cmds.ls(sl=1)
        item_3 = []
        items = self.list_widget_1.selectedItems()
        item_1 = []
        items_parent_1=[]
        if items:
            item_1 = items[0].text(0)
            item_3.append(item_1)
            items_parent_1 = items[0].parent()
        # print(items_parent)
        parent_is_bs_1 = False
        items_parent_text_1 = ''
        if items_parent_1:
            items_parent_text_1 = items_parent_1.text(0)
            if cmds.nodeType(items_parent_text_1) == 'blendShape':
                parent_is_bs_1 = True
        items = self.list_widget_2.selectedItems()
        item_2 = []
        items_parent_2 = []
        if items:
            item_2 = items[0].text(0)
            item_3.append(item_2)
            items_parent_2 = items[0].parent()
        # print(items_parent)
        parent_is_bs_2 = False
        items_parent_text_2 = ''
        if items_parent_2:
            items_parent_text_2 = items_parent_2.text(0)
            if cmds.nodeType(items_parent_text_2) == 'blendShape':
                parent_is_bs_2 = True
        # items = self.list_widget_3.selectedItems()
        # text = items[0].data(0, Qt.UserRole)
        self.copy_weight_commend(item_1,item_2,parent_is_bs_1,parent_is_bs_2,self.obj_1,self.obj_2,items_parent_text_1,items_parent_text_2)
        cmds.select(sel)

    # 复制权重(不同转移)
    def copy_weight_commend(self,item_1,item_2,parent_is_bs_1,parent_is_bs_2,obj_1,obj_2,items_parent_text_1,items_parent_text_2):
        if item_1 and item_2 and item_1 != item_2:
            item_1_type = []
            item_2_type = []
            if cmds.objExists(item_1):
                item_1_type = cmds.nodeType(item_1)
            if cmds.objExists(item_2):
                item_2_type = cmds.nodeType(item_2)
            if item_1_type == 'skinCluster' and item_2_type == item_1_type:
                # 都是蒙皮则默认复制权重
                print('复制蒙皮权重')
                # print(self.obj_1, self.obj_2, item_1, [item_2])
                # print(item_1, item_2)
                cmds.copySkinWeights(ss=item_1, ds=item_2, noMirror=1, surfaceAssociation='closestPoint')
            elif (item_1_type == 'skinCluster' or item_2_type == 'skinCluster') and item_1_type != item_2_type:
                cmds.warning('蒙皮蔟不可和其他变形器权重公用。')
            else:

                if parent_is_bs_1 == True or parent_is_bs_2 == True or item_1_type == 'blendShape' or item_2_type == 'blendShape':
                    if parent_is_bs_1 == True:
                        print('获取bs权重')
                        weight_list, bs_list = self.read_weight(obj_1, items_parent_text_1, 'bs.'+item_1)
                        # print(weight_list, bs_list)
                    else:
                        if cmds.nodeType(item_1) == 'blendShape':
                            print('获取初始bs变形器权重')
                            # print(self.obj_1, item_1, 'bs.'+item_1)
                            weight_list, bs_list = self.read_weight(obj_1, item_1, item_1)

                        else:
                            print('获取初始变形器权重')
                            # print(self.obj_1, item_1, 'bs.'+item_1)
                            weight_list, bs_list = self.read_weight(obj_1, item_1, [])
                            # print(weight_list, bs_list)

                    # 选择变形器权重
                    if parent_is_bs_2 == True:
                        print('设置bs权重')
                        cluster = self.create_skin(obj_1, weight_list, 'copy')
                        self.set_deform_weight(obj_1, obj_2, items_parent_text_2, cluster, item_2, 1)
                    else:
                        if cmds.nodeType(item_2) == 'blendShape':
                            # if self.obj_1 != self.obj_2:
                            print('设置bs变形器权重')
                            cluster = self.create_skin(obj_1, weight_list, 'copy')
                            self.set_deform_weight(obj_1, obj_2, item_2, cluster, [], 1)
                        else:
                            print('设置变形器权重')
                            cluster = self.create_skin(obj_1, weight_list, 'copy')
                            self.set_deform_weight(obj_1, obj_2, item_2, cluster, [], 2)

                else:
                    # 既不是bs也不是蒙皮的情况
                    # 自带复制权重
                    print('默认通用变形器权重')
                    # print(self.obj_1, self.obj_2, item_1, [item_2])

                    if obj_1 != obj_2:
                        if type(obj_2) == list:
                            # cmds.sets(self.obj_2, fe=set[0])
                            cmds.deformer(item_1, e=1, geometry=obj_2)
                            obj = obj_2[0].split('.')[0]

                            weight_list, bs_list = self.read_weight(obj_1, item_1, [])
                            weight_list_old, bs_list_old = self.read_weight(obj, item_2, [])

                            need_keep_point = []
                            for i in range(len(obj_2)):
                                num = int(obj_2[i].split('[')[-1][:-1])
                                need_keep_point.append(num)
                                weight_list[num] = weight_list_old[num]

                            cluster = self.create_skin(obj_1, weight_list, 'copy')
                            self.set_deform_weight(obj_1, obj, item_2, cluster, [], 2)

                            # cmds.copyDeformerWeights(ss=self.obj_1, sd=item_1, nm=1, ds=obj, dd=item_2,
                            #                          surfaceAssociation='closestPoint')
                        else:
                            cmds.copyDeformerWeights(ss=obj_1, sd=item_1, nm=1, ds=obj_2, dd=item_2,surfaceAssociation='closestPoint')
                    else:
                        # set = cmds.listConnections(item_1 + '.message', d=True, type='objectSet')
                        # set_obj = cmds.sets(set, q=True)

                        # print(set_obj)
                        # set = cmds.listConnections('blendShape4.message', d=True, type='objectSet')
                        # set_obj = cmds.sets(set, q=True)
                        # print(set_obj)
                        obj = cmds.duplicate(obj_1)
                        # print(obj)
                        add_set = cmds.ls(obj[0] + '.vtx[*]')
                        # cmds.sets(add_set, fe=set[0])
                        cmds.deformer(item_1, e=1, geometry=add_set)
                        cmds.copyDeformerWeights(ss=obj_1, sd=item_1, nm=1, ds=obj[0], dd=item_1,surfaceAssociation='closestPoint')
                        cmds.copyDeformerWeights(ss=obj[0], sd=item_1, nm=1, ds=obj_1, dd=item_2,surfaceAssociation='closestPoint')
                        cmds.delete(obj)
        else:
            cmds.warning('不能复制同一个变形器权重。')

            # print(cmds.percent('blendSha                              pe3', 'pCube1', q=1, v=1))
        # print(cmds.percent('cluster1', 'pCube2', q=1, v=1))

    # 镜像指定变形器权重
    def mirror_deformer_weight(self):
        sel = cmds.ls(sl=1,fl=1)
        items = self.list_widget_1.selectedItems()
        item_1 = ''
        items_parent = []
        if items:
            item_1 = items[0].text(0)
            items_parent = items[0].parent()
        # print(items_parent)
        parent_is_bs_1 = False
        items_parent_text = []
        if items_parent:
            items_parent_text = items_parent.text(0)
            if cmds.nodeType(items_parent_text) == 'blendShape':
                parent_is_bs_1 = True
        item_1_type = []
        if item_1:
            if cmds.objExists(item_1):
                item_1_type = cmds.nodeType(item_1)
        sel_obj = []
        if len(sel[0].split('|'))>1:
            sel_obj = sel[0].split('|')[0]
        num = self.comboBox_2.currentIndex()
        # print(num)
        list = [['YZ',True],['YZ',False],['XZ',True],['XZ',False],['XY',True],['XY',False]]
        direction = list[num]

        if item_1:
            if item_1_type == 'skinCluster':
                cmds.copySkinWeights(ss=item_1, surfaceAssociation='closestPoint', influenceAssociation='closestJoint', ds=item_1, mirrorMode=direction[0],mirrorInverse = direction[1])
            elif item_1_type == 'blendShape':
                if sel_obj:
                    obj = sel_obj
                else:
                    obj = sel[0]
                weight_list, bs_list = self.read_weight(obj, item_1, item_1)
                cluster = self.create_skin(self.obj_1, weight_list, ['mirror',direction[0],direction[1]])
                self.set_deform_weight(self.obj_1, self.obj_1, item_1, cluster, [], 1)
            elif parent_is_bs_1 == True:
                if sel_obj:
                    obj = sel_obj
                else:
                    obj = sel[0]
                # print(obj)
                weight_list, bs_list = self.read_weight(obj, items_parent_text, 'bs.'+item_1)
                cluster = self.create_skin(self.obj_1, weight_list, ['mirror',direction[0],direction[1]])
                self.set_deform_weight(self.obj_1, self.obj_1, items_parent_text, cluster, items_parent_text, 1)
            else:
                cmds.copyDeformerWeights(ss=self.obj_1, ds=self.obj_1, sd=item_1, mirrorMode=direction[0], mirrorInverse = direction[1],surfaceAssociation='closestPoint')

    # 反转指定变形器权重
    def reversal_deformer_weight(self):
        sel = cmds.ls(sl=1,fl=1)
        items = self.list_widget_1.selectedItems()
        item_1 = ''
        items_parent = []
        if items:
            item_1 = items[0].text(0)
            items_parent = items[0].parent()
        # print(items_parent)
        parent_is_bs_1 = False
        items_parent_text = ''
        if items_parent:
            items_parent_text = items_parent.text(0)
            if cmds.nodeType(items_parent_text) == 'blendShape':
                parent_is_bs_1 = True
        item_1_type = []
        if item_1:
            if cmds.objExists(item_1):
                item_1_type = cmds.nodeType(item_1)
        sel_obj = []
        if len(sel[0].split('|'))>1:
            sel_obj = sel[0].split('|')[0]
        if sel_obj:
            obj = sel_obj
        else:
            obj = sel[0]
        if item_1:
            if item_1_type == 'skinCluster':
                cmds.warning('skinCluster不能反转')
            elif item_1_type == 'blendShape':
                weight_list, bs_list = self.read_weight(obj, item_1, item_1)
                cluster = self.create_skin(self.obj_1, weight_list, ['reversal'])
                self.set_deform_weight(self.obj_1, self.obj_1, item_1, cluster, [], 1)
            elif parent_is_bs_1 == True:
                weight_list, bs_list = self.read_weight(obj, items_parent_text, 'bs.'+item_1)
                cluster = self.create_skin(self.obj_1, weight_list, ['reversal'])
                self.set_deform_weight(self.obj_1, self.obj_1, items_parent_text, cluster, items_parent_text, 1)
            else:
                weight_list, bs_list = self.read_weight(obj, item_1, [])
                cluster = self.create_skin(self.obj_1, weight_list, ['reversal'])
                self.set_deform_weight(self.obj_1, self.obj_1, item_1, cluster, item_1, 2)

    # 设置为软选择权重
    def set_soft_weight(self):
        # 创建一个 MRichSelection 对象
        rich_sel = om.MGlobal.getRichSelection(0)

        # 获取软选择列表
        soft_sel = rich_sel.getSelection()

        # 遍历软选择中的元素并获取权重
        iter = om.MItSelectionList(soft_sel, om.MFn.kMeshVertComponent)
        while not iter.isDone():
            # print('aaa')
            sel = cmds.ls(sl=1, fl=1)
            items = self.list_widget_1.selectedItems()
            item_1 = ''
            items_parent = []
            if items:
                item_1 = items[0].text(0)
                items_parent = items[0].parent()
            # print(items_parent)
            parent_is_bs_1 = False
            items_parent_text = ''
            if items_parent:
                items_parent_text = items_parent.text(0)
                if cmds.nodeType(items_parent_text) == 'blendShape':
                    parent_is_bs_1 = True
            item_1_type = []
            if item_1:
                if cmds.objExists(item_1):
                    item_1_type = cmds.nodeType(item_1)
            sel_obj = []
            if len(sel[0].split('|')) > 1:
                sel_obj = sel[0].split('|')[0]
            if sel_obj:
                obj = sel_obj
            else:
                obj = sel[0]
            if item_1:
                self.obj_1 = self.obj_1[0].split('.')[0]
                list = cmds.ls(self.obj_1 + '.vtx[*]', fl=1)
                # print(list)
                weight_list = []
                for i in list:
                    weight_list.append(0)
                # 苍之幻灵（太久没写api了，复习一下，顺便改点直接用了）
                # 创建一个 MRichSelection 对象
                rich_sel = om.MGlobal.getRichSelection(0)

                # 获取软选择列表
                soft_sel = rich_sel.getSelection()

                # 遍历软选择中的元素并获取权重
                iter = om.MItSelectionList(soft_sel, om.MFn.kMeshVertComponent)
                while not iter.isDone():
                    dag_path, component = iter.getComponent()
                    # print(dag_path.fullPathName())
                    mesh_fn = om.MFnMesh(dag_path)

                    # 创建一个 MFnSingleIndexedComponent 对象, 用于操作组件
                    mfn_component = om.MFnSingleIndexedComponent(component)
                    # 获取每个组件的id
                    elements = mfn_component.getElements()
                    for i in range(len(elements)):
                        # 获取每个组件的权重
                        weight = mfn_component.weight(i).influence
                        # print("Vertex Index: {}, Weight: {}".format(elements[i], weight))
                        # print(elements[i])
                        weight_list[elements[i]]= weight
                        # cmds.setAttr(cluster[0] + '.weightList[0].weights[' + elements[i] + ']', weight)
                    iter.next()

                if item_1_type == 'skinCluster':
                    cmds.warning('skinCluster不能反转')
                elif item_1_type == 'blendShape':
                    # weight_list, bs_list = self.read_weight(obj, item_1, item_1)
                    cluster = self.create_skin(self.obj_1, weight_list, ['copy'])
                    self.set_deform_weight(self.obj_1, self.obj_1, item_1, cluster, [], 1)
                elif parent_is_bs_1 == True:
                    # weight_list, bs_list = self.read_weight(obj, items_parent_text, 'bs.' + item_1)
                    cluster = self.create_skin(self.obj_1, weight_list, ['copy'])
                    self.set_deform_weight(self.obj_1, self.obj_1, items_parent_text, cluster, items_parent_text, 1)
                else:
                    # weight_list, bs_list = self.read_weight(obj, item_1, [])
                    cluster = self.create_skin(self.obj_1, weight_list, ['copy'])
                    # print(self.obj_1)
                    self.set_deform_weight(self.obj_1, self.obj_1, item_1, cluster, item_1, 2)
            iter.next()


    # 读取变形器黑白权重
    def read_weight(self,obj,deform,bs_name):
        if bs_name:
            weight_list = []
            # 获取bs选集
            # set = cmds.listConnections(deform + '.message', d=True, type='objectSet')
            # set_obj = cmds.ls(cmds.sets(set, q=True),fl=1)

            point = cmds.ls(obj+'.vtx[*]',fl=1)
            # # 获取模型对象在选集列表中的位置
            # obj_point_in_set = []
            # for i in range(len(set_obj)):
            #     set_obj = set_obj[i].split('.')[0]
            #     if obj == set_obj:
            #         obj_point_in_set.append(i)
            # 获取bs所含的模型列表
            an_list = cmds.ls(deform+'.originalGeometry[*]')
            # print('aaaa',an_list)
            mesh_list = cmds.listConnections(an_list, d=True, s=True)
            # print(mesh_list)
            mesh_ind = 0
            for i in range(len(mesh_list)):
                if obj == mesh_list[i]:
                    mesh_ind = i
            # 判断是节点还是属性
            node = bs_name.split('.')
            # 当是属性的情况下查询属性指针
            bs_ind = 0
            if len(node) > 1:
                targets = cmds.ls(deform + '.inputTarget['+str(mesh_ind)+'].inputTargetGroup[*]')
                for target in targets:
                    target = target.split('[')[-1][:-1]
                    # print(target)
                    name = cmds.aliasAttr(deform + '.w[' + target + ']', q=1)
                    if name == node[-1]:
                        bs_ind = target
                        break
            # 开始获取权重
            for i in range(len(point)):
                if bs_ind:
                    an = cmds.ls(deform+'.inputTarget['+str(mesh_ind)+'].inputTargetGroup['+str(bs_ind)+'].targetWeights['+str(i)+']')
                else:
                    an = cmds.ls(deform + '.inputTarget['+str(mesh_ind)+'].baseWeights[' + str(i) + ']')
                weight = cmds.getAttr(an)
                weight_list.append(weight)
            return weight_list, [mesh_ind, bs_ind]
        else:
            weight_list = cmds.percent(deform, obj, q=1, v=1)
            return weight_list, []

    # 给黑白权重创建一个蔟处理好权重并返需要的权重列表
    def create_skin(self, obj, base_weight, process_type):
        weight = []
        # 创建蔟
        # print(obj)
        cluster = cmds.cluster(obj)
        if process_type[0] == 'copy':
            for i in range(len(base_weight)):
                cmds.setAttr(cluster[0] + '.weightList[0].weights[' + str(i) + ']', base_weight[i])
        else:
            for i in range(len(base_weight)):
                cmds.setAttr(cluster[0] + '.weightList[0].weights[' + str(i) + ']', base_weight[i])
            if process_type[0] == 'mirror':
                # print(cluster)
                # for mirror in ['YZ','XZ', 'XY']
                cmds.copyDeformerWeights(ss=obj, ds=obj, sd=cluster[0], mirrorMode=process_type[1], mirrorInverse = process_type[2],surfaceAssociation='closestPoint')
                for i in range(len(base_weight)):
                    num = cmds.getAttr(cluster[0] + '.weightList[0].weights['+str(i)+']')
                    weight.append(num)
            if process_type[0] == 'reversal':
                for i in range(len(base_weight)):
                    num = 1 - base_weight[i]
                    weight.append(num)
                for i in range(len(weight)):
                    cmds.setAttr(cluster[0] + '.weightList[0].weights[' + str(i) + ']', weight[i])
        return cluster


    # 设置指定变形器权重
    def set_deform_weight(self, obj, tag_obj, deform, cluster, bs_an, other_deform):
        # print(obj, tag_obj, deform, cluster, bs_list, other_deform)
        if other_deform == 0:
            cmds.copyDeformerWeights(ss=obj, sd=cluster[0], nm=1, ds=tag_obj, dd=deform,surfaceAssociation='closestPoint')
        if other_deform == 1:
            # 再创建一个簇进行拷贝后重学读取赋予权重
            mesh = cmds.duplicate(tag_obj)
            cluster_tag = cmds.cluster(mesh)
            # print(obj, cluster[0], mesh, cluster_tag)
            cmds.copyDeformerWeights(ss=obj, sd=cluster[0], nm=1, ds=mesh[0], dd=cluster_tag[0],surfaceAssociation='closestPoint')
            weight_list = cmds.percent(cluster_tag[0], mesh, q=1, v=1)

            # 获取bs所含的模型列表
            an_list = cmds.ls(deform + '.originalGeometry[*]')
            # print(deform)
            # print(an_list)
            # print('aaaa',an_list)
            mesh_list = cmds.listConnections(an_list, d=True, s=True)
            mesh_ind = 0
            # print(mesh_list)
            for i in range(len(mesh_list)):
                if obj == mesh_list[i]:
                    mesh_ind = i

            # 当是属性的情况下查询属性指针
            bs_ind = 0
            if bs_an:
                targets = cmds.ls(deform + '.inputTarget[' + str(mesh_ind) + '].inputTargetGroup[*]')
                for target in targets:
                    target = target.split('[')[-1][:-1]
                    # print(target)
                    name = cmds.aliasAttr(deform + '.w[' + target + ']', q=1)
                    if name == bs_an:
                        bs_ind = target
                        break

            for i in range(len(weight_list)):
                if bs_an:
                    cmds.setAttr(deform +'.inputTarget[' + str(mesh_ind) + '].inputTargetGroup[' + str(bs_ind) + '].targetWeights[' + str(i) + ']', weight_list[i])
                else:
                    cmds.setAttr(deform + '.inputTarget['+str(mesh_ind)+'].baseWeights[' + str(i) + ']', weight_list[i])
            cmds.delete(cluster_tag,mesh)

        else:
            if other_deform == 2:
            # 再创建一个簇进行拷贝后重学读取赋予权重
                mesh = cmds.duplicate(tag_obj)
                cluster_tag = cmds.cluster(mesh)
                # print(obj, cluster[0], mesh, cluster_tag)
                cmds.copyDeformerWeights(ss=obj, sd=cluster[0], nm=1, ds=mesh[0], dd=cluster_tag[0],surfaceAssociation='closestPoint')

                cmds.copyDeformerWeights(ss=mesh[0], sd=cluster_tag[0], nm=1, ds=tag_obj, dd=deform,surfaceAssociation='closestPoint')
                cmds.delete(cluster_tag, mesh)

        cmds.delete(cluster)



    # 改bs名称
    def rename_blendshape_deformation(self,name_1,name_2,name_3,num_indicator,deform_name):
        targets = cmds.ls(deform_name + '.inputTarget[0].inputTargetGroup[*]')
        # print(targets)
        # print(cmds.aliasAttr(parent_item.text(0)+'.w[0]', q=1))
        blendshape_targets = cmds.listAttr(deform_name + '.w', m=True)
        for i in range(len(blendshape_targets)):
            if not name_2:
                name_2 = blendshape_targets[i]
            text = ''
            if num_indicator == 0:
                text = str(i) + name_1 + name_2 + name_3
            if num_indicator == 1:
                text = name_1 + str(i) + name_2 + name_3
            if num_indicator == 2:
                text = name_1 + name_2 + str(i) + name_3
            if num_indicator == 3:
                text = name_1 + name_2 + name_3 + str(i)
            for target in targets:
                target = target.split('[')[-1][:-1]
                # print(target)
                name = cmds.aliasAttr(deform_name + '.w[' + target + ']', q=1)
                if name == blendshape_targets[i]:
                    cmds.aliasAttr(text, deform_name + '.w[' + str(i) + ']')

    # 导出权重
    def export_deform_weight(self,Model,deform_name):
        # 查询当前Maya安装路径
        MAYA_VERSION = cmds.about(version=True)[:4]
        # MayaPath = os.environ['HOME'] + "/maya/" + MAYA_VERSION
        # 查询并建立临时文件夹
        try:
            wight_file_path = cmds.iconTextButton('MayaWindow_menu_Process_formLayout1_AddButton', q=1, ann=1)
            print(wight_file_path)
            path = wight_file_path + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder_2'
        except:
            path = file_path + '\scratch_file\MayaWeightExportImportWeightProvisionalFolder_2'
        path_split = path.split('\\')
        MayaPath = path_split[0]
        for i in range(1, len(path_split)):
            MayaPath = MayaPath + '/' + path_split[i]
        # if not os.path.exists(path):
        #     os.makedirs(path)
        # 清理与即将生成的文件重名的文件
        # print (MayaPath + '/scratch_file/MayaWeightExportImportWeightProvisionalFolder')
        if any(name.endswith(('.xml')) for name in
               os.listdir(path + '\\')):
            my_path = (path + '\\')
            for file_name in os.listdir(my_path):
                if file_name.endswith('.xml'):
                    os.remove(my_path + file_name)
                if file_name.endswith('.txt'):
                    os.remove(my_path + file_name)
        # 按名字创建文本
        for MD in Model:
            SkinCluster = mel.eval('findRelatedSkinCluster ' + MD + ';')
            if not SkinCluster:
                break
        for MD in Model:
            SkinCluster = mel.eval('findRelatedSkinCluster ' + MD + ';')
            if SkinCluster:
                Joint = cmds.skinCluster(MD, q=1, inf=1)
                file = open((path + '\\' + MD + '.txt'), "w")
                for Jon in Joint:
                    file.write(Jon + '\n')
                file.close()
                mel.eval(
                    'deformerWeights -export -deformer \"' + SkinCluster + '\" -path \"' + MayaPath + '/' + '\" \"' + MD + '.xml\";')
        print('\n如果要查询，下面是路径：' + '\n' + str(path) + '\n')
    # button.customContextMenuRequested.connect(partial(self.edit_controller, button))

    # 添加到选择组
    def add_to_selection_grp(self):
        sel = cmds.ls(sl=1)
        layer_items = self.list_widget_3.selectedItems()
        manage_text = self.comboBox_1.currentText()
        print(manage_text)
        type_text = self.comboBox_3.currentText()
        print(type_text)
        if layer_items:
            item = layer_items[0]
            # print(item.text(0))
            data = item.data(0, Qt.UserRole)
            if data:
                layer_items_text = layer_items[0].text(0)
                print(layer_items_text)
                all_deform = []
                for s in sel:
                    deform = self.list_deformer_hierarchy(s)
                    all_deform = all_deform + deform
                all_deform = list(set(all_deform))
                print(all_deform)
                # all_deform_type = self.deform_types + self.deform_types_1
                # print(all_deform_type)
                out_deform = []
                if type_text == 'all':
                    out_deform = all_deform
                else:
                    for deform in all_deform:
                        type = cmds.nodeType(deform, inherited=True)
                        # if type in self.deform_types:
                        #     pass
                        if 'nonLinear' in type:
                            # for name_1, deform_type_1 in zip(self.icon_name_1, self.deform_types_1):
                            connected_node = cmds.listConnections(deform + '.matrix', source=True)
                            shape_nodes = cmds.listRelatives(connected_node, shapes=True)
                            type = cmds.nodeType(shape_nodes[0], inherited=True)
                            # print('type:',type)
                        if type_text in type:
                            out_deform.append(deform)
                        # print('type:', type)
                    # for deform_type in all_deform_type:
                    #     if type_text in deform_type:
                    #         pass
                # print(out_deform)
                set_deform = []
                if manage_text == '将当前选择物体变形器的':
                    set_deform = out_deform

                if manage_text == '将当前选择物体变形器不在组内的':
                    set_deform = [x for x in all_deform if x not in out_deform]

                if manage_text == '将当前选择物体变形器没有加到任意组内的':
                    # set_deform = [x for x in all_deform if x not in out_deform]
                    # 获取所有子集
                    # 从隐藏的根节点开始遍历（包括所有顶层项）
                    root = self.list_widget_3.invisibleRootItem()
                    self.child_items = []
                    for i in range(root.childCount()):
                        top_level_item = root.child(i)
                        for i in range(top_level_item.childCount()):
                            child = top_level_item.child(i)
                            self.child_items.append(child)
                    items_text = []
                    for item in self.child_items:
                        items_text.append(item.text(0))
                    items_text = list(set(items_text))
                    # print(items_text)
                    # print(out_deform)
                    set_deform = [x for x in out_deform if x not in items_text]
                # print(set_deform)
                # for deform in set_deform:
                self.add_sub_item2(True, layer_items, set_deform)
            else:
                cmds.warning('请选择一个组')
        else:
            cmds.warning('请选择一个组')

    # 定义一个递归函数来遍历子项
    def recurse(self,item):
        # 将当前项添加到列表
        self.child_items.append(item)
        # 遍历当前项的所有子项
        for i in range(item.childCount()):
            child = item.child(i)
            self.recurse(child)

    # 导入纯权重数据
    def import_weight_data(self):
        print('导入数据')
        data = self.select_weight_file()
        mel.eval('TranslateToolWithSnapMarkingMenu;')
        """显示文件基本信息"""
        if not data:
            return

        dragged_items = self.list_widget_1.selectedItems()
        # print(dragged_items)
        dragged_items_text = ''
        if dragged_items:
            dragged_items_text = dragged_items[0].text(0)
        # print('变形器:', dragged_items_text)
        deformer_type = cmds.nodeType(dragged_items_text)

        deform_type = data["deform"]
        weight_data = data['data']
        # print(deform_type)
        # print(mesh_data)

        mesh = self.list_widget_1.headerItem().text(0)

        if not (deformer_type == 'skinCluster') == (deform_type == 'skinCluster'):
            cmds.warning('变形器类型有蒙皮和其他两种，两种不能互相导入。(可以继续)')
            return

        if deform_type == 'skinCluster':
            print('导入蒙皮数据')
            need_joint = weight_data['joint_data']
            # print(need_joint)
            have_joint = cmds.skinCluster(dragged_items_text, q=True, influence=True)
            # print(have_joint)

            joint = [j for j in have_joint if j not in need_joint]
            # print('移除骨骼:',joint)
            if joint:
                for j in joint:
                    cmds.skinCluster(dragged_items_text, edit=True, removeInfluence=j)

            joint = [j for j in need_joint if j not in have_joint]
            # print('添加骨骼:',joint)
            if joint:
                for j in joint:
                    cmds.skinCluster(dragged_items_text, e=1, ai=j, wt=0)

            # 添加完成再次获取骨骼指针
            joint = cmds.skinCluster(dragged_items_text, q=True, influence=True)

            joint_index_list = [joint.index(item) for item in need_joint]
            # print(joint_index_list)
            influence_indices = om.MIntArray(joint_index_list)  # 骨骼索引


            vertex_indices_list = self.get_all_vertex_indices(mesh)
            vertex_indices = om.MIntArray(vertex_indices_list)

            weight = [item for sublist in weight_data['weights'] for item in sublist]
            weights_data = om.MDoubleArray(weight)

            # print(dragged_items_text)
            # print(influence_indices)
            # print(weights_data)
            # print(vertex_indices)

            self.set_skin_weights_api(dragged_items_text, influence_indices, weights_data, vertex_indices)
        else:
            try:
                print('导入统一数据')
                all_vertices = cmds.ls(f'{mesh}.vtx[*]', flatten=True)
                # 使用列表批量操作，效率更高（推荐）
                for vtx, weight in zip(all_vertices, weight_data):
                    cmds.percent(dragged_items_text, vtx, value=weight)
            except Exception as e:
                print(f"发生错误: {e}")
                # 获取错误类型和详细信息
                error_type = type(e).__name__
                error_msg = str(e)
                print(f"错误类型: {error_type}, 错误信息: {error_msg}")


    # 导出纯权重数据
    def output_weight_data(self):
        print('导出数据')
        # 读取数据获取来源：[maya,2024.0]
        major = cmds.about(version=True)
        minor = cmds.about(minorVersion=True)
        maya_version = f"{major}.{minor}"
        # print(maya_version)  # 输出例如：2024.2
        deta_source = ['maya', maya_version]
        print('数据来源:', deta_source)

        mesh = self.list_widget_1.headerItem().text(0)
        print('模型:',mesh)

        dragged_items = self.list_widget_1.selectedItems()
        # print(dragged_items)
        dragged_items_text = ''
        if dragged_items:
            dragged_items_text = dragged_items[0].text(0)
        print('变形器:',dragged_items_text)

        deformer_type = cmds.nodeType(dragged_items_text)
        result = {
            'deform': deformer_type,
            'data': [],
        }

        if deformer_type == 'skinCluster':
            skin_joint = cmds.skinCluster(dragged_items_text, q=1, inf=1) or []

            # 获取权重数据
            all_weight = []
            mesh_vtx_list = cmds.ls(mesh + '.vtx[*]', fl=1)
            for vtx in mesh_vtx_list:
                weight = cmds.skinPercent(dragged_items_text, vtx, q=True, v=True)
                # 确保权重数据是基本Python类型[5](@ref)
                all_weight.append([float(w) for w in weight])
            result['data']={
                'joint_data': skin_joint,
                'weights': all_weight,
            }
            self.create_base_weight_json_file(deformer_type, result)
        else:
            weights = self.get_deformer_weights(dragged_items_text, mesh)
            result['data'] = weights
            self.create_base_weight_json_file(deformer_type, result)

        print(result)

    # 导出纯权重数据json文件
    def create_base_weight_json_file(self, deformer_type,data):
        all_selected = cmds.ls(selection=True)
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                       self.controller_file_path + '\\scratch_file\\weight_data')
        if not folder_path:  # 用户取消了选择
            cmds.warning("您已取消了选择")
            return

        # 替换文件名中不允许的字符
        clean_name = re.sub(r'[<>:"/\\|?*]', '_', deformer_type)

        # 获取当前时间的毫秒级时间戳
        milliseconds = int(time.time() * 1000)

        # 构建完整的文件路径
        filename = f"{clean_name}_{milliseconds}.json"
        full_path = folder_path + '/' + filename

        # print(f"保存路径: {full_path}")

        # 调用导出函数
        self.save_weights_to_json(deformer_type, data, full_path)

    # 选择json文件加载权重
    def select_weight_file(self):
        """选择JSON文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择JSON文件",
            self.controller_file_path + '\\scratch_file\\weight_data',  # 默认路径
            "JSON文件 (*.json);;所有文件 (*.*)"  # 文件过滤器
        )
        # print(file_path)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data

    # 保存数据
    def save_weights_to_json(self, mesh, data, file_path=None):
        """
        将变形器数据保存为JSON文件[4,5](@ref)
        """
        if file_path is None:
            cmds.warning('没有路径')
            return

        all_deformer_data = []

        deformer_data = data
        all_deformer_data.append(deformer_data)
        # print(deformer_data)

        # 使用json.dump()保存数据[4](@ref)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(deformer_data, f, indent=2, ensure_ascii=False)  # 设置indent让JSON更易读[5](@ref)

        print(f"成功保存变形器数据到: {file_path}")
        return file_path

    # 选择json文件加载变形器
    def select_file(self):
        """选择JSON文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择JSON文件",
            self.controller_file_path + '\\scratch_file\\all_deform_data',  # 默认路径
            "JSON文件 (*.json);;所有文件 (*.*)"  # 文件过滤器
        )
        # print(file_path)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.show_info(data)  # 自动显示基本信息

    # 显示数据并运行
    def show_info(self,data):
        mel.eval('TranslateToolWithSnapMarkingMenu;')
        """显示文件基本信息"""
        if not data:
            return

        metadata = data['metadata']
        mesh_data = data['deformers']['mesh']

        # info_text = "=== 文件基本信息 ===\n\n"
        # info_text += f"版本: {metadata.get('version', 'N/A')}\n"
        # info_text += f"网格名称: {metadata.get('mesh', 'N/A')}\n"
        # info_text += f"变形器数量: {metadata.get('deformer_count', 'N/A')}\n"

        # 顶点信息
        vertices = mesh_data[1]
        # info_text += f"顶点: {mesh_data[1]}\n"
        # info_text += f"法线: {mesh_data[2]}\n"
        # info_text += f"面拓扑: {mesh_data[3]}\n"
        # info_text += f"UV_u坐标: {mesh_data[4]}\n"
        # info_text += f"UV_v坐标: {mesh_data[5]}\n"
        # info_text += f"UV_面拓扑: {mesh_data[6]}\n"
        # info_text += f"光滑组: {mesh_data[7]}\n\n"

        # 根据数据创建模型，此模型负责拷贝
        mesh_obj = self.model.creare_mesh(mesh_data[1], mesh_data[2], mesh_data[3], mesh_data[4], mesh_data[5], mesh_data[6], mesh_data[7])
        print(mesh_obj)
        # 骨骼信息
        if 'deformers' in data['deformers']:
            deform_len = len(data['deformers']['deformers'])
            for i in range(deform_len):
                deform = data['deformers']['deformers'][deform_len-1-i]
                # print('deform_type',deform['deform_type'])
                if deform:
                    if deform['deform_type'] == 'skinCluster':
                        joint_data = deform['joint_data']
                        weights =  deform['weights']
                        # info_text += f"骨骼: {joint_data}\n"
                        # info_text += f"skinCluster权重数据: {weights}\n"

                        # 显示属性
                        attributes = deform['attributes']
                        # for an_data in attributes:
                        #     info_text += an_data[0]+"属性:\n"
                        #     for key, value in an_data[1].items():
                        #         info_text += f"  {key}: {value}\n"
                        # info_text += f"\n"

                        self.get_data_create_skinCluster(mesh_obj, joint_data, weights, attributes)

                    elif deform['deform_type'] in ['cluster','deformBend','deformFlare','deformSine','deformSquash','deformTwist','deformWave']:
                        weights = deform['weights']
                        # info_text += f"cluster权重数据: {weights}\n"

                        attributes = deform['attributes']
                        # for an_data in attributes:
                        #     info_text += an_data[0]+"属性:\n"
                        #     for key, value in an_data[1].items():
                        #         info_text += f"  {key}: {value}\n"
                        # info_text += f"\n"

                        self.get_data_create_cluster(mesh_obj, weights, attributes, deform['deform_type'])

                    elif deform['deform_type'] == 'ffd':
                        weights = deform['weights']
                        # info_text += f"ffd权重数据: {weights}\n"

                        attributes = deform['attributes']
                        # for an_data in attributes:
                        #     info_text += an_data[0]+"属性:\n"
                        #     for key, value in an_data[1].items():
                        #         info_text += f"  {key}: {value}\n"

                        point_t = deform['point_t']
                        # info_text += f"晶格点数据: {point_t}\n"
                        # info_text += f"\n"
                        self.get_data_create_ffd(mesh_obj, weights, attributes, point_t)

                    elif deform['deform_type'] == 'jiggle':
                        info_text += f"抖动权重数据: {weights}\n"

                        attributes = deform['attributes']
                        # for an_data in attributes:
                        #     info_text += an_data[0] + "属性:\n"
                        #     for key, value in an_data[1].items():
                        #         info_text += f"  {key}: {value}\n"
                        # info_text += f"\n"

                        # 创建抖动变形器
                        cmds.select(mesh_obj)
                        mel.eval(r'doJiggle 1 { "0.5", "0.5", "1", "0", "0", "default", "" };')
                        cluster = cmds.ls(sl=1)[0]
                        cluster_node = cmds.listConnections(cluster + '.diskCache', source=True,d=1)[0]
                        # print(cluster_node)
                        # print('cluster_handle',cluster_handle)
                        all_vertices = cmds.ls(f'{mesh_obj}.vtx[*]', flatten=True)
                        # 使用列表批量操作，效率更高（推荐）
                        for vtx, weight in zip(all_vertices, weights):
                            cmds.percent(cluster_node, vtx, value=weight)
                        # 获取需要设置的对象
                        an_list = [cluster_node]
                        for an_obj, an in zip(an_list, attributes):
                            self.set_deformer_attributes(an_obj, an[1])
                    else:
                        pass
        # print(info_text)

    # 按数据创建蒙皮
    def get_data_create_skinCluster(self, mesh, joint_data, weight, attributes):
        # 创建骨骼并父化
        all_joint = []
        for data in joint_data:
            joint_name = data['joint_name']
            all_joint.append(joint_name)
            if not cmds.objExists(joint_name):
                cmds.select(cl=1)
                cmds.joint(n=joint_name)

        for data in joint_data:
            joint_name = data['joint_name']
            parent = data['parent']
            if parent:
                cmds.parent(joint_name, parent)

        # 设置骨骼位置

        for data in joint_data:
            joint_name = data['joint_name']
            translate = data['translate']
            rotate = data['rotate']
            joint_orient = data['joint_orient']
            scale = data['scale']

            try:
                cmds.setAttr(f'{joint_name}.jointOrientX', joint_orient[0])
                cmds.setAttr(f'{joint_name}.jointOrientY', joint_orient[1])
                cmds.setAttr(f'{joint_name}.jointOrientZ', joint_orient[2])
            except:
                pass

            try:
                cmds.xform(joint_name,
                           translation=translate,
                           rotation=rotate,
                           scale=scale)
            except:
                pass

        # 开始蒙皮并设置权重
        # print(all_joint)
        skin_cluster = cmds.skinCluster(
            all_joint,
            mesh,  # 关键：在此处指定要绑定的网格
            bindMethod=0,
            skinMethod=0,
            maximumInfluences=1,
        )
        # 设置蒙皮权重和属性
        # 假设我们要设置顶点 [0, 1, 2, 3] 的权重
        # vertex_indices_list = [0, 1, 2, 3]
        vertex_indices_list = self.get_all_vertex_indices(mesh)
        vertex_indices = om.MIntArray(vertex_indices_list)

        # 假设皮肤簇影响这两根骨骼（通过 cmds.skinCluster(skin_cluster_name, q=True, influence=True) 可获取骨骼列表和对应索引）
        joint = cmds.skinCluster(skin_cluster, q=True, influence=True)
        # print('all_joint',all_joint)
        # print('joint',joint)
        joint_index_list = [all_joint.index(item) for item in joint]
        influence_indices = om.MIntArray(joint_index_list)  # 骨骼索引，例如 0 对应 'joint1', 1 对应 'joint2'

        # 准备权重数据
        # 权重数组结构：每个顶点对所有影响骨骼的权重。顺序是：顶点0对骨骼0，顶点0对骨骼1，顶点1对骨骼0，顶点1对骨骼1...
        # 例如，设置顶点0完全受骨骼0影响，顶点1完全受骨骼1影响，顶点2受两者平均影响，顶点3受骨骼0影响0.8，骨骼1影响0.2
        # weights_list = [
        #     1.0, 0.0,  # vtx0: joint1 weight=1.0, joint2 weight=0.0
        #     0.0, 1.0,  # vtx1: joint1 weight=0.0, joint2 weight=1.0
        #     0.5, 0.5,  # vtx2: joint1 weight=0.5, joint2 weight=0.5
        #     0.8, 0.2  # vtx3: joint1 weight=0.8, joint2 weight=0.2
        # ]
        weight = [item for sublist in weight for item in sublist]
        weights_data = om.MDoubleArray(weight)

        self.set_skin_weights_api(skin_cluster[0], influence_indices, weights_data, vertex_indices)

        # 设置属性
        # print(attributes)
        for an in attributes:
            # print(an[0])
            # print(an[1])
            self.set_deformer_attributes(skin_cluster[0], an[1])

    def set_skin_weights_api(self, skin_cluster_name, influence_indices, weights_data, vertex_indices):
        """
        使用 OpenMaya API 批量设置蒙皮权重。

        参数:
            skin_cluster_name (str): 皮肤簇节点的名称。
            influence_indices (MIntArray): 影响骨骼的索引数组。
            weights_data (MDoubleArray): 权重值的一维数组，结构为 [顶点0对骨骼0的权重, 顶点0对骨骼1的权重, ..., 顶点N对骨骼M的权重]。
            vertex_indices (MIntArray): 要设置权重的顶点索引数组。
        """
        selection_list = om.MSelectionList()
        selection_list.add(skin_cluster_name)
        skin_cluster_obj = selection_list.getDependNode(0)

        # 使用 oma.MFnSkinCluster 而不是 om.MFnSkinCluster
        skin_cluster_fn = oma.MFnSkinCluster(skin_cluster_obj)  # 修正这里

        # 获取受皮肤簇影响的几何体（网格）
        dag_path = skin_cluster_fn.getPathAtIndex(0)
        components = om.MFnSingleIndexedComponent()
        vertex_component = components.create(om.MFn.kMeshVertComponent)
        components.addElements(vertex_indices)

        # 使用 setWeights 方法批量设置权重
        skin_cluster_fn.setWeights(dag_path, vertex_component, influence_indices, weights_data, normalize=False)

    def get_all_vertex_indices(self, model_name):
        """
        高效地获取模型所有顶点的索引列表。
        """
        # 关键步骤：一次性列出模型的所有顶点组件名
        all_vertices = cmds.ls(f'{model_name}.vtx[*]', flatten=True)
        # 使用列表推导式批量提取索引，这是效率最高的方式
        indices = [self.get_vertex_index(vtx) for vtx in all_vertices]
        return indices

    def get_vertex_index(self, vertex_full_name):
        """
        从顶点的完整名称（如 'pCube1.vtx[4]'）中提取索引号。
        """
        try:
            # 方法1：使用字符串分割（推荐，简单高效）
            index_str = vertex_full_name.split('[')[-1].split(']')[0]
            vertex_index = int(index_str)
            return vertex_index
        except:
            return None

    # 按数据创建蔟
    def get_data_create_cluster(self, mesh, weights, attributes, node_type):
        deform_node = []
        deform_handle = []
        if node_type == 'cluster':
            cluster_node, cluster_handle = cmds.cluster(mesh, envelope=1)
        if node_type in ['deformBend','deformFlare','deformSine','deformSquash','deformTwist','deformWave']:
            cmds.select(mesh)
            if node_type == 'deformBend':
                cmds.Bend(envelope=1)
            if node_type == 'deformFlare':
                cmds.Flare(envelope=1)
            if node_type == 'deformSine':
                cmds.Sine(envelope=1)
            if node_type == 'deformSquash':
                cmds.Squash(envelope=1)
            if node_type == 'deformTwist':
                cmds.Twist(envelope=1)
            if node_type == 'deformWave':
                cmds.Wave(envelope=1)
            cluster_handle = cmds.ls(sl=1)[0]
            cluster_node = cmds.listConnections(cluster_handle+'.worldMatrix[0]', destination=True, source=False)[0]

        # print('cluster_handle',cluster_handle)
        all_vertices = cmds.ls(f'{mesh}.vtx[*]', flatten=True)
        # 使用列表批量操作，效率更高（推荐）
        for vtx, weight in zip(all_vertices, weights):
            cmds.percent(cluster_node, vtx, value=weight)
        # 获取需要设置的对象
        an_list = [cluster_node, cluster_handle]
        for an_obj, an in zip(an_list,attributes):
            self.set_deformer_attributes(an_obj, an[1])

    # 按数据创建晶格
    def get_data_create_ffd(self, mesh, weights, attributes, point_t):
        lattice_node = cmds.lattice(mesh)
        print('lattice_node', lattice_node)
        all_vertices = cmds.ls(f'{mesh}.vtx[*]', flatten=True)
        # 使用列表批量操作，效率更高（推荐）
        for vtx, weight in zip(all_vertices, weights):
            cmds.percent(lattice_node[0], vtx, value=weight)


    # 导出数据
    def export_data(self, sel):
        # 读取数据获取来源：[maya,2024.0]
        major = cmds.about(version=True)
        minor = cmds.about(minorVersion=True)
        maya_version = f"{major}.{minor}"
        # print(maya_version)  # 输出例如：2024.2
        deta_source = ['maya', maya_version]
        print('数据来源:', deta_source)
        # 读取所有模型名称
        # sel = cmds.ls(sl=True)
        # sel_mesh = []
        # for s in sel:
        #     mesh = cmds.listRelatives(s,ad=True,type='mesh')
        #     if mesh:
        #         sel_mesh.append(mesh[0])
        sel_mesh = cmds.listRelatives(sel, ad=True, type='mesh')
        # print(sel_mesh)
        if sel_mesh:
            # 读取所有变形器名称和类型
            # 获取与模型相关的变形器节点
            out_mesh = []
            out_deform = []
            # for s in sel_mesh:
            deforms = cmds.listHistory(sel, pruneDagObjects=True, interestLevel=True)
            out_deform = cmds.ls(deforms, type='geometryFilter')  # 过滤出变形器节点
            # if deforms:
            #     deform_position = []
            #     for i in range(len(deforms)):
            #             # deform_position.append(len(out_deform)-1)
            #         for j in range(len(out_deform)):
            #             if out_deform[j] == deform[i]:
            #                 deform_position.append(j)
            #             break

                # mesh_deform_data = [sel_mesh[0],deform_position]
                # out_mesh.append(mesh_deform_data)
            out_mesh = sel_mesh[0]
            deforms = out_deform

            print('导出模型:', out_mesh)
            print('导出变形器:', out_deform)
            all_deform = []
            all_deform_self_data = []
            # 开始构建数据
            if out_mesh:
                out_mesh_data = []
                mesh = out_mesh
                # for mesh, deforms in zip(out_mesh, out_deform):
                transform = cmds.listRelatives(mesh, p=True)
                sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = self.model.get_mesh_structure_2(transform[0])
                all_topology = MyTreeWidget_2().mintarray_list_to_python_list(all_topology)
                uv_coords_us = list(uv_coords_us)
                uv_coords_vs = list(uv_coords_vs)

                mesh_deta = [sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group]
                # print(mesh_deta)

                # 将变形器数据序列化为JSON兼容的字典结构

                result = {
                    'mesh':mesh_deta,
                    'deformers': []
                }

                for deform in deforms:
                    deformer_type = cmds.nodeType(deform)
                    if deformer_type == 'nonLinear':
                        target = cmds.listConnections(deform + '.deformerData', source=1, shapes=True)
                        deformer_type = cmds.nodeType(target[0])
                    deformer_data = {}  # 为每个变形器创建独立字典

                    if deformer_type == 'skinCluster':
                        # 处理皮肤簇数据
                        skin_joint = cmds.skinCluster(deform, q=1, inf=1) or []
                        joint_data = []

                        for j in range(len(skin_joint)):
                            parent = cmds.listRelatives(skin_joint[j], p=True, type='joint') or []
                            translate = list(cmds.getAttr(skin_joint[j] + ".translate")[0])
                            rotate = list(cmds.getAttr(skin_joint[j] + ".rotate")[0])
                            joint_orient = list(cmds.getAttr(skin_joint[j] + ".jointOrient")[0])
                            scale = list(cmds.getAttr(skin_joint[j] + ".scale")[0])

                            joint_data.append({
                                'joint_name': skin_joint[j],
                                'parent': parent,
                                'translate': translate,
                                'rotate': rotate,
                                'joint_orient': joint_orient,
                                'scale': scale
                            })

                        # 获取权重数据
                        all_weight = []
                        mesh_vtx_list = cmds.ls(mesh + '.vtx[*]', fl=1)
                        for vtx in mesh_vtx_list:
                            weight = cmds.skinPercent(deform, vtx, q=True, v=True)
                            # 确保权重数据是基本Python类型[5](@ref)
                            all_weight.append([float(w) for w in weight])

                        # 获取可编辑属性
                        # editable_attrs, skipped_attrs = self.get_editable_deformer_attributes(deform)
                        editable_attrs = []
                        for obj, type1 in zip([deform], ['skinCluster']):
                            editable_attrs1, skipped_attrs = self.get_editable_deformer_attributes(obj)
                            editable_attrs.append([type1, editable_attrs1])
                        deformer_data.update({
                            'deform_type': deformer_type,
                            'joint_data': joint_data,
                            'weights': all_weight,
                            'attributes': editable_attrs,
                        })

                    elif deformer_type in ['cluster','deformBend','deformFlare','deformSine','deformSquash','deformTwist','deformWave']:
                        # 处理簇变形器数据
                        weights = self.get_deformer_weights(deform, mesh)
                        if deformer_type == 'cluster':
                            handle_connections = cmds.listConnections(deform + ".matrix", source=True,destination=False)
                        else:
                            target = cmds.listConnections(deform + '.deformerData', source=1, shapes=True)[0]
                            handle_connections = cmds.listRelatives(target,p=1)

                        editable_attrs = []
                        for obj,type1 in zip([deform, handle_connections[0]],[deformer_type, 'transform']):
                            editable_attrs1, skipped_attrs = self.get_editable_deformer_attributes(obj)
                            editable_attrs.append([type1,editable_attrs1])
                        deformer_data.update({
                            'deform_type': deformer_type,
                            'weights': weights,
                            'attributes': editable_attrs,
                        })

                    elif cmds.nodeType(deform) == 'ffd':
                        source_nodes = cmds.listConnections(deform,
                                                            source=True,  # 输入方向
                                                            destination=False,
                                                            plugs=False,  # 是否返回属性名（False 返回节点名）
                                                            skipConversionNodes=True,  # 忽略单位转换节点
                                                            sh=1)
                        source_nodes = list(dict.fromkeys(source_nodes))
                        # print(source_nodes)
                        baseLattice_parent = []
                        lattice_parent = []
                        point_num = []
                        for node in source_nodes:
                            parent = []
                            node_type = cmds.nodeType(node)
                            # print(node_type)
                            if node_type == 'baseLattice':
                                baseLattice_parent = cmds.listRelatives(node, p=1)
                                # launch_cycle += 1
                            if node_type == 'lattice':
                                lattice_parent = cmds.listRelatives(node, p=1)
                                point_name = cmds.ls(node + '.pt[*]', fl=1)
                                for p in point_name:
                                    t = cmds.xform(p, query=True, worldSpace=True,translation=True)
                                    point_num.append(t)

                        # print(source_nodes)
                        weights = self.get_deformer_weights(deform, mesh)
                        editable_attrs = []
                        for obj,type1 in zip([deform, lattice_parent[0], baseLattice_parent[0]],['ffd', 'lattice', 'baseLattice']):
                            editable_attrs1, skipped_attrs = self.get_editable_deformer_attributes(obj)
                            editable_attrs.append([type1,editable_attrs1])
                        deformer_data.update({
                            'deform_type': deformer_type,
                            'weights': weights,
                            'attributes': editable_attrs,
                            'point_t':point_num
                        })

                    elif cmds.nodeType(deform) == 'sculpt':
                        cmds.warning('雕刻变形没有权重，无法导出。')


                    else:
                        # 其他类型变形器
                        # print(deform, mesh)
                        # print('deform',deform)
                        weights = self.get_deformer_weights(deform, mesh)
                        editable_attrs = []
                        for obj, type1 in zip([deform],
                                              [cmds.nodeType(deform)]):
                            editable_attrs1, skipped_attrs = self.get_editable_deformer_attributes(obj)
                            editable_attrs.append([type1, editable_attrs1])
                        deformer_data.update({
                            'deform_type': deformer_type,
                            'weights': weights,
                            'attributes': editable_attrs,
                        })

                    # 将当前变形器数据添加到列表中
                    result['deformers'].append(deformer_data)
                return result

    # 保存数据
    def save_deformers_to_json(self, mesh, file_path=None):
        """
        将变形器数据保存为JSON文件[4,5](@ref)

        参数:
            deforms: 变形器列表
            mesh: 网格名称
            file_path: 保存路径，如果为None则自动生成
        """
        if file_path is None:
            cmds.warning('没有路径')
            return

        all_deformer_data = []


        deformer_data = self.export_data(mesh)
        all_deformer_data.append(deformer_data)
        # print(deformer_data)
        try:
            # 使用json.dump()保存数据[4](@ref)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'version': '1.0',
                        'mesh': mesh,
                        # 'export_date': cmds.date(),
                        'deformer_count': len(all_deformer_data)
                    },
                    'deformers': deformer_data
                }, f, indent=2, ensure_ascii=False)  # 设置indent让JSON更易读[5](@ref)

            print(f"成功保存变形器数据到: {file_path}")
            return file_path

        except Exception as e:
            cmds.error(f"保存JSON文件失败: {e}")
            return None

    # 导入数据
    def load_deformers_from_json(self, file_path):
        """
        从JSON文件读取变形器数据[6](@ref)

        参数:
            file_path: JSON文件路径

        返回:
            dict: 包含所有变形器数据的字典
        """
        if not os.path.exists(file_path):
            cmds.error(f"JSON文件不存在: {file_path}")
            return None

        try:
            # 使用json.load()读取数据[6](@ref)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"成功从 {file_path} 加载数据")
            print(f"网格: {data['metadata']['mesh']}")
            print(f"变形器数量: {data['metadata']['deformer_count']}")

            return data

        except json.JSONDecodeError as e:
            cmds.error(f"JSON文件格式错误: {e}")
            return None
        except Exception as e:
            cmds.error(f"读取JSON文件失败: {e}")
            return None

    # 导出json文件
    def export_deformers_as_json(self, mesh_name, export_path=None):
        """
        导出网格的所有变形器数据到JSON文件
        """
        shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh') or []
        # 获取网格的所有变形器
        deforms = cmds.listHistory(shapes, pruneDagObjects=True, interestLevel=True) or []
        deforms = cmds.ls(deforms, type='geometryFilter')  # 过滤出变形器节点

        if not deforms:
            cmds.warning(f"网格 {mesh_name} 没有找到变形器")
            return None


        # 保存为JSON
        json_file = self.save_deformers_to_json(mesh_name, export_path)

        if json_file:
            print(f"导出完成: {json_file}")
            return json_file
        else:
            cmds.warning("导出失败")
            return None

    # 导入json文件
    def import_deformers_from_json(self, json_file, target_mesh):
        """
        从JSON文件导入变形器数据到目标网格
        """
        data = self.load_deformers_from_json(json_file)

        if not data:
            return False
        print(data)
        # success_count = 0
        # for deformer_data in data['deformers']:
        #     if self.recreate_deformer_from_json(deformer_data, target_mesh):
        #         success_count += 1
        #
        # print(f"成功重建 {success_count}/{len(data['deformers'])} 个变形器")
        return success_count > 0

    # 从maya导出权重json文件
    def create_weight_json_file(self):
        all_selected = cmds.ls(selection=True)
        index = 0
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                       self.controller_file_path + '\\scratch_file\\all_deform_data')
        if not folder_path:  # 用户取消了选择
            cmds.warning("您已取消了选择")
            return

        if not all_selected:  # 没有选中任何对象
            cmds.warning("请先选择一个对象")
            return

        for selected in all_selected:
            output_mesh = []

            # 获取变换节点下的形状子节点
            shapes = cmds.listRelatives(selected, shapes=True, type='mesh') or []
            if shapes:
                # 替换文件名中不允许的字符
                clean_name = re.sub(r'[<>:"/\\|?*]', '_', selected)

                # 获取当前时间的毫秒级时间戳[1,4](@ref)
                milliseconds = int(time.time() * 1000)

                # 构建完整的文件路径
                filename = f"{clean_name}_{index}_{milliseconds}.json"
                full_path = folder_path + '/' + filename

                print(f"保存路径: {full_path}")

                # 调用导出函数
                self.export_deformers_as_json(selected, full_path)
                output_mesh.append(selected)
                index += 1
        # cmds.warning('已经导出:', output_mesh)

    # 获取变形器权重
    def get_deformer_weights(self, deformer_name, mesh_name):
        # 获取变形器节点
        sel = om.MSelectionList()
        sel.add(deformer_name)
        deformer_node = sel.getDependNode(0)

        # 获取几何体的顶点数据
        sel.add(mesh_name)
        dag_path = sel.getDagPath(1)
        mesh_fn = om.MFnMesh(dag_path)
        vertices = mesh_fn.numVertices

        # 使用 MFnWeightGeometryFilter 获取权重
        deformer_fn = oma.MFnWeightGeometryFilter(deformer_node)
        # weights = []
        # # 获取几何体的顶点数量
        # sel.add(mesh_name)
        # dag_path = sel.getDagPath(1)
        # num_vertices = om.MFnMesh(dag_path).numVertices
        # 创建顶点组件对象
        component_fn = om.MFnSingleIndexedComponent()
        components = component_fn.create(om.MFn.kMeshVertComponent)
        for idx in range(vertices):
            component_fn.addElement(idx)
        # for i in range(vertices):
        #     # point = om.MObject()
        #     # point = mesh_fn.getPoint(i)
        #     # weight = deformer_fn.getEnvelopeWeights(i)
        #     # components = om.MObject()
        #     weight = deformer_fn.getWeights(dag_path,components)
        #     weights.append(weight)
        weight = deformer_fn.getWeights(dag_path, components)
        # 转换为普通列表
        weights = []
        for i in range(len(weight)):
            weights.append(weight[i])
        return weights

    # 复制当前选择同类变形器属性
    def copy_deform_an(self):
        items = self.list_widget_1.selectedItems()
        item_1 = []
        items_parent_1 = []
        if items:
            item_1 = items[0].text(0)
            items_parent_1 = items[0].parent()
        # print(items_parent)
        parent_is_bs_1 = False
        items_parent_text_1 = ''
        if items_parent_1:
            items_parent_text_1 = items_parent_1.text(0)
            if cmds.nodeType(items_parent_text_1) == 'blendShape':
                parent_is_bs_1 = True
        items = self.list_widget_2.selectedItems()
        item_2 = []
        items_parent_2 = []
        if items:
            item_2 = items[0].text(0)
            items_parent_2 = items[0].parent()
        if item_1 and item_2:
            self.copy_editable_deformer_attributes(item_1, item_2)

    def copy_deform_an2(self):
        sel = cmds.ls(sl=1)
        # print(sel)
        if len(sel)>1:
            self.copy_editable_deformer_attributes(sel[0], sel[-1])

    # 复制所有属性
    def copy_editable_deformer_attributes2(self, source_deformer, target_deformer):
        """
        将一个变形器的可编辑属性设置复制到另一个同类型变形器上。
        重点复制可键控（Keyable）的属性。

        参数:
            source_deformer (str): 作为模板的源变形器名称。
            target_deformer (str): 需要被修改的目标变形器名称。
        """

        # 基础检查
        if not cmds.objExists(source_deformer):
            raise ValueError(f"错误：源变形器 '{source_deformer}' 不存在。")
        if not cmds.objExists(target_deformer):
            raise ValueError(f"错误：目标变形器 '{target_deformer}' 不存在。")

        # source_type = cmds.nodeType(source_deformer)
        # target_type = cmds.nodeType(target_deformer)
        # if source_type != target_type:
        #     raise TypeError(f"错误：变形器类型不匹配！源是 '{source_type}'，目标是 '{target_type}'。")

        # 1. 获取所有可设置的属性
        all_settable_attrs = cmds.listAttr(source_deformer) or []
        # single_attrs = cmds.listAttr(source_deformer, settable=True, multi=False) or []
        # all_settable_attrs = list(set(all_settable_attrs+single_attrs))
        # 2. 定义需要排除的系统属性列表（可根据需要扩充）
        system_attrs_to_skip = ['caching', 'nodeState', 'binMembership']

        # 用于记录过程的列表
        editable_attrs_found = []
        skipped_attrs = []

        # print(f"开始分析 '{source_deformer}' 的可编辑属性...")

        for attr in all_settable_attrs:
            # 跳过明确要排除的系统属性
            if attr in system_attrs_to_skip:
                skipped_attrs.append(f"{attr} (系统属性)")
                continue

            # 构建完整的属性名
            full_attr_name = f"{source_deformer}.{attr}"

            try:
                # 检查属性是否可键控 - 这是判断用户属性的关键条件[3](@ref)
                is_keyable = cmds.getAttr(full_attr_name, keyable=True)

                # 检查属性是否被锁定
                is_locked = cmds.getAttr(full_attr_name, lock=True)

                # 检查属性是否已被连接（可选：如果希望跳过已连接的属性，可以取消下一行的注释）
                is_connected = cmds.connectionInfo(full_attr_name, isDestination=True)

                # 筛选条件：可键控、未锁定（并且可以选择是否未连接）
                if is_keyable and not is_locked and not is_connected:  # and not is_connected
                    editable_attrs_found.append(attr)
                else:
                    reason = "不可键控" if not is_keyable else "已锁定"
                    skipped_attrs.append(f"{attr} ({reason})")

            except:
                pass

        # 3. 开始复制可编辑属性
        copied_count = 0
        print(f"\n找到 {len(editable_attrs_found)} 个可编辑属性，开始复制...")

        for attr in editable_attrs_found:
            try:
                source_attr = f"{source_deformer}.{attr}"
                target_attr = f"{target_deformer}.{attr}"

                # 获取源属性值
                attr_value = cmds.getAttr(source_attr)

                # 设置目标属性值
                cmds.setAttr(target_attr, attr_value)

                copied_count += 1
                print(f"  已复制: {attr} = {attr_value}")

            except Exception as e:
                print(f"  警告: 复制属性 '{attr}' 时出错: {e}")

        # 4. 输出总结报告
        print(f"\n=== 复制完成 ===")
        # print(f"* 成功复制: {copied_count} 个属性")
        # if skipped_attrs:
        #     print(f"* 已跳过的属性:", skipped_attrs)
            # for skipped in skipped_attrs:
            #     print(f"  - {skipped}")

    # 检查属性
    def check_deformer_type_compatibility(self, source_deformer, target_deformer):
        """
        检查两个变形器类型是否一致，确保兼容性。

        参数:
            source_deformer (str): 源变形器名称
            target_deformer (str): 目标变形器名称

        返回:
            bool: 类型是否一致
        """
        if not cmds.objExists(source_deformer):
            raise ValueError(f"错误：源变形器 '{source_deformer}' 不存在。")
        if not cmds.objExists(target_deformer):
            raise ValueError(f"错误：目标变形器 '{target_deformer}' 不存在。")

        source_type = cmds.nodeType(source_deformer)
        target_type = cmds.nodeType(target_deformer)

        if source_type != target_type:
            raise TypeError(f"错误：变形器类型不匹配！源是 '{source_type}'，目标是 '{target_type}'。")

        return True

    # 获取属性
    def get_editable_deformer_attributes(self, deformer_name):
        """
        获取变形器的所有可编辑属性及其值。

        参数:
            deformer_name (str): 变形器名称

        返回:
            dict: 可编辑属性字典 {属性名: 属性值}
            list: 跳过的属性列表（包含原因）
        """
        if not cmds.objExists(deformer_name):
            raise ValueError(f"错误：变形器 '{deformer_name}' 不存在。")

        # 获取所有可设置属性[6,8](@ref)
        all_settable_attrs = cmds.listAttr(deformer_name) or []

        # 定义需要排除的系统属性列表
        system_attrs_to_skip = ['caching', 'nodeState', 'binMembership']

        editable_attrs = {}
        skipped_attrs = []

        # print(f"开始分析 '{deformer_name}' 的可编辑属性...")

        for attr in all_settable_attrs:
            # 跳过系统属性
            if attr in system_attrs_to_skip:
                skipped_attrs.append(f"{attr} (系统属性)")
                continue

            full_attr_name = f"{deformer_name}.{attr}"

            try:
                # 检查属性是否可键控[7](@ref)
                is_keyable = cmds.getAttr(full_attr_name, keyable=True)
                # 检查属性是否被锁定[6](@ref)
                is_locked = cmds.getAttr(full_attr_name, lock=True)
                # 检查属性是否已被连接
                is_connected = cmds.connectionInfo(full_attr_name, isDestination=True)

                # 筛选条件：可键控、未锁定、未连接
                if is_keyable and not is_locked and not is_connected:
                    # 获取属性值[6](@ref)
                    attr_value = cmds.getAttr(full_attr_name)
                    editable_attrs[attr] = attr_value
                else:
                    reason = "不可键控" if not is_keyable else "已锁定" if is_locked else "已连接"
                    skipped_attrs.append(f"{attr} ({reason})")

            except Exception as e:
                skipped_attrs.append(f"{attr} (访问错误: {str(e)})")
                continue

        # print(f"找到 {len(editable_attrs)} 个可编辑属性，跳过 {len(skipped_attrs)} 个属性")
        return editable_attrs, skipped_attrs

    # 设置属性
    def set_deformer_attributes(self, target_deformer, attributes_dict):
        """
        将属性字典设置到目标变形器上。

        参数:
            target_deformer (str): 目标变形器名称
            attributes_dict (dict): 属性字典 {属性名: 属性值}

        返回:
            dict: 复制结果统计 {'success': 成功数量, 'failed': 失败列表}
        """
        if not cmds.objExists(target_deformer):
            raise ValueError(f"错误：目标变形器 '{target_deformer}' 不存在。")

        if not attributes_dict:
            print("警告：属性字典为空，无需设置")
            return {'success': 0, 'failed': []}

        success_count = 0
        failed_attrs = []

        print(f"开始设置 '{target_deformer}' 的属性...")

        for attr, value in attributes_dict.items():
            try:
                target_attr = f"{target_deformer}.{attr}"

                # 再次确认目标属性可写[8](@ref)
                if cmds.getAttr(target_attr, lock=True):
                    failed_attrs.append(f"{attr} (目标属性被锁定)")
                    continue

                if cmds.connectionInfo(target_attr, isDestination=True):
                    failed_attrs.append(f"{attr} (目标属性已连接)")
                    continue

                # 设置属性值[6](@ref)
                cmds.setAttr(target_attr, value)
                success_count += 1
                print(f"  ✓ 已设置: {attr} = {value}")

            except Exception as e:
                failed_attrs.append(f"{attr} (错误: {str(e)})")
                print(f"  ✗ 设置失败: {attr} - {e}")

        return {'success': success_count, 'failed': failed_attrs}

    # 整合使用
    def copy_editable_deformer_attributes(self, source_deformer, target_deformer):
        """
        增强版：使用三个独立函数复制变形器属性。
        """
        try:
            # 1. 检查类型兼容性
            self.check_deformer_type_compatibility(source_deformer, target_deformer)

            # 2. 获取源变形器属性
            editable_attrs, skipped_attrs = self.get_editable_deformer_attributes(source_deformer)

            # 3. 设置到目标变形器
            result = self.set_deformer_attributes(target_deformer, editable_attrs)

            # 输出详细报告
            print(f"\n=== 复制完成 ===")
            print(f"成功复制: {result['success']} 个属性")
            print(f"跳过属性: {len(skipped_attrs)} 个")
            if skipped_attrs:
                print("跳过的属性详情:")
                for skipped in skipped_attrs[:5]:  # 只显示前5个
                    print(f"  - {skipped}")

            if result['failed']:
                print(f"设置失败: {len(result['failed'])} 个")
                for failed in result['failed']:
                    print(f"  - {failed}")

            return True

        except (ValueError, TypeError) as e:
            print(f"错误: {e}")
            return False


    # 所有点蒙皮权重列表集合：骨骼列表指针,对应权重列表
    # 按模型获取bs权重和偏移数据
    # 获取蔟等变形器权重，加自定义数据
    # 动画部分记录动画数据，包括指针数据和驱动属性
    # 记录导入导出规范


window = Window()


if __name__ == '__main__':
    window.show()


#删除无影响驱动
