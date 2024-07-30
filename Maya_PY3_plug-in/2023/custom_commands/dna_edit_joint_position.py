#coding=gbk
from os import makedirs
from os import path as ospath
import maya.cmds as cmds
from sys import path as syspath
from sys import platform
import os
import inspect

# 版本号
maya_version = cmds.about(version=True)
#################################################################################################
# 请手动修改以下路径，都是默认的话就不用改了
reader = []
writer = []
if maya_version == '2022' or maya_version == '2023':
# 文件路径
    file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    # print('路径:',file_path)
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
    from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter

    flie = f"{ROOT_DIR}/data/mh4/dna_files/Ada.dna"
    stream = FileStream(flie, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    flie = f"{ROOT_DIR}/data/mh4/dna_files/Ada_modify.dna"
    stream = FileStream(flie, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
else:
    print("Maya版本错误,仅支持2022和2023版本，如尝试再别的版本请自行修改。")
#################################################################################################
def edit_joint_tr():
    getJointCount = reader.getJointCount()
    print('getJointCount:'+str(getJointCount))
    need_write_translate_list = []
    need_write_rotate_list = []
    for i in range(getJointCount):
        # 获取骨骼名称
        getJointName = reader.getJointName(i)
        print('getJointName:'+str(getJointName))
        # 获取位移数值
        translate = cmds.xform(getJointName, q=True, t=True)
        print(translate)
        # 获取旋转数值
        rotate = cmds.xform(getJointName, q=True, ro=True)
        print(rotate)
        # 获取已有的旋转数值
        getNeutralJointRotation = reader.getNeutralJointRotation(i)
        print('getJointName:'+str(getNeutralJointRotation))
        # 重组位移数值列表
        need_write_translate_list.append(translate)
        # 重计算并组合旋转数值列表
        for j in range(0,len(getNeutralJointRotation)):
            getNeutralJointRotation[j] = getNeutralJointRotation[j] + rotate[j]
        need_write_rotate_list.append(getNeutralJointRotation)

    writer.setNeutralJointTranslations(need_write_translate_list)
    writer.setNeutralJointRotations(need_write_rotate_list)
    writer.write()  # 写入数据
    print('写入新文件完毕')
    print('已经全部运行，请加载新dna查看效果')
edit_joint_tr()

