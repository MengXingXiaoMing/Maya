# -*- coding: utf-8 -*-
"""
transformTransfer 误差校正·四对象对比演示
==========================================
四个对象角色：
  A_ctrl    控制源(手动旋转/动画驱动)
  B_orient  被 orientConstraint 旋转约束的(传统约束效果, 会翻转 ±180)
  C_ref     被 orientConstraint 约束, 同时作为节点的 refMatrix 参考(矫正方向来源)
  D_out     节点输出对象(增量累积 + 误差校正, 旋转可连续 >360° 不翻转)

连接关系：
  A -> orientConstraint -> B
  A -> orientConstraint -> C
  A.worldMatrix  -> 节点.inputMatrix
  C.worldMatrix  -> 节点.refMatrix (enableCorrection=True)
  节点.outputRotate -> D.rotate

用法：在 Maya Script Editor 里运行本文件。运行后选择 A_ctrl 旋转即可观察。
"""
import maya.cmds as cmds

PLUGIN_PATH = r'e:/code/my_code/IterativeVersion/Maya_PY3_plug-in_2025/2023/node/transformTransfer.py'

CTRL = 'A_ctrl'
ORIENT = 'B_orient'
REF = 'C_ref'
OUT = 'D_out'
NODE = 'tt_demo'


def load_plugin():
    for n in cmds.ls(type='transformTransfer'):
        cmds.delete(n)
    cmds.flushUndo()
    if cmds.pluginInfo('transformTransfer', q=True, loaded=True):
        cmds.unloadPlugin('transformTransfer')
    cmds.loadPlugin(PLUGIN_PATH)
    print('plugin loaded:', cmds.pluginInfo('transformTransfer', q=True, loaded=True))


def build():
    """建立 4 个对象、2 个约束、1 个节点，并完成连接。"""
    for n in [CTRL, ORIENT, REF, OUT, NODE]:
        if cmds.objExists(n):
            cmds.delete(n)

    # 四个立方体排成一排
    a = cmds.polyCube(name=CTRL)[0]
    b = cmds.polyCube(name=ORIENT)[0]
    c = cmds.polyCube(name=REF)[0]
    d = cmds.polyCube(name=OUT)[0]
    cmds.xform(a, t=[0, 0, 0], ws=True)
    cmds.xform(b, t=[4, 0, 0], ws=True)
    cmds.xform(c, t=[8, 0, 0], ws=True)
    cmds.xform(d, t=[12, 0, 0], ws=True)

    # 统一旋转顺序
    for obj in (a, b, c, d):
        cmds.setAttr(obj + '.rotateOrder', 0)

    # 着色区分
    cmds.polyColorPerVertex(a, rgb=[1, 0.2, 0.2], cdo=True)   # 红: 控制源
    cmds.polyColorPerVertex(b, rgb=[0.2, 0.6, 1], cdo=True)   # 蓝: 传统约束
    cmds.polyColorPerVertex(c, rgb=[0.2, 1, 0.4], cdo=True)   # 绿: 矫正参考
    cmds.polyColorPerVertex(d, rgb=[1, 1, 0.2], cdo=True)     # 黄: 节点输出

    # 两个 orientConstraint
    cmds.orientConstraint(a, b, mo=False)
    cmds.orientConstraint(a, c, mo=False)

    # 节点 + 连接
    n = cmds.createNode('transformTransfer', name=NODE)
    cmds.connectAttr(a + '.worldMatrix[0]', n + '.inputMatrix')
    cmds.connectAttr(c + '.worldMatrix[0]', n + '.refMatrix')
    cmds.setAttr(n + '.enableCorrection', True)
    cmds.connectAttr(n + '.outputRotate', d + '.rotate')

    print('=== 四对象建立完成 ===')
    print('红  A_ctrl   : 控制源(旋转它)')
    print('蓝  B_orient : 传统 orientConstraint(会翻转)')
    print('绿  C_ref    : 矫正参考(约束方向来源)')
    print('黄  D_out    : 节点输出(连续累积, 不翻转)')
    return a, b, c, d, n


def refresh(a):
    cmds.dgdirty(a)
    cmds.refresh()


def demo_spin(a, b, c, d, steps=24, deg_per_step=30):
    """演示: 用 xform ws 绕 Y 连续旋转控制源, 打印四对象对比。"""
    print('=== 演示: 控制源绕 Y 连续旋转(每步 %d 度 x %d) ===' % (deg_per_step, steps))
    print('%-8s %-14s %-14s %-14s %-14s' % ('step', 'A_ctrl.ry', 'B_orient.ry', 'C_ref.ry', 'D_out.ry'))
    cmds.setAttr(a + '.rotate', 0, 0, 0)
    refresh(a)
    prev = 0
    for i in range(1, steps + 1):
        prev += deg_per_step
        cmds.xform(a, rotation=[0, prev, 0], ws=True)
        refresh(a)
        if i % 2 == 0:  # 每 2 步打印一次, 减少输出
            print('%-8d %-14.1f %-14.1f %-14.1f %-14.1f' % (
                i,
                cmds.getAttr(a + '.rotateY'),
                cmds.getAttr(b + '.rotateY'),
                cmds.getAttr(c + '.rotateY'),
                cmds.getAttr(d + '.rotateY'),
            ))


# ======================================================================
load_plugin()
a, b, c, d, n = build()
cmds.currentTime(1)
refresh(a)

demo_spin(a, b, c, d, steps=24, deg_per_step=30)

print()
print('演示结束。现在可在视口中选择红方块 A_ctrl 手动旋转, 观察四对象差异。')
print('B_orient 会翻转到 ±180, D_out 连续累积。')
