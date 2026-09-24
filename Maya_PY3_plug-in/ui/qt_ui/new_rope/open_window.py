#coding=gbk
import sys
# 获取文件路径
import os
import inspect
import importlib
import maya.cmds as cmds
# 文件路径a
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library = root_path + '\\' + maya_version

sys.path.append(file_path)

import new_rope_window
importlib.reload(new_rope_window)
from new_rope_window import *
window.show()
# stretch_condition = cmds.shadingNode('condition', asUtility=1)
        # cmds.connectAttr((self.prefix + 'TotalControl_Curve.stretch'), stretch_condition + '.firstTerm', f=1)
        # cmds.setAttr(stretch_condition + '.colorIfTrueR', 3)
        # cmds.setAttr(stretch_condition + '.colorIfFalseR', 4)
# cmds.connectAttr(stretch_condition + '.outColorR', value_condition + '.operation',f=1)
# 弹簧结算器
#ikSpringSolver