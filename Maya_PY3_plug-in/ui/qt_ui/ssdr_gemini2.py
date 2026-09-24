# coding=gbk
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma  # 添加这个导入
import maya.cmds as cmds
import numpy as np
import time


def get_mesh_data(mesh_name):
    """使用 API 2.0 快速获取模型数据"""
    sel = om.MSelectionList()
    sel.add(mesh_name)
    dag_path = sel.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path)
    points = np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3]  # 取 XYZ
    return mesh_fn, points, dag_path


def solve_weights_coordinate_descent(A, B, max_inf=4, iterations=10):
    """
    SSDR 核心优化器：坐标下降法求解受限最小二乘
    A: 骨骼变形后的预测位置 [3*Frames, Influences]
    B: 顶点的实际变形位置 [3*Frames]
    """
    n_bones = A.shape[1]
    # 初始权重：均匀分布
    w = np.ones(n_bones) / n_bones

    # 预计算 AtA 和 AtB 以大幅提升速度
    AtA = A.T @ A
    AtB = A.T @ B

    for _ in range(iterations):
        for i in range(n_bones):
            # 坐标下降更新公式
            # w_i = (AtB_i - sum_{j!=i} AtA_ij * w_j) / AtA_ii
            others_sum = AtA[i].dot(w) - AtA[i, i] * w[i]
            w[i] = (AtB[i] - others_sum) / (AtA[i, i] + 1e-8)

            # 约束处理：非负
            w[i] = max(0, w[i])

        # 约束处理：归一化
        s = w.sum()
        if s > 0: w /= s

    # 稀疏性处理：保留最大的 N 个影响
    if n_bones > max_inf:
        idx = np.argsort(w)[-max_inf:]
        new_w = np.zeros(n_bones)
        new_w[idx] = w[idx]
        s = new_w.sum()
        if s > 0: new_w /= s
        return new_w
    return w


def run_ssdr_decomposition(mesh_name, start_frame, end_frame, step=2, max_inf=4):
    """主执行函数"""
    start_time_total = time.time()

    # 1. 基础检查
    history = cmds.listHistory(mesh_name)
    sc = cmds.ls(history, type='skinCluster')
    if not sc:
        # 如果没有皮肤簇，创建一个简单的
        joints = cmds.ls(type='joint', selection=True) or []
        if not joints:
            cmds.warning("请先选择骨骼或确保存在皮肤簇")
            return

        # 创建皮肤簇
        sc = cmds.skinCluster(joints, mesh_name, toSelectedBones=True)[0]
        print(f"创建了皮肤簇: {sc}")
    else:
        sc_name = sc[0]

    joints = cmds.skinCluster(sc_name, q=True, influence=True)
    num_joints = len(joints)

    # 获取 API 对象
    sel = om.MSelectionList()
    sel.add(sc_name)
    sc_obj = sel.getDependNode(0)
    sc_fn = oma.MFnSkinCluster(sc_obj)  # 使用 oma 而不是 om
    mesh_fn, _, mesh_dag = get_mesh_data(mesh_name)
    num_verts = mesh_fn.numVertices

    # 2. 收集绑定姿态和动画数据
    # 获取 bindPreMatrix
    bind_inv_mats = []
    for i in range(num_joints):
        # 注意：bindPreMatrix 可能不是每个皮肤簇都有
        # 尝试获取，如果失败则使用世界逆矩阵
        try:
            matrix_list = cmds.getAttr(f"{sc_name}.bindPreMatrix[{i}]")
            bind_inv_mats.append(om.MMatrix(matrix_list))
        except:
            # 如果没有 bindPreMatrix，使用世界逆矩阵作为替代
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
            world_m = om.MMatrix(cmds.getAttr(f"{jnt}.worldMatrix[0]"))
            mats.append(world_m * bind_inv_mats[i])
        all_frame_joint_mats.append(mats)
        # 获取顶点位置
        all_frame_vert_pos.append(np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3])

    cmds.currentTime(old_time)

    # 参考位姿（用于计算预测位置）
    ref_points = all_frame_vert_pos[0]

    # 3. 求解权重
    print("正在通过坐标下降法计算 SSDR 权重...")
    new_weights_flat = np.zeros(num_verts * num_joints)

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

        # 核心求解
        w_optimized = solve_weights_coordinate_descent(A, B, max_inf=max_inf)
        new_weights_flat[v_idx * num_joints: (v_idx + 1) * num_joints] = w_optimized

        if v_idx % 2000 == 0:
            print(f"计算进度: {v_idx}/{num_verts}")

    # 4. 使用 API 2.0 批量写入权重（比 setAttr 快百倍）
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
    for w in new_weights_flat:
        m_weights.append(w)

    # 写入执行
    sc_fn.setWeights(mesh_dag, vtx_comp, inf_indices, m_weights, normalize=True)

    print(f"全部完成！耗时: {time.time() - start_time_total:.2f}秒")

    # 刷新视图
    cmds.refresh()


def create_test_scene():
    """创建测试场景"""
    print("创建测试场景...")

    # 创建立方体
    cube = cmds.polyCube(
        width=2,
        height=6,
        depth=1,
        subdivisionsX=3,
        subdivisionsY=6,
        subdivisionsZ=2,
        name="test_cube"
    )[0]

    cmds.move(0, 3, 0, cube)

    # 创建骨骼
    joints = []

    # 创建根骨骼
    root = cmds.joint(name="root_joint")
    cmds.move(0, 0, 0, root)
    joints.append(root)

    # 创建几个子骨骼
    for i in range(1, 4):
        joint = cmds.joint(name=f"bone_{i}")
        cmds.move(0, i * 2, 0, joint)
        joints.append(joint)

    # 设置关键帧姿势
    cmds.currentTime(1)
    cmds.setKeyframe(joints)

    # 姿势1：弯曲
    cmds.currentTime(10)
    cmds.rotate(30, 0, 0, "bone_1")
    cmds.setKeyframe(joints)

    # 姿势2：扭曲
    cmds.currentTime(20)
    cmds.rotate(-20, 15, 0, "bone_1")
    cmds.rotate(10, 0, 5, "bone_2")
    cmds.setKeyframe(joints)

    # 回到第一帧
    cmds.currentTime(1)

    # 选择所有对象
    cmds.select([cube] + joints)

    print("测试场景创建完成！")
    return cube


def show_ui():
    """显示UI界面"""
    window_name = "ssdr_tool_window"

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    window = cmds.window(
        window_name,
        title="SSDR 权重计算工具",
        widthHeight=(400, 300)
    )

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="SSDR 自动权重计算", align="center", font="boldLabelFont")
    cmds.separator(height=10)

    # 网格名称
    cmds.text(label="网格名称:", align="left")
    mesh_field = cmds.textField("ssdr_mesh_field", text="", placeholderText="输入网格名称")

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
    start_frame = cmds.intField("ssdr_start_frame", value=1, minValue=1)
    cmds.text(label="结束帧:")
    end_frame = cmds.intField("ssdr_end_frame", value=10, minValue=2)
    cmds.setParent("..")

    cmds.separator(height=10)

    # 采样步长
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[80, 80, 80, 80])
    cmds.text(label="采样步长:")
    step_field = cmds.intField("ssdr_step_field", value=2, minValue=1)
    cmds.text(label="最大影响:")
    max_inf_field = cmds.intField("ssdr_max_inf_field", value=4, minValue=1, maxValue=8)
    cmds.setParent("..")

    cmds.separator(height=20)

    # 按钮
    cmds.button(
        label="创建测试场景",
        command=lambda *args: create_test_scene(),
        height=30
    )

    cmds.button(
        label="运行 SSDR 计算",
        command=lambda *args: run_ssdr_from_ui(mesh_field, start_frame, end_frame, step_field, max_inf_field),
        height=40,
        backgroundColor=[0.3, 0.5, 0.8]
    )

    cmds.showWindow(window)


def run_ssdr_from_ui(mesh_field, start_frame_widget, end_frame_widget, step_widget, max_inf_widget):
    """从UI运行SSDR"""
    mesh_name = cmds.textField(mesh_field, query=True, text=True)

    if not mesh_name or not cmds.objExists(mesh_name):
        cmds.warning("请输入有效的网格名称")
        return

    start_frame = cmds.intField(start_frame_widget, query=True, value=True)
    end_frame = cmds.intField(end_frame_widget, query=True, value=True)
    step = cmds.intField(step_widget, query=True, value=True)
    max_inf = cmds.intField(max_inf_widget, query=True, value=True)

    if end_frame <= start_frame:
        cmds.warning("结束帧必须大于开始帧")
        return

    print(f"开始SSDR计算:")
    print(f"  网格: {mesh_name}")
    print(f"  帧范围: {start_frame} - {end_frame}")
    print(f"  采样步长: {step}")
    print(f"  最大影响: {max_inf}")

    # 运行SSDR
    try:
        run_ssdr_decomposition(mesh_name, start_frame, end_frame, step, max_inf)

        # 显示完成消息
        cmds.confirmDialog(
            title="完成",
            message="SSDR权重计算完成！",
            button=["确定"]
        )
    except Exception as e:
        cmds.warning(f"SSDR计算失败: {str(e)}")


# 直接运行UI
if __name__ == "__main__":
    # show_ui()
    run_ssdr_decomposition("bace_bs_Mesh1", start_frame=0, end_frame=33, step=1, max_inf=4)