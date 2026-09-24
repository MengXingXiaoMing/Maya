#coding=gbk
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import maya.OpenMayaUI as Omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
from functools import wraps
import importlib




class CustomListViewDialog(QtWidgets.QDialog):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        super(CustomListViewDialog, self).__init__(parent)

        self.setWindowTitle("Maya 列表视图工具")
        self.setMinimumSize(400, 500)
        # 移除帮助按钮（Windows系统）[1](@ref)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.populate_list_view()

    def create_widgets(self):
        """创建界面控件"""
        # 列表视图
        self.list_view = QtWidgets.QListView()
        self.list_model = QtGui.QStandardItemModel(self.list_view)
        self.list_view.setModel(self.list_model)

        # 第一组单选按钮：显示模式
        self.display_mode_label = QtWidgets.QLabel("显示模式:")
        self.wireframe_rb = QtWidgets.QRadioButton("线框模式")
        self.solid_rb = QtWidgets.QRadioButton("实体模式")
        self.textured_rb = QtWidgets.QRadioButton("纹理模式")
        self.textured_rb.setChecked(True)

        # 第二组单选按钮：操作类型
        self.operation_label = QtWidgets.QLabel("操作类型:")
        self.select_rb = QtWidgets.QRadioButton("选择")
        self.hide_rb = QtWidgets.QRadioButton("隐藏")
        self.delete_rb = QtWidgets.QRadioButton("删除")
        self.select_rb.setChecked(True)

        # 按钮
        self.apply_btn = QtWidgets.QPushButton("应用")
        self.close_btn = QtWidgets.QPushButton("关闭")

    def create_layouts(self):
        """创建布局"""
        main_layout = QtWidgets.QVBoxLayout(self)

        # 列表视图部分
        list_label = QtWidgets.QLabel("场景对象列表:")
        main_layout.addWidget(list_label)
        main_layout.addWidget(self.list_view)

        # 第一组单选按钮
        main_layout.addWidget(self.display_mode_label)

        display_layout = QtWidgets.QHBoxLayout()
        display_layout.addWidget(self.wireframe_rb)
        display_layout.addWidget(self.solid_rb)
        display_layout.addWidget(self.textured_rb)
        main_layout.addLayout(display_layout)

        # 第二组单选按钮
        main_layout.addWidget(self.operation_label)

        operation_layout = QtWidgets.QHBoxLayout()
        operation_layout.addWidget(self.select_rb)
        operation_layout.addWidget(self.hide_rb)
        operation_layout.addWidget(self.delete_rb)
        main_layout.addLayout(operation_layout)

        # 按钮布局
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)
        main_layout.addLayout(button_layout)

        # 创建按钮组确保单选按钮互斥[9](@ref)
        self.display_group = QtWidgets.QButtonGroup(self)
        self.display_group.addButton(self.wireframe_rb)
        self.display_group.addButton(self.solid_rb)
        self.display_group.addButton(self.textured_rb)

        self.operation_group = QtWidgets.QButtonGroup(self)
        self.operation_group.addButton(self.select_rb)
        self.operation_group.addButton(self.hide_rb)
        self.operation_group.addButton(self.delete_rb)

    def create_connections(self):
        """创建信号连接"""
        self.apply_btn.clicked.connect(self.apply_changes)
        self.close_btn.clicked.connect(self.close)
        self.list_view.doubleClicked.connect(self.on_item_double_clicked)

        # 单选按钮组信号连接[9](@ref)
        self.display_group.buttonClicked.connect(self.on_display_mode_changed)
        self.operation_group.buttonClicked.connect(self.on_operation_changed)

    def populate_list_view(self):
        """填充列表视图数据"""
        # 获取Maya场景中的几何体
        geometries = cmds.ls(geometry=True)
        self.list_model.clear()

        for geo in geometries:
            item = QtGui.QStandardItem(geo)
            item.setCheckable(True)
            self.list_model.appendRow(item)

    def on_item_double_clicked(self, index):
        """处理列表项双击事件"""
        item = self.list_model.itemFromIndex(index)
        item_text = item.text()
        cmds.select(item_text)
        print(f"已选择: {item_text}")

    def on_display_mode_changed(self, button):
        """处理显示模式更改"""
        print(f"显示模式改为: {button.text()}")

        # 实际应用中这里可以添加更改显示模式的代码
        if button == self.wireframe_rb:
            cmds.modelEditor(cmds.getPanel(withLabel="模型面板1"), e=True, displayAppearance="wireframe")
        elif button == self.solid_rb:
            cmds.modelEditor(cmds.getPanel(withLabel="模型面板1"), e=True, displayAppearance="smoothShaded")
        elif button == self.textured_rb:
            cmds.modelEditor(cmds.getPanel(withLabel="模型面板1"), e=True, displayAppearance="smoothShaded")
            cmds.modelEditor(cmds.getPanel(withLabel="模型面板1"), e=True, useDefaultMaterial=False)

    def on_operation_changed(self, button):
        """处理操作类型更改"""
        print(f"操作类型改为: {button.text()}")

    def apply_changes(self):
        """应用更改"""
        selected_items = []
        for row in range(self.list_model.rowCount()):
            item = self.list_model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                selected_items.append(item.text())

        if not selected_items:
            cmds.warning("请至少选择一个对象")
            return

        operation = self.operation_group.checkedButton().text()

        # 根据选择的操作类型执行相应操作
        if operation == "选择":
            cmds.select(selected_items)
            print(f"已选择: {selected_items}")
        elif operation == "隐藏":
            for obj in selected_items:
                cmds.hide(obj)
            print(f"已隐藏: {selected_items}")
        elif operation == "删除":
            result = cmds.confirmDialog(title="确认删除", message="确定要删除选中的对象吗?", button=["是", "否"], defaultButton="是",
                                        cancelButton="否", dismissString="否")
            if result == "是":
                try:
                    cmds.delete(selected_items)
                    self.populate_list_view()  # 刷新列表
                    print("删除完成")
                except Exception as e:
                    cmds.warning(f"删除失败: {str(e)}")


# 显示对话框的函数
def show_custom_dialog():
    """显示自定义对话框"""
    try:
        # 如果窗口已存在，先关闭它
        global custom_dialog
        custom_dialog.close()
        custom_dialog.deleteLater()
    except:
        pass

    custom_dialog = CustomListViewDialog()
    custom_dialog.show()


# 在Maya中运行此代码后，执行show_custom_dialog()即可显示窗口
if __name__ == "__main__":
    show_custom_dialog()




sel = cmds.ls(sl=1)
print(len(sel))
print(4093*178)
for s in sel:
    cmds.select(cl=1)
    joint = cmds.joint()
    cmds.pointConstraint(s,joint)


sel = cmds.ls(sl=1)
# 获取所有顶点并添加进列表
all_point = []
all_point_position = []
for s in sel:
    point = cmds.ls(s+'.cv[*][*]', fl=1)
    for p in point:
        all_point.append(p)
        position = cmds.xform(p, query=True, worldSpace=True, translation=True)
        all_point_position.append(position)
print(all_point)
# 开始按位置创建蔟
d = 0
i = 0  # 初始化索引
while all_point:
    need_create_cluster = []
    obj_name = all_point[i]
    obj_position = all_point_position[i]
    all_point.pop(i)
    all_point_position.pop(i)
    need_create_cluster.append(obj_name)
    j = 0
    need_delect_liist = []
    while j < len(all_point):
        p2 = all_point_position[j]
        dx = obj_position[0] - p2[0]
        dy = obj_position[1] - p2[1]
        dz = obj_position[2] - p2[2]
        distance_squared = dx * dx + dy * dy + dz * dz
        # 比较距离的平方和阈值的平方
        if distance_squared < 0.001 * 0.001:
            need_create_cluster.append(all_point[j])
            # 删除后，列表变短，下一个元素会移动到当前位置
            # 所以我们 **不** 增加 i，让下一次循环检查新移动过来的元素
            all_point.pop(j) # pop(i) 会删除索引 i 处的元素并返回它
            all_point_position.pop(j)
        else:
            j += 1
    cmds.cluster(need_create_cluster)
    d += 1
    print('创建蔟', d)

def find_close_points_brute_force(points, threshold=0.001):
    """
    使用双重循环找出所有距离小于阈值的点对。
    返回一个列表，每个元素是一个包含两个点索引的元组 [(i1, j1), (i2, j2), ...]。
    """
    close_pairs = []
    num_points = len(points)

    # 外层循环从第一个点到倒数第二个点
    for i in range(num_points - 1):
        p1 = points[i]
        # 内层循环从 i 的下一个点开始，避免重复比较和自身比较
        for j in range(i + 1, num_points):
            p2 = points[j]

            # 计算两点距离的平方（避免开方，提高效率）
            dx = p1[0] - p2[0]
            dy = p1[1] - p2[1]
            dz = p1[2] - p2[2]
            distance_squared = dx * dx + dy * dy + dz * dz

            # 比较距离的平方和阈值的平方
            if distance_squared < threshold * threshold:
                close_pairs.append((i, j))

    return close_pairs