# Maya_PY3_plug-in

一套用于 Autodesk Maya（Python 3）的绑定 / 蒙皮 / 表情生产插件集合，包含一个主插件窗口和一批按功能拆分的工具模块，另有若干自定义节点（C++ `.mll` 与 Python 节点）。

主要面向角色绑定流程：权重处理、蒙皮包裹、控制器处理、Blendshape 编辑、表情制作、绳子 / 拉链 / 面片链等辅助建模与绑定工具，以及魔方这类程序化绑定节点。

## 环境要求

- Autodesk Maya，**Python 3** 版本（建议 2022 及以上）
- 仅使用 Maya 自带模块：`maya.cmds`、`maya.api.OpenMaya`、`PySide2`
- 无第三方依赖；部分节点为已编译的 `.mll`，随版本文件夹一起提供
- 源码多数字文件使用 **GBK** 编码（文件头标注 `#coding=gbk`），用编辑器打开时请注意编码

## 安装

1. **改版本文件夹名**
   把根目录下的版本文件夹改成你正在使用的 Maya 版本号（`2023` → 例如 `2024`）。
   插件在加载时会从当前 Maya 版本号向下查找第一个存在的版本文件夹，所以文件夹名不低于你的 Maya 版本即可正常加载。

2. **执行安装脚本**
   把 `ui/Install.py` 直接拖拽到 Maya 视窗中运行，弹出安装窗口。

3. **填写用户文件夹**
   - `用户文件夹路径`：默认是插件根目录下的 `user`，一般不用改。
   - `文件夹名称`：默认 `self`（管理员目录），个人用户直接点「安装」即可。
   - 如果装在服务器上给多人共用，除管理员外每个人都要把这里改成自己的 **纯英文** 文件夹名，避免互相覆盖配置。

4. **同意强制加载**
   安装后如果弹出强制加载提示窗口，点「同意」。

5. 安装脚本会自动写入 Maya 的 `modules` 目录（`ZKM_plug_in_mod.mod` / `ZKM_plug_in_library_mod.mod`）并把 `ZKM_plug_in.py` 复制到用户文件夹，之后重启 Maya，或在**插件管理器**中确认 `ZKM_plug_in` 已勾选自动加载。

## 使用

插件加载后会在 Maya 主菜单注册入口，通过菜单打开各工具窗口；也可以直接运行某个工具模块下的 `open_window.py`。

核心模块一览（`2023/`，随版本改名）：

| 模块 | 说明 |
| --- | --- |
| `curve.py` | 曲线相关公共方法 |
| `controller.py` | 控制器创建与处理 |
| `weight.py` | 权重处理公共方法 |
| `blendshape.py` | Blendshape 公共方法 |
| `model.py` / `ui_edit.py` | 模型与 UI 编辑辅助 |
| `general_settings.py` / `others_library.py` | 全局设置与通用库 |
| `script.py` / `outside.py` | 脚本入口与外部调用 |
| `maya_common.py` / `common.py` | 通用工具函数 |

## 目录结构

```
Maya_PY3_plug-in/
├─ 2023/                    版本文件夹（按 Maya 版本命名，可改名）
│  ├─ node/                 自定义节点：.mll 与 Python 节点
│  ├─ custom_commands/      自定义命令
│  ├─ curve_library/        曲线库（曲线 .txt + 预览 .jpg）
│  └─ *.py                  曲线 / 控制器 / 权重 / BS 等公共模块
├─ ui/
│  ├─ Install.py            安装入口（拖进 Maya 视窗运行）
│  ├─ ZKM_plug_in_UI/       插件主入口（菜单注册、命令分发）
│  └─ qt_ui/                各功能工具窗口
└─ user/                    按用户隔离的配置与数据（self 为管理员目录）
```

## 内置工具（ui/qt_ui）

| 模块 | 功能 |
| --- | --- |
| `weight_processing` | 权重处理 |
| `surface_skin_clueter_wrap` | 曲面蒙皮包裹 |
| `bs_edit` | BS 编辑 |
| `add_Intermediate` | bs 改驱动 |
| `bs_convert_drver` | 改驱动加 bs |
| `face` | 表情制作 |
| `controller_processing` | 控制器处理 |
| `edit_deform_layer` | 变形器层级编辑 |
| `custom_commands` | 自定义命令 |
| `clear_files` | 文件清理 + 小功能 |
| `disk_drive` | 驱动器 |
| `curved_rope` / `new_rope` | 绳子 |
| `zipper` | 拉链生成 |
| `patch_chain` | 面片链 |
| `create_hole` | 创建洞 |
| `wing_rig` | 鸟翅膀绑定 |
| `skirt_drver` | 裙子驱动 |
| `scroll` | 通用附着版卷轴 |
| `track` | 履带 |
| `tire_baking_expression` | 轮胎烘焙表达式 |
| `volume` | 体积 |
| `universal_link` | 通用链接器 |
| `connect_train` | 链接火车（适配 SteamTrainBlock_rig / CarriageBlock_rig） |
| `RedirectCurve` | 重定向工具（动画数据导入） |
| `help` | 帮助 |

各工具窗口都带自己的 `open_window.py`，可以单独运行调试。

## 自定义节点（2023/node）

- `.mll` 编译节点：`BsChangeNormal.mll`、`skin.mll`、`maya2024.mll`、`maya2024A.mll`
- Python 节点脚本：`rubikCube.py`（魔方绑定）、`selfIK.py`、`new_wire*.py`、`new_wrap*.py`、`uv_deform*.py`、`write_weight*.py`、`canBakingWeight*.py`、`get_from_array*.py` 等

其中**魔方绑定节点**已单独整理文档，见 [2023/node/README.md](2023/node/README.md)：支持自定义长宽高（如 4×4×4）、每层独立控制器与总控控制器。

## 说明与注意事项

- 本插件早期在 Maya 2019（Python 2）上测试，Python 3 版本以 2024 为基础开发，其他版本请复制版本文件夹改名后使用。
- 版本文件夹内的 `node`、`ui` 路径会在安装时写入 Maya 的 module 文件，**移动插件目录后需要重新运行一次安装**。
- `user/` 目录下是各使用者自己的配置、曲线库与临时数据，`self` 为管理员目录；插件运行时会往用户目录写入数据。
- 工具窗口带脚本回调（如权重处理、变形器层级编辑），日常写别的代码时建议先关闭窗口，避免影响效率与撤销。
- `.gitignore` 已排除 `_*.py` / `_*.log` 调试脚本、`__pycache__`、`*.pyc`、`.idea`、`Thumbs.db` 以及运行时的 `scratch_file` 暂存目录。
