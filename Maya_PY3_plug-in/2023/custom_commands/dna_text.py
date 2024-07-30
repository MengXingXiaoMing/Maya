"""
This example demonstrates creating DNA from scratch.
IMPORTANT: You have to setup the environment before running this example. Please refer to the 'Environment setup' section in README.md.

- usage in command line:
    python dna_demo.py
    mayapy dna_demo.py
- usage in Maya:
    1. copy whole content of this file to Maya Script Editor
    2. change value of ROOT_DIR to absolute path of dna_calibration, e.g. `c:/dna_calibration` in Windows or `/home/user/dna_calibration`. Important:
    Use `/` (forward slash), because Maya uses forward slashes in path.

- customization:
    - change CHARACTER_NAME to Taro, or the name of a custom DNA file placed in /data/dna_files

Expected: Script will generate Ada_output.dna in OUTPUT_DIR from original Ada.dna.
NOTE: If OUTPUT_DIR does not exist, it will be created.
"""

from os import makedirs
from os import path as ospath

# If you use Maya, use absolute path
ROOT_DIR = r'D:\scenes\plug-in\MetaHuman-DNA-Calibration-main\MetaHuman-DNA-Calibration-main\data\dna_files\Ada.dna'
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

dna_reader = load_dna(ROOT_DIR)
i=50
while i<51:#170
    try:
        i = i + 1
        a = dna_reader.getGUIControlCount()
        print ('GUI控制计数:'+str(a))
        a = dna_reader.getGUIControlName(i)
        print ('GUI控件名称:'+str(a))
        a = dna_reader.getRawControlCount()
        print ('Raw控件计数:'+str(a))
        a = dna_reader.getRawControlName(i)
        print ('原始控制名称:'+str(a))
        a = dna_reader.getJointCount()
        print ('骨骼计数:'+str(a))
        a = dna_reader.getJointName(i)
        print ('骨骼名称:'+str(a))
        a = dna_reader.getJointIndicesForLOD(0)
        print ('LOD骨骼索引:'+str(a))
        a = dna_reader.getJointParentIndex(i)
        print ('骨骼父索引:'+str(a))
        a = dna_reader.getBlendShapeChannelCount()
        print ('BS频道计数:'+str(a))
        a = dna_reader.getBlendShapeChannelName(i)
        print ('BS频道名称:'+str(a))
        a = dna_reader.getBlendShapeChannelIndexListCount()
        print ('BS通道索引列表计数:'+str(a))
        a = dna_reader.getBlendShapeChannelIndicesForLOD(0)
        print ('BSLOD的通道标记:'+str(a))
        a = dna_reader.getAnimatedMapCount()
        print ('动画贴图计数:'+str(a))
        a = dna_reader.getAnimatedMapName(i)
        print ('动画贴图名称:'+str(a))
        a = dna_reader.getAnimatedMapIndexListCount()
        print ('动画贴图索引列表计数:'+str(a))
        a = dna_reader.getAnimatedMapIndicesForLOD(0)
        print ('LOD的动画地图标记:'+str(a))
        a = dna_reader.getMeshCount()
        print ('获取网格计数:'+str(a))
        a = dna_reader.getMeshName(i)
        print ('网格名称:'+str(a))
        a = dna_reader.getMeshIndexListCount()
        print ('网格索引列表计数:'+str(a))
        a = dna_reader.getMeshIndicesForLOD(0)
        print ('LOD的网格标记:'+str(a))
        a = dna_reader.getMeshBlendShapeChannelMappingCount()
        print ('网格BSLOD的网格标记:'+str(a))
        a = dna_reader.getMeshBlendShapeChannelMapping(i)
        print ('网格BS通道映射:'+str(a))
        a = dna_reader.getMeshBlendShapeChannelMappingIndicesForLOD(0)
        print ('网格BSLOD的通道映射标记:'+str(a))
        a = dna_reader.getNeutralJointTranslation(i)
        print ('中性骨骼位移:'+str(a))
        a = dna_reader.getNeutralJointTranslationXs()
        print ('中性骨骼位移Xs:'+str(a))
        a = dna_reader.getNeutralJointRotation(i)
        print ('中性骨骼旋转:'+str(a))
        a = dna_reader.getNeutralJointRotationXs()
        print ('中性骨骼旋转Xs:'+str(a))
        print('###############################################################################################')
        # a = dna_reader.getVertexPositionCount(0)
        # print('顶点位置计数:' + str(a))
        # a = dna_reader.getVertexPosition(0,0)
        # print('顶点位置:' + str(a))
        # a = dna_reader.getVertexPositionXs(0)
        # print('顶点位置Xs:' + str(a))
        # a = dna_reader.getVertexTextureCoordinateCount(0)
        # print('顶点纹理坐标计数:' + str(a))
        # a = dna_reader.getVertexTextureCoordinate(0,0)
        # print('顶点纹理坐标:' + str(a))
        # a = dna_reader.getVertexTextureCoordinateUs(0)
        # print('顶点纹理坐标Us:' + str(a))
        # a = dna_reader.getVertexTextureCoordinateVs(0)
        # print('顶点纹理坐标Vs:' + str(a))
        # a = dna_reader.getVertexNormalCount(0)
        # print('顶点法线计数:' + str(a))
        # a = dna_reader.getVertexNormal(0,0)
        # print('顶点法线:' + str(a))
        # a = dna_reader.getVertexNormalXs(0)
        # print('顶点法线Xs:' + str(a))
        # a = dna_reader.getVertexLayoutCount(0)
        # print('顶点布局计数:' + str(a))
        # a = dna_reader.getVertexLayout(0,0)
        # print('顶点布局:' + str(a))
        # a = dna_reader.getVertexLayoutPositionIndices(0)
        # print('顶点布局位置索引:' + str(a))
        # a = dna_reader.getVertexLayoutTextureCoordinateIndices(0)
        # print('顶点布局纹理坐标指示:' + str(a))
        # a = dna_reader.getVertexLayoutNormalIndices(0)
        # print('顶点布局法线索引:' + str(a))
        # a = dna_reader.getFaceCount(0)
        # print('面部计数:' + str(a))
        # a = dna_reader.getFaceVertexLayoutIndices(0,0)
        # print('面顶点布局索引:' + str(a))
        # a = dna_reader.getMaximumInfluencePerVertex(0)
        # print('每个顶点的最大影响:' + str(a))
        # a = dna_reader.getSkinWeightsCount(0)
        # print('蒙皮权重计数:' + str(a))
        # a = dna_reader.getSkinWeightsValues(0,0)
        # print('蒙皮权重值:' + str(a))
        # a = dna_reader.getSkinWeightsJointIndices(0, 0)
        # print('蒙皮权重关节指数:' + str(a))
        # a = dna_reader.getBlendShapeTargetCount(0)
        # print('BS目标计数:' + str(a))
        # a = dna_reader.getBlendShapeChannelIndex(0,0)
        # print('BS频道索引:' + str(a))
        # a = dna_reader.getBlendShapeTargetDeltaCount(0, 0)
        # print('BS目标增量计数:' + str(a))
        # a = dna_reader.getBlendShapeTargetDelta(0, 0,0)
        # print('BS目标Delta:' + str(a))
        # a = dna_reader.getBlendShapeTargetDeltaXs(0, 0)
        # print('BS目标DeltaXs:' + str(a))
        # a = dna_reader.getBlendShapeTargetVertexIndices(0, 0)
        # print('BS目标顶点索引:' + str(a))
        j = 0
        a = dna_reader.getGUIToRawInputIndices()
        print('GUI到原始输入索引:' + str(a[j]))
        a = dna_reader.getGUIToRawOutputIndices()
        print('GUI到原始输出索引:' + str(a[j]))
        a = dna_reader.getGUIToRawFromValues()
        print('GUI来自原始值:' + str(a[j]))
        a = dna_reader.getGUIToRawToValues()
        print('GUI到原始值:' + str(a[j]))
        a = dna_reader.getGUIToRawSlopeValues()
        print('GUI到原始斜率值:' + str(a[j]))
        a = dna_reader.getGUIToRawCutValues()
        print('GUI到原始切割值:' + str(a[j]))
        a = dna_reader.getPSDCount()
        print('PSD计数:' + str(a))
        a = dna_reader.getPSDRowIndices()
        print('PSD行索引:' + str(a[j]))
        a = dna_reader.getPSDColumnIndices()
        print('PSD列索引:' + str(a[j]))
        a = dna_reader.getPSDValues()
        print('PSD值:' + str(a))
        a = dna_reader.getJointRowCount()
        print('骨骼行计数:' + str(a))
        a = dna_reader.getJointColumnCount()
        print('骨骼纵计数:' + str(a))
        a = dna_reader.getJointVariableAttributeIndices(0)
        print('骨骼变量属性索引:' + str(a[j]))
        a = dna_reader.getJointGroupCount()
        print('骨骼组计数:' + str(a))
        a = dna_reader.getJointGroupLODs(10)
        print('骨骼组LOD:' + str(a[j]))
        a = dna_reader.getJointGroupInputIndices(10)
        print('骨骼组输入指数:' + str(a))
        a = dna_reader.getJointGroupOutputIndices(10)
        print('骨骼组输出指数:' + str(a))
        a = dna_reader.getJointGroupValues(10)
        print('骨骼组数值:' + str(a))
        print('骨骼组数值数量:' + str(len(a)))
        a = dna_reader.getJointGroupJointIndices(10)
        print('BS目标顶点索引:' + str(a))
        a = dna_reader.getBlendShapeChannelLODs()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getBlendShapeChannelInputIndices()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getBlendShapeChannelOutputIndices()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getAnimatedMapLODs()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getAnimatedMapInputIndices()
        print('BS目标顶点索引5:' + str(a[j]))
        a = dna_reader.getAnimatedMapOutputIndices()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getAnimatedMapFromValues()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getAnimatedMapToValues()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getAnimatedMapSlopeValues()
        print('BS目标顶点索引:' + str(a[j]))
        a = dna_reader.getAnimatedMapCutValues()
        print('BS目标顶点索引6:' + str(a[j]))
        print('#########################################################################################')
        a = dna_reader.getJointCount()
        print('骨骼计数:' + str(a))
        a = dna_reader.getJointName(i)
        print('骨骼名称:' + str(a))
        a = dna_reader.getJointGroupJointIndices(10)
        print('BS目标顶点索引:' + str(a))
        a = dna_reader.getNeutralJointTranslation(i)
        print('中性骨骼位移:' + str(a))
        a = dna_reader.getNeutralJointRotation(i)
        print('中性骨骼旋转:' + str(a))
        a = dna_reader.getJointGroupCount()
        print('骨骼组计数:' + str(a))
        a = dna_reader.getJointGroupInputIndices(10)
        print('骨骼组输入指数:' + str(a))
        a = dna_reader.getJointGroupOutputIndices(10)
        print('骨骼组输出指数:' + str(a))
        a = dna_reader.getJointGroupCount()
        print('骨骼组计数:' + str(a))
        a = dna_reader.getJointGroupValues(10)
        print('骨骼组数值:' + str(a))
    except :
        pass


if __name__ == "__main__":
    #makedirs(OUTPUT_DIR, exist_ok=True)
    #create_new_dna(OUTPUT_DNA)
    pass