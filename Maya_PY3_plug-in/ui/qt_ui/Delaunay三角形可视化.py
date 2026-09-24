import matplotlib

matplotlib.use('Agg')  # 必须在导入pyplot之前设置
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
import maya.cmds as cmds
import os

# 设置随机种子
np.random.seed(42)

# 创建点集：4个固定角点 + 10个随机点
fixed_points = np.array([
    [0.0, 0.0],  # 左下角
    [0.0, 1.0],  # 左上角
    [1.0, 0.0],  # 右下角
    [1.0, 1.0]  # 右上角
])

# 生成10个随机点
num_random_points = 100
random_points = np.random.rand(num_random_points, 2)

# 合并所有点
all_points = np.vstack([fixed_points, random_points])

# 执行Delaunay三角剖分
tri = Delaunay(all_points)

# 创建可视化图形
plt.figure(figsize=(10, 8))

# 绘制三角形
plt.triplot(all_points[:, 0], all_points[:, 1], tri.simplices,
            color='blue', linewidth=1.5, alpha=0.7)

# 绘制点，用不同颜色区分固定点和随机点
# 固定点（角点）
plt.plot(fixed_points[:, 0], fixed_points[:, 1], 's',
         markersize=10, color='green', markeredgecolor='black',
         markeredgewidth=1, label='固定点')

# 随机点
plt.plot(random_points[:, 0], random_points[:, 1], 'o',
         markersize=8, color='red', markeredgecolor='black',
         markeredgewidth=0.5, label='随机点')

# 添加点标签
for i, point in enumerate(all_points):
    if i < 4:  # 固定点
        plt.text(point[0] + 0.02, point[1] + 0.02, f'F{i + 1}',
                 fontsize=10, ha='left', va='bottom', color='green', weight='bold')
    else:  # 随机点
        plt.text(point[0] + 0.02, point[1] + 0.02, f'R{i - 3}',
                 fontsize=9, ha='left', va='bottom', color='red')

plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
plt.gca().set_aspect('equal')
plt.grid(True, alpha=0.3)
plt.title('带固定角点的Delaunay三角剖分 (1x1平面)', fontsize=14)
plt.xlabel('X坐标')
plt.ylabel('Y坐标')
plt.legend()

# 添加统计信息
num_triangles = len(tri.simplices)
info_text = f'总点数: {len(all_points)}\n固定点: 4个\n随机点: {num_random_points}个\n三角形数: {num_triangles}个'
plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
         verticalalignment='top', fontsize=10)

# 保存图像
temp_image = os.path.join(os.path.expanduser('~'), 'delaunay_with_fixed_points.png')
plt.savefig(temp_image, dpi=150, bbox_inches='tight')
plt.close()

print("=" * 60)
print("带固定点的Delaunay三角剖分结果")
print("=" * 60)
print(f"固定角点坐标:")
for i, point in enumerate(fixed_points):
    print(f"  点F{i + 1}: ({point[0]}, {point[1]})")

print(f"\n随机点坐标:")
for i, point in enumerate(random_points, 1):
    print(f"  点R{i}: ({point[0]:.3f}, {point[1]:.3f})")

print(f"\n生成的三角形 ({num_triangles}个):")
for i, triangle in enumerate(tri.simplices):
    # 将索引转换为点标签
    labels = []
    for idx in triangle:
        if idx < 4:  # 固定点
            labels.append(f'F{idx + 1}')
        else:  # 随机点
            labels.append(f'R{idx - 3}')

    print(f"  三角形{i + 1}: {labels[0]}-{labels[1]}-{labels[2]}")

# 在Maya中显示结果
if cmds.window('delaunayWindow', exists=True):
    cmds.deleteUI('delaunayWindow')

cmds.window('delaunayWindow', title='带固定点的Delaunay三角剖分', width=600, height=500)
cmds.paneLayout()
cmds.image(image=temp_image)
cmds.showWindow('delaunayWindow')

print(f"\n图像已保存: {temp_image}")
print("结果已在Maya中显示！")