#coding=gbk
import maya.cmds as cmds
import numpy as np
import math
from scipy.spatial import Delaunay


def generate_sample_point_cloud(num_points=200, shape="sphere"):
    """
    生成示例点云数据

    参数:
        num_points: 点数量
        shape: 点云形状 ("sphere", "cube", "cylinder")
    """
    points = []

    if shape == "sphere":
        # 生成球体点云
        radius = 5.0
        for i in range(num_points):
            u = np.random.random()
            v = np.random.random()

            theta = u * 2.0 * math.pi
            phi = math.acos(2.0 * v - 1.0)

            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)

            # 添加噪声使点云更自然
            x += (np.random.random() - 0.5) * 0.3
            y += (np.random.random() - 0.5) * 0.3
            z += (np.random.random() - 0.5) * 0.3

            points.append([x, y, z])

    elif shape == "cube":
        # 生成立方体点云
        size = 4.0
        for i in range(num_points):
            x = (np.random.random() - 0.5) * size * 2
            y = (np.random.random() - 0.5) * size * 2
            z = (np.random.random() - 0.5) * size * 2
            points.append([x, y, z])

    elif shape == "cylinder":
        # 生成圆柱体点云
        radius = 3.0
        height = 8.0
        for i in range(num_points):
            angle = np.random.random() * 2 * math.pi
            r = radius * math.sqrt(np.random.random())
            h = (np.random.random() - 0.5) * height

            x = r * math.cos(angle)
            y = h
            z = r * math.sin(angle)
            points.append([x, y, z])

    return np.array(points)


def create_point_cloud_visualization(points, group_name="point_cloud"):
    """创建点云可视化"""
    if cmds.objExists(group_name):
        cmds.delete(group_name)

    group = cmds.group(empty=True, name=group_name)

    # 创建定位器表示点
    for i, point in enumerate(points):
        if i % 10 == 0:  # 每10个点创建一个，避免太多对象
            locator = cmds.spaceLocator(name=f"point_{i:03d}")[0]
            cmds.setAttr(f"{locator}.translateX", point[0])
            cmds.setAttr(f"{locator}.translateY", point[1])
            cmds.setAttr(f"{locator}.translateZ", point[2])
            cmds.setAttr(f"{locator}.localScaleX", 0.1)
            cmds.setAttr(f"{locator}.localScaleY", 0.1)
            cmds.setAttr(f"{locator}.localScaleZ", 0.1)

            # 根据高度设置颜色
            normalized_y = (point[1] + 5) / 10
            color_index = int(normalized_y * 31) % 32
            cmds.setAttr(f"{locator}.overrideEnabled", 1)
            cmds.setAttr(f"{locator}.overrideColor", color_index)

            cmds.parent(locator, group)

    return group


def create_surface_from_points(points, method="convex_hull"):
    """
    从点云创建表面网格

    参数:
        points: 点云数据
        method: 重建方法 ("convex_hull", "simple_mesh")
    """
    if len(points) < 3:
        cmds.warning("点数量不足，无法创建表面")
        return None

    points_2d = points[:, :2]  # 使用XZ平面进行投影

    try:
        # 执行Delaunay三角剖分
        tri = Delaunay(points_2d)
    except Exception as e:
        cmds.warning(f"三角剖分失败: {e}")
        return None

    mesh_name = f"{method}_mesh"

    # 创建所有面片
    face_meshes = []
    for i, triangle in enumerate(tri.simplices):
        if len(triangle) == 3:  # 确保是三角形
            # 获取三角形的三个顶点坐标
            v0 = points[triangle[0]]
            v1 = points[triangle[1]]
            v2 = points[triangle[2]]

            # 创建单个三角形面片
            try:
                face_mesh = cmds.polyCreateFacet(
                    p=[v0, v1, v2],
                    name=f"{mesh_name}_face_{i:04d}"
                )[0]
                face_meshes.append(face_mesh)
            except Exception as e:
                print(f"创建面片 {i} 失败: {e}")
                continue

    # 合并所有面片
    if len(face_meshes) > 1:
        try:
            combined_mesh = cmds.polyUnite(
                face_meshes,
                name=mesh_name,
                mergeUVs=True,
                constructionHistory=False
            )[0]
            # 清理临时面片
            for face_mesh in face_meshes:
                if cmds.objExists(face_mesh):
                    cmds.delete(face_mesh)
        except Exception as e:
            print(f"合并网格失败: {e}")
            # 如果合并失败，使用第一个面片
            combined_mesh = face_meshes[0] if face_meshes else None
    elif face_meshes:
        combined_mesh = face_meshes[0]
        cmds.rename(combined_mesh, mesh_name)
    else:
        cmds.warning("无法创建任何面片")
        return None

    # 设置材质
    set_mesh_material(combined_mesh, method)

    return combined_mesh


def set_mesh_material(mesh, method):
    """为网格设置材质"""
    if method == "convex_hull":
        color = (0.2, 0.6, 0.8)  # 蓝色
    elif method == "simple_mesh":
        color = (0.8, 0.3, 0.2)  # 红色
    else:
        color = (0.5, 0.5, 0.5)  # 灰色

    shader_name = f"{mesh}_shader"
    shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
    cmds.setAttr(f"{shader}.color", color[0], color[1], color[2], type='double3')
    cmds.setAttr(f"{shader}.transparency", 0.4, 0.4, 0.4, type='double3')

    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
                              name=f"{shader}SG")
    cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
    cmds.sets(mesh, edit=True, forceElement=shading_group)


def create_bounding_box(points, group_name="bounding_box"):
    """创建点云的边界框"""
    if cmds.objExists(group_name):
        cmds.delete(group_name)

    group = cmds.group(empty=True, name=group_name)

    # 计算边界
    min_x, min_y, min_z = np.min(points, axis=0)
    max_x, max_y, max_z = np.max(points, axis=0)

    # 创建边界框的8个顶点
    bbox_points = [
        [min_x, min_y, min_z],
        [max_x, min_y, min_z],
        [max_x, max_y, min_z],
        [min_x, max_y, min_z],
        [min_x, min_y, max_z],
        [max_x, min_y, max_z],
        [max_x, max_y, max_z],
        [min_x, max_y, max_z]
    ]

    # 创建边界框线框
    lines = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
        [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
        [0, 4], [1, 5], [2, 6], [3, 7]  # 侧面
    ]

    for i, line in enumerate(lines):
        p1 = bbox_points[line[0]]
        p2 = bbox_points[line[1]]

        curve = cmds.curve(
            p=[p1, p2],
            d=1,
            name=f"{group_name}_line_{i:02d}"
        )
        cmds.setAttr(f"{curve}.lineWidth", 2)
        cmds.setAttr(f"{curve}.overrideEnabled", 1)
        cmds.setAttr(f"{curve}.overrideColor", 13)  # 黄色

        cmds.parent(curve, group)

    return group


def setup_scene_lighting():
    """设置场景照明"""
    # 创建环境光
    ambient_light = cmds.ambientLight(name="scene_ambient_light")
    cmds.setAttr(f"{ambient_light}.intensity", 0.3)

    # 创建方向光
    directional_light = cmds.directionalLight(name="scene_directional_light")
    cmds.setAttr(f"{directional_light}.intensity", 0.8)
    cmds.setAttr(f"{directional_light}.rotateX", -45)
    cmds.setAttr(f"{directional_light}.rotateY", 45)

    return ambient_light, directional_light


def create_info_hud(points, mesh_info):
    """创建信息显示"""
    # 在脚本编辑器中显示信息
    print("=" * 60)
    print("点云重建信息")
    print("=" * 60)
    print(f"点云点数: {len(points)}")
    print(f"生成三角形: {mesh_info['triangle_count']} 个")
    print(f"网格顶点: {mesh_info['vertex_count']} 个")
    print(f"使用算法: {mesh_info['method']}")
    print(f"边界尺寸: {mesh_info['bounds']}")
    print("=" * 60)


def point_cloud_reconstruction_demo():
    """
    点云重建演示主函数
    """
    # 清理场景
    if cmds.objExists('point_cloud_demo'):
        cmds.delete('point_cloud_demo')

    main_group = cmds.group(empty=True, name='point_cloud_demo')

    # 设置随机种子以便结果可重现
    np.random.seed(42)

    print("开始点云重建演示...")
    shapes = ["sphere", "cube", "cylinder"]
    # 1. 生成点云数据
    points = generate_sample_point_cloud(num_points=1000, shape=shapes[0])
    print(f"? 生成点云: {len(points)} 个点")

    # 2. 创建点云可视化
    point_cloud_group = create_point_cloud_visualization(points, "raw_point_cloud")
    cmds.parent(point_cloud_group, main_group)
    print("? 创建点云可视化")

    # 3. 创建表面网格
    mesh = create_surface_from_points(points, method="convex_hull")
    if mesh:
        cmds.parent(mesh, main_group)
        print("? 创建表面网格")

        # 获取网格信息
        triangle_count = cmds.polyEvaluate(mesh, triangle=True)
        vertex_count = cmds.polyEvaluate(mesh, vertex=True)

        mesh_info = {
            'triangle_count': triangle_count,
            'vertex_count': vertex_count,
            'method': 'Delaunay三角剖分',
            'bounds': f"{np.ptp(points[:, 0]):.2f} x {np.ptp(points[:, 1]):.2f} x {np.ptp(points[:, 2]):.2f}"
        }
    else:
        mesh_info = {'triangle_count': 0, 'vertex_count': 0, 'method': '失败', 'bounds': 'N/A'}

    # 4. 创建边界框
    bbox_group = create_bounding_box(points)
    cmds.parent(bbox_group, main_group)
    print("? 创建边界框")

    # 5. 设置照明
    # setup_scene_lighting()
    print("? 设置场景照明")

    # 6. 显示信息
    create_info_hud(points, mesh_info)

    # 7. 调整视图
    cmds.viewFit(all=True)
    cmds.select(clear=True)

    print("\n点云重建演示完成！")
    print("场景包含:")
    print("- 原始点云可视化（彩色定位器）")
    print("- 重建的表面网格（半透明蓝色）")
    print("- 点云边界框（黄色线框）")

    return main_group


# 高级功能：多形状比较
def compare_shapes_demo():
    """比较不同形状的点云重建"""
    shapes = ["sphere", "cube", "cylinder"]
    comparison_group = cmds.group(empty=True, name='shape_comparison')

    for i, shape in enumerate(shapes):
        # 为每个形状生成点云
        points = generate_sample_point_cloud(num_points=150, shape=shape)

        # 创建网格
        mesh = create_surface_from_points(points, method="convex_hull")
        if mesh:
            # 在X轴上排列不同的形状
            cmds.setAttr(f"{mesh}.translateX", i * 15)
            cmds.parent(mesh, comparison_group)

            # 添加形状标签
            text = cmds.textCurves(text=shape.capitalize(), font="Arial")[0]
            cmds.setAttr(f"{text}.translateX", i * 15)
            cmds.setAttr(f"{text}.translateY", 8)
            cmds.setAttr(f"{text}.scaleX", 0.3)
            cmds.setAttr(f"{text}.scaleY", 0.3)
            cmds.setAttr(f"{text}.scaleZ", 0.3)
            cmds.parent(text, comparison_group)

    cmds.viewFit(all=True)
    return comparison_group


# 在Maya中运行
if __name__ == "__main__":
    # 运行主演示
    demo_scene = point_cloud_reconstruction_demo()

    # 取消注释以下行来运行形状比较演示
    # comparison_scene = compare_shapes_demo()

    print("\n使用说明:")
    print("1. 在Outliner中选择不同对象查看详细信息")
    print("2. 通过属性编辑器调整材质和透明度")
    print("3. 使用鼠标进行视图导航（Alt+鼠标按键）")
    print("4. 修改代码参数生成不同形状的点云")