# coding=gbk

import maya.cmds as cmds
import numpy as np


class SmoothWeightCalculator(MayaWeightCalculator):
    """支持平滑权重过渡的改进版本"""

    def __init__(self):
        super(SmoothWeightCalculator, self).__init__()
        # 用于存储上一帧的状态
        self.previous_indices = None
        self.previous_weights = None
        self.transition_progress = 0.0  # 过渡进度 (0-1)
        self.is_in_transition = False
        self.transition_duration = 10  # 过渡持续时间(帧数)
        self.current_frame = 0

    def calculate_smooth_weights(self, top_k=3, power=2, transition_speed=0.1):
        """
        计算平滑过渡的权重

        参数:
            top_k: 保留的最近点数量
            power: 距离幂次
            transition_speed: 过渡速度 (0-1)
        """
        if self.active_point is None or not self.fixed_points:
            cmds.warning("请先设置活动点和固定点")
            return None, None

        # 计算当前帧的基础权重
        current_weights, current_indices = self.calculate_weights(top_k, power)

        if current_weights is None:
            return None, None

        # 检查是否需要开始新的过渡
        needs_transition = self._check_transition_needed(current_indices)

        if needs_transition or self.is_in_transition:
            return self._apply_smooth_transition(current_weights, current_indices, transition_speed)
        else:
            # 不需要过渡，直接使用当前权重
            self.previous_weights = current_weights.copy()
            self.previous_indices = current_indices.copy()
            return current_weights, current_indices

    def _check_transition_needed(self, current_indices):
        """检查是否需要权重过渡"""
        if self.previous_indices is None:
            return False  # 第一帧，不需要过渡

        # 检查最近点集合是否发生变化
        previous_set = set(self.previous_indices)
        current_set = set(current_indices)

        return previous_set != current_set

    def _apply_smooth_transition(self, current_weights, current_indices, transition_speed):
        """应用平滑权重过渡"""
        if not self.is_in_transition:
            # 开始新的过渡
            self.is_in_transition = True
            self.transition_progress = 0.0
            print("开始权重平滑过渡...")

        # 更新过渡进度
        self.transition_progress = min(1.0, self.transition_progress + transition_speed)
        t = self._ease_in_out(self.transition_progress)  # 使用缓动函数使过渡更自然

        # 计算过渡权重
        transition_weights = self._calculate_transition_weights(
            current_weights, current_indices, t
        )

        # 检查过渡是否完成
        if self.transition_progress >= 1.0:
            self.is_in_transition = False
            self.previous_weights = current_weights.copy()
            self.previous_indices = current_indices.copy()
            print("权重过渡完成")

        return transition_weights, current_indices

    def _calculate_transition_weights(self, target_weights, target_indices, t):
        """计算过渡期间的权重"""
        if self.previous_weights is None:
            return target_weights

        transition_weights = np.zeros_like(target_weights)

        # 获取新旧最近点集合
        previous_set = set(self.previous_indices)
        current_set = set(target_indices)

        # 共同点（在整个过渡期间都保持为最近点）
        common_points = previous_set.intersection(current_set)

        # 新增点（上一帧不是最近点，这一帧变成最近点）
        new_points = current_set - previous_set

        # 消失点（上一帧是最近点，这一帧不再是最近点）
        fading_points = previous_set - current_set

        # 1. 处理共同点：平滑过渡到目标权重
        for point_idx in common_points:
            start_weight = self.previous_weights[point_idx]
            end_weight = target_weights[point_idx]
            transition_weights[point_idx] = self._lerp(start_weight, end_weight, t)

        # 2. 处理新增点：从0平滑过渡到目标权重
        for point_idx in new_points:
            start_weight = 0.0  # 从0开始
            end_weight = target_weights[point_idx]
            transition_weights[point_idx] = self._lerp(start_weight, end_weight, t)

        # 3. 处理消失点：从之前权重平滑过渡到0
        for point_idx in fading_points:
            start_weight = self.previous_weights[point_idx]
            end_weight = 0.0  # 过渡到0
            transition_weights[point_idx] = self._lerp(start_weight, end_weight, t)

        # 确保权重和为1（防止浮点误差）
        weight_sum = np.sum(transition_weights)
        if weight_sum > 0:
            transition_weights = transition_weights / weight_sum

        return transition_weights

    def _lerp(self, a, b, t):
        """线性插值"""
        return a + (b - a) * t

    def _ease_in_out(self, t):
        """缓动函数，使过渡更自然"""
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    def update_frame(self):
        """更新帧计数（用于时间相关的过渡）"""
        self.current_frame += 1


class AdvancedSmoothWeightCalculator(SmoothWeightCalculator):
    """更高级的平滑权重计算器，支持距离加权过渡"""

    def __init__(self):
        super(AdvancedSmoothWeightCalculator, self).__init__()
        self.distance_threshold = 1.0  # 距离阈值，小于此值才进行平滑过渡
        self.min_weight_change = 0.01  # 最小权重变化阈值

    def calculate_weights_with_distance_based_transition(self, top_k=3, power=2):
        """
        基于距离变化的权重过渡
        只有当最近点发生较大距离变化时才进行平滑过渡
        """
        current_weights, current_indices = self.calculate_weights(top_k, power)

        if current_weights is None:
            return None, None

        # 计算距离变化
        distance_change = self._calculate_distance_change(current_indices)

        # 只有当距离变化超过阈值时才进行过渡
        if distance_change > self.distance_threshold or self.is_in_transition:
            transition_speed = min(0.3, distance_change * 0.1)  # 根据距离变化调整速度
            return self.calculate_smooth_weights(top_k, power, transition_speed)
        else:
            # 距离变化很小，直接使用当前权重
            self.previous_weights = current_weights.copy()
            self.previous_indices = current_indices.copy()
            return current_weights, current_indices

    def _calculate_distance_change(self, current_indices):
        """计算最近点集合的距离变化"""
        if self.previous_indices is None:
            return 0.0

        distances = self.calculate_distances()
        if distances is None:
            return 0.0

        # 计算新旧最近点集合的平均距离变化
        previous_avg_dist = np.mean([distances[i] for i in self.previous_indices])
        current_avg_dist = np.mean([distances[i] for i in current_indices])

        return abs(current_avg_dist - previous_avg_dist)

    def print_detailed_transition_report(self, top_k=3, power=2):
        """打印详细的过渡报告"""
        weights, indices = self.calculate_weights_with_distance_based_transition(top_k, power)

        if weights is None:
            return

        distances = self.calculate_distances()

        print("=" * 70)
        print("平滑权重过渡详细报告")
        print("=" * 70)
        print(f"过渡状态: {'进行中' if self.is_in_transition else '已完成'}")
        print(f"过渡进度: {self.transition_progress:.2f}")
        print(f"最近点数量: {len(indices)}")
        print()

        # 分类显示点状态
        if self.previous_indices is not None:
            previous_set = set(self.previous_indices)
            current_set = set(indices)

            common_points = previous_set.intersection(current_set)
            new_points = current_set - previous_set
            fading_points = previous_set - current_set

            print("点状态分类:")
            print(f"  持续点: {len(common_points)}个 (在整个过渡期间保持活跃)")
            print(f"  新增点: {len(new_points)}个 (从0开始渐入)")
            print(f"  消失点: {len(fading_points)}个 (逐渐淡出到0)")
            print()

        print("各点详细信息:")
        for i, (weight, distance) in enumerate(zip(weights, distances)):
            status = "活跃" if weight > 0 else "非活跃"

            # 判断点状态
            point_status = ""
            if self.previous_indices is not None:
                if i in common_points:
                    point_status = "持续点"
                elif i in new_points:
                    point_status = "新增点 ↑"
                elif i in fading_points:
                    point_status = "消失点 ↓"
                else:
                    point_status = "非最近点"

            print(f"  点{i + 1}: 权重={weight:.4f}, 距离={distance:.3f} [{status}] {point_status}")

        print(f"权重和: {np.sum(weights):.6f}")
        print("=" * 70)

        return weights, indices


# 使用示例和测试函数
def test_smooth_transition():
    """测试平滑过渡功能"""
    print("测试平滑权重过渡系统...")

    # 创建测试数据
    calculator = AdvancedSmoothWeightCalculator()

    # 模拟活动点移动轨迹（测试过渡效果）
    test_trajectory = [
        [1.0, 2.0, 3.0],  # 靠近点1
        [1.5, 2.5, 3.5],  # 稍微移动
        [2.5, 3.5, 4.5],  # 移动到点2附近（触发过渡）
        [3.0, 4.0, 5.0],  # 完全切换到点2
    ]

    # 固定测试点
    calculator.fixed_points = [
        [1, 2, 3],  # 点1
        [3, 4, 5],  # 点2
        [2, 5, 1],  # 点3
        [5, 1, 3]  # 点4
    ]
    calculator.fixed_objects = [f"point_{i + 1}" for i in range(len(calculator.fixed_points))]

    print("固定点位置:")
    for i, point in enumerate(calculator.fixed_points):
        print(f"  点{i + 1}: {point}")

    print("\n模拟活动点移动轨迹:")
    for i, active_point in enumerate(test_trajectory):
        print(f"\n--- 第{i + 1}帧: 活动点位置 {active_point} ---")
        calculator.active_point = np.array(active_point)
        calculator.update_frame()

        weights, indices = calculator.print_detailed_transition_report()

        if weights is not None:
            # 应用权重到Maya属性（如果运行在Maya中）
            try:
                # 这里可以添加实际应用到Maya属性的代码
                blendshape_attrs = ["blendShape1.pCube1", "blendShape1.pCube2",
                                    "blendShape1.pCube3", "blendShape1.pCube4"]
                for j, attr in enumerate(blendshape_attrs):
                    if cmds.objExists(attr):
                        cmds.setAttr(attr, weights[j])
                        print(f"    设置 {attr} = {weights[j]:.4f}")
            except:
                pass  # 不在Maya环境中运行时忽略


# 集成到主接口
def run_smooth_weight_calculation(active_point_source=None, top_k=3, power=2, use_smooth=True):
    """
    运行平滑权重计算

    参数:
        use_smooth: 是否使用平滑过渡
    """
    if use_smooth:
        calculator = AdvancedSmoothWeightCalculator()
    else:
        calculator = MayaWeightCalculator()

    # 获取固定点
    if not calculator.get_selected_objects_positions():
        return None, None, None

    # 获取活动点
    if not calculator.get_active_point_position(active_point_source):
        return None, None, None

    # 计算权重
    if use_smooth:
        weights, important_indices = calculator.print_detailed_transition_report(top_k, power)
    else:
        weights, important_indices = calculator.print_weight_report(top_k, power)

    return calculator, weights, important_indices


# 替换原来的测试函数
def test_with_sample_data():
    """使用平滑过渡版本的测试函数"""
    print("使用平滑权重过渡系统测试...")

    calculator = AdvancedSmoothWeightCalculator()

    # 获取场景中的对象数据
    sample_fixed_points = []
    fixed_objects = []

    # 获取pCube1-4的位置
    for i in range(1, 5):
        obj_name = f'pCube{i}'
        if cmds.objExists(obj_name):
            try:
                t = cmds.getAttr(obj_name + '.t')[0]
                sample_fixed_points.append([t[0], t[1], t[2]])
                fixed_objects.append(obj_name)
            except:
                print(f"无法获取对象 {obj_name} 的位置")

    if not sample_fixed_points:
        print("未找到测试对象，使用示例数据")
        sample_fixed_points = [
            [1, 2, 3],
            [3, 4, 5],
            [2, 5, 1],
            [5, 1, 3]
        ]
        fixed_objects = [f"point_{i + 1}" for i in range(len(sample_fixed_points))]

    # 获取活动点位置（pCube5）
    if cmds.objExists('pCube5'):
        t = cmds.getAttr('pCube5.t')[0]
        sample_active_point = [t[0], t[1], t[2]]
    else:
        sample_active_point = [2.0, 3.0, 4.0]  # 默认位置

    calculator.fixed_points = sample_fixed_points
    calculator.fixed_objects = fixed_objects
    calculator.active_point = np.array(sample_active_point)

    print("测试数据:")
    print(f"固定点: {len(sample_fixed_points)}个")
    print(f"活动点: {sample_active_point}")

    # 运行平滑权重计算
    weights, important_indices = calculator.print_detailed_transition_report()

    # 应用权重到blendShape属性
    if weights is not None:
        for i, obj_name in enumerate(fixed_objects):
            attr_name = f"blendShape1.{obj_name}"
            if cmds.objExists(attr_name):
                cmds.setAttr(attr_name, weights[i])
                print(f"应用权重: {attr_name} = {weights[i]:.4f}")

    return calculator, weights, important_indices


# 主函数更新
def main():
    """主函数：运行平滑权重计算"""
    print("Maya平滑权重过渡系统")
    print("使用方法:")
    print("1. 选择作为固定点的对象")
    print("2. 运行 main() 函数")
    print("3. 移动活动点观察平滑过渡效果")

    # 运行平滑版本
    calculator, weights, important_indices = run_smooth_weight_calculation(use_smooth=True)

    return calculator, weights, important_indices


# 保持原有接口兼容性
if __name__ == "__main__":
    # 测试平滑过渡功能
    test_smooth_transition()

    # 在Maya中运行时取消注释：
    # main()