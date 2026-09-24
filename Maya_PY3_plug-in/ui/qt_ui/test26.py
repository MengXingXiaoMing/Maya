import maya.cmds as cmds
import maya.mel as mel


def voxelization_procedural():
    # 1. 检查并获取选择的物体
    sel = cmds.ls(sl=True)
    if not sel:
        return cmds.warning('请先选择一个多边形模型！')

    mesh_transform = sel[0]
    shapes = cmds.listRelatives(mesh_transform, shapes=True, type='mesh')
    if not shapes:
        return cmds.warning('选择的对象没有网格节点 (Shape)！')
    source_shape = shapes[0]

    # 计算初始的体素大小 (detail_size)
    bbox = cmds.xform(mesh_transform, query=True, boundingBox=True, worldSpace=True)
    width, height, depth = bbox[3] - bbox[0], bbox[4] - bbox[1], bbox[5] - bbox[2]
    initial_detail_size = max(width, height, depth) / 20.0

    cmds.undoInfo(openChunk=True)
    try:
        # 2. 确保 Bifrost 插件已加载
        if not cmds.pluginInfo('bifrostGraph', query=True, loaded=True):
            cmds.loadPlugin('bifrostGraph')

        # 3. 安全创建并获取 Bifrost Graph 节点
        graphs_before = set(cmds.ls(type='bifrostGraphShape'))
        mel.eval('CreateNewBifrostGraph;')
        graphs_after = set(cmds.ls(type='bifrostGraphShape'))

        # 精确捕获新生成的 Shape 节点，避免 selection 带来的不确定性
        bifrost_shape = list(graphs_after - graphs_before)[0]
        bifrost_transform = cmds.listRelatives(bifrost_shape, parent=True)[0]

        cmds.setAttr(bifrost_transform + '.visibility', 0)

        # 4. 创建 Bifrost 内部转换节点 (使用现代标准节点)
        node_vol = cmds.vnnCompound(bifrost_shape, "/", addNode="BifrostGraph,Geometry::Volume,convert_to_volume")[0]
        node_mesh = cmds.vnnCompound(bifrost_shape, "/", addNode="BifrostGraph,Geometry::Mesh,convert_to_mesh")[0]

        # 5. 设置输入端口 (这就是实现外部调节参数的秘诀！)
        # 创建 Object 类型的 mesh 输入端 (不要给 portValues)
        cmds.vnnNode(bifrost_shape, "/input", createOutputPort=("in_mesh", "Object"))

        # 创建 detail_size 输入端 (Bifrost会自动在外部生成这个属性)
        cmds.vnnNode(bifrost_shape, "/input", createOutputPort=("detail_size", "float"))
        cmds.vnnNode(bifrost_shape, "/input", setPortDefaultValues=("detail_size", str(initial_detail_size)))

        # (可选) 你还可以暴露其他参数，比如 smoothing 平滑度
        cmds.vnnNode(bifrost_shape, "/input", createOutputPort=("smoothing", "float"))
        cmds.vnnNode(bifrost_shape, "/input", setPortDefaultValues=("smoothing", "0.0"))

        # 6. 进行内部连线 (Input -> Volume -> Mesh -> Output)
        cmds.vnnConnect(bifrost_shape, "in_mesh", f"/{node_vol}.geometry")
        cmds.vnnConnect(bifrost_shape, "detail_size", f"/{node_vol}.detail_size")

        cmds.vnnConnect(bifrost_shape, f"/{node_vol}.volume", f"/{node_mesh}.volume")
        cmds.vnnConnect(bifrost_shape, "smoothing", f"/{node_mesh}.smoothing")  # 连入平滑度参数

        # 设置输出端
        cmds.vnnNode(bifrost_shape, "/output", createInputPort=("out_mesh", "Object"))
        cmds.vnnConnect(bifrost_shape, f"/{node_mesh}.mesh", "out_mesh")

        # 7. 外部连接：将 Maya 模型数据喂给 Bifrost
        cmds.connectAttr(source_shape + ".outMesh", bifrost_transform + ".in_mesh")

        # 8. 外部连接：将 Bifrost 结果输出回 Maya 实体模型
        bifrostGeoToMaya = cmds.createNode('bifrostGeoToMaya')
        cmds.connectAttr(bifrost_transform + '.out_mesh', bifrostGeoToMaya + '.bifrostGeo')

        # 创建接收网格并连接
        output_mesh_transform = cmds.polyCube(ch=False, name=mesh_transform + "_Voxelized")[0]
        output_shape = cmds.listRelatives(output_mesh_transform, shapes=True)[0]
        cmds.connectAttr(bifrostGeoToMaya + '.mayaMesh[0]', output_shape + '.inMesh')

        # 清理操作
        cmds.select(bifrost_transform)
        print("? 体素化完成！请在右侧通道盒(Channel Box) 或 属性编辑器调节 'detail_size' 与 'smoothing' 参数。")

    except Exception as e:
        cmds.warning(f"发生错误: {e}")
    finally:
        cmds.undoInfo(closeChunk=True)


voxelization_procedural()