#coding=gbk
import maya.cmds as cmds
import numpy as np
from scipy.spatial import Delaunay


def create_spherical_triangulation():
    """
    在球面上创建基于Delaunay三角剖分的三维网格
    """
    # 清理场景
    if cmds.objExists('spherical_triangulation_group'):
        cmds.delete('spherical_triangulation_group')

    # 创建组来组织所有几何体
    sphere_group = cmds.group(empty=True, name='spherical_triangulation_group')

    # 1. 在1x1平面内生成点集（包含4个固定角点）
    fixed_points = np.array([
        [0.0, 0.0],  # 左下角
        [0.0, 1.0],  # 左上角
        [1.0, 0.0],  # 右下角
        [1.0, 1.0]  # 右上角
    ])
    # 生成随机点
    np.random.seed(42)
    num_random_points = 100
    random_points = np.random.rand(num_random_points, 2)

    # 合并所有点
    all_points_2d = np.vstack([fixed_points, random_points])
    all_points_2d = random_points
    # 2. 执行Delaunay三角剖分
    tri = Delaunay(all_points_2d)

    print(f"生成 {len(all_points_2d)} 个点，{len(tri.simplices)} 个三角形")

    # 3. 将2D点映射到球面
    sphere_radius = 1.0
    all_points_3d = []

    for point_2d in all_points_2d:
        # 将2D坐标转换为球面坐标
        u, v = point_2d

        # 将UV坐标转换为球面坐标
        theta = u * 2 * np.pi  # 经度 [0, 2π]
        phi = v * np.pi  # 纬度 [0, π]

        # 球面坐标转笛卡尔坐标
        x = sphere_radius * np.sin(phi) * np.cos(theta)
        y = sphere_radius * np.cos(phi)  # 让Y轴向上
        z = sphere_radius * np.sin(phi) * np.sin(theta)

        all_points_3d.append([x, y, z])

    all_points_3d = np.array(all_points_3d)

    # 4. 在Maya中创建球面三角形网格
    for i, triangle in enumerate(tri.simplices):
        # 获取三角形的三个3D顶点
        v0 = all_points_3d[triangle[0]]
        v1 = all_points_3d[triangle[1]]
        v2 = all_points_3d[triangle[2]]

        # 创建多边形面片
        mesh_name = f"spherical_triangle_{i:02d}"
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

    # 5. 创建球面顶点标记
    for i, point in enumerate(all_points_3d):
        if i < 4:  # 固定点
            locator = cmds.spaceLocator(name=f'fixed_point_{i + 1}')[0]
            cmds.setAttr(f'{locator}.overrideColor', 13)  # 绿色
        else:  # 随机点
            locator = cmds.spaceLocator(name=f'random_point_{i - 3}')[0]
            cmds.setAttr(f'{locator}.overrideColor', 13)  # 红色

        cmds.setAttr(f'{locator}.translateX', point[0])
        cmds.setAttr(f'{locator}.translateY', point[1])
        cmds.setAttr(f'{locator}.translateZ', point[2])
        cmds.setAttr(f'{locator}.localScaleX', 0.2)
        cmds.setAttr(f'{locator}.localScaleY', 0.2)
        cmds.setAttr(f'{locator}.localScaleZ', 0.2)

        cmds.parent(locator, sphere_group)

    # 6. 创建参考球体
    reference_sphere = cmds.polySphere(name='reference_sphere', radius=sphere_radius)[0]
    cmds.setAttr(f'{reference_sphere}.overrideEnabled', 1)
    cmds.setAttr(f'{reference_sphere}.overrideColor', 18)  # 灰色
    cmds.setAttr(f'{reference_sphere}.overrideShading', 0)
    cmds.setAttr(f'{reference_sphere}.visibility', 1)
    cmds.parent(reference_sphere, sphere_group)

    # 居中视图
    cmds.viewFit(all=True)

    print("球面三角剖分创建完成！")
    return sphere_group


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


def visualize_uv_mapping():
    """
    可视化UV映射过程：显示2D平面和3D球面的对应关系
    """
    # 创建可视化组
    if cmds.objExists('uv_mapping_visualization'):
        cmds.delete('uv_mapping_visualization')

    viz_group = cmds.group(empty=True, name='uv_mapping_visualization')

    # 创建2D平面表示UV空间
    plane = cmds.polyPlane(name='uv_plane', width=1, height=1)[0]
    cmds.setAttr(f'{plane}.translateY', 8)
    cmds.setAttr(f'{plane}.overrideEnabled', 1)
    cmds.setAttr(f'{plane}.overrideColor', 20)  # 浅蓝色

    # 在平面上创建棋盘格纹理显示UV分布
    shader = cmds.shadingNode('checker', asTexture=True, name='uv_checker')
    place2d = cmds.shadingNode('place2dTexture', asUtility=True)

    cmds.connectAttr(f'{place2d}.outU', f'{shader}.uvCoordU')
    cmds.connectAttr(f'{place2d}.outV', f'{shader}.uvCoordV')
    cmds.setAttr(f'{shader}.color1', 1, 1, 1, type='double3')  # 白色
    cmds.setAttr(f'{shader}.color2', 0.7, 0.7, 0.7, type='double3')  # 灰色

    cmds.parent(plane, viz_group)

    print("UV映射可视化已创建")
    return viz_group


# 执行主函数
if __name__ == "__main__":
    # 创建球面三角剖分
    spherical_mesh = create_spherical_triangulation()

    # 创建UV映射可视化
    # uv_viz = visualize_uv_mapping()

    # 将两者组合
    main_group = cmds.group(empty=True, name='spherical_triangulation_complete')
    cmds.parent(spherical_mesh, main_group)
    # cmds.parent(uv_viz, main_group)

    print("=" * 60)
    print("球面三角剖分已完成！")
    print("包含：")
    print("- 基于Delaunay三角剖分的球面网格")
    print("- UV映射可视化（上方的平面）")
    print("- 彩色半透明三角形面片")
    print("- 顶点定位器（绿色：固定点，红色：随机点）")
    print("=" * 60)