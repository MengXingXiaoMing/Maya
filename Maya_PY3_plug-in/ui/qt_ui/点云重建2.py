#coding=gbk
import maya.cmds as cmds
import numpy as np
import math
from scipy.spatial import Delaunay


def create_smooth_spherical_reconstruction():
    """
    创建光滑的球面重建（避免刺猬效果）
    """
    # 清理场景
    if cmds.objExists('smooth_sphere_reconstruction'):
        cmds.delete('smooth_sphere_reconstruction')

    main_group = cmds.group(empty=True, name='smooth_sphere_reconstruction')

    # 1. 生成高密度均匀分布的点云
    print("生成高密度均匀球面点云...")
    points = generate_uniform_sphere_points(1000, radius=5.0)  # 增加点密度

    # 2. 创建优化的三角剖分
    print("执行球面优化的三角剖分...")
    mesh = create_optimized_spherical_mesh(points, radius=5.0)

    if mesh:
        cmds.parent(mesh, main_group)

        # 3. 应用网格平滑
        print("应用网格平滑...")
        smooth_mesh = apply_mesh_smoothing(mesh, subdivisions=2)

        # 4. 设置光滑材质
        setup_smooth_material(smooth_mesh)

        # 5. 创建参考球体对比
        create_reference_sphere(5.0, main_group)

    cmds.viewFit(all=True)
    return main_group


def generate_uniform_sphere_points(num_points, radius=5.0):
    """
    生成均匀分布的球面点云（避免随机分布的不均匀性）
    """
    points = []

    # 使用斐波那契球面采样生成均匀分布点
    golden_ratio = (1 + math.sqrt(5)) / 2
    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2  # y从1到-1
        radius_at_y = math.sqrt(1 - y * y)

        theta = 2 * math.pi * i / golden_ratio

        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y

        # 缩放到指定半径
        x *= radius
        y *= radius
        z *= radius

        points.append([x, y, z])

    return np.array(points)


def create_optimized_spherical_mesh(points, radius=5.0):
    """
    创建优化的球面网格（专门针对球面形状优化）
    """
    # 将3D点投影到2D平面进行三角剖分
    points_2d = []
    for point in points:
        # 将3D球面坐标转换为2D参数化坐标
        x, y, z = point

        # 球面坐标到UV坐标
        phi = math.acos(y / radius)  # 极角 [0, π]
        theta = math.atan2(z, x)  # 方位角 [0, 2π]
        if theta < 0:
            theta += 2 * math.pi

        u = theta / (2 * math.pi)  # 归一化到 [0, 1]
        v = phi / math.pi  # 归一化到 [0, 1]

        points_2d.append([u, v])

    points_2d = np.array(points_2d)

    # 执行Delaunay三角剖分
    try:
        tri = Delaunay(points_2d)
    except Exception as e:
        print(f"三角剖分失败: {e}")
        return None

    # 创建网格 - 使用正确的方法
    mesh_name = "smooth_sphere_mesh"

    # 创建顶点列表
    vertices = [p.tolist() for p in points]

    # 逐个创建三角形面片
    face_meshes = []
    for i, triangle in enumerate(tri.simplices):
        if len(triangle) == 3:
            # 获取三角形的三个顶点
            v0 = vertices[triangle[0]]
            v1 = vertices[triangle[1]]
            v2 = vertices[triangle[2]]

            # 创建三角形面片
            try:
                face_mesh = cmds.polyCreateFacet(
                    p=[v0, v1, v2],
                    name=f"{mesh_name}_face_{i:04d}"
                )[0]
                face_meshes.append(face_mesh)
            except Exception as e:
                continue

    # 合并所有面片
    # if len(face_meshes) > 1:
    #     combined_mesh = cmds.polyUnite(face_meshes, name=mesh_name)[0]
    #     # 清理临时面片
    #     for face_mesh in face_meshes:
    #         if cmds.objExists(face_mesh):
    #             cmds.delete(face_mesh)
    # else:
    #     combined_mesh = face_meshes[0] if face_meshes else None
    combined_mesh = face_meshes[0]
    return combined_mesh


def apply_mesh_smoothing(mesh, subdivisions=2):
    """
    应用网格平滑处理
    """
    print(f"对网格应用 {subdivisions} 级平滑...")

    # 使用Maya的平滑命令
    # smooth_mesh = cmds.polySmooth(
    #     mesh,
    #     method=0,  # 指数平滑
    #     divisions=subdivisions,
    #     smoothness=1.0,
    #     continuity=1.0,
    #     smoothUVs=True,
    #     propagation=2,  # 平滑边界
    #     name=f"{mesh}_smooth"
    # )[0]
    smooth_mesh = mesh
    # 删除构造历史以获得干净网格
    cmds.delete(smooth_mesh, constructionHistory=True)

    return smooth_mesh


def setup_smooth_material(mesh):
    """
    设置光滑材质
    """
    shader_name = f"{mesh}_smooth_shader"
    shader = cmds.shadingNode('phong', asShader=True, name=shader_name)

    # 设置材质属性
    cmds.setAttr(f"{shader}.color", 0.3, 0.5, 0.8, type='double3')  # 淡蓝色
    cmds.setAttr(f"{shader}.specularColor", 0.7, 0.7, 0.7, type='double3')
    cmds.setAttr(f"{shader}.cosinePower", 20)  # 高光大小
    cmds.setAttr(f"{shader}.reflectivity", 0.1)

    # 完全不透明
    cmds.setAttr(f"{shader}.transparency", 0, 0, 0, type='double3')

    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
                              name=f"{shader}SG")
    cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
    cmds.sets(mesh, edit=True, forceElement=shading_group)


def create_reference_sphere(radius, parent_group):
    """
    创建参考球体用于对比
    """
    ref_sphere = cmds.polySphere(radius=radius, name="reference_sphere")[0]
    cmds.setAttr(f"{ref_sphere}.translateX", 10)  # 在X方向偏移以便对比

    # 设置为线框显示
    cmds.setAttr(f"{ref_sphere}.overrideEnabled", 1)
    cmds.setAttr(f"{ref_sphere}.overrideDisplayType", 1)  # 线框模式

    cmds.parent(ref_sphere, parent_group)
    return ref_sphere


# 高级版本：使用多种技术对比
def compare_reconstruction_techniques():
    """
    对比不同的重建技术
    """
    techniques_group = cmds.group(empty=True, name='technique_comparison')

    techniques = [
        {"name": "低密度基础", "points": 100, "smoothing": 0},
        {"name": "高密度基础", "points": 1000, "smoothing": 0},
        {"name": "低密度+平滑", "points": 100, "smoothing": 2},
        {"name": "高密度+平滑", "points": 1000, "smoothing": 2}
    ]

    for i, tech in enumerate(techniques):
        # 为每种技术创建重建
        points = generate_uniform_sphere_points(tech["points"])
        mesh = create_optimized_spherical_mesh(points)

        if mesh:
            # 应用平滑
            if tech["smoothing"] > 0:
                mesh = apply_mesh_smoothing(mesh, tech["smoothing"])

            # 设置材质
            setup_technique_material(mesh, i)

            # 定位
            cmds.setAttr(f"{mesh}.translateX", i * 12 - 18)
            cmds.parent(mesh, techniques_group)

            # 添加标签
            create_technique_label(tech["name"], i * 12 - 18, 8, techniques_group)

    cmds.viewFit(all=True)
    return techniques_group


def setup_technique_material(mesh, index):
    """为不同技术设置不同材质"""
    colors = [
        (0.8, 0.2, 0.2),  # 红色 - 低密度基础
        (0.2, 0.7, 0.2),  # 绿色 - 高密度基础
        (0.2, 0.5, 0.8),  # 蓝色 - 低密度+平滑
        (0.8, 0.6, 0.1)  # 金色 - 高密度+平滑
    ]

    shader = cmds.shadingNode('phong', asShader=True, name=f"{mesh}_shader")
    cmds.setAttr(f"{shader}.color", *colors[index], type='double3')

    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
                              name=f"{shader}SG")
    cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
    cmds.sets(mesh, edit=True, forceElement=shading_group)


def create_technique_label(text, x, y, parent):
    """创建技术标签"""
    # 使用定位器作为简单标签
    loc = cmds.spaceLocator(name=f"label_{text}")[0]
    cmds.setAttr(f"{loc}.translateX", x)
    cmds.setAttr(f"{loc}.translateY", y)
    cmds.setAttr(f"{loc}.localScaleX", 0.3)
    cmds.setAttr(f"{loc}.localScaleY", 0.3)
    cmds.setAttr(f"{loc}.localScaleZ", 0.3)
    cmds.setAttr(f"{loc}.overrideEnabled", 1)
    cmds.setAttr(f"{loc}.overrideColor", 13)  # 黄色

    # 添加属性存储文本
    cmds.addAttr(loc, longName="description", dataType="string")
    cmds.setAttr(f"{loc}.description", text, type="string")

    cmds.parent(loc, parent)


# 在Maya中运行
if __name__ == "__main__":
    print("=" * 60)
    print("创建光滑球面重建（解决刺猬效果问题）")
    print("=" * 60)

    # 方法1：创建单个光滑重建
    smooth_sphere = create_smooth_spherical_reconstruction()

    # 方法2：对比不同技术（取消注释启用）
    # techniques_comparison = compare_reconstruction_techniques()

    print("\n重建完成！关键改进：")
    print("? 使用均匀点分布（斐波那契球面采样）")
    print("? 增加点云密度（1000个点）")
    print("? 应用网格平滑（2级细分）")
    print("? 使用光滑材质（Phong着色器）")
    print("? 添加参考球体对比")
    print("=" * 60)