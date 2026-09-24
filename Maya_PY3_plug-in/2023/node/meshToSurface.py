# coding=gbk
"""meshToSurface - 将多边形模型转换为NURBS曲面面片
每个面生成一张曲面数据，输出到数组供下游使用。
"""
import maya.api.OpenMaya as om
import sys


def maya_useNewAPI():
    pass


class MeshToSurfaceNode(om.MPxNode):
    kNodeId = om.MTypeId(0x00141480 + 21)
    kNodeName = "meshToSurface"

    aInMesh = om.MObject()
    aInMeshMatrix = om.MObject()
    aDegree = om.MObject()
    aOutSurface = om.MObject()

    def __init__(self):
        super(MeshToSurfaceNode, self).__init__()
        self._cache = None

    @staticmethod
    def creator():
        return MeshToSurfaceNode()

    @staticmethod
    def initialize():
        tAttr = om.MFnTypedAttribute()
        MeshToSurfaceNode.aInMesh = tAttr.create("inMesh", "im", om.MFnData.kMesh)
        tAttr.storable = True
        MeshToSurfaceNode.addAttribute(MeshToSurfaceNode.aInMesh)

        mAttr = om.MFnMatrixAttribute()
        MeshToSurfaceNode.aInMeshMatrix = mAttr.create("inMeshMatrix", "imm")
        mAttr.storable = True
        MeshToSurfaceNode.addAttribute(MeshToSurfaceNode.aInMeshMatrix)

        nAttr = om.MFnNumericAttribute()
        MeshToSurfaceNode.aDegree = nAttr.create(
            "degree", "deg", om.MFnNumericData.kInt, 3)
        nAttr.setMin(1)
        nAttr.setMax(7)
        nAttr.storable = True
        nAttr.keyable = True
        MeshToSurfaceNode.addAttribute(MeshToSurfaceNode.aDegree)

        tAttr2 = om.MFnTypedAttribute()
        MeshToSurfaceNode.aOutSurface = tAttr2.create(
            "outSurface", "os", om.MFnData.kNurbsSurface)
        tAttr2.array = True
        tAttr2.writable = False
        tAttr2.storable = False
        MeshToSurfaceNode.addAttribute(MeshToSurfaceNode.aOutSurface)

        MeshToSurfaceNode.attributeAffects(
            MeshToSurfaceNode.aInMesh, MeshToSurfaceNode.aOutSurface)
        MeshToSurfaceNode.attributeAffects(
            MeshToSurfaceNode.aInMeshMatrix, MeshToSurfaceNode.aOutSurface)
        MeshToSurfaceNode.attributeAffects(
            MeshToSurfaceNode.aDegree, MeshToSurfaceNode.aOutSurface)

    # ==================================================================
    def compute(self, plug, dataBlock):
        plugAttr = plug.attribute()
        if plugAttr != self.aOutSurface and plugAttr != om.MObject.kNullObj:
            try:
                if plug.parent().attribute() != self.aOutSurface:
                    return om.kUnknownParameter
            except:
                return om.kUnknownParameter

        # ----- 获取输入网格 -----
        meshHandle = dataBlock.inputValue(self.aInMesh)
        meshData = meshHandle.asMesh()
        if meshData.isNull():
            dataBlock.setClean(plug)
            return

        meshFn = om.MFnMesh(meshData)
        meshMatrix = dataBlock.inputValue(self.aInMeshMatrix).asMatrix()
        degree = dataBlock.inputValue(self.aDegree).asInt()

        # ----- 读取顶点 -----
        meshPoints = meshFn.getPoints()
        numFaces = meshFn.numPolygons

        # ----- 缓存判断 -----
        newSig = (numFaces, len(meshPoints), degree)
        if newSig == self._cache:
            dataBlock.setClean(plug)
            return
        self._cache = newSig

        # ----- 限制度数 -----
        if degree > 3:
            degree = 3
        if degree < 1:
            degree = 1

        numCVs = degree + 1  # 每条边 4 个 CV (degree=3 时)
        knots = self._makeKnots(numCVs, degree)

        # ----- 逐个面生成曲面数据 -----
        patches = []
        for faceId in range(numFaces):
            vtxIds = meshFn.getPolygonVertices(faceId)
            nv = len(vtxIds)

            if nv == 4:
                corners = self._quadCorners(vtxIds, meshPoints, meshMatrix)
            elif nv == 3:
                corners = self._triCorners(vtxIds, meshPoints, meshMatrix)
            else:
                patches.append(None)
                continue

            cvGrid = self._buildCVGrid(corners, numCVs)
            patch = self._createPatch(cvGrid, knots, degree)
            patches.append(patch)

        # ----- 输出到数组 -----
        outHandle = dataBlock.outputArrayValue(self.aOutSurface)
        for i in range(numFaces):
            p = patches[i]
            if p is not None:
                outHandle.jumpToLogicalElement(i)
                outHandle.outputValue().setMObject(p)
        outHandle.setAllClean()
        dataBlock.setClean(plug)

    # ==================================================================
    @staticmethod
    def _quadCorners(vtxIds, meshPoints, meshMatrix):
        pts = [meshPoints[vtxIds[i]] * meshMatrix for i in range(4)]
        return pts[0], pts[1], pts[2], pts[3]

    @staticmethod
    def _triCorners(vtxIds, meshPoints, meshMatrix):
        pts = [meshPoints[vtxIds[i]] * meshMatrix for i in range(3)]
        return pts[0], pts[1], pts[2], pts[2]

    # ==================================================================
    @staticmethod
    def _buildCVGrid(corners, n):
        """双线性插值: 4个角 -> n*n CV网格"""
        v0 = om.MVector(corners[0])
        v1 = om.MVector(corners[1])
        v2 = om.MVector(corners[2])
        v3 = om.MVector(corners[3])
        cvs = om.MPointArray()
        for j in range(n):
            tV = j / float(n - 1)
            left = v0 + (v3 - v0) * tV
            right = v1 + (v2 - v1) * tV
            for i in range(n):
                tU = i / float(n - 1)
                cvs.append(om.MPoint(left + (right - left) * tU))
        return cvs

    # ==================================================================
    @staticmethod
    def _makeKnots(numCVs, degree):
        """构建 clamped 节点向量
        Maya官方文档: numKnots = numCVs + degree - 1
        degree=3, numCVs=4 -> [0,0,0, 1,1,1] (6个节点，首尾各degree个重复)
        """
        nk = numCVs + degree - 1
        ks = om.MDoubleArray()
        for i in range(nk):
            if i < degree:
                ks.append(0.0)
            elif i >= nk - degree:
                ks.append(1.0)
            else:
                ks.append(float(i - degree + 1) / float(numCVs - degree + 1))
        return ks

    # ==================================================================
    @staticmethod
    def _createPatch(cvGrid, knots, degree):
        """创建NURBS曲面数据对象(纯DG数据，不创建场景节点)
        MFnNurbsSurfaceData.create() 先创建空数据容器，
        MFnNurbsSurface.create() 传入dataObj作为parent，将几何写入数据对象。
        """
        dataFn = om.MFnNurbsSurfaceData()
        dataObj = dataFn.create()
        surfFn = om.MFnNurbsSurface()
        surfFn.create(
            cvGrid, knots, knots,
            degree, degree,
            om.MFnNurbsSurface.kOpen,
            om.MFnNurbsSurface.kOpen,
            False,
            dataObj  # 作为parent传入，几何数据写入此数据对象
        )
        return dataObj


# ======================================================================
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin, "KangmingZhan", "1.0", "Any")
    try:
        pluginFn.registerNode(
            MeshToSurfaceNode.kNodeName,
            MeshToSurfaceNode.kNodeId,
            MeshToSurfaceNode.creator,
            MeshToSurfaceNode.initialize)
        sys.stderr.write("meshToSurface registered OK\n")
    except Exception as e:
        sys.stderr.write("meshToSurface registration FAILED: " + str(e) + "\n")
        raise


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(MeshToSurfaceNode.kNodeId)
        sys.stderr.write("meshToSurface deregistered OK\n")
    except Exception as e:
        sys.stderr.write("meshToSurface deregister FAILED: " + str(e) + "\n")
        raise
