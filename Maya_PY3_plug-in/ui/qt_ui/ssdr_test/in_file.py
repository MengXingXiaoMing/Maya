# -*- coding: gbk -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import numpy as np
import os


def import_refined_weights(mesh_name, weight_file):
    if not os.path.exists(weight_file):
        cmds.error("找不到权重文件，请先在 PyCharm 中运行计算。")

    print("正在加载权重文件...")
    weights = np.load(weight_file).flatten()  # 展平以适配 API

    # 1. 获取节点对象
    sel = om.MGlobal.getSelectionListByName(mesh_name)
    mesh_dag = sel.getDagPath(0)

    history = cmds.listHistory(mesh_name)
    sc_list = cmds.ls(history, type="skinCluster")
    if not sc_list: cmds.error("找不到 skinCluster")
    sc_name = sc_list[0]

    sc_obj = om.MGlobal.getSelectionListByName(sc_name).getDependNode(0)
    sc_fn = oma.MFnSkinCluster(sc_obj)

    # 2. 准备数据结构
    joints = cmds.skinCluster(sc_name, q=True, influence=True)
    num_j = len(joints)
    num_v = om.MFnMesh(mesh_dag).numVertices

    if len(weights) != num_v * num_j:
        cmds.error(f"权重数量不匹配！模型需要 {num_v * num_j}, 文件包含 {len(weights)}")

    # 组件列表 (所有顶点)
    v_comp = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
    om.MFnSingleIndexedComponent(v_comp).addElements(om.MIntArray(range(num_v)))

    # 骨骼索引列表
    inf_indices = om.MIntArray(range(num_j))

    # 3. 极速写入
    print("正在写入 SkinCluster...")
    sc_fn.setWeights(mesh_dag, v_comp, inf_indices, om.MDoubleArray(weights), normalize=True)

    print("权重优化完成！")


# --- 运行配置 ---
import_refined_weights("bace_bs_Mesh1", "D:/ssdr_refined.npy")