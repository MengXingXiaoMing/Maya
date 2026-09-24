# -*- coding: utf-8 -*-
import pygame
import sys
import numpy as np
import torch
import time
import math
import os

# 初始化Pygame
pygame.init()

# 屏幕尺寸
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame GPU计算与可视化")

# 检查GPU是否可用
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")
if torch.cuda.is_available():
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 255)
CYAN = (50, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]


# 字体初始化
def load_fonts():
    """尝试加载中文字体，如果失败则使用系统字体"""
    # 尝试加载常见的中文字体
    chinese_fonts = [
        "simhei.ttf",  # 黑体
        "simsun.ttc",  # 宋体
        "msyh.ttc",  # 微软雅黑
        "arial.ttf",  # Arial (英文)
        None  # 最后尝试系统默认字体
    ]

    # 也尝试从系统字体目录查找
    font_paths = []
    if sys.platform == "win32":
        font_paths.append("C:/Windows/Fonts/")
    elif sys.platform == "darwin":
        font_paths.append("/System/Library/Fonts/")
        font_paths.append("/Library/Fonts/")
    else:  # Linux
        font_paths.append("/usr/share/fonts/")

    # 创建字体对象
    font = None
    title_font = None

    for font_name in chinese_fonts:
        try:
            if font_name is None:
                font = pygame.font.SysFont(None, 28)
                title_font = pygame.font.SysFont(None, 36)
                print("使用系统默认字体")
                break

            # 首先在当前目录查找
            if os.path.exists(font_name):
                font = pygame.font.Font(font_name, 28)
                title_font = pygame.font.Font(font_name, 36)
                print(f"使用字体: {font_name}")
                break

            # 在系统字体目录查找
            for path in font_paths:
                full_path = os.path.join(path, font_name)
                if os.path.exists(full_path):
                    font = pygame.font.Font(full_path, 28)
                    title_font = pygame.font.Font(full_path, 36)
                    print(f"使用字体: {full_path}")
                    break

            if font is not None:
                break

        except Exception as e:
            print(f"加载字体 {font_name} 失败: {e}")
            continue

    # 如果所有中文字体都失败，使用系统字体
    if font is None:
        try:
            font = pygame.font.SysFont(None, 28)
            title_font = pygame.font.SysFont(None, 36)
            print("使用系统默认字体")
        except:
            # 如果系统字体也失败，创建最基本的字体
            print("无法加载任何字体，使用基本渲染")
            font = pygame.font.Font(None, 28)
            title_font = pygame.font.Font(None, 36)

    return font, title_font


# 加载字体
font, title_font = load_fonts()


class ParticleSystem:
    """GPU加速的粒子系统"""

    def __init__(self, num_particles=5000):
        self.num_particles = num_particles

        # 初始化粒子位置 (在CPU上创建，然后移到GPU)
        self.positions = torch.rand(num_particles, 2, device=device) * torch.tensor([WIDTH, HEIGHT], device=device)

        # 初始化粒子速度
        self.velocities = (torch.rand(num_particles, 2, device=device) - 0.5) * 4.0

        # 初始化粒子属性
        self.colors = torch.randint(0, len(COLORS), (num_particles,), device=device)
        self.sizes = torch.rand(num_particles, device=device) * 3 + 1
        self.masses = torch.rand(num_particles, device=device) * 0.5 + 0.5

        # 引力点
        self.gravity_points = torch.tensor([
            [WIDTH / 2, HEIGHT / 2],
            [WIDTH / 4, HEIGHT / 2],
            [3 * WIDTH / 4, HEIGHT / 2],
            [WIDTH / 2, HEIGHT / 4],
            [WIDTH / 2, 3 * HEIGHT / 4]
        ], device=device)

        # 物理参数
        self.gravity_strength = 0.5
        self.repulsion_strength = 1000
        self.damping = 0.99
        self.bounce_factor = 0.8

        # 性能统计
        self.update_times = []
        self.render_times = []
        self.frame_count = 0

    def update(self, mouse_pos, mouse_pressed):
        """更新粒子位置（GPU计算）"""
        start_time = time.time()

        # 转换为张量
        mouse_tensor = torch.tensor(mouse_pos, device=device).unsqueeze(0)

        # 计算鼠标对粒子的影响
        if mouse_pressed[0]:  # 左键：引力
            diff = mouse_tensor - self.positions
            dist_sq = torch.sum(diff ** 2, dim=1) + 0.1  # 避免除以0
            force = self.gravity_strength * 500.0 * diff / dist_sq.view(-1, 1)
            self.velocities += force / self.masses.view(-1, 1)

        if mouse_pressed[2]:  # 右键：斥力
            diff = mouse_tensor - self.positions
            dist_sq = torch.sum(diff ** 2, dim=1) + 0.1
            force = -self.repulsion_strength * diff / dist_sq.view(-1, 1)
            self.velocities += force / self.masses.view(-1, 1)

        # 引力点的影响
        for point in self.gravity_points:
            diff = point - self.positions
            dist_sq = torch.sum(diff ** 2, dim=1) + 100.0
            force = self.gravity_strength * diff / dist_sq.view(-1, 1)
            self.velocities += force / self.masses.view(-1, 1)

        # 粒子间斥力（简化计算，只计算附近粒子）
        # 为了性能，这里只计算每个粒子与随机10个粒子的相互作用
        if self.num_particles > 10:
            indices = torch.randint(0, self.num_particles, (self.num_particles, 10), device=device)
            for i in range(10):
                other_positions = self.positions[indices[:, i]]
                diff = self.positions - other_positions
                dist_sq = torch.sum(diff ** 2, dim=1) + 25.0
                force = -self.repulsion_strength * 0.1 * diff / dist_sq.view(-1, 1)
                self.velocities += force / self.masses.view(-1, 1)

        # 更新速度（应用阻尼）
        self.velocities *= self.damping

        # 更新位置
        self.positions += self.velocities

        # 边界碰撞检测
        # 左边界
        left_mask = self.positions[:, 0] < 0
        self.positions[left_mask, 0] = 0
        self.velocities[left_mask, 0] = -self.velocities[left_mask, 0] * self.bounce_factor

        # 右边界
        right_mask = self.positions[:, 0] > WIDTH
        self.positions[right_mask, 0] = WIDTH
        self.velocities[right_mask, 0] = -self.velocities[right_mask, 0] * self.bounce_factor

        # 上边界
        top_mask = self.positions[:, 1] < 0
        self.positions[top_mask, 1] = 0
        self.velocities[top_mask, 1] = -self.velocities[top_mask, 1] * self.bounce_factor

        # 下边界
        bottom_mask = self.positions[:, 1] > HEIGHT
        self.positions[bottom_mask, 1] = HEIGHT
        self.velocities[bottom_mask, 1] = -self.velocities[bottom_mask, 1] * self.bounce_factor

        # 记录更新时间
        self.update_times.append(time.time() - start_time)
        if len(self.update_times) > 100:
            self.update_times.pop(0)

    def draw(self, surface):
        """绘制粒子（GPU数据传回CPU）"""
        start_time = time.time()

        # 将数据从GPU传回CPU
        positions_cpu = self.positions.cpu().numpy()
        colors_cpu = self.colors.cpu().numpy()
        sizes_cpu = self.sizes.cpu().numpy()

        # 绘制粒子
        for i in range(self.num_particles):
            pos = positions_cpu[i]
            color_idx = colors_cpu[i]
            size = sizes_cpu[i]

            # 根据速度计算颜色强度
            velocity = self.velocities[i].cpu().numpy()
            speed = np.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
            intensity = min(1.0, speed / 5.0)

            # 调整颜色
            base_color = COLORS[color_idx % len(COLORS)]
            adjusted_color = (
                min(255, int(base_color[0] * (0.7 + 0.3 * intensity))),
                min(255, int(base_color[1] * (0.7 + 0.3 * intensity))),
                min(255, int(base_color[2] * (0.7 + 0.3 * intensity)))
            )

            # 绘制粒子
            pygame.draw.circle(surface, adjusted_color, (int(pos[0]), int(pos[1])), int(size))

        # 绘制引力点
        for i, point in enumerate(self.gravity_points.cpu().numpy()):
            color = COLORS[i % len(COLORS)]
            pygame.draw.circle(surface, color, (int(point[0]), int(point[1])), 10)
            pygame.draw.circle(surface, WHITE, (int(point[0]), int(point[1])), 10, 2)

        # 记录渲染时间
        self.render_times.append(time.time() - start_time)
        if len(self.render_times) > 100:
            self.render_times.pop(0)

    def get_performance_stats(self):
        """获取性能统计"""
        avg_update = np.mean(self.update_times) * 1000 if self.update_times else 0
        avg_render = np.mean(self.render_times) * 1000 if self.render_times else 0
        return avg_update, avg_render


class MatrixMultiplicationDemo:
    """矩阵乘法性能演示"""

    def __init__(self):
        self.matrix_size = 100
        self.result_surface = None
        self.computation_time = 0
        self.is_computing = False

    def perform_computation(self):
        """执行矩阵乘法计算"""
        self.is_computing = True

        # 创建随机矩阵
        size = self.matrix_size
        if torch.cuda.is_available():
            a = torch.randn(size, size, device=device)
            b = torch.randn(size, size, device=device)

            # 同步确保准确计时
            torch.cuda.synchronize()
            start = time.time()

            # 执行矩阵乘法
            result = torch.mm(a, b)

            # 同步并记录时间
            torch.cuda.synchronize()
            self.computation_time = (time.time() - start) * 1000  # 转换为毫秒

            # 将结果转换为可视化的表面
            result_cpu = result.cpu().numpy()

            # 归一化到0-255范围
            result_normalized = (result_cpu - result_cpu.min()) / (result_cpu.max() - result_cpu.min() + 1e-8) * 255
            result_int = result_normalized.astype(np.uint8)

            # 创建表面
            self.result_surface = pygame.Surface((size, size))
            for i in range(size):
                for j in range(size):
                    value = result_int[i, j]
                    self.result_surface.set_at((j, i), (value, value, value))
        else:
            # CPU版本
            a = torch.randn(size, size)
            b = torch.randn(size, size)

            start = time.time()
            result = torch.mm(a, b)
            self.computation_time = (time.time() - start) * 1000

            result_np = result.numpy()
            result_normalized = (result_np - result_np.min()) / (result_np.max() - result_np.min() + 1e-8) * 255
            result_int = result_normalized.astype(np.uint8)

            self.result_surface = pygame.Surface((size, size))
            for i in range(size):
                for j in range(size):
                    value = result_int[i, j]
                    self.result_surface.set_at((j, i), (value, value, value))

        self.is_computing = False

    def draw(self, surface, x, y):
        """绘制矩阵乘法演示"""
        # 绘制背景
        pygame.draw.rect(surface, (30, 30, 40), (x, y, 300, 200))
        pygame.draw.rect(surface, (50, 50, 60), (x, y, 300, 200), 2)

        # 绘制标题
        title = title_font.render("Matrix Multiplication Demo", True, CYAN)
        surface.blit(title, (x + 10, y + 10))

        # 绘制矩阵大小信息
        size_text = font.render(f"Matrix Size: {self.matrix_size}x{self.matrix_size}", True, WHITE)
        surface.blit(size_text, (x + 10, y + 50))

        # 绘制计算时间
        if self.computation_time > 0:
            time_text = font.render(f"Compute Time: {self.computation_time:.2f}ms", True, GREEN)
            surface.blit(time_text, (x + 10, y + 80))

        # 绘制计算按钮
        button_color = (70, 120, 70) if not self.is_computing else (100, 100, 100)
        pygame.draw.rect(surface, button_color, (x + 10, y + 120, 120, 40))
        button_text = font.render("Compute" if not self.is_computing else "Computing...", True, WHITE)
        surface.blit(button_text, (x + 20, y + 130))

        # 绘制矩阵大小调整按钮
        pygame.draw.rect(surface, (70, 70, 120), (x + 150, y + 120, 60, 40))
        size_btn_text = font.render("+Size", True, WHITE)
        surface.blit(size_btn_text, (x + 155, y + 130))

        # 绘制结果矩阵
        if self.result_surface:
            scaled_result = pygame.transform.scale(self.result_surface, (100, 100))
            surface.blit(scaled_result, (x + 190, y + 90))


def main():
    # 创建粒子系统
    particle_system = ParticleSystem(num_particles=3000)

    # 创建矩阵乘法演示
    matrix_demo = MatrixMultiplicationDemo()

    # 创建时钟
    clock = pygame.time.Clock()

    # 性能统计
    fps = 0
    last_fps_update = time.time()
    frame_count = 0

    # 主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    particle_system.num_particles = min(20000, particle_system.num_particles + 500)
                    # 重新初始化粒子系统
                    particle_system = ParticleSystem(num_particles=particle_system.num_particles)
                elif event.key == pygame.K_MINUS:
                    particle_system.num_particles = max(100, particle_system.num_particles - 500)
                    # 重新初始化粒子系统
                    particle_system = ParticleSystem(num_particles=particle_system.num_particles)
                elif event.key == pygame.K_r:
                    # 重置粒子系统
                    particle_system = ParticleSystem(num_particles=particle_system.num_particles)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # 检查是否点击了矩阵计算的按钮
                if 10 <= mouse_x <= 130 and 420 <= mouse_y <= 460:
                    if not matrix_demo.is_computing:
                        import threading
                        thread = threading.Thread(target=matrix_demo.perform_computation)
                        thread.start()
                # 检查是否点击了增加矩阵大小的按钮
                elif 150 <= mouse_x <= 210 and 420 <= mouse_y <= 460:
                    matrix_demo.matrix_size = min(500, matrix_demo.matrix_size + 50)

        # 获取鼠标状态
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # 更新粒子系统
        particle_system.update(mouse_pos, mouse_pressed)

        # 清屏
        screen.fill(BLACK)

        # 绘制粒子系统
        particle_system.draw(screen)

        # 绘制矩阵乘法演示
        matrix_demo.draw(screen, 10, 380)

        # 绘制控制说明
        pygame.draw.rect(screen, (40, 40, 50), (WIDTH - 310, 10, 300, 150))
        pygame.draw.rect(screen, (60, 60, 70), (WIDTH - 310, 10, 300, 150), 2)
        title = title_font.render("Controls", True, YELLOW)
        screen.blit(title, (WIDTH - 300, 15))

        controls = [
            "Left Click: Attract particles",
            "Right Click: Repel particles",
            "+/=: Increase particle count",
            "-: Decrease particle count",
            "R: Reset particle system",
            "ESC: Exit program"
        ]

        for i, text in enumerate(controls):
            control_text = font.render(text, True, WHITE)
            screen.blit(control_text, (WIDTH - 300, 50 + i * 20))

        # 绘制性能统计
        avg_update, avg_render = particle_system.get_performance_stats()

        pygame.draw.rect(screen, (40, 40, 50), (WIDTH - 310, HEIGHT - 130, 300, 120))
        pygame.draw.rect(screen, (60, 60, 70), (WIDTH - 310, HEIGHT - 130, 300, 120), 2)
        stats_title = title_font.render("Performance Stats", True, YELLOW)
        screen.blit(stats_title, (WIDTH - 300, HEIGHT - 125))

        stats = [
            f"Particles: {particle_system.num_particles}",
            f"GPU Accelerated: {'Yes' if torch.cuda.is_available() else 'No'}",
            f"Update Time: {avg_update:.1f}ms",
            f"Render Time: {avg_render:.1f}ms",
            f"FPS: {fps}"
        ]

        for i, stat in enumerate(stats):
            stat_text = font.render(stat, True, WHITE)
            screen.blit(stat_text, (WIDTH - 300, HEIGHT - 95 + i * 20))

        # 绘制设备信息
        device_text = font.render(f"Device: {device}", True, CYAN)
        screen.blit(device_text, (10, 10))

        # 更新显示
        pygame.display.flip()

        # 计算FPS
        frame_count += 1
        current_time = time.time()
        if current_time - last_fps_update >= 1.0:
            fps = frame_count
            frame_count = 0
            last_fps_update = current_time

        # 控制帧率
        clock.tick(60)

    # 退出游戏
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()