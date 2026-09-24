# coding=gbk
import maya.api.OpenMaya as om
import sys


def maya_useNewAPI():
    pass


class SimpleSplineIKNode(om.MPxNode):
    kNodeId = om.MTypeId(0x00141480 + 35)
    kNodeName = "simpleSplineIK"

    aInCurve = om.MObject()
    aInCurveWorldMatrix = om.MObject()
    aUpVector = om.MObject()
    aRadius = om.MObject()
    aAverage = om.MObject()
    aStartOffset = om.MObject()
    aSampleDensity = om.MObject()
    aOutMatrices = om.MObject()

    def __init__(self):
        super(SimpleSplineIKNode, self).__init__()
        self._cachedJointCount = -1
        self._cachedNumElements = -1

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
        nAttr2.channelBox = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aUpVector)

        # ---------- radius (数组) ----------
        nAttr3 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aRadius = nAttr3.create("radius", "ras", om.MFnNumericData.kFloat, 0.0)
        nAttr3.array = True
        nAttr3.storable = True
        nAttr3.keyable = True
        nAttr3.channelBox = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aRadius)

        # ---------- average ----------
        nAttr4 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aAverage = nAttr4.create("average", "avg", om.MFnNumericData.kBoolean, False)
        nAttr4.storable = True
        nAttr4.keyable = True
        nAttr4.channelBox = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aAverage)

        # ---------- startOffset ----------
        nAttr5 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aStartOffset = nAttr5.create("startOffset", "sof", om.MFnNumericData.kFloat, 0.0)
        nAttr5.setMin(0.0)
        nAttr5.storable = True
        nAttr5.keyable = True
        nAttr5.channelBox = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aStartOffset)

        # ---------- sampleDensity ----------
        nAttr6 = om.MFnNumericAttribute()
        SimpleSplineIKNode.aSampleDensity = nAttr6.create("sampleDensity", "sden", om.MFnNumericData.kInt, 60)
        nAttr6.setMin(5)
        nAttr6.setMax(500)
        nAttr6.storable = True
        nAttr6.keyable = True
        nAttr6.channelBox = True
        SimpleSplineIKNode.addAttribute(SimpleSplineIKNode.aSampleDensity)

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
        SimpleSplineIKNode.attributeAffects(SimpleSplineIKNode.aSampleDensity, SimpleSplineIKNode.aOutMatrices)

    # ==================================================================
    def compute(self, plug, dataBlock):
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

        # 缓存骨骼数，仅在连接/断开时重新检测
        jointCount = self._getJointCount(plug.node())
        if jointCount < 2:
            jointCount = 2

        sampleDensity = dataBlock.inputValue(self.aSampleDensity).asInt()
        upVec = om.MVector(dataBlock.inputValue(self.aUpVector).asFloatVector()).normal()

        totalLength = curveFn.length()
        if totalLength < 0.0001:
            return

        # 读取半径数组（MPlug 读取，可靠稳定）
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

        knots = curveFn.knots()
        uMin = float(knots[0])
        uMax = float(knots[-1])

        uniformFallback = dataBlock.inputValue(self.aAverage).asBool()
        startOffsetU = dataBlock.inputValue(self.aStartOffset).asFloat()

        numSpans = curveFn.numCVs - curveFn.degree
        if numSpans < 1:
            numSpans = 1
        t = startOffsetU / float(numSpans)
        if t < 0.0: t = 0.0
        if t > 1.0: t = 1.0
        firstParam = uMin + (uMax - uMin) * t

        if firstParam >= uMax - 0.00001:
            self._computeAllAtEnd(plug, curveFn, curveWorldMat, upVec,
                                  jointCount, uMax, dataBlock)
            return

        if uniformFallback:
            self._computeUniform(plug, curveFn, curveWorldMat, upVec,
                                 jointCount, uMin, uMax, dataBlock)
            return

        if not radiusValues:
            self._computeZero(plug, curveFn, curveWorldMat, upVec,
                              jointCount, firstParam, dataBlock)
            return

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
                curveFn, curveWorldMat, prevParam, uMax, prevPos, r,
                totalLength, sampleDensity)

            if crossings:
                crossings.sort()
                nextParam = None
                for c in crossings:
                    if c > prevParam + 0.00001:
                        nextParam = c
                        break
                if nextParam is None:
                    nextParam = crossings[-1]
            else:
                nextParam = uMax

            if nextParam < prevParam:
                nextParam = prevParam

            jointParams.append(nextParam)
            jointWorldPositions.append(
                om.MPoint(curveFn.getPointAtParam(nextParam, om.MSpace.kObject)) * curveWorldMat)

            if nextParam >= uMax - 0.00001:
                break

        self._outputMatrices(plug, curveFn, curveWorldMat, upVec,
                             jointParams, dataBlock)

    # ==================================================================
    def _getJointCount(self, nodeObj):
        """缓存骨骼数，只在 outMatrices 元素个数变化时重新检测"""
        arrayPlug = om.MPlug(nodeObj, self.aOutMatrices)
        try:
            curNum = arrayPlug.numElements()
        except:
            curNum = 0

        if curNum == self._cachedNumElements and self._cachedJointCount >= 2:
            return self._cachedJointCount

        count = 0
        maxCheck = max(curNum, 32)
        for i in range(maxCheck):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if elemPlg.isNull:
                break
            dests = elemPlg.destinations()
            if dests and len(dests) > 0:
                count = i + 1

        self._cachedNumElements = curNum
        self._cachedJointCount = count
        return count

    # ==================================================================
    def _outputMatrices(self, plug, curveFn, curveWorldMat, upVec,
                        jointParams, dataBlock):
        """统一的输出逻辑 + 全元素 setClean"""
        finalCount = len(jointParams)
        outArrayHandle = dataBlock.outputArrayValue(self.aOutMatrices)
        builder = om.MArrayDataBuilder(dataBlock, self.aOutMatrices, finalCount)

        for i in range(finalCount):
            self._buildMatrix(curveFn, jointParams[i], curveWorldMat, upVec, builder, i)

        outArrayHandle.set(builder)
        outArrayHandle.setAllClean()

        arrayPlug = om.MPlug(plug.node(), self.aOutMatrices)
        for i in range(finalCount):
            elemPlg = arrayPlug.elementByLogicalIndex(i)
            if not elemPlg.isNull:
                dataBlock.setClean(elemPlg)
        dataBlock.setClean(arrayPlug)

    # ==================================================================
    def _computeUniform(self, plug, curveFn, curveWorldMat, upVec,
                        jointCount, startParam, uMax, dataBlock):
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
                             startU, endU, center, radius,
                             totalLength, sampleDensity):
        numSamples = max(int(totalLength * sampleDensity), 120)
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
