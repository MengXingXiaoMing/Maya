# coding=gbk
import maya.cmds as cmds
import os
import pickle
import threading
import time
import math
import mmap
import maya.cmds as cmds
maya_useNewAPI = True
import maya.api.OpenMaya as om
import os
import pickle
def get_mesh_point(model_name):
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
            # 关键：将 MObject 转换为节点名称
            shape_fn = om.MFnDependencyNode(child)
            shape_name = shape_fn.name()
            shape_names.append(shape_name)

    # 创建选择列表获取形状节点的MObject
    shape_sel = om.MSelectionList()
    shape_sel.add(shape_names[0])
    shape_mobject = shape_sel.getDependNode(0)

    # 如果是网格，则创建MFnMesh对象以访问网格数据
    mesh_fn = om.MFnMesh(shape_mobject)
    # 获取网格的顶点数
    num_verts = mesh_fn.numVertices
    # 获取网格的面数

    # 创建一个列表来存储顶点位置
    vertex_positions = []
    # 遍历所有顶点并获取它们的位置
    for i in range(num_verts):
        point = mesh_fn.getPoint(i)
        vertex_positions.append([point.x, point.y, point.z])


    return vertex_positions
    # return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group
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
    # num_faces = mesh_fn.numPolygons
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

        '''# 获取当前面的UV索引 [uv0, uv1, uv2, ...]
        face_uv_indices = []
        for i in range(len(face_vert_indices)):
            uv_index = face_iter.getUVIndex(i)  # 按顶点顺序获取UV索引
            face_uv_indices.append(uv_index)
        all_uv_topology.append(face_uv_indices)'''

        face_iter.next()  # 移动到下一个面
    # print('拓扑', all_topology)

    # print('已获取当前选择模型结构数据。')
    # 返回当前选择的名称、点数组、顶点法线数组、拓扑数组、UV的u值，、UV的v值
    normal_list = [list(mintarray) for mintarray in all_topology]
    faces = normal_list
    list1 = uv_coords_us
    list2 = uv_coords_vs
    combined_list = list(zip(list1, list2))
    return vertex_positions, faces, combined_list, vertex_normals
    # return name, vertex_positions, vertex_normals, all_topology, uv_coords_us, uv_coords_vs, all_uv_topology, smooth_group


def write_to_shared_memory(data, shared_file):
    """安全写入共享内存"""
    try:
        # 序列化数据
        data_bytes = pickle.dumps(data)
        data_size = len(data_bytes)
        total_size = 4 + data_size

        # 使用临时文件写入
        temp_file = shared_file + ".tmp"
        with open(temp_file, "wb") as f:
            f.write(data_size.to_bytes(4, byteorder='big'))
            f.write(data_bytes)
            f.flush()
            os.fsync(f.fileno())

        # 原子替换文件
        if os.path.exists(shared_file):
            os.remove(shared_file)
        os.rename(temp_file, shared_file)
        print(f"? 数据安全写入: {shared_file}")
    except Exception as e:
        print(f"? 写入共享内存失败: {e}")
class IndependentModelMonitor:
    """独立目录多模型监控系统 - 每个模型完全独立"""

    def __init__(self, base_root_dir, check_interval=0.3):
        """
        初始化独立监控器
        :param base_root_dir: 基础根目录，每个模型在此创建独立子目录
        :param check_interval: 检查间隔
        """
        self.base_root_dir = base_root_dir
        self.check_interval = check_interval
        self.model_monitors = {}  # {model_name: monitor_data}
        self.active = False

        # 确保基础根目录存在
        if not os.path.exists(self.base_root_dir):
            os.makedirs(self.base_root_dir)
            print(f"? 创建基础根目录: {self.base_root_dir}")

    def add_model_monitor(self, model_name):
        """添加模型监控 - 修复版本"""
        if model_name in self.model_monitors:
            print(f"?? 模型 {model_name} 已在监控中")
            return False

        # 创建模型专属目录和文件
        model_dir, shared_file = self.create_model_directory(model_name)

        # 初始化监控数据
        monitor_data = {
            'model_dir': model_dir,
            'shared_file': shared_file,
            'last_positions': get_mesh_point(model_name),
            'thread': None,
            'active': False,
            'deformation_count': 0
        }

        self.model_monitors[model_name] = monitor_data

        # 立即生成初始数据
        self.update_model_data(model_name)

        print(f"? 添加模型监控: {model_name} -> {model_dir}")
        return True

    def create_model_directory(self, model_name):
        """为每个模型创建独立的监控目录"""
        # 清理模型名称中的非法字符
        safe_name = ''.join(c if c.isalnum() else '_' for c in model_name)

        # 创建模型专属目录
        model_dir = os.path.join(self.base_root_dir, safe_name)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            print(f"? 创建模型专属目录: {model_dir}")

        # 在模型目录下创建共享文件
        shared_file = os.path.join(model_dir, "model_data.bin")

        return model_dir, shared_file



    def update_model_data(self, model_name):
        """更新模型数据到独立文件"""
        try:
            if model_name not in self.model_monitors:
                return False

            monitor_data = self.model_monitors[model_name]
            shared_file = monitor_data['shared_file']

            # 获取模型结构数据
            vertices, faces, combined_list, vertex_normals = get_mesh_structure(model_name)

            # 组织数据
            data = {
                "model_name": model_name,
                "vertices": vertices,
                "faces": faces,
                "tex_coords": combined_list,
                "normals": vertex_normals,
                "timestamp": time.time(),
                "deformation_count": monitor_data['deformation_count'],
                "monitor_dir": monitor_data['model_dir']
            }
            data = [vertices, faces, combined_list, vertex_normals]
            write_to_shared_memory(data, shared_file)
            # # 写入独立文件
            # with open(shared_file, "wb") as f:
            #     pickle.dump(data, f)
            #     f.flush()
            #     os.fsync(f.fileno())

            print(f"? {model_name} 数据已更新到: {shared_file}")
            return True

        except Exception as e:
            print(f"? 更新 {model_name} 数据失败: {e}")
            return False

    def start_model_monitor(self, model_name):
        """启动单个模型的监控"""
        if model_name not in self.model_monitors:
            print(f"? 模型 {model_name} 未添加监控")
            return False

        monitor_data = self.model_monitors[model_name]
        if monitor_data['active']:
            print(f"?? 模型 {model_name} 已在监控中")
            return False

        monitor_data['active'] = True

        def monitoring_loop():
            while monitor_data['active']:
                try:
                    # 检测变形
                    if self.detect_model_deformation(model_name):
                        self.update_model_data(model_name)
                        monitor_data['deformation_count'] += 1

                    time.sleep(self.check_interval)
                except Exception as e:
                    print(f"? 监控 {model_name} 时出错: {e}")
                    time.sleep(self.check_interval)

        # 启动监控线程
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_data['thread'] = thread
        thread.start()

        print(f"? 启动模型监控: {model_name}")
        return True

    def detect_model_deformation(self, model_name):
        """检测单个模型的变形"""
        if model_name not in self.model_monitors:
            return False

        monitor_data = self.model_monitors[model_name]
        current_positions = get_mesh_point(model_name)
        last_positions = monitor_data['last_positions']

        if not last_positions or not current_positions:
            monitor_data['last_positions'] = current_positions
            return False

        # 检查顶点数量变化（拓扑结构变化）
        if len(last_positions) != len(current_positions):
            print(f"? {model_name} 拓扑结构发生变化")
            monitor_data['last_positions'] = current_positions
            return True

        # 检查顶点位置变化
        deformation_threshold = 0.01
        for i, (current, last) in enumerate(zip(current_positions, last_positions)):
            distance = math.sqrt(
                (current[0] - last[0]) ** 2 +
                (current[1] - last[1]) ** 2 +
                (current[2] - last[2]) ** 2
            )
            if distance > deformation_threshold:
                print(f"? {model_name} 顶点 {i} 发生变形，距离: {distance:.4f}")
                monitor_data['last_positions'] = current_positions
                return True

        return False

    def remove_model_monitor(self, model_name):
        """移除模型监控"""
        self.stop_model_monitor(model_name)
        if model_name in self.model_monitors:
            del self.model_monitors[model_name]
            print(f"?? 移除模型监控: {model_name}")
            return True
        return False

    def stop_model_monitor(self, model_name):
        """停止单个模型的监控"""
        if model_name not in self.model_monitors:
            return False

        monitor_data = self.model_monitors[model_name]
        monitor_data['active'] = False

        if monitor_data['thread']:
            monitor_data['thread'].join(timeout=2)
            monitor_data['thread'] = None

        print(f"?? 停止模型监控: {model_name}")
        return True

    def start_all_monitors(self):
        """启动所有模型监控"""
        self.active = True
        started_count = 0

        for model_name in list(self.model_monitors.keys()):
            if self.start_model_monitor(model_name):
                started_count += 1

        print(f"? 启动 {started_count} 个模型监控")
        return started_count

    def stop_all_monitors(self):
        """停止所有模型监控"""
        self.active = False
        stopped_count = 0

        for model_name in list(self.model_monitors.keys()):
            if self.stop_model_monitor(model_name):
                stopped_count += 1

        print(f"?? 停止 {stopped_count} 个模型监控")
        return stopped_count

    def get_monitor_status(self):
        """获取所有监控器状态"""
        status = {}
        for model_name, monitor_data in self.model_monitors.items():
            status[model_name] = {
                'active': monitor_data['active'],
                'directory': monitor_data['model_dir'],
                'shared_file': monitor_data['shared_file'],
                'deformation_count': monitor_data['deformation_count']
            }
        return status


# 全局变量声明
g_independent_monitor = None


# 创建独立目录监控UI
def create_independent_monitor_ui():
    """创建独立目录监控UI界面"""
    if cmds.window("independentMonitorUI", exists=True):
        cmds.deleteUI("independentMonitorUI")

    window = cmds.window("independentMonitorUI", title="独立目录多模型监控", width=600)
    cmds.columnLayout(adjustableColumn=True)

    # 标题
    cmds.text(label="独立目录多模型监控系统", align="center", height=30, font="boldLabelFont")
    cmds.separator(height=10)

    # 基础根目录设置
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[100, 400], adjustableColumn=2)
    cmds.text(label="基础根目录:", align="right")
    base_dir_field = cmds.textField(text="D:/Personal/zhankangming/Desktop/model_monitors")
    cmds.setParent("..")

    # 监控间隔设置
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[100, 100], adjustableColumn=2)
    cmds.text(label="监控间隔(秒):", align="right")
    interval_field = cmds.floatField(value=0.01, minValue=0.001, maxValue=1.0)
    cmds.setParent("..")

    cmds.separator(height=10)

    # 模型管理区域
    cmds.frameLayout(label="模型管理", marginWidth=5, marginHeight=5)
    cmds.columnLayout(adjustableColumn=True)

    # 模型列表
    cmds.text(label="已添加的模型:", align="left")
    model_list = cmds.textScrollList(numberOfRows=6, allowMultiSelection=True)

    # 模型操作按钮
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[120, 120, 120, 120], adjustableColumn=4)

    def add_selected_model(*args):
        """添加选中的模型"""
        global g_independent_monitor

        # 确保监控器已初始化
        if g_independent_monitor is None:
            # 从UI获取参数并初始化监控器
            base_dir = cmds.textField(base_dir_field, query=True, text=True)
            interval = cmds.floatField(interval_field, query=True, value=True)
            g_independent_monitor = IndependentModelMonitor(base_dir, interval)
            print("? 监控器已初始化")

        selected = cmds.ls(selection=True)
        if not selected:
            cmds.warning("请先选择模型")
            return

        added_count = 0
        for model in selected:
            shapes = cmds.listRelatives(model, shapes=True, type="mesh")
            if shapes:
                if g_independent_monitor.add_model_monitor(model):
                    cmds.textScrollList(model_list, edit=True, append=model)
                    added_count += 1

        if added_count > 0:
            print(f"? 成功添加 {added_count} 个模型")
        else:
            cmds.warning("没有有效的网格模型被添加")

    cmds.button(label="? 添加选中模型", command=add_selected_model)

    def remove_selected_model(*args):
        """移除选中的模型"""
        global g_independent_monitor

        if g_independent_monitor is None:
            cmds.warning("监控器未初始化，请先添加模型")
            return

        selected = cmds.textScrollList(model_list, query=True, selectItem=True)
        if selected:
            removed_count = 0
            for model in selected:
                if g_independent_monitor.remove_model_monitor(model):
                    cmds.textScrollList(model_list, edit=True, removeItem=model)
                    removed_count += 1

            if removed_count > 0:
                print(f"? 成功移除 {removed_count} 个模型")
        else:
            cmds.warning("请先选择要移除的模型")

    cmds.button(label="? 移除选中模型", command=remove_selected_model)

    def clear_all_models(*args):
        """清空所有模型"""
        global g_independent_monitor

        if g_independent_monitor is None:
            cmds.warning("监控器未初始化")
            return

        models = cmds.textScrollList(model_list, query=True, allItems=True) or []
        if not models:
            cmds.warning("模型列表为空")
            return

        for model in models:
            g_independent_monitor.remove_model_monitor(model)

        cmds.textScrollList(model_list, edit=True, removeAll=True)
        print("? 已清空所有模型")

    cmds.button(label="?? 清空所有模型", command=clear_all_models)

    def show_model_info(*args):
        """显示模型信息"""
        global g_independent_monitor

        if g_independent_monitor is None:
            cmds.warning("监控器未初始化")
            return

        selected = cmds.textScrollList(model_list, query=True, selectItem=True)
        if selected:
            model_name = selected[0]
            status = g_independent_monitor.get_monitor_status().get(model_name, {})
            if status:
                message = f"模型: {model_name}\n"
                message += f"状态: {'运行中' if status['active'] else '已停止'}\n"
                message += f"目录: {status['directory']}\n"
                message += f"变形次数: {status['deformation_count']}"
                cmds.confirmDialog(title="模型信息", message=message)
        else:
            cmds.warning("请先选择一个模型")

    cmds.button(label="?? 模型信息", command=show_model_info)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    cmds.separator(height=10)

    # 监控控制区域
    cmds.frameLayout(label="监控控制", marginWidth=5, marginHeight=5)
    cmds.columnLayout(adjustableColumn=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=[180, 180, 180], adjustableColumn=3)

    def start_all_monitors(*args):
        """启动所有监控"""
        global g_independent_monitor

        # 获取UI设置
        base_dir = cmds.textField(base_dir_field, query=True, text=True)
        interval = cmds.floatField(interval_field, query=True, value=True)

        # 创建或更新监控器
        if g_independent_monitor is None:
            g_independent_monitor = IndependentModelMonitor(base_dir, interval)
        else:
            # 更新现有监控器的设置
            g_independent_monitor.base_root_dir = base_dir
            g_independent_monitor.check_interval = interval

        started_count = g_independent_monitor.start_all_monitors()
        cmds.confirmDialog(title="监控启动", message=f"已启动 {started_count} 个模型监控")

    cmds.button(label="? 启动所有监控", command=start_all_monitors, height=40)

    def stop_all_monitors(*args):
        """停止所有监控"""
        global g_independent_monitor

        if g_independent_monitor is None:
            cmds.warning("没有运行的监控实例")
            return

        stopped_count = g_independent_monitor.stop_all_monitors()
        cmds.confirmDialog(title="监控停止", message=f"已停止 {stopped_count} 个模型监控")

    cmds.button(label="?? 停止所有监控", command=stop_all_monitors, height=40)

    def show_system_status(*args):
        """显示系统状态"""
        global g_independent_monitor

        if g_independent_monitor is None:
            cmds.warning("没有运行的监控实例")
            return

        status = g_independent_monitor.get_monitor_status()
        message = f"系统状态报告\n"
        message += f"监控模型数量: {len(status)}\n"
        message += f"运行中模型: {sum(1 for s in status.values() if s['active'])}\n"
        message += f"基础根目录: {g_independent_monitor.base_root_dir}\n"
        message += "─" * 30 + "\n"

        for model_name, info in status.items():
            message += f"{model_name}: {'?运行中' if info['active'] else '??已停止'} "
            message += f"(变形:{info['deformation_count']})\n"

        cmds.scrollFieldDialog(title="系统状态", message=message, w=500, h=300)

    cmds.button(label="? 系统状态", command=show_system_status, height=40)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    # 初始化监控器
    global g_independent_monitor
    if g_independent_monitor is None:
        base_dir = cmds.textField(base_dir_field, query=True, text=True)
        interval = cmds.floatField(interval_field, query=True, value=True)
        g_independent_monitor = IndependentModelMonitor(base_dir, interval)
        print("? 独立目录监控器已初始化")

    cmds.showWindow(window)


# 主启动函数
def start_independent_monitor_ui():
    """启动独立目录监控UI"""
    create_independent_monitor_ui()


# 启动UI
start_independent_monitor_ui()