# coding=gbk
import maya.api.OpenMaya as om
import sys


def maya_useNewAPI():
    pass


class SimpleSplineIKNode(om.MPxNode):
    kNodeId = om.MTypeId(0x00141480 + 6)
    kNodeName = "simpleSplineIK"

    aInCurve = om.MObject()
    aInCurveWorldMatrix = om.MObject()
    aUpVector = om.MObject()
    aRadius = om.MObject()
    aAverage = om.MObject()
    aStartOffset = om.MObject()
    aOutMatrices = om.MObject()

    @staticmethod
    def creator():
        return SimpleSplineIKNode()

    @staticmethod
    def initialize():
        # ---------- inCurve ----------
        tAttr1 = om.MFnTypedAttribute()
        SimpleSplineIKNode.aInCurve = tAttr1.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        tAttr1.storable = True
        tAttr1.keyable = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aInCurve)

        # ---------- inWorldMatrix ----------
        mAttr1 = om.MFnMatrixAttribute()
        SimpleSplineIKNode.aInCurveWorldMatrix = mAttr1.create("inWorldMatrix", "iwm")
        mAttr1.storable = True
        mAttr1.keyable = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aInCurveWorldMatrix)

        # ---------- upVector ----------
        nAttr2 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aUpVector = nAttr2.createPoint("upVector", "upv")
        nAttr2.default = (0.0, 1.0, 0.0)
        nAttr2.storable = True
        nAttr2.keyable = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aUpVector)

        # ---------- radius (数组) ----------
        nAttr3 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aRadius = nAttr3.create("radius", "ras", om.MFnNumericData.kFloat, 0.0)
        nAttr3.array = True
        nAttr3.storable = True
        nAttr3.keyable = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aRadius)

        # ---------- average (布尔，开启后强制按全长均匀分布) ----------
        nAttr4 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aAverage = nAttr4.create("average", "avg", om.MFnNumericData.kBoolean, False)
        nAttr4.storable = True
        nAttr4.keyable = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aAverage)

        # ---------- startOffset (float，按曲线 spans 滑动) ----------
        nAttr5 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aStartOffset = nAttr5.create("startOffset", "sof", om.MFnNumericData.kFloat, 0.0)
        nAttr5.setMin(0.0)
        nAttr5.storable = True
        nAttr5.keyable = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aStartOffset)

        # ---------- outMatrices ----------
        mAttr2 = om.MFnMatrixAttribute()
        SimpleSplineIKNode.aOutMatrices = mAttr2.create("outMatrices", "omat")
        mAttr2.array = True
        mAttr2.usesArrayDataBuilder = True
        mAttr2.writable = False
        mAttr2.storable = False
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aOutMatrices)

        # ---------- 依赖关系 ----------
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aInCurve, SimpleSplineIKNode.aOutMatrices)
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aInCurveWorldMatrix, SimpleSplineIKNode.aOutMatrices)
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aUpVector, SimpleSplineIKNode.aOutMatrices)
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aRadius, SimpleSplineIKNode.aOutMatrices)
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aAverage, SimpleSplineIKNode.aOutMatrices)
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aStartOffset, SimpleSplineIKNode.aOutMatrices)

    # ==================================================================
    def compute(self, plug, dataBlock):
        # 兼容数组元素 plug 触发（API2.0 中数组输出可能传元素 plug）
        plugAttr = plug.attribute()
        if plugAttr != self.aOutMatrices and plugAttr != om.MObject.kNullObj:
            try:
                if plug.parent().attribute() != self.aOutMatrices:
                    return om.kUnknownParameter
            except:
                return om.kUnknownParameter

        curveHandle = dataBlock.inputValue(self.aInCurve)
        if curveHandle.data().isNull():
            dataBlock.setClean(plug)
            return

        curveFn = om.MFnNurbsCurve(curveHandle.asNurbsCurve())
        curveWorldMat = dataBlock.inputValue(self.aInCurveWorldMatrix).asMatrix()

        # 自动检测输出矩阵的已连接数量 = 骨骼数
        jointCount = self._countOutputConnections(plug.node())
        if jointCount < 2:
            jointCount = 2
        upVec = om.MVector(dataBlock.inputValue(self.aUpVector).asFloatVector()).normal()

        totalLength = curveFn.length()
        if totalLength < 0.0001:
            return

        # 读取半径数组（用 MPlug 读取）
        radiusValues = []
        radiusPlug = om.MPlug(plug.node(), self.aRadius)
        for i in range(jointCount - 1):
            elemPlug = radiusPlug.elementByLogicalIndex(i)
            if elemPlug.isNull:
                break
            val = elemPlug.asFloat()
            if val < 0.0001:
                break
            radiusValues.append(val)

        # 用 knot 向量获取真正的 u 值范围
        knots = curveFn.knots()
        uMin = float(knots[0])
        uMax = float(knots[-1])

        uniformFallback = dataBlock.inputValue(self.aAverage).asBool()
        startOffsetU = dataBlock.inputValue(self.aStartOffset).asFloat()

        # 首个骨骼按 spans 偏移：numSpans = numCVs - degree
        numSpans = curveFn.numCVs - curveFn.degree
        if numSpans < 1:
            numSpans = 1
        t = startOffsetU / float(numSpans)
        if t < 0.0: t = 0.0
        if t > 1.0: t = 1.0
        firstParam = uMin + (uMax - uMin) * t

        # 首个骨骼到达末端 → 所有骨骼全部刷新到末端
        if firstParam >= uMax - 0.00001:
            self._computeAllAtEnd(plug, curveFn, curveWorldMat, upVec,
                                  jointCount, uMax, dataBlock)
            return

        # average 开启 → 强制按全长均匀分布，无视 radius
        if uniformFallback:
            self._computeUniform(plug, curveFn, curveWorldMat, upVec,
                                 jointCount, uMin, uMax, dataBlock)
            return

        # 无半径 → 全部输出在 firstParam
        if not radiusValues:
            self._computeZero(plug, curveFn, curveWorldMat, upVec,
                              jointCount, firstParam, dataBlock)
            return

        # 半径驱动：球体交点法
        actualJointCount = min(jointCount, len(radiusValues) + 1)
        jointParams = [firstParam]
        jointWorldPositions = [
            om.MPoint(curveFn.getPointAtParam(firstParam, om.MSpace.kObject)) * curveWorldMat
        ]

        for i in range(1, actualJointCount):
            r = radiusValues[i - 1]
            if r <= 0.0001:
                break

            prevParam = jointParams[i - 1]
            prevPos   = jointWorldPositions[i - 1]

            crossings = self._findSphereCrossings(
                curveFn, curveWorldMat, prevParam, uMax, prevPos, r, totalLength)

            if crossings:
                # 取比当前 u 值大且最近的那个交点
                crossings.sort()
                nextParam = None
                for c in crossings:
                    if c > prevParam + 0.00001:
                        nextParam = c
                        break
                if nextParam is None:
                    nextParam = crossings[-1]  # 兜底：取最后一个
            else:
                nextParam = uMax

            if nextParam < prevParam:
                nextParam = prevParam

            jointParams.append(nextParam)
            jointWorldPositions.append(
                om.MPoint(curveFn.getPointAtParam(nextParam, om.MSpace.kObject)) * curveWorldMat)

            if nextParam >= uMax - 0.00001:
                break

        # 输出
        finalCount = len(jointParams)
        outArrayHandle = dataBlock.outputArrayValue(self.aOutMatrices)
        builder = om.MArrayDataBuilder(dataBlock, self.aOutMatrices, finalCount)

        for i in range(finalCount):
            self._buildMatrix(curveFn, jointParams[i], curveWorldMat, upVec, builder, i)

        outArrayHandle.set(builder)
        outArrayHandle.setAllClean()

        # 强制刷新所有输出元素，防止拖拽时只有部分元素更新
        arrayPlug = om.MPlug(plug.node(), self.aOutMatrices)
        for i in range(finalCount):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if not elemPlg.isNull:
                dataBlock.setClean(elemPlg)
        dataBlock.setClean(arrayPlug)

    # ==================================================================
    def _countOutputConnections(self, nodeObj):
        """统计 outMatrices 上有多少元素被连接，返回骨骼数量"""
        count = 0
        arrayPlug = om.MPlug(nodeObj, self.aOutMatrices)
        try:
            existing = arrayPlug.numElements()
        except:
            existing = 0
        # 先用 existing 作为上限，再探测具体连接
        maxCheck = max(existing, 32)
        for i in range(maxCheck):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if elemPlg.isNull:
                break
            dests = elemPlg.destinations()
            if dests and len(dests) > 0:
                count = i + 1
        return count

    # ==================================================================
    def _computeUniform(self, plug, curveFn, curveWorldMat, upVec,
                        jointCount, startParam, uMax, dataBlock):
        """弧长均匀分布，实时响应曲线全长变化"""
        totalLen = curveFn.length()
        outArrayHandle = dataBlock.outputArrayValue(self.aOutMatrices)
        builder = om.MArrayDataBuilder(dataBlock, self.aOutMatrices, jointCount)

        for i in range(jointCount):
            dist = totalLen * float(i) / float(jointCount - 1)
            param = curveFn.findParamFromLength(dist)
            self._buildMatrix(curveFn, param, curveWorldMat, upVec, builder, i)

        outArrayHandle.set(builder)
        outArrayHandle.setAllClean()

        arrayPlug = om.MPlug(plug.node(), self.aOutMatrices)
        for i in range(jointCount):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if not elemPlg.isNull:
                dataBlock.setClean(elemPlg)
        dataBlock.setClean(arrayPlug)

    # ==================================================================
    def _computeZero(self, plug, curveFn, curveWorldMat, upVec,
                      jointCount, firstParam, dataBlock):
        """无半径时，所有骨骼输出在 firstParam 位置"""
        outArrayHandle = dataBlock.outputArrayValue(self.aOutMatrices)
        builder = om.MArrayDataBuilder(dataBlock, self.aOutMatrices, jointCount)

        for i in range(jointCount):
            self._buildMatrix(curveFn, firstParam, curveWorldMat, upVec, builder, i)

        outArrayHandle.set(builder)
        outArrayHandle.setAllClean()

        arrayPlug = om.MPlug(plug.node(), self.aOutMatrices)
        for i in range(jointCount):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if not elemPlg.isNull:
                dataBlock.setClean(elemPlg)
        dataBlock.setClean(arrayPlug)

    # ==================================================================
    def _computeAllAtEnd(self, plug, curveFn, curveWorldMat, upVec,
                         jointCount, uMax, dataBlock):
        """首个骨骼到末端时，所有骨骼输出在曲线末端"""
        outArrayHandle = dataBlock.outputArrayValue(self.aOutMatrices)
        builder = om.MArrayDataBuilder(dataBlock, self.aOutMatrices, jointCount)

        for i in range(jointCount):
            self._buildMatrix(curveFn, uMax, curveWorldMat, upVec, builder, i)

        outArrayHandle.set(builder)
        outArrayHandle.setAllClean()

        arrayPlug = om.MPlug(plug.node(), self.aOutMatrices)
        for i in range(jointCount):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if not elemPlg.isNull:
                dataBlock.setClean(elemPlg)
        dataBlock.setClean(arrayPlug)

    # ==================================================================
    def _findSphereCrossings(self, curveFn, curveWorldMat,
                             startU, endU, center, radius, totalLength):
        numSamples = max(int(totalLength * 60), 120)
        crossings = []
        prevDist = None
        prevU = startU

        for s in range(numSamples + 1):
            t = float(s) / numSamples
            sampleU = startU + (endU - startU) * t

            pWorld = om.MPoint(curveFn.getPointAtParam(sampleU, om.MSpace.kObject)) * curveWorldMat
            dist = (pWorld - center).length()

            if prevDist is not None:
                if (prevDist - radius) * (dist - radius) <= 0.0:
                    lo, hi = prevU, sampleU
                    for _ in range(15):
                        mid = (lo + hi) * 0.5
                        midPW = om.MPoint(curveFn.getPointAtParam(mid, om.MSpace.kObject)) * curveWorldMat
                        midDist = (midPW - center).length()
                        if midDist < radius:
                            lo = mid
                        else:
                            hi = mid
                    crossings.append(hi)

            prevDist = dist
            prevU = sampleU

        return crossings

    # ==================================================================
    def _buildMatrix(self, curveFn, param, curveWorldMat, upVec, builder, index):
        posLocal = om.MPoint(curveFn.getPointAtParam(param, om.MSpace.kObject))
        tangent  = curveFn.tangent(param, om.MSpace.kObject).normal()

        xAxis = tangent

        cross = xAxis ^ upVec
        if cross.length() < 0.0001:
            cross = xAxis ^ om.MVector(0.0, 0.0, 1.0)
            if cross.length() < 0.0001:
                cross = xAxis ^ om.MVector(1.0, 0.0, 0.0)
        zAxis = cross.normal()
        yAxis = (zAxis ^ xAxis).normal()

        matVals = [
            xAxis.x,   xAxis.y,   xAxis.z,   0.0,
            yAxis.x,   yAxis.y,   yAxis.z,   0.0,
            zAxis.x,   zAxis.y,   zAxis.z,   0.0,
            posLocal.x, posLocal.y, posLocal.z, 1.0,
        ]
        worldMat = om.MMatrix(matVals) * curveWorldMat

        hOut = builder.addElement(index)
        hOut.setMMatrix(worldMat)


# ======================================================================
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin, "KangmingZhan", "1.0", "Any")
    try:
        pluginFn.registerNode(
            SimpleSplineIKNode.kNodeName,
            SimpleSplineIKNode.kNodeId,
            SimpleSplineIKNode.creator,
            SimpleSplineIKNode.initialize)
        sys.stderr.write("simpleSplineIK registered OK\n")
    except Exception as e:
        sys.stderr.write("simpleSplineIK registration FAILED: " + str(e) + "\n")
        raise


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(SimpleSplineIKNode.kNodeId)
        sys.stderr.write("simpleSplineIK deregistered OK\n")
    except Exception as e:
        sys.stderr.write("simpleSplineIK deregister FAILED: " + str(e) + "\n")
        raise
