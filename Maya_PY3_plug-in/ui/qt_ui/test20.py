# coding=gbk
import pygame
import numpy as np
import math
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import torch

# 初始化Pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("GPU加速三维鸟群模拟 - 分组算法 | Alt+鼠标: Maya风格操控 | 空格: 暂停")

# 检查GPU可用性
USE_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if USE_GPU else "cpu")
print(f"使用设备: {DEVICE} | GPU加速: {USE_GPU}")

# 设置OpenGL
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glPointSize(2.0)

# 字体
font = pygame.font.SysFont('Arial', 16)
big_font = pygame.font.SysFont('Arial', 24, bold=True)

# 颜色定义
BACKGROUND = (0.05, 0.05, 0.1, 1.0)
TEXT_COLOR = (0.8, 0.9, 1.0, 1.0)

# 鸟群参数
NUM_BOIDS = 2500
MAX_BOIDS = 100000
BOID_SIZE = 1.5

# 分组算法参数
NUM_GROUPS = 25  # 分组数量
BIRDS_PER_GROUP = NUM_BOIDS // NUM_GROUPS  # 每组鸟数

# 组内鸟群参数（每组独立计算）
GROUP_PERCEPTION_RADIUS = 15.0  # 组内感知半径
GROUP_MAX_SPEED = 3.5
GROUP_MAX_FORCE = 0.2
GROUP_SEPARATION_WEIGHT = 3.0
GROUP_ALIGNMENT_WEIGHT = 1.0
GROUP_COHESION_WEIGHT = 1.0

# 组长移动参数
LEADER_PERCEPTION_RADIUS = 50.0  # 组长之间的感知半径
LEADER_MAX_SPEED = 2.0  # 组长移动慢一点
LEADER_MAX_FORCE = 0.1
LEADER_SEPARATION_WEIGHT = 1.5
LEADER_ALIGNMENT_WEIGHT = 1.0
LEADER_COHESION_WEIGHT = 0.5
MOUSE_WEIGHT = 0.8

# 组约束参数
GROUP_RADIUS = 60.0  # 组内鸟的最大活动半径
GROUP_RADIUS_FORCE = 2.0  # 将鸟拉回组半径内的力

# 模拟状态
paused = False
show_info = True
performance_mode = False
alt_pressed = False
frame_count = 0


# Maya风格相机控制参数
class Camera:
    def __init__(self):
        self.position = np.array([0.0, 100.0, 400.0], dtype=np.float32)
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        self.front = np.array([0.0, -0.2, -1.0], dtype=np.float32)
        self.front = self.front / np.linalg.norm(self.front)
        self.right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self.world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        self.yaw = -90.0
        self.pitch = -10.0

        self.fov = 60.0
        self.near = 0.1
        self.far = 10000.0

        self.rotate_sensitivity = 0.3
        self.pan_sensitivity = 0.005
        self.dolly_sensitivity = 0.01

        self.update_vectors()

    def update_vectors(self):
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ], dtype=np.float32)

        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)
        self.target = self.position + self.front * 10.0

    def rotate(self, dx, dy):
        self.yaw -= dx * self.rotate_sensitivity
        self.pitch -= dy * self.rotate_sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))
        self.update_vectors()

    def pan(self, dx, dy):
        move_right = self.right * (dx * self.pan_sensitivity * np.linalg.norm(self.position))
        move_up = self.up * (dy * self.pan_sensitivity * np.linalg.norm(self.position))
        self.position += move_right + move_up
        self.target += move_right + move_up

    def dolly(self, dy):
        move_forward = self.front * (dy * self.dolly_sensitivity * np.linalg.norm(self.position))
        self.position += move_forward
        min_distance = 10.0
        if np.linalg.norm(self.position) < min_distance:
            self.position = self.position / np.linalg.norm(self.position) * min_distance
        self.update_vectors()

    def zoom(self, dy):
        self.fov -= dy * 2.0
        self.fov = max(10.0, min(120.0, self.fov))

    def apply(self):
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )


# 创建相机
camera = Camera()

# 鼠标目标位置
mouse_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)


# 初始化鸟群和分组
def init_boids_and_groups(num_boids, num_groups, device):
    """初始化鸟群数据并分组"""
    birds_per_group = num_boids // num_groups

    # 初始化组长位置（在空间中均匀分布）
    grid_size = int(np.ceil(np.sqrt(num_groups)))
    leader_positions = []

    for i in range(num_groups):
        x = ((i % grid_size) / grid_size - 0.5) * 600
        z = ((i // grid_size) / grid_size - 0.5) * 600
        y = random.uniform(0, 100)
        leader_positions.append([x, y, z])

    leader_positions = torch.tensor(leader_positions, device=device, dtype=torch.float32)

    # 初始化组长速度（随机方向）
    leader_velocities = torch.randn(num_groups, 3, device=device)
    leader_velocities = leader_velocities / torch.norm(leader_velocities, dim=1, keepdim=True).clamp(min=1e-6)
    leader_velocities = leader_velocities * LEADER_MAX_SPEED * 0.5

    # 初始化组内鸟的位置（在组长周围随机分布）
    all_positions = []
    all_velocities = []

    for g in range(num_groups):
        leader_pos = leader_positions[g]

        # 在组长周围随机生成鸟的位置
        group_positions = leader_pos.unsqueeze(0) + torch.randn(birds_per_group, 3, device=device) * GROUP_RADIUS * 0.3

        # 初始化组内鸟的速度
        group_velocities = torch.randn(birds_per_group, 3, device=device)
        group_velocities = group_velocities / torch.norm(group_velocities, dim=1, keepdim=True).clamp(min=1e-6)
        group_velocities = group_velocities * GROUP_MAX_SPEED * 0.5

        all_positions.append(group_positions)
        all_velocities.append(group_velocities)

    positions = torch.cat(all_positions, dim=0)
    velocities = torch.cat(all_velocities, dim=0)

    # 创建分组索引
    group_indices = []
    for g in range(num_groups):
        start_idx = g * birds_per_group
        end_idx = start_idx + birds_per_group
        group_indices.append(torch.arange(start_idx, end_idx, device=device))

    return positions, velocities, leader_positions, leader_velocities, group_indices


# 创建鸟群颜色（按组着色）
def create_boid_colors_by_group(num_boids, num_groups, device):
    """按组创建鸟群颜色，同一组的鸟颜色相近"""
    birds_per_group = num_boids // num_groups
    colors = torch.zeros(num_boids, 3, device=device)

    # 为每个组分配一个基础色调
    for group_idx in range(num_groups):
        hue = group_idx / num_groups  # 0到1的色调
        saturation = 0.7 + torch.rand(1, device=device).item() * 0.3
        value = 0.8 + torch.rand(1, device=device).item() * 0.2

        # 组内鸟的颜色有轻微变化
        for i in range(birds_per_group):
            bird_idx = group_idx * birds_per_group + i
            if bird_idx < num_boids:
                # 轻微调整色调
                h = hue + (torch.rand(1, device=device).item() - 0.5) * 0.05
                s = saturation + (torch.rand(1, device=device).item() - 0.5) * 0.1
                v = value + (torch.rand(1, device=device).item() - 0.5) * 0.1

                # HSV到RGB转换
                h = max(0.0, min(1.0, h)) * 6
                i_h = int(h)
                f = h - i_h

                p = v * (1 - s)
                q = v * (1 - f * s)
                t = v * (1 - (1 - f) * s)

                if i_h == 0:
                    colors[bird_idx] = torch.tensor([v, t, p], device=device)
                elif i_h == 1:
                    colors[bird_idx] = torch.tensor([q, v, p], device=device)
                elif i_h == 2:
                    colors[bird_idx] = torch.tensor([p, v, t], device=device)
                elif i_h == 3:
                    colors[bird_idx] = torch.tensor([p, q, v], device=device)
                elif i_h == 4:
                    colors[bird_idx] = torch.tensor([t, p, v], device=device)
                elif i_h == 5:
                    colors[bird_idx] = torch.tensor([v, p, q], device=device)

    return colors


# 更新组长（简单的组长之间的鸟群算法）
def update_leaders(leader_positions, leader_velocities, mouse_target_tensor):
    """更新组长位置和速度"""
    num_leaders = leader_positions.shape[0]

    if num_leaders <= 1:
        return leader_positions, leader_velocities

    # 计算组长之间的距离
    diff = leader_positions.unsqueeze(1) - leader_positions.unsqueeze(0)
    distances = torch.norm(diff, dim=2) + 1e-8

    # 邻居掩码
    self_mask = torch.eye(num_leaders, device=DEVICE, dtype=torch.bool)
    neighbor_mask = (distances < LEADER_PERCEPTION_RADIUS) & ~self_mask

    # 分离力
    inv_dist = 1.0 / distances.unsqueeze(2)
    separation_dir = diff * inv_dist
    separation_force = (separation_dir * neighbor_mask.unsqueeze(2)).sum(dim=1)
    neighbor_counts = neighbor_mask.sum(dim=1, keepdim=True).clamp(min=1)
    separation_force = separation_force / neighbor_counts
    separation_force = separation_force * LEADER_SEPARATION_WEIGHT

    # 对齐力
    alignment_force = (leader_velocities.unsqueeze(1) * neighbor_mask.unsqueeze(2)).sum(dim=1)
    alignment_force = alignment_force / neighbor_counts - leader_velocities
    alignment_force = alignment_force * LEADER_ALIGNMENT_WEIGHT

    # 凝聚力
    cohesion_force = (leader_positions.unsqueeze(1) * neighbor_mask.unsqueeze(2)).sum(dim=1)
    cohesion_force = cohesion_force / neighbor_counts - leader_positions
    cohesion_force = cohesion_force * LEADER_COHESION_WEIGHT

    # 鼠标吸引力
    to_mouse = mouse_target_tensor - leader_positions
    mouse_dist = torch.norm(to_mouse, dim=1, keepdim=True).clamp(min=1e-6)
    mouse_force = (to_mouse / mouse_dist) * MOUSE_WEIGHT

    # 合力
    acceleration = separation_force + alignment_force + cohesion_force + mouse_force

    # 限制加速度
    acc_norm = torch.norm(acceleration, dim=1, keepdim=True).clamp(min=1e-6)
    acceleration = acceleration / acc_norm * torch.minimum(acc_norm, torch.tensor(LEADER_MAX_FORCE, device=DEVICE))

    # 更新速度
    leader_velocities = leader_velocities + acceleration
    vel_norm = torch.norm(leader_velocities, dim=1, keepdim=True).clamp(min=1e-6)
    leader_velocities = leader_velocities / vel_norm * torch.minimum(vel_norm,
                                                                     torch.tensor(LEADER_MAX_SPEED, device=DEVICE))

    # 更新位置
    leader_positions = leader_positions + leader_velocities

    # 边界处理
    boundary = 500.0
    leader_positions = torch.remainder(leader_positions + boundary, 2 * boundary) - boundary

    return leader_positions, leader_velocities


# 更新组内鸟（只计算组内相互作用）
def update_group_boids(positions, velocities, group_indices, leader_positions):
    """更新组内鸟的位置和速度"""
    num_groups = len(group_indices)

    for g in range(num_groups):
        # 获取当前组的鸟索引
        bird_indices = group_indices[g]
        if len(bird_indices) == 0:
            continue

        # 获取当前组的鸟数据
        group_positions = positions[bird_indices]
        group_velocities = velocities[bird_indices]
        leader_pos = leader_positions[g]

        num_birds_in_group = len(bird_indices)

        if num_birds_in_group > 1:
            # 计算组内鸟之间的距离
            diff = group_positions.unsqueeze(1) - group_positions.unsqueeze(0)
            distances = torch.norm(diff, dim=2) + 1e-8

            # 邻居掩码
            self_mask = torch.eye(num_birds_in_group, device=DEVICE, dtype=torch.bool)
            neighbor_mask = (distances < GROUP_PERCEPTION_RADIUS) & ~self_mask

            # 分离力（组内鸟之间避免碰撞）
            inv_dist = 1.0 / distances.unsqueeze(2)
            separation_dir = diff * inv_dist
            separation_force = (separation_dir * neighbor_mask.unsqueeze(2)).sum(dim=1)
            neighbor_counts = neighbor_mask.sum(dim=1, keepdim=True).clamp(min=1)
            separation_force = separation_force / neighbor_counts
            separation_force = separation_force * GROUP_SEPARATION_WEIGHT

            # 对齐力（匹配组内邻居的平均速度）
            alignment_force = (group_velocities.unsqueeze(1) * neighbor_mask.unsqueeze(2)).sum(dim=1)
            alignment_force = alignment_force / neighbor_counts - group_velocities
            alignment_force = alignment_force * GROUP_ALIGNMENT_WEIGHT

            # 凝聚力（飞向组长）
            to_leader = leader_pos - group_positions
            leader_dist = torch.norm(to_leader, dim=1, keepdim=True).clamp(min=1e-6)
            cohesion_force = (to_leader / leader_dist) * GROUP_COHESION_WEIGHT

            # 组半径约束力（防止鸟飞离组长太远）
            distance_to_leader = torch.norm(to_leader, dim=1, keepdim=True)
            radius_force = torch.zeros_like(to_leader)
            too_far = distance_to_leader > GROUP_RADIUS
            if too_far.any():
                # 将太远的鸟拉回组半径内
                pull_back = -to_leader / distance_to_leader
                radius_force = pull_back * GROUP_RADIUS_FORCE * too_far.float()

            # 合力
            acceleration = separation_force + alignment_force + cohesion_force + radius_force
        else:
            # 如果组里只有一只鸟，直接跟随组长
            to_leader = leader_pos - group_positions
            leader_dist = torch.norm(to_leader, dim=1, keepdim=True).clamp(min=1e-6)
            acceleration = (to_leader / leader_dist) * GROUP_COHESION_WEIGHT

        # 限制加速度
        acc_norm = torch.norm(acceleration, dim=1, keepdim=True).clamp(min=1e-6)
        acceleration = acceleration / acc_norm * torch.minimum(acc_norm, torch.tensor(GROUP_MAX_FORCE, device=DEVICE))

        # 更新速度
        group_velocities = group_velocities + acceleration
        vel_norm = torch.norm(group_velocities, dim=1, keepdim=True).clamp(min=1e-6)
        group_velocities = group_velocities / vel_norm * torch.minimum(vel_norm,
                                                                       torch.tensor(GROUP_MAX_SPEED, device=DEVICE))

        # 更新位置
        group_positions = group_positions + group_velocities

        # 写回数据
        positions[bird_indices] = group_positions
        velocities[bird_indices] = group_velocities

    return positions, velocities


# 初始化鸟群和分组
positions, velocities, leader_positions, leader_velocities, group_indices = init_boids_and_groups(
    NUM_BOIDS, NUM_GROUPS, DEVICE
)

# 创建颜色
colors = create_boid_colors_by_group(NUM_BOIDS, NUM_GROUPS, DEVICE)


# 绘制坐标轴
def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.3, 0.3)
    glVertex3f(0, 0, 0)
    glVertex3f(100, 0, 0)
    glColor3f(0.3, 1.0, 0.3)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 100, 0)
    glColor3f(0.3, 0.3, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 100)
    glEnd()


# 绘制网格
def draw_grid(size=300, step=30):
    glBegin(GL_LINES)
    glColor4f(0.3, 0.4, 0.5, 0.2)

    for z in range(-size, size + step, step):
        glVertex3f(-size, 0, z)
        glVertex3f(size, 0, z)

    for x in range(-size, size + step, step):
        glVertex3f(x, 0, -size)
        glVertex3f(x, 0, size)

    glEnd()


# 绘制组长（调试用）
def draw_leaders(leader_positions):
    glPointSize(8.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 0.0)  # 黄色表示组长

    for pos in leader_positions:
        glVertex3f(pos[0], pos[1], pos[2])

    glEnd()
    glPointSize(2.0)


# 主循环
def main():
    global paused, show_info, performance_mode, alt_pressed, NUM_BOIDS
    global positions, velocities, colors, mouse_target, frame_count
    global leader_positions, leader_velocities, group_indices

    clock = pygame.time.Clock()

    # 性能统计
    frames = 0
    last_time = pygame.time.get_ticks()
    fps = 0
    update_time = 0

    # 缓存渲染数据
    positions_cpu = None
    colors_cpu = None
    last_data_update = 0
    data_update_interval = 2

    # 鼠标控制状态
    mouse_rotation = False
    mouse_panning = False
    mouse_dollying = False

    # 将鼠标目标转换为PyTorch张量
    mouse_target_tensor = torch.tensor(mouse_target, device=DEVICE, dtype=torch.float32)

    # 创建大号字体用于显示帧率
    fps_font = pygame.font.SysFont('Arial', 36, bold=True)
    fps_font_small = pygame.font.SysFont('Arial', 20)

    running = True
    while running:
        frame_count += 1
        current_time = pygame.time.get_ticks()

        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    paused = not paused
                elif event.key == K_i:
                    show_info = not show_info
                elif event.key == K_p:
                    performance_mode = not performance_mode
                elif event.key == K_UP:
                    # 增加鸟的数量
                    new_num = min(MAX_BOIDS, int(NUM_BOIDS * 1.2))
                    if new_num != NUM_BOIDS:
                        old_num = NUM_BOIDS
                        NUM_BOIDS = new_num

                        # 重新初始化鸟群
                        positions, velocities, leader_positions, leader_velocities, group_indices = init_boids_and_groups(
                            NUM_BOIDS, NUM_GROUPS, DEVICE
                        )
                        colors = create_boid_colors_by_group(NUM_BOIDS, NUM_GROUPS, DEVICE)

                        positions_cpu = None
                        colors_cpu = None

                        print(f"鸟群数量增加到: {NUM_BOIDS}")
                elif event.key == K_DOWN:
                    # 减少鸟的数量
                    new_num = max(100, int(NUM_BOIDS * 0.8))
                    if new_num != NUM_BOIDS:
                        NUM_BOIDS = new_num
                        positions, velocities, leader_positions, leader_velocities, group_indices = init_boids_and_groups(
                            NUM_BOIDS, NUM_GROUPS, DEVICE
                        )
                        colors = create_boid_colors_by_group(NUM_BOIDS, NUM_GROUPS, DEVICE)

                        positions_cpu = None
                        colors_cpu = None

                        print(f"鸟群数量减少到: {NUM_BOIDS}")
                elif event.key == K_r:
                    # 重置鸟群
                    positions, velocities, leader_positions, leader_velocities, group_indices = init_boids_and_groups(
                        NUM_BOIDS, NUM_GROUPS, DEVICE
                    )
                    colors = create_boid_colors_by_group(NUM_BOIDS, NUM_GROUPS, DEVICE)

                    positions_cpu = None
                    colors_cpu = None

                    print("鸟群已重置")
                elif event.key == K_c:
                    camera.__init__()
                    print("相机已重置")
                elif event.key == K_LALT or event.key == K_RALT:
                    alt_pressed = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)

            elif event.type == KEYUP:
                if event.key == K_LALT or event.key == K_RALT:
                    alt_pressed = False
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    mouse_rotation = False
                    mouse_panning = False
                    mouse_dollying = False

            elif event.type == MOUSEBUTTONDOWN:
                if alt_pressed:
                    if event.button == 1:
                        mouse_rotation = True
                    elif event.button == 2:
                        mouse_panning = True
                    elif event.button == 3:
                        mouse_dollying = True
                    elif event.button == 4:
                        camera.zoom(5)
                    elif event.button == 5:
                        camera.zoom(-5)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_rotation = False
                elif event.button == 2:
                    mouse_panning = False
                elif event.button == 3:
                    mouse_dollying = False

            elif event.type == MOUSEMOTION:
                if alt_pressed:
                    dx, dy = event.rel
                    if mouse_rotation:
                        camera.rotate(dx, dy)
                    elif mouse_panning:
                        camera.pan(dx, dy)
                    elif mouse_dollying:
                        camera.dolly(dy)

        # 更新鼠标目标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ndc_x = (mouse_x - WIDTH / 2) / (WIDTH / 2)
        ndc_y = -(mouse_y - HEIGHT / 2) / (HEIGHT / 2)

        mouse_target[0] = ndc_x * 200
        mouse_target[1] = 0
        mouse_target[2] = ndc_y * 200
        mouse_target_tensor = torch.tensor(mouse_target, device=DEVICE, dtype=torch.float32)

        # 清屏
        glClearColor(*BACKGROUND)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 设置投影矩阵
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.fov, WIDTH / HEIGHT, camera.near, camera.far)

        # 设置模型视图矩阵
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.apply()

        # 绘制网格和坐标轴
        if not performance_mode:
            draw_grid()
            draw_axes()

        # 更新鸟群
        if not paused:
            update_start = pygame.time.get_ticks()

            # 1. 先更新组长
            leader_positions, leader_velocities = update_leaders(
                leader_positions, leader_velocities, mouse_target_tensor
            )

            # 2. 再更新组内鸟（只计算组内相互作用）
            positions, velocities = update_group_boids(
                positions, velocities, group_indices, leader_positions
            )

            update_time = pygame.time.get_ticks() - update_start

        # 渲染鸟群
        render_start = pygame.time.get_ticks()

        # 将数据从GPU传输到CPU进行渲染
        if positions_cpu is None or frames % data_update_interval == 0:
            if USE_GPU:
                positions_cpu = positions.cpu().numpy()
                colors_cpu = colors.cpu().numpy()
                leader_positions_cpu = leader_positions.cpu().numpy()
            else:
                positions_cpu = positions.numpy()
                colors_cpu = colors.numpy()
                leader_positions_cpu = leader_positions.numpy()
            last_data_update = frames

        # 使用顶点数组渲染点
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, positions_cpu)
        glColorPointer(3, GL_FLOAT, 0, colors_cpu)
        glDrawArrays(GL_POINTS, 0, NUM_BOIDS)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        # 绘制组长（调试用）
        if not performance_mode and show_info:
            draw_leaders(leader_positions_cpu)

        render_time = pygame.time.get_ticks() - render_start

        # 计算帧率
        frames += 1
        if current_time - last_time >= 1000:
            fps = frames
            frames = 0
            last_time = current_time

        # 切换到2D模式渲染文本
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WIDTH, HEIGHT, 0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)

        # 在右上角添加大型帧率显示
        fps_color = (0, 255, 0) if fps >= 30 else (255, 255, 0) if fps >= 15 else (255, 0, 0)

        fps_text = fps_font.render(f"{fps}", True, fps_color)
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (WIDTH - 20, 20)
        screen.blit(fps_text, fps_rect)

        fps_label = fps_font_small.render("FPS", True, (200, 220, 255))
        label_rect = fps_label.get_rect()
        label_rect.topright = (WIDTH - 20, 60)
        screen.blit(fps_label, label_rect)

        performance_indicator = ""
        if fps >= 60:
            performance_indicator = "流畅"
        elif fps >= 30:
            performance_indicator = "良好"
        elif fps >= 15:
            performance_indicator = "一般"
        else:
            performance_indicator = "卡顿"

        indicator_text = fps_font_small.render(performance_indicator, True, fps_color)
        indicator_rect = indicator_text.get_rect()
        indicator_rect.topright = (WIDTH - 20, 85)
        screen.blit(indicator_text, indicator_rect)

        # 渲染UI信息
        if show_info:
            title = big_font.render("GPU加速三维鸟群模拟 (分组算法)", True, (255, 255, 255))
            screen.blit(title, (10, 10))

            info_lines = [
                f"鸟群数量: {NUM_BOIDS:,}",
                f"分组数量: {NUM_GROUPS} (每组{NUM_BOIDS // NUM_GROUPS}只)",
                f"帧率: {fps} FPS",
                f"状态: {'暂停' if paused else '运行'}",
                f"更新耗时: {update_time}ms",
                f"渲染耗时: {render_time}ms",
                f"GPU加速: {'开启' if USE_GPU else '关闭'}",
                f"性能模式: {'开启' if performance_mode else '关闭'}",
                f"组半径: {GROUP_RADIUS}",
                f"组内感知半径: {GROUP_PERCEPTION_RADIUS}"
            ]

            for i, line in enumerate(info_lines):
                text = font.render(line, True, (200, 220, 255))
                screen.blit(text, (10, 50 + i * 25))

            controls = [
                "=== 分组算法说明 ===",
                "? 将鸟群分成100个独立小组",
                "? 每组鸟只在组内计算相互作用",
                "? 不同组的鸟之间完全独立",
                "? 每个组有组长，组内鸟围绕组长活动",
                "",
                "=== Maya风格视图控制 ===",
                "Alt + 鼠标左键拖拽: 旋转视图",
                "Alt + 鼠标中键拖拽: 平移视图",
                "Alt + 鼠标右键拖拽: 推拉视图",
                "鼠标滚轮: 缩放视野",
                "",
                "=== 功能控制 ===",
                "空格键: 暂停/继续模拟",
                "I键: 显示/隐藏信息",
                "P键: 切换性能模式",
                "上下箭头: 增加/减少鸟的数量",
                "R键: 重置鸟群",
                "C键: 重置相机",
                "ESC键: 退出程序"
            ]

            for i, line in enumerate(controls):
                text = font.render(line, True, (180, 200, 220))
                screen.blit(text, (WIDTH - 400, 50 + i * 22))

        # 恢复3D模式
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        # 交换缓冲区
        pygame.display.flip()

        # 动态调整帧率限制
        if NUM_BOIDS > 50000:
            clock.tick(30)
        elif NUM_BOIDS > 20000:
            clock.tick(45)
        else:
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()