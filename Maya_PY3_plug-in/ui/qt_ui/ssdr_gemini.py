#coding=gbk
import maya.api.OpenMaya as om
import maya.cmds as cmds
import numpy as np


def get_skin_cluster(mesh_name):
    """获取模型关联的 skinCluster 节点名称"""
    history = cmds.listHistory(mesh_name) or []
    for node in history:
        if cmds.nodeType(node) == "skinCluster":
            return node
    return None


def solve_weights_gd(A, B, iterations=100, learning_rate=0.01):
    """
    使用梯度下降法求解非负最小二乘法 (无需 SciPy)
    A: 变换后的位置矩阵 [3*frames, num_joints]
    B: 实际目标位置向量 [3*frames]
    """
    num_joints = A.shape[1]
    # 初始权重平分
    w = np.ones(num_joints) / num_joints

    # 预计算 AtA 和 AtB 以加速计算
    AtA = A.T @ A
    AtB = A.T @ B

    for _ in range(iterations):
        # 计算梯度: grad = AtAw - AtB
        grad = AtA @ w - AtB
        # 更新
        w = w - learning_rate * grad
        # 约束1: 非负 (ReLU 操作)
        w = np.maximum(1e-6, w)
        # 约束2: 归一化
        total = np.sum(w)
        if total > 0:
            w /= total

    return w


def calculate_inverse_skinning_multi_frame(mesh_name, start_frame, end_frame, step=5):
    """
    主函数：多帧采样并计算权重
    """
    # 1. 初始化和检测
    sc = get_skin_cluster(mesh_name)
    if not sc:
        cmds.error("未找到 skinCluster，请先对模型进行基础蒙皮（即使权重是错的）。")
        return

    joints = cmds.skinCluster(sc, q=True, influence=True)
    num_joints = len(joints)

    sel = om.MSelectionList()
    sel.add(mesh_name)
    mesh_dag = sel.getDagPath(0)
    mesh_fn = om.MFnMesh(mesh_dag)

    num_vertices = mesh_fn.numVertices

    # 获取绑定姿态（从 skinCluster 的 bindPreMatrix 属性获取最准）
    bind_inv_matrices = []
    for i in range(num_joints):
        mat_vals = cmds.getAttr(f"{sc}.bindPreMatrix[{i}]")
        bind_inv_matrices.append(om.MMatrix(mat_vals))

    # 准备存储多帧采样数据的结构
    # 每个顶点都需要一个 A 矩阵和 B 向量
    # vertex_data[v_idx]['A'] = [] ...
    all_A = [[] for _ in range(num_vertices)]
    all_B = [[] for _ in range(num_vertices)]

    # 2. 多帧采样
    original_time = cmds.currentTime(q=True)
    frames = list(range(start_frame, end_frame + 1, step))

    print(f"正在采样 {len(frames)} 帧数据...")
    for f in frames:
        cmds.currentTime(f)

        # 当前帧骨骼的变换矩阵 T = WorldMatrix * BindInverseMatrix
        t_matrices = []
        for i, jnt in enumerate(joints):
            curr_m = om.MMatrix(cmds.getAttr(f"{jnt}.worldMatrix[0]"))
            t_matrices.append(curr_m * bind_inv_matrices[i])

        # 当前帧模型顶点的实际世界坐标 (Deformed Position)
        # 注意：这里假设模型本身没有额外的 Transform 位移，如果有，需要乘模型世界逆矩阵
        curr_points = mesh_fn.getPoints(om.MSpace.kWorld)

        # 假设绑定姿态坐标是固定的（这里取第一帧或从属性取）
        # 如果模型有原位坐标属性（如 origMesh），最好从那里取
        if f == frames[0]:
            bind_points = curr_points  # 简化演示，实际通常通过 getPoints 获取未变形状态

        for v_idx in range(num_vertices):
            p_bind = om.MPoint(bind_points[v_idx])
            p_target = curr_points[v_idx]

            # 填充 A 矩阵的行：每个骨骼如果完全控制该顶点，顶点会去哪
            for j_idx in range(num_joints):
                p_transformed = p_bind * t_matrices[j_idx]
                all_A[v_idx].append([p_transformed.x, p_transformed.y, p_transformed.z])

            # 填充 B 向量：顶点实际去了哪
            all_B[v_idx].extend([p_target.x, p_target.y, p_target.z])

    # 回归原始时间
    cmds.currentTime(original_time)

    # 3. 求解权重
    print("正在计算最佳权重（梯度下降法）...")
    final_weights = []
    for v_idx in range(num_vertices):
        A = np.array(all_A[v_idx]).reshape(-1, num_joints)  # [3*frames, num_joints]
        B = np.array(all_B[v_idx])  # [3*frames]

        w_sol = solve_weights_gd(A, B)
        final_weights.append(w_sol)

        if v_idx % 500 == 0:
            print(f"进度: {v_idx}/{num_vertices}")

    # 4. 应用回 Maya
    print("正在写入权重到 SkinCluster...")
    for v_idx, w_list in enumerate(final_weights):
        for j_idx, val in enumerate(w_list):
            cmds.setAttr(f"{sc}.weightList[{v_idx}].weights[{j_idx}]", val)

    print("计算完成！")

# --- 执行脚本 ---
# 使用方法：选中你的模型，确保它有动画和 skinCluster，然后运行：
calculate_inverse_skinning_multi_frame("pPlane3", 1, 10, step=1)