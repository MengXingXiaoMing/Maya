# -*- coding: utf-8 -*-
import random
import maya.mel as mel
import maya.cmds as cmds
# 获取文件路径
import os
import sys
import inspect
import importlib
from functools import partial


from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *


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
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

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

class Common:
    def __init__(self):
        # 文件路径
        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        # 根路径
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
        # 版本号
        self.maya_version = cmds.about(version=True)
    # 加载对应后缀文件名称并返回
    def load_file_fame_of_the_corresponding_suffix(self, file_path, have_suffix, *all_suffix):
        files = os.listdir(file_path)  # 获取文件夹下所有文件名称
        Out = []
        for suffix in all_suffix:
            for file in files:
                if not os.path.splitext(file)[1]:
                    continue
                if file == '__init__.py':
                    continue
                if os.path.splitext(file)[1] in suffix:  # 找到指定后缀的文件
                    if (have_suffix > 0):
                        Out.append(file)  # 将元素添加到列表最后
                    else:
                        Out.append(os.path.splitext(file)[0])  # 将元素添加到列表最后
        return (Out)
    #运行对应命令,括号内为完整路径
    def run_corresponding_command(self,file_path):
        FileName = file_path.split('/')
        Name = FileName[len(FileName)-1].split('.')
        if Name[1]=='mel':
            mel.eval('source ('+file_path+');')
        if Name[1]=='py':
            import maya.app.general.executeDroppedPythonFile as myTempEDPF
            myTempEDPF.executeDroppedPythonFile(file_path, "")
            del myTempEDPF

    # 导入导出文件
    def import_export_file(self,name, import_additional_path, imp_exp_file,file_type):
        #name = cmds.optionMenu(ImportFileName, q=1, value=1)

        suffix = ''
        if file_type == 'mayaAscii':
            suffix = '.ma'
        if file_type == 'mayaBinary':
            suffix = '.mb'
        print('performFileDropAction  ("' + import_additional_path + '/' + name + suffix + '");')
        if imp_exp_file == 1:  # 导入
            cmds.file(import_additional_path + '/' + name + suffix,
                pr=1, ignoreVersion=1, i=1, type=file_type, importFrameRate=True, namespace=":",
                importTimeRange="override", ra=True, mergeNamespacesOnClash=True, options="v=0;")
            # mel.eval('performFileDropAction  ("' + import_additional_path + '/' + name + suffix+'");')
        else:  # mayaAscii#mayaBinary#导出
            cmds.file((import_additional_path + '/' + name + suffix), pr=1, typ=file_type, force=1,
                         options="v=0;", es=1)
