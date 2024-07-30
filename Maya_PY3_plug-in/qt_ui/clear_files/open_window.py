#coding=gbk
import sys
# 获取文件路径
import os
import inspect
import importlib
import maya.cmds as cmds
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library = root_path + '\\' + maya_version

sys.path.append(file_path)

import clear_files_window
importlib.reload(clear_files_window)
from clear_files_window import *
window.show()

