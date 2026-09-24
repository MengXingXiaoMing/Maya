# coding=gbk
import math

import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import time
import multiprocessing as mp
import threading
import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np

import os
import time
import threading
import os
import time
from collections import OrderedDict
import mmap
import os
import pickle  # 需要导入pickle模块

class MultiModelManager:
    """多模型管理器 - 负责管理多个模型的数据和状态"""
    def __init__(self):
        self.models = OrderedDict()  # 模型字典: {model_id: model_data}
        self.file_to_model_map = {}  # 文件到模型的映射
        self.dirty_models = set()  # 需要更新的模型标记

    def add_model(self, model_id, shared_file, initial_data=None):
        """添加一个新模型到管理器"""
        self.models[model_id] = {
            'vertices': initial_data[0] if initial_data else [],
            'faces': initial_data[1] if initial_data else [],
            'tex_coords': initial_data[2] if initial_data else [],
            'normals': initial_data[3] if initial_data and len(initial_data) > 3 else [],
            'position': [0, 0, 0],  # 模型位置（可独立设置）
            'rotation': [0, 0, 0],  # 模型旋转（可独立设置）
            'visible': True,  # 可见性
            'last_updated': time.time()  # 最后更新时间
        }
        self.file_to_model_map[shared_file] = model_id
        print(f"? 添加模型: {model_id} -> {shared_file}")

    def update_model(self, model_id, vertices, faces, tex_coords, normals=None):
        """更新特定模型的数据"""
        if model_id in self.models:
            self.models[model_id]['vertices'] = vertices
            self.models[model_id]['faces'] = faces
            self.models[model_id]['tex_coords'] = tex_coords
            if normals:
                self.models[model_id]['normals'] = normals
            self.models[model_id]['last_updated'] = time.time()
            self.dirty_models.add(model_id)

    def get_model_data(self, model_id):
        """获取模型数据"""
        return self.models.get(model_id)

    def get_all_models(self):
        """获取所有模型"""
        return self.models

    def get_model_by_file(self, shared_file):
        """通过文件路径获取模型ID"""
        return self.file_to_model_map.get(shared_file)


class MultiFileMonitor:
    """多文件监控器 - 监控多个共享内存文件的变化"""

    def __init__(self, check_interval=0.3):
        self.check_interval = check_interval
        self.monitored_files = {}  # {file_path: last_modified_time}
        self.model_manager = None
        self.monitor_thread = None
        self.stop_monitoring = False

    def add_file_monitor(self, file_path, model_id):
        """添加文件监控"""
        if os.path.exists(file_path):
            self.monitored_files[file_path] = {
                'last_modified': os.path.getmtime(file_path),
                'model_id': model_id
            }
            print(f"? 开始监控文件: {file_path} -> 模型: {model_id}")
        else:
            print(f"?? 文件不存在: {file_path}")

    def set_model_manager(self, model_manager):
        """设置模型管理器"""
        self.model_manager = model_manager

    def start_monitoring(self):
        """启动多文件监控线程"""
        if not self.monitored_files:
            print("?? 没有要监控的文件")
            return

        self.stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self._monitoring_worker, daemon=True)
        self.monitor_thread.start()
        print(f"? 启动多文件监控，监控 {len(self.monitored_files)} 个文件")

    def _monitoring_worker(self):
        """监控工作线程"""
        while not self.stop_monitoring:
            try:
                for file_path, file_info in self.monitored_files.items():
                    if not os.path.exists(file_path):
                        continue

                    current_modified = os.path.getmtime(file_path)
                    if current_modified > file_info['last_modified']:
                        print(f"? 检测到文件更新: {file_path}")
                        file_info['last_modified'] = current_modified

                        # 读取更新数据
                        data = read_from_shared_memory(file_path)
                        if data and self.model_manager:
                            model_id = file_info['model_id']
                            # 根据数据长度决定是否包含法线
                            if len(data) >= 4:
                                self.model_manager.update_model(model_id, data[0], data[1], data[2], data[3])
                            else:
                                self.model_manager.update_model(model_id, data[0], data[1], data[2])

            except Exception as e:
                print(f"? 文件监控错误: {e}")

            time.sleep(self.check_interval)

    def stop(self):  # 将 stop_monitoring 改为 stop
        """停止监控"""
        self.stop_monitoring = True
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("?? 多文件监控已停止")


class ModelViewer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.vertices = []
        self.normals = []
        self.faces = []
        self.tex_coords = []
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_z = -5
        self.is_orthographic = False  # 默认透视投影
        self.mouse_dragging = False
        self.last_mouse_pos = (0, 0)
        # 添加正交投影的缩放控制变量
        self.ortho_zoom = 1.0  # 正交投影缩放因子，1.0为原始大小
        self.ortho_size = 5  # 正交投影基础大小
        self.texture_id = 0
        # 初始化窗口
        self.init_window()


    def init_window(self):
        """初始化Pygame和OpenGL窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D模型查看器 - 半透明贴图测试")
        # pygame.display.set_caption("3D模型查看器 - 按空格键切换正交/透视视图")

        # 设置初始透视投影[1,8](@ref)
        self.set_perspective()

        # 启用深度测试
        glEnable(GL_DEPTH_TEST)

        # # 设置基本光照
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])

        # 设置混合参数（新增）
        glEnable(GL_BLEND)  # 启用混合[1,3](@ref)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # 设置混合函数[3,6](@ref)

        # 启用背面剔除（关键添加）
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)  # 剔除背面（默认值，可省略）

        # # 启用深度测试（关键添加）
        # glEnable(GL_DEPTH_TEST)
        # glDepthFunc(GL_LESS)  # 默认值：近的物体遮挡远的物体
        #
        # # 设置深度缓冲清除值
        # glClearDepth(1.0)

        # 禁用光照以确保颜色一致（根据你的需求选择）
        glDisable(GL_LIGHTING)

        print("混合模式已启用，准备加载半透明纹理")
    def set_perspective(self):
        """设置透视投影[1,8,10](@ref)"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # 设置透视投影：45度视野，当前宽高比，近裁剪面0.1，远裁剪面100[1](@ref)
        gluPerspective(45, (self.width / self.height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def set_orthographic(self):
        """设置正交投影[6](@ref)"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # 计算正交投影参数，应用缩放因子
        aspect_ratio = self.width / self.height
        # 使用缩放因子调整显示范围
        zoomed_size = self.ortho_size * self.ortho_zoom

        # 根据窗口宽高比调整正交投影范围
        if aspect_ratio > 1:
            left = -zoomed_size * aspect_ratio
            right = zoomed_size * aspect_ratio
            bottom = -zoomed_size
            top = zoomed_size
        else:
            left = -zoomed_size
            right = zoomed_size
            bottom = -zoomed_size / aspect_ratio
            top = zoomed_size / aspect_ratio

        glOrtho(left, right, bottom, top, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def load_obj(self, filename):
        """加载OBJ格式的3D模型[1](@ref)"""
        self.vertices = []
        self.faces = []

        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith('v '):  # 顶点
                        vertex = list(map(float, line.strip().split()[1:4]))
                        self.vertices.append(vertex)
                    elif line.startswith('f '):  # 面
                        face = []
                        for vertex_data in line.strip().split()[1:]:
                            # 处理顶点索引（只取顶点位置索引，忽略纹理和法线索引）
                            vertex_index = int(vertex_data.split('/')[0]) - 1
                            face.append(vertex_index)
                        self.faces.append(face)
            print(f"模型加载成功: {len(self.vertices)} 个顶点, {len(self.faces)} 个面")
        except Exception as e:
            print(f"加载模型失败: {e}")
            # 创建一个简单的立方体作为默认模型
            self.create_default_cube()

    def load_maya_obj(self, filename):
        """加载OBJ格式的3D模型[1](@ref)"""
        self.vertices = []
        self.faces = []

        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith('v '):  # 顶点
                        vertex = list(map(float, line.strip().split()[1:4]))
                        self.vertices.append(vertex)
                    elif line.startswith('f '):  # 面
                        face = []
                        for vertex_data in line.strip().split()[1:]:
                            # 处理顶点索引（只取顶点位置索引，忽略纹理和法线索引）
                            vertex_index = int(vertex_data.split('/')[0]) - 1
                            face.append(vertex_index)
                        self.faces.append(face)
            print(f"模型加载成功: {len(self.vertices)} 个顶点, {len(self.faces)} 个面")
        except Exception as e:
            print(f"加载模型失败: {e}")
            # 创建一个简单的立方体作为默认模型
            self.create_default_cube()

    def load_texture(self, image_path):
        """加载纹理并返回纹理ID"""
        try:
            # 使用PIL加载图像
            from PIL import Image
            img = Image.open(image_path)

            # 确保图像是RGBA格式（支持透明度）
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 翻转图像（OpenGL坐标原点在左下角）
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = img.tobytes()

            # 生成纹理ID（关键步骤）
            texture_id = glGenTextures(1)  # 注意：这里返回的是整数，不是列表

            if texture_id <= 0:
                print("错误：纹理生成失败")
                self.texture_id = None  # 确保设置为None
                return None

            # 绑定纹理并设置参数
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # 上传纹理数据
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height,
                         0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            self.texture_id = texture_id
            print(f"纹理加载成功: {image_path}, ID: {texture_id}")
            return texture_id  # 返回整数纹理ID



            # ... [原有代码] ...

            # 生成纹理ID（关键步骤）
            texture_id = glGenTextures(1)  # 注意：这里返回的是整数，不是列表

            if texture_id <= 0:
                print("错误：纹理生成失败")
                self.texture_id = None  # 确保设置为None
                return None

            # ... [绑定纹理并上传数据] ...

            self.texture_id = texture_id
            print(f"纹理加载成功: {image_path}, ID: {texture_id}")
            return texture_id

        except Exception as e:
            print(f"纹理加载失败: {e}")
            self.texture_id = None  # 确保设置为None
            return None

    def draw_normals(self):
        """绘制法线用于调试（可选）"""
        if not self.vertices or not hasattr(self, 'normals'):
            return

        glDisable(GL_TEXTURE_2D)
        glColor3f(1.0, 1.0, 1.0)  # 红色法线
        glBegin(GL_LINES)

        for i, vertex in enumerate(self.vertices):
            if i < len(self.normals):
                normal = self.normals[i]
                # 顶点位置
                glVertex3fv(vertex)
                # 法线方向（缩放以便观察）
                glVertex3f(vertex[0] + normal[0] * 0.2,
                           vertex[1] + normal[1] * 0.2,
                           vertex[2] + normal[2] * 0.2)

        glEnd()
        glEnable(GL_TEXTURE_2D)

    def draw_model(self):
        print('绘制法线')
        """绘制3D模型"""
        if not self.vertices or not self.faces:
            return
        # 启用纹理和混合（确保在绘制前设置）
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 绑定纹理（如果你有纹理的话）
        # 验证纹理ID有效性
        print('纹理ID：',self.texture_id)
        if hasattr(self, 'texture_id') and self.texture_id is not None and self.texture_id > 0:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            print(f"绑定纹理ID: {self.texture_id}")
        else:
            print("警告：纹理ID无效，使用纯色渲染")
            glDisable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 0.5)  # 回退到半透明白色

        # 禁用光照，确保颜色不受光照影响
        glDisable(GL_LIGHTING)

        # # 设置纯色（例如白色）
        # glColor3f(1.0, 1.0, 1.0)  # RGB值范围0.0-1.0
        # # 设置颜色（包含Alpha值）
        # glColor4f(1.0, 1.0, 1.0, 0.5)  # 白色，50%透明度[1,6](@ref)

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            # 如果当前面是四边形（4个顶点），则拆分为两个三角形
            if len(face) == 4:
                # 将四边形拆分为两个三角形：[v0, v1, v2] 和 [v0, v2, v3]
                triangle1 = [face[0], face[1], face[2]]  # 第一个三角形
                triangle2 = [face[0], face[2], face[3]]  # 第二个三角形

                # 绘制第一个三角形
                for vertex_index in triangle1:
                    if vertex_index < len(self.vertices):
                        # 设置纹理坐标（关键添加）
                        if vertex_index < len(self.tex_coords):
                            glTexCoord2fv(self.tex_coords[vertex_index])
                        glVertex3fv(self.vertices[vertex_index])
                # 绘制第二个三角形
                for vertex_index in triangle2:
                    if vertex_index < len(self.vertices):
                        # 设置纹理坐标（关键添加）
                        if vertex_index < len(self.tex_coords):
                            glTexCoord2fv(self.tex_coords[vertex_index])
                        glVertex3fv(self.vertices[vertex_index])
            else:
                # 对于非四边形（如三角形），按原样处理
                for vertex_index in face:
                    if vertex_index < len(self.vertices):
                        # 设置纹理坐标（关键添加）
                        if vertex_index < len(self.tex_coords):
                            glTexCoord2fv(self.tex_coords[vertex_index])
                        glVertex3fv(self.vertices[vertex_index])

        for i, vertex in enumerate(self.vertices):
            if i < len(self.normals):
                normal = self.normals[i]
                # 顶点位置
                glVertex3fv(vertex)
                # 法线方向（缩放以便观察）
                glVertex3f(vertex[0] + normal[0] * 0.2,
                           vertex[1] + normal[1] * 0.2,
                           vertex[2] + normal[2] * 0.2)

        glEnd()
        self.draw_normals()

        # # 禁用纹理（可选）
        # glDisable(GL_TEXTURE_2D)

    def handle_events(self):
        """处理用户输入事件 - 修复版本"""
        running = True

        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_SPACE:
                    self.is_orthographic = not self.is_orthographic
                    if self.is_orthographic:
                        self.set_orthographic()
                        print("切换到正交视图")
                    else:
                        self.set_perspective()
                        print("切换到透视视图")
                elif event.key == K_r:  # R键重置视图
                    self._reset_view()
                elif event.key == K_c:  # C键重置相机
                    self._reset_camera()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    self.mouse_dragging = True
                    self.last_mouse_pos = event.pos
                    print(f"鼠标按下: {event.pos}")
                elif event.button == 4:  # 滚轮上滚 - 放大
                    self._handle_zoom_in()
                elif event.button == 5:  # 滚轮下滚 - 缩小
                    self._handle_zoom_out()

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    print("鼠标释放")

            elif event.type == MOUSEMOTION:
                if self.mouse_dragging:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5
                    self.last_mouse_pos = event.pos
                    print(f"鼠标拖动: dx={dx}, dy={dy}, 新旋转: X={self.rotation_x}, Y={self.rotation_y}")

        return True

    def _reset_view(self):
        """重置视图位置和旋转"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_z = -5
        self.ortho_zoom = 1.0  # 重置正交缩放因子
        if self.is_orthographic:
            self.set_orthographic()  # 重新设置正交投影
        print("视图已重置")

    def _reset_camera(self):
        """重置相机位置"""
        self.translation_z = -5
        print("相机位置已重置")

    def _handle_zoom_in(self):
        """处理放大操作"""
        if self.is_orthographic:
            # 正交模式：减小视景体范围实现放大
            self.ortho_zoom *= 0.9  # 乘以小于1的数实现放大
            self.set_orthographic()  # 更新正交投影
            print(f"正交放大: 新缩放因子={self.ortho_zoom}")
        else:
            # 透视模式：传统方式
            self.translation_z += 0.5
            print(f"透视放大: 新Z位置={self.translation_z}")

    def _handle_zoom_out(self):
        """处理缩小操作"""
        if self.is_orthographic:
            # 正交模式：增大视景体范围实现缩小
            self.ortho_zoom /= 0.9  # 除以小于1的数实现缩小
            self.set_orthographic()  # 更新正交投影
            print(f"正交缩小: 新缩放因子={self.ortho_zoom}")
        else:
            # 透视模式：传统方式
            self.translation_z -= 0.5
            print(f"透视缩小: 新Z位置={self.translation_z}")

    def render(self):
        """渲染场景 - 确保视图变换被应用"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 应用视图变换 - 确保这些调用存在
        glTranslatef(0.0, 0.0, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # 绘制模型
        self.draw_model()

        pygame.display.flip()

    def run(self, model_file=None):
        """运行主循环"""
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.render()
            clock.tick(60)  # 限制60FPS

        pygame.quit()


# class AutoReloadModelViewer(ModelViewer):
#     def __init__(self, width=800, height=600, shared_file=None, check_interval=1.0):
#         super().__init__(width, height)
#         self.shared_file = shared_file
#         self.check_interval = check_interval
#         self.last_modified = 0
#         self.reload_thread = None
#         self.stop_reload = False
#
#         # 启动自动重载线程
#         self.start_auto_reload()
#
#     def start_auto_reload(self):
#         """启动自动重载线程"""
#         if self.shared_file and os.path.exists(self.shared_file):
#             self.last_modified = os.path.getmtime(self.shared_file)
#             self.stop_reload = False
#             self.reload_thread = threading.Thread(target=self._auto_reload_worker, daemon=True)
#             self.reload_thread.start()
#             print(f"开始监控文件: {self.shared_file}")
#
#     def _auto_reload_worker(self):
#         """自动重载的工作线程"""
#         while not self.stop_reload:
#             try:
#                 current_modified = os.path.getmtime(self.shared_file)
#                 if current_modified > self.last_modified:
#                     print("检测到文件更新，重新加载数据...")
#                     self.last_modified = current_modified
#                     self.reload_shared_data()
#             except Exception as e:
#                 print(f"监控文件时出错: {e}")
#
#             time.sleep(self.check_interval)
#
#     def reload_shared_data(self):
#         """重载共享内存数据"""
#         data = read_from_shared_memory(self.shared_file)
#         if data:
#             # 使用线程锁确保数据安全更新（如果需要）
#             self.vertices = data[0]
#             self.faces = data[1]
#             self.tex_coords = data[2]
#             print("数据重载完成")
#
#     def stop_auto_reload(self):
#         """停止自动重载"""
#         self.stop_reload = True
#         if self.reload_thread:
#             self.reload_thread.join(timeout=5)

class MultiModelViewer(ModelViewer):
    """支持多模型的查看器"""

    def __init__(self, width=800, height=600):
        super().__init__(width, height)

        # 多模型管理核心组件
        self.model_manager = MultiModelManager()
        self.file_monitor = MultiFileMonitor(check_interval=0.01)
        self.file_monitor.set_model_manager(self.model_manager)

        # 模型显示列表缓存（性能优化）
        self.display_lists = {}

        # 当前激活的模型（用于独立控制）
        self.active_model_id = None
        print(f"初始相机位置: translation_z={self.translation_z}")


    def add_model_from_file(self, model_id, shared_file, initial_position=None):
        """从共享内存文件添加模型"""
        # 读取初始数据
        data = read_from_shared_memory(shared_file)
        if not data:
            print(f"? 无法从 {shared_file} 加载模型数据")
            return False

        # 设置初始位置
        if initial_position is None:
            initial_position = [0, 0, 0]

        # 添加到模型管理器
        self.model_manager.add_model(model_id, shared_file, data)

        # 更新模型位置
        model_data = self.model_manager.get_model_data(model_id)
        if model_data:
            model_data['position'] = initial_position

        # 添加到文件监控
        self.file_monitor.add_file_monitor(shared_file, model_id)

        # 创建显示列表（性能优化）
        self._create_display_list(model_id)

        # 设置第一个模型为激活模型
        if self.active_model_id is None:
            self.active_model_id = model_id

        return True

    def _create_display_list(self, model_id):
        """为模型创建OpenGL显示列表（性能优化）"""
        model_data = self.model_manager.get_model_data(model_id)
        if not model_data:
            return

        # 删除旧的显示列表（如果存在）
        if model_id in self.display_lists:
            glDeleteLists(self.display_lists[model_id], 1)

        # 创建新的显示列表
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)

        # 编译模型绘制代码
        self._compile_model_drawing(model_data)

        glEndList()
        self.display_lists[model_id] = display_list

    def _compile_model_drawing(self, model_data):
        """编译模型绘制代码到显示列表"""
        vertices = model_data['vertices']
        faces = model_data['faces']
        tex_coords = model_data['tex_coords']

        if not vertices or not faces:
            return

        # 设置渲染状态
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 修复：添加更安全的纹理ID检查
        print('纹理ID：', self.texture_id)
        if hasattr(self, 'texture_id') and self.texture_id is not None and self.texture_id > 0:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            # 如果纹理ID无效，禁用纹理
            glDisable(GL_TEXTURE_2D)
            print("?? 纹理ID无效，使用纯色渲染")
            glColor4f(1.0, 1.0, 1.0, 0.5)  # 回退到半透明白色

        glDisable(GL_LIGHTING)

        # 绘制模型几何
        glBegin(GL_TRIANGLES)
        for face in faces:
            if len(face) == 4:
                # 四边形拆分为两个三角形
                triangles = [[face[0], face[1], face[2]], [face[0], face[2], face[3]]]
                for triangle in triangles:
                    for vertex_index in triangle:
                        if vertex_index < len(vertices) and vertex_index < len(tex_coords):
                            glTexCoord2fv(tex_coords[vertex_index])
                            glVertex3fv(vertices[vertex_index])
            else:
                for vertex_index in face:
                    if vertex_index < len(vertices) and vertex_index < len(tex_coords):
                        glTexCoord2fv(tex_coords[vertex_index])
                        glVertex3fv(vertices[vertex_index])
        glEnd()

    def draw_model(self):
        """重写绘制方法 - 添加渲染顺序控制"""
        # 检查是否有模型需要更新显示列表
        dirty_models = self.model_manager.dirty_models.copy()
        for model_id in dirty_models:
            if model_id in self.display_lists:
                print(f"? 更新模型显示列表: {model_id}")
                self._create_display_list(model_id)
                self.model_manager.dirty_models.remove(model_id)

        # 收集所有可见模型
        models_to_draw = []
        for model_id, model_data in self.model_manager.get_all_models().items():
            if not model_data['visible']:
                continue
            # print('模型id：', model_id)
            models_to_draw.append((model_id, model_data))

        # 按深度排序（从远到近）
        models_to_draw = self._sort_models_by_depth(models_to_draw)

        # 绘制所有可见模型
        for model_id, model_data in models_to_draw:
            self._draw_single_model(model_id, model_data)

    def _sort_models_by_depth(self, models):
        """按模型深度排序（从远到近）"""
        # 计算相机位置（视图空间原点）
        camera_pos = [0, 0, -self.translation_z]

        models_with_depth = []
        for model_id, model_data in models:
            # 计算模型位置到相机的距离
            pos = model_data['position']
            dx = pos[0] - camera_pos[0]
            dy = pos[1] - camera_pos[1]
            dz = pos[2] - camera_pos[2]
            depth = math.sqrt(dx * dx + dy * dy + dz * dz)

            models_with_depth.append((depth, model_id, model_data))

        # 按深度从大到小排序（远到近）
        models_with_depth.sort(key=lambda x: x[0], reverse=True)

        # 返回排序后的模型列表（去掉深度值）
        return [(model_id, model_data) for depth, model_id, model_data in models_with_depth]

    def _draw_single_model(self, model_id, model_data):
        """绘制单个模型"""
        glPushMatrix()

        # 应用模型变换
        pos = model_data['position']
        rot = model_data['rotation']
        glTranslatef(pos[0], pos[1], pos[2])
        glRotatef(rot[0], 1, 0, 0)
        glRotatef(rot[1], 0, 1, 0)
        glRotatef(rot[2], 0, 0, 1)

        # 使用显示列表绘制
        if model_id in self.display_lists:
            glCallList(self.display_lists[model_id])
        else:
            self._compile_model_drawing(model_data)

        glPopMatrix()

    def set_model_visibility(self, model_id, visible):
        """设置模型可见性"""
        model_data = self.model_manager.get_model_data(model_id)
        if model_data:
            model_data['visible'] = visible
            print(f"?? 模型 {model_id} 可见性: {visible}")

    def set_model_position(self, model_id, position):
        """设置模型位置"""
        model_data = self.model_manager.get_model_data(model_id)
        if model_data:
            model_data['position'] = position
            print(f"? 设置模型 {model_id} 位置: {position}")

    def set_active_model(self, model_id):
        """设置当前激活的模型（用于独立控制）"""
        if model_id in self.model_manager.models:
            self.active_model_id = model_id
            print(f"? 激活模型: {model_id}")

    def _toggle_model_visibility(self, model_id):
        """切换模型可见性"""
        model_data = self.model_manager.get_model_data(model_id)
        if model_data:
            new_visibility = not model_data['visible']
            self.set_model_visibility(model_id, new_visibility)

    def _reset_all_models(self):
        """重置所有模型位置和视角"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_z = -5
        self.ortho_zoom = 1.0

        # 重置所有模型位置
        for model_id in self.model_manager.models:
            self.set_model_position(model_id, [0, 0, 0])

        if self.is_orthographic:
            self.set_orthographic()

    def start_monitoring(self):
        """启动文件监控"""

        self.file_monitor.start_monitoring()

    def cleanup(self):
        """清理资源"""
        # 停止文件监控
        self.file_monitor.stop()

        # 清理显示列表 - 添加有效性检查
        for model_id, display_list in list(self.display_lists.items()):
            if display_list > 0:  # 只删除有效的显示列表
                try:
                    glDeleteLists(display_list, 1)
                    print(f"? 删除显示列表: {display_list}")
                except Exception as e:
                    print(f"? 删除显示列表错误: {e}")
            else:
                print(f"?? 跳过无效显示列表: {display_list}")

        self.display_lists.clear()

    def handle_events(self):
        """处理用户输入事件 - 修复版本"""
        running = True

        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_SPACE:
                    self.is_orthographic = not self.is_orthographic
                    if self.is_orthographic:
                        self.set_orthographic()
                        print("切换到正交视图")
                    else:
                        self.set_perspective()
                        print("切换到透视视图")
                elif event.key == K_r:  # R键重置视图
                    self._reset_view()
                elif event.key == K_c:  # C键重置相机
                    self._reset_camera()
                elif event.key == K_p:  # P键渲染PNG
                    self.render_to_png()
                elif event.key == K_b:  # B键批量渲染
                    self.render_high_quality_sequence()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    self.mouse_dragging = True
                    self.last_mouse_pos = event.pos
                    print(f"鼠标按下: {event.pos}")
                elif event.button == 4:  # 滚轮上滚 - 放大
                    self._handle_zoom_in()
                elif event.button == 5:  # 滚轮下滚 - 缩小
                    self._handle_zoom_out()

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    print("鼠标释放")

            elif event.type == MOUSEMOTION:
                if self.mouse_dragging:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5
                    self.last_mouse_pos = event.pos
                    # print(f"鼠标拖动: dx={dx}, dy={dy}, 新旋转: X={self.rotation_x}, Y={self.rotation_y}")

        return True


    def render_to_png(self, filename=None, width=None, height=None):
        """将当前3D场景渲染为PNG图片"""
        if filename is None:
            filename = f"render_{time.strftime('%Y%m%d_%H%M%S')}.png"

        # 设置渲染尺寸（默认为窗口尺寸）
        render_width = width or self.width
        render_height = height or self.height

        try:
            from PIL import Image

            # 创建离屏渲染缓冲区
            self._setup_offscreen_render(render_width, render_height)

            # 渲染场景
            self.render_offscreen()

            # 读取像素数据
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, render_width, render_height, GL_RGBA, GL_UNSIGNED_BYTE)

            # 转换为PIL图像（需要翻转Y轴）
            img = Image.frombytes("RGBA", (render_width, render_height), data)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

            # 保存为PNG
            img.save(filename, "PNG")

            # 恢复正常渲染设置
            self._restore_normal_render()

            print(f"? PNG图片已保存: {filename}")
            return True

        except Exception as e:
            print(f"? 渲染PNG失败: {e}")
            self._restore_normal_render()
            return False

    def _setup_offscreen_render(self, width, height):
        """设置离屏渲染"""
        # 保存当前视口和投影矩阵
        self.saved_viewport = glGetIntegerv(GL_VIEWPORT)
        self.saved_projection_matrix = glGetDoublev(GL_PROJECTION_MATRIX)

        # 设置离屏渲染视口
        glViewport(0, 0, width, height)

        # 设置投影矩阵（根据当前模式）
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.is_orthographic:
            self.set_orthographic_for_size(width, height)
        else:
            gluPerspective(45, (width / height), 0.1, 1000.0)

        glMatrixMode(GL_MODELVIEW)

    def set_orthographic_for_size(self, width, height):
        """为指定尺寸设置正交投影"""
        aspect_ratio = width / height
        zoomed_size = self.ortho_size * self.ortho_zoom

        if aspect_ratio > 1:
            left = -zoomed_size * aspect_ratio
            right = zoomed_size * aspect_ratio
            bottom = -zoomed_size
            top = zoomed_size
        else:
            left = -zoomed_size
            right = zoomed_size
            bottom = -zoomed_size / aspect_ratio
            top = zoomed_size / aspect_ratio

        glOrtho(left, right, bottom, top, 0.1, 1000.0)

    def render_high_quality_sequence(self, output_dir="renders",
                                     num_frames=10,
                                     resolution_scale=2.0):
        """渲染高质量旋转序列"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        # 保存初始状态
        initial_rotation_y = self.rotation_y
        initial_width, initial_height = self.width, self.height

        try:
            # 设置高分辨率渲染
            render_width = int(self.width * resolution_scale)
            render_height = int(self.height * resolution_scale)

            for frame in range(num_frames):
                # 计算旋转角度（完整旋转）
                self.rotation_y = initial_rotation_y + (frame / num_frames) * 360.0

                # 渲染单帧
                filename = os.path.join(output_dir, f"frame_{frame:04d}.png")
                success = self.render_to_png(filename, render_width, render_height)

                if not success:
                    print(f"? 第{frame}帧渲染失败")
                    break

                print(f"? 进度: {frame + 1}/{num_frames} ({((frame + 1) / num_frames) * 100:.1f}%)")

            # 恢复初始状态
            self.rotation_y = initial_rotation_y
            print(f"? 序列渲染完成: {output_dir}")

        except Exception as e:
            print(f"? 批量渲染失败: {e}")
            # 恢复初始状态
            self.rotation_y = initial_rotation_y

    def render_offscreen(self):
        """离屏渲染"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 应用视图变换
        glTranslatef(0.0, 0.0, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # 绘制模型
        self.draw_model()

    def _restore_normal_render(self):
        """恢复正常渲染设置"""
        if hasattr(self, 'saved_viewport'):
            glViewport(*self.saved_viewport)

        if hasattr(self, 'saved_projection_matrix'):
            glMatrixMode(GL_PROJECTION)
            glLoadMatrixd(self.saved_projection_matrix)
            glMatrixMode(GL_MODELVIEW)

    def render_with_custom_settings(self, filename=None,
                                    background_color=(0, 0, 0, 1),
                                    resolution=(1920, 1080),
                                    anti_aliasing=True):
        """使用自定义设置渲染PNG"""
        if filename is None:
            filename = f"custom_render_{time.strftime('%Y%m%d_%H%M%S')}.png"

        try:
            from PIL import Image

            width, height = resolution

            # 设置离屏渲染
            self._setup_offscreen_render(width, height)

            # 设置背景色
            glClearColor(*background_color)

            # 如果启用抗锯齿（需要OpenGL扩展）
            if anti_aliasing:
                glEnable(GL_MULTISAMPLE)

            # 渲染场景
            self.render_offscreen()

            # 读取像素数据
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)

            # 转换为PIL图像
            img = Image.frombytes("RGBA", (width, height), data)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

            # 后处理：锐化、调整对比度等
            if anti_aliasing:
                # 简单的锐化滤波
                from PIL import ImageFilter
                img = img.filter(ImageFilter.SHARPEN)

            # 保存为高质量PNG
            img.save(filename, "PNG", optimize=True, quality=95)

            # 恢复设置
            if anti_aliasing:
                glDisable(GL_MULTISAMPLE)
            self._restore_normal_render()

            print(f"? 自定义渲染完成: {filename}")
            return True

        except Exception as e:
            print(f"? 自定义渲染失败: {e}")
            self._restore_normal_render()
            return False


def read_from_shared_memory(shared_file):
    if not os.path.exists(shared_file):
        print("Shared memory file not found.")
        return None
    try:
        with open(shared_file, "r+b") as f:
            with mmap.mmap(f.fileno(), 0) as mm:
                mm.seek(0)
                # 读取数据长度（前4字节）
                data_size_bytes = mm.read(4)
                data_size = int.from_bytes(data_size_bytes, byteorder='big')

                # 读取实际数据
                data_bytes = mm.read(data_size)

                # 使用pickle反序列化，而不是UTF-8解码
                data = pickle.loads(data_bytes)

                print(f"Data read from shared memory: {data}")
                return data
    except Exception as e:
        print(f"Error reading shared memory: {e}")
        return None


class AutoReloadModelViewer(ModelViewer):
    def __init__(self, width=800, height=600, shared_file=None, check_interval=1.0):
        super().__init__(width, height)
        self.shared_file = shared_file
        self.check_interval = check_interval
        self.last_modified = 0
        self.reload_thread = None
        self.stop_reload = False
        self.data_lock = threading.Lock()  # 线程安全锁

        # 确保共享文件存在
        if self.shared_file and os.path.exists(self.shared_file):
            self.last_modified = os.path.getmtime(self.shared_file)

        # 启动自动重载线程
        self.start_auto_reload()

    def start_auto_reload(self):
        """启动自动重载线程"""
        if self.shared_file and os.path.exists(self.shared_file):
            self.stop_reload = False
            self.reload_thread = threading.Thread(
                target=self._auto_reload_worker,
                daemon=True
            )
            self.reload_thread.start()
            print(f"? 开始监控文件: {self.shared_file}")
        else:
            print(f"?? 文件不存在: {self.shared_file}")

    def _auto_reload_worker(self):
        """自动重载的工作线程 - 优化版本"""
        while not self.stop_reload:
            try:
                if not os.path.exists(self.shared_file):
                    time.sleep(self.check_interval)
                    continue

                current_modified = os.path.getmtime(self.shared_file)
                if current_modified > self.last_modified:
                    print(f"? 检测到文件更新: {self.shared_file}")
                    self.last_modified = current_modified

                    # 添加延迟，确保文件完全写入
                    time.sleep(0.05)

                    self.reload_shared_data()
            except Exception as e:
                print(f"? 监控文件时出错: {e}")
                # 添加错误恢复延迟
                time.sleep(1.0)

            # 添加短暂休眠，减少CPU占用
            time.sleep(self.check_interval)

    def reload_shared_data(self):
        """重载共享内存数据 - 线程安全版本"""
        try:
            data = read_from_shared_memory(self.shared_file)
            if data:
                # 使用线程锁确保数据安全更新
                with self.data_lock:
                    self.vertices = data[0]
                    self.faces = data[1]
                    self.tex_coords = data[2]
                    if len(data) > 3:
                        self.normals = data[3]
                    print("? 数据安全重载完成")
        except Exception as e:
            print(f"? 重载数据错误: {e}")

    def stop_auto_reload(self):
        """安全停止自动重载"""
        self.stop_reload = True
        if self.reload_thread:
            self.reload_thread.join(timeout=2.0)
            print("?? 自动重载已停止")

        # 确保线程已退出
        if self.reload_thread and self.reload_thread.is_alive():
            print("?? 重载线程未正常退出，强制终止")
            # 注意：在Python中无法安全终止线程
            # 建议设置超时后忽略

    def draw_model(self):
        """绘制3D模型 - 线程安全版本"""
        # 使用线程锁保护数据访问
        with self.data_lock:
            vertices = self.vertices.copy() if self.vertices else []
            faces = self.faces.copy() if self.faces else []
            tex_coords = self.tex_coords.copy() if hasattr(self, 'tex_coords') else []
            normals = self.normals.copy() if hasattr(self, 'normals') else []

        if not vertices or not faces:
            return

        # 启用纹理和混合
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 绑定纹理
        if hasattr(self, 'texture_id') and self.texture_id is not None and self.texture_id > 0:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 0.5)

        glDisable(GL_LIGHTING)

        # 绘制模型几何
        glBegin(GL_TRIANGLES)
        for face in faces:
            if len(face) == 4:
                # 四边形拆分为两个三角形
                triangles = [[face[0], face[1], face[2]], [face[0], face[2], face[3]]]
                for triangle in triangles:
                    for vertex_index in triangle:
                        if vertex_index < len(vertices):
                            if vertex_index < len(tex_coords):
                                glTexCoord2fv(tex_coords[vertex_index])
                            glVertex3fv(vertices[vertex_index])
            else:
                for vertex_index in face:
                    if vertex_index < len(vertices):
                        if vertex_index < len(tex_coords):
                            glTexCoord2fv(tex_coords[vertex_index])
                        glVertex3fv(vertices[vertex_index])
        glEnd()

        # 绘制法线（如果存在）
        if normals and len(vertices) == len(normals):
            self.draw_normals_safe(vertices, normals)

    def draw_normals_safe(self, vertices, normals):
        """线程安全的法线绘制"""
        glDisable(GL_TEXTURE_2D)
        glColor3f(1.0, 1.0, 1.0)  # 白色法线
        glBegin(GL_LINES)

        for i in range(len(vertices)):
            if i < len(normals):
                glVertex3fv(vertices[i])
                end_point = [
                    vertices[i][0] + normals[i][0] * 0.2,
                    vertices[i][1] + normals[i][1] * 0.2,
                    vertices[i][2] + normals[i][2] * 0.2
                ]
                glVertex3fv(end_point)

        glEnd()
        glEnable(GL_TEXTURE_2D)

    def run(self, model_file=None):
        """运行主循环 - 添加安全停止"""
        clock = pygame.time.Clock()
        running = True

        try:
            while running:
                running = self.handle_events()
                self.render()
                clock.tick(60)  # 限制60FPS
        except Exception as e:
            print(f"? 主循环错误: {e}")
        finally:
            self.stop_auto_reload()
            pygame.quit()



# 使用示例
if __name__ == "__main__":

    # 创建多模型查看器
    viewer = MultiModelViewer()
    # 加载纹理
    texture_path = 'D:/Personal/zhankangming/Desktop/super_man.png'
    success = viewer.load_texture(texture_path)
    viewer.texture_id = success
    print('输出纹理:', viewer.texture_id)

    # 添加多个模型（可以设置不同位置）
    viewer.add_model_from_file('model1', os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pPlane1', "model_data.bin"), [0, 0, 0])  # 左边
    viewer.add_model_from_file('model2', os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pSphere1', "model_data.bin"), [0, 0, 0])  # 右边
    viewer.add_model_from_file('model3',os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pPlane2',"model_data.bin"), [0, 0, 0])  # 右边

    # 启动多文件监控
    viewer.start_monitoring()

    print("=" * 50)
    print("? 多模型查看器控制说明:")
    print("  空格键: 切换正交/透视视图")
    print("  R键: 重置视角和模型位置")
    print("=" * 50)

    try:
        viewer.run()
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        viewer.cleanup()