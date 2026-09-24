# coding=gbk
import maya.cmds as cmds
import os
import sys
import inspect
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    # 库路径
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    # 方法2：直接判断是否是目录（更简洁）
    if os.path.isdir(library_path):
        # 库添加到系统路径
        sys.path.append(library_path)
        maya_version_int = test_version
        # print('文件夹存在')
        break
import general_settings
from general_settings import *
importlib.reload(general_settings)

mesh = cmds.ls(sl=1)

bbox = cmds.xform(mesh, query=True, boundingBox=True, worldSpace=True)
# 计算尺寸（宽度=X轴差值，高度=Y轴差值，深度=Z轴差值）
width = bbox[3] - bbox[0]  # X 轴长度
height = bbox[4] - bbox[1]  # Y 轴长度
depth = bbox[5] - bbox[2]  # Z 轴长度
num = max(width, height, depth)
num = num / 10

shape = cmds.listRelatives(mesh[0], s=1, type='mesh')
cmds.select(shape)

# 方法2：通过创建bifrostGraphShape节点（更底层的控制）
mel.eval('CreateNewBifrostGraph;')
bifrost_graph_shape = cmds.ls(sl=1)[0]
cmds.setAttr(bifrost_graph_shape + '.visibility', 0)

bifrost_graph = cmds.listRelatives(bifrost_graph_shape, p=1)[0]


# 创建初始节点
# 1. 创建mesh_to_level_set节点
mesh_to_level_set = cmds.vnnCompound(bifrost_graph_shape, "/", addNode="BifrostGraph,Geometry::Converters,mesh_to_level_set")[0]
# 1. 为 input 节点创建 mesh 输出端口，类型为 Object
cmds.vnnNode(bifrost_graph_shape, "/input", createOutputPort=("mesh", "Object"), portValues="")
# 2. 连接 input 节点的 mesh 输出到 mesh_to_level_set 节点的 mesh 输入
cmds.vnnConnect(bifrost_graph_shape, ".mesh", "/mesh_to_level_set.mesh", copyMetaData=True)

# 2. 创建volume_to_mesh节点
volume_to_mesh = cmds.vnnCompound(bifrost_graph_shape, "/", addNode="BifrostGraph,Geometry::Converters,volume_to_mesh")[0]
# 3. 连接输入mesh到mesh_to_level_set节点
cmds.vnnConnect(bifrost_graph_shape, ".mesh", "/mesh_to_level_set.mesh")
# 4. 为volume_to_mesh节点创建输入端口
cmds.vnnNode(bifrost_graph_shape, "/volume_to_mesh", createInputPort=("volumes.level_set", "auto"))
# 5. 连接mesh_to_level_set的输出到volume_to_mesh的输入
cmds.vnnConnect(bifrost_graph_shape, "/mesh_to_level_set.level_set", "/volume_to_mesh.volumes.level_set")


# # 6. 创建输入节点的detail_size输出端口
# cmds.vnnNode(bifrost_graph_shape, "/input", createOutputPort=("detail_size", "float"), portValues="0.05")
# # 7. 连接detail_size到mesh_to_level_set节点
# cmds.vnnConnect(bifrost_graph_shape, ".detail_size", "/mesh_to_level_set.detail_size", copyMetaData=True)

for node, attribute_name, attribute_type, attribute_num in zip([mesh_to_level_set, mesh_to_level_set, mesh_to_level_set, mesh_to_level_set,
                                                                volume_to_mesh, volume_to_mesh, volume_to_mesh, volume_to_mesh, volume_to_mesh],
                                                               ['detail_size', 'max_relative_error', 'min_hole_radius', 'thickening',
                                                                'level_set_threshold', 'property_threshold', 'detail_size_scale', 'smoothing', 'enable_subdivision'],
                                                               ['float', 'float', 'float', 'float',
                                                                'float', 'float', 'float', 'float', 'bool'],
                                                               ['0.05', '0.005', '0', '1',
                                                                '0', '0.05', '1', '0.1', '0']):

    cmds.vnnNode(bifrost_graph_shape, '/input', createOutputPort=(attribute_name, attribute_type), portValues=attribute_num)
    cmds.vnnConnect(bifrost_graph_shape, '.'+attribute_name, '/'+node+'.'+attribute_name, copyMetaData=True)

keyable_attrs = cmds.listAttr(bifrost_graph_shape, keyable=True) or []
for node, attribute_name, attribute_type, attribute_num, attribute_enum_text in zip([mesh_to_level_set, mesh_to_level_set, mesh_to_level_set,
                                                                                     volume_to_mesh, volume_to_mesh, volume_to_mesh, volume_to_mesh,],
                                                                                    ['volume_mode', 'adaptivity', 'volume_subdivision_structure',
                                                                                     'mesh_mode', 'contouring_method', 'custom_interior_mode', 'adaptivity'],
                                                                                    ['Geometry::Converters::VolumeMode', 'Geometry::Volume::Adaptivity', 'Geometry::Volume::AutoSubdivisionStructure',
                                                                                     'Geometry::Converters::MeshMode', 'Geometry::Converters::ContouringMethod', 'Geometry::Converters::Interior', 'Geometry::Common::Adaptivity'],
                                                                                    [0, 2, 0,
                                                                                     0, 1, 1, 0],
                                                                                    [['Solid', 'Shell'], ['Optimized', 'VariedFromProperty', 'Off'], ['Automatic', 'Power2', 'Power5'],
                                                                                     ['Automatic', 'Custom'], ['SurfaceNets', 'DualMarchingCubes'], ['Less', 'Greater'], ['Automatic', 'VariedFromProperty', 'Off']]):

    # 3. 创建build_array节点
    build_array = cmds.vnnCompound(bifrost_graph_shape, '/', addNode='BifrostGraph,Core::Array,build_array')[0]

    # 创建value节点
    if attribute_enum_text:
        for i in range(len(attribute_enum_text)):
            value = cmds.vnnCompound(bifrost_graph_shape, '/', addNode='BifrostGraph,Core::Constants,float')[0]

            cmds.vnnNode(bifrost_graph_shape, ('/' + value), setMetaData=('valuenode_type', attribute_type))
            cmds.vnnNode(bifrost_graph_shape, ('/' + value), setPortDefaultValues=('value', str(i)))

            # 4. 连接value节点到build_array
            cmds.vnnPort(bifrost_graph_shape, ('/' + value + '.output'), 1, 1, set=16)
            cmds.vnnNode(bifrost_graph_shape, ('/' + build_array), createInputPort=('output' + str(i), attribute_type))
            cmds.vnnConnect(bifrost_graph_shape, ('/' + value + '.output'), ('/' + build_array + '.output' + str(i)))
            cmds.vnnPort(bifrost_graph_shape, ('/' + value + '.output'), 1, 1, clear=16)

    # 6. 创建get_from_array节点
    get_from_array = cmds.vnnCompound(bifrost_graph_shape, '/', addNode='BifrostGraph,Core::Array,get_from_array')[0]

    # 7. 连接build_array到get_from_array
    cmds.vnnPort(bifrost_graph_shape, ('/'+build_array+'.array'), 1, 1, set=16)
    cmds.vnnConnect(bifrost_graph_shape, ('/'+build_array+'.array'), ('/'+get_from_array+'.array'))
    cmds.vnnPort(bifrost_graph_shape, ('/'+build_array+'.array'), 1, 1, clear=16)

    # 链接存好的数组
    # 8. 连接get_from_array到mesh_to_level_set
    cmds.vnnPort(bifrost_graph_shape, ('/'+get_from_array+'.value'), 1, 1, set=16)
    cmds.vnnConnect(bifrost_graph_shape, ('/'+get_from_array+'.value'), ('/'+node+'.'+attribute_name))
    cmds.vnnPort(bifrost_graph_shape, ('/'+get_from_array+'.value'), 1, 1, clear=16)

    # 9. 设置索引连接
    cmds.vnnPort(bifrost_graph_shape, ('/'+get_from_array+'.index'), 0, 1, set=16)
    aaa = cmds.vnnNode(bifrost_graph_shape, '/input', createOutputPort=(attribute_name, 'long'), portValues='0')

    cmds.vnnConnect(bifrost_graph_shape, '.' + attribute_name, ('/'+get_from_array+'.index'), copyMetaData=True)
    cmds.vnnPort(bifrost_graph_shape, ('/'+get_from_array+'.index'), 0, 1, clear=16)

    new_keyable_attrs = cmds.listAttr(bifrost_graph_shape, keyable=True) or []
    attribute_name = [x for x in new_keyable_attrs if x not in keyable_attrs][0]
    keyable_attrs = new_keyable_attrs

    attribute = ''
    for an in attribute_enum_text:
        attribute += an+':'
    cmds.addAttr(bifrost_graph, ln=attribute_name, en=attribute, at='enum')
    cmds.setAttr(bifrost_graph + '.' + attribute_name, e=1, keyable=True)
    cmds.setAttr(bifrost_graph + '.' + attribute_name, attribute_num)

    cmds.connectAttr(bifrost_graph + '.' + attribute_name, bifrost_graph_shape + '.' + attribute_name)

cmds.setAttr(bifrost_graph_shape+'.detail_size', num)
# 输出
cmds.vnnPort(bifrost_graph_shape, ('/'+volume_to_mesh+'.meshes'), 1, 1, set=16)
cmds.vnnNode(bifrost_graph_shape, '/output', createInputPort=("meshes", "array<Object>"))
cmds.vnnConnect(bifrost_graph_shape, ('/'+volume_to_mesh+'.meshes'), ".meshes")
cmds.vnnPort(bifrost_graph_shape, ('/'+volume_to_mesh+'.meshes'), 1, 1, clear=16)
# 外部链接
bifrostGeoToMaya = cmds.createNode('bifrostGeoToMaya')
cmds.connectAttr(bifrost_graph_shape + '.meshes', bifrostGeoToMaya + '.bifrostGeo')
polyCube = cmds.polyCube(ch=0)
shape = cmds.listRelatives(polyCube, s=1)
cmds.connectAttr(bifrostGeoToMaya + '.mayaMesh[0]', shape[0] + '.inMesh')