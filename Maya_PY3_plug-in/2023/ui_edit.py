# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
print(root_path)
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

# 编辑ui
class FlowLayout(QLayout):
    def __init__(self, parent=None, h_spacing=-1, v_spacing=-1, *args, **kwargs):
        super(FlowLayout, self).__init__(parent)
        self._h_spacing = h_spacing
        self._v_spacing = v_spacing

        self.itemList = []

    def __del__(self):
        while self.count():
            self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        # return QSize(self.minimumWidth(), self.totalHeight)
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

        # width = max([item.sizeHint().width() for item in self.itemList], default=0)
        # return QSize(width, self.totalHeight)

    def smartSpacing(self, pm):
        if not self.parent():
            return -1
        elif isinstance(self.parent(), QWidget):
            return self.parent().style().pixelMetric(pm, None, self.parent())
        else:
            return self.parent().spacing()

    def horizontalSpacing(self):
        return self._h_spacing if self._h_spacing >= 0 else self.smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        return self._v_spacing if self._v_spacing >= 0 else self.smartSpacing(QStyle.PM_LayoutVerticalSpacing)

    def setHorizontalSpacing(self, value):
        self._h_spacing = value

    def setVerticalSpacing(self, value):
        self._v_spacing = value

    def setSpacing(self, value):
        self.setHorizontalSpacing(value)
        self.setVerticalSpacing(value)
        return super().setSpacing(value)

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(
                    QSizePolicy.CheckBox,
                    QSizePolicy.PushButton,
                    Qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton,
                    Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()
class UiEdit:
    # 将选择的物体加载到ui
    def load_select_for_ui_text(self, soure_ui, soure_ui_type):
        sel = cmds.ls(sl=1, fl=1)
        attribute = cmds.channelBox('mainChannelBox', q=1, sma=1)
        if sel or attribute:
            # 建立具体的文本
            if attribute:
                all_attribute_sel = []
                for i in sel:
                    for j in range(0, len(attribute)):
                        attribute_sel = i + '.' + attribute[j]
                        all_attribute_sel.append(attribute_sel)
                all_sel = all_attribute_sel[0]
                for i in range(1, len(all_attribute_sel)):
                    all_sel = all_sel + ',' + all_attribute_sel[i]
            else:
                all_sel = sel[0]
                for i in range(1, len(sel)):
                    all_sel = all_sel + ',' + sel[i]
            # 有属性加载物体属性，没属性加载物体
            if soure_ui_type[0] == 'QLineEdit':
                soure_ui.setMaxLength(len(all_sel)*100+999999)
                # soure_ui.maxLength(len(all_sel))
                soure_ui.setText(all_sel)
        else:
            cmds.warning('请选择物体或者属性')

    # 自动调整滑块范围且返回数值
    def automatically_adjust_the_slider_range_and_return_the_value(self, soure_ui, soure_ui_type):
        if soure_ui_type == 'QSlider':
            num = soure_ui.sliderPosition()
            min_num = soure_ui.minimum()
            max_num = soure_ui.maximum()

            width = max_num - min_num
            # 判断是否达到前后四分之一的位置
            min_threshold = min_num + width / 10.0
            max_threshold = max_num - width / 10.0

            if num < min_threshold:
                soure_ui.setMinimum(min_num - width)
                soure_ui.setMaximum(max_threshold)
            if num > max_threshold:
                soure_ui.setMinimum(min_threshold)
                soure_ui.setMaximum(max_num + width)
            return num

    # 将数值给到滑块
    def give_the_value_to_the_slider(self, num, target_ui, target_ui_type):
        if target_ui_type == 'QSlider':
            max_num = target_ui.maximum()
            max_num = float(max_num)
            if max_num < num:
                target_ui.setMaximum(num)
            min_num = target_ui.minimum()
            if min_num > num:
                target_ui.setMinimum(num)
            target_ui.setValue(num)

    # 创建带自动生成滑块的界面
    def create_ui_with_auto_slider(self, parent):
        # 创建滚动区域
        scroll_area = QtWidgets.QScrollArea(parent)
        scroll_area.setWidgetResizable(True)  # 关键：允许内容部件调整大小
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        Widget = QtWidgets.QWidget()
        scroll_area.setWidget(Widget)
        flow_layout = FlowLayout(Widget)
        flow_layout.setContentsMargins(0, 0, 0, 0)
        flow_layout.setSpacing(1)
        return scroll_area, Widget, flow_layout