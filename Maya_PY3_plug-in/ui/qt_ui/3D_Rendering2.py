# coding=gbk
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

        except Exception as e:
            print(f"纹理加载失败: {e}")
            return None

    def create_default_cube(self):
        """创建默认的立方体模型"""
        # 立方体的8个顶点
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # 背面
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]  # 前面
        ]

        # 立方体的6个面（每个面2个三角形）
        self.faces = [
            [0, 1, 2], [2, 3, 0],  # 背面
            [4, 5, 6], [6, 7, 4],  # 前面
            [1, 5, 6], [6, 2, 1],  # 右面
            [0, 4, 7], [7, 3, 0],  # 左面
            [3, 2, 6], [6, 7, 3],  # 上面
            [0, 1, 5], [5, 4, 0]  # 下面
        ]

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
        print(self.texture_id)
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
        """处理用户输入事件"""
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

                    self.rotation_x = 0
                    self.rotation_y = 0
                    self.translation_z = -5
                    self.ortho_zoom = 1.0  # 重置正交缩放因子
                    if self.is_orthographic:
                        self.set_orthographic()  # 重新设置正交投影
                    # 注意：这里读取共享内存并更新模型数据的逻辑可能需要调整
                    data = read_from_shared_memory()
                    if data:
                        self.vertices = data[0]
                        self.faces = data[1]
                        self.tex_coords = data[2]
                        texture_path = os.path.join("D:", "Personal", "zhankangming", "Desktop", "super_man.png")
                        success = viewer.load_texture(texture_path)
                        self.texture_id = success

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    self.mouse_dragging = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:  # 滚轮上滚 - 放大
                    if self.is_orthographic:
                        # 正交模式：减小视景体范围实现放大
                        self.ortho_zoom *= 0.9  # 乘以小于1的数实现放大
                        self.set_orthographic()  # 更新正交投影
                    else:
                        # 透视模式：传统方式
                        self.translation_z += 0.5
                elif event.button == 5:  # 滚轮下滚 - 缩小
                    if self.is_orthographic:
                        # 正交模式：增大视景体范围实现缩小
                        self.ortho_zoom /= 0.9  # 除以小于1的数实现缩小
                        self.set_orthographic()  # 更新正交投影
                    else:
                        # 透视模式：传统方式
                        self.translation_z -= 0.5

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False

            elif event.type == MOUSEMOTION:
                if self.mouse_dragging:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5
                    self.last_mouse_pos = event.pos

        return True

    def render(self):
        """渲染场景"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 应用视图变换
        glTranslatef(0.0, 0.0, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # 绘制模型
        self.draw_model()

        pygame.display.flip()

    def run(self, model_file=None):
        """运行主循环"""
        # self.get_mesh_structure('pSphere1')
        # if model_file:
        #     self.load_obj(model_file)
        # else:
        #     self.create_default_cube()
        # print('点：', self.vertices)
        # print('面：', self.faces)


        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.render()
            clock.tick(60)  # 限制60FPS

        pygame.quit()

import mmap
import os
import pickle  # 需要导入pickle模块

def read_from_shared_memory(shared_file=os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem.bin")):
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

        # 启动自动重载线程
        self.start_auto_reload()

    def start_auto_reload(self):
        """启动自动重载线程"""
        if self.shared_file and os.path.exists(self.shared_file):
            self.last_modified = os.path.getmtime(self.shared_file)
            self.stop_reload = False
            self.reload_thread = threading.Thread(target=self._auto_reload_worker, daemon=True)
            self.reload_thread.start()
            print(f"开始监控文件: {self.shared_file}")

    def _auto_reload_worker(self):
        """自动重载的工作线程"""
        while not self.stop_reload:
            try:
                current_modified = os.path.getmtime(self.shared_file)
                if current_modified > self.last_modified:
                    print("检测到文件更新，重新加载数据...")
                    self.last_modified = current_modified
                    self.reload_shared_data()
            except Exception as e:
                print(f"监控文件时出错: {e}")

            time.sleep(self.check_interval)

    def reload_shared_data(self):
        """重载共享内存数据"""
        data = read_from_shared_memory(self.shared_file)
        if data:
            # 使用线程锁确保数据安全更新（如果需要）
            self.vertices = data[0]
            self.faces = data[1]
            self.tex_coords = data[2]
            print("数据重载完成")

    def stop_auto_reload(self):
        """停止自动重载"""
        self.stop_reload = True
        if self.reload_thread:
            self.reload_thread.join(timeout=5)
# 使用示例
if __name__ == "__main__":
    # data = read_from_shared_memory()
    # viewer = ModelViewer()
    # viewer.vertices = data[0]
    # viewer.faces = data[1]
    # viewer.tex_coords = data[2]
    # # viewer.get_mesh_structure('pSphere1')
    # # 如果有一个model.obj文件，可以这样加载：
    # # viewer.run("model.obj")
    # # 然后加载纹理（此时OpenGL上下文已就绪）
    # texture_path = os.path.join("D:", "Personal", "zhankangming", "Desktop", "super_man.png")
    # success = viewer.load_texture(texture_path)
    # viewer.texture_id = success
    # if success:
    #     print("纹理加载成功，开始渲染...")
    # else:
    #     print("纹理加载失败，将使用纯色渲染")
    # # 否则使用默认的立方体
    # viewer.run()

    shared_file_path = os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem_1.bin")

    # 使用自动重载的查看器
    viewer = AutoReloadModelViewer(shared_file=shared_file_path, check_interval=0.01)

    # 初始加载数据
    data = read_from_shared_memory(shared_file_path)
    if data:
        viewer.vertices = data[0]
        viewer.faces = data[1]
        viewer.tex_coords = data[2]
        viewer.normals = data[3]

    texture_path = os.path.join("D:", "Personal", "zhankangming", "Desktop", "super_man.png")
    success = viewer.load_texture(texture_path)
    viewer.texture_id = success

    try:
        viewer.run()
    finally:
        viewer.stop_auto_reload()