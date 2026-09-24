# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys
import math


class ballRotate(ompx.MPxNode):
    def __init__(self):
        super(ballRotate, self).__init__()

    node_name = "ballRotate"
    n = 108  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 输入
    inTranslate = om.MObject()
    inDiameter = om.MObject()
    inStartRot = om.MObject()
    startNum = om.MObject()

    # 输出
    outRotate = om.MObject()

    # 内部状态
    stateLastPos = om.MObject()
    stateLastRot = om.MObject()
    stateInitialized = om.MObject()

    def compute(self, plug, dataBlock):
        if not (plug == self.outRotate or plug.parent() == self.outRotate):
            return om.kUnknownParameter

        # === 获取数据 ===
        currentTime = cmds.currentTime(query=True)

        startNumHandle = dataBlock.inputValue(self.startNum)
        startNum = startNumHandle.asTime().value()

        diameterHandle = dataBlock.inputValue(self.inDiameter)
        diameter = diameterHandle.asFloat()

        translateHandle = dataBlock.inputValue(self.inTranslate)
        translate = translateHandle.asFloat3()
        currentPos = om.MVector(translate[0], translate[1], translate[2])

        startRotHandle = dataBlock.inputValue(self.inStartRot)
        startRotVec = startRotHandle.asFloat3()
        startRot = om.MVector(startRotVec[0], startRotVec[1], startRotVec[2])

        lastPosHandle = dataBlock.inputValue(self.stateLastPos)
        lastPosVec = lastPosHandle.asFloat3()
        lastPos = om.MVector(lastPosVec[0], lastPosVec[1], lastPosVec[2])

        lastRotHandle = dataBlock.inputValue(self.stateLastRot)
        lastRotVec = lastRotHandle.asFloat3()
        lastRot = om.MVector(lastRotVec[0], lastRotVec[1], lastRotVec[2])

        initHandle = dataBlock.inputValue(self.stateInitialized)
        initialized = initHandle.asBool()

        # === 初始化检查 ===
        if not initialized:
            # 第一帧：使用初始旋转
            outRotateHandle = dataBlock.outputValue(self.outRotate)
            outRotateHandle.set3Float(startRot.x, startRot.y, startRot.z)

            # 保存当前状态
            lastPosHandle.set3Float(currentPos.x, currentPos.y, currentPos.z)
            lastRotHandle.set3Float(startRot.x, startRot.y, startRot.z)
            initHandle.setBool(True)

            dataBlock.setClean(plug)
            return

        if startNum > currentTime:
            # 时间未到，使用初始旋转
            outRotateHandle = dataBlock.outputValue(self.outRotate)
            outRotateHandle.set3Float(startRot.x, startRot.y, startRot.z)

            lastPosHandle.set3Float(currentPos.x, currentPos.y, currentPos.z)
            lastRotHandle.set3Float(startRot.x, startRot.y, startRot.z)

            dataBlock.setClean(plug)
            return

        # === 计算滚动 ===
        displacement = currentPos - lastPos
        distance = displacement.length()

        if distance < 0.000001:
            # 没有位移，保持上一帧旋转
            outRotateHandle = dataBlock.outputValue(self.outRotate)
            outRotateHandle.set3Float(lastRot.x, lastRot.y, lastRot.z)

            dataBlock.setClean(plug)
            return

        # 计算球体半径
        radius = diameter / 2.0

        # 计算滚动角度（弧度）
        rollAngle = distance / radius

        # 位移方向
        worldDispDir = displacement.normal()

        # 计算旋转轴：位移方向 × 垂直方向
        vertical = om.MVector(0, 1, 0)
        axis = worldDispDir ^ vertical

        if axis.length() < 0.000001:
            # 特殊情况：位移方向与垂直方向平行
            outRotateHandle = dataBlock.outputValue(self.outRotate)
            outRotateHandle.set3Float(lastRot.x, lastRot.y, lastRot.z)

            # 更新位置
            lastPosHandle.set3Float(currentPos.x, currentPos.y, currentPos.z)

            dataBlock.setClean(plug)
            return

        # 归一化旋转轴
        axis.normalize()

        # === 正确的MQuaternion创建方式 ===
        # 方法1：使用角度和轴
        rotationQuat = om.MQuaternion(rollAngle, axis)

        # 将上一帧的旋转转换为四元数
        # 方法2：使用MEulerRotation的asQuaternion方法
        lastEuler = om.MEulerRotation(
            math.radians(lastRot.x),
            math.radians(lastRot.y),
            math.radians(lastRot.z)
        )
        lastQuat = lastEuler.asQuaternion()

        # 应用新的旋转（乘法顺序很重要：新旋转 * 旧旋转）
        newQuat = rotationQuat * lastQuat

        # 转换为欧拉角
        newEuler = newQuat.asEulerRotation()

        # 转换为角度
        newRot = om.MVector(
            math.degrees(newEuler.x),
            math.degrees(newEuler.y),
            math.degrees(newEuler.z)
        )

        # === 设置输出 ===
        outRotateHandle = dataBlock.outputValue(self.outRotate)
        outRotateHandle.set3Float(newRot.x, newRot.y, newRot.z)

        # === 更新内部状态 ===
        lastPosHandle.set3Float(currentPos.x, currentPos.y, currentPos.z)
        lastRotHandle.set3Float(newRot.x, newRot.y, newRot.z)

        dataBlock.setClean(plug)
        return

    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
        uAttr = om.MFnUnitAttribute()

        # ----- 输入属性 -----
        cls.inDiameter = nAttr.create("diameter", "dia", om.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        cls.addAttribute(cls.inDiameter)

        startRotX = nAttr.create("startRotX", "srx", om.MFnNumericData.kFloat, 0.0)
        startRotY = nAttr.create("startRotY", "sry", om.MFnNumericData.kFloat, 0.0)
        startRotZ = nAttr.create("startRotZ", "srz", om.MFnNumericData.kFloat, 0.0)
        cls.inStartRot = nAttr.create("startRotate", "sr", startRotX, startRotY, startRotZ)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        cls.addAttribute(cls.inStartRot)

        translateX = nAttr.create("translateX", "tx", om.MFnNumericData.kFloat, 0.0)
        translateY = nAttr.create("translateY", "ty", om.MFnNumericData.kFloat, 0.0)
        translateZ = nAttr.create("translateZ", "tz", om.MFnNumericData.kFloat, 0.0)
        cls.inTranslate = nAttr.create("translate", "t", translateX, translateY, translateZ)
        nAttr.setStorable(True)
        nAttr.setConnectable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.inTranslate)

        cls.startNum = uAttr.create("startNum", "sn", om.MFnUnitAttribute.kTime, 10.0)
        uAttr.setWritable(True)
        uAttr.setReadable(False)
        uAttr.setKeyable(True)
        cls.addAttribute(cls.startNum)

        # ----- 输出属性 -----
        outRotateX = nAttr.create("outputRotateX", "orx", om.MFnNumericData.kFloat, 0.0)
        outRotateY = nAttr.create("outputRotateY", "ory", om.MFnNumericData.kFloat, 0.0)
        outRotateZ = nAttr.create("outputRotateZ", "orz", om.MFnNumericData.kFloat, 0.0)
        cls.outRotate = nAttr.create("outputRotate", "or", outRotateX, outRotateY, outRotateZ)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setKeyable(False)
        cls.addAttribute(cls.outRotate)

        # ----- 内部状态属性 -----
        lastPosX = nAttr.create("lastPosX", "lpx", om.MFnNumericData.kFloat, 0.0)
        lastPosY = nAttr.create("lastPosY", "lpy", om.MFnNumericData.kFloat, 0.0)
        lastPosZ = nAttr.create("lastPosZ", "lpz", om.MFnNumericData.kFloat, 0.0)
        cls.stateLastPos = nAttr.create("lastPosition", "lp", lastPosX, lastPosY, lastPosZ)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setHidden(True)
        nAttr.setConnectable(False)
        cls.addAttribute(cls.stateLastPos)

        lastRotX = nAttr.create("lastRotX", "lrx", om.MFnNumericData.kFloat, 0.0)
        lastRotY = nAttr.create("lastRotY", "lry", om.MFnNumericData.kFloat, 0.0)
        lastRotZ = nAttr.create("lastRotZ", "lrz", om.MFnNumericData.kFloat, 0.0)
        cls.stateLastRot = nAttr.create("lastRotation", "lr", lastRotX, lastRotY, lastRotZ)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setHidden(True)
        nAttr.setConnectable(False)
        cls.addAttribute(cls.stateLastRot)

        cls.stateInitialized = nAttr.create("initialized", "init", om.MFnNumericData.kBoolean, False)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setHidden(True)
        nAttr.setConnectable(False)
        cls.addAttribute(cls.stateInitialized)

        # ----- 属性关联 -----
        cls.attributeAffects(cls.inTranslate, cls.outRotate)
        cls.attributeAffects(cls.inDiameter, cls.outRotate)
        cls.attributeAffects(cls.inStartRot, cls.outRotate)
        cls.attributeAffects(cls.startNum, cls.outRotate)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(ballRotate())


def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            ballRotate.node_name,
            ballRotate.Uv_id,
            ballRotate.nodeCreator,
            ballRotate.nodeInitializer
        )
    except:
        sys.stderr.write(f"注册节点失败: {ballRotate.node_name}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(ballRotate.Uv_id)