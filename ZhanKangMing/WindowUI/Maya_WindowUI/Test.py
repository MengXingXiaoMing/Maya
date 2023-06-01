from PySide2 import QtWidgets, QtCore, QtGui
from maya import mel
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import random

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)


class CreatePolygonUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(CreatePolygonUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setObjectName('CreatePolygonUI_uniqueId')
        self.setWindowTitle('Create polygon')
        self.setGeometry(50, 50, 250, 150)
        self.initUI()
        self.cmd = 'polyCone'

    def initUI(self):
        self.combo = QComboBox(self)
        self.combo.addItem('Cone')
        self.combo.addItem('Cube')
        self.combo.addItem('Sphere')
        self.combo.addItem('Torus')
        self.combo.setCurrentIndex(0)
        self.combo.move(20, 20)
        self.combo.activated[str].connect(self.combo_onActivated)

        self.button = QPushButton('Create', self)
        self.button.move(20, 50)
        self.button.clicked.connect(self.button_onClicked)

    def combo_onActivated(self, text):
        self.cmd = 'poly' + text + '()'

    def button_onClicked(self):
        mel.eval(self.cmd)


class MyWidget(QtWidgets.QWidget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "妤把我志快找 技我把"]
    self.button = QtWidgets.QPushButton("Click me!")
    self.text = QtWidgets.QLabel("Hello World")
    self.text.setAlignment(QtCore.Qt.AlignCenter)
    self.layout = QtWidgets.QVBoxLayout()
    self.layout.addWidget(self.text)
    self.layout.addWidget(self.button)
    self.setLayout(self.layout)
    self.button.clicked.connect(self.magic)

  def magic(self):
    self.text.setText(random.choice(self.hello))

def main():
    ui = CreatePolygonUI()
    ui.show()
    return ui


if __name__ == '__main__':
    #main()
    ui1=MyWidget()
    #ui1.show()


import pymel.core as pm
print('selected: ', pm.channelBox('mainChannelBox',q=True,sma=True))
