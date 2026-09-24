# -*- coding: utf-8 -*-
"""鸟翅膀绑定插件（羽毛优先）

工作流：
    1. 「每节手臂」按顺序加载根骨骼与对应的手臂骨骼，拼出翅膀手臂骨链；
    2. 「羽毛」按顺序加载每根羽毛的羽毛根骨骼与它对应的手臂骨骼
       （可用「自动匹配手臂骨骼」按距离自动配对）；
    3. 点「生成翅膀绑定」：
       - 手臂每节插一个 `<骨骼>_fk` 偏移组 + 一个可见的 `<骨骼>_fkCtrl` 圆环：
         层级 = 父骨骼 -> <骨骼>_fk -> 骨骼，且**圆环的 rotate 连到偏移组的 rotate**
         （转圆环 = 摆这一节），所以动画师在视口里点那个圆环就能摆肩/肘/腕。
         收起仍写在骨骼自己的 rotate 上（羽毛的驱动源就是它，单层驱动关键帧才可靠），
         两边通道不重叠、互不抢——之前收起直接驱动骨骼，转到一半就被弹回、手臂摆不动。
       - 羽毛根骨骼若没挂在对应手臂骨骼下，会自动重新父子（保持世界位置），
         之后它就是相对该骨骼权重 1 的刚性跟随；
       - 每根羽毛生成一套控制器（全部挂在「对应手臂骨骼」下，所以手臂随便怎么摆，
         它们都整体刚性跟随，羽毛与手臂的夹角严格守恒＝始终垂直于手臂）：
             <羽毛>_ctrlGrp  偏移组——收起偏转与层叠的驱动关键帧写在它的 rotate/translate 上
             <羽毛>_ctrl     朝向控制器（圆环）——手动转它，整根羽毛跟着转向
             <羽毛>_tip      末端控制器（小方块）——拖动它改变羽尖，末端由曲线控制
             另外还有一条严格穿过各关节的驱动样条（1 次曲线，静止姿态零形变）；
       - 羽毛骨骼用「定位器 + 点约束 + 方向约束」贴合样条（不用 IK）：
         第 k 个定位器取样条第 k 个控制点，位置锁到骨骼上、朝向指向下一个定位器；
       - 收起偏转用驱动关键帧写在羽毛偏移组的 rotate 上，驱动源是
         「对应手臂关节的 rotate」，一根手臂关节只管挂在它上面的那几根羽毛；
       - 手臂表整列折叠角填的是同一个数时（＝表格默认填充），生成前会自己挑一次
         「该折哪几行」（和「一键生成」同一条路）；逐行填过不同的角就照你填的折。
       - 手臂按 Z 形对折 / 扇形卷曲逐节折叠，由「收起」控制器的 fold 属性一根根
         写入各手臂关节；「根部后掠角」让整只收好的翅膀再往收拢方向转一个角度
         （＝转肩）。这一下默认**自动**：Z 形对折只把手臂折回来、并不转肩，
         收到底以后翼包还朝翼尖那一侧伸着（真翼形实测外伸 0.221 × 翼展），
         而真实鸟翼是贴身体前后方向收着的。自动值把羽毛收好后的朝向转到
         「弦向的后方」（见 Window.auto_root_sweep），实测外伸降到 0.000~0.062。
       - 「折叠控制器」会挂到手臂根骨骼下，角色移动/旋转时跟着走。
    4. 拖「收起程度」滑块或点「收起 / 展开」实时预览；
       「扇形微张 / 层叠厚度 / 整体朝向偏转」可以批量调整收起后的朝向与层次，
       点「全选羽毛控制器」再旋转，可以手动批量微调各根羽毛的朝向。

羽毛收拢的核心公式：
    羽毛要收到目标方向，需要绕世界轴 N 转 δ。偏移组挂在手臂骨骼下，
    手臂一折起来它的世界朝向就跟着转了，所以这根世界轴必须按
    「写关键帧那一刻父级的真实世界旋转 P」换算：
        R(偏移组) = P · A(t_world, tilt) · A(N, δ) · P⁻¹
    其中 tilt 只用来抹掉这根羽毛自己静止时的离面角（让收起后所有羽毛严格共面）。
    层叠（谁压在谁上面）**不是旋转**，而是沿翼面法线平移：
        Δ_local = (N · 层叠厚度 · (1−rank)) · P⁻¹
    偏移组和羽毛根骨骼写**同一个**位移，整根羽毛刚性平移。
    为什么不能用旋转做层叠：两根转过不同角度的羽毛平面不再平行，深度差沿长度线性
    变化、必然经过 0，而它们的投影交叉点在收起过程中又在移动 —— 扫到过零点时两根
    就正好共面切进去（卡片会互相割）。平移则所有羽毛严格平行、深度差恒定，永不共面。
    静止时 δ = tilt = Δ = 0，R = I，也就是严格回到建模姿态。
    早期版本用「静止姿态」换算（等于把 P 当成静止朝向），羽毛会偏出目标方向
    二十几度，而且每根偏的量都不一样，收起后不是「一叠」而是「一团刺球」。

    手臂关节折叠用另一条更精确的公式（Maya 的 MMatrix 为行向量约定，
    实测关节世界旋转 W(k) = R(k)·jointOrient(k)·W(parent)）：
        R'(J) = W(J) · A(N, Δ) · W(J)⁻¹ · R(J)，Δ = ψ(J) - ψ(父关节)
    它与 jointOrient、父级变换、初始 rotate 全部无关，任意绑定姿态下都精确成立。
"""
import os
import sys
import json
import inspect
import importlib
import math

import maya.cmds as cmds

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号（向下寻找已存在的版本目录，例如 2023）
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for _i in range(30):
    _test_version = maya_version_int - _i
    _library_path = root_path + '\\' + str(_test_version)
    if os.path.isdir(_library_path):
        sys.path.append(_library_path)
        maya_version = str(_test_version)
        maya_version_int = _test_version
        break

import general_settings
from general_settings import *
importlib.reload(general_settings)

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import maya_common
importlib.reload(maya_common)
from maya_common import *

from maya.api import OpenMaya as om

# 控制器命名
CTRL_NAME = 'Wing_Fold_Ctrl'
FOLD_ATTR = 'fold'
# 每根羽毛的控制器命名后缀：
#   _ctrlGrp  偏移组（收起偏转的驱动关键帧写在它上面）
#   _ctrl     朝向控制器（圆环，动画师手动转）
#   _tip      末端控制器（小方块，拖动它改变羽尖，末端由曲线控制）
CTRL_GRP_SUFFIX = '_ctrlGrp'
CTRL_SUFFIX = '_ctrl'
TIP_SUFFIX = '_tip'
# 手臂每节插入的「FK 偏移组」后缀。
# 层级：父骨骼 -> <骨骼>_fk -> 骨骼。收起带来的旋转仍然写在骨骼自己的 rotate 上
# （羽毛的驱动源就是它，单层驱动关键帧才可靠），动画师要摆姿势就转 <骨骼>_fk，
# 这样既不会跟驱动曲线抢通道，也不会形成「驱动套驱动」的求值链。
FK_OFF_SUFFIX = '_fk'
# 每节手臂 FK 控制器（可见的圆环）的后缀
FK_CTRL_SUFFIX = '_fkCtrl'
# 控制器上存「这套绑定都建了哪些节点」的字符串属性。
# 插件原本只把这份登记表放在 Python 内存里，可是绑定是跟着文件走的：
# 存盘、第二天重新打开，插件就不认识自己建过的绑定了——
# 下拉里是空的、删不掉、再点「生成」会在旧绑定上叠第二套，
# 而且旧约束还在，会直接报错（setAttr: No object matches name: ..._ctrlGrp.rotate）。
# 所以把它序列化成 JSON 存在控制器上，跟文件一起走。
RIG_DATA_ATTR = 'rigData'
# 控制器的线框颜色（Maya 索引色）。一套 44 根羽毛的翅膀会有 44 个羽毛圆环 +
# 44 个末端方块 + 4 个手臂 FK 环 + 1 个收起控制器，全用默认灰色的话，
# 视口里长得一模一样，动画师分不清哪个是哪个、也不知道该抓哪个。
# 按通行约定上色：总控黄、手臂 FK 红、羽毛朝向绿、羽毛末端青。
CTRL_COLOR_FOLD = 17        # 黄：收起总控（最常用的那一个）
CTRL_COLOR_FK = 13          # 红：手臂每节的 FK 姿势环
CTRL_COLOR_FEATHER = 14     # 绿：羽毛朝向控制器
CTRL_COLOR_TIP = 18         # 青：羽毛末端控制器
# 手臂折叠模式
MODE_Z = 'Z 形对折(交替)'
MODE_CURL = '扇形卷曲(同向)'
# 各模式下的默认每节折叠角（度）。Z 形对折要接近 180° 才能把前臂真正贴回上臂、
# 让挂在两段上的羽毛收到同一条线上，收起来才整齐。
#
# 为什么是「Z 形、且在翼面内对折」——这是鸟类解剖决定的，不是随便挑的：
#   · 鸟的腕关节只能往尺骨那一侧弯（手部常态偏向尺骨），弯折方向就在翼面内；
#     肘、腕两个关节联动着把翅膀收起来（文献里就把它简化成四连杆机构）。
#   · 所以「绕翼面法线做 Z 形对折」正是真实机制；绕其它轴转都会把羽毛拧出翼面。
#   参考: Sullivan et al. 2010, Proc R Soc B 277:2027（腕关节不对称与折翅）;
#         Tang et al. 2024, PLoS ONE 19(4): e0299982（隼翼折叠的四连杆建模）。
MODE_DEFAULT_ANGLE = {MODE_Z: 170.0, MODE_CURL: 45.0}
DEFAULT_FOLD_ANGLE = MODE_DEFAULT_ANGLE[MODE_Z]
# 羽毛贴拢方向：默认顺着折叠后的手臂把羽毛收回来（翅膀才会收成一包）
DIR_AUTO = '自动(沿手臂收回)'
DIR_FLIP = '反向(往外伸)'
# 收起后羽毛之间的默认夹角（扇形微张，从翼根到翼尖递增），0 表示全部严格平行。
# 4° 是量过之后留的（原来这条一条依据都没写，界面上还写着「10~20° 更接近真实鸟翼」，
# 那句是没验过的）。三个场景扫 0/4/8/12/16/24°（sweep_fan.py → out/sweep_fan.txt）：
#   · 实际散差 ≈ 9~10°（那是**旧的旋转式层叠**带来的）＋ 0.5×这个值 —— 填 12° 只多散 5°。
#     层叠改成沿法线平移之后，这两个角不再叠加：填多少就散多少，所以 4° 现在
#     呈现的扇形比当时更收敛（这方向是安全的 —— 0° 本来在这三个量上都最好）；
#   · 调大主要是代价：中心线相交对数 0→48 / 0→8 / 0→53，
#     手臂到最近羽毛的平均距离（越小盖得越好）0.35→0.61 / 0.11→0.20 / 0.30→0.48；
#   · 收益几乎为零：收起后尺寸 21.1%→19.3%（真翼形）、分层间隔与厚度不变。
# 0° 也没有原来担心的「完全重叠」问题（实测分层间隔是羽毛长的 0.79%~1.21%，
# 和 4° 一样），反而在这三个量上都最好。留在 4° 是因为它保留了一点点扇形层次，
# 而代价可以忽略。
DEFAULT_FAN = 4.0
# 收起后整叠羽毛的默认厚度，占**中位羽毛长**的百分比（层叠厚度）。
# 按羽毛长度分配层号：短覆羽在最外面一层、长飞羽最贴翼面，同一翼展位置上重叠的
# 两排就被分到不同深度。取负值可以把里外两层对调，0 = 所有羽毛收进同一个平面。
# （试过改成「每层间距 ×(根数−1)」，想让根数少的模型自然更薄 —— 实测更差：
#   层间距是**相邻两层**的差，而判「几乎共面」的门槛是羽毛长的 0.5%，两者太近。
#   build_wing_long（20 根）在 0.5%/层 冒出 2 对真切进去（5 对 / 静止基线 3 对），
#   换回整叠 17%（＝0.85%/层）就是 3 对，通过。保留「整叠厚度」这组默认。）
# **已知代价**：根数特别多（>80）时相邻两层被压到 0.5% 门槛以下，那种模型把
# 这个值往上调（38 根时 17% ≈ 每层 0.46%；20 根时 ≈ 0.85%）。
#
# 这里是「沿翼面法线平移」，不是「把羽毛翘出翼面」。换掉旋转式分层的原因：
# 绕面内轴转过**不同**角度之后两根羽毛的平面不再平行，深度差沿长度线性变化、
# 必然经过 0；而它们的投影交叉点在收起过程中是移动的，扫到那个过零点时两根就
# 正好共面切进去（自检第 9 项那一项）。平移没有这个问题：所有羽毛严格平行、
# 深度差沿整条羽毛恒定，只要两根深度不同就永远不会相交。
#
# 厚度扫参（四个夹具 × 整叠 0/4/8/12/17/24%，看自检「羽毛穿插合理」那一项，
# 记「真切进去 / 几乎完全共面 / 交叉处深度间隔中位」）：
#   0%    形状 23/23/0.0000  解剖 48/33/0.0043  真翼 18/18/0.0000  鸟形 20/20/0.0000  全 FAIL
#   4%    形状 11/0/0.0047   解剖 35/0/0.0109   真翼 11/0/0.0053   鸟形 12/0/0.0048   三个 FAIL
#   8%    形状  8/0/0.0094   解剖 17/0/0.0175   真翼 10/0/0.0106   鸟形  5/0/0.0096   形状 FAIL
#   12%   形状  7/0/0.0141   解剖  9/0/0.0241   真翼  6/0/0.0158   鸟形  5/0/0.0144   全过（余量薄）
#   17%   形状  5/0/0.0199   解剖  9/0/0.0323   真翼  6/0/0.0224   鸟形  0/0/0.0241   全过
#   24%   形状  5/0/0.0281   解剖  1/0/0.0438   真翼  0/0/0.0317   鸟形  0/0/0.0340   全过
# 门槛在整叠 12% 附近（0% 时全部羽毛落在一个平面里 → 全 FAIL；4~8% 相邻两层只差
# 0.4~1.0% 羽毛长，还是被判「深度几乎相同」）。取 17% 是留余量：12% 时形状那套
# 只剩 3 对余量（7 对 / 静止基线 10 对）。
# 代价如实记下：整叠越厚，羽毛整体离手臂越远（「手臂到最近羽毛的平均距离」相对
# 展开姿态，真翼那套 38 根：整叠 0%→0.77、8%→0.89、17%→1.05、30%→1.27），
# 所以别往大调。
DEFAULT_STACK = 17.0
# 收起后所有羽毛一起绕翼面法线多转的角度（批量调整朝向）
DEFAULT_YAW = 0.0
# 羽毛收拢进度指数：羽毛转过的世界角度 = 总收拢角 × (t ** FEATHER_EASE)。
# =1 跟手臂同步收；<1 羽毛先收拢、手臂后折；>1 手臂先折、羽毛后收。
#
# 取 0.45。这个常数来回改过好几次（0.45 → 1.00 → 又回 0.45），前几次都是被
# 单个指标带跑的，所以把这次的完整证据写在这里，别再凭一个数拍脑袋：
#
# 为什么 1.00 不行 —— **渲图直接看**（同一机位、同一个场景，图在 shots/ease_ab2/）：
#   1.00：收起 40% 时羽毛还是一把「耙子」（一根根分开立着），手臂整段光杆露在
#         外面；60% 时羽毛和手臂仍然分成两块 —— 这就是用户说的「效果很差」。
#   0.45：40% 时羽毛已经互相搭上、把手臂盖住，是一整坨收起来的翅膀；
#         60% 时同样。
#
# 再上四个相机无关的量（八个场景扫 0.35/0.45/0.60/0.80/1.00，见
# sweep_ease2.py，结果在 out/sweep_ease2.txt）：
#   bulge  收起途中所有关节点在翼面内的凸包面积，相对展开姿态的最大值
#          1.00 三个场景 111.8% / 116.9% / 110.6% —— **收起途中翅膀先胀大 10%~17%**；
#          0.45 是 100.0% / 105.8% / 100.0%（基本不胀）
#   expose 手臂骨链采样点到最近羽毛中心线的平均距离，越小 = 手臂被羽毛盖得越好
#          0.45 → 0.59 / 0.80 / 0.62；0.60 → 0.64 / 0.84 / 0.67；
#          1.00 → 0.73 / 0.89 / 0.75（三个场景单调，0.45 最好）
#   dead   收起 10% 时半径还剩多少。1.00 → 96.9% / 99.1%（滑块前 10% 几乎没反应），
#          0.45 → 79.5% / 78.2%（一开始就在收）
# 三个量都指向「越小越好」，而且都是单调的。
#
# 后来层叠从「翘出翼面」改成「沿翼面法线平移」（见 DEFAULT_STACK），上面那组数
# 是旧模型的，所以在**新模型**下重量了一遍（五个场景 × 0.45/0.70/1.00，
# 层叠厚度固定 17%，sweep_shift.py）—— 结论没变，仍是 0.45：
#   dead   0.45 → 79.5 / 88.7 / 78.2 / 77.4 / 99.3（五个场景全是最小）
#          1.00 → 96.9 / 94.8 / 99.1 / 96.4 / 99.3（滑块前 10% 几乎没反应）
#   bulge  0.45 → 105.8 / 100.0 / 100.0 / 100.0 / 100.0（其余两档最多涨到 116.9）
#   expose 0.45 → 1.05 / 0.77 / 0.77 / 1.17 / 0.69（四个场景最小，一个与 0.70 持平）
#   （expose 的绝对值比旧模型大，是因为平移把整叠羽毛挪离了翼面 —— 那是层叠的
#    代价，不是这个常数造成的；同一厚度下 0.45 仍是最好的那一档。）
#
# 「羽毛中心线相交对数」这个指标**不能用来定这个常数**：它在 0.45/0.60/1.00 之间
# 是乱的（同一个场景 61 / 20 / 21），而且和渲出来的图相反 —— 在 build_wing_shape
# 0.45 的 70% 档上它报 61 对穿过（三个里最差），可那一档渲出来是一整片光滑的羽毛
# 盖在手臂上；1.00 那档报 21 对，渲出来却是零零碎碎的羽毛插在裸露的手臂旁边。
# 原因：羽毛本来就会像瓦片一样互相压着，中心线投影相交 ≠ 看得见穿模。
# 所以这项只保留在自检里做「有没有真的穿过去」的粗筛，不参与挑默认值。
#
# 代价（如实记下来，别以后又当成「没验过」）：0.45 会让**收起末段**的半径
# 回升一点 —— 半径先收到最小、之后又涨回去（占展开半径的百分点）：
#   build_wing_shape：0.45 → 5.0 个点（51% 收到最低、末尾回到 56%）；
#                     1.00 → 1.2 个点。build_wing_long 同量级（3.5）。
#   其余六个场景 0.45 和 1.00 一样（多为 ≤1 个点）。
# build_wing_real 的 10.4 个点回升**跟这个常数无关**：0.45 到 1.00 六档全是
# 100 97 93 86 79 69 59 48 36 41 46 同一条曲线 —— 那是那套手臂自己折到底的
# 几何（最远点从头换到尾），不是羽毛甩出来的。
# 拿 3.8 个点的末段回升换「40%~60% 档位上手臂被羽毛盖住、不再是一把耙子」，
# 从渲图看是划算的。
#
# 界面上仍然暴露成「羽毛收拢进度」：羽毛又短又密、展开姿态就糊在一起的模型，
# 可以往 1.00 调（那时羽毛晚收一点更贴，末段回升也小）。
FEATHER_EASE = 0.45
# 收起 0~100% 之间的解算采样点数（写进驱动关键帧）。
# 采样太稀，中间帧靠欧拉插值补，收起过程会出现「先弹出去一下」的回弹。
# 实测：6 点时中途半径回升 0.42（约 23%，肉眼可见），12 点时降到 0.15 且大回弹消失。
DEFAULT_SAMPLES = 12


# ============================================================ 骨骼与数学工具
def short_name(name):
    """取骨骼短名（去掉命名空间与路径）"""
    if not name:
        return ''
    return name.split('|')[-1].split(':')[-1]


def as_joint(name):
    """校验并返回骨骼长名；不是骨骼则返回 None"""
    if not name:
        return None
    found = cmds.ls(name, long=True) or []
    if not found:
        # **命名空间**：带命名空间的对象（参考进来的模型、导入时带 ns 的模型）
        # 用短名是查不到的 —— cmds.ls('humerus') 不会匹配 'refWing:humerus'，
        # cmds.objExists 也一样返回 False。实测（Maya 2025）：参考进来的翅膀，
        # 手臂表里照抄界面显示的短名去点生成，会一路 resolve 成 None，最后报
        # 「第 1 节手臂的根骨骼与手臂骨骼不在同一条层级链上」——用户看到的就是
        # 「这个插件功能不对」。这里用通配符把命名空间补回来再查一次。
        leaf = name.split('|')[-1].split(':')[-1]
        if leaf:
            found = sorted(cmds.ls('*:' + leaf, long=True) or [])
    for f in found:
        if cmds.nodeType(f) == 'joint':
            return f
    return None


def resolve_joint(name):
    """把表格里填的骨骼名解析成当前的长名

    骨骼被重新父子后层级会变、旧长名会失效，这里回退到用短名重新查找。
    """
    joint = as_joint(name)
    if joint is None and name:
        joint = as_joint(short_name(name))
    return joint


def get_parent(node):
    """取父节点长名"""
    rel = cmds.listRelatives(node, p=True, f=True) or []
    return rel[0] if rel else None


def selected_chain(sel):
    """把选中的骨骼整理成「从根到梢」的一条链，不理会用户的选择顺序

    返回 (按层级排好的骨骼列表, 说明文字)。第二位为空串表示成功。

    以前是直接按「选择顺序」两两成节，于是用户在大纲里框选、或从翼尖往回点，
    表里就会写进「前臂 → 上臂」这种反着的节，一路要到点「生成」时才报
    「不在同一条层级链上」—— 用户看到的就是「这个插件功能不对」。
    这里改成认层级：谁的「被选中祖先」最少谁在最前，依次往下。
    分叉（有两根骨骼的祖先个数相同）时说明白是哪几根，而不是硬排一个顺序。
    """
    picked = set(sel)
    depth = {}
    for j in sel:
        n = 0
        node = get_parent(j)
        while node:
            if node in picked:
                n += 1
            node = get_parent(node)
        depth[j] = n
    order = sorted(sel, key=lambda j: depth[j])
    got = sorted(depth.values())
    if got != list(range(len(sel))):
        # 祖先个数不是 0,1,2… 就是「几段互不相连的骨架」或者「有分叉」
        heads = [j for j in sel if depth[j] == 0]
        if len(heads) != 1:
            return [], ('选中的骨骼不是一条链：有 %d 个起点（%s）。'
                        '请只选同一节手臂的骨骼'
                        % (len(heads), '、'.join(short_name(h) for h in heads[:4])))
        by_depth = {}
        for j in sel:
            by_depth.setdefault(depth[j], []).append(short_name(j))
        br = [v for v in by_depth.values() if len(v) > 1]
        return [], ('选中的骨骼在主链上有分叉：同一层级同时有 %s。'
                    '分叉出去的骨骼（例如腕部的拇指、小翼羽）不用选进来，'
                    '只选主链就行'
                    % '、'.join('与'.join(v) for v in br[:2]))
    return order, ''


ARM_TURN_LIMIT = 75.0
# 「末节手臂」允许的转向上限：比 ARM_TURN_LIMIT 紧得多。
# 真正的末节手臂几乎顺着上一节的走向延续下去（实测 4 节/6 节手臂的末节都是 17° 以内），
# 而羽毛是从手臂上岔出去的（实测 28° 起）。24° 落在两者中间。
ARM_TIP_TURN = 24.0
# 走链时「方向贴合度」的权重尺度（度）。分数 = 还能延伸多长 × exp(−(转向/这个值)²)。
# 为什么不是简单的 cos 加权：手臂的下一节几乎顺着上一节（实测 5~17°），而羽毛至少
# 岔开 28°；可羽毛往往**更长**，光按「长度 × cos」会算输给一根长飞羽 ——
# 实测 build_wing_true 把整根羽毛一起选中时，手臂链被吃成
# humerus → radius → hand → primary10_1 → primary10_2，`tip` 整节丢了。
# 换成这个陡得多的贴合度权重之后，「几乎共线的那一节」才稳定压过长羽毛；
# 尺度取 22 是实测出来的：28° 的飞羽权重 0.20、17° 的末节权重 0.55，末节稳赢。
ARM_ALIGN_SIGMA = 22.0


def longest_selected_chain(sel):
    """在「选中的骨骼」里挑出最长的一条 **手臂** 主链（给一键生成用）

    只在选中的子图里走：每个选中的骨骼接它那些**也被选中**的子骨骼。

    难在「羽毛常常已经挂在手臂骨骼下面」（真实模型、以及生成过一次绑定之后都是
    这样），这时单纯的「最长路径」会从手腕直接拐进最长的那根飞羽里，把羽毛当成
    手臂的延续。实测 23 根羽毛的场景里手臂链会变成
        humerus → radius → hand → flight13_1 → flight13_2 → flight13_3
    —— 那根飞羽既被从羽毛表里吃掉，又被当成手臂节去折叠，生成出来是一套废绑定。

    所以每走一步都要看**转向角**：手臂是顺着上一节的走向延续下去的，羽毛是从
    手臂上「岔」出去的。实测这个场景里手臂各节之间只转 5°~6°，而羽毛的岔角是
    97°~135°，区分得非常干净。打分 = 这条分支还能延伸多长 × 转向的贴合度；
    最好的那个候选转向也超过 ARM_TURN_LIMIT 就直接停住 —— 宁可少走一节，
    也不要把羽毛吞进手臂里（用户少选一节会立刻看出来，吞了羽毛则是一套隐形废绑定）。
    """
    picked = set(sel)
    memo = {}

    def seg(a, b):
        return (om.MVector(*world_pos(b)) - om.MVector(*world_pos(a))).length()

    def down_len(node):
        """node 往下（只在选中的子图里走）最长的一条路径有多长"""
        if node in memo:
            return memo[node]
        best = 0.0
        for c in child_joints(node):
            if c in picked:
                best = max(best, seg(node, c) + down_len(c))
        memo[node] = best
        return best

    def dir_to(a, b):
        v = om.MVector(*world_pos(b)) - om.MVector(*world_pos(a))
        return v.normal() if v.length() > 1e-9 else None

    def bone_dir(c, node):
        """这根骨头**自身**往哪个方向走（不是「从上一节指向它」）

        区分手臂和羽毛必须用这个。羽毛的根骨骼就落在它依附的那节手臂骨骼末端
        附近（实测最后一根主飞羽的根几乎就在 hand 的延长线上），所以从 hand 看
        过去，它和真正的下一节手臂几乎同向 —— 实测 1.7° 对 2.6°，完全分不开。
        换成骨骼自身的走向就干净了：有子骨骼时取「根 → 子骨骼」的方向；
        光杆骨骼用局部 X 轴（Maya 里骨骼的 X 轴指向子骨骼）。

        光杆骨骼的 X 轴有两种情况，得分开处理：
          · 手臂的最后一节（tip）：X 轴是 orientJoint 给的，可能顺着链也可能反着
            （实测镜像那只翅膀的 tip 恰好反了 160°，于是手臂链被截在 hand 上，
            长度只有正确值的 64%，双翼拆分因此判定失败）。这种 X 轴和
            「父级指向它」几乎平行，按父级方向的正负号翻一下就好。
          · 单节羽毛：X 轴记的是羽毛自己的朝向，和「父级指向它」差得远（>90°），
            这时不能翻，翻了就正好变成手臂方向、把羽毛认成手臂的延续。
        """
        kids = child_joints(c)
        if kids:
            end = max(kids, key=lambda k: down_len(k))
            v = om.MVector(*world_pos(end)) - om.MVector(*world_pos(c))
            if v.length() > 1e-9:
                return v.normal()
        d = joint_direction(c)
        if d is None:
            return dir_to(node, c)
        ref = dir_to(node, c)
        if ref is not None and d * ref < -0.9:
            d = om.MVector(-d.x, -d.y, -d.z)
        return d

    best, best_key = [], None
    for head in [j for j in sel if get_parent(j) not in picked]:
        path, node = [head], head
        while True:
            d_in = dir_to(path[-2], node) if len(path) > 1 else None
            pick, pick_score, pick_turn = None, -1e18, 0.0
            for c in child_joints(node):
                if c not in picked:
                    continue
                reach = seg(node, c) + down_len(c)
                turn = 0.0
                if d_in is not None:
                    d = bone_dir(c, node) or dir_to(node, c)
                    if d is not None:
                        cos = max(-1.0, min(1.0, d_in * d))
                        turn = math.degrees(math.acos(cos))
                score = reach * math.exp(-((turn / ARM_ALIGN_SIGMA) ** 2))
                if score > pick_score:
                    pick, pick_score, pick_turn = c, score, turn
            if pick is None or pick_turn > ARM_TURN_LIMIT:
                break
            path.append(pick)
            node = pick
        path = trim_arm_tail(path)
        key = (chain_length(joint_positions(path)), len(path))
        if best_key is None or key > best_key:
            best, best_key = list(path), key
    if len(best) < 2:
        return [], ('选中里找不到一条手臂链：请把这一节手臂的骨骼一起选中'
                    '（至少要根骨骼 + 手臂骨骼两根）')
    return best, ''


def trim_arm_tail(path):
    """把「走到手臂尽头之后顺手吞进来的一根羽毛」从链尾摘掉

    手臂走到最末一节时，它的孩子**全是**羽毛：转向角那道 75° 的闸门拦不住 ——
    最外侧那几根主飞羽本来就顺着翼展方向伸出去，与手臂只差 30~50°。
    实测 2 节手臂的最简模型上，一键生成把最外侧那根飞羽当成了第 2 节手臂
    （手臂表里出现「肱骨 → 羽毛05_1」这种行，还往羽毛上插了 FK 偏移组，
    `hand` 反而整节丢了）。

    摘的判据：从链尾往前找**最长的一段「不分叉的条」**（每节只有一个子骨骼、
    末节是光杆 —— 羽毛就是从根到尖的一条），如果这段条的整体走向与它前面那节的
    走向夹角 > ARM_TIP_TURN，就把整段条摘掉，然后再看一次。
    要点：
      · 条必须**至少 2 节**才考虑。手臂的末节是光杆，它自己单独构不成一段条，
        于是天然被保护住 —— 早期版本拿末节自己的 X 轴去算转向，那个轴是 orientJoint
        给的、和链的方向没关系，build_wing_b 的末节被误判成 40°+，整节手臂被摘掉，
        验收里挂了 6 项。
      · 也不能只看链尾那一节：被吞进来的羽毛，它的**末节是光杆**（照上面那条会被
        保护），要看的其实是条根那一节的走向（条根有子骨骼，能拿到真实方向）。
    摘完至少要剩 2 节，否则原样返回。
    """
    path = list(path)

    def trail_dir(i):
        """path[i:] 这段「尾巴」整体往哪走；返回 None 表示它不是一根独立的条

        要求从 path[i] 到链尾在**场景里**都是单链（每节只有一个子骨骼、且就是链上的
        下一节）。链尾那一节可以是光杆（条尖），也可以是「选中里链就断在这儿」
        （只选了羽毛根、没选子骨骼时就是这样）。
        """
        for k in range(i, len(path) - 1):
            kids = child_joints(path[k])
            if len(kids) != 1 or kids[0] != path[k + 1]:
                return None
        if i == len(path) - 1:
            # 尾巴只有一节：它在场景里还有子骨骼才说明这是「被截断的一条」；
            # 真正的光杆末节（手臂的梢）返回 None，天然被保护住。
            return bone_dir_for_trim(path[i])
        v = om.MVector(*world_pos(path[-1])) - om.MVector(*world_pos(path[i]))
        return v.normal() if v.length() > 1e-9 else None

    while len(path) > 2:
        start, d = None, None
        for cand in range(1, len(path)):
            v = trail_dir(cand)
            if v is not None:
                start, d = cand, v
                break
        if start is None or start < 2 or d is None:
            break
        d_in = om.MVector(*world_pos(path[start])) - om.MVector(
            *world_pos(path[start - 1]))
        if d_in.length() < 1e-9:
            break
        d_in.normalize()
        turn = math.degrees(math.acos(max(-1.0, min(1.0, d_in * d))))
        if turn <= ARM_TIP_TURN:
            break
        path = path[:start]
    return path


def bone_dir_for_trim(node):
    """摘链尾时用的「自身走向」：沿着这条条下一步往哪走

    只在 node 有子骨骼时被调用，所以永远能拿到真实的方向，不依赖骨骼自身的 X 轴。
    """
    kids = child_joints(node)
    if not kids:
        return None
    end = max(kids, key=lambda k: (om.MVector(*world_pos(k))
                                   - om.MVector(*world_pos(node))).length())
    v = om.MVector(*world_pos(end)) - om.MVector(*world_pos(node))
    return v.normal() if v.length() > 1e-9 else None


def selected_groups(sel):
    """把选中的骨骼按「没有被选中的父级」拆成几组骨架，每组一棵独立的树

    左右两只翅膀一起框选时，它们的根骨骼（肩）都没有被选中的父级，
    自然就分成两组；一只翅膀内部的骨骼都有被选中的祖先，不会拆开。
    """
    picked = set(sel)
    out = []
    for head in [j for j in sel if get_parent(j) not in picked]:
        group, stack = [], [head]
        while stack:
            node = stack.pop()
            group.append(node)
            stack.extend([c for c in child_joints(node) if c in picked])
        out.append(group)
    return out


def count_long_leaf_paths(joint, min_len):
    """从 joint 往下，有几条「末端路径」的累计长度超过 min_len

    用来分辨「这是一条手臂」还是「这是一根羽毛」：
    羽毛是一根光杆（从根到尖只有一条路径）；一条手臂下面挂着它自己的羽毛，
    会有很多条够长的末端路径。光看「子链有多长」会误判 —— 长飞羽能到手臂的
    六成，按长度一刀切会把最长的那根飞羽当成手臂扔掉。
    """
    def seg(a, b):
        return (om.MVector(*world_pos(b)) - om.MVector(*world_pos(a))).length()
    n = 0
    stack = [(c, seg(joint, c)) for c in child_joints(joint)]
    while stack:
        node, ln = stack.pop()
        kids = child_joints(node)
        if not kids:
            if ln > min_len:
                n += 1
            continue
        for c in kids:
            stack.append((c, ln + seg(node, c)))
    return n


def fk_ctrl_of(off_group):
    """由 FK 偏移组的名字推出对应的 FK 圆环控制器名

    生成时圆环叫 `<骨骼>_fkCtrl`、偏移组叫 `<骨骼>_fk`，一一对应。
    自检、重新生成、将来要「一键选中所有手臂控制器」都要在两者之间换算，
    写成一个函数，免得命名规则散落在各处、改一处漏一处。
    """
    n = short_name(off_group or '')
    if not n.endswith(FK_OFF_SUFFIX):
        return None
    ring = n[:-len(FK_OFF_SUFFIX)] + FK_CTRL_SUFFIX
    return ring if cmds.objExists(ring) else None


def longest_subtree_len(joint):
    """joint 往下最长的一条路径有多长（走场景里全部子骨骼，不只是选中的）

    用来分辨「这是一条手臂」还是「一根羽毛」：手臂往下一直是手臂，能延伸到整条
    臂长；羽毛往下最多就是羽毛自己的长度。实测最长的主飞羽是手臂的 64%，
    所以拿 80% 当门槛能干净地分开，又不会冤枉长飞羽。
    """
    def seg(a, b):
        return (om.MVector(*world_pos(b)) - om.MVector(*world_pos(a))).length()
    best = 0.0
    stack = [(c, seg(joint, c)) for c in child_joints(joint)]
    while stack:
        node, ln = stack.pop()
        if ln > best:
            best = ln
        for c in child_joints(node):
            stack.append((c, ln + seg(node, c)))
    return best


def is_fk_offset(node):
    """是不是本插件插入的手臂 FK 偏移组"""
    return bool(node) and short_name(node).endswith(FK_OFF_SUFFIX)


def set_ctrl_color(node, index):
    """给控制器的线框上一个索引色（用绘制覆盖，不动材质）

    只影响显示：overrideEnabled + overrideColor 是 Maya 的「绘制覆盖」，
    不会改材质、不会被渲染出来，纯粹让动画师在视口里分得清控制器。
    """
    if not node or not cmds.objExists(node):
        return
    for s in cmds.listRelatives(node, s=True) or []:
        cmds.setAttr(s + '.overrideEnabled', 1)
        cmds.setAttr(s + '.overrideColor', index)


def child_joints(node):
    """取直接子骨骼（长名）

    中间夹着本插件插入的 FK 偏移组时自动穿过去，保证骨链逻辑不受影响。
    """
    out = []
    for c in cmds.listRelatives(node, c=True, f=True) or []:
        if cmds.nodeType(c) == 'joint':
            out.append(c)
        elif is_fk_offset(c):
            out.extend(child_joints(c))
    return out


def get_parent(node):
    """取父节点长名；穿过本插件插入的 FK 偏移组"""
    rel = cmds.listRelatives(node, p=True, f=True) or []
    parent = rel[0] if rel else None
    guard = 0
    while parent and is_fk_offset(parent) and guard < 8:
        rel = cmds.listRelatives(parent, p=True, f=True) or []
        parent = rel[0] if rel else None
        guard += 1
    return parent


def get_direct_parent(node):
    """取直接父节点长名（不穿过 FK 偏移组）"""
    rel = cmds.listRelatives(node, p=True, f=True) or []
    return rel[0] if rel else None


def is_referenced(node):
    """节点是不是来自参考（reference）进来的文件"""
    if not node or not cmds.objExists(node):
        return False
    try:
        return bool(cmds.referenceQuery(node, isNodeReferenced=True))
    except Exception:
        return False


def ref_parent_block(feathers):
    """找出「必须重新父子、但骨骼在参考里」的第一根羽毛，没有则返回 None

    Maya 硬限制：参考进来的文件**不许改层级结构**。实测（Maya 2025）三条路全堵死：
      · cmds.parent(root, arm)  → "Cannot parent a referenced object to another
        referenced object. Use the 'group' command."
      · cmds.group(root, parent=arm) → "Objects with Read Only parents may not
        be grouped"（root 挂在参考里的父节点下，那个父是只读的）
      · 先建空组再 cmds.parent(root, grp) → "Referenced objects parented to
        referenced objects may not be reparented."
    所以不试图硬来，只把「哪一根、为什么」讲清楚，让用户自己去 Reference Editor
    里 Import 进来（或重新导入时不勾 Reference）再生成。
    """
    for i, feather in enumerate(feathers):
        root = resolve_joint(short_name(feather['root']))
        arm = resolve_joint(short_name(feather['arm']))
        if root is None or arm is None or get_parent(root) == arm:
            continue
        if is_referenced(root):
            return i + 1, short_name(root), short_name(arm)
    return None


def get_chain(root, tip=None):
    """按顺序取出一节手臂的关节链

    root：该节手臂的根骨骼
    tip ：该节手臂的手臂骨骼（末端）；为空时自动沿第一个子关节走到末端
    """
    root = resolve_joint(root)
    if root is None:
        return []
    tip = resolve_joint(tip)
    if tip is None:
        chain = [root]
        node = root
        while True:
            children = child_joints(node)
            if not children:
                break
            node = children[0]
            chain.append(node)
        return chain
    path = []
    node = tip
    while node and node != root:
        path.append(node)
        node = get_parent(node)
    if node != root:
        return [root]
    path.append(root)
    path.reverse()
    return path


def get_longest_chain(root):
    """从 root 出发取最长的一条关节链（用来确定羽毛的朝向）"""
    root = resolve_joint(root)
    if root is None:
        return []
    best = [root]
    for child in child_joints(root):
        sub = get_longest_chain(child)
        if len(sub) + 1 > len(best):
            best = [root] + sub
    return best


def chain_ancestor(joint, chain_set):
    """沿父级往上找第一个属于 chain_set 的骨骼（含自己），找不到返回 None

    用来处理「羽毛挂在手臂骨骼的下级分支上」——鸟类腕部的拇指就是这样：
    它自己不参与折叠，但挂在它所依附的那节手臂骨骼下，会跟着那节一起转，
    挂在上面的小翼羽（alula）能正常收。这类羽毛的驱动轴、收拢量都要按
    「它最早的那节手臂链祖先」算，而不是按它自己（分支不折叠，旋转变化量为 0）。
    """
    node = joint
    seen = set()
    while node and node not in seen:
        seen.add(node)
        if node in chain_set:
            return node
        node = get_parent(node)
    return None


def feat_arm_source(arm, chain, chain_set=None):
    """一根羽毛实际「跟着哪一节手臂骨骼动」：返回 chain 里的那节，没有则 None

    羽毛的「对应手臂骨骼」有两种合法填法：手臂链上的某一节本身，
    或者手臂骨骼的下级分支（拇指）。后者要归到它最早的链祖先那一节上，
    折叠轴、收拢进度、驱动源都按那一节算。
    """
    if arm is None:
        return None
    if arm in chain:
        return arm
    return chain_ancestor(arm, chain_set if chain_set is not None else set(chain))


def world_pos(node):
    """世界坐标"""
    return cmds.xform(node, q=True, ws=True, t=True)


def joint_positions(chain):
    """取关节的世界坐标列表"""
    return [world_pos(j) for j in chain]


def joint_direction(node):
    """骨骼自身的朝向（关节局部 X 轴在世界空间的方向）

    Maya 的骨骼约定是「局部 X 轴指向子骨骼」（orientJoint 的默认主轴就是 xyz），
    因此只有一根骨骼、没有子骨骼可以参照时，用它来判断这根羽毛朝哪。
    """
    m = om.MMatrix(cmds.xform(node, q=True, ws=True, m=True))
    v = om.MVector(m[0], m[1], m[2])
    if v.length() < 1e-9:
        return None
    v.normalize()
    return v


def feather_direction(feather_root):
    """羽毛的静止朝向：根骨骼指向羽毛末端；没有子骨骼时用骨骼自身朝向"""
    chain = get_longest_chain(feather_root)
    if len(chain) >= 2:
        v = om.MVector(*world_pos(chain[-1])) - om.MVector(*world_pos(chain[0]))
        if v.length() > 1e-6:
            v.normalize()
            return v
    return joint_direction(feather_root)


def plane_normal(points):
    """由一组点求最佳拟合平面的法线"""
    normal = om.MVector()
    count = len(points)
    for i in range(count - 2):
        a = om.MVector(*points[i])
        b = om.MVector(*points[i + 1])
        c = om.MVector(*points[i + 2])
        normal += (b - a) ^ (c - b)
    if normal.length() < 1e-6:
        # 退化：换一个稳定的构造方式
        v = om.MVector(*points[-1]) - om.MVector(*points[0])
        if v.length() < 1e-6:
            return om.MVector(0.0, 0.0, 1.0)
        v.normalize()
        candidates = [om.MVector(1, 0, 0), om.MVector(0, 1, 0), om.MVector(0, 0, 1)]
        best = min(candidates, key=lambda a: abs(a * v))
        normal = v ^ best
    normal.normalize()
    return normal


def wing_axis(arm_pts, roots, tips):
    """翼面法线（折叠轴）：由「手臂走的方向」和「羽毛走的方向」张成的平面的法线

    为什么不用「把所有点丢进一个拟合平面」：
    那种做法是把相邻三点的叉乘累加起来，对**点的顺序**和**是否严格共面**极其敏感。
    真实翅膀的点几乎是共面的，各叉乘的符号会互相抵消，剩下的残差被那一点点厚度
    噪声主导，算出来的轴可以歪掉几十度——实测过一个场景，羽毛朝向与算出来的
    「法线」夹角达到 53°~74°，等于绕着一根几乎和羽毛平行的轴去收羽毛，
    收起后当然是一团乱的（羽包厚度 1.09，比细长叶子的 0.07 厚了 15 倍）。
    手臂 × 羽毛 的叉乘只依赖两个整体方向，跟点的顺序、点是否共面都无关。

    退化（手臂与羽毛几乎平行）时返回 None，交给调用方回退。
    """
    if len(arm_pts) < 2:
        return None
    arm_dir = om.MVector(*arm_pts[-1]) - om.MVector(*arm_pts[0])
    if arm_dir.length() < 1e-6:
        return None
    feather_dir = om.MVector()
    for r, t in zip(roots, tips):
        d = om.MVector(*t) - om.MVector(*r)
        if d.length() > 1e-9:
            d.normalize()
            feather_dir += d
    if feather_dir.length() < 1e-6:
        return None
    axis = arm_dir ^ feather_dir
    if axis.length() < 1e-6 * arm_dir.length():
        return None                      # 手臂与羽毛平行，叉乘退化
    axis.normalize()
    return axis


def pack_rig_data(info):
    """把「拆除绑定 / 自检需要的登记信息」序列化成字符串，存到控制器上（见 RIG_DATA_ATTR）

    只存重开文件以后用得上的东西：全部骨骼名、静止姿态、手臂偏移组、每根羽毛的那几个
    节点名。收起解算用的 sweep / 轴 / 驱动通道这些不用存——重新生成时会重算。
    """
    def nl(names):
        return [short_name(n) for n in (names or []) if n]

    data = {
        'root': short_name((info.get('joints') or [''])[0]),
        # 手臂 + 羽毛的全部骨骼。以前没存这一项，重开文件后 info['joints'] 是空的，
        # 自检第 3 项要取 chain[0] 就直接 IndexError 崩掉 —— 用户打开演示场景点「自检」
        # 就报错。必须存下来。
        'joints': nl(info.get('joints')),
        # 翼面法线：重开文件后自检第 9 项要用它判「深度有没有翻过来」，
        # 不存就会 KeyError 直接崩。
        'normal': [info['normal'][0], info['normal'][1], info['normal'][2]]
        if info.get('normal') else [0.0, 0.0, 1.0],
        'rest_rotate': dict((short_name(k), list(v))
                            for k, v in (info.get('rest_rotate') or {}).items()),
        # 生成前每根骨骼世界矩阵的 3x3（自检「骨骼静止朝向还原」要用）
        'rest_rot3': dict((short_name(k), list(v))
                          for k, v in (info.get('rest_rot3') or {}).items()),
        'rest_translate': dict((short_name(k), list(v))
                               for k, v in (info.get('rest_translate') or {}).items()),
        'offsets': dict((short_name(k), short_name(v))
                        for k, v in (info.get('offsets') or {}).items()),
        'extras': [{'root': short_name(e['root']),
                    'arm': short_name(e.get('arm') or ''),
                    'grp': short_name(e.get('grp') or ''),
                    'ctrl': short_name(e.get('ctrl') or ''),
                    'tip': short_name(e.get('tip') or ''),
                    'curve': short_name(e.get('curve') or ''),
                    'constraints': nl(e.get('constraints')),
                    'locators': nl(e.get('locators')),
                    'poci': nl(e.get('poci')),
                    'tip_nodes': nl(e.get('tip_nodes'))}
                   for e in (info.get('extras') or [])],
    }
    return json.dumps(data, separators=(',', ':'))


def unpack_rig_data(text):
    """把存进文件的信息还原成登记表（节点名按短名重新找回来；找不到的记成 None）"""
    try:
        data = json.loads(text)
    except Exception:
        return None

    def find(name):
        if not name:
            return None
        found = cmds.ls(name) or []
        return found[0] if found else None

    info = {'root': data.get('root') or '', 'joints': [],
            'normal': om.MVector(*(data.get('normal') or [0.0, 0.0, 1.0])),
            'rest_rotate': {}, 'rest_translate': {}, 'offsets': {}, 'extras': [],
            'rest_rot3': {}}
    for k in (data.get('joints') or []):
        j = resolve_joint(k)
        if j:
            info['joints'].append(j)
    for k, v in (data.get('rest_rotate') or {}).items():
        j = resolve_joint(k)
        if j:
            info['rest_rotate'][j] = list(v)
    for k, v in (data.get('rest_translate') or {}).items():
        j = resolve_joint(k)
        if j:
            info['rest_translate'][j] = list(v)
    for k, v in (data.get('rest_rot3') or {}).items():
        j = resolve_joint(k)
        if j:
            info['rest_rot3'][j] = list(v)
    for k, v in (data.get('offsets') or {}).items():
        j = resolve_joint(k)
        g = find(v)
        if j and g:
            info['offsets'][j] = g
    for e in (data.get('extras') or []):
        root = resolve_joint(e.get('root') or '')
        if root is None:
            continue
        info['extras'].append({
            'root': root,
            'arm': resolve_joint(e.get('arm') or ''),
            'grp': find(e.get('grp')), 'ctrl': find(e.get('ctrl')),
            'tip': find(e.get('tip')), 'curve': find(e.get('curve')),
            'constraints': [find(x) for x in (e.get('constraints') or [])],
            'locators': [find(x) for x in (e.get('locators') or [])],
            'poci': [find(x) for x in (e.get('poci') or [])],
            'tip_nodes': [find(x) for x in (e.get('tip_nodes') or [])],
        })
    return info


def signed_angle(normal, vec_from, vec_to):
    """vec_from 绕 normal 转到 vec_to 的有符号角（弧度），范围 (-pi, pi]"""
    cross = vec_from ^ vec_to
    return math.atan2(cross * normal, vec_from * vec_to)


def axis_angle_matrix(axis, angle):
    """绕任意轴旋转 angle(弧度) 的旋转矩阵（axis 已归一化）

    注意：Maya 的 MMatrix 采用行向量约定（矩阵的行 = 基向量在世界中的方向），
    因此这里是标准旋转矩阵的转置，保证与 MEulerRotation.asMatrix() 一致。
    """
    x, y, z = axis.x, axis.y, axis.z
    c = math.cos(angle)
    s = math.sin(angle)
    t = 1.0 - c
    m = om.MMatrix()
    m[0] = t * x * x + c
    m[1] = t * x * y + s * z
    m[2] = t * x * z - s * y
    m[4] = t * x * y - s * z
    m[5] = t * y * y + c
    m[6] = t * y * z + s * x
    m[8] = t * x * z + s * y
    m[9] = t * y * z - s * x
    m[10] = t * z * z + c
    return m


def rotate_vector(vec, axis, angle):
    """把向量绕轴旋转 angle(弧度)（行向量约定：v' = v · M）"""
    m = axis_angle_matrix(axis, angle)
    return om.MVector(
        vec.x * m[0] + vec.y * m[4] + vec.z * m[8],
        vec.x * m[1] + vec.y * m[5] + vec.z * m[9],
        vec.x * m[2] + vec.y * m[6] + vec.z * m[10],
    )


def matrix_det3(m):
    """世界矩阵 3x3 部分的行列式（<0 = 这一支被镜像过，是左手系）"""
    return (m[0] * (m[5] * m[10] - m[6] * m[9])
            - m[1] * (m[4] * m[10] - m[6] * m[8])
            + m[2] * (m[4] * m[9] - m[5] * m[8]))


def orthonormal_rotation(m):
    """取矩阵的旋转部分（正交化，剔除缩放/剪切）

    第三行用 x×y 重建，也就是**强行当成右手系**。

    曾经以为这就是「父级带负缩放的镜像翅膀收起会炸」的原因，还试过「保留手性」
    （第三行拿矩阵自己的第三行去正交化），结果更糟，于是留下了「这条管线假设
    行列式 +1，改不得」的结论。

    那个结论是**错的**，2026-09 重新量过（diag_mirror.py，夹具 build_wing_shape
    带 WING_GROUP_SCALE=-1,1,1）：
      · 只要**整只翅膀连羽毛一起**被镜像（世界矩阵行列式统一是 -1），插件一切正常 ——
        收起到底「最远羽尖离肩」1.644，和没镜像时逐位相同，静止姿态还原误差 0.0000。
      · 之前量到的 5.16 是一个**自相矛盾**的夹具造成的：那套夹具只把一部分羽毛挂进
        翅膀层级（其余留在世界根下），于是手臂被镜像（det -1）、那些羽毛没被镜像
        （det +1）。羽毛和它的手臂根本不在同一个坐标系里，插件再把它们挂到镜像过的
        手臂下，局部矩阵里就多出一个负缩放，手臂一折羽毛就飞出去 —— 这不是手性问题，
        是场景本身不自洽。
    所以这里维持右手化，改成在 build_rig 里检测「羽毛和手臂的行列式符号不一致」
    并明确报出来（那种场景下绑定必然是坏的，说清楚比静默生成一套废绑定好）。
    """
    x = om.MVector(m[0], m[1], m[2])
    y = om.MVector(m[4], m[5], m[6])
    x.normalize()
    y = y - x * (x * y)
    y.normalize()
    z = x ^ y
    r = om.MMatrix()
    r[0], r[1], r[2] = x.x, x.y, x.z
    r[4], r[5], r[6] = y.x, y.y, y.z
    r[8], r[9], r[10] = z.x, z.y, z.z
    return r


def world_rot_matrix(node):
    """取节点世界矩阵的旋转部分（正交化，剔除缩放/剪切）"""
    return orthonormal_rotation(om.MMatrix(cmds.xform(node, q=True, ws=True, m=True)))


def axis_in_space(rot_matrix, world_axis):
    """把世界轴换算到某个局部坐标系里（rot_matrix 的行就是该系的三个基向量）"""
    return om.MVector(
        rot_matrix[0] * world_axis.x + rot_matrix[1] * world_axis.y + rot_matrix[2] * world_axis.z,
        rot_matrix[4] * world_axis.x + rot_matrix[5] * world_axis.y + rot_matrix[6] * world_axis.z,
        rot_matrix[8] * world_axis.x + rot_matrix[9] * world_axis.y + rot_matrix[10] * world_axis.z,
    )


def euler_matrix(rot_deg, order):
    """把 rotate 属性值（度）转成矩阵"""
    return om.MEulerRotation(
        math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]), order
    ).asMatrix()


def matrix_to_euler(m, order):
    """矩阵分解成指定旋转顺序的欧拉角（度）"""
    e = om.MTransformationMatrix(m).rotation()
    e = e.reorder(order)
    return (math.degrees(e.x), math.degrees(e.y), math.degrees(e.z))


def euler_rot_angle(a, b, order):
    """两组欧拉角**组成的旋转**之间的夹角（度）—— 与分量怎么取无关"""
    m = euler_matrix(a, order).inverse() * euler_matrix(b, order)
    tr = m[0] + m[5] + m[10]
    return math.degrees(math.acos(max(-1.0, min(1.0, (tr - 1.0) * 0.5))))


def unwrap_euler(prev, cur, order=0, target=None):
    """把欧拉角按「离上一帧最近」展开，避免 ±180 环绕把插值绕到远路上去

    绕任意轴的旋转分解成欧拉角时，相邻两个采样点可能从 -179° 直接跳到 +179°
    （其实是同一侧、只差 2°）。驱动关键帧之间是线性插值，这样会让关节绕着反方向
    扫过 358°，收起过程就会剧烈乱跳、甚至有的羽毛像没收一样。
    这里把每个分量加减 360°，使相邻变化量落在 (-180, 180] 内。

    但**只按分量取最短路径还不够**：欧拉分解有**等价双解**（XYZ 顺序下
    (x, y, z) 与 (x±180, 180∓y, z±180) 表示同一个旋转）。逐分量展开可能整组
    落到另一支上去 —— 每个分量各自看着都「没绕远路」，但组成的旋转在相邻两档
    之间反了一次。实测「解剖比例」那套：收起 81.8% → 90.9% 之间，肘关节
    `anat_wing_radius` 的某个分量跳了 175°，线性插值让手臂中途翻过去，
    整只翅膀在 85%~90% 之间弹到展开半径的 45% 再收回去（自检只采 0/50/100，
    所以一直没报出来）。

    所以给了 target 矩阵时，把等价的第二组解也当候选，**先用矩阵验证它确实表示同一个
    旋转**，再按「相邻两档之间每个分量的最大变化量最小」挑（线性插值走的就是分量，
    所以这个量才是插值路径的长度）。这样选出来的那一支，插值路径才真的是短的。

    注意不能用「组成的旋转离上一档最近」当判据 —— 等价解的旋转是**同一个**，
    旋转距离完全一样，分不出来；而如果候选公式写错、根本不是同一个旋转，
    那个判据还会把它误选进来（实测整只翅膀会乱跳）。
    """
    cands = []
    if target is not None:
        b = matrix_to_euler(target, order)
        m_true = euler_matrix(b, order)
        raw = [b]
        for sx in (-180.0, 180.0):
            for sz in (-180.0, 180.0):
                raw.append((b[0] + sx, 180.0 - b[1], b[2] + sz))
        for c in raw:
            m_c = euler_matrix(c, order)
            if max(abs(m_c[i] - m_true[i]) for i in range(11)) < 1e-4:
                cands.append(c)
    else:
        cands = [cur]
    best = None
    for c in cands:
        out = []
        for i in range(3):
            v = c[i]
            p = prev[i]
            while v - p > 180.0:
                v -= 360.0
            while v - p < -180.0:
                v += 360.0
            out.append(v)
        d = max(abs(out[i] - prev[i]) for i in range(3))
        if best is None or d < best[0]:
            best = (d, out)
    return tuple(best[1])


def hungarian_assign(cost):
    """最小代价的**一对一**分配（匈牙利算法，O(n³) 势函数版）

    返回 assign[i] = 分给第 i 行的列号；行数 > 列数（没法一一对应）时返回 None。

    为什么羽毛权重归一要用它：给每张羽毛卡认「它属于哪根羽毛」时，逐张卡各挑
    最近的一条链会**两张卡抢同一条链** —— 覆羽和它压在下面那根飞羽的根骨骼
    只差 0.086，谁快算谁的，被抢的那根羽毛就没卡认领了。全局一对一之后被抢的
    羽毛必须去找它自己那张卡。实测真翼形 38 张卡：逐卡挑认对 35 张，
    全局一对一认对 38 张（求解器本身拿 300 个随机方阵和暴力枚举对过，全一致）。
    """
    n = len(cost)
    m = len(cost[0]) if n else 0
    if not n or not m or n > m:
        return None
    INF = float('inf')
    u = [0.0] * (n + 1)
    v = [0.0] * (m + 1)
    p = [0] * (m + 1)            # p[j] = 第 j 列配给哪一行（1 起）
    way = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    out = [-1] * n
    for j in range(1, m + 1):
        if p[j]:
            out[p[j] - 1] = j - 1
    return out


def feather_goal(origin, folded_tip, arm_pts, auto_dir=True, ref_u=None):
    """羽毛收拢的目标方向 —— 生成、折点估算、方向估算三处共用同一条规则

    · 「自动(沿手臂收回)」：先取「肩 − 折完的手」，再按**静止时的手臂方向 u** 判正负。
      正常情况下这个方向本来就朝里；但换一个折叠方向（例如只折靠肩的那一节）折完的
      「手」会跑到肩的另一侧，这个方向就变成朝外了 —— 羽毛顺着它往外甩，整只翅膀
      越收越大。所以必须用静止方向兜这一道。
    · 「反向(往外伸)」：直接取另一侧。

    为什么要抽成共用函数：以前只有生成时的 feather_targets 做了这一步，两个估算函数
    （fold_package / folded_extent）只按 sign 翻手臂、不翻羽毛方向，于是「羽毛朝哪收」
    估的和生成的不是一回事。实测 human.mb 的真实骨架：估算说「手臂收回 48%」，
    实际收起后羽尖到肩是展开的 105%（就是「收起反而变大」那条警告）。
    """
    goal = om.MVector(*origin) - om.MVector(*folded_tip)
    if goal.length() < 1e-9:
        return None
    goal.normalize()
    if not auto_dir:
        return -goal
    # ref_u 是「判正负用的那个朝外方向」。默认取静止时的手臂方向；**施加了根部
    # 后掠角时必须把同一份旋转传进来**（ref_u = 静止手臂方向绕 N 转过那个后掠角）——
    # 后掠约 90° 时「折完的手 → 肩」正好和新 u 垂直，拿没转过的那把尺子去量、
    # 正负号就是抽签：实测 build_wing_real 会被翻反，收起从 46% 掉到 86%、
    # 中途还冒出 9.6% 的回弹。传进来的是「和后掠一起转过的尺子」，量出来才是不变量。
    if ref_u is not None:
        u = om.MVector(*ref_u)
    else:
        u = om.MVector(*arm_pts[-1]) - om.MVector(*arm_pts[0])
    if u.length() > 1e-9:
        u.normalize()
        if goal * u > 0.0:
            goal = -goal
    return goal


def feather_base(feather, arm_pts, k, psis, normal, sign, sim):
    """折完以后这根羽毛的**根部**落在哪

    羽毛根刚性挂在手臂骨骼下（权重 1），所以它跟着第 k 节手臂骨骼一起绕 N 转过
    ψ_k —— 根部相对关节的那个静止偏移也要一起转：
        base = 折后关节位置 + 偏移 · A(N, ψ_k)
    早期两个估算函数直接把根部当成关节本身（base = 折后关节位置 = sim[k]），
    羽毛挂在「离关节有一段距离」的位置时（真实模型里很常见）估出来的伸出量会差
    很多，于是「自动收拢」挑的折叠方向可能挑反 —— 实测 build_wing_real 收起
    39% 变 52%。sim 是调用方按同一组 psis/sign 模拟出来的折后骨链。
    """
    root_w = om.MVector(*world_pos(feather['root']))
    off = root_w - om.MVector(*arm_pts[k])
    off = rotate_vector(off, normal, math.radians(psis[k] * sign))
    return sim[k] + off


def simulated_chain(pts, psis_deg, normal):
    """按各关节的世界旋转增量模拟骨链折叠后的位置（用于判断收拢方向）

    第 k 段（Pk -> Pk+1）的方向由关节 k 的世界旋转决定，因此它绕 N 转过 psis_deg[k]。
    """
    count = len(pts)
    if count < 2:
        return [om.MVector(*pts[0])]
    out = [om.MVector(*pts[0])]
    for k in range(count - 1):
        d = om.MVector(*pts[k + 1]) - om.MVector(*pts[k])
        out.append(out[-1] + rotate_vector(d, normal, math.radians(psis_deg[k])))
    return out


def chain_length(pts):
    """链的总长度"""
    return sum((om.MVector(*pts[i + 1]) - om.MVector(*pts[i])).length()
               for i in range(len(pts) - 1))


# ============================================================ 折叠解算
class RestPose(object):
    """静止姿态数据：每个关节的世界旋转矩阵、局部 rotate、旋转顺序"""

    def __init__(self, joints):
        self.world = {}
        self.rotate = {}
        self.order = {}
        for j in joints:
            self.world[j] = world_rot_matrix(j)
            self.rotate[j] = list(cmds.getAttr(j + '.rotate')[0])
            self.order[j] = cmds.getAttr(j + '.rotateOrder')

    def local_rotation_matrix(self, joint, delta_deg, normal):
        """关节在「世界空间额外绕 N 转过 delta_deg」时的局部旋转**矩阵**"""
        w = self.world[joint]
        a = axis_angle_matrix(normal, math.radians(delta_deg))
        return w * a * w.inverse() * euler_matrix(self.rotate[joint], self.order[joint])

    def rotation_at(self, joint, delta_deg, normal):
        """关节在「世界空间额外绕 N 转过 delta_deg」时的局部 rotate（度）"""
        return matrix_to_euler(self.local_rotation_matrix(joint, delta_deg, normal),
                               self.order[joint])

    def offset_rotation(self, parent_joint, delta_deg, normal):
        """偏移组在「世界空间额外绕 N 转过 delta_deg」时该写的局部 rotate（度）

        偏移组插在关节与它的父骨骼之间、静止朝向与父骨骼一致，
        所以用父骨骼的世界旋转做共轭：R = W(父) · A(N, δ) · W(父)⁻¹。
        （`_fk` 组是动画师的姿势层，目前不参与解算，保留这个工具备用。）
        """
        w = self.world.get(parent_joint)
        if w is None:
            w = world_rot_matrix(parent_joint)
        a = axis_angle_matrix(normal, math.radians(delta_deg))
        return matrix_to_euler(w * a * w.inverse(), 0)


def solve_psis_chain(chain, phis):
    """手臂：把每节折叠角换算成各关节的世界旋转增量

    phis[k] 是关节 k 相对上一根骨骼的折叠角，从根骨骼开始累加。
    根骨骼的 φ 就是界面上的「根部后掠角」：默认为 0，整只翅膀原地折叠不额外后掠。
    """
    psis = {}
    acc = 0.0
    for k, j in enumerate(chain):
        acc += phis[k]
        psis[j] = acc
    return psis


def main_rotate_channel(rest_rot, folded_rot):
    """挑出手臂骨骼上变化最大的 rotate 通道——它就是羽毛的驱动源"""
    deltas = [abs(folded_rot[i] - rest_rot[i]) for i in range(3)]
    index = deltas.index(max(deltas))
    return 'XYZ'[index], deltas[index]


def make_psi_functions(psi_all, chain):
    """返回 (psi_at, parent_psi)：给定收起进度 t，算出关节的世界旋转增量与父级已转过的量

    所有关节按同一个 t 一起折（不做错开）。试过「远端关节先折」的错开：
    Z 形对折里，某个关节的局部折角常常是「替父级做反向补偿」
    （例如 ψ_手 = 0 时，手的折角完全等于 ψ_桡尺骨 的反向），
    它天然绑在父级的进度上、错不开；把错开按链上顺序分下去，
    反而把唯一可见的折叠关节排到了最后，整只翅膀前 60% 一动不动、
    最后 20% 一下子折完（实测已折进度 0,0,0,0,0,0,4,20,46,68 对比 0,0,2,6,14,26,41,56,67,68）。
    """
    parents = {}
    for j in chain[1:]:
        parents[j] = get_parent(j)

    def psi_at(j, t):
        return psi_all.get(j, 0.0) * t

    def parent_psi(j, t):
        node = parents.get(j)
        while node:
            if node in psi_all:
                return psi_all[node] * t
            node = get_parent(node)
        return 0.0

    return psi_at, parent_psi


def _is_ancestor(node, ancestor):
    """node 是不是 ancestor 的后代（穿过 FK 偏移组看）"""
    p = get_parent(node)
    guard = 0
    while p and guard < 256:
        if p == ancestor:
            return True
        p = get_parent(p)
        guard += 1
    return False


def order_arm_rows(rows):
    """把手臂表的行理成「从翼根到翼尖」的顺序，顺手纠正填反的两列

    表格是按顺序用的，但用户在大纲里从下往上框选、或者反复点「上移/下移」之后，
    表里的行很容易不是从翼根到翼尖。这时旧代码直接报「第 2 节手臂没有接上一节：
    期望根骨骼 X、实际 Y」，用户看到的就是「我明明填了，它说不对」。
    行与行之间的父子关系是确定的，按层级深度重排一遍就能恢复；**本来顺序就对的表
    排完一模一样**，所以不会有副作用。排不出来（比如有重复行）就原样返回，
    交给后面的校验去报清楚。

    同时纠正两列填反的情况：正常一行是「根骨骼（父）→ 手臂骨骼（子）」，
    如果反过来「根骨骼」其实是「手臂骨骼」的后代，说明两列填反了，换回来。
    """
    fixed = []
    for r in rows:
        root = resolve_joint(r['root'])
        arm = resolve_joint(r['arm'] or '')
        if root and arm and _is_ancestor(root, arm):
            root, arm = arm, root
        fixed.append(dict(r,
                          root=short_name(root) if root else r['root'],
                          arm=(short_name(arm) if arm else (r['arm'] or ''))))

    def depth(row):
        j = resolve_joint(row['root'])
        if j is None:
            return 1 << 30            # 解析不出来的排到最后，不影响其它行的相对次序
        d, node = 0, get_parent(j)
        while node and d < 256:
            d += 1
            node = get_parent(node)
        return d

    try:
        out = sorted(fixed, key=depth)
    except Exception:
        return rows
    if [r['root'] for r in out] != [r['root'] for r in rows]:
        print('[翅膀绑定] 手臂表的行不是从翼根到翼尖的顺序，已按层级重排成：%s'
              % ' → '.join('%s→%s' % (r['root'], r['arm']) for r in out))
    return out


def rows_to_chain(rows, zigzag=True, root_sweep=0.0):
    """把手臂表格的「行」（每行是一节：root → arm）整理成完整骨链与各关节折叠角

    返回 (chain, phis, err)。err 为 None 表示成功，否则是
    (行号, 原因码, 细节) 三元组，由调用方决定怎么讲给用户听。

    每节的折叠角平均分给该节新增的关节；整条链的根骨骼不参与分角，
    它自己的「根部后掠角」单独控制整只翅膀往收拢方向转多少。
    Z 形对折：相邻节符号相反；扇形卷曲：所有节同号。

    抽成模块级函数是为了让「自动分配折叠角」能反复试算不同行组合，
    而不用每试一次就去改一遍界面上的表。
    """
    rows = order_arm_rows(rows)
    chain = []
    groups = []
    angles = []
    for gi, row in enumerate(rows):
        sub = get_chain(row['root'], row['arm'] or None)
        if len(sub) < 2:
            return [], [], (gi, 'with_arm' if row['arm'] else 'leaf',
                            (row['root'], row['arm']))
        if chain and sub[0] != chain[-1]:
            return [], [], (gi, 'gap', (chain[-1], sub[0]))
        new_joints = sub[1:] if chain else sub
        if not new_joints:
            return [], [], (gi, 'empty', ())
        chain.extend(new_joints)
        groups.extend([gi] * len(new_joints))
        angles.append(row['angle'])

    phis = [0.0] * len(chain)
    phis[0] = root_sweep
    # 正负号按「**真正参与折叠的行**的序号」交替，而不是按行号。
    # 角度为 0 的行根本不折，不该占掉一个正负号 —— 否则会折出两种坏形状：
    #   · [150, 0, 150]（中间那节不折）：按行号两行都是正号 → 手臂卷成 300° 的
    #     螺旋，收起反而更大（实测展开 3.79 → 收起 4.15，109%）；按折叠序号
    #     就是一正一负的 Z 形。
    #   · 自动分配折叠角时挑到「第 1 行 + 第 3 行」这类组合也一样（它本来靠
    #     「两个折点必须隔奇数行」这条约束绕开这个 bug，现在不需要了）。
    # 没有 0 行时（最常见的情况：每行都折，或者折的是相邻两行）序号与行号一致，
    # 行为与以前完全一样。
    folded = 0
    for gi, angle in enumerate(angles):
        targets = [i for i, g in enumerate(groups) if g == gi and i != 0]
        if not targets:
            continue
        sign = -1.0 if (zigzag and folded % 2 == 1) else 1.0
        per = angle * sign / float(len(targets))
        for i in targets:
            phis[i] = per
        if abs(angle) > 1e-9:
            folded += 1
    return chain, phis, None


def dist_to_bone_chains(point, chains):
    """点到一组骨链的最近距离（按**骨段**算，不是按关节原点算）

    为什么要按骨段：手臂一共只有 4~6 个关节，手臂网格中段离最近那个关节原点
    可能有半米远；而羽毛骨骼又密又多，于是「离最近骨骼」比出来手臂网格的顶点
    反而「更贴羽毛」—— 实测 6 节手臂场景里手臂网格 52 根影响骨骼被判成羽毛卡，
    自检报它的权重是 0.000。按骨段算就对了：手臂网格中段离肱骨那一段只有网格
    厚度那么点距离。
    """
    best = 1e18
    for pts in chains:
        if not pts:
            continue
        if len(pts) == 1:
            best = min(best, (point - pts[0]).length())
            continue
        for k in range(len(pts) - 1):
            a, b = pts[k], pts[k + 1]
            ab = b - a
            denom = ab * ab
            t = 0.0 if denom < 1e-12 else max(0.0, min(1.0, ((point - a) * ab) / denom))
            best = min(best, (point - (a + ab * t)).length())
    return best


def arm_body_chains(info):
    """手臂链的世界坐标点（整条链一串），用来判断某块几何是不是「手臂/身体」

    「手臂有哪些骨骼」= 本次生成涉及的全部骨骼（info['joints']）里**除羽毛之外**
    的那些。以前是从手臂根骨骼用 get_longest_chain 往下走，这是错的：羽毛就是
    挂在手臂骨骼下面的，往下走会拐进羽毛自己那 3 节关节里 —— 实测 4 节手臂被
    走成 6 节「手臂链」，末尾 3 节其实是某根羽毛的骨头（primary06）。
    后果很实在：离那根羽毛近的顶点，算出来「离手臂链」的距离等于「离羽毛链」的
    距离，于是「贴着手臂的顶点别动」那道护栏把它们连同整张卡一起跳过不改 ——
    实测 primary_mesh04/05 共 5 个顶点因此留在了相邻羽毛的骨头上，收起时被剪开。
    """
    keys = set((info.get('offsets') or {}).keys())
    if not keys:
        return []
    # 羽毛自己的骨骼 = 各根羽毛的根骨骼及其所有下级
    feather = set()
    for e in (info.get('extras') or []):
        r = resolve_joint(short_name(e.get('root')))
        if r is None or r in feather:
            continue
        stack = [r]
        while stack:
            b = stack.pop()
            if b in feather or not cmds.objExists(b):
                continue
            feather.add(b)
            stack.extend(child_joints(b))
    left = set()
    for b in list(info.get('joints') or []) + list(keys):
        b = resolve_joint(short_name(b))
        if b and b not in feather:
            left.add(b)
    if not left:
        return []
    # 按层级把这堆手臂骨骼排成「从根到梢」的几条链（有拇指那种分支时不止一条）
    out = []
    while left:
        root = None
        for b in sorted(left):
            if get_parent(b) not in left:
                root = b
                break
        if root is None:
            root = sorted(left)[0]
        chain = [root]
        left.discard(root)
        while True:
            nxt = None
            for c in child_joints(root):
                if c in left:
                    nxt = c
                    break
            if nxt is None:
                break
            chain.append(nxt)
            left.discard(nxt)
            root = nxt
        out.append([om.MVector(*world_pos(b)) for b in chain])
    return out


# ============================================================ 主窗口
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except Exception:
            pass
        super(Window, self).__init__(parent)

        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('鸟翅膀绑定(Maya' + str(self.maya_version) + ')')
        self.setFixedWidth(620)

        # 已生成的绑定：ctrl 长名 -> {'joints': [...], 'rest_rotate': {...}}
        self.rigs = {}
        # 当前预览的控制器
        self.current_ctrl = None

        self.create_widgets()
        self.create_layouts()
        self.create_connect()

    # -------------------------------------------------------- 控件
    def create_widgets(self):
        # ---- 手臂骨骼链 ----
        self.table_arm = self._make_table(['#', '根骨骼', '手臂骨骼', '折叠角(°)'],
                                          [34, 0, 0, 80], 92)
        self.button_arm_root = QtWidgets.QPushButton('加载根骨骼')
        self.button_arm_tip = QtWidgets.QPushButton('加载手臂骨骼')
        self.button_arm_chain = QtWidgets.QPushButton('读取选中链')
        self.button_arm_up = QtWidgets.QPushButton('上移')
        self.button_arm_down = QtWidgets.QPushButton('下移')
        self.button_arm_del = QtWidgets.QPushButton('删除')
        self.button_arm_clear = QtWidgets.QPushButton('清空')
        self.label_arm_hint = QtWidgets.QLabel(
            '选中这一节手臂的骨骼再点「读取选中链」（选择顺序不限，按层级自动排）')
        self.button_arm_chain.setToolTip(
            '把选中的骨骼按**层级**从根排到梢，相邻两根记成一节：\n'
            '  上臂 → 前臂  记成第 1 节\n'
            '  前臂 → 掌骨  记成第 2 节\n'
            '所以先点哪根、后点哪根都行（在大纲里框选也可以）。\n'
            '节内夹着的中间骨骼（例如前臂的 A/B 辅助骨）会自动按层级补全。\n'
            '重复点不会加重复行。')

        # ---- 羽毛（重点）----
        self.table_feather = self._make_table(['#', '羽毛根骨骼', '对应手臂骨骼', '额外角(°)'],
                                              [34, 0, 0, 80], 148)
        self.button_feather_root = QtWidgets.QPushButton('加载羽毛根骨骼')
        self.button_feather_arm = QtWidgets.QPushButton('加载对应手臂骨骼')
        self.button_feather_chain = QtWidgets.QPushButton('读取选中链')
        self.button_feather_auto = QtWidgets.QPushButton('自动匹配手臂骨骼')
        self.button_feather_up = QtWidgets.QPushButton('上移')
        self.button_feather_down = QtWidgets.QPushButton('下移')
        self.button_feather_sort = QtWidgets.QPushButton('按翼展排序')
        self.button_feather_del = QtWidgets.QPushButton('删除')
        self.button_feather_clear = QtWidgets.QPushButton('清空')
        self.label_feather_hint = QtWidgets.QLabel(
            '选中羽毛根骨骼后点「加载羽毛根骨骼」，再点「自动匹配」挂到最近的手臂骨骼')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        # ---- 收起参数 ----
        self.label_axis = QtWidgets.QLabel('折叠轴:')
        self.combo_axis = QtWidgets.QComboBox()
        self.combo_axis.addItems(['自动(翼面法线)', '世界 X', '世界 Y', '世界 Z', '自定义'])
        self.line_axis = QtWidgets.QLineEdit('0,0,1')
        self.line_axis.setFixedWidth(90)
        self.line_axis.setEnabled(False)

        self.label_dir = QtWidgets.QLabel('手臂折叠方向:')
        self.combo_dir = QtWidgets.QComboBox()
        self.combo_dir.addItems(['自动收拢', '正向', '反向'])

        self.label_mode = QtWidgets.QLabel('折叠模式:')
        self.combo_fold_mode = QtWidgets.QComboBox()
        self.combo_fold_mode.addItems([MODE_Z, MODE_CURL])

        self.label_angle = QtWidgets.QLabel('每节折叠角:')
        self.spin_angle = QtWidgets.QDoubleSpinBox()
        self.spin_angle.setRange(0.0, 180.0)
        self.spin_angle.setValue(DEFAULT_FOLD_ANGLE)
        self.spin_angle.setSingleStep(5.0)
        self.spin_angle.setDecimals(1)
        self.spin_angle.setSuffix('°')
        self.button_apply_angle = QtWidgets.QPushButton('应用到全部')
        self.button_apply_angle.setToolTip(
            '把「每节折叠角」这个数填到手臂表的每一行。\n\n'
            '注意**整列都是同一个数**时，点「生成翅膀绑定」会让插件自己挑「该折哪几行」\n'
            '（和「一键生成」一样）—— 行数一多，每行都折就是一条来回折的手风琴，\n'
            '收起来是一坨而不是「细长一片」。\n'
            '想完全按自己写的折：逐行填**不同的**值，不要整列一个数；\n'
            '不想折的行填 0。')
        self.button_auto_angle = QtWidgets.QPushButton('自动分配折叠角')
        self.button_auto_angle.setToolTip(
            '挑出「该折的那几行」，只在那几行填折叠角，其余行填 0。\n'
            '为什么需要：Z 形对折是逐行交替正负号的。手臂节数一多，还按「每行都填\n'
            '170°」去折，累积起来就是一条来回折的锯齿（5 行 = 折 5 次的手风琴），\n'
            '不是真实鸟翼的「肘 + 腕两个折点」——羽毛全挂在这条手臂上，折点一多\n'
            '整个羽包就被折成一坨厚厚的锯齿，收起效果会很差。\n'
            '插件会把每种折点组合都估一遍「收起后翅膀伸出多远」，取最短的那个；\n'
            '「每行都折」也在候选里，所以最坏不会比手工按「应用到全部」差。\n\n'
            '（手臂表整列都是同一个数时，「生成翅膀绑定」会自己跑一遍这个分配，\n'
            '不用先手动点这个按钮。）')

        self.label_ease = QtWidgets.QLabel('羽毛收拢进度:')
        self.spin_ease = QtWidgets.QDoubleSpinBox()
        self.spin_ease.setRange(0.3, 1.6)
        self.spin_ease.setValue(FEATHER_EASE)
        self.spin_ease.setSingleStep(0.05)
        self.spin_ease.setDecimals(2)
        self.spin_ease.setToolTip(
            '羽毛转过的角度 = 总收拢角 × (收起程度 ** 这个指数)。\n'
            '  = 1.00 跟手臂同步收；< 1 羽毛先收、手臂后折（默认 0.45）；> 1 手臂先折、羽毛后收。\n\n'
            '默认 0.45 是拿渲图定下来的：\n'
            '  1.00 时收起 40% 羽毛还是一根根分开立着的「耙子」、手臂整段光杆露在外面，\n'
            '       收起途中翅膀的投影面积还会先胀大 10%~17%；\n'
            '  0.45 时羽毛已经互相搭上、把手臂盖住，是一整坨收起来的翅膀。\n'
            '另外两个相机无关的量也都支持 0.45：手臂到羽毛的距离（越小越盖得住）\n'
            '0.73 → 0.59，收起 10% 时的半径（越小越跟手）99% → 79%。\n\n'
            '往 1.00 调：羽毛又短又密、展开姿态本来就互相糊在一起的模型，晚收一点更贴。\n'
            '往 0.30 调：羽毛特别长、想让它们更早贴到手臂上。')

        self.label_feather_sweep = QtWidgets.QLabel('羽毛收拢量:')
        self.spin_feather_sweep = QtWidgets.QDoubleSpinBox()
        self.spin_feather_sweep.setRange(0.0, 200.0)
        self.spin_feather_sweep.setValue(100.0)
        self.spin_feather_sweep.setSingleStep(5.0)
        self.spin_feather_sweep.setDecimals(0)
        self.spin_feather_sweep.setSuffix('%')

        self.label_feather_dir = QtWidgets.QLabel('羽毛贴拢方向:')
        self.combo_feather_dir = QtWidgets.QComboBox()
        self.combo_feather_dir.addItems([DIR_AUTO, DIR_FLIP])

        self.label_fan = QtWidgets.QLabel('扇形微张:')
        self.spin_fan = QtWidgets.QDoubleSpinBox()
        self.spin_fan.setRange(0.0, 90.0)
        self.spin_fan.setValue(DEFAULT_FAN)
        self.spin_fan.setSingleStep(2.0)
        self.spin_fan.setDecimals(1)
        self.spin_fan.setSuffix('°')
        self.spin_fan.setToolTip(
            '收起后各羽毛之间的夹角，从翼根到翼尖递增（像合拢的折扇）。默认 4°。\n\n'
            '层叠改成「沿翼面法线平移」之后，这个角是**唯一**让收起后的羽毛互不平行\n'
            '的东西（以前「层叠错开」也会让它们差 9~10°，所以那时填 24° 只多散 5°）。\n\n'
            '往大调主要是**代价**（三个场景扫 0/4/8/12/16/24°；这批数是在旧层叠下量的，\n'
            '方向仍然成立）：\n'
            '  中心线相交对数 0/5/15/30/33/48（真翼形 38 根）、0/3/5/6/7/8（23 根）、\n'
            '  0/6/9/24/33/53（形状 38 根）；\n'
            '  手臂到最近羽毛的距离（越小盖得越好）0.35→0.61 / 0.11→0.20 / 0.30→0.48；\n'
            '  而收起后的尺寸、分层间隔、厚度几乎不动（21.1%→19.3% 之类，就两三个点）。\n'
            '所以默认留 4°：留住一点点扇形层次，代价可以忽略。\n'
            '想让羽毛收得更贴、更平行就往 0 调；想让层次更明显再往上加，代价就是上面的相交与裸露。')

        self.label_stack = QtWidgets.QLabel('层叠厚度:')
        self.spin_stack = QtWidgets.QDoubleSpinBox()
        self.spin_stack.setRange(-60.0, 60.0)
        self.spin_stack.setValue(DEFAULT_STACK)
        self.spin_stack.setSingleStep(1.0)
        self.spin_stack.setDecimals(0)
        self.spin_stack.setSuffix('%')
        self.spin_stack.setToolTip(
            '收起后整叠羽毛的**厚度**，占中位羽毛长的百分比，默认 17%。\n'
            '按羽毛长度分配层号：短覆羽在最外面一层、长飞羽最贴翼面，收起时一层压一层。\n'
            '取负值把里外两层对调，0 表示所有羽毛收进同一个平面（会糊成一片）。\n\n'
            '这里是「沿翼面法线平移」而不是「把羽毛翘出翼面」——平移时两根羽毛始终\n'
            '平行、深度差沿整条羽毛恒定，收起过程中永远不会出现「两根共面切进去」的\n'
            '瞬间（翘出翼面做不到：转过不同角度后两根不再平行，深度差沿长度线性变化、\n'
            '必然经过 0，而它们的交叉点又在动）。\n\n'
            '调大 = 层与层分得更开、看得更清楚，代价是整叠更厚、羽毛整体离手臂更远\n'
            '（38 根实测：整叠 0%→30% 时「手臂到最近羽毛的平均距离」0.77→1.27）；\n'
            '调小 = 更薄更贴身，但相邻两层深度差变小，低于整叠 12% 左右又会糊成一片。\n'
            '根数特别多（>80）的模型相邻两层会被压得太近，往上调一点。')

        self.chk_parent = QtWidgets.QCheckBox('羽毛根骨骼自动挂到对应手臂骨骼下')
        self.chk_parent.setChecked(True)
        self.label_root_sweep = QtWidgets.QLabel('根部后掠角:')
        self.spin_root_sweep = QtWidgets.QDoubleSpinBox()
        self.spin_root_sweep.setRange(-180.0, 180.0)
        self.spin_root_sweep.setValue(0.0)
        self.spin_root_sweep.setSingleStep(5.0)
        self.spin_root_sweep.setDecimals(1)
        self.spin_root_sweep.setSuffix('°')
        self.spin_root_sweep.setToolTip(
            '收起时根关节绕翼面法线多转的角度（＝转肩）。\n'
            '勾着右边的「自动」时这个数不生效，插件会自己算（推荐）；\n'
            '取消勾选就用这里手填的值。')
        self.chk_root_sweep_auto = QtWidgets.QCheckBox('自动')
        self.chk_root_sweep_auto.setChecked(True)
        self.chk_root_sweep_auto.setToolTip(
            '收起时自动把整只翅膀转到「顺着身体」的方向，而不是继续朝翼尖那一侧伸着。\n\n'
            '为什么需要：Z 形对折只把手臂折回来，**没有转肩**。收到底以后整叠羽毛的\n'
            '长轴仍然沿着原来的翼展方向，翼包从肩部往翼尖那一侧还伸出好大一截\n'
            '（实测真翼形：0.221 × 翼展）；真实鸟翼收起时是贴身体前后方向收着的。\n\n'
            '转多少不需要填：鸟的弦向（前缘→后缘）就是体轴的前后方向，而羽毛就长在\n'
            '后缘那一侧，所以「羽毛在翼面内偏向的那一侧」就是「后方」。插件把收好后\n'
            '羽毛的朝向转到这个「后方」上，得到的角度就是该转的量。\n'
            '实测（真翼形 38 根，收起到底，外伸量是相对翼展）：\n'
            '  后掠 0°   外伸 0.221、细长比 3.9\n'
            '  后掠 90°  外伸 0.000~0.062、紧凑度与穿插照旧全过\n'
            '  后掠 120° 外伸 0.117，而且羽毛穿插开始真的切进去 —— 别超过 90° 附近\n\n'
            '取消勾选就用手填的那个角度（想自己微调用）。')

        self.label_samples = QtWidgets.QLabel('过渡采样:')
        self.spin_samples = QtWidgets.QSpinBox()
        self.spin_samples.setRange(2, 32)
        self.spin_samples.setValue(DEFAULT_SAMPLES)
        self.spin_samples.setToolTip(
            '收起 0~100% 之间采多少个姿态点、写进驱动关键帧。\n'
            '采样太稀，中间帧靠欧拉插值补，收起过程会出现「先弹出去一下」的回弹：\n'
            '实测 6 点时中途半径回升 0.42（约 23%%），12 点时降到 0.15 且大回弹消失。')

        self.label_yaw = QtWidgets.QLabel('朝向偏转:')
        self.spin_yaw = QtWidgets.QDoubleSpinBox()
        self.spin_yaw.setRange(-180.0, 180.0)
        self.spin_yaw.setValue(DEFAULT_YAW)
        self.spin_yaw.setSingleStep(5.0)
        self.spin_yaw.setDecimals(1)
        self.spin_yaw.setSuffix('°')
        self.spin_yaw.setToolTip(
            '所有羽毛一起绕翼面法线多转的角度（批量调整朝向）。\n'
            '正的往一侧偏、负的往另一侧偏；单根要微调就点「全选羽毛控制器」\n'
            '之后逐个转，或者只选中要改的那几个转。')

        self.splitter_2 = QtWidgets.QSplitter()
        self.splitter_2.setFixedHeight(1)
        self.splitter_2.setFrameStyle(1)

        # ---- 生成与预览 ----
        self.button_oneclick = QtWidgets.QPushButton('一键生成（选中手臂 + 所有羽毛）')
        self.button_oneclick.setToolTip(
            '最省事的用法：\n'
            '  1. 在视口/大纲里把「这一节手臂的骨骼」和「所有羽毛的根骨骼」一起选中\n'
            '     （整根羽毛的骨骼都选上也行，子骨骼会自动忽略）\n'
            '  2. 点这个按钮\n'
            '插件会自动认出哪条是手臂链、哪些是羽毛，填好两张表、排好序、\n'
            '自动匹配手臂骨骼，然后直接生成。不用管先点哪个按钮。\n'
            '想改「每节折叠角」「收起参数」就改了再点。')
        self.button_build = QtWidgets.QPushButton('生成翅膀绑定')
        self.button_build.setToolTip(
            '按 ①② 两张表把骨骼加载好之后点这里。\n'
            '生成后：羽毛会挂到对应手臂骨骼下，每根羽毛带一条驱动样条，\n'
            '样条的驱动源就是对应手臂关节的旋转——之后直接转手臂关节，羽毛会自动跟上。')
        self.button_ctrls = QtWidgets.QPushButton('全选羽毛控制器')
        self.button_ctrls.setToolTip(
            '一键选中所有羽毛的朝向控制器（圆环）。\n'
            '选中后用旋转工具转，就能批量调整所有羽毛的朝向。')
        self.button_del_rig = QtWidgets.QPushButton('删除绑定')
        self.combo_rig = QtWidgets.QComboBox()
        self.chk_weights = QtWidgets.QCheckBox('生成时刷羽毛权重=1')
        self.chk_weights.setChecked(True)
        self.chk_weights.setToolTip(
            '生成完顺手把羽毛卡的权重刷成刚性（每张卡只跟一根羽毛、权重 1），'
            '不用再单独点一次「羽毛权重=1」。\n\n'
            '为什么要默认做：你自己的蒙皮权重往往是把每张卡的顶点各自绑到「离它最近的'
            '那根骨骼」上，而在密集羽毛里相邻两条骨链挨得比卡片自己的半宽还近 ——'
            '实测一张卡的顶点会散到 3~7 根羽毛上，收起时同一张卡被几根羽毛往不同方向'
            '拽、边长被拉坏：真翼形 38 张卡收起到底边长最大变 **27%**。'
            '整卡一根链之后是 0.7%。\n\n'
            '只动「几何上属于羽毛」的顶点（离羽毛骨骼比离手臂骨骼更近的那些），'
            '手臂网格一根都不碰。刷权重是生成之后的**独立一步**，'
            '一次 Ctrl+Z 撤回这一步、再按一次撤回生成。\n'
            '不想让插件碰你的权重就取消勾选，之后手动点「羽毛权重=1」也一样。')
        self.chk_helpers = QtWidgets.QCheckBox('显示辅助物')
        # 驱动样条 / 定位器是内部解算用的中间物，生成时就藏起来了。
        # 需要调样条、查约束时勾上这一个开关，不用去大纲里一个个找。
        self.chk_helpers.setToolTip(
            '显示/隐藏内部解算用的「驱动样条 + 定位器」。\n'
            '它们是羽毛贴合用的中间物（用户实际动的是圆环控制器和末端方块），\n'
            '44 根羽毛有 44 条曲线 + 132 个定位器，默认藏起来视口才看得清翅膀。')
        self.button_check = QtWidgets.QPushButton('自检')
        self.button_check.setToolTip(
            '生成完之后点一下，直接把「这套绑定行不行」的关键指标算出来：\n'
            '  静止姿态还原 / 骨骼零形变 / 收起紧凑度 / 垂直基线守恒 /\n'
            '  FK 控制器能驱动骨骼 / 羽毛权重归属 / 控制器齐全 / 羽毛贴合样条 /\n'
            '  驱动关键帧齐全 / 羽毛穿插合理\n'
            '哪一环没达标会标出来，方便对着数值找问题，不用凭感觉判断效果。')
        self.button_weights = QtWidgets.QPushButton('羽毛权重=1')
        self.button_weights.setToolTip(
            '把羽毛的权重刷成刚性：每个顶点权重 1、落在离它最近的那根羽毛骨骼上。\n'
            '这是「羽毛对应的骨骼权重就是1」那条要求的做法，作用是让羽毛卡刚性\n'
            '跟着自己那根羽毛走，不被手臂或旁边的羽毛拽着变形。\n'
            '（对「收起有多紧」影响不大：实测三个场景 65.4→57.2% / 44.0→43.2% /\n'
            ' 45.2→49.4%，稀疏模型有改善，密集模型基本持平。）\n'
            '只动羽毛网格、且只动「离羽毛骨骼比离手臂骨骼更近」的顶点。\n'
            '一次 Ctrl+Z 可撤回。')

        self.label_fold = QtWidgets.QLabel('收起程度:')
        self.slider_fold = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_fold.setMinimum(0)
        self.slider_fold.setMaximum(100)
        self.slider_fold.setValue(0)
        self.spin_fold = QtWidgets.QSpinBox()
        self.spin_fold.setRange(0, 100)
        self.spin_fold.setSuffix('%')
        self.button_open = QtWidgets.QPushButton('展开')
        self.button_close = QtWidgets.QPushButton('收起')

        self.label_info = QtWidgets.QLabel('')

    def _make_table(self, headers, widths, height):
        table = QtWidgets.QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked |
                              QtWidgets.QAbstractItemView.SelectedClicked)
        table.setFixedHeight(height)
        header = table.horizontalHeader()
        for i, w in enumerate(widths):
            header.setSectionResizeMode(
                i, QtWidgets.QHeaderView.Fixed if w else QtWidgets.QHeaderView.Stretch)
            if w:
                table.setColumnWidth(i, w)
        return table

    # -------------------------------------------------------- 布局
    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(6)

        main_layout.addWidget(self.button_oneclick)
        main_layout.addWidget(QtWidgets.QLabel('① 手臂骨骼（按顺序加载每节的根骨骼与手臂骨骼）:'))
        main_layout.addWidget(self.table_arm)
        main_layout.addLayout(self._row(self.button_arm_root, self.button_arm_tip,
                                        self.button_arm_chain))
        main_layout.addLayout(self._row(self.button_arm_up, self.button_arm_down,
                                        self.button_arm_del, self.button_arm_clear))
        main_layout.addWidget(self.label_arm_hint)

        main_layout.addWidget(QtWidgets.QLabel('② 羽毛（按顺序加载羽毛根骨骼与其对应的手臂骨骼）:'))
        main_layout.addWidget(self.table_feather)
        main_layout.addLayout(self._row(self.button_feather_root, self.button_feather_arm,
                                        self.button_feather_chain))
        main_layout.addLayout(self._row(self.button_feather_auto, self.button_feather_up,
                                        self.button_feather_down, self.button_feather_sort,
                                        self.button_feather_del, self.button_feather_clear))
        main_layout.addWidget(self.label_feather_hint)

        main_layout.addWidget(self.splitter_1)

        main_layout.addLayout(self._row(self.label_axis, self.combo_axis, self.line_axis))
        main_layout.addLayout(self._row(self.label_dir, self.combo_dir, self.label_mode,
                                        self.combo_fold_mode))
        main_layout.addLayout(self._row(self.label_angle, self.spin_angle,
                                        self.button_apply_angle,
                                        self.button_auto_angle, self.label_root_sweep,
                                        self.spin_root_sweep,
                                        self.chk_root_sweep_auto))
        main_layout.addLayout(self._row(self.label_feather_sweep, self.spin_feather_sweep,
                                        self.label_ease, self.spin_ease,
                                        self.label_feather_dir, self.combo_feather_dir))
        main_layout.addLayout(self._row(self.label_fan, self.spin_fan,
                                        self.label_stack, self.spin_stack,
                                        self.chk_parent))
        main_layout.addLayout(self._row(self.label_yaw, self.spin_yaw,
                                        self.button_ctrls, self.label_samples,
                                        self.spin_samples, self.button_weights))

        main_layout.addWidget(self.splitter_2)

        main_layout.addLayout(self._row(self.button_build, self.combo_rig,
                                        self.button_check, self.button_del_rig,
                                        self.chk_helpers, self.chk_weights))
        # 收起程度这一行不放弹簧，让滑块撑满，方便精细拖动
        fold_row = QtWidgets.QHBoxLayout()
        for w in (self.label_fold, self.slider_fold, self.spin_fold,
                  self.button_open, self.button_close):
            fold_row.addWidget(w)
        main_layout.addLayout(fold_row)
        main_layout.addWidget(self.label_info)
        main_layout.addStretch(1)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        # 内容自然高度约 950px：在 1080p 以下的屏（笔记本 900px，或者 Maya 自身 UI
        # 占掉一截）上，最下面那排按钮 ——「生成翅膀绑定 / 自检 / 展开 / 收起」——
        # 会被挤出可视区，用户看到的就是「按钮不见了、功能不全」。
        # 套一层滚动区：屏幕够高时完全看不出区别，不够高时出现滚动条，按钮永远够得着。
        area = QtWidgets.QScrollArea()
        area.setWidgetResizable(True)
        area.setFrameShape(QtWidgets.QFrame.NoFrame)
        area.setWidget(widget)
        self.setCentralWidget(area)
        # 开窗时别顶到屏幕外：高度限制到可用屏幕高度的 90%
        try:
            avail = QtWidgets.QApplication.primaryScreen().availableGeometry()
            want = min(main_layout.sizeHint().height() + 16,
                       int(avail.height() * 0.9))
            self.resize(self.width(), max(320, want))
        except Exception:
            pass
        self.restore_rigs()

    def restore_rigs(self):
        """扫描场景里已有的翅膀控制器，把登记表还原回来

        绑定是跟着文件走的：存盘、重开之后 Python 内存里什么都没有。
        控制器上存着登记表（见 RIG_DATA_ATTR），这里读回来，
        于是「下拉里能列出来 / 能删掉 / 重新生成不会叠第二套」都恢复正常。
        """
        for ctrl in cmds.ls(CTRL_NAME + '*', type='transform') or []:
            if not cmds.attributeQuery(FOLD_ATTR, n=ctrl, ex=True):
                continue
            if not cmds.attributeQuery(RIG_DATA_ATTR, n=ctrl, ex=True):
                continue
            info = unpack_rig_data(cmds.getAttr(ctrl + '.' + RIG_DATA_ATTR))
            if info:
                self.rigs[ctrl] = info
        if self.rigs:
            self.refresh_rig_combo(sorted(self.rigs)[0])
            self.current_ctrl = self.combo_rig.currentText()
            self.sync_fold_from_ctrl()
            print('[翅膀绑定] 发现 %d 套已有绑定：%s'
                  % (len(self.rigs), ', '.join(sorted(self.rigs))))
            # 文件里可能存着「辅助物体是显示状态」（旧版本生成的绑定），
            # 开窗时按当前开关收一下，视口保持干净
            self.set_helpers_visible(self.chk_helpers.isChecked())

    @staticmethod
    def _row(*widgets):
        layout = QtWidgets.QHBoxLayout()
        for w in widgets:
            layout.addWidget(w)
        layout.addStretch(1)
        return layout

    # -------------------------------------------------------- 信号
    def create_connect(self):
        self.button_arm_root.clicked.connect(self.arm_add_root)
        self.button_arm_tip.clicked.connect(self.arm_add_tip)
        self.button_arm_chain.clicked.connect(self.arm_read_selection)
        self.button_arm_up.clicked.connect(lambda: self.arm_move(-1))
        self.button_arm_down.clicked.connect(lambda: self.arm_move(1))
        self.button_arm_del.clicked.connect(lambda: self.delete_rows(self.table_arm))
        self.button_arm_clear.clicked.connect(lambda: self.clear_rows(self.table_arm))

        self.button_feather_root.clicked.connect(self.feather_add_root)
        self.button_feather_arm.clicked.connect(self.feather_add_arm)
        self.button_feather_chain.clicked.connect(self.feather_read_selection)
        self.button_feather_auto.clicked.connect(self.feather_auto_match)
        self.button_feather_up.clicked.connect(lambda: self.move_feather(-1))
        self.button_feather_down.clicked.connect(lambda: self.move_feather(1))
        self.button_feather_sort.clicked.connect(self.feather_sort)
        self.button_feather_del.clicked.connect(lambda: self.delete_rows(self.table_feather))
        self.button_feather_clear.clicked.connect(lambda: self.clear_rows(self.table_feather))

        self.button_apply_angle.clicked.connect(self.apply_angle_to_all)
        self.button_auto_angle.clicked.connect(self.auto_fold_angles)
        # 「根部后掠角」的自动 / 手动是一对：勾着自动时手填框置灰，用户一旦动手填就
        # 自动取消勾选。不这么做的话，勾着自动时手填的数字会被**静默忽略** ——
        # 用户填了 40° 却什么也没发生（验收就抓到过这个：整只翅膀转了 0.0°）。
        self.chk_root_sweep_auto.toggled.connect(
            lambda on: self.spin_root_sweep.setEnabled(not on))
        self.spin_root_sweep.setEnabled(
            not self.chk_root_sweep_auto.isChecked())
        self.spin_root_sweep.valueChanged.connect(
            lambda _v: self.chk_root_sweep_auto.setChecked(False))
        self.combo_axis.currentIndexChanged.connect(
            lambda i: self.line_axis.setEnabled(i == 4))
        self.combo_fold_mode.currentIndexChanged.connect(self.on_mode_changed)
        self.button_oneclick.clicked.connect(self.one_click)
        self.button_build.clicked.connect(self.build_rig)
        self.button_ctrls.clicked.connect(self.select_feather_ctrls)
        self.button_del_rig.clicked.connect(self.delete_rig)
        self.combo_rig.currentIndexChanged.connect(self.on_rig_changed)
        self.chk_helpers.toggled.connect(self.on_helpers_toggled)
        self.button_check.clicked.connect(self.on_self_check)
        self.button_weights.clicked.connect(self.on_normalize_weights)
        self.slider_fold.valueChanged.connect(self.on_fold_slider)
        self.spin_fold.valueChanged.connect(self.on_fold_spin)
        self.button_open.clicked.connect(lambda: self.set_fold(0))
        self.button_close.clicked.connect(lambda: self.set_fold(100))

    # -------------------------------------------------------- 表格读写
    def read_rows(self, table):
        """读表格 -> [{'root':..,'arm':..,'angle':..}]（第 4 列可以是折叠角或额外角）"""
        rows = []
        for r in range(table.rowCount()):
            def cell(c):
                item = table.item(r, c)
                return item.text().strip() if item else ''
            try:
                angle = float(cell(3))
            except ValueError:
                angle = 0.0
            rows.append({'root': cell(1), 'arm': cell(2), 'angle': angle})
        return rows

    def write_rows(self, table, rows):
        table.setRowCount(0)
        for row in rows:
            self.append_row(table, row.get('root', ''), row.get('arm', ''),
                            row.get('angle', 0.0))
        self.refresh_index(table)

    def append_row(self, table, root, arm, angle):
        r = table.rowCount()
        table.insertRow(r)
        table.setItem(r, 0, QtWidgets.QTableWidgetItem(''))
        table.setItem(r, 1, QtWidgets.QTableWidgetItem(str(root)))
        table.setItem(r, 2, QtWidgets.QTableWidgetItem(str(arm)))
        table.setItem(r, 3, QtWidgets.QTableWidgetItem('%.1f' % angle))
        return r

    def refresh_index(self, table):
        for r in range(table.rowCount()):
            item = table.item(r, 0)
            if item is None:
                item = QtWidgets.QTableWidgetItem('')
                table.setItem(r, 0, item)
            item.setText(str(r + 1))
            item.setFlags(QtCore.Qt.ItemIsEnabled)

    def selected_rows(self, table):
        return sorted(set(idx.row() for idx in table.selectedIndexes()))

    def has_row(self, table, root, arm=None):
        """表格里是否已经有这一节 / 这根羽毛（避免重复点加载按钮时灌进重复行）"""
        for row in self.read_rows(table):
            if row['root'] != root:
                continue
            if arm is None or row['arm'] == arm:
                return True
        return False

    def move_rows(self, table, step):
        rows = self.read_rows(table)
        if not rows:
            return
        targets = self.selected_rows(table)
        if not targets:
            return
        if step < 0:
            targets = [r for r in targets if r > 0]
            for r in targets:
                rows[r - 1], rows[r] = rows[r], rows[r - 1]
        else:
            targets = [r for r in reversed(targets) if r < len(rows) - 1]
            for r in targets:
                rows[r + 1], rows[r] = rows[r], rows[r + 1]
        self.write_rows(table, rows)
        for r in targets:
            table.selectRow(r + step)

    def delete_rows(self, table):
        rows = self.read_rows(table)
        for r in reversed(self.selected_rows(table)):
            if 0 <= r < len(rows):
                rows.pop(r)
        self.write_rows(table, rows)

    def clear_rows(self, table):
        self.write_rows(table, [])

    # -------------------------------------------------------- 手臂骨骼
    def arm_add_root(self):
        sel = cmds.ls(sl=True, type='joint', long=True) or []
        if not sel:
            cmds.warning('请先选中骨骼')
            return
        added = 0
        for j in sel:
            name = short_name(j)
            if self.has_row(self.table_arm, name):
                continue
            self.append_row(self.table_arm, name, '', self.spin_angle.value())
            added += 1
        self.refresh_index(self.table_arm)
        print('[翅膀绑定] 已加载 %d 节手臂根骨骼%s'
              % (added, '' if added else '（都已在表里，没有重复添加）'))

    def arm_add_tip(self):
        sel = cmds.ls(sl=True, type='joint', long=True) or []
        if not sel:
            cmds.warning('请先选中骨骼')
            return
        if self.table_arm.rowCount() == 0:
            cmds.warning('请先用「加载根骨骼」创建一节手臂')
            return
        rows = self.selected_rows(self.table_arm)
        row = rows[0] if rows else self.table_arm.rowCount() - 1
        self.table_arm.setItem(row, 2, QtWidgets.QTableWidgetItem(short_name(sel[0])))
        print('[翅膀绑定] 第 %d 节手臂骨骼: %s' % (row + 1, short_name(sel[0])))

    def arm_read_selection(self):
        """把选中的骨骼读成手臂节表

        顺序不用管：按层级从根排到梢，相邻两根成节（节内夹着的中间骨骼
        会在生成时按层级自动补全，见 build_arm_chain）。
        """
        cmds.selectPref(trackSelectionOrder=True)
        sel = cmds.ls(sl=True, type='joint', long=True) or []
        if len(sel) < 2:
            cmds.warning('请至少选中 2 根骨骼（一节手臂的根骨骼与手臂骨骼）')
            return
        order, why = selected_chain(sel)
        if not order:
            cmds.warning(why)
            return
        rows = self.read_rows(self.table_arm)
        added = 0
        for i in range(len(order) - 1):
            root, tip = short_name(order[i]), short_name(order[i + 1])
            if self.has_row(self.table_arm, root, tip):
                continue
            rows.append({'root': root, 'arm': tip, 'angle': self.spin_angle.value()})
            added += 1
        self.write_rows(self.table_arm, rows)
        print('[翅膀绑定] 已按层级加载 %d 节手臂（%s）%s'
              % (added, ' → '.join(short_name(j) for j in order),
                 '' if added else '（都已在表里，没有重复添加）'))

    def arm_move(self, step):
        self.move_rows(self.table_arm, step)

    # -------------------------------------------------------- 羽毛骨骼
    def feather_add_root(self):
        """把当前选中的骨骼作为新的羽毛根骨骼，并按选择顺序逐个追加（已有的不重复加）"""
        cmds.selectPref(trackSelectionOrder=True)
        sel = cmds.ls(orderedSelection=True, type='joint', long=True) or []
        if not sel:
            cmds.warning('请先选中羽毛根骨骼')
            return
        rows = self.read_rows(self.table_feather)
        added = 0
        for j in sel:
            name = short_name(j)
            if self.has_row(self.table_feather, name):
                continue
            rows.append({'root': name, 'arm': '', 'angle': 0.0})
            added += 1
        self.write_rows(self.table_feather, rows)
        print('[翅膀绑定] 已加载 %d 根羽毛根骨骼%s'
              % (added, '' if added else '（都已在表里，没有重复添加）'))

    def one_click(self):
        """一键：把选中的骨骼自动分成「手臂链」和「羽毛根骨骼」，然后直接生成

        用户不用先想清楚「哪张表填什么、先点哪个按钮」：
          1. 选中里最长的那条从根到梢的链 = 手臂链，写进表①
             （每一节按当前「每节折叠角」填，Z 形模式会自动交替正负号）
          2. 剩下的骨骼里只保留「在被选中的那部分里最靠上」的那些 = 羽毛根骨骼。
             整根羽毛的骨骼都被选中时，只有羽毛根会被留下，子骨骼自动忽略。
          3. 按翼展方向排序 → 自动匹配「对应手臂骨骼」→ 直接生成

        选中的骨骼里如果**不止一组骨架**（最典型的是左右两只翅膀一起框选），
        会按「没有被选中的父级」拆开、每只翅膀各生成一套绑定，互不干扰。

        选中的骨骼少于两根、或里面找不到手臂链时，给出具体原因，不静默失败。
        """
        cmds.selectPref(trackSelectionOrder=True)
        sel = cmds.ls(sl=True, type='joint', long=True) or []
        if len(sel) < 2:
            cmds.warning('请先选中骨骼：这一节手臂的骨骼 + 所有羽毛的根骨骼一起选中，'
                         '再点「一键生成」')
            return
        # 选中里可能有好几组骨架（最典型的是左右两只翅膀一起框选）。
        # 以前只当成一组处理，另一只翅膀会被当成「一根羽毛」挂到这只翅膀的手臂上
        # （实测：左翼的 humerus 出现在羽毛列表里，37 根「羽毛」、折叠量 850°），
        # 生成出来是一套废绑定，而且一句提示都没有。
        #
        # 找「候选手臂链」：一组骨架要同时满足两条才算「一只翅膀的手臂」——
        #   · 链长 ≥ 75% 最长的一条：羽毛天生比手臂短（实测最长的主飞羽是手臂的
        #     64%），单看长度已经能分开；留 75% 是给左右翅膀长短略有出入留余量
        #   · 这组骨骼数 ≥ 全部选中的 20%：一只手臂（连同挂在它下面的羽毛）在
        #     整个选中里占的份量很大，单根羽毛只占 2%~5%
        # 两条都卡住，才敢把选中拆成几组、各生成一套绑定。单只翅膀（哪怕羽毛
        # 还散在世界根下、各成一组）永远只有 ≤1 条候选，会走同一条老路子。
        groups = []
        for g in selected_groups(sel):
            ch, _why = longest_selected_chain(g)
            if len(ch) >= 2:
                groups.append((chain_length(joint_positions(ch)), len(g), ch))
        cands = []
        if groups:
            top = max(ln for ln, _n, _ch in groups)
            share = 0.2 * len(sel)
            cands = sorted([ch for ln, n, ch in groups
                            if ln >= 0.75 * top and n >= share],
                           key=lambda ch: short_name(ch[0]))
        if len(cands) <= 1:
            ctrl = self.one_click_one(sel)
            made = [ctrl] if ctrl else []
        else:
            # 多只翅膀：按「离哪条候选手臂链最近」把选中的骨骼分给各自的手臂
            arms = [[om.MVector(*world_pos(j)) for j in ch] for ch in cands]
            buckets = [[] for _ in arms]
            for j in sel:
                p = om.MVector(*world_pos(j))
                k = min(range(len(arms)),
                        key=lambda i: dist_to_bone_chains(p, [arms[i]]))
                buckets[k].append(j)
            print('[翅膀绑定] 一键：选中里有 %d 条手臂（如左右两只翅膀），逐条生成'
                  % len(arms))
            made = []
            for b in buckets:
                c = self.one_click_one(b)
                if c:
                    made.append(c)
        if not made:
            return
        if len(made) > 1:
            print('[翅膀绑定] 一键：已各生成一套绑定：%s' % made)
            self.label_info.setText('%s｜一键生成了 %d 套绑定'
                                    % (self.label_info.text(), len(made)))

    def one_click_one(self, joints):
        """一键生成里的「一套翅膀」：写表 → 排序 → 匹配 → 自动分配折叠角 → 生成

        返回生成的控制器名；失败返回 None（并给出具体原因）。
        """
        chain, why = longest_selected_chain(joints)
        if not chain:
            cmds.warning(why)
            return None
        chain_set = set(chain)
        off = [j for j in joints if j not in chain_set]
        off_set = set(off)
        # 只留每条羽毛分支最上面的那一根：整根羽毛（含子骨骼）都被选中时不会重复加
        roots = [j for j in off if get_direct_parent(j) not in off_set]
        if not roots:
            cmds.warning('选中里只有手臂链、没有羽毛根骨骼：请把羽毛的根骨骼也一起选中')
            return None
        # 有些「不在手臂链上的选中骨骼」其实是**另一条手臂**（另一只翅膀的骨架，
        # 或者两只翅膀共用一个父级、拆不开）。两条判据：
        #   · 它下面挂着 ≥2 条够长的末端路径 —— 它有自己的羽毛（羽毛自己是光杆）
        #   · 它往下能延伸 ≥80% 臂长 —— 它自己就是一条完整的手臂
        # 不挑出来的话会被当成一根羽毛挂到手臂上（实测另一只翅膀整条手臂被吃进去，
        # 37 根「羽毛」、折叠量 850°，生成出来是一套废绑定）。
        arm_len = chain_length(joint_positions(chain))
        keep, limbs = [], []
        for j in roots:
            if (count_long_leaf_paths(j, 0.25 * arm_len) >= 2
                    or longest_subtree_len(j) >= 0.8 * arm_len):
                limbs.append(j)
            else:
                keep.append(j)
        if limbs:
            cmds.warning(
                '选中的 %s 下面还挂着自己的羽毛 / 本身就是一条完整的手臂，看起来是'
                '**另一条手臂**而不是一根羽毛，已跳过。左右两只翅膀请分别选中再各点'
                '一次「一键生成」。'
                % '、'.join(short_name(j) for j in limbs[:4]))
        roots = keep
        if not roots:
            cmds.warning('去掉那些「另一条手臂」之后没有羽毛了，请检查选中')
            return None

        self.write_rows(self.table_arm, [
            {'root': short_name(chain[i]), 'arm': short_name(chain[i + 1]),
             'angle': self.spin_angle.value()}
            for i in range(len(chain) - 1)])
        self.write_rows(self.table_feather, [
            {'root': short_name(j), 'arm': '', 'angle': 0.0}
            for j in sorted(roots, key=short_name)])
        self.feather_sort()
        self.feather_auto_match()
        # 折叠角交给「自动分配」挑折点：行数多时（真实鸟翼的手臂常有 5~8 节）
        # 每行都折会变成手风琴，收起来是一坨锯齿。
        self.auto_fold_angles()
        print('[翅膀绑定] 一键：手臂 %d 根（%s），羽毛 %d 根'
              % (len(chain), ' → '.join(short_name(j) for j in chain), len(roots)))
        self.build_rig()
        return self.current_ctrl

    def feather_add_arm(self):
        """把当前选中的骨骼填为选中行的「对应手臂骨骼」"""
        sel = cmds.ls(sl=True, type='joint', long=True) or []
        if not sel:
            cmds.warning('请先选中手臂骨骼')
            return
        targets = self.selected_rows(self.table_feather)
        if not targets:
            cmds.warning('请先在羽毛列表中选中要设置的行')
            return
        for r in targets:
            self.table_feather.setItem(r, 2, QtWidgets.QTableWidgetItem(short_name(sel[0])))
        print('[翅膀绑定] 已把第 %s 行的对应手臂骨骼设为 %s'
              % (','.join(str(r + 1) for r in targets), short_name(sel[0])))

    def feather_read_selection(self):
        """按选择顺序两两成组：羽毛根骨骼 -> 对应手臂骨骼（已有的不重复加）"""
        cmds.selectPref(trackSelectionOrder=True)
        sel = cmds.ls(orderedSelection=True, type='joint', long=True) or []
        if len(sel) < 2:
            cmds.warning('请按顺序选中「羽毛根骨骼 → 对应手臂骨骼」成对加载')
            return
        rows = self.read_rows(self.table_feather)
        added = 0
        for i in range(0, len(sel) - 1, 2):
            root, arm = short_name(sel[i]), short_name(sel[i + 1])
            if self.has_row(self.table_feather, root, arm):
                continue
            rows.append({'root': root, 'arm': arm, 'angle': 0.0})
            added += 1
        self.write_rows(self.table_feather, rows)
        print('[翅膀绑定] 已按选择顺序加载 %d 根羽毛%s'
              % (added, '' if added else '（都已在表里，没有重复添加）'))

    def feather_auto_match(self):
        """按空间距离把每根羽毛自动挂到最近的手臂骨骼段

        候选不只手臂链本身，还包括手臂骨骼的**下级分支**：真实鸟翼在腕部有一根
        拇指，小翼羽（alula）长在它上面。只按手臂链找最近点的话，小翼羽会被挂到
        离得较远的腕骨上——功能上也能收（腕骨会动），但拇指怎么转它都不理。
        分支候选只在「比手臂段更近」时才采用，所以普通羽毛的匹配结果不受影响。

        羽毛自己的骨骼链要排除，否则羽毛会被匹配到另一根羽毛身上（那会让同一根
        骨骼同时被手臂折叠和羽毛驱动两条链管着，静止姿态都回不去）。
        """
        chain, _phis = self.build_arm_chain(quiet=True)
        if len(chain) < 2:
            cmds.warning('请先加载手臂骨骼链')
            return
        rows = self.read_rows(self.table_feather)
        if not rows:
            cmds.warning('请先加载羽毛根骨骼')
            return

        # 羽毛自己的骨骼链（羽毛根 + 它们的子骨骼）
        feather_joints = set()
        for row in rows:
            root = resolve_joint(row['root'])
            if root is None:
                continue
            feather_joints.add(root)
            feather_joints.update(get_longest_chain(root) or [])

        # 手臂骨骼的下级分支（不含手臂链本身、不含羽毛骨骼）
        chain_set = set(chain)
        branches = []
        stack = []
        for j in chain:
            stack.extend((c, 1) for c in child_joints(j))
        while stack:
            node, depth = stack.pop()
            if depth > 6 or node in chain_set or node in feather_joints:
                continue
            branches.append(node)
            stack.extend((c, depth + 1) for c in child_joints(node))
        branch_pts = [(j, om.MVector(*world_pos(j))) for j in branches]

        pts = joint_positions(chain)
        for row in rows:
            root = resolve_joint(row['root'])
            if root is None:
                continue
            p = om.MVector(*world_pos(root))
            best = (1e18, chain[0])
            for k in range(len(chain) - 1):
                a = om.MVector(*pts[k])
                b = om.MVector(*pts[k + 1])
                ab = b - a
                if ab.length() < 1e-9:
                    continue
                t = max(0.0, min(1.0, ((p - a) * ab) / (ab * ab)))
                d = (p - (a + ab * t)).length()
                if d < best[0]:
                    best = (d, chain[k])
            for j, q in branch_pts:
                d = (p - q).length()
                if d < best[0]:
                    best = (d, j)
            row['arm'] = short_name(best[1])
        self.write_rows(self.table_feather, rows)
        print('[翅膀绑定] 已自动匹配 %d 根羽毛的手臂骨骼' % len(rows))

    def feather_sort(self):
        """按羽毛根骨骼在翼展方向上的投影排序"""
        chain, _phis = self.build_arm_chain(quiet=True)
        if len(chain) < 2:
            cmds.warning('请先加载手臂骨骼链')
            return
        rows = self.read_rows(self.table_feather)
        if not rows:
            return
        pts = joint_positions(chain)
        origin = om.MVector(*pts[0])
        axis = om.MVector(*pts[-1]) - origin
        axis.normalize()

        def key(row):
            root = resolve_joint(row['root'])
            if root is None:
                return 0.0
            return (om.MVector(*world_pos(root)) - origin) * axis
        rows.sort(key=key)
        self.write_rows(self.table_feather, rows)
        print('[翅膀绑定] 已按翼展方向排序羽毛')

    def move_feather(self, step):
        self.move_rows(self.table_feather, step)

    def apply_angle_to_all(self):
        rows = self.read_rows(self.table_arm)
        for row in rows:
            row['angle'] = self.spin_angle.value()
        self.write_rows(self.table_arm, rows)

    @staticmethod
    def fold_package(chain, arm_pts, psis, feathers, normal, sign, auto_dir=True):
        """估某个折点组合收完以后「羽包在翼面里占多大、手臂收完还剩多长」

        返回 (羽包投影面积, 折完以后手臂离肩最远的多远)。

        羽毛按「收到『折完的手 → 肩』这个方向上、长度不变」估，
        和 folded_extent 用的是同一套假设；手臂长度按同一套模拟折出来的骨链量。
        羽毛**朝哪一侧收**用 feather_goal 那条共用规则（和生成时一模一样），
        否则估的和生成出来的不是一回事。
        """
        sim = simulated_chain(arm_pts, [p * sign for p in psis], normal)
        origin = om.MVector(*arm_pts[0])
        u = om.MVector(*arm_pts[-1]) - origin
        if u.length() < 1e-9:
            return 0.0, 0.0
        u.normalize()
        v = normal ^ u
        v.normalize()
        reach = max((p - origin).length() for p in sim)
        goal = feather_goal(arm_pts[0], sim[-1], arm_pts, auto_dir)
        if goal is None:
            return 0.0, reach

        def uv(p):
            d = p - origin
            return d * u, d * v

        chain_set = set(chain)
        pts = list(sim)
        for feather in feathers:
            src = feat_arm_source(feather['arm'], chain, chain_set)
            if src is None:
                continue
            k = chain.index(src)
            if k >= len(sim):
                continue
            ln = chain_length(joint_positions(get_longest_chain(feather['root'])))
            pts.append(feather_base(feather, arm_pts, k, psis, normal, sign, sim)
                       + goal * ln)
        pu = [uv(p)[0] for p in pts]
        pv = [uv(p)[1] for p in pts]
        return (max(pu) - min(pu)) * (max(pv) - min(pv)), reach

    def pick_fold_rows(self, rows, chain, angle, zigzag, root_sweep, feathers):
        """挑「该折的那几行」—— 返回 (行号元组, 羽包面积, 收完手臂伸出量, 展开伸出量)

        两个调用方：界面上的「自动分配折叠角」按钮，和 build_rig 在
        「整列折叠角都填成同一个值」（＝用户没有逐行表态）时自动调一次。
        一个组合都挑不出来时返回 None，调用方保持原样。

        挑法：在「行」这一级枚举折点组合，然后
          ① 先要求**手臂真的折进去了**：折完离肩最远不超过原来的 60%。
             （只折最后一节之类「等于没折」的组合，羽包投影面积反而最小 ——
              实测 6 节手臂只折最后一节面积 0.96，比真折起来的 1.57 还小，
              但那根 5.7 长的手臂整条露在外面，不是收起。这一条不能松：
              所有「收起途中不扎堆」的组合（细长比 8~10、自检 0~2 对穿过）
              都是靠手臂少折一点换来的，实测伸出量 69%~85% —— 放它们进来，
              面积判据就会挑一个「几乎没折」的方案。）
          ② 在满足 ① 的组合里取**羽包投影面积最小**的。
        """
        arm_pts = joint_positions(chain)
        origin = om.MVector(*arm_pts[0])
        rest_reach = max((om.MVector(*p) - origin).length() for p in arm_pts)

        # 估算收拢效果必须把羽毛算进去（羽毛比手臂长得多，撑出轮廓的是羽毛），
        # 所以这里和生成时一样要先量出翼面法线。
        plane_pts = list(arm_pts)
        f_roots, f_tips = [], []
        for feather in feathers:
            root_w = world_pos(feather['root'])
            plane_pts.append(root_w)
            f_roots.append(root_w)
            tip_chain = get_longest_chain(feather['root'])
            if len(tip_chain) > 1:
                tip_w = world_pos(tip_chain[-1])
                plane_pts.append(tip_w)
                f_tips.append(tip_w)
        normal = self.resolve_axis(plane_pts, arm_pts, f_roots, f_tips)

        total = len(rows)
        cands = [tuple(range(total))]
        if zigzag:
            for i in range(total):
                cands.append((i,))
                for j in range(i + 1, total):
                    # 以前这里卡了「两个折点必须隔奇数行（j−i 为奇数）」——那是为了
                    # 绕开「正负号按行号交替」的 bug（隔偶数行会拿到同号、折成螺旋）。
                    # 现在符号是按**真正参与折叠的行**序号交替的，任意两个折点都是
                    # 一正一负，所以这条约束可以去掉：候选更多，自动分配才可能挑到
                    # 更好的折点组合（例如只折第 1、3 行）。
                    cands.append((i, j))
        best = None
        auto_dir = self.combo_feather_dir.currentText() != DIR_FLIP
        for act in cands:
            test = [dict(r, angle=(angle if k in act else 0.0))
                    for k, r in enumerate(rows)]
            ch, phis, e = rows_to_chain(test, zigzag, root_sweep)
            if e:
                continue
            psi_all = solve_psis_chain(ch, phis)
            psis = [psi_all[j] for j in ch]
            # 用生成时真正会采用的那个折叠方向来估（「自动收拢」取伸出最短的那个），
            # 否则估的和最后生成出来的不是一回事。
            s = min((1.0, -1.0),
                    key=lambda sg: self.folded_extent(ch, arm_pts, psis, feathers,
                                                      normal, sg, auto_dir))
            area, reach = self.fold_package(ch, arm_pts, psis, feathers, normal, s,
                                            auto_dir)
            if rest_reach > 1e-9 and reach > 0.6 * rest_reach:
                continue                      # 折了跟没折一样，手臂整条还伸在外面
            if best is None or area < best[0]:
                best = (area, act, reach)
        if best is None:
            return None
        area, act, reach = best
        return act, area, reach, rest_reach

    def assign_fold_rows(self, rows, chain, angle, zigzag, root_sweep, feathers):
        """挑好折点并写回手臂表。返回 'changed' / 'same' / 'none'（一个都挑不出来）

        只由调用方在「表看起来还是默认填充」（整列填了同一个角）时才调 ——
        逐行填过不同的角，那是用户自己的决定，不该被改掉。
        """
        picked = self.pick_fold_rows(rows, chain, angle, zigzag, root_sweep, feathers)
        if picked is None:
            return 'none'
        act, area, reach, rest_reach = picked
        if set(act) == set(range(len(rows))):
            return 'same'                    # 就是「每行都折」，不用改表
        self.write_rows(self.table_arm, [
            {'root': r['root'], 'arm': r['arm'],
             'angle': (angle if k in act else 0.0)}
            for k, r in enumerate(rows)])
        print('[翅膀绑定] 折叠角自动分配：折第 %s 行（其余填 0），'
              '手臂收回 %.0f%%、羽包 %.2f'
              % ('、'.join(str(k + 1) for k in sorted(act)),
                 100.0 * reach / rest_reach if rest_reach else 0.0, area))
        return 'changed'

    def auto_fold_angles(self):
        """自动挑出「该折的那几行」，把每节折叠角分配过去，其余行填 0

        为什么需要这个：Z 形对折是**逐行交替正负号**的。行数一多，还按「每行都填
        170°」去折，累积起来就是一条来回折的锯齿 —— 5 行就是折 5 次的手风琴，
        不是真实鸟翼的「肘 + 腕两个折点」。羽毛全挂在这条手臂上，手臂怎么折它就
        怎么跟，折点一多整个羽包就被折成一坨厚厚的锯齿（实测 6 节手臂 20 根羽毛：
        每行都折 收起后翼面内 2.91 x 1.05、细长比 2.8；只折两行 3.59 x 0.36、
        细长比 10.0 —— 后者才是收起来的鸟翼那种「细长一片」）。
        """
        rows = [r for r in self.read_rows(self.table_arm) if r['root']]
        if not rows:
            cmds.warning('请先在 ① 里加载手臂骨骼')
            return
        angle = self.spin_angle.value()
        if angle <= 0:
            cmds.warning('请先把「每节折叠角」设成大于 0 的值')
            return
        zigzag = self.combo_fold_mode.currentText() == MODE_Z
        root_sweep = self.spin_root_sweep.value()
        chain, _, err = rows_to_chain(rows, zigzag, root_sweep)
        if err:
            cmds.warning('手臂表第 %d 行有问题，先修好再自动分配' % (err[0] + 1))
            return
        feathers = self.validate_feathers(self.collect_feathers(), chain)
        if not feathers:
            cmds.warning('没有可用的羽毛，无法估算收拢效果')
            return
        got = self.assign_fold_rows(rows, chain, angle, zigzag, root_sweep, feathers)
        if got == 'none':
            print('[翅膀绑定] 折叠角自动分配：没有一个组合能把手臂真正折进去，'
                  '保持现在的填法')
        elif got == 'same':
            print('[翅膀绑定] 折叠角自动分配：现在的填法就是最好的，表格没动')

    def on_mode_changed(self, index):
        """切换折叠模式时，若角度还是别的模式的默认值则自动跟随"""
        mode = self.combo_fold_mode.currentText()
        others = [v for k, v in MODE_DEFAULT_ANGLE.items() if k != mode]
        if self.spin_angle.value() in others:
            self.spin_angle.setValue(MODE_DEFAULT_ANGLE.get(mode, DEFAULT_FOLD_ANGLE))
            self.apply_angle_to_all()

    # -------------------------------------------------------- 合并手臂链
    def build_arm_chain(self, quiet=False):
        """把手臂表格里的每节手臂合并成完整骨骼链

        返回 (chain, phis)。真正的整理逻辑在模块级的 rows_to_chain 里
        （自动分配折叠角要反复试算不同行组合，用的是同一份逻辑）。
        """
        rows = [r for r in self.read_rows(self.table_arm) if r['root']]
        if not rows:
            return [], []
        # 行顺序不是从翼根到翼尖时（大纲里从下往上框选、或者反复点过「上移/下移」），
        # 先按层级理正，并把理正后的顺序写回表格 —— 否则用户看到的是「我明明填了，
        # 它却报第 2 节没接上」，而且表格显示的顺序和实际用的顺序还不一致。
        ordered = order_arm_rows(rows)
        if [r['root'] for r in ordered] != [r['root'] for r in rows]:
            self.write_rows(self.table_arm, [
                {'root': r['root'], 'arm': r['arm'], 'angle': r['angle']}
                for r in ordered])
            rows = ordered
        zigzag = self.combo_fold_mode.currentText() == MODE_Z
        chain, phis, err = rows_to_chain(rows, zigzag, self.spin_root_sweep.value())
        if err is None:
            return chain, phis
        if not quiet:
            gi, kind, info = err
            if kind == 'with_arm':
                cmds.warning('第 %d 节手臂的根骨骼与手臂骨骼不在同一条层级链上: %s -> %s'
                             % (gi + 1, short_name(info[0]), short_name(info[1])))
            elif kind == 'leaf':
                cmds.warning('第 %d 节手臂只填了根骨骼，且它没有子骨骼: %s'
                             % (gi + 1, short_name(info[0])))
            elif kind == 'gap':
                cmds.warning('第 %d 节手臂没有接上一节：期望根骨骼 %s，实际 %s'
                             % (gi + 1, short_name(info[0]), short_name(info[1])))
            else:
                cmds.warning('第 %d 节手臂没有新增骨骼' % (gi + 1))
        return [], []

    def validate_feathers(self, feathers, chain):
        """挑出填错的羽毛行，跳过后再生成，并把问题说清楚

        照着一张填错的表硬做，会出三种很难查的问题（都实测过）：
          · 同一根骨骼既当手臂节、又当羽毛根：它的 rotate 上会被写两套驱动关键帧、
            位置还会被羽毛样条的点/方向约束拽走，静止姿态直接偏 0.5 以上，
            而且删掉绑定也恢复不了（实测 0.50784536）
          · 「对应手臂骨骼」填成另一根羽毛的骨骼：那根骨骼同时被手臂折叠和羽毛
            驱动两条链管着，同样静默损坏（实测 0.64185177）
          · 挂到一根跟手臂无关的骨骼上：收起时羽毛纹丝不动（实测只收到 96%）
        与其生成一套坏绑定，不如跳过这几行并告诉用户是哪几行、该怎么改。

        合法的情况都放行：
          · 「对应手臂骨骼」就是手臂链上的某一节——这是最常见的正确填法；
          · 手臂骨骼的下级分支（例如鸟类腕部的拇指，小翼羽挂它上面）——
            分支自己不折叠，但跟着它所依附的那节手臂骨骼一起动，能正常收。
        """
        chain_set = set(chain)
        root_set = set(f['root'] for f in feathers)
        # 羽毛链上的所有骨骼（羽毛根 + 它们的子骨骼）
        feather_joints = set()
        for r in root_set:
            feather_joints.add(r)
            for c in get_longest_chain(r) or []:
                feather_joints.add(c)
        arm_section = {}
        for i, j in enumerate(chain):
            arm_section[j] = i + 1

        keep, bad, seen = [], [], set()
        for f in feathers:
            root = f['root']
            arm = f['arm']
            if root in seen:
                bad.append((short_name(root), '在表里出现了两次（第二行会重复加一套约束）'))
                continue
            seen.add(root)
            if arm is None:
                bad.append((short_name(root), '没有填「对应手臂骨骼」'))
                continue
            if root in chain_set:
                bad.append((short_name(root), '它本身是第 %d 节手臂骨骼，'
                            '不能同时当羽毛根骨骼' % arm_section.get(root, 0)))
                continue
            if arm == root:
                bad.append((short_name(root), '「对应手臂骨骼」填成了它自己'))
                continue
            if arm in feather_joints:
                bad.append((short_name(root), '「对应手臂骨骼」%s 是另一根羽毛的骨骼'
                            % short_name(arm)))
                continue
            if chain_ancestor(arm, chain_set) is None:
                bad.append((short_name(root), '「对应手臂骨骼」%s 既不在手臂链上、'
                            '也不是手臂的下级骨骼，收起时它不会动' % short_name(arm)))
                continue
            keep.append(f)
        if bad:
            self.skipped_feathers = len(bad)
            cmds.warning('有 %d 根羽毛填得不对，已跳过（不影响其它羽毛）：%s。'
                         '请改好「对应手臂骨骼」后再生成。'
                         % (len(bad),
                            '；'.join('%s: %s' % (n, why) for n, why in bad[:5])))
        return keep

    def collect_feathers(self):
        """读羽毛表 -> [{'root':长名, 'arm':长名, 'extra':度}]（按表格顺序）"""
        out = []
        for row in self.read_rows(self.table_feather):
            root = resolve_joint(row['root'])
            if root is None:
                continue
            out.append({'root': root, 'arm': resolve_joint(row['arm']),
                        'extra': row['angle']})
        return out

    def refresh_table_names(self):
        """生成后把表格里的骨骼名刷新成最新短名

        羽毛根骨骼被重新父子后层级会变，用短名显示既稳定又好读。
        """
        for table in (self.table_arm, self.table_feather):
            rows = self.read_rows(table)
            for row in rows:
                for key in ('root', 'arm'):
                    joint = resolve_joint(row[key])
                    if joint:
                        row[key] = short_name(joint)
            self.write_rows(table, rows)

    # -------------------------------------------------------- 折叠轴
    def resolve_axis(self, pts, arm_pts=None, roots=None, tips=None):
        """求折叠轴（翼面法线）

        「自动」优先用 手臂方向 × 羽毛方向（见 wing_axis，稳），
        只有在两者退化（手臂和羽毛几乎平行）时才退回拟合平面。
        """
        text = self.combo_axis.currentText()
        if text == '自动(翼面法线)':
            if arm_pts and roots and tips:
                axis = wing_axis(arm_pts, roots, tips)
                if axis is not None:
                    return axis
            return plane_normal(pts)
        if text == '世界 X':
            return om.MVector(1, 0, 0)
        if text == '世界 Y':
            return om.MVector(0, 1, 0)
        if text == '世界 Z':
            return om.MVector(0, 0, 1)
        parts = self.line_axis.text().replace('，', ',').split(',')
        try:
            vec = om.MVector(float(parts[0]), float(parts[1]), float(parts[2]))
        except Exception:
            cmds.warning('自定义折叠轴格式错误，应为 0,0,1')
            return plane_normal(pts)
        if vec.length() < 1e-9:
            return plane_normal(pts)
        vec.normalize()
        return vec

    # -------------------------------------------------------- 生成绑定
    @staticmethod
    def folded_extent(chain, arm_pts, psis, feathers, normal, sign, auto_dir=True):
        """估这个折叠方向收完以后整只翅膀能伸出多远（把羽毛算进去）

        只看「手臂翼尖到肩的距离」是不够的：收起后真正撑出轮廓的是羽毛——
        羽毛比手臂长得多，折叠方向换一个，手臂翼尖的距离可能只差 2%，
        但羽包整体伸出去的方向完全变了。实测场景 A：自动收拢按手臂翼尖挑，
        挑出来的方向羽包反而比另一个方向远 2%（1.584 vs 1.552）。
        羽毛收完会被摆到「折完的手 → 肩」这个方向上、长度不变，所以可以直接估：
            tip_k ≈ 折后第 k 个手臂关节 + goal · 羽毛长
        goal 用 feather_goal 那条共用规则（含「朝肩那一侧收」的兜底），
        否则估出来的伸出量和真正生成出来的对不上（实测 human.mb 的真实骨架：
        估 48%、实际 105%）。
        """
        sim = simulated_chain(arm_pts, [p * sign for p in psis], normal)
        origin = om.MVector(*arm_pts[0])
        goal = feather_goal(arm_pts[0], sim[-1], arm_pts, auto_dir)
        if goal is None:
            return 0.0
        best = 0.0
        chain_set = set(chain)
        for feather in feathers:
            # 羽毛挂在手臂骨骼的下级分支上时（拇指/小翼羽），
            # 它跟着「分支所依附的那节手臂骨骼」一起走，按那一节估伸出量
            src = feat_arm_source(feather['arm'], chain, chain_set)
            if src is None:
                continue
            k = chain.index(src)
            if k >= len(sim):
                continue
            length = chain_length(joint_positions(get_longest_chain(feather['root'])))
            base = feather_base(feather, arm_pts, k, psis, normal, sign, sim)
            best = max(best, ((base + goal * length) - origin).length())
        return best

    def auto_root_sweep(self, chain, phis, feathers):
        """算「根部后掠角」：让收好的翅膀顺着身体，而不是继续朝翼尖那一侧伸着

        为什么需要这一下：Z 形对折只把手臂折回来，**没有转肩**。收到底以后整叠
        羽毛的长轴仍然沿着原来的翼展方向 —— 翼包从肩部往翼尖那一侧杵出去一截。
        实测真翼形 38 根：沿静止翼展方向的外伸量是翼展的 0.221；真实鸟翼收起时
        是贴身体前后方向收着的，不该还往外杵。加一个绕翼面法线的根旋转就能把它
        转到体轴上（实测 0.221 → 0.000~0.062，紧凑度 21% 与穿插全过不变）。

        转多少由一条模型无关的判据定：
          鸟的**弦向**（前缘→后缘）就是体轴的前后方向，而羽毛长在后缘那一侧 ——
          所以「羽毛在翼面内偏向的那一侧」就是「后方」。把收起后羽毛的朝向
          （= feather_goal 给的方向）转到这个「后方」上，转角就是要转的量：
              sweep = signed_angle(N, goal₀, trail)

        goal₀ 必须用**后掠 0** 的姿态算：后掠是整体刚性旋转，用它自己算出来的
        goal 再去解后掠，会得到「恒等于自己」的方程（下次生成时算出来是 0，
        来回抖）。所以这里显式把 phis[0] 归零再模拟一次。
        """
        pts = joint_positions(chain)
        if len(pts) < 2 or not feathers:
            return None
        roots = []
        tips = []
        for f in feathers:
            ch = get_longest_chain(f['root'])
            if len(ch) > 1:
                roots.append(world_pos(f['root']))
                tips.append(world_pos(ch[-1]))
        normal = self.resolve_axis(pts + roots + tips, pts, roots, tips)
        normal.normalize()
        # 1) 后掠 0 的折叠姿态 → 羽毛收好后朝哪
        zero = [0.0] + list(phis[1:])
        sim = simulated_chain(pts, zero, normal)
        goal = feather_goal(pts[0], sim[-1], pts,
                            self.combo_feather_dir.currentText() != DIR_FLIP)
        if goal is None:
            return None
        # 2) 「后方」= 翼面内、羽毛偏向的那一侧
        u = om.MVector(*pts[-1]) - om.MVector(*pts[0])
        if u.length() < 1e-9:
            return None
        u.normalize()
        acc = om.MVector()
        for f in feathers:
            d = feather_direction(f['root'])
            if d is not None:
                acc += d
        if acc.length() < 1e-9:
            return None
        acc.normalize()
        trail = acc - u * (acc * u)
        if trail.length() < 1e-6:
            # 羽毛几乎和手臂平行（整排顺着手指出去的模型），弦向判不出来，
            # 这时不动它，交给用户手填。
            return None
        trail.normalize()
        return math.degrees(signed_angle(normal, goal, trail))

    def build_rig(self):
        # 先清掉上一次的状态栏，避免生成失败时还显示上一次的成功信息
        self.label_info.setText('')
        chain, phis = self.build_arm_chain()
        if len(chain) < 2:
            if not chain:
                cmds.warning('请先按顺序加载手臂骨骼（每节的根骨骼与手臂骨骼）')
            else:
                cmds.warning('手臂骨骼链至少需要 2 根骨骼')
            self.label_info.setText('生成失败：手臂骨骼链不完整')
            return

        feathers = self.collect_feathers()
        self.skipped_feathers = 0
        feathers = self.validate_feathers(feathers, chain)
        if not feathers:
            cmds.warning('没有可用的羽毛（都被跳过了），请检查羽毛列表')
            self.label_info.setText('生成失败：没有可用的羽毛')
            return

        if all(abs(p) < 1e-9 for p in phis):
            cmds.warning('所有折叠角都是 0，请设置每节的折叠角')
            self.label_info.setText('生成失败：折叠角都是 0')
            return

        # **参考（reference）进来的模型**：Maya 不许改参考里的层级结构，
        # 「羽毛根骨骼挂到对应手臂骨骼下」这一步做不到（三条写法全被 Maya 拦下，
        # 见 ref_parent_block 的注释）。与其让用户看到一句英文报错、以为插件坏了，
        # 不如提前讲清楚是什么、怎么办。
        if self.chk_parent.isChecked():
            block = ref_parent_block(feathers)
            if block:
                idx, fname, aname = block
                cmds.warning(
                    '模型是**参考（reference）**进来的，Maya 不允许改动参考里的骨骼'
                    '层级，羽毛挂不到手臂骨骼下（第 %d 根 %s → %s）。'
                    '请到 Window > General Editors > Reference Editor 里把这条参考'
                    'Import 进来（或在 Reference Editor 里右键 > Import Reference），'
                    '再点「生成」；也可以先手动把羽毛根骨骼挂到对应手臂骨骼下，'
                    '并把「羽毛根骨骼自动挂到对应手臂骨骼下」的勾去掉。'
                    % (idx, fname, aname))
                self.label_info.setText('生成失败：模型是参考进来的，Maya 不允许改参考里的'
                                        '骨骼层级（详见脚本编辑器）')
                return

        # 「自动后掠」在下面「折叠方向」定下来之后才施加（见 root_phi 那一段）——
        # 方向一翻，后掠的符号就跟着反，必须等方向定了再算。

        # 记下**生成之前**每根骨骼世界矩阵的 3x3（朝向+缩放）。
        # 为什么必须记：自检第 1 项查的是「驱动通道的旋转值回没回到静止值」，
        # 查不出「骨骼的世界朝向被转了 180°」。实测真翼形 38 根羽毛里，
        # 有 44 根骨骼生成后世界矩阵某个元素差了整整 2.0（＝绕自身轴翻转 180°），
        # 而位置一点没变 —— 只比位置的自检一路绿灯，卡片却已经被翻了个面：
        # 收起=0 时网格顶点最大偏离建模姿态 0.93、整张卡的包围盒差 0.52，
        # 渲出来一目了然（一半卡片亮着、一半是背面）。这里把生成前的朝向存进
        # 登记表，自检就能把它抓出来，用户在自己模型上也能一眼看到有没有中招。
        rest_rot3 = {}
        _all_j = list(chain)
        for _f in feathers:
            _all_j += get_longest_chain(_f['root'])
        for _j in _all_j:
            if not cmds.objExists(_j):
                continue
            _m = cmds.xform(_j, q=True, ws=True, m=True)
            rest_rot3[short_name(_j)] = [round(_m[0], 6), round(_m[1], 6),
                                         round(_m[2], 6), round(_m[4], 6),
                                         round(_m[5], 6), round(_m[6], 6),
                                         round(_m[8], 6), round(_m[9], 6),
                                         round(_m[10], 6)]
        # 给下面建方向约束用：翼面法线当「上方向」尺子、生成前的朝向当比对基准
        self._rest_rot3 = rest_rot3

        # 整列折叠角都填成同一个值 ＝ 表格的默认填充（「读取选中链 / 加载骨骼」
        # 会把每一行都填成「每节折叠角」那个数），也就是用户没有逐行表态 ——
        # 这时让插件自己挑折点。行数一多，每行都折就是一条来回折的手风琴，
        # 收起来是一坨而不是「细长一片」（6 节手臂 20 根羽毛实测：每行都折
        # 翼面内 2.91 x 1.05、细长比 2.8；只折两行 3.59 x 0.36、细长比 10.0）。
        # 逐行填过不同的角就一个字都不改 —— 表里写什么就按什么折。
        #
        # **只在 3 行以上才挑**：1~2 行时「每行都折」正好就是「该折的那几个关节」
        # （2 行＝肘+腕），没有手风琴可治；而挑点器只有 3 个候选，会挑到「只折第 1 行」
        # 这种更差的组合 —— 实测工程里真实的 human.mb 骨架（2 行、每行夹着 A/B 辅助骨）：
        # 「每行都折」收起后羽尖到肩 31%，挑成「只折第 1 行」变成 105%（手臂只弯一次，
        # 腕落在肩后 1.5，长飞羽从那里再往后伸）。
        arm_rows = [r for r in self.read_rows(self.table_arm) if r['root']]
        if (len(arm_rows) >= 3 and arm_rows[0]['angle'] > 0
                and len(set(round(r['angle'], 6) for r in arm_rows)) == 1):
            if self.assign_fold_rows(arm_rows, chain, arm_rows[0]['angle'],
                                     self.combo_fold_mode.currentText() == MODE_Z,
                                     self.spin_root_sweep.value(),
                                     feathers) == 'changed':
                chain, phis = self.build_arm_chain()

        # 父级带**非均匀缩放**时这条解算管线会出问题，提前讲清楚：
        # 收起会把骨骼和网格拉出剪切形变（世界空间里骨长会变）。这是 Maya 自己的
        # 层级行为，任何绑定都躲不掉。用「把翅膀的缩放冻结/烘进骨骼」解决。
        # （负缩放/镜像不在此列：整只翅膀一起镜像时插件是正常的，见下面那段。）
        skew = []
        for j in chain:
            wm = cmds.xform(j, q=True, ws=True, m=True)
            s = [om.MVector(wm[k], wm[k + 1], wm[k + 2]).length() for k in (0, 4, 8)]
            lo = max(min(s), 1e-12)
            if max(s) / lo > 1.001:
                skew.append((short_name(j), max(s) / lo))
        # 「羽毛和手臂不在同一个坐标系里」：两边世界矩阵的行列式符号不一致。
        #
        # **镜像翅膀本身没问题**：只要整只翅膀（手臂 + 羽毛）一起被镜像，行列式符号
        # 就一致，收起解算完全正常 —— 实测夹具整体 scale (-1,1,1) 时收起到底
        # 「最远羽尖离肩」1.644，和不镜像时逐位相同，静止姿态还原误差 0.0000。
        # 之前这里误报「父级负缩放 = 收起不准」，那是拿一个自相矛盾的夹具量出来的。
        #
        # 真正会炸的是「只镜像了一半」：手臂在带 -1 的组里（det -1），羽毛还留在
        # 世界根下（det +1）。插件把羽毛挂到镜像过的手臂骨骼下时，局部矩阵里会多出
        # 一个负缩放，手臂一折羽毛就被甩出去（实测「最远羽尖离肩」1.64 → 5.16、
        # 关节包围盒 1.57 → 4.08）。这种场景下绑定必然是坏的，明确说出来，
        # 别静默生成一套废绑定。
        arm_det = matrix_det3(cmds.xform(chain[0], q=True, ws=True, m=True))
        bad_frame = []
        for feather in feathers:
            wm = cmds.xform(feather['root'], q=True, ws=True, m=True)
            if matrix_det3(wm) * arm_det < 0.0:
                bad_frame.append(short_name(feather['root']))
        if bad_frame:
            cmds.warning(
                '有 %d/%d 根羽毛和手臂**不在同一个坐标系里**（%s …）：手臂的父级带镜像'
                '（负缩放），这些羽毛没有。收起时它们会被甩出去、整只翅膀越收越大。'
                '请让羽毛跟着翅膀一起被镜像（把羽毛放进同一个父级下再镜像），'
                '或者先把缩放冻结（Freeze Transformations）再生成绑定。'
                % (len(bad_frame), len(feathers), '、'.join(bad_frame[:3])))
            self.label_info.setText('注意：%d根羽毛与手臂坐标系不一致（镜像只做了一半）'
                                    % len(bad_frame))
        if skew:
            cmds.warning(
                '手臂骨骼的父级带非均匀缩放（%s 上最大/最小轴向差了 %.2f 倍）：'
                '收起时骨骼和网格会被拉出剪切形变，看起来像「收起来变形了」。'
                '建议先把翅膀的缩放统一（冻结变换 / 把非均匀缩放烘进模型）再生成绑定。'
                % (skew[0][0], skew[0][1]))
            self.label_info.setText('注意：父级非均匀缩放，收起会有拉伸')

        cmds.undoInfo(openChunk=True, chunkName='Wing Rig')
        # 生成过程会密集 setAttr（fold、各关节 rotate）。用户若开着自动关键帧，
        # 这些 setAttr 会在属性上留下杂散关键帧，把动画和收起曲线都搞乱，先关掉。
        auto_key = cmds.autoKeyframe(q=True, state=True)
        if auto_key:
            cmds.autoKeyframe(state=False)
        try:
            # 1) 若之前生成过，先撤掉旧的驱动关键帧，把骨骼还原到静止姿态。
            #    必须还原后再测量，否则在收起状态下再次生成会算错折叠轴与静止姿态。
            ctrl = self.find_ctrl_for(chain)
            if ctrl:
                self.remove_driven(ctrl)
                # 拆除会把 FK 偏移组拆掉、层级回退，之前收集的长名全部失效，重新解析
                chain = [resolve_joint(short_name(j)) or j for j in chain]
                for feather in feathers:
                    feather['root'] = (resolve_joint(short_name(feather['root']))
                                       or feather['root'])
                    feather['arm'] = (resolve_joint(short_name(feather['arm']))
                                      or feather['arm'])

            # 2) 羽毛根骨骼挂到对应手臂骨骼下（保持世界位置）
            if not self.bind_feathers(feathers):
                self.label_info.setText('生成失败：羽毛没有挂到对应手臂骨骼下')
                return

            # 2.5) 给手臂每节插一个 FK 偏移组：收起仍驱动骨骼本身，
            #      动画师要摆肩/肘/腕就转 <骨骼>_fk，两边不抢通道
            offsets = self.insert_fk_offsets(chain)
            # 插组会改变层级，骨骼/羽毛的长名全部失效，刷新一遍再继续
            chain = [resolve_joint(short_name(j)) or j for j in chain]
            for feather in feathers:
                feather['root'] = (resolve_joint(short_name(feather['root']))
                                   or feather['root'])
                feather['arm'] = (resolve_joint(short_name(feather['arm']))
                                  or feather['arm'])

            # 3) 在静止姿态下测量：手臂位置、翼面法线（折叠轴）
            arm_pts = joint_positions(chain)
            plane_pts = list(arm_pts)
            f_roots = []
            f_tips = []
            for feather in feathers:
                root_w = world_pos(feather['root'])
                plane_pts.append(root_w)
                f_roots.append(root_w)
                tip_chain = get_longest_chain(feather['root'])
                if len(tip_chain) > 1:
                    tip_w = world_pos(tip_chain[-1])
                    plane_pts.append(tip_w)
                    f_tips.append(tip_w)
            normal = self.resolve_axis(plane_pts, arm_pts, f_roots, f_tips)
            # 建羽毛方向约束时要用它当「上方向」尺子（见 build_feather_constraints）
            self._build_normal = om.MVector(normal)

            # 4) 折叠方向：自动收拢时，取「收完以后整只翅膀（含羽毛）伸出最短」的那个方向。
            #    根部后掠角先排除在外，否则改一下后掠角就可能把整个折叠方向翻过去；
            #    后掠角本身按用户填的字面值施加（不随折叠方向翻转），方向不对反号即可。
            root_phi = phis[0]
            phis[0] = 0.0
            dir_mode = self.combo_dir.currentText()
            auto_dir = self.combo_feather_dir.currentText() != DIR_FLIP
            if dir_mode != '正向':
                psis = [solve_psis_chain(chain, phis)[j] for j in chain]
                if dir_mode == '自动收拢':
                    sign = min((1.0, -1.0),
                               key=lambda s: self.folded_extent(
                                   chain, arm_pts, psis, feathers, normal, s,
                                   auto_dir))
                else:
                    sign = -1.0
                if sign < 0:
                    phis = [-p for p in phis]
            phis[0] = root_phi
            # 「自动后掠」：方向定了再算 —— 收好的翅膀要从「沿翼展」转到「沿体轴」。
            # 这里只改 phis[0]，下面 psi_all / folded_pts / feather_targets /
            # 驱动关键帧全都是从 phis 推出来的，所以一处生效、处处一致。
            if self.chk_root_sweep_auto.isChecked():
                sweep = self.auto_root_sweep(chain, phis, feathers)
                if sweep is not None:
                    phis[0] = sweep

            # 5) 创建控制器
            if not ctrl:
                ctrl = self.create_ctrl(chain, arm_pts, normal)

            # 6) 解算：手臂各关节的世界旋转增量 ψ、每根羽毛的收拢角 δ
            roots = [f['root'] for f in feathers]
            rest = RestPose(chain + roots)
            psi_all = solve_psis_chain(chain, phis)
            # 折叠后手臂各关节的位置——羽毛要顺着这个方向排列（见 feather_targets）
            folded_pts = simulated_chain(arm_pts, [psi_all[j] for j in chain], normal)
            sweeps = {}
            tilts = {}
            depths = {}
            # 判「羽毛朝哪收」用的那把尺子必须和后掠一起转（见 feather_goal 的 ref_u）。
            # 后掠就是根关节绕 N 转 phis[0]，所以把静止手臂方向转同一个角即可。
            ref_u = None
            if abs(phis[0]) > 1e-9:
                u0 = om.MVector(*arm_pts[-1]) - om.MVector(*arm_pts[0])
                if u0.length() > 1e-9:
                    ref_u = rotate_vector(u0.normal(), normal, math.radians(phis[0]))
            for feather, delta, tilt, depth in self.feather_targets(chain, feathers,
                                                                    normal, folded_pts,
                                                                    ref_u):
                sweeps[feather['root']] = delta
                tilts[feather['root']] = tilt
                depths[feather['root']] = depth

            samples = self.spin_samples.value()
            psi_at, parent_psi = make_psi_functions(psi_all, chain)

            # 7) 手臂：控制器 fold -> 每个手臂关节的 rotate（一个个驱动）
            folded_vals = self.build_driven(ctrl, chain, rest, psi_at, parent_psi,
                                            normal, samples, offsets)

            # 8) 羽毛：每根一条驱动样条 + splineIK，样条控制点由「对应手臂关节的旋转」驱动
            feather_joints = []
            for feather in feathers:
                feather_joints.extend(get_longest_chain(feather['root']))
            extras = self.build_feather_splines(ctrl, chain, feathers, rest, psi_all,
                                                normal, sweeps, tilts, depths,
                                                offsets, folded_vals)
            self.drive_feather_splines(ctrl, extras, samples)
            cmds.setAttr(ctrl + '.' + FOLD_ATTR, 0)
            cmds.select(ctrl)          # 放进同一个撤销块，一次 Ctrl+Z 可整体回退
        finally:
            if auto_key:
                cmds.autoKeyframe(state=True)
            cmds.undoInfo(closeChunk=True)

        joints_all = list(chain) + roots + [j for j in feather_joints if j not in roots]
        rest_rotate = {}
        rest_translate = {}
        for j in joints_all:
            rest_rotate[j] = list(cmds.getAttr(j + '.rotate')[0])
            # 点约束会改到关节的 translate，拆除时必须一起还原
            rest_translate[j] = list(cmds.getAttr(j + '.translate')[0])
        self.rigs[ctrl] = {'joints': joints_all, 'rest_rotate': rest_rotate,
                           'rest_translate': rest_translate, 'extras': extras,
                           'offsets': offsets, 'normal': om.MVector(normal),
                           'rest_rot3': rest_rot3}
        # 把登记表一起写进控制器，这样存盘重开以后插件还认得这套绑定
        try:
            if not cmds.attributeQuery(RIG_DATA_ATTR, n=ctrl, ex=True):
                cmds.addAttr(ctrl, ln=RIG_DATA_ATTR, dt='string')
            cmds.setAttr(ctrl + '.' + RIG_DATA_ATTR,
                         pack_rig_data(self.rigs[ctrl]), type='string')
        except Exception as e:
            cmds.warning('登记绑定信息失败（不影响这次生成，但重开文件后要手工删绑定）：%s' % e)
        self.refresh_rig_combo(ctrl)
        self.current_ctrl = ctrl
        self.set_fold(0)
        # 重新父子会改变骨骼长名，把表格里的名字刷新一遍，方便再次生成
        self.refresh_table_names()
        # 辅助物体（驱动样条 / 定位器）按界面开关显示。刚生成的是藏着的，
        # 否则 44 根羽毛的 44 条曲线 + 132 个定位器会盖满视口。
        self.set_helpers_visible(self.chk_helpers.isChecked())

        total = sum(abs(p) for p in phis)
        self.label_info.setText(
            '手臂 %d根/%d节｜羽毛 %d根｜%s｜轴(%.2f,%.2f,%.2f)｜折叠量%.0f°'
            % (len(chain), len(chain) - 1, len(feathers),
               self.combo_fold_mode.currentText(), normal.x, normal.y, normal.z, total))
        if self.skipped_feathers:
            self.label_info.setText(self.label_info.text()
                                    + '｜跳过%d根填错的' % self.skipped_feathers)
        # 大部分羽毛都挂在根骨骼上、而根骨骼又不动（根部后掠角 = 0）时，它们的根部
        # 在收起过程中一动不动（羽毛权重 1），羽包会明显收不紧。这多半是把「对应手臂
        # 骨骼」整列填成了同一根，提示一下，免得用户只看到「怎么收不紧」。
        # 少量羽毛挂在根骨骼上是正常的（靠近肩的覆羽本来就该挂根骨骼），不提示；
        # 只有 1 节手臂时所有羽毛本来就只能挂根骨骼，也不提示。
        if abs(root_phi) < 1e-9 and feathers and len(chain) >= 3:
            stuck = len([f for f in feathers
                         if feat_arm_source(f['arm'], chain) == chain[0]])
            if stuck >= max(2, len(feathers) * 0.7):
                cmds.warning(
                    '%d/%d 根羽毛的「对应手臂骨骼」都是根骨骼（%s），而「根部后掠角」是 0：'
                    '收起时这些羽毛的根部不会跟着手臂移动，羽包会收不紧。'
                    '建议把它们改成离各自最近的那一节手臂。'
                    % (stuck, len(feathers), short_name(chain[0])))
                self.label_info.setText(self.label_info.text() + '｜注意:%d根挂根骨骼上' % stuck)
        # 收起到底之后翅膀**有没有变小**：折叠角是用户自己填/自动分配的，填歪了
        # （最典型：把中间某一节填成 0，剩下的节又同号，手臂会卷成一圈螺旋）时，
        # 收起后反而比展开还长。实测 3 节手臂填 [150, 0, 150]：展开 3.79 → 收起 4.15
        # （109%），而插件一声不吭 —— 用户看到的就是「点了收起，翅膀没变小/还变大了」。
        if feathers:
            origin = om.MVector(*world_pos(chain[0]))

            def reach(percent):
                # 量的是**羽尖到肩**的最大距离（和自检里的「收起紧凑度」同一把尺）。
                # ① 不要把手臂链上的关节也算进来：只有 1 节手臂时手臂本来就折不动
                #    （末端没有东西可带），但羽毛自己会扫拢、翅膀照样收小了一半；
                #    把手臂关节算进去会把它误报成「收起没变小」。
                # ② 单节骨骼的羽毛要跳过：它 `get_longest_chain` 出来只有自己一根，
                #    `ch[-1]` 就是羽毛根、量到的其实是「羽毛根离肩多远」——
                #    实测把「1/2/3/4 节混合」那个场景误报成 93%（实际 38%）。
                self.set_fold(percent)
                cmds.refresh(force=True)
                best = 0.0
                for f in feathers:
                    ch = get_longest_chain(f['root'])
                    if len(ch) >= 2:
                        best = max(best,
                                   (om.MVector(*world_pos(ch[-1])) - origin).length())
                return best

            r_rest = reach(0)
            r_fold = reach(100)
            self.set_fold(0)
            cmds.refresh(force=True)
            # 只在**收起后反而比展开还长**时报。这条是实测过的（`[150, 0, 150]`
            # 这种手填角度会让手臂卷成一圈螺旋，展开 3.79 → 收起 4.15 = 109%）。
            #
            # 曾经还想在这里加一条「只小到 X% 说明你的模型是扇子形」的提示，写完之后
            # 专门造了个扇子形场景（羽毛从翼根 -92° 一路掠到翼尖 -142°，尖端完全不伸
            # 出翼展）去验 —— 结果它照样收到 **29%**（羽尖到肩 3.92 → 1.13）。
            # 也就是说「扇子形收不动」这个说法是错的：羽毛的收拢是靠扫向肩部完成的，
            # 跟展开姿态长什么样关系不大。既然是错的就没留，免得拿一个没验证过的
            # 结论去解释用户的问题（那比不解释更误导）。
            if r_rest > 1e-9 and r_fold > r_rest:
                cmds.warning(
                    '收起到底之后翅膀**反而变大了**（羽尖到肩：展开 %.2f → 收起 %.2f，%.0f%%）：'
                    '这套折叠角填歪了 —— 常见原因是把某一节填成 0 而其余节同号，'
                    '手臂会卷成一圈螺旋。建议点「自动分配折叠角」重挑折点，'
                    '或者检查一下手臂表里每行的角度。'
                    % (r_rest, r_fold, 100.0 * r_fold / r_rest))
                self.label_info.setText(self.label_info.text() + '｜注意:收起反而变大')

        # 翼面法线是从「手臂关节 + 羽毛根」这一堆点拟合出来的。如果这些点根本不在
        # 一个平面上（手臂是三维弯的、羽毛根参差不齐），这条法线就是猜出来的，
        # 折叠轴会跟你想的不一样 —— 表现出来就是「收是收了，但折的方向不对 / 翅膀歪着折」。
        # 量一下最大偏离（相对整根翅膀的跨度），超了就说清楚，并指出可以手动指定折叠轴。
        plane_pts = [world_pos(j) for j in chain]
        for f in feathers:
            plane_pts.append(world_pos(f['root']))
        try:
            nrm = om.MVector(*self.rigs[ctrl]['normal'])
        except Exception:
            nrm = om.MVector(0.0, 0.0, 1.0)
        if nrm.length() > 1e-9 and len(plane_pts) >= 3:
            nrm.normalize()
            base = om.MVector(*plane_pts[0])
            span = max((om.MVector(*p) - base).length() for p in plane_pts)
            dev = max(abs((om.MVector(*p) - base) * nrm) for p in plane_pts)
            if span > 1e-9 and dev / span > 0.08:
                cmds.warning(
                    '手臂关节和羽毛根**不在一个平面上**（最大偏离 %.0f%%，跨度的 %.2f/%.2f）：'
                    '折叠轴（翼面法线）只能靠拟合这些点猜出来，可能跟你想的不一样 ——'
                    '如果收起时翅膀是「歪着折 / 折向奇怪的方向」，把「折叠轴」改成手动指定'
                    '（多数情况填世界 Z 或 Y）就会正常。'
                    % (100.0 * dev / span, dev, span))
                self.label_info.setText(self.label_info.text() + '｜注意:翼面不共面')
        # 生成时顺手把羽毛权重刷成刚性（默认勾着）。用户的要求本来就是
        # 「羽毛对应骨骼权重 = 1」，而大多数模型的蒙皮是「每个顶点各自绑最近的骨骼」——
        # 那样一张卡会散到 3~7 根羽毛上、收起时被剪开（边长最大变 27%）。
        # 放在最后一步、且在同一个撤销块里，所以一次 Ctrl+Z 能把「生成 + 刷权重」
        # 一起撤回。失败不影响绑定本身，只提示一下。
        if self.chk_weights.isChecked():
            try:
                note = self.normalize_feather_weights(quiet=True)
                if note:
                    self.label_info.setText(self.label_info.text() + '｜' + note)
            except Exception as e:
                cmds.warning('顺手刷羽毛权重时出错（绑定本身不受影响，可手动点'
                             '「羽毛权重=1」重试）：%s' % e)
        print('[翅膀绑定] 已生成绑定 %s：手臂骨骼 %d 根，羽毛 %d 根，总折叠量 %.1f°'
              % (ctrl, len(chain), len(feathers), total))

    def bind_feathers(self, feathers):
        """把羽毛根骨骼重新父子到对应的手臂骨骼下（保持世界位置）

        父子关系一变，骨骼的长名也会变，因此这里同时把羽毛根骨骼的名字刷新一遍。
        返回 False 表示校验失败（调用方应中断）
        """
        ok = True
        reparent = self.chk_parent.isChecked()
        for i, feather in enumerate(feathers):
            # 层级可能被上一次生成/拆除改过，长名一律按短名重新解析
            root = resolve_joint(short_name(feather['root']))
            arm = resolve_joint(short_name(feather['arm']))
            short = short_name(feather['root'])
            if root is None or arm is None:
                cmds.warning('第 %d 根羽毛没有填「对应手臂骨骼」' % (i + 1))
                ok = False
                continue
            if get_parent(root) != arm:
                if not reparent:
                    cmds.warning('第 %d 根羽毛（%s）没有挂在对应手臂骨骼（%s）下，'
                                 '请勾选「羽毛根骨骼自动挂到对应手臂骨骼下」'
                                 % (i + 1, short, short_name(arm)))
                    ok = False
                    continue
                cmds.parent(root, arm)
            # 刷新长名（层级变了）
            feather['root'] = as_joint(short) or feather['root']
            feather['arm'] = arm
        return True if ok else None

    def select_feather_ctrls(self):
        """一键全选所有羽毛的朝向控制器，方便批量调整朝向"""
        names = []
        for ctrl_name, info in self.rigs.items():
            if not cmds.objExists(ctrl_name):
                continue
            names += [e['ctrl'] for e in info.get('extras', [])
                      if e.get('ctrl') and cmds.objExists(e['ctrl'])]
        if not names:
            self.label_info.setText('没有找到羽毛朝向控制器，请先生成翅膀绑定')
            return
        cmds.select(names, replace=True)
        self.label_info.setText('已选中 %d 个羽毛朝向控制器，用旋转工具即可批量调整朝向'
                                % len(names))

    def set_helpers_visible(self, on):
        """显示/隐藏内部解算用的「驱动样条 + 定位器」，返回操作了几个

        这两样是羽毛贴合样条用的中间物，不是给动画师用的控制器：
        「收起偏转」写在偏移组上，动画师动的是圆环（朝向）和末端方块（末端）。
        44 根羽毛会产生 44 条样条曲线 + 132 个定位器，默认全开的话视口里
        全是线，翅膀本身都看不清 —— 所以生成时就把它们藏起来，需要排查
        约束/样条时再用界面上的开关显出来。
        """
        n = 0
        for ctrl_name, info in self.rigs.items():
            if not cmds.objExists(ctrl_name):
                continue
            for e in info.get('extras', []):
                for name in [e.get('curve')] + list(e.get('locators') or []):
                    if name and cmds.objExists(name):
                        cmds.setAttr(name + '.visibility', 1 if on else 0)
                        n += 1
        return n

    def on_helpers_toggled(self, on):
        n = self.set_helpers_visible(bool(on))
        if not n:
            self.label_info.setText('还没有绑定，先生成翅膀绑定')
            return
        self.label_info.setText('%s %d 个辅助物体（驱动样条/定位器）'
                                % ('已显示' if on else '已隐藏', n))

    def feather_geometries(self, info):
        """扫出所有「受羽毛骨骼影响」的 (skinCluster, 几何) 组合（去重）

        自检和「羽毛权重归一」都用它：从每根羽毛链的骨骼反查 skinCluster，
        再取这些 skinCluster 的几何。注意网格上可能挂着不打算改的皮肤簇，
        所以只认「影响列表里有羽毛骨骼」的那些。
        """
        seen, out = set(), []
        for e in info.get('extras', []):
            if not e.get('root'):
                continue
            r = resolve_joint(short_name(e['root']))
            if r is None:
                continue
            sks = set()
            for b in get_longest_chain(r):
                sks.update(cmds.listConnections(b, s=False, d=True,
                                                type='skinCluster') or [])
            for sk in sks:
                if not cmds.objExists(sk):
                    continue
                for g in (cmds.skinCluster(sk, q=True, geometry=True) or []):
                    if (sk, g) in seen or not cmds.objExists(g):
                        continue
                    seen.add((sk, g))
                    out.append((sk, g))
        return out

    def normalize_feather_weights(self, quiet=False):
        """把羽毛的权重改成刚性：**每张卡只跟一根羽毛**，卡上顶点权重 1

        用户的要求就是「羽毛对应的骨骼权重=1」：羽毛卡要刚性跟着自己那根羽毛，
        不被手臂或旁边的羽毛拽着变形（渲染出来才不会糊、不会互相拉扯）。

        归属是**整张卡**定的，不是逐顶点。逐顶点（每根顶点各自找最近的骨骼）看着
        合理，在这类密集羽毛上会直接把卡剪开 —— 详述见下面那段注释，实测收起到底
        「卡片上顶点两两距离」平均变 28.2%、最差 51.8%（刚性本该是 0），改成整卡
        一根链之后是 7.5% / 43.6%。

        对「收起有多紧」影响不大 —— 这里踩过一次坑，记下来：
        早期夹具里用了 skinPercent(..., transformValue=[(骨,1.0)], normalize=True)，
        那**不会**清掉顶点上原来那根，结果每个顶点两根都 1.0、合计 2.0，
        形变等于两个骨骼矩阵相加（被手臂拽着走），量出来「收紧 20~46%」是假的。
        把夹具改成正确写法（整条影响列表一次性给全）之后重测：
        三个场景收到底 65.4→57.2%、44.0→43.2%、45.2→49.4%（稀疏有改善，密集基本持平）。

        只动「几何上属于羽毛」的顶点（离羽毛骨骼比离手臂骨骼更近的那些）：
        手臂网格、羽毛根部那一圈转轴顶点保持原样，不会把角色别的地方改坏。

        整个过程放在一个撤销块里，Ctrl+Z 一次就能撤回。
        """
        ctrl = self.current_ctrl
        if not ctrl or not cmds.objExists(ctrl):
            self.label_info.setText('还没有绑定，先生成翅膀绑定')
            return
        info = self.rigs.get(ctrl)
        if not info:
            self.label_info.setText('这套绑定没有登记信息，重新生成一次再改权重')
            return
        # 整段在**展开姿态**下做，而且必须在读骨骼坐标之前就拨回去：下面
        # chains / arm_chains 都是**当场读世界坐标**建的，姿势不对齐就会拿收起
        # 姿态的坐标去判静止姿态的顶点，一个顶点都过不了。
        # 拨回来这一步单独反悔不了（没包在撤销块里），但下面的块里会把收起程度
        # 一起恢复，所以用户一次 Ctrl+Z 仍然干净。
        prev_fold = self.spin_fold.value()
        self.set_fold(0)
        cmds.refresh(force=True)
        arm_bones = sorted(set((info.get('offsets') or {}).keys()))
        chains = []
        for e in info['extras']:
            if not e.get('root'):
                continue
            r = resolve_joint(short_name(e['root']))
            if r is None:
                continue
            ch = get_longest_chain(r)
            if ch:
                chains.append((short_name(e['root']), ch,
                               [om.MVector(*world_pos(b)) for b in ch]))
        geos = self.feather_geometries(info)
        if not (arm_bones and chains and geos):
            self.label_info.setText('没有找到羽毛网格的蒙皮，无法归一权重')
            return
        arm_chains = arm_body_chains(info)
        feather_pts_lists = [pts for _n, _c, pts in chains]
        # 羽毛骨骼的短名全集 —— 用来判「一块几何的权重落在羽毛上还是手臂上」
        feather_names = set(short_name(b) for _n, ch, _p in chains for b in ch)

        all_bones = [(name, b, om.MVector(*world_pos(b)))
                     for name, ch, _ in chains for b in ch]
        cmds.undoInfo(openChunk=True, chunkName='Wing Feather Weights')
        try:
            n_vtx, n_geo, n_skip = 0, 0, 0
            n_pose = 0      # 因为「当前姿态≠绑定姿态」而在当前姿态下带位移的顶点数
            # ---- 第一遍：把每块几何拆成「卡」，给每张卡算一行代价 ----
            # 归属必须**整张卡一根链**。逐顶点（每个顶点各找自己最近的骨骼）
            # 看着合理，在密集羽毛上会把卡剪开：一张卡的顶点会散到 3~7 根羽毛上
            # （只有 35% 的顶点落在自己那根羽毛上 —— 相邻两条骨链挨得比卡片
            # 自己的半宽还近，「最近的骨骼」根本分不出是哪根），收起时同一张卡
            # 被几根羽毛往不同方向拽。实测真翼形 38 张卡收起到底，
            # 「卡片上顶点两两距离」平均变 28.2%、最差 51.8%（刚性本该是 0）；
            # 整卡一根链之后是 1.4%。
            #
            # 走连通块而不是整块网格投票：合并成一个网格的模型里，各张卡之间
            # 通常没有焊在一起，连通块正好就是一张张卡。
            cards_meta = []
            for sk, g in geos:
                try:
                    nv = cmds.polyEvaluate(g, v=True)
                except Exception:
                    continue
                if not nv:
                    continue
                infl = cmds.skinCluster(sk, q=True, influence=True) or []
                # 影响列表按**短名**查表：写入的骨骼必须真的在这条蒙皮的影响列表里，
                # 否则 transformValue 里一个都匹配不上，整串权重会被写成 0 ——
                # 顶点谁都不跟，网格留在绑定姿态上。
                name_set = set(short_name(x) for x in infl)
                for comp in (self._mesh_components(g, nv) or [list(range(nv))]):
                    if len(comp) < 3:
                        continue
                    cpts = []
                    for vi in comp:
                        if vi >= nv:
                            continue
                        cpts.append((vi, om.MVector(
                            *cmds.xform('%s.vtx[%d]' % (g, vi), q=True,
                                        ws=True, t=True))))
                    if len(cpts) < 3:
                        continue
                    span = max((a - b).length()
                               for _i, a in cpts for _j, b in cpts)
                    if span < 1e-9:
                        continue
                    # 判「这张卡算不算羽毛」——**按卡判，不按整块几何判**：
                    # 满足下面任一条就算：
                    #   a) 有顶点伸到离手臂很远的地方（真羽毛卡总会戳出去一大截）；
                    #   b) 它的权重主要落在羽毛骨上（正常蒙皮的羽毛卡都满足）。
                    # 为什么要两条：只按距离判会误伤翼中段那几根主飞羽 ——
                    # 它们的根部就贴在手臂上（实测 primary_mesh04/05 只有 44% 的采样点
                    # 算「离羽毛骨更近」），整块被判成手臂、一个字都不改，于是那两张卡
                    # 保持用户原来的权重、散在 3 根羽毛上，收起时被剪开（剩下的那 18%）。
                    # 只按权重判又会漏掉**绑错了**的卡（羽毛卡被绑到手臂骨上，
                    # 恰恰是最需要修的那种）。两条并用，两个方向都不会漏。
                    far = max(dist_to_bone_chains(p, arm_chains)
                              for _vi, p in cpts)
                    clear = far > 0.35 * span
                    if not clear:
                        fw = aw = 0.0
                        for _vi, _p in cpts[:6]:
                            vals = cmds.skinPercent(
                                sk, '%s.vtx[%d]' % (g, _vi), q=True,
                                value=True) or []
                            for x, val in zip(infl, vals):
                                if val <= 0.0:
                                    continue
                                if short_name(x) in feather_names:
                                    fw += val
                                else:
                                    aw += val
                        if fw <= aw:
                            continue
                    row, clen = self._card_cost_row([p for _vi, p in cpts],
                                                    arm_chains, chains)
                    if row is None:
                        continue
                    cards_meta.append({
                        'sk': sk, 'g': g, 'infl': infl, 'name_set': name_set,
                        'cpts': cpts, 'row': row, 'clen': clen,
                        'span': span, 'clear': clear})

            # ---- 第二遍：全局**一对一**分配 —— 一根羽毛只能被一张卡认领 ----
            # 逐卡各挑最近的链会「两张卡抢同一条链」：覆羽和它压在下面那根飞羽的
            # 根骨骼只差 0.086，谁快算谁的，被抢的那根羽毛就没人认了。
            # 全局一对一之后，被抢的羽毛必须去找自己那张卡，总代价下降、配对变准：
            # 实测真翼形 38 张卡，逐卡挑认对 35、全局一对一认对 38。
            # 卡比羽毛多时（用户把一张卡拆成好几块）没法一一对应，退回逐卡挑最近的。
            assign = None
            if cards_meta and len(cards_meta) <= len(chains):
                assign = hungarian_assign([c['row'] for c in cards_meta])

            def _pick(meta, k):
                """这张卡归哪条链：全局一对一的结果优先，退化时逐卡挑最近的"""
                if assign is not None:
                    return assign[k]
                return min(range(len(chains)), key=lambda t: meta['row'][t])

            def _chlen(j):
                cp = chains[j][2]
                return sum((cp[i + 1] - cp[i]).length()
                           for i in range(len(cp) - 1))

            def _is_big(meta, j):
                """这块连通块是不是「焊接成一大块」（远大于一根羽毛的骨链）"""
                return (len(chains[j][2]) > 1 and _chlen(j) > 1e-6
                        and meta['span'] > 2.5 * _chlen(j))

            # ---- 第三遍：按几何写权重 ----
            by_geo = {}
            for k, meta in enumerate(cards_meta):
                by_geo.setdefault((meta['sk'], meta['g']), []).append(k)
            for (sk, g), idxs in by_geo.items():
                try:
                    nv = cmds.polyEvaluate(g, v=True)
                except Exception:
                    continue
                if not nv:
                    continue
                infl = cards_meta[idxs[0]]['infl']
                name_set = cards_meta[idxs[0]]['name_set']
                before = {}
                old_w = {}
                for vi in range(nv):
                    before[vi] = om.MVector(*cmds.xform('%s.vtx[%d]' % (g, vi),
                                                        q=True, ws=True, t=True))
                # 旧权重（回滚用）批量读；批量读不成就逐点读 —— 只能用 q=True, value=True
                # （Maya 的 flag 前缀匹配会把 transformValue 拆成 transform + Value，
                # 查询模式直接报错）；返回顺序与 influence 列表一一对应。
                bulk = self._bulk_weights(sk, g, infl, nv)
                if bulk is not None:
                    for vi in range(nv):
                        old_w[vi] = list(zip(infl, bulk[vi]))
                else:
                    for vi in range(nv):
                        ws_old = cmds.skinPercent(sk, '%s.vtx[%d]' % (g, vi),
                                                  q=True, value=True) or []
                        old_w[vi] = list(zip(infl, ws_old))
                changed = 0
                written = []          # 写过的 (顶点号, 目标骨短名)，回读验证用
                plan = {}             # 目标骨短名 → [顶点号]，批量写用
                for k in idxs:
                    meta = cards_meta[k]
                    j = _pick(meta, k)
                    ch_own = chains[j][1]
                    cp_own = chains[j][2]
                    # 「这块连通块是不是一整张卡」：拿它跟**这条链的长度**比。
                    # 焊接成一大块（手臂+羽毛焊在一起）时连通块会远大于一根羽毛，
                    # 那就不该整块绑成一根羽毛，退回逐顶点。
                    # （以前是拿「卡片自己的长度」比，两者本来就差不多，这条永远不触发。）
                    #
                    # 「链条本身是不是有效长度」必须一起判：只有一节骨骼的羽毛
                    # （实测 build_bird_wing 的 single 类）链长天然是 0，除以 0 之后
                    # 任何卡都「远大于链」→ 整张卡退回逐顶点、4 个顶点散到旁边 3 根
                    # 羽毛上（实测那张卡收起时边长变 38.9%）。一节骨骼的羽毛卡片
                    # 本来就该整张刚性跟这一节。
                    big = _is_big(meta, j)
                    for vi, p in meta['cpts']:
                        # 真的长在手臂里的顶点不要动（让手臂网格继续跟手臂）。
                        # 判据要跟卡片的尺度比：羽毛卡根部那几个顶点本来就贴在手臂上、
                        # 「离手臂更近」，但它们是卡的一部分、必须跟着自己的链走 ——
                        # 不按尺度判的话，翼中段那两张主飞羽卡会有 11 个顶点被留成
                        # 原来的权重、散到别的羽毛上（实测 primary_mesh04 出现
                        # primary04×11 + primary05×7）。
                        # 卡片明明白白戳在空中的（clear）就整张全改：它整块都是羽毛。
                        if not meta['clear'] and not big:
                            darm = dist_to_bone_chains(p, arm_chains)
                            if darm <= dist_to_bone_chains(p, feather_pts_lists) \
                                    and darm < 0.15 * max(meta['span'], 1e-9):
                                n_skip += 1
                                continue
                        if big:
                            onm, _b, _q = min(all_bones,
                                              key=lambda kv: (p - kv[2]).length())
                            owners = [(b, q) for name, ch, pts in chains
                                      if name == onm for b, q in zip(ch, pts)]
                        else:
                            owners = list(zip(ch_own, cp_own))
                        b = min(owners, key=lambda kv: (p - kv[1]).length())[0]
                        # 一定要按**短名**比：这里 ch 里的骨骼是长名（|a|b|c），
                        # 而 skinCluster(q=True, influence=True) 返回的是短名，
                        # 直接 x == b 永远不成立 → 整个影响列表全被写成 0.0，
                        # 顶点一根骨骼都不跟、网格被冻在绑定姿态上。
                        # 实测（羽毛合并成一个网格）：写完「收起」完全不生效，
                        # 展开 5.72 → 收起 5.72（100%），而分开的卡片场景却看着正常。
                        target = short_name(b)
                        if target not in name_set:
                            n_skip += 1
                            continue
                        plan.setdefault(target, []).append(vi)
                # 批量写：同一根骨的目标顶点一次写完。
                # skinPercent 支持一次给一串顶点（实测 22 个顶点一次调用，权重与逐点写
                # 完全一致），所以按目标骨骼分组就够了 —— 逐顶点写 1728 次要 5 秒，
                # 分组之后是「网格 × 该网格用到的骨骼数」次（96 根羽毛约 300 次）。
                for target, vl in plan.items():
                    vals = [(x, 1.0 if short_name(x) == target else 0.0)
                            for x in infl]
                    cmds.skinPercent(sk, ['%s.vtx[%d]' % (g, i) for i in vl],
                                     transformValue=vals, normalize=False)
                    written.extend((i, target) for i in vl)
                    changed += len(vl)
                # 防呆：正常情况下改权重**不该让模型动一下**（骨骼精确复现建模姿态，
                # 生成前后世界矩阵逐元素相同，实测偏差 0.00000000）。
                #
                # 但「模型当前姿态 ≠ 绑定姿态」时（被摆过姿势、带着动画、或者绑定
                # 姿态本来就不是现在这个姿态），把顶点从「几根骨骼的混合」改成
                # 「一根」**必然**带一点位移 —— 那正是这个按钮承诺的结果（卡片变刚性）。
                # 所以**位移本身不能当错误判据**：实测在「羽毛静止时带 ±12° 离面角、
                # 且先转骨骼后绑」的夹具上，只看位移会把 38 张卡全部回滚，界面提示
                # 「0 个网格 / 0 个顶点 / 跳过 684」—— 用户看到的就是「点了没反应，
                # 收起照样被剪开」。
                #
                # 现在改成：位移超阈值时**把权重读回来直接验** —— 每个写过的顶点必须
                # 恰好一根影响 = 1.0 且就是打算写的那根。验过了就接受（并如实说明这次
                # 位移来自姿态差），没验过才回滚（那才是真的写坏了）。
                cmds.refresh(force=True)
                moved = 0.0
                for vi in range(nv):
                    q = om.MVector(*cmds.xform('%s.vtx[%d]' % (g, vi), q=True,
                                               ws=True, t=True))
                    moved = max(moved, (q - before[vi]).length())
                if changed and moved > 1e-3:
                    ok, why = self._verify_written_weights(sk, g, infl, written)
                    if not ok:
                        print('[翅膀绑定]   回滚 %s：权重写坏了（%s）'
                              % (short_name(g), why))
                        for vi in range(nv):
                            if old_w[vi]:
                                cmds.skinPercent(sk, '%s.vtx[%d]' % (g, vi),
                                                 transformValue=old_w[vi],
                                                 normalize=False)
                        n_skip += changed
                        changed = 0
                    else:
                        n_pose += changed
                        print('[翅膀绑定]   %s：模型当前姿态不是绑定姿态，改完权重'
                              '在当前姿态下最多挪 %.4f（卡片变刚性的正常位移，已保留）'
                              % (short_name(g), moved))
                if changed:
                    n_geo += 1
                    n_vtx += changed
        finally:
            self.set_fold(prev_fold)
            cmds.undoInfo(closeChunk=True)
        cmds.refresh(force=True)
        # 「当前姿态≠绑定姿态」时改权重会在当前姿态下带一点位移（正常，见上面那段
        # 注释）。这件事必须说出来，否则用户看到模型动了一下、又没被告知，会以为改坏了。
        pose_note = ''
        if n_pose:
            pose_note = ('；其中 %d 个顶点因为模型当前姿态不是绑定姿态，'
                         '改完在当前姿态下有少量位移（卡片变刚性带来的，正常）'
                         % n_pose)
        summary = ('羽毛权重已刷成刚性：%d 个网格 / %d 个顶点'
                   '（另有 %d 个顶点本来就该跟手臂，未改动）%s'
                   % (n_geo, n_vtx, n_skip, pose_note))
        if not quiet:
            self.label_info.setText('已把 %d 个羽毛网格的 %d 个顶点权重改成 1'
                                    '（另有 %d 个顶点本来就该跟手臂，未改动）%s'
                                    '｜可 Ctrl+Z 撤回'
                                    % (n_geo, n_vtx, n_skip, pose_note))
        print('[翅膀绑定] 羽毛权重归一: %d 个网格 / %d 个顶点（跳过 %d）%s'
              % (n_geo, n_vtx, n_skip, pose_note))
        return summary

    @staticmethod
    def _bulk_weights(sk, g, infl, nv):
        """一次读回整块几何的权重，返回 [[w…], …]（长度 nv，列序与 infl 一致）

        为什么要批量读：逐顶点 cmds.skinPercent 查一次约 3ms，96 根羽毛 1728 个顶点
        光「存旧权重」就 5 秒 —— 实测整段权重归一 12.6 秒里 10.7 秒全花在
        skinPercent 上（cProfile）。这里用 API 1.0 的 MFnSkinCluster.getWeights
        一次拿完（API 2.0 里没有 MFnSkinCluster）。

        顺序是**关键**（以前踩过 getAttr(weightList[i].weights) 与 influence 顺序
        对不上的坑）：这里显式按短名把 cmds 的 influence 列表映射成 API 的下标再请求，
        所以列序一定与 infl 一致；对不上（骨骼不在簇里、拿不到 API）就返回 None，
        调用方退回逐点读，宁可慢也不写错。
        """
        try:
            import maya.OpenMaya as om1
            import maya.OpenMayaAnim as oma1
        except Exception:
            return None
        try:
            sel = om1.MSelectionList()
            sel.add(sk)
            node = om1.MObject()
            sel.getDependNode(0, node)
            fn = oma1.MFnSkinCluster(node)
            arr = om1.MDagPathArray()
            fn.influenceObjects(arr)
            api_names = [short_name(arr[i].partialPathName())
                         for i in range(arr.length())]
            want = [short_name(x) for x in infl]
            if len(api_names) != len(want) or sorted(api_names) != sorted(want):
                return None
            ids = om1.MIntArray()
            for n in want:
                ids.append(api_names.index(n))
            # 注意 g 通常**本身就是 shape**（feather_geometries 取自
            # skinCluster(q=True, geometry=True)，返回的就是 shape 名）：
            # listRelatives 找不到就说明 g 是 shape，直接用。
            shapes = cmds.listRelatives(g, s=True, type='mesh') or []
            if shapes:
                shape = shapes[0]
            elif cmds.nodeType(g) == 'mesh':
                shape = g
            else:
                return None
            dsel = om1.MSelectionList()
            dsel.add(shape)
            dag = om1.MDagPath()
            dsel.getDagPath(0, dag)
            comp = om1.MFnSingleIndexedComponent()
            cobj = comp.create(om1.MFn.kMeshVertComponent)
            for vi in range(nv):
                comp.addElement(vi)
            flat = om1.MDoubleArray()
            fn.getWeights(dag, cobj, ids, flat)
            if flat.length() != nv * len(want):
                return None
            n_i = len(want)
            return [[flat[vi * n_i + k] for k in range(n_i)] for vi in range(nv)]
        except Exception:
            return None

    @staticmethod
    def _verify_written_weights(sk, g, infl, written):
        """把刚写过的权重**读回来验**：每个顶点必须恰好一根影响 = 1.0，且是目标那根

        为什么要这一步：只看「模型有没有动」分不清两件事 ——
        「当前姿态≠绑定姿态导致的正常位移」和「权重被写坏了」。skinPercent 会静默
        失败（骨骼不在这个簇里、影响列表对不上、normalize 把值改掉），那时顶点会被
        甩到别的骨骼上；读回来一看就知道。

        返回 (是否全部正确, 第一个不对的说明)。
        """
        for vi, target in written:
            vals = cmds.skinPercent(sk, '%s.vtx[%d]' % (g, vi), q=True,
                                    value=True) or []
            on = [short_name(x) for x, v in zip(infl, vals) if v > 0.5]
            if len(on) != 1 or on[0] != target:
                return False, 'vtx[%d] 读回来是 %s（应为 %s）' % (
                    vi, on or '空', target)
        return True, ''

    @staticmethod
    def _mesh_components(shape, nv):
        """网格的连通块（按边连通），返回 [[顶点号…], …]；拿不到就返回 None

        羽毛卡在合并网格里通常仍是互不相连的一片片，所以连通块≈一张张卡。
        用 polyInfo 的边-顶点表做并查集，一次调用拿全，不用逐边问。
        """
        try:
            lines = cmds.polyInfo(shape, edgeToVertex=True) or []
        except Exception:
            return None
        if not lines:
            return None
        parent = dict((v, v) for v in range(nv))

        def find(x):
            r = x
            while parent.get(r, r) != r:
                r = parent[r]
            while parent.get(x, x) != r:
                parent[x], x = r, parent[x]
            return r

        for ln in lines:
            nums = [int(t) for t in ln.replace(':', ' ').split()
                    if t.lstrip('-').isdigit()]
            if len(nums) < 3:
                continue
            a, b = nums[1], nums[2]
            if a not in parent or b not in parent:
                continue
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
        groups = {}
        for v in range(nv):
            groups.setdefault(find(v), []).append(v)
        return list(groups.values())

    @staticmethod
    def _card_cost_row(pts, arm_chains, chains):
        """给一张卡算「它跟每条羽毛链有多像」的一整行代价（越小越像）

        三项都是可量的：
          1. 卡片**根端**（离手臂最近的那个顶点）离这条链的**根骨骼**多远 ——
             羽毛的根骨骼就立在自己根部，正经的东家这一项≈0；
          2. 这条链比卡片还长出去多少 —— 骨链一般只铺到卡片 2/3 长左右，
             「比卡片还长」说明这是压在卡片上的那根长飞羽，不是它的东家；
          3. 朝向对不对得上。
        返回 (代价行, 卡片长度)；卡片退化成一个点时返回 (None, 0)。
        """
        if not pts:
            return None, 0.0
        root_p = min(pts, key=lambda p: dist_to_bone_chains(p, arm_chains))
        tip_p = max(pts, key=lambda p: (p - root_p).length())
        card_len = (tip_p - root_p).length()
        if card_len < 1e-9:
            return None, 0.0
        axis = (tip_p - root_p) / card_len
        row = []
        for _name, ch, cp in chains:
            if len(cp) < 2:
                row.append(1e6)
                continue
            clen = sum((cp[k + 1] - cp[k]).length() for k in range(len(cp) - 1))
            if clen < 1e-9:
                row.append(1e6)
                continue
            cdir = (cp[-1] - cp[0]).normal()
            s = (root_p - cp[0]).length() / card_len
            s += max(0.0, clen - card_len) / card_len
            s += 0.5 * (1.0 - abs(axis * cdir))
            row.append(s)
        return row, card_len

    def _card_shear(self, info):
        """收起到底时羽毛卡「被拉长/剪开」的程度（0~1，越接近 0 越好）

        量法：只看**同一条边上的两个顶点**，比较它的长度在展开/收起之间的变化。
        权重=1 的刚性卡片被刚性变换搬来搬去时，边长一点都不会变 ——
        所以这个数就是「卡片有没有被拉坏」的直接度量（剩下的那点来自羽毛自己
        3 节骨骼的正常弯曲）。实测真翼形 38 张卡：默认那套绑定 27%、
        点一次「羽毛权重=1」之后 0.7%。

        为什么用边而不是「随便抽两个顶点」：合并成一个网格的模型里，抽到的两点
        可能分属**两张卡**，而不同卡本来就跟着不同羽毛跑 —— 跨卡配对会把卡与卡
        之间的正常相对运动算成形变（实测真能报出 232%，完全失真）。
        边永远在一张卡内部（各张卡之间没有焊在一起的边），所以不会犯这个错。
        """
        geos = self.feather_geometries(info)
        if not geos:
            return None
        blocks = []
        for _sk, g in geos:
            try:
                nv = cmds.polyEvaluate(g, v=True)
            except Exception:
                continue
            if not nv:
                continue
            pairs = []
            for ln in (cmds.polyInfo(g, edgeToVertex=True) or []):
                nums = [int(t) for t in ln.replace(':', ' ').split()
                        if t.lstrip('-').isdigit()]
                if len(nums) >= 3:
                    pairs.append((nums[1], nums[2]))
            for comp in (self._mesh_components(g, nv) or [list(range(nv))]):
                if len(comp) < 3:
                    continue
                cs = set(comp)
                cp = [(a, b) for a, b in pairs if a in cs and b in cs][:400]
                if len(cp) < 3:
                    continue
                step = max(1, len(comp) // 60)
                vids = comp[::step][:60]
                need = sorted(set(vids) | set([v for pr in cp for v in pr]))
                blocks.append((g, cp, vids, need))
        if not blocks:
            return None
        snaps = {}
        try:
            for pct in (0, 100):
                self.set_fold(pct)
                cmds.refresh(force=True)
                snaps[pct] = [[om.MVector(*cmds.xform('%s.vtx[%d]' % (g, vi),
                                                      q=True, ws=True, t=True))
                               for vi in need]
                              for g, _cp, _vids, need in blocks]
        except Exception:
            return None
        finally:
            self.set_fold(0)
            cmds.refresh(force=True)
        worst = 0.0
        for bi, (g, cp, vids, need) in enumerate(blocks):
            p0 = snaps[0][bi]
            p1 = snaps[100][bi]
            idx = dict((vi, k) for k, vi in enumerate(need))
            scale = max(((p0[idx[a]] - p0[idx[b]]).length()
                         for a in vids for b in vids), default=0.0) or 1.0
            dmax = 0.0
            for a, b in cp:
                la = (p0[idx[a]] - p0[idx[b]]).length()
                lb = (p1[idx[a]] - p1[idx[b]]).length()
                dmax = max(dmax, abs(lb - la))
            worst = max(worst, dmax / scale)
        return worst

    def on_normalize_weights(self):
        """「羽毛权重=1」按钮：会覆盖用户现有的蒙皮权重，所以先确认一次"""
        ctrl = self.current_ctrl
        info = self.rigs.get(ctrl) if ctrl else None
        if not info:
            self.label_info.setText('还没有绑定，先生成翅膀绑定')
            return
        n = len(self.feather_geometries(info))
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle('羽毛权重归一')
        box.setText('把受羽毛骨骼影响的 %d 个网格里的羽毛顶点权重改成 1（刚性）？\n\n'
                    '这会覆盖这些顶点现有的权重。手臂网格、以及羽毛根部那一圈'
                    '贴着转轴的顶点不动。\n操作可一次 Ctrl+Z 撤回。' % n)
        box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        if box.exec_() != QtWidgets.QMessageBox.Yes:
            self.label_info.setText('已取消，权重没有改动')
            return
        self.normalize_feather_weights()

    def self_check(self):
        """自检：把「这套绑定到底行不行」的关键指标算出来，返回 [(名称, 是否达标, 说明)]

        不用渲染，秒出。用户在自己模型上生成完，最需要知道的是「哪一环没达标」——
        不然只能凭感觉说「效果不好」。这里量的十件事都是可判定的：

          1 静止姿态还原  fold=0 时每个驱动通道必须回到登记表里的静止值
                          （回不去 = 折叠会污染他的模型，最严重的一类问题）
          2 骨骼零形变    0~100 全程骨长不变（变了 = 解算把骨骼拉长了）
          3 收起紧凑度    羽尖到肩的距离收到底相对展开态的比例（越小越收得紧）
          4 垂直基线守恒  转手臂的 FK 圆环摆姿势时，羽毛与手臂的夹角不变
          5 FK 控制器能驱动骨骼  转那个圆环，骨骼真的动了
                          （不单独量这一条的话，「圆环根本没接线」也会让第 4 项通过）
          6 羽毛权重归属  羽毛网格上「跟着羽毛骨骼而不是手臂」的权重占比
                          （用户要求权重=1：混到手臂上，羽毛就会被手臂拽着走形）
          7 控制器齐全    每根羽毛的偏移组/朝向圆环/末端方块都在
          8 羽毛贴合样条  每节骨骼与它样条上的定位器重合（点约束+方向约束生效）
          9 驱动关键帧齐全  手臂各关节与每根羽毛偏移组的 rotate 都有驱动曲线
         10 羽毛穿插合理  收起后叠在一起的羽毛卡没有互相穿过、也没有完全重合
        """
        ctrl = self.current_ctrl
        if not ctrl or not cmds.objExists(ctrl):
            self.label_info.setText('还没有绑定，先生成翅膀绑定')
            return None
        info = self.rigs.get(ctrl)
        if not info:
            self.label_info.setText('这套绑定没有登记信息，重新生成一次再做自检')
            return None
        res = []

        def add(name, ok, text):
            res.append((name, bool(ok), text))

        def wpos(n):
            return om.MVector(*cmds.xform(n, q=True, ws=True, t=True))

        chain = [j for j in info.get('joints', []) if cmds.objExists(j)]
        if not chain:
            # 旧版本存的文件里没有登记骨骼列表，自检做不了。别直接崩，说清楚就行。
            self.label_info.setText('这套绑定没有登记骨骼信息，重新生成一次再做自检')
            cmds.warning('这套绑定是旧版本存下的，登记信息里没有骨骼列表，'
                         '重新生成一次（或按表里的骨骼重新生成）再做自检')
            return None
        chain_set = set(chain)
        extras = [e for e in info.get('extras', []) if e.get('root')]
        roots = []
        for e in extras:
            r = resolve_joint(short_name(e['root']))
            if r is not None:
                roots.append(r)
        # info['joints'] 存的是「手臂链 + 羽毛链」。手臂链只取**第一个羽毛根之前**
        # 的那一段：层叠是沿翼面法线把羽毛根平移出去的（见 feather_targets），
        # 「手臂骨骼 → 羽毛根」那一跳的距离当然会跟着变，它不该算进骨骼形变。
        root_set = set(roots)
        arm_chain = []
        for j in chain:
            if j in root_set:
                break
            arm_chain.append(j)
        arm_set = set(arm_chain)
        # 第 1 项量的是「fold=0 时各驱动通道有没有回到静止值」，所以自检必须自己
        # 先把收起拨回 0。以前是调用方负责（界面按钮会先拨 0），从脚本里直接调
        # self_check() 时会带着当时的收起点，第 1 项就假报失败。
        self.set_fold(0)
        cmds.refresh(force=True)

        def kids(j):
            return [c for c in child_joints(j) if c in arm_set]

        def bone_lens():
            out = {}
            # 手臂链上相邻两节
            for j in arm_chain:
                for c in kids(j):
                    out[(short_name(j), short_name(c))] = (wpos(c) - wpos(j)).length()
            # 每根羽毛**自己链上**相邻两节：羽毛骨骼是被点/方向约束拉到样条上的，
            # 只量手臂就漏了这一半 —— 收起偏转的驱动、层叠的平移都写在羽毛这边，
            # 正是最需要盯住的地方。
            # 刻意不量「手臂骨骼 → 羽毛根骨骼」那一跳：层叠是沿翼面法线把羽毛根
            # 平移出去（那就是层与层之间的深度差），这一跳的距离本来就会变。
            for r in roots:
                ch = get_longest_chain(r)
                for i in range(len(ch) - 1):
                    out[(short_name(ch[i]), short_name(ch[i + 1]))] = (
                        wpos(ch[i + 1]) - wpos(ch[i])).length()
            return out

        # 1) 静止姿态还原
        # 比的是**旋转本身**（旋转矩阵），不是欧拉角数字：同一个旋转既能写成
        # (-180, 0, 0) 也能写成 (180, 0, 0)，重开文件后 Maya 会把 -180 归一成 180，
        # 逐分量比就会假报 360 度偏差（实测打开演示场景点自检就是这样，明明没坏）。
        dev = 0.0
        who = ''
        for j, rot in (info.get('rest_rotate') or {}).items():
            if not cmds.objExists(j):
                continue
            order = cmds.getAttr(j + '.rotateOrder')
            cur = list(cmds.getAttr(j + '.rotate')[0])
            m0 = euler_matrix(tuple(cur), order)
            m1 = euler_matrix(tuple(rot), order)
            d = max(abs(m0[i] - m1[i]) for i in (0, 1, 2, 4, 5, 6, 8, 9, 10))
            if d > dev:
                dev = d
                who = '（%s 现在 %s，登记 %s）' % (short_name(j),
                                              [round(x, 3) for x in cur],
                                              [round(x, 3) for x in rot])
        add('静止姿态还原', dev < 1e-6,
            'fold=0 时旋转矩阵最大元素差 %.8f%s' % (dev, who))

        # 1b) 骨骼静止**朝向**还原
        #     上面那一项只查「驱动通道的旋转值」。骨骼还可能被别的东西（样条上的
        #     方向约束、重新父子、翻转的 jointOrient）把**世界朝向**转过去，而
        #     驱动通道看起来完全正常 —— 实测真翼形 38 根羽毛里有 44 根中招，
        #     世界矩阵某个元素差了整整 2.0（＝绕自身轴翻转 180°），位置一点没变，
        #     所以只比位置的自检一路绿灯，可卡片已经被翻了个面：收起=0 时网格顶点
        #     最大偏离建模姿态 0.93、整张卡包围盒差 0.52，渲出来一半卡片是背面。
        #     这里拿生成前存下的世界矩阵 3x3 逐根比。
        r3 = info.get('rest_rot3') or {}
        flip = []
        worst_r3 = 0.0
        worst_r3_j = ''
        if r3:
            fj = []
            for r in roots:
                fj += get_longest_chain(r)
            check = list(chain) + list(roots) + [x for x in fj if x not in roots]
            for j in check:
                k = short_name(j)
                if k not in r3 or not cmds.objExists(j):
                    continue
                m = cmds.xform(j, q=True, ws=True, m=True)
                cur = [m[0], m[1], m[2], m[4], m[5], m[6], m[8], m[9], m[10]]
                d = max(abs(a - b) for a, b in zip(cur, r3[k]))
                if d > worst_r3:
                    worst_r3, worst_r3_j = d, k
                if d > 1e-3:
                    flip.append((d, k))
            add('骨骼静止朝向还原', not flip,
                '收起=0 时每根骨骼的世界朝向与生成前一致：%d/%d 根达标'
                '（最大差 %.6f%s）%s'
                % (len(check) - len(flip), len(check), worst_r3,
                   '（' + worst_r3_j + '）' if worst_r3_j else '',
                   '' if not flip else
                   '｜**%d 根骨骼被翻过去了**（最大差 %.3f ≈ 180° 翻转）：'
                   '这些羽毛卡在展开姿态下就已经不是建模时的样子了。'
                   '原因通常是驱动羽毛的方向约束没能复现骨骼原来的朝向。'
                   % (len(flip), worst_r3)))

        # 2) 骨骼零形变
        rest_len = bone_lens()
        worst = 0.0
        worst_bone = ''
        for p in (25, 50, 75, 100):
            self.set_fold(p)
            cmds.refresh(force=True)
            now = bone_lens()
            for k, v in now.items():
                if k in rest_len:
                    d = abs(v - rest_len[k])
                    if d > worst:
                        worst = d
                        worst_bone = '%s → %s（%d%%）' % (k[0], k[1], p)
        add('骨骼零形变', worst < 1e-3,
            '0~100 骨长最大变化 %.6f%s' % (worst, '（' + worst_bone + '）' if worst_bone else ''))

        # 3) 收起紧凑度
        # 两个数一起报，判据用骨骼那个：
        #   · 骨骼（羽尖到肩）：收得动多少，反映解算；实测 4.90 → 1.55 = 32%
        #   · 网格直径（两两顶点最大距离，与朝向无关）：肉眼看到的尺寸；
        #     实测 5.72 → 3.59 = 63%，比骨骼那个大得多 —— 这是**必然的**：
        #     羽毛是刚性跟着骨骼走的（用户要求权重=1），长度不缩，所以整只翅膀
        #     最多只能收到「最长那根飞羽那么长」，飞羽越长的模型这个比例越高。
        #     真实鸟类收起翅膀也就是一根飞羽的长度，所以 63% 不是缺陷。
        # 不能用世界轴对齐包围盒：收起后羽包会转向，轴对齐盒反而变大
        # （实测 6.44 → 8.50，报 132%，完全是假象）。
        self.set_fold(0)
        cmds.refresh(force=True)
        sh = wpos(resolve_joint(short_name(chain[0])) or chain[0])

        # 翼面内的「长 x 宽（细长比）」—— 「羽尖到肩」看不到的信息。
        # 只量伸出多远，会把「收成一坨厚饼」判得比「细长一片」还紧凑：
        # 6 节手臂 20 根羽毛实测（同一套绑定、只换折点）
        #   每行都折  翼面内 2.91 x 1.05（细长比 2.8）、羽尖到肩 32%
        #   只折两行  翼面内 3.59 x 0.36（细长比 10.0）、羽尖到肩 57%
        # 渲出来后者才像收起来的鸟翼（前者是一把摊开的扇子）。所以把细长比一起报，
        # 用户才看得出「收得更小」和「收得像鸟翼」是两件事。
        rp = joint_positions(chain)
        f_roots = [world_pos(r) for r in roots]
        f_tips = [world_pos(get_longest_chain(r)[-1]) for r in roots
                  if len(get_longest_chain(r)) > 1]
        nrm = self.resolve_axis(rp + f_roots + f_tips, rp, f_roots, f_tips)
        nrm.normalize()
        u_rest = om.MVector(*rp[-1]) - om.MVector(*rp[0])
        if u_rest.length() < 1e-9:
            u_rest = om.MVector(1.0, 0.0, 0.0)
        u_rest.normalize()
        v_rest = nrm ^ u_rest
        if v_rest.length() < 1e-9:
            v_rest = om.MVector(0.0, 0.0, 1.0)
        v_rest.normalize()

        def inplane():
            # 手臂关节必须**当场读**：下面是在 fold=100 的姿态上调用的，而 rp 是
            # fold=0 时抓的。混用会把「展开时的手臂」和「收起后的羽毛」放进同一个
            # 盒子里量，长度直接被撑成展开那根手臂的跨度（实测真翼形报 7.58，
            # 而同一套绑定的网格直径只有 3.42 —— 一个直径 3.42 的点集不可能有
            # 7.58 的跨度，细长比因此全是假的、还偏好看）。
            pts = [wpos(j) for j in chain]
            for r in roots:
                pts += [wpos(x) for x in get_longest_chain(r)]
            us = [p * u_rest for p in pts]
            vs = [p * v_rest for p in pts]
            return max(us) - min(us), max(vs) - min(vs)

        def tip_max():
            best = 0.0
            for r in roots:
                ch = get_longest_chain(r)
                if ch:
                    best = max(best, (wpos(ch[-1]) - sh).length())
            return best

        geos = [g for _sk, g in self.feather_geometries(info)]
        meshes = sorted(set((cmds.listRelatives(g, p=True, f=True) or [g])[0]
                            for g in geos
                            if cmds.listRelatives(g, p=True, f=True)))
        # 取样方式：把**所有**羽毛网格的顶点收集起来，再整体等距抽样到 ≤800 个。
        # 原来写的是「每张卡取 6 个、最多 60 张」—— 两个毛病：
        #   · 大于 60 根羽毛的模型，后面的卡根本没进统计；
        #   · 每张卡固定取 6 个顶点，遇到顶点多的卡（羽片分段的）取的相位不一样，
        #     实测同一套绑定只改取样方式，展开态直径就能在 6.59~7.26 之间跳。
        # 整体等距抽样对每张卡是均匀的，展开/收起两次量的是同一批顶点，比值才可信。
        allvs = []
        for g in geos:
            allvs += cmds.ls(g + '.vtx[*]', flatten=True) or []
        step = max(1, len(allvs) // 800)
        samples = allvs[::step]

        def mesh_diam():
            pts = [om.MVector(*cmds.xform(v, q=True, ws=True, t=True))
                   for v in samples]
            if len(pts) < 2:
                return 0.0
            return max((a - b).length() for a in pts for b in pts)

        r0 = tip_max()
        d0 = mesh_diam()
        self.set_fold(100)
        cmds.refresh(force=True)
        r1 = tip_max()
        d1 = mesh_diam()
        l1, wid1 = inplane()
        ratio = r1 / r0 * 100 if r0 > 1e-9 else 100.0
        # 细长比必须与朝向无关：u_rest / v_rest 是**静止时**的翼展方向与弦向，
        # 而「自动后掠」会把收好的翼包绕法线转约 90°（从沿翼展转到沿体轴），
        # 这时再拿 l1/wid1 去比就变成 0.2 了 —— 翼包明明是 2.92 x 0.69 的细长条。
        # 所以取长短边的比。
        long1, short1 = max(l1, wid1), min(l1, wid1)
        slender = long1 / max(short1, 1e-6)
        if d0 > 1e-9:
            mratio = d1 / d0 * 100
            # 网格直径收不下来时给一句说明，否则用户看到 90%+ 会以为绑定坏了。
            # 真实鸟翼的翼尖是**最外侧那几根主飞羽伸出去**形成的，展开态的最远点
            # 落在羽尖上 → 收起后尺寸自然会明显变小。实测：
            #   真翼形（羽尖伸到手臂外侧，翼展 7.26）：收起 47%
            #   扇子形（羽毛都只往翼根方向指，最远点就是手 4.32）：收起 95%
            # 后者是模型本身「一根羽毛都没伸出翼尖」，不是解算没收。
            hint = ''
            if mratio > 80.0:
                hint = ('（展开态的最远两点之间几乎全是手臂/羽毛根部 —— 说明这根翅膀'
                        '的羽毛**没有伸到翼尖外侧**，翼展最远点落在手上，「扇子形」'
                        '模型收起时尺寸本来就不会小多少；真实鸟翼的翼尖是最外侧主'
                        '飞羽伸出去形成的）')
            add('收起紧凑度', ratio < 60.0,
                '骨骼（羽尖到肩）展开 %.2f → 收起 %.2f（%.0f%%，建议 <60%%）；'
                '网格直径 %.2f → %.2f（%.0f%%）；收到底翼面内 %.2f x %.2f'
                '（细长比 %.1f，收好的鸟翼是细长一条）%s'
                % (r0, r1, ratio, d0, d1, mratio, long1, short1, slender, hint))
        else:
            add('收起紧凑度', ratio < 60.0,
                '展开 %.2f → 收起 %.2f（%.0f%%，建议 <60%%）；收到底翼面内 %.2f x %.2f'
                '（细长比 %.1f）（没有羽毛网格，按骨骼算）'
                % (r0, r1, ratio, long1, short1, slender))

        # 4) 垂直基线守恒：从视口里摆这一节手臂（转它自己的 FK 圆环）前后，
        #    羽毛与手臂的夹角变化。
        #    这里必须用**圆环**摆姿势，不能用偏移组 —— 偏移组的 rotate 是圆环的
        #    下游（圆环转 -> 偏移组跟着转），直接写偏移组等于绕开了动画师真正会
        #    去点的那个东西。以前圆环和偏移组之间根本没有连接，这一项是「自己写个
        #    值再自己读回来」，验了个寂寞。
        self.set_fold(0)
        cmds.refresh(force=True)

        def angles():
            out = []
            for e in extras:
                r = resolve_joint(short_name(e['root']))
                a = resolve_joint(short_name(e['arm'] or ''))
                if r is None or a is None:
                    continue
                f = wpos(get_longest_chain(r)[-1]) - wpos(r)
                ks = kids(a)
                if not ks:
                    continue
                g = wpos(ks[0]) - wpos(a)
                if f.length() < 1e-9 or g.length() < 1e-9:
                    continue
                f.normalize()
                g.normalize()
                out.append(math.degrees(math.acos(max(-1.0, min(1.0, f * g)))))
            return out

        a0 = angles()
        posed = 0.0
        moved = 0.0
        offs = info.get('offsets') or {}
        key = chain[1] if len(chain) > 1 else None
        off = offs.get(key)
        ring = fk_ctrl_of(off)
        # 量「动了没」必须量**下游**：转某一节的 FK 组是绕这一节自己转，
        # 这一节的坐标本来就不动（偏移组的轴心就落在它身上）。
        # 而且不能随便在链上往后找一节 —— 登记表里的骨骼顺序是「手臂链 + 羽毛」，
        # 后面那根未必挂在被转的这一节下面（2 节手臂时就是这样：手骨下面是空的、
        # 羽毛全挂在肱骨上，随手取下一根量出来永远是 0，假报「驱动不了骨骼」）。
        # 所以必须确认「确实是它的后代」才用它当探针。
        def descendant_of(node, ancestor):
            p = get_parent(node)
            guard = 0
            while p and guard < 64:
                if p == ancestor:
                    return True
                p = get_parent(p)
                guard += 1
            return False

        probe = None
        if key and key in chain:
            for cand in chain[chain.index(key) + 1:]:
                if descendant_of(cand, key):
                    probe = cand
                    break
        if probe is None and key:
            sub = child_joints(key)
            probe = sub[0] if sub else None
        if ring and a0 and probe:
            before = wpos(probe)
            cmds.setAttr(ring + '.rotateZ', 35.0)
            cmds.refresh(force=True)
            a1 = angles()
            posed = max((abs(x - y) for x, y in zip(a0, a1)), default=0.0)
            moved = (wpos(probe) - before).length()
            cmds.setAttr(ring + '.rotateZ', 0.0)
            cmds.refresh(force=True)
        add('垂直基线守恒', bool(a0) and posed < 1e-2,
            '转 FK 圆环 %s 35° 后夹角最大变化 %.4f 度'
            % (short_name(ring) if ring else '（找不到圆环）', posed))
        # 圆环必须真的驱动骨骼：只报「夹角没变」是不够的 —— 圆环完全没接线时
        # 夹角也不会变（因为什么都没动）。这里额外要求骨骼真的被推动过。
        if probe is None:
            # 这一节下面一根骨骼都没有（例如只有 2 节骨骼的手臂、手骨是个光杆尖），
            # 没有任何东西可以拿来量。这不是「驱动不了」，是「无从量」，判过。
            add('FK 控制器能驱动骨骼', True,
                '这一节（%s）下面是空的，没有骨骼可量，跳过'
                % (short_name(key) if key else '（没有手臂骨）'))
        else:
            add('FK 控制器能驱动骨骼', moved > 1e-3,
                '转 %s 35° → %s 移动 %.4f'
                % (short_name(ring) if ring else '（找不到圆环）',
                   short_name(probe), moved))

        # 5) 羽毛权重归属（用户要求「羽毛对应的骨骼权重就是1」）
        # 量的是「几何上属于羽毛的顶点，有多少权重落在羽毛骨骼而不是手臂骨骼上」。
        # 为什么这样量：
        #   · getAttr(weightList[i].weights) 这行数组只有 4 个数，而
        #     skinCluster(q=True, influence=True) 有 30 根，下标不是一回事
        #     （数值对得上、骨骼名完全错位），zip 出来是错的；
        #   · 逐骨骼 skinPercent 是唯一可靠读法，但 130+ 根全查太慢，
        #     所以只查手臂那几根（FK 偏移组的键就是手臂链）。
        # 「几何上属于羽毛」= 顶点离最近的羽毛骨骼比离最近的手臂骨骼更近；
        # 手臂网格、贴着肩膀的覆羽本来就该绑在手臂上，不算进这一项。
        arm_bones = sorted(set((info.get('offsets') or {}).keys()))
        arm_chains = arm_body_chains(info)
        feather_chains = []
        for e in extras:
            r = resolve_joint(short_name(e['root']))
            if r is None:
                continue
            ch = get_longest_chain(r)
            if ch:
                feather_chains.append([wpos(b) for b in ch])
        shares, skipped, n_card = [], 0, 0
        per_geo = {}
        infl_cache = {}

        def influences(sk):
            """这个 skinCluster 的影响骨骼集合（**短名**）

            必须过滤：skinPercent(..., transform=b, q=True) 对**不是**本簇影响的
            骨骼会直接抛 RuntimeError（实测「wingR_humerus 不是这个簇的影响骨骼」），
            而同一个网格的簇里可能只有羽毛骨（手臂骨被移到别的簇去了）。
            注意一定要用**短名**比：skinCluster(q=True, influence=True) 返回的是短名，
            而 info['offsets'] 的键是长名（|a|b|c）。直接拿长名去比会「永远不匹配」，
            于是每一根手臂骨都被 continue 掉、leak 永远是 0 —— 这一项就瞎了，
            实测「把羽毛卡全绑到手臂上」这种明显错误也照样报 1.000。
            """
            if sk not in infl_cache:
                try:
                    infl_cache[sk] = set(
                        short_name(x) for x in
                        (cmds.skinCluster(sk, q=True, influence=True) or []))
                except Exception:
                    infl_cache[sk] = set()
            return infl_cache[sk]

        if arm_chains and feather_chains:
            for sk, g in self.feather_geometries(info):
                try:
                    nv = cmds.polyEvaluate(g, v=True)
                except Exception:
                    continue
                if not nv:
                    continue
                # 先判这块几何到底是不是「羽毛卡」：采样点里离羽毛骨更近的要有 7 成以上。
                # 真实模型里整个翅膀常共用一个 skinCluster，或者手臂网格的簇里混进了
                # 羽毛骨（Maya 建簇时会把当时挂在手臂骨下的羽毛骨一起收进去），
                # 那样手臂网格也会被 feather_geometries 扫进来 —— 它整块都绑在手臂上，
                # 会把这一项直接拉到 0 分、假报「羽毛权重不对」。
                # 距离按**骨段**算（见 dist_to_bone_chains 的注释），不然手臂网格会误判。
                step = max(1, nv // 5)
                probes = list(range(0, nv, step))
                hits = 0
                for vi in probes:
                    nm = '%s.vtx[%d]' % (g, vi)
                    p = om.MVector(*cmds.xform(nm, q=True, ws=True, t=True))
                    if dist_to_bone_chains(p, feather_chains) < \
                            dist_to_bone_chains(p, arm_chains):
                        hits += 1
                if hits * 10 < len(probes) * 7:
                    continue            # 大多顶点更贴手臂 → 是手臂/身体网格，不算羽毛卡
                n_card += 1
                for vi in probes:
                    name = '%s.vtx[%d]' % (g, vi)
                    p = om.MVector(*cmds.xform(name, q=True, ws=True, t=True))
                    if dist_to_bone_chains(p, arm_chains) <= \
                            dist_to_bone_chains(p, feather_chains):
                        skipped += 1        # 这根顶点本来就该跟手臂
                        continue
                    leak = 0.0
                    infl = influences(sk)
                    for b in arm_bones:
                        if short_name(b) not in infl:
                            continue
                        leak += (cmds.skinPercent(sk, name, transform=b, q=True) or 0.0)
                    v = max(0.0, min(1.0, 1.0 - leak))
                    shares.append(v)
                    per_geo.setdefault(short_name(g), []).append(v)
        # 按「每一张羽毛卡」看，而不是逐顶点：羽毛卡最靠根的那一排顶点本来就
        # 贴着手臂骨（那是转轴），逐顶点的最小值必然是 0，说明不了问题。
        # 真正要抓的是「整张卡都绑在手臂上」（那样收起时它根本不跟着羽毛链弯）。
        # 阈值取 0.4：短羽毛卡（单节骨骼那种）有一半顶点跨在手臂上也算正常，
        # 实测最差的一张是 0.500；整张卡绑在手臂上时这个值是 0.000。
        geo_means = sorted((sum(v) / len(v), k) for k, v in per_geo.items() if v)
        if geo_means:
            worst, worst_name = geo_means[0]
            n_bad = len([m for m, _ in geo_means if m <= 0.5])
            # 光看「权重大于一半落在羽毛上」是不够的：一张卡可以整卡都是 1，却
            # **散在好几根羽毛上**（实测真翼形 38 张卡，只有 35% 的顶点落在自己
            # 那根羽毛上）。那种卡收起时会被几根羽毛往不同方向拽 —— 卡片被剪开。
            # 这里直接量结果：收起到底时羽毛卡的**边长**变了多少
            # （权重=1 的刚性卡片应当≈0）
            rig = self._card_shear(info)
            tip = ''
            if rig is not None:
                tip = ('；卡片刚性：收起到底时羽毛卡的边长最大变了 %.1f%%'
                       '（越接近 0 越好；这一项大说明同一张卡被几根羽毛同时拽着、'
                       '收起时会被拉坏）%s'
                       % (100.0 * rig,
                          '（若还没点过「羽毛权重=1」，点一次通常能把它降到 1% 左右）'
                          if rig >= 0.15 else ''))
            add('羽毛权重归属', worst > 0.4,
                '每张羽毛卡上「不落在手臂上」的平均权重：最差 %.3f（%s）；'
                '低于一半的有 %d / %d 张；逐顶点最低 %.3f、平均 %.3f%s'
                % (worst, worst_name, n_bad, len(geo_means), min(shares),
                   sum(shares) / len(shares), tip))
        elif n_card:
            add('羽毛权重归属', True,
                '%d 张羽毛卡上「几何上属于羽毛」的采样点都落在靠近手臂转轴的那一排'
                '（本来就该跟手臂），这项没有可判断的顶点，跳过' % n_card)
        else:
            add('羽毛权重归属', True,
                '没有扫到羽毛网格的蒙皮（羽毛可能和手臂共用一个 skinCluster '
                '且顶点都更贴手臂），这项跳过')

        # 6) 控制器齐全
        n_grp = len([e for e in extras if e.get('grp') and cmds.objExists(e['grp'])])
        n_ctl = len([e for e in extras if e.get('ctrl') and cmds.objExists(e['ctrl'])])
        n_tip = len([e for e in extras if e.get('tip') and cmds.objExists(e['tip'])])
        add('控制器齐全', n_grp == n_ctl == n_tip == len(extras),
            '偏移组 %d / 朝向圆环 %d / 末端方块 %d（羽毛 %d 根）'
            % (n_grp, n_ctl, n_tip, len(extras)))

        # 7) 羽毛每一节都贴在各自的驱动样条上
        # 用户要求「末端由样条控制、用方向约束（不是 IK）」：羽毛每一节都被点约束
        # 锁在样条上的定位器上，所以骨骼世界坐标必须和定位器一致。
        # 约束被删/被别的约束抢了，这里立刻看得出来（那种情况下羽毛会僵硬地
        # 跟着手臂走，收起时和别的羽毛打架）。
        # 单节骨骼的羽毛本来就没有样条（改用朝向约束跟随圆环），不算不达标。
        # 必须在「收起一半」的状态下量：静止姿态时骨骼本来就和定位器重合，
        # 约束被删掉也看不出来（这条踩过坑）。
        self.set_fold(50)
        cmds.refresh(force=True)
        worst, n_ok, n_missing = 0.0, 0, 0
        for e in extras:
            # 羽毛骨链现场按名字找回来，不依赖登记表里的 joints 字段：
            # 重开文件后那份登记里没有它，取不到就会把整项检查空过去（假通过）。
            r = resolve_joint(short_name(e['root']))
            joints = get_longest_chain(r) if r else []
            if len(joints) < 2:
                continue
            locs = [l for l in (e.get('locators') or []) if l and cmds.objExists(l)]
            if not locs:
                n_missing += 1
                continue
            n_ok += 1
            for k in range(1, min(len(locs), len(joints))):
                worst = max(worst, (wpos(joints[k]) - wpos(locs[k])).length())
        add('羽毛贴合样条', worst < 5e-3 and not n_missing,
            '收起一半时每节骨骼与样条定位器的最大偏差 %.6f（%d 根有样条%s）'
            % (worst, n_ok, '' if not n_missing else '，%d 根缺样条' % n_missing))

        # 8) 驱动齐全：手臂每个关节的 rotate、每根羽毛偏移组的 rotate 都要有驱动关键帧
        # （用户要求「用手臂关节一个个驱动」）。少了任何一条，那部分就收不动。
        # 注意要按 X/Y/Z 逐轴查：对 .rotate 这个复合属性查 listConnections 拿不到曲线。
        def driven_axes(node):
            n = 0
            for ax in 'XYZ':
                if cmds.listConnections('%s.rotate%s' % (node, ax), s=True, d=False,
                                        type='animCurve'):
                    n += 1
            return n

        n_arm_ch = sum(driven_axes(j) for j in (info.get('offsets') or {}).keys()
                       if cmds.objExists(j))
        fk_missing = [short_name(e['root']) for e in extras
                      if e.get('grp') and cmds.objExists(e['grp'])
                      and driven_axes(e['grp']) == 0]
        add('驱动关键帧齐全', n_arm_ch > 0 and not fk_missing,
            '手臂被驱动的 rotate 通道 %d 条；没有驱动关键帧的羽毛 %d 根%s'
            % (n_arm_ch, len(fk_missing),
               ('（%s…）' % '、'.join(fk_missing[:3])) if fk_missing else ''))

        # 9) 羽毛穿插合理（用户要求「合理穿插」）
        # 羽毛卡是二维薄片（零厚度），所以「互相切进去」的判据应当是：
        #   · 两根在**翼面投影**里真的交叉（这才是「横向叠着」）；
        #   · 交叉那一点上两者的深度几乎相同 —— 一根压着另一根只是正常的瓦片叠压。
        #
        # 这个判据换过三次，把过程记下来免得再走一遍（九个夹具实测）：
        #   ①「同一个参数位置比深度差」：两根长度不同时，同参数指的是两个不相干的
        #      位置，深度差凭空翻来翻去。而且「横向叠着」用的是「3D 距离 < 羽毛长 25%」，
        #      压根不要求投影交叉 —— 实测 build_wing_rigged 的 feather02×feather03
        #      被误报成穿过，可它们的中心线在投影里根本没交叉（新判据对这套报 0 对）。
        #   ②「彼此 3D 距离小于阈值的点对里比深度」：更糟，一根的尖和另一根的根也
        #      可能靠得近，八个夹具里七个炸成几十上百对。
        #   ③ 现在这个（投影交叉点比一次深度）：跑出来 build_wing_real 22 对/静止 30 对、
        #      真翼形 10/10、两套少的 0 对，都通过；结构上就是对的。
        # 换成 ③ 之后仍有三套「收起来比静止多出若干对共面交叉」（形状 22/7、
        # 鸟形 10/6、长翼 4/3）—— 那是旋转式分层的固有限制：羽毛卡本身在静止姿态
        # 就是共面的（有些模型静止就有 30 对交叉），收起过程中它们又会两两经过
        # 同一个深度。把「层叠错开」从 4° 调到 16° 能把形状那套从 22 对压到 13 对，
        # 但压不到静止基线 —— 要真正消掉得改分层方式（不是调参）。
        #
        # 长翼那套（6 节手臂）现在是「折第 2、4 行」：多出 1 对（4 对 / 静止 3 对）。
        # 这一对是**折点选择**带来的，把折点换成「每行都折」就正好等于基线（3 对），
        # 但那时收起来是一把摊开的扇子（翼面内 2.91 x 1.05、细长比 2.8），
        # 而不是细长一片（3.59 x 0.36、细长比 10.0）。把 16 种折点组合都量过一遍：
        # 凡是「细长比 8~10 且这一项不超标」的组合，都是靠**手臂少折一点**
        # 换来的（伸出量 69%~85%，会过「手臂真的折进去了」那道闸），
        # 所以这不是能靠换折点同时拿到的两件事，只能二选一。
        # 选了「收起来像鸟翼」：收起 20% 那一档渲图对比在 shots/mid20/
        # （「每行都折」是一把张开的耙子、「折第 2、4 行」是一整条后掠的羽面）。
        # 另外这个判据是**相对静止姿态**看的（新增的穿过才算坏），因为很多模型
        # 静止时本来就有交叉的卡片。
        # 全程每 10% 都扫：驱动关键帧的欧拉展开曾在一档上选错分支，相邻两档之间
        # 差 175°，插值时手臂中途翻过去（半径在 85%~90% 弹到展开的 45% 又收回来），
        # 只采 0/50/100 的档位全是干净的 —— 中途的瞬态只有密采才藏不住。
        nrm = om.MVector(info['normal'])
        nrm.normalize()
        segs = []
        for e in extras:
            r = resolve_joint(short_name(e['root']))
            if r is None:
                continue
            ch = get_longest_chain(r)
            if len(ch) < 2:
                continue
            segs.append((wpos(ch[0]), wpos(ch[-1]),
                         chain_length(joint_positions(ch))))
        if len(segs) >= 2:
            L = sorted(s[2] for s in segs)[len(segs) // 2]
            # 判据要在**翼面投影**里求两根羽毛的交叉点，所以先定一组面内正交基：
            # U = 静止姿态的肩→手方向，V = N × U。
            U = wpos(chain[-1]) - wpos(chain[0])
            U = U - nrm * (U * nrm)
            if U.length() < 1e-9:
                U = om.MVector(1.0, 0.0, 0.0)
            U.normalize()
            V = nrm ^ U
            V.normalize()
            margin = L * 0.005

            def scan(fold):
                """在某个收起档位上数「横向叠着 / 真的穿过去 / 几乎重合」的对数"""
                self.set_fold(fold)
                cmds.refresh(force=True)
                live = []
                for e in extras:
                    r = resolve_joint(short_name(e['root']))
                    if r is None:
                        continue
                    ch = get_longest_chain(r)
                    if len(ch) < 2:
                        continue
                    live.append((wpos(ch[0]), wpos(ch[-1])))
                if len(live) < 2:
                    return (0, 0, 0, 0.0)
                overlap_n = cross_n = coincide_n = 0
                seps = []
                for i in range(len(live)):
                    for j in range(i + 1, len(live)):
                        a1, b1 = live[i]
                        a2, b2 = live[j]
                        # 判据：**两根羽毛在翼面里的投影交叉处，深度差是不是 0**。
                        #
                        # 羽毛卡是零厚度的薄片，所以「互相切进去」的充要条件就是：
                        # 它们在翼面投影上真的交叉，而交叉那一点上两者的深度几乎相同
                        # —— 交叉处一根压着另一根（深度差明显）只是正常的瓦片式叠压。
                        #
                        # 试过另外两种量法，都有毛病，记在这里免得再走一遍：
                        #   ① 按「同一个参数位置」比深度差：两根长度不同时（覆羽 vs 飞羽、
                        #      或长短不一的一对），同参数位置指的是两个毫不相干的位置，
                        #      深度差会凭空翻来翻去 —— 实测 build_wing_rigged 的
                        #      feather02×feather03 被误报成穿过。
                        #   ② 改成「彼此 3D 距离小于横向阈值的那些点对」再比：更糟，
                        #      因为「3D 距离近」不等于「同一处」—— 一根的尖和另一根的根
                        #      也可能靠得很近，深度差照样乱翻；实测八个夹具里七个炸成
                        #      几十上百对。
                        # 只有「在投影交叉点上比一次深度」才是几何上对的那个量。
                        d1u = (b1 - a1) * U
                        d1v = (b1 - a1) * V
                        d2u = (b2 - a2) * U
                        d2v = (b2 - a2) * V
                        den = d1u * d2v - d1v * d2u
                        if abs(den) < 1e-12:
                            continue
                        r1u = (a1 - a2) * U
                        r1v = (a1 - a2) * V
                        t1 = (r1u * d2v - r1v * d2u) / den
                        t2 = (r1u * d1v - r1v * d1u) / den
                        if not (0.0 <= t1 <= 1.0 and 0.0 <= t2 <= 1.0):
                            continue
                        overlap_n += 1
                        p1 = a1 + (b1 - a1) * t1
                        p2 = a2 + (b2 - a2) * t2
                        dep = (p1 - p2) * nrm
                        seps.append(abs(dep))
                        if abs(dep) < margin:
                            cross_n += 1
                seps.sort()
                med = seps[len(seps) // 2] if seps else 0.0
                # 「几乎重合」：交叉处深度差小到看不出来（本来也判成穿过了），
                # 这里保留一个计数，方便判断模型本身是不是一堆共面卡片。
                coincide_n = len([s for s in seps if s < L * 0.0002])
                return (fold, cross_n, overlap_n, coincide_n, med)

            # 静止姿态当作基线：有些模型本来就有一两根羽毛是叠着交叉的（实测稀疏
            # 压测场景静止时就有 2 对），那不是「收起收坏了」。判据改成
            # 「收起过程中新增的穿过 = 0」，才是真的在说这套解算有没有问题。
            #
            # **全程每 10% 都扫**，不是只看 50%/100%。踩过这个坑：驱动关键帧的欧拉
            # 展开曾在一档上选错分支，相邻两档之间差 175°，插值时手臂中途翻过去 ——
            # 整只翅膀在 85%~90% 之间弹到展开半径的 45% 又收回去，而只采 0/50/100
            # 的档位全是干净的。现在十一个档位一起看，这种中途的瞬态才藏不住。
            base = scan(0)
            cands = [scan(p) for p in range(10, 101, 10)]
            end = cands[-1]                          # 收到底那一档
            worst = max(cands, key=lambda r: r[1])   # 「穿过」最多的一档
            fold, cross_n, overlap_n, coincide_n, _unused = worst
            # 「穿过」是过程量：全程每一档都不能比静止姿态更多。
            # 「分层间隔」是另一回事：它说的是「叠在一起的那两根，深度差多少」，
            # 所以要看**有交叉的那一档**（收到底的形态优先，收到底没有交叉就看
            # 交叉最多的一档）；全程一对交叉都对不上时这个量无从谈起，按通过算。
            src = end if end[2] > 0 else (worst if overlap_n > 0 else None)
            med = src[4] if src else L
            if overlap_n == 0:
                # 一根羽毛和任何邻居在翼面投影里都不交叉 —— 没有会叠在一起的两根，
                # 也就无从穿插。实测羽毛少而稀（6 根）时就是这种情况。
                add('羽毛穿插合理', True,
                    '羽毛之间在翼面投影里都不交叉（全程十一个档位里最多的一档 %d%% '
                    '也只有 0 对），没有会叠在一起的两根，无从穿插' % fold)
            else:
                # 「几乎重合」单独报个数：交叉处深度差小于羽毛长的 0.02% 时，
                # 那两根基本是共面的（渲染会互相割），它和得分是两件事。
                add('羽毛穿插合理', cross_n <= base[1] and med > L * 0.002,
                    '收起 0~100%% 每 10%% 一档里最差的一档（%d%%）：投影交叉 %d 对里'
                    '深度几乎相同（＝真的切进去）%d 对（静止姿态本来就有 %d 对）、'
                    '几乎完全共面 %d 对；交叉处的深度间隔中位 %.4f（羽毛长的 %.1f%%）%s'
                    % (fold, overlap_n, cross_n, base[1], coincide_n, med,
                       100.0 * med / L if L else 0.0,
                       '' if src else '（全程没有投影交叉的对，分层间隔无从考量）'))
        else:
            add('羽毛穿插合理', True, '羽毛太少，跳过')

        # 12) 卡片贴合翼面（收起到底时卡片平面相对翼面歪了多少）
        # 为什么量它：卡片若在收起后绕自身长轴拧着（卡面不躺在翼面里），而相邻两层的
        # 深度差只有羽毛长的 0.4%（37 层挤在 17% 的整叠厚度里），相邻卡片就会**真的
        # 互相穿**。实测（线段－三角形真求交，不是投影判据）：
        #   · 严格共面的夹具：卡面偏 0.00°、真穿模 0 对；
        #   · 「每根羽毛随机翘 ±12°」的夹具：收起后卡面中位 7.3°、最大 60.3°，
        #     80% 档真穿模 51 对 —— 而「羽毛穿插合理」那一项只报 1 对，看不见这类。
        # 模型静止时羽毛本来就不共面（羽毛做了扇开/卷曲）时这一项必然偏高，那是
        # **模型的属性**、不是绑定坏了，所以判据取「中位 ≤ 15°」，文案里写清原因与处置。
        cmds.setAttr(ctrl + '.' + FOLD_ATTR, 1.0)
        cmds.refresh(force=True)
        pn = om.MVector(*(info.get('normal') or (0.0, 0.0, 1.0)))
        if pn.length() < 1e-9:
            pn = om.MVector(0.0, 0.0, 1.0)
        pn.normalize()
        devs = []
        # 手臂网格不是羽毛卡，跳过。手臂是垂直插在翼面里的，它的卡面法线相对翼面
        # 天然就是 90°，混进来会把「最大拧角」报成假的 37.5°/90°。
        # 判据用「顶点真的带着手臂骨的权重」，不能用「皮肤簇影响列表里有没有手臂骨」：
        # 合并成一个皮肤簇的模型里，羽毛卡和手臂共用一个影响列表（里面有手臂骨也有
        # 羽毛骨），用影响列表判会把羽毛卡一起误杀 —— 实测 build_bird_wing 那样
        # 整项报成「没有可量的羽毛卡片，跳过」。羽毛卡生成时被归一成只跟自己那根
        # 羽毛骨（手臂骨权重=0），所以「有顶点的手臂骨权重>0」才是手臂网格。
        arm_bones = set(short_name(b) for b in (info.get('offsets') or {}).keys())
        for _sk, g in (self.feather_geometries(info) or []):
            try:
                nv = cmds.polyEvaluate(g, v=True) or 0
            except Exception:
                continue
            if nv < 3:
                continue
            if arm_bones:
                infl = cmds.skinCluster(_sk, q=True, influence=True) or []
                on_arm = False
                for vi in range(min(nv, 6)):
                    vals = (cmds.skinPercent(_sk, '%s.vtx[%d]' % (g, vi),
                                             q=True, value=True) or [])
                    for x, v in zip(infl, vals):
                        if v > 1e-6 and short_name(x) in arm_bones:
                            on_arm = True
                            break
                    if on_arm:
                        break
                if on_arm:
                    continue
            pts = [wpos('%s.vtx[%d]' % (g, i)) for i in range(nv)]
            c = om.MVector()
            for p in pts:
                c += p
            c /= float(nv)
            v1 = max(pts, key=lambda p: (p - c).length())
            d1 = v1 - c
            if d1.length() < 1e-9:
                continue
            d1.normalize()
            # 离「质心→最远点」这条轴最远的点，与轴一起张出卡片平面
            far = None
            for p in pts:
                q = p - c
                perp = q - d1 * (q * d1)
                if far is None or perp.length() > far.length():
                    far = perp
            if far is None or far.length() < 1e-9:
                continue
            nrm = d1 ^ far.normal()
            if nrm.length() < 1e-9:
                continue
            nrm.normalize()
            devs.append(math.degrees(math.acos(
                max(-1.0, min(1.0, abs(nrm * pn))))))
        if devs:
            devs.sort()
            med = devs[len(devs) // 2]
            note = ''
            if med > 15.0:
                note = ('；模型静止时羽毛本来就不共面（扇开/卷曲），收起后卡面会拧着、'
                        '相邻卡片会真的互相穿 —— 把「层叠厚度」往上调能缓解'
                        '（实测 38 根 ±12° 的夹具：17% 时真穿模 51 对 → 60% 时 19 对，'
                        '压不到 0；代价是羽毛整体离手臂更远）')
            elif devs[-1] > 25.0:
                note = ('；中位没问题，但有卡片拧到 %.0f°（最拧的那几张与邻居靠得很近时'
                        '会互相穿）' % devs[-1])
            add('卡片贴合翼面', med <= 15.0,
                '收起到底时卡片平面相对翼面：中位 %.1f°、最大 %.1f°（0=卡片平躺在翼面里）%s'
                % (med, devs[-1], note))
        else:
            add('卡片贴合翼面', True, '没有可量的羽毛卡片，跳过')

        self.set_fold(0)
        cmds.refresh(force=True)
        return res

    def on_self_check(self):
        res = self.self_check()
        if not res:
            return
        print('[翅膀绑定] 自检 %s' % self.current_ctrl)
        for name, ok, text in res:
            print('   %s %s：%s' % ('[通过]' if ok else '[注意]', name, text))
        bad = [n for n, ok, _ in res if not ok]
        if bad:
            self.label_info.setText('自检 %d/%d 通过｜注意: %s'
                                    % (len(res) - len(bad), len(res), '、'.join(bad)))
        else:
            self.label_info.setText('自检 %d 项全部通过（%s）'
                                    % (len(res), self.current_ctrl))

    def feather_targets(self, chain, feathers, normal, folded_pts=None, ref_u=None):
        """解算每根羽毛的目标：返回 [(feather, δ, 层叠角)]

        δ = 让羽毛绕 N 从静止朝向转到「目标朝向」所需的角度。

        收拢方向 = 从「折叠后的手」指回「肩」。羽毛顺着折叠后的手臂收回来，
        整只翅膀才会变成贴着手臂的紧凑一包——实测能收到展开尺寸的 32%。
        反过来（让羽毛沿手臂往外伸）只能收到 91%，等于没折。
        「反向」取另一侧。

        关键是「所有羽毛朝同一个方向」。折叠后的手臂本身是 Z 形折返的，羽毛根部
        会被带到一前一后两条线上（根部刚性挂在骨骼下，权重 1，改不了）。如果为了
        把羽尖拉到一起而给每根羽毛单独解一个角度，相邻羽毛的朝向就会差到六七十度，
        收起后是一团刺球而不是一叠羽毛——实测朝向散差 67.5°、羽尖横向散开 0.78。
        真实鸟翼收起时飞羽几乎平行，只按翼展顺序微微张开（扇形微张），
        整包是一条细长的叶子：朝向散差 17°、羽尖横向 0.51、细长比 0.19。

        层叠：按羽毛长度单调分层，沿翼面法线平移（不是绕轴抬起）——
        短覆羽在最外面一层、长飞羽最贴翼面，一层压一层、互不相交。
        「层叠厚度」是这个**整叠**的厚度（占中位羽毛长的百分比）。

        为什么不是「每根都占一层」的更聪明排法（量过了，别再试）：
        收起后所有羽毛都平行于收拢方向，投影就是一叠**平行**的带子，所以「谁和谁
        会叠上」是一维区间重叠，理论上只需 max 并发数的层数 —— 实测 38 根只要
        14 层、96 根只要 35 层（安全余量 0 时），层间距本可放大 2.5~2.8 倍。
        但真正决定穿不穿的是**重叠对的深度差的最小值**，不是中位：把层数压到 14
        会让一部分重叠对只剩 1 层之隔（比现在的 0.4% 更糟）；保持 38 层、只把顺序
        重排（贪心把重叠对尽量推开）也试算过：中位层差 10→12、23→29（+20%），
        而**最小值仍是 1 层**（241 对重叠里必然有相邻的）—— 换不来结果、却要动所有
        模型的深度分配。所以维持「按长度单调分层」。
        （真模型羽毛静止时本来就翘出翼面时的残余互穿，只能靠调大「层叠厚度」压，
        实测 17%→60% 是 51→19 对，压不到 0，代价是羽毛整体离手臂更远。）
        """
        if not feathers:
            return []
        pts = joint_positions(chain)
        origin = om.MVector(*pts[0])
        axis_vector = om.MVector(*pts[-1]) - origin
        span = axis_vector.length()

        if folded_pts and len(folded_pts) >= 2:
            tip_for_goal = folded_pts[-1]
        else:
            tip_for_goal = pts[-1]
        # 收拢方向 = 从「折叠后的手」指回「肩」；「自动」时还要兜一道「必须朝肩那一侧
        # 收、不能朝翼尖外侧伸」的规则 —— 完整说明见模块级 feather_goal。
        # 生成、折点估算、方向估算三处共用同一份规则，免得再出现「估的和生成的不一致」。
        goal = feather_goal(pts[0], tip_for_goal, pts,
                            self.combo_feather_dir.currentText() != DIR_FLIP,
                            ref_u)
        if goal is None:
            return []

        amount = self.spin_feather_sweep.value() / 100.0
        fan = math.radians(self.spin_fan.value())
        yaw = self.spin_yaw.value()

        directions = {}
        spread = {}
        lengths = {}
        for feather in feathers:
            root = feather['root']
            directions[root] = feather_direction(root)
            # 这根羽毛在翼展上的位置（0=翼根，1=翼尖），用来分配扇形微张的夹角
            if span > 1e-6:
                along = ((om.MVector(*world_pos(root)) - origin)
                         * axis_vector) / (span * span)
            else:
                along = 0.5
            spread[root] = min(1.0, max(0.0, along))
            lengths[root] = chain_length(joint_positions(get_longest_chain(root)))

        # 层叠错开的次序按「羽毛长度」排：短的是覆羽、长的飞羽。
        # 短覆羽抬得最多（压在飞羽根部上面）、最外侧的长飞羽抬得最少（在最外层），
        # 这样同一翼展位置上重叠的覆羽与飞羽会被分到不同深度，不会糊成一片。
        # 试过改成按「翼展位置」排（想的是羽毛真正叠压的是翼展上的邻居），
        # 实测反而更差：稀疏场景收起后深度翻转的对数 2 -> 5，密集场景几乎不变
        # （合计 77->77、288->286）。所以保留按长度排。
        order = sorted(lengths.items(), key=lambda kv: kv[1])
        total = len(order)
        rank = dict((root, (i / float(total - 1) if total > 1 else 0.0))
                    for i, (root, _) in enumerate(order))
        # 抬升量试过「按长度反过来补偿」（想让**尖端**的离面距离也按 rank 单调）——
        # **两次实测都更差**：静止离面量还没抹平时：稀疏场景穿过 3 -> 6；抹平之后
        # 重测：穿过 1 -> 4，而且从 60% 档就开始穿。原因：这么一缩放，长飞羽的抬角
        # 被压到接近 0，长飞羽之间反而失去分层。所以抬升量只按 rank 线性分配。
        #
        # 旋转式分层的固有限制（想清楚了才敢换成平移，过程记在这里）：
        #   两根羽毛的**投影交叉点在收起过程中是移动的**，一路扫过它们的深度差曲线；
        #   而两根转过不同角度的羽毛，深度差沿长度线性变化、必然经过 0 ——
        #   交叉点扫到那个位置时，它们就正好共面切进去。
        #   调参压不到底：层叠错开 4°→16° 只把形状那套从 22 对压到 13 对，静止基线 7 对。
        #   试过把 rank 量化成 6 层（同层抬角相同 → 平面平行）：18 → 16 对，仍不通过。
        #   试过「放大模型自带的层叠」：这些夹具的羽毛卡本来就建在同一平面里
        #   （静止离面角全是 0），放大 0 还是 0 → 收起后全部共面（23/23 对），撤回。
        #   「沿翼面法线平移分层」理论上对：深度差沿整条羽毛恒定、不经过 0。
        #   早先试过三次都被「约束链把骨链拉长」卡住（骨骼零形变全挂），原因是
        #   只挪了偏移组：羽毛根骨骼还留在手臂上、下面的关节却被点约束拉到平移过的
        #   样条上，根到第一节之间被拉长。**把根骨骼和偏移组用同一个局部位移一起挪**
        #   就整条链刚性平移了（见 drive_feather_splines 里的实现）。
        # 层叠：「层叠厚度」是**整叠**的厚度（占中位羽毛长的百分比）。
        # 按长度 rank 从翼根到翼尖递减分配：短覆羽在最外面一层、长飞羽最贴翼面。
        # 试过改成「每层间距 ×(根数−1)」（想让根数少的模型自然更薄）——**实测更差**：
        # 层间距是**相邻两层**的差，而判「几乎共面」的门槛是羽毛长的 0.5%，两者太近。
        # build_wing_long（20 根）在 0.5%/层 时冒出 2 对真切进去（5 对 / 静止基线 3 对），
        # 换回整叠 17%（＝0.85%/层）就是 3 对（通过）。而 38 根的密集夹具在 0.46%/层
        # 反而没事（相邻 rank 本来就不交叉），所以「整叠总厚度」这组默认更稳。
        # 代价：根数特别多（>80）时相邻两层会被压到门槛以下 —— 那种模型把「层叠厚度」
        # 往上调一点（界面提示里写了）。
        depth_total = 0.0
        if lengths:
            depth_total = (self.spin_stack.value() / 100.0
                           * sorted(lengths.values())[len(lengths) // 2])
        out = []
        for feather in feathers:
            root = feather['root']
            f = directions[root]
            if f is None:
                out.append((feather, 0.0, 0.0, 0.0))
                continue
            # 扇形微张从翼根到翼尖单调递增，像合拢的折扇一样层层叠压
            layer = spread.get(root, 0.5)
            delta = (math.degrees(signed_angle(normal, f, goal)) * amount
                     + math.degrees(fan * layer)
                     + yaw
                     + feather['extra'])
            # 旋转只留「抹掉这根羽毛自己静止时的离面角」，让收起后所有羽毛严格
            # 共面（都平行于翼面），层叠完全交给平移。
            # 为什么必须抹：模型很少严格共面，实测稀疏场景 13 根羽毛静止时的离面角
            # 从 −4.0° 散到 +2.7°，而相邻两根的层叠差只有羽毛长的 0.45% —— 静止这点
            # 散乱会盖过分层，收起后羽毛在深度上的次序基本是随机的。
            #
            # 两个量都必须**在「收拢量」很小的时候就到位**，不能跟收拢量线性走：
            # 「收拢量」拧到 25~75%（想让收起轻一点是很自然的调法）时，线性缩放会
            # 同时把层叠厚度也按比例削掉，而羽毛之间仍然互相交叉 —— 结果是几百对
            # 羽毛同时落到几乎同一深度、收起过程糊成一片。
            # 实测「深度几乎相同（＝真的切进去）」的对数（同一套夹具逐项 A/B）：
            #                   收拢量 100%   75%        50%         25%
            #   38 根真翼形       0 → 0      4 → 4    19 → 10      20 → 7
            #   96 根密集         3 → 3     18 → 14  143 → 66     139 → 54
            #   44 根 real       4 → 4      8 → 8    22 → 12      46 → 15
            # 深度间隔中位也从 0.0112 升到 0.0320（38 根 @25%）。收拢量 100%（默认）
            # 一行不改 —— 上面这些改动在 amount=1 时恒等。
            # 改成：离面角用三次曲线尽快抹平（收拢量 50% 时已抹掉 87%），
            # 层叠厚度到达 35% 收拢量就给满；两者在收拢量=0 时仍然严格为 0
            # （收拢量拉到 0 就是不动这只翅膀，必须保持模型原样）。
            rest_off = math.degrees(math.asin(max(-1.0, min(1.0, f * normal))))
            flat = 1.0 - (1.0 - amount) ** 3
            lay = min(1.0, amount / 0.35)
            depth = -depth_total * (1.0 - rank.get(root, 0.5))
            out.append((feather, delta, rest_off * flat, depth * lay))
        return out

    def create_ctrl(self, chain, pts, normal):
        """创建折叠控制器曲线

        控制器大小**一律按手臂长的比例**算（纯相对量），不掺绝对下限/上限 ——
        掺了就跟模型尺度绑死。实测：原来写成 max(total_len * 0.18, 0.5)，
        在 0.01 倍的小模型上（手臂长 0.043）会做出半径是整只翅膀 **11.6 倍** 的巨圈；
        另一头羽毛圈被 min(..., 0.12) 压住，100 倍的大模型上是手臂长的 0.03%，
        细得根本点不着。改成纯比例之后，从 0.01 倍到 100 倍这个量都是臂长的 18%。
        """
        total_len = chain_length(pts)
        size = max(total_len * 0.18, 1e-5)
        index = 1
        while cmds.objExists(CTRL_NAME if index == 1 else CTRL_NAME + str(index)):
            index += 1
        name = CTRL_NAME if index == 1 else CTRL_NAME + str(index)
        ctrl = cmds.circle(n=name, ch=False, r=size, nr=(normal.x, normal.y, normal.z))[0]
        if ctrl != name and not cmds.objExists(name):
            ctrl = cmds.rename(ctrl, name)
        cmds.xform(ctrl, ws=True, t=world_pos(chain[0]))
        # 控制器必须挂到手臂根骨骼下，否则角色一动它就留在原地、动画师根本找不到
        if cmds.objExists(chain[0]):
            cmds.parent(ctrl, chain[0])
        cmds.addAttr(ctrl, ln=FOLD_ATTR, at='double', min=0.0, max=1.0, dv=0.0, k=True)
        set_ctrl_color(ctrl, CTRL_COLOR_FOLD)
        for attr in ('sx', 'sy', 'sz'):
            cmds.setAttr(ctrl + '.' + attr, l=True, k=False, cb=False)
        print('[翅膀绑定] 已创建控制器: ' + ctrl + '（已挂到 %s 下）' % short_name(chain[0]))
        return ctrl

    def find_ctrl_for(self, chain):
        """若手臂根骨骼上已挂有本插件的控制器则复用

        重开文件后 joints 那份长名列表没有了，登记表里存了根骨骼短名（root），
        按短名比一比就够判断「这套绑定就是这只翅膀的」。
        """
        root = short_name(chain[0])
        for ctrl, info in self.rigs.items():
            if not cmds.objExists(ctrl):
                continue
            joints = info.get('joints') or []
            if joints:
                if joints[0] == chain[0]:
                    return ctrl
            elif info.get('root') == root:
                return ctrl
        return None

    def insert_fk_offsets(self, chain):
        """给手臂每节插一个「FK 偏移组」，让动画师有地方摆姿势

        层级变成：父骨骼 -> <骨骼>_fk -> 骨骼。
        收起仍然写在骨骼自己的 rotate 上（羽毛的驱动源就是它，单层驱动关键帧才可靠），
        动画师要摆肩/肘/腕就转 <骨骼>_fk —— 既不会和驱动曲线抢通道，
        骨骼自己那一层也不用被动画曲线覆盖。
        两个 parent 都用 relative=True，保证插入前后世界变换完全不变。
        关键：偏移组的轴心必须落在关节自己的位置上（把关节原有的局部位移挪到组上、
        关节自身归零），否则动画师转这一节时，整段手臂会绕着上一节甩而不是在这里弯。
        返回 {骨骼: FK 偏移组}
        """
        offsets = {}
        # 兜底半径也按手臂总长的比例取，不用绝对值（理由见 create_ctrl 的注释）
        arm_len = chain_length(joint_positions(chain))
        for j in chain:
            # 每插一节，后面骨骼的长名就变了，所以一律按短名重新解析
            j = resolve_joint(short_name(j)) or j
            parent = get_direct_parent(j)
            if parent is None:
                continue
            if is_fk_offset(parent):
                # 复用上一套绑定留下的偏移组。它上面那圈可能是**老版本**建的：
                # 圆环和偏移组之间一根线都没连，圆环的 rotate 上还带着父级朝向的逆。
                # 直接接上会把这一节手臂在静止姿态拧一个角，所以删掉重建。
                old = fk_ctrl_of(parent)
                if old:
                    cmds.delete(old)
                off = parent
            else:
                local_t = list(cmds.getAttr(j + '.translate')[0])
                off = cmds.group(em=True, n=short_name(j) + FK_OFF_SUFFIX)
                cmds.parent(off, parent, relative=True)
                cmds.setAttr(off + '.translate', local_t[0], local_t[1], local_t[2])
                cmds.parent(j, off, relative=True)
                # 位移已经挪到偏移组上，骨骼自身相对偏移组归零 → 世界位置不变、轴心在关节上
                j = resolve_joint(short_name(j)) or j
                cmds.setAttr(j + '.translate', 0.0, 0.0, 0.0)
            cmds.setAttr(off + '.rotate', 0.0, 0.0, 0.0)
            # 可见的 FK 控制器：套在骨骼上的一个小圆环（法线沿骨骼方向）。
            # 空组在视口里根本看不见，动画师只能去大纲里翻，没法用。
            kids = child_joints(j)
            direction = None
            rad = arm_len * 0.02
            if kids:
                d = om.MVector(*world_pos(kids[0])) - om.MVector(*world_pos(j))
                if d.length() > 1e-6:
                    rad = max(d.length() * 0.16, arm_len * 0.012)
                    d.normalize()
                    direction = (d.x, d.y, d.z)
            ring = cmds.circle(n=short_name(j) + FK_CTRL_SUFFIX, ch=False, r=rad)[0]
            # 先把每个 CV 在「圈自己的平面」里的角度与半径记下来（此刻圈躺在世界 XY
            # 平面、rotate=0，atan2(y,x) 就是它真正的角度），挂完再按这个摆。
            cvs = cmds.ls(ring + '.cv[*]', flatten=True) or []
            polar = []
            for cv in cvs:
                p = cmds.xform(cv, q=True, ws=True, t=True)
                polar.append((math.hypot(p[0], p[1]), math.atan2(p[1], p[0])))
            cmds.parent(ring, off)
            # cmds.parent 保持世界变换，会把父级（骨骼）那套朝向的逆**反算到圈的 rotate 上**
            # —— 实测 radius 那节是 -11.87°、tip 是 -180°。
            # 下面要把圈的 rotate 接到偏移组上，不先归零就等于把这一节手臂在静止姿态
            # 拧了一个角：实测「静止姿态逐节严格还原」最大偏差 1.2986，
            # 最外侧那几根长飞羽的尖被凭空拽出去 1.29。
            cmds.setAttr(ring + '.rotate', 0.0, 0.0, 0.0)
            cmds.setAttr(ring + '.translate', 0.0, 0.0, 0.0)
            set_ctrl_color(ring, CTRL_COLOR_FK)
            if direction:
                # 归零之后圈的形状躺在「父级的局部 XY 平面」里，得把 CV 重新摆到
                # 「垂直于骨骼」的那个平面（骨骼方向是世界量，所以在世界空间里摆）。
                nv = om.MVector(*direction)
                nv.normalize()
                ref = (om.MVector(1.0, 0.0, 0.0) if abs(nv.x) < 0.9
                       else om.MVector(0.0, 1.0, 0.0))
                uu = ref ^ nv
                uu.normalize()
                vv = nv ^ uu
                c = om.MVector(*world_pos(ring))
                for cv, (r_cv, ang0) in zip(cvs, polar):
                    v = (c + uu * (r_cv * math.cos(ang0))
                         + vv * (r_cv * math.sin(ang0)))
                    cmds.xform(cv, ws=True, t=(v.x, v.y, v.z))
            # 圆环必须**真的能驱动骨骼**。以前圆环只是「摆在那儿」：它和偏移组之间
            # 一根线都没连，视口里点它、转它，这一节手臂一动不动 —— 动画师看到的
            # 就是「这个控制器是坏的」，整只翅膀根本没法从视口里摆姿势。
            # 实测（build_wing_true）：转 radius_fkCtrl 40° → 骨骼位移 0.0000。
            # 现在把圆环的 rotate 连到偏移组的 rotate 上：转圆环 = 摆这一节手臂。
            # 收起解算写在**骨骼自己的 rotate** 上，和这条线不冲突，两者叠加。
            cmds.connectAttr(ring + '.rotate', off + '.rotate', force=True)
            # 控制器只需要 rotate，缩放一律锁掉（顺手防止误操作把骨骼缩坏）
            for attr in ('sx', 'sy', 'sz'):
                cmds.setAttr(ring + '.' + attr, l=True, k=False, cb=False)
            cmds.select(clear=True)
            offsets[j] = off
        # 插完之后父级关系变了，把长名刷新一遍
        return dict((resolve_joint(short_name(k)) or k, v) for k, v in offsets.items())

    def remove_fk_offsets(self, offsets):
        """把 FK 偏移组拆掉：位移还给骨骼、骨骼挂回原父级（世界变换不变）

        偏移组是层层嵌套的（humerus_fk -> radius_fk -> ...），每拆一层，
        里面骨骼的长名就变一次，所以每一步都必须按短名重新解析；
        而且要先把骨骼搬出来、确认组里没东西了再删组，
        否则会把还没搬出来的骨骼连同组一起删掉（会直接删掉用户的骨骼）。
        """
        pairs = [(resolve_joint(short_name(j)) or j, off) for j, off in offsets.items()]
        # 最外层的先拆（chain 顺序就是由外到内）
        for j, off in pairs:
            found = cmds.ls(short_name(off), transforms=True) or []
            off = found[0] if found else None
            if not off or not cmds.objExists(off):
                continue
            j = resolve_joint(short_name(j))
            if j is None:
                continue
            parent = get_parent(off)
            t = list(cmds.getAttr(off + '.translate')[0])
            cmds.setAttr(j + '.translate', t[0], t[1], t[2])
            if parent:
                cmds.parent(j, parent, relative=True)
            # 只有确认组里没有骨骼了才删（FK 控制器曲线可以跟着删）
            rest_kids = cmds.listRelatives(off, c=True) or []
            if not any(cmds.nodeType(k) == 'joint' for k in rest_kids):
                cmds.delete(off)
        cmds.select(clear=True)

    def build_driven(self, ctrl, chain, rest, psi_at, parent_psi, normal, samples,
                     offsets=None):
        """手臂驱动：在 fold 0~1 上多点采样，把精确解算的旋转一个个写进手臂关节

        多点采样的意义：欧拉角线性插值并不等于绕轴的匀速旋转，
        采样足够密才能保证收起过程中每一帧的姿态都正确好看。
        「根部后掠角」是整只翅膀的刚体旋转，也按同一个 t 推进。
        写的是关节自己的 rotate（羽毛的驱动源就是它）；动画师要摆姿势转它的 _fk 组。
        """
        driven_joints = list(chain[1:])
        # 设了「根部后掠角」时根骨骼自己也要驱动
        if abs(psi_at(chain[0], 1.0) - parent_psi(chain[0], 1.0)) > 1e-9:
            driven_joints.insert(0, chain[0])

        # 逐采样点做欧拉展开：绕任意轴的旋转分解成欧拉角会有 ±180 环绕，
        # 相邻关键帧之间线性插值就会绕远路（358°），收起过程剧烈乱跳。
        prev = dict((j, list(rest.rotate[j])) for j in driven_joints)

        for s in range(samples):
            t = s / float(samples - 1) if samples > 1 else 1.0
            cmds.setAttr(ctrl + '.' + FOLD_ATTR, t)
            for j in driven_joints:
                delta = psi_at(j, t) - parent_psi(j, t)
                rot = list(unwrap_euler(
                    prev[j], None, rest.order[j],
                    rest.local_rotation_matrix(j, delta, normal)))
                prev[j] = list(rot)
                cmds.setAttr(j + '.rotate', rot[0], rot[1], rot[2])
                for ax in ('X', 'Y', 'Z'):
                    cmds.setDrivenKeyframe(j + '.rotate' + ax,
                                           cd=ctrl + '.' + FOLD_ATTR,
                                           itt='linear', ott='linear')
        cmds.setAttr(ctrl + '.' + FOLD_ATTR, 0)
        # 把展开后的终值交出去：羽毛的驱动范围必须和这些关键帧一致
        return prev

    def fold_channel(self, rest, joint, delta_deg, normal, offsets, folded_vals=None):
        """某根手臂骨骼的「收起」对应哪个属性的变化：返回 (属性节点, 静止值, 折叠值)

        收起写在骨骼自己的 rotate 上；_fk 组只是动画师的姿势层，不参与解算。
        折叠值优先用 build_driven 实际写进关键帧的那组（已做欧拉展开），
        否则羽毛的驱动范围会和关键帧对不上，收起就会跳。
        """
        if folded_vals and joint in folded_vals:
            return joint, list(rest.rotate[joint]), list(folded_vals[joint])
        return joint, rest.rotate[joint], rest.rotation_at(joint, delta_deg, normal)

    def feather_driver(self, chain, rest, arm, psi_all, normal, offsets=None,
                       folded_vals=None):
        """决定一根羽毛的驱动源

        返回 (驱动骨骼, rotate 通道, 该通道变化量, 被驱动属性节点)。

        优先用「羽毛跟着的那节手臂骨骼」本身——它就是这根羽毛挂着的骨头。
        羽毛挂在手臂的下级分支上时（腕部的拇指/小翼羽），分支自己不折叠，
        要改用它所依附的那节手臂骨骼的旋转来驱动。
        还有些羽毛挂在完全不参与折叠的骨骼上（例如根部骨骼、后掠角为 0 时它一动不动），
        这时改用链上转动量最大的那个手臂关节来驱动，否则这些羽毛收不起来。
        """

        def channel_of(joint):
            if joint not in chain:
                return None, 0.0, joint
            k = chain.index(joint)
            delta = psi_all[joint] - (psi_all[chain[k - 1]] if k > 0 else 0.0)
            attr, v_rest, v_fold = self.fold_channel(rest, joint, delta, normal, offsets,
                                                     folded_vals)
            return main_rotate_channel(v_rest, v_fold) + (attr,)

        source = feat_arm_source(arm, chain) if arm is not None else None
        ch, amount, attr = channel_of(source) if source else (None, 0.0, arm)
        if ch and amount > 1e-6:
            return source, ch, amount, attr
        best = (source or arm, ch or 'Z', 0.0, attr)
        for j in chain:
            c, a, at = channel_of(j)
            if c and a > best[2]:
                best = (j, c, a, at)
        return best

    def make_feather_controls(self, name_base, arm, root, joints, size, normal=None):
        """给一根羽毛建「偏移组 + 朝向控制器 + 末端控制器」，全部挂到对应手臂骨骼下

        三者都挂在手臂骨骼下，所以手臂做任何动画（弯肘/翻腕）时它们整体刚性跟随，
        羽毛与手臂的夹角严格保持不变——这就是「始终垂直于手臂」的基线。

        两个控制器的**朝向**都要按「翼面法线 normal」摆，不能由着骨骼自己的轴：
        cmds.circle / cmds.curve 建出来是躺在世界 XY / XZ 平面里的，挂到骨骼下
        再把 rotate 清零，它的平面就跟着骨骼的 jointOrient 走了 ——
        换一套骨骼朝向约定（实测另一套差 90°），方块和圈就侧过去变成一条线，
        动画师从翼面上方看过去根本找不到、也点不着。

        返回 (grp, ctrl, tip) 三个节点名；失败返回 (None, None, None)。
        """
        root_w = om.MVector(*world_pos(root))
        # 偏移组：位置落在羽毛根、朝向与对应手臂骨骼一致、局部旋转为 0。
        # 「收起偏转」的驱动关键帧就写在它的 rotate 上，因此偏移是叠加在垂直基线上的。
        grp = cmds.group(em=True, n=name_base + CTRL_GRP_SUFFIX)
        cmds.xform(grp, ws=True, t=(root_w.x, root_w.y, root_w.z))
        cmds.parent(grp, arm)
        cmds.setAttr(grp + '.rotate', 0.0, 0.0, 0.0)
        nvec = om.MVector(normal) if normal is not None else om.MVector(0.0, 0.0, 1.0)
        nvec.normalize()
        # 朝向控制器：圆环，动画师手动转它 → 整根羽毛绕羽毛根转向。
        # 两件事必须同时成立，否则这个圈没法用：
        #   ① 圈的平面要正对翼面（不然从翼面上方看是一条线）；
        #   ② 圈的局部 Z 轴要就是翼面法线（不然「转 Z」不是绕翼面转，
        #      羽毛会斜着甩出翼面 —— 实测换个骨骼朝向约定就偏 45°）。
        # 做法：形状照常画在自身局部 XY 平面里（平面法线 = 局部 Z），
        # 再把变换的朝向摆成「局部 Z 指向翼面法线」。这样「转圈的 Z」= 在翼面里转，
        # 而且与骨骼的 jointOrient 完全无关。（圈在自己的平面里怎么转都看不出来，
        # 所以静止时带的这点旋转不影响外观。）
        ctrl = cmds.circle(n=name_base + CTRL_SUFFIX, ch=False, r=size)[0]
        cmds.parent(ctrl, grp)
        cmds.setAttr(ctrl + '.translate', 0.0, 0.0, 0.0)
        zw = om.MVector(0.0, 0.0, 1.0)
        cross = zw ^ nvec
        if cross.length() < 1e-9:
            q = (om.MMatrix() if zw * nvec > 0.0
                 else axis_angle_matrix(om.MVector(1.0, 0.0, 0.0), math.pi))
        else:
            cross.normalize()
            q = axis_angle_matrix(cross, math.acos(max(-1.0, min(1.0, zw * nvec))))
        rl = q * world_rot_matrix(grp).inverse()
        # 旋转顺序设成 zxy（Z 最先作用），这样「Z 通道」就是绕圈自己的法线转，
        # 也就是动画师要的「在翼面里拨羽毛」。默认的 xyz 顺序下，静止朝向的
        # X/Y 一旦不为 0，改 Z 就不再是纯的绕面内旋转（实测偏成 19.9°/25°）。
        cmds.setAttr(ctrl + '.rotateOrder', 2)
        cmds.setAttr(ctrl + '.rotate', *matrix_to_euler(rl, 2))
        set_ctrl_color(ctrl, CTRL_COLOR_FEATHER)
        # 末端控制器：小方块，拖它 → 驱动样条末端控制点跟着走（末端由曲线控制）。
        # 它和驱动样条一样挂在圆环控制器下，所以转圆环时两者一起转，
        # 羽毛是「整体刚性转向」而不是被拧弯；单独拖方块才让羽毛末端变形。
        # 同样画在自身局部 XY 平面里：父级（圆环）的局部 Z 已经是翼面法线，
        # 方块自身旋转为 0 就自然正对翼面。
        tip_w = om.MVector(*world_pos(joints[-1]))
        half = size * 0.75
        square = [(-half, -half, 0.0), (half, -half, 0.0), (half, half, 0.0),
                  (-half, half, 0.0), (-half, -half, 0.0)]
        tip = cmds.curve(n=name_base + TIP_SUFFIX, degree=1, p=square)
        cmds.parent(tip, ctrl)
        cmds.xform(tip, ws=True, t=(tip_w.x, tip_w.y, tip_w.z))
        cmds.setAttr(tip + '.rotate', 0.0, 0.0, 0.0)
        set_ctrl_color(tip, CTRL_COLOR_TIP)
        cmds.select(clear=True)
        return grp, ctrl, tip

    def build_feather_splines(self, ctrl, chain, feathers, rest, psi_all, normal,
                              sweeps, tilts, depths, offsets=None, folded_vals=None):
        """给每根羽毛建「朝向控制器 + 末端控制器 + 驱动样条」，并用约束把羽毛绑上去

        每根羽毛的层级（全部挂在「对应手臂骨骼」下）：

            对应手臂骨骼
              └─ <羽毛>_ctrlGrp    偏移组：承载「收起偏转」，驱动关键帧写在它的 rotate 上
                   └─ <羽毛>_ctrl  朝向控制器（圆环）：手动转它，整根羽毛跟着转向
                        ├─ <羽毛>_crv   驱动样条：原点在羽毛根，控制点相对羽毛根
                        └─ <羽毛>_tip   末端控制器（小方块）：拖动它，样条末端控制点跟着走

        因为控制器、样条、末端方块都挂在手臂骨骼下，手臂随便怎么摆，它们都整体
        刚性跟随，羽毛与手臂骨骼的夹角严格不变（基线严格垂直）；
        收起只是在这个基线上再叠加偏移组的旋转。

        羽毛骨骼用「定位器 + 点约束 + 方向约束」贴合样条（不用 IK）：
        1 次曲线严格穿过所有控制点、第 k 个控制点对应参数 k，所以静止姿态零形变；
        羽毛根骨骼的位置不约束（始终刚性挂在手臂骨骼下，权重 1）。
        单节骨骼的羽毛没有骨链可挂样条，改用朝向约束直接跟随圆环控制器。
        """
        extras = []
        # 所有羽毛用同一个控制器尺寸：按手臂总长取一个百分比，既好点又不会挤在一起。
        # 纯相对量，不掺绝对上下限（理由见 create_ctrl 的注释：绝对限会把大小跟模型
        # 尺度绑死，小模型上圈巨大、大模型上细得点不着）。
        ctrl_size = max(chain_length(joint_positions(chain)) * 0.012, 1e-6)
        chain_set = set(chain)
        for feather in feathers:
            root = feather['root']
            arm = feather['arm']
            # 这根羽毛实际跟着哪一节手臂骨骼动：分支（拇指）归到它的链祖先上
            source = feat_arm_source(arm, chain, chain_set) or arm
            joints = get_longest_chain(root)
            name_base = short_name(root)
            driver, channel, amount, driver_attr = self.feather_driver(
                chain, rest, arm, psi_all, normal, offsets, folded_vals)
            # sweep = 把羽毛从静止朝向转到「收拢目标方向」需要绕 N 转的总角度；
            # 羽毛同时还被它挂着的骨骼带着转过 ψ，所以偏移组上补的是相对量 sweep - ψ。
            item = {'root': root, 'arm': arm, 'driver': driver, 'joints': joints,
                    'ctrl_size': ctrl_size,
                    'channel': channel, 'amount': amount,
                    'driver_attr': driver_attr,
                    'sweep': sweeps.get(root, 0.0),
                    'tilt': tilts.get(root, 0.0),
                    'depth': depths.get(root, 0.0),
                    'grp': None, 'ctrl': None, 'tip': None, 'tip_nodes': [],
                    'curve': None, 'shape': None,
                    'locators': [], 'poci': [], 'constraints': []}
            item['psi_sub'] = psi_all.get(source, 0.0)  # 控制器与羽毛根都挂在对应手臂骨骼下
            grp, ring, tip = self.make_feather_controls(name_base, arm, root, joints,
                                                        ctrl_size, normal)
            item['grp'], item['ctrl'], item['tip'] = grp, ring, tip
            if grp:
                # 收起偏移用的两根「世界轴」。这里存的是世界轴本身，**不**换算到局部系：
                # 偏移组挂在手臂骨骼下，手臂一折起来它的世界朝向就跟着转了，
                # 必须在写关键帧的那一刻按「当时的父级世界旋转」再换算（见
                # drive_feather_splines 里的 R_local = P · R_world · P⁻¹）。
                # 之前用静止姿态换算，羽毛会偏出目标方向二十几度，
                # 每根各偏各的，收起后就从「一叠」变成「一团刺球」。
                item['w_axis'] = om.MVector(normal)
                # 第二根世界轴：翼面内、垂直于羽毛静止朝向的那根。它现在只用来
                # **抹掉这根羽毛自己静止时的离面角**（让收起后所有羽毛严格平行于翼面）；
                # 层叠（分层）不靠旋转，而是沿翼面法线平移，见 feather_targets / drive_feather_splines。
                tip_dir = feather_direction(root)
                if tip_dir is not None:
                    tilt_axis = normal ^ tip_dir
                    if tilt_axis.length() > 1e-6:
                        tilt_axis.normalize()
                        item['w_axis2'] = om.MVector(tilt_axis)
            if len(joints) >= 2 and ring:
                # 样条：先建在同名控制点数的空曲线上，挂到圆环控制器下、把自身变换清零，
                # 之后按「曲线真实世界矩阵的逆」把各关节的世界坐标换算成控制点。
                # 用真实矩阵（而不是只取旋转部分）才能兼容手臂父级带缩放的情况。
                crv = cmds.curve(n=name_base + '_crv', degree=1,
                                 p=[(0.0, 0.0, 0.0)] * len(joints))
                cmds.parent(crv, ring)
                cmds.setAttr(crv + '.translate', 0.0, 0.0, 0.0)
                cmds.setAttr(crv + '.rotate', 0.0, 0.0, 0.0)
                cmds.select(clear=True)
                item['curve'] = crv
                item['shape'] = cmds.listRelatives(crv, s=True, f=True)[0]
                # 驱动样条是内部解算用的中间物（用户动的是圆环和末端方块），默认藏起来。
                # 不藏的话，44 根羽毛就是 44 条曲线叠在翅膀上，视口里根本看不清翅膀。
                # 想看就勾界面上的「显示辅助物」。
                cmds.setAttr(crv + '.visibility', 0)
                inv = om.MMatrix(cmds.xform(crv, q=True, ws=True, m=True)).inverse()
                for k, j in enumerate(joints):
                    p = om.MPoint(*world_pos(j)) * inv
                    cmds.setAttr('%s.controlPoints[%d]' % (item['shape'], k),
                                 p.x, p.y, p.z)
                self.build_feather_constraints(item, joints, name_base)
                item['tip_nodes'] = self.connect_tip_to_spline(item, tip)
            elif ring:
                # 单节羽毛：没有样条可挂，朝向约束到圆环控制器上（保持静止偏移）
                item['constraints'].append(
                    cmds.orientConstraint(ring, root, mo=True, w=1)[0])
                cmds.select(clear=True)
            extras.append(item)
        return extras

    @staticmethod
    def connect_tip_to_spline(item, tip):
        """末端控制器的世界位置换算到样条自身空间，接到末控制点上

        末端控制器一动，样条末端控制点就跟着动 → 羽毛末端的位置与朝向随曲线变化。
        """
        shape = item['shape']
        last = len(item['joints']) - 1
        mult = cmds.createNode('multMatrix', n=short_name(item['root']) + '_tipMat')
        # Maya 是行向量约定（p' = p · M），所以「末端世界坐标 -> 曲线局部坐标」
        # 要写成 tipWorld · curveWorldInverse，矩阵相乘的顺序不能反。
        cmds.connectAttr(tip + '.worldMatrix[0]', mult + '.matrixIn[0]')
        cmds.connectAttr(shape + '.worldInverseMatrix[0]', mult + '.matrixIn[1]')
        dm = cmds.createNode('decomposeMatrix', n=short_name(item['root']) + '_tipDm')
        cmds.connectAttr(mult + '.matrixSum', dm + '.inputMatrix')
        for ax in ('x', 'y', 'z'):
            cmds.connectAttr(dm + '.outputTranslate' + ax.upper(),
                             '%s.controlPoints[%d].%sValue' % (shape, last, ax))
        return [mult, dm]

    def build_feather_constraints(self, item, joints, name_base):
        """用「定位器 + 点约束 + 方向约束」让羽毛每一节贴合驱动样条（不用 IK）

        每个关节在样条上对应一个定位器：
          - 第 k 个关节的位置锁到第 k 个定位器（点约束）——位置由样条决定；
          - 第 k 个关节用方向约束指向第 k+1 个定位器——朝向由样条决定，
            这样羽毛末端的位置和朝向都被样条管住。
        1 次样条的第 k 个控制点正好在参数 k 上，所以定位器直接取参数 k 即可。
        羽毛根骨骼的位置不约束（它始终刚性挂在对应手臂骨骼上），只给它加方向约束。
        """
        shape = item['shape']
        locs = []
        # 定位器默认是 1 个世界单位大：小模型上（整只翅膀才 0.04）它比翅膀大二十几倍，
        # 点「显示辅助物」时满屏全是叉子；大模型上又看不见。按羽毛控制器尺寸缩一下。
        loc_scale = max(item.get('ctrl_size', 0.05) or 0.05, 1e-6) * 6.0
        for k in range(len(joints)):
            loc = cmds.spaceLocator(n='%s_pt%d' % (name_base, k))[0]
            for s in (cmds.listRelatives(loc, s=True, f=True) or []):
                cmds.setAttr(s + '.localScale', loc_scale, loc_scale, loc_scale)
            poci = cmds.createNode('pointOnCurveInfo', n='%s_poci%d' % (name_base, k))
            cmds.connectAttr(shape + '.worldSpace[0]', poci + '.inputCurve')
            cmds.setAttr(poci + '.parameter', k)
            cmds.connectAttr(poci + '.position', loc + '.translate')
            # 定位器是样条上的取样点，纯内部实现。44 根羽毛就是 132 个定位器，
            # 默认全开的话视口里密密麻麻，默认藏起来（界面可一键显示）。
            cmds.setAttr(loc + '.visibility', 0)
            locs.append(loc)
            item['poci'].append(poci)
        item['locators'] = locs
        # 位置：除根骨骼外，每个关节都锁到样条上的对应点
        for k in range(1, len(joints)):
            item['constraints'].append(
                cmds.pointConstraint(locs[k], joints[k], w=1)[0])
        # 朝向：每个关节指向下一个点（方向约束）
        #
        # **必须给方向约束一把「上方向」尺子**。原来写的是
        #     aimConstraint(..., upVector=(0,1,0), worldUpType='none')
        # —— worldUpType='none' 表示**根本不用上方向**，那根骨骼绕自身长轴的
        # **滚转（roll）就由 Maya 内部随便定**。后果实测（真翼形 38 根羽毛）：
        # 生成之后 114 根羽毛骨骼里有 88 根的世界朝向被翻了过去（矩阵差整整 2.0
        # ＝ 180°），位置却一点没变 —— 于是自检里只比位置/驱动通道的项一路绿灯，
        # 而羽毛卡已经被翻了个面：展开姿态下网格顶点最大偏离建模姿态 0.93、
        # 单张卡的包围盒差 0.52，渲出来一半卡片是背面（发暗）、轮廓被剃成锯齿。
        #
        # 尺子取**这根骨骼生成前的世界 +Y 轴**（不是翼面法线！试过：用翼面法线
        # 反而把 228 根都转错 90°，因为骨骼的 +Y 不见得就是卡片法线）。
        # 用骨骼自己的静止 +Y，滚转在展开姿态下按构造就是对的。
        # 收起时这把尺子是**钉死的世界向量**：折叠全程在翼面内做，所以模型本身共面
        # （卡片都躺在翼面里）时它一直合适；但模型羽毛静止时本来就翘出翼面时，骨骼
        # 在折叠中绕 N 扫过 0~170°，约束拽着 +Y 去追那个固定向量，卡片会绕自身长轴
        # 拧（实测 ±12° 夹具：收起后卡面最大偏 60.3°）。详见下面那段「试过两次」。
        def up_for(j):
            r = (getattr(self, '_rest_rot3', None) or {}).get(short_name(j))
            if r and len(r) >= 6:
                v = om.MVector(r[3], r[4], r[5])
                if v.length() > 1e-9:
                    return v.normal()
            return None

        nrm = getattr(self, '_build_normal', None)
        fallback = None
        if nrm is not None and nrm.length() > 1e-9:
            fallback = om.MVector(nrm).normal()
        for k in range(len(joints) - 1):
            up = up_for(joints[k]) or fallback or om.MVector(0.0, 1.0, 0.0)
            item['constraints'].append(
                cmds.aimConstraint(locs[k + 1], joints[k], aimVector=(1, 0, 0),
                                   upVector=(0, 1, 0), worldUpType='vector',
                                   worldUpVector=(up.x, up.y, up.z))[0])
        # 试过两次把「上方向」也写成驱动关键帧，让滚转基准随折叠从「静止 +Y」过渡到
        # 「翼面内、垂直于该骨骼朝向的横轴 N × dir」（先按整根羽毛的朝向、再改成每节
        # 骨骼各算各的）。两次都是：卡片最坏拧角 60.3° → 21.2°、而**中位偏角 7.3° →
        # 8.5° 没降**、真三维穿模对数也没改善（80% 档 51 → 54 对）。查清楚了原因，
        # 记在这里免得再试：
        #   · 上方向确实能控滚转（最小结构实测：改 worldUpVector，骨骼 +Y 跟着变；
        #     真夹具里 64 条方向约束的上方向通道都有 12 个驱动关键帧、值确实在变）；
        #   · 卡片的法线就是**骨骼的 +Z**（实测卡面法线与骨骼 Z 轴夹角 2~15°、
        #     与 X/Y 都是 80~90°，即平面 = span{骨骼+X 长度轴, +Y}）；
        #   · 但把 +Y 摆到翼面内之后，卡面仍偏 8.5°：因为**各节骨骼自己的朝向**
        #     偏离翼面比整根羽毛的朝向大得多（骨链在收起后是条曲线），而约束是
        #     「把 +Y 投影到垂直于该节 aim 的平面」——aim 一歪，投影就带出离面分量。
        # 也就是说：这类残余拧角来自**骨链在收起后不是直线**，不是滚转基准选错了。
        # 共面模型本来就没这个问题（自检「卡片贴合翼面」实测中位 0.0°）。
        cmds.select(clear=True)

    def drive_feather_splines(self, ctrl, extras, samples):
        """把「收起偏转」的驱动关键帧挂到「手臂关节的旋转」上

        驱动源：对应手臂骨骼的 rotate 通道（一根根手臂关节各自驱动自己那几根羽毛）；
        被驱动：该羽毛偏移组（_ctrlGrp）的 rotate —— 因为偏移组、圆环控制器、
        驱动样条、末端方块都挂在手臂骨骼下，转偏移组就等于整根羽毛绕羽毛根偏转。

        采样按「收起控制器」推进：每个采样点先把 fold 设到 t，
        手臂各关节就通过它们自己的驱动曲线取到精确的折叠姿态（三个通道都对），
        然后 setDrivenKeyframe 会把驱动通道此刻的真实值记成关键帧的输入值。

        偏移组的局部旋转由世界轴换算：
            R_local = P · R_world · P⁻¹
        P 是父级（羽毛挂着的骨骼）**当前**的世界旋转，R_world 是希望羽毛在世界上
        额外转过的角度（绕世界轴 N 转 δ、再绕翼面内轴抬 tilt）。
        用静止姿态的 P 去换算是错的，这也是收起后羽毛散成一团的主因之一。

        R_world 的 δ 必须是「世界目标角 − 骨骼已经带着转过的角」：
            δ = sweep·u(t) − ψ·t          （见下方循环里的长注释）
        ψ 是羽毛挂着的那节手臂骨骼累计转过的世界角，它在 t 时刻已经转了 ψ·t。

        层叠：沿**翼面法线平移**（不再是绕轴转）。偏移组和羽毛根骨骼被写进**同一个**
        世界位移，所以整根羽毛（根 → 子骨骼 → 控制器 → 样条 → 定位器）刚性平移，
        骨长一点都不变。为什么两个都要挪：只挪偏移组的话，样条和定位器走了、羽毛根
        还留在手臂上，而下面的关节被点约束拉到平移过的定位器上 —— 根到第一节之间被
        拉长（早先三次尝试都栽在这里）。
        位移方向要按「当时的父级世界旋转」换算成局部量：Δ_local = Δ_world · P⁻¹，
        手臂一折，同一个世界方向在骨骼局部系里已经变了。

        关键：驱动关键帧的输入值是「驱动通道的值」，所以不同的采样点必须落在这个通道
        不同的值上，否则后写的会把先写的覆盖掉。折叠不做错开时，每个关节自己的折角
        Δ(t) = (ψ_关节 - ψ_父关节)·t 与 t 成正比（见 make_psi_functions 的注释），
        所以通道值随 t 严格单调、各采样点的输入值互不相同——用 t 算收拢量是安全的。
        （试过「远端关节先折」的错开，那时通道会出现一段平的、必须改用通道自己的进度；
        错开方案已废弃，原因写在 make_psi_functions 里。）
        """
        for item in extras:
            grp = item.get('grp')
            if not grp or item['amount'] < 1e-6 or abs(item['sweep']) < 1e-6:
                continue
            arm = item['arm']
            root = item['root']
            driver = item['driver_attr'] + '.rotate' + item['channel']
            axis_w = item['w_axis']
            axis2_w = item.get('w_axis2')
            psi = item.get('psi_sub', 0.0)
            prev_rot = [0.0, 0.0, 0.0]
            # 静止位移：写驱动的量都叠加在这上面（偏移组的位移是「根相对手臂」，
            # 根骨骼自己的位移是 bind_feathers 重挂父级时烘出来的，都不能覆盖掉）
            grp_rest = list(cmds.getAttr(grp + '.translate')[0])
            root_rest = list(cmds.getAttr(root + '.translate')[0])
            for s in range(samples):
                t = s / float(samples - 1) if samples > 1 else 1.0
                cmds.setAttr(ctrl + '.' + FOLD_ATTR, t)
                # 羽毛自己的收拢进度（手臂按 t 折，羽毛按这个进度收）
                u = t ** self.spin_ease.value()
                p = world_rot_matrix(arm)
                rw = om.MMatrix()
                if axis2_w is not None:
                    # 抬升轴必须跟着这根羽毛挂着的骨骼转过 ψ·t 一起转，
                    # 否则抬升方向会带上 cos(ψ·t)，ψ 超过 90° 的骨骼上的羽毛会往
                    # 翼面另一侧抬，一叠羽毛一半朝上一半朝下、在深度上互相穿过。
                    turned = rotate_vector(axis2_w, axis_w, math.radians(psi * t))
                    rw = axis_angle_matrix(turned, math.radians(item['tilt'] * u))
                # 偏移组上到底要补多少度：羽毛的目标是「世界朝向 = 静止朝向 绕 N 转过
                # sweep·u(t)」。但羽毛是挂在手臂骨骼下的，骨骼自己已经把它转过 ψ·t 了，
                # 所以补的是两者的差：
                #        补角 = sweep·u(t) − ψ·t
                # 必须分开写这两项！以前写成 (sweep − ψ)·u(t)，等于把「骨骼带着转的那
                # 部分」也乘上了羽毛的进度指数 u。凡是 ψ≠0 的骨骼（折叠后被转过去的
                # 腕/掌）上的羽毛，中途就会严重滞后甚至先反着转一下再回来：
                #   实测 ψ=170 的骨骼、sweep=92.5：25% 时目标 +49.6° 实际 −1.1°，
                #   50% 时目标 +67.7° 实际 −28.3°，75% 时目标 +81.3° 实际 −59.4°。
                # 相邻两根羽毛（一根挂在 ψ=0 的骨骼、一根挂在 ψ=170 的骨骼）在收起
                # 中段会一个转到位、一个还没动 —— 视觉上就是两片羽毛互相穿过去、整只
                # 翅膀乱成一团。分开写以后每根羽毛的世界朝向严格等于 sweep·u(t)：
                #   角度 = (1−u)·静止角 + u·目标角，顺序永远保持，羽毛不会互相穿过。
                rw = rw * axis_angle_matrix(
                    axis_w, math.radians(item['sweep'] * u - psi * t))
                rl = p * rw * p.inverse()
                # 同样做欧拉展开，否则羽毛会在某两个关键帧之间绕远路翻过去
                rot = list(unwrap_euler(prev_rot, None, 0, rl))
                prev_rot = list(rot)
                cmds.setAttr(grp + '.rotate', rot[0], rot[1], rot[2])
                for ax in ('X', 'Y', 'Z'):
                    cmds.setDrivenKeyframe(grp + '.rotate' + ax, cd=driver,
                                           itt='linear', ott='linear')
                # 层叠：沿翼面法线平移。法线 N 是折叠轴，绕自己转不改变方向，所以
                # 任何 t 下的世界方向都还是 axis_w；但父级骨骼转过 ψ·t 之后，
                # 这个世界方向在骨骼局部系里已经变了，必须按当时的 P 换算。
                # 偏移组和羽毛根骨骼写**同一个**局部位移 → 整根羽毛刚性平移。
                #
                # 试过让位移比 u 更快到位（u/0.5，想压中段「交叉最多 + 层还没分开」
                # 叠加出来的真穿模）：38 根 ±12° 夹具 80% 档 51 → 49 对、60% 档
                # 23 → 19 对，两端不变、共面夹具仍 0 对。**只降 4%**，却让羽毛在
                # 收起前 1/3 就提前离开手臂（视觉上是「先浮起来」）—— 收益不抵代价，
                # 已改回按 u 线性到位。
                dw = axis_w * (item['depth'] * u)
                dl = om.MPoint(dw.x, dw.y, dw.z) * p.inverse()
                for node, rest_t in ((grp, grp_rest), (root, root_rest)):
                    cmds.setAttr(node + '.translate', rest_t[0] + dl.x,
                                 rest_t[1] + dl.y, rest_t[2] + dl.z)
                    for ax in ('X', 'Y', 'Z'):
                        cmds.setDrivenKeyframe(node + '.translate' + ax, cd=driver,
                                               itt='linear', ott='linear')

    def remove_driven(self, ctrl):
        """拆除绑定：删掉约束、控制器、偏移组、样条、驱动关键帧与定位器，并还原关节旋转"""
        if not cmds.objExists(ctrl):
            return
        info = self.rigs.get(ctrl)
        if info is None:
            # 老版本建的绑定没往控制器上写登记表，只能删掉控制器本身，
            # 约束 / 驱动关键帧得手工清——至少要让用户知道，别以为删干净了
            cmds.warning('这套绑定缺少登记信息（可能是旧版本建的），'
                         '只能删掉控制器本身，约束和驱动关键帧需要手工清理')
        # 顺序：先解掉约束（否则羽毛骨骼一直被约束拽着），再删驱动关键帧与控制器层级，
        #       然后清掉定位器 / pointOnCurveInfo / 末端换算节点，最后复位所有骨骼旋转
        if info and info.get('extras'):
            # 挂在偏移组 rotate / 折叠偏移组 rotate / 羽毛骨骼上的驱动关键帧
            dead = []
            for name in list(info.get('offsets', {}).values()):
                if cmds.objExists(name):
                    dead += cmds.listConnections(name, s=True, d=False,
                                                 type='animCurve') or []
            for e in info['extras']:
                for name in (e.get('grp'), e['root']):
                    if name and cmds.objExists(name):
                        dead += cmds.listConnections(name, s=True, d=False,
                                                     type='animCurve') or []
            if dead:
                cmds.delete(list(set(dead)))
            cons = [c for e in info['extras'] for c in e.get('constraints', [])
                    if cmds.objExists(c)]
            if cons:
                cmds.delete(cons)
            helpers = [n for e in info['extras']
                       for n in list(e.get('locators', [])) + list(e.get('poci', []))
                       + list(e.get('tip_nodes', []))
                       if cmds.objExists(n)]
            if helpers:
                cmds.delete(helpers)
            # 偏移组是控制器 / 样条 / 末端方块的父级，删掉它整棵子树就一起清掉了
            tops = [e['grp'] for e in info['extras']
                    if e.get('grp') and cmds.objExists(e['grp'])]
            if tops:
                cmds.delete(tops)
        curves = cmds.listConnections(ctrl + '.' + FOLD_ATTR, d=True, s=False,
                                      type='animCurve') or []
        if curves:
            cmds.delete(curves)
        if info:
            for j, tx in info.get('rest_translate', {}).items():
                if cmds.objExists(j):
                    cmds.setAttr(j + '.translate', tx[0], tx[1], tx[2])
            for j, rot in info['rest_rotate'].items():
                if cmds.objExists(j):
                    cmds.setAttr(j + '.rotate', rot[0], rot[1], rot[2])
            # 最后再拆 FK 偏移组：它会把位移还给骨骼并挂回原父级，收尾到这里正好
            self.remove_fk_offsets(info.get('offsets') or {})

    # -------------------------------------------------------- 预览与删除
    def refresh_rig_combo(self, select=None):
        self.combo_rig.blockSignals(True)
        self.combo_rig.clear()
        for ctrl in self.rigs.keys():
            if cmds.objExists(ctrl):
                self.combo_rig.addItem(ctrl)
        if select and self.combo_rig.findText(select) >= 0:
            self.combo_rig.setCurrentIndex(self.combo_rig.findText(select))
        self.combo_rig.blockSignals(False)

    def on_rig_changed(self, index):
        if index < 0:
            return
        self.current_ctrl = self.combo_rig.currentText()
        self.sync_fold_from_ctrl()

    def sync_fold_from_ctrl(self):
        ctrl = self.current_ctrl
        if ctrl and cmds.objExists(ctrl) and cmds.attributeQuery(FOLD_ATTR, n=ctrl, ex=True):
            value = cmds.getAttr(ctrl + '.' + FOLD_ATTR)
            self.slider_fold.blockSignals(True)
            self.spin_fold.blockSignals(True)
            self.slider_fold.setValue(int(round(value * 100)))
            self.spin_fold.setValue(int(round(value * 100)))
            self.slider_fold.blockSignals(False)
            self.spin_fold.blockSignals(False)

    def on_fold_slider(self, value):
        self.spin_fold.blockSignals(True)
        self.spin_fold.setValue(value)
        self.spin_fold.blockSignals(False)
        self.apply_fold(value)

    def on_fold_spin(self, value):
        self.slider_fold.blockSignals(True)
        self.slider_fold.setValue(value)
        self.slider_fold.blockSignals(False)
        self.apply_fold(value)

    def apply_fold(self, percent):
        ctrl = self.current_ctrl
        if not ctrl or not cmds.objExists(ctrl):
            return
        if not cmds.attributeQuery(FOLD_ATTR, n=ctrl, ex=True):
            return
        cmds.setAttr(ctrl + '.' + FOLD_ATTR, percent / 100.0)

    def set_fold(self, percent):
        """把收起拨到某个百分比（「展开 / 收起」按钮、生成完复位、自检开头都走这里）

        必须**直接写属性**，不能只动滑块：滑块的值没变时 Qt 根本不发 valueChanged
        信号，属性就一点没动。而属性是会被外部改掉的 —— 播放收起动画、脚本 setAttr、
        或者拖过滑块之后又被驱动曲线拉回去。这时滑块停在旧值上，
        点「展开 / 收起」就会毫无反应（实测：收起动画播到 60 帧停下，再点「展开」
        翅膀不动）。所以这里自己 setValue 之后一定要补一次 apply_fold。
        """
        self.slider_fold.blockSignals(True)
        self.spin_fold.blockSignals(True)
        self.slider_fold.setValue(percent)
        self.spin_fold.setValue(percent)
        self.slider_fold.blockSignals(False)
        self.spin_fold.blockSignals(False)
        self.apply_fold(percent)

    def delete_rig(self):
        ctrl = self.combo_rig.currentText() or self.current_ctrl
        if not ctrl or not cmds.objExists(ctrl):
            cmds.warning('没有可删除的绑定')
            return
        cmds.undoInfo(openChunk=True, chunkName='Delete Wing Rig')
        try:
            self.remove_driven(ctrl)
            cmds.delete(ctrl)
        finally:
            cmds.undoInfo(closeChunk=True)
        self.rigs.pop(ctrl, None)
        if self.current_ctrl == ctrl:
            self.current_ctrl = None
        self.refresh_rig_combo()
        self.label_info.setText('')
        print('[翅膀绑定] 已删除绑定: ' + ctrl)


window = Window()
if __name__ == '__main__':
    window.show()
