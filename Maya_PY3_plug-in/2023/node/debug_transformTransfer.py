# -*- coding: utf-8 -*-
"""
transformTransfer 节点完整调试脚本(含误差校正)
================================================
功能：
  1. 把源对象 A 的位移/旋转实时传递到目标对象 B，旋转解缠绕(可累积 >360°)。
  2. 可选误差校正：用 Maya 自带约束(orientConstraint)驱动一个参考对象 R，
     提供"绝对准确的方向"。节点每帧把累积值按整数周对齐到 R 的方向，
     消除增量累积的漂移，同时保留超过 360° 的圈数。

用法：在 Maya Script Editor 里直接运行本文件。
"""
import maya.cmds as cmds

PLUGIN_PATH = r'e:/code/my_code/IterativeVersion/Maya_PY3_plug-in_2025/2023/node/transformTransfer.py'

SRC = 'A_src'
DST = 'B_dst'
REF = 'R_ref'
NODE = 'tt_debug'


def load_plugin():
    for n in cmds.ls(type='transformTransfer'):
        cmds.delete(n)
    cmds.flushUndo()
    if cmds.pluginInfo('transformTransfer', q=True, loaded=True):
        cmds.unloadPlugin('transformTransfer')
    cmds.loadPlugin(PLUGIN_PATH)
    print('plugin loaded:', cmds.pluginInfo('transformTransfer', q=True, loaded=True))


def build_and_connect(use_correction=True):
    """建立源/目标/参考对象、约束、节点，并完成连接。"""
    for n in [SRC, DST, REF, NODE]:
        if cmds.objExists(n):
            cmds.delete(n)

    a = cmds.polyCube(name=SRC)[0]
    b = cmds.polyCube(name=DST)[0]
    r = cmds.polyCube(name=REF)[0]

    cmds.xform(b, t=[4, 0, 0], ws=True)
    cmds.xform(r, t=[8, 0, 0], ws=True)

    cmds.setAttr(a + '.rotateOrder', 0)
    cmds.setAttr(b + '.rotateOrder', 0)
    cmds.setAttr(r + '.rotateOrder', 0)

    # Maya 自带约束: 用 orientConstraint 让参考对象 R 跟随 A 的准确方向
    # (注意: 约束会翻转到 ±180, 但方向绝对准确)
    cmds.orientConstraint(a, r, mo=False)

    n = cmds.createNode('transformTransfer', name=NODE)
    cmds.connectAttr(a + '.worldMatrix[0]', n + '.inputMatrix')
    cmds.connectAttr(n + '.outputTranslate', b + '.translate')
    cmds.connectAttr(n + '.outputRotate', b + '.rotate')

    # 误差校正连接
    if use_correction:
        cmds.connectAttr(r + '.worldMatrix[0]', n + '.refMatrix')
        cmds.setAttr(n + '.enableCorrection', True)
        print('误差校正: 开启 (refMatrix <-', r, ')')
    else:
        print('误差校正: 关闭')

    return a, b, r, n


def refresh(a):
    cmds.dgdirty(a)
    cmds.refresh()


# ======================================================================
load_plugin()
a, b, r, n = build_and_connect(use_correction=True)
cmds.currentTime(1)
refresh(a)

print('=== 对象与连接建立完成 ===')
print('src =', a, '| dst =', b, '| ref =', r, '| node =', n)

# ======================================================================
# 单轴旋转累积 + 误差校正对比
# ======================================================================
print('=== 单轴旋转累积(每步+30度 x15 = 450度), 校正后方向应与约束一致 ===')
cmds.setAttr(a + '.rotate', 0, 0, 0)
refresh(a)
for i in range(15):
    cmds.rotate(0, 30, 0, a, r=True, ws=True)
    refresh(a)
print('A.rotateY =', round(cmds.getAttr(a + '.rotateY'), 3),
      '| R.rotateY(约束) =', round(cmds.getAttr(r + '.rotateY'), 3),
      '| B.rotateY =', round(cmds.getAttr(b + '.rotateY'), 3))

# ======================================================================
# 关键: xform ws 走矩阵, 源欧拉角翻转, 校正后 B 应连续且方向准确
# ======================================================================
print('=== 关键: xform ws 走矩阵(源翻转), 校正后 B 连续累积 ===')
cmds.setAttr(a + '.rotate', 0, 0, 0)
refresh(a)
prev = 0
for i in range(15):
    prev += 30
    cmds.xform(a, rotation=[0, prev, 0], ws=True)
    refresh(a)
print('设置到', prev,
      '-> A.rotateY =', round(cmds.getAttr(a + '.rotateY'), 3),
      '| R.rotateY =', round(cmds.getAttr(r + '.rotateY'), 3),
      '| B.rotateY =', round(cmds.getAttr(b + '.rotateY'), 3))

# ======================================================================
# 三轴旋转 + 误差校正
# ======================================================================
print('=== 三轴同时旋转(每步 xyz 各+30度), 校正后方向应贴近约束 ===')
cmds.setAttr(a + '.rotate', 0, 0, 0)
refresh(a)
for i in range(6):
    cmds.rotate(30, 30, 30, a, r=True, ws=True)
    refresh(a)
print('A.rotate =', [round(v, 3) for v in cmds.getAttr(a + '.rotate')[0]])
print('R.rotate =', [round(v, 3) for v in cmds.getAttr(r + '.rotate')[0]])
print('B.rotate =', [round(v, 3) for v in cmds.getAttr(b + '.rotate')[0]])
