# coding=gbk
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os
import pickle
import threading
import time
import math

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import mmap
import os
import pickle

class AdvancedDeformationMonitor:
    def __init__(self, shared_memory_file, monitor_name="变形监控器", check_interval=0.5):
        self.shared_memory_file = shared_memory_file
        self.monitor_name = monitor_name  # 监控器名称
        self.check_interval = check_interval
        self.monitoring = False
        self.monitor_thread = None
        self.last_vertex_positions = {}
        self.deformation_threshold = 0.01  # 顶点移动阈值

        # 变形统计信息
        self.deformation_count = 0
        self.total_deformation = 0.0
        self.max_deformation = 0.0

        print(f"? 初始化监控器: {self.monitor_name}")

    def get_mesh_vertex_positions(self, mesh_name):
        """获取网格所有顶点的世界坐标位置"""
        vertex_positions = []
        try:
            vertex_count = cmds.polyEvaluate(mesh_name, vertex=True)
            for i in range(vertex_count):
                vertex_name = "{}.vtx[{}]".format(mesh_name, i)
                pos = cmds.pointPosition(vertex_name, world=True)
                vertex_positions.append(pos)
            return vertex_positions
        except Exception as e:
            print(f"{self.monitor_name} - 获取顶点位置错误: {e}")
            return []

    def calculate_deformation_amount(self, mesh_name):
        """计算变形的具体量和统计信息"""
        current_positions = self.get_mesh_vertex_positions(mesh_name)

        if mesh_name not in self.last_vertex_positions:
            self.last_vertex_positions[mesh_name] = current_positions
            return 0.0, 0.0, 0  # 总变形量, 最大变形, 变形顶点数

        last_positions = self.last_vertex_positions[mesh_name]

        if len(current_positions) != len(last_positions):
            # 拓扑结构变化，视为最大变形
            self.last_vertex_positions[mesh_name] = current_positions
            return 100.0, 100.0, len(current_positions)

        total_deformation = 0.0
        max_deformation = 0.0
        deformed_vertex_count = 0

        for i, (current, last) in enumerate(zip(current_positions, last_positions)):
            # 计算欧几里得距离
            distance = math.sqrt(
                (current[0] - last[0]) ** 2 +
                (current[1] - last[1]) ** 2 +
                (current[2] - last[2]) ** 2
            )

            if distance > self.deformation_threshold:
                total_deformation += distance
                max_deformation = max(max_deformation, distance)
                deformed_vertex_count += 1

        return total_deformation, max_deformation, deformed_vertex_count

    def detect_deformation(self, mesh_name):
        """检测网格变形并返回详细信息"""
        total_deform, max_deform, deform_count = self.calculate_deformation_amount(mesh_name)

        has_deformation = deform_count > 0

        if has_deformation:
            # 更新统计信息
            self.deformation_count += 1
            self.total_deformation += total_deform
            self.max_deformation = max(self.max_deformation, max_deform)

            # 打印详细的变形信息
            self.print_deformation_info(mesh_name, total_deform, max_deform, deform_count)

            # 更新最后记录的位置
            self.last_vertex_positions[mesh_name] = self.get_mesh_vertex_positions(mesh_name)

        return has_deformation, total_deform, max_deform, deform_count

    def print_deformation_info(self, mesh_name, total_deform, max_deform, deform_count):
        """打印详细的变形信息"""
        vertex_count = cmds.polyEvaluate(mesh_name, vertex=True)
        deform_percentage = (deform_count / vertex_count) * 100

        print(f"\n? [{self.monitor_name}] 检测到模型变形!")
        print(f"   ? 模型名称: {mesh_name}")
        print(f"   ? 变形统计:")
        print(f"      ? 变形顶点数: {deform_count}/{vertex_count} ({deform_percentage:.1f}%)")
        print(f"      ? 总变形量: {total_deform:.6f} 单位")
        print(f"      ? 最大单点变形: {max_deform:.6f} 单位")
        print(f"      ? 平均变形量: {total_deform / max(deform_count, 1):.6f} 单位")
        print(f"   ? 累计统计:")
        print(f"      ? 总变形次数: {self.deformation_count}")
        print(f"      ? 历史最大变形: {self.max_deformation:.6f} 单位")
        print("─" * 50)

    def get_deformation_statistics(self):
        """获取变形统计信息"""
        return {
            "monitor_name": self.monitor_name,
            "deformation_count": self.deformation_count,
            "total_deformation": self.total_deformation,
            "max_deformation": self.max_deformation,
            "average_deformation": self.total_deformation / max(self.deformation_count, 1)
        }

    def update_shared_memory(self, mesh_name, deformation_info=None):
        """检测到变形时更新共享内存，包含变形信息"""
        try:
            vertices, faces, combined_list, vertex_normals = get_mesh_structure(mesh_name)
            # vertices = self.get_mesh_data(mesh_name)
            # faces = self.get_face_data(mesh_name)
            # tex_coords = self.get_tex_coord_data(mesh_name)
            # write_to_shared_memory()
            # # 包含变形信息的数据结构
            # data = {
            #     "vertices": vertices,
            #     "faces": faces,
            #     "tex_coords": tex_coords,
            #     "deformation_info": deformation_info or {},
            #     "timestamp": time.time(),
            #     "monitor_name": self.monitor_name,
            #     "mesh_name": mesh_name
            # }
            # vertices, faces, combined_list
            # # 写入共享内存文件
            # with open(self.shared_memory_file, "w+b") as f:
            #     data_bytes = pickle.dumps(data)
            #     data_size = len(data_bytes)
            #
            #     f.write(data_size.to_bytes(4, byteorder='big'))
            #     f.write(data_bytes)
            #     f.flush()
            #     os.fsync(f.fileno())
            write_to_shared_memory([vertices, faces, combined_list, vertex_normals],
                                   shared_file=os.path.join("D:", "Personal", "zhankangming", "Desktop", 'model_monitors', 'pSphere1', "model_data.bin"))
            print(f"? [{self.monitor_name}] 共享内存已更新")
            return True

        except Exception as e:
            print(f"? [{self.monitor_name}] 更新共享内存失败: {e}")
            return False

    def start_monitoring(self, mesh_name):
        """开始监控指定网格的变形"""
        if self.monitoring:
            print(f"?? [{self.monitor_name}] 监控已在运行中")
            return

        self.monitoring = True
        print(f"? [{self.monitor_name}] 开始监控模型: {mesh_name}")

        # 初始化顶点位置记录
        self.last_vertex_positions[mesh_name] = self.get_mesh_vertex_positions(mesh_name)

        def monitoring_loop():
            while self.monitoring:
                try:
                    has_deformation, total_deform, max_deform, deform_count = self.detect_deformation(mesh_name)

                    if has_deformation:
                        # 准备变形信息
                        deformation_info = {
                            "total_deformation": total_deform,
                            "max_deformation": max_deform,
                            "deformed_vertex_count": deform_count,
                            "detection_time": time.time()
                        }

                        # 更新共享内存
                        print('更新共享内存')
                        self.update_shared_memory(mesh_name, deformation_info)

                    time.sleep(self.check_interval)
                except Exception as e:
                    print(f"[{self.monitor_name}] 监控循环错误: {e}")
                    time.sleep(self.check_interval)

        self.monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """停止监控并打印最终统计"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

        stats = self.get_deformation_statistics()
        print(f"\n? [{self.monitor_name}] 监控结束 - 最终统计:")
        print(f"   ? 总变形次数: {stats['deformation_count']}")
        print(f"   ? 累计变形量: {stats['total_deformation']:.6f}")
        print(f"   ? 最大单次变形: {stats['max_deformation']:.6f}")
        print(f"   ? 平均变形量: {stats['average_deformation']:.6f}")
        print("? 监控任务完成!")


# 使用示例和UI增强
def create_advanced_monitor_ui():
    """创建增强版的变形监控UI界面"""
    if cmds.window("advancedDeformationMonitorUI", exists=True):
        cmds.deleteUI("advancedDeformationMonitorUI")

    window = cmds.window("advancedDeformationMonitorUI", title="高级模型变形监控器", width=400)
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="高级模型变形实时监控", align="center", height=30, font="boldLabelFont")
    cmds.separator(height=10)

    # 监控器名称输入
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="监控器名称:", width=80)
    monitor_name_field = cmds.textField(text="主变形监控器", width=200)
    cmds.setParent("..")

    # 阈值设置
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="检测阈值:", width=80)
    threshold_field = cmds.floatField(value=0.01, minValue=0.001, maxValue=1.0, width=200)
    cmds.setParent("..")

    # 间隔设置
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="检测间隔(秒):", width=80)
    interval_field = cmds.floatField(value=0.01, minValue=0.001, maxValue=2.0, width=200)
    cmds.setParent("..")

    cmds.separator(height=10)
    cmds.text(label="选择要监控的网格，然后点击开始监控", align="center")
    cmds.separator(height=10)

    # 按钮区域
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)

    def start_advanced_monitor(*args):
        monitor_name = cmds.textField(monitor_name_field, query=True, text=True)
        threshold = cmds.floatField(threshold_field, query=True, value=True)
        interval = cmds.floatField(interval_field, query=True, value=True)

        global g_advanced_monitor
        try:
            if 'g_advanced_monitor' in globals() and g_advanced_monitor:
                g_advanced_monitor.stop_monitoring()

            selected = cmds.ls(selection=True)
            if not selected:
                cmds.warning("请先选择一个网格模型")
                return

            mesh_name = selected[0]
            shapes = cmds.listRelatives(mesh_name, shapes=True, type="mesh")
            if not shapes:
                cmds.warning("请选择一个有效的网格模型")
                return

            # 创建高级监控器实例
            shared_file = os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem.bin")
            g_advanced_monitor = AdvancedDeformationMonitor(
                shared_file, monitor_name, interval
            )
            g_advanced_monitor.deformation_threshold = threshold

            # 立即更新一次共享内存
            g_advanced_monitor.update_shared_memory(mesh_name)

            # 开始监控
            g_advanced_monitor.start_monitoring(mesh_name)

            cmds.confirmDialog(title="监控启动",
                               message=f"监控器 '{monitor_name}' 已启动监控模型: {mesh_name}")

        except Exception as e:
            cmds.warning(f"启动失败: {e}")

    cmds.button(label="? 开始高级监控", command=start_advanced_monitor, height=40)

    def stop_advanced_monitor(*args):
        global g_advanced_monitor
        try:
            if 'g_advanced_monitor' in globals() and g_advanced_monitor:
                g_advanced_monitor.stop_monitoring()
                g_advanced_monitor = None
                cmds.confirmDialog(title="监控停止", message="高级变形监控已停止")
            else:
                cmds.warning("没有运行的监控实例")
        except Exception as e:
            cmds.warning(f"停止失败: {e}")

    cmds.button(label="?? 停止监控", command=stop_advanced_monitor, height=40)

    def show_stats(*args):
        global g_advanced_monitor
        try:
            if 'g_advanced_monitor' in globals() and g_advanced_monitor:
                stats = g_advanced_monitor.get_deformation_statistics()
                message = f"监控器: {stats['monitor_name']}\n"
                message += f"变形次数: {stats['deformation_count']}\n"
                message += f"累计变形: {stats['total_deformation']:.6f}\n"
                message += f"最大变形: {stats['max_deformation']:.6f}"
                cmds.confirmDialog(title="当前统计", message=message)
            else:
                cmds.warning("没有运行的监控实例")
        except Exception as e:
            cmds.warning(f"获取统计失败: {e}")

    cmds.button(label="? 查看统计", command=show_stats, height=40)
    cmds.setParent("..")

    cmds.separator(height=10)
    cmds.text(label="共享内存文件路径:", align="left")
    shared_path = os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem.bin")
    cmds.text(label=shared_path, align="center")

    cmds.showWindow(window)


# 快速启动函数
def quick_start_advanced():
    """快速启动高级监控"""
    global g_advanced_monitor
    try:
        if 'g_advanced_monitor' in globals() and g_advanced_monitor:
            g_advanced_monitor.stop_monitoring()

        selected = cmds.ls(selection=True)
        if not selected:
            cmds.warning("请先选择一个网格模型")
            return

        mesh_name = selected[0]
        shared_file = os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem.bin")

        g_advanced_monitor = AdvancedDeformationMonitor(shared_file, "快速监控器", 0.3)
        g_advanced_monitor.start_monitoring(mesh_name)

        print(f"? 高级变形监控已启动: {mesh_name}")

    except Exception as e:
        print(f"? 启动失败: {e}")
# 获取maya模型数据
def get_mesh_structure(model_name):
    # 将名称转换为 MObject
    # 1. 通过名称获取 MObject
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

    # 创建选择列表获取形状节点的MObject
    shape_sel = om.MSelectionList()
    shape_sel.add(shape_names[0])
    shape_mobject = shape_sel.getDependNode(0)
    # 获取DAG路径用于面迭代器
    dag_path = om.MDagPath.getAPathTo(shape_mobject)

    # 如果是网格，则创建MFnMesh对象以访问网格数据
    mesh_fn = om.MFnMesh(shape_mobject)
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

    print('已获取当前选择模型结构数据。')
    # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
    vertices = vertex_positions
    normal_list = [list(mintarray) for mintarray in all_topology]
    faces = normal_list
    list1 = uv_coords_us
    list2 = uv_coords_vs
    combined_list = list(zip(list1, list2))
    return vertices, faces, combined_list, vertex_normals
    # return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group
def write_to_shared_memory(data,shared_file):
    # 使用pickle序列化数据（更可靠）
    data_bytes = pickle.dumps(data)
    data_size = len(data_bytes)
    total_size = 4 + data_size  # 头部4字节 + 数据本身

    print(f"数据大小: {data_size} 字节, 需要分配: {total_size} 字节")

    with open(shared_file, "wb") as f:
        # 分配足够的空间：头部4字节 + 数据本身
        f.write(b'\x00' * total_size)

    with open(shared_file, "r+b") as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            # 确保有足够空间
            if len(mm) < total_size:
                raise ValueError(f"内存映射大小不足: {len(mm)} < {total_size}")

            mm.seek(0)
            # 写入数据长度（4字节）
            mm.write(data_size.to_bytes(4, byteorder='big'))
            # 写入实际数据
            mm.write(data_bytes)
            mm.flush()

    print(f"数据写入成功，总共写入 {total_size} 字节")
# 运行高级UI界面
create_advanced_monitor_ui()