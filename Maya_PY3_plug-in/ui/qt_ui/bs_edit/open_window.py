#coding=gbk
import sys
# ��ȡ�ļ�·��
import os
import inspect
import importlib
import maya.cmds as cmds
# �ļ�·��
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# ��·��
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# �汾��
maya_version = cmds.about(version=True)
# ��·��
library = root_path + '\\' + maya_version

sys.path.append(file_path)

import bs_edit_window
importlib.reload(bs_edit_window)
from bs_edit_window import *
window.show()

