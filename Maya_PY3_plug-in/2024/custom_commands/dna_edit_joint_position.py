#coding=gbk
from os import makedirs
from os import path as ospath
import maya.cmds as cmds
from sys import path as syspath
from sys import platform
import os
import inspect

# �汾��
maya_version = cmds.about(version=True)
#################################################################################################
# ���ֶ��޸�����·��������Ĭ�ϵĻ��Ͳ��ø���
reader = []
writer = []
if maya_version == '2022' or maya_version == '2023':
# �ļ�·��
    file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    # print('·��:',file_path)
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
    print("Maya�汾����,��֧��2022��2023�汾���糢���ٱ�İ汾�������޸ġ�")
#################################################################################################
def edit_joint_tr():
    getJointCount = reader.getJointCount()
    print('getJointCount:'+str(getJointCount))
    need_write_translate_list = []
    need_write_rotate_list = []
    for i in range(getJointCount):
        # ��ȡ��������
        getJointName = reader.getJointName(i)
        print('getJointName:'+str(getJointName))
        # ��ȡλ����ֵ
        translate = cmds.xform(getJointName, q=True, t=True)
        print(translate)
        # ��ȡ��ת��ֵ
        rotate = cmds.xform(getJointName, q=True, ro=True)
        print(rotate)
        # ��ȡ���е���ת��ֵ
        getNeutralJointRotation = reader.getNeutralJointRotation(i)
        print('getJointName:'+str(getNeutralJointRotation))
        # ����λ����ֵ�б�
        need_write_translate_list.append(translate)
        # �ؼ��㲢�����ת��ֵ�б�
        for j in range(0,len(getNeutralJointRotation)):
            getNeutralJointRotation[j] = getNeutralJointRotation[j] + rotate[j]
        need_write_rotate_list.append(getNeutralJointRotation)

    writer.setNeutralJointTranslations(need_write_translate_list)
    writer.setNeutralJointRotations(need_write_rotate_list)
    writer.write()  # д������
    print('д�����ļ����')
    print('�Ѿ�ȫ�����У��������dna�鿴Ч��')
edit_joint_tr()

