# -*- coding: utf-8 -*-
import importlib

import maya.cmds as cmds
import maya.mel as mel
# 获取文件路径
import os
import sys
import inspect
import webbrowser
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

# 模型处理
class Model:
    # 按拓扑传递UV
    def transfer_uv(self, soure, target, transfer_method):
        UVsetA = cmds.polyUVSet(soure, q=1, currentUVSet=1)[0]
        UVsetB = cmds.polyUVSet(target, q=1, currentUVSet=1)[0]
        if transfer_method == 0:
            cmds.transferAttributes(soure, target, flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace=UVsetA,
                                    searchMethod=3,
                                    transferNormals=0, transferColors=2, targetUvSpace=UVsetB, colorBorders=1,
                                    sampleSpace=5)
            cmds.warning('按拓扑传递UV完成')
        if transfer_method == 1:
            cmds.transferAttributes(flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace=str(UVsetA),
                                    searchMethod=3,
                                    transferNormals=0, transferColors=2, targetUvSpace=str(UVsetB), colorBorders=1,
                                    sampleSpace=0)
            cmds.warning('按位置传递UV完成')
        cmds.select(target, r=1)
        cmds.DeleteHistory()
