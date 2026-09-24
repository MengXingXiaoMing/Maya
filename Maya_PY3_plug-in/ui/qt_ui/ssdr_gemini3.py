# coding=gbk
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import numpy as np
import time
import math


def get_mesh_data(mesh_name):
    """使用 API 2.0 快速获取模型数据"""
    sel = om.MSelectionList()
    sel.add(mesh_name)
    dag_path = sel.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path)
    points = np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3]  # 取 XYZ
    return mesh_fn, points, dag_path


def solve_weights_global_optimization(all_A, all_B, num_joints, num_vertices, max_inf=4, iterations=20):
    """
    全局优化方法：同时优化所有顶点的权重
    适用于表情动画（多骨骼协同运动）

    all_A: 列表，每个元素是一个顶点的A矩阵 [3*Frames, J]
    all_B: 列表，每个元素是一个顶点的B向量 [3*Frames]
    """
    print(f"开始全局优化，顶点数: {num_vertices}, 骨骼数: {num_joints}")

    # 初始化权重矩阵 [顶点数, 骨骼数]
    W = np.ones((num_vertices, num_joints)) / num_joints

    # 预计算每个顶点的 A^T A 和 A^T B
    all_AtA = []
    all_AtB = []

    for v_idx in range(num_vertices):
        A = all_A[v_idx]
        B = all_B[v_idx]
        all_AtA.append(A.T @ A)
        all_AtB.append(A.T @ B)

    # 全局迭代优化
    for iter_idx in range(iterations):
        total_error = 0.0

        # 对每个顶点进行坐标下降
        for v_idx in range(num_vertices):
            A = all_A[v_idx]
            B = all_B[v_idx]
            AtA = all_AtA[v_idx]
            AtB = all_AtB[v_idx]
            w = W[v_idx]

            # 对每个骨骼进行坐标下降
            for j in range(num_joints):
                # 计算其他骨骼的贡献
                others_sum = AtA[j].dot(w) - AtA[j, j] * w[j]

                # 更新权重
                if AtA[j, j] > 1e-10:
                    new_w = (AtB[j] - others_sum) / AtA[j, j]
                    w[j] = max(new_w, 0.0)  # 非负约束

            # 归一化
            total = w.sum()
            if total > 0:
                w /= total

            # 计算误差
            predicted = A @ w
            error = np.linalg.norm(predicted - B) / len(B)
            total_error += error

        # 应用稀疏性约束：限制最大影响数
        if iter_idx % 5 == 0:  # 每5次迭代应用一次稀疏约束
            for v_idx in range(num_vertices):
                w = W[v_idx]
                if len(w) > max_inf:
                    # 只保留最大的 max_inf 个权重
                    sorted_indices = np.argsort(w)[::-1]  # 从大到小
                    new_w = np.zeros_like(w)
                    for i in range(min(max_inf, len(w))):
                        new_w[sorted_indices[i]] = w[sorted_indices[i]]

                    # 归一化
                    total = new_w.sum()
                    if total > 0:
                        new_w /= total
                    W[v_idx] = new_w

        avg_error = total_error / num_vertices
        print(f"迭代 {iter_idx + 1}/{iterations}, 平均误差: {avg_error:.6f}")

        if avg_error < 0.001:
            print("已收敛")
            break

    return W


def solve_weights_with_bone_correlation(A, B, num_joints, max_inf=4, iterations=15):
    """
    考虑骨骼相关性的优化方法
    专门处理多骨骼协同运动的表情动画
    """
    # 1. 计算骨骼之间的相关性
    n_bones = num_joints

    # 如果骨骼数量很多，先进行骨骼聚类
    if n_bones > 10:
        # 计算骨骼运动的相关性矩阵
        bone_corr = np.zeros((n_bones, n_bones))
        for i in range(n_bones):
            for j in range(n_bones):
                if i != j:
                    # 使用A矩阵的列来计算骨骼相关性
                    col_i = A[:, i]
                    col_j = A[:, j]
                    corr = np.abs(np.corrcoef(col_i, col_j)[0, 1])
                    bone_corr[i, j] = corr

        # 找出相关性高的骨骼组
        high_corr_groups = []
        for i in range(n_bones):
            for j in range(i + 1, n_bones):
                if bone_corr[i, j] > 0.8:  # 相关性阈值
                    high_corr_groups.append((i, j))

    # 2. 初始化权重
    w = np.ones(n_bones) / n_bones

    # 3. 预计算
    AtA = A.T @ A
    AtB = A.T @ B

    # 4. 添加正则化项，鼓励相关性高的骨骼共享权重
    alpha = 0.01 * np.trace(AtA) / n_bones
    for i in range(n_bones):
        AtA[i, i] += alpha

    # 5. 坐标下降优化
    for _ in range(iterations):
        for i in range(n_bones):
            # 计算其他骨骼的贡献
            others_sum = AtA[i].dot(w) - AtA[i, i] * w[i]

            # 更新权重
            if AtA[i, i] > 1e-10:
                new_w = (AtB[i] - others_sum) / AtA[i, i]
                w[i] = max(new_w, 0.0)

        # 归一化
        total = w.sum()
        if total > 0:
            w /= total

    # 6. 限制最大影响数
    if n_bones > max_inf:
        sorted_indices = np.argsort(w)[::-1]
        new_w = np.zeros(n_bones)
        for i in range(max_inf):
            new_w[sorted_indices[i]] = w[sorted_indices[i]]

        total = new_w.sum()
        if total > 0:
            new_w /= total
        w = new_w

    return w


def run_ssdr_decomposition_expression(mesh_name, start_frame, end_frame, step=2, max_inf=4, use_global=True):
    """
    专门处理表情动画的SSDR分解
    use_global: True使用全局优化，False使用传统方法
    """
    start_time_total = time.time()

    # 1. 基础检查
    history = cmds.listHistory(mesh_name)
    sc = cmds.ls(history, type='skinCluster')
    if not sc:
        joints = cmds.ls(type='joint', selection=True) or []
        if not joints:
            cmds.warning("请先选择骨骼或确保存在皮肤簇")
            return

        sc = cmds.skinCluster(joints, mesh_name, toSelectedBones=True)[0]
        print(f"创建了皮肤簇: {sc}")
    else:
        sc_name = sc[0]

    joints = cmds.skinCluster(sc_name, q=True, influence=True)
    num_joints = len(joints)

    # 获取骨骼名称，用于调试
    print(f"参与计算的骨骼 ({num_joints}个): {joints}")

    # 获取 API 对象
    sel = om.MSelectionList()
    sel.add(sc_name)
    sc_obj = sel.getDependNode(0)
    sc_fn = oma.MFnSkinCluster(sc_obj)
    mesh_fn, _, mesh_dag = get_mesh_data(mesh_name)
    num_verts = mesh_fn.numVertices

    # 2. 收集绑定姿态和动画数据
    bind_inv_mats = []
    for i in range(num_joints):
        try:
            matrix_list = cmds.getAttr(f"{sc_name}.bindPreMatrix[{i}]")
            bind_inv_mats.append(om.MMatrix(matrix_list))
        except:
            joint = joints[i]
            matrix_list = cmds.getAttr(f"{joint}.worldInverseMatrix[0]")
            bind_inv_mats.append(om.MMatrix(matrix_list))

    frames = list(range(start_frame, end_frame + 1, step))
    num_frames = len(frames)

    print(f"开始采样数据：{num_frames} 帧...")

    all_frame_joint_mats = []
    all_frame_vert_pos = []

    old_time = cmds.currentTime(q=True)
    for f in frames:
        cmds.currentTime(f)

        # 获取当前帧骨骼变换 (M * Binv)
        mats = []
        for i, jnt in enumerate(joints):
            try:
                world_m = om.MMatrix(cmds.getAttr(f"{jnt}.worldMatrix[0]"))
                mats.append(world_m * bind_inv_mats[i])
            except:
                # 如果获取失败，使用单位矩阵
                mats.append(om.MMatrix())

        all_frame_joint_mats.append(mats)

        # 获取顶点位置
        all_frame_vert_pos.append(np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3])

    cmds.currentTime(old_time)

    # 参考位姿（用于计算预测位置）
    ref_points = all_frame_vert_pos[0]

    # 3. 求解权重
    print("正在通过坐标下降法计算 SSDR 权重...")

    # 准备所有顶点的A和B数据
    all_A = []  # 每个顶点的A矩阵
    all_B = []  # 每个顶点的B向量

    for v_idx in range(num_verts):
        # 构建 A [3*F, J], B [3*F]
        A = np.zeros((num_frames * 3, num_joints))
        B = np.zeros(num_frames * 3)
        p_ref = om.MPoint(ref_points[v_idx])

        for f_idx in range(num_frames):
            p_actual = all_frame_vert_pos[f_idx][v_idx]
            B[f_idx * 3: f_idx * 3 + 3] = p_actual

            for j_idx in range(num_joints):
                p_pred = p_ref * all_frame_joint_mats[f_idx][j_idx]
                A[f_idx * 3: f_idx * 3 + 3, j_idx] = [p_pred.x, p_pred.y, p_pred.z]

        all_A.append(A)
        all_B.append(B)

    # 选择优化方法
    if use_global:
        print("使用全局优化方法（适合表情动画）...")
        weights = solve_weights_global_optimization(
            all_A, all_B, num_joints, num_verts, max_inf=max_inf
        )
    else:
        print("使用传统方法（逐个顶点优化）...")
        weights = np.zeros((num_verts, num_joints))
        for v_idx in range(num_verts):
            if v_idx % 100 == 0:
                print(f"计算进度: {v_idx}/{num_verts}")

            A = all_A[v_idx]
            B = all_B[v_idx]

            # 使用考虑骨骼相关性的方法
            w = solve_weights_with_bone_correlation(A, B, num_joints, max_inf=max_inf)
            weights[v_idx] = w

    # 4. 使用 API 2.0 批量写入权重
    print("正在批量写入权重到 SkinCluster...")
    inf_indices = om.MIntArray()
    for i in range(num_joints):
        inf_indices.append(i)

    vtx_indices = om.MIntArray()
    for i in range(num_verts):
        vtx_indices.append(i)

    single_id_comp = om.MFnSingleIndexedComponent()
    vtx_comp = single_id_comp.create(om.MFn.kMeshVertComponent)
    single_id_comp.addElements(vtx_indices)

    # 转换权重为 MDoubleArray
    m_weights = om.MDoubleArray()
    for v_idx in range(num_verts):
        for j_idx in range(num_joints):
            m_weights.append(weights[v_idx, j_idx])

    # 写入执行
    sc_fn.setWeights(mesh_dag, vtx_comp, inf_indices, m_weights, normalize=True)

    print(f"全部完成！耗时: {time.time() - start_time_total:.2f}秒")

    # 刷新视图
    cmds.refresh()

    return weights


def analyze_bone_movement(mesh_name, start_frame, end_frame, step=2):
    """
    分析骨骼的运动模式，找出相关性高的骨骼组
    """
    print("分析骨骼运动模式...")

    history = cmds.listHistory(mesh_name)
    sc = cmds.ls(history, type='skinCluster')
    if not sc:
        return None

    sc_name = sc[0]
    joints = cmds.skinCluster(sc_name, q=True, influence=True)
    num_joints = len(joints)

    # 收集骨骼位置数据
    frames = list(range(start_frame, end_frame + 1, step))
    bone_positions = []

    old_time = cmds.currentTime(q=True)
    for f in frames:
        cmds.currentTime(f)
        frame_positions = []
        for joint in joints:
            pos = cmds.xform(joint, q=True, translation=True, ws=True)
            frame_positions.append(pos)
        bone_positions.append(frame_positions)
    cmds.currentTime(old_time)

    # 转换为numpy数组 [frames, joints, 3]
    bone_positions = np.array(bone_positions)

    # 计算骨骼运动的相关性
    print("计算骨骼运动相关性...")
    correlations = np.zeros((num_joints, num_joints))

    for i in range(num_joints):
        for j in range(i + 1, num_joints):
            # 计算位置变化的相关性
            pos_i = bone_positions[:, i, :].flatten()
            pos_j = bone_positions[:, j, :].flatten()

            corr = np.corrcoef(pos_i, pos_j)[0, 1]
            correlations[i, j] = corr
            correlations[j, i] = corr

    # 找出相关性高的骨骼对
    high_corr_pairs = []
    for i in range(num_joints):
        for j in range(i + 1, num_joints):
            if abs(correlations[i, j]) > 0.7:  # 相关性阈值
                high_corr_pairs.append((joints[i], joints[j], correlations[i, j]))

    print(f"找到 {len(high_corr_pairs)} 对高相关性骨骼:")
    for joint1, joint2, corr in high_corr_pairs:
        print(f"  {joint1} - {joint2}: {corr:.3f}")

    return high_corr_pairs, correlations


def create_expression_test_scene():
    """创建表情动画测试场景"""
    print("创建表情动画测试场景...")

    # 创建面部基础网格
    face = cmds.polyPlane(
        width=10,
        height=10,
        subdivisionsX=10,
        subdivisionsY=10,
        name="face_mesh"
    )[0]

    cmds.move(0, 5, 0, face)

    # 创建表情控制骨骼
    joints = []

    # 左眼周围骨骼
    joints.append(cmds.joint(name="L_eyebrow_inner", p=[-2, 8, 0]))
    joints.append(cmds.joint(name="L_eyebrow_outer", p=[-4, 8, 0]))
    joints.append(cmds.joint(name="L_eye_upper", p=[-3, 7, 0]))
    joints.append(cmds.joint(name="L_eye_lower", p=[-3, 6, 0]))

    # 右眼周围骨骼
    joints.append(cmds.joint(name="R_eyebrow_inner", p=[2, 8, 0]))
    joints.append(cmds.joint(name="R_eyebrow_outer", p=[4, 8, 0]))
    joints.append(cmds.joint(name="R_eye_upper", p=[3, 7, 0]))
    joints.append(cmds.joint(name="R_eye_lower", p=[3, 6, 0]))

    # 嘴巴周围骨骼
    joints.append(cmds.joint(name="mouth_left", p=[-2, 4, 0]))
    joints.append(cmds.joint(name="mouth_right", p=[2, 4, 0]))
    joints.append(cmds.joint(name="mouth_upper", p=[0, 5, 0]))
    joints.append(cmds.joint(name="mouth_lower", p=[0, 3, 0]))

    # 设置关键帧姿势
    cmds.currentTime(1)
    cmds.setKeyframe(joints)

    # 表情1：微笑（多骨骼协同）
    cmds.currentTime(10)
    # 嘴角向上
    cmds.move(0, 1, 0, "mouth_left", relative=True)
    cmds.move(0, 1, 0, "mouth_right", relative=True)
    # 眼睛微眯
    cmds.move(0, -0.5, 0, "L_eye_upper", relative=True)
    cmds.move(0, 0.5, 0, "L_eye_lower", relative=True)
    cmds.move(0, -0.5, 0, "R_eye_upper", relative=True)
    cmds.move(0, 0.5, 0, "R_eye_lower", relative=True)
    cmds.setKeyframe(joints)

    # 表情2：惊讶（多骨骼协同）
    cmds.currentTime(20)
    # 眉毛抬高
    cmds.move(0, 1, 0, "L_eyebrow_inner", relative=True)
    cmds.move(0, 1, 0, "L_eyebrow_outer", relative=True)
    cmds.move(0, 1, 0, "R_eyebrow_inner", relative=True)
    cmds.move(0, 1, 0, "R_eyebrow_outer", relative=True)
    # 眼睛睁大
    cmds.move(0, 0.5, 0, "L_eye_upper", relative=True)
    cmds.move(0, -0.5, 0, "L_eye_lower", relative=True)
    cmds.move(0, 0.5, 0, "R_eye_upper", relative=True)
    cmds.move(0, -0.5, 0, "R_eye_lower", relative=True)
    # 嘴巴张大
    cmds.move(0, -0.5, 0, "mouth_upper", relative=True)
    cmds.move(0, 0.5, 0, "mouth_lower", relative=True)
    cmds.setKeyframe(joints)

    # 回到第一帧
    cmds.currentTime(1)

    # 创建皮肤簇
    skin_cluster = cmds.skinCluster(joints, face, toSelectedBones=True)[0]
    print(f"创建皮肤簇: {skin_cluster}")

    # 选择所有对象
    cmds.select([face] + joints)

    print("表情动画测试场景创建完成！")
    return face


def show_expression_ui():
    """显示表情动画专用的UI"""
    window_name = "ssdr_expression_window"

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    window = cmds.window(
        window_name,
        title="表情动画 SSDR 权重工具",
        widthHeight=(450, 400)
    )

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="表情动画 SSDR 权重计算", align="center", font="boldLabelFont")
    cmds.separator(height=10)

    # 网格名称
    cmds.text(label="面部网格名称:", align="left")
    mesh_field = cmds.textField("expr_mesh_field", text="", placeholderText="输入面部网格名称")

    cmds.button(
        label="从选择获取",
        command=lambda *args: cmds.textField(mesh_field, edit=True,
                                             text=cmds.ls(selection=True)[0] if cmds.ls(selection=True) else ""),
        height=25
    )

    cmds.separator(height=10)

    # 帧范围
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[60, 80, 60, 80])
    cmds.text(label="开始帧:")
    start_frame = cmds.intField("expr_start_frame", value=1, minValue=1)
    cmds.text(label="结束帧:")
    end_frame = cmds.intField("expr_end_frame", value=30, minValue=2)
    cmds.setParent("..")

    cmds.separator(height=10)

    # 采样步长和最大影响
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[80, 80, 80, 80])
    cmds.text(label="采样步长:")
    step_field = cmds.intField("expr_step_field", value=1, minValue=1)
    cmds.text(label="最大影响:")
    max_inf_field = cmds.intField("expr_max_inf_field", value=4, minValue=1, maxValue=8)
    cmds.setParent("..")

    cmds.separator(height=10)

    # 优化方法选择
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100, 150, 100])
    cmds.text(label="优化方法:")
    method_menu = cmds.optionMenu("expr_method_menu")
    cmds.menuItem(label="全局优化 (推荐)")
    cmds.menuItem(label="传统方法")
    cmds.text(label="")
    cmds.setParent("..")

    cmds.separator(height=20)

    # 按钮
    cmds.button(
        label="分析骨骼运动",
        command=lambda *args: run_bone_analysis(mesh_field, start_frame, end_frame, step_field),
        height=30
    )

    cmds.button(
        label="创建表情测试场景",
        command=lambda *args: create_expression_test_scene(),
        height=30
    )

    cmds.button(
        label="运行表情SSDR计算",
        command=lambda *args: run_expression_ssdr(mesh_field, start_frame, end_frame, step_field, max_inf_field,
                                                  method_menu),
        height=40,
        backgroundColor=[0.3, 0.5, 0.8]
    )

    cmds.separator(height=10)

    cmds.text(label="说明:", align="left")
    cmds.text(label="1. 全局优化适合多骨骼协同的表情", align="left")
    cmds.text(label="2. 先分析骨骼运动，再计算权重", align="left")
    cmds.text(label="3. 确保每个表情都有关键帧", align="left")

    cmds.showWindow(window)


def run_bone_analysis(mesh_field, start_frame_widget, end_frame_widget, step_widget):
    """运行骨骼运动分析"""
    mesh_name = cmds.textField(mesh_field, query=True, text=True)

    if not mesh_name or not cmds.objExists(mesh_name):
        cmds.warning("请输入有效的网格名称")
        return

    start_frame = cmds.intField(start_frame_widget, query=True, value=True)
    end_frame = cmds.intField(end_frame_widget, query=True, value=True)
    step = cmds.intField(step_widget, query=True, value=True)

    results = analyze_bone_movement(mesh_name, start_frame, end_frame, step)

    if results:
        cmds.confirmDialog(
            title="骨骼运动分析完成",
            message="骨骼运动分析已完成，请查看脚本编辑器输出",
            button=["确定"]
        )


def run_expression_ssdr(mesh_field, start_frame_widget, end_frame_widget, step_widget, max_inf_widget, method_menu):
    """运行表情动画SSDR"""
    mesh_name = cmds.textField(mesh_field, query=True, text=True)

    if not mesh_name or not cmds.objExists(mesh_name):
        cmds.warning("请输入有效的网格名称")
        return

    start_frame = cmds.intField(start_frame_widget, query=True, value=True)
    end_frame = cmds.intField(end_frame_widget, query=True, value=True)
    step = cmds.intField(step_widget, query=True, value=True)
    max_inf = cmds.intField(max_inf_widget, query=True, value=True)
    method = cmds.optionMenu(method_menu, query=True, value=True)

    use_global = (method == "全局优化 (推荐)")

    print(f"开始表情SSDR计算:")
    print(f"  网格: {mesh_name}")
    print(f"  帧范围: {start_frame} - {end_frame}")
    print(f"  采样步长: {step}")
    print(f"  最大影响: {max_inf}")
    print(f"  优化方法: {'全局优化' if use_global else '传统方法'}")

    try:
        weights = run_ssdr_decomposition_expression(
            mesh_name, start_frame, end_frame, step, max_inf, use_global
        )

        if weights is not None:
            cmds.confirmDialog(
                title="完成",
                message="表情SSDR权重计算完成！",
                button=["确定"]
            )
    except Exception as e:
        cmds.warning(f"SSDR计算失败: {str(e)}")
        import traceback
        traceback.print_exc()


# 直接运行
if __name__ == "__main__":
    # 创建一个简单测试
    # create_expression_test_scene()

    # 或者显示UI
    # show_expression_ui()

    # 使用全局优化方法（推荐）
    weights = run_ssdr_decomposition_expression(
        "bace_bs_Mesh1",
        start_frame=1,
        end_frame=35,
        step=1,
        max_inf=8,
        use_global=True
    )