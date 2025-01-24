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
# 载入完dna文件后，断开骨骼链接，修改骨骼属性后运行,目前默认修改张嘴
#################################################################################################

def load_date(base_face,reader):
    all_date = []
    getJointGroupCount = reader.getJointGroupCount()  # 获取骨骼组指数
    # print('骨骼组数量:' + str(getJointGroupCount))
    getRawControlName = reader.getRawControlName(base_face)
    print('需要修改的初始表情：' + str(base_face))
    print('基础表情名称:' + str(getRawControlName))
    # 查询所有组中是否有要修改的主表情
    # max = 0
    for j in range(0, getJointGroupCount):  #
        getJointGroupInputIndices = reader.getJointGroupInputIndices(j)  # 获取骨骼组所关联的微表情
        # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
        joint_group = []
        base_face_in_joint_group_indices = 0
        for i in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[i] == base_face:
                joint_group = j  # 骨骼组
                base_face_in_joint_group_indices = i  # 需要修改的基础表情在属性列表所含数据的位置
                break
        if joint_group:  # 如果骨骼组存在则创建骨骼组和骨骼字典
            group_with_values = []
            getJointGroupOutputIndices = reader.getJointGroupOutputIndices(j)  # 获取骨骼组所关联的属性
            # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
            # 按属性数量拆解值到新列表
            joint_value = []
            getJointGroupValues = reader.getJointGroupValues(j)  # 获取骨骼组所关联的微表情所含的属性值
            # print('getJointGroupValues:' + str(len(getJointGroupValues)) + str(getJointGroupValues))
            for x in range(0,len(getJointGroupOutputIndices)):
                ls_list = []
                for k in range(0,len(getJointGroupInputIndices)):
                    ls_list.append(getJointGroupValues[len(getJointGroupInputIndices)*x+k])
                joint_value.append(ls_list)
            # print(joint_value)
            # 建立修改列表
            ls_list = [joint_group, joint_value,base_face_in_joint_group_indices]
            group_with_values.append(ls_list)
            all_date.append(group_with_values)
    print('表情数据加载完毕')
    return all_date
def write_date(all_date,reader,writer):
    getJointCount = reader.getJointCount()  # 获取骨骼指数
    # print('骨骼数量:' + str(getJointCount))
    attr = []
    for j in range(0, getJointCount):
        getJointName = reader.getJointName(j)  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
        list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ','scaleX','scaleY','scaleZ']
        for at in list:
            joint_name = getJointName
            ls_list = [j, joint_name, at]
            attr.append(ls_list)
    # print('所有骨骼属性:' + str(len(attr)) + str(attr))
    for n in range(0,len(all_date)):
        group_all_date = all_date[n][0]
        joint_group = group_all_date[0]  # 获取骨骼组名称
        joint_value = group_all_date[1]  # 获取按属性拆分的值
        base_face_in_joint_group_indices = group_all_date[2]  # 获取骨骼组中需要修改的表情再所关联的所有表情的位置
        getJointGroupInputIndices = reader.getJointGroupInputIndices(joint_group)  # 获取骨骼组所关联的微表情
        # 获取属性列表以及其关联的属性
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(joint_group)  # 获取骨骼组所关联的属性
        for i in range(0, len(getJointGroupOutputIndices)):  # 骨骼组中所有表情
            for j in range(0, len(attr)):  # 所有骨骼的属性
                if j == getJointGroupOutputIndices[i]:
                    translate = cmds.xform((attr[j][1]),q=1,t=1)  # 获取当前骨骼位移
                    getNeutralJointTranslation = reader.getNeutralJointTranslation(attr[j][0])  # 获取默认状态位移
                    rotate = cmds.getAttr(attr[j][1] + '.rotate')[0]  # 获取旋转值
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
                    num = now_num - base_num  # 重计算驱动数值
                    joint_value[i][base_face_in_joint_group_indices] = num
                    break
        # 开始修改值
        new_values = []
        for i in range(0, len(joint_value)):
            for x in range(0, len(getJointGroupInputIndices)):
                new_values.append(joint_value[i][x])
        writer.setJointGroupValues(joint_group, new_values)  # 修改数据
    writer.write()  # 写入数据
    print('写入新文件完毕')
date = load_date(191,reader)
write_date(date,reader,writer)
print('已经全部运行，请加载新dna查看效果')


