# -*- coding: utf-8 -*-

from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)
class WindowClass():
    def __init__(self):
        pass
    def Window(self):
        window = QWidget()
        window.setWindowTitle('这是一个窗口')
        window.resize(500, 500)
        window.move(100, 100)

        vbox = QVBoxLayout()
        window.setLayout(vbox)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch(1)

        label = QLabel(window)
        label.setText('你好世界！')
        labelA = QLabel(window)
        labelA.setText('你好世界！')
        labelB = QLabel(window)
        labelB.setText('你好世界！')
        labelC = QLabel(window)
        labelC.setText('你好世界！')
        hbox.addWidget(label)
        hbox.addWidget(labelA)
        hbox.addStretch(1)
        hbox.addWidget(labelB)
        hbox.addWidget(labelC)

        vbox.addStretch(1)

        text = label.text()
        print(text)

        for i in range(0,5):
            locals()['New_label'+str(i)] = QLabel(window)
            locals()['New_label'+str(i)].setText('Hello Word!'+str(i))
            vbox.addWidget(locals()['New_label'+str(i)])

        locals()['New_label2'] = locals()['New_label2'].text()
        print(locals()['New_label2'])

        vbox.addStretch(1)
        window.show()
        sys.exit(app.exec_())


ShowWindow = WindowClass()
if __name__ == '__main__':
    ShowWindow.Window()
# 还差自动保存和数字替换成字母
#ShowWindow.Window()