# -*- coding: utf-8 -*-
"""
魔方绑定节点 (rubikCubeNode)
============================

功能
----
固定 3×3×3 的魔方绑定节点，配合 `buildRubikCube()` 构建脚本使用：

- 6 个侧面控制器分别控制 6 个面（±X / ±Y / ±Z），每个面绕各自轴旋转。
- 当某个轴的控制器数值不是 90° 的整数倍时，其它轴的控制器自动隐藏，
  此时只有当前轴的两个控制器可以继续操作。
- 当所有控制器都回到 90° 的整数倍时，其它轴的控制器重新显示。
- 节点内部记录"已提交"的旋转状态：只有控制器到达 90° 整数倍时，才会把
  这次转动固化（提交）到魔方状态中；未到达整数倍时仅做临时显示旋转，
  这就是"记录上一次数值 -> 判断要转多少 -> 达到 90° 倍数后清空记录"的实现。

设计说明
--------
- 每个小方块记录：网格坐标 (px, py, pz) + 方向四元数 (qx, qy, qz, qw)。
- 提交(commit)：控制器角度吸附到 90° 整数倍时，用 `delta = 吸附值 - 已提交值`
  对当前处于该面切片内的方块执行一次旋转，然后更新已提交值。
- 显示(display)：未吸附时，把 `raw - 已提交值` 作为临时增量旋转显示出来。
- 状态以 JSON 字符串形式存在隐藏属性 `cubeState` 中，避免大量散列属性。

用法
----
    import maya.cmds as cmds
    cmds.loadPlugin('rubikCube.py')
    import rubikCube
    rubikCube.buildRubikCube()
"""

import sys
import math
import json

import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds

# 判断"是否吸附到 90° 整数倍"的容差（单位：度）
SNAP_EPS = 0.01

# 6 个面的定义：(轴索引, 切片坐标)
# 轴索引：0 = X, 1 = Y, 2 = Z；切片坐标：-1 负向面，+1 正向面
FACES = [
    (0, -1),  # 0 左面 (X 负向)
    (0, +1),  # 1 右面 (X 正向)
    (1, -1),  # 2 下面 (Y 负向)
    (1, +1),  # 3 上面 (Y 正向)
    (2, -1),  # 4 后面 (Z 负向)
    (2, +1),  # 5 前面 (Z 正向)
]

# 6 个控制器输入属性长名
INPUT_NAMES = ["rotXN", "rotXP", "rotYN", "rotYP", "rotZN", "rotZP"]

# 6 个控制器输入属性短名
INPUT_SHORTS = ["rxn", "rxp", "ryn", "ryp", "rzn", "rzp"]

CUBIE_COUNT = 27


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------
def home_position(index):
    """返回第 index 个小方块的初始网格坐标 (x, y, z)，范围均为 -1..1。"""
    x = (index % 3) - 1
    y = ((index // 3) % 3) - 1
    z = (index // 9) - 1
    return x, y, z


def _axis_quat(axis, degrees):
    """返回绕 axis(0/1/2) 旋转 degrees 度的单位四元数。"""
    rad = math.radians(degrees)
    if axis == 0:
        e = om.MEulerRotation(rad, 0.0, 0.0)
    elif axis == 1:
        e = om.MEulerRotation(0.0, rad, 0.0)
    else:
        e = om.MEulerRotation(0.0, 0.0, rad)
    return e.asQuaternion()


def _snap90(value):
    """把数值吸附到最近的 90° 整数倍。"""
    return round(value / 90.0) * 90.0


def _default_state():
    """生成魔方初始状态。

    cubies 每个元素为 [px, py, pz, qx, qy, qz, qw]。
    committed 为 6 个控制器上一次"已提交"的角度（90° 整数倍）。
    """
    cubies = []
    for i in range(CUBIE_COUNT):
        x, y, z = home_position(i)
        cubies.append([x, y, z, 0.0, 0.0, 0.0, 1.0])
    return {"cubies": cubies, "committed": [0.0] * 6}


def _commit(state, raws):
    """根据 6 个控制器的原始角度，对魔方状态执行 90° 增量提交。

    只有当某个控制器吸附到 90° 整数倍时，才把 `吸附值 - 已提交值` 的增量
    旋转固化到状态中；否则视为"进行中"，不提交。
    """
    committed = state["committed"]
    for k in range(6):
        raw = raws[k]
        snapped = _snap90(raw)
        if abs(raw - snapped) >= SNAP_EPS:
            continue  # 未吸附，暂不提交

        delta = snapped - committed[k]
        if abs(delta) <= 1e-6:
            continue  # 与上次提交值一致，无需处理

        axis, coord = FACES[k]
        q_move = _axis_quat(axis, delta)

        for c in state["cubies"]:
            px, py, pz = c[0], c[1], c[2]
            if (px, py, pz)[axis] != coord:
                continue  # 不在该面切片内

            # 旋转位置（90° 整数倍，结果仍是整数，四舍五入取整）
            v = om.MVector(px, py, pz).rotateBy(q_move)
            c[0] = int(round(v.x))
            c[1] = int(round(v.y))
            c[2] = int(round(v.z))

            # 旋转方向：q_new = q_old * q_move（先旧方向，再面旋转）
            q_old = om.MQuaternion(c[3], c[4], c[5], c[6])
            q_new = q_old * q_move
            q_new.normalizeIt()
            c[3] = q_new.x
            c[4] = q_new.y
            c[5] = q_new.z
            c[6] = q_new.w

        committed[k] = snapped


def _active_axis(raws):
    """返回当前"进行中"的轴索引（0=X / 1=Y / 2=Z）。

    若所有控制器都吸附到 90° 整数倍，则返回 None。
    存在多个轴同时进行时，只取第一个（保证"同时只能动一个轴"）。
    """
    for k in range(6):
        if abs(raws[k] - _snap90(raws[k])) >= SNAP_EPS:
            return FACES[k][0]
    return None


def _compute_display(state, raws, spacing):
    """根据"已提交状态 + 进行中的旋转"计算 27 个小方块的平移与欧拉旋转。

    返回两个列表：translates、rotates，长度均为 27。
    """
    committed = state["committed"]
    active_axis = _active_axis(raws)

    # 收集进行中的控制器：索引 -> 相对已提交值的增量角度。
    # 只收集当前活动轴（同一轴两个控制器），保证"同时只能动一个轴"。
    in_progress = []
    for k in range(6):
        if active_axis is not None and FACES[k][0] != active_axis:
            continue
        raw = raws[k]
        snapped = _snap90(raw)
        if abs(raw - snapped) >= SNAP_EPS:
            in_progress.append((k, raw - committed[k]))

    translates = []
    rotates = []
    for c in state["cubies"]:
        px, py, pz = c[0], c[1], c[2]
        q = om.MQuaternion(c[3], c[4], c[5], c[6])
        pos = om.MVector(px, py, pz)

        for k, angle in in_progress:
            axis, coord = FACES[k]
            # 用已提交的位置判断切片归属（同轴两面切片互斥，不会重复命中）
            if (px, py, pz)[axis] == coord:
                q_move = _axis_quat(axis, angle)
                pos = pos.rotateBy(q_move)
                q = q * q_move

        q.normalizeIt()
        euler = q.asEulerRotation()

        translates.append((pos.x * spacing, pos.y * spacing, pos.z * spacing))
        rotates.append((math.degrees(euler.x),
                        math.degrees(euler.y),
                        math.degrees(euler.z)))

    return translates, rotates


def _compute_visibility(raws):
    """计算 6 个控制器的可见性。

    若存在"进行中"（未吸附）的控制器，则只显示该轴的两个控制器；
    否则全部显示。
    """
    active_axis = _active_axis(raws)
    return [active_axis is None or FACES[k][0] == active_axis for k in range(6)]


# ---------------------------------------------------------------------------
# 节点类
# ---------------------------------------------------------------------------
class RubikCubeNode(ompx.MPxNode):
    kNodeName = "rubikCubeNode"
    kNodeId = om.MTypeId(0x00130001)

    # 输入属性
    spacing = om.MObject()
    cubeState = om.MObject()
    rotXN = om.MObject()
    rotXP = om.MObject()
    rotYN = om.MObject()
    rotYP = om.MObject()
    rotZN = om.MObject()
    rotZP = om.MObject()

    # 输出属性
    outTranslate = om.MObject()
    outTranslateX = om.MObject()
    outTranslateY = om.MObject()
    outTranslateZ = om.MObject()
    outRotate = om.MObject()
    outRotateX = om.MObject()
    outRotateY = om.MObject()
    outRotateZ = om.MObject()
    outVisible = om.MObject()

    def __init__(self):
        super(RubikCubeNode, self).__init__()

    # ------------------------------------------------------------------
    def compute(self, plug, dataBlock):
        attr = plug.attribute()
        if (attr != self.outTranslate and attr != self.outRotate
                and attr != self.outVisible):
            return om.kUnknownParameter

        # 1. 读取 6 个控制器角度
        raws = []
        for name in INPUT_NAMES:
            raws.append(dataBlock.inputValue(getattr(self, name)).asFloat())

        spacing = dataBlock.inputValue(self.spacing).asFloat()
        if spacing <= 0.0001:
            spacing = 1.0

        # 2. 读取状态（JSON 字符串）
        state_str = dataBlock.inputValue(self.cubeState).asString()
        try:
            state = json.loads(state_str)
        except Exception:
            state = _default_state()

        # 3. 执行提交
        _commit(state, raws)

        # 4. 计算显示结果与可见性
        translates, rotates = _compute_display(state, raws, spacing)
        vis = _compute_visibility(raws)

        # 5. 写回状态
        dataBlock.inputValue(self.cubeState).setString(json.dumps(state))

        # 6. 写出输出
        _write_compound_array(dataBlock, self.outTranslate,
                              self.outTranslateX, self.outTranslateY, self.outTranslateZ,
                              translates)
        _write_compound_array(dataBlock, self.outRotate,
                              self.outRotateX, self.outRotateY, self.outRotateZ,
                              rotates)
        _write_bool_array(dataBlock, self.outVisible, vis)

        dataBlock.setClean(plug)
        return

    # ------------------------------------------------------------------
    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
        tAttr = om.MFnTypedAttribute()

        # --- 输入：6 个面的旋转角度 ---
        for name, short in zip(INPUT_NAMES, INPUT_SHORTS):
            attr = nAttr.create(name, short, om.MFnNumericData.kFloat, 0.0)
            nAttr.setKeyable(True)
            nAttr.setWritable(True)
            nAttr.setStorable(True)
            setattr(cls, name, attr)
            cls.addAttribute(attr)

        # --- 输入：小方块间距 ---
        cls.spacing = nAttr.create("spacing", "spc", om.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setMin(0.0001)
        cls.addAttribute(cls.spacing)

        # --- 隐藏状态：魔方状态 JSON 字符串 ---
        cls.cubeState = tAttr.create("cubeState", "cst", om.MFnData.kString)
        default_str = om.MFnStringData().create(json.dumps(_default_state()))
        tAttr.setDefault(default_str)
        tAttr.setHidden(True)
        tAttr.setStorable(True)
        tAttr.setWritable(True)
        tAttr.setKeyable(False)
        tAttr.setConnectable(False)
        cls.addAttribute(cls.cubeState)

        # --- 输出：平移（复合 3 float 数组，27 元素） ---
        cls.outTranslateX = nAttr.create("outTranslateX", "otx", om.MFnNumericData.kFloat, 0.0)
        cls.outTranslateY = nAttr.create("outTranslateY", "oty", om.MFnNumericData.kFloat, 0.0)
        cls.outTranslateZ = nAttr.create("outTranslateZ", "otz", om.MFnNumericData.kFloat, 0.0)
        cls.outTranslate = nAttr.create("outTranslate", "ot",
                                        cls.outTranslateX, cls.outTranslateY, cls.outTranslateZ)
        nAttr.setArray(True)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setKeyable(False)
        cls.addAttribute(cls.outTranslate)

        # --- 输出：旋转（复合 3 float 数组，27 元素） ---
        cls.outRotateX = nAttr.create("outRotateX", "orx", om.MFnNumericData.kFloat, 0.0)
        cls.outRotateY = nAttr.create("outRotateY", "ory", om.MFnNumericData.kFloat, 0.0)
        cls.outRotateZ = nAttr.create("outRotateZ", "orz", om.MFnNumericData.kFloat, 0.0)
        cls.outRotate = nAttr.create("outRotate", "orr",
                                     cls.outRotateX, cls.outRotateY, cls.outRotateZ)
        nAttr.setArray(True)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setKeyable(False)
        cls.addAttribute(cls.outRotate)

        # --- 输出：可见性（bool 数组，6 元素） ---
        cls.outVisible = nAttr.create("outVisible", "ovs", om.MFnNumericData.kBoolean, True)
        nAttr.setArray(True)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setKeyable(False)
        cls.addAttribute(cls.outVisible)

        # --- 依赖关系 ---
        for name in INPUT_NAMES:
            cls.attributeAffects(getattr(cls, name), cls.outTranslate)
            cls.attributeAffects(getattr(cls, name), cls.outRotate)
            cls.attributeAffects(getattr(cls, name), cls.outVisible)
        cls.attributeAffects(cls.spacing, cls.outTranslate)
        cls.attributeAffects(cls.spacing, cls.outRotate)

    # ------------------------------------------------------------------
    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(RubikCubeNode())


# ---------------------------------------------------------------------------
# 输出写入辅助
# ---------------------------------------------------------------------------
def _write_compound_array(dataBlock, array_attr, child_x, child_y, child_z, values):
    arr = dataBlock.outputArrayValue(array_attr)
    builder = arr.builder()
    for i, (x, y, z) in enumerate(values):
        h = builder.addElement(i)
        h.child(child_x).setFloat(x)
        h.child(child_y).setFloat(y)
        h.child(child_z).setFloat(z)
    arr.set(builder)
    arr.setAllClean()


def _write_bool_array(dataBlock, array_attr, values):
    arr = dataBlock.outputArrayValue(array_attr)
    builder = arr.builder()
    for i, v in enumerate(values):
        builder.addElement(i).setBool(v)
    arr.set(builder)
    arr.setAllClean()


# ---------------------------------------------------------------------------
# 构建脚本
# ---------------------------------------------------------------------------
def _create_controller(axis, coord, spacing, scale, labels):
    """在对应面外侧创建一个圆形控制器（NURBS 圆环）。"""
    radius = spacing * 1.5 * scale
    off = spacing * 1.8

    if axis == 0:
        name = labels[0] if coord < 0 else labels[1]
        ctrl = cmds.circle(nr=(1, 0, 0), r=radius, name=name)[0]
        pos = (coord * off, 0.0, 0.0)
    elif axis == 1:
        name = labels[2] if coord < 0 else labels[3]
        ctrl = cmds.circle(nr=(0, 1, 0), r=radius, name=name)[0]
        pos = (0.0, coord * off, 0.0)
    else:
        name = labels[4] if coord < 0 else labels[5]
        ctrl = cmds.circle(nr=(0, 0, 1), r=radius, name=name)[0]
        pos = (0.0, 0.0, coord * off)

    cmds.xform(ctrl, t=pos, ws=True)
    cmds.setAttr(ctrl + ".rotate", 0, 0, 0)
    return ctrl


def buildRubikCube(spacing=1.0, cubie_scale=0.95, controller_scale=1.0):
    """构建一个固定 3×3×3 的魔方绑定。

    参数
    ----
    spacing         : 相邻小方块中心间距
    cubie_scale     : 单个小方块相对间距的缩放（默认 0.95，留出间隙）
    controller_scale: 控制器尺寸缩放

    返回
    ----
    (主组, 节点, 控制器列表, 小方块列表)
    """
    labels = ["rubikCtrl_XN", "rubikCtrl_XP",
              "rubikCtrl_YN", "rubikCtrl_YP",
              "rubikCtrl_ZN", "rubikCtrl_ZP"]

    cmds.undoInfo(openChunk=True)
    try:
        grp = cmds.group(empty=True, name="rubikCube_grp")

        # 1. 创建 27 个小方块（索引顺序必须与 home_position 一致）
        cubies = []
        for i in range(CUBIE_COUNT):
            x, y, z = home_position(i)
            cube = cmds.polyCube(w=cubie_scale, h=cubie_scale, d=cubie_scale,
                                 name="rubikCubie_%d" % i)[0]
            cmds.parent(cube, grp)
            cmds.setAttr(cube + ".translate", x * spacing, y * spacing, z * spacing)
            cubies.append(cube)

        # 2. 创建节点
        node = cmds.createNode("rubikCubeNode", name="rubikCubeNode1")
        cmds.setAttr(node + ".spacing", spacing)

        # 3. 连接小方块输出
        for i, cube in enumerate(cubies):
            cmds.connectAttr("%s.outTranslate[%d]" % (node, i), "%s.translate" % cube, f=True)
            cmds.connectAttr("%s.outRotate[%d]" % (node, i), "%s.rotate" % cube, f=True)

        # 4. 创建 6 个控制器并连接
        controllers = []
        for k, (axis, coord) in enumerate(FACES):
            ctrl = _create_controller(axis, coord, spacing, controller_scale, labels)
            cmds.parent(ctrl, grp)
            controllers.append(ctrl)

            # 连接旋转输入（对应轴通道）
            channel = {0: "rotateX", 1: "rotateY", 2: "rotateZ"}[axis]
            cmds.connectAttr("%s.%s" % (ctrl, channel), "%s.%s" % (node, INPUT_NAMES[k]), f=True)

            # 连接可见性输出
            cmds.connectAttr("%s.outVisible[%d]" % (node, k), "%s.visibility" % ctrl, f=True)

        cmds.select(clear=True)
        print("魔方绑定构建完成：组=%s 节点=%s" % (grp, node))
        return grp, node, controllers, cubies
    finally:
        cmds.undoInfo(closeChunk=True)


# ---------------------------------------------------------------------------
# 构建命令（让用户可以直接 cmds.rubikCube() 构建）
# ---------------------------------------------------------------------------
class RubikCubeCommand(ompx.MPxCommand):
    kCommandName = "rubikCube"

    def __init__(self):
        ompx.MPxCommand.__init__(self)

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag("-sp", "-spacing", om.MSyntax.kDouble)
        syntax.addFlag("-cs", "-cubieScale", om.MSyntax.kDouble)
        syntax.addFlag("-cts", "-controllerScale", om.MSyntax.kDouble)
        return syntax

    def doIt(self, args):
        spacing = 1.0
        cubie_scale = 0.95
        controller_scale = 1.0
        try:
            db = om.MArgDatabase(self.syntax(), args)
            if db.isFlagSet("-spacing"):
                spacing = db.flagArgumentDouble("-spacing", 0)
            if db.isFlagSet("-cubieScale"):
                cubie_scale = db.flagArgumentDouble("-cubieScale", 0)
            if db.isFlagSet("-controllerScale"):
                controller_scale = db.flagArgumentDouble("-controllerScale", 0)
        except Exception:
            pass
        grp, node, controllers, cubies = buildRubikCube(spacing, cubie_scale, controller_scale)
        self.setResult(grp)

    @classmethod
    def cmdCreator(cls):
        return ompx.asMPxPtr(RubikCubeCommand())


# ---------------------------------------------------------------------------
# 插件注册
# ---------------------------------------------------------------------------
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            RubikCubeNode.kNodeName,
            RubikCubeNode.kNodeId,
            RubikCubeNode.nodeCreator,
            RubikCubeNode.nodeInitializer,
        )
        print("成功注册节点: %s" % RubikCubeNode.kNodeName)
    except Exception as e:
        sys.stderr.write("注册节点失败: %s, 错误: %s\n" % (RubikCubeNode.kNodeName, str(e)))

    try:
        plugin.registerCommand(
            RubikCubeCommand.kCommandName,
            RubikCubeCommand.cmdCreator,
            RubikCubeCommand.syntaxCreator,
        )
        print("成功注册命令: %s" % RubikCubeCommand.kCommandName)
    except Exception as e:
        sys.stderr.write("注册命令失败: %s, 错误: %s\n" % (RubikCubeCommand.kCommandName, str(e)))


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(RubikCubeNode.kNodeId)
    plugin.deregisterCommand(RubikCubeCommand.kCommandName)
