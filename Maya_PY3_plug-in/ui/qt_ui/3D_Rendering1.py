# coding=gbk
import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import threading
import os
import pickle
import mmap
import math
from collections import OrderedDict
from PIL import Image  # 添加PIL库支持


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

class UnifiedModelViewer:
    """统一模型查看器 - 集成所有功能"""

    def __init__(self, width=800, height=600):
        # 基础设置
        self.width = width
        self.height = height

        # 视图控制
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_z = -5
        self.is_orthographic = False
        self.ortho_zoom = 1.0
        self.ortho_size = 5
        # 添加平移变量
        self.translation_x = 0.0  # X轴平移
        self.translation_y = 0.0  # Y轴平移
        self.middle_mouse_dragging = False  # 中键拖动状态

        # 模型数据
        self.models = {}  # {model_id: model_data}
        self.active_model_id = None
        self.display_lists = {}  # 显示列表缓存

        # 文件监控
        self.monitored_files = {}  # {file_path: {model_id, last_modified}}
        self.monitor_thread = None
        self.stop_monitoring = False
        self.check_interval = 0.01
        self.data_lock = threading.Lock()
        self.model_manager = None
        # 多模型管理核心组件
        self.model_manager = MultiModelManager()
        self.file_monitor = MultiFileMonitor(check_interval=0.01)
        self.file_monitor.set_model_manager(self.model_manager)


        # 交互状态
        self.mouse_dragging = False
        self.last_mouse_pos = (0, 0)

        # 纹理管理
        self.texture_id = None
        self.texture_path = None

        # 初始化窗口
        self.init_window()

        # 添加自动渲染设置
        self.auto_render_enabled = True  # 启用自动渲染
        self.auto_render_path = "D:/Personal/zhankangming/Desktop/auto_renders"  # 自动渲染保存路径
        self.auto_render_counter = 0  # 自动渲染计数器
        self.last_render_time = 0  # 上次渲染时间
        self.render_interval = 0.5  # 渲染间隔（秒）

        # 确保自动渲染目录存在
        os.makedirs(self.auto_render_path, exist_ok=True)

        print("? 统一模型查看器初始化完成")



    # ==================== 窗口初始化 ====================
    def init_window(self):
        """初始化Pygame和OpenGL窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("统一3D模型查看器")

        # 设置初始投影
        self.set_perspective()

        # OpenGL状态设置
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glDisable(GL_LIGHTING)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    # ==================== 投影系统 ====================
    def set_perspective(self):
        """设置透视投影"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width / self.height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def set_orthographic(self):
        """设置正交投影"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect_ratio = self.width / self.height
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
        glMatrixMode(GL_MODELVIEW)

    # ==================== 模型管理 ====================
    def add_model_from_file(self, model_id, shared_file, texture_path=None, initial_position=None):
        """从共享内存文件添加模型 - 修复版本"""
        # 读取初始数据
        data = read_from_shared_memory(shared_file)  # 修复函数名
        if not data:
            print(f"? 无法从 {shared_file} 加载模型数据")
            return False

        # 设置初始位置
        if initial_position is None:
            initial_position = [0, 0, 0]

        # 添加到模型管理器
        self.model_manager.add_model(model_id, shared_file, data)

        # 同时添加到查看器的模型字典（用于渲染）
        self.models[model_id] = {
            'vertices': data[0],
            'faces': data[1],
            'tex_coords': data[2],
            'normals': data[3] if len(data) > 3 else [],
            'position': initial_position,
            'rotation': [0, 0, 0],
            'visible': True,
            'last_updated': time.time(),
            'texture_path': texture_path  # 添加贴图路径
        }
        # 如果提供了贴图路径，加载贴图
        if texture_path:
            self.load_texture_for_model(model_id, texture_path)

        # 添加到文件监控
        self.file_monitor.add_file_monitor(shared_file, model_id)

        # 创建显示列表（性能优化）
        self._create_display_list(model_id)

        # 设置第一个模型为激活模型
        if self.active_model_id is None:
            self.active_model_id = model_id

        return True

    def load_texture_for_model(self, model_id, texture_path):
        """为特定模型加载贴图"""
        if model_id not in self.models:
            print(f"? 模型不存在: {model_id}")
            return False

        try:
            # 加载贴图
            texture_id = self.load_texture(texture_path)
            if texture_id:
                # 将贴图ID存储到模型数据中
                self.models[model_id]['texture_id'] = texture_id
                print(f"? 为模型 {model_id} 加载贴图: {texture_path}")
                return True
            return False
        except Exception as e:
            print(f"? 为模型加载贴图失败: {model_id}, {e}")
            return False

    def remove_model(self, model_id):
        """移除模型"""
        if model_id not in self.models:
            return False

        # 停止文件监控（如果存在）
        model_data = self.models[model_id]
        if model_data['shared_file'] in self.monitored_files:
            del self.monitored_files[model_data['shared_file']]

        # 删除显示列表
        if model_id in self.display_lists:
            glDeleteLists(self.display_lists[model_id], 1)
            del self.display_lists[model_id]

        # 删除模型数据
        del self.models[model_id]

        # 更新激活模型
        if self.active_model_id == model_id:
            self.active_model_id = list(self.models.keys())[0] if self.models else None

        print(f"?? 移除模型: {model_id}")
        return True

    def update_model_data(self, model_id, vertices, faces, tex_coords, normals=None):
        """更新模型数据"""
        if model_id not in self.models:
            return False

        with self.data_lock:
            self.models[model_id]['vertices'] = vertices
            self.models[model_id]['faces'] = faces
            self.models[model_id]['tex_coords'] = tex_coords
            if normals:
                self.models[model_id]['normals'] = normals
            self.models[model_id]['last_updated'] = time.time()

        # 更新显示列表
        self._create_display_list(model_id)

        print(f"? 更新模型数据: {model_id}")
        return True

    def set_model_position(self, model_id, position):
        """设置模型位置"""
        if model_id in self.models:
            self.models[model_id]['position'] = position
            return True
        return False

    def set_model_visibility(self, model_id, visible):
        """设置模型可见性"""
        if model_id in self.models:
            self.models[model_id]['visible'] = visible
            return True
        return False

    def set_active_model(self, model_id):
        """设置激活模型"""
        if model_id in self.models:
            self.active_model_id = model_id
            return True
        return False

    # ==================== 显示列表优化 ====================
    def _create_display_list(self, model_id):
        """为模型创建显示列表（性能优化） - 修复版本"""
        # 从 models 字典获取模型数据
        if model_id not in self.models:
            return

        model_data = self.models[model_id]

        # 删除旧显示列表（如果存在）
        if model_id in self.display_lists:
            glDeleteLists(self.display_lists[model_id], 1)

        # 创建新显示列表
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)
        self._compile_model_geometry(model_data)
        glEndList()

        self.display_lists[model_id] = display_list

    def _compile_model_geometry(self, model_data):
        """编译模型几何到显示列表"""
        vertices = model_data['vertices']
        faces = model_data['faces']
        tex_coords = model_data['tex_coords']

        if not vertices or not faces:
            return

        # 设置渲染状态
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # # 绑定纹理
        # if self.texture_id and self.texture_id > 0:
        #     glBindTexture(GL_TEXTURE_2D, self.texture_id)
        # else:
        #     glDisable(GL_TEXTURE_2D)
        #     glColor4f(1.0, 1.0, 1.0, 0.5)
        # 绑定纹理 - 使用模型特定的纹理
        if 'texture_id' in model_data and model_data['texture_id'] > 0:
            glBindTexture(GL_TEXTURE_2D, model_data['texture_id'])
        elif self.texture_id and self.texture_id > 0:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)  # 使用全局纹理
        else:
            glDisable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 0.5)

        glDisable(GL_LIGHTING)

        # 绘制几何
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

    # ==================== 纹理管理 ====================
    def load_texture(self, image_path):
        """加载纹理"""
        try:
            from PIL import Image
            img = Image.open(image_path)

            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                print(f"? 图像转换为RGBA格式")

            # 检查Alpha通道
            alpha_data = img.getchannel('A')
            alpha_min, alpha_max = alpha_data.getextrema()
            print(f"? Alpha通道范围: {alpha_min} - {alpha_max}")

            # 翻转图像
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = img.tobytes()

            # 生成纹理
            texture_id = glGenTextures(1)
            if texture_id <= 0:
                print("? 纹理生成失败")
                return None

            # 设置纹理参数
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # 上传纹理数据
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height,
                         0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

            self.texture_id = texture_id
            self.texture_path = image_path

            print(f"? 纹理加载成功: {image_path}")
            print(f"   - 尺寸: {img.width} x {img.height}")
            print(f"   - 纹理ID: {texture_id}")

            return texture_id

        except Exception as e:
            print(f"? 纹理加载失败: {e}")
            return None

    # ==================== 文件监控系统 ====================
    def start_monitoring(self):
        """启动文件监控 - 修复版本"""
        # 使用 file_monitor 启动监控
        self.file_monitor.start_monitoring()
        print('? 文件监控已启动')

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

    # ==================== 渲染系统 ====================
    def _update_dirty_models(self):
        """更新所有脏模型"""
        # 获取脏模型列表
        dirty_models = self.model_manager.dirty_models.copy()

        for model_id in dirty_models:
            print(f"? 更新脏模型: {model_id}")

            # 获取模型数据
            model_data = self.model_manager.get_model_data(model_id)
            if not model_data:
                continue

            # 更新本地模型数据
            if model_id in self.models:
                self.models[model_id]['vertices'] = model_data['vertices']
                self.models[model_id]['faces'] = model_data['faces']
                self.models[model_id]['tex_coords'] = model_data['tex_coords']
                if 'normals' in model_data:
                    self.models[model_id]['normals'] = model_data['normals']

            # 更新显示列表
            self._create_display_list(model_id)

            # 从脏集合中移除
            self.model_manager.dirty_models.remove(model_id)

    # def render(self):
    #     # 检查并更新脏模型
    #     self._update_dirty_models()
    #
    #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #     glLoadIdentity()
    #     """渲染场景 - 添加调试信息"""
    #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #     glLoadIdentity()
    #
    #     # 应用视图变换
    #     # 3. 应用视图变换
    #     glTranslatef(self.translation_x, self.translation_y, self.translation_z)
    #     # glTranslatef(0.0, 0.0, self.translation_z)
    #     glRotatef(self.rotation_x, 1, 0, 0)
    #     glRotatef(self.rotation_y, 0, 1, 0)
    #
    #     # 绘制所有可见模型
    #     # print(f"?? 准备绘制 {len(self.models)} 个模型")
    #     self._draw_all_models()
    #
    #     # 检查OpenGL错误
    #     error = glGetError()
    #     if error != GL_NO_ERROR:
    #         print(f"? OpenGL错误: {error}")
    #
    #     pygame.display.flip()

    # == == == == == == == == == == 自动渲染 == == == == == == == == == ==
    def render(self):
        """渲染场景 - 添加自动渲染功能"""
        # 检查并更新脏模型
        self._update_dirty_models()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 应用视图变换
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # 绘制所有可见模型
        self._draw_all_models()

        # 检查OpenGL错误
        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"? OpenGL错误: {error}")

        pygame.display.flip()

        # 自动渲染到PNG
        if self.auto_render_enabled:
            current_time = time.time()
            if current_time - self.last_render_time >= self.render_interval:
                self._auto_render_to_png()
                self.last_render_time = current_time

    def _auto_render_to_png(self):
        """自动渲染到PNG"""
        try:
            print('自动渲染图片')
            # 生成文件名
            filename = os.path.join(
                self.auto_render_path,
                f"render_{self.auto_render_counter:04d}.png"
            )

            # 渲染到PNG（透明背景）
            success = self.render_to_png(
                filename=filename,
                transparent_background=True
            )

            if success:
                print(f"? 自动渲染保存: {filename}")
                # self.auto_render_counter += 1
            else:
                print(f"?? 自动渲染失败: {filename}")

        except Exception as e:
            print(f"?? 自动渲染错误: {e}")

    def _draw_all_models(self):
        """绘制所有模型 - 修复版本"""
        # 从 models 字典获取可见模型
        models_to_draw = []
        for model_id, model_data in self.models.items():
            if model_data['visible']:
                models_to_draw.append((model_id, model_data))

        # 按深度排序（从远到近）
        models_with_depth = []
        for model_id, model_data in models_to_draw:
            pos = model_data['position']
            depth = abs(pos[2] - self.translation_z)
            models_with_depth.append((depth, model_id, model_data))

        models_with_depth.sort(key=lambda x: x[0], reverse=True)

        # 绘制模型
        for depth, model_id, model_data in models_with_depth:
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
                # 回退到即时渲染
                self._compile_model_geometry(model_data)

            glPopMatrix()

    # ==================== 事件处理 ====================
    def handle_events(self):
        """处理用户输入事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self._handle_keydown(event):
                    return False
            elif event.type == MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            elif event.type == MOUSEBUTTONUP:
                self._handle_mouse_up(event)
            elif event.type == MOUSEMOTION:
                self._handle_mouse_motion(event)

        return True

    def _handle_keydown(self, event):
        """处理键盘按下事件"""
        if event.key == K_ESCAPE:
            return False
        elif event.key == K_SPACE:
            self._toggle_projection()
        elif event.key == K_r:  # R键重置视图
            self._reset_view()
        elif event.key == K_c:  # C键重置相机
            self._reset_camera()
        elif event.key == K_v:  # V键切换激活模型可见性
            self._toggle_active_model_visibility()
        elif event.key == K_p:  # P键截图
            self.screenshot_to_png()
        elif event.key == K_o:  # O键高质量渲染
            self.render_to_png()
        elif event.key == K_b:  # B键批量渲染
            self.render_high_quality_sequence()
        elif event.key == K_t:  # T键透明背景渲染（新增）
            self.render_to_png(transparent_background=True)

        return True

    def _handle_mouse_down(self, event):
        """处理鼠标按下事件"""
        if event.button == 1:  # 左键
            self.mouse_dragging = True
            self.last_mouse_pos = event.pos
        elif event.button == 2:  # 中键
            self.middle_mouse_dragging = True
            self.last_mouse_pos = event.pos
            print("?? 中键按下 - 开始平移")
        elif event.button == 4:  # 滚轮上滚
            self._handle_zoom_in()
        elif event.button == 5:  # 滚轮下滚
            self._handle_zoom_out()

    def _handle_mouse_up(self, event):
        """处理鼠标释放事件"""
        if event.button == 1:
            self.mouse_dragging = False
        elif event.button == 2:  # 中键
            self.middle_mouse_dragging = False
            print("?? 中键释放 - 结束平移")

    def _handle_mouse_motion(self, event):
        """处理鼠标移动事件 - 添加中键平移"""
        if self.mouse_dragging:
            # 旋转处理
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]
            self.rotation_y += dx * 0.5
            self.rotation_x += dy * 0.5
            self.last_mouse_pos = event.pos
            print(f"?? 旋转: X={self.rotation_x:.1f}, Y={self.rotation_y:.1f}")
        elif self.middle_mouse_dragging:
            # 中键平移处理
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]

            # 根据缩放因子调整平移速度
            scale_factor = 0.01 * abs(self.translation_z) / 5.0
            self.translation_x += dx * scale_factor
            self.translation_y -= dy * scale_factor  # 注意：屏幕坐标Y轴向下为正

            self.last_mouse_pos = event.pos
            print(f"?? 平移: X={self.translation_x:.2f}, Y={self.translation_y:.2f}")

    def _toggle_projection(self):
        """切换投影模式"""
        self.is_orthographic = not self.is_orthographic
        if self.is_orthographic:
            self.set_orthographic()
            print("? 切换到正交视图")
        else:
            self.set_perspective()
            print("?? 切换到透视视图")

    def _reset_view(self):
        """重置视图"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_z = -5
        self.translation_x = 0.0  # 重置X平移
        self.translation_y = 0.0  # 重置Y平移
        self.ortho_zoom = 1.0
        if self.is_orthographic:
            self.set_orthographic()
        print("? 视图已重置")

    def _reset_camera(self):
        """重置相机"""
        self.translation_z = -5
        print("? 相机位置已重置")

    def _toggle_active_model_visibility(self):
        """切换激活模型可见性"""
        if self.active_model_id and self.active_model_id in self.models:
            current = self.models[self.active_model_id]['visible']
            new_visibility = not current
            self.set_model_visibility(self.active_model_id, new_visibility)
            print(f"?? 模型 {self.active_model_id} 可见性: {new_visibility}")

    def _handle_zoom_in(self):
        """处理放大"""
        if self.is_orthographic:
            self.ortho_zoom *= 0.9
            self.set_orthographic()
            print(f"? 正交放大: {self.ortho_zoom:.2f}")
        else:
            self.translation_z += 0.5
            print(f"? 透视放大: Z={self.translation_z:.1f}")

    def _handle_zoom_out(self):
        """处理缩小"""
        if self.is_orthographic:
            self.ortho_zoom /= 0.9
            self.set_orthographic()
            print(f"? 正交缩小: {self.ortho_zoom:.2f}")
        else:
            self.translation_z -= 0.5
            print(f"? 透视缩小: Z={self.translation_z:.1f}")

    # ==================== 主循环 ====================
    def run(self):
        """运行主循环"""
        clock = pygame.time.Clock()
        running = True

        print("? 控制说明:")
        print("  空格键: 切换正交/透视视图")
        print("  R键: 重置视图")
        print("  C键: 重置相机")
        print("  V键: 切换激活模型可见性")
        print("  P键: 截图")
        print("  O键: 高质量渲染")
        print("  T键: 透明背景渲染")
        print("  B键: 批量渲染序列")
        print("  X键: 重置平移位置")
        print("  左键拖动: 旋转视图")
        print("  中键拖动: 平移视图")
        print("  滚轮: 缩放")

        try:
            while running:
                running = self.handle_events()
                self.render()
                clock.tick(60)  # 限制60FPS
        except Exception as e:
            print(f"? 主循环错误: {e}")
        finally:
            self.cleanup()

    # ==================== 工具方法 ====================
    def get_model_info(self, model_id):
        """获取模型信息"""
        if model_id in self.models:
            model_data = self.models[model_id]
            return {
                'vertices_count': len(model_data['vertices']),
                'faces_count': len(model_data['faces']),
                'position': model_data['position'],
                'visible': model_data['visible'],
                'last_updated': model_data['last_updated']
            }
        return None

    def get_system_status(self):
        """获取系统状态"""
        status = {
            'total_models': len(self.models),
            'visible_models': sum(1 for m in self.models.values() if m['visible']),
            'active_model': self.active_model_id,
            'projection_mode': '正交' if self.is_orthographic else '透视',
            'monitored_files': len(self.monitored_files),
            'texture_loaded': self.texture_id is not None
        }
        return status

    def print_status(self):
        """打印当前状态"""
        status = self.get_system_status()
        print("? 系统状态:")
        for key, value in status.items():
            print(f"   {key}: {value}")

    # ==================== 图片渲染功能 ====================

    def render_to_png(self, filename=None, width=None, height=None, transparent_background=False):
        """将当前3D场景渲染为PNG图片 - 添加透明背景选项"""
        # if filename is None:
        #     timestamp = time.strftime('%Y%m%d_%H%M%S')
        #     if transparent_background:
        #         filename = f"render_transparent_{timestamp}.png"
        #     else:
        #         filename = f"render_{timestamp}.png"
        if filename is None:
            filename = f"D:/Personal/zhankangming/Desktop/auto_renders/render.png"
        # 设置渲染尺寸（默认为窗口尺寸）
        render_width = width or self.width
        render_height = height or self.height

        try:
            # 保存当前清除颜色
            saved_clear_color = glGetFloatv(GL_COLOR_CLEAR_VALUE)

            # 根据透明背景选项设置清除颜色
            if transparent_background:
                glClearColor(0.0, 0.0, 0.0, 0.0)  # 透明黑色 (Alpha=0.0)
                print("? 使用透明背景渲染")
            else:
                glClearColor(0.0, 0.0, 0.0, 1.0)  # 不透明黑色 (Alpha=1.0)
                print("? 使用不透明背景渲染")

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

            # 如果要求透明背景但图像有黑色边缘，可以进行后期处理
            if transparent_background:
                # 将纯黑色像素转换为完全透明
                # img = self._make_black_transparent(img)
                img = self._remove_green_background(img)

            # 转换为RGBA字节数据
            rgba_data = img.tobytes()
            # 创建内存映射
            mmap_data = self._create_rgba_memory_map(rgba_data, render_width, render_height)
            print(mmap_data)
            # 保存为PNG
            img.save(filename, "PNG")

            # 恢复清除颜色
            glClearColor(*saved_clear_color)
            # 恢复正常渲染设置
            self._restore_normal_render()

            print(f"? PNG图片已保存: {filename}")
            print(f"   - 尺寸: {render_width} x {render_height}")
            print(f"   - 背景: {'透明' if transparent_background else '不透明'}")
            return True

        except Exception as e:
            print(f"? 渲染PNG失败: {e}")
            # 尝试恢复清除颜色
            try:
                glClearColor(*saved_clear_color)
                self._restore_normal_render()
            except:
                pass
            return False

    def _create_rgba_memory_map(self, rgba_data, width, height):
        """创建RGBA数据的内存映射"""
        try:
            import mmap
            import tempfile
            import os

            # 计算数据总大小（包含头部信息）
            header_size = 16  # 4个int32：宽度、高度、数据大小、版本
            data_size = len(rgba_data)
            total_size = header_size + data_size

            # 创建临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.bin')
            temp_filename = temp_file.name
            temp_file.close()

            # 创建文件并设置大小
            with open(temp_filename, 'wb') as f:
                f.write(b'\x00' * total_size)  # 预分配空间

            # 创建内存映射
            with open(temp_filename, 'r+b') as f:
                mm = mmap.mmap(f.fileno(), total_size)

                # 写入头部信息
                mm.seek(0)
                mm.write(width.to_bytes(4, byteorder='little'))  # 宽度
                mm.write(height.to_bytes(4, byteorder='little'))  # 高度
                mm.write(data_size.to_bytes(4, byteorder='little'))  # 数据大小
                mm.write(b'\x01\x00\x00\x00')  # 版本号 (1)

                # 写入RGBA数据
                mm.write(rgba_data)

                # 返回内存映射对象和相关信息
                return {
                    'mmap': mm,
                    'filename': temp_filename,
                    'width': width,
                    'height': height,
                    'data_size': data_size,
                    'total_size': total_size,
                    'header_size': header_size
                }

        except Exception as e:
            print(f"? 创建内存映射失败: {e}")
            return None

    def read_rgba_from_memory_map(self, mmap_info):
        """从内存映射读取RGBA数据"""
        try:
            mm = mmap_info['mmap']

            # 读取头部信息
            mm.seek(0)
            width = int.from_bytes(mm.read(4), byteorder='little')
            height = int.from_bytes(mm.read(4), byteorder='little')
            data_size = int.from_bytes(mm.read(4), byteorder='little')
            version = int.from_bytes(mm.read(4), byteorder='little')

            # 读取RGBA数据
            rgba_data = mm.read(data_size)

            # 转换为PIL图像
            img = Image.frombytes("RGBA", (width, height), rgba_data)

            return {
                'image': img,
                'width': width,
                'height': height,
                'data_size': data_size,
                'version': version
            }

        except Exception as e:
            print(f"? 读取内存映射失败: {e}")
            return None

    def _make_black_transparent(self, img):
        """将纯黑色像素转换为完全透明"""
        try:
            # 将图像转换为RGBA模式（确保有Alpha通道）
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 获取像素数据
            data = img.getdata()
            new_data = []

            # 定义黑色的阈值（纯黑色或接近黑色）
            black_threshold = 0  # RGB值都小于这个阈值认为是黑色

            for item in data:
                # 检查是否是黑色或接近黑色
                if item[0] <= black_threshold and item[1] <= black_threshold and item[2] <= black_threshold:
                    # 设置为完全透明
                    new_data.append((0, 0, 0, 0))
                else:
                    # 保持原样
                    new_data.append(item)

            img.putdata(new_data)
            return img

        except Exception as e:
            print(f"? 透明化处理失败: {e}")
            return img

    def _remove_green_background(self, img):
        """将绿色背景转换为透明 - 绿幕抠图"""
        try:
            # 将图像转换为RGBA模式（确保有Alpha通道）
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 获取像素数据
            data = img.getdata()
            new_data = []

            # 定义绿色的阈值范围
            green_min = (0, 244, 0)  # 最小绿色值 (R, G, B)
            green_max = (0, 255, 0)  # 最大绿色值 (R, G, B)

            for item in data:
                r, g, b, a = item

                # 检查是否在绿色范围内
                if (g > r * 1.5 and g > b * 1.5 and g > 50) or \
                        (green_min[0] <= r <= green_max[0] and
                         green_min[1] <= g <= green_max[1] and
                         green_min[2] <= b <= green_max[2]):
                    # 设置为完全透明
                    new_data.append((0, 0, 0, 0))
                else:
                    # 保持原样
                    new_data.append(item)

            img.putdata(new_data)
            return img

        except Exception as e:
            print(f"? 去除绿色背景失败: {e}")
            return img
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

    def render_offscreen(self):
        """离屏渲染"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 应用视图变换
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # 绘制模型
        self._draw_all_models()

    def _restore_normal_render(self):
        """恢复正常渲染设置"""
        if hasattr(self, 'saved_viewport'):
            glViewport(*self.saved_viewport)

        if hasattr(self, 'saved_projection_matrix'):
            glMatrixMode(GL_PROJECTION)
            glLoadMatrixd(self.saved_projection_matrix)
            glMatrixMode(GL_MODELVIEW)

    def screenshot_to_png(self, filename=None):
        """使用Pygame截图功能保存PNG"""
        if filename is None:
            filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"

        try:
            # 渲染当前帧
            self.render()
            pygame.display.flip()

            # 获取屏幕表面
            screen_surface = pygame.display.get_surface()

            # 保存为PNG
            pygame.image.save(screen_surface, filename)

            print(f"? 截图已保存: {filename}")
            return True

        except Exception as e:
            print(f"? 截图失败: {e}")
            return False

    def render_high_quality_sequence(self, output_dir="renders",
                                     num_frames=360,
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
# 从共享文件读取初始数据
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
# ==================== 使用示例 ====================
def main():
    """主函数示例"""
    # 创建查看器
    viewer = UnifiedModelViewer(width=1000, height=800)

    # 加载纹理
    # texture_path = "D:/Personal/zhankangming/Desktop/super_man.png"
    # viewer.load_texture(texture_path)

    viewer.add_model_from_file(1, os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pPlane1',"model_data.bin"),texture_path="D:/Personal/zhankangming/Desktop/asd.png", initial_position=[0, 0, 0])  # 左边
    viewer.add_model_from_file(2, os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pSphere1',"model_data.bin"),texture_path="D:/Personal/zhankangming/Desktop/super_man2.png", initial_position=[0, 0, 0])  # 右边
    viewer.add_model_from_file(3, os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pPlane2',"model_data.bin"),texture_path="D:/Personal/zhankangming/Desktop/OMvxPV8Yvl.png", initial_position=[0, 0, 0])  # 右边

    # 设置激活模型
    viewer.set_active_model("model1")
    viewer.start_monitoring()
    # 打印初始状态
    viewer.print_status()

    # 运行查看器
    viewer.run()


if __name__ == "__main__":
    main()