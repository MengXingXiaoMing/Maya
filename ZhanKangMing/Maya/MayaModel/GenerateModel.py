#coding=gbk
import maya.cmds as cmds
import pymel.core as pm
import sys
sys.dont_write_bytecode = True
#加载文本
class ZKM_RegenerateExistingModelClass:
    def GeneratingSimpleModule(self, sel, FaceNum, ModelMirror, ReduceDetail, Smoothness):
        pm.select(sel)
        pm.duplicate(rr=1)
        sel = pm.ls(sl=1)
        if not ModelMirror == "None":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=0, cutMesh=1, axis=0, smoothingAngle=30,
                              mergeThresholdType=0, mergeThreshold=0.001, mergeMode=3, mirrorPosition=0,
                              axisDirection=0)
            pm.polySeparate(ch=0)
            pm.mel.DeleteHistory()
            pm.mel.CenterPivot()
            MorrySel = pm.ls(sl=1)
            Loc = pm.spaceLocator(p=(0, 0, 0))
            pm.pointConstraint(MorrySel[0], Loc, weight=1, offset=(0, 0, 0))
            num = pm.xform(Loc, q=1, ws=1, t=1)
            pm.select(MorrySel)
            if ModelMirror == "X":
                if num[0] < 0:
                    pm.delete(MorrySel[1])
                else:
                    pm.delete(MorrySel[0])
            if ModelMirror == "FX":
                if num[0] > 0:
                    pm.delete(MorrySel[1])
                else:
                    pm.delete(MorrySel[0])
            if ModelMirror == "Y":
                if num[1] < 0:
                    pm.delete(MorrySel[1])
                else:
                    pm.delete(MorrySel[0])
            if ModelMirror == "FY":
                if num[1] > 0:
                    pm.delete(MorrySel[1])
                else:
                    pm.delete(MorrySel[0])
            if ModelMirror == "Z":
                if num[2] < 0:
                    pm.delete(MorrySel[1])
                else:
                    pm.delete(MorrySel[0])
            if ModelMirror == "FZ":
                if num[2] > 0:
                    pm.delete(MorrySel[1])
                else:
                    pm.delete(MorrySel[0])
            pm.mel.DeleteHistory()
            pm.delete(Loc)
        sel = pm.ls(sl=1)
        pm.mel.polyCleanupArgList(4, ["0", "1", "1", "1", "1", "1", "1", "1", "0", "1e-05", "0", "1e-05", "0", "1e-05",
                                      "0", "2", "0", "0"])
        pm.mel.DeleteHistory()
        pm.polyRemesh(smoothStrength=Smoothness, refineThreshold=0.1, reduceThreshold=ReduceDetail, ch=0)
        pm.select(sel)
        pm.mel.DeleteHistory()
        if not ModelMirror == "None":
            FaceNum = (FaceNum / 2)
        pm.mel.polyRetopo('-targetFaceCount', FaceNum, '-targetEdgeLengthMax', 1)
        pm.mel.DeleteHistory()
        if ModelMirror == "X":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=1, cutMesh=1, axis=0, smoothingAngle=30,
                              mergeThresholdType=1, mergeThreshold=0.001, mergeMode=1, mirrorPosition=0,
                              axisDirection=0)

        if ModelMirror == "FX":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=1, cutMesh=1, axis=0, smoothingAngle=30,
                              mergeThresholdType=1, mergeThreshold=0.001, mergeMode=1, mirrorPosition=0,
                              axisDirection=1)

        if ModelMirror == "Y":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=1, cutMesh=1, axis=1, smoothingAngle=30,
                              mergeThresholdType=1, mergeThreshold=0.001, mergeMode=1, mirrorPosition=0,
                              axisDirection=0)

        if ModelMirror == "FY":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=1, cutMesh=1, axis=1, smoothingAngle=30,
                              mergeThresholdType=1, mergeThreshold=0.001, mergeMode=1, mirrorPosition=0,
                              axisDirection=1)

        if ModelMirror == "Z":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=1, cutMesh=1, axis=2, smoothingAngle=30,
                              mergeThresholdType=1, mergeThreshold=0.001, mergeMode=1, mirrorPosition=0,
                              axisDirection=0)

        if ModelMirror == "FZ":
            pm.polyMirrorFace(sel[0], flipUVs=0, mirrorAxis=2, ch=1, cutMesh=1, axis=2, smoothingAngle=30,
                              mergeThresholdType=1, mergeThreshold=0.001, mergeMode=1, mirrorPosition=0,
                              axisDirection=1)
        pm.mel.DeleteHistory()
        print ('生成完成！')
