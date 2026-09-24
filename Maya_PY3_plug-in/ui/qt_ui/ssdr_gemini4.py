# -*- coding: gbk -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import numpy as np
import time


def get_dag_path(node_name):
    sel = om.MGlobal.getSelectionListByName(node_name)
    return sel.getDagPath(0)


def solve_weights_ssdr_advanced(A_tensor, B_matrix, max_inf=5, lambda_reg=0.8):
    """
    强化版求解器：引入数据中心化和强正则化
    A_tensor: [Frames, 3, Joints]
    B_matrix: [Frames, 3]
    """
    num_frames, _, num_joints = A_tensor.shape

    # 1. 数据中心化 (Data Centering) - 消除背景位移干扰，只看形变趋势
    # 这一步是面部权重计算的灵魂
    A_flat = A_tensor.reshape(-1, num_joints)
    B_flat = B_matrix.reshape(-1)

    A_mean = np.mean(A_flat, axis=0)
    B_mean = np.mean(B_flat)

    A_centered = A_flat - A_mean
    B_centered = B_flat - B_mean

    # 2. 构造协方差阵
    AtA = A_centered.T @ A_centered
    AtB = A_centered.T @ B_centered

    # 3. 强正则化：处理面部骨骼同步运动 (Multicollinearity)
    # lambda_reg 越高，权重越平滑；越低，权重越锐利
    reg = np.eye(num_joints) * (lambda_reg * np.mean(np.diag(AtA)) + 1e-6)

    try:
        # 初始解：岭回归
        w = np.linalg.solve(AtA + reg, AtB)
    except:
        w = np.ones(num_joints) / num_joints

    # 4. 非负约束与稀疏化 (Top-K)
    w[w < 0] = 0
    relevant_idx = np.argsort(w)[-max_inf:]

    # 5. 子空间投影优化 (精细化计算选中的骨骼)
    A_sub = A_centered[:, relevant_idx]
    AtA_s = A_sub.T @ A_sub
    AtB_s = A_sub.T @ B_centered

    w_sub = np.ones(len(relevant_idx)) / len(relevant_idx)
    for _ in range(20):  # 增加迭代次数提高精度
        for i in range(len(relevant_idx)):
            res = AtB_s[i] - np.dot(AtA_s[i], w_sub) + AtA_s[i, i] * w_sub[i]
            w_sub[i] = max(0, res / (AtA_s[i, i] + 1e-9))

    # 6. 最终归一化
    final_w = np.zeros(num_joints)
    sum_w = np.sum(w_sub)
    if sum_w > 1e-6:
        final_w[relevant_idx] = w_sub / sum_w
    return final_w


def run_facial_ssdr_pro(mesh_name, start_frame, end_frame, max_inf=4):
    start_t = time.time()

    # 节点准备
    history = cmds.listHistory(mesh_name)
    sc = cmds.ls(history, type="skinCluster")[0]
    joints = cmds.skinCluster(sc, q=True, influence=True)
    num_j = len(joints)

    mesh_dag = get_dag_path(mesh_name)
    mesh_fn = om.MFnMesh(mesh_dag)
    sc_fn = oma.MFnSkinCluster(om.MGlobal.getSelectionListByName(sc).getDependNode(0))
    num_v = mesh_fn.numVertices

    # 获取 BindPose
    bind_invs = [om.MMatrix(cmds.getAttr(f"{sc}.bindPreMatrix[{i}]")) for i in range(num_j)]

    # 采样数据
    frames = list(range(start_frame, end_frame + 1))
    num_f = len(frames)

    all_j_mats = np.zeros((num_f, num_j, 4, 4), dtype=np.float32)
    all_v_pos = np.zeros((num_f, num_v, 3), dtype=np.float32)

    print(f"正在采样 {num_f} 帧数据...")
    curr = cmds.currentTime(q=True)
    for i, f in enumerate(frames):
        cmds.currentTime(f)
        all_v_pos[i] = np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3]
        for j in range(num_j):
            wm = om.MMatrix(cmds.getAttr(f"{joints[j]}.worldMatrix[0]"))
            all_j_mats[i, j] = np.array(wm * bind_invs[j]).reshape(4, 4)
    cmds.currentTime(curr)

    # 预计算
    ref_pos_h = np.ones((num_v, 4), dtype=np.float32)
    ref_pos_h[:, :3] = all_v_pos[0]
    final_weights = np.zeros(num_v * num_j)

    print("开始深度优化权重...")
    for v in range(num_v):
        # 向量化预测位置
        p_ref = ref_pos_h[v]
        preds = np.einsum('fjik,k->fji', all_j_mats, p_ref)
        A_v = preds[:, :, :3].transpose(0, 2, 1)
        B_v = all_v_pos[:, v, :]

        # 调用强化求解器
        w = solve_weights_ssdr_advanced(A_v, B_v, max_inf=max_inf, lambda_reg=0.8)
        final_weights[v * num_j: (v + 1) * num_j] = w

    # 写入
    v_idx_arr = om.MIntArray(range(num_v))
    j_idx_arr = om.MIntArray(range(num_j))
    sic = om.MFnSingleIndexedComponent()
    v_comp = sic.create(om.MFn.kMeshVertComponent)
    sic.addElements(v_idx_arr)

    sc_fn.setWeights(mesh_dag, v_comp, j_idx_arr, om.MDoubleArray(final_weights), normalize=True)
    print(f"完成！耗时: {time.time() - start_t:.2f}s")


# 运行
run_facial_ssdr_pro("bace_bs_Mesh1", 1, 35, max_inf=5)