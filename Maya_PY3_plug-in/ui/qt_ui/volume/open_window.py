# -*- coding: utf-8 -*-
import sys
import os
import inspect
import importlib
import maya.cmds as cmds

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

sys.path.append(file_path)

import volume_window
importlib.reload(volume_window)
from volume_window import *
window.show()
