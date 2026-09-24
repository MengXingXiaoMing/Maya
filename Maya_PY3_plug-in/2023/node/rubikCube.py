# -*- coding: utf-8 -*-
"""
魔方绑定节点 (rubikCubeNode) —— 可调尺寸版
============================================

功能
----
可调长宽高（dimX × dimY × dimZ）的魔方绑定节点，配合 `buildRubikCube()` 构建脚本使用：

- 每一层（沿每个轴的每一个切片）都有一个控制器，绕该轴旋转该层。例如 3×3×3
  有 3+3+3=9 个层控制器（不只是 6 个面），4×4×4 有 12 个。
- 总控控制器 `rubikMaster` 控制整个魔方（所有小方块 + 所有层控制器一起移动/旋转）。
- 当某个轴的控制器数值不是 90° 的整数倍时，其它轴的控制器自动隐藏，
  此时只能操作当前轴的各层控制器。
- 只有所有控制器都回到 90° 的整数倍时，其它轴的控制器才重新显示。
- 节点内部记录"已提交"旋转状态：只有控制器到达 90° 整数倍时，才会把这次转动
  固化（提交）到魔方状态中；未到达整数倍时仅做临时预览旋转。
- 小方块按经典魔方配色自动上色：+X 红、-X 橙、+Y 白、-Y 黄、+Z 绿、-Z 蓝，
  只有暴露在外表面的面才着色，内部面保持默认材质。
- 同一场景可重复构建多个魔方，后建的自动加 `_2`、`_3` ... 后缀，互不重名。

设计说明
--------
- 每个小方块记录：网格坐标 (px, py, pz) + 方向四元数 (qx, qy, qz, qw)。
  坐标为"居中坐标"：奇数维是整数（3 维 -> -1/0/1），偶数维是半整数
  （4 维 -> -1.5/-0.5/0.5/1.5），统一吸附到 0.5 的倍数。
- 提交(commit)：控制器角度吸附到 90° 整数倍时，用 `delta = 吸附值 - 已提交值`
  对当前处于该层切片内的方块执行一次旋转，然后更新已提交值。
- 显示(display)：未吸附时，把 `raw - 已提交值` 作为临时增量旋转显示出来。
- 状态以 JSON 字符串形式存在隐藏属性 `cubeState` 中，避免大量散列属性。

关于输入属性的说明（重要）
--------------------------
- 层控制器角度不使用 Maya 的数组输入属性，而是固定数量的标量属性
  `rotX0..rotZ{MAX_DIM-1}`。数组输入属性在并行求值(EM)下读取
  `MArrayDataHandle` 会与输出数组求值产生竞争，导致 Maya 卡死；
  固定标量输入与旧版（已验证不卡死）的结构一致。
- 因此每个轴支持的层数上限由 `MAX_DIM` 决定（当前 64，即最大 64×64×64）。
  属性数量随 `MAX_DIM` 线性增长（每个轴 MAX_DIM 个），注册开销很小；
  实际可构建的尺寸主要受性能限制：方块数按立方增长（8³=512、18³=5832），
  构建时间与每次求值开销都会随之显著上升。

用法
----
    import maya.cmds as cmds
    cmds.loadPlugin('rubikCube.py')
    import rubikCube
    rubikCube.buildRubikCube(4, 4, 4)   # 4×4×4

    # 或使用命令：
    cmds.rubikCube(dimX=4, dimY=4, dimZ=4)
"""

import sys
import math
import json

import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds

# 判断"是否吸附到 90° 整数倍"的容差（单位：度）
SNAP_EPS = 0.01

# 默认尺寸
DEFAULT_DIMS = (3, 3, 3)

# 每个轴最多支持的层数（即最大支持 MAX_DIM × MAX_DIM × MAX_DIM）。
# 由于层控制器角度使用固定标量输入，此值决定了需要预先注册的输入属性数量
# （每个轴 MAX_DIM 个，共 3 × MAX_DIM 个输入属性）。属性数量线性增长、注册
# 开销很小，所以这里给得比较宽松；实际可构建尺寸受性能限制（方块数按立方增长）。
MAX_DIM = 64

# 六个外表面的材质颜色（经典魔方配色）：方向 -> (材质名, RGB)
FACE_COLORS = {
    "posX": ("rubikMat_posX", (0.85, 0.10, 0.10)),  # 红
    "negX": ("rubikMat_negX", (0.95, 0.45, 0.05)),  # 橙
    "posY": ("rubikMat_posY", (0.95, 0.95, 0.95)),  # 白
    "negY": ("rubikMat_negY", (0.95, 0.85, 0.10)),  # 黄
    "posZ": ("rubikMat_posZ", (0.05, 0.55, 0.20)),  # 绿
    "negZ": ("rubikMat_negZ", (0.05, 0.30, 0.75)),  # 蓝
}

# polyCube 面索引与方向的对应关系（实测：f0=+Z f1=+Y f2=-Z f3=-Y f4=+X f5=-X）
FACE_INDEX = {
    "posX": 4, "negX": 5,
    "posY": 1, "negY": 3,
    "posZ": 0, "negZ": 2,
}

# 控制器颜色（视口显示色，走 drawing override）：同一轴上的层控制器同色
CTRL_COLORS = {
    "master": (0.85, 0.85, 0.85),  # 浅灰
    "X": (0.90, 0.25, 0.25),  # 红：绕 X 轴旋转的层
    "Y": (0.25, 0.80, 0.35),  # 绿：绕 Y 轴旋转的层
    "Z": (0.30, 0.50, 0.95),  # 蓝：绕 Z 轴旋转的层
}

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------
def _axis_quat(axis, degrees):
    """返回绕 axis(0=X / 1=Y / 2=Z) 旋转 degrees 度的单位四元数。"""
    rad = math.radians(degrees)
    if axis == 0:
        e = om.MEulerRotation(rad, 0.0, 0.0)
    elif axis == 1:
        e = om.MEulerRotation(0.0, rad, 0.0)
    else:
        e = om.MEulerRotation(0.0, 0.0, rad)
    return e.asQuaternion()


def _snap90(value):
    """把角度吸附到最近的 90° 整数倍。"""
    return round(value / 90.0) * 90.0


def _snap_coord(value):
    """把网格坐标吸附到最近的 0.5（奇数维为整数、偶数维为半整数）。"""
    return round(value * 2.0) / 2.0


def _cubie_count(dims):
    return dims[0] * dims[1] * dims[2]


def _slice_count(dims):
    return dims[0] + dims[1] + dims[2]


def _home_indices(dims, index):
    """由小方块序号反推其网格索引 (ix, iy, iz)，顺序与构建脚本一致。"""
    dx, dy, dz = dims
    iz = index // (dx * dy)
    rem = index % (dx * dy)
    iy = rem // dx
    ix = rem % dx
    return ix, iy, iz


def _home_position(dims, index):
    """返回第 index 个小方块的初始居中坐标 (x, y, z)。"""
    dx, dy, dz = dims
    ix, iy, iz = _home_indices(dims, index)
    return (ix - (dx - 1) / 2.0,
            iy - (dy - 1) / 2.0,
            iz - (dz - 1) / 2.0)


def _axis_of(k, dims):
    """第 k 个层控制器所属的轴（0=X / 1=Y / 2=Z）。"""
    dx, dy, dz = dims
    if k < dx:
        return 0
    if k < dx + dy:
        return 1
    return 2


def _axis_local_index(k, dims):
    """第 k 个层控制器在所属轴上的局部序号 (axis, local_index)。"""
    dx, dy, dz = dims
    if k < dx:
        return 0, k
    k -= dx
    if k < dy:
        return 1, k
    k -= dy
    return 2, k


def _slice_coord(k, dims):
    """第 k 个层控制器对应的 (轴索引, 切片坐标)。"""
    dx, dy, dz = dims
    if k < dx:
        return 0, (k - (dx - 1) / 2.0)
    k -= dx
    if k < dy:
        return 1, (k - (dy - 1) / 2.0)
    k -= dy
    return 2, (k - (dz - 1) / 2.0)


def _controller_name(axis, k, dims, tag=""):
    """生成层控制器名字，例如 rubikCtrl_X0 / rubikCtrl_Y1 / rubikCtrl_Z2。"""
    dx, dy, dz = dims
    if axis == 0:
        idx = k
    elif axis == 1:
        idx = k - dx
    else:
        idx = k - dx - dy
    return "rubikCtrl_%s%d%s" % ("XYZ"[axis], idx, tag)


def _next_cube_tag():
    """返回本次构建可用的名字后缀，保证同场景多魔方互不重名。

    第一个魔方使用原始名字（rubikMaster / rubikCubie_0 ...），之后依次
    追加 _2、_3 ...，避免 Maya 在重名时把名字末尾数字自动递增
    （例如 rubikCtrl_X0 被改成 rubikCtrl_X1），从而错连到别的轴上。
    """
    i = 1
    while True:
        tag = "" if i == 1 else "_%d" % i
        if not (cmds.objExists("rubikMaster" + tag)
                or cmds.objExists("rubikCubie_0" + tag)):
            return tag
        i += 1


def _default_state(dims):
    """生成初始魔方状态。

    cubies 每个元素为 [px, py, pz, qx, qy, qz, qw]；
    committed 为每个层控制器上一次"已提交"的角度（长度 = 层数）。
    """
    cubies = []
    for i in range(_cubie_count(dims)):
        x, y, z = _home_position(dims, i)
        cubies.append([x, y, z, 0.0, 0.0, 0.0, 1.0])
    return {"cubies": cubies, "committed": [0.0] * _slice_count(dims)}


# ---------------------------------------------------------------------------
# 旋转 / 显示 / 可见性逻辑
# ---------------------------------------------------------------------------
def _commit(state, dims, raws):
    """根据各层控制器的原始角度，对魔方状态执行 90° 增量提交。

    只有某个控制器吸附到 90° 整数倍时，才把 `吸附值 - 已提交值` 的增量旋转
    固化到状态中；否则视为"进行中"，不提交。
    """
    committed = state["committed"]
    for k in range(len(raws)):
        raw = raws[k]
        snapped = _snap90(raw)
        if abs(raw - snapped) >= SNAP_EPS:
            continue  # 未吸附，暂不提交

        delta = snapped - committed[k]
        if abs(delta) <= 1e-6:
            continue  # 与上次提交值一致，无需处理

        axis, coord = _slice_coord(k, dims)
        q_move = _axis_quat(axis, delta)

        for c in state["cubies"]:
            px, py, pz = c[0], c[1], c[2]
            if (px, py, pz)[axis] != coord:
                continue  # 不在该层切片内

            v = om.MVector(px, py, pz).rotateBy(q_move)
            c[0] = _snap_coord(v.x)
            c[1] = _snap_coord(v.y)
            c[2] = _snap_coord(v.z)

            q_old = om.MQuaternion(c[3], c[4], c[5], c[6])
            q_new = q_old * q_move
            q_new.normalizeIt()
            c[3] = q_new.x
            c[4] = q_new.y
            c[5] = q_new.z
            c[6] = q_new.w

        committed[k] = snapped


def _active_axis(dims, raws):
    """返回当前"进行中"的轴索引（0=X / 1=Y / 2=Z）。

    若所有控制器都吸附到 90° 整数倍，返回 None。
    多个轴同时进行时只取第一个（保证"同时只能动一个轴"）。
    """
    for k in range(len(raws)):
        if abs(raws[k] - _snap90(raws[k])) >= SNAP_EPS:
            return _axis_of(k, dims)
    return None


def _compute_display(state, dims, raws, spacing):
    """根据"已提交状态 + 进行中的旋转"计算所有小方块的平移与欧拉旋转。"""
    committed = state["committed"]
    active_axis = _active_axis(dims, raws)

    # 收集进行中的控制器：只收集当前活动轴（同一轴各层），保证"只能动一个轴"。
    in_progress = []
    for k in range(len(raws)):
        if active_axis is not None and _axis_of(k, dims) != active_axis:
            continue
        raw = raws[k]
        if abs(raw - _snap90(raw)) >= SNAP_EPS:
            in_progress.append((k, raw - committed[k]))

    translates = []
    rotates = []
    for c in state["cubies"]:
        px, py, pz = c[0], c[1], c[2]
        q = om.MQuaternion(c[3], c[4], c[5], c[6])
        pos = om.MVector(px, py, pz)

        for k, angle in in_progress:
            axis, coord = _slice_coord(k, dims)
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


def _compute_visibility(dims, raws):
    """计算各层控制器的可见性。

    存在"进行中"（未吸附）的控制器时，只显示该轴的所有层控制器；否则全部显示。
    """
    active_axis = _active_axis(dims, raws)
    return [active_axis is None or _axis_of(k, dims) == active_axis
            for k in range(len(raws))]


# ---------------------------------------------------------------------------
# 节点类
# ---------------------------------------------------------------------------
class RubikCubeNode(ompx.MPxNode):
    kNodeName = "rubikCubeNode"
    kNodeId = om.MTypeId(0x00141488)

    # 输入属性
    dimX = om.MObject()
    dimY = om.MObject()
    dimZ = om.MObject()
    spacing = om.MObject()
    cubeState = om.MObject()

    # 各层控制器角度：固定标量输入 (axis, local_index) -> MObject。
    # 不使用数组输入，避免并行求值(EM)下 MArrayDataHandle 与输出数组竞争导致卡死。
    rotAttrs = {}

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

        dx = max(1, dataBlock.inputValue(self.dimX).asInt())
        dy = max(1, dataBlock.inputValue(self.dimY).asInt())
        dz = max(1, dataBlock.inputValue(self.dimZ).asInt())
        dims = (dx, dy, dz)
        slice_n = _slice_count(dims)
        cubie_n = _cubie_count(dims)

        spacing = dataBlock.inputValue(self.spacing).asFloat()
        if spacing <= 0.0001:
            spacing = 1.0

        # 1. 读取各层控制器角度（固定标量输入）
        raws = []
        for k in range(slice_n):
            axis, local_idx = _axis_local_index(k, dims)
            raws.append(dataBlock.inputValue(self.rotAttrs[(axis, local_idx)]).asFloat())

        # 2. 读取状态（JSON 字符串，直接写回 cubeState，与旧版一致）
        state_str = dataBlock.inputValue(self.cubeState).asString()
        try:
            state = json.loads(state_str)
        except Exception:
            state = None
        if (state is None
                or len(state.get("cubies", [])) != cubie_n
                or len(state.get("committed", [])) != slice_n):
            state = _default_state(dims)

        # 3. 执行提交
        _commit(state, dims, raws)

        # 4. 计算显示结果与可见性
        translates, rotates = _compute_display(state, dims, raws, spacing)
        vis = _compute_visibility(dims, raws)

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

        # --- 输入：尺寸 ---
        for name, short in (("dimX", "dmx"), ("dimY", "dmy"), ("dimZ", "dmz")):
            a = nAttr.create(name, short, om.MFnNumericData.kInt, 3)
            nAttr.setMin(1)
            nAttr.setKeyable(True)
            nAttr.setWritable(True)
            nAttr.setStorable(True)
            setattr(cls, name, a)
            cls.addAttribute(a)

        # --- 输入：小方块间距 ---
        cls.spacing = nAttr.create("spacing", "spc", om.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setMin(0.0001)
        cls.addAttribute(cls.spacing)

        # --- 输入：各层控制器旋转角度（固定标量，每个轴 MAX_DIM 个） ---
        cls.rotAttrs = {}
        for axis in range(3):
            for idx in range(MAX_DIM):
                long_name = "rot%s%d" % ("XYZ"[axis], idx)
                short_name = "r%s%d" % ("xyz"[axis], idx)
                a = nAttr.create(long_name, short_name, om.MFnNumericData.kFloat, 0.0)
                nAttr.setKeyable(False)
                nAttr.setWritable(True)
                nAttr.setStorable(True)
                cls.rotAttrs[(axis, idx)] = a
                cls.addAttribute(a)

        # --- 隐藏状态：魔方状态 JSON 字符串 ---
        cls.cubeState = tAttr.create("cubeState", "cst", om.MFnData.kString)
        default_str = om.MFnStringData().create(json.dumps(_default_state(DEFAULT_DIMS)))
        tAttr.setDefault(default_str)
        tAttr.setHidden(True)
        tAttr.setStorable(True)
        tAttr.setWritable(True)
        tAttr.setKeyable(False)
        tAttr.setConnectable(False)
        cls.addAttribute(cls.cubeState)

        # --- 输出：平移（复合 3 float 数组） ---
        cls.outTranslateX = nAttr.create("outTranslateX", "otx", om.MFnNumericData.kFloat, 0.0)
        cls.outTranslateY = nAttr.create("outTranslateY", "oty", om.MFnNumericData.kFloat, 0.0)
        cls.outTranslateZ = nAttr.create("outTranslateZ", "otz", om.MFnNumericData.kFloat, 0.0)
        cls.outTranslate = nAttr.create("outTranslate", "ot",
                                        cls.outTranslateX, cls.outTranslateY, cls.outTranslateZ)
        nAttr.setArray(True)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        cls.addAttribute(cls.outTranslate)

        # --- 输出：旋转（复合 3 float 数组） ---
        cls.outRotateX = nAttr.create("outRotateX", "orx", om.MFnNumericData.kFloat, 0.0)
        cls.outRotateY = nAttr.create("outRotateY", "ory", om.MFnNumericData.kFloat, 0.0)
        cls.outRotateZ = nAttr.create("outRotateZ", "orz", om.MFnNumericData.kFloat, 0.0)
        cls.outRotate = nAttr.create("outRotate", "orr",
                                     cls.outRotateX, cls.outRotateY, cls.outRotateZ)
        nAttr.setArray(True)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        cls.addAttribute(cls.outRotate)

        # --- 输出：可见性（bool 数组，长度 = 层数） ---
        cls.outVisible = nAttr.create("outVisible", "ovs", om.MFnNumericData.kBoolean, True)
        nAttr.setArray(True)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        cls.addAttribute(cls.outVisible)

        # --- 依赖关系 ---
        for name in ("dimX", "dimY", "dimZ"):
            cls.attributeAffects(getattr(cls, name), cls.outTranslate)
            cls.attributeAffects(getattr(cls, name), cls.outRotate)
            cls.attributeAffects(getattr(cls, name), cls.outVisible)
        for axis in range(3):
            for idx in range(MAX_DIM):
                a = cls.rotAttrs[(axis, idx)]
                cls.attributeAffects(a, cls.outTranslate)
                cls.attributeAffects(a, cls.outRotate)
                cls.attributeAffects(a, cls.outVisible)
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
        h = builder.addElement(i)
        h.setBool(v)
    arr.set(builder)
    arr.setAllClean()


# ---------------------------------------------------------------------------
# 构建脚本
# ---------------------------------------------------------------------------
def _outer_faces(ix, iy, iz, dims):
    """返回位于魔方表面的小方块需要上色的方向列表。

    只有当方块处于某个轴的最外层时，该方向的面才露在外面需要着色。
    """
    dx, dy, dz = dims
    keys = []
    if ix == 0:
        keys.append("negX")
    if ix == dx - 1:
        keys.append("posX")
    if iy == 0:
        keys.append("negY")
    if iy == dy - 1:
        keys.append("posY")
    if iz == 0:
        keys.append("negZ")
    if iz == dz - 1:
        keys.append("posZ")
    return keys


def _get_shading_group(name, rgb):
    """创建（或复用）指定名称与颜色的材质，返回其 shading group 名。

    材质在所有魔方之间共享，因此只创建一次。
    """
    if not cmds.objExists(name):
        mat = cmds.shadingNode("lambert", asShader=True, name=name)
        cmds.setAttr(mat + ".color", rgb[0], rgb[1], rgb[2], type="double3")
    sg = name + "SG"
    if not cmds.objExists(sg):
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg)
        cmds.connectAttr(name + ".outColor", sg + ".surfaceShader", f=True)
    return sg


def _set_controller_color(ctrl, rgb):
    """用 drawing override 给控制器（NURBS 曲线）上色。

    曲线不参与材质着色，显示颜色只能由 override 控制；这里用 RGB 覆盖
    以获得精确颜色，而不是调色板索引。
    """
    cmds.setAttr(ctrl + ".overrideEnabled", 1)
    cmds.setAttr(ctrl + ".overrideRGBColors", 1)
    cmds.setAttr(ctrl + ".overrideColorRGB", rgb[0], rgb[1], rgb[2], type="double3")


def _square_curve(size, axis, name):
    """创建一个闭合的正方形曲线控制器，法线方向为 axis 对应的轴。"""
    h = size / 2.0
    if axis == 0:      # 法线 X：正方形位于 YZ 平面
        corners = [(0.0, -h, -h), (0.0, h, -h), (0.0, h, h), (0.0, -h, h)]
    elif axis == 1:    # 法线 Y：正方形位于 XZ 平面
        corners = [(-h, 0.0, -h), (h, 0.0, -h), (h, 0.0, h), (-h, 0.0, h)]
    else:              # 法线 Z：正方形位于 XY 平面
        corners = [(-h, -h, 0.0), (h, -h, 0.0), (h, h, 0.0), (-h, h, 0.0)]
    return cmds.curve(degree=1, point=corners + [corners[0]], name=name)


def _create_master_controller(dims, spacing, tag=""):
    """创建总控控制器：一个位于原点的水平正方形，控制整个魔方。"""
    size = max(dims) * spacing * 1.7
    master = _square_curve(size, 1, "rubikMaster" + tag)
    cmds.setAttr(master + ".translate", 0, 0, 0)
    cmds.setAttr(master + ".rotate", 0, 0, 0)
    _set_controller_color(master, CTRL_COLORS["master"])
    return master


def _create_slice_controller(axis, coord, dims, spacing, scale, name):
    """在指定层的切片位置创建一个正方形层控制器。"""
    if axis == 0:
        cross = max(dims[1], dims[2])
        pos = (coord * spacing, 0.0, 0.0)
    elif axis == 1:
        cross = max(dims[0], dims[2])
        pos = (0.0, coord * spacing, 0.0)
    else:
        cross = max(dims[0], dims[1])
        pos = (0.0, 0.0, coord * spacing)

    ctrl = _square_curve(cross * spacing * 1.4 * scale, axis, name)
    cmds.xform(ctrl, t=pos, ws=True)
    cmds.setAttr(ctrl + ".rotate", 0, 0, 0)
    return ctrl


def _setup_slice_controller(ctrl, axis):
    """按轴给层控制器上色，并只保留该轴的旋转通道。

    必须在大纲层级(parent)确定之后调用：锁定 translate 会阻止后续
    的父子补偿操作。
    """
    _set_controller_color(ctrl, CTRL_COLORS["XYZ"[axis]])

    keep = "rotate%s" % "XYZ"[axis]
    for attr in ("translateX", "translateY", "translateZ",
                 "rotateX", "rotateY", "rotateZ",
                 "scaleX", "scaleY", "scaleZ"):
        if attr == keep:
            continue
        cmds.setAttr("%s.%s" % (ctrl, attr), lock=True, keyable=False, channelBox=False)
    # visibility 由节点输出驱动（自动隐藏其它轴的控制器），只隐藏不锁定
    cmds.setAttr(ctrl + ".visibility", keyable=False, channelBox=False)
    # 唯一保留的旋转通道：可打关键帧（keyable 属性会自动显示在通道盒）
    # 注意 keyable 与 channelBox 互斥，不能同时设置
    cmds.setAttr("%s.%s" % (ctrl, keep), lock=False, keyable=True)
    return ctrl


def buildRubikCube(dimX=3, dimY=3, dimZ=3, spacing=1.0,
                   cubie_scale=1.0, controller_scale=1.0):
    """构建一个可调长宽高的魔方绑定。

    参数
    ----
    dimX/dimY/dimZ  : 三个方向的方块数量（默认 3×3×3，可传 4×4×4 等；
                      每个轴最大为 MAX_DIM）
    spacing         : 相邻小方块中心间距
    cubie_scale     : 单个小方块相对间距的缩放（默认 1.0，与间距等大即紧贴）
    controller_scale: 层控制器尺寸缩放

    返回
    ----
    (总控控制器, 节点, 层控制器列表, 小方块列表)

    说明
    ----
    同一场景可重复构建多个魔方：若已存在魔方，则本次所有对象自动追加
    后缀 _2、_3 ...（例如 rubikMaster_2 / rubikCubie_0_2 / rubikCtrl_X0_2），
    各魔方的节点与控制器相互独立，互不影响。
    """
    dims = (max(1, int(dimX)), max(1, int(dimY)), max(1, int(dimZ)))
    dx, dy, dz = dims
    if max(dims) > MAX_DIM:
        raise ValueError("尺寸 %dx%dx%d 超过单轴最大层数 MAX_DIM=%d，"
                         "请在 rubikCube.py 中增大 MAX_DIM。" % (dx, dy, dz, MAX_DIM))

    cubie_n = dx * dy * dz
    slice_n = dx + dy + dz

    cmds.undoInfo(openChunk=True)
    try:
        # 名字后缀：同场景已存在魔方时自动加 _2、_3 ...，避免任何重名
        tag = _next_cube_tag()

        # 总控控制器（作为整个魔方的父级）
        master = _create_master_controller(dims, spacing, tag)
        cubies_grp = cmds.group(empty=True, name="rubikCube_cubies" + tag, parent=master)
        ctrls_grp = cmds.group(empty=True, name="rubikCube_ctrls" + tag, parent=master)

        # 1. 创建小方块（索引顺序必须与 _home_position 一致），
        #    同时收集各外露面，稍后按方向统一上色
        cubies = []
        face_groups = dict((key, []) for key in FACE_COLORS)
        for i in range(cubie_n):
            x, y, z = _home_position(dims, i)
            ix, iy, iz = _home_indices(dims, i)
            cube = cmds.polyCube(w=cubie_scale, h=cubie_scale, d=cubie_scale,
                                 name="rubikCubie_%d%s" % (i, tag))[0]
            cmds.parent(cube, cubies_grp)
            cmds.setAttr(cube + ".translate", x * spacing, y * spacing, z * spacing)
            for key in _outer_faces(ix, iy, iz, dims):
                face_groups[key].append("%s.f[%d]" % (cube, FACE_INDEX[key]))
            cubies.append(cube)

        # 1.1 按方向统一上色（每个方向只需一次 assign，避免逐面操作）
        for key, faces in face_groups.items():
            if faces:
                cmds.sets(faces, e=True, forceElement=_get_shading_group(*FACE_COLORS[key]))

        # 2. 创建节点并设置尺寸
        node = cmds.createNode("rubikCubeNode", name="rubikCubeNode1" + tag)
        cmds.setAttr(node + ".dimX", dx)
        cmds.setAttr(node + ".dimY", dy)
        cmds.setAttr(node + ".dimZ", dz)
        cmds.setAttr(node + ".spacing", spacing)

        # 3. 连接小方块输出
        for i, cube in enumerate(cubies):
            cmds.connectAttr("%s.outTranslate[%d]" % (node, i), "%s.translate" % cube, f=True)
            cmds.connectAttr("%s.outRotate[%d]" % (node, i), "%s.rotate" % cube, f=True)

        # 4. 创建每个层的控制器并连接
        controllers = []
        for k in range(slice_n):
            axis, coord = _slice_coord(k, dims)
            name = _controller_name(axis, k, dims, tag)
            ctrl = _create_slice_controller(axis, coord, dims, spacing,
                                            controller_scale, name)
            cmds.parent(ctrl, ctrls_grp)
            controllers.append(ctrl)

            channel = {0: "rotateX", 1: "rotateY", 2: "rotateZ"}[axis]
            _, local_idx = _axis_local_index(k, dims)
            input_name = "rot%s%d" % ("XYZ"[axis], local_idx)
            cmds.connectAttr("%s.%s" % (ctrl, channel), "%s.%s" % (node, input_name), f=True)
            cmds.connectAttr("%s.outVisible[%d]" % (node, k), "%s.visibility" % ctrl, f=True)

            # 全部连接完成后再上色并收敛通道（放在最后，避免锁定影响前面的连接）
            _setup_slice_controller(ctrl, axis)

        cmds.select(clear=True)
        print("魔方绑定构建完成：master=%s 节点=%s 尺寸=%dx%dx%d 层控制器=%d"
              % (master, node, dx, dy, dz, slice_n))
        return master, node, controllers, cubies
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
        syntax.addFlag("-dx", "-dimX", om.MSyntax.kLong)
        syntax.addFlag("-dy", "-dimY", om.MSyntax.kLong)
        syntax.addFlag("-dz", "-dimZ", om.MSyntax.kLong)
        syntax.addFlag("-sp", "-spacing", om.MSyntax.kDouble)
        syntax.addFlag("-cs", "-cubieScale", om.MSyntax.kDouble)
        syntax.addFlag("-cts", "-controllerScale", om.MSyntax.kDouble)
        return syntax

    def doIt(self, args):
        dx, dy, dz = 3, 3, 3
        spacing = 1.0
        cubie_scale = 1.0
        controller_scale = 1.0
        try:
            db = om.MArgDatabase(self.syntax(), args)
            if db.isFlagSet("-dimX"):
                dx = db.flagArgumentInt("-dimX", 0)
            if db.isFlagSet("-dimY"):
                dy = db.flagArgumentInt("-dimY", 0)
            if db.isFlagSet("-dimZ"):
                dz = db.flagArgumentInt("-dimZ", 0)
            if db.isFlagSet("-spacing"):
                spacing = db.flagArgumentDouble("-spacing", 0)
            if db.isFlagSet("-cubieScale"):
                cubie_scale = db.flagArgumentDouble("-cubieScale", 0)
            if db.isFlagSet("-controllerScale"):
                controller_scale = db.flagArgumentDouble("-controllerScale", 0)
        except Exception:
            pass
        master, node, controllers, cubies = buildRubikCube(
            dx, dy, dz, spacing, cubie_scale, controller_scale)
        self.setResult(master)

    @classmethod
    def cmdCreator(cls):
        return ompx.asMPxPtr(RubikCubeCommand())


# ---------------------------------------------------------------------------
# 插件注册
# ---------------------------------------------------------------------------
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.1.0")
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
