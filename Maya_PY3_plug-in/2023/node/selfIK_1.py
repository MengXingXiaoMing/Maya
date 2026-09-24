# coding=gbk
import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass


class SimpleSplineIKNode(om.MPxNode):
    kNodeId = om.MTypeId(0x00141480 + 19)
    kNodeName = "hierarchicalSplineIK"

    aInCurve = om.MObject()
    aInCurveWorldMatrix = om.MObject()
    aJointOffsets = om.MObject()  # 新增：每根骨骼距离起始点的长度
    aParentInverseMatrices = om.MObject()  # 新增：父级的世界逆矩阵
    aUpVector = om.MObject()
    aOutLocalMatrices = om.MObject()  # 输出：局部空间的矩阵

    def __init__(self):
        super(SimpleSplineIKNode, self).__init__()

    @classmethod
    def creator(cls):
        return SimpleSplineIKNode()

    @classmethod
    def initialize(cls):
        numAttr = om.MFnNumericAttribute()
        matAttr = om.MFnMatrixAttribute()
        typedAttr = om.MFnTypedAttribute()

        cls.aInCurve = typedAttr.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        cls.aInCurveWorldMatrix = matAttr.create("inWorldMatrix", "iwm")

        # 骨骼距离链条顶端的距离数组 (例如: [0, 2.5, 5.0, 7.5])
        cls.aJointOffsets = numAttr.create("jointOffsets", "jofs", om.MFnNumericData.kFloat, 0.0)
        numAttr.array = True

        # 输入父级的 World Inverse Matrix，用于抵消层级影响
        cls.aParentInverseMatrices = matAttr.create("parentInverseMatrices", "pim")
        matAttr.array = True

        cls.aUpVector = numAttr.createPoint("upVector", "upv")
        numAttr.default = (0.0, 1.0, 0.0)

        cls.aOutLocalMatrices = matAttr.create("outLocalMatrices", "olmat")
        matAttr.array = True
        matAttr.usesArrayDataBuilder = True
        matAttr.hidden = True

        cls.addAttribute(cls.aInCurve)
        cls.addAttribute(cls.aInCurveWorldMatrix)
        cls.addAttribute(cls.aJointOffsets)
        cls.addAttribute(cls.aParentInverseMatrices)
        cls.addAttribute(cls.aUpVector)
        cls.addAttribute(cls.aOutLocalMatrices)

        cls.attributeAffects(cls.aInCurve, cls.aOutLocalMatrices)
        cls.attributeAffects(cls.aInCurveWorldMatrix, cls.aOutLocalMatrices)
        cls.attributeAffects(cls.aJointOffsets, cls.aOutLocalMatrices)
        cls.attributeAffects(cls.aParentInverseMatrices, cls.aOutLocalMatrices)

    def compute(self, plug, dataBlock):
        if plug != self.aOutLocalMatrices and plug.parent() != self.aOutLocalMatrices:
            return om.kUnknownParameter

        curveHandle = dataBlock.inputValue(self.aInCurve)
        if curveHandle.data().isNull():
            return

        curveFn = om.MFnNurbsCurve(curveHandle.asNurbsCurve())
        curveWorldMat = dataBlock.inputValue(self.aInCurveWorldMatrix).asMatrix()
        upVec = om.MVector(dataBlock.inputValue(self.aUpVector).asFloatVector()).normal()

        # 获取数组输入
        offsetHandle = dataBlock.inputArrayValue(self.aJointOffsets)
        parentInvHandle = dataBlock.inputArrayValue(self.aParentInverseMatrices)

        count = len(offsetHandle)
        builder = om.MArrayDataBuilder(dataBlock, self.aOutLocalMatrices, count)

        totalCurveLength = curveFn.length()

        for i in range(count):
            offsetHandle.jumpToLogicalElement(i)
            dist = offsetHandle.inputValue().asFloat()

            # 如果骨骼长度超过曲线，clamp在末尾或沿切线延伸
            if dist > totalCurveLength: dist = totalCurveLength

            param = curveFn.findParamFromLength(dist)
            pos_local = curveFn.getPointAtParam(param, om.MSpace.kObject)
            tangent_local = curveFn.tangent(param, om.MSpace.kObject).normal()

            # 构建世界空间目标矩阵
            x_axis = tangent_local
            z_axis = (x_axis ^ upVec).normal()
            y_axis = (z_axis ^ x_axis).normal()

            mat_vals = [
                x_axis.x, x_axis.y, x_axis.z, 0.0,
                y_axis.x, y_axis.y, y_axis.z, 0.0,
                z_axis.x, z_axis.y, z_axis.z, 0.0,
                pos_local.x, pos_local.y, pos_local.z, 1.0
            ]
            world_target = om.MMatrix(mat_vals) * curveWorldMat

            # 核心步骤：转换回父级的局部空间
            try:
                parentInvHandle.jumpToLogicalElement(i)
                parentInvMat = parentInvHandle.inputValue().asMatrix()
            except:
                parentInvMat = om.MMatrix.kIdentity  # 如果没有父级，则视为世界空间

            local_result = world_target * parentInvMat

            h_out = builder.addElement(i)
            h_out.setMMatrix(local_result)

        dataBlock.outputArrayValue(self.aOutLocalMatrices).set(builder)
        dataBlock.setClean(plug)


def initializePlugin(plugin):
    om.MFnPlugin(plugin, "Custom", "1.2", "Any").registerNode(SimpleSplineIKNode.kNodeName, SimpleSplineIKNode.kNodeId,
                                                              SimpleSplineIKNode.creator, SimpleSplineIKNode.initialize)


def uninitializePlugin(plugin):
    om.MFnPlugin(plugin).deregisterNode(SimpleSplineIKNode.kNodeId)

'''import maya.cmds as cmds

# 1. 准备骨骼链
joints = ["joint1", "joint2", "joint3", "joint4", "joint5"]  # 你的父子级骨骼
curve = "curveShape1"

# 2. 创建节点
node = cmds.createNode("hierarchicalSplineIK")
cmds.connectAttr(curve + ".local", node + ".inCurve")
cmds.connectAttr(curve + ".worldMatrix[0]", node + ".inWorldMatrix")

# 3. 计算并连接每根骨骼的偏移和父级矩阵
accumulated_dist = 0.0

for i, jnt in enumerate(joints):
    # 计算该骨骼相对于根部的累积距离（间距不变的关键）
    if i > 0:
        # 获取当前骨骼相对于父级的位移长度
        tx = cmds.getAttr(jnt + ".tx")
        ty = cmds.getAttr(jnt + ".ty")
        tz = cmds.getAttr(jnt + ".tz")
        dist = (tx ** 2 + ty ** 2 + tz ** 2) ** 0.5
        accumulated_dist += dist

    cmds.setAttr(f"{node}.jointOffsets[{i}]", accumulated_dist)

    # 连接父级的世界逆矩阵，用来抵消父级变换
    parent = cmds.listRelatives(jnt, parent=True)
    if parent:
        cmds.connectAttr(parent[0] + ".worldInverseMatrix[0]", f"{node}.parentInverseMatrices[{i}]")
    else:
        # 如果是根骨骼，没有父级，保持 parentInverseMatrices 为单位矩阵即可
        pass

    # 连接输出到 offsetParentMatrix
    cmds.connectAttr(f"{node}.outLocalMatrices[{i}]", jnt + ".offsetParentMatrix")

    # 清空骨骼自身的变换（重要：否则会跟矩阵叠加导致偏移）
    cmds.setAttr(jnt + ".t", 0, 0, 0)
    cmds.setAttr(jnt + ".r", 0, 0, 0)
    cmds.setAttr(jnt + ".jo", 0, 0, 0)'''