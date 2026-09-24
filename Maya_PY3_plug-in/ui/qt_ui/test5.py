# coding=gbk
import maya.cmds as cmds
import math


class CurveInfluenceSystem:
    """曲线影响系统：物体在距离曲线1米内受到影响"""

    def __init__(self):
        self.influence_curve = None
        self.influenced_objects = []
        self.influence_distance = 1.0  # 1米影响距离
        self.influence_strength = 1.0  # 影响强度

    def create_influence_curve(self, points=None):
        """创建影响曲线（基于您图片中的S形轮廓）"""

        if points is None:
            # 根据您图片的S形轮廓创建三维曲线点
            points = [
                (0, 0, 0),  # 起点
                (0, 2, 0),  # 向上弯曲
                (0, 4, 0),  # 向左弯曲
                (0, 6, 0),  # 回到中心
                (0, 8, 0),  # 向右弯曲
                (0, 10, 0),  # 向上延伸
                (0, 12, 0)  # 终点
            ]

        self.influence_curve = cmds.curve(degree=3, p=points, name="influenceCurve")

        # 设置曲线显示属性（红色，类似您图片中的轮廓）
        cmds.setAttr(f"{self.influence_curve}.overrideEnabled", 1)
        cmds.setAttr(f"{self.influence_curve}.overrideColor", 13)  # 红色

        print(f"影响曲线创建成功: {self.influence_curve}")
        return self.influence_curve

    def add_influenced_object(self, obj_name=None, obj_type="sphere"):
        """添加受影响的物体"""

        if obj_name is None:
            if obj_type == "sphere":
                obj = cmds.polySphere(radius=0.2, name="influencedSphere")[0]
            elif obj_type == "cube":
                obj = cmds.polyCube(width=0.4, height=0.4, depth=0.4, name="influencedCube")[0]
            else:
                obj = cmds.polySphere(radius=0.2, name="influencedObject")[0]
        else:
            obj = obj_name

        # 设置物体显示属性（黄色，类似您图片中的内部线条）
        cmds.setAttr(f"{obj}.overrideEnabled", 1)
        cmds.setAttr(f"{obj}.overrideColor", 17)  # 黄色

        self.influenced_objects.append(obj)
        print(f"受影响物体添加成功: {obj}")
        return obj

    def calculate_curve_influence(self, point_position):
        """计算点受曲线影响的强度（基于1米距离）"""

        if self.influence_curve is None:
            return 0.0

        # 找到曲线上距离该点最近的位置
        curve_shape = cmds.listRelatives(self.influence_curve, shapes=True)[0]
        closest_point = cmds.pointOnCurve(curve_shape, parameter=0.0, position=True)
        print(closest_point)
        # 计算距离
        distance = self.calculate_distance(point_position, closest_point)
        print(distance)
        # 如果距离大于1米，没有影响
        if distance > self.influence_distance:
            return 0.0

        # 计算影响强度（距离越近，影响越强）
        influence = 1.0 - (distance / self.influence_distance)
        return influence * self.influence_strength

    def calculate_distance(self, point1, point2):
        """计算两点之间的距离"""
        dx = point1[0] - point2[0]
        dy = point1[1] - point2[1]
        dz = point1[2] - point2[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def create_influence_zone_visualization(self):
        """创建影响区域的可视化（1米范围）"""

        # 沿着曲线创建一系列小球来表示影响范围
        curve_shape = cmds.listRelatives(self.influence_curve, shapes=True)[0]

        # 在曲线上采样多个点
        sample_points = []
        for i in range(0, 11):
            param = i * 0.1
            point = cmds.pointOnCurve(curve_shape, parameter=param, position=True)
            sample_points.append(point)

        # 在每个采样点创建影响范围指示器
        for i, point in enumerate(sample_points):
            sphere = cmds.polySphere(radius=self.influence_distance*0.01, name=f"influenceIndicator_{i}")[0]
            cmds.move(point[0], point[1], point[2], sphere)

            # 创建透明材质表示影响范围
            shader = cmds.shadingNode("lambert", asShader=True, name=f"influenceShader_{i}")
            cmds.setAttr(f"{shader}.color", 1, 0, 0)  # 红色
            cmds.setAttr(f"{shader}.transparency", 0.7, 0.7, 0.7)  # 半透明

            # 应用材质
            cmds.select(sphere)
            cmds.hyperShade(assign=shader)

        print("影响区域可视化创建完成")

    def setup_automatic_influence(self):
        """设置自动影响系统（使用表达式或脚本作业）"""

        # 创建表达式来自动计算影响
        expression_code = """
        // 自动影响表达式
        for ($obj in {objects}) {{
            // 获取物体位置
            float $pos[] = `getAttr ($obj + ".translate")`;

            // 计算受曲线影响的强度
            // 这里需要调用Maya的曲线最近点计算函数
            // 实际实现中可以使用python脚本作业更精确地控制
        }}
        """.format(objects=str(self.influenced_objects))

        # # 使用脚本作业来实时计算影响
        # script_job = cmds.scriptJob(
        #     event=["SelectionChanged", self.update_influence_calculation],
        #     permanent=True
        # )

        # return script_job

    def update_influence_calculation(self):
        """更新影响计算（脚本作业回调函数）"""

        for obj in self.influenced_objects:
            # 获取物体当前位置
            position = cmds.xform(obj, query=True, translation=True, worldSpace=True)

            # 计算影响强度
            influence = self.calculate_curve_influence(position)

            if influence > 0:
                # 应用影响效果（例如：改变颜色、大小或位置）
                self.apply_influence_effect(obj, influence)
            else:
                # 重置为不受影响状态
                self.reset_influence_effect(obj)
        print(self.influenced_objects)

    def apply_influence_effect(self, obj, influence_strength):
        """应用影响效果到物体"""

        # 效果1：改变颜色（越接近曲线，颜色越红）
        cmds.setAttr(f"{obj}.overrideColor", 13)  # 红色

        # 效果2：轻微缩放（受吸引力影响）
        scale_factor = 1.0 + influence_strength * 0.3
        cmds.setAttr(f"{obj}.scaleX", scale_factor)
        cmds.setAttr(f"{obj}.scaleY", scale_factor)
        cmds.setAttr(f"{obj}.scaleZ", scale_factor)

        # 效果3：朝向曲线方向（可选）
        # 这里可以添加朝向曲线的旋转逻辑

    def reset_influence_effect(self, obj):
        """重置物体为不受影响状态"""

        cmds.setAttr(f"{obj}.overrideColor", 17)  # 黄色
        cmds.setAttr(f"{obj}.scaleX", 1.0)
        cmds.setAttr(f"{obj}.scaleY", 1.0)
        cmds.setAttr(f"{obj}.scaleZ", 1.0)

    def create_demo_scene(self):
        """创建完整的演示场景"""

        print("正在创建曲线影响系统演示场景...")

        # 1. 创建影响曲线（基于您图片的S形状）
        self.create_influence_curve()

        # 2. 添加多个受影响物体
        for i in range(5):
            # 在曲线周围随机位置创建物体
            x = (i - 2) * 2  # 在X轴上分布
            x = 0
            obj = self.add_influenced_object()
            cmds.move(x, i * 1.5, 0, obj)  # 分散放置

        # 3. 创建影响区域可视化
        self.create_influence_zone_visualization()
        #
        # # 4. 设置自动影响系统
        # self.setup_automatic_influence()

        print("演示场景创建完成！")
        print(f"影响曲线: {self.influence_curve}")
        print(f"受影响物体: {self.influenced_objects}")
        print("物体在距离曲线1米内时会受到红色影响效果")


# 使用示例
def main():
    """主函数：运行曲线影响系统"""

    # 创建影响系统实例
    influence_system = CurveInfluenceSystem()

    # 设置影响参数
    influence_system.influence_distance = 10.0  # 1米影响距离
    influence_system.influence_strength = 1.0  # 完全影响强度

    # 创建演示场景
    influence_system.create_demo_scene()

    # 手动测试影响计算
    test_point = [0, 0, 0]  # 测试点位置
    influence = influence_system.calculate_curve_influence(test_point)
    print(f"测试点 {test_point} 的影响强度: {influence}")

    return influence_system








# 运行系统
if __name__ == "__main__":
    system = main()

import maya.OpenMaya as om
import math


def get_closest_point_on_curve_api(query_point, curve_dag_path):
    """
    使用 Maya API 获取曲线上最近的点
    基于您图片中的红黄曲线结构
    """
    # 创建曲线函数集
    curve_fn = om.MFnNurbsCurve()
    curve_fn.setObject(curve_dag_path)

    # 将查询点转换为 MPoint
    query_mPoint = om.MPoint(query_point[0], query_point[1], query_point[2])
    # 方法1: 使用 getParamAtPoint 获取最近参数
    param = om.MDoublePtr()
    success = curve_fn.getParamAtPoint(query_mPoint, param, 1e-6, om.MSpace.kWorld)
    print(success)
    if success:
        # 根据参数获取精确点位置
        closest_point = om.MPoint()
        curve_fn.getPointAtParam(param[0], closest_point, om.MSpace.kWorld)

        distance = query_mPoint.distanceTo(closest_point)

        return {
            'point': (closest_point.x, closest_point.y, closest_point.z),
            'parameter': param[0],
            'distance': distance,
            'method': 'getParamAtPoint'
        }



def get_curve_dag_path(curve_name):
    """获取曲线的DAG路径"""

    selection_list = om.MSelectionList()
    selection_list.add(curve_name)
    dag_path = om.MDagPath()
    selection_list.getDagPath(0, dag_path)
    return dag_path

# 获取曲线DAG路径
curve_dag_path = get_curve_dag_path("nurbsCircleShape1")

# 定义查询点
query_point = (1, 1, 1)  # 三维坐标

# 调用函数计算最近点
result = get_closest_point_on_curve_api(query_point, curve_dag_path)

# 处理结果
if result:
    print(f"最近点: {result['point']}")
    print(f"距离: {result['distance']}")

def get_closest_point_by_sampling(query_point, curve_fn, samples=100):
    """采样法：在曲线上均匀采样找到最近点"""

    query_mPoint = om.MPoint(query_point[0], query_point[1], query_point[2])

    min_distance = float('inf')
    best_point = None
    best_param = 0.0

    # 在曲线参数空间均匀采样
    for i in range(samples + 1):
        param = i / float(samples)

        try:
            point = om.MPoint()
            curve_fn.getPointAtParam(param, point, om.MSpace.kWorld)

            distance = query_mPoint.distanceTo(point)

            if distance < min_distance:
                min_distance = distance
                best_point = point
                best_param = param
        except:
            continue

    if best_point:
        return {
            'point': (best_point.x, best_point.y, best_point.z),
            'parameter': best_param,
            'distance': min_distance,
            'method': 'sampling'
        }

    return None