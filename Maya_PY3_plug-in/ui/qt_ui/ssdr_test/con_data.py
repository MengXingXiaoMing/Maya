# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import nnls


def solve_ssdr_v3(input_path, output_path, max_inf=4):
    data = np.load(input_path)
    # v_pos 是采样到的世界坐标 [F, V, 3]
    v_pos = data['v_pos']
    j_mats = data['j_mats']  # [F, J, 4, 4]
    b_inv = data['bind_invs']  # [J, 4, 4]
    w_init = data['init_weights']  # [V, J]

    num_f, num_v, _ = v_pos.shape
    num_j = j_mats.shape[1]

    # 1. 将所有数据转换到相对第一帧的“形变空间”
    # 第一帧作为 Bind Pose (参考姿态)
    ref_points = v_pos[0]  # [V, 3]

    # 计算每一帧相对于第一帧的骨骼增量矩阵: M_delta = M_bindInv * M_currWorld
    # 注意：在 Maya 中是 点 * Matrix，所以顺序必须极其精确
    delta_mats = np.zeros((num_f, num_j, 4, 4))
    for f in range(num_f):
        for j in range(num_j):
            # Maya 逻辑：P_bind * (InverseBind * World)
            delta_mats[f, j] = b_inv[j] @ j_mats[f, j]

    final_weights = np.zeros((num_v, num_j))

    print("正在执行 V3 修正版解算 (对齐 Maya 变形逻辑)...")

    for v in range(num_v):
        p_ref = np.append(ref_points[v], 1.0)  # 转为齐次坐标 [4]

        # A 矩阵：每根骨骼如果单独作用，顶点会跑到哪？
        # B 向量：顶点实际跑到了哪？
        A = np.zeros((num_f * 3, num_j))
        for j in range(num_j):
            # 模拟计算：P_deformed = P_ref * DeltaMatrix
            # 在 NumPy 中，(1,4) @ (4,4) 得到变形后的点
            p_transformed = (p_ref @ delta_mats[:, j])[:, :3]  # [Frames, 3]
            A[:, j] = p_transformed.flatten()

        B = v_pos[:, v, :].flatten()

        # --- 核心改进：引入权重先验约束 ---
        # 只在初始权重不为 0 的骨骼周围寻找解，防止权重飞到不相关的骨骼上
        active_indices = np.where(w_init[v] > 0.001)[0]
        # 如果初始权重太烂，扩大搜索范围到最近的几根骨骼
        if len(active_indices) < 2:
            # 找到 A 矩阵中与 B 最接近的几列
            correlations = [np.corrcoef(A[:, i], B)[0, 1] for i in range(num_j)]
            active_indices = np.argsort(correlations)[-8:]  # 扩大到8根备选

        A_sub = A[:, active_indices]

        try:
            # 在受限空间内解 NNLS
            w_sub, _ = nnls(A_sub, B)
        except:
            w_sub = w_init[v][active_indices]

        # 写回全局权重
        w_final = np.zeros(num_j)
        w_final[active_indices] = w_sub

        # 稀疏化与归一化
        if np.count_nonzero(w_final) > max_inf:
            w_final[np.argsort(w_final)[:-max_inf]] = 0

        sum_w = w_final.sum()
        if sum_w > 1e-6:
            w_final /= sum_w
        else:
            w_final = w_init[v]  # 彻底失败则退回初始

        final_weights[v] = w_final

        if v % 2000 == 0:
            print(f"解算进度: {v}/{num_v}")

    np.save(output_path, final_weights)
    print("修正版计算完成。")


solve_ssdr_v3("D:/ssdr_source.npz", "D:/ssdr_refined.npy", max_inf=4)