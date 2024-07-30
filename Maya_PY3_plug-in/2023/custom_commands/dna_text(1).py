#coding=gbk

from os import makedirs
from os import path as ospath
import maya.cmds as cmds
# If you use Maya, use absolute path
ROOT_DIR = 'E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main'
OUTPUT_DIR = f"{ROOT_DIR}/output"

CHARACTER_NAME = "Ada"

DATA_DIR = f"{ROOT_DIR}/data"
CHARACTER_DNA = f"{DATA_DIR}/dna_files/{CHARACTER_NAME}.dna"
OUTPUT_DNA = f"{OUTPUT_DIR}/{CHARACTER_NAME}_output.dna"


from dna import DataLayer_All, FileStream, Status, BinaryStreamReader, BinaryStreamWriter


def create_dna(path):
    stream = FileStream(path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)

    # Sets a couple of parameters about in the dna that is about to be created and written to
    writer.setName("rig name")
    writer.setLODCount(4)
    writer.setJointName(0, "spine")
    writer.setJointName(1, "neck")

    writer.setMeshName(0, "head")
    writer.setVertexPositions(0, [[0.0, 0.5, 0.3], [1.0, 3.0, -8.0]])
    writer.setVertexTextureCoordinates(0, [[0.25, 0.55], [1.5, 3.6]])

    # Creates the DNA
    writer.write()
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error saving DNA: {status.message}")


def load_dna(path):
    stream = FileStream(path, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error loading DNA: {status.message}")
    return reader


def print_dna_summary(dna_reader):
    print(f"Name: {dna_reader.getName()}")
    print(f"Joint count: {dna_reader.getJointCount()}")
    joint_names = ", ".join(
        dna_reader.getJointName(i) for i in range(dna_reader.getJointCount())
    )
    print(f"Joint names: {joint_names}")

    for mesh_idx in range(dna_reader.getMeshCount()):
        # Get vertices one by one
        for vtx_id in range(dna_reader.getVertexPositionCount(mesh_idx)):
            vtx = dna_reader.getVertexPosition(mesh_idx, vtx_id)
            print(f"Mesh {mesh_idx} - Vertex {vtx_id} : {vtx}")
        # Get all X / Y / Z coordinates
        print(dna_reader.getVertexPositionXs(mesh_idx))
        print(dna_reader.getVertexPositionYs(mesh_idx))
        print(dna_reader.getVertexPositionZs(mesh_idx))

        for tc_idx in range(dna_reader.getVertexTextureCoordinateCount(mesh_idx)):
            tex_coord = dna_reader.getVertexTextureCoordinate(mesh_idx, tc_idx)
            print(f"Mesh {mesh_idx} - Texture coordinate {tc_idx} : {tex_coord}")


def create_new_dna(dna_path):
    create_dna(dna_path)
    dna_reader = load_dna(dna_path)
    print_dna_summary(dna_reader)

flie = 'D:/scenes/plug-in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada_A.dna'
def print_dna():
    # dna_reader = load_dna('E:\maya_plug_in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna')
    stream = FileStream(
        'E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada.dna',
        FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    stream = FileStream(
        'E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada_A.dna',
        FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    getJointGroupCount_range = reader.getJointGroupCount()
    # '''
    for tempid in range(0, getJointGroupCount_range):  # 125
        print(tempid)
        getJointCount = reader.getJointCount()
        print('getJointCount:'+str(getJointCount))
        getJointName = reader.getJointName(700)
        print('getJointName:'+str(getJointName))
        getJointGroupJointIndices = reader.getJointGroupJointIndices(tempid)
        print('getJointGroupJointIndices:'+str(getJointGroupJointIndices))
        getNeutralJointTranslation = reader.getNeutralJointTranslation(tempid)
        print('getNeutralJointTranslation:'+str(getNeutralJointTranslation))
        getNeutralJointRotation = reader.getNeutralJointRotation(tempid)
        print('getNeutralJointRotation:'+str(getNeutralJointRotation))
        getJointGroupCount = reader.getJointGroupCount()
        print('getJointGroupCount:'+str(getJointGroupCount))
        getJointGroupInputIndices = reader.getJointGroupInputIndices(tempid)
        print('getJointGroupInputIndices:' + str(getJointGroupInputIndices))
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(tempid)
        print('getJointGroupOutputIndices:' + str(getJointGroupOutputIndices))
        getJointGroupCountNew = reader.getJointGroupCount()
        print('getJointGroupCountNew:'+str(getJointGroupCountNew))
        getJointGroupValues = reader.getJointGroupValues(tempid)
        print('getJointGroupValues:'+str(getJointGroupValues))

def modify_dna():
    #dna_reader = load_dna('E:\maya_plug_in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna')
    stream = FileStream('E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada.dna', FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    stream = FileStream('E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada_A.dna', FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    getJointGroupCount_range = reader.getJointGroupCount()
    #'''
    for tempid in range(0,getJointGroupCount_range):#124
        print(tempid)
        getJointCount = reader.getJointCount()
        #print('getJointCount:'+str(getJointCount))
        getJointName = reader.getJointName(tempid)
        print('getJointName:'+str(getJointName))
        getJointGroupJointIndices = reader.getJointGroupJointIndices(tempid)
        #print('getJointGroupJointIndices:'+str(getJointGroupJointIndices))
        getNeutralJointTranslation = reader.getNeutralJointTranslation(tempid)
        #print('getNeutralJointTranslation:'+str(getNeutralJointTranslation))
        getNeutralJointRotation = reader.getNeutralJointRotation(tempid)
        #print('getNeutralJointRotation:'+str(getNeutralJointRotation))
        getJointGroupCount = reader.getJointGroupCount()
        print('getJointGroupCount:'+str(getJointGroupCount))
        getJointGroupLODs = reader.getJointGroupLODs(tempid)
        print('getJointGroupLODs:' + str(getJointGroupLODs))
        getJointGroupJointIndices = reader.getJointGroupJointIndices(tempid)
        print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
        getJointGroupInputIndices =reader.getJointGroupInputIndices(tempid)
        print('getJointGroupInputIndices:'+str(len(getJointGroupInputIndices))+str(getJointGroupInputIndices))
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(tempid)
        print('getJointGroupOutputIndices:'+str(len(getJointGroupOutputIndices))+str(getJointGroupOutputIndices))
        getJointGroupCountNew = reader.getJointGroupCount()
        #print('getJointGroupCountNew:'+str(getJointGroupCountNew))
        getJointGroupValues = reader.getJointGroupValues(tempid)
        #print('getJointGroupValues:'+str(getJointGroupValues))
        values = getJointGroupValues

        '''for i in range(0,len(values)):
            if values[i]:
                values[i] = getJointGroupValues[i]*10'''
        #FACIAL_L_LipLowerSkin
        '''for i in range(0,len(getJointGroupInputIndices)): # 对骨骼进行循环
            if getJointGroupInputIndices[i]<800:
                k = i*len(getJointGroupOutputIndices)
                for n in range(0,len(getJointGroupOutputIndices)): # 对组进行循环
                    values[k+n] = getJointGroupValues[k+n] * 0'''
        for i in range(0, len(getJointGroupOutputIndices)):  # 对组进行循环
            k = i * len(getJointGroupInputIndices)
            for n in range(0, len(getJointGroupInputIndices)):  # 对骨骼进行循环
                if getJointGroupInputIndices[n] < 600:
                    values[k + n] = 0
        print('values:' + str(values))
        writer.setJointGroupValues(tempid, values)
    writer.write()
def modify_dna2():
    #dna_reader = load_dna('E:\maya_plug_in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna')
    stream = FileStream('E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada.dna', FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    stream = FileStream('E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada_A.dna', FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    getJointCount = reader.getJointCount() # 获取骨骼指数
    print('getJointCount:' + str(getJointCount))
    jointCount = 700
    print(jointCount)
    getJointName = reader.getJointName(jointCount) # 获取骨骼名称，骨骼对骨骼组是一对一的关系
    print('getJointName:' + str(getJointName))
    getJointGroupCount = reader.getJointGroupCount() # 获取骨骼组指数
    print('getJointGroupCount:'+str(getJointGroupCount))

    JointToJointGroupOneByOne = 0
    for i in range(0,getJointGroupCount):
        getJointGroupJointIndices = reader.getJointGroupJointIndices(i)  # 获取骨骼组骨骼指数
        for j in range(0,len(getJointGroupJointIndices)):
            if jointCount == getJointGroupJointIndices[j]:
                JointToJointGroupOneByOne = i
                print('骨骼对应的骨骼组'+str(i))
                print('getJointGroupJointIndices(骨骼组所控制的骨骼指数):' + str(len(getJointGroupJointIndices)) + str(getJointGroupJointIndices))
    getJointGroupLODs = reader.getJointGroupLODs(JointToJointGroupOneByOne)  # 获取骨骼组LOD
    print('getJointGroupLODs:' + str(getJointGroupLODs))
    num_1 = 0
    num_2 = 0
    for i in range(0,getJointGroupCount):
        getJointGroupInputIndices = reader.getJointGroupInputIndices(JointToJointGroupOneByOne)
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(JointToJointGroupOneByOne)
        for j in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[j]>num_1:
                num_1 = getJointGroupInputIndices[j]
        for j in range(0,len(getJointGroupOutputIndices)):
            if getJointGroupOutputIndices[j]>num_2:
                num_2 = getJointGroupOutputIndices[j]
    print('微表情数量'+str(num_1+1)) # 814个微表情
    print('属性数量'+str(num_2+1)) # 6720个属性
    getJointGroupInputIndices = reader.getJointGroupInputIndices(JointToJointGroupOneByOne)
    print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
    getJointGroupOutputIndices = reader.getJointGroupOutputIndices(JointToJointGroupOneByOne)
    print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
    getJointGroupValues = reader.getJointGroupValues(JointToJointGroupOneByOne)
    print('getJointGroupValues:'+str(len(getJointGroupValues))+str(getJointGroupValues))
    getArchetype = reader.getAnimatedMapIndexListCount()
    print('getArchetype:' + str(getArchetype))
    print('第' + str(jointCount) + '个骨骼， 名字是' + getJointName + ',对应' + str(
        JointToJointGroupOneByOne) + '号骨骼组，输入索引数量是' + str(len(getJointGroupInputIndices)) +
          ',输出索引数量是' + str(len(getJointGroupOutputIndices)) + ',值数量是' + str(len(getJointGroupValues)))

    getGUIControlCount = reader.getGUIControlCount()
    print('getGUIControlCount:' + str(getGUIControlCount))
    getGUIControlName = reader.getGUIControlName(10)
    print('getGUIControlName:' + str(getGUIControlName))
    getRawControlCount = reader.getRawControlCount()
    print('getRawControlCount:' + str(getRawControlCount))
    getRawControlName = reader.getRawControlName(10)
    print('getRawControlName:' + str(getRawControlName))
    getAnimatedMapCount = reader.getAnimatedMapCount()
    print('getRawControlName:' + str(getAnimatedMapCount))
    getAnimatedMapName = reader.getAnimatedMapName(10)
    print('getAnimatedMapName:' + str(getAnimatedMapName))
    getAnimatedMapIndexListCount = reader.getAnimatedMapIndexListCount()
    print('getAnimatedMapIndexListCount:' + str(getAnimatedMapIndexListCount))
    getGUIToRawInputIndices = reader.getGUIToRawInputIndices()
    print('getGUIToRawInputIndices:' + str(len(getGUIToRawInputIndices)))
    getGUIToRawOutputIndices = reader.getGUIToRawOutputIndices()
    print('getGUIToRawOutputIndices:' + str(len(getGUIToRawOutputIndices)))
    getGUIToRawFromValues = reader.getGUIToRawFromValues()
    print('getGUIToRawFromValues:' + str(len(getGUIToRawFromValues)))
    getGUIToRawToValues = reader.getGUIToRawToValues()
    print('getGUIToRawToValues:' + str(len(getGUIToRawToValues)))
    getGUIToRawSlopeValues = reader.getGUIToRawSlopeValues()
    print('getGUIToRawSlopeValues:' + str(len(getGUIToRawSlopeValues)))
    getGUIToRawCutValues = reader.getGUIToRawCutValues()
    print('getGUIToRawCutValues:' + str(len(getGUIToRawCutValues)))
    getPSDCount = reader.getPSDCount()
    print('getPSDCount:' + str(getPSDCount))
    getJointRowCount = reader.getJointRowCount()
    print('getJointRowCount:' + str(getJointRowCount))
    getJointVariableAttributeIndices = reader.getJointVariableAttributeIndices(0)
    print('getJointVariableAttributeIndices:' + str(len(getJointVariableAttributeIndices)))
    getAnimatedMapInputIndices = reader.getAnimatedMapInputIndices()
    print('ggetAnimatedMapInputIndices:' + str(len(getAnimatedMapInputIndices)))

def modify_dna3():
    #dna_reader = load_dna('E:\maya_plug_in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna')
    stream = FileStream('E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada.dna', FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    stream = FileStream('E:/maya_plug_in/MetaHuman-DNA-Calibration-main/MetaHuman-DNA-Calibration-main/data/mh4/dna_files/Ada_A.dna', FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    Microexpression = 200 # 微表情
    print(Microexpression)
    getJointCount = reader.getJointCount()  # 获取骨骼指数
    #print('骨骼指数:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount()  # 获取骨骼组指数
    #print('骨骼组指数:' + str(getJointGroupCount))
    for g in range(0,getJointGroupCount):  # 循环所有骨骼组
        getJointGroupInputIndices = reader.getJointGroupInputIndices(g) # 获取所有微表情
        #print('骨骼组' + str(g) + ':微表情' + str(len(getJointGroupInputIndices)) + ':' + str(getJointGroupInputIndices))
        Microexpression_in_group_indices = 0
        values = []
        getJointGroupJointIndices = reader.getJointGroupJointIndices(g)  # 获取骨骼组骨骼指数
        # print('骨骼组' + str(g) + '骨骼指数:'+ str(getJointGroupJointIndices))
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(g)  # 获取骨骼组属性
        # print('骨骼组' + str(g) + '骨骼属性:'+ str(getJointGroupOutputIndices))
        getJointGroupValues = reader.getJointGroupValues(g)  # 获取骨骼组值
        # print('骨骼组' + str(g) + '属性值:'+ str(getJointGroupValues))
        values = getJointGroupValues  # 创建一个新变量来保存获取出来的值
        for i in getJointGroupInputIndices:  # 循环此骨骼组中的所有微表情
            if Microexpression != i: # 如果微表情中有要修改的微表情
                start = Microexpression_in_group_indices * len(getJointGroupOutputIndices)  # 获取要修改的微表情的数值记录在值的初始位置
                for j in range(0,len(getJointGroupOutputIndices)):  # 循环修改此微表情所有骨骼属性值
                    values[start+j] = 0
                Microexpression_in_group_indices = Microexpression_in_group_indices + 1
        writer.setJointGroupValues(g, values)  # 写入所有骨骼属性值
        print(values)
    writer.write()
    print('表情修改完毕')
def modify_dna4():
    #dna_reader = load_dna('E:\maya_plug_in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna')
    stream = FileStream(flie, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    stream = FileStream(flie, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    getJointCount = reader.getJointCount() # 获取骨骼指数
    print('getJointCount:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount() # 获取骨骼组指数
    print('getJointGroupCount:' + str(getJointGroupCount))
    attr = []
    for j in range(0,getJointCount):
        getJointName = reader.getJointName(j)  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
        for at in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            attr.append(getJointName+ '.' + at)
    print('attr:'+str(len(attr)))
    # getJointGroupCount = reader.getJointGroupCount()  # 获取骨骼组指数
    # print('getJointGroupCount:' + str(getJointGroupCount))
    # for i in range(0, getJointGroupCount):
    #     getJointGroupJointIndices = reader.getJointGroupJointIndices(i)  # 获取骨骼组骨骼指数
    #     for j in range(0, len(getJointGroupJointIndices)):
    #         getJointName = reader.getJointName(getJointGroupJointIndices[j])  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
    #         print(str(i) + 'getJointName:' + str(getJointName))
    # 118getJointName:FACIAL_C_Jaw
    grp = 118
    print(str(grp))
    getJointGroupJointIndices = reader.getJointGroupJointIndices(grp)  # 获取骨骼组骨骼指数
    print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
    getJointName = reader.getJointName(getJointGroupJointIndices[0])  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
    print('getJointName:' + str(getJointName))
    getJointGroupInputIndices = reader.getJointGroupInputIndices(grp)
    print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
    num = 0
    for i in range(0, getJointGroupCount):
        for j in range(0, len(getJointGroupInputIndices)):
            if num < getJointGroupInputIndices[j]:
                num = getJointGroupInputIndices[j]
    print(num+1)
    getJointGroupOutputIndices = reader.getJointGroupOutputIndices(grp)
    print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
    # for i in range(0, len(getJointGroupOutputIndices)):
    #     print (attr[getJointGroupOutputIndices[i]])
    getJointGroupValues = reader.getJointGroupValues(grp)
    print('getJointGroupValues:' + str(len(getJointGroupValues)) + str(getJointGroupValues))
    # for i in range(0, len(getJointGroupOutputIndices)):
    #     values = []
    #     for j in range(0, len(getJointGroupInputIndices)):
    #         values.append(getJointGroupValues[len(getJointGroupInputIndices) * i + j])
    #     print(values)

    getRawControlCount = reader.getRawControlCount()
    print('getRawControlCount:' + str(getRawControlCount))
    getRawControlName = reader.getRawControlName(118)
    print('getRawControlName:' + str(getRawControlName))
    getGUIControlCount = reader.getGUIControlCount()
    print('getGUIControlCount:' + str(getGUIControlCount))
    getGUIControlName = reader.getGUIControlName(118)
    print('getGUIControlName:' + str(getGUIControlName))
    getJointIndexListCount = reader.getJointIndexListCount()
    print('getJointIndexListCount:' + str(getJointIndexListCount))
    print('')
    getPSDCount = reader.getPSDCount()
    print('getPSDCount:' + str(getPSDCount))
    getPSDRowIndices = reader.getPSDRowIndices()
    print('getPSDRowIndices:'+ str(len(getPSDRowIndices)) + str(getPSDRowIndices))
    getPSDColumnIndices = reader.getPSDColumnIndices()
    print('getPSDColumnIndices:'+ str(len(getPSDColumnIndices)) + str(getPSDColumnIndices))
    getPSDValues = reader.getPSDValues()
    print('getPSDValues:' + str(len(getPSDValues)) + str(getPSDValues))
    getGUIControlCount = reader.getGUIControlCount()
    print('getGUIControlCount:' + str(getGUIControlCount))
    getGUIControlName = reader.getGUIControlName(0)
    print('getGUIControlName:' + str(getGUIControlName))
    getRawControlCount = reader.getRawControlCount()
    print('getRawControlCount:' + str(getRawControlCount))
    getRawControlName = reader.getRawControlName(0)
    print('getRawControlName:' + str(getRawControlName))
    getGUIToRawInputIndices = reader.getGUIToRawInputIndices()
    print('getGUIToRawInputIndices:' + str(len(getGUIToRawInputIndices)))
    getGUIToRawOutputIndices = reader.getGUIToRawOutputIndices()
    print('getGUIToRawOutputIndices:' + str(len(getGUIToRawOutputIndices)))
    getGUIToRawFromValues = reader.getGUIToRawFromValues()
    print('getGUIToRawFromValues:' + str(len(getGUIToRawFromValues)) + str(getGUIToRawFromValues))
    getGUIToRawToValues = reader.getGUIToRawToValues()
    print('getGUIToRawToValues:' + str(len(getGUIToRawToValues)) + str(getGUIToRawToValues))
    getGUIToRawSlopeValues = reader.getGUIToRawSlopeValues()
    print('getGUIToRawSlopeValues:' + str(len(getGUIToRawSlopeValues)) + str(getGUIToRawSlopeValues))
    getGUIToRawCutValues = reader.getGUIToRawCutValues()
    print('getGUIToRawCutValues:' + str(len(getGUIToRawCutValues)) + str(getGUIToRawCutValues))

    print('aaaaa')
    getRawControlCount = reader.getRawControlCount()
    print('getRawControlCount:' + str(getRawControlCount))
    getRawControlName = reader.getRawControlName(118)
    print('getRawControlName:' + str(getRawControlName))
    getPSDCount = reader.getPSDCount()
    print('getPSDCount:' + str(getPSDCount))
    getPSDRowIndices = reader.getPSDRowIndices()
    print('getPSDRowIndices:814:' + str(len(getPSDRowIndices)) + str(getPSDRowIndices))
    num = 1000
    for i in range(len(getPSDRowIndices)):
        if num > getPSDRowIndices[i]:
            num = getPSDRowIndices[i]
    print(num)
    getPSDColumnIndices = reader.getPSDColumnIndices()
    print('getPSDColumnIndices:269:' + str(len(getPSDColumnIndices)) + str(getPSDColumnIndices))
    getGUIControlCount = reader.getGUIControlCount()
    print('getGUIControlCount:' + str(getGUIControlCount))
    getGUIControlName = reader.getGUIControlName(118)
    print('getGUIControlName:' + str(getGUIControlName))
    # for i in getJointGroupInputIndices:
    #     getRawControlName = reader.getRawControlName(i)
    #     print('getRawControlName:' + str(getRawControlName))
    # for jointCount in range(0,jointCount):
    #     getJointName = reader.getJointName(jointCount) # 获取骨骼名称，骨骼对骨骼组是一对一的关系
    #     print('getJointName:' + str(getJointName))
    # getJointGroupCount = reader.getJointGroupCount() # 获取骨骼组指数
    # print('getJointGroupCount:' + str(getJointGroupCount))
    # getGUIControlCount = reader.getGUIControlCount()
    # print('getGUIControlCount:' + str(getGUIControlCount))
    # getGUIControlName = reader.getGUIControlName(10)
    # print('getGUIControlName:' + str(getGUIControlName))

    # getAnimatedMapCount = reader.getAnimatedMapCount()
    # print('getRawControlName:' + str(getAnimatedMapCount))

stream = FileStream(flie, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
reader = BinaryStreamReader(stream, DataLayer_All)
reader.read()
stream = FileStream(flie, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
writer = BinaryStreamWriter(stream)
writer.setFrom(reader)
def Load_the_dictionary_to_be_modified(base_face):
    need_change_values = []
    getJointCount = reader.getJointCount() # 获取骨骼指数
    print('骨骼数量:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount() # 获取骨骼组指数
    print('骨骼组数量:' + str(getJointGroupCount))
    attr = []
    for j in range(0,getJointCount):
        getJointName = reader.getJointName(j)  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
        list = ['tx','ty','tz','rx','ry','rz']
        if j == 93:
            list = ['ty','rx','ry','rz']
        if j == 113:
            list = ['ty','tz','rx','ry','rz']
        for at in list:
            attr.append(getJointName+ '.' + at)
    print('所有骨骼属性:'+str(len(attr)))
    getRawControlCount = reader.getRawControlCount()
    print('基础表情数量:' + str(getRawControlCount))
    # for i in range(0,getRawControlCount):
    #     getRawControlName = reader.getRawControlName(i)
    #     print('基础表情名称:' + str(getRawControlName))
    # base_face = 192
    getRawControlName = reader.getRawControlName(base_face)
    print('需要修改的初始表情：' + str(base_face))
    print('基础表情名称:' + str(getRawControlName))
    getPSDColumnIndices = reader.getPSDColumnIndices()
    print('主表情和微表情关联:' + str(len(getPSDColumnIndices)) + str(getPSDColumnIndices))
    getPSDCount = reader.getPSDCount()
    print('微表情数量:' + str(getPSDCount))
    getPSDRowIndices = reader.getPSDRowIndices()
    print('微表情数量索引:' + str(len(getPSDRowIndices)) + str(getPSDRowIndices))
    need_change_PSD_face = []
    # 查询需要修改基础表情所关联的微表情
    for i in range(0,len(getPSDColumnIndices)):
        if base_face == getPSDColumnIndices[i]:
            need_change_PSD_face.append(getPSDRowIndices[i])
    print('需要修改的微表情:' + str(need_change_PSD_face))
    # 查询所有组中是否有要修改的主表情
    for j in range(0, getJointGroupCount):  #
        getJointGroupInputIndices = reader.getJointGroupInputIndices(j)  # 获取骨骼组所关联的微表情
        # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
        joint_group = []
        base_face_in_joint_group_indices = []
        for i in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[i] == base_face:
                joint_group = j  # 骨骼组
                base_face_in_joint_group_indices = i  # 需要修改的基础表情在骨骼组所含微表情的位置
                break
        if joint_group:  # 如果骨骼组存在则创建骨骼组和骨骼字典
            getJointGroupJointIndices = reader.getJointGroupJointIndices(j)  # 获取骨骼组骨骼指数
            # print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
            getJointGroupOutputIndices = reader.getJointGroupOutputIndices(j)  # 获取骨骼组所关联的属性
            # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
            # 按骨骼数量拆解属性到新列表
            group_attr = []
            for x in range(0,len(getJointGroupJointIndices)):
                ls_list = []
                num = 6
                if j == 93:
                    num = 4
                if j == 113:
                    num = 5
                for k in range(0,num):
                    ls_list.append(getJointGroupOutputIndices[len(group_attr)+k])
                # print(j)
                # print(getJointGroupOutputIndices)
                # getJointName = reader.getJointName(getJointGroupJointIndices[x])
                # print(getJointName)
                #print(ls_list)
                group_attr.append(ls_list)
            # print(group_attr)
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
            # 获取在组中有当前表情偏移数值的属性
            have_num_attr = []
            for x in range(0,len(joint_value)):
                if joint_value[x][base_face_in_joint_group_indices] != 0:
                    #print(joint_value[x][base_face_in_joint_group_indices])
                    have_num_attr.append(getJointGroupOutputIndices[x])
                    #print(getJointGroupOutputIndices[x])
            # 在有偏移数值的属性中获取有数值的骨骼
            have_num_joint = []
            for jo in range(0, len(group_attr)):  # 循环判断每个骨骼
                for x in range(0, len(group_attr[jo])):  # 循环查询这个骨骼的属性
                    for y in range(0, len(have_num_attr)):  # 循环获取有数值的属性
                        if have_num_attr[y] == group_attr[jo][x]:
                            if not getJointGroupJointIndices[jo] in have_num_joint:
                                have_num_joint.append(getJointGroupJointIndices[jo])
            '''# 按字典选择骨骼
            for joint_indices in have_num_joint:
                getJointName = reader.getJointName(joint_indices)
                cmds.select(getJointName,add=1)'''
            '''dict = {
                "骨骼组指针": joint_group,
                "骨骼": getJointGroupJointIndices,  # 骨骼组所含的骨骼
                "表情在骨骼组中的指针": [base_face_in_joint_group_indices],
            }'''
            # print(dict)
            # 在所有值中定位到对应属性的值
            for i in range(0, len(joint_value)):
                for x in range(0, len(have_num_attr)):
                    if have_num_attr[x] == getJointGroupOutputIndices[i]:
                        joint_value[i][base_face_in_joint_group_indices] = 0

            # 开始修改值
            new_values = []
            for i in range(0, len(joint_value)):
                for x in range(0, len(getJointGroupInputIndices)):
                    new_values.append(joint_value[i][x])
            # 设置要修改骨骼组的值
            writer.setJointGroupValues(joint_group, new_values)
    writer.write()
    print('表情修改完毕')




    #     for i in range(0,len(need_change_PSD_face)):
    #         # print('需要修改的微表情:' + str(need_change_PSD_face[i]))
    #         for k in range(0,len(getJointGroupInputIndices)):
    #             if need_change_PSD_face[i] == getJointGroupInputIndices[k]:  # 在骨骼组所关联的微表情中判断是否有需要修改的微表情
    #                 for n in range(0,len(getJointGroupOutputIndices)):  # 循环所有关联属性
    #                     dict = {
    #                         "骨骼组指针": j,
    #                         "微表情与此骨骼组关联的数量": len(getJointGroupInputIndices),
    #                         "微表情在此骨骼组的指针": k,
    #                         "微表情指针": getJointGroupInputIndices[k],
    #                         "骨骼": getJointGroupJointIndices,  # 骨骼组所含的骨骼 [75, 78, 79]
    #                         "骨骼组属性输出": getJointGroupOutputIndices, # 骨骼组关联的骨骼属性
    #                         "值": getJointGroupValues  # 骨骼组所含的值
    #                     }  # 需要修改表情，提前加载好骨骼列表和输出属性列表
    #                     # need_change_values = len(getJointGroupInputIndices) * n + k  # 每一个要改属性在属性值的位置
    #                     # if not need_change_values in need_change_values_num: # 每一个要改属性的位置添加到总列表中
    #                     #     need_change_values_num.append(need_change_values)
    #                     need_change_values.append(dict)
    # # print(need_change_values[0])
    # print(len(need_change_values))
    # # 筛选出所有的需要修改的组
    # all_grp = []
    # for i in range(0, len(need_change_values)):
    #     g = need_change_values[i]["骨骼组指针"]
    #     if not g in all_grp:
    #         all_grp.append(g)
    # print(all_grp)
    #
    # # 建立按组查询的字典
    # dictionary_queried_by_group = []
    # for j in range(0, len(all_grp)):
    #     # print(all_grp[j])
    #     ls_grp = all_grp[j]
    #     ls_list = []
    #     for i in range(0, len(need_change_values)):
    #         if all_grp[j] == need_change_values[i]["骨骼组指针"]:
    #             ls_list.append(need_change_values[i])
    #     dict = {
    #         "骨骼组指针": ls_grp,
    #         "此骨骼指针下要修改的部分": ls_list,
    #     }
    #     dictionary_queried_by_group.append(dict)
    # print(dictionary_queried_by_group[0])
    # print('加载要修改的骨骼组字典列表')
    # return dictionary_queried_by_group
    # 修改骨骼数值
    # 获取变化值，重新赋予

def start_modifying_values_according_to_the_dictionary_and_writing_them(base_face):
    dictionary_queried_by_group_list = Load_the_dictionary_to_be_modified(base_face)
    # print(dictionary_queried_by_group_list[0])
    for i in range(0,len(dictionary_queried_by_group_list)):
        if i == -1:
            print('asd')
            print(dictionary_queried_by_group_list[i]['骨骼组指针'])
            print(dictionary_queried_by_group_list[i]['此骨骼指针下要修改的部分'])
            print(len(dictionary_queried_by_group_list[i]['此骨骼指针下要修改的部分']))
        pass
        '''
        # print(dict_list[0])
        # for dict in dict_list:
        for i in range(0,1):
            dict = dict_list[i]
    
            # 拆解骨骼属性输出，按骨骼数量分组
            face_num = dict["微表情在此骨骼组的指针"]
            all_face_num = dict["微表情与此骨骼组关联的数量"]
            attr_name = dict["骨骼组属性输出"]
    
            joint = dict["骨骼"]
            joint_attr_dict = []  # 按骨骼数量拆解骨骼属性列表
            for j in range(0,len(joint)):
                ls_list = []
                for f in range(0,6):
                    ls_list.append(attr_name[j*6]+f)
                joint_attr_dict.append(ls_list)
            # print(joint_attr_dict)
    
            num = dict["值"]
            joint_attr_dict_num = []  # 按属性拆解值列表,把值按微表情和属性拆成列表
            for at in range(0, len(attr_name)):
                ls_list = []
                for f in range(0, all_face_num):
                    ls_list.append(num[at * all_face_num]+f)
                joint_attr_dict_num.append(ls_list)
            # print(joint_attr_dict_num)
    
            # 开始修改这些表情影响的所有值
            values = []
            for j in range(0, len(attr_name)):
                for f in range(0, all_face_num):
                    if f == face_num:
                        joint_attr_dict_num[j][f] = joint_attr_dict_num[j][f] + 1
                    values.append(joint_attr_dict_num[j][f])
            # print(values)
    
            # 还原所有值
            # 设置要修改骨骼组的值
            writer.setJointGroupValues(dict['骨骼组指针'], values)
        writer.write()
        print('表情修改完毕')
        '''


def Load_the_dictionary_to_be_modified_A(base_face):
    need_change_values = []
    getJointCount = reader.getJointCount() # 获取骨骼指数
    print('骨骼数量:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount() # 获取骨骼组指数
    print('骨骼组数量:' + str(getJointGroupCount))
    attr = []
    for j in range(0,getJointCount):
        getJointName = reader.getJointName(j)  # 获取骨骼名称，骨骼对骨骼组是一对一的关系
        list = ['tx','ty','tz','rx','ry','rz']
        if j == 93:
            list = ['ty','rx','ry','rz']
        if j == 113:
            list = ['ty','tz','rx','ry','rz']
        for at in list:
            attr.append(getJointName+ '.' + at)
    print('所有骨骼属性:'+str(len(attr)))
    getRawControlCount = reader.getRawControlCount()
    print('基础表情数量:' + str(getRawControlCount))
    # for i in range(0,getRawControlCount):
    #     getRawControlName = reader.getRawControlName(i)
    #     print('基础表情名称:' + str(getRawControlName))
    # base_face = 192
    getRawControlName = reader.getRawControlName(base_face)
    print('需要修改的初始表情：' + str(base_face))
    print('基础表情名称:' + str(getRawControlName))
    getPSDColumnIndices = reader.getPSDColumnIndices()
    print('主表情和微表情关联:' + str(len(getPSDColumnIndices)) + str(getPSDColumnIndices))
    getPSDCount = reader.getPSDCount()
    print('微表情数量:' + str(getPSDCount))
    getPSDRowIndices = reader.getPSDRowIndices()
    print('微表情数量索引:' + str(len(getPSDRowIndices)) + str(getPSDRowIndices))
    need_change_PSD_face = []
    # 查询需要修改基础表情所关联的微表情
    for i in range(0,len(getPSDColumnIndices)):
        if base_face == getPSDColumnIndices[i]:
            need_change_PSD_face.append(getPSDRowIndices[i])
    print('需要修改的微表情:' + str(need_change_PSD_face))
    # 查询所有组中是否有要修改的主表情
    for j in range(0, getJointGroupCount):  #
        getJointGroupInputIndices = reader.getJointGroupInputIndices(j)  # 获取骨骼组所关联的微表情
        # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
        joint_group = []
        base_face_in_joint_group_indices = []
        for i in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[i] == base_face:
                joint_group = j  # 骨骼组
                base_face_in_joint_group_indices = i  # 需要修改的基础表情在骨骼组所含微表情的位置
                break
        if joint_group:  # 如果骨骼组存在则创建骨骼组和骨骼字典
            getJointGroupJointIndices = reader.getJointGroupJointIndices(j)  # 获取骨骼组骨骼指数
            # print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
            getJointGroupOutputIndices = reader.getJointGroupOutputIndices(j)  # 获取骨骼组所关联的属性
            # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
            # 按骨骼数量拆解属性到新列表
            group_attr = []
            for x in range(0,len(getJointGroupJointIndices)):
                ls_list = []
                num = 6
                if j == 93:
                    num = 4
                if j == 113:
                    num = 5
                for k in range(0,num):
                    ls_list.append(getJointGroupOutputIndices[len(group_attr)+k])
                # print(j)
                # print(getJointGroupOutputIndices)
                # getJointName = reader.getJointName(getJointGroupJointIndices[x])
                # print(getJointName)
                #print(ls_list)
                group_attr.append(ls_list)
            # print(group_attr)
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
            # 获取在组中有当前表情偏移数值的属性
            have_num_attr = []
            for x in range(0,len(joint_value)):
                if joint_value[x][base_face_in_joint_group_indices] != 0:
                    # print(joint_value[x][base_face_in_joint_group_indices])
                    have_num_attr.append(getJointGroupOutputIndices[x])
                    # print(getJointGroupOutputIndices[x])
            # 在有偏移数值的属性中获取有数值的骨骼
            have_num_joint = []
            for jo in range(0, len(group_attr)):  # 循环判断每个骨骼
                for x in range(0, len(group_attr[jo])):  # 循环查询这个骨骼的属性
                    for y in range(0, len(have_num_attr)):  # 循环获取有数值的属性
                        if have_num_attr[y] == group_attr[jo][x]:
                            if not getJointGroupJointIndices[jo] in have_num_joint:
                                have_num_joint.append(getJointGroupJointIndices[jo])
            '''# 按字典选择骨骼
            for joint_indices in have_num_joint:
                getJointName = reader.getJointName(joint_indices)
                cmds.select(getJointName,add=1)'''
            '''dict = {
                "骨骼组指针": joint_group,
                "骨骼": getJointGroupJointIndices,  # 骨骼组所含的骨骼
                "表情在骨骼组中的指针": [base_face_in_joint_group_indices],
            }'''
            # print(dict)
            # 在所有值中定位到对应属性的值
            for i in range(0, len(joint_value)):
                for x in range(0, len(have_num_attr)):
                    if have_num_attr[x] == getJointGroupOutputIndices[i]:
                        joint_value[i][base_face_in_joint_group_indices] = 0

            # 开始修改值
            new_values = []
            for i in range(0, len(joint_value)):
                for x in range(0, len(getJointGroupInputIndices)):
                    new_values.append(joint_value[i][x])
            # 设置要修改骨骼组的值
            writer.setJointGroupValues(joint_group, new_values)
    writer.write()
    print('表情修改完毕')




    #     for i in range(0,len(need_change_PSD_face)):
    #         # print('需要修改的微表情:' + str(need_change_PSD_face[i]))
    #         for k in range(0,len(getJointGroupInputIndices)):
    #             if need_change_PSD_face[i] == getJointGroupInputIndices[k]:  # 在骨骼组所关联的微表情中判断是否有需要修改的微表情
    #                 for n in range(0,len(getJointGroupOutputIndices)):  # 循环所有关联属性
    #                     dict = {
    #                         "骨骼组指针": j,
    #                         "微表情与此骨骼组关联的数量": len(getJointGroupInputIndices),
    #                         "微表情在此骨骼组的指针": k,
    #                         "微表情指针": getJointGroupInputIndices[k],
    #                         "骨骼": getJointGroupJointIndices,  # 骨骼组所含的骨骼 [75, 78, 79]
    #                         "骨骼组属性输出": getJointGroupOutputIndices, # 骨骼组关联的骨骼属性
    #                         "值": getJointGroupValues  # 骨骼组所含的值
    #                     }  # 需要修改表情，提前加载好骨骼列表和输出属性列表
    #                     # need_change_values = len(getJointGroupInputIndices) * n + k  # 每一个要改属性在属性值的位置
    #                     # if not need_change_values in need_change_values_num: # 每一个要改属性的位置添加到总列表中
    #                     #     need_change_values_num.append(need_change_values)
    #                     need_change_values.append(dict)
    # # print(need_change_values[0])
    # print(len(need_change_values))
    # # 筛选出所有的需要修改的组
    # all_grp = []
    # for i in range(0, len(need_change_values)):
    #     g = need_change_values[i]["骨骼组指针"]
    #     if not g in all_grp:
    #         all_grp.append(g)
    # print(all_grp)
    #
    # # 建立按组查询的字典
    # dictionary_queried_by_group = []
    # for j in range(0, len(all_grp)):
    #     # print(all_grp[j])
    #     ls_grp = all_grp[j]
    #     ls_list = []
    #     for i in range(0, len(need_change_values)):
    #         if all_grp[j] == need_change_values[i]["骨骼组指针"]:
    #             ls_list.append(need_change_values[i])
    #     dict = {
    #         "骨骼组指针": ls_grp,
    #         "此骨骼指针下要修改的部分": ls_list,
    #     }
    #     dictionary_queried_by_group.append(dict)
    # print(dictionary_queried_by_group[0])
    # print('加载要修改的骨骼组字典列表')
    # return dictionary_queried_by_group
    # 修改骨骼数值
    # 获取变化值，重新赋予



#print_dna()
#modify_dna()
#modify_dna4()
#Load_the_dictionary_to_be_modified(191)
#start_modifying_values_according_to_the_dictionary_and_writing_them(191)
Load_the_dictionary_to_be_modified_A(191)
'''tempid = 123
print(tempid)
getJointCount = reader.getJointCount()
print('getJointCount:'+str(getJointCount))
getJointName = reader.getJointName(700)
print('getJointName:'+str(getJointName))
getJointGroupJointIndices = reader.getJointGroupJointIndices(tempid)
print('getJointGroupJointIndices:'+str(getJointGroupJointIndices))
getNeutralJointTranslation = reader.getNeutralJointTranslation(tempid)
print('getNeutralJointTranslation:'+str(getNeutralJointTranslation))
getNeutralJointRotation = reader.getNeutralJointRotation(tempid)
print('getNeutralJointRotation:'+str(getNeutralJointRotation))
getJointGroupCount = reader.getJointGroupCount()
print('getJointGroupCount:'+str(getJointGroupCount))
getJointGroupInputIndices = reader.getJointGroupInputIndices(tempid)
print('getJointGroupInputIndices:' + str(getJointGroupInputIndices))
getJointGroupOutputIndices = reader.getJointGroupOutputIndices(tempid)
print('getJointGroupOutputIndices:' + str(getJointGroupOutputIndices))
getJointGroupCountNew = reader.getJointGroupCount()
print('getJointGroupCountNew:'+str(getJointGroupCountNew))
getJointGroupValues = reader.getJointGroupValues(tempid)
print('getJointGroupValues:'+str(getJointGroupValues))
getGUIControlCount = reader.getGUIControlCount()
print('getGUIControlCount:'+str(getGUIControlCount))
getGUIControlName = reader.getGUIControlName(0)
print('getGUIControlName:'+str(getGUIControlName))
getRawControlCount = reader.getRawControlCount()
print('getRawControlCount:'+str(getRawControlCount))
getGUIToRawInputIndices = reader.getGUIToRawInputIndices()
print('getGUIToRawInputIndices:'+str(len(getGUIToRawInputIndices)))
getGUIToRawOutputIndices = reader.getGUIToRawOutputIndices()
print('getGUIToRawOutputIndices:'+str(len(getGUIToRawOutputIndices)))
getJointGroupCount = reader.getJointGroupCount()
print('getJointGroupCount:'+str(getJointGroupCount))'''