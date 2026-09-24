#coding=gbk
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
from PySide6 import QtWidgets, QtGui, QtCore
import shiboken6

# 获取投射位置，最近点名称以及距离
def get_closest_vertex():
    # 1. 获取选中的模型
    selection = cmds.ls(sl=True, long=True)
    if not selection:
        cmds.warning("请先选中一个多边形模型！")
        return

    # 2. 获取视口并处理坐标翻转
    active_view = omui.M3dView.active3dView()
    view_ptr = active_view.widget()
    widget = shiboken6.wrapInstance(int(view_ptr), QtWidgets.QWidget)

    global_pos = QtGui.QCursor.pos()
    local_pos = widget.mapFromGlobal(global_pos)

    _, _, _, vheight = active_view.viewport()
    final_x = int(local_pos.x())
    final_y = int(vheight - local_pos.y())

    # 3. 转换射线
    ray_source = om.MPoint()
    ray_direction = om.MVector()
    active_view.viewToWorld(final_x, final_y, ray_source, ray_direction)

    found = False
    for obj in selection:
        try:
            sel_list = om.MSelectionList()
            sel_list.add(obj)
            dag_path = sel_list.getDagPath(0)

            if not dag_path.hasFn(om.MFn.kMesh):
                dag_path.extendToShape()

            fn_mesh = om.MFnMesh(dag_path)

            # --- A. 射线检测获取表面坐标和所在的 Face ID ---
            hit_info = fn_mesh.closestIntersection(
                om.MFloatPoint(ray_source),
                om.MFloatVector(ray_direction),
                om.MSpace.kWorld,
                999999.0,
                True
            )

            if hit_info:
                hit_point = om.MPoint(hit_info[0])
                face_id = hit_info[2]  # 获取碰撞点所在的三角面/多边形 ID

                # --- B. 寻找该面上最近的顶点 ---
                # 获取该多边形包含的所有顶点索引
                face_vertices = fn_mesh.getPolygonVertices(face_id)

                closest_vtx_id = -1
                min_dist = float('inf')

                for vtx_id in face_vertices:
                    # 获取顶点坐标
                    vtx_pos = fn_mesh.getPoint(vtx_id, space=om.MSpace.kWorld)
                    # 计算到点击点的距离
                    dist = hit_point.distanceTo(vtx_pos)

                    if dist < min_dist:
                        min_dist = dist
                        closest_vtx_id = vtx_id

                # 4. 格式化输出
                if closest_vtx_id != -1:
                    full_vertex_name = f"{obj}.vtx[{closest_vtx_id}]"
                    # print("-" * 50)
                    # print(f"鼠标点击位置: {hit_point.x:.4f}, {hit_point.y:.4f}, {hit_point.z:.4f}")
                    # print(f"最近顶点名称: {full_vertex_name}")
                    # print(f"距离差值: {min_dist:.6f}")
                    # print("-" * 50)
                    found = True
                    return [[hit_point.x, hit_point.y, hit_point.z], full_vertex_name, min_dist]
                    # break
        except Exception as e:
            print(f"处理失败: {e}")
            continue

    if not found:
        print("未击中任何模型表面。")
        return None

# 获取当前绘制选择蒙皮
def get_current_paint_skin_cluster():
    """
    针对 Maya 2025 蒙皮笔刷面板获取当前选中的真实蒙皮节点名
    """
    # 控件名称根据你的日志确定为 'skinClusterPaintList'
    list_control = 'skinClusterPaintList'

    # 1. 优先尝试从 UI 列表控件获取
    if cmds.textScrollList(list_control, q=True, exists=True):
        # 获取选中的显示名称列表
        selected_items = cmds.textScrollList(list_control, q=True, selectItem=True)

        if selected_items:
            # 还原真实节点名：将日志中的 " → " (u'\u2192') 换回 "|"
            # 即使没有层级符号，replace 也不影响普通字符串
            display_name = selected_items[0]
            real_skin_cluster = display_name.replace(u' \u2192 ', '|')
            return real_skin_cluster

    # 2. 如果 UI 获取不到，使用上下文查询（注意：必须是 artAttrSkinPaintCtx）
    ctx = "artSkinPaintContext"
    if cmds.contextInfo(ctx, ex=True):
        try:
            # 查询笔刷当前绑定的 skinCluster
            active_sc = cmds.artAttrSkinPaintCtx(ctx, q=True, skinCluster=True)
            if active_sc:
                return active_sc
        except Exception as e:
            print(f"上下文查询失败: {e}")

# 获取当前点当前蒙皮权重
def get_max_weight_influence(point, skin_cluster):
    # 2. 获取该点的所有权重值
    # transformValues=True 会返回 (骨骼名, 权重值) 的对子
    weights = cmds.skinPercent(skin_cluster, point, query=True, value=True)
    influences = cmds.skinCluster(skin_cluster, q=True, inf=True)
    # print(weights,influences)
    # 3. 将骨骼名与权重值一一对应
    weight_map = dict(zip(influences, weights))

    # 4. 找到权重最大的骨骼
    max_influence = max(weight_map, key=weight_map.get)
    max_value = weight_map[max_influence]

    return max_influence, max_value

mel.eval("ArtPaintSkinWeightsTool;")
list = get_closest_vertex()
skin = get_current_paint_skin_cluster()
if list and skin:
    inf_name, val = result = get_max_weight_influence(list[1], skin)
    mel.eval('artSkinInflListChanging \"' + inf_name + '\" 1;''artSkinInflListChanged artAttrSkinPaintCtx;refreshAE;')


