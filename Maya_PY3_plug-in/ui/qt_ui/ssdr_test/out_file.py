# -*- coding: gbk -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma  # 必须引入这个模块
import maya.cmds as cmds
import numpy as np


def export_with_initial_weights(mesh_name, start_frame, end_frame, save_path):
    # 1. 节点检测
    if not cmds.objExists(mesh_name):
        cmds.error(f"找不到模型: {mesh_name}")

    history = cmds.listHistory(mesh_name)
    sc_list = cmds.ls(history, type="skinCluster")
    if not sc_list:
        cmds.error("模型没有蒙皮 (skinCluster)")
    sc_name = sc_list[0]

    joints = cmds.skinCluster(sc_name, q=True, influence=True)
    num_j = len(joints)

    # 获取 API 对象
    sel = om.MGlobal.getSelectionListByName(mesh_name)
    mesh_dag = sel.getDagPath(0)
    mesh_fn = om.MFnMesh(mesh_dag)
    num_v = mesh_fn.numVertices

    # 【修正处】使用 OpenMayaAnim 获取 SkinCluster 函数集
    sc_sel = om.MGlobal.getSelectionListByName(sc_name)
    sc_obj = sc_sel.getDependNode(0)
    sc_fn = oma.MFnSkinCluster(sc_obj)  # 正确的模块是 oma

    # 2. 获取初始权重 (Initial Weights)
    print("正在从 SkinCluster 读取当前权重...")
    # API 2.0 getWeights 返回 (weightsArray, numInfluence)
    weights_flat, _ = sc_fn.getWeights(mesh_dag, om.MObject())
    init_weights = np.array(weights_flat).reshape(num_v, num_j)

    # 3. 获取 BindPreMatrix (逆矩阵)
    bind_invs = [np.array(cmds.getAttr(f"{sc_name}.bindPreMatrix[{i}]")).reshape(4, 4) for i in range(num_j)]

    # 4. 采样动画数据
    frames = list(range(start_frame, end_frame + 1))
    v_pos_list = []
    j_mat_list = []

    print(f"正在采样 {len(frames)} 帧动画数据...")
    curr = cmds.currentTime(q=True)
    for f in frames:
        cmds.currentTime(f)
        # 获取世界空间顶点位置
        v_pos_list.append(np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3])
        # 采集骨骼世界矩阵
        mats = [np.array(cmds.getAttr(f"{j}.worldMatrix[0]")).reshape(4, 4) for j in joints]
        j_mat_list.append(mats)
    cmds.currentTime(curr)

    # 5. 保存数据
    np.savez(save_path,
             v_pos=np.array(v_pos_list),
             j_mats=np.array(j_mat_list),
             bind_invs=np.array(bind_invs),
             init_weights=init_weights,
             joints=joints)

    print(f"导出成功！文件已保存至: {save_path}")


# --- 运行 ---
# 请确保模型名正确，路径有写入权限
export_with_initial_weights("bace_bs_Mesh", 1, 35, "D:/ssdr_source.npz")