#coding=gbk
from os import path as ospath
from sys import path as syspath
from sys import platform
import maya.cmds as cmds
import os
import inspect


# 版本号
maya_version = cmds.about(version=True)
if maya_version == '2022' or maya_version == '2023':
    # 文件路径
    file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    ROOT_DIR = file_path + '/MetaHuman-DNA-Calibration-main'
    MAYA_VERSION = maya_version  # 2022 or 2023
    ROOT_LIB_DIR = f"{ROOT_DIR}/lib/Maya{MAYA_VERSION}"
    if platform == "win32":
        LIB_DIR = f"{ROOT_LIB_DIR}/windows"
    elif platform == "linux":
        LIB_DIR = f"{ROOT_LIB_DIR}/linux"
    else:
        raise OSError(
            "OS not supported, please compile dependencies and add value to LIB_DIR"
        )

    # Adds directories to path
    syspath.insert(0, ROOT_DIR)
    syspath.insert(0, LIB_DIR)

    # This example is intended to be used in Maya
    import dna_viewer
    dna_viewer.show()
else:
    cmds.warning('仅支持maya2022和maya2023，如尝试在别的版本运行请自行修改。')
