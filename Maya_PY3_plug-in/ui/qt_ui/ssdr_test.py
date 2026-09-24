"""
Maya 2025 SSDR 自动权重工具 - 修复版本
按钮回调函数已修正
"""

import maya.cmds as cmds
import math
import time
import json
import os

class SimpleMath:
    """简化数学运算类，替代 numpy"""

    @staticmethod
    def array(data):
        """创建数组"""
        if isinstance(data, list):
            return data
        return [data]

    @staticmethod
    def zeros(shape):
        """创建零数组"""
        if isinstance(shape, int):
            return [0.0] * shape
        elif isinstance(shape, tuple):
            if len(shape) == 1:
                return [0.0] * shape[0]
            elif len(shape) == 2:
                return [[0.0] * shape[1] for _ in range(shape[0])]
        return []

    @staticmethod
    def ones(shape):
        """创建一数组"""
        if isinstance(shape, int):
            return [1.0] * shape
        elif isinstance(shape, tuple):
            if len(shape) == 1:
                return [1.0] * shape[0]
            elif len(shape) == 2:
                return [[1.0] * shape[1] for _ in range(shape[0])]
        return []

    @staticmethod
    def dot(a, b):
        """点积"""
        if isinstance(a[0], list) and isinstance(b[0], list):
            # 矩阵乘法
            rows_a = len(a)
            cols_a = len(a[0])
            rows_b = len(b)
            cols_b = len(b[0])

            if cols_a != rows_b:
                raise ValueError("矩阵维度不匹配")

            result = [[0.0] * cols_b for _ in range(rows_a)]
            for i in range(rows_a):
                for j in range(cols_b):
                    for k in range(cols_a):
                        result[i][j] += a[i][k] * b[k][j]
            return result
        elif isinstance(a[0], list) and not isinstance(b[0], list):
            # 矩阵向量乘法
            rows = len(a)
            cols = len(a[0])
            if cols != len(b):
                raise ValueError("维度不匹配")

            result = [0.0] * rows
            for i in range(rows):
                for j in range(cols):
                    result[i] += a[i][j] * b[j]
            return result
        else:
            # 向量点积
            if len(a) != len(b):
                raise ValueError("向量长度不匹配")
            return sum(ai * bi for ai, bi in zip(a, b))

    @staticmethod
    def norm(vec):
        """向量范数"""
        if isinstance(vec[0], list):
            # 如果是矩阵，展平
            flat = [item for row in vec for item in row]
            return math.sqrt(sum(x*x for x in flat))
        else:
            return math.sqrt(sum(x*x for x in vec))

    @staticmethod
    def transpose(matrix):
        """转置矩阵"""
        if not matrix or not isinstance(matrix[0], list):
            return matrix

        rows = len(matrix)
        cols = len(matrix[0])
        return [[matrix[j][i] for j in range(rows)] for i in range(cols)]

    @staticmethod
    def argmax(array):
        """返回最大值的索引"""
        max_val = max(array)
        return array.index(max_val)

    @staticmethod
    def argsort(array, reverse=False):
        """返回排序后的索引"""
        return sorted(range(len(array)), key=lambda i: array[i], reverse=reverse)

    @staticmethod
    def mean(array):
        """计算平均值"""
        if not array:
            return 0
        return sum(array) / len(array)

    @staticmethod
    def subtract(a, b):
        """减法"""
        if isinstance(a[0], list) and isinstance(b[0], list):
            # 矩阵减法
            return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
        elif not isinstance(a[0], list) and not isinstance(b[0], list):
            # 向量减法
            return [ai - bi for ai, bi in zip(a, b)]
        else:
            raise ValueError("类型不匹配")

# 使用我们的简单数学库
np = SimpleMath()

class SimpleSSDR:
    """完全无依赖的 SSDR 实现"""

    def __init__(self):
        self.mesh = None
        self.joints = []
        self.weights = None

    def get_vertex_positions(self, mesh_name):
        """获取顶点位置"""
        vtx_count = cmds.polyEvaluate(mesh_name, vertex=True)
        positions = []

        for i in range(vtx_count):
            vtx_name = f"{mesh_name}.vtx[{i}]"
            pos = cmds.xform(vtx_name, q=True, translation=True, ws=True)
            positions.append(list(pos))

        return positions

    def get_joint_matrices(self, joint_list):
        """获取关节变换矩阵"""
        matrices = []

        for joint in joint_list:
            matrix_list = cmds.xform(joint, q=True, matrix=True, ws=True)
            # 转换为 4x4 矩阵
            matrix = [matrix_list[i:i+4] for i in range(0, 16, 4)]
            matrices.append(matrix)

        return matrices

    def solve_linear_equations(self, A, b):
        """解线性方程组（使用简单的高斯消元法）"""
        n = len(A)
        m = len(A[0])

        # 创建增广矩阵
        M = [row[:] + [b[i]] for i, row in enumerate(A)]

        # 高斯消元
        for col in range(min(n, m)):
            # 寻找主元
            max_row = col
            for row in range(col + 1, n):
                if abs(M[row][col]) > abs(M[max_row][col]):
                    max_row = row

            # 交换行
            M[col], M[max_row] = M[max_row], M[col]

            # 消元
            for row in range(col + 1, n):
                factor = M[row][col] / M[col][col] if M[col][col] != 0 else 0
                for j in range(col, m + 1):
                    M[row][j] -= factor * M[col][j]

        # 回代
        x = [0.0] * m
        for i in range(min(n, m) - 1, -1, -1):
            if M[i][i] != 0:
                x[i] = M[i][m] / M[i][i]
                for k in range(i - 1, -1, -1):
                    M[k][m] -= M[k][i] * x[i]

        return x

    def compute_weights(self, V_rest, V_deformed, T_joints, max_iter=10, max_influences=4):
        """计算权重"""
        num_vertices = len(V_rest)
        num_frames = len(V_deformed)
        num_joints = len(T_joints[0])

        # 初始化权重
        weights = np.ones((num_vertices, num_joints))
        for i in range(num_vertices):
            total = sum(weights[i])
            weights[i] = [w/total for w in weights[i]]

        # 迭代优化
        for iteration in range(max_iter):
            print(f"迭代 {iteration + 1}/{max_iter}")

            # 对每个顶点优化权重
            for v_idx in range(num_vertices):
                # 构建线性方程组
                equations = []
                targets = []

                for f_idx in range(num_frames):
                    for dim in range(3):  # x, y, z
                        equation = []
                        for j_idx in range(num_joints):
                            # 计算变换后的顶点位置
                            v = V_rest[v_idx] + [1.0]  # 齐次坐标
                            T = T_joints[f_idx][j_idx]

                            # 矩阵乘法
                            transformed = [
                                T[0][0]*v[0] + T[0][1]*v[1] + T[0][2]*v[2] + T[0][3]*v[3],
                                T[1][0]*v[0] + T[1][1]*v[1] + T[1][2]*v[2] + T[1][3]*v[3],
                                T[2][0]*v[0] + T[2][1]*v[1] + T[2][2]*v[2] + T[2][3]*v[3]
                            ]

                            equation.append(transformed[dim])

                        equations.append(equation)
                        targets.append(V_deformed[f_idx][v_idx][dim])

                # 解方程组
                if equations and len(equations[0]) > 0:
                    new_weights = self.solve_linear_equations(equations, targets)

                    # 确保权重非负
                    new_weights = [max(w, 0) for w in new_weights]

                    # 归一化
                    total = sum(new_weights)
                    if total > 0:
                        weights[v_idx] = [w/total for w in new_weights]

            # 限制最大影响数
            weights = self.limit_influences(weights, max_influences)

            # 计算误差
            error = self.compute_error(V_rest, V_deformed, T_joints, weights)
            print(f"  误差: {error:.6f}")

            if error < 0.001:
                break

        return weights

    def limit_influences(self, weights, max_influences):
        """限制最大影响数"""
        num_vertices = len(weights)
        num_joints = len(weights[0])

        result = [[0.0] * num_joints for _ in range(num_vertices)]

        for v_idx in range(num_vertices):
            # 找到权重最大的几个关节
            sorted_indices = np.argsort(weights[v_idx])
            sorted_indices.reverse()  # 从大到小

            top_indices = sorted_indices[:max_influences]
            total = sum(weights[v_idx][j] for j in top_indices)

            if total > 0:
                for j_idx in top_indices:
                    result[v_idx][j_idx] = weights[v_idx][j_idx] / total
            else:
                # 平均分配
                for j in range(max_influences):
                    result[v_idx][j] = 1.0 / max_influences

        return result

    def compute_error(self, V_rest, V_deformed, T_joints, weights):
        """计算重建误差"""
        num_vertices = len(V_rest)
        num_frames = len(V_deformed)
        num_joints = len(T_joints[0])

        total_error = 0.0
        total_points = 0

        for f_idx in range(num_frames):
            for v_idx in range(num_vertices):
                predicted = [0.0, 0.0, 0.0]

                for j_idx in range(num_joints):
                    w = weights[v_idx][j_idx]
                    if w > 0.001:
                        v = V_rest[v_idx] + [1.0]
                        T = T_joints[f_idx][j_idx]

                        transformed = [
                            T[0][0]*v[0] + T[0][1]*v[1] + T[0][2]*v[2] + T[0][3]*v[3],
                            T[1][0]*v[0] + T[1][1]*v[1] + T[1][2]*v[2] + T[1][3]*v[3],
                            T[2][0]*v[0] + T[2][1]*v[1] + T[2][2]*v[2] + T[2][3]*v[3]
                        ]

                        for dim in range(3):
                            predicted[dim] += w * transformed[dim]

                actual = V_deformed[f_idx][v_idx]
                error = math.sqrt(
                    (predicted[0] - actual[0])**2 +
                    (predicted[1] - actual[1])**2 +
                    (predicted[2] - actual[2])**2
                )

                total_error += error
                total_points += 1

        return total_error / total_points if total_points > 0 else 0.0

    def apply_weights(self, mesh, joints, weights):
        """应用权重到皮肤簇"""
        print("应用权重...")

        # 创建或获取皮肤簇
        skin_cluster = None
        history = cmds.listHistory(mesh) or []

        for node in history:
            if cmds.nodeType(node) == 'skinCluster':
                skin_cluster = node
                break

        if not skin_cluster:
            # 创建新的皮肤簇
            try:
                skin_cluster = cmds.skinCluster(
                    joints,
                    mesh,
                    toSelectedBones=True,
                    maximumInfluences=4
                )[0]
            except:
                cmds.warning("无法创建皮肤簇")
                return None

        # 清除现有权重
        cmds.skinPercent(skin_cluster, mesh, normalize=False, pruneWeights=100)

        # 应用新权重
        vtx_count = len(weights)

        for v_idx in range(vtx_count):
            weight_list = []

            for j_idx, w in enumerate(weights[v_idx]):
                if w > 0.001:
                    weight_list.append((joints[j_idx], w))

            if weight_list:
                vtx_name = f"{mesh}.vtx[{v_idx}]"
                try:
                    cmds.skinPercent(
                        skin_cluster,
                        vtx_name,
                        transformValue=weight_list,
                        normalize=False
                    )
                except:
                    pass

        # 最终归一化
        cmds.skinPercent(skin_cluster, mesh, normalize=True)

        print("权重应用完成")
        return skin_cluster

class SimpleSSDRUI:
    """简单的 SSDR 用户界面"""

    @staticmethod
    def show_window():
        """显示主窗口"""
        window_name = "simple_ssdr_window"

        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name)

        window = cmds.window(
            window_name,
            title="简单 SSDR 权重工具",
            widthHeight=(350, 300)
        )

        cmds.columnLayout(adjustableColumn=True)

        cmds.separator(height=10)
        cmds.text(label="简单 SSDR 权重计算", align="center", font="boldLabelFont")
        cmds.separator(height=10)

        cmds.text(label="使用步骤:", align="left")
        cmds.text(label="1. 选择模型和骨骼", align="left")
        cmds.text(label="2. 设置几个姿势关键帧", align="left")
        cmds.text(label="3. 点击下面的按钮", align="left")

        cmds.separator(height=20)

        # 修复按钮回调：使用lambda或带参数的函数
        cmds.button(
            label="创建测试场景",
            command=lambda *args: SimpleSSDRUI.create_test_scene(),
            height=30
        )

        cmds.separator(height=10)

        cmds.button(
            label="运行 SSDR 计算",
            command=lambda *args: SimpleSSDRUI.run_calculation(),
            height=40,
            backgroundColor=[0.3, 0.5, 0.8]
        )

        cmds.separator(height=10)

        cmds.text(label="注意: 这是一个简化版本", align="center")
        cmds.text(label="适合简单模型和骨骼", align="center")

        cmds.showWindow(window)

    @staticmethod
    def create_test_scene(*args):  # 添加*args参数以接收Maya的回调参数
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

        # 显示提示
        cmds.confirmDialog(
            title="测试场景已创建",
            message="已创建立方体和骨骼链\n\n现在请点击'运行 SSDR 计算'按钮",
            button=["确定"]
        )

    @staticmethod
    def run_calculation(*args):  # 添加*args参数以接收Maya的回调参数
        """运行 SSDR 计算"""
        selection = cmds.ls(selection=True)

        if not selection:
            cmds.warning("请先选择模型和骨骼")
            return

        # 分离模型和骨骼
        meshes = []
        joints = []

        for obj in selection:
            # 检查是否为网格
            shapes = cmds.listRelatives(obj, shapes=True) or []
            for shape in shapes:
                if cmds.nodeType(shape) == 'mesh':
                    meshes.append(obj)
                    break

            # 检查是否为关节
            if cmds.nodeType(obj) == 'joint':
                joints.append(obj)

        if not meshes:
            cmds.warning("没有找到网格对象")
            return

        if not joints:
            cmds.warning("没有找到骨骼对象")
            return

        mesh = meshes[0]
        joints = joints

        print(f"使用网格: {mesh}")
        print(f"使用骨骼: {joints}")

        # 收集数据
        print("收集数据...")

        # 获取关键帧范围
        keyframes = []
        for joint in joints:
            keys = cmds.keyframe(joint, query=True, timeChange=True) or []
            keyframes.extend(keys)

        if not keyframes:
            cmds.warning("没有找到关键帧，请至少设置2个姿势")
            return

        keyframes = sorted(set(keyframes))
        print(f"找到关键帧: {keyframes}")

        # 收集每个关键帧的数据
        V_deformed = []  # 变形后的顶点位置
        T_joints = []    # 关节变换矩阵

        current_time = cmds.currentTime(q=True)

        for frame in keyframes:
            cmds.currentTime(frame)
            print(f"  收集第 {frame} 帧...")

            # 获取顶点位置
            vtx_positions = []
            vtx_count = cmds.polyEvaluate(mesh, vertex=True)

            for i in range(vtx_count):
                vtx_name = f"{mesh}.vtx[{i}]"
                pos = cmds.xform(vtx_name, q=True, translation=True, ws=True)
                vtx_positions.append(list(pos))

            V_deformed.append(vtx_positions)

            # 获取关节变换矩阵
            joint_matrices = []
            for joint in joints:
                matrix_list = cmds.xform(joint, q=True, matrix=True, ws=True)
                matrix = [matrix_list[i:i+4] for i in range(0, 16, 4)]
                joint_matrices.append(matrix)

            T_joints.append(joint_matrices)

        cmds.currentTime(current_time)

        # 第一帧作为 T-pose
        V_rest = V_deformed[0]

        print(f"数据收集完成: {len(V_deformed)} 个姿势, {len(V_rest)} 个顶点")

        # 创建 SSDR 实例并计算权重
        ssdr = SimpleSSDR()

        print("开始计算权重...")
        weights = ssdr.compute_weights(
            V_rest,
            V_deformed,
            T_joints,
            max_iter=5,  # 减少迭代次数以加快计算
            max_influences=3
        )

        print("应用权重到模型...")
        skin_cluster = ssdr.apply_weights(mesh, joints, weights)

        if skin_cluster:
            # 测试权重效果
            cmds.currentTime(keyframes[1] if len(keyframes) > 1 else 10)

            cmds.confirmDialog(
                title="完成",
                message=f"SSDR 权重计算完成！\n\n创建的皮肤簇: {skin_cluster}\n\n现在可以检查变形效果。",
                button=["确定"]
            )
        else:
            cmds.warning("权重应用失败")

# 直接运行简单版本
def run_simple_ssdr():
    """运行简单的 SSDR 版本"""
    print("=" * 50)
    print("启动简单 SSDR 权重工具")
    print("此版本不需要安装任何额外库")
    print("=" * 50)

    SimpleSSDRUI.show_window()

# 运行工具
run_simple_ssdr()