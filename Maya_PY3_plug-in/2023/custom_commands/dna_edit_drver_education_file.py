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
# ������dna�ļ��󣬶Ͽ��������ӣ��޸Ĺ������Ժ�����,ĿǰĬ���޸�����
#################################################################################################

def load_date(base_face,reader):
    all_date = []
    getJointGroupCount = reader.getJointGroupCount()  # ��ȡ������ָ��
    # print('����������:' + str(getJointGroupCount))
    getRawControlName = reader.getRawControlName(base_face)
    print('��Ҫ�޸ĵĳ�ʼ���飺' + str(base_face))
    print('������������:' + str(getRawControlName))
    # ��ѯ���������Ƿ���Ҫ�޸ĵ�������
    # max = 0
    for j in range(0, getJointGroupCount):  #
        getJointGroupInputIndices = reader.getJointGroupInputIndices(j)  # ��ȡ��������������΢����
        # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
        joint_group = []
        base_face_in_joint_group_indices = 0
        for i in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[i] == base_face:
                joint_group = j  # ������
                base_face_in_joint_group_indices = i  # ��Ҫ�޸ĵĻ��������������б��������ݵ�λ��
                break
        if joint_group:  # �������������򴴽�������͹����ֵ�
            group_with_values = []
            getJointGroupOutputIndices = reader.getJointGroupOutputIndices(j)  # ��ȡ������������������
            # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
            # �������������ֵ�����б�
            joint_value = []
            getJointGroupValues = reader.getJointGroupValues(j)  # ��ȡ��������������΢��������������ֵ
            # print('getJointGroupValues:' + str(len(getJointGroupValues)) + str(getJointGroupValues))
            for x in range(0,len(getJointGroupOutputIndices)):
                ls_list = []
                for k in range(0,len(getJointGroupInputIndices)):
                    ls_list.append(getJointGroupValues[len(getJointGroupInputIndices)*x+k])
                joint_value.append(ls_list)
            # print(joint_value)
            # �����޸��б�
            ls_list = [joint_group, joint_value,base_face_in_joint_group_indices]
            group_with_values.append(ls_list)
            all_date.append(group_with_values)
    print('�������ݼ������')
    return all_date
def write_date(all_date,reader,writer):
    getJointCount = reader.getJointCount()  # ��ȡ����ָ��
    # print('��������:' + str(getJointCount))
    attr = []
    for j in range(0, getJointCount):
        getJointName = reader.getJointName(j)  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
        list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ','scaleX','scaleY','scaleZ']
        for at in list:
            joint_name = getJointName
            ls_list = [j, joint_name, at]
            attr.append(ls_list)
    # print('���й�������:' + str(len(attr)) + str(attr))
    for n in range(0,len(all_date)):
        group_all_date = all_date[n][0]
        joint_group = group_all_date[0]  # ��ȡ����������
        joint_value = group_all_date[1]  # ��ȡ�����Բ�ֵ�ֵ
        base_face_in_joint_group_indices = group_all_date[2]  # ��ȡ����������Ҫ�޸ĵı����������������б����λ��
        getJointGroupInputIndices = reader.getJointGroupInputIndices(joint_group)  # ��ȡ��������������΢����
        # ��ȡ�����б��Լ������������
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(joint_group)  # ��ȡ������������������
        for i in range(0, len(getJointGroupOutputIndices)):  # �����������б���
            for j in range(0, len(attr)):  # ���й���������
                if j == getJointGroupOutputIndices[i]:
                    translate = cmds.xform((attr[j][1]),q=1,t=1)  # ��ȡ��ǰ����λ��
                    getNeutralJointTranslation = reader.getNeutralJointTranslation(attr[j][0])  # ��ȡĬ��״̬λ��
                    rotate = cmds.getAttr(attr[j][1] + '.rotate')[0]  # ��ȡ��תֵ
                    now_num = 0
                    base_num = 0
                    if attr[j][2] == 'translateX':
                        now_num = translate[0]
                        base_num = getNeutralJointTranslation[0]
                    if attr[j][2] == 'translateY':
                        now_num = translate[1]
                        base_num = getNeutralJointTranslation[1]
                    if attr[j][2] == 'translateZ':
                        now_num = translate[2]
                        base_num = getNeutralJointTranslation[2]
                    if attr[j][2] == 'rotateX':
                        now_num = rotate[0]
                        base_num = 0
                    if attr[j][2] == 'rotateY':
                        now_num = rotate[1]
                        base_num = 0
                    if attr[j][2] == 'rotateZ':
                        now_num = rotate[2]
                        base_num = 0
                    # print(attr[j][1] + '.' + attr[j][2])
                    # print(now_num)
                    # print(base_num)
                    num = now_num - base_num  # �ؼ���������ֵ
                    joint_value[i][base_face_in_joint_group_indices] = num
                    break
        # ��ʼ�޸�ֵ
        new_values = []
        for i in range(0, len(joint_value)):
            for x in range(0, len(getJointGroupInputIndices)):
                new_values.append(joint_value[i][x])
        writer.setJointGroupValues(joint_group, new_values)  # �޸�����
    writer.write()  # д������
    print('д�����ļ����')
date = load_date(191,reader)
write_date(date,reader,writer)
print('�Ѿ�ȫ�����У��������dna�鿴Ч��')


