#coding=gbk
import maya.cmds as cmds
import numpy as np
from scipy.spatial import Delaunay

# 清理场景
if cmds.objExists('delaunay_with_fixed_points'):
    cmds.delete('delaunay_with_fixed_points')

# 创建组
delaunay_group = cmds.group(empty=True, name='delaunay_with_fixed_points')

# 定义点集（固定点 + 随机点）
fixed_points = np.array([
    [0.0, 0.0, 0.0],  # 左下角
    [0.0, 1.0, 0.0],  # 左上角（放大到10倍便于查看）
    [1.0, 0.0, 0.0],  # 右下角
    [1.0, 1.0, 0.0]  # 右上角
])

# 生成随机点（放大到10倍）
np.random.seed(42)
num_random_points = 100
random_points = np.random.rand(num_random_points, 2) * 1
random_points_3d = np.column_stack([random_points, np.zeros(num_random_points)])

# 合并所有点
all_points = np.vstack([fixed_points, random_points_3d])
all_points = random_points_3d
# Delaunay三角剖分（只使用x,y坐标）
tri = Delaunay(all_points[:, :2])

# 创建定位器表示点
for i, point in enumerate(all_points):
    if i < 4:  # 固定点
        locator = cmds.spaceLocator(name=f'fixed_point_{i + 1}')[0]
        cmds.setAttr(f'{locator}.overrideColor', 13)  # 绿色
    else:  # 随机点
        locator = cmds.spaceLocator(name=f'random_point_{i - 3}')[0]
        cmds.setAttr(f'{locator}.overrideColor', 13)  # 红色

    cmds.setAttr(f'{locator}.translateX', point[0])
    cmds.setAttr(f'{locator}.translateY', point[1])
    cmds.setAttr(f'{locator}.translateZ', point[2])
    cmds.setAttr(f'{locator}.localScaleX', 0.3)
    cmds.setAttr(f'{locator}.localScaleY', 0.3)
    cmds.setAttr(f'{locator}.localScaleZ', 0.3)
    cmds.parent(locator, delaunay_group)

# 创建三角形网格
for i, triangle in enumerate(tri.simplices):
    # 获取三个顶点的坐标
    vertices = [all_points[idx] for idx in triangle]

    # 创建多边形面片
    mesh = cmds.polyCreateFacet(
        name=f'triangle_{i + 1}',
        p=[(v[0], v[1], v[2]) for v in vertices]
    )[0]

    # 设置材质
    shader = cmds.shadingNode('lambert', asShader=True, name=f'triangle_shader_{i + 1}')

    # 为不同三角形设置不同颜色
    hue = (i * 0.618) % 1.0  # 使用黄金比例分布颜色
    # rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.8)
    # cmds.setAttr(f'{shader}.color', rgb[0], rgb[1], rgb[2], type='double3')

    cmds.select(mesh)
    cmds.hyperShade(assign=shader)

    # 使三角形半透明
    cmds.setAttr(f'{shader}.transparency', 0.3, 0.3, 0.3, type='double3')

    cmds.parent(mesh, delaunay_group)

# 创建边界线
boundary_lines = [
    [0, 1],  # 左边界
    [1, 3],  # 上边界
    [3, 2],  # 右边界
    [2, 0]  # 下边界
]

for i, line in enumerate(boundary_lines):
    curve = cmds.curve(
        name=f'boundary_{i + 1}',
        p=[all_points[line[0]].tolist(), all_points[line[1]].tolist()],
        d=1
    )
    cmds.setAttr(f'{curve}.lineWidth', 2)
    cmds.setAttr(f'{curve}.overrideColor', 17)  # 黄色
    cmds.parent(curve, delaunay_group)

# 居中视图
cmds.viewFit(all=True)

print("=" * 60)
print("Maya 3D三角网创建完成！")
print(f"固定点: 4个（绿色定位器）")
print(f"随机点: {num_random_points}个（红色定位器）")
print(f"三角形: {len(tri.simplices)}个（彩色半透明面片）")
print("=" * 60)