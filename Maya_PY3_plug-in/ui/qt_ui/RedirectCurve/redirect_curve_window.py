# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
import json
from maya import OpenMayaUI as Omui
import importlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import shiboken6
import maya.api.OpenMaya as om
import maya.OpenMaya as OpenMaya  # MSceneMessage 回调
import math

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    maya_version_str = str(test_version)
    library_path = root_path + '\\' + maya_version_str
    if os.path.isdir(library_path):
        sys.path.append(library_path)
        maya_version_int = test_version
        break

import general_settings
from general_settings import *
importlib.reload(general_settings)
import others_library
from others_library import *
importlib.reload(others_library)
import ui_edit
from ui_edit import *
importlib.reload(ui_edit)
import model
from model import *
importlib.reload(model)


# ========== Maya 风格大纲树控件 ==========
class MayaTreeWidget(QtWidgets.QTreeWidget):
    dropped = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAnimated(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._arrow_color = QtGui.QColor("#888888")
        self._arrow_size = 4

    def _is_folder(self, item):
        p = item.data(0, QtCore.Qt.UserRole)
        return bool(p and os.path.isdir(p))

    def dropEvent(self, event):
        target = self.itemAt(event.pos())
        if target is not None and self._is_folder(target):
            event.ignore()
            return
        super().dropEvent(event)
        QtCore.QTimer.singleShot(0, self.dropped.emit)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and \
                event.modifiers() & QtCore.Qt.ShiftModifier:
            item = self.itemAt(event.pos())
            if item is not None and item.childCount() > 0:
                arrow_x = self._branch_arrow_x(item)
                if arrow_x is not None:
                    click_x = self.visualItemRect(item).left() + arrow_x
                    if abs(event.pos().x() - click_x) < 12:
                        if self.isExpanded(self.indexFromItem(item)):
                            self._collapse_recursive(item)
                        else:
                            self._expand_recursive(item)
                        event.accept()
                        return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None and item.childCount() > 0:
            if self.isExpanded(self.indexFromItem(item)):
                self._collapse_recursive(item)
            else:
                self._expand_recursive(item)
            return
        super().mouseDoubleClickEvent(event)

    def _branch_arrow_x(self, item):
        depth = 0
        parent = item.parent()
        while parent is not None:
            depth += 1
            parent = parent.parent()
        indent = self.indentation()
        return depth * indent + indent // 2

    def _expand_recursive(self, item):
        if item.childCount() == 0:
            return
        item.setExpanded(True)
        for i in range(item.childCount()):
            self._expand_recursive(item.child(i))

    def _collapse_recursive(self, item):
        item.setExpanded(False)
        for i in range(item.childCount()):
            self._collapse_recursive(item.child(i))

    def drawBranches(self, painter, rect, index):
        if not index.isValid():
            return
        model = index.model()
        if model is None or model.rowCount(index) == 0:
            return

        depth = 0
        parent_idx = index.parent()
        while parent_idx.isValid():
            depth += 1
            parent_idx = parent_idx.parent()

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        is_open = self.isExpanded(index)
        indent = self.indentation()
        x = rect.left() + depth * indent + indent // 2
        y = rect.center().y()

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._arrow_color)

        s = self._arrow_size
        if is_open:
            triangle = QtGui.QPolygonF([
                QtCore.QPointF(x - s, y - s * 0.6),
                QtCore.QPointF(x + s, y - s * 0.6),
                QtCore.QPointF(x, y + s * 0.6),
            ])
        else:
            triangle = QtGui.QPolygonF([
                QtCore.QPointF(x - s * 0.6, y - s),
                QtCore.QPointF(x + s * 0.6, y),
                QtCore.QPointF(x - s * 0.6, y + s),
            ])

        painter.drawPolygon(triangle)
        painter.restore()


# ========== 流式布局 ==========
class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=10, spacing=10):
        super().__init__(parent)
        self._items = []
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        while self._items:
            item = self._items.pop()
            del item

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QtCore.QRect(0, 0, width, 0), True)

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margin_left, margin_top, margin_right, margin_bottom = self.getContentsMargins()
        size += QtCore.QSize(margin_left + margin_right, margin_top + margin_bottom)
        return size

    def sizeHint(self):
        return self.minimumSize()

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def _do_layout(self, rect, test_only):
        margin_left, margin_top, margin_right, margin_bottom = self.getContentsMargins()
        effective_rect = rect.adjusted(margin_left, margin_top, -margin_right, -margin_bottom)
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._items:
            size = item.sizeHint()
            next_x = x + size.width() + spacing
            if next_x - spacing > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + spacing
                next_x = x + size.width() + spacing
                line_height = 0
            if not test_only:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), size))
            x = next_x
            line_height = max(line_height, size.height())

        return y + line_height - rect.y() + margin_bottom


# ========== 修改后的嵌入式视频播放器 ==========
class EmbeddedVideoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.video_widget.setAttribute(QtCore.Qt.WA_NativeWindow, True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video_widget)

        self.player.setVideoOutput(self.video_widget)
        self.is_playing = False
        self._source_set = False

        self.player.errorOccurred.connect(self._on_player_error)
        self.player.mediaStatusChanged.connect(self._on_media_status)

        # 重写视频组件的事件，实现穿透右键菜单和点击暂停/继续
        self.video_widget.mousePressEvent = self.mousePressEvent
        self.video_widget.contextMenuEvent = self.contextMenuEvent

        self.container_ref = None   # 指向包含该播放器的缩略图容器
        self.browser_ref = None     # 指向 AnimationAssetBrowser 实例

    def _on_player_error(self, error, error_string):
        print(f"[视频错误] {error_string}")
        self.is_playing = False
        self._source_set = False
        if self.browser_ref and self.container_ref:
            stack = self.container_ref.property("stack")
            if stack:
                stack.setCurrentIndex(0)

    def _on_media_status(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self._source_set = True
        elif status == QMediaPlayer.InvalidMedia:
            self._source_set = False
            self.is_playing = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if not self._source_set:
                return
            if self.is_playing:
                self.player.pause()
                self.is_playing = False
            else:
                self.player.play()
                self.is_playing = True

    def contextMenuEvent(self, event):
        if self.browser_ref and self.container_ref:
            base_name = self.container_ref.property("base_name")
            self.browser_ref.show_context_menu(event, self.container_ref, base_name)


# ========== 修改后的动画资源浏览器 ==========
class AnimationAssetBrowser(QtWidgets.QWidget):
    def __init__(self, animation_data_path, parent=None):
        super(AnimationAssetBrowser, self).__init__(parent)
        self._ready = False
        self._renaming = False
        self.animation_data_path = animation_data_path
        self.current_folder = None
        self.current_container = None
        self.current_player = None
        self._export_source_getter = None
        self._mapping_getter = None  # 左→右映射数据获取器
        self.init_ui()
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        self.tree_json = os.path.join(self.file_path, "tree_hierarchy.json")
        self.load_folders()
        self._ready = True
        self.save_tree_structure()

    def init_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧导航栏
        nav_container = QtWidgets.QWidget()
        nav_container.setFixedWidth(200)
        nav_container.setStyleSheet("""
            QWidget {
                background-color: #1c1c1e;
                border-right: 1px solid rgba(255,255,255,0.04);
            }
        """)
        nav_layout = QtWidgets.QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 10, 8, 10)
        nav_layout.setSpacing(8)

        title_label = QtWidgets.QLabel(" 动画资源库")
        title_label.setStyleSheet("""
            QLabel {
                color: #d4d4d4;
                font-size: 13px;
                font-weight: 500;
                padding: 10px 12px;
                background-color: #252528;
                border-radius: 6px;
                border: 1px solid rgba(255,255,255,0.03);
            }
        """)
        nav_layout.addWidget(title_label)

        self.tree_widget = MayaTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setIndentation(15)
        self.tree_widget.setStyleSheet("""
            MayaTreeWidget {
                background-color: #1c1c1e;
                border: none;
                padding: 4px 2px;
                color: #b0b0b0;
                font-size: 12px;
                outline: none;
            }
            MayaTreeWidget::item {
                padding: 5px 8px;
                border-radius: 4px;
                margin: 1px 0px;
            }
            MayaTreeWidget::item:selected {
                background-color: rgba(255,255,255,0.06);
                color: #e0e0e0;
            }
            MayaTreeWidget::item:hover:!selected {
                background-color: rgba(255,255,255,0.03);
            }
            MayaTreeWidget::branch {
                background: transparent;
                image: none;
            }
        """)
        self.tree_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.tree_widget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.on_tree_context_menu)

        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        nav_layout.addWidget(self.tree_widget)

        add_folder_btn = QtWidgets.QPushButton("+ 添加文件夹")
        add_folder_btn.setCursor(QtCore.Qt.PointingHandCursor)
        add_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.04);
                color: #9a9a9a;
                padding: 9px 12px;
                border-radius: 6px;
                border: 1px solid rgba(255,255,255,0.05);
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.08);
                color: #c0c0c0;
                border: 1px solid rgba(255,255,255,0.1);
            }
        """)
        add_folder_btn.clicked.connect(self.add_new_folder)
        nav_layout.addWidget(add_folder_btn)

        main_layout.addWidget(nav_container)

        # 右侧内容区
        content_container = QtWidgets.QWidget()
        content_container.setStyleSheet("background-color: #202022;")
        content_layout = QtWidgets.QVBoxLayout(content_container)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(10)

        self.breadcrumb_label = QtWidgets.QLabel("选择文件夹查看内容")
        self.breadcrumb_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
                padding: 8px 14px;
                background-color: rgba(255,255,255,0.02);
                border-radius: 6px;
                border: 1px solid rgba(255,255,255,0.03);
            }
        """)
        content_layout.addWidget(self.breadcrumb_label)

        self.content_scroll = QtWidgets.QScrollArea()
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #202022;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.08);
                min-height: 30px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255,255,255,0.15);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.grid_widget = QtWidgets.QWidget()
        self.grid_layout = FlowLayout(self.grid_widget, margin=15, spacing=15)
        self.grid_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.grid_widget.customContextMenuRequested.connect(self.on_grid_context_menu)

        self.content_scroll.setWidget(self.grid_widget)
        content_layout.addWidget(self.content_scroll)

        main_layout.addWidget(content_container)

        # 拖拽后自动保存树结构
        self.tree_widget.dropped.connect(
            self.save_tree_structure
        )
        self.tree_widget.model().rowsMoved.connect(
            lambda *args: self.save_tree_structure()
        )
        self.tree_widget.model().rowsRemoved.connect(
            lambda *args: self.save_tree_structure()
        )
        self.tree_widget.model().layoutChanged.connect(
            self.save_tree_structure
        )
        self.tree_widget.itemChanged.connect(self._on_item_renamed)

    # ========== 树结构重名检测 ==========
    def _collect_all_names(self, item):
        names = set()
        def walk(root):
            for i in range(root.childCount()):
                child = root.child(i)
                if child is not item:
                    names.add(child.text(0))
                walk(child)
        for i in range(self.tree_widget.topLevelItemCount()):
            top = self.tree_widget.topLevelItem(i)
            if top is not item:
                names.add(top.text(0))
            walk(top)
        return names

    def _unique_name(self, base, item):
        taken = self._collect_all_names(item)
        if base not in taken:
            return base
        index = 1
        while f"{base}_{index}" in taken:
            index += 1
        return f"{base}_{index}"

    def _on_item_renamed(self, item, column):
        if not self._ready or self._renaming:
            return
        new_name = item.text(0)
        unique = self._unique_name(new_name, item)
        if unique != new_name:
            self._renaming = True
            item.setText(0, unique)
            self._renaming = False
        self.save_tree_structure()

    # ========== 树结构 JSON 持久化 ==========
    def save_tree_structure(self):
        if not self._ready:
            return
        data = []
        def serialize(item):
            folder_path = item.data(0, QtCore.Qt.UserRole)
            if folder_path and os.path.isdir(folder_path):
                node = {"name": item.text(0), "type": "folder", "path": folder_path, "children": []}
            else:
                node = {"name": item.text(0), "type": "virtual", "children": []}
            for i in range(item.childCount()):
                node["children"].append(serialize(item.child(i)))
            return node
        for i in range(self.tree_widget.topLevelItemCount()):
            data.append(serialize(self.tree_widget.topLevelItem(i)))
        try:
            with open(self.tree_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存树结构失败: {e}")

    def load_folders(self):
        tree_json = os.path.join(self.file_path, "tree_hierarchy.json")
        self.tree_widget.clear()

        json_nodes = []
        if os.path.exists(tree_json):
            try:
                with open(tree_json, "r", encoding="utf-8") as f:
                    json_nodes = json.load(f)
            except Exception as e:
                print(f"加载树结构失败: {e}")

        disk_folders = self._scan_disk_folders()

        # 过滤：移除磁盘不存在的文件夹节点
        json_cleaned = []
        json_dirty = False
        for node in json_nodes:
            cleaned = self._clean_tree_node(node, disk_folders)
            if cleaned is None:
                json_dirty = True
                print(f"已移除失效节点: {node.get('name', '?')}")
            elif cleaned is not node:
                json_dirty = True
                json_cleaned.append(cleaned)
            else:
                json_cleaned.append(cleaned)

        # 脏数据写回
        if json_dirty:
            try:
                with open(tree_json, "w", encoding="utf-8") as f:
                    json.dump(json_cleaned, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"保存清理后的树结构失败: {e}")

        def build(parent, node):
            item = QtWidgets.QTreeWidgetItem(parent)
            item.setText(0, node["name"])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            node_type = node.get("type", "folder")
            if node_type == "folder":
                folder_path = node.get("path", os.path.join(self.animation_data_path, node["name"]))
                item.setData(0, QtCore.Qt.UserRole, folder_path)
                item.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
                name = os.path.basename(folder_path)
                disk_folders.pop(name, None)
            else:
                item.setData(0, QtCore.Qt.UserRole, None)
            for child in node.get("children", []):
                build(item, child)
            return item

        for node in json_cleaned:
            build(self.tree_widget, node)

        for name, path in sorted(disk_folders.items()):
            item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            item.setText(0, name)
            item.setData(0, QtCore.Qt.UserRole, path)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            item.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))

    def _clean_tree_node(self, node, disk_folders):
        """递归清理树节点：移除磁盘不存在的文件夹，保留虚拟节点

        Returns:
            清理后的节点 dict，或 None 表示该节点应被移除
        """
        node_type = node.get("type", "folder")

        # 文件夹节点：检查磁盘是否存在
        if node_type == "folder":
            folder_path = node.get("path", os.path.join(self.animation_data_path, node["name"]))
            if not os.path.isdir(folder_path):
                return None  # 文件夹不存在 → 移除节点

        # 递归清理子节点
        children = node.get("children", [])
        if children:
            cleaned_children = []
            for child in children:
                c = self._clean_tree_node(child, disk_folders)
                if c is not None:
                    cleaned_children.append(c)
            node["children"] = cleaned_children

        return node

    def _scan_disk_folders(self):
        result = {}
        if os.path.exists(self.animation_data_path):
            for folder_name in sorted(os.listdir(self.animation_data_path)):
                folder_path = os.path.join(self.animation_data_path, folder_name)
                if os.path.isdir(folder_path):
                    result[folder_name] = folder_path
        return result

    def add_new_folder(self):
        folder_name, ok = QtWidgets.QInputDialog.getText(self, "添加新文件夹", "请输入文件夹名称:")
        if ok and folder_name:
            illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            if any(char in folder_name for char in illegal_chars):
                QtWidgets.QMessageBox.warning(self, "错误", "文件夹名称包含非法字符")
                return
            new_folder_path = os.path.join(self.animation_data_path, folder_name)
            if os.path.exists(new_folder_path):
                QtWidgets.QMessageBox.warning(self, "错误", "该文件夹已存在")
                return
            try:
                os.makedirs(os.path.join(new_folder_path, "animation"))
                os.makedirs(os.path.join(new_folder_path, "picture"))
                os.makedirs(os.path.join(new_folder_path, "video"))
                # 添加到树并保存
                item = QtWidgets.QTreeWidgetItem(self.tree_widget)
                item.setText(0, folder_name)
                item.setData(0, QtCore.Qt.UserRole, new_folder_path)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                item.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
                self.save_tree_structure()
                print(f"已创建新文件夹: {folder_name}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "错误", f"创建文件夹失败: {str(e)}")

    # ========== 大纲右键菜单 ==========
    def on_tree_context_menu(self, pos):
        item = self.tree_widget.itemAt(pos)
        menu = QtWidgets.QMenu(self.tree_widget)

        new_virtual_act = menu.addAction("新建空层级")
        rename_act = None
        delete_act = None
        if item is not None:
            rename_act = menu.addAction("改名")
            menu.addSeparator()
            delete_act = menu.addAction("删除层级")

        action = menu.exec(self.tree_widget.mapToGlobal(pos))
        if action is None:
            return

        if action == new_virtual_act:
            new_item = QtWidgets.QTreeWidgetItem()
            new_item.setData(0, QtCore.Qt.UserRole, None)
            new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)
            if item is not None:
                if self.tree_widget._is_folder(item):
                    parent = item.parent()
                    if parent is None:
                        idx = self.tree_widget.indexOfTopLevelItem(item)
                        self.tree_widget.insertTopLevelItem(idx + 1, new_item)
                    else:
                        idx = parent.indexOfChild(item)
                        parent.insertChild(idx + 1, new_item)
                else:
                    item.addChild(new_item)
                    item.setExpanded(True)
            else:
                self.tree_widget.addTopLevelItem(new_item)
            unique_name = self._unique_name("新分组", new_item)
            new_item.setText(0, unique_name)
            self.save_tree_structure()

        elif item is not None and action == rename_act:
            self.tree_widget.editItem(item)

        elif item is not None and action == delete_act:
            folder_path = item.data(0, QtCore.Qt.UserRole)
            is_folder = folder_path and os.path.isdir(folder_path)
            reply = QtWidgets.QMessageBox.question(
                self, "确认删除",
                f"确定要删除层级 '{item.text(0)}' 吗？\n（仅从大纲移除，不会删除磁盘文件）",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                if is_folder:
                    self.stop_current_video()
                parent = item.parent()
                while item.childCount() > 0:
                    child = item.takeChild(0)
                    if parent is None:
                        self.tree_widget.addTopLevelItem(child)
                    else:
                        parent.addChild(child)
                if parent is None:
                    index = self.tree_widget.indexOfTopLevelItem(item)
                    self.tree_widget.takeTopLevelItem(index)
                else:
                    parent.removeChild(item)
                self.save_tree_structure()

    # ========== 缩略图与嵌入式视频 ==========
    def create_thumbnail_item(self, image_path, file_name):
        wrapper = QtWidgets.QWidget()
        wrapper.setFixedWidth(100)
        wrapper_layout = QtWidgets.QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(4)

        container = QtWidgets.QWidget()
        container.setFixedSize(100, 100)
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(255,255,255,0.03);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
            }
            QWidget:hover {
                background-color: rgba(255,255,255,0.07);
                border: 1px solid rgba(255,255,255,0.12);
            }
        """)

        stack = QtWidgets.QStackedLayout(container)

        image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(90, 90, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        image_label.setAlignment(QtCore.Qt.AlignCenter)

        video_widget = EmbeddedVideoWidget()
        video_widget.browser_ref = self
        video_widget.container_ref = container

        stack.addWidget(image_label)
        stack.addWidget(video_widget)
        stack.setCurrentIndex(0)

        base_name = os.path.splitext(file_name)[0]

        name_label = QtWidgets.QLabel(base_name)
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setMaximumWidth(100)
        name_label.setStyleSheet(
            "color: #808080; font-size: 10px; background: transparent; border: none;"
        )

        wrapper_layout.addWidget(container, 0, QtCore.Qt.AlignHCenter)
        wrapper_layout.addWidget(name_label)

        wrapper.setProperty("container", container)
        wrapper.setProperty("stack", stack)
        wrapper.setProperty("video_widget", video_widget)
        wrapper.setProperty("base_name", base_name)

        def mouse_press_event(event):
            if event.button() == QtCore.Qt.LeftButton:
                container.setFixedSize(100, 99)

        def mouse_release_event(event):
            if event.button() == QtCore.Qt.LeftButton:
                container.setFixedSize(100, 100)
                self.toggle_media(wrapper, base_name)
            elif event.button() == QtCore.Qt.RightButton:
                self.show_context_menu(event, wrapper, base_name)

        container.mousePressEvent = mouse_press_event
        container.mouseReleaseEvent = mouse_release_event
        return wrapper

    def toggle_media(self, container, base_name):
        if self.current_container == container:
            video_widget = container.property("video_widget")
            if not video_widget._source_set:
                return
            player = video_widget.player
            if video_widget.is_playing:
                player.pause()
                video_widget.is_playing = False
            else:
                player.play()
                video_widget.is_playing = True
            return

        self.stop_current_video()

        video_path = os.path.join(self.current_folder, "video", f"{base_name}.mov")
        if not os.path.exists(video_path):
            print(f"[视频缺失] {video_path}")
            return

        stack = container.property("stack")
        video_widget = container.property("video_widget")
        video_widget.player.setSource(QtCore.QUrl.fromLocalFile(video_path))
        video_widget.player.setLoops(QMediaPlayer.Infinite)
        video_widget.player.play()
        video_widget.is_playing = True
        stack.setCurrentIndex(1)

        # 延迟检查播放是否启动成功
        QtCore.QTimer.singleShot(400, lambda: self._check_playback_started(container, stack))

        self.current_container = container

    def _check_playback_started(self, container, stack):
        video_widget = container.property("video_widget")
        if not video_widget._source_set:
            video_widget.is_playing = False
            stack.setCurrentIndex(0)
            if self.current_container == container:
                self.current_container = None

    def stop_current_video(self):
        if self.current_container:
            stack = self.current_container.property("stack")
            video_widget = self.current_container.property("video_widget")
            video_widget.player.stop()
            video_widget.player.setSource(QtCore.QUrl())  # 释放文件句柄
            video_widget._source_set = False
            video_widget.is_playing = False
            stack.setCurrentIndex(0)   # 切回图片
            self.current_container = None

    def clear_grid(self):
        self.stop_current_video()
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_tree_item_clicked(self, item, column):
        folder_path = item.data(0, QtCore.Qt.UserRole)
        if not folder_path or not os.path.isdir(folder_path):
            # 文件夹不存在 → 重建大纲（自动清理失效节点）
            self.load_folders()
            self.clear_grid()
            self.breadcrumb_label.setText(f"分组: {item.text(0)}")
            self.current_folder = None
            return
        self.current_folder = folder_path
        self.current_folder_selected(folder_path)

    def populate_grid(self, picture_path):
        self.clear_grid()
        if not os.path.exists(picture_path):
            return
        for file_name in sorted(os.listdir(picture_path)):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(picture_path, file_name)
                thumb = self.create_thumbnail_item(image_path, file_name)
                self.grid_layout.addWidget(thumb)

    def set_export_source(self, getter):
        self._export_source_getter = getter

    def set_mapping_source(self, getter):
        self._mapping_getter = getter

    def on_grid_context_menu(self, pos):
        if self.current_folder is None:
            return
        # 只响应空白区域，不响应子控件（thumbnail 有自己的菜单）
        child = self.grid_widget.childAt(pos)
        if child is not None:
            return
        menu = QtWidgets.QMenu(self.grid_widget)
        export_act = menu.addAction("导出动画")
        action = menu.exec(self.grid_widget.mapToGlobal(pos))
        if action == export_act:
            self.export_animation()

    def export_animation(self):
        if self.current_folder is None:
            print("未选择文件夹")
            return

        if self._export_source_getter is None:
            print("未设置动画源")
            return

        source_data = self._export_source_getter()
        if not source_data:
            print("左侧栏无控制器数据，请先在下拉框选择模板或手动添加行")
            return

        anim_name, ok = QtWidgets.QInputDialog.getText(
            self, "导出动画", "请输入动画名称:",
            text="new_anim"
        )
        if not ok or not anim_name.strip():
            return
        anim_name = anim_name.strip()

        picture_dir = os.path.join(self.current_folder, "picture")
        video_dir = os.path.join(self.current_folder, "video")
        anim_dir = os.path.join(self.current_folder, "animation")
        for d in (picture_dir, video_dir, anim_dir):
            os.makedirs(d, exist_ok=True)

        json_path = os.path.join(anim_dir, f"{anim_name}.json")
        if os.path.exists(json_path):
            reply = QtWidgets.QMessageBox.question(
                self, "覆盖确认",
                f"动画 '{anim_name}' 已存在，是否覆盖？",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply != QtWidgets.QMessageBox.Yes:
                return

        frame_min = int(cmds.playbackOptions(q=True, minTime=True))
        frame_max = int(cmds.playbackOptions(q=True, maxTime=True))
        fps = cmds.currentUnit(q=True, time=True)
        fps_map = {"film": 24, "game": 15, "pal": 25, "ntsc": 30, "show": 48, "palf": 50, "ntscf": 60}
        fps_val = fps_map.get(fps, 24)

        curves = []
        skipped_ctrl = []
        no_keys_ctrl = []

        for src_name, namespace in source_data:
            if not src_name:
                continue

            full_name = src_name
            if not cmds.objExists(full_name):
                alt = None
                for ns_info in cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True):
                    if ns_info in ('UI', 'shared'):
                        continue
                    prefix = ns_info if ns_info == ':' else f"{ns_info}:"
                    candidate = f"{prefix}{src_name}"
                    if cmds.objExists(candidate):
                        alt = candidate
                        break
                if alt:
                    full_name = alt
                else:
                    skipped_ctrl.append(src_name)
                    continue

            anim_attrs = cmds.listAnimatable(full_name)
            if anim_attrs is None:
                no_keys_ctrl.append(src_name)
                continue

            # 收集该控制器所有 keyframe 时间的并集
            all_key_times = set()
            for attr_path in anim_attrs:
                short_attr = attr_path.split('.')[-1]
                if short_attr in ('visibility',):
                    continue
                key_times = cmds.keyframe(attr_path, query=True, timeChange=True)
                if key_times:
                    all_key_times.update(int(t) for t in key_times)

            if not all_key_times:
                no_keys_ctrl.append(src_name)
                continue

            all_key_times = sorted(all_key_times)

            # 以第一个关键帧的本地 TRS 作为参考
            cmds.currentTime(all_key_times[0])
            ref_trs = {
                "tx": cmds.getAttr(f"{full_name}.translateX"),
                "ty": cmds.getAttr(f"{full_name}.translateY"),
                "tz": cmds.getAttr(f"{full_name}.translateZ"),
                "rx": cmds.getAttr(f"{full_name}.rotateX"),
                "ry": cmds.getAttr(f"{full_name}.rotateY"),
                "rz": cmds.getAttr(f"{full_name}.rotateZ"),
                "sx": cmds.getAttr(f"{full_name}.scaleX"),
                "sy": cmds.getAttr(f"{full_name}.scaleY"),
                "sz": cmds.getAttr(f"{full_name}.scaleZ"),
            }

            deltas = []
            for t in all_key_times:
                cmds.currentTime(t)
                d = {
                    "dtx": cmds.getAttr(f"{full_name}.translateX") - ref_trs["tx"],
                    "dty": cmds.getAttr(f"{full_name}.translateY") - ref_trs["ty"],
                    "dtz": cmds.getAttr(f"{full_name}.translateZ") - ref_trs["tz"],
                    "drx": cmds.getAttr(f"{full_name}.rotateX") - ref_trs["rx"],
                    "dry": cmds.getAttr(f"{full_name}.rotateY") - ref_trs["ry"],
                    "drz": cmds.getAttr(f"{full_name}.rotateZ") - ref_trs["rz"],
                    "dsx": cmds.getAttr(f"{full_name}.scaleX") - ref_trs["sx"],
                    "dsy": cmds.getAttr(f"{full_name}.scaleY") - ref_trs["sy"],
                    "dsz": cmds.getAttr(f"{full_name}.scaleZ") - ref_trs["sz"],
                }
                deltas.append([int(t), d])

            curves.append({
                "object": src_name,
                "ref_trs": ref_trs,
                "deltas": deltas
            })

        if not curves:
            print("未找到任何动画曲线数据")
            return

        data = {
            "version": "4.0",
            "name": anim_name,
            "frame_range": [frame_min, frame_max],
            "fps": float(fps_val),
            "curves": curves
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"动画数据已保存: {json_path}")

        png_path = os.path.join(picture_dir, f"{anim_name}.png")
        try:
            cmds.playblast(
                frame=frame_min,
                format='image',
                compression='png',
                completeFilename=png_path,
                viewer=False,
                showOrnaments=False,
                widthHeight=[320, 240]
            )
            print(f"缩略图已保存: {png_path}")
        except Exception as e:
            print(f"截图失败: {e}")

        mov_path = os.path.join(video_dir, f"{anim_name}.mov")
        mov_base = os.path.join(video_dir, anim_name)   # Maya 自动加 .mov

        try:
            cmds.playblast(
                format='qt',
                filename=mov_base,
                forceOverwrite=True,
                viewer=False,
                clearCache=True,
                showOrnaments=False,
                widthHeight=[640, 480],
                startTime=frame_min,
                endTime=frame_max
            )
            if os.path.exists(mov_path):
                print(f"视频已保存: {mov_path}")
            else:
                print(f"playblast 完成但未找到文件: {mov_path}")
        except Exception as e:
            print(f"playblast 失败: {e}")

        status = f"导出完成: {len(curves)} 条曲线"
        if skipped_ctrl:
            status += f", 跳过控制器: {', '.join(skipped_ctrl[:3])}"
        if no_keys_ctrl:
            status += f", 无动画曲线: {', '.join(no_keys_ctrl[:3])}"
        print(status)

        if os.path.exists(png_path):
            self.current_folder_selected(self.current_folder)

    def current_folder_selected(self, folder_path):
        folder_name = os.path.basename(folder_path)
        self.breadcrumb_label.setText(f"文件夹: {folder_name}")
        self.stop_current_video()
        picture_path = os.path.join(folder_path, "picture")
        if os.path.exists(picture_path):
            self.populate_grid(picture_path)
        else:
            self.clear_grid()

    def show_context_menu(self, event, widget, base_name):
        menu = QtWidgets.QMenu(widget)
        pos = event.globalPos()
        import_direct_act = menu.addAction("导入动画")
        menu.addSeparator()
        delete_act = menu.addAction("删除动画")
        menu.addSeparator()
        info_act = menu.addAction(f"文件: {base_name}")
        action = menu.exec(pos)
        if action == import_direct_act:
            self.import_animation(base_name)
        elif action == delete_act:
            self.delete_animation(widget, base_name)

    def import_animation(self, base_name):
        if not self.current_folder:
            print("未选择文件夹")
            return

        json_path = os.path.join(self.current_folder, "animation", f"{base_name}.json")
        if not os.path.exists(json_path):
            print(f"动画JSON文件不存在: {json_path}")
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"读取动画JSON失败: {e}")
            return

        curves = data.get("curves", [])
        if not curves:
            print("动画数据为空")
            return

        frame_range = data.get("frame_range", None)
        fps = data.get("fps", 24.0)

        # 读取当前帧作为偏移基准（必须在任何场景修改之前）
        frame_offset = int(cmds.currentTime(q=True))

        if frame_range and len(frame_range) >= 2:
            self._setup_scene_for_import(fps)

        if frame_offset != 0:
            print(f"当前帧 {frame_offset} 作为偏移基准，关键帧将偏移 +{frame_offset}")

        # ---- 计算总关键帧数用于进度条 ----
        total_keys = 0
        for entry in curves:
            frames = entry.get("keys", []) or entry.get("deltas", [])
            total_keys += len(frames)

        progress = QtWidgets.QProgressDialog(
            f"正在导入动画: {base_name}", "取消", 0, total_keys, self
        )
        progress.setWindowTitle("导入动画")
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.setStyleSheet("""
            QProgressDialog {
                background-color: #2a2a2e;
                color: #d4d4d4;
            }
            QProgressBar {
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 4px;
                text-align: center;
                background-color: #1c1c1e;
                color: #d4d4d4;
            }
            QProgressBar::chunk {
                background-color: #4a90d9;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #3a3a3e;
                color: #d4d4d4;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 4px;
                padding: 4px 16px;
            }
            QPushButton:hover {
                background-color: #4a4a4e;
            }
            QLabel {
                color: #d4d4d4;
            }
        """)

        imported = 0
        skipped = 0
        key_count = 0

        # ---- 建立 左栏控制器名 → (右栏控制器名, 命名空间) 映射 ----
        mapping = {}  # {left_name: (right_name, namespace)}
        if self._mapping_getter:
            for left, right, ns in self._mapping_getter():
                left = left.strip()
                right = right.strip() if right else ""
                if left:
                    mapping[left] = (right, ns)

        # ---- 辅助：解析目标对象全名 ----
        def resolve_target(right_name, ns):
            """根据右栏名和命名空间解析场景中的目标对象全名

            严格按命名空间匹配：
            - 指定命名空间 → ns:right_name
            - 根命名空间 ':' → 直接 right_name 查找
            - 找不到 → 跳过（不兜底搜索其他命名空间）
            """
            if not right_name:
                return None
            if ns and ns != ':':
                target = f"{ns}:{right_name}"
                if cmds.objExists(target):
                    return target
                return None  # 指定了命名空间但找不到 → 跳过
            # 根命名空间或无命名空间 → 直接查
            if cmds.objExists(right_name):
                return right_name
            return None

        # ---- 辅助：安全 setKeyframe（跳过锁定轴和不存在的属性） ----
        def safe_set_key(obj, attr, frame, value):
            try:
                cmds.setKeyframe(obj, at=attr, t=frame, v=value)
                return True
            except Exception:
                return False

        # 探测格式
        first_entry = curves[0] if curves else {}
        if "ref_trs" in first_entry:
            fmt = "v4"
        elif "ref_matrix" in first_entry:
            fmt = "v3"
        else:
            fmt = "v2"

        for entry in curves:
            if progress.wasCanceled():
                print("导入已取消")
                break

            src_name = entry.get("object", "")
            keys = entry.get("keys", []) or entry.get("deltas", [])

            if not src_name or not keys:
                skipped += 1
                continue

            # ---- 查找左→右映射 ----
            if src_name not in mapping:
                print(f"  跳过: 左边栏无对应映射 '{src_name}'")
                skipped += 1
                continue

            right_name, ns = mapping[src_name]
            if not right_name:
                print(f"  跳过: '{src_name}' 对应的右边栏为空")
                skipped += 1
                continue

            target = resolve_target(right_name, ns)
            if target is None:
                print(f"  跳过: 目标对象 '{right_name}' 不存在于场景中")
                skipped += 1
                continue

            if fmt == "v4":
                # ---- v4.0 本地 TRS 偏移模式 ----
                deltas = entry.get("deltas", [])
                for d in deltas:
                    if progress.wasCanceled():
                        break
                    if len(d) < 2:
                        continue

                    frame_t = int(d[0]) + frame_offset
                    delta = d[1]
                    if not isinstance(delta, dict):
                        continue

                    safe_set_key(target, "translateX", frame_t,
                                 cmds.getAttr(f"{target}.translateX") + delta.get("dtx", 0))
                    safe_set_key(target, "translateY", frame_t,
                                 cmds.getAttr(f"{target}.translateY") + delta.get("dty", 0))
                    safe_set_key(target, "translateZ", frame_t,
                                 cmds.getAttr(f"{target}.translateZ") + delta.get("dtz", 0))
                    safe_set_key(target, "rotateX", frame_t,
                                 cmds.getAttr(f"{target}.rotateX") + delta.get("drx", 0))
                    safe_set_key(target, "rotateY", frame_t,
                                 cmds.getAttr(f"{target}.rotateY") + delta.get("dry", 0))
                    safe_set_key(target, "rotateZ", frame_t,
                                 cmds.getAttr(f"{target}.rotateZ") + delta.get("drz", 0))
                    safe_set_key(target, "scaleX", frame_t,
                                 cmds.getAttr(f"{target}.scaleX") + delta.get("dsx", 0))
                    safe_set_key(target, "scaleY", frame_t,
                                 cmds.getAttr(f"{target}.scaleY") + delta.get("dsy", 0))
                    safe_set_key(target, "scaleZ", frame_t,
                                 cmds.getAttr(f"{target}.scaleZ") + delta.get("dsz", 0))

                    key_count += 1
                    progress.setValue(key_count)
                    QtWidgets.QApplication.processEvents()

            elif fmt == "v3":
                # ---- v3.0 世界矩阵偏移模式 ----
                parent = cmds.listRelatives(target, parent=True, fullPath=True)
                if parent:
                    parent_mm = om.MMatrix(
                        cmds.xform(parent[0], query=True, worldSpace=True, matrix=True)
                    )
                    parent_inv = parent_mm.inverse()
                else:
                    parent_inv = om.MMatrix()

                for key_data in keys:
                    if progress.wasCanceled():
                        break
                    if len(key_data) < 2:
                        continue

                    frame_t = int(key_data[0]) + frame_offset
                    offset_flat = key_data[1]

                    if not isinstance(offset_flat, (list, tuple)) or len(offset_flat) != 16:
                        continue

                    offset_mm = om.MMatrix(offset_flat)
                    current_mm = om.MMatrix(
                        cmds.xform(target, query=True, worldSpace=True, matrix=True)
                    )
                    target_world_mm = current_mm * offset_mm
                    local_mm = target_world_mm * parent_inv

                    mtf = om.MTransformationMatrix(local_mm)
                    t = mtf.translation(om.MSpace.kTransform)
                    r = mtf.rotation()
                    s = mtf.scale(om.MSpace.kTransform)

                    safe_set_key(target, "translateX", frame_t, t.x)
                    safe_set_key(target, "translateY", frame_t, t.y)
                    safe_set_key(target, "translateZ", frame_t, t.z)
                    safe_set_key(target, "rotateX", frame_t, math.degrees(r.x))
                    safe_set_key(target, "rotateY", frame_t, math.degrees(r.y))
                    safe_set_key(target, "rotateZ", frame_t, math.degrees(r.z))
                    safe_set_key(target, "scaleX", frame_t, s[0])
                    safe_set_key(target, "scaleY", frame_t, s[1])
                    safe_set_key(target, "scaleZ", frame_t, s[2])

                    key_count += 1
                    progress.setValue(key_count)
                    QtWidgets.QApplication.processEvents()

            else:
                # ---- v2.0 直接数值模式（含自定义属性检测） ----
                attr = entry.get("attribute", "")

                for key_data in keys:
                    if progress.wasCanceled():
                        break
                    if len(key_data) < 2:
                        continue
                    frame_t = key_data[0] + frame_offset
                    values = key_data[1]
                    if isinstance(values, (list, tuple)):
                        if len(values) == 3:
                            safe_set_key(target, f"{attr}X", frame_t, values[0])
                            safe_set_key(target, f"{attr}Y", frame_t, values[1])
                            safe_set_key(target, f"{attr}Z", frame_t, values[2])
                        elif len(values) == 1:
                            safe_set_key(target, attr, frame_t, values[0])
                    else:
                        safe_set_key(target, attr, frame_t, values)

                    key_count += 1
                    progress.setValue(key_count)
                    QtWidgets.QApplication.processEvents()

            imported += 1

        progress.close()
        print(f"动画导入完成: 导入 {imported} 条曲线, 跳过 {skipped} 个")

    def _setup_scene_for_import(self, fps):
        cmds.currentUnit(time=f"{int(fps)}fps")

    def _find_object_in_namespaces(self, short_name):
        for ns_info in cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True):
            if ns_info in ('UI', 'shared'):
                continue
            prefix = ns_info if ns_info == ':' else f"{ns_info}:"
            candidate = f"{prefix}{short_name}"
            if cmds.objExists(candidate):
                return candidate
        return None

    def delete_animation(self, widget, base_name):
        if not self.current_folder:
            return
        reply = cmds.confirmDialog(
            title="删除确认",
            message=f"确定要删除 '{base_name}' 及其所有相关文件吗？",
            button=["是", "否"],
            defaultButton="否",
            cancelButton="否"
        )
        if reply == "是":
            self.stop_current_video()
            QtWidgets.QApplication.processEvents()  # 确保 QMediaPlayer 释放完毕
            for sub in ["picture", "video", "animation"]:
                ext = ".png" if sub == "picture" else ".json" if sub == "animation" else ".mov"
                file_path = os.path.join(self.current_folder, sub, f"{base_name}{ext}")
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
            self.grid_layout.removeWidget(widget)
            widget.deleteLater()
            print(f"已删除动画资源: {base_name}")


# ========== 行组件 ==========


class DynamicRowWidget(QtWidgets.QWidget):
    """动态添加的行UI组件"""

    def __init__(self, parent=None, left_text="", right_text="", namespace="", mode=0):
        super(DynamicRowWidget, self).__init__(parent)
        self.namespace = namespace
        self.mode = mode  # 0=R, 1=TR, 2=Others
        self.setup_ui()

        if left_text:
            self.text_input_1.setText(left_text)
        if right_text:
            self.text_input_2.setText(right_text)

        self.update_namespace_label()
        self.update_mode_button()

    def setup_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 3, 4, 3)
        layout.setSpacing(6)

        self.select_btn_1 = QtWidgets.QPushButton("选择")
        self.select_btn_1.setFixedSize(50, 26)
        self.select_btn_1.setCursor(QtCore.Qt.PointingHandCursor)
        self.select_btn_1.setStyleSheet(self._btn_style())

        self.text_input_1 = QtWidgets.QLineEdit()
        self.text_input_1.setPlaceholderText("源对象...")
        self.text_input_1.setMinimumWidth(100)
        self.text_input_1.setStyleSheet(self._input_style())

        self.label_text = QtWidgets.QLabel("→")
        self.label_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_text.setMinimumWidth(24)
        self.label_text.setStyleSheet("color: rgba(255,255,255,0.25); font-weight: 300;")

        self.namespace_label = QtWidgets.QLabel(":")
        self.namespace_label.setAlignment(QtCore.Qt.AlignCenter)
        self.namespace_label.setMinimumWidth(54)
        self.namespace_label.setStyleSheet("color: rgba(255,255,255,0.25); font-size: 11px;")

        self.select_btn_2 = QtWidgets.QPushButton("选择")
        self.select_btn_2.setFixedSize(50, 26)
        self.select_btn_2.setCursor(QtCore.Qt.PointingHandCursor)
        self.select_btn_2.setStyleSheet(self._btn_style())

        self.text_input_2 = QtWidgets.QLineEdit()
        self.text_input_2.setPlaceholderText("目标对象...")
        self.text_input_2.setMinimumWidth(100)
        self.text_input_2.setStyleSheet(self._input_style())

        self.mode_btn = QtWidgets.QPushButton("R")
        self.mode_btn.setFixedSize(40, 26)
        self.mode_btn.setVisible(False)  # 隐藏模式切换按钮
        self.mode_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.mode_btn.setStyleSheet(self._mode_style("#8a8a92"))

        self.delete_btn = QtWidgets.QPushButton("X")
        self.delete_btn.setFixedSize(26, 26)
        self.delete_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255,255,255,0.2);
                border-radius: 13px;
                font-size: 14px;
                font-weight: 300;
                border: 1px solid transparent;
            }
            QPushButton:hover {
                background-color: rgba(220,80,80,0.15);
                color: #d45050;
                border: 1px solid rgba(220,80,80,0.2);
            }
        """)

        layout.addWidget(self.select_btn_1)
        layout.addWidget(self.text_input_1)
        layout.addWidget(self.label_text)
        layout.addWidget(self.namespace_label)
        layout.addWidget(self.select_btn_2)
        layout.addWidget(self.text_input_2)
        layout.addWidget(self.mode_btn)
        layout.addWidget(self.delete_btn)

        self.delete_btn.clicked.connect(self.delete_self)
        self.select_btn_1.clicked.connect(self.select_source_object)
        self.select_btn_2.clicked.connect(self.select_target_object)
        self.mode_btn.clicked.connect(self.toggle_mode)

    @staticmethod
    def _btn_style():
        return """
            QPushButton {
                background-color: rgba(255,255,255,0.04);
                color: #a0a0a0;
                border-radius: 5px;
                font-size: 11px;
                border: 1px solid rgba(255,255,255,0.05);
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.08);
                color: #c8c8c8;
                border: 1px solid rgba(255,255,255,0.1);
            }
        """

    @staticmethod
    def _input_style():
        return """
            QLineEdit {
                background-color: rgba(255,255,255,0.03);
                color: #c0c0c0;
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255,255,255,0.15);
                background-color: rgba(255,255,255,0.05);
            }
        """

    @staticmethod
    def _mode_style(color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: #e0e0e0;
                border-radius: 5px;
                font-size: 10px;
                font-weight: 500;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {DynamicRowWidget._lighten(color)};
            }}
        """

    @staticmethod
    def _lighten(hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, c + 28) for c in rgb)
        return f"#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}"

    def update_namespace(self, namespace):
        self.namespace = namespace
        self.update_namespace_label()

    def update_namespace_label(self):
        if self.namespace and self.namespace != ':':
            self.namespace_label.setText(f"{self.namespace}:")
        else:
            self.namespace_label.setText(":")

    def toggle_mode(self):
        self.mode = (self.mode + 1) % 3
        self.update_mode_button()

    def update_mode_button(self):
        mode_text = self.get_mode_text()
        self.mode_btn.setText(mode_text)
        colors = {0: "#787880", 1: "#6e6e78", 2: "#7a746e"}
        self.mode_btn.setStyleSheet(self._mode_style(colors.get(self.mode, "#787880")))

    def get_mode_text(self):
        return ["R", "TR", "Other"][self.mode]

    def get_mode_value(self):
        return self.mode

    def select_source_object(self):
        """选择源对象"""
        object_name = self.text_input_1.text().strip()
        if not object_name:
            print("请在第一个文本框中输入对象名称")
            return

        # 构建完整对象名称（不带命名空间）
        full_name = object_name

        # 检查对象是否存在
        if cmds.objExists(full_name):
            cmds.select(full_name, replace=True)
            print(f"已选择源对象: {full_name}")
        else:
            print(f"源对象不存在: {full_name}")

    def select_target_object(self):
        """选择目标对象"""
        object_name = self.text_input_2.text().strip()
        if not object_name:
            print("请在第二个文本框中输入对象名称")
            return

        # 构建完整对象名称（带命名空间）
        if self.namespace and self.namespace != ':':
            full_name = f"{self.namespace}:{object_name}"
        else:
            full_name = object_name

        # 检查对象是否存在
        if cmds.objExists(full_name):
            cmds.select(full_name, replace=True)
            print(f"已选择目标对象: {full_name}")
        else:
            print(f"目标对象不存在: {full_name}")

    def delete_self(self):
        """删除自身"""
        self.setParent(None)
        self.deleteLater()


class TitleBar(QtWidgets.QWidget):
    _edge_margin = 5

    def __init__(self, parent_window):
        super().__init__(parent_window)
        self._window = parent_window
        self._dragging = False
        self._drag_pos = None
        self._resizing = False
        self._resize_edge = None
        self._resize_start_geo = None
        self._resize_start_pos = None
        self.setFixedHeight(34)
        self.setMouseTracking(True)
        self.setStyleSheet("""
            TitleBar {
                background-color: #1a1a1c;
                border-bottom: 1px solid rgba(255,255,255,0.04);
            }
        """)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 4, 0)
        layout.setSpacing(0)

        self.title_label = QtWidgets.QLabel(parent_window.windowTitle())
        self.title_label.setStyleSheet("color: #808080; font-size: 11px; font-weight: 400;")
        self.title_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.min_btn = QtWidgets.QPushButton("─")
        self.min_btn.setFixedSize(36, 28)
        self.min_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.min_btn.setStyleSheet(self._title_btn_style())
        self.min_btn.clicked.connect(parent_window.showMinimized)

        self.close_btn = QtWidgets.QPushButton("✕")
        self.close_btn.setFixedSize(36, 28)
        self.close_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.close_btn.setStyleSheet(self._title_btn_style(close=True))
        self.close_btn.clicked.connect(parent_window.close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)

    def set_title(self, text):
        self.title_label.setText(text)

    @staticmethod
    def _title_btn_style(close=False):
        hover_bg = "rgba(220,80,80,0.6)" if close else "rgba(255,255,255,0.08)"
        hover_color = "#fff" if close else "#c0c0c0"
        return f"""
            QPushButton {{
                background-color: transparent;
                color: #606060;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                color: {hover_color};
            }}
        """

    def _edge_at(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        m = self._edge_margin
        left = x <= m
        right = x >= w - m
        top = y <= m
        if top and left:
            return "top_left"
        if top and right:
            return "top_right"
        if top:
            return "top"
        return None

    def _edge_cursor(self, edge):
        return {
            "top_left": QtCore.Qt.SizeFDiagCursor,
            "top_right": QtCore.Qt.SizeBDiagCursor,
            "top": QtCore.Qt.SizeVerCursor,
        }.get(edge, QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            edge = self._edge_at(event.pos())
            if edge:
                self._resizing = True
                self._resize_edge = edge
                self._resize_start_geo = self._window.geometry()
                self._resize_start_pos = event.globalPosition().toPoint()
                event.accept()
                return
            self._dragging = True
            self._drag_pos = event.globalPosition().toPoint() - self._window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._resizing:
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            geo = QtCore.QRect(self._resize_start_geo)
            e = self._resize_edge
            if "top" in e:
                geo.setTop(geo.top() + delta.y())
            if "left" in e:
                geo.setLeft(geo.left() + delta.x())
            if "right" in e:
                geo.setRight(geo.right() + delta.x())
            self._window.setGeometry(geo)
            event.accept()
            return
        if self._dragging:
            self._window.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            return
        edge = self._edge_at(event.pos())
        self.setCursor(self._edge_cursor(edge) if edge else QtCore.Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._resizing = False
        self._resize_edge = None

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._window.showMinimized()


class RefreshComboBox(QtWidgets.QComboBox):
    """点击展开时自动调用刷新函数的组合框"""

    def __init__(self, refresh_func, parent=None):
        super().__init__(parent)
        self._refresh_func = refresh_func

    def showPopup(self):
        self._refresh_func()
        super().showPopup()


class Window(QtWidgets.QMainWindow):
    _edge_margin = 5

    def __init__(self, parent=None):
        if parent is None:
            try:
                maya_main_window = shiboken6.wrapInstance(
                    int(Omui.MQtUtil.mainWindow()),
                    QtWidgets.QWidget
                )
                parent = maya_main_window
            except:
                parent = None

        try:
            window.close()
            window.deleteLater()
        except:
            pass

        super(Window, self).__init__(parent)

        self.maya_version = cmds.about(version=True)
        self.setWindowTitle(f'重定向工具 (Maya {self.maya_version})')
        self.setMaximumHeight(900)
        self.setMinimumSize(1300, 300)
        self.resize(1200, 500)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        self._resizing = False
        self._resize_edge = None
        self._resize_start_geo = None
        self._resize_start_pos = None

        # 初始化变量
        self.dynamic_rows = []  # 存储动态添加的UI行
        self.current_bone_mapping = []  # 存储当前的bone_mapping列表
        self.association_bone_mapping = {}  # 存储关联数据的bone_mapping字典
        self._scene_callback_ids = []  # Maya 场景事件回调 ID 列表 (Int/MMessage ptr)

        self.ui_edit = UiEdit()
        self.model = Model()
        self.others_library = OthersLibrary()

        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

        # 基础动画数据路径
        self.base_data_folder = self.file_path + '\\base_animation_json_data'
        # 额外动画数据路径
        self.add_data_folder = self.file_path + '\\add_controller_animation_json_data'
        # 关联动画数据路径
        self.association_data_folder = self.file_path + '\\association_controller_animation_json_data'
        # 动画数据路径
        self.animation_data_path = self.file_path + '\\animation_data'

        self.create_widgets()
        self.create_layouts()
        self._app = QtWidgets.QApplication.instance()
        self._app.installEventFilter(self)
        self.create_connections()

        # 窗口创建后立即加载JSON文件到下拉框
        self.load_json_files_to_comboboxes()

        # 窗口创建后立即加载命名空间
        self.refresh_namespace_list()

        # 注册 Maya 场景事件回调（打开/新建/引用导入/引用移除）
        self._register_scene_callbacks()

    def _register_scene_callbacks(self):
        """注册 Maya 场景事件：新建/打开场景 + 引用导入/移除时自动刷新命名空间

        - 新建/打开用 scriptJob → SceneOpened（覆盖 New 和 Open）
        - 引用操作用 MSceneMessage（scriptJob 不支持 namespace 事件）
        """
        # scriptJob: 新建/打开场景（protected=True 防止切换场景时被销毁）
        self._scene_callback_ids.append(
            cmds.scriptJob(event=["SceneOpened", self._refresh_ns_deferred], protected=True)
        )

        # MSceneMessage: 引用导入/移除（绑定方法，不用闭包）
        self._scene_callback_ids.append(
            OpenMaya.MSceneMessage.addCallback(
                OpenMaya.MSceneMessage.kAfterImportReference,
                self._on_ref_changed
            )
        )
        self._scene_callback_ids.append(
            OpenMaya.MSceneMessage.addCallback(
                OpenMaya.MSceneMessage.kAfterRemoveReference,
                self._on_ref_changed
            )
        )
        print("已注册场景事件 (SceneOpened/ImportRef/RemoveRef)")

    def _refresh_ns_deferred(self):
        """延迟刷新命名空间（等 Maya DG 稳定）"""
        QtCore.QTimer.singleShot(300, self.refresh_namespace_list)

    def _on_ref_changed(self, client_data=None):
        """引用变化回调 → 延迟刷新"""
        QtCore.QTimer.singleShot(300, self.refresh_namespace_list)

    def _unregister_scene_callbacks(self):
        """注销所有场景事件"""
        for cb in self._scene_callback_ids:
            if isinstance(cb, int):
                try:
                    cmds.scriptJob(kill=cb, force=True)
                except Exception:
                    pass
            else:
                try:
                    OpenMaya.MMessage.removeCallback(cb)
                except Exception:
                    pass
        self._scene_callback_ids.clear()
        print("已注销场景事件")

    def closeEvent(self, event):
        """窗口关闭时注销 Maya 回调"""
        self._unregister_scene_callbacks()
        super().closeEvent(event)

    def _is_within_titlebar(self, widget):
        while widget is not None:
            if widget is getattr(self, 'title_bar', None):
                return True
            if widget is self:
                return False
            widget = widget.parent()
        return False

    def _window_edge_at(self, pos):
        x, y = pos.x(), pos.y()
        w = self.centralWidget().width()
        h = self.centralWidget().height()
        m = self._edge_margin
        left = x <= m
        right = x >= w - m
        bottom = y >= h - m
        if bottom and left:
            return "bottom_left"
        if bottom and right:
            return "bottom_right"
        if bottom:
            return "bottom"
        if left:
            return "left"
        if right:
            return "right"
        return None

    def _edge_cursor(self, edge):
        return {
            "left": QtCore.Qt.SizeHorCursor,
            "right": QtCore.Qt.SizeHorCursor,
            "bottom": QtCore.Qt.SizeVerCursor,
            "bottom_left": QtCore.Qt.SizeBDiagCursor,
            "bottom_right": QtCore.Qt.SizeFDiagCursor,
        }.get(edge, QtCore.Qt.ArrowCursor)

    def eventFilter(self, obj, event):
        t = event.type()
        if t not in (QtCore.QEvent.MouseMove, QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease):
            return super().eventFilter(obj, event)

        widget = obj
        while widget is not None:
            if widget is self:
                break
            widget = widget.parent()
        else:
            return super().eventFilter(obj, event)

        if self._is_within_titlebar(obj):
            return super().eventFilter(obj, event)

        local_pos = self.centralWidget().mapFromGlobal(event.globalPosition().toPoint())

        if t == QtCore.QEvent.MouseMove:
            if not self._resizing:
                edge = self._window_edge_at(local_pos)
                self.centralWidget().setCursor(
                    self._edge_cursor(edge) if edge else QtCore.Qt.ArrowCursor
                )
        elif t == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            edge = self._window_edge_at(local_pos)
            if edge:
                self._resizing = True
                self._resize_edge = edge
                self._resize_start_geo = self.geometry()
                self._resize_start_pos = event.globalPosition().toPoint()
                return True
        elif t == QtCore.QEvent.MouseButtonRelease:
            self._resizing = False
            self._resize_edge = None
            self.centralWidget().setCursor(QtCore.Qt.ArrowCursor)
        return super().eventFilter(obj, event)

    def mouseMoveEvent(self, event):
        if self._resizing:
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            geo = QtCore.QRect(self._resize_start_geo)
            e = self._resize_edge
            if "top" in e:
                geo.setTop(geo.top() + delta.y())
            if "bottom" in e:
                geo.setBottom(geo.bottom() + delta.y())
            if "left" in e:
                geo.setLeft(geo.left() + delta.x())
            if "right" in e:
                geo.setRight(geo.right() + delta.x())
            self.setGeometry(geo)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_edge = None
        super().mouseReleaseEvent(event)

    def refresh_namespace_list(self):
        """刷新命名空间列表"""
        self.namespace_combo.blockSignals(True)
        self.namespace_combo.clear()

        # 获取所有命名空间
        namespaces = self.get_all_namespaces()

        if namespaces:
            self.namespace_combo.addItems(namespaces)

            # 设置当前命名空间为选中状态
            current_namespace = cmds.namespaceInfo(currentNamespace=True)
            index = self.namespace_combo.findText(current_namespace)
            if index >= 0:
                self.namespace_combo.setCurrentIndex(index)

            print(f"已加载 {len(namespaces)} 个命名空间")
        else:
            self.namespace_combo.addItem("无命名空间")
            print("警告: 未找到任何命名空间")

        self.namespace_combo.blockSignals(False)

        # blockSignals 阻断了信号，手动联动更新所有动态行命名空间标签
        self.switch_namespace(self.namespace_combo.currentText())

    def get_all_namespaces(self):
        """获取当前Maya文件中的所有命名空间"""
        namespaces = []
        all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        default_namespaces = ['UI', 'shared']
        for ns in all_namespaces:
            if ns not in default_namespaces and not ns.startswith(':'):
                namespaces.append(ns)
        namespaces.insert(0, ':')
        return namespaces

    def load_json_files_to_comboboxes(self):
        """从指定文件夹加载JSON文件到下拉框"""
        # 清空现有选项
        self.namespace_combo.clear()
        self.combo_box_1.clear()
        self.combo_box_2.clear()
        self.combo_box_3.clear()

        # 加载基础模板类型的JSON文件
        base_files = self.get_json_files(self.base_data_folder)
        if base_files:
            self.combo_box_1.addItems(base_files)
            print(f"已加载 {len(base_files)} 个基础模板类型文件")
        else:
            self.combo_box_1.addItem("无可用文件")
            print(f"警告: 文件夹 '{self.base_data_folder}' 中没有JSON文件")

        # 加载附加控制器/动画的JSON文件
        add_files = self.get_json_files(self.add_data_folder)
        if add_files:
            self.combo_box_2.addItems(add_files)
            print(f"已加载 {len(add_files)} 个附加控制器/动画文件")
        else:
            self.combo_box_2.addItem("无可用文件")
            print(f"警告: 文件夹 '{self.add_data_folder}' 中没有JSON文件")

        # 加载关联数据的JSON文件
        association_files = self.get_json_files(self.association_data_folder)
        if association_files:
            self.combo_box_3.addItems(association_files)
            print(f"已加载 {len(association_files)} 个关联数据文件")
        else:
            self.combo_box_3.addItem("无可用文件")
            print(f"警告: 文件夹 '{self.association_data_folder}' 中没有JSON文件")

    def get_json_files(self, folder_path):
        """获取指定文件夹中的所有JSON文件名（不带扩展名）"""
        json_files = []
        try:
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    if file.lower().endswith('.json'):
                        file_name = os.path.splitext(file)[0]
                        json_files.append(file_name)
        except Exception as e:
            print(f"读取文件夹 '{folder_path}' 时出错: {str(e)}")
        return json_files

    def create_widgets(self):
        self.namespace_combo = RefreshComboBox(self.refresh_namespace_list)
        self.namespace_combo.setMinimumWidth(130)
        self.namespace_combo.setToolTip("点击展开自动刷新命名空间列表")
        self.namespace_combo.setStyleSheet(self._combo_style())

        self.refresh_namespace_btn = QtWidgets.QPushButton("↻")
        self.refresh_namespace_btn.setFixedSize(28, 28)
        self.refresh_namespace_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.refresh_namespace_btn.setToolTip("刷新命名空间列表")
        self.refresh_namespace_btn.setVisible(False)  # 已由下拉框展开自动刷新替代

        self.combo_box_1 = QtWidgets.QComboBox()
        self.combo_box_1.setMinimumWidth(120)
        self.combo_box_1.setStyleSheet(self._combo_style())

        self.combo_box_2 = QtWidgets.QComboBox()
        self.combo_box_2.setMinimumWidth(120)
        self.combo_box_2.setStyleSheet(self._combo_style())

        self.combo_box_3 = QtWidgets.QComboBox()
        self.combo_box_3.setMinimumWidth(120)
        self.combo_box_3.setStyleSheet(self._combo_style())

        # ---- 删除模板按钮 ----
        self.btn_del_base = QtWidgets.QPushButton("X")
        self.btn_del_base.setFixedSize(22, 22)
        self.btn_del_base.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_del_base.setToolTip("删除当前基础模板")

        self.btn_del_add = QtWidgets.QPushButton("X")
        self.btn_del_add.setFixedSize(22, 22)
        self.btn_del_add.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_del_add.setToolTip("删除当前附加数据")

        self.btn_del_assoc = QtWidgets.QPushButton("X")
        self.btn_del_assoc.setFixedSize(22, 22)
        self.btn_del_assoc.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_del_assoc.setToolTip("删除当前关联数据")

        self.btn_add_row = QtWidgets.QPushButton("+ 添加新行")
        self.btn_add_row.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_add_row.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.btn_add_row.setStyleSheet(self._btn_secondary_style())

        self.btn_generate_constraints = QtWidgets.QPushButton("生成约束")
        self.btn_generate_constraints.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_generate_constraints.setVisible(False)  # 暂时隐藏
        self.btn_generate_constraints.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.08);
                color: #d0d0d0;
                padding: 10px 40px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                border: 1px solid rgba(255,255,255,0.1);
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.13);
                color: #e8e8e8;
                border: 1px solid rgba(255,255,255,0.18);
            }
        """)

        self.btn_print_left = QtWidgets.QPushButton("打印左边栏")
        self.btn_print_left.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_print_left.setStyleSheet(self._btn_secondary_style())

        self.btn_print_right = QtWidgets.QPushButton("打印右边栏")
        self.btn_print_right.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_print_right.setStyleSheet(self._btn_secondary_style())

        # ---- 对照预设按钮 ----
        self.btn_save_base = QtWidgets.QPushButton("保存基础模板")
        self.btn_save_base.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_save_base.setStyleSheet(self._btn_secondary_style())

        self.btn_save_add = QtWidgets.QPushButton("保存附加数据")
        self.btn_save_add.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_save_add.setStyleSheet(self._btn_secondary_style())

        self.btn_save_assoc = QtWidgets.QPushButton("保存关联数据")
        self.btn_save_assoc.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_save_assoc.setStyleSheet(self._btn_secondary_style())

    @staticmethod
    def _combo_style():
        return """
            QComboBox {
                background-color: rgba(255,255,255,0.03);
                color: #b0b0b0;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QComboBox:hover {
                border: 1px solid rgba(255,255,255,0.12);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid rgba(255,255,255,0.05);
            }
            QComboBox::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid rgba(255,255,255,0.3);
                margin-right: 6px;
            }
            QComboBox QAbstractItemView {
                background-color: #222225;
                color: #b0b0b0;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 4px;
                selection-background-color: rgba(255,255,255,0.08);
                outline: none;
            }
        """

    @staticmethod
    def _btn_secondary_style():
        return """
            QPushButton {
                background-color: rgba(255,255,255,0.04);
                color: #9a9a9a;
                padding: 8px 18px;
                border-radius: 6px;
                font-size: 12px;
                border: 1px solid rgba(255,255,255,0.05);
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.08);
                color: #c0c0c0;
                border: 1px solid rgba(255,255,255,0.1);
            }
        """

    def create_layouts(self):
        central_widget = QtWidgets.QWidget()
        central_widget.setStyleSheet("background-color: #1c1c1e;")
        self.setCentralWidget(central_widget)

        root_layout = QtWidgets.QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        root_layout.addWidget(self.title_bar)

        main_h_layout = QtWidgets.QHBoxLayout()
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        left_widget = QtWidgets.QWidget()
        left_widget.setStyleSheet("background-color: #1c1c1e;")
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(14, 14, 14, 14)
        left_layout.setSpacing(10)

        ns_label = QtWidgets.QLabel("命名空间")
        ns_label.setStyleSheet("color: #808080; font-size: 11px;")
        namespace_layout = QtWidgets.QHBoxLayout()
        namespace_layout.addWidget(ns_label)
        namespace_layout.addWidget(self.namespace_combo)
        namespace_layout.addWidget(self.refresh_namespace_btn)
        namespace_layout.addStretch()

        label_style = "color: #808080; font-size: 11px; padding: 0px 4px;"

        top_selection_layout = QtWidgets.QHBoxLayout()
        lbl1 = QtWidgets.QLabel("基础模板类型")
        lbl1.setStyleSheet(label_style)
        top_selection_layout.addWidget(lbl1)
        top_selection_layout.addWidget(self.combo_box_1)
        top_selection_layout.addWidget(self.btn_del_base)
        top_selection_layout.addSpacing(16)
        lbl2 = QtWidgets.QLabel("附加控制器/动画")
        lbl2.setStyleSheet(label_style)
        top_selection_layout.addWidget(lbl2)
        top_selection_layout.addWidget(self.combo_box_2)
        top_selection_layout.addWidget(self.btn_del_add)
        top_selection_layout.addSpacing(16)
        lbl3 = QtWidgets.QLabel("关联数据")
        lbl3.setStyleSheet(label_style)
        top_selection_layout.addWidget(lbl3)
        top_selection_layout.addWidget(self.combo_box_3)
        top_selection_layout.addWidget(self.btn_del_assoc)
        top_selection_layout.addStretch()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1c1c1e;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.06);
                min-height: 30px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255,255,255,0.12);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: transparent;
                height: 6px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255,255,255,0.06);
                min-width: 30px;
                border-radius: 3px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(255,255,255,0.12);
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setStyleSheet("background-color: #1c1c1e;")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(4)
        self.scroll_layout.addStretch()

        scroll_area.setWidget(self.scroll_content)

        bottom_btn_layout = QtWidgets.QHBoxLayout()
        bottom_btn_layout.addWidget(self.btn_print_left)
        bottom_btn_layout.addWidget(self.btn_add_row)
        bottom_btn_layout.addWidget(self.btn_print_right)

        preset_layout = QtWidgets.QHBoxLayout()
        preset_label = QtWidgets.QLabel("对照预设:")
        preset_label.setStyleSheet("color: #808080; font-size: 11px; padding: 0px 4px;")
        preset_layout.addWidget(preset_label)
        preset_layout.addWidget(self.btn_save_base)
        preset_layout.addWidget(self.btn_save_add)
        preset_layout.addWidget(self.btn_save_assoc)
        preset_layout.addStretch()

        left_layout.addLayout(namespace_layout)
        left_layout.addLayout(top_selection_layout)
        left_layout.addWidget(scroll_area, 1)
        left_layout.addLayout(bottom_btn_layout)
        left_layout.addLayout(preset_layout)

        self.animation_browser = AnimationAssetBrowser(self.animation_data_path)
        self.animation_browser.set_export_source(self._get_export_source_data)
        self.animation_browser.set_mapping_source(self._get_mapping_data)

        main_h_layout.addWidget(left_widget, 2)
        main_h_layout.addWidget(self.animation_browser, 3)

        root_layout.addLayout(main_h_layout)

    def create_connections(self):
        """连接信号和槽"""
        self.btn_add_row.clicked.connect(self.add_dynamic_row)
        self.namespace_combo.currentTextChanged.connect(self.switch_namespace)
        self.refresh_namespace_btn.clicked.connect(self.refresh_namespace_list)

        self.btn_print_left.clicked.connect(self.print_left_column)
        self.btn_print_right.clicked.connect(self.print_right_column)
        self.btn_generate_constraints.clicked.connect(self.generate_constraints)

        self.combo_box_1.currentTextChanged.connect(self.on_combo1_changed)
        self.combo_box_2.currentTextChanged.connect(self.on_combo2_changed)
        self.combo_box_3.currentTextChanged.connect(self.on_combo3_changed)

        self.btn_save_base.clicked.connect(self.save_base_preset)
        self.btn_save_add.clicked.connect(self.save_add_preset)
        self.btn_save_assoc.clicked.connect(self.save_assoc_preset)

        self.btn_del_base.clicked.connect(lambda: self.delete_template(self.combo_box_1, self.base_data_folder, "基础模板", 1))
        self.btn_del_add.clicked.connect(lambda: self.delete_template(self.combo_box_2, self.add_data_folder, "附加数据", 2))
        self.btn_del_assoc.clicked.connect(lambda: self.delete_template(self.combo_box_3, self.association_data_folder, "关联数据", 3))

    def switch_namespace(self, namespace):
        """切换命名空间并更新所有行的命名空间标签"""
        print(f"切换到命名空间: {namespace}")

        # 更新所有动态行的命名空间
        for row in self.dynamic_rows:
            row.update_namespace(namespace)

    def on_combo1_changed(self, text):
        """第一个下拉框选择变化时的处理"""
        print(f"选择了基础模板类型: {text}")
        self.update_dynamic_rows_from_json()

    def on_combo2_changed(self, text):
        """第二个下拉框选择变化时的处理"""
        print(f"选择了附加控制器/动画: {text}")
        self.update_dynamic_rows_from_json()

    def on_combo3_changed(self, text):
        """第三个下拉框选择变化时的处理（关联数据）"""
        print(f"选择了关联数据: {text}")
        self.load_association_data(text)
        # 更新所有现有行的右边文本框
        self.update_all_rows_with_association()

    def load_association_data(self, text):
        """加载关联数据文件"""
        if text and text != "无可用文件":
            association_file = os.path.join(self.association_data_folder, f"{text}.json")
            if os.path.exists(association_file):
                try:
                    with open(association_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'bone_mapping' in data and isinstance(data['bone_mapping'], dict):
                            self.association_bone_mapping = data['bone_mapping']
                            print(f"成功加载关联数据: {text}，包含 {len(data['bone_mapping'])} 个映射")
                        else:
                            self.association_bone_mapping = {}
                            print(f"关联数据文件格式不正确，缺少bone_mapping字典")
                except Exception as e:
                    self.association_bone_mapping = {}
                    print(f"加载关联数据JSON文件失败: {str(e)}")
            else:
                self.association_bone_mapping = {}
                print(f"关联数据文件不存在: {association_file}")
        else:
            self.association_bone_mapping = {}

    def update_all_rows_with_association(self):
        """根据关联数据更新所有行的右边文本框"""
        for row in self.dynamic_rows:
            left_text = row.text_input_1.text().strip()
            if left_text and left_text in self.association_bone_mapping:
                row.text_input_2.setText(self.association_bone_mapping[left_text])
            else:
                row.text_input_2.clear()

    def update_dynamic_rows_from_json(self):
        """根据两个下拉框的选择更新动态行"""
        # 清空现有的动态行
        self.clear_all_rows()

        # 获取两个JSON文件中的bone_mapping
        bone_mapping_list = []

        # 获取基础模板的bone_mapping
        base_template = self.combo_box_1.currentText()
        if base_template and base_template != "无可用文件":
            base_file = os.path.join(self.base_data_folder, f"{base_template}.json")
            if os.path.exists(base_file):
                try:
                    with open(base_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'bone_mapping' in data and isinstance(data['bone_mapping'], list):
                            # 新格式：[[bone_name, mode], ...]
                            bone_mapping_list.extend(data['bone_mapping'])
                            print(f"从基础模板加载了 {len(data['bone_mapping'])} 个骨骼映射")
                except Exception as e:
                    print(f"加载基础模板JSON文件失败: {str(e)}")

        # 获取附加控制器的bone_mapping
        add_animation = self.combo_box_2.currentText()
        if add_animation and add_animation != "无可用文件":
            add_file = os.path.join(self.add_data_folder, f"{add_animation}.json")
            if os.path.exists(add_file):
                try:
                    with open(add_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'bone_mapping' in data and isinstance(data['bone_mapping'], list):
                            # 新格式：[[bone_name, mode], ...]
                            bone_mapping_list.extend(data['bone_mapping'])
                            print(f"从附加控制器加载了 {len(data['bone_mapping'])} 个骨骼映射")
                except Exception as e:
                    print(f"加载附加控制器JSON文件失败: {str(e)}")

        # 去重（保持顺序）
        seen = set()
        unique_bone_mapping = []
        for item in bone_mapping_list:
            # 将列表转换为元组以便可以放入set中
            if isinstance(item, list):
                item_tuple = tuple(item)
            else:
                item_tuple = item

            if item_tuple not in seen:
                seen.add(item_tuple)
                unique_bone_mapping.append(item)

        # 存储当前的bone_mapping
        self.current_bone_mapping = unique_bone_mapping

        # 为每个bone_mapping创建一个动态行
        for bone_item in unique_bone_mapping:
            if isinstance(bone_item, list) and len(bone_item) >= 2:
                bone_name = bone_item[0]
                mode = bone_item[1]
                self.add_dynamic_row_with_text(bone_name, mode)
            else:
                # 兼容旧格式
                bone_name = bone_item
                mode = 0
                self.add_dynamic_row_with_text(bone_name, mode)

        print(f"总共创建了 {len(unique_bone_mapping)} 个动态行")

    def add_dynamic_row_with_text(self, left_text="", mode=0):
        """添加带有预填文本的动态行"""
        # 检查关联数据中是否有对应的右边文本
        right_text = ""
        if left_text and left_text in self.association_bone_mapping:
            right_text = self.association_bone_mapping[left_text]

        # 获取当前命名空间
        current_namespace = self.namespace_combo.currentText()

        row_widget = DynamicRowWidget(self.scroll_content, left_text, right_text, current_namespace, mode)
        self.dynamic_rows.append(row_widget)

        # 连接删除按钮到删除函数
        row_widget.delete_btn.clicked.connect(lambda checked=False, rw=row_widget: self.remove_dynamic_row(rw))

        # 插入到最后一个元素之前（在stretch之前）
        insert_index = self.scroll_layout.count() - 1
        self.scroll_layout.insertWidget(insert_index, row_widget)

    def add_dynamic_row(self):
        """添加新的动态行"""
        current_namespace = self.namespace_combo.currentText()
        row_widget = DynamicRowWidget(self.scroll_content, namespace=current_namespace)
        self.dynamic_rows.append(row_widget)

        # 连接删除按钮到删除函数
        row_widget.delete_btn.clicked.connect(lambda checked=False, rw=row_widget: self.remove_dynamic_row(rw))

        # 插入到最后一个元素之前（在stretch之前）
        insert_index = self.scroll_layout.count() - 1
        self.scroll_layout.insertWidget(insert_index, row_widget)

        # 设置焦点到第一个输入框
        row_widget.text_input_1.setFocus()

    def remove_dynamic_row(self, row_widget):
        """从列表中移除动态行并删除UI"""
        if row_widget in self.dynamic_rows:
            self.dynamic_rows.remove(row_widget)
        row_widget.delete_self()
        print(f"已删除一行，剩余 {len(self.dynamic_rows)} 行")

    def clear_all_rows(self):
        """清除所有动态行"""
        for row in self.dynamic_rows[:]:  # 使用切片复制列表
            self.remove_dynamic_row(row)
        self.dynamic_rows.clear()

    def _get_export_source_data(self):
        data = []
        for row in self.dynamic_rows:
            src = row.text_input_1.text().strip()
            if src:
                data.append((src, row.namespace))
        return data

    def _get_mapping_data(self):
        """提供左栏→右栏+命名空间的映射数据给 AnimationAssetBrowser"""
        current_ns = self.namespace_combo.currentText()
        data = []
        for row in self.dynamic_rows:
            left = row.text_input_1.text().strip()
            right = row.text_input_2.text().strip()
            data.append((left, right, current_ns))
        return data

    def generate_constraints(self):
        """生成约束"""
        print("开始生成约束...")

        # 检查是否有动态行
        if not self.dynamic_rows:
            print("没有可处理的行，请先添加行")
            return

        success_count = 0
        fail_count = 0

        for row in self.dynamic_rows:
            source_name = row.text_input_1.text().strip()
            target_name = row.text_input_2.text().strip()
            mode = row.get_mode_value()

            if not source_name or not target_name:
                print(f"跳过空行: 源='{source_name}', 目标='{target_name}'")
                fail_count += 1
                continue

            # 构建完整对象名称
            current_namespace = row.namespace
            if current_namespace and current_namespace != ':':
                full_source_name = source_name  # 源对象通常不带命名空间
                full_target_name = f"{current_namespace}:{target_name}"
            else:
                full_source_name = source_name
                full_target_name = target_name

            # 检查对象是否存在
            if not cmds.objExists(full_source_name):
                print(f"源对象不存在: {full_source_name}")
                fail_count += 1
                continue

            if not cmds.objExists(full_target_name):
                print(f"目标对象不存在: {full_target_name}")
                fail_count += 1
                continue

            try:
                # 根据模式创建不同的约束
                if mode == 0:  # R - 旋转约束
                    constraint = cmds.orientConstraint(full_source_name, full_target_name, maintainOffset=True)[0]
                    print(f"已创建旋转约束: {full_source_name} -> {full_target_name}")
                elif mode == 1:  # TR - 父子约束
                    constraint = cmds.parentConstraint(full_source_name, full_target_name, maintainOffset=True)[0]
                    print(f"已创建父子约束: {full_source_name} -> {full_target_name}")
                else:  # Others - 缩放约束
                    constraint = cmds.scaleConstraint(full_source_name, full_target_name, maintainOffset=True)[0]
                    print(f"已创建缩放约束: {full_source_name} -> {full_target_name}")

                success_count += 1
            except Exception as e:
                print(f"创建约束失败 {full_source_name} -> {full_target_name}: {str(e)}")
                fail_count += 1

        print(f"约束生成完成! 成功: {success_count}, 失败: {fail_count}")

    def print_left_column(self):
        """打印左边栏的所有文字及模式"""
        left_texts = []
        for row in self.dynamic_rows:
            text = row.text_input_1.text().strip()
            mode = row.get_mode_value()
            mode_text = row.get_mode_text()
            if text:
                left_texts.append((text, mode, mode_text))
            else:
                left_texts.append(('', mode, mode_text))

        print("=" * 50)
        print("左边栏文字列表（含模式）:")
        print("=" * 50)
        if left_texts:
            for i, (text, mode, mode_text) in enumerate(left_texts, 1):
                print(f"{i}. {text} [模式: {mode_text}({mode})]")
        else:
            print("左边栏没有填写任何文字")
        print("=" * 50)

    def print_right_column(self):
        """打印右边栏的所有文字"""
        right_texts = []
        for row in self.dynamic_rows:
            text = row.text_input_2.text().strip()
            if text:
                right_texts.append(text)
            else:
                right_texts.append('')
        print("=" * 50)
        print("右边栏文字列表:")
        print("=" * 50)
        if right_texts:
            for i, text in enumerate(right_texts, 1):
                print(f"{i}. {text}")
        else:
            print("右边栏没有填写任何文字")
        print("=" * 50)

    def _save_preset_with_dialog(self, folder, combo, label, mapping_type="list"):
        """弹出命名对话框后保存预设到指定文件夹

        Args:
            folder: 目标文件夹路径
            combo: 对应的下拉框控件
            label: 对话框标题标签（如"基础模板"）
            mapping_type: "list" 用于基础/附加模板, "dict" 用于关联数据
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

        # 弹框让用户输入文件名
        name, ok = QtWidgets.QInputDialog.getText(
            self, f"保存{label}预设", "请输入预设名称:",
            text=""
        )
        if not ok or not name.strip():
            return
        filename = name.strip()

        # 检查同名文件是否已存在
        preset_path = os.path.join(folder, f"{filename}.json")
        if os.path.exists(preset_path):
            reply = QtWidgets.QMessageBox.question(
                self, "覆盖确认",
                f"预设 \"{filename}\" 已存在，是否覆盖？",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply != QtWidgets.QMessageBox.Yes:
                return

        # 收集当前对照数据
        if mapping_type == "dict":
            bone_mapping = {}
            for row in self.dynamic_rows:
                left = row.text_input_1.text().strip()
                right = row.text_input_2.text().strip()
                if left:
                    bone_mapping[left] = right if right else ""
        else:
            bone_mapping = []
            for row in self.dynamic_rows:
                left = row.text_input_1.text().strip()
                if left:
                    bone_mapping.append([left, row.get_mode_value()])

        data = {
            "template_name": filename,
            "version": "1.0",
            "description": "",
            "bone_mapping": bone_mapping
        }
        with open(preset_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self._refresh_combo_after_save(combo, folder, filename)
        print(f"{label}预设 \"{filename}\" 已保存: {len(bone_mapping)} 个映射 → {preset_path}")

    def save_base_preset(self):
        self._save_preset_with_dialog(
            self.base_data_folder, self.combo_box_1, "基础模板", "list"
        )

    def save_add_preset(self):
        self._save_preset_with_dialog(
            self.add_data_folder, self.combo_box_2, "附加数据", "list"
        )

    def save_assoc_preset(self):
        self._save_preset_with_dialog(
            self.association_data_folder, self.combo_box_3, "关联数据", "dict"
        )

    def _refresh_combo_after_save(self, combo, folder, filename):
        """保存后刷新下拉框，选中刚保存的预设"""
        combo.blockSignals(True)
        combo.clear()
        files = self.get_json_files(folder)
        if files:
            combo.addItems(files)
        else:
            combo.addItem("无可用文件")
        idx = combo.findText(filename)
        if idx >= 0:
            combo.setCurrentIndex(idx)
        combo.blockSignals(False)

    def delete_template(self, combo, folder, label, combo_index):
        """删除当前选中的模板文件

        Args:
            combo: 对应的下拉框
            folder: 模板文件夹路径
            label: 类型标签（如"基础模板"）
            combo_index: 1=基础模板, 2=附加数据, 3=关联数据
        """
        current = combo.currentText()
        if not current or current == "无可用文件":
            print(f"没有可删除的{label}文件")
            return

        reply = QtWidgets.QMessageBox.question(
            self, "删除确认",
            f"确定要删除{label} \"{current}\" 吗？\n此操作不可撤销。",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        file_path = os.path.join(folder, f"{current}.json")
        try:
            os.remove(file_path)
            print(f"已删除{label}: {file_path}")
        except Exception as e:
            print(f"删除{label}失败: {e}")
            return

        # 刷新下拉框
        combo.blockSignals(True)
        combo.clear()
        files = self.get_json_files(folder)
        if files:
            combo.addItems(files)
        else:
            combo.addItem("无可用文件")
        combo.blockSignals(False)

        # 删除后联动刷新下方动态行：combo 1/2 → 重建行, combo 3 → 刷新关联映射
        if combo_index in (1, 2):
            self.update_dynamic_rows_from_json()
        elif combo_index == 3:
            self.load_association_data(combo.currentText())
            self.update_all_rows_with_association()


# 全局变量用于存储窗口实例
window = Window()
if __name__ == '__main__':
    window.show()
