# -*- coding: utf-8 -*-
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaRender as omr
import maya.cmds as cmds
import math
import time


# ============================================================================
# GPU 几何体覆盖类 (核心加速部件)
# ============================================================================
class GPUSkinGeometryOverride(omr.MPxGeometryOverride):
    """
    用于 basicSkinCluster 的 GPU 几何体覆盖。
    它直接将变形器输出的顶点位置数据传递给 GPU，绕过 setPoints。
    """

    # 用于标识位置数据流的字符串常量
    kPositionStreamName = "positionStream"
    # 顶点着色器中位置属性的名称（必须匹配）
    kPositionSemantic = "position"

    def __init__(self, obj):
        """
        初始化几何体覆盖。
        :param obj: 关联的 MObject（通常是 basicSkinCluster 节点）
        """
        omr.MPxGeometryOverride.__init__(self, obj)

        # --- 关键数据结构初始化 ---
        # 存储从变形器获取的顶点数据
        self._vertex_positions = None  # 将存储为一个列表的列表 [[x,y,z], ...]
        self._vertex_count = 0

        # 用于渲染的 GPU 缓冲区
        self._position_buffer = None

        # 关联的变形器节点信息
        self._deformer_node = om.MObject(obj)
        self._deformer_node_name = None
        try:
            dep_node = om.MFnDependencyNode(self._deformer_node)
            self._deformer_node_name = dep_node.name()
        except:
            self._deformer_node_name = "unknown"

        print(f"[GPU覆盖] 已创建，关联节点: {self._deformer_node_name}")

    def supportedDrawAPIs(self):
        """声明支持的绘制API (Viewport 2.0)。"""
        return omr.MRenderer.kOpenGL | omr.MRenderer.kDirectX11 | omr.MRenderer.kOpenGLCoreProfile

    def hasUIDrawables(self):
        """我们不自定义UI绘制，所以返回False。"""
        return False

    def updateDG(self):
        """
        从依赖图(DG)获取数据（关键步骤1：取数据）。
        在这里，我们从关联的 basicSkinCluster 节点获取计算好的顶点位置。
        """
        # print(f"[GPU覆盖] updateDG 被调用")
        try:
            if self._deformer_node.isNull():
                return

            # 创建到变形器节点的连接
            dep_node = om.MFnDependencyNode(self._deformer_node)

            # 为了演示，我们假设节点有一个名为“outputPositions”的属性来输出数据
            # 在实际中，你可能需要通过其他方式获取数据，例如全局缓存或自定义属性
            output_positions_attr = dep_node.attribute("outputPositions")

            if output_positions_attr.isNull():
                # 如果自定义属性不存在，尝试从节点消息或全局状态获取
                # 这里我们模拟从全局缓存获取数据
                self._get_positions_from_cache()
            else:
                # 如果属性存在，从数据块读取数据
                self._get_positions_from_datablock(dep_node, output_positions_attr)

        except Exception as e:
            print(f"[GPU覆盖] updateDG 错误: {e}")

    def _get_positions_from_cache(self):
        """
        从全局缓存获取顶点位置数据（示例方法）。
        在实际实现中，你的 basicSkinCluster.deform() 方法应将其计算结果存储在一个可被此处访问的位置。
        """
        # 这是关键数据接口：你的 basicSkinCluster 必须把结果放在这里
        # 为了示例，我们创建一些模拟数据
        if hasattr(self, '_last_update_time') and (time.time() - self._last_update_time) < 0.1:
            # 避免过于频繁的模拟数据生成
            return

        self._last_update_time = time.time()

        # 模拟：生成一个简单的波浪动画作为顶点位置
        if self._vertex_count == 0:
            self._vertex_count = 1000  # 示例顶点数

        self._vertex_positions = []
        time_val = time.time()

        for i in range(self._vertex_count):
            # 生成一个简单的波浪网格
            x = (i % 32) * 0.1
            z = (i // 32) * 0.1
            y = math.sin(x * 2.0 + time_val) * 0.05 + math.cos(z * 2.0 + time_val) * 0.05
            self._vertex_positions.append([x, y, z])

        # print(f"[GPU覆盖] 从缓存更新了 {len(self._vertex_positions)} 个顶点")

    def _get_positions_from_datablock(self, dep_node, attr):
        """从数据块获取顶点位置（理想方式）。"""
        try:
            plug = dep_node.findPlug(attr, True)
            if plug.isNull():
                return

            # 这里需要根据你的实际数据结构来解析数据
            # 例如，可能是一个包含所有顶点位置的数组属性
            data_handle = plug.asMDataHandle()

            # 具体解析逻辑取决于你如何设计输出属性
            # 此处仅为示例框架
            print(f"[GPU覆盖] 从数据块读取位置数据")

        except Exception as e:
            print(f"[GPU覆盖] 从数据块读取失败: {e}")

    def populateGeometry(self, requirements, render_items, data):
        """
        定义几何体需求（关键步骤2：申明需求）。
        告诉 Maya 我们需要哪些数据流（这里只需要位置）。
        """
        # print(f"[GPU覆盖] populateGeometry 被调用")

        # 获取位置需求
        position_requirements = requirements.getVertexRequirements()

        # 添加位置流需求
        position_requirements.addElement(
            self.kPositionStreamName,  # 数据流名称
            omr.MGeometry.kPosition,  # 几何体成分类型（位置）
            omr.MGeometry.kFloat,  # 数据类型
            3  # 数据维度 (x, y, z)
        )

        # 创建渲染项（使用三角形列表作为示例）
        # 实际使用时，你应该根据变形器影响的网格拓扑来设置正确的图元类型
        render_item = omr.MRenderItem.create(
            self._deformer_node_name + "_renderItem",
            omr.MRenderItem.NonMaterialSceneItem,  # 不依赖特定材质的场景项
            omr.MGeometry.kTriangles  # 图元类型（示例）
        )

        # 设置着色器
        shader_manager = omr.MRenderer.getShaderManager()
        shader = shader_manager.getStockShader(omr.MShaderManager.k3dSolidShader)
        if shader:
            render_item.setShader(shader)
            shader_manager.releaseShader(shader)

        # 将渲染项添加到列表
        render_items.append(render_item)

        # 设置渲染项使用的数据流
        render_item.setVertexBuffer(self._position_buffer)

    def updateVertexBuffers(self, render_items, data):
        """
        更新顶点缓冲区（关键步骤3：传数据到GPU）。
        这是性能最关键的函数，将顶点数据从内存复制到GPU缓冲区。
        """
        # print(f"[GPU覆盖] updateVertexBuffers 被调用，顶点数: {self._vertex_count}")

        if self._vertex_count == 0 or self._vertex_positions is None:
            # print("[GPU覆盖] 无顶点数据可更新")
            return

        # 确保我们有一个顶点缓冲区
        if self._position_buffer is None:
            self._create_position_buffer()
            if self._position_buffer is None:
                return

        try:
            # 将顶点数据写入缓冲区
            vertex_count = len(self._vertex_positions)
            if vertex_count > self._vertex_count:
                vertex_count = self._vertex_count

            # 获取缓冲区的写入接口
            buffer_writer = self._position_buffer.acquire(vertex_count, True)  # True 表示可写

            if buffer_writer is not None:
                # 将数据复制到缓冲区
                for i in range(vertex_count):
                    pos = self._vertex_positions[i]
                    # 将位置数据写入缓冲区
                    buffer_writer.setFloatArray(i * 3, pos[0], pos[1], pos[2])

                # 提交数据到GPU
                buffer_writer.commit()
                # print(f"[GPU覆盖] 已更新 {vertex_count} 个顶点到GPU缓冲区")
            else:
                print("[GPU覆盖] 无法获取缓冲区写入器")

        except Exception as e:
            print(f"[GPU覆盖] 更新顶点缓冲区时出错: {e}")

    def _create_position_buffer(self):
        """创建位置顶点缓冲区。"""
        try:
            # 确保有顶点数据
            if self._vertex_count == 0 or self._vertex_positions is None:
                print("[GPU覆盖] 无顶点数据，无法创建缓冲区")
                return

            # 创建顶点缓冲区描述符
            buffer_descriptor = omr.MVertexBufferDescriptor(
                self.kPositionStreamName,  # 数据流名称
                omr.MGeometry.kPosition,  # 几何体成分类型
                omr.MGeometry.kFloat,  # 数据类型
                3,  # 数据维度
                self._vertex_count  # 顶点数量
            )

            # 创建顶点缓冲区
            self._position_buffer = omr.MVertexBuffer.createVertexBuffer(buffer_descriptor)

            if self._position_buffer is not None:
                print(f"[GPU覆盖] 已创建位置缓冲区，容量: {self._vertex_count} 顶点")
            else:
                print("[GPU覆盖] 创建位置缓冲区失败")

        except Exception as e:
            print(f"[GPU覆盖] 创建位置缓冲区时出错: {e}")

    def cleanUp(self):
        """清理资源。"""
        # print(f"[GPU覆盖] cleanUp 被调用")
        self._position_buffer = None
        self._vertex_positions = None
        self._vertex_count = 0

    def requiresUpdate(self, render_item):
        """
        控制何时需要更新。
        为了高性能，可以根据变形器的变化频率来优化。
        """
        # 简单实现：总是需要更新（确保动画流畅）
        # 在实际使用中，可以检查变形器的脏标记或时间戳来优化
        return True

    @staticmethod
    def creator(obj):
        """静态创建方法，供 Maya 调用。"""
        return GPUSkinGeometryOverride(obj)