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
        '''for i in range(0,len(getJointGroupInputIndices)): # �Թ�������ѭ��
            if getJointGroupInputIndices[i]<800:
                k = i*len(getJointGroupOutputIndices)
                for n in range(0,len(getJointGroupOutputIndices)): # �������ѭ��
                    values[k+n] = getJointGroupValues[k+n] * 0'''
        for i in range(0, len(getJointGroupOutputIndices)):  # �������ѭ��
            k = i * len(getJointGroupInputIndices)
            for n in range(0, len(getJointGroupInputIndices)):  # �Թ�������ѭ��
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
    getJointCount = reader.getJointCount() # ��ȡ����ָ��
    print('getJointCount:' + str(getJointCount))
    jointCount = 700
    print(jointCount)
    getJointName = reader.getJointName(jointCount) # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
    print('getJointName:' + str(getJointName))
    getJointGroupCount = reader.getJointGroupCount() # ��ȡ������ָ��
    print('getJointGroupCount:'+str(getJointGroupCount))

    JointToJointGroupOneByOne = 0
    for i in range(0,getJointGroupCount):
        getJointGroupJointIndices = reader.getJointGroupJointIndices(i)  # ��ȡ���������ָ��
        for j in range(0,len(getJointGroupJointIndices)):
            if jointCount == getJointGroupJointIndices[j]:
                JointToJointGroupOneByOne = i
                print('������Ӧ�Ĺ�����'+str(i))
                print('getJointGroupJointIndices(�����������ƵĹ���ָ��):' + str(len(getJointGroupJointIndices)) + str(getJointGroupJointIndices))
    getJointGroupLODs = reader.getJointGroupLODs(JointToJointGroupOneByOne)  # ��ȡ������LOD
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
    print('΢��������'+str(num_1+1)) # 814��΢����
    print('��������'+str(num_2+1)) # 6720������
    getJointGroupInputIndices = reader.getJointGroupInputIndices(JointToJointGroupOneByOne)
    print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
    getJointGroupOutputIndices = reader.getJointGroupOutputIndices(JointToJointGroupOneByOne)
    print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
    getJointGroupValues = reader.getJointGroupValues(JointToJointGroupOneByOne)
    print('getJointGroupValues:'+str(len(getJointGroupValues))+str(getJointGroupValues))
    getArchetype = reader.getAnimatedMapIndexListCount()
    print('getArchetype:' + str(getArchetype))
    print('��' + str(jointCount) + '�������� ������' + getJointName + ',��Ӧ' + str(
        JointToJointGroupOneByOne) + '�Ź����飬��������������' + str(len(getJointGroupInputIndices)) +
          ',�������������' + str(len(getJointGroupOutputIndices)) + ',ֵ������' + str(len(getJointGroupValues)))

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
    Microexpression = 200 # ΢����
    print(Microexpression)
    getJointCount = reader.getJointCount()  # ��ȡ����ָ��
    #print('����ָ��:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount()  # ��ȡ������ָ��
    #print('������ָ��:' + str(getJointGroupCount))
    for g in range(0,getJointGroupCount):  # ѭ�����й�����
        getJointGroupInputIndices = reader.getJointGroupInputIndices(g) # ��ȡ����΢����
        #print('������' + str(g) + ':΢����' + str(len(getJointGroupInputIndices)) + ':' + str(getJointGroupInputIndices))
        Microexpression_in_group_indices = 0
        values = []
        getJointGroupJointIndices = reader.getJointGroupJointIndices(g)  # ��ȡ���������ָ��
        # print('������' + str(g) + '����ָ��:'+ str(getJointGroupJointIndices))
        getJointGroupOutputIndices = reader.getJointGroupOutputIndices(g)  # ��ȡ����������
        # print('������' + str(g) + '��������:'+ str(getJointGroupOutputIndices))
        getJointGroupValues = reader.getJointGroupValues(g)  # ��ȡ������ֵ
        # print('������' + str(g) + '����ֵ:'+ str(getJointGroupValues))
        values = getJointGroupValues  # ����һ���±����������ȡ������ֵ
        for i in getJointGroupInputIndices:  # ѭ���˹������е�����΢����
            if Microexpression != i: # ���΢��������Ҫ�޸ĵ�΢����
                start = Microexpression_in_group_indices * len(getJointGroupOutputIndices)  # ��ȡҪ�޸ĵ�΢�������ֵ��¼��ֵ�ĳ�ʼλ��
                for j in range(0,len(getJointGroupOutputIndices)):  # ѭ���޸Ĵ�΢�������й�������ֵ
                    values[start+j] = 0
                Microexpression_in_group_indices = Microexpression_in_group_indices + 1
        writer.setJointGroupValues(g, values)  # д�����й�������ֵ
        print(values)
    writer.write()
    print('�����޸����')
def modify_dna4():
    #dna_reader = load_dna('E:\maya_plug_in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna')
    stream = FileStream(flie, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    stream = FileStream(flie, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    getJointCount = reader.getJointCount() # ��ȡ����ָ��
    print('getJointCount:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount() # ��ȡ������ָ��
    print('getJointGroupCount:' + str(getJointGroupCount))
    attr = []
    for j in range(0,getJointCount):
        getJointName = reader.getJointName(j)  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
        for at in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            attr.append(getJointName+ '.' + at)
    print('attr:'+str(len(attr)))
    # getJointGroupCount = reader.getJointGroupCount()  # ��ȡ������ָ��
    # print('getJointGroupCount:' + str(getJointGroupCount))
    # for i in range(0, getJointGroupCount):
    #     getJointGroupJointIndices = reader.getJointGroupJointIndices(i)  # ��ȡ���������ָ��
    #     for j in range(0, len(getJointGroupJointIndices)):
    #         getJointName = reader.getJointName(getJointGroupJointIndices[j])  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
    #         print(str(i) + 'getJointName:' + str(getJointName))
    # 118getJointName:FACIAL_C_Jaw
    grp = 118
    print(str(grp))
    getJointGroupJointIndices = reader.getJointGroupJointIndices(grp)  # ��ȡ���������ָ��
    print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
    getJointName = reader.getJointName(getJointGroupJointIndices[0])  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
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
    #     getJointName = reader.getJointName(jointCount) # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
    #     print('getJointName:' + str(getJointName))
    # getJointGroupCount = reader.getJointGroupCount() # ��ȡ������ָ��
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
    getJointCount = reader.getJointCount() # ��ȡ����ָ��
    print('��������:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount() # ��ȡ������ָ��
    print('����������:' + str(getJointGroupCount))
    attr = []
    for j in range(0,getJointCount):
        getJointName = reader.getJointName(j)  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
        list = ['tx','ty','tz','rx','ry','rz']
        if j == 93:
            list = ['ty','rx','ry','rz']
        if j == 113:
            list = ['ty','tz','rx','ry','rz']
        for at in list:
            attr.append(getJointName+ '.' + at)
    print('���й�������:'+str(len(attr)))
    getRawControlCount = reader.getRawControlCount()
    print('������������:' + str(getRawControlCount))
    # for i in range(0,getRawControlCount):
    #     getRawControlName = reader.getRawControlName(i)
    #     print('������������:' + str(getRawControlName))
    # base_face = 192
    getRawControlName = reader.getRawControlName(base_face)
    print('��Ҫ�޸ĵĳ�ʼ���飺' + str(base_face))
    print('������������:' + str(getRawControlName))
    getPSDColumnIndices = reader.getPSDColumnIndices()
    print('�������΢�������:' + str(len(getPSDColumnIndices)) + str(getPSDColumnIndices))
    getPSDCount = reader.getPSDCount()
    print('΢��������:' + str(getPSDCount))
    getPSDRowIndices = reader.getPSDRowIndices()
    print('΢������������:' + str(len(getPSDRowIndices)) + str(getPSDRowIndices))
    need_change_PSD_face = []
    # ��ѯ��Ҫ�޸Ļ���������������΢����
    for i in range(0,len(getPSDColumnIndices)):
        if base_face == getPSDColumnIndices[i]:
            need_change_PSD_face.append(getPSDRowIndices[i])
    print('��Ҫ�޸ĵ�΢����:' + str(need_change_PSD_face))
    # ��ѯ���������Ƿ���Ҫ�޸ĵ�������
    for j in range(0, getJointGroupCount):  #
        getJointGroupInputIndices = reader.getJointGroupInputIndices(j)  # ��ȡ��������������΢����
        # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
        joint_group = []
        base_face_in_joint_group_indices = []
        for i in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[i] == base_face:
                joint_group = j  # ������
                base_face_in_joint_group_indices = i  # ��Ҫ�޸ĵĻ��������ڹ���������΢�����λ��
                break
        if joint_group:  # �������������򴴽�������͹����ֵ�
            getJointGroupJointIndices = reader.getJointGroupJointIndices(j)  # ��ȡ���������ָ��
            # print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
            getJointGroupOutputIndices = reader.getJointGroupOutputIndices(j)  # ��ȡ������������������
            # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
            # ����������������Ե����б�
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
            # ��ȡ�������е�ǰ����ƫ����ֵ������
            have_num_attr = []
            for x in range(0,len(joint_value)):
                if joint_value[x][base_face_in_joint_group_indices] != 0:
                    #print(joint_value[x][base_face_in_joint_group_indices])
                    have_num_attr.append(getJointGroupOutputIndices[x])
                    #print(getJointGroupOutputIndices[x])
            # ����ƫ����ֵ�������л�ȡ����ֵ�Ĺ���
            have_num_joint = []
            for jo in range(0, len(group_attr)):  # ѭ���ж�ÿ������
                for x in range(0, len(group_attr[jo])):  # ѭ����ѯ�������������
                    for y in range(0, len(have_num_attr)):  # ѭ����ȡ����ֵ������
                        if have_num_attr[y] == group_attr[jo][x]:
                            if not getJointGroupJointIndices[jo] in have_num_joint:
                                have_num_joint.append(getJointGroupJointIndices[jo])
            '''# ���ֵ�ѡ�����
            for joint_indices in have_num_joint:
                getJointName = reader.getJointName(joint_indices)
                cmds.select(getJointName,add=1)'''
            '''dict = {
                "������ָ��": joint_group,
                "����": getJointGroupJointIndices,  # �����������Ĺ���
                "�����ڹ������е�ָ��": [base_face_in_joint_group_indices],
            }'''
            # print(dict)
            # ������ֵ�ж�λ����Ӧ���Ե�ֵ
            for i in range(0, len(joint_value)):
                for x in range(0, len(have_num_attr)):
                    if have_num_attr[x] == getJointGroupOutputIndices[i]:
                        joint_value[i][base_face_in_joint_group_indices] = 0

            # ��ʼ�޸�ֵ
            new_values = []
            for i in range(0, len(joint_value)):
                for x in range(0, len(getJointGroupInputIndices)):
                    new_values.append(joint_value[i][x])
            # ����Ҫ�޸Ĺ������ֵ
            writer.setJointGroupValues(joint_group, new_values)
    writer.write()
    print('�����޸����')




    #     for i in range(0,len(need_change_PSD_face)):
    #         # print('��Ҫ�޸ĵ�΢����:' + str(need_change_PSD_face[i]))
    #         for k in range(0,len(getJointGroupInputIndices)):
    #             if need_change_PSD_face[i] == getJointGroupInputIndices[k]:  # �ڹ�������������΢�������ж��Ƿ�����Ҫ�޸ĵ�΢����
    #                 for n in range(0,len(getJointGroupOutputIndices)):  # ѭ�����й�������
    #                     dict = {
    #                         "������ָ��": j,
    #                         "΢������˹��������������": len(getJointGroupInputIndices),
    #                         "΢�����ڴ˹������ָ��": k,
    #                         "΢����ָ��": getJointGroupInputIndices[k],
    #                         "����": getJointGroupJointIndices,  # �����������Ĺ��� [75, 78, 79]
    #                         "�������������": getJointGroupOutputIndices, # ����������Ĺ�������
    #                         "ֵ": getJointGroupValues  # ������������ֵ
    #                     }  # ��Ҫ�޸ı��飬��ǰ���غù����б����������б�
    #                     # need_change_values = len(getJointGroupInputIndices) * n + k  # ÿһ��Ҫ������������ֵ��λ��
    #                     # if not need_change_values in need_change_values_num: # ÿһ��Ҫ�����Ե�λ����ӵ����б���
    #                     #     need_change_values_num.append(need_change_values)
    #                     need_change_values.append(dict)
    # # print(need_change_values[0])
    # print(len(need_change_values))
    # # ɸѡ�����е���Ҫ�޸ĵ���
    # all_grp = []
    # for i in range(0, len(need_change_values)):
    #     g = need_change_values[i]["������ָ��"]
    #     if not g in all_grp:
    #         all_grp.append(g)
    # print(all_grp)
    #
    # # ���������ѯ���ֵ�
    # dictionary_queried_by_group = []
    # for j in range(0, len(all_grp)):
    #     # print(all_grp[j])
    #     ls_grp = all_grp[j]
    #     ls_list = []
    #     for i in range(0, len(need_change_values)):
    #         if all_grp[j] == need_change_values[i]["������ָ��"]:
    #             ls_list.append(need_change_values[i])
    #     dict = {
    #         "������ָ��": ls_grp,
    #         "�˹���ָ����Ҫ�޸ĵĲ���": ls_list,
    #     }
    #     dictionary_queried_by_group.append(dict)
    # print(dictionary_queried_by_group[0])
    # print('����Ҫ�޸ĵĹ������ֵ��б�')
    # return dictionary_queried_by_group
    # �޸Ĺ�����ֵ
    # ��ȡ�仯ֵ�����¸���

def start_modifying_values_according_to_the_dictionary_and_writing_them(base_face):
    dictionary_queried_by_group_list = Load_the_dictionary_to_be_modified(base_face)
    # print(dictionary_queried_by_group_list[0])
    for i in range(0,len(dictionary_queried_by_group_list)):
        if i == -1:
            print('asd')
            print(dictionary_queried_by_group_list[i]['������ָ��'])
            print(dictionary_queried_by_group_list[i]['�˹���ָ����Ҫ�޸ĵĲ���'])
            print(len(dictionary_queried_by_group_list[i]['�˹���ָ����Ҫ�޸ĵĲ���']))
        pass
        '''
        # print(dict_list[0])
        # for dict in dict_list:
        for i in range(0,1):
            dict = dict_list[i]
    
            # �����������������������������
            face_num = dict["΢�����ڴ˹������ָ��"]
            all_face_num = dict["΢������˹��������������"]
            attr_name = dict["�������������"]
    
            joint = dict["����"]
            joint_attr_dict = []  # ���������������������б�
            for j in range(0,len(joint)):
                ls_list = []
                for f in range(0,6):
                    ls_list.append(attr_name[j*6]+f)
                joint_attr_dict.append(ls_list)
            # print(joint_attr_dict)
    
            num = dict["ֵ"]
            joint_attr_dict_num = []  # �����Բ��ֵ�б�,��ֵ��΢��������Բ���б�
            for at in range(0, len(attr_name)):
                ls_list = []
                for f in range(0, all_face_num):
                    ls_list.append(num[at * all_face_num]+f)
                joint_attr_dict_num.append(ls_list)
            # print(joint_attr_dict_num)
    
            # ��ʼ�޸���Щ����Ӱ�������ֵ
            values = []
            for j in range(0, len(attr_name)):
                for f in range(0, all_face_num):
                    if f == face_num:
                        joint_attr_dict_num[j][f] = joint_attr_dict_num[j][f] + 1
                    values.append(joint_attr_dict_num[j][f])
            # print(values)
    
            # ��ԭ����ֵ
            # ����Ҫ�޸Ĺ������ֵ
            writer.setJointGroupValues(dict['������ָ��'], values)
        writer.write()
        print('�����޸����')
        '''


def Load_the_dictionary_to_be_modified_A(base_face):
    need_change_values = []
    getJointCount = reader.getJointCount() # ��ȡ����ָ��
    print('��������:' + str(getJointCount))
    getJointGroupCount = reader.getJointGroupCount() # ��ȡ������ָ��
    print('����������:' + str(getJointGroupCount))
    attr = []
    for j in range(0,getJointCount):
        getJointName = reader.getJointName(j)  # ��ȡ�������ƣ������Թ�������һ��һ�Ĺ�ϵ
        list = ['tx','ty','tz','rx','ry','rz']
        if j == 93:
            list = ['ty','rx','ry','rz']
        if j == 113:
            list = ['ty','tz','rx','ry','rz']
        for at in list:
            attr.append(getJointName+ '.' + at)
    print('���й�������:'+str(len(attr)))
    getRawControlCount = reader.getRawControlCount()
    print('������������:' + str(getRawControlCount))
    # for i in range(0,getRawControlCount):
    #     getRawControlName = reader.getRawControlName(i)
    #     print('������������:' + str(getRawControlName))
    # base_face = 192
    getRawControlName = reader.getRawControlName(base_face)
    print('��Ҫ�޸ĵĳ�ʼ���飺' + str(base_face))
    print('������������:' + str(getRawControlName))
    getPSDColumnIndices = reader.getPSDColumnIndices()
    print('�������΢�������:' + str(len(getPSDColumnIndices)) + str(getPSDColumnIndices))
    getPSDCount = reader.getPSDCount()
    print('΢��������:' + str(getPSDCount))
    getPSDRowIndices = reader.getPSDRowIndices()
    print('΢������������:' + str(len(getPSDRowIndices)) + str(getPSDRowIndices))
    need_change_PSD_face = []
    # ��ѯ��Ҫ�޸Ļ���������������΢����
    for i in range(0,len(getPSDColumnIndices)):
        if base_face == getPSDColumnIndices[i]:
            need_change_PSD_face.append(getPSDRowIndices[i])
    print('��Ҫ�޸ĵ�΢����:' + str(need_change_PSD_face))
    # ��ѯ���������Ƿ���Ҫ�޸ĵ�������
    for j in range(0, getJointGroupCount):  #
        getJointGroupInputIndices = reader.getJointGroupInputIndices(j)  # ��ȡ��������������΢����
        # print('getJointGroupInputIndices:' + str(len(getJointGroupInputIndices)) + str(getJointGroupInputIndices))
        joint_group = []
        base_face_in_joint_group_indices = []
        for i in range(0,len(getJointGroupInputIndices)):
            if getJointGroupInputIndices[i] == base_face:
                joint_group = j  # ������
                base_face_in_joint_group_indices = i  # ��Ҫ�޸ĵĻ��������ڹ���������΢�����λ��
                break
        if joint_group:  # �������������򴴽�������͹����ֵ�
            getJointGroupJointIndices = reader.getJointGroupJointIndices(j)  # ��ȡ���������ָ��
            # print('getJointGroupJointIndices:' + str(getJointGroupJointIndices))
            getJointGroupOutputIndices = reader.getJointGroupOutputIndices(j)  # ��ȡ������������������
            # print('getJointGroupOutputIndices:' + str(len(getJointGroupOutputIndices)) + str(getJointGroupOutputIndices))
            # ����������������Ե����б�
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
            # ��ȡ�������е�ǰ����ƫ����ֵ������
            have_num_attr = []
            for x in range(0,len(joint_value)):
                if joint_value[x][base_face_in_joint_group_indices] != 0:
                    # print(joint_value[x][base_face_in_joint_group_indices])
                    have_num_attr.append(getJointGroupOutputIndices[x])
                    # print(getJointGroupOutputIndices[x])
            # ����ƫ����ֵ�������л�ȡ����ֵ�Ĺ���
            have_num_joint = []
            for jo in range(0, len(group_attr)):  # ѭ���ж�ÿ������
                for x in range(0, len(group_attr[jo])):  # ѭ����ѯ�������������
                    for y in range(0, len(have_num_attr)):  # ѭ����ȡ����ֵ������
                        if have_num_attr[y] == group_attr[jo][x]:
                            if not getJointGroupJointIndices[jo] in have_num_joint:
                                have_num_joint.append(getJointGroupJointIndices[jo])
            '''# ���ֵ�ѡ�����
            for joint_indices in have_num_joint:
                getJointName = reader.getJointName(joint_indices)
                cmds.select(getJointName,add=1)'''
            '''dict = {
                "������ָ��": joint_group,
                "����": getJointGroupJointIndices,  # �����������Ĺ���
                "�����ڹ������е�ָ��": [base_face_in_joint_group_indices],
            }'''
            # print(dict)
            # ������ֵ�ж�λ����Ӧ���Ե�ֵ
            for i in range(0, len(joint_value)):
                for x in range(0, len(have_num_attr)):
                    if have_num_attr[x] == getJointGroupOutputIndices[i]:
                        joint_value[i][base_face_in_joint_group_indices] = 0

            # ��ʼ�޸�ֵ
            new_values = []
            for i in range(0, len(joint_value)):
                for x in range(0, len(getJointGroupInputIndices)):
                    new_values.append(joint_value[i][x])
            # ����Ҫ�޸Ĺ������ֵ
            writer.setJointGroupValues(joint_group, new_values)
    writer.write()
    print('�����޸����')




    #     for i in range(0,len(need_change_PSD_face)):
    #         # print('��Ҫ�޸ĵ�΢����:' + str(need_change_PSD_face[i]))
    #         for k in range(0,len(getJointGroupInputIndices)):
    #             if need_change_PSD_face[i] == getJointGroupInputIndices[k]:  # �ڹ�������������΢�������ж��Ƿ�����Ҫ�޸ĵ�΢����
    #                 for n in range(0,len(getJointGroupOutputIndices)):  # ѭ�����й�������
    #                     dict = {
    #                         "������ָ��": j,
    #                         "΢������˹��������������": len(getJointGroupInputIndices),
    #                         "΢�����ڴ˹������ָ��": k,
    #                         "΢����ָ��": getJointGroupInputIndices[k],
    #                         "����": getJointGroupJointIndices,  # �����������Ĺ��� [75, 78, 79]
    #                         "�������������": getJointGroupOutputIndices, # ����������Ĺ�������
    #                         "ֵ": getJointGroupValues  # ������������ֵ
    #                     }  # ��Ҫ�޸ı��飬��ǰ���غù����б����������б�
    #                     # need_change_values = len(getJointGroupInputIndices) * n + k  # ÿһ��Ҫ������������ֵ��λ��
    #                     # if not need_change_values in need_change_values_num: # ÿһ��Ҫ�����Ե�λ����ӵ����б���
    #                     #     need_change_values_num.append(need_change_values)
    #                     need_change_values.append(dict)
    # # print(need_change_values[0])
    # print(len(need_change_values))
    # # ɸѡ�����е���Ҫ�޸ĵ���
    # all_grp = []
    # for i in range(0, len(need_change_values)):
    #     g = need_change_values[i]["������ָ��"]
    #     if not g in all_grp:
    #         all_grp.append(g)
    # print(all_grp)
    #
    # # ���������ѯ���ֵ�
    # dictionary_queried_by_group = []
    # for j in range(0, len(all_grp)):
    #     # print(all_grp[j])
    #     ls_grp = all_grp[j]
    #     ls_list = []
    #     for i in range(0, len(need_change_values)):
    #         if all_grp[j] == need_change_values[i]["������ָ��"]:
    #             ls_list.append(need_change_values[i])
    #     dict = {
    #         "������ָ��": ls_grp,
    #         "�˹���ָ����Ҫ�޸ĵĲ���": ls_list,
    #     }
    #     dictionary_queried_by_group.append(dict)
    # print(dictionary_queried_by_group[0])
    # print('����Ҫ�޸ĵĹ������ֵ��б�')
    # return dictionary_queried_by_group
    # �޸Ĺ�����ֵ
    # ��ȡ�仯ֵ�����¸���



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