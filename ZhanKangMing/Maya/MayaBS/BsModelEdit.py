#coding=gbk
import os
from os import listdir
import maya.cmds as cmds
import pymel.core as pm
#不同拓补BS处理类
class ZKM_DifferentTopologiesBSClass:
    # 不同拓补传递BS
    def ZKM_TransferDifferentTopologies_BS(self, TransmitSource, TransmitTarget, IntermediateState):
        pm.select(TransmitSource, r=1)
        pm.duplicate(rr=1)
        pm.mel.rename(TransmitSource + '_Copy')
        pm.blendShape((TransmitSource + "_Copy"), TransmitSource, IntermediateState, n="FirstPass_BS")
        pm.setAttr(("FirstPass_BS." + TransmitSource + "_Copy"), -1)
        pm.setAttr(("FirstPass_BS." + TransmitSource), 1)
        pm.delete(TransmitSource + "_Copy")
        pm.select(TransmitTarget, r=1)
        pm.duplicate(rr=1)
        pm.mel.rename(TransmitTarget + "_Copy")
        pm.select(IntermediateState, r=1)
        pm.select((TransmitTarget + "_Copy"), add=1)
        pm.transferAttributes(flipUVs=0, transferPositions=1, transferUVs=0, sourceUvSpace="map1", searchMethod=3,
                              transferNormals=1, transferColors=0, targetUvSpace="map1", colorBorders=1, sampleSpace=3)
        pm.select((TransmitTarget + "_Copy"), r=1)
        pm.duplicate(rr=1)
        pm.mel.rename(TransmitTarget + "_CopySecond")
        pm.blendShape((TransmitTarget + "_Copy"), (TransmitTarget + "_CopySecond"), TransmitTarget, n="SecondPass_BS")
        pm.setAttr(("SecondPass_BS." + TransmitTarget + "_Copy"), 1)
        pm.setAttr(("SecondPass_BS." + TransmitTarget + "_CopySecond"), -1)
        pm.delete(TransmitTarget + "_CopySecond")
        pm.setAttr((TransmitSource + ".visibility"), 0)
        pm.setAttr((IntermediateState + ".visibility"), 0)
        pm.setAttr((TransmitTarget + "_Copy.visibility"), 0)
    # 烘焙BS
    def ZKM_BakingBS(self,BakingModel, BakingModel_BS,BakingBsAttributeAll):
        # 清理BS属性
        pm.setAttr((BakingModel_BS + ".envelope"), 1)
        for i in range(0, len(BakingBsAttributeAll)):
            pm.setAttr(BakingBsAttributeAll[i], 0)
        # 开始生成
        for i in range(0, len(BakingBsAttributeAll)):
            Reame = BakingBsAttributeAll[i].split(".")
            pm.select(BakingModel, r=1)
            pm.setAttr(BakingBsAttributeAll[i], 1)
            pm.duplicate(rr=1)
            pm.mel.rename(Reame[1])
            pm.setAttr(BakingBsAttributeAll[i], 0)
    # 分解BS
    def ZKM_DecomposeBS(self,DecomposeSource,DecomposeSourceAll,DecomposereFerence):
        DecomposereFerenceShapes = pm.listRelatives(DecomposereFerence, shapes=1)
        pm.select((DecomposereFerenceShapes[0] + ".vtx[*]"), r=1)
        DecomposereFerenceVtx = pm.ls(fl=1, sl=1)
        DecomposeBS = DecomposeSourceAll[0].split(".")
        # 清理BS属性
        pm.setAttr((DecomposeBS[0] + ".envelope"), 1)
        DecomposeBS_Welght = pm.listAttr((DecomposeBS[0] + ".weight"), k=1, m=1)
        for i in range(0, len(DecomposeBS_Welght)):
            pm.setAttr((DecomposeBS[0] + "." + DecomposeBS_Welght[i]), 0)
        # 开始轮流bs分解
        for i in range(0, len(DecomposeSourceAll)):
            pm.select(DecomposereFerence)
            pm.duplicate(rr=1)
            pm.mel.rename(DecomposereFerence + '_' + DecomposeSourceAll[i].split(".")[1] + "_X")
            pm.duplicate(rr=1)
            pm.mel.rename(DecomposereFerence + '_' + DecomposeSourceAll[i].split(".")[1] + "_Y")
            pm.duplicate(rr=1)
            pm.mel.rename(DecomposereFerence + '_' + DecomposeSourceAll[i].split(".")[1] + "_Z")
            pm.setAttr(DecomposeSourceAll[i], 1)
            pm.select(DecomposeSource, r=1)
            pm.duplicate(rr=1)
            Copy = pm.ls(sl=1)
            pm.select((Copy[0] + ".vtx[*]"), r=1)
            DecomposeSourceVtx = pm.ls(fl=1, sl=1)
            pm.setAttr(DecomposeSourceAll[i], 0)
            for j in range(0, len(DecomposeSourceVtx)):
                DecomposeSourceNum = pm.xform(DecomposeSourceVtx[j], q=1, ws=1, t=1)
                DecomposereFerenceNum = pm.xform(DecomposereFerenceVtx[j], q=1, ws=1, t=1)
                pm.setAttr((DecomposereFerence + '_' + DecomposeSourceAll[i].split(".")[1] + "_XShape" + ".pnts[" + str(j) + "].pntx"),
                           (DecomposeSourceNum[0] - DecomposereFerenceNum[0]))
                pm.setAttr((DecomposereFerence + '_' + DecomposeSourceAll[i].split(".")[1] + "_YShape" + ".pnts[" + str(j) + "].pnty"),
                           (DecomposeSourceNum[1] - DecomposereFerenceNum[1]))
                pm.setAttr((DecomposereFerence + '_' + DecomposeSourceAll[i].split(".")[1] + "_ZShape" + ".pnts[" + str(j) + "].pntz"),
                           (DecomposeSourceNum[2] - DecomposereFerenceNum[2]))
            pm.delete(Copy)
        cmds.refresh()

