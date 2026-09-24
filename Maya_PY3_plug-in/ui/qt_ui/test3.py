#coding=gbk
import maya.mel as mel
import maya.cmds as cmds
import math
from scipy.interpolate import Rbf
def rbf_test():
    sour_x = cmds.getAttr('pCube1.tx')
    sour_y = cmds.getAttr('pCube1.ty')
    sour_z = cmds.getAttr('pCube1.tz')

    tag_a_x = cmds.getAttr('pCube2.tx')
    tag_a_y = cmds.getAttr('pCube2.ty')
    tag_a_z = cmds.getAttr('pCube2.tz')

    tag_b_x = cmds.getAttr('pCube3.tx')
    tag_b_y = cmds.getAttr('pCube3.ty')
    tag_b_z = cmds.getAttr('pCube3.tz')

    tag_c_x = cmds.getAttr('pCube4.tx')
    tag_c_y = cmds.getAttr('pCube4.ty')
    tag_c_z = cmds.getAttr('pCube4.tz')

    tag_d_x = cmds.getAttr('pCube5.tx')
    tag_d_y = cmds.getAttr('pCube5.ty')
    tag_d_z = cmds.getAttr('pCube5.tz')

    # 计算欧式几何距离
    a_jl = math.sqrt((sour_x-tag_a_x)**2+(sour_y-tag_a_y)**2+(sour_z-tag_a_z)**2)
    b_jl = math.sqrt((sour_x-tag_b_x)**2+(sour_y-tag_b_y)**2+(sour_z-tag_b_z)**2)
    c_jl = math.sqrt((sour_x-tag_c_x)**2+(sour_y-tag_c_y)**2+(sour_z-tag_c_z)**2)
    d_jl = math.sqrt((sour_x-tag_d_x)**2+(sour_y-tag_d_y)**2+(sour_z-tag_d_z)**2)

    # 使用高斯核函数（σ=1.0）
    index=1.0
    a_weight = math.exp(-1*(pow(a_jl, 2)/(2 * pow(index, 2))))
    b_weight = math.exp(-1*(pow(b_jl, 2)/(2 * pow(index, 2))))
    c_weight = math.exp(-1*(pow(c_jl, 2)/(2 * pow(index, 2))))
    d_weight = math.exp(-1*(pow(d_jl, 2)/(2 * pow(index, 2))))

    weight_list = [a_weight, b_weight, c_weight, d_weight]
    print(weight_list)
    # 降序排序后取前3个元素
    # lst = [10, 5, 20, 15, 30, 25]

    # 生成带索引的元组并按值降序排序
    sorted_with_indices = sorted(enumerate(weight_list), key=lambda x: x[1], reverse=True)
    # print(sorted_with_indices)
    # 取前3个元素
    top3 = sorted_with_indices[:3]
    # 提取索引和值
    indices = [index for index, value in top3]
    values = [value for index, value in top3]
    # print(indices, values)

    # 权重归一化
    weight_add = sum(values)
    weight1 = values[0]/weight_add
    weight2 = values[1]/weight_add
    weight3 = values[2]/weight_add
    out_weight = [weight1, weight2, weight3]
    # 输出混合结果
    an_list = ['blendShape1.pCube2','blendShape1.pCube3','blendShape1.pCube4','blendShape1.pCube5']
    for an in an_list:
        cmds.setAttr(an, 0)
    for date in zip(indices,out_weight):
        cmds.setAttr(an_list[date[0]],date[1])


# cmds.scriptJob(kill=617, force=True)

def rbf_test():
    sour_x = cmds.getAttr('pCube1.tx')
    sour_y = cmds.getAttr('pCube1.ty')
    sour_z = cmds.getAttr('pCube1.tz')

    tag_a_x = cmds.getAttr('pCube2.tx')
    tag_a_y = cmds.getAttr('pCube2.ty')
    tag_a_z = cmds.getAttr('pCube2.tz')

    tag_b_x = cmds.getAttr('pCube3.tx')
    tag_b_y = cmds.getAttr('pCube3.ty')
    tag_b_z = cmds.getAttr('pCube3.tz')

    tag_c_x = cmds.getAttr('pCube4.tx')
    tag_c_y = cmds.getAttr('pCube4.ty')
    tag_c_z = cmds.getAttr('pCube4.tz')

    tag_d_x = cmds.getAttr('pCube5.tx')
    tag_d_y = cmds.getAttr('pCube5.ty')
    tag_d_z = cmds.getAttr('pCube5.tz')

    # 计算欧式几何距离
    a_jl = math.sqrt((sour_x-tag_a_x)**2+(sour_y-tag_a_y)**2+(sour_z-tag_a_z)**2)
    b_jl = math.sqrt((sour_x-tag_b_x)**2+(sour_y-tag_b_y)**2+(sour_z-tag_b_z)**2)
    c_jl = math.sqrt((sour_x-tag_c_x)**2+(sour_y-tag_c_y)**2+(sour_z-tag_c_z)**2)
    d_jl = math.sqrt((sour_x-tag_d_x)**2+(sour_y-tag_d_y)**2+(sour_z-tag_d_z)**2)

    # 使用高斯核函数（σ=1.0）
    index=2.0
    a_weight = math.exp(-(pow(a_jl, 2)/(2 * pow(index, 2))))
    b_weight = math.exp(-(pow(b_jl, 2)/(2 * pow(index, 2))))
    c_weight = math.exp(-(pow(c_jl, 2)/(2 * pow(index, 2))))
    d_weight = math.exp(-(pow(d_jl, 2)/(2 * pow(index, 2))))

    weight_list = [a_weight, b_weight, c_weight, d_weight]
    print(weight_list)

    # 权重归一化
    weight_add = sum(weight_list)
    weight1 = weight_list[0] / weight_add
    weight2 = weight_list[1] / weight_add
    weight3 = weight_list[2] / weight_add
    weight4 = weight_list[3] / weight_add
    out_weight = [weight1, weight2, weight3, weight4]
    # 输出混合结果
    an_list = ['blendShape1.pCube2','blendShape1.pCube3','blendShape1.pCube4','blendShape1.pCube5']
    for date in zip(an_list,out_weight):
        cmds.setAttr(date[0],date[1])

# job_number = cmds.scriptJob(
#             attributeChange=('pCube1.translate', rbf_test),
#             protected=True
#         )

# 获取相邻的点
def get_connected_vertices(vertex):
    """
    获取某个顶点直接相连的所有相邻顶点
    :param vertex: 顶点名称（例如 "pCube1.vtx[0]"）
    :return: 相邻顶点列表
    """
    # 将顶点转换为连接的边
    connected_edges = cmds.polyListComponentConversion(vertex, fromVertex=True, toEdge=True)
    connected_edges = cmds.ls(connected_edges, flatten=True)

    # 将边转换为顶点（包括原始顶点和相邻顶点）
    connected_vertices = cmds.polyListComponentConversion(connected_edges, fromEdge=True, toVertex=True)
    connected_vertices = cmds.ls(connected_vertices, flatten=True)

    # 排除原始顶点
    adjacent_vertices = [vtx for vtx in connected_vertices if vtx != vertex]
    adjacent_vertices_point = []
    for obj in adjacent_vertices:
        t = cmds.xform(obj, q=1, t=1)
        adjacent_vertices_point.append(t)
    return adjacent_vertices_point
# 平滑
def smooth_3d_points2(points, radius=1.0, sigma=0.5, sel=''):
    smoothed = []
    n = len(points)
    for i in range(n):
        x, y, z = points[i]
        total_weight = 0.0
        # sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
        next_point = get_connected_vertices(sel[i])
        # ===== 1. 计算点集中心 =====
        n = len(next_point)
        sum_x = sum(p[0] for p in next_point)
        sum_y = sum(p[1] for p in next_point)
        sum_z = sum(p[2] for p in next_point)
        center = [sum_x / n, sum_y / n, sum_z / n]
        # 计算三维欧氏距离
        dx = x - center[0]
        dy = y - center[1]
        dz = z - center[2]
        distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        # if distance <= radius:
        # # 计算高斯权重
        # weight = math.exp(-(distance / sigma) ** 2)
        weight = distance / radius
        # weight = weight - 0.1
        # if weight < 0:
        #     weight = 1
        sum_x = weight * dx + center[0]
        sum_y = weight * dy + center[1]
        sum_z = weight * dz + center[2]
        print(sel[i])
        print(weight)
        print(center)
        # weight = 1 - distance / radius
        # total_weight += weight
        # # 加权平均计算新坐标
        # if total_weight > 0:
        #     new_x = sum_x / total_weight
        #     new_y = sum_y / total_weight
        #     new_z = sum_z / total_weight
        # else:
        #     new_x, new_y, new_z = x, y, z  # 无邻域时保持原值
        #     # new_x = sum_x / total_weight * 0.01
        #     # new_y = sum_y / total_weight * 0.01
        #     # new_z = sum_z / total_weight * 0.01
        smoothed.append([sum_x, sum_y, sum_z])

    return smoothed
# 示例输入数据（可替换为您的实际数据）
# sel = cmds.ls(sl=1, fl=1)
# original_points = []
# for obj in sel:
#     t = cmds.xform(obj, q=1, t=1)
#     original_points.append(t)
# # t = cmds.xform('pPlane1.vtx[83]', q=1, t=1)
# # print(t)
# # 执行平滑
# smoothed_points2 = smooth_3d_points2(
#     points=original_points,
#     radius=2.5,  # 控制邻域范围
#     sigma=1.5,  # 控制平滑强度（值越小越局部）
#     sel=sel
# )
# for obj,num in zip(sel,smoothed_points2):
#     cmds.xform(obj, t=num)





def smooth_3d_points(points, radius=1.0, sigma=0.5, sel=''):
    print(radius,sigma)
    """
    直接对三维点列表进行RBF平滑
    参数:
        points : 原始点列表 [[x1,y1,z1], [x2,y2,z2], ...]
        radius : 邻域搜索半径
        sigma  : 高斯核参数（控制平滑强度）
    返回:
        平滑后的新点列表 [[x1_new,y1_new,z1_new], ...]
    """
    smoothed = []
    n = len(points)

    for i in range(n):
        x, y, z = points[i]
        total_weight = 0.0
        sum_x, sum_y, sum_z = 0.0, 0.0, 0.0

        # 遍历所有点寻找邻域
        for j in range(n):
            # 计算三维欧氏距离
            dx = x - points[j][0]
            dy = y - points[j][1]
            dz = z - points[j][2]
            distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

            if distance <= radius:
                # 计算高斯权重
                weight = math.exp(-(distance / sigma) ** 2)
                # weight = 1 - distance / radius
                total_weight += weight
                sum_x += weight * points[j][0]
                sum_y += weight * points[j][1]
                sum_z += weight * points[j][2]
        # print(sel[i])
        # print(weight)
        # 加权平均计算新坐标
        if total_weight > 0:
            new_x = sum_x / total_weight
            new_y = sum_y / total_weight
            new_z = sum_z / total_weight
        else:
            # new_x, new_y, new_z = x, y, z  # 无邻域时保持原值
            new_x = sum_x / total_weight*0.01
            new_y = sum_y / total_weight*0.01
            new_z = sum_z / total_weight*0.01


        smoothed.append([new_x, new_y, new_z])

    # print(smoothed)
    # points = smoothed
    # smoothed = []
    # # ===== 1. 计算点集中心 =====
    # n = len(points)
    # sum_x = sum(p[0] for p in points)
    # sum_y = sum(p[1] for p in points)
    # sum_z = sum(p[2] for p in points)
    # center = [sum_x / n, sum_y / n, sum_z / n]
    # for pt, obj in zip(points, sel):
    #     x, y, z = pt
    #     # 计算到中心的距离
    #     dx = x - center[0]
    #     dy = y - center[1]
    #     dz = z - center[2]
    #     distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    #
    #     # 计算权重（距离越大权重越大）
    #     sigma = 0.5
    #     weight = math.exp(-(distance / sigma) ** 2)
    #     print(obj, weight)
    #
    #     # 计算新坐标：原始坐标与中心的加权平均
    #     if distance > 0:
    #         new_x = (x + weight * center[0]) / (1 + weight)
    #         new_y = (y + weight * center[1]) / (1 + weight)
    #         new_z = (z + weight * center[2]) / (1 + weight)
    #     else:
    #         new_x, new_y, new_z = x, y, z  # 中心点不调整
    #
    #     smoothed.append([new_x, new_y, new_z])
    return smoothed
# 示例用法

# 示例输入数据（可替换为您的实际数据）
# sel = cmds.ls(sl=1, fl=1)
# original_points = []
# for obj in sel:
#     t = cmds.xform(obj, q=1, t=1)
#     original_points.append(t)
# # t = cmds.xform('pPlane1.vtx[83]', q=1, t=1)
# # print(t)
# # 执行平滑
# smoothed_points = smooth_3d_points(
#     points=original_points,
#     radius=1.5,  # 控制邻域范围
#     sigma=0.1,  # 控制平滑强度（值越小越局部）
#     sel=sel
# )
# for obj,num in zip(sel,smoothed_points):
#     cmds.xform(obj, t=num)
# # 打印结果
# print("原始数据:")
# for p in original_points:
#     print([round(v, 2) for v in p])
#
# print("\n平滑后数据:")
# for p in smoothed_points:
#     print([round(v, 2) for v in p])

def smooth_points_with_central_weight(points,sel):
    """
    权重规则：点离中心越远，平滑时向中心拉动的权重越大
    参数:
        points : 三维点列表 [[x1,y1,z1], [x2,y2,z2], ...]
    返回:
        平滑后的新点列表
    """
    # ===== 1. 计算点集中心 =====
    n = len(points)
    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    sum_z = sum(p[2] for p in points)
    center = [sum_x / n, sum_y / n, sum_z / n]

    # ===== 3. 对每个点计算平滑位置 =====
    smoothed = []
    for pt,obj in zip(points,sel):
        x, y, z = pt
        # 计算到中心的距离
        dx = x - center[0]
        dy = y - center[1]
        dz = z - center[2]
        distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        # 计算权重（距离越大权重越大）
        sigma = 0.5
        weight = math.exp(-(distance / sigma) ** 2)
        print(obj,weight)


        # 计算新坐标：原始坐标与中心的加权平均
        if distance > 0:
            new_x = (x + weight * center[0]) / (1 + weight)
            new_y = (y + weight * center[1]) / (1 + weight)
            new_z = (z + weight * center[2]) / (1 + weight)
        else:
            new_x, new_y, new_z = x, y, z  # 中心点不调整

        smoothed.append([new_x, new_y, new_z])

    return smoothed


# 示例使用
# 示例输入包含离群点

# sel = cmds.ls(sl=1, fl=1)
# original_points = []
# for obj in sel:
#     t = cmds.xform(obj, q=1, t=1)
#     original_points.append(t)
# # original_points = [
# #     [1.0, 1.0, 1.0],
# #     [1.1, 0.9, 1.0],
# #     [0.9, 1.1, 0.9],
# #     [50.0, 50.0, 50.0]  # 远离中心的点
# # ]
#
# # 执行平滑
# smoothed_points = smooth_points_with_central_weight(original_points,sel)
#
# for obj, num in zip(sel, smoothed_points):
#     cmds.xform(obj, t=num)
# # # 打印结果（保留2位小数）

# print("原始数据：")
# for p in original_points:
#     print([round(v, 2) for v in p])
#
# print("\n平滑后数据：")
# for p in smoothed_points:
#     print([round(v, 2) for v in p])

import maya.cmds as cmds

import math

def get_connected_vertices2(vertex):
    """获取相邻顶点坐标（优化版）"""
    edges = cmds.polyListComponentConversion(vertex, fromVertex=True, toEdge=True)
    edges = cmds.ls(edges, flatten=True)
    vertices = cmds.polyListComponentConversion(edges, fromEdge=True, toVertex=True)
    vertices = cmds.ls(vertices, flatten=True)
    print(vertices)
    adjacent = [v for v in vertices if v != vertex]
    # print(adjacent)
    return [cmds.xform(v, q=1, t=1) for v in vertices]

def smooth_3d_points3(points, radius=1.0, sigma=0.5, sel=None):
    smoothed = []
    original_points = points.copy()  # 使用原始位置计算，避免连锁更新

    for i, (x, y, z) in enumerate(original_points):
        adjacent_points = get_connected_vertices2(sel[i])  # 获取相邻点坐标

        sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
        total_weight = 0.0

        # 计算每个相邻点的权重
        for (ax, ay, az) in adjacent_points:
            dx = ax - x
            dy = ay - y
            dz = az - z
            distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

            # 高斯权重 + 距离限制
            if distance <= radius:
                weight = math.exp(-(distance ** 2) / (2 * sigma ** 2))
                sum_x += ax * weight
                sum_y += ay * weight
                sum_z += az * weight
                total_weight += weight

        # 计算新坐标（加权平均）
        if total_weight > 0:
            new_x = (sum_x + x * sigma) / (total_weight + sigma)  # 加入原始位置权重
            new_y = (sum_y + y * sigma) / (total_weight + sigma)
            new_z = (sum_z + z * sigma) / (total_weight + sigma)
        else:
            new_x, new_y, new_z = x, y, z  # 无相邻点时保持原位

        smoothed.append([new_x, new_y, new_z])

    return smoothed

# # 执行平滑时先计算所有新位置，再一次性更新
# sel = cmds.ls(sl=1, fl=1)
# original_points = [cmds.xform(obj, q=1, t=1) for obj in sel]
# smoothed_points = smooth_3d_points3(original_points, radius=1.0, sigma=1.0, sel=sel)
#
# # 批量更新（避免连锁反应）
# for obj, new_pos in zip(sel, smoothed_points):
#     cmds.xform(obj, t=new_pos)




# 弹簧
def spring_3d_points(points, k=1.0, rest_length=1.0, max_iterations=100):
    pass

#

import numpy as np

def fit_rbf_deformation(source_mesh, target_mesh, sigma=1.0, reg=1e-6):
    # 获取控制点（需要提前手动选择对应点）
    source_ctl = cmds.ls(f"{source_mesh}.vtx[*]", sl=True)  # 源模型选中的点
    target_ctl = [v.replace(source_mesh, target_mesh) for v in source_ctl]  # 目标模型对应点

    # 提取控制点坐标
    src_points = np.array([cmds.xform(v, q=True, t=True) for v in source_ctl])
    tgt_points = np.array([cmds.xform(v, q=True, t=True) for v in target_ctl])
    displacements = tgt_points - src_points

    # 构建RBF矩阵
    n_ctl = len(src_points)
    A = np.zeros((n_ctl, n_ctl))
    for i in range(n_ctl):
        for j in range(n_ctl):
            r = np.linalg.norm(src_points[i] - src_points[j])
            A[i, j] = np.exp(-(r ** 2) / (2 * sigma ** 2))  # 高斯核函数
    A += np.eye(n_ctl) * reg  # 添加正则化防止矩阵奇异

    # 求解权重
    W = np.linalg.solve(A, displacements)

    # 变形所有顶点
    all_vtx = cmds.ls(f"{source_mesh}.vtx[*]", fl=True)
    all_src = np.array([cmds.xform(v, q=True, t=True) for v in all_vtx])
    deformed = all_src.copy()

    # 遍历每个顶点计算变形
    for i, point in enumerate(all_src):
        delta = np.zeros(3)
        for j in range(n_ctl):
            r = np.linalg.norm(point - src_points[j])
            delta += W[j] * np.exp(-(r ** 2) / (2 * sigma ** 2))
        deformed[i] += delta

    # 应用变形
    for vtx, pos in zip(all_vtx, deformed):
        cmds.xform(vtx, t=pos.tolist())


# 使用示例（需要先手动选择对应控制点）
fit_rbf_deformation("sourceMesh", "targetMesh", sigma=2.0)


cmds.select('joint100','joint200','joint300','joint400','joint500','joint600','joint700','joint800','joint900')
for i in range(1000):
    cmds.joint(p=(0, 0, 0))
import time
# 记录开始时间
start_time = time.time()

sel = cmds.ls(sl=1)
source_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + sel[0] + '\");')
print(source_skin_cluster)
source_skin_joint = cmds.skinCluster(source_skin_cluster, q=1, inf=1)
print(source_skin_joint)
# source_skin_joint=source_skin_joint[:100]
restore = []
for j in source_skin_joint:
    layer = cmds.ls(j, long=True)
    layer_num = len(layer[0].split("|"))
    if layer_num%100==0:
        parent = cmds.listRelatives(j, p=True)
        cmds.parent(j, w=True)
        p_s = [parent, j]
        restore.append(p_s)
        # print(layer_num)
cmds.select(sel)
cmds.DetachSkin()
for p,j in restore:
    cmds.parent(j,p)
# 记录结束时间
end_time = time.time()
# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time:.6f} seconds to complete.")


# 记录开始时间
start_time = time.time()
cmds.DetachSkin()
# 记录结束时间
end_time = time.time()
# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time:.6f} seconds to complete.")


sel = cmds.ls(type='lattice')
print(sel)
source_nodes = cmds.listConnections('ffd1',t='lattice')
print(source_nodes)

source_nodes = cmds.listConnections('ffd1',
                                    source=True,  # 输入方向
                                    destination=False,
                                    plugs=False,  # 是否返回属性名（False 返回节点名）
                                    skipConversionNodes=True,
                                    et=0,
                                    # t='lattice',
                                    sh=1
                                    )  # 忽略单位转换节点
print(source_nodes)


target_nodes = cmds.listRelatives('ffd1LatticeShape',p=1)
print(target_nodes)




# 获取世界空间平移值（返回 [x, y, z]）
world_translate = cmds.xform('ffd2Lattice', query=True, worldSpace=True, translation=True)
print(f"世界平移: {world_translate}")
world_rotate = cmds.xform('ffd2Lattice', query=True, worldSpace=True, rotation=True)
print(f"世界旋转: {world_rotate}")
world_scale = cmds.xform('ffd2Lattice', query=True, worldSpace=True, scale=True)
print(f"世界缩放: {world_scale}")




a = cmds.xform('ffd1Lattice.pt[0][4][1]', query=True, worldSpace=True, translation=True)
print(a)



# 对过多骨骼添加ik链
for i in range(1001):
    cmds.joint(p=(i*0.1, 0, 0))

curve = 'curve1'
sel = cmds.ls(sl=1)
print(len(sel))
ik_soure = sel[0]
all_ik = []
all_top_joint = []
add_joint = []
for j in sel:
    layer = cmds.ls(j, long=True)
    layer_num = len(layer[0].split("|"))
    if layer_num%102==0:
        parent = cmds.listRelatives(j, p=True)
        # ik_soure = parent
        cmds.parent(j, w=True)
        add_joint = cmds.joint(p=(0, 0, 0),n=j+'_add_joint')
        cmds.setAttr(add_joint+".drawStyle", 2)
        cmds.delete(cmds.parentConstraint(j,add_joint,w=1))
        cmds.parent(add_joint, parent)
        ik = cmds.ikHandle(sj=ik_soure, ee=add_joint, c=curve, ccv=False, scv=False, roc=False, sol='ikSplineSolver')
        all_top_joint.append(ik_soure)
        all_ik.append(ik)
        cmds.pointConstraint(add_joint,j,w=1)
        # cmds.parent(j,add_joint)
        ik_soure = j
print(ik_soure)
print(sel[-1])
if ik_soure != sel[-1]:
    ik = cmds.ikHandle(sj=ik_soure, ee=sel[-1], c=curve, ccv=False, scv=False, roc=False, sol='ikSplineSolver')
    all_ik.append(ik)
    all_top_joint.append(ik_soure)
else:
    cmds.orientConstraint(add_joint, sel[-1],w=1)
    add_joint_a = cmds.joint(p=(0, 0, 0), n=sel[-1] + '_add_joint')
    cmds.setAttr(add_joint_a + ".drawStyle", 2)
    cmds.delete(cmds.parentConstraint(sel[-1], add_joint_a, w=1))
    cmds.parent(add_joint_a, sel[-1])
    all_top_joint.append(sel[-1])
print(all_ik,all_top_joint)


for i in range(1338):
    have_connect = cmds.listConnections("SpringJ"+str(i)+".translateX")
    # print(have_connect)
    if not have_connect:
        condition = cmds.createNode("condition")
        tx = cmds.getAttr("SpringJ"+str(i)+".translateX")
        # print(tx)
        cmds.setAttr(condition+".colorIfFalseR",0.151)
        cmds.connectAttr("anim_globalMove01.retract",condition+".firstTerm")
        cmds.setAttr(condition+".secondTerm",1338-i+1)
        cmds.setAttr(condition+".operation",3)
        cmds.connectAttr(condition+".outColorR" ,"SpringJ"+str(i)+".translateX")
for i in [99,200,301,402,503,604,705,806,907,1008,1109,1210,1311,1338]:
    condition = cmds.createNode("condition")
    tx = cmds.getAttr("SpringJ"+str(i)+".translateX")
    # print(tx)
    cmds.setAttr(condition+".colorIfFalseR",0.151)
    cmds.connectAttr("anim_globalMove01.retract",condition+".firstTerm")
    cmds.setAttr(condition+".secondTerm",1338-i+1)
    cmds.setAttr(condition+".operation",3)
    cmds.connectAttr(condition+".outColorR" ,"SpringJ"+str(i)+".translateX")


shape = 'curveShape6'
target = 'LocatorSC'
motionPath = cmds.createNode('motionPath')
cmds.connectAttr(shape+'.worldSpace[0]', motionPath+'.geometryPath')
cmds.connectAttr(motionPath+'.rotateX', target+'.rotateX')
cmds.connectAttr(motionPath+'.rotateY', target+'.rotateY')
cmds.connectAttr(motionPath+'.rotateZ', target+'.rotateZ')
cmds.connectAttr(motionPath+'.rotateOrder', target+'.rotateOrder')
cmds.connectAttr(motionPath+'.message', target+'.specifiedManipLocation')
cmds.setAttr(motionPath+'.fractionMode', 1)

addDoubleLinear_x = cmds.createNode('addDoubleLinear')
cmds.connectAttr(target+'.transMinusRotatePivotX', addDoubleLinear_x+'.input1')
cmds.connectAttr(motionPath+'.xCoordinate', addDoubleLinear_x+'.input2')
cmds.connectAttr(addDoubleLinear_x+'.output', target+'.translateX')
addDoubleLinear_y = cmds.createNode('addDoubleLinear')
cmds.connectAttr(target+'.transMinusRotatePivotX', addDoubleLinear_y+'.input1')
cmds.connectAttr(motionPath+'.yCoordinate', addDoubleLinear_y+'.input2')
cmds.connectAttr(addDoubleLinear_y+'.output', target+'.translateY')
addDoubleLinear_z = cmds.createNode('addDoubleLinear')
cmds.connectAttr(target+'.transMinusRotatePivotX', addDoubleLinear_z+'.input1')
cmds.connectAttr(motionPath+'.zCoordinate', addDoubleLinear_z+'.input2')
cmds.connectAttr(addDoubleLinear_z+'.output', target+'.translateZ')



cmds.undoInfo(ock=1)
mel.eval('ConvertSelectionToVertices;')
sel = cmds.ls(fl=1, sl=1)
all_joint = []
for i in range(0, len(sel)):
    cmds.select(sel[i], r=1)
    mel.eval('PolySelectConvert 2;')
    new_sel = cmds.ls(sl=1, fl=1)
    new_sel = [x for x in new_sel if x not in sel]
    cmds.select(new_sel[0])
    mel.eval('SelectContiguousEdges;')
    cluster = cmds.cluster()
    cmds.select(cl=1)
    joint = cmds.joint(p=(0, 0, 0))
    cmds.delete(cmds.parentConstraint(cluster[1], joint, weight=1))
    cmds.delete(cluster)
    joint = cmds.ls(sl=1)
    all_joint.append(joint)
print(all_joint[0][0])
print(all_joint[len(all_joint)-1])
for i in range(1, len(all_joint)):
    cmds.parent(all_joint[len(all_joint)-i], all_joint[len(all_joint)-i-1])
for i in range(1, len(all_joint)):
    cmds.parent(all_joint[i], all_joint[i - 1])
cmds.undoInfo(cck=1)



cmds.addAttr('ToeCurl_L.bigCurl', e=1, softMaxValue=10.0, softMinValue=-2.0)
cmds.setAttr('ToeCurl_R.bigCurl', cb=False, k=True)
cmds.setAttr('ToeCurl_R.bigCurl', cb=True, k=False)


sel = cmds.ls(sl=1)
for s in sel:
    cmds.select(s)
    cmds.pickWalk(d='up')
    mel.eval('doGroup 0 1 1;')
    grp = cmds.ls(sl=1)
    grp = cmds.rename(grp[0], s + '_add_drver_grp')
    for an in ['translateX','translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']:
        soure_an = cmds.listConnections(s+'.'+an,p=1)
        if soure_an:
            cmds.connectAttr(soure_an[0],s+'_add_drver_grp.'+an)
            cmds.disconnectAttr(soure_an[0], s + '.' + an)





sel = cmds.ls(sl=1)
for s in sel:
    cmds.select(s)
    cmds.pickWalk(d='up')
    mel.eval('doGroup 0 1 1;')
    old_grp = cmds.ls(sl=1)
    grp = cmds.rename(old_grp[0], s + '_add_drver_grp')
    if cmds.objExists(s[:-1] + 'R'):
        mirror = s[:-1] + 'R'

    for an in ['translateX', 'translateY', 'translateZ']: #,'rotateX', 'rotateY', 'rotateZ'
        soure_an = cmds.listConnections(mirror + '_add_drver_grp.'+an, s=1, d=1)
        if soure_an:
            cmds.select(soure_an)
            cmds.duplicate(rr=1)
            drver_node = cmds.ls(sl=1)
            cmds.connectAttr('wing_drver_Grp.wing_retract_drver_L', drver_node[0] + '.input')

            mirror_an = cmds.listConnections(mirror + '_add_drver_grp.' + an, p=1)
            if mirror_an:
                cmds.connectAttr(drver_node[0]+'.output',grp+'.'+an)


sel = cmds.ls(sl=1)
for s in sel:
    grp = s + '_add_drver_grp'
    if cmds.objExists(s[:-1] + 'R'):
        mirror = s[:-1] + 'R'
    for an in ['rotateX', 'rotateY', 'rotateZ']: #,
        soure_an = cmds.listConnections(mirror + '_add_drver_grp.'+an, s=1, d=1)
        if soure_an:
            cmds.select(soure_an)
            cmds.duplicate(rr=1)
            drver_node = cmds.ls(sl=1)
            cmds.connectAttr('wing_drver_Grp.wing_retract_drver_L', drver_node[0] + '.input')

            mirror_an = cmds.listConnections(mirror + '_add_drver_grp.' + an, p=1)
            if mirror_an:
                cmds.connectAttr(drver_node[0]+'.output',grp+'.'+an)
















sel = cmds.ls(sl=1)
for s in sel:
    cmds.select(s)
    mel.eval('doGroup 0 1 1;')
    grp = cmds.ls(sl=1)
    grp = cmds.rename(grp[0], s + '_add_drver_grp')
    for an in ['translateX','translateY', 'translateZ']:
        soure_an = cmds.listConnections(s+'.'+an,p=1)
        if soure_an:
            cmds.connectAttr(soure_an[0],s+'_add_drver_grp.'+an)
            cmds.disconnectAttr(soure_an[0], s + '.' + an)

sel = cmds.ls(sl=1)
for s in sel:
    cmds.select(s)
    # cmds.pickWalk(d='up')
    mel.eval('doGroup 0 1 1;')
    old_grp = cmds.ls(sl=1)
    grp = cmds.rename(old_grp[0], s + '_add_drver_grp')
    if cmds.objExists(s[:-1] + 'R'):
        mirror = s[:-1] + 'R'

    for an in ['translateX', 'translateY', 'translateZ']: #, 'rotateX', 'rotateY', 'rotateZ'
        soure_an = cmds.listConnections(mirror + '_add_drver_grp.'+an, s=1, d=1)
        if soure_an:
            cmds.select(soure_an)
            cmds.duplicate(rr=1)
            drver_node = cmds.ls(sl=1)
            cmds.connectAttr('wing_drver_Grp.wing_retract_drver_L', drver_node[0] + '.input')

            mirror_an = cmds.listConnections(mirror + '_add_drver_grp.' + an, p=1)
            if mirror_an:
                cmds.connectAttr(drver_node[0]+'.output',grp+'.'+an)

sel = cmds.ls(sl=1)
for s in sel:
    grp = s + '_add_drver_grp'
    if cmds.objExists(s[:-1] + 'R'):
        mirror = s[:-1] + 'R'
    for an in ['rotateX', 'rotateY', 'rotateZ']: #,
        soure_an = cmds.listConnections(mirror + '_add_drver_grp.'+an, s=1, d=1)
        if soure_an:
            cmds.select(soure_an)
            cmds.duplicate(rr=1)
            drver_node = cmds.ls(sl=1)
            cmds.connectAttr('drver_Curve.wing_retract_L', drver_node[0] + '.input')

            mirror_an = cmds.listConnections(mirror + '_add_drver_grp.' + an, p=1)
            if mirror_an:
                cmds.connectAttr(drver_node[0]+'.output',grp+'.'+an)





sel = cmds.ls(sl=1)
for s in sel:
    if cmds.objExists(s + '_add_drver_grp'):
        parent = cmds.listRelatives(s + '_add_drver_grp',p=1)
        child = cmds.listRelatives(s + '_add_drver_grp',c=1)
        cmds.parent(child,parent)
        cmds.delete(s + '_add_drver_grp')


sel = cmds.ls(sl=1)
for s in sel:
    if cmds.objExists(s + '_add_drver_grp*'):
        print(s)



# 创建附着
def attachment_surface(mesh, obj, position, model_type):
    # mesh = 'Hole_up_surface_0'
    grp = cmds.spaceLocator(name=obj + '_attachment_surface')[0]
    # position = 'locator1'
    type_list = ['worldMesh', 'worldSpace']
    # model_type = 0

    proximityPin = cmds.createNode('proximityPin')
    cmds.select(mesh)
    cmds.delete(cmds.cluster())
    shape_nodes = cmds.listRelatives(mesh, shapes=True, fullPath=True)
    cmds.connectAttr(shape_nodes[0] + '.' + type_list[model_type] + '[0]', proximityPin + '.deformedGeometry')
    cmds.connectAttr(shape_nodes[-1] + '.' + type_list[model_type], proximityPin + '.originalRailCurve')
    cmds.connectAttr(proximityPin + '.outputMatrix[0]', grp + '.offsetParentMatrix')
    matrix = cmds.getAttr(position + '.worldMatrix[0]')
    # print(matrix[-4])
    composeMatrix_matrix = cmds.createNode('composeMatrix')
    cmds.connectAttr(composeMatrix_matrix + '.outputMatrix', proximityPin + '.inputMatrix[0]')
    cmds.setAttr(composeMatrix_matrix + '.inputTranslateX', matrix[-4])
    cmds.setAttr(composeMatrix_matrix + '.inputTranslateY', matrix[-3])
    cmds.setAttr(composeMatrix_matrix + '.inputTranslateZ', matrix[-2])
    # 约束对象
    cmds.parent(grp, mesh)
    cmds.parentConstraint(grp, obj, mo=1)
attachment_surface('Hole_up_surface_0', 'locator1', 'locator1', 1)







s = 6368/6936
print(s)
d = s-a
print(d)


def find_optimal_n_integer(x):
    n_real = 0.5 * x + 1.25
    # 检查附近的整数
    n_floor = int(n_real)
    n_ceil = n_floor + 1

    # 计算两个候选值的 z
    z_floor = -0.4 * n_floor ** 2 + (0.4 * x + 1) * n_floor
    z_ceil = -0.4 * n_ceil ** 2 + (0.4 * x + 1) * n_ceil

    # 选择更大的 z（确保 n 非负）
    candidates = []
    if n_floor >= 0:
        candidates.append((n_floor, z_floor))
    if n_ceil >= 0:
        candidates.append((n_ceil, z_ceil))

    if not candidates:
        return 0, 0  # 默认处理无解情况

    best_n, best_z = max(candidates, key=lambda item: item[1])
    return best_n, best_z


# 示例：x = 20
n_int, z_int = find_optimal_n_integer(20)
print(f"当 x = 20 且 n 为整数时，n = {n_int}，z = {z_int:.2f}")



sel = cmds.ls(sl=True)

for obj in sel:
    plusMinusAverage = cmds.createNode('multiplyDivide')
    cmds.connectAttr('wrap_surface_loc.scaleZ', plusMinusAverage+'.input1X')
    cmds.addAttr(obj, ln="mul", at='double', dv=1 )
    cmds.setAttr(obj+'.mul', e=1, keyable=1)
    cmds.connectAttr(obj+'.mul', plusMinusAverage+'.input2X')
    cmds.connectAttr(plusMinusAverage+'.outputX', obj+'.scaleZ')







# 创建中间控制器按比例约束
sel = cmds.ls(sl=1)
follow_joint = sel[0]
follow_obj = sel[1]
all_center_ctr = [sel[2],sel[3],sel[4]]
follow_joint_parentConstraint = cmds.parentConstraint(follow_joint, all_center_ctr[0], mo=1)
cmds.parentConstraint(follow_obj, all_center_ctr[0], mo=1)
plusMinusAverage = cmds.createNode('plusMinusAverage')
cmds.setAttr(plusMinusAverage+'.operation', 2)
cmds.setAttr(plusMinusAverage+'.input1D[0]', 10)
cmds.connectAttr((all_center_ctr[2] + '.follow'), plusMinusAverage+'.input1D[1]')
multiplyDivide = cmds.createNode('multiplyDivide')
cmds.connectAttr((all_center_ctr[2] + '.follow'), multiplyDivide+'.input1X')
cmds.connectAttr(plusMinusAverage+'.output1D', multiplyDivide+'.input1Y')
cmds.setAttr(multiplyDivide+'.input2X', 0.1)
cmds.setAttr(multiplyDivide+'.input2Y', 0.1)
cmds.connectAttr(multiplyDivide+'.outputX', follow_joint_parentConstraint[0]+'.'+follow_joint+'W0')
cmds.connectAttr(multiplyDivide+'.outputY', follow_joint_parentConstraint[0]+'.'+follow_obj+'W1')


sel = cmds.ls(sl=1)
for s in sel:
    cmds.connectAttr(s+'.inverseMatrix', s+'.offsetParentMatrix')






sel = cmds.ls(sl=1)
loc_grp = cmds.ls(sl=1)
num_list = [[1.0,1.0], [0,0], [0.8,0.6], [1.0,0.8], [0,0], [0.8,0.6], [1.0,0.8]]
for grp, num in zip(loc_grp, num_list):
    multiplyDivide = cmds.createNode('multiplyDivide')
    cmds.connectAttr(sel[0]+'.translateX', multiplyDivide + '.input1X')
    cmds.connectAttr(sel[0]+'.translateY', multiplyDivide + '.input1Y')
    cmds.setAttr(multiplyDivide + '.input2X', num[0])
    cmds.setAttr(multiplyDivide + '.input2Y', num[0])
    plusMinusAverage = cmds.createNode('plusMinusAverage')
    cmds.connectAttr(multiplyDivide+'.outputX', plusMinusAverage+'.input2D[0].input2Dx')
    cmds.connectAttr(multiplyDivide+'.outputY', plusMinusAverage+'.input2D[0].input2Dy')

    multiplyDivide = cmds.createNode('multiplyDivide')
    cmds.connectAttr(sel[1] + '.translateX', multiplyDivide + '.input1X')
    cmds.connectAttr(sel[1] + '.translateY', multiplyDivide + '.input1Y')
    cmds.setAttr(multiplyDivide + '.input2X', num[1])
    cmds.setAttr(multiplyDivide + '.input2Y', num[1])
    cmds.connectAttr(multiplyDivide+'.outputX', plusMinusAverage+'.input2D[1].input2Dx')
    cmds.connectAttr(multiplyDivide+'.outputY', plusMinusAverage+'.input2D[1].input2Dy')

    cmds.connectAttr(plusMinusAverage+'.output2D.output2Dx', grp+'.translateX')
    cmds.connectAttr(plusMinusAverage+'.output2D.output2Dy', grp+'.translateY')



sel = cmds.ls(sl=True)
for s in sel:
    chlid = cmds.listRelatives(s,p=1)
    parent = cmds.listRelatives(chlid, p=1)
    grp = cmds.group(n=s+'_drver_grp',em=1)
    cmds.delete(cmds.parentConstraint(s,grp))
    cmds.parent(grp,parent)
    cmds.parent(chlid, grp)



sel = cmds.ls(sl=True)
for s in sel:

    if cmds.objExists(s+'_drver_grp'):
        parent = cmds.listRelatives(s+'_drver_grp', p=1)
        child = cmds.listRelatives(s+'_drver_grp', c=1)
        cmds.parent(child,parent)
        cmds.delete(s+'_drver_grp')




from binascii import hexlify
cmds.setAttr(('type1.textInput'),' '.join([hexlify(x.encode('utf-16 be'))for x in "textFieldGrpNew"]),typ="string")

sel_1 = cmds.ls(sl=1)

sel = cmds.ls(sl=1)
for i in range(len(sel)):
    loc = cmds.spaceLocator(n=sel[i]+'_loc')
    cmds.delete(cmds.parentConstraint(sel[i],loc))
    parent = cmds.listRelatives(sel[i],p=1)
    parent = cmds.listRelatives(parent, p=1)
    parent_1 = cmds.listRelatives(parent, p=1)
    cmds.parent(loc, parent_1)
    cmds.connectAttr(loc[0]+'.translate', parent[0]+'.translate')
    cmds.connectAttr(loc[0]+'.rotate', parent[0]+'.rotate')
    cmds.parentConstraint(sel_1[i], loc, mo=1)
    cmds.setAttr(loc[0]+'.visibility', 0)


sel = cmds.ls(sl=1, type='joint')
even_index_list = sel[::2]
filtered_list = [item for item in sel if item not in even_index_list]
print(filtered_list)
for i in range(1,len(even_index_list)):
    cmds.parent(even_index_list[i],even_index_list[i-1])
cmds.delete(filtered_list[:-1])

# 获取形状节点
print(cmds.listRelatives('ik_con_0_Curve', shapes=1))




soure = 'nurbsCircle1'
target = 'nurbsCircle2'

soure = 'nurbsCircle3'
target = 'nurbsCircle5'
is_end = 1
is_parentCparentConstraint = cmds.ls(soure+'_parentConstraint1', type="parentConstraint")
parentConstraint = cmds.parentConstraint(soure, target, mo=1)
if is_end == 0:
    cmds.disconnectAttr(parentConstraint[0] + '.constraintTranslateX', target + '.translateX')
    cmds.disconnectAttr(parentConstraint[0] + '.constraintTranslateY', target + '.translateY')
    cmds.disconnectAttr(parentConstraint[0] + '.constraintTranslateZ', target + '.translateZ')

    cmds.disconnectAttr(parentConstraint[0] + '.constraintRotateX', target + '.rotateX')
    cmds.disconnectAttr(parentConstraint[0] + '.constraintRotateY', target + '.rotateY')
    cmds.disconnectAttr(parentConstraint[0] + '.constraintRotateZ', target + '.rotateZ')

print(parentConstraint)
if is_parentCparentConstraint:
    plusMinusAverage = cmds.createNode('plusMinusAverage')
    cmds.connectAttr(is_parentCparentConstraint[0]+'.constraintRotate', plusMinusAverage+'.input3D[0]')
    cmds.connectAttr(soure+'.rotate', plusMinusAverage + '.input3D[1]')
    cmds.disconnectAttr(soure + '.rotate', parentConstraint[0]+'.target[0].targetRotate')
    cmds.connectAttr(plusMinusAverage+'.output3D', parentConstraint[0]+'.target[0].targetRotate')






print(cmds.ls('nurbsCircle2_parentConstraint1', type="parentConstraint"))

all_list = [['nurbsCircle1'], ['nurbsCircle2'], []],[['nurbsCircle2'], ['nurbsCircle3'], []],[['nurbsCircle3'], ['nurbsCircle4'], []],[['nurbsCircle4'], ['nurbsCircle5'], []],
# 创建父化数值叠加机制,(仅支持父对象约束)
def parent_constraint(all_list):
    ls_list = all_list[0][0]
    # print(ls_list)
    # print(ls_list[0])
    all_grp = cmds.group(n=ls_list[0]+'_parent_add_all_grp',em=1) # 输出骨骼
    loc = cmds.spaceLocator(n=ls_list[0]+'_parent_add_loc')
    cmds.setAttr(loc[0] + '.visibility', 0)
    cmds.parent(loc, all_grp)
    cmds.delete(cmds.parentConstraint(ls_list, loc))
    parentConstraint_1 = cmds.parentConstraint(ls_list, loc, dr=1, mo=0)

    all_grp_2 = cmds.group(n=ls_list[0] + '_parent_add_follow_parent_all_grp', em=1)
    ls_list_2 = all_list[0][1]
    # 创建输出位置定位器
    loc_1 = cmds.spaceLocator(n=ls_list_2[0] + '_parent_add_loc')
    cmds.setAttr(loc_1[0] + '.visibility', 0)
    cmds.parent(loc_1, all_grp)
    cmds.delete(cmds.parentConstraint(ls_list_2, loc_1))
    parentConstraint_2 = cmds.parentConstraint(ls_list_2, loc_1, dr=1, mo=0)
    # 创建当前位置必定旋转定位器，且约束一个外部定位器
    loc_2 = cmds.spaceLocator(n=ls_list_2[0] + '_parent_add_follow_parent_loc')
    cmds.setAttr(loc_2[0]+'.visibility', 0)
    cmds.parent(loc_2, ls_list)
    cmds.delete(cmds.parentConstraint(ls_list_2, loc_2))
    loc_3 = cmds.spaceLocator(n=ls_list_2[0] + '_parent_add_follow_parent_parentConstraint_loc')
    cmds.setAttr(loc_3[0] + '.visibility', 0)
    cmds.parent(loc_3, all_grp_2)
    cmds.delete(cmds.parentConstraint(ls_list_2, loc_3))
    parentConstraint_3 = cmds.parentConstraint(loc_2, loc_3, dr=1, mo=0)
    # 将约束数值提取并计算
    # 减少
    plusMinusAverage_subtract = cmds.createNode('plusMinusAverage')
    cmds.setAttr(plusMinusAverage_subtract+'.operation', 2)
    cmds.connectAttr(parentConstraint_1[0] + '.constraintRotate', plusMinusAverage_subtract + '.input3D[0]', f=1)
    cmds.connectAttr(parentConstraint_3[0] + '.constraintRotate', plusMinusAverage_subtract + '.input3D[1]', f=1)
    # 和上一个相加
    plusMinusAverage_sum = cmds.createNode('plusMinusAverage')
    cmds.connectAttr(parentConstraint_2[0] + '.constraintRotate', plusMinusAverage_sum + '.input3D[0]', f=1)
    cmds.connectAttr(plusMinusAverage_subtract + '.output3D', plusMinusAverage_sum + '.input3D[1]', f=1)
    cmds.disconnectAttr(parentConstraint_2[0] + '.constraintRotateX', loc_1[0] + '.rotateX')
    cmds.disconnectAttr(parentConstraint_2[0] + '.constraintRotateY', loc_1[0] + '.rotateY')
    cmds.disconnectAttr(parentConstraint_2[0] + '.constraintRotateZ', loc_1[0] + '.rotateZ')
    cmds.connectAttr(plusMinusAverage_sum+'.output3D', loc_1[0]+'.rotate')
    # 判断是否有输出对象
    if all_list[0][2]:
        cmds.parentConstraint(loc_1[0], all_list[0][2], dr=1, mo=0)

    out_connect = plusMinusAverage_sum+'.output3D'
    # end_loc = []
    for i in range(1, len(all_list)):
        # 创建输出位置定位器
        loc_1 = cmds.spaceLocator(n=all_list[i][1][0] + '_parent_add_loc')
        cmds.setAttr(loc_1[0] + '.visibility', 0)
        # end_loc = loc_1
        cmds.parent(loc_1, all_grp)
        cmds.delete(cmds.parentConstraint(all_list[i][1], loc_1))
        parentConstraint_2 = cmds.parentConstraint(all_list[i][1], loc_1, dr=1, mo=0)
        # 创建当前位置必定旋转定位器，且约束一个外部定位器
        loc_2 = cmds.spaceLocator(n=all_list[i][1][0] + '_parent_add_follow_parent_loc')
        cmds.setAttr(loc_2[0] + '.visibility', 0)
        cmds.parent(loc_2, all_list[i][0])
        cmds.delete(cmds.parentConstraint(all_list[i][1], loc_2))
        loc_3 = cmds.spaceLocator(n=all_list[i][1][0] + '_parent_add_follow_parent_parentConstraint_loc')
        cmds.setAttr(loc_3[0] + '.visibility', 0)
        cmds.parent(loc_3, all_grp_2)
        cmds.delete(cmds.parentConstraint(all_list[i][1], loc_3))
        parentConstraint_3 = cmds.parentConstraint(loc_2, loc_3, dr=1, mo=0)
        # 将约束数值提取并计算
        # 减少
        plusMinusAverage_subtract = cmds.createNode('plusMinusAverage')
        cmds.setAttr(plusMinusAverage_subtract + '.operation', 2)
        cmds.connectAttr(parentConstraint_2[0] + '.constraintRotate', plusMinusAverage_subtract + '.input3D[0]', f=1)
        cmds.connectAttr(parentConstraint_3[0] + '.constraintRotate', plusMinusAverage_subtract + '.input3D[1]', f=1)
        # 和上一个相加
        plusMinusAverage_sum = cmds.createNode('plusMinusAverage')
        cmds.connectAttr(out_connect, plusMinusAverage_sum + '.input3D[0]', f=1)
        cmds.connectAttr(plusMinusAverage_subtract + '.output3D', plusMinusAverage_sum + '.input3D[1]', f=1)
        cmds.disconnectAttr(parentConstraint_2[0] + '.constraintRotateX', loc_1[0] + '.rotateX')
        cmds.disconnectAttr(parentConstraint_2[0] + '.constraintRotateY', loc_1[0] + '.rotateY')
        cmds.disconnectAttr(parentConstraint_2[0] + '.constraintRotateZ', loc_1[0] + '.rotateZ')
        cmds.connectAttr(plusMinusAverage_sum + '.output3D', loc_1[0] + '.rotate')

        # 判断是否有输出对象
        if all_list[i][2]:
            cmds.parentConstraint(loc_1[0], all_list[i][2], dr=1, mo=0)
        out_connect = plusMinusAverage_sum + '.output3D'
    return [all_grp,all_grp_2]
    # print(out_connect)
    # print(end_loc[0] + '.rotate')
    # cmds.connectAttr(out_connect,end_loc[0] + '.rotate')

parent_constraint(all_list)











#
import maya.cmds as cmds
import math


# 计算组合数（二项式系数）
def binomial_coeff(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


# 计算贝塞尔曲线上的点
def bezier_point(t, control_points):
    n = len(control_points) - 1
    x, y, z = 0.0, 0.0, 0.0
    for i, point in enumerate(control_points):
        # 伯恩斯坦多项式权重
        weight = binomial_coeff(n, i) * ((1 - t) ** (n - i)) * (t ** i)
        x += weight * point[0]
        y += weight * point[1]
        z += weight * point[2]  # Maya是三维空间，需处理Z轴
    return (x, y, z)


# 生成贝塞尔曲线点集
def generate_bezier_curve(control_points, num_joints=10):
    return [bezier_point(i / num_joints, control_points) for i in range(num_joints + 1)]


# 用骨骼链表示曲线
def create_joints_from_curve(curve_points):
    joints = []
    for i, point in enumerate(curve_points):
        # 创建关节并重命名
        joint = cmds.joint(p=point, name=f"bezierJoint_{i:02d}")
        joints.append(joint)
    return joints


# ====== 使用示例 ======
if __name__ == "__main__":
    # 1. 定义控制点（三维坐标 [x, y, z]）
    control_points = [
        [0, 0, 0],  # P0: 起点
        [3, 5, 21],  # P1: 控制点
        [6, 0, -1]  # P2: 终点（二次贝塞尔曲线）
    ]

    # 2. 生成曲线点集（骨骼数量可调）
    curve_points = generate_bezier_curve(control_points, num_joints=15)

    # 3. 创建骨骼链
    cmds.select(clear=True)  # 清空选择避免骨骼层级错误
    joint_chain = create_joints_from_curve(curve_points)

    print(f"? 已创建 {len(joint_chain)} 个骨骼表示贝塞尔曲线")




import numpy as np
import matplotlib.pyplot as plt

# 生成数据点
x = np.linspace(-5, 5, 500)  # x范围：-5到5，500个点
y = x**2                      # y = x?

# 绘制图像
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', linewidth=2, label='$y = x^2$')  # 蓝色实线
plt.title('$y = x^2$ 的图像', fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)  # 网格线
plt.axhline(y=0, color='k', linewidth=0.8)  # 横轴
plt.axvline(x=0, color='k', linewidth=0.8)  # 纵轴
plt.legend()
plt.show()


list_1 = [0,1,2,3,4,5,6,7,8,9,10]
for i in list_1:
    if i % 3 == 0:
        print(i)



all_position_out_joint = ['joint52_actual_position_out_joint', 'joint53_actual_position_out_joint', 'joint54_actual_position_out_joint', 'joint55_actual_position_out_joint', 'joint56_actual_position_out_joint', 'joint57_actual_position_out_joint', 'joint58_actual_position_out_joint', 'joint59_actual_position_out_joint', 'joint60_actual_position_out_joint', 'joint61_actual_position_out_joint', 'joint62_actual_position_out_joint', 'joint63_actual_position_out_joint', 'joint64_actual_position_out_joint', 'joint65_actual_position_out_joint', 'joint66_actual_position_out_joint', 'joint67_actual_position_out_joint', 'joint68_actual_position_out_joint', 'joint69_actual_position_out_joint', 'joint70_actual_position_out_joint', 'joint71_actual_position_out_joint', 'joint72_actual_position_out_joint', 'joint73_actual_position_out_joint', 'joint74_actual_position_out_joint', 'joint75_actual_position_out_joint', 'joint76_actual_position_out_joint', 'joint77_actual_position_out_joint', 'joint78_actual_position_out_joint', 'joint79_actual_position_out_joint', 'joint80_actual_position_out_joint', 'joint81_actual_position_out_joint', 'joint82_actual_position_out_joint']
skinCluster = ['skinCluster2']  # 蒙皮
point = cmds.ls('ik_con_0_Curve.cv[*]', fl=1)


for i in range(len(point)):
    cmds.skinPercent(skinCluster[0], point[i], tv=(all_position_out_joint[i], 1.0))










# 新版本修改蒙皮矩阵
# 处理权重矩阵，使低版本maya模型移动过远产生点抖动的问题
def handling_weight_jitter(sel, switch):
    cmds.undoInfo(ock=1)
    if switch == 1:
        multMatrix = cmds.shadingNode('multMatrix', asUtility=1)
        Matrix = cmds.listConnections((sel[0] + '.worldMatrix[0]'), p=1, type='skinCluster')
        for M in Matrix:
            cmds.connectAttr((multMatrix + '.matrixSum'), M, force=1)
        cmds.connectAttr((sel[0] + '.worldMatrix[0]'), (multMatrix + '.matrixIn[0]'), force=1)
        cmds.connectAttr((sel[0] + '.worldInverseMatrix[0]'), (multMatrix + '.matrixIn[1]'), force=1)
        for i in range(1, len(sel)):
            multMatrix = cmds.shadingNode('multMatrix', asUtility=1)
            Matrix = cmds.listConnections((sel[i] + '.worldMatrix[0]'), p=1, type='skinCluster')
            print(Matrix)
            # for M in Matrix:
            #     target = cmds.skinCluster(M.split('.')[0], q=1, g=1)
            #     if target:
            #         if not cmds.ls(target[0], type='mesh'):
            #             Matrix.remove(M)
            for M in Matrix:
                cmds.connectAttr((multMatrix + '.matrixSum'), M, force=1)
            cmds.connectAttr((sel[i] + '.worldMatrix[0]'), (multMatrix + '.matrixIn[0]'), force=1)
            cmds.connectAttr((sel[0] + '.worldInverseMatrix[0]'), (multMatrix + '.matrixIn[1]'), force=1)
    else:
        Matrix = cmds.listConnections((sel[0] + '.worldInverseMatrix[0]'), d=1, type='multMatrix')
        for i in range(0, len(Matrix)):
            Soure = cmds.listConnections((Matrix[i] + '.matrixIn[0]'), p=1)
            Target = cmds.listConnections((Matrix[i] + '.matrixSum'), p=1)
            if Target:
                for T in Target:
                    cmds.connectAttr(Soure[0], T, force=1)
            cmds.delete(Matrix[i])
    cmds.undoInfo(cck=1)
sel = cmds.ls(sl=1)
handling_weight_jitter(sel, 1)


def create_str_shape_curve(text):
    cmds.undoInfo(ock=1)
    top_grp = cmds.textCurves(t=text)
    cmds.duplicate()
    sel = cmds.ls(sl=1)
    cmds.delete(top_grp[0])
    mel.eval('SelectHierarchy;')
    mel.eval('FreezeTransformations')

    shape = cmds.ls(sl=1, type='nurbsCurve')
    grp = cmds.ls(sl=1, type='transform')
    cmds.parent(shape, sel[0], s=1, add=1)
    cmds.delete(grp[1:])
    rename_shape_curve(grp[0])
    cmds.undoInfo(cck=1)

    return grp[0]

parent_grp = create_str_shape_curve('a')
print(parent_grp)

# 修正形状节点名称
def rename_shape_curve(obj):
    cmds.undoInfo(ock=1)
    shape = cmds.listRelatives(obj, c=1, type='nurbsCurve')
    new_shape = []
    for s in shape:
        cmds.select(s)
        cmds.rename(s, obj + 'Shape')
        sel = cmds.ls(sl=1)
        new_shape.append(sel)
    cmds.undoInfo(cck=1)

    return new_shape
print(rename_shape_curve('Text_a_4'))




import maya.cmds as cmds
import random

def sphrand_python(radius):
    # 球坐标系转笛卡尔坐标
    theta = random.uniform(0, 2 * 3.1415926)
    phi = random.uniform(0, 3.1415926)
    r = random.uniform(0, radius)
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return (x, y, z)

# 示例：创建随机点
for i in range(100):
    pos = sphrand_python(1.0)
    cmds.sphere(p=pos)



import maya.cmds as cmds

# 设置球的欧拉角旋转 (ZYX顺序)
cmds.setAttr('ball.rotateZ', 0.460)
cmds.setAttr('ball.rotateY', 0.150)
cmds.setAttr('ball.rotateX', -0.620)








import maya.cmds as cmds
from maya.api.OpenMaya import MQuaternion, MEulerRotation

# 声明使用新版API（必需！）
def maya_useNewAPI():
    pass

# 1. 定义工具函数
def apply_rotation_to_object(obj, w, x, y, z):
    """
    将四元数应用到Maya对象，使用XYZ旋转顺序
    """
    # 转换为欧拉角
    quat = MQuaternion(x, y, z, w)
    euler = MEulerRotation.setValue(quat, MEulerRotation.kXYZ)

    # 应用旋转到对象
    cmds.setAttr(f"{obj}.rotateX", euler.x)
    cmds.setAttr(f"{obj}.rotateY", euler.y)
    cmds.setAttr(f"{obj}.rotateZ", euler.z)
    return (euler.x, euler.y, euler.z)


# 2. 创建测试场景
if not cmds.objExists("testSphere"):
    sphere = cmds.polySphere(name="testSphere", radius=5)[0]
    cmds.setAttr(f"{sphere}.rotate", 0, 0, 0)  # 初始旋转归零

# 3. 测试数据（四元数输入）
test_quaternions = [
    (1, 0, 0, 0),  # 无旋转 (恒等四元数)
    (0.707, 0.707, 0, 0),  # 绕X轴旋转90度
    (0.707, 0, 0.707, 0),  # 绕Y轴旋转90度
    (0.707, 0, 0, 0.707),  # 绕Z轴旋转90度
    (0.5, 0.5, 0.5, 0.5),  # 组合旋转
]

# 4. 应用并打印结果
for w, x, y, z in test_quaternions:
    angles = apply_rotation_to_object("testSphere", w, x, y, z)
    degrees = [f"{a * 180 / 3.14159:.1f}" for a in angles]
    print(f"四元数 ({w:.3f}, {x:.3f}, {y:.3f}, {z:.3f}) => "
          f"XYZ: ({degrees[0]}°, {degrees[1]}°, {degrees[2]}°)")



def joint_weight_to_game_specification():
    cmds.undoInfo(ock=1)
    sel = cmds.ls(sl=1)
    for s in sel:
        mesh_shape = cmds.listRelatives(s, s=1)
        point = cmds.ls((mesh_shape[0] + '.vtx[*]'), fl=1)
        skin_cluster = cmds.listConnections((mesh_shape[0] + '.inMesh'), d=1)
        SkinJoint = cmds.skinCluster(s, q=1, inf=1)
        for joint in SkinJoint:
            cmds.setAttr((joint + '.liw'), 0)
        # 按骨骼归一化
        for p in point:
            all_skin = []
            edit_num = 0.0
            for i in range(0, (len(SkinJoint))):
                weights = cmds.skinPercent(skin_cluster[0], p, query=True, value=True)
                if weights != 0:
                    weights_num = round(weights[i], 2)  # 取小数点后一位
                    add_num = weights[i] - weights_num
                    edit_num = edit_num + add_num
                    unit = 0.01
                    if edit_num < 0:
                        unit = -0.01
                    cunt = int(edit_num / unit)
                    if cunt > 0:
                        weights_num = weights_num + unit
                        edit_num = edit_num - unit
                    all_skin.append((SkinJoint[i], weights_num))
            num = 1
            for j in range(0, (len(all_skin))):
                num = num - all_skin[j][1]
            all_skin[-1] = (all_skin[-1][0], round(all_skin[-1][1] + num, 2))
            cmds.skinPercent(skin_cluster[0], p, tv=all_skin)
            print(all_skin)

    cmds.warning('骨骼权重清理为小数点后一位清理完成。')
    cmds.undoInfo(cck=1)
joint_weight_to_game_specification()

point = cmds.ls(('pSphere1.vtx[*]'), fl=1)
for p in point:
    weights = cmds.skinPercent('skinCluster1', p, query=True, value=True)
    print(weights)
















bbox = cmds.xform("pCube2", query=True, boundingBox=True, worldSpace=True)

# 计算尺寸（宽度=X轴差值，高度=Y轴差值，深度=Z轴差值）
width = bbox[3] - bbox[0]  # X 轴长度
height = bbox[4] - bbox[1] # Y 轴长度
depth = bbox[5] - bbox[2]  # Z 轴长度
max = max(width, height, depth)
print(max)
max= int(max/10)














# 创建bifrost
mesh = cmds.ls(sl=1)
if mesh:
    shape = cmds.listRelatives(mesh[0], s=1, type='mesh')
    cmds.select(shape)

    # 创建样条生成命令
    mel.eval('CreateNewBifrostGraph;')
    Bifrost = cmds.ls(sl=1)
    cmds.setAttr(Bifrost[0]+'.visibility', 0)
    # mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "mesh" "Object" -portOptions "pathinfo={path=pSphereShape1;setOperation=+;active=true;channels=*;normalsPerFaceVertex=true;normalsPerPoint=true;normalsPerFace=false;componentTags=*}";')
    mel.eval('vnnCompound '+Bifrost[0]+' "/" -addNode "BifrostGraph,Geometry::Converters,mesh_to_level_set";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".mesh" "/mesh_to_level_set.mesh";')
    mel.eval('vnnCompound '+Bifrost[0]+' "/" -addNode "BifrostGraph,Geometry::Converters,volume_to_mesh" -connectTo "mesh_to_level_set";')
    mel.eval('vnnNode '+Bifrost[0]+' "/volume_to_mesh" -createInputPort "volumes.level_set" "auto";')
    mel.eval('vnnConnect '+Bifrost[0]+' "/mesh_to_level_set.level_set" "/volume_to_mesh.volumes.level_set";')
    mel.eval('vnnNode '+Bifrost[0]+' "/output" -createInputPort "meshes" "array<Object>";')
    mel.eval('vnnConnect '+Bifrost[0]+' "/volume_to_mesh.meshes" ".meshes";')

    # 额外添加属性
    cmds.addAttr(Bifrost, ln='ex', at='double',  dv=0)
    cmds.setAttr(Bifrost[0]+'.ex', e=1, keyable=1)
    expression_text = Bifrost[0]+'.ex = 0;\n'

    cmds.addAttr(Bifrost[0], ln="mesh_to_level_set", en="_:", at="enum")
    cmds.setAttr(Bifrost[0]+'.mesh_to_level_set', e=1, channelBox=True)

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "detail_size" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".detail_size" "/mesh_to_level_set.detail_size" -copyMetaData;')
    cmds.setAttr(Bifrost[0]+'.detail_size', 0.05)

    cmds.addAttr(Bifrost[0], ln='volume_mode', en='Solid:Shell:', at="enum")
    cmds.setAttr(Bifrost[0]+'.volume_mode', e=1, keyable=True)
    text = ('int $i = ' + Bifrost[0] + '.volume_mode;\n'
           'vnnNode ' + Bifrost[0] + ' "/mesh_to_level_set" -setPortDefaultValues "volume_mode" $i;\n')
    expression_text += text

    cmds.addAttr(Bifrost[0], ln="adaptivity", en="Optimized:VariedFromProperty:Off:", at="enum")
    cmds.setAttr(Bifrost[0]+'.adaptivity', e=1, keyable=True)
    cmds.setAttr(Bifrost[0]+'.adaptivity', 2)
    text = ('$i = ' + Bifrost[0] + '.adaptivity;\n'
           'vnnNode ' + Bifrost[0] + ' "/mesh_to_level_set" -setPortDefaultValues "adaptivity" $i;\n')
    expression_text += text

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "max_relative_error" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".max_relative_error" "/mesh_to_level_set.max_relative_error" -copyMetaData;')
    cmds.setAttr(Bifrost[0]+'.max_relative_error', 0.1)

    cmds.addAttr(Bifrost[0], ln="volume_subdivision_structure", en="Automatic:Power2:Power5:", at="enum")
    cmds.setAttr(Bifrost[0]+'.volume_subdivision_structure', e=1, keyable=True)
    text = ('$i = ' + Bifrost[0] + '.volume_subdivision_structure;\n'
           'vnnNode ' + Bifrost[0] + ' "/mesh_to_level_set" -setPortDefaultValues "volume_subdivision_structure" $i;\n')
    expression_text += text

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "min_hole_radius" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".min_hole_radius" "/mesh_to_level_set.min_hole_radius" -copyMetaData;')

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "thickening" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".thickening" "/mesh_to_level_set.thickening" -copyMetaData;')
    cmds.setAttr(Bifrost[0]+'.thickening', 1)

    ####
    cmds.addAttr(Bifrost[0], ln="volume_to_mesh", en="_:", at="enum")
    cmds.setAttr(Bifrost[0]+'.volume_to_mesh', e=1, channelBox=True)

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "level_set_threshold" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".level_set_threshold" "/volume_to_mesh.level_set_threshold" -copyMetaData;')

    cmds.addAttr(Bifrost[0], ln="mesh_mode", en="Automatic:Custom:", at="enum")
    cmds.setAttr(Bifrost[0]+'.mesh_mode', e=1, keyable=True)
    text = ('$i = ' + Bifrost[0] + '.mesh_mode;\n'
           'vnnNode ' + Bifrost[0] + ' "/volume_to_mesh" -setPortDefaultValues "mesh_mode" $i;\n')
    expression_text += text

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "property_threshold" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".property_threshold" "/volume_to_mesh.property_threshold" -copyMetaData;')

    cmds.addAttr(Bifrost[0], ln="custom_interior_mode", en="less:Greater:", at="enum")
    cmds.setAttr(Bifrost[0]+'.custom_interior_mode', e=1, keyable=True)
    cmds.setAttr(Bifrost[0]+'.custom_interior_mode', 1)
    text = ('$i = ' + Bifrost[0] + '.custom_interior_mode;\n'
           'vnnNode ' + Bifrost[0] + ' "/volume_to_mesh" -setPortDefaultValues "custom_interior_mode" $i;\n')
    expression_text += text

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "detail_size_scale" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".detail_size_scale" "/volume_to_mesh.detail_size_scale" -copyMetaData;')
    cmds.setAttr(Bifrost[0]+'.detail_size_scale', 1)

    cmds.addAttr(Bifrost[0], ln="adaptivity_", en="Automatic:VariedFromProperty:Off:", at="enum")
    cmds.setAttr(Bifrost[0]+'.adaptivity_', e=1, keyable=True)
    text = ('$i = ' + Bifrost[0] + '.adaptivity_;\n'
           'vnnNode ' + Bifrost[0] + ' "/volume_to_mesh" -setPortDefaultValues "adaptivity" $i;\n')
    expression_text += text

    mel.eval('vnnNode '+Bifrost[0]+' "/input" -createOutputPort "smoothing" "float";')
    mel.eval('vnnConnect '+Bifrost[0]+' ".smoothing" "/volume_to_mesh.smoothing" -copyMetaData;')
    cmds.setAttr(Bifrost[0]+'.smoothing', 0.1)

    cmds.expression(s=expression_text, ae=1, uc='all', o='')

    bifrostGeoToMaya = cmds.createNode('bifrostGeoToMaya')
    cmds.connectAttr(Bifrost[0]+'.meshes', bifrostGeoToMaya+'.bifrostGeo')
    polyCube = cmds.polyCube(ch=0)
    shape = cmds.listRelatives(polyCube, s=1)
    cmds.connectAttr(bifrostGeoToMaya+'.mayaMesh[0]', shape[0]+'.inMesh')
else:
    cmds.warning('请选择模型')





########
import maya.cmds as cmds


def get_uv_borders(objects):
    # 获取所有网格边
    mesh_edges = []
    for obj in objects:
        try:
            edges = cmds.polyListComponentConversion(obj, toEdge=True)
            mesh_edges.extend(cmds.ls(edges, fl=True, l=True))
        except:
            pass

    if not mesh_edges:
        raise RuntimeError("未选中有效网格对象")

    uv_border_edges = []
    # 遍历每条边
    for edge in mesh_edges:
        # 获取该边关联的 UV 点
        edge_uvs = cmds.polyListComponentConversion(edge, toUV=True)
        edge_uvs = cmds.ls(edge_uvs, fl=True) if edge_uvs else []

        # 获取该边关联的面
        edge_faces = cmds.polyListComponentConversion(edge, toFace=True)
        edge_faces = cmds.ls(edge_faces, fl=True) if edge_faces else []

        # 判断逻辑：UV 数量 > 2 或 关联面数 < 2
        if len(edge_uvs) > 2 or len(edge_faces) < 2:
            uv_border_edges.append(edge)

    return uv_border_edges


# 执行选择
selected = cmds.ls(selection=True, long=True)
if selected:
    border_edges = get_uv_borders(selected)
    cmds.select(border_edges)
    print(f"已选中 {len(border_edges)} 条 UV 接缝边")
else:
    print("请先选中模型")


#

import os
import sys
import inspect
from sys import path as syspath
from sys import platform

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel
def get_mesh_structure_2():
    selectList = om.MGlobal.getActiveSelectionList()
    # print(type(selectList))
    depFn = om.MFnDependencyNode()
    for i in range(selectList.length()):
        node = selectList.getDependNode(i)
        type_syr = node.apiTypeStr
        # print("Type: %s" % type_syr)
        if type_syr == "kMesh":
            depFn.setObject(node)
            # types = om.MGlobal.getFunctionSetList(node)
            name = depFn.name()
            print("Name: %s" % name)

            # 从选择列表中获取第i个被选对象的DAG路径
            dag_path = selectList.getDagPath(0)
            # 获取节点
            node = dag_path.node()
            # 从选择列表中获取第i个被选对象的DAG路径
            # node = selectList.getDagPath(i)

            # 检查节点是否为网格
            # node.hasFn(om.MFn.kMesh)

            # 如果是网格，则创建MFnMesh对象以访问网格数据
            mesh_fn = om.MFnMesh(node)
            # 获取网格的顶点数
            num_verts = mesh_fn.numVertices
            # 获取网格的面数
            num_faces = mesh_fn.numPolygons
            # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

            # 创建一个列表来存储顶点位置
            vertex_positions = []
            # 遍历所有顶点并获取它们的位置
            for i in range(num_verts):
                point = mesh_fn.getPoint(i)
                vertex_positions.append([point.x, point.y, point.z])
            # print('点：', vertex_positions)

            # 获取平滑组
            # selection_list = om.MSelectionList()
            # selection_list.add(name)
            # dag_path = selection_list.getDagPath(0)
            # line_3 = om.MItMeshEdge(dag_path)
            # smooth_group = []
            # while not line_3.isDone():
            #     # print(line_3.index())
            #     # print(line_3.isSmooth)
            #     if not line_3.isSmooth == True:
            #         smooth_group.append(line_3.index())
            #     line_3.next()

            line = cmds.ls(name+'.e[*]',fl=1)
            smooth_group = []
            for i in range(len(line)):
                is_smooth = mesh_fn.isEdgeSmooth(i)
                if is_smooth == False:
                    smooth_group.append(i)

            # mesh_fn.polygonSmoothingGroupID(0)
            # smooth = mesh_fn.getSmoothMeshDisplayOptions()
            # smooth = cmds.polySoftEdge('pCube1.e[0]',q=True,a=True)
            # smooth = cmds.polyInfo('pCube1.f[0]', smoothingGroupID=True)
            # print(smooth)
            # print('平滑组：', smooth.smoothness)

            # 获取线
            # a = [('polySurface1.f[0]'),('polySurface1.f[1]')]
            # dag_path_2 = a[0].getDagPath(0)
            # iterator = om.MItMeshPolygon(dag_path_2)
            # edges = iterator.getEdges()
            # print(edges)

            # 获取顶法线数组
            normals = mesh_fn.getVertexNormals(False)
            # 获取顶点法线数值数组
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
            # print('法线：', vertex_normals)

            # 获取uv集
            uv_set = mesh_fn.getUVSetNames()

            # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
            uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
            # print('U：', uv_coords_us)
            # print('V：', uv_coords_vs)
            # 遍历面并建立
            all_uv_topology = []
            all_topology = []
            '''
            for i in range(num_faces):
                # 按面获取拓扑
                topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                topology = cmds.ls(topology, fl=1)
                all_uv_num_1 = []
                all_uv_num_2 = []
                for j in range(len(topology)):
                    # 按拓扑获取点
                    uv = cmds.polyListComponentConversion(topology[j], tv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num_1.append(num)
                    # 按拓扑获取uv
                    uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num_2.append(num)

                all_topology.append(all_uv_num_1)
                all_uv_topology.append(all_uv_num_2)'''
            # 使用面迭代器遍历
            face_iter = om.MItMeshPolygon(dag_path)
            while not face_iter.isDone():
                # 获取当前面的顶点索引 [v0, v1, v2, ...]
                face_vert_indices = face_iter.getVertices()
                all_topology.append(face_vert_indices)

                # 获取当前面的UV索引 [uv0, uv1, uv2, ...]
                face_uv_indices = []
                for i in range(len(face_vert_indices)):
                    uv_index = face_iter.getUVIndex(i)  # 按顶点顺序获取UV索引
                    face_uv_indices.append(uv_index)
                all_uv_topology.append(face_uv_indices)

                face_iter.next()  # 移动到下一个面
            # print('拓扑', all_topology)

            # all_uv_topology = []
            # for i in range(num_faces):
            #     # 按面获取拓扑
            #     topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
            #     topology = cmds.ls(topology, fl=1)
            #     all_uv_num = []
            #     for j in range(len(topology)):
            #
            #     all_uv_topology.append(all_uv_num)
            # 重新选择回当前选择
            print('已获取当前选择模型结构数据。')
            # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
            return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group

# 创建网格
def creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group):
        # print(vertex_positions) # 3
        # print(vertex_normals) # 3
        # print(all_topology) # 4
        # print(uv_coords_us) # 1
        # print(uv_coords_vs) # 1
        # print(all_uv_topology) # 4
        # print(smooth_group) # 1
        # # 顶点位置
        vertices = vertex_positions
        # 转换为OM类型
        vertex_positions = []
        for vertex in vertices:
            vertex_positions.append(om.MPoint(vertex[0], vertex[1], vertex[2]))

        # 每个面所含的顶点数量
        face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
        for f in all_topology:
            face_counts.append(len(f))

        # 每个面的顶点索引
        face_connects = []
        for face in all_topology:
            for index in face:
                face_connects.append(index)

        # print(vertex_positions)
        # print(face_counts)
        # # print(face_connects)
        # 创建网格
        mesh_fn = om.MFnMesh()
        mesh_obj = mesh_fn.create(vertex_positions, face_counts, face_connects, uv_coords_us, uv_coords_vs)

        # print(all_uv_topology)
        uv_face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
        for f in all_uv_topology:
            uv_face_counts.append(len(f))
        uvIds = [item for sublist in all_uv_topology for item in sublist]
        # print(len(uvIds), uvIds)
        # 设置UV
        mesh_uv = mesh_fn.assignUVs(uv_face_counts, uvIds)

        # 设置法线
        # print(vertex_normals)
        normals = []
        for vertex in vertex_normals:
            normals.append(om.MVector(vertex[0], vertex[1], vertex[2]))
        # print(normals)
        normals_indices = []
        for i in range(len(normals)):
            normals_indices.append(i)
        mesh_fn.setVertexNormals(normals, normals_indices)

        # 设置平滑组
        name = mesh_fn.name()
        # 建立平滑组选集
        smooth_line = []
        if smooth_line:
            for i in smooth_group:
                smooth_line.append(name+'.e['+str(i)+']')
            # print('平滑组：',smooth_line)
            # print('平滑组：',smooth_group)
            cmds.polySoftEdge(smooth_line, a=0, ch=0)
        # 冻结当前法线
        cmds.polyNormalPerVertex(name,ufn=1)


        # # 创建一个新的变换节点作为网格的父节点
        # dep_fn = om.MFnDependencyNode()
        # transform_obj = om.MFnTransform().create()
        # dep_fn.setObject(transform_obj)
        #
        # # 将网格附加到变换节点上
        # # 注意：在 Maya 中，网格节点通常不是直接创建的，而是作为变换节点的子节点创建的
        # # 但由于我们使用的是底层 API，这里我们手动创建一个变换节点，并将网格对象附加到它上面
        # # 在 UI 中，这通常是通过在“大纲视图”中拖动网格到变换节点下来完成的
        # # 但在底层 API 中，我们需要使用 MDagModifier 来完成这个操作
        # dag_modifier = om.MDagModifier()
        # dag_modifier.reparentNode(mesh_obj, transform_obj)
        # dag_modifier.doIt()

        # 清理
        # del dag_modifier
        return name

def cccc():
    shape = 'pSphereShape1'
    cmds.select(shape)
    sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = get_mesh_structure_2()
    # print(shape)
    # # 将模型的点数据转换成uv数据，z轴数值为o
    # point = cmds.ls(shape+'.vtx[*]',fl=1)
    # for i in range(len(vertex_positions)):
    #     uv_points = cmds.polyListComponentConversion(point[i], fromVertex=True, toUV=True)
    #     uv_points = cmds.filterExpand(uv_points, sm=35)[0]  # 过滤为 UV 组件[4](@ref)
    #     num = int(uv_points.split('[')[1].split(']')[0])
    #     vertex_positions[i][0] = uv_coords_us[num]
    #     vertex_positions[i][1] = uv_coords_vs[num]
    #     vertex_positions[i][2] = 0.0

    mesh = creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group)
    print('生成的模型：',mesh)
    cmds.select(mesh)
    cmds.hyperShade(mesh, assign='lambert1')

import time
import contextlib

@contextlib.contextmanager
def timer_context(label="代码块"):
    """上下文管理器，统计任意代码块耗时"""
    start = time.perf_counter()
    try:
        yield  # 在此处插入被计时代码
    finally:
        end = time.perf_counter()
        elapsed = end - start
        print(f"?? {label} 耗时: {elapsed:.6f} 秒")

# 使用示例
with timer_context("数据加载"):
    cccc()  # 模拟数据加载
    print("数据加载完成")






import maya.cmds as cmds

# 获取模型顶点列表（如模型名称为 "pCube1"）
vertices = cmds.ls("polySurface1.vtx[*]", fl=True)
# 将所有顶点移动到 (1,1,1)
cmds.move(1, 1, 1, vertices, absolute=True)


#
import maya.cmds as cmds


vertex_name = "polySurface1.vtx[0]"
uv_points = cmds.polyListComponentConversion(vertex_name, fromVertex=True, toUV=True)
uv_points = cmds.filterExpand(uv_points, sm=35)  # 过滤为 UV 组件[4](@ref)
print(uv_points[0])
uv_data = []
cmds.select("polySurface1.vtx[0]")
for uv in uv_points:
    # 获取 UV 坐标值
    u = cmds.getAttr(f"{uv}.u")[0]
    v = cmds.getAttr(f"{uv}.v")[0]
    # 获取关联面（可选）
    face = cmds.polyListComponentConversion(uv, fromUV=True, toFace=True)[0]
    uv_data.append({"uv_point": uv, "u": u, "v": v, "face": face})




# 示例：获取顶点 pCube1.vtx[0] 的 UV 数据

# for data in uv_info:
#     print(f"UV点: {data['uv_point']}, U: {data['u']:.3f}, V: {data['v']:.3f}, 所在面: {data['face']}")



sel = 'uv_edit_model'
mesh = ['eye_base_planeShape','uv_modelShape']
point = cmds.ls(sel + '.vtx[*]', fl=1)
an = 'uv_edit_model.refresh'
objs = cmds.ls(sl=1)

expression_txt  = ''
for con in objs:
    txt = (an + ' = '+con+'.translateX;\n' +
            an + ' = '+con+'.translateY;\n' +
            an + ' = '+con+'.translateZ;\n' +
            an + ' = '+con+'.rotateX;\n' +
            an + ' = '+con+'.rotateY;\n' +
            an + ' = '+con+'.rotateZ;\n' +
            an + ' = '+con+'.scaleX;\n' +
            an + ' = '+con+'.scaleY;\n' +
            an + ' = '+con+'.scaleZ;\n')
    expression_txt += txt

for i in range(len(point)):
    uv_points = cmds.polyListComponentConversion(point[i], fromVertex=True, toUV=True)
    uv_points = cmds.filterExpand(uv_points, sm=35)[0]  # 过滤为 UV 组件[4](@ref)
    num = int(uv_points.split('[')[1].split(']')[0])
    # xform = cmds.xform(point[i], q=1, t=1, ws=1)
    # plusMinusAverage = cmds.createNode('plusMinusAverage')
    txt = 'float $xform[] = `xform -q -t -a  "'+point[i]+'"`;\n'
    for me in mesh:
        txt += ''+me+'.uvSet[0].uvSetPoints['+str(num)+'].uvSetPointsU = $xform[0];\n'
        txt += ''+me+'.uvSet[0].uvSetPoints['+str(num)+'].uvSetPointsV = $xform[1];\n'
        #  ''+plusMinusAverage+'.input3D[1].input3Dx = $xform[0];\n' \
    # ''+plusMinusAverage+'.input3D[1].input3Dy = $xform[1];\n'

    expression_txt += txt


    # cmds.connectAttr(sel+'.pnts['+str(num)+']', plusMinusAverage+'.input3D[0]')
    # cmds.setAttr(plusMinusAverage+'.input3D[1].input3Dx', xform[0])
    # cmds.setAttr(plusMinusAverage+'.input3D[1].input3Dy', xform[1])
    # cmds.setAttr(plusMinusAverage + '.input3D[1].input3Dz', xform[2])
    #
    # cmds.connectAttr(plusMinusAverage+'.output3Dx', mesh+'.uvSet[0].uvSetPoints['+str(num)+'].uvSetPointsU')
    # cmds.connectAttr(plusMinusAverage+'.output3Dy', mesh+'.uvSet[0].uvSetPoints['+str(num)+'].uvSetPointsV')
    print(uv_points)
cmds.expression(s=expression_txt, ae=1, uc='all', o='')



output = cmds.getAttr(f"polyBoolean1.output")


xform = cmds.xform('polySurface1.vtx[85]', q=1, t=1, a=1)
print(xform)


sel = cmds.ls(sl=1)
for s in sel:
    cmds.connectAttr(s+'.inverseMatrix', s+'.offsetParentMatrix')
    cmds.connectAttr(s+'.translate', s[7:]+'.translate')
    cmds.connectAttr(s + '.rotate', s[7:] + '.rotate')
    cmds.connectAttr(s + '.scale', s[7:] + '.scale')


jobs = cmds.scriptJob( listJobs=True )
for s in jobs:
    print (s)

selectList = om.MGlobal.getActiveSelectionList()
dag_path = selectList.getDagPath(0)
print(dag_path)


# 转换函数
def mobject_to_dagpath(mobject):
    dag_path = om.MDagPath()
    om.MDagPath.getAPathTo(mobject)
    return dag_path

model_name = 'pSphere1'
# 将名称转换为 MObject
sel = om.MSelectionList()
sel.add(model_name)
mobject = sel.getDependNode(0)

# 遍历子节点，找到形状节点
dag_node = om.MFnDagNode(mobject)
shapes = []
for i in range(dag_node.childCount()):
    child = dag_node.child(i)
    if child.hasFn(om.MFn.kShape):
        shapes.append(child)
# 打印转换后的形状节点路径
for shape in shapes:
    dag_path = mobject_to_dagpath(shape)
    print(dag_path.fullPathName())  # 输出：|pSphere1|pSphereShape1
# print(shapes)

model_name = 'pSphere1'
sel = om.MSelectionList()
sel.add(model_name)  # 添加模型名称

# 获取变换节点的DAG路径
transform_dag = om.MDagPath()
sel.getDagPath(0, transform_dag)  # ? 参数1：索引；参数2：目标路径对象

# 获取形状节点路径
shapes = []
for i in range(transform_dag.numberOfShapesDirectlyBelow()):
    shape_dag = om.MDagPath(transform_dag)
    shape_dag.extendToShapeDirectlyBelow(i)  # 扩展至形状节点
    shapes.append(shape_dag)
    print(shape_dag.fullPathName())  # 输出：|pSphere1|pSphereShape1

################
def get_dag_path(selection_list, index=0):
    try:
        # 尝试新版 API 调用
        dag_path = om.MDagPath()
        selection_list.getDagPath(index, dag_path)
        return dag_path
    except TypeError:
        # 回退到旧版 API
        return selection_list.getDagPath(index)
model_name = 'pSphere1'
sel = om.MSelectionList()
sel.add(model_name)  # 添加模型名称
dag_path = get_dag_path(sel)
print(dag_path)

##########################
import maya.api.OpenMaya as om

def name_to_dagpath(name):
    sel = om.MSelectionList()
    sel.add(name)
    return sel.getDagPath(0)

transform_dag = name_to_dagpath("pSphere1")
# 注意：numberOfShapesDirectlyBelow()返回直接在该变换节点下的形状节点数量
for i in range(transform_dag.numberOfShapesDirectlyBelow()):
    # 复制当前变换节点的路径
    shape_dag = om.MDagPath(transform_dag)
    # 使用extendToShape(i)扩展到第i个形状节点
    shape_dag.extendToShape(i)   # 注意：这里使用extendToShape，并传入索引i
    print(shape_dag.fullPathName())

# 修改第一段代码：获取形状节点的局部名称
shape_dag = om.MDagPath(transform_dag)
shape_dag.extendToShape(0)
shape_node = shape_dag.node()  # 获取形状节点的 MObject
shape_name = om.MFnDependencyNode(shape_node).name()
print(shape_name)  # 输出: pSphereShape1

selectList = om.MGlobal.getActiveSelectionList()
dag_path = selectList.getDagPath(0)
print(dag_path)

# 声明使用新版API（必需！）
def maya_useNewAPI():
    pass


def get_mesh_structure_2(model_name):
    # 将名称转换为 MObject
    sel = om.MSelectionList()
    sel.add(model_name)
    mobject = sel.getDependNode(0)
    # 检查是否是 transform 节点
    if not mobject.hasFn(om.MFn.kTransform):
        print(f"{model_name} 不是 transform 节点")
        return []

    # 遍历子节点，找到形状节点
    dag_node = om.MFnDagNode(mobject)
    shape_names = []
    for i in range(dag_node.childCount()):
        child = dag_node.child(i)
        if child.hasFn(om.MFn.kShape):
            # shapes.append(child)
            # 关键：将 MObject 转换为节点名称
            shape_fn = om.MFnDependencyNode(child)
            shape_name = shape_fn.name()
            shape_names.append(shape_name)
            # print(shapes)
            if shape_names:
                cmds.select(shape_names, replace=True)  # ? 替换当前选择
    selectList = om.MGlobal.getActiveSelectionList()
    # print(type(selectList))
    depFn = om.MFnDependencyNode()
    for i in range(selectList.length()):
        node = selectList.getDependNode(i)
        type_syr = node.apiTypeStr
        # print("Type: %s" % type_syr)
        if type_syr == "kMesh":
            depFn.setObject(node)
            # types = om.MGlobal.getFunctionSetList(node)
            name = depFn.name()
            print("Name: %s" % name)

            # 从选择列表中获取第i个被选对象的DAG路径
            dag_path = selectList.getDagPath(0)
            # 获取节点
            node = dag_path.node()
            # 从选择列表中获取第i个被选对象的DAG路径
            # node = selectList.getDagPath(i)

            # 检查节点是否为网格
            # node.hasFn(om.MFn.kMesh)

            # 如果是网格，则创建MFnMesh对象以访问网格数据
            mesh_fn = om.MFnMesh(node)
            # 获取网格的顶点数
            num_verts = mesh_fn.numVertices
            # 获取网格的面数
            num_faces = mesh_fn.numPolygons
            # print(f"Mesh has {num_verts} vertices and {num_faces} faces.")

            # 创建一个列表来存储顶点位置
            vertex_positions = []
            # 遍历所有顶点并获取它们的位置
            for i in range(num_verts):
                point = mesh_fn.getPoint(i)
                vertex_positions.append([point.x, point.y, point.z])
            # print('点：', vertex_positions)

            # 获取平滑组
            # selection_list = om.MSelectionList()
            # selection_list.add(name)
            # dag_path = selection_list.getDagPath(0)
            # line_3 = om.MItMeshEdge(dag_path)
            # smooth_group = []
            # while not line_3.isDone():
            #     # print(line_3.index())
            #     # print(line_3.isSmooth)
            #     if not line_3.isSmooth == True:
            #         smooth_group.append(line_3.index())
            #     line_3.next()

            line = cmds.ls(name + '.e[*]', fl=1)
            smooth_group = []
            for i in range(len(line)):
                is_smooth = mesh_fn.isEdgeSmooth(i)
                if is_smooth == False:
                    smooth_group.append(i)

            # mesh_fn.polygonSmoothingGroupID(0)
            # smooth = mesh_fn.getSmoothMeshDisplayOptions()
            # smooth = cmds.polySoftEdge('pCube1.e[0]',q=True,a=True)
            # smooth = cmds.polyInfo('pCube1.f[0]', smoothingGroupID=True)
            # print(smooth)
            # print('平滑组：', smooth.smoothness)

            # 获取线
            # a = [('polySurface1.f[0]'),('polySurface1.f[1]')]
            # dag_path_2 = a[0].getDagPath(0)
            # iterator = om.MItMeshPolygon(dag_path_2)
            # edges = iterator.getEdges()
            # print(edges)

            # 获取顶法线数组
            normals = mesh_fn.getVertexNormals(False)
            # 获取顶点法线数值数组
            vertex_normals = []
            for i in range(num_verts):
                normal_vec = normals[i]
                vertex_normals.append([normal_vec.x, normal_vec.y, normal_vec.z])
            # print('法线：', vertex_normals)

            # 获取uv集
            uv_set = mesh_fn.getUVSetNames()

            # 调用getUVs方法，传入UV集合名称和MFloatArray的引用
            uv_coords_us, uv_coords_vs = mesh_fn.getUVs(uv_set[0])
            # print('U：', uv_coords_us)
            # print('V：', uv_coords_vs)
            # 遍历面并建立
            all_uv_topology = []
            all_topology = []
            '''
            for i in range(num_faces):
                # 按面获取拓扑
                topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
                topology = cmds.ls(topology, fl=1)
                all_uv_num_1 = []
                all_uv_num_2 = []
                for j in range(len(topology)):
                    # 按拓扑获取点
                    uv = cmds.polyListComponentConversion(topology[j], tv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num_1.append(num)
                    # 按拓扑获取uv
                    uv = cmds.polyListComponentConversion(topology[j], tuv=True)
                    uv = cmds.ls(uv, fl=1)
                    num = int(uv[0].split('[')[1][:-1])
                    all_uv_num_2.append(num)

                all_topology.append(all_uv_num_1)
                all_uv_topology.append(all_uv_num_2)'''
            # 使用面迭代器遍历
            face_iter = om.MItMeshPolygon(dag_path)
            while not face_iter.isDone():
                # 获取当前面的顶点索引 [v0, v1, v2, ...]
                face_vert_indices = face_iter.getVertices()
                all_topology.append(face_vert_indices)

                # 获取当前面的UV索引 [uv0, uv1, uv2, ...]
                face_uv_indices = []
                for i in range(len(face_vert_indices)):
                    uv_index = face_iter.getUVIndex(i)  # 按顶点顺序获取UV索引
                    face_uv_indices.append(uv_index)
                all_uv_topology.append(face_uv_indices)

                face_iter.next()  # 移动到下一个面
            # print('拓扑', all_topology)

            # all_uv_topology = []
            # for i in range(num_faces):
            #     # 按面获取拓扑
            #     topology = cmds.polyListComponentConversion(name + '.f[' + str(i) + ']', tvf=True)
            #     topology = cmds.ls(topology, fl=1)
            #     all_uv_num = []
            #     for j in range(len(topology)):
            #
            #     all_uv_topology.append(all_uv_num)
            # 重新选择回当前选择
            print('已获取当前选择模型结构数据。')
            # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
            return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group

# 创建网格
def creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs,all_uv_topology, smooth_group):
    # print(vertex_positions)
    # print(vertex_normals)
    # print(all_topology)
    # print(uv_coords_us)
    # print(uv_coords_vs)
    # print(all_uv_topology)
    # print(smooth_group)
    # 顶点位置
    vertices = vertex_positions
    # 转换为OM类型
    vertex_positions = []
    for vertex in vertices:
        vertex_positions.append(om.MPoint(vertex[0], vertex[1], vertex[2]))

    # 每个面所含的顶点数量
    face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
    for f in all_topology:
        face_counts.append(len(f))

    # 每个面的顶点索引
    face_connects = []
    for face in all_topology:
        for index in face:
            face_connects.append(index)

    # print(vertex_positions)
    # print(face_counts)
    # # print(face_connects)
    # 创建网格
    mesh_fn = om.MFnMesh()
    mesh_obj = mesh_fn.create(vertex_positions, face_counts, face_connects, uv_coords_us, uv_coords_vs)

    # print(all_uv_topology)
    uv_face_counts = []  # 每个面的顶点数，这里都是四边形，所以都是4
    for f in all_uv_topology:
        uv_face_counts.append(len(f))
    uvIds = [item for sublist in all_uv_topology for item in sublist]
    # print(len(uvIds), uvIds)
    # 设置UV
    mesh_uv = mesh_fn.assignUVs(uv_face_counts, uvIds)

    # 设置法线
    # print(vertex_normals)
    normals = []
    for vertex in vertex_normals:
        normals.append(om.MVector(vertex[0], vertex[1], vertex[2]))
    # print(normals)
    normals_indices = []
    for i in range(len(normals)):
        normals_indices.append(i)
    mesh_fn.setVertexNormals(normals, normals_indices)

    # 设置平滑组
    name = mesh_fn.name()
    # 建立平滑组选集
    smooth_line = []
    if smooth_line:
        for i in smooth_group:
            smooth_line.append(name + '.e[' + str(i) + ']')
        # print('平滑组：',smooth_line)
        # print('平滑组：',smooth_group)
        cmds.polySoftEdge(smooth_line, a=0, ch=0)
    # 冻结当前法线
    cmds.polyNormalPerVertex(name, ufn=1)

    # # 创建一个新的变换节点作为网格的父节点
    # dep_fn = om.MFnDependencyNode()
    # transform_obj = om.MFnTransform().create()
    # dep_fn.setObject(transform_obj)
    #
    # # 将网格附加到变换节点上
    # # 注意：在 Maya 中，网格节点通常不是直接创建的，而是作为变换节点的子节点创建的
    # # 但由于我们使用的是底层 API，这里我们手动创建一个变换节点，并将网格对象附加到它上面
    # # 在 UI 中，这通常是通过在“大纲视图”中拖动网格到变换节点下来完成的
    # # 但在底层 API 中，我们需要使用 MDagModifier 来完成这个操作
    # dag_modifier = om.MDagModifier()
    # dag_modifier.reparentNode(mesh_obj, transform_obj)
    # dag_modifier.doIt()

    # 清理
    # del dag_modifier
    return name

# 为模型赋予材质
def assign_material(mesh_shape, material_type, have_material):
        # 尝试获取模型的着色组
        shading_groups = cmds.listConnections(mesh_shape[0] + '.instObjGroups', shapes=True) or []
        if not shading_groups:
            # 则创建一个新的着色组
            shading_groups = cmds.shadingNode('shadingEngine', asUtility=1, n=mesh_shape[0] + '_SG')
            # 链接模型和材质组
            cmds.connectAttr((mesh_shape[0] + '.instObjGroups[0]'), (shading_groups + '.dagSetMembers[0]'), force=1)
        else:
            # 如果存在多个着色组，通常我们只关心第一个
            shading_groups = shading_groups[0]
        if have_material:
            shader_name = have_material[0]
        else:
            # 创建一个材质
            shader_name = cmds.shadingNode(material_type, asShader=True, name=mesh_shape[0] + '_material')
            # print(shader_name)
        # 连接材质和着色组
        cmds.connectAttr((shader_name + '.outColor'), (shading_groups + '.surfaceShader'), force=1)
        return shader_name
# 获取模型uv边界对应的边
def get_uv_borders(objects):
    # 获取所有网格边
    mesh_edges = []
    for obj in objects:
        try:
            edges = cmds.polyListComponentConversion(obj, toEdge=True)
            mesh_edges.extend(cmds.ls(edges, fl=True, l=True))
        except:
            pass

    if not mesh_edges:
        raise RuntimeError("未选中有效网格对象")

    uv_border_edges = []
    # 遍历每条边
    for edge in mesh_edges:
        # 获取该边关联的 UV 点
        edge_uvs = cmds.polyListComponentConversion(edge, toUV=True)
        edge_uvs = cmds.ls(edge_uvs, fl=True) if edge_uvs else []

        # 获取该边关联的面
        edge_faces = cmds.polyListComponentConversion(edge, toFace=True)
        edge_faces = cmds.ls(edge_faces, fl=True) if edge_faces else []

        # 判断逻辑：UV 数量 > 2 或 关联面数 < 2
        if len(edge_uvs) > 2 or len(edge_faces) < 2:
            uv_border_edges.append(edge)

    return uv_border_edges

sel = cmds.ls(sl=1)
# cmds.select(cl=1)
for s in sel:
    cmds.select(get_uv_borders(cmds.ls(sl=1)))
    cmds.undoInfo(ock=1)
    cmds.DetachComponent()
    sel, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group = get_mesh_structure_2(s)
    cmds.undoInfo(cck=1)
    # 将模型的点数据转换成uv数据，z轴数值为o
    cmds.undo()
    print(vertex_positions)
    point = cmds.ls(sel + '.vtx[*]', fl=1)
    uv_with_point = []
    for i in range(len(vertex_positions)):
        uv_points = cmds.polyListComponentConversion(point[i], fromVertex=True, toUV=True)
        uv_points = cmds.filterExpand(uv_points, sm=35)[0]  # 过滤为 UV 组件[4](@ref)
        num = int(uv_points.split('[')[1].split(']')[0])
        list = [i,num]
        uv_with_point.append(list)
        vertex_positions[i][0] = uv_coords_us[i]
        vertex_positions[i][1] = uv_coords_vs[i]
        vertex_positions[i][2] = 0.0
        vertex_normals[i][0] = 0
        vertex_normals[i][1] = 0
        vertex_normals[i][2] = 1

    # 建立顶点对照表

    mesh = creare_mesh(vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology,
                            smooth_group)
    if cmds.objExists('lambert1'):
        cmds.select(mesh)
        cmds.hyperShade(assign='lambert1')
    print('生成的模型1：', mesh)




###########
import maya.OpenMaya as om

# 获取当前选择列表
selectList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selectList)

# 检查选择是否为空
if selectList.length() == 0:
    raise RuntimeError("没有选择任何对象")

# 获取第一个选择的依赖节点
node = om.MObject()
selectList.getDependNode(0, node)

# 获取节点类型
type_str = node.apiTypeStr()

# 检查是否为网格类型
if type_str == "kMesh":
    # 创建依赖节点函数集
    depFn = om.MFnDependencyNode(node)
    name = depFn.name()
    print("节点名称: %s" % name)

    # 获取DAG路径
    dagPath = om.MDagPath()
    selectList.getDagPath(0, dagPath)

    # 创建网格函数集
    meshFn = om.MFnMesh(dagPath)

    # 获取UV集名称
    uvSetNames = []
    meshFn.getUVSetNames(uvSetNames)

    if uvSetNames.length() > 0:
        # 获取第一个UV集的坐标
        uArray = om.MFloatArray()
        vArray = om.MFloatArray()
        meshFn.getUVs(uArray, vArray, uvSetNames[0])

        # 打印UV坐标
        print("U坐标:", list(uArray))
        print("V坐标:", list(vArray))
    else:
        print("警告: 没有找到UV集")
else:
    print("所选节点不是网格类型")
