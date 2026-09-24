# coding=gbk
import maya.OpenMaya as om
import math


def get_closest_point_on_curve_api(query_point, curve_dag_path):
    """
    使用 Maya API 获取曲线上最近的点 - 增强错误处理版本
    """
    try:
        # 创建曲线函数集
        curve_fn = om.MFnNurbsCurve()
        curve_fn.setObject(curve_dag_path)

        # 获取曲线参数范围[6,10](@ref)
        start_param = om.MScriptUtil().asDoublePtr()
        end_param = om.MScriptUtil().asDoublePtr()
        curve_fn.getKnotDomain(start_param, end_param)

        start_val = om.MScriptUtil().getDouble(start_param)
        end_val = om.MScriptUtil().getDouble(end_param)

        print(f"曲线参数范围: {start_val} 到 {end_val}")

        # 将查询点转换为 MPoint
        query_mPoint = om.MPoint(query_point[0], query_point[1], query_point[2])

        # 方法1: 使用 getParamAtPoint 获取最近参数
        script_util = om.MScriptUtil()
        param_ptr = script_util.asDoublePtr()

        # 调整容差设置
        tolerance = 0.001  # 增大容差

        status = curve_fn.getParamAtPoint(query_mPoint, param_ptr, tolerance, om.MSpace.kWorld)

        print(f"getParamAtPoint 状态: {status}")

        if status == om.MStatus.kSuccess:
            param_value = script_util.getDouble(param_ptr)
            print(f"获取到的参数值: {param_value}")

            # 验证参数值是否在有效范围内
            if param_value < start_val or param_value > end_val:
                print(f"警告: 参数值 {param_value} 超出曲线范围 [{start_val}, {end_val}]")
                # 进行参数裁剪
                param_value = max(start_val, min(param_value, end_val))
                print(f"调整后参数值: {param_value}")

            # 根据参数获取精确点位置
            closest_point = om.MPoint()
            point_status = curve_fn.getPointAtParam(param_value, closest_point, om.MSpace.kWorld)

            if point_status == om.MStatus.kSuccess:
                distance = query_mPoint.distanceTo(closest_point)

                return {
                    'point': (closest_point.x, closest_point.y, closest_point.z),
                    'parameter': param_value,
                    'distance': distance,
                    'method': 'getParamAtPoint',
                    'status': 'success'
                }
            else:
                print(f"getPointAtParam 失败: {point_status}")
                return None
        else:
            print(f"getParamAtPoint 失败，尝试备用方法")
            return get_closest_point_by_sampling(query_point, curve_fn, start_val, end_val)

    except Exception as e:
        print(f"方法失败: {e}")
        return None


def get_closest_point_by_sampling(query_point, curve_fn, start_param, end_param, samples=100):
    """采样法：在曲线参数范围内均匀采样找到最近点"""

    try:
        query_mPoint = om.MPoint(query_point[0], query_point[1], query_point[2])

        min_distance = float('inf')
        best_point = None
        best_param = start_param

        # 在曲线实际参数范围内均匀采样
        param_range = end_param - start_param
        for i in range(samples + 1):
            param = start_param + (i / float(samples)) * param_range

            try:
                point = om.MPoint()
                point_status = curve_fn.getPointAtParam(param, point, om.MSpace.kWorld)

                if point_status == om.MStatus.kSuccess:
                    distance = query_mPoint.distanceTo(point)

                    if distance < min_distance:
                        min_distance = distance
                        best_point = point
                        best_param = param
            except:
                continue

        if best_point:
            print(f"采样法找到最近点，距离: {min_distance}")
            return {
                'point': (best_point.x, best_point.y, best_point.z),
                'parameter': best_param,
                'distance': min_distance,
                'method': 'sampling'
            }

    except Exception as e:
        print(f"采样法出错: {e}")

    return None


def get_curve_dag_path(curve_name):
    """获取曲线的DAG路径"""

    selection_list = om.MSelectionList()
    try:
        selection_list.add(curve_name)
        dag_path = om.MDagPath()
        selection_list.getDagPath(0, dag_path)
        return dag_path
    except Exception as e:
        print(f"无法获取曲线 {curve_name}: {e}")
        return None


def test_with_real_curve():
    """使用实际存在的曲线进行测试"""

    # 检查场景中是否有曲线
    curves = cmds.ls(type='nurbsCurve')
    if not curves:
        print("场景中没有NURBS曲线，创建测试曲线...")
        # 创建测试曲线
        curve = cmds.circle(name='testCircle')[0]
        curve_shape = cmds.listRelatives(curve, shapes=True)[0]
        curve_name = curve_shape
    else:
        curve_name = curves[0]
        print(f"使用现有曲线: {curve_name}")

    return curve_name


# 使用示例
if __name__ == "__main__":
    import maya.cmds as cmds

    # 获取或创建测试曲线
    curve_name = test_with_real_curve()

    # 获取曲线DAG路径
    curve_dag_path = get_curve_dag_path(curve_name)

    if curve_dag_path:
        print("成功获取曲线DAG路径")

        # 获取曲线边界框以确定合理的测试点
        curve_transform = cmds.listRelatives(curve_name, parent=True)[0]
        bbox = cmds.exactWorldBoundingBox(curve_transform)

        # 在曲线附近创建测试点
        center_x = (bbox[0] + bbox[3]) / 2
        center_y = (bbox[1] + bbox[4]) / 2
        center_z = (bbox[2] + bbox[5]) / 2

        # 创建在曲线边界外的测试点
        query_point = (center_x + 2.0, center_y, center_z)
        print(f"测试点坐标: {query_point}")

        # 调用函数计算最近点
        result = get_closest_point_on_curve_api(query_point, curve_dag_path)

        # 处理结果
        if result:
            print("? 测试成功！")
            print(f"最近点: {result['point']}")
            print(f"距离: {result['distance']:.6f}")
            print(f"曲线参数: {result['parameter']:.6f}")
            print(f"计算方法: {result['method']}")
        else:
            print("? 无法计算最近点")
    else:
        print("无法获取曲线DAG路径")

import maya.OpenMaya as om

# 1. 获取曲线的函数集
selection_list = om.MSelectionList()
selection_list.add('curveShape1')  # 替换为您的曲线形状节点名称

dag_path = om.MDagPath()
component = om.MObject()

# 获取DAG路径
selection_list.getDagPath(0, dag_path, component)

curve_fn = om.MFnNurbsCurve(dag_path)

# 2. 定义世界空间中的一个查询点
test_point = om.MPoint(-1.0, 1.0, 0.0)  # 替换为您感兴趣的坐标

# 3. 使用 getParamAtPoint 1.0版本（不带容差参数）
# 根据图片中的第一个方法签名：getParamAtPoint(MPoint, double&, MSpace)
script_util = om.MScriptUtil()
param_ptr = script_util.asDoublePtr()

# 调用1.0版本：只有3个参数（点、参数引用、空间）
point_status = curve_fn.getParamAtPoint(test_point, param_ptr, om.MSpace.kWorld)

if point_status == 0:  # 0表示成功
    param_value = script_util.getDouble(param_ptr)
    print("曲线参数:", param_value)
else:
    print("获取参数失败，状态码:", point_status)

param_value = 0.5
# 4. 获取该参数对应的曲线上的点坐标
point_on_curve = curve_fn.getPointAtParam(param_value, om.MSpace.kWorld)
print("曲线上最近点的坐标:", (point_on_curve.x, point_on_curve.y, point_on_curve.z))


