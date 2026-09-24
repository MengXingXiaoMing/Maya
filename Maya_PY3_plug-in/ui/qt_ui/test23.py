# coding=gbk
import maya.OpenMaya as om
import maya.cmds as cmds


def duplicate_selected_spline():
    """
    获取选中的 NURBS 曲线数据并创建一个副本
    使用 Maya Python API 1.0
    """
    # 1. 获取当前选择
    selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection)

    if selection.length() < 1:
        cmds.warning("请选择一条NURBS曲线")
        return None

    # 获取第一个选中的对象
    selected_node = om.MObject()
    selection.getDependNode(0, selected_node)

    # 2. 寻找曲线形状节点 (Shape Node)
    curve_shape = om.MObject()

    if selected_node.hasFn(om.MFn.kNurbsCurve):
        curve_shape = selected_node
    elif selected_node.hasFn(om.MFn.kTransform):
        dag_node = om.MFnDagNode(selected_node)
        # 遍历子节点找 Shape
        for i in range(dag_node.childCount()):
            child = dag_node.child(i)
            if child.hasFn(om.MFn.kNurbsCurve):
                curve_shape = child
                break

    if curve_shape.isNull():
        cmds.warning("未找到有效的 NURBS 曲线形状节点")
        return None

    # 3. 提取曲线数据
    curve_fn = om.MFnNurbsCurve(curve_shape)

    cvs = om.MPointArray()
    curve_fn.getCVs(cvs, om.MSpace.kObject)  # 获取物体空间坐标

    knots = om.MDoubleArray()
    curve_fn.getKnots(knots)

    # 注意：API 1.0 中这些是方法，必须带括号 ()
    degree = curve_fn.degree()
    form = curve_fn.form()

    # 判断是否为有理曲线 (Rational)
    is_rational = False
    for i in range(cvs.length()):
        if cvs[i].w != 1.0:
            is_rational = True
            break

    # 4. 创建新曲线
    new_curve_fn = om.MFnNurbsCurve()

    # API 1.0 Python 参数顺序:
    # (cvs, knots, degree, form, isRational, is2D, parent)
    # 注意：这里没有 status 参数！
    new_shape_obj = new_curve_fn.create(
        cvs,
        knots,
        degree,
        form,
        is_rational,
        False,  # is2D
        om.MObject()  # parent (传空对象 Maya 会自动创建新的 Transform)
    )

    # 5. 重命名与选择
    # 获取新曲线的变换节点 (Parent)
    new_dag_fn = om.MFnDagNode(new_shape_obj)
    new_transform_obj = new_dag_fn.parent(0)

    # 获取原始名称用于参考
    orig_name = om.MFnDagNode(selected_node).name()


duplicate_selected_spline()