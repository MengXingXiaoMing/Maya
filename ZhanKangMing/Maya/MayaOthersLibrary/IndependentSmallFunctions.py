# coding=gbk
import pymel.core as pm
# 加载文本
class ZKM_IndependentSmallfunctions:
    # 显隐轴向
    def ShowAxial(self):
        Sel = pm.ls(sl=1)
        for i in range(0, len(Sel)):
            Ture = int(pm.getAttr(Sel[i] + ".displayLocalAxis"))
            if Ture < 1:
                pm.setAttr((Sel[i] + ".displayLocalAxis"), 1)
            else:
                pm.setAttr((Sel[i] + ".displayLocalAxis"), 0)

    # 生成骨骼链
    def GenerateBoneChain(self,ShuLiang):
        Nurbs = pm.ls(sl=1)
        pm.spaceLocator(p=(0, 0, 0), n="LocatorSC")
        pm.select("LocatorSC", r=1)
        pm.select(Nurbs, tgl=1)
        pm.pathAnimation(upAxis='x', fractionMode=True, endTimeU=pm.playbackOptions(query=1, maxTime=1),
                         startTimeU=pm.playbackOptions(minTime=1, query=1), worldUpType="vector", inverseUp=False,
                         inverseFront=False, follow=True, bank=False, followAxis='y', worldUpVector=(0, 1, 0))
        LuJingJieDian = pm.listConnections("LocatorSC.rx", s=1, d=0)
        pm.disconnectAttr((LuJingJieDian[0] + "_uValue.output"), (LuJingJieDian[0] + ".uValue"))
        pm.select(cl=1)
        for i in range(0, ShuLiang + 1):
            number = 1.0 / ShuLiang * i
            pm.setAttr((LuJingJieDian[0] + ".uValue"), number)
            pm.joint(p=(0, 0, 0), n=("Joint" + str(i)))
            pm.delete(pm.pointConstraint("LocatorSC", ("Joint" + str(i))))
        pm.delete("LocatorSC")

    # 镜像骨骼
    def MirrorJoint(self,ChaoXiangh):
        Sel = pm.ls(sl=1)
        pm.select(cl=1)
        pm.joint(p=(0, 0, 0), n="Mirror_joint")
        for i in range(0, len(Sel)):
            pm.delete(pm.pointConstraint(Sel[i], "Mirror_joint", weight=1))
            if ChaoXiangh == "X":
                Num = float(pm.getAttr("Mirror_joint.translateX"))
                pm.setAttr("Mirror_joint.translateX", (Num * (-1)))
                pm.select(Sel[i], r=1)
                pm.mirrorJoint(mirrorBehavior=1, mirrorYZ=1)
            if ChaoXiangh == "Y":
                Num = float(pm.getAttr("Mirror_joint.translateY") * (-1))
                pm.setAttr("Mirror_joint.translateY", Num)
                pm.select(Sel[i], r=1)
                pm.mirrorJoint(mirrorBehavior=1, mirrorXZ=1)
            if ChaoXiangh == "Z":
                Num = float(pm.getAttr("Mirror_joint.translateZ") * (-1))
                pm.setAttr("Mirror_joint.translateZ", Num)
                pm.select(Sel[i], r=1)
                pm.mirrorJoint(mirrorXY=1, mirrorBehavior=1)
            sel = pm.ls(sl=1)
            pm.delete(pm.pointConstraint("Mirror_joint", sel[0], weight=1))
        pm.delete("Mirror_joint")

    # 把所选线单独转化为样条
    def ChangeLineToSpline(self):
        Lint = pm.ls(fl=1, sl=1)
        ModelName = []
        numTokens = ModelName = Lint[0].split(".")
        for i in range(0, len(Lint)):
            pm.select(Lint[i])
            pm.polyToCurve(conformToSmoothMeshPreview=0, degree=1, form=2)
            pm.mel.rename("LingShiLint" + str(i))
            if i > 0:
                pm.parent(("LingShiLintShape" + str(i)),
                          "LingShiLint0", s=1, add=1)
                pm.delete("LingShiLint" + str(i))
        pm.select('LingShiLint0', r=1)
        pm.mel.CenterPivot()
        pm.mel.rename(ModelName[0] + "Cur")

    # 在所选线中心创建骨骼
    def CentreJoint(self):
        sel = pm.ls(sl=1,fl=1)
        CurveName = []
        for s in sel:
            pm.select(s)
            pm.polyToCurve(conformToSmoothMeshPreview=0, degree=1, form=2)
            CurveName.append(pm.ls(sl=1))
        pm.select(CurveName[1:])
        pm.pickWalk(d='down')
        pm.select(CurveName[0],add=1)
        pm.parent(s=1, add=1)
        pm.select(CurveName[0])
        pm.mel.CenterPivot()
        pm.select(cl=1)
        pm.joint(p=(0, 0, 0), n="LingShiJoint")
        pm.delete(pm.pointConstraint(CurveName[0], 'LingShiJoint', weight=1, offset=(0, 0, 0)))
        pm.parent('LingShiJoint', w=1)
        pm.select('LingShiJoint', r=1)
        pm.rename('LingShiJoint',CurveName[0][0] + 'Joint')
        pm.delete(CurveName)

    # 在中心建立骨骼链
    def CreateCentreJoint(self):
        pm.mel.SelectEdgeRingSp()
        ele = pm.ls(fl=1, sl=1)
        skip = []
        OldJoint = ""
        NewJoint = ""
        for i in range(0, len(ele)):
            if ele[i] in skip:
                continue
            pm.select(ele[i], r=1)
            pm.mel.performSelContiguousEdges(0)
            newEle = pm.ls(fl=1, sl=1)
            skip = skip + newEle
            pm.polyToCurve(conformToSmoothMeshPreview=1, degree=1, form=2)
            Curve = pm.ls(sl=1)
            pm.mel.CenterPivot()
            pm.select(cl=1)
            joint = str(pm.joint(p=(0, 0, 0)))
            OldJoint = NewJoint
            NewJoint = joint
            pm.pointConstraint(Curve[0], joint, weight=1, offset=(0, 0, 0))
            pm.delete(Curve)
            if len(OldJoint) != 0:
                pm.parent(NewJoint, OldJoint)

    # 反转层次
    def ReversalArrangement(self):
        pm.mel.SelectHierarchy()
        Select = pm.ls(sl=1)
        for i in range(1, len(Select)):
            pm.parent(Select[i], w=1)
        for i in range(0, (len(Select) - 1)):
            pm.parent(Select[i], Select[i + 1])

    # 骨骼转样条
    def JointTransformationCurve(self):
        pm.mel.SelectHierarchy()
        Select = pm.ls(sl=1)
        CurveP = ""
        for i in range(0, len(Select)):
            pm.spaceLocator(p=(0, 0, 0), n="LS_Loc")
            pm.pointConstraint(Select[i], "LS_Loc", weight=1)
            TX = str(pm.getAttr("LS_Loc.translateX"))
            TY = str(pm.getAttr("LS_Loc.translateY"))
            TZ = str(pm.getAttr("LS_Loc.translateZ"))
            CP = (" -p " + TX + " " + " " + TY + " " + TZ)
            CurveP = CurveP + CP
            pm.delete("LS_Loc")
        pm.mel.eval("curve -d 3" + CurveP)

    # 插入骨骼
    def InsertJoint(self):
        # pm.undoInfo(st=1,ock=1,infinity=1)
        Sel = pm.ls(sl=1)
        # 查询创建骨骼数量
        JointNum = pm.intSliderGrp('WindowControllerProcessingInsertBone', q=1, v=1) - 1
        pm.curve(p=[(0, 0, 0), (0, 0, 1)], d=1)
        Curve = pm.ls(sl=1)
        pm.select((Curve[0] + ".cv[0]"), r=1)
        pm.mel.newCluster(" -envelope 1")
        Cluster1 = pm.ls(sl=1)
        pm.select((Curve[0] + ".cv[1]"), r=1)
        pm.mel.newCluster(" -envelope 1")
        Cluster2 = pm.ls(sl=1)
        pm.delete(pm.pointConstraint(Sel[0], Cluster1[0], weight=1, offset=(0, 0, 0)))
        pm.delete(pm.pointConstraint(Sel[1], Cluster2[0], weight=1, offset=(0, 0, 0)))
        pm.select(cl=1)
        pm.spaceLocator(p=(0, 0, 0), n=("LS_Loc"))
        pm.select(Curve[0], tgl=1)
        pm.pathAnimation(upAxis='x', fractionMode=True, endTimeU=pm.playbackOptions(query=1, maxTime=1),
                         startTimeU=pm.playbackOptions(minTime=1, query=1), worldUpType="vector", inverseUp=False,
                         inverseFront=False, follow=True, bank=False, followAxis='y', worldUpVector=(0, 1, 0))
        LuJingJieDian = pm.listConnections(("LS_Loc.rx"), s=1, d=0)
        pm.disconnectAttr((LuJingJieDian[0] + "_uValue.output"), (LuJingJieDian[0] + ".uValue"))
        pm.select(cl=1)
        for i in range(1, JointNum):
            number = 1.0 / JointNum * i
            pm.setAttr((LuJingJieDian[0] + ".uValue"), number)
            pm.joint(p=(0, 0, 0), n=(str(Sel[0]) + str(Sel[1]) + "_Joint" + str(i)))
            pm.delete(pm.pointConstraint("LS_Loc", (str(Sel[0]) + str(Sel[1]) + "_Joint" + str(i)), weight=1))
        pm.delete("LS_Loc")
        pm.parent((str(Sel[0]) + str(Sel[1]) + "_Joint1"), Sel[0])
        pm.parent(Sel[1], (str(Sel[0]) + str(Sel[1]) + "_Joint" + str((JointNum - 1))))
        pm.delete(Curve, Cluster1, Cluster2)
        # pm.undoInfo(cck=1)

    # 偏移属性
    def gtMoveUpDnAttrsProc(self,updn):
        objs = pm.ls(sl=1)
        attrs = pm.channelBox('mainChannelBox', q=1, sma=1)
        ex = 0
        for j in range(0, len(objs)):
            obj = objs[j]
            for i in range(0, len(attrs)):
                attr = attrs[i]
                ex = int(pm.objExists(obj + "." + attr))
                if ex == 0:
                    continue

                udAttrs = pm.listAttr(obj, ud=1, u=1)
                index = -1
                for a in range(0, len(udAttrs)):
                    if attr == udAttrs[a]:
                        index = int(a)

                if index == -1:
                    continue

                indexUp = index - 1
                if indexUp < 0:
                    indexUp = index

                upAttr = udAttrs[indexUp]
                if updn == 1:
                    if index == 0:
                        continue

                    pm.deleteAttr(obj + "." + upAttr)
                    pm.undo()
                    for aa in range((index + 1), len(udAttrs)):
                        pm.deleteAttr(obj + "." + udAttrs[aa])
                        pm.undo()

                if updn == 0:
                    pm.deleteAttr(obj + "." + attr)
                    pm.undo()
                    dnSize = len(attrs)
                    for aa in range((index + dnSize + 1), len(udAttrs)):
                        pm.deleteAttr(obj + "." + udAttrs[aa])
                        pm.undo()

    # 隐藏选择属性
    def HideSelectionProperties(self):
        QvDongYvan = pm.ls(sl=1)
        LianJieYvan = pm.channelBox('mainChannelBox', q=1, sma=1)
        for i in range(0, len(LianJieYvan)):
            pm.setAttr((QvDongYvan[0] + "." + LianJieYvan[i]),
                       channelBox=False, keyable=False)

    # 显示默认属性
    def ShowDefaultProperties(self):
        QvDongYvan = pm.ls(sl=1)
        LianJieYvan = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        for j in range(0, len(QvDongYvan)):
            for i in range(0, len(LianJieYvan)):
                pm.setAttr((QvDongYvan[j] + "." + LianJieYvan[i]), k=True)

    # 隔行选线
    # edgeRing  # edgeLoop
    def InterlacedLineSelection(self,MS,int):
        pm.mel.polySelectEdgesEveryN(MS,int)

    # 统一循环边骨骼权重
    def UniformEdgeLoopWeights(self):
        sel = pm.ls(sl=1, fl=1)
        pm.mel.ConvertSelectionToVertices()
        point = pm.ls(sl=1, fl=1)
        pm.select(point[0])
        for i in range(0, len(point)):
            pm.select(point[i])
            pm.mel.CopyVertexWeights()
            pm.mel.polySelectEdgesEveryN("edgeLoop", 1)
            SelA = pm.ls(sl=1, fl=1)
            pm.select(list(set(SelA).difference(set(sel))))
            pm.mel.SelectEdgeLoopSp()
            pm.mel.ConvertSelectionToVertices()
            LoopPoint = pm.ls(sl=1, fl=1)
            pm.select(LoopPoint)
            pm.mel.PasteVertexWeights()

    # 显影骨骼
    def SetBoneDisplay(self,num):
        Joint = pm.ls(typ="joint")
        for i in range(0, len(Joint)):
            pm.setAttr((Joint[i] + ".drawStyle"),num)

    # 按循环边中心创建骨骼
    def CreateJointByEdgeLoop(self):
        sel = pm.ls(sl=1, fl=1)
        pm.mel.ConvertSelectionToVertices()
        point = pm.ls(sl=1, fl=1)
        pm.select(point[0])
        J = []
        for i in range(0, len(point)):
            pm.select(point[i])
            pm.mel.polySelectEdgesEveryN("edgeLoop", 1)
            SelA = pm.ls(sl=1, fl=1)
            pm.select(list(set(SelA).difference(set(sel))))
            pm.mel.SelectEdgeLoopSp()
            pm.mel.ConvertSelectionToVertices()
            LoopPoint = pm.ls(sl=1, fl=1)
            pm.select(LoopPoint)
            cluster = pm.cluster()
            pm.select(cl=1)
            joint = pm.joint(p=(0, 0, 0))
            pm.delete(pm.pointConstraint(cluster, joint, w=1))
            pm.delete(cluster)
            if i > 0:
                pm.parent(joint, J)
            J = joint










