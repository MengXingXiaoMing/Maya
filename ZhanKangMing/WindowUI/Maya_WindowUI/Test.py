#coding=gbk
import pymel.core as pm
#拷贝权重(Normal)
def ZKM_CopyWeight(CopyWay, Soure, Target, SoureUVset, TargetUVset):
    if CopyWay and Soure and Target :
        HaveWeightSoure = []
        Joint = []
        try:
            HaveWeightSoure = pm.mel.findRelatedSkinCluster(Soure)
            Joint = pm.skinCluster(Soure, q=1, inf=1)
        except:
            pass
        if len(Target[0].split('.')) == 1:
            TargetType = 'Model'
        else:
            TargetType = 'Point'
        if HaveWeightSoure:
            Removejoint = []
            #先进行添加影响和蒙皮
            if TargetType == 'Model':
                for T in Target:
                    try:
                        HaveWeight = pm.mel.findRelatedSkinCluster(T)
                    except:
                        HaveWeight = []
                    if HaveWeight:
                        pm.select(T)
                        pm.mel.DetachSkin()
                    pm.select(Joint, T)
                    pm.mel.SmoothBindSkin()
            if TargetType == 'Point':
                TargetModel = Target[0].split('.')[0]
                try:
                    HaveWeight = pm.mel.findRelatedSkinCluster(TargetModel)
                except:
                    HaveWeight = []
                if HaveWeight:
                    TargetJoint = pm.skinCluster(TargetModel, q=1, inf=1)
                    joint = [i for i in Joint if i not in TargetJoint]
                    if joint:
                        for j in joint:
                            pm.skinCluster(HaveWeight, e=1, ai=j, wt=0)
                    Removejoint = [i for i in TargetJoint if i not in Joint]
                    if Removejoint:
                        for j in Removejoint:
                            pm.select(Soure,j)
                            pm.skinCluster(HaveWeightSoure, e=1, ai=j, wt=0)
                else:
                    pm.select(Joint, TargetModel)
                    pm.mel.SmoothBindSkin()
            #进行拷贝权重
            if CopyWay == 'Normal':
                if TargetType == 'Model':
                    for T in Target:
                        pm.select(Soure, T)
                        pm.copySkinWeights(surfaceAssociation='closestPoint', influenceAssociation=['closestJoint', 'oneToOne'], noMirror=1)
                if TargetType == 'Point':
                    pm.select(Soure,Target)
                    pm.copySkinWeights(surfaceAssociation='closestPoint', influenceAssociation=['closestJoint', 'oneToOne'], noMirror=1)
                    if Removejoint:
                        for j in Removejoint:
                            pm.skinCluster(HaveWeightSoure, e=1, ri=j)
            if CopyWay == 'UV':
                if SoureUVset and TargetUVset:
                    if TargetType == 'Model':
                        for T in Target:
                            pm.select(Soure, T)
                            pm.copySkinWeights(surfaceAssociation='closestPoint', uvSpace=(SoureUVset, TargetUVset), noMirror=1, influenceAssociation=['closestJoint', 'oneToOne'])
                    if TargetType == 'Point':
                        pm.select(Soure,Target)
                        pm.copySkinWeights(surfaceAssociation='closestPoint', uvSpace=(SoureUVset, TargetUVset), noMirror=1, influenceAssociation=['closestJoint', 'oneToOne'])
                        if Removejoint:
                            for j in Removejoint:
                                pm.skinCluster(HaveWeightSoure, e=1, ri=j)
                else:
                    pm.error('请加载uv选集')
        else:
            pm.error('源没有骨骼蒙皮')
ZKM_CopyWeight('UV', 'pCube1', ['pCube2'], 'map1', 'map1')








































# 清理Bs中间帧
#ZKM_ClearBsIntermediateFrame('blendShape1')
def ZKM_ClearBsIntermediateFrame(BsName):
    AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
    #获取所有主要bs的对应数字
    AllNum = pm.listAttr(BsName+'.inputTarget[0].inputTargetGroup[*]', c=1)
    i = 0
    AllBsNum = []
    while i < len(AllNum):
        AllBsNum.append(int(AllNum[i][-2:-1]))
        i = i + 12
    print (AllBsNum)
    for i in range(1, len(AllBsNum)):
        # 获取中间帧
        if pm.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
            IntermediateFrameName = pm.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
            print (i)
            print (AllBsNum[i])
            print (IntermediateFrameName)
            print (type(IntermediateFrameName))
            if type(IntermediateFrameName) == list:
                for name in IntermediateFrameName:
                    num = name[-3:]
                    num = float(num) * 1000
                    pm.mel.blendShapeDeleteInBetweenTarget(BsName, int(AllBsNum[i]), int(5000 + num))
            else:
                num = IntermediateFrameName[-3:]
                num = float(num) * 1000
                pm.mel.blendShapeDeleteInBetweenTarget(BsName, int(AllBsNum[i]), int(5000 + num))









