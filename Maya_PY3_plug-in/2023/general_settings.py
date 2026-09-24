# -*- coding: utf-8 -*-
# 必定导入
import os
import sys
import shutil
# 其他导入
import inspect
import importlib
import json
import math
import random
import time
import webbrowser
from datetime import datetime
from functools import partial, wraps
from traceback import format_exception
import re

# Maya相关导入
import maya.mel as mel
import maya.OpenMayaUI as Omui
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.app.general.artAttrSkinJointMenuUpdater as skinUpdater
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as omui
import ast



import maya.cmds as cmds
# 版本号
maya_version_base = cmds.about(version=True)
maya_version_int_base = int(maya_version_base)
if maya_version_int_base >= 2025:
    # print('maya版本等于2025')
    # PySide6相关导入
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                   QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QAbstractItemView,
                                   QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QToolButton,
                                   QMenu, QScrollArea, QFrame, QSplitter, QMenuBar, QFileDialog)
    from PySide6.QtCore import Qt, Signal, QSize, QPoint, QTimer
    from shiboken6 import wrapInstance
    import shiboken6
if maya_version_int_base < 2025:
    # print('maya版本小于2025')
    # PySide2相关导入

    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from shiboken2 import wrapInstance
    from PySide2.QtGui import QIcon, QPixmap, QPainter
    from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                   QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QAbstractItemView,
                                   QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QToolButton,
                                   QMenu, QScrollArea, QFrame, QSplitter, QMenuBar, QFileDialog, QAbstractItemDelegate)
    from PySide2.QtCore import Qt, Signal, QSize, QPoint, QTimer
    import shiboken2
    # from PySide2.QtCore import Signal, Qt, QObject, QEvent

    # from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
    # from PySide2.QtMultimediaWidgets import QVideoWidget














