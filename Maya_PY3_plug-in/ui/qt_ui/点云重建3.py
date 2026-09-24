#coding=gbk
import maya.cmds as cmds
import random
import math


def create_point_cloud_sphere_model():
    """
    创建由点云数据构成的连续拓扑球体模型
    """
    # 清理场景
    if cmds.objExists('PointCloudSphere'):
        cmds.delete('PointCloudSphere')

    # 创建主组
    main_group = cmds.group(empty=True, name='PointCloudSphere')

    print("=" * 60)
    print("创建点云连续拓扑球体模型")
    print("=" * 60)

    # 1. 生成球面点云数据
    print("生成球面点云数据...")
    point_cloud = generate_sphere_point_cloud(1500, radius=5.0)

    # 2. 创建连续拓扑网格
    print("构建连续拓扑网格...")
    sphere_model = create_continuous_topology_mesh(point_cloud, "point_cloud_sphere")

    if sphere_model:
        cmds.parent(sphere_model, main_group)

        # 3. 应用点云风格材质
        print("应用点云风格材质...")
        apply_point_cloud_material(sphere_model)

        # 4. 添加点云可视化
        print("添加点云可视化...")
        point_visualization = create_point_visualization(point_cloud, "point_visuals")
        cmds.parent(point_visualization, main_group)

        # 5. 验证模型质量
        verify_model_quality(sphere_model)

        print("? 点云球体模型创建完成！")
    else:
        # 回退方案
        print("使用回退方案创建基础球体...")
        fallback_sphere = create_fallback_sphere()
        cmds.parent(fallback_sphere, main_group)

    # 调整视图
    cmds.viewFit(all=True)

    return main_group


def generate_sphere_point_cloud(num_points, radius=5.0):
    """
    生成均匀分布的球面点云数据
    """
    points = []

    # 使用斐波那契螺旋采样确保均匀分布
    golden_ratio = (1 + math.sqrt(5)) / 2
    golden_angle = 2 * math.pi * (1 - 1 / golden_ratio)

    for i in range(num_points):
        # 避免在极点过度采样
        y = 1 - (i / float(num_points - 1)) * 2  # y从1到-1
        radius_at_y = math.sqrt(1 - y * y)

        theta = golden_angle * i

        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y

        # 添加轻微随机扰动
        jitter = 0.99 + random.random() * 0.02
        x = x * jitter * radius
        y = y * jitter * radius
        z = z * jitter * radius

        points.append([x, y, z])

    print(f"生成 {len(points)} 个球面点")
    return points


def create_continuous_topology_mesh(points, name):
    """
    创建连续拓扑的三角网格
    """
    try:
        # 方法1: 使用细分球体作为基础，然后将顶点吸附到点云
        return create_subdivision_sphere_with_points(points, name)
    except Exception as e:
        print(f"连续拓扑创建失败: {e}")
        return create_robust_sphere_with_points(points, name)


def create_subdivision_sphere_with_points(points, name):
    """
    创建高细分球体并将顶点吸附到点云
    """
    # 创建基础球体（高细分确保连续性）
    base_sphere = cmds.polySphere(
        name=name,
        radius=5.0,
        subdivisionsX=32,  # 高细分确保连续拓扑
        subdivisionsY=32,
        createUVs=2  # 球面映射
    )[0]

    # 计算点云中心
    center = calculate_points_center(points)

    # 将球体移动到点云中心
    cmds.setAttr(f"{base_sphere}.translateX", center[0])
    cmds.setAttr(f"{base_sphere}.translateY", center[1])
    cmds.setAttr(f"{base_sphere}.translateZ", center[2])

    # 将球体顶点吸附到最近的点云点
    snap_vertices_to_points(base_sphere, points, influence=0.8)

    # 应用平滑保持连续性
    smooth_sphere = cmds.polySmooth(
        base_sphere,
        divisions=1,
        smoothUVs=True,
        continuity=0.8  # 保持形状但平滑
    )[0]

    # 确保网格是流形的
    cmds.polyCloseBorder(smooth_sphere, constructionHistory=False)
    cmds.polyNormal(smooth_sphere, normalMode=2, constructionHistory=False)

    # 清理历史
    cmds.delete(smooth_sphere, constructionHistory=True)

    return smooth_sphere


def snap_vertices_to_points(mesh, points, influence=0.5):
    """
    将网格顶点吸附到点云，保持连续性
    """
    try:
        vertex_count = cmds.polyEvaluate(mesh, vertex=True)

        for i in range(vertex_count):
            # 获取顶点原始位置
            vertex_pos = cmds.pointPosition(f"{mesh}.vtx[{i}]")

            # 找到最近的点云点
            nearest_point = find_nearest_point(vertex_pos, points)
            if nearest_point:
                # 混合原始位置和点云位置
                new_x = vertex_pos[0] * (1 - influence) + nearest_point[0] * influence
                new_y = vertex_pos[1] * (1 - influence) + nearest_point[1] * influence
                new_z = vertex_pos[2] * (1 - influence) + nearest_point[2] * influence

                cmds.xform(f"{mesh}.vtx[{i}]", translation=[new_x, new_y, new_z])

    except Exception as e:
        print(f"顶点吸附失败: {e}")


def find_nearest_point(reference_point, points):
    """
    找到距离参考点最近的点云点
    """
    if not points:
        return None

    min_distance = float('inf')
    nearest_point = None

    for point in points:
        dx = point[0] - reference_point[0]
        dy = point[1] - reference_point[1]
        dz = point[2] - reference_point[2]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        if distance < min_distance:
            min_distance = distance
            nearest_point = point

    return nearest_point


def calculate_points_center(points):
    """
    计算点云中心
    """
    if not points:
        return [0, 0, 0]

    x_sum = sum(p[0] for p in points)
    y_sum = sum(p[1] for p in points)
    z_sum = sum(p[2] for p in points)

    count = len(points)
    return [x_sum / count, y_sum / count, z_sum / count]


def create_robust_sphere_with_points(points, name):
    """
    创建稳健的球体模型（备用方法）
    """
    try:
        # 创建基础球体
        sphere = cmds.polySphere(
            name=name,
            radius=5.0,
            subdivisionsX=24,
            subdivisionsY=24
        )[0]

        # 将球体移动到点云中心
        center = calculate_points_center(points)
        cmds.setAttr(f"{sphere}.translateX", center[0])
        cmds.setAttr(f"{sphere}.translateY", center[1])
        cmds.setAttr(f"{sphere}.translateZ", center[2])

        return sphere

    except Exception as e:
        print(f"稳健球体创建失败: {e}")
        return None


def apply_point_cloud_material(mesh):
    """
    应用点云风格材质
    """
    try:
        # 创建点云风格着色器
        shader = cmds.shadingNode('surfaceShader', asShader=True, name=f"{mesh}_point_cloud_shader")

        # 设置材质属性 - 深色基础配合高光边缘
        cmds.setAttr(f"{shader}.outColor", 0.1, 0.1, 0.2, type='double3')  # 深蓝灰色

        # 创建着色组
        shading_group = cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{shader}SG"
        )
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        cmds.sets(mesh, edit=True, forceElement=shading_group)

        # 启用线框显示以突出拓扑结构
        cmds.setAttr(f"{mesh}.displayOverrides", 1)
        cmds.setAttr(f"{mesh}.overrideDisplayType", 1)  # 模板显示

    except Exception as e:
        print(f"材质应用失败: {e}")


def create_point_visualization(points, name):
    """
    创建点云可视化
    """
    group = cmds.group(empty=True, name=name)

    # 每20个点创建一个定位器
    for i in range(0, len(points), 20):
        point = points[i]
        locator = cmds.spaceLocator(name=f"point_{i:04d}")[0]
        cmds.setAttr(f"{locator}.translateX", point[0])
        cmds.setAttr(f"{locator}.translateY", point[1])
        cmds.setAttr(f"{locator}.translateZ", point[2])
        cmds.setAttr(f"{locator}.localScaleX", 0.08)
        cmds.setAttr(f"{locator}.localScaleY", 0.08)
        cmds.setAttr(f"{locator}.localScaleZ", 0.08)

        # 设置颜色 - 红色标记点
        cmds.setAttr(f"{locator}.overrideEnabled", 1)
        cmds.setAttr(f"{locator}.overrideColor", 13)  # 红色

        cmds.parent(locator, group)

    return group


def verify_model_quality(mesh):
    """
    验证模型质量
    """
    if not cmds.objExists(mesh):
        return

    print("验证模型质量...")

    try:
        # 检查顶点和面数
        vertex_count = cmds.polyEvaluate(mesh, vertex=True)
        face_count = cmds.polyEvaluate(mesh, face=True)

        print(f"模型统计: {vertex_count} 顶点, {face_count} 面")

        # 检查网格连续性
        border_edges = 0
        edge_count = cmds.polyEvaluate(mesh, edge=True)

        for i in range(edge_count):
            edge_name = f"{mesh}.e[{i}]"
            connected_faces = cmds.polyListComponentConversion(edge_name, fromEdge=True, toFace=True)
            if connected_faces:
                face_list = cmds.ls(connected_faces, flatten=True)
                if len(face_list) == 1:  # 开放边
                    border_edges += 1

        if border_edges == 0:
            print("? 模型拓扑连续（无开放边界）")
        else:
            print(f"? 发现 {border_edges} 个开放边界")

        # 检查非流形几何
        try:
            cmds.select(mesh)
            cmds.polySelectConstraint(mode=3, type=0x0001, nonManifold=True)
            non_manifold = cmds.ls(selection=True)
            cmds.polySelectConstraint(disable=True)
            cmds.select(clear=True)

            if non_manifold:
                print("? 发现非流形几何")
            else:
                print("? 模型是流形几何")

        except:
            pass

    except Exception as e:
        print(f"质量验证失败: {e}")


def create_fallback_sphere():
    """
    创建回退球体
    """
    sphere = cmds.polySphere(name="fallback_sphere", radius=5.0)[0]
    apply_point_cloud_material(sphere)
    return sphere


def create_comparison_demo():
    """
    创建对比演示
    """
    if cmds.objExists('ComparisonDemo'):
        cmds.delete('ComparisonDemo')

    comparison_group = cmds.group(empty=True, name='ComparisonDemo')

    # 生成点云
    points = generate_sphere_point_cloud(1000, radius=4.0)

    # 1. 仅显示点云
    points_group = create_point_visualization(points, "points_only")
    cmds.setAttr(f"{points_group}.translateX", -15)
    cmds.parent(points_group, comparison_group)

    # 2. 点云+线框球体
    wireframe_sphere = cmds.polySphere(
        name="wireframe_sphere",
        radius=4.0,
        subdivisionsX=16,
        subdivisionsY=16
    )[0]
    cmds.setAttr(f"{wireframe_sphere}.translateX", 0)
    apply_point_cloud_material(wireframe_sphere)
    cmds.setAttr(f"{wireframe_sphere}.displayOverrides", 1)
    cmds.setAttr(f"{wireframe_sphere}.overrideDisplayType", 2)  # 参考显示模式
    cmds.parent(wireframe_sphere, comparison_group)

    # 添加点云到线框球体
    points_for_wireframe = create_point_visualization(points, "points_wireframe")
    cmds.setAttr(f"{points_for_wireframe}.translateX", 0)
    cmds.parent(points_for_wireframe, comparison_group)

    # 3. 连续拓扑球体（目标结果）
    continuous_sphere = create_continuous_topology_mesh(points, "continuous_sphere")
    if continuous_sphere:
        cmds.setAttr(f"{continuous_sphere}.translateX", 15)
        apply_point_cloud_material(continuous_sphere)
        cmds.parent(continuous_sphere, comparison_group)

    # 添加标签
    create_demo_labels(comparison_group)

    cmds.viewFit(all=True)
    return comparison_group


def create_demo_labels(parent_group):
    """
    创建演示标签
    """
    labels = [
        {"text": "仅点云", "x": -15, "y": 6},
        {"text": "点云+线框", "x": 0, "y": 6},
        {"text": "连续拓扑球体", "x": 15, "y": 6}
    ]

    for label in labels:
        try:
            text = cmds.textCurves(text=label["text"], font="Arial")[0]
            cmds.setAttr(f"{text}.translateX", label["x"])
            cmds.setAttr(f"{text}.translateY", label["y"])
            cmds.setAttr(f"{text}.scaleX", 0.3)
            cmds.setAttr(f"{text}.scaleY", 0.3)
            cmds.setAttr(f"{text}.scaleZ", 0.3)
            cmds.parent(text, parent_group)
        except:
            pass


# 在Maya中运行
if __name__ == "__main__":
    print("=" * 60)
    print("点云连续拓扑球体生成系统")
    print("=" * 60)

    # 设置随机种子以便结果可重现
    random.seed(42)

    print("选择运行模式:")
    print("1. 创建点云球体模型（主功能）")
    print("2. 查看对比演示")

    # 运行主功能
    try:
        result = create_point_cloud_sphere_model()
        print("? 点云球体模型创建成功！")

        # 可选：运行对比演示
        # demo = create_comparison_demo()
        # print("? 对比演示创建完成")

    except Exception as e:
        print(f"执行失败: {e}")
        print("尝试创建基本球体...")

        try:
            basic_sphere = cmds.polySphere(radius=5.0)[0]
            apply_point_cloud_material(basic_sphere)
            cmds.viewFit(all=True)
            print("基本球体创建完成")
        except:
            print("所有方法均失败")