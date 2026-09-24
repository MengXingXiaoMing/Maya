# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys
import math
import maya.mel as mel
class ballRotate(ompx.MPxNode):
    def __init__(self):
        super(ballRotate, self).__init__()

    node_name = "ballRotate"
    n = 60  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 输入
    inTranslateX = om.MObject()  # 当前位置X
    inTranslateZ = om.MObject()  # 当前位置Z
    inDiameter = om.MObject()  # 球体直径
    inStartRotX = om.MObject()  # 初始旋转X (度)
    inStartRotY = om.MObject()
    inStartRotZ = om.MObject()
    # inTime = om.MObject()  # 当前时间（用于判断帧数）

    # 输出
    outRotate = om.MObject()  # 输出旋转
    outRotateX = om.MObject()
    outRotateY = om.MObject()
    outRotateZ = om.MObject()

    # 内部状态（用于记录上一帧位置）
    stateLastX = om.MObject()
    stateLastZ = om.MObject()
    stateInitialized = om.MObject()  # 标记是否已初始化

    outputRot = om.MVector(0.0, 0.0, 0.0)

    '''def compute(self, plug, dataBlock):
        # 只处理输出旋转属性
        if not (plug == self.outRotate or plug.parent() == self.outRotate):
            return om.kUnknownParameter

        # 获取当前旋转
        outRotateHandle = dataBlock.outputValue(self.outRotate)
        prevRot = outRotateHandle.asFloat3()

        # === 2. 获取输入数据 ===
        currentTime = cmds.currentTime(query=True)

        start_numHandle = dataBlock.inputValue(self.start_num)
        start_num = start_numHandle.asFloat()  # 直径

        diameterHandle = dataBlock.inputValue(self.inDiameter)
        diameter = diameterHandle.asFloat()  # 直径

        txHandle = dataBlock.inputValue(self.inTranslateX)
        tzHandle = dataBlock.inputValue(self.inTranslateZ)
        currentX = txHandle.asFloat()  # $tx
        currentZ = tzHandle.asFloat()  # $tz

        # 获取内部状态
        lastXHandle = dataBlock.inputValue(self.stateLastX)
        lastZHandle = dataBlock.inputValue(self.stateLastZ)
        lastX = lastXHandle.asFloat()  # 上一次的tx
        lastZ = lastZHandle.asFloat()  # 上一次的tz


        # 获取初始旋转
        startRxHandle = dataBlock.inputValue(self.inStartRotX)
        startRyHandle = dataBlock.inputValue(self.inStartRotY)
        startRzHandle = dataBlock.inputValue(self.inStartRotZ)
        startRot = om.MVector(
            startRxHandle.asFloat(),
            startRyHandle.asFloat(),
            startRzHandle.asFloat()
        )


        # === 3. 核心逻辑 (严格遵循表达式) ===
        if start_num >= currentTime:
            # print('计算')
            # 计算位移
            deltaX = currentX - lastX
            deltaZ = currentZ - lastZ

            # 计算位移距离
            distance = math.sqrt(deltaX * deltaX + deltaZ * deltaZ)

            if distance > 0.000001:
                # 单位化位移向量
                normX = deltaX / distance
                normZ = deltaZ / distance

                # 计算滚动角度 (表达式中的 $xrot)
                # 滚动角度 = (位移距离 / 圆周长) * 360度
                circumference = math.pi * diameter
                xrot = 360.0 * distance / circumference

                # 计算旋转角度（弧度）
                yrot_rad = math.atan2(normX, normZ)
                yrot = math.radians(yrot_rad)
                # print(yrot_rad)
                # 使用矩阵计算组合旋转
                # 第一步: Y轴旋转 -yRot
                rot1 = om.MEulerRotation(0, -yrot, 0, om.MEulerRotation.kXYZ)
                mat1 = rot1.asMatrix()

                # 第二步: X轴旋转 xRot
                rot2 = om.MEulerRotation(xrot, 0, 0, om.MEulerRotation.kXYZ)
                mat2 = rot2.asMatrix()

                # 第三步: Y轴旋转 yRot
                rot3 = om.MEulerRotation(0, yrot, 0, om.MEulerRotation.kXYZ)
                mat3 = rot3.asMatrix()

                # 组合旋转: mat3 * mat2 * mat1
                combinedMat = mat3 * mat2 * mat1

                # 将矩阵转换为变换矩阵，然后提取旋转
                transformMat = om.MTransformationMatrix(combinedMat)
                rotation = transformMat.rotation()

                # 转换为角度并
                self.outputRot.x = math.degrees(rotation.x)
                self.outputRot.y = math.degrees(rotation.y)
                self.outputRot.z = math.degrees(rotation.z)

            # else:
            #     # 位移太小，保持上一帧的旋转输出
            #     # 这里需要从输出属性获取上一帧的旋转值
            #     # outHandle = dataBlock.outputValue(self.outRotate)
            #     # prevRot = outHandle.asFloat3()
            #     self.outputRot.x = 0.0
            #     self.outputRot.y = 0.0
            #     self.outputRot.z = 0.0
        else:
            print('清理')
            # 第一帧或未初始化：使用初始旋转
            # outputRot = (0.0, 0.0, 0.0)  # startRot
            # 记录初始位置
            self.outputRot.x = startRot[0]
            self.outputRot.y = startRot[1]
            self.outputRot.z = startRot[2]

        # 设置上一刻缓存
        lastXHandle.setFloat(currentX)
        lastZHandle.setFloat(currentZ)
        # === 5. 设置输出 ===
        print(self.outputRot.x,self.outputRot.y,self.outputRot.z)
        outRotateHandle.set3Float(self.outputRot.x+prevRot[0], self.outputRot.y+prevRot[1], self.outputRot.z+prevRot[2])
        # print(self.outputRot.x, self.outputRot.y, self.outputRot.z)
        # 标记数据块为已更新
        dataBlock.setClean(plug)

        return'''

    def compute(self, plug, dataBlock):
        # 只处理旋转输出
        if not (plug == self.outRotate or plug.parent() == self.outRotate):
            return om.kUnknownParameter

        # 获取当前旋转
        outRotateHandle = dataBlock.outputValue(self.outRotate)
        prevRot = outRotateHandle.asFloat3()

        # 获取输入值
        currentTime = cmds.currentTime(query=True)

        start_numHandle = dataBlock.inputValue(self.start_num)
        start_num = start_numHandle.asFloat()

        diameterHandle = dataBlock.inputValue(self.inDiameter)
        diameter = diameterHandle.asFloat()

        txHandle = dataBlock.inputValue(self.inTranslateX)
        tzHandle = dataBlock.inputValue(self.inTranslateZ)
        currentX = txHandle.asFloat()
        currentZ = tzHandle.asFloat()

        # 获取内部状态
        lastXHandle = dataBlock.inputValue(self.stateLastX)
        lastZHandle = dataBlock.inputValue(self.stateLastZ)
        lastX = lastXHandle.asFloat()
        lastZ = lastZHandle.asFloat()

        # 获取初始旋转
        startRxHandle = dataBlock.inputValue(self.inStartRotX)
        startRyHandle = dataBlock.inputValue(self.inStartRotY)
        startRzHandle = dataBlock.inputValue(self.inStartRotZ)
        startRot = om.MVector(
            startRxHandle.asFloat(),
            startRyHandle.asFloat(),
            startRzHandle.asFloat()
        )

        # 初始化输出为初始旋转
        outputRot = om.MVector(startRot.x, startRot.y, startRot.z)

        if start_num >= currentTime:
            # 计算位移
            deltaX = currentX - lastX
            deltaZ = currentZ - lastZ
            distance = math.sqrt(deltaX * deltaX + deltaZ * deltaZ)

            if distance > 0.000001:
                # 计算移动方向
                normX = deltaX / distance
                normZ = deltaZ / distance

                # 计算X轴旋转角度（球体滚动）
                circumference = math.pi * diameter
                xrot = 360.0 * distance / circumference  # 角度值

                # 计算Y轴旋转角度（移动方向）- 这是关键修正
                yrot_rad = math.atan2(normX, normZ)  # 弧度值
                yrot_deg = math.degrees(yrot_rad)  # 角度值

                # print(f"位移: {distance}, X旋转: {xrot}°, Y旋转: {yrot_deg}°")

                # 使用矩阵计算旋转（模拟表达式的旋转顺序）
                # 第一步: Y轴旋转 -yrot（对应表达式：rotate -ws -r 0 (-yrot) 0）
                rot1 = om.MEulerRotation(0, -math.radians(yrot_deg), 0, om.MEulerRotation.kXYZ)
                mat1 = rot1.asMatrix()

                # 第二步: X轴旋转 xrot（对应表达式：rotate -ws -r (xrot) 0 0）
                rot2 = om.MEulerRotation(math.radians(xrot), 0, 0, om.MEulerRotation.kXYZ)
                mat2 = rot2.asMatrix()

                # 第三步: Y轴旋转 yrot（对应表达式：rotate -ws -r 0 (yrot) 0）
                rot3 = om.MEulerRotation(0, math.radians(yrot_deg), 0, om.MEulerRotation.kXYZ)
                mat3 = rot3.asMatrix()

                # 组合旋转: mat3 * mat2 * mat1（正确的乘法顺序）
                combinedMat = mat3 * mat2 * mat1

                # 转换为变换矩阵
                transformMat = om.MTransformationMatrix(combinedMat)

                # 获取旋转（作为四元数然后转换为欧拉角）
                rotation = transformMat.rotation()
                eulerRotation = rotation.asEulerRotation()

                # 计算最终旋转（基于初始旋转加上增量旋转）
                outputRot.x = startRot.x + math.degrees(eulerRotation.x)
                outputRot.y = startRot.y + math.degrees(eulerRotation.y)
                outputRot.z = startRot.z + math.degrees(eulerRotation.z)

                # 更新位置记录
                lastXHandle.setFloat(currentX)
                lastZHandle.setFloat(currentZ)

        # 设置输出旋转（不累加之前的旋转）
        outRotateHandle.set3Float(prevRot[0]+outputRot.x, prevRot[1]-outputRot.y, prevRot[2]-outputRot.z)

        # 标记为清洁
        dataBlock.setClean(plug)

        return

    @classmethod
    def nodeInitializer(cls):
        # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        uAttr = om.MFnUnitAttribute()
        tAttr = om.MFnTypedAttribute()

        # ----- 输入属性 -----
        # 直径
        cls.inDiameter = nAttr.create("diameter", "dia", om.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        cls.addAttribute(cls.inDiameter)

        # 初始旋转
        cls.inStartRotX = nAttr.create("startRotX", "srx", om.MFnNumericData.kFloat, 0.0)
        cls.inStartRotY = nAttr.create("startRotY", "sry", om.MFnNumericData.kFloat, 0.0)
        cls.inStartRotZ = nAttr.create("startRotZ", "srz", om.MFnNumericData.kFloat, 0.0)
        cls.inStartRot = nAttr.create("startRotate", "sr",
                                                 cls.inStartRotX,
                                                 cls.inStartRotY,
                                                 cls.inStartRotZ)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        cls.addAttribute(cls.inStartRot)

        # 当前位置
        # cls.inTranslateX = nAttr.create("translateX", "tx", om.MFnNumericData.kFloat, 0.0)
        # nAttr.setKeyable(True)
        # nAttr.setWritable(True)
        # cls.inTranslateZ = nAttr.create("translateZ", "tz", om.MFnNumericData.kFloat, 0.0)
        # nAttr.setKeyable(True)
        # nAttr.setWritable(True)
        # cls.addAttribute(cls.inTranslateX)
        # cls.addAttribute(cls.inTranslateZ)

        cls.inTranslateX = nAttr.create("translateX", "tx", om.MFnNumericData.kFloat, 0.0)
        cls.inTranslateY = nAttr.create("translateY", "ty", om.MFnNumericData.kFloat, 0.0)
        cls.inTranslateZ = nAttr.create("translateZ", "tz", om.MFnNumericData.kFloat, 0.0)
        cls.inTranslate = nAttr.create("translate", "t",
                                     cls.inTranslateX,
                                     cls.inTranslateY,
                                     cls.inTranslateZ)
        # nAttr.setArray(True)
        nAttr.setStorable(True)
        nAttr.setConnectable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.inTranslate)

        # 当前时间
        cls.start_num = uAttr.create("startNum", "sn", om.MFnUnitAttribute.kTime, 10.0)
        uAttr.setWritable(True)
        uAttr.setReadable(False)
        uAttr.setKeyable(True)
        cls.addAttribute(cls.start_num)

        # ----- 输出属性 -----
        cls.outRotateX = nAttr.create("outputRotateX", "orx", om.MFnNumericData.kFloat, 0.0)
        cls.outRotateY = nAttr.create("outputRotateY", "ory", om.MFnNumericData.kFloat, 0.0)
        cls.outRotateZ = nAttr.create("outputRotateZ", "orz", om.MFnNumericData.kFloat, 0.0)
        cls.outRotate = nAttr.create("outputRotate", "or",
                                                cls.outRotateX,
                                                cls.outRotateY,
                                                cls.outRotateZ)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setKeyable(False)
        cls.addAttribute(cls.outRotate)

        # ----- 内部状态属性 -----
        cls.stateLastX = nAttr.create("lastTranslateX", "ltx", om.MFnNumericData.kFloat, 0.0)
        cls.stateLastZ = nAttr.create("lastTranslateZ", "ltz", om.MFnNumericData.kFloat, 0.0)
        cls.stateInitialized = nAttr.create("initialized", "init", om.MFnNumericData.kBoolean, False)

        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setHidden(True)  # 对用户隐藏
        nAttr.setConnectable(False)

        cls.addAttribute(cls.stateLastX)
        cls.addAttribute(cls.stateLastZ)
        cls.addAttribute(cls.stateInitialized)

        # ----- 属性关联 -----
        # 所有输入属性都会影响输出
        cls.attributeAffects(cls.inTranslate, cls.outRotate)
        cls.attributeAffects(cls.inDiameter, cls.outRotate)
        cls.attributeAffects(cls.inStartRot, cls.outRotate)
        cls.attributeAffects(cls.start_num, cls.outRotate)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(ballRotate())


# 插件注册保持不变
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