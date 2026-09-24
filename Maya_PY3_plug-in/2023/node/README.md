# rubikCube — Maya 魔方绑定节点

一个用于 Autodesk Maya 的魔方绑定插件：程序化生成可自定义尺寸的魔方，每一层都有独立控制器，可以像真实魔方一样逐层转动。

![Maya](https://img.shields.io/badge/Maya-2025-blue) ![Python](https://img.shields.io/badge/Python-3-yellow) ![License](https://img.shields.io/badge/License-MIT-green)

## 特性

- **任意尺寸**：3×3×3、4×4×4 …… 直到 64×64×64（`MAX_DIM` 可调），长宽高也可不同（如 3×4×5）。
- **逐层控制器**：每个轴上的每一层都有独立控制器，共 `Nx + Ny + Nz` 个，绕轴旋转该层。3×3×3 有 9 个，4×4×4 有 12 个，18×18×18 有 54 个。
- **总控控制器**：`rubikMaster` 控制整个魔方（所有小方块与层控制器一起移动 / 旋转 / 缩放）。
- **智能隐藏**：当某一轴上的控制器角度不是 90° 整数倍时，其它轴的控制器自动隐藏，避免多层同时可操作导致状态错乱；所有控制器回到 90° 整数倍后，其它轴控制器重新显示。
- **90° 吸附提交**：只有控制器转到 90° 的整数倍时才把这次转动固化（提交）进魔方状态；不到整数倍只做临时预览旋转，松开即可看到真实状态。
- **自动配色**：小方块按经典魔方配色上色，六个外表面分别为 +X 红、-X 橙、+Y 白、-Y 黄、+Z 绿、-Z 蓝；只有真正露在外表面的面才着色，内部面保持默认材质。
- **同场景多魔方**：可以反复构建，后建的魔方自动追加 `_2`、`_3` … 后缀，命名互不冲突、节点互相独立。
- **干净的控制器**：控制器为正方形曲线，同一轴的控制器同色（X 红 / Y 绿 / Z 蓝 / 总控浅灰），且只保留该轴必需的旋转通道，其余通道锁定并隐藏。

## 环境要求

- Autodesk Maya（开发与测试环境：**Maya 2025 / Python 3**）
- 无第三方依赖，仅使用 Maya 自带模块：`maya.OpenMaya`、`maya.OpenMayaMPx`、`maya.cmds`
- 使用 OpenMaya API 1.0，未在其它 Maya 版本上逐一测试

## 安装

1. 把 `rubikCube.py` 放到 Maya 的插件搜索路径下（`MAYA_PLUG_IN_PATH`），或者放在任意目录，加载时写完整路径。
   - Windows 默认插件目录示例：`C:/Users/<用户名>/Documents/maya/2025/plug-ins/`
2. 在 Maya 的 **Script Editor → Python** 标签中加载：

```python
import maya.cmds as cmds
cmds.loadPlugin("rubikCube.py")
```

如果插件不在搜索路径里：

```python
cmds.loadPlugin(r"D:/maya_plugins/rubikCube.py")
```

## 快速开始

```python
import maya.cmds as cmds

cmds.loadPlugin("rubikCube.py")

# 默认构建 3×3×3
cmds.rubikCube()

# 构建 4×4×4
cmds.rubikCube(dimX=4, dimY=4, dimZ=4)

# 长宽高可以不同（3×4×5），并自定义间距与方块尺寸
cmds.rubikCube(dimX=3, dimY=4, dimZ=5, spacing=1.2,
               cubieScale=0.95, controllerScale=1.0)
```

命令返回总控控制器的名字，方便后续引用：

```python
master = cmds.rubikCube(dimX=4, dimY=4, dimZ=4)
```

也可以直接调用模块里的构建函数，拿到所有部件：

```python
import rubikCube

master, node, controllers, cubies = rubikCube.buildRubikCube(4, 4, 4)
```

### 操作魔方

```python
# 绕 X 轴转动第 0 层 90°
cmds.setAttr("rubikCtrl_X0.rotateX", 90)

# 绕 Y 轴转动最外层 -90°
cmds.setAttr("rubikCtrl_Y2.rotateY", -90)

# 整体移动 / 旋转魔方
cmds.setAttr("rubikMaster.translate", 0, 10, 0)
cmds.setAttr("rubikMaster.rotateY", 45)
```

在视口里直接框选控制器、拖动旋转手柄也能操作（层控制器的旋转通道是唯一未锁定的通道）。

### 清除魔方

```python
cmds.delete(cmds.ls("rubikMaster*", long=True))
```

## 构建参数

**命令 `cmds.rubikCube(...)`**

| 短标志 | 长标志 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `-dx` | `-dimX` | int | 3 | X 方向的方块数量 |
| `-dy` | `-dimY` | int | 3 | Y 方向的方块数量 |
| `-dz` | `-dimZ` | int | 3 | Z 方向的方块数量 |
| `-sp` | `-spacing` | float | 1.0 | 相邻小方块的中心间距 |
| `-cs` | `-cubieScale` | float | 1.0 | 小方块相对间距的缩放（1.0 即紧贴） |
| `-cts` | `-controllerScale` | float | 1.0 | 层控制器尺寸的缩放 |

**函数 `buildRubikCube(dimX, dimY, dimZ, spacing, cubie_scale, controller_scale)`**

返回 `(总控控制器, 节点, 层控制器列表, 小方块列表)`。

## 生成的对象

以默认 3×3×3 为例：

| 对象 | 命名 | 说明 |
| --- | --- | --- |
| 总控控制器 | `rubikMaster` | 正方形曲线，整体变换 |
| 小方块 | `rubikCubie_0` … `rubikCubie_26` | 按索引顺序生成，索引顺序与内部状态一一对应 |
| 层控制器 | `rubikCtrl_X0` … `rubikCtrl_Z2` | X / Y / Z 各 3 个 |
| 容器组 | `rubikCube_cubies`、`rubikCube_ctrls` | 位于总控之下 |
| 插件节点 | `rubikCubeNode1` | 计算并驱动小方块的位置与旋转 |

第二个魔方的所有对象会带 `_2` 后缀（`rubikMaster_2`、`rubikCubie_0_2`、`rubikCtrl_X0_2` …），以此类推。

## 实现说明

### 为什么用固定标量输入而不是数组属性

插件的层控制器角度使用固定数量的**标量输入属性** `rotX0…rotZ63`（每个轴 `MAX_DIM` 个），而不是数组输入属性。

原因是：Maya 在并行求值（Evaluation Manager）下读取数组输入 `MArrayDataHandle` 会与输出数组求值产生竞争，实测会导致 Maya 卡死。固定标量输入不存在这个问题，代价是支持的层数上限由 `MAX_DIM` 预先决定（属性必须在插件注册时一次性创建，Maya 不支持运行时动态添加属性）。

`MAX_DIM` 默认 64，属性数量随它线性增长（共 `3 × MAX_DIM` 个），注册开销很小，按需调整即可。

### 状态与提交

- 每个小方块记录网格坐标 `(px, py, pz)` 与方向四元数 `(qx, qy, qz, qw)`，坐标统一吸附到 0.5 的倍数（奇数尺寸为整数、偶数尺寸为半整数）。
- 控制器角度吸附到 90° 整数倍时，用 `delta = 吸附值 - 已提交值` 对该层内的方块执行一次旋转，然后更新已提交值——这就是一次"提交"。
- 未吸附到 90° 时，只把 `raw - 已提交值` 作为临时增量旋转显示出来，不会污染魔方状态。
- 全部状态以 JSON 字符串形式存放在隐藏属性 `cubeState` 中，避免为每个方块创建大量属性。

### 输出

插件节点对外提供三个数组输出，由构建脚本连接到方块与控制器：

| 属性 | 类型 | 连接目标 |
| --- | --- | --- |
| `outTranslate` | 复合 float3 数组 | 各小方块的 `translate` |
| `outRotate` | 复合 float3 数组 | 各小方块的 `rotate` |
| `outVisible` | bool 数组 | 各层控制器的 `visibility` |

## 常见问题

**构建 / 卸载插件时报 `cannot be unloaded because it is still in use`**

场景里还有节点，或者 undo 队列里还留着引用该插件的命令。先删对象并清空 undo 队列：

```python
cmds.delete(cmds.ls("rubikMaster*", long=True))
cmds.flushUndo()
for m in list(sys.modules):
    if m == "rubikCube" or m.startswith("rubikCube."):
        del sys.modules[m]
cmds.unloadPlugin("rubikCube.py")
```

**报 `尺寸 NxNxN 超过单轴最大层数 MAX_DIM=...`**

需要更大的尺寸时，把 `rubikCube.py` 顶部的 `MAX_DIM` 改成更大的值（例如 100），重新加载插件即可，输入属性会随之自动注册。

**构建很大尺寸时很慢**

方块数量按立方增长，构建时间也随之增长（实测 8×8×8 约 2.9 秒、18×18×18 约 94 秒）。耗时主要在创建小方块与连线，属于 Maya DG 操作的固有成本。构建完成后转动仍然流畅（18×18×18 单次旋转求值约 0.1 秒）。

**控制器为什么不使用材质上色**

NURBS 曲线的显示颜色不参与材质着色，只能用 drawing override 控制，因此控制器颜色通过 `overrideEnabled + overrideRGBColors + overrideColorRGB` 设置；小方块则使用普通的 lambert 材质。

## 已知限制

- 单轴层数上限为 `MAX_DIM`（默认 64）。
- 大尺寸（如 18×18×18 以上）构建耗时明显，且场景中对象数量庞大。
- `cubeState` 以单个 JSON 字符串存放全部状态，超大尺寸下字符串会变得很大（18³ 约 350 KB）。

## 许可证

本项目基于 MIT 许可证开源，详见 `LICENSE`。

## 作者

KangmingZhan
