import maya.cmds as cmds
import math


def create_locators_at_intersections(curve_name, circle_radius=1.0, sampling_step=0.0001, tolerance=0.0001):
    """
    在曲线与圆的交点处直接创建定位器

    参数:
    curve_name: 样条曲线的名称
    circle_radius: 圆的半径 (默认为1.0)
    sampling_step: 沿曲线的采样精度
    tolerance: 判定为交点的距离容差
    """

    # 存储找到的交点位置
    intersections = []

    print(f"开始沿曲线 '{curve_name}' 搜索与半径 {circle_radius} 的圆的交点...")

    # 从曲线起点到终点进行采样
    param = 0.0
    while param <= 1.0:
        try:
            # 直接获取曲线上点的位置坐标
            point_pos = cmds.pointOnCurve(curve_name, parameter=param, position=True, turnOnPercentage=True)

            # 计算该点到原点的距离 (在XY平面计算)
            distance_to_origin = math.sqrt(point_pos[0] ** 2 + point_pos[1] ** 2)

            # 如果距离在容差范围内接近圆的半径，则认为是交点
            if abs(distance_to_origin - circle_radius) <= tolerance:
                # 检查是否与已找到的交点过近，避免重复创建
                is_duplicate = False
                for existing_pos in intersections:
                    if (abs(existing_pos[0] - point_pos[0]) < tolerance and
                            abs(existing_pos[1] - point_pos[1]) < tolerance and
                            abs(existing_pos[2] - point_pos[2]) < tolerance):
                        is_duplicate = True
                        break

                if not is_duplicate:
                    intersections.append(point_pos)
                    print(f"发现交点 at 参数 {param:.3f}: 位置 ({point_pos[0]:.3f}, {point_pos[1]:.3f}, {point_pos[2]:.3f})")

            param += sampling_step

        except Exception as e:
            print(f"在参数 {param} 处采样时出错: {str(e)}")
            param += sampling_step

    # 在找到的每个交点处创建定位器
    locators = []
    for i, pos in enumerate(intersections):
        locator_name = f"curve_circle_intersect_loc_{i:02d}"
        locator = cmds.spaceLocator(name=locator_name)[0]
        cmds.xform(locator, worldSpace=True, translation=pos)
        locators.append(locator)
        print(f"已创建定位器: {locator_name}")

    print(f"操作完成！在 {len(locators)} 个交点处创建了定位器。")
    return locators


# 简化的演示函数
def simple_demo():
    """创建测试曲线并在交点处生成定位器"""
    # 创建测试曲线
    test_curve_points = [
        (-2, 0.5, 0), (-1.5, -0.3, 0), (-1, 0.7, 0),
        (-0.5, -0.5, 0), (0, 0.2, 0), (0.5, -0.8, 0),
        (1, 0.4, 0), (1.5, -0.6, 0), (2, 0.3, 0)
    ]

    test_curve = cmds.curve(name="demo_curve", point=test_curve_points, degree=3)

    # 执行定位器创建
    result = create_locators_at_intersections(test_curve, circle_radius=1.0)

    if result:
        cmds.select(result)
        return result
    else:
        print("未找到交点，请检查曲线是否与半径为1的圆相交")
        return None


# 使用示例
if __name__ == "__main__":
    # 运行演示
    simple_demo()