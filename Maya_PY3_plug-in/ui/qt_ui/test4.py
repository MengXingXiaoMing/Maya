# coding=utf-8
import json
import gzip
import base64
import os
from io import BytesIO  # 用于流式处理



# 使用标准库压缩加密
def save_file(filename, readable, unreadable):
    # 可读部分：JSON文本
    json_str = json.dumps(readable, indent=2)

    # 不可读部分：GZIP压缩 + Base64编码（实现伪加密）
    compressed = gzip.compress(unreadable)
    encoded = base64.b85encode(compressed)  # 比Base64更紧凑

    # 合并存储
    with open(filename, 'wb') as f:
        f.write(json_str.encode('utf-8'))
        f.write(b'\n-----BINARY-----\n')  # 分隔符
        f.write(encoded)

# 同之前保存函数，省略重复代码...

def read_json_part(filename):
    """仅读取JSON部分，不加载二进制数据"""
    with open(filename, 'rb') as f:
        # 读取直到分隔符
        json_content = bytearray()
        while True:
            line = f.readline()
            if line.startswith(b'-----BINARY-----'):
                break
            json_content.extend(line)
        return json.loads(json_content.decode('utf-8'))


def stream_binary_part(filename, chunk_size=1024 * 1024):
    """流式分块读取二进制部分"""
    with open(filename, 'rb') as f:
        # 定位到二进制数据起始位置
        while True:
            line = f.readline()
            if line.startswith(b'-----BINARY-----'):
                break

        # 读取并解压流
        compressed = base64.b85decode(f.read())
        with gzip.GzipFile(fileobj=BytesIO(compressed), mode='rb') as gz:
            while True:
                chunk = gz.read(chunk_size)
                if not chunk:
                    break
                yield chunk


# 使用示例
if __name__ == "__main__":
    # 仅读取JSON元数据
    metadata = read_json_part('data.txt')
    print("元数据:", metadata)

    # 分块处理二进制数据
    total_size = 0
    for i, chunk in enumerate(stream_binary_part('data.txt')):
        print(f"处理第 {i + 1} 块，大小 {len(chunk)} 字节")
        total_size += len(chunk)
        # 此处可添加自定义处理逻辑

    print("二进制数据总大小:", total_size, "bytes")

import numpy as np
import math


class BallRotationCalculator:
    def __init__(self, radius=10):
        self.radius = radius

    def calculate_rotation_from_displacement(self, start_pos, end_pos, initial_rotation_matrix=None):
        """
        计算小球从起始位置到终点位置的旋转矩阵

        参数:
            start_pos: 起始位置 (x, y, z)
            end_pos: 终点位置 (x, y, z)
            initial_rotation_matrix: 初始旋转矩阵 (3x3)，默认为单位矩阵

        返回:
            最终的变换矩阵 (4x4，包含旋转和平移)
        """
        # 1. 计算位移向量和距离
        displacement = np.array(end_pos) - np.array(start_pos)
        distance = np.linalg.norm(displacement)

        print(f"位移向量: {displacement}")
        print(f"位移距离: {distance}")

        # 如果没有位移，返回初始矩阵
        if distance < 1e-10:
            print("位移太小，忽略旋转")
            return self._create_transform_matrix(np.eye(3), end_pos)

        # 2. 计算旋转角度 (弧度)
        rotation_angle = distance / self.radius
        print(f"旋转角度 (弧度): {rotation_angle}")
        print(f"旋转角度 (度数): {math.degrees(rotation_angle)}")

        # 3. 计算旋转轴 (垂直于位移方向)
        # 使用一个参考向量来计算叉积
        if np.allclose(displacement, [0, 0, 0]):
            rotation_axis = np.array([0, 0, 1])  # 默认Z轴
        else:
            # 归一化位移向量
            displacement_normalized = displacement / distance

            # 选择一个参考向量（这里使用Y轴）
            reference_vector = np.array([0, 1, 0])

            # 计算旋转轴（垂直于位移方向和参考向量）
            rotation_axis = np.cross(reference_vector, displacement_normalized)
            axis_length = np.linalg.norm(rotation_axis)

            if axis_length < 1e-10:
                # 如果叉积结果太小，使用另一个参考向量
                reference_vector = np.array([1, 0, 0])
                rotation_axis = np.cross(reference_vector, displacement_normalized)
                axis_length = np.linalg.norm(rotation_axis)

            if axis_length < 1e-10:
                # 如果还是太小，使用Z轴
                rotation_axis = np.array([0, 0, 1])
            else:
                rotation_axis = rotation_axis / axis_length  # 归一化

        print(f"旋转轴: {rotation_axis}")

        # 4. 计算旋转四元数
        rotation_quaternion = self._axis_angle_to_quaternion(rotation_axis, rotation_angle)
        print(f"旋转四元数 (x, y, z, w): {rotation_quaternion}")

        # 5. 将四元数转换为旋转矩阵
        rotation_matrix = self._quaternion_to_matrix(rotation_quaternion)
        print("旋转矩阵:")
        print(rotation_matrix)

        # 6. 组合初始旋转（如果提供）
        if initial_rotation_matrix is None:
            initial_rotation_matrix = np.eye(3)

        # 将旋转矩阵与初始旋转矩阵相乘
        final_rotation_matrix = np.dot(rotation_matrix, initial_rotation_matrix)
        print("最终旋转矩阵:")
        print(final_rotation_matrix)

        # 7. 创建完整的变换矩阵（包含平移）
        final_transform_matrix = self._create_transform_matrix(final_rotation_matrix, end_pos)
        print("最终变换矩阵 (4x4):")
        print(final_transform_matrix)

        return final_transform_matrix

    def _axis_angle_to_quaternion(self, axis, angle):
        """将轴角表示转换为四元数"""
        half_angle = angle / 2.0
        sin_half = math.sin(half_angle)

        x = axis[0] * sin_half
        y = axis[1] * sin_half
        z = axis[2] * sin_half
        w = math.cos(half_angle)

        return np.array([x, y, z, w])

    def _quaternion_to_matrix(self, q):
        """将四元数转换为旋转矩阵"""
        x, y, z, w = q

        # 计算旋转矩阵的元素
        xx = x * x
        yy = y * y
        zz = z * z
        xy = x * y
        xz = x * z
        yz = y * z
        wx = w * x
        wy = w * y
        wz = w * z

        matrix = np.array([
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
        ])

        return matrix

    def _create_transform_matrix(self, rotation_matrix, translation):
        """创建4x4变换矩阵"""
        transform_matrix = np.eye(4)
        transform_matrix[0:3, 0:3] = rotation_matrix
        transform_matrix[0:3, 3] = translation
        return transform_matrix


# 使用示例
if __name__ == "__main__":
    # 创建计算器实例，小球半径为10
    calculator = BallRotationCalculator(radius=10)

    # 定义起始点和终点
    start_position = [0, 0, 0]
    end_position = [15, 8, 5]  # 示例终点

    # 可选的初始旋转矩阵（单位矩阵表示无初始旋转）
    initial_rot = np.eye(3)

    # 计算旋转效果
    print("=== 小球旋转计算开始 ===")
    final_matrix = calculator.calculate_rotation_from_displacement(
        start_position, end_position, initial_rot
    )
    print("=== 计算完成 ===")

    # 验证：可以计算反向变换或应用变换到其他点
    print("\n应用示例:")
    test_point = [1, 0, 0]  # 测试点
    rotated_point = np.dot(final_matrix[0:3, 0:3], test_point) + final_matrix[0:3, 3]
    print(f"点 {test_point} 经过变换后位置: {rotated_point}")

import math
import maya.cmds as cmds


class BallRollCalculator:
    def __init__(self, radius=10):
        self.radius = radius

    def calculate_roll_rotation(self, start_pos, end_pos):
        """
        计算小球从起始位置滚动到终点位置的旋转效果

        参数:
            start_pos: 起始位置 (x, y, z)
            end_pos: 终点位置 (x, y, z)

        返回:
            包含位移、旋转轴、旋转角度和变换矩阵的字典
        """
        # 1. 计算位移向量和距离
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        dz = end_pos[2] - start_pos[2]

        displacement = [dx, dy, dz]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        print(f"位移向量: ({dx}, {dy}, {dz})")
        print(f"位移距离: {distance}")

        # 如果没有位移，返回单位矩阵
        if distance < 1e-10:
            print("位移太小，忽略旋转")
            return self._identity_matrix()

        # 2. 计算旋转角度 (弧度)
        # 滚动角度 = 移动距离 / 球体半径
        rotation_angle = distance / self.radius
        print(f"旋转角度 (弧度): {rotation_angle}")
        print(f"旋转角度 (度数): {math.degrees(rotation_angle)}")

        # 3. 计算旋转轴 (垂直于位移方向)
        # 使用Y轴作为参考向量来计算叉积
        ref_vector = [0, 1, 0]  # Y轴

        # 计算叉积: ref_vector × displacement
        cross_x = ref_vector[1] * dz - ref_vector[2] * dy
        cross_y = ref_vector[2] * dx - ref_vector[0] * dz
        cross_z = ref_vector[0] * dy - ref_vector[1] * dx

        rotation_axis = [cross_x, cross_y, cross_z]
        axis_length = math.sqrt(cross_x * cross_x + cross_y * cross_y + cross_z * cross_z)

        # 如果叉积结果太小，尝试使用X轴作为参考向量
        if axis_length < 1e-10:
            ref_vector = [1, 0, 0]  # X轴
            cross_x = ref_vector[1] * dz - ref_vector[2] * dy
            cross_y = ref_vector[2] * dx - ref_vector[0] * dz
            cross_z = ref_vector[0] * dy - ref_vector[1] * dx

            rotation_axis = [cross_x, cross_y, cross_z]
            axis_length = math.sqrt(cross_x * cross_x + cross_y * cross_y + cross_z * cross_z)

        # 归一化旋转轴
        if axis_length > 1e-10:
            rotation_axis = [cross_x / axis_length, cross_y / axis_length, cross_z / axis_length]
        else:
            # 如果还是太小，使用Z轴
            rotation_axis = [0, 0, 1]

        print(f"旋转轴: ({rotation_axis[0]}, {rotation_axis[1]}, {rotation_axis[2]})")

        # 4. 计算旋转四元数
        rotation_quaternion = self._axis_angle_to_quaternion(rotation_axis, rotation_angle)
        print(f"旋转四元数 (x, y, z, w): {rotation_quaternion}")

        # 5. 将四元数转换为旋转矩阵
        rotation_matrix = self._quaternion_to_matrix(rotation_quaternion)
        print("旋转矩阵:")
        self._print_matrix(rotation_matrix)

        # 6. 创建初始旋转矩阵（单位矩阵）
        initial_matrix = self._identity_matrix()

        # 7. 将旋转矩阵与初始矩阵相乘（这里初始矩阵是单位矩阵，所以结果不变）
        final_rotation_matrix = self._matrix_multiply(rotation_matrix, initial_matrix)
        print("最终旋转矩阵:")
        self._print_matrix(final_rotation_matrix)

        # 8. 创建完整的变换矩阵（包含平移）
        final_transform_matrix = self._create_transform_matrix(final_rotation_matrix, end_pos)
        print("最终变换矩阵 (4x4):")
        self._print_matrix(final_transform_matrix)

        return {
            'displacement': displacement,
            'distance': distance,
            'rotation_axis': rotation_axis,
            'rotation_angle': rotation_angle,
            'quaternion': rotation_quaternion,
            'rotation_matrix': rotation_matrix,
            'transform_matrix': final_transform_matrix
        }

    def _axis_angle_to_quaternion(self, axis, angle):
        """将轴角表示转换为四元数[6,7](@ref)"""
        half_angle = angle / 2.0
        sin_half = math.sin(half_angle)

        x = axis[0] * sin_half
        y = axis[1] * sin_half
        z = axis[2] * sin_half
        w = math.cos(half_angle)

        return [x, y, z, w]

    def _quaternion_to_matrix(self, q):
        """将四元数转换为旋转矩阵[6,7](@ref)"""
        x, y, z, w = q

        # 计算旋转矩阵的元素[6](@ref)
        xx = x * x
        yy = y * y
        zz = z * z
        xy = x * y
        xz = x * z
        yz = y * z
        wx = w * x
        wy = w * y
        wz = w * z

        # 构建3x3旋转矩阵[6,7](@ref)
        matrix = [
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
        ]

        return matrix

    def _matrix_multiply(self, a, b):
        """3x3矩阵乘法"""
        result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += a[i][k] * b[k][j]

        return result

    def _identity_matrix(self):
        """返回3x3单位矩阵"""
        return [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

    def _create_transform_matrix(self, rotation_matrix, translation):
        """创建4x4变换矩阵"""
        transform_matrix = [
            [rotation_matrix[0][0], rotation_matrix[0][1], rotation_matrix[0][2], translation[0]],
            [rotation_matrix[1][0], rotation_matrix[1][1], rotation_matrix[1][2], translation[1]],
            [rotation_matrix[2][0], rotation_matrix[2][1], rotation_matrix[2][2], translation[2]],
            [0, 0, 0, 1]
        ]
        return transform_matrix

    def _print_matrix(self, matrix):
        """打印矩阵"""
        for row in matrix:
            print([f"{val:.6f}" for val in row])

    def apply_to_maya_ball(self, ball_name, start_pos, end_pos):
        """
        将计算出的变换应用到Maya中的小球

        参数:
            ball_name: 小球在Maya中的名称
            start_pos: 起始位置
            end_pos: 终点位置
        """
        try:
            # 检查小球是否存在
            if not cmds.objExists(ball_name):
                print(f"错误: 对象 {ball_name} 不存在")
                return False

            # 计算旋转效果
            result = self.calculate_roll_rotation(start_pos, end_pos)

            # 在Maya中应用变换[1,4](@ref)
            # 设置位置
            cmds.xform(ball_name, translation=end_pos, worldSpace=True)

            # 从旋转矩阵提取欧拉角（简化处理）
            # 注意：这只是一个近似，实际应用中可能需要更复杂的转换
            rotation = self._matrix_to_euler(result['rotation_matrix'])
            cmds.xform(ball_name, rotation=rotation, worldSpace=True)

            print(f"已将变换应用到 {ball_name}")
            return True

        except Exception as e:
            print(f"应用变换时出错: {e}")
            return False

    def _matrix_to_euler(self, matrix):
        """
        将旋转矩阵转换为欧拉角（简化版本）
        注意：这是一个简化实现，实际应用中可能需要更健壮的转换
        """
        # 提取旋转矩阵的元素
        m00, m01, m02 = matrix[0]
        m10, m11, m12 = matrix[1]
        m20, m21, m22 = matrix[2]

        # 计算Y旋转（绕Y轴）
        sy = math.sqrt(m00 * m00 + m10 * m10)

        if sy > 1e-6:  # 非奇异情况
            x = math.atan2(m21, m22)
            y = math.atan2(-m20, sy)
            z = math.atan2(m10, m00)
        else:  # 奇异情况
            x = math.atan2(-m12, m11)
            y = math.atan2(-m20, sy)
            z = 0

        # 转换为度数
        x_deg = math.degrees(x)
        y_deg = math.degrees(y)
        z_deg = math.degrees(z)

        return [x_deg, y_deg, z_deg]


# 使用示例
if __name__ == "__main__":
    # 创建计算器实例，小球半径为10
    calculator = BallRollCalculator(radius=10)

    # 定义起始点和终点
    start_position = [0, 0, 0]
    end_position = [1, 2, 3]

    # 计算旋转效果
    print("=== 小球旋转计算开始 ===")
    result = calculator.calculate_roll_rotation(start_position, end_position)
    print("=== 计算完成 ===")

    # 如果在Maya中，可以应用到一个实际的小球
    print("\nMaya应用示例:")
    # 取消注释以下代码来在Maya中实际应用
    # calculator.apply_to_maya_ball("pSphere1", start_position, end_position)

import maya.cmds as cmds
import math


class BallPositionPrinter:
    def __init__(self, ball_name, radius=10):
        self.ball_name = ball_name
        self.radius = radius
        self.initial_position = [0, 0, 0]  # 初始XYZ为0

    def print_final_position(self):
        """打印小球的最终位置"""
        try:
            # 获取小球当前的世界空间位置[6,7](@ref)
            if cmds.objExists(self.ball_name):
                # 方法1: 使用xform命令获取位置[7](@ref)
                position = cmds.xform(self.ball_name, query=True, translation=True, worldSpace=True)

                # 方法2: 也可以使用getAttr获取单个坐标值[7](@ref)
                # x_pos = cmds.getAttr(f"{self.ball_name}.translateX")
                # y_pos = cmds.getAttr(f"{self.ball_name}.translateY")
                # z_pos = cmds.getAttr(f"{self.ball_name}.translateZ")
                # position = [x_pos, y_pos, z_pos]

                print("=== 小球位置信息 ===")
                print(f"初始位置: X={self.initial_position[0]}, Y={self.initial_position[1]}, Z={self.initial_position[2]}")
                print(f"最终位置: X={position[0]:.6f}, Y={position[1]:.6f}, Z={position[2]:.6f}")

                # 计算位移量
                displacement = [
                    position[0] - self.initial_position[0],
                    position[1] - self.initial_position[1],
                    position[2] - self.initial_position[2]
                ]

                print(f"位移量: ΔX={displacement[0]:.6f}, ΔY={displacement[1]:.6f}, ΔZ={displacement[2]:.6f}")

                return position
            else:
                print(f"错误: 对象 {self.ball_name} 不存在")
                return None

        except Exception as e:
            print(f"获取位置时出错: {e}")
            return None

    def print_formatted_position(self):
        """使用格式化字符串打印位置信息[1,2,3](@ref)"""
        position = self.print_final_position()
        if position:
            # 使用f-string格式化输出[1,3](@ref)
            print("\n=== 格式化输出 ===")
            print(f"最终坐标: ({position[0]:.3f}, {position[1]:.3f}, {position[2]:.3f})")

            # 使用旧式格式化[2](@ref)
            print("坐标分解: X=%.4f, Y=%.4f, Z=%.4f" % (position[0], position[1], position[2]))

            # 使用str.format()方法[3](@ref)
            print("位置信息: X={0[0]:.2f}, Y={0[1]:.2f}, Z={0[2]:.2f}".format(position))


# 使用示例
if __name__ == "__main__":
    # 假设你的小球名称是 "ball" 或 "pSphere1"
    ball_name = "pSphere1"  # 请替换为你的小球实际名称

    # 创建打印机实例
    printer = BallPositionPrinter(ball_name)

    # 打印最终位置
    printer.print_final_position()

    # 打印格式化位置
    printer.print_formatted_position()

import math


class BallRotationCalculator:
    def __init__(self, radius=1):
        self.radius = radius

    def calculate_rotation(self, start_pos, end_pos, initial_rotation_matrix=None):
        """
        计算小球从起始位置滚动到终点位置的旋转效果

        参数:
            start_pos: 起始位置 [x, y, z]
            end_pos: 终点位置 [x, y, z]
            initial_rotation_matrix: 初始旋转矩阵 (3x3)，默认为单位矩阵

        返回:
            包含所有计算结果的字典
        """
        print("=" * 60)
        print("小球旋转计算开始")
        print("=" * 60)

        # 1. 计算位移向量和距离
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        dz = end_pos[2] - start_pos[2]

        displacement = [dx, dy, dz]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        print(f"1. 位移计算:")
        print(f"   起始位置: ({start_pos[0]}, {start_pos[1]}, {start_pos[2]})")
        print(f"   目标位置: ({end_pos[0]}, {end_pos[1]}, {end_pos[2]})")
        print(f"   位移向量: ({dx:.6f}, {dy:.6f}, {dz:.6f})")
        print(f"   位移距离: {distance:.6f}")

        # 如果没有位移，返回单位矩阵
        if distance < 1e-10:
            print("警告: 位移太小，忽略旋转")
            identity_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            return {
                'displacement': displacement,
                'distance': distance,
                'rotation_angle': 0,
                'rotation_axis': [0, 0, 1],
                'quaternion': [0, 0, 0, 1],
                'rotation_matrix': identity_matrix,
                'final_matrix': self._create_transform_matrix(identity_matrix, end_pos),
                'euler_angles': [0, 0, 0]
            }

        # 2. 计算旋转角度 (弧度)
        rotation_angle = distance / self.radius
        print(f"\n2. 旋转角度计算:")
        print(f"   球体半径: {self.radius}")
        print(f"   旋转角度: {rotation_angle:.6f} 弧度")
        print(f"   旋转角度: {math.degrees(rotation_angle):.6f} 度")

        # 3. 计算旋转轴 (垂直于位移方向)
        # 归一化位移向量
        displacement_normalized = [dx / distance, dy / distance, dz / distance]

        # 使用Z轴作为参考向量来计算叉积 (假设初始向上方向为Z轴)
        ref_vector = [0, 0, 1]

        # 计算叉积: ref_vector × displacement_normalized
        cross_x = ref_vector[1] * displacement_normalized[2] - ref_vector[2] * displacement_normalized[1]
        cross_y = ref_vector[2] * displacement_normalized[0] - ref_vector[0] * displacement_normalized[2]
        cross_z = ref_vector[0] * displacement_normalized[1] - ref_vector[1] * displacement_normalized[0]

        axis_length = math.sqrt(cross_x * cross_x + cross_y * cross_y + cross_z * cross_z)

        if axis_length < 1e-10:
            # 如果叉积结果太小，使用Y轴作为参考向量
            ref_vector = [0, 1, 0]
            cross_x = ref_vector[1] * displacement_normalized[2] - ref_vector[2] * displacement_normalized[1]
            cross_y = ref_vector[2] * displacement_normalized[0] - ref_vector[0] * displacement_normalized[2]
            cross_z = ref_vector[0] * displacement_normalized[1] - ref_vector[1] * displacement_normalized[0]
            axis_length = math.sqrt(cross_x * cross_x + cross_y * cross_y + cross_z * cross_z)

        if axis_length < 1e-10:
            # 如果还是太小，使用X轴作为旋转轴
            rotation_axis = [1, 0, 0]
        else:
            # 归一化旋转轴
            rotation_axis = [cross_x / axis_length, cross_y / axis_length, cross_z / axis_length]

        print(f"\n3. 旋转轴计算:")
        print(f"   参考向量 (Z轴): ({ref_vector[0]}, {ref_vector[1]}, {ref_vector[2]})")
        print(f"   旋转轴: ({rotation_axis[0]:.6f}, {rotation_axis[1]:.6f}, {rotation_axis[2]:.6f})")

        # 4. 计算旋转四元数
        half_angle = rotation_angle / 2.0
        sin_half = math.sin(half_angle)
        cos_half = math.cos(half_angle)

        quaternion = [
            rotation_axis[0] * sin_half,  # x
            rotation_axis[1] * sin_half,  # y
            rotation_axis[2] * sin_half,  # z
            cos_half  # w
        ]

        print(f"\n4. 四元数计算:")
        print(f"   四元数 (x, y, z, w): ")
        print(f"   ({quaternion[0]:.6f}, {quaternion[1]:.6f}, {quaternion[2]:.6f}, {quaternion[3]:.6f})")

        # 5. 将四元数转换为旋转矩阵
        rotation_matrix = self._quaternion_to_matrix(quaternion)
        print(f"\n5. 旋转矩阵计算:")
        print(f"   旋转矩阵:")
        for i, row in enumerate(rotation_matrix):
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}]")

        # 6. 组合初始旋转（如果提供）
        if initial_rotation_matrix is None:
            initial_rotation_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        # 将旋转矩阵与初始旋转矩阵相乘
        final_rotation_matrix = self._matrix_multiply(rotation_matrix, initial_rotation_matrix)
        print(f"\n6. 最终旋转矩阵计算:")
        print(f"   最终旋转矩阵:")
        for i, row in enumerate(final_rotation_matrix):
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}]")

        # 7. 创建完整的变换矩阵（包含平移）
        final_transform_matrix = self._create_transform_matrix(final_rotation_matrix, end_pos)
        print(f"\n7. 完整变换矩阵:")
        print(f"   4x4变换矩阵:")
        for i, row in enumerate(final_transform_matrix):
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}, {row[3]:.6f}]")

        # 8. 计算欧拉角（实际旋转数值）
        euler_angles = self._rotation_matrix_to_euler(final_rotation_matrix)
        print(f"\n8. 实际旋转数值 (欧拉角):")
        print(f"   X轴旋转: {math.degrees(euler_angles[0]):.6f} 度")
        print(f"   Y轴旋转: {math.degrees(euler_angles[1]):.6f} 度")
        print(f"   Z轴旋转: {math.degrees(euler_angles[2]):.6f} 度")
        print(f"   弧度值: ({euler_angles[0]:.6f}, {euler_angles[1]:.6f}, {euler_angles[2]:.6f})")

        print("\n" + "=" * 60)
        print("计算完成!")
        print("=" * 60)

        return {
            'displacement': displacement,
            'distance': distance,
            'rotation_angle': rotation_angle,
            'rotation_axis': rotation_axis,
            'quaternion': quaternion,
            'rotation_matrix': rotation_matrix,
            'final_rotation_matrix': final_rotation_matrix,
            'transform_matrix': final_transform_matrix,
            'euler_angles': euler_angles,
            'euler_angles_degrees': [math.degrees(euler_angles[0]),
                                     math.degrees(euler_angles[1]),
                                     math.degrees(euler_angles[2])]
        }

    def _quaternion_to_matrix(self, q):
        """将四元数转换为旋转矩阵[6,7](@ref)"""
        x, y, z, w = q

        # 计算旋转矩阵的元素
        xx = x * x
        yy = y * y
        zz = z * z
        xy = x * y
        xz = x * z
        yz = y * z
        wx = w * x
        wy = w * y
        wz = w * z

        matrix = [
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
        ]

        return matrix

    def _matrix_multiply(self, a, b):
        """3x3矩阵乘法"""
        result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += a[i][k] * b[k][j]

        return result

    def _create_transform_matrix(self, rotation_matrix, translation):
        """创建4x4变换矩阵（包含旋转和平移）"""
        transform_matrix = [
            [rotation_matrix[0][0], rotation_matrix[0][1], rotation_matrix[0][2], translation[0]],
            [rotation_matrix[1][0], rotation_matrix[1][1], rotation_matrix[1][2], translation[1]],
            [rotation_matrix[2][0], rotation_matrix[2][1], rotation_matrix[2][2], translation[2]],
            [0, 0, 0, 1]
        ]
        return transform_matrix

    def _rotation_matrix_to_euler(self, R):
        """将旋转矩阵转换为欧拉角（XYZ顺序）[6,8](@ref)"""
        # 检查矩阵是否为旋转矩阵
        sy = math.sqrt(R[0][0] * R[0][0] + R[1][0] * R[1][0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(R[2][1], R[2][2])
            y = math.atan2(-R[2][0], sy)
            z = math.atan2(R[1][0], R[0][0])
        else:
            x = math.atan2(-R[1][2], R[1][1])
            y = math.atan2(-R[2][0], sy)
            z = 0

        return [x, y, z]


# 使用示例
if __name__ == "__main__":
    # 创建计算器实例，小球半径为10
    calculator = BallRotationCalculator(radius=1)

    # 定义起始点和终点
    start_position = [0, 0, 0]
    end_position = [1, 0, 0]

    # 可选的初始旋转矩阵（这里使用绕Z轴旋转30度的矩阵作为示例）
    import math

    angle_rad = math.radians(30)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)

    initial_rotation = [
        [cos_angle, -sin_angle, 0],
        [sin_angle, cos_angle, 0],
        [0, 0, 1]
    ]

    # 计算旋转效果
    result = calculator.calculate_rotation(start_position, end_position, initial_rotation)

    # 单独打印最终的旋转数值
    print("\n" + "=" * 60)
    print("最终旋转数值总结")
    print("=" * 60)
    print(f"欧拉角 (度): X={math.degrees(result['euler_angles'][0]):.2f}, " +
          f"Y={math.degrees(result['euler_angles'][1]):.2f}, " +
          f"Z={math.degrees(result['euler_angles'][2]):.2f}")
    print(f"欧拉角 (弧度): X={result['euler_angles'][0]:.6f}, " +
          f"Y={result['euler_angles'][1]:.6f}, " +
          f"Z={result['euler_angles'][2]:.6f}")

import math


class CorrectedBallRotation:
    def __init__(self, radius=1):
        self.radius = radius

    def calculate_rotation(self, start_pos, end_pos, initial_rotation=None):
        """
        修正后的小球旋转计算
        """
        print("=" * 60)
        print("修正版小球旋转计算")
        print("=" * 60)

        # 1. 计算位移和距离
        dx, dy, dz = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1], end_pos[2] - start_pos[2]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        print(f"位移向量: ({dx:.6f}, {dy:.6f}, {dz:.6f})")
        print(f"位移距离: {distance:.6f}")

        if distance < 1e-10:
            return self._identity_matrix()

        # 2. 计算旋转角度
        rotation_angle = distance / self.radius
        print(f"旋转角度: {rotation_angle:.6f} 弧度, {math.degrees(rotation_angle):.6f} 度")

        # 3. 计算旋转轴（修正版）
        # 对于纯X轴移动，旋转轴应该是Z轴或Y轴，而不是三个轴都有
        if abs(dx) > 1e-10 and abs(dy) < 1e-10 and abs(dz) < 1e-10:
            # 纯X轴移动：绕Y轴旋转（右手法则）
            rotation_axis = [0, 1, 0]  # Y轴
        elif abs(dy) > 1e-10 and abs(dx) < 1e-10 and abs(dz) < 1e-10:
            # 纯Y轴移动：绕X轴旋转
            rotation_axis = [1, 0, 0]  # X轴
        elif abs(dz) > 1e-10 and abs(dx) < 1e-10 and abs(dy) < 1e-10:
            # 纯Z轴移动：绕X轴或Y轴旋转
            rotation_axis = [0, 0, 1]  # Z轴
        else:
            # 复合移动：使用叉积计算旋转轴
            displacement_norm = [dx / distance, dy / distance, dz / distance]
            up_vector = [0, 0, 1]  # 假设Z轴向上
            rotation_axis = self._cross_product(up_vector, displacement_norm)
            axis_length = math.sqrt(rotation_axis[0] ** 2 + rotation_axis[1] ** 2 + rotation_axis[2] ** 2)
            if axis_length > 1e-10:
                rotation_axis = [rotation_axis[0] / axis_length, rotation_axis[1] / axis_length,
                                 rotation_axis[2] / axis_length]
            else:
                rotation_axis = [0, 0, 1]  # 默认Z轴

        print(f"旋转轴: ({rotation_axis[0]:.6f}, {rotation_axis[1]:.6f}, {rotation_axis[2]:.6f})")

        # 4. 计算四元数
        quaternion = self._axis_angle_to_quaternion(rotation_axis, rotation_angle)
        print(f"四元数 (x, y, z, w): ({quaternion[0]:.6f}, {quaternion[1]:.6f}, {quaternion[2]:.6f}, {quaternion[3]:.6f})")

        # 5. 四元数转旋转矩阵
        rotation_matrix = self._quaternion_to_matrix(quaternion)
        print("旋转矩阵:")
        for row in rotation_matrix:
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}]")

        # 6. 处理初始旋转（修正：确保初始矩阵为单位矩阵如果未提供）
        if initial_rotation is None:
            initial_rotation = self._identity_matrix()

        final_rotation_matrix = self._matrix_multiply(rotation_matrix, initial_rotation)
        print("最终旋转矩阵:")
        for row in final_rotation_matrix:
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}]")

        # 7. 正确的欧拉角转换（使用标准ZYX顺序）[8](@ref)
        euler_angles = self._corrected_matrix_to_euler(final_rotation_matrix)
        print("实际旋转数值 (欧拉角-ZYX顺序):")
        print(f"   X轴旋转 (Roll):  {math.degrees(euler_angles[0]):.6f} 度")
        print(f"   Y轴旋转 (Pitch): {math.degrees(euler_angles[1]):.6f} 度")
        print(f"   Z轴旋转 (Yaw):   {math.degrees(euler_angles[2]):.6f} 度")
        print(f"   弧度值: ({euler_angles[0]:.6f}, {euler_angles[1]:.6f}, {euler_angles[2]:.6f})")

        return {
            'rotation_axis': rotation_axis,
            'quaternion': quaternion,
            'rotation_matrix': rotation_matrix,
            'final_rotation_matrix': final_rotation_matrix,
            'euler_angles': euler_angles
        }

    def _corrected_matrix_to_euler(self, matrix):
        """修正的旋转矩阵到欧拉角转换（ZYX顺序）[8](@ref)"""
        # 提取矩阵元素
        m00, m01, m02 = matrix[0]
        m10, m11, m12 = matrix[1]
        m20, m21, m22 = matrix[2]

        # 标准ZYX顺序转换公式[8](@ref)
        # 俯仰角 (pitch - Y轴)
        sinp = 2 * (m20)  # 简化处理
        if abs(sinp) >= 1:
            # 万向节死锁处理[8](@ref)
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        # 偏航角 (yaw - Z轴) 和滚转角 (roll - X轴)
        if abs(sinp) > 0.9999:
            # 万向节死锁情况
            roll = math.atan2(-m01, m11)
            yaw = 0.0
        else:
            roll = math.atan2(m21, m22)
            yaw = math.atan2(m10, m00)

        return [roll, pitch, yaw]  # [X, Y, Z] 对应 [Roll, Pitch, Yaw]

    def _axis_angle_to_quaternion(self, axis, angle):
        """轴角转四元数"""
        half_angle = angle / 2.0
        sin_half = math.sin(half_angle)
        return [
            axis[0] * sin_half,
            axis[1] * sin_half,
            axis[2] * sin_half,
            math.cos(half_angle)
        ]

    def _quaternion_to_matrix(self, q):
        """四元数转旋转矩阵"""
        x, y, z, w = q
        xx, yy, zz = x * x, y * y, z * z
        xy, xz, yz = x * y, x * z, y * z
        wx, wy, wz = w * x, w * y, w * z

        return [
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
        ]

    def _matrix_multiply(self, a, b):
        """3x3矩阵乘法"""
        result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    def _identity_matrix(self):
        """单位矩阵"""
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def _cross_product(self, a, b):
        """叉积计算"""
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        ]


# 测试修正后的算法
if __name__ == "__main__":
    calculator = CorrectedBallRotation(radius=1)

    print("\n测试1: 纯X轴移动 (应该主要显示Y轴旋转)")
    result1 = calculator.calculate_rotation([0, 0, 0], [1, 0, 0])

    print("\n测试2: 纯Y轴移动 (应该主要显示X轴旋转)")
    result2 = calculator.calculate_rotation([0, 0, 0], [0, 1, 0])

    print("\n测试3: 对角线移动")
    result3 = calculator.calculate_rotation([0, 0, 0], [1, 1, 0])

import math


class CorrectedBallRotation:
    def __init__(self, radius=1):
        self.radius = radius

    def calculate_rotation(self, start_pos, end_pos, initial_rotation=None):
        """
        修正后的小球旋转计算 - XYZ旋转顺序
        """
        print("=" * 60)
        print("修正版小球旋转计算 (XYZ旋转顺序)")
        print("=" * 60)

        # 1. 计算位移和距离
        dx, dy, dz = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1], end_pos[2] - start_pos[2]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        print(f"位移向量: ({dx:.6f}, {dy:.6f}, {dz:.6f})")
        print(f"位移距离: {distance:.6f}")

        if distance < 1e-10:
            return self._identity_matrix()

        # 2. 计算旋转角度
        rotation_angle = distance / self.radius
        print(f"旋转角度: {rotation_angle:.6f} 弧度, {math.degrees(rotation_angle):.6f} 度")

        # 3. 计算旋转轴（修正版）
        # 对于纯X轴移动，旋转轴应该是Z轴或Y轴，而不是三个轴都有
        if abs(dx) > 1e-10 and abs(dy) < 1e-10 and abs(dz) < 1e-10:
            # 纯X轴移动：绕Y轴旋转（右手法则）
            rotation_axis = [0, 1, 0]  # Y轴
        elif abs(dy) > 1e-10 and abs(dx) < 1e-10 and abs(dz) < 1e-10:
            # 纯Y轴移动：绕X轴旋转
            rotation_axis = [1, 0, 0]  # X轴
        elif abs(dz) > 1e-10 and abs(dx) < 1e-10 and abs(dy) < 1e-10:
            # 纯Z轴移动：绕X轴或Y轴旋转
            rotation_axis = [0, 0, 1]  # Z轴
        else:
            # 复合移动：使用叉积计算旋转轴
            displacement_norm = [dx / distance, dy / distance, dz / distance]
            up_vector = [0, 0, 1]  # 假设Z轴向上
            rotation_axis = self._cross_product(up_vector, displacement_norm)
            axis_length = math.sqrt(rotation_axis[0] ** 2 + rotation_axis[1] ** 2 + rotation_axis[2] ** 2)
            if axis_length > 1e-10:
                rotation_axis = [rotation_axis[0] / axis_length, rotation_axis[1] / axis_length,
                                 rotation_axis[2] / axis_length]
            else:
                rotation_axis = [0, 0, 1]  # 默认Z轴

        print(f"旋转轴: ({rotation_axis[0]:.6f}, {rotation_axis[1]:.6f}, {rotation_axis[2]:.6f})")

        # 4. 计算四元数
        quaternion = self._axis_angle_to_quaternion(rotation_axis, rotation_angle)
        print(f"四元数 (x, y, z, w): ({quaternion[0]:.6f}, {quaternion[1]:.6f}, {quaternion[2]:.6f}, {quaternion[3]:.6f})")

        # 5. 四元数转旋转矩阵
        rotation_matrix = self._quaternion_to_matrix(quaternion)
        print("旋转矩阵:")
        for row in rotation_matrix:
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}]")

        # 6. 处理初始旋转（修正：确保初始矩阵为单位矩阵如果未提供）
        if initial_rotation is None:
            initial_rotation = self._identity_matrix()

        final_rotation_matrix = self._matrix_multiply(rotation_matrix, initial_rotation)
        print("最终旋转矩阵:")
        for row in final_rotation_matrix:
            print(f"   [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}]")

        # 7. 正确的欧拉角转换（使用XYZ顺序）[2,6](@ref)
        euler_angles = self._corrected_matrix_to_euler_xyz(final_rotation_matrix)
        print("实际旋转数值 (欧拉角-XYZ顺序):")
        print(f"   X轴旋转: {math.degrees(euler_angles[0]):.6f} 度")
        print(f"   Y轴旋转: {math.degrees(euler_angles[1]):.6f} 度")
        print(f"   Z轴旋转: {math.degrees(euler_angles[2]):.6f} 度")
        print(f"   弧度值: ({euler_angles[0]:.6f}, {euler_angles[1]:.6f}, {euler_angles[2]:.6f})")

        return {
            'rotation_axis': rotation_axis,
            'quaternion': quaternion,
            'rotation_matrix': rotation_matrix,
            'final_rotation_matrix': final_rotation_matrix,
            'euler_angles': euler_angles
        }

    def _corrected_matrix_to_euler_xyz(self, matrix):
        """修正的旋转矩阵到欧拉角转换（XYZ顺序）[2,6](@ref)"""
        # 提取矩阵元素
        m00, m01, m02 = matrix[0]
        m10, m11, m12 = matrix[1]
        m20, m21, m22 = matrix[2]

        # XYZ顺序转换公式：先绕X轴，再绕Y轴，最后绕Z轴[2](@ref)
        # 计算Y轴旋转（pitch）
        sin_y = -m20  # 根据XYZ顺序的公式

        # 处理万向节锁情况[2](@ref)
        if abs(sin_y) >= 0.9999:
            # Y轴接近±90度，万向节锁发生
            y_angle = math.copysign(math.pi / 2, sin_y)
            x_angle = 0.0
            z_angle = math.atan2(-m01, m11) if sin_y < 0 else math.atan2(m01, -m11)
        else:
            # 正常情况
            y_angle = math.asin(sin_y)
            x_angle = math.atan2(m21, m22)
            z_angle = math.atan2(m10, m00)

        return [x_angle, y_angle, z_angle]  # [X, Y, Z] 旋转角度

    def _axis_angle_to_quaternion(self, axis, angle):
        """轴角转四元数"""
        half_angle = angle / 2.0
        sin_half = math.sin(half_angle)
        return [
            axis[0] * sin_half,
            axis[1] * sin_half,
            axis[2] * sin_half,
            math.cos(half_angle)
        ]

    def _quaternion_to_matrix(self, q):
        """四元数转旋转矩阵"""
        x, y, z, w = q
        xx, yy, zz = x * x, y * y, z * z
        xy, xz, yz = x * y, x * z, y * z
        wx, wy, wz = w * x, w * y, w * z

        return [
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]
        ]

    def _matrix_multiply(self, a, b):
        """3x3矩阵乘法"""
        result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    def _identity_matrix(self):
        """单位矩阵"""
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def _cross_product(self, a, b):
        """叉积计算"""
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        ]


# 测试修正后的算法
if __name__ == "__main__":
    calculator = CorrectedBallRotation(radius=1)

    print("\n测试1: 纯X轴移动 (XYZ顺序)")
    result1 = calculator.calculate_rotation([0, 0, 0], [1, 1, 1])

    print("\n测试2: 纯Y轴移动 (XYZ顺序)")
    result2 = calculator.calculate_rotation([0, 0, 0], [0, 1, 0])

    print("\n测试3: 对角线移动 (XYZ顺序)")
    result3 = calculator.calculate_rotation([0, 0, 0], [0, 1, 1])



import maya.cmds as cmds

def get_selected_vertex_normals():
    """
    获取当前选中顶点的法线数值。
    返回一个字典，键为顶点名称，值为法线向量（X, Y, Z）的列表。
    """
    selection = cmds.ls(selection=True, flatten=True)
    if not selection:
        cmds.warning("没有选择任何对象或组件。")
        return None

    vertex_normals = {}

    for item in selection:
        # 检查选中的是否是顶点组件（一个粗略的检查）
        if ".vtx[" in item:
            normal = cmds.polyNormalPerVertex(item, query=True, xyz=True)
            print(normal)
            if normal:
                vertex_normals[item] = normal
            else:
                cmds.warning("无法获取顶点 %s 的法线。" % item)
        else:
            # 如果选择的是整个物体，可以尝试获取其所有顶点的法线
            # 或者忽略非顶点选择。这里我们忽略。
            cmds.warning("选项 %s 似乎不是顶点组件，已跳过。" % item)

    return vertex_normals

# 使用函数
normals_dict = get_selected_vertex_normals()
if normals_dict:
    for vertex, normal in normals_dict.items():
        print("顶点: %s, 法线: X=%.4f, Y=%.4f, Z=%.4f" % (vertex, normal[0], normal[1], normal[2]))