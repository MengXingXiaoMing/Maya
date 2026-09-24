# coding=utf-8
"""
transformTransfer 节点
=======================
把一个源对象的位移/旋转实时传递到另一个目标对象，并对旋转做"解缠绕"
(unwrap)，使旋转值可以连续累积超过 360 度，不会像约束那样在 180 度处
翻转。

原理：
  约束(parentConstraint/orientConstraint)内部通过世界矩阵分解欧拉角，
  分解结果被归一化到 [-180, 180]，因此旋转一旦超过 180 度就会翻转回
  负值或 0。本节点改用"四元数增量累积"：
      - 每帧读取源对象世界矩阵，提取四元数 q_cur；
      - 与上一帧四元数 q_prev 求相对增量 delta = q_cur * q_prev^-1；
      - 取最短路径(delta.w < 0 时取负)后转为欧拉角增量；
      - 把增量累加到累计欧拉角上。
  由于逐帧累加的是"增量"，累计值可以无限增长(如 720、1080...)。

用法：
  1. 加载插件:  cmds.loadPlugin('transformTransfer.py')
  2. 创建节点:  n = cmds.createNode('transformTransfer')
  3. 连接源:    cmds.connectAttr(src + '.worldMatrix[0]', n + '.inputMatrix')
  4. 连接目标:  cmds.connectAttr(n + '.outputTranslate', dst + '.translate')
                cmds.connectAttr(n + '.outputRotate',   dst + '.rotate')
  5. 按需设置 rotateOrder 与目标对象一致。
"""
import math
import sys

import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds


# 枚举 rotateOrder -> MEulerRotation.RotationOrder 的映射
_ROTATE_ORDER_MAP = {
    0: om.MEulerRotation.kXYZ,
    1: om.MEulerRotation.kYZX,
    2: om.MEulerRotation.kZXY,
    3: om.MEulerRotation.kXZY,
    4: om.MEulerRotation.kYXZ,
    5: om.MEulerRotation.kZYX,
}


class TransformTransfer(ompx.MPxNode):
    """实时传递位移/旋转并解缠绕的 MPxNode。"""

    kNodeName = "transformTransfer"
    kNodeId = om.MTypeId(0x00151501)

    # 输入
    inMatrix = om.MObject()       # 源对象世界矩阵
    inRotateOrder = om.MObject()  # 输出欧拉角旋转顺序(枚举)
    refMatrix = om.MObject()      # 参考对象世界矩阵(可选, 用于误差校正)
    enableCorrection = om.MObject()  # 是否启用误差校正(布尔)

    # 输出
    outputTranslate = om.MObject()
    outputRotate = om.MObject()

    # 内部状态(隐藏、可存储、不可连接)
    stateQuatX = om.MObject()
    stateQuatY = om.MObject()
    stateQuatZ = om.MObject()
    stateQuatW = om.MObject()
    stateEulerX = om.MObject()
    stateEulerY = om.MObject()
    stateEulerZ = om.MObject()
    stateInit = om.MObject()

    def __init__(self):
        super(TransformTransfer, self).__init__()

    # ------------------------------------------------------------------
    def _plug_belongs(self, plug, compound_attr):
        """判断 plug 是否等于 compound_attr 或为其子属性。"""
        try:
            if plug.attribute() == compound_attr:
                return True
            if plug.isChild():
                parent = plug.parent()
                if not parent.isNull and parent.attribute() == compound_attr:
                    return True
        except Exception:
            pass
        return False

    # ------------------------------------------------------------------
    def compute(self, plug, dataBlock):
        # 分别处理位移输出与旋转输出
        if self._plug_belongs(plug, self.outputTranslate):
            mat = dataBlock.inputValue(self.inMatrix).asMatrix()
            tm = om.MTransformationMatrix(mat)
            translate = tm.translation(om.MSpace.kWorld)
            t_out = dataBlock.outputValue(self.outputTranslate)
            t_out.set3Double(translate.x, translate.y, translate.z)
            t_out.setClean()
            dataBlock.setClean(plug)
            return om.kUnknownParameter

        if self._plug_belongs(plug, self.outputRotate):
            # 读输入矩阵
            mat = dataBlock.inputValue(self.inMatrix).asMatrix()
            tm = om.MTransformationMatrix(mat)

            # 读旋转顺序
            order_enum = dataBlock.inputValue(self.inRotateOrder).asShort()
            order = _ROTATE_ORDER_MAP.get(order_enum, om.MEulerRotation.kXYZ)

            # 当前帧四元数(从矩阵旋转提取, 与顺序无关)
            q_cur = tm.rotation()

            # 读状态
            init = dataBlock.inputValue(self.stateInit).asBool()
            q_prev = om.MQuaternion(
                dataBlock.inputValue(self.stateQuatX).asFloat(),
                dataBlock.inputValue(self.stateQuatY).asFloat(),
                dataBlock.inputValue(self.stateQuatZ).asFloat(),
                dataBlock.inputValue(self.stateQuatW).asFloat(),
            )
            acc = om.MVector(
                dataBlock.inputValue(self.stateEulerX).asFloat(),
                dataBlock.inputValue(self.stateEulerY).asFloat(),
                dataBlock.inputValue(self.stateEulerZ).asFloat(),
            )

            if not init:
                # 首帧: 用当前旋转初始化累计欧拉角
                e0 = q_cur.asEulerRotation()
                out_euler = om.MVector(
                    math.degrees(e0.x),
                    math.degrees(e0.y),
                    math.degrees(e0.z),
                )
            else:
                # 相对旋转增量
                delta = q_cur * q_prev.conjugate()
                # 取最短路径(四元数双覆盖)
                if delta.w < 0.0:
                    delta = om.MQuaternion(-delta.x, -delta.y, -delta.z, -delta.w)
                # 增量转欧拉角(默认 kXYZ), 再重排到目标旋转顺序
                de = delta.asEulerRotation()
                de.reorderIt(order)
                # 累计
                out_euler = om.MVector(
                    acc.x + math.degrees(de.x),
                    acc.y + math.degrees(de.y),
                    acc.z + math.degrees(de.z),
                )

            # 可选误差校正: 用参考对象(由 Maya 自带约束驱动)的准确方向,
            # 把累积值按"整数周"对齐回正确方向, 消除增量累积的漂移。
            if dataBlock.inputValue(self.enableCorrection).asBool():
                ref_mat = dataBlock.inputValue(self.refMatrix).asMatrix()
                ref_tm = om.MTransformationMatrix(ref_mat)
                ref_e = ref_tm.rotation().asEulerRotation()
                ref_e.reorderIt(order)
                ref_deg = (math.degrees(ref_e.x), math.degrees(ref_e.y), math.degrees(ref_e.z))
                out_deg = (out_euler.x, out_euler.y, out_euler.z)
                # 对每个轴: 保留累积值提供的"圈数", 用参考方向修正 0~360 内的值
                corr = []
                for axis in range(3):
                    # 找最接近 out_deg 的、与 ref_deg 相差 360 整数倍的值
                    n = round((out_deg[axis] - ref_deg[axis]) / 360.0)
                    corr.append(ref_deg[axis] + n * 360.0)
                out_euler = om.MVector(corr[0], corr[1], corr[2])

            # 写状态
            dataBlock.outputValue(self.stateQuatX).setFloat(q_cur.x)
            dataBlock.outputValue(self.stateQuatY).setFloat(q_cur.y)
            dataBlock.outputValue(self.stateQuatZ).setFloat(q_cur.z)
            dataBlock.outputValue(self.stateQuatW).setFloat(q_cur.w)
            dataBlock.outputValue(self.stateEulerX).setFloat(out_euler.x)
            dataBlock.outputValue(self.stateEulerY).setFloat(out_euler.y)
            dataBlock.outputValue(self.stateEulerZ).setFloat(out_euler.z)
            dataBlock.outputValue(self.stateInit).setBool(True)

            r_out = dataBlock.outputValue(self.outputRotate)
            r_out.set3Double(out_euler.x, out_euler.y, out_euler.z)
            r_out.setClean()

            dataBlock.setClean(plug)
            return om.kUnknownParameter

        return om.kUnknownParameter

    # ------------------------------------------------------------------
    @classmethod
    def nodeInitializer(cls):
        n_attr = om.MFnNumericAttribute()
        m_attr = om.MFnMatrixAttribute()
        e_attr = om.MFnEnumAttribute()

        # 输入矩阵
        cls.inMatrix = m_attr.create("inputMatrix", "im", om.MFnMatrixAttribute.kDouble)
        m_attr.setStorable(True)
        m_attr.setConnectable(True)
        m_attr.setReadable(True)
        m_attr.setWritable(True)
        cls.addAttribute(cls.inMatrix)

        # 旋转顺序枚举
        cls.inRotateOrder = e_attr.create("rotateOrder", "ro", 0)
        e_attr.addField("xyz", 0)
        e_attr.addField("yzx", 1)
        e_attr.addField("zxy", 2)
        e_attr.addField("xzy", 3)
        e_attr.addField("yxz", 4)
        e_attr.addField("zyx", 5)
        e_attr.setStorable(True)
        e_attr.setKeyable(True)
        cls.addAttribute(cls.inRotateOrder)

        # 参考对象世界矩阵(可选, 用于误差校正)
        cls.refMatrix = m_attr.create("refMatrix", "rfm", om.MFnMatrixAttribute.kDouble)
        m_attr.setStorable(True)
        m_attr.setConnectable(True)
        m_attr.setReadable(True)
        m_attr.setWritable(True)
        cls.addAttribute(cls.refMatrix)

        # 是否启用误差校正
        cls.enableCorrection = n_attr.create("enableCorrection", "ecor", om.MFnNumericData.kBoolean, False)
        n_attr.setStorable(True)
        n_attr.setKeyable(True)
        n_attr.setWritable(True)
        cls.addAttribute(cls.enableCorrection)

        # 输出位移
        tx = n_attr.create("outputTranslateX", "otx", om.MFnNumericData.kDouble, 0.0)
        ty = n_attr.create("outputTranslateY", "oty", om.MFnNumericData.kDouble, 0.0)
        tz = n_attr.create("outputTranslateZ", "otz", om.MFnNumericData.kDouble, 0.0)
        cls.outputTranslate = n_attr.create("outputTranslate", "ot", tx, ty, tz)
        n_attr.setWritable(False)
        n_attr.setStorable(False)
        n_attr.setKeyable(False)
        cls.addAttribute(cls.outputTranslate)

        # 输出旋转(解缠绕后, 可超过 360)
        rx = n_attr.create("outputRotateX", "orx", om.MFnNumericData.kDouble, 0.0)
        ry = n_attr.create("outputRotateY", "ory", om.MFnNumericData.kDouble, 0.0)
        rz = n_attr.create("outputRotateZ", "orz", om.MFnNumericData.kDouble, 0.0)
        cls.outputRotate = n_attr.create("outputRotate", "or", rx, ry, rz)
        n_attr.setWritable(False)
        n_attr.setStorable(False)
        n_attr.setKeyable(False)
        cls.addAttribute(cls.outputRotate)

        # 内部状态
        cls.stateQuatX = n_attr.create("stateQuatX", "sqx", om.MFnNumericData.kDouble, 0.0)
        cls.stateQuatY = n_attr.create("stateQuatY", "sqy", om.MFnNumericData.kDouble, 0.0)
        cls.stateQuatZ = n_attr.create("stateQuatZ", "sqz", om.MFnNumericData.kDouble, 0.0)
        cls.stateQuatW = n_attr.create("stateQuatW", "sqw", om.MFnNumericData.kDouble, 1.0)
        cls.stateEulerX = n_attr.create("stateEulerX", "sex", om.MFnNumericData.kDouble, 0.0)
        cls.stateEulerY = n_attr.create("stateEulerY", "sey", om.MFnNumericData.kDouble, 0.0)
        cls.stateEulerZ = n_attr.create("stateEulerZ", "sez", om.MFnNumericData.kDouble, 0.0)
        cls.stateInit = n_attr.create("stateInit", "sini", om.MFnNumericData.kBoolean, False)
        for a in (cls.stateQuatX, cls.stateQuatY, cls.stateQuatZ, cls.stateQuatW,
                  cls.stateEulerX, cls.stateEulerY, cls.stateEulerZ, cls.stateInit):
            n_attr.setWritable(True)
            n_attr.setStorable(True)
            n_attr.setHidden(True)
            n_attr.setConnectable(False)
            cls.addAttribute(a)

        # 依赖关系
        cls.attributeAffects(cls.inMatrix, cls.outputTranslate)
        cls.attributeAffects(cls.inMatrix, cls.outputRotate)
        cls.attributeAffects(cls.inRotateOrder, cls.outputRotate)
        cls.attributeAffects(cls.refMatrix, cls.outputRotate)
        cls.attributeAffects(cls.enableCorrection, cls.outputRotate)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(TransformTransfer())


def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            TransformTransfer.kNodeName,
            TransformTransfer.kNodeId,
            TransformTransfer.nodeCreator,
            TransformTransfer.nodeInitializer,
        )
    except Exception:
        sys.stderr.write("registerNode failed: %s\n" % TransformTransfer.kNodeName)
        raise


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(TransformTransfer.kNodeId)


if __name__ == "__main__":
    # 便捷测试: 在 Maya 脚本编辑器里直接运行本文件即可
    cmds.evalDeferred(
        'if cmds.pluginInfo("transformTransfer", q=True, loaded=True): '
        'cmds.unloadPlugin("transformTransfer")\n'
        'cmds.loadPlugin("transformTransfer.py")'
    )
