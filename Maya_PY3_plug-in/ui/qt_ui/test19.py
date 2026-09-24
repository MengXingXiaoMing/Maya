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
pygame.display.set_caption("GPU加速三维鸟群模拟 - Alt+鼠标: Maya风格操控 | 空格: 暂停")

# 检查GPU可用性
USE_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if USE_GPU else "cpu")
print(f"使用设备: {DEVICE} | GPU加速: {USE_GPU}")

# -------- 新增的诊断代码开始 --------
print("\n=== 环境诊断信息 ===")
print(f"1. PyTorch版本: {torch.__version__}")

if hasattr(torch.version, 'cuda'):
    print(f"2. PyTorch编译的CUDA版本: {torch.version.cuda}")
else:
    print("2. PyTorch编译的CUDA版本: 无 (这表示安装的是CPU-only版本)")

print(f"3. 系统中可用的CUDA设备数量: {torch.cuda.device_count()}")

if torch.cuda.device_count() > 0:
    print(f"4. 显卡0名称: {torch.cuda.get_device_name(0)}")
else:
    print("4. 显卡0名称: 未检测到NVIDIA显卡")
print("=== 诊断结束 ===\n")
# -------- 新增的诊断代码结束 --------

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

# 鸟群参数 - 进一步优化
NUM_BOIDS = 1000  # 初始鸟的数量，可以逐步增加测试
MAX_BOIDS = 100000  # 最大鸟的数量
BOID_SIZE = 1.5
PERCEPTION_RADIUS = 10.0  # 增加感知半径，使鸟群更分散
MAX_SPEED = 3.5
MAX_FORCE = 0.2

# 行为权重 - 大幅调整以防止聚集
SEPARATION_WEIGHT = 3.2  # 显著增强分离
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 0.01  # 降低凝聚
MOUSE_WEIGHT = 0.8  # 降低鼠标影响

# 模拟状态
paused = False
show_info = True
performance_mode = False
alt_pressed = False


# Maya风格相机控制参数
class Camera:
    def __init__(self):
        # 相机位置和目标
        self.position = np.array([0.0, 100.0, 400.0], dtype=np.float32)
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        # 相机方向向量
        self.front = np.array([0.0, -0.2, -1.0], dtype=np.float32)
        self.front = self.front / np.linalg.norm(self.front)
        self.right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self.world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        # 欧拉角
        self.yaw = -90.0
        self.pitch = -10.0  # 初始向下看一点

        # 相机参数
        self.fov = 60.0
        self.near = 0.1
        self.far = 10000.0

        # 控制灵敏度 - 调整旋转方向
        self.rotate_sensitivity = 0.3
        self.pan_sensitivity = 0.005
        self.dolly_sensitivity = 0.01

        self.update_vectors()

    def update_vectors(self):
        # 更新前向量
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ], dtype=np.float32)

        self.front = front / np.linalg.norm(front)

        # 更新右向量和上向量
        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)

        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)

        # 更新目标点
        self.target = self.position + self.front * 10.0

    def rotate(self, dx, dy):
        """旋转相机 (Maya: Alt+鼠标左键) - 修复旋转方向"""
        # 反转dx和dy以匹配Maya标准
        self.yaw -= dx * self.rotate_sensitivity  # 改为减号，使旋转更自然
        self.pitch -= dy * self.rotate_sensitivity  # 改为减号

        # 限制俯仰角
        self.pitch = max(-89.0, min(89.0, self.pitch))
        self.update_vectors()

    def pan(self, dx, dy):
        """平移相机 (Maya: Alt+鼠标中键)"""
        # 使用相机右向量和上向量进行平移
        move_right = self.right * (dx * self.pan_sensitivity * np.linalg.norm(self.position))
        move_up = self.up * (dy * self.pan_sensitivity * np.linalg.norm(self.position))

        self.position += move_right + move_up
        self.target += move_right + move_up

    def dolly(self, dy):
        """推拉相机 (Maya: Alt+鼠标右键)"""
        move_forward = self.front * (dy * self.dolly_sensitivity * np.linalg.norm(self.position))
        self.position += move_forward

        # 限制最近距离
        min_distance = 10.0
        if np.linalg.norm(self.position) < min_distance:
            self.position = self.position / np.linalg.norm(self.position) * min_distance

        self.update_vectors()

    def zoom(self, dy):
        """缩放视野"""
        self.fov -= dy * 2.0
        self.fov = max(10.0, min(120.0, self.fov))

    def apply(self):
        """应用相机变换到OpenGL"""
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )


# 创建相机
camera = Camera()

# 鼠标目标位置 (世界空间)
mouse_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)


# 初始化鸟群数据 (使用PyTorch张量)
def init_boids(num_boids, device):
    """初始化鸟群数据"""
    # 随机位置 (-300, 300)，分散开避免初始聚集
    positions = (torch.rand(num_boids, 3, device=device) * 2 - 1) * 300

    # 随机速度方向，归一化后乘以随机速度
    velocities = torch.randn(num_boids, 3, device=device)
    velocities = velocities / torch.norm(velocities, dim=1, keepdim=True).clamp(min=1e-6)
    speeds = torch.rand(num_boids, device=device) * MAX_SPEED * 0.5 + MAX_SPEED * 0.5
    velocities = velocities * speeds.unsqueeze(1)

    return positions, velocities


# 初始化鸟群
positions, velocities = init_boids(NUM_BOIDS, DEVICE)


# GPU加速的鸟群算法 - 完全向量化版本
def update_boids_vectorized(positions, velocities, mouse_target_tensor):
    """完全向量化的GPU鸟群算法"""
    num_boids = positions.shape[0]

    # 1. 计算所有鸟对之间的位移向量 [N, N, 3] 和距离 [N, N]
    diff = positions.unsqueeze(1) - positions.unsqueeze(0)  # 广播减法 [N, N, 3]
    distances = torch.norm(diff, dim=2) + 1e-8  # 避免除零，加小常数 [N, N]

    # 2. 创建邻居掩码 (排除自身，且在感知半径内)
    self_mask = torch.eye(num_boids, device=DEVICE, dtype=torch.bool)
    neighbor_mask = (distances < PERCEPTION_RADIUS) & ~self_mask

    # 3. 分离力：对于每只鸟，计算其所有邻居的排斥力向量和
    inv_dist = 1.0 / distances.unsqueeze(2)  # [N, N, 1]
    separation_dir = diff * inv_dist  # 指向远离邻居的单位方向 [N, N, 3]

    # 对邻居方向求和，并取平均（注意排除无邻居的情况）
    separation_force = (separation_dir * neighbor_mask.unsqueeze(2)).sum(dim=1)  # [N, 3]
    neighbor_counts = neighbor_mask.sum(dim=1, keepdim=True).clamp(min=1)  # [N, 1]
    separation_force = separation_force / neighbor_counts
    separation_force = separation_force * SEPARATION_WEIGHT

    # 4. 对齐力：匹配邻居的平均速度
    alignment_force = (velocities.unsqueeze(1) * neighbor_mask.unsqueeze(2)).sum(dim=1)  # [N, 3]
    alignment_force = alignment_force / neighbor_counts - velocities
    alignment_force = alignment_force * ALIGNMENT_WEIGHT

    # 5. 凝聚力：飞向邻居的平均位置
    cohesion_force = (positions.unsqueeze(1) * neighbor_mask.unsqueeze(2)).sum(dim=1)  # [N, 3]
    cohesion_force = cohesion_force / neighbor_counts - positions
    cohesion_force = cohesion_force * COHESION_WEIGHT

    # 6. 鼠标吸引力
    to_mouse = mouse_target_tensor - positions
    mouse_dist = torch.norm(to_mouse, dim=1, keepdim=True).clamp(min=1e-6)
    mouse_force = (to_mouse / mouse_dist) * MOUSE_WEIGHT

    # 7. 合力、限制、更新
    acceleration = separation_force + alignment_force + cohesion_force + mouse_force

    # 限制力的大小
    acc_norm = torch.norm(acceleration, dim=1, keepdim=True).clamp(min=1e-6)
    acceleration = acceleration / acc_norm * torch.minimum(acc_norm, torch.tensor(MAX_FORCE, device=DEVICE))

    # 更新速度
    velocities = velocities + acceleration

    # 限制速度大小
    vel_norm = torch.norm(velocities, dim=1, keepdim=True).clamp(min=1e-6)
    velocities = velocities / vel_norm * torch.minimum(vel_norm, torch.tensor(MAX_SPEED, device=DEVICE))

    # 8. 更新位置和边界处理 (优化版)
    positions = positions + velocities

    # 使用取模运算实现无限循环边界，比条件判断更快更平滑
    boundary = 400.0
    positions = torch.remainder(positions + boundary, 2 * boundary) - boundary

    return positions, velocities


# 绘制坐标轴
def draw_axes():
    glBegin(GL_LINES)

    # X轴 (红色)
    glColor3f(1.0, 0.3, 0.3)
    glVertex3f(0, 0, 0)
    glVertex3f(100, 0, 0)

    # Y轴 (绿色)
    glColor3f(0.3, 1.0, 0.3)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 100, 0)

    # Z轴 (蓝色)
    glColor3f(0.3, 0.3, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 100)

    glEnd()


# 绘制网格
def draw_grid(size=300, step=30):
    glBegin(GL_LINES)
    glColor4f(0.3, 0.4, 0.5, 0.2)

    # 绘制X方向的线
    for z in range(-size, size + step, step):
        glVertex3f(-size, 0, z)
        glVertex3f(size, 0, z)

    # 绘制Z方向的线
    for x in range(-size, size + step, step):
        glVertex3f(x, 0, -size)
        glVertex3f(x, 0, size)

    glEnd()


# 创建鸟群颜色
def create_boid_colors(num_boids, device):
    """创建鸟群颜色"""
    # 随机颜色 (HSV到RGB转换)
    hues = torch.rand(num_boids, device=device) * 0.3 + 0.5  # 蓝色到青色
    saturations = torch.rand(num_boids, device=device) * 0.3 + 0.7
    values = torch.rand(num_boids, device=device) * 0.2 + 0.8

    # HSV到RGB转换
    colors = torch.zeros(num_boids, 3, device=device)
    h = hues * 6
    i = torch.floor(h).long()
    f = h - i.float()

    p = values * (1 - saturations)
    q = values * (1 - f * saturations)
    t = values * (1 - (1 - f) * saturations)

    # 根据色调区间分配RGB值
    for idx in range(6):
        mask = (i == idx)
        if idx == 0:
            colors[mask] = torch.stack([values[mask], t[mask], p[mask]], dim=1)
        elif idx == 1:
            colors[mask] = torch.stack([q[mask], values[mask], p[mask]], dim=1)
        elif idx == 2:
            colors[mask] = torch.stack([p[mask], values[mask], t[mask]], dim=1)
        elif idx == 3:
            colors[mask] = torch.stack([p[mask], q[mask], values[mask]], dim=1)
        elif idx == 4:
            colors[mask] = torch.stack([t[mask], p[mask], values[mask]], dim=1)
        elif idx == 5:
            colors[mask] = torch.stack([values[mask], p[mask], q[mask]], dim=1)

    return colors


# 创建初始颜色
colors = create_boid_colors(NUM_BOIDS, DEVICE)


# 主循环
def main():
    global paused, show_info, performance_mode, alt_pressed, NUM_BOIDS
    global positions, velocities, colors, mouse_target

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
    data_update_interval = 2  # 每2帧更新一次数据（减少GPU-CPU传输）

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

                        # 保存原有鸟群，添加新鸟
                        new_positions, new_velocities = init_boids(NUM_BOIDS - old_num, DEVICE)
                        positions = torch.cat([positions, new_positions], dim=0)
                        velocities = torch.cat([velocities, new_velocities], dim=0)
                        colors = create_boid_colors(NUM_BOIDS, DEVICE)

                        # 重置数据缓存
                        positions_cpu = None
                        colors_cpu = None

                        print(f"鸟群数量增加到: {NUM_BOIDS}")
                elif event.key == K_DOWN:
                    # 减少鸟的数量
                    new_num = max(100, int(NUM_BOIDS * 0.8))
                    if new_num != NUM_BOIDS:
                        NUM_BOIDS = new_num
                        positions = positions[:NUM_BOIDS]
                        velocities = velocities[:NUM_BOIDS]
                        colors = colors[:NUM_BOIDS]

                        # 重置数据缓存
                        positions_cpu = None
                        colors_cpu = None

                        print(f"鸟群数量减少到: {NUM_BOIDS}")
                elif event.key == K_r:
                    # 重置鸟群
                    positions, velocities = init_boids(NUM_BOIDS, DEVICE)

                    # 重置数据缓存
                    positions_cpu = None
                    colors_cpu = None

                    print("鸟群已重置")
                elif event.key == K_c:
                    # 重置相机
                    camera.__init__()
                    print("相机已重置")
                elif event.key == K_LALT or event.key == K_RALT:
                    alt_pressed = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)  # 锁定鼠标

            elif event.type == KEYUP:
                if event.key == K_LALT or event.key == K_RALT:
                    alt_pressed = False
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)  # 释放鼠标
                    mouse_rotation = False
                    mouse_panning = False
                    mouse_dollying = False

            elif event.type == MOUSEBUTTONDOWN:
                if alt_pressed:
                    if event.button == 1:  # 左键 - 旋转
                        mouse_rotation = True
                    elif event.button == 2:  # 中键 - 平移
                        mouse_panning = True
                    elif event.button == 3:  # 右键 - 推拉
                        mouse_dollying = True
                    elif event.button == 4:  # 滚轮上 - 缩小视野
                        camera.zoom(5)
                    elif event.button == 5:  # 滚轮下 - 放大视野
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

                    if mouse_rotation:  # Alt+左键: 旋转
                        camera.rotate(dx, dy)
                    elif mouse_panning:  # Alt+中键: 平移
                        camera.pan(dx, dy)
                    elif mouse_dollying:  # Alt+右键: 推拉
                        camera.dolly(dy)

        # 更新鼠标目标位置 (基于屏幕中心)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 简单的屏幕到世界坐标转换
        ndc_x = (mouse_x - WIDTH / 2) / (WIDTH / 2)
        ndc_y = -(mouse_y - HEIGHT / 2) / (HEIGHT / 2)

        # 将鼠标目标放在地面上方一点
        mouse_target[0] = ndc_x * 200
        mouse_target[1] = 0  # 地面高度
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

            # 使用向量化版本更新鸟群
            positions, velocities = update_boids_vectorized(positions, velocities, mouse_target_tensor)

            update_time = pygame.time.get_ticks() - update_start

        # 渲染鸟群
        render_start = pygame.time.get_ticks()

        # 将数据从GPU传输到CPU进行渲染（优化：减少传输频率）
        if positions_cpu is None or frames % data_update_interval == 0:
            if USE_GPU:
                positions_cpu = positions.cpu().numpy()
                colors_cpu = colors.cpu().numpy()
            else:
                positions_cpu = positions.numpy()
                colors_cpu = colors.numpy()
            last_data_update = frames

        # 使用顶点数组渲染点
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, positions_cpu)
        glColorPointer(3, GL_FLOAT, 0, colors_cpu)
        glDrawArrays(GL_POINTS, 0, NUM_BOIDS)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

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

        # 主帧率数字
        fps_text = fps_font.render(f"{fps}", True, fps_color)
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (WIDTH - 20, 20)
        screen.blit(fps_text, fps_rect)

        # "FPS"标签
        fps_label = fps_font_small.render("FPS", True, (200, 220, 255))
        label_rect = fps_label.get_rect()
        label_rect.topright = (WIDTH - 20, 60)
        screen.blit(fps_label, label_rect)

        # 性能指示器
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
            # 标题
            title = big_font.render("GPU加速三维鸟群模拟 (向量化优化版)", True, (255, 255, 255))
            screen.blit(title, (10, 10))

            # 状态信息
            info_lines = [
                f"鸟群数量: {NUM_BOIDS:,}",
                f"帧率: {fps} FPS",
                f"状态: {'暂停' if paused else '运行'}",
                f"更新耗时: {update_time}ms",
                f"渲染耗时: {render_time}ms",
                f"GPU加速: {'开启' if USE_GPU else '关闭'}",
                f"性能模式: {'开启' if performance_mode else '关闭'}",
                f"数据更新间隔: 每{data_update_interval}帧",
                f"鼠标目标: ({mouse_target[0]:.1f}, {mouse_target[1]:.1f}, {mouse_target[2]:.1f})"
            ]

            for i, line in enumerate(info_lines):
                text = font.render(line, True, (200, 220, 255))
                screen.blit(text, (10, 50 + i * 25))

            # 控制说明
            controls = [
                "=== Maya风格视图控制 ===",
                "Alt + 鼠标左键拖拽: 旋转视图 (已修复方向)",
                "Alt + 鼠标中键拖拽: 平移视图",
                "Alt + 鼠标右键拖拽: 推拉视图",
                "鼠标滚轮: 缩放视野",
                "",
                "=== 功能控制 ===",
                "空格键: 暂停/继续模拟",
                "I键: 显示/隐藏信息",
                "P键: 切换性能模式",
                "上下箭头: 增加/减少鸟的数量",
                "R键: 重置鸟群 (解决聚集问题)",
                "C键: 重置相机",
                "ESC键: 退出程序"
            ]

            for i, line in enumerate(controls):
                text = font.render(line, True, (180, 200, 220))
                screen.blit(text, (WIDTH - 350, 50 + i * 22))

        # 恢复3D模式
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        # 交换缓冲区
        pygame.display.flip()

        # 动态调整帧率限制以优化性能
        if NUM_BOIDS > 50000:
            clock.tick(30)  # 鸟多时降低帧率
        elif NUM_BOIDS > 20000:
            clock.tick(45)
        else:
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()