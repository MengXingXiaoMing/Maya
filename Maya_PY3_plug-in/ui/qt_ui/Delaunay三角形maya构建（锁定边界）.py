#coding=gbk
import maya.cmds as cmds
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
import math


def hsv_to_rgb(h, s, v):
    """将HSV颜色转换为RGB颜色"""
    if s == 0.0:
        return (v, v, v)

    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    i = i % 6
    if i == 0:
        return (v, t, p)
    elif i == 1:
        return (q, v, p)
    elif i == 2:
        return (p, v, t)
    elif i == 3:
        return (p, q, v)
    elif i == 4:
        return (t, p, v)
    else:
        return (v, p, q)


def create_convex_hull_spherical_triangulation(num_points=15, sphere_radius=1.0):
    """
    基于随机点凸包边界的球面三角剖分

    参数:
        num_points: 随机点数量
        sphere_radius: 球体半径
    """
    # 清理场景
    if cmds.objExists('convex_hull_sphere_group'):
        cmds.delete('convex_hull_sphere_group')

    # 创建组
    sphere_group = cmds.group(empty=True, name='convex_hull_sphere_group')

    # 1. 生成随机点
    np.random.seed(42)  # 固定随机种子以便结果可重现
    points_2d = np.random.rand(num_points, 2)

    print(f"生成 {num_points} 个随机点")

    # 2. 计算凸包边界
    hull = ConvexHull(points_2d)
    hull_points = points_2d[hull.vertices]  # 凸包边界点

    print(f"凸包边界点数量: {len(hull_points)}")

    # 3. 执行Delaunay三角剖分
    tri = Delaunay(points_2d)

    print(f"生成 {len(tri.simplices)} 个三角形")

    # 4. 将2D点映射到球面
    points_3d = []
    for point_2d in points_2d:
        u, v = point_2d

        # 将UV坐标转换为球面坐标
        theta = u * 2 * math.pi  # 经度 [0, 2π]
        phi = v * math.pi  # 纬度 [0, π]

        # 球面坐标转笛卡尔坐标
        x = sphere_radius * math.sin(phi) * math.cos(theta)
        y = sphere_radius * math.cos(phi)  # 让Y轴向上
        z = sphere_radius * math.sin(phi) * math.sin(theta)

        points_3d.append([x, y, z])

    points_3d = np.array(points_3d)

    # 5. 在Maya中创建球面三角形网格
    for i, triangle in enumerate(tri.simplices):
        # 获取三角形的三个3D顶点
        v0 = points_3d[triangle[0]]
        v1 = points_3d[triangle[1]]
        v2 = points_3d[triangle[2]]

        # 创建多边形面片
        mesh_name = f"sphere_triangle_{i:02d}"
        mesh = cmds.polyCreateFacet(
            name=mesh_name,
            p=[(v0[0], v0[1], v0[2]),
               (v1[0], v1[1], v1[2]),
               (v2[0], v2[1], v2[2])]
        )[0]

        # 设置材质颜色（基于三角形索引）
        hue = (i * 0.618) % 1.0  # 使用黄金比例分布颜色
        rgb = hsv_to_rgb(hue, 0.7, 0.8)

        # 创建着色器
        shader_name = f"{mesh_name}_shader"
        shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
        cmds.setAttr(f'{shader}.color', rgb[0], rgb[1], rgb[2], type='double3')

        # 使三角形半透明以便观察重叠部分
        cmds.setAttr(f'{shader}.transparency', 0.3, 0.3, 0.3, type='double3')

        # 应用着色器
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
                                  name=f"{shader_name}SG")
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        cmds.sets(mesh, edit=True, forceElement=shading_group)

        # 添加到组
        cmds.parent(mesh, sphere_group)

    # 6. 创建顶点标记（区分凸包边界点和内部点）
    for i, point in enumerate(points_3d):
        # 检查点是否为凸包边界点
        is_hull_point = i in hull.vertices

        if is_hull_point:
            locator = cmds.spaceLocator(name=f'hull_point_{i}')[0]
            cmds.setAttr(f'{locator}.overrideColor', 13)  # 绿色 - 边界点
        else:
            locator = cmds.spaceLocator(name=f'interior_point_{i}')[0]
            cmds.setAttr(f'{locator}.overrideColor', 13)  # 红色 - 内部点

        cmds.setAttr(f'{locator}.translateX', point[0])
        cmds.setAttr(f'{locator}.translateY', point[1])
        cmds.setAttr(f'{locator}.translateZ', point[2])
        cmds.setAttr(f'{locator}.localScaleX', 0.2)
        cmds.setAttr(f'{locator}.localScaleY', 0.2)
        cmds.setAttr(f'{locator}.localScaleZ', 0.2)

        cmds.parent(locator, sphere_group)

    # 7. 创建凸包边界线（在球面上）
    hull_curve_points = []
    for vertex_idx in hull.vertices:
        hull_curve_points.append(points_3d[vertex_idx].tolist())

    # 闭合曲线（添加第一个点到最后）
    hull_curve_points.append(hull_curve_points[0])

    # 创建边界曲线
    hull_curve = cmds.curve(
        name='convex_hull_boundary',
        p=hull_curve_points,
        d=1  # 1阶曲线（线性）
    )
    cmds.setAttr(f'{hull_curve}.lineWidth', 3)
    cmds.setAttr(f'{hull_curve}.overrideColor', 17)  # 黄色
    cmds.parent(hull_curve, sphere_group)

    # 8. 创建参考球体
    reference_sphere = cmds.polySphere(name='reference_sphere', radius=sphere_radius)[0]
    cmds.setAttr(f'{reference_sphere}.overrideEnabled', 1)
    cmds.setAttr(f'{reference_sphere}.overrideColor', 18)  # 灰色
    cmds.setAttr(f'{reference_sphere}.overrideShading', 0)
    cmds.setAttr(f'{reference_sphere}.visibility', 1)
    cmds.parent(reference_sphere, sphere_group)

    # 9. 创建2D凸包可视化（在平面上）
    create_2d_convex_hull_visualization(points_2d, hull, sphere_group)

    # 居中视图
    cmds.viewFit(all=True)

    print("基于凸包边界的球面三角剖分创建完成！")
    return sphere_group


def create_2d_convex_hull_visualization(points_2d, hull, parent_group):
    """
    创建2D凸包和三角剖分的可视化
    """
    # 缩放因子，将2D点映射到3D空间
    scale = 8
    offset_x = -15  # 在X轴负方向放置2D可视化

    # 创建2D点
    for i, point in enumerate(points_2d):
        locator = cmds.spaceLocator(name=f'point_2d_{i}')[0]
        cmds.setAttr(f'{locator}.translateX', point[0] * scale + offset_x)
        cmds.setAttr(f'{locator}.translateY', point[1] * scale)
        cmds.setAttr(f'{locator}.translateZ', 0)
        cmds.setAttr(f'{locator}.localScaleX', 0.15)
        cmds.setAttr(f'{locator}.localScaleY', 0.15)
        cmds.setAttr(f'{locator}.localScaleZ', 0.15)

        # 设置颜色：凸包边界点为绿色，内部点为红色
        if i in hull.vertices:
            cmds.setAttr(f'{locator}.overrideColor', 14)  # 绿色
        else:
            cmds.setAttr(f'{locator}.overrideColor', 13)  # 红色

        cmds.parent(locator, parent_group)

    # 创建2D凸包边界线
    hull_points_2d = []
    for vertex_idx in hull.vertices:
        point = points_2d[vertex_idx]
        hull_points_2d.append([point[0] * scale + offset_x, point[1] * scale, 0])

    # 闭合曲线
    hull_points_2d.append(hull_points_2d[0])

    hull_curve_2d = cmds.curve(
        name='convex_hull_2d',
        p=hull_points_2d,
        d=1
    )
    cmds.setAttr(f'{hull_curve_2d}.lineWidth', 2)
    cmds.setAttr(f'{hull_curve_2d}.overrideColor', 17)  # 黄色
    cmds.parent(hull_curve_2d, parent_group)

    # 创建2D三角剖分可视化
    for i, triangle in enumerate(hull._simplices):
        # 获取三角形的三个2D顶点
        v0 = points_2d[triangle[0]]
        v1 = points_2d[triangle[1]]
        v2 = points_2d[triangle[2]]

        # 转换为3D坐标（添加X轴偏移）
        v0_3d = [v0[0] * scale + offset_x, v0[1] * scale, 0]
        v1_3d = [v1[0] * scale + offset_x, v1[1] * scale, 0]
        v2_3d = [v2[0] * scale + offset_x, v2[1] * scale, 0]

        # 创建多边形面片
        mesh_2d = cmds.polyCreateFacet(
            name=f'triangle_2d_{i:02d}',
            p=[v0_3d, v1_3d, v2_3d]
        )[0]

        # 设置半透明材质
        shader_2d = cmds.shadingNode('lambert', asShader=True, name=f'triangle_2d_shader_{i}')
        cmds.setAttr(f'{shader_2d}.color', 0.8, 0.8, 0.8, type='double3')
        cmds.setAttr(f'{shader_2d}.transparency', 0.7, 0.7, 0.7, type='double3')

        shading_group_2d = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
                                     name=f"{shader_2d}SG")
        cmds.connectAttr(f'{shader_2d}.outColor', f'{shader_2d}SG.surfaceShader')
        cmds.sets(mesh_2d, edit=True, forceElement=shader_2d)

        cmds.parent(mesh_2d, parent_group)

    # 添加标签
    text = cmds.textCurves(
        text="2D凸包与三角剖分",
        font="Arial",
        name="2d_visualization_label"
    )[0]
    cmds.setAttr(f'{text}.translateX', offset_x + 4)
    cmds.setAttr(f'{text}.translateY', 9)
    cmds.setAttr(f'{text}.translateZ', 0)
    cmds.setAttr(f'{text}.scaleX', 0.5)
    cmds.setAttr(f'{text}.scaleY', 0.5)
    cmds.setAttr(f'{text}.scaleZ', 0.5)
    cmds.parent(text, parent_group)

    text2 = cmds.textCurves(
        text="3D球面映射",
        font="Arial",
        name="3d_visualization_label"
    )[0]
    cmds.setAttr(f'{text2}.translateX', 0)
    cmds.setAttr(f'{text2}.translateY', 9)
    cmds.setAttr(f'{text2}.translateZ', 0)
    cmds.setAttr(f'{text2}.scaleX', 0.5)
    cmds.setAttr(f'{text2}.scaleY', 0.5)
    cmds.setAttr(f'{text2}.scaleZ', 0.5)
    cmds.parent(text2, parent_group)


# 执行函数
if __name__ == "__main__":
    # 创建基于凸包边界的球面三角剖分
    sphere_group = create_convex_hull_spherical_triangulation(
        num_points=100,  # 随机点数量
        sphere_radius=1.0  # 球体半径
    )

    print("=" * 60)
    print("基于凸包边界的球面三角剖分已完成！")
    print("特点：")
    print("- 使用随机点自动计算凸包边界")
    print("- 三角剖分仅限于凸包内部区域")
    print("- 自动将2D三角剖分映射到3D球面")
    print("- 绿色点：凸包边界点")
    print("- 红色点：内部点")
    print("- 左侧：2D凸包和三角剖分可视化")
    print("- 右侧：3D球面映射结果")
    print("=" * 60)