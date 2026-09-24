# coding=gbk
import maya.OpenMaya as om
import maya.cmds as cmds


def merge_selected_splines():
    """
    将选中的多条 NURBS 曲线合并为一条新的曲线
    修复了 MDagPath 导致的世界空间转换错误
    """
    # 1. 获取当前选择列表
    selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection)

    if selection.length() < 2:
        cmds.warning("请选择至少两条 NURBS 曲线进行合并")
        return None

    combined_cvs = om.MPointArray()
    first_degree = 3
    first_form = om.MFnNurbsCurve.kOpen
    is_rational = False
    found_curves_count = 0

    # 2. 遍历所有选中对象
    for i in range(selection.length()):
        # 获取 DAG 路径
        dag_path = om.MDagPath()
        selection.getDagPath(i, dag_path)

        # 寻找曲线形状节点 (Shape Node)
        # 如果选中的是 Transform，尝试延伸到其 Shape
        if not dag_path.hasFn(om.MFn.kNurbsCurve):
            try:
                # 尝试延伸到第一个 Shape 节点
                dag_path.extendToShape()
            except:
                # 如果该路径下没有 Shape，跳过
                continue

        # 再次检查确认当前路径指向的是 NURBS 曲线
        if dag_path.hasFn(om.MFn.kNurbsCurve):
            # 重要：使用 MDagPath 初始化 MFnNurbsCurve 以支持世界空间
            curve_fn = om.MFnNurbsCurve(dag_path)

            current_cvs = om.MPointArray()
            # 现在可以安全地使用 kWorld 了
            curve_fn.getCVs(current_cvs, om.MSpace.kWorld)

            if found_curves_count == 0:
                first_degree = curve_fn.degree()
                first_form = curve_fn.form()

            for k in range(current_cvs.length()):
                combined_cvs.append(current_cvs[k])
                if current_cvs[k].w != 1.0:
                    is_rational = True

            found_curves_count += 1

    if found_curves_count < 2:
        cmds.warning("未找到足够的有效 NURBS 曲线节点")
        return None

    # 3. 计算新的节点矢量 (Knots)
    num_cvs = combined_cvs.length()
    num_knots = num_cvs + first_degree - 1
    new_knots = om.MDoubleArray()

    counter = 0.0
    for i in range(num_knots):
        if i < first_degree:
            new_knots.append(0.0)
        elif i <= (num_cvs - 1):
            counter += 1.0
            new_knots.append(counter)
        else:
            new_knots.append(counter + 1.0)

    # 4. 创建合并后的新曲线
    new_curve_fn = om.MFnNurbsCurve()

    new_shape_obj = new_curve_fn.create(
        combined_cvs,
        new_knots,
        first_degree,
        first_form,
        is_rational,
        False,
        om.MObject()
    )

    # 5. 反馈
    new_dag_fn = om.MFnDagNode(new_shape_obj)
    cmds.select(new_dag_fn.fullPathName())
    print("成功合并 %d 条曲线到新对象。" % found_curves_count)


merge_selected_splines()