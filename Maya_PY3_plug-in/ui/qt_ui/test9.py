import maya.cmds as cmds
import maya.OpenMaya as om
import math


class SplineWeightSystem:
    def __init__(self):
        self.weights = []  # 存储四条样条的权重
        self.u_params = []  # 存储每条样条上最近点的U参数
        self.initial_closest_points = []  # 存储初始最近点位置
        self.initial_reference_point = None  # 存储参考点初始位置
        self.curve_fns = []  # 存储样条曲线函数对象

    def initialize_system(self, reference_point_pos, curve_shape_names):
        """
        初始化权重系统
        :param reference_point_pos: 参考点位置 (x, y, z)
        :param curve_shape_names: 四条样条曲线形状节点名称列表
        """
        if len(curve_shape_names) != 4:
            raise ValueError("需要提供四条样条曲线")

        # 将参考点转换为MPoint
        self.initial_reference_point = om.MPoint(
            reference_point_pos[0],
            reference_point_pos[1],
            reference_point_pos[2]
        )

        # 准备工具对象
        util = om.MScriptUtil()
        param_ptr = util.asDoublePtr()

        # 清空之前的数据
        self.curve_fns = []
        self.u_params = []
        self.initial_closest_points = []
        distances = []

        # 获取每条样条的曲线函数对象并计算最近点
        for curve_name in curve_shape_names:
            # 获取曲线API对象
            selection_list = om.MSelectionList()
            selection_list.add(curve_name)
            dag_path = om.MDagPath()
            selection_list.getDagPath(0, dag_path)

            curve_fn = om.MFnNurbsCurve(dag_path)
            self.curve_fns.append(curve_fn)

            # 计算最近点
            closest_point = om.MPoint()
            curve_fn.closestPoint(
                self.initial_reference_point,
                closest_point,
                param_ptr,
                0.001,
                om.MSpace.kWorld
            )

            u_param = util.getDouble(param_ptr)
            self.u_params.append(u_param)
            self.initial_closest_points.append(om.MPoint(closest_point))

            # 计算距离
            distance = self.initial_reference_point.distanceTo(closest_point)
            distances.append(distance)
            print(f"样条 {curve_name}: 最近点距离 = {distance:.4f}, U参数 = {u_param:.4f}")

        # 计算权重
        self.calculate_weights(distances)

        # 验证权重总和为1
        weight_sum = sum(self.weights)
        print(f"权重计算完成: {[f'{w:.4f}' for w in self.weights]}, 总和 = {weight_sum:.6f}")

        return self.weights

    def calculate_weights(self, distances):
        """基于距离计算归一化权重"""
        epsilon = 1e-6  # 防止除零的小常数

        # 计算原始权重（距离越小权重越大）
        raw_weights = [1.0 / (d + epsilon) for d in distances]

        # 归一化处理，使权重总和为1
        total_weight = sum(raw_weights)
        self.weights = [w / total_weight for w in raw_weights]

        return self.weights

    def calculate_reference_point_displacement(self):
        """
        计算参考点的新位置基于样条变形
        返回: 参考点的位移向量
        """
        if not self.weights or not self.curve_fns:
            raise ValueError("系统未初始化，请先调用initialize_system方法")

        total_displacement = om.MVector(0, 0, 0)

        for i, (weight, curve_fn, u_param, initial_point) in enumerate(zip(
                self.weights, self.curve_fns, self.u_params, self.initial_closest_points)):
            # 获取当前样条在U参数处的点位置
            current_point = om.MPoint()
            curve_fn.getPointAtParam(u_param, current_point, om.MSpace.kWorld)

            # 计算该样条最近点的位移
            point_displacement = om.MVector(current_point - initial_point)

            # 加权位移
            weighted_displacement = point_displacement * weight
            total_displacement += weighted_displacement

            print(f"样条 {i}: 位移 = ({point_displacement.x:.4f}, {point_displacement.y:.4f}, {point_displacement.z:.4f}), "
                  f"权重 = {weight:.4f}, 加权位移 = ({weighted_displacement.x:.4f}, {weighted_displacement.y:.4f}, {weighted_displacement.z:.4f})")

        print(f"总位移向量: ({total_displacement.x:.4f}, {total_displacement.y:.4f}, {total_displacement.z:.4f})")
        return total_displacement

    def get_current_reference_position(self):
        """获取参考点当前应处的位置"""
        displacement = self.calculate_reference_point_displacement()
        new_position = self.initial_reference_point + displacement
        return new_position


# 使用示例
def setup_spline_weight_system():
    """设置并测试样条权重系统"""

    # 创建测试场景：四边面和一个参考点
    plane = cmds.polyPlane(w=10, h=10, sx=1, sy=1, n="basePlane")[0]
    reference_locator = cmds.spaceLocator(n="referencePoint")[0]
    cmds.move(0, 0, 0, reference_locator)  # 将参考点放在平面上方

    # 创建四条样条曲线（模拟四边面的边）
    curves = []
    curve_points = [
        [(-5, 0, -5), (-5, 0, 5)],  # 左边
        [(-5, 0, 5), (5, 0, 5)],  # 上边
        [(5, 0, 5), (5, 0, -5)],  # 右边
        [(5, 0, -5), (-5, 0, -5)]  # 下边
    ]

    for i, points in enumerate(curve_points):
        curve = cmds.curve(p=points, d=1, n=f"spline_{i}")
        curves.append(cmds.listRelatives(curve, shapes=True)[0])

    # 获取参考点位置
    ref_pos = cmds.xform(reference_locator, q=True, worldSpace=True, translation=True)

    # 初始化权重系统
    weight_system = SplineWeightSystem()
    weights = weight_system.initialize_system(ref_pos, curves)

    # 创建可视化标记（每条样条的最近点）
    for i, (point, weight) in enumerate(zip(weight_system.initial_closest_points, weights)):
        locator = cmds.spaceLocator(n=f"closestPoint_{i}")[0]
        cmds.move(point.x, point.y, point.z, locator)
        cmds.setAttr(f"{locator}.overrideColor", i)  # 不同颜色区分

        # 显示权重文本
        text = cmds.textCurves(text=f"{weight:.3f}", n=f"weightText_{i}")[0]
        text_pos = [point.x, point.y + 1, point.z]  # 在点上方显示
        cmds.move(text_pos[0], text_pos[1], text_pos[2], text)

    print("=== 系统初始化完成 ===")
    print("权重分配:", [f"{w:.3f}" for w in weights])

    return weight_system, reference_locator, curves


# 测试变形效果
def test_deformation(weight_system, reference_locator):
    """测试样条变形对参考点的影响"""

    # 模拟样条变形：整体抬起
    print("\n=== 测试整体抬起 ===")
    curves = cmds.ls("spline_*", type="transform")
    for curve in curves:
        cmds.move(0, 0, 0, curve, relative=True)  # 所有样条向上移动3个单位

    # 计算参考点新位置
    new_position = weight_system.get_current_reference_position()
    cmds.move(new_position.x, new_position.y, new_position.z, reference_locator)

    # 验证：参考点也应该抬起3个单位（权重总和为1的效果）
    actual_pos = cmds.xform(reference_locator, q=True, worldSpace=True, translation=True)
    expected_lift = 3.0  # 与样条移动量一致
    actual_lift = actual_pos[1] - weight_system.initial_reference_point.y
    print(f"预期抬起高度: {expected_lift}, 实际抬起高度: {actual_lift:.4f}")

    # 测试局部变形
    print("\n=== 测试局部变形 ===")
    # 只移动一条样条
    cmds.move(1, 0, 0, "spline_0", relative=True)

    new_position = weight_system.get_current_reference_position()
    cmds.move(new_position.x, new_position.y, new_position.z, reference_locator)

    return weight_system


# 运行示例
if __name__ == "__main__":
    system, ref_loc, curve_shapes = setup_spline_weight_system()
    test_deformation(system, ref_loc)





















# //loadPlugin basicSkinCluster;
#
# proc connectJointCluster( string $j, int $i )
# {
#     if ( !objExists( $j+".lockInfluenceWeights" ) )
#     {
#         select -r $j;
#         addAttr -sn "liw" -ln "lockInfluenceWeights" -at "bool";
#     }
#     connectAttr ($j+".liw") ("surfaceSkinCluster1.lockWeights["+$i+"]");
#     connectAttr ($j+".worldMatrix[0]") ("surfaceSkinCluster1.matrix["+$i+"]");
#     connectAttr ($j+".objectColorRGB") ("surfaceSkinCluster1.influenceColor["+$i+"]");
#     float $m[] = `getAttr ($j+".wim")`;
#     setAttr ("surfaceSkinCluster1.bindPreMatrix["+$i+"]") -type "matrix" $m[0] $m[1] $m[2] $m[3] $m[4] $m[5] $m[6] $m[7] $m[8] $m[9] $m[10] $m[11] $m[12] $m[13] $m[14] $m[15];
# }
# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 0;
# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 0;
# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 0;
# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 0;
# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 0;
# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 0;
# polyPlane -w 1 -h 1 -sx 4 -sy 4 -ax 0 1 0 -cuv 2 -ch 0;
# deformer -type "surfaceSkinCluster";
# setAttr surfaceSkinCluster1.useComponentsMatrix 1;
# connectJointCluster( "nurbsPlane1", 0 );
# connectAttr -f nurbsPlaneShape4.worldSpace[0] surfaceSkinCluster1.baseSurface[0];
# connectAttr -f nurbsPlaneShape1.worldSpace[0] surfaceSkinCluster1.wrapSurface[0];
# connectJointCluster( "nurbsPlane2", 1 );
# connectAttr -f nurbsPlaneShape5.worldSpace[0] surfaceSkinCluster1.baseSurface[1];
# connectAttr -f nurbsPlaneShape2.worldSpace[0] surfaceSkinCluster1.wrapSurface[1];
# connectJointCluster( "nurbsPlane3", 2 );
# connectAttr -f nurbsPlaneShape6.worldSpace[0] surfaceSkinCluster1.baseSurface[2];
# connectAttr -f nurbsPlaneShape3.worldSpace[0] surfaceSkinCluster1.wrapSurface[2];
# skinCluster -e -maximumInfluences 3 surfaceSkinCluster1;  // forces computation of default weights