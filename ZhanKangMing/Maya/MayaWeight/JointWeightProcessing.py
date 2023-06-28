#coding=gbk
import os
from os import listdir
import maya.cmds as cmds
import pymel.core as pm
#����Ȩ�ش���
class ZKM_JointWeightProcessingClass:
    # ����ģ��Ȩ��
    # ZKM_JointWeightProcessingClass().ZKM_CopyModelWeightApply()
    def ZKM_CopyModelWeightApply(self):
        AllSel = pm.ls(sl=1)
        self.ZKM_CopyWeight('Normal', AllSel[0], AllSel[1:], '', '')

    # �԰뿽��ģ��Ȩ��
    # ZKM_JointWeightProcessingClass().ZKM_HalfCopyModelWeightApply()
    def ZKM_HalfCopyModelWeightApply(self):
        AllSel = pm.ls(sl=1)
        FirstHalf = AllSel[:len(AllSel) / 2]
        LatterHalf = AllSel[len(AllSel) / 2:]
        pm.select(FirstHalf)
        pm.mel.SelectHierarchy()
        FirstHalfMesh = pm.ls(type="mesh", sl=1)
        pm.select(LatterHalf)
        pm.mel.SelectHierarchy()
        LatterHalfMesh = pm.ls(type="mesh", sl=1)
        if len(FirstHalfMesh) == len(LatterHalfMesh):
            for i in range(0, len(FirstHalfMesh)):
                pm.select(FirstHalfMesh[i], r=1)
                pm.pickWalk(d='up')
                S = pm.ls(sl=1)
                pm.select(LatterHalfMesh[i], r=1)
                pm.pickWalk(d='up')
                T = pm.ls(sl=1)
                pm.select(S,T)
                self.ZKM_CopyModelWeightApply()
        else:
            pm.pm.mel.error("�����ż����ѡ��")

    # �ײ㿽��Ȩ��
    # ��ʾ��TargetӦΪ�б�
    # ZKM_JointWeightProcessingClass().ZKM_CopyWeight('Normal', 'pSphere1', ['pSphere3'], '', '')
    def ZKM_CopyWeight(self, CopyWay, Soure, Target, SoureUVset, TargetUVset):
        if CopyWay and Soure and Target:
            try:
                HaveWeightSoure = pm.mel.findRelatedSkinCluster(Soure)
                Joint = pm.skinCluster(Soure, q=1, inf=1)
            except:
                HaveWeightSoure = []
                Joint = []
            if len(Target[0].split('.')) == 1:
                TargetType = 'Model'
            else:
                TargetType = 'Point'
            if HaveWeightSoure:
                Removejoint = []
                # �Ƚ������Ӱ�����Ƥ
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
                                pm.select(Soure, j)
                                pm.skinCluster(HaveWeightSoure, e=1, ai=j, wt=0)
                    else:
                        pm.select(Joint, TargetModel)
                        pm.mel.SmoothBindSkin()
                # ���п���Ȩ��
                if CopyWay == 'Normal':
                    if TargetType == 'Model':
                        for T in Target:
                            pm.select(Soure, T)
                            pm.copySkinWeights(surfaceAssociation='closestPoint',
                                               influenceAssociation=['closestJoint', 'oneToOne'], noMirror=1)
                    if TargetType == 'Point':
                        pm.select(Soure, Target)
                        pm.copySkinWeights(surfaceAssociation='closestPoint',
                                           influenceAssociation=['closestJoint', 'oneToOne'], noMirror=1)
                        if Removejoint:
                            for j in Removejoint:
                                pm.skinCluster(HaveWeightSoure, e=1, ri=j)
                if CopyWay == 'UV':
                    if SoureUVset and TargetUVset:
                        if TargetType == 'Model':
                            for T in Target:
                                pm.select(Soure, T)
                                pm.copySkinWeights(surfaceAssociation='closestPoint', uvSpace=(SoureUVset, TargetUVset),
                                                   noMirror=1, influenceAssociation=['closestJoint', 'oneToOne'])
                        if TargetType == 'Point':
                            pm.select(Soure, Target)
                            pm.copySkinWeights(surfaceAssociation='closestPoint', uvSpace=(SoureUVset, TargetUVset),
                                               noMirror=1, influenceAssociation=['closestJoint', 'oneToOne'])
                            if Removejoint:
                                for j in Removejoint:
                                    pm.skinCluster(HaveWeightSoure, e=1, ri=j)
                    else:
                        pm.error('�����uvѡ��')
            else:
                pm.error('Դû�й�����Ƥ')

    # �ײ�ƽ��Ȩ��
    # ZKM_JointWeightProcessingClass().ZKM_SmoothWeight('pSphere1', 1, 3)
    def ZKM_SmoothWeight(self, Model, NormalizeWeight, CS):
        Joint = pm.skinCluster(q=1, inf=1)
        pm.select(Model)
        if NormalizeWeight == 1:
            pm.skinCluster(e=1, nw=2)
        else:
            pm.skinCluster(e=1, nw=1)
        pm.select(Model)
        pm.mel.ArtPaintSkinWeightsTool()
        pm.mel.artAttrPaintOperation('artAttrSkinPaintCtx', 'Smooth')
        for i in range(0, len(Joint)):
            pm.mel.setSmoothSkinInfluence(Joint[i])
            pm.mel.eval('artSkinRevealSelected artAttrSkinPaintCtx;')
            for J in range(0, CS):
                pm.artAttrSkinPaintCtx(pm.currentCtx(),
                                       opacity=1, clear=1, e=1)

    # ��ģ�ͷ�����������Ȩ�ط�������ײ�
    # ZKM_JointWeightProcessingClass().ZKM_MergeWeightsToTargets(['pSphere7'], ['pSphere1','pSphere2','pSphere3'])
    def ZKM_MergeWeightsToTargets(self, SoureModel, DecomposeModel):
        ModelCopyGrp = []
        for i in range(0, len(DecomposeModel)):
            pm.select(DecomposeModel[i])
            Joint = pm.skinCluster(q=1, inf=1)
            pm.duplicate(rr=1)
            ModelCopy = pm.ls(sl=1)
            ModelCopyGrp.append(ModelCopy)
            pm.select(Joint, ModelCopy)
            pm.mel.SmoothBindSkin()
            pm.select(DecomposeModel[i], ModelCopy)
            self.ZKM_CopyModelWeightApply()
        pm.select(ModelCopyGrp)
        pm.polyUniteSkinned(ModelCopyGrp, centerPivot=1, ch=0, mergeUVSets=1)
        CureModel = pm.ls(sl=1)
        self.ZKM_CopyWeight('Normal', str(CureModel[0]), SoureModel, '', '')
        pm.delete(ModelCopyGrp)
        pm.delete(CureModel)

    # ����Ȩ��
    # ZKM_JointWeightProcessingClass().ExportWeight(['pSphere1'])
    def ExportWeight(self, Model):
        # ��ѯ��ǰMaya��װ·��
        MAYA_VERSION = cmds.about(version=True)[:4]
        MayaPath = os.environ['HOME'] + "/maya/" + MAYA_VERSION
        # ��ѯ��������ʱ�ļ���
        AllPath = MayaPath.split('/')
        path = AllPath[0]
        for i in range(1, len(AllPath)):
            path = path + '\\' + AllPath[i]
        if not os.path.exists(path + '\scripts\MayaWeightExportImportWeightProvisionalFolder'):
            os.mkdir(path + '\scripts\MayaWeightExportImportWeightProvisionalFolder')
        # �����뼴�����ɵ��ļ��������ļ�
        #print (MayaPath + '/scripts/MayaWeightExportImportWeightProvisionalFolder')
        if any(name.endswith(('.xml')) for name in
               os.listdir(MayaPath + '/scripts/MayaWeightExportImportWeightProvisionalFolder/')):
            my_path = (MayaPath + '/scripts/MayaWeightExportImportWeightProvisionalFolder/')
            for file_name in listdir(my_path):
                if file_name.endswith('.xml'):
                    os.remove(my_path + file_name)
                if file_name.endswith('.txt'):
                    os.remove(my_path + file_name)
        # �����ִ����ı�
        for MD in Model:
            SkinCluster = pm.mel.findRelatedSkinCluster(MD)
            if not SkinCluster:
                break
        for MD in Model:
            SkinCluster = pm.mel.findRelatedSkinCluster(MD)
            if SkinCluster:
                Joint = pm.skinCluster(MD, q=1, inf=1)
                file = open((path + '\scripts\MayaWeightExportImportWeightProvisionalFolder\\' + MD + '.txt'), "w")
                for Jon in Joint:
                    file.write(Jon + '\n')
                file.close()
                pm.mel.eval('deformerWeights -export -deformer \"' + SkinCluster + '\" -path \"' + MayaPath + '/scripts/MayaWeightExportImportWeightProvisionalFolder/' + '\" \"' + MD + '.xml\";')
        print('\n���Ҫ��ѯ��������·����' + '\n' + str(path) + '\scripts\MayaWeightExportImportWeightProvisionalFolder\n')
    # ����Ȩ��
    # noinspection PyTypeChecker
    # ZKM_JointWeightProcessingClass().ImportWeight(['Flour'])
    def ImportWeight(self, Model):
        # ��ѯ��ǰMaya��װ·��
        MAYA_VERSION = cmds.about(version=True)[:4]
        MayaPath = os.environ['HOME'] + "/maya/" + MAYA_VERSION
        # ��ѯ��ʱ�ļ���
        AllPath = MayaPath.split('/')
        path = AllPath[0]
        for i in range(1, len(AllPath)):
            path = path + '\\' + AllPath[i]
        if not os.path.exists(path + '\scripts\MayaWeightExportImportWeightProvisionalFolder'):
            print('\nû���ҵ��������Ȩ�ش���ļ��У����ȵ���Ȩ�ء�\n���Ҫ��ѯ��������·����' + '\n' + str(
                path) + '\scripts\MayaWeightExportImportWeightProvisionalFolder\n')
        else:
            AllNodes = pm.ls(type='joint')
            for MD in Model:
                if not os.path.exists(path + '\scripts\MayaWeightExportImportWeightProvisionalFolder\\'+ MD + ".xml"):
                    print('\n���û���ҵ��������Ȩ�ش���ļ��У����ȵ���Ȩ�ء�\n���Ҫ��ѯ��������·����' + '\n' + str(path) + '\scripts\MayaWeightExportImportWeightProvisionalFolder\\'+ str(MD) + ".xml"+'\n')
                else:

                    fo = open(path + "\scripts\MayaWeightExportImportWeightProvisionalFolder\\" + MD + ".txt", "r")
                    lines = [l.split() for l in fo if l.strip()]
                    fo.close()
                    for i in range(0, len(lines)):
                        lines[i] = str(lines[i])[2:-2]
                    addJoint = [x for x in lines if x not in AllNodes]  # ɸѡ����Ҫ���䴴���Ĺ���
                    for J in addJoint:  # �������
                        pm.select(cl=1)
                        pm.joint(p=(0, 0, 0), n=J)
                    try:
                        HaveSkinCluster = str(pm.mel.findRelatedSkinCluster(MD))  # ��ѯ�Ƿ�����Ƥ�ڵ�
                    except:
                        HaveSkinCluster = []

                    if HaveSkinCluster:
                        pm.select(MD, r=1)
                        shapes = pm.listRelatives(MD, shapes=1)
                        pm.skinCluster(shapes[0], e=1, ub=1)

                    pm.select(lines, MD)
                    pm.mel.SmoothBindSkin()
                    pm.select(MD)
                    SkinCluster = str(pm.mel.findRelatedSkinCluster(MD))  # ��ѯ��Ƥ�ڵ�
                    pm.deformerWeights((MD + ".xml"),
                                       path=(MayaPath + "/scripts/MayaWeightExportImportWeightProvisionalFolder/"), im=1,
                                       method="index", deformer=SkinCluster)
                    pm.skinCluster(SkinCluster, forceNormalizeWeights=1, e=1)
                    #print('\n���Ҫ��ѯ��������·����' + '\n' + str(path) + '\scripts\MayaWeightExportImportWeightProvisionalFolder\n���û�е�����ȷ���Ƿ������������Ʋ�һ��\n')
        cmds.refresh()

    # ת��Ȩ��
    # ZKM_JointWeightProcessingClass().TransferWeight('pSphere1')
    def TransferWeight(self, Model):
        Joint = pm.ls(sl=1)
        SkinCluster = str(pm.mel.findRelatedSkinCluster(Model))
        pm.select((Model + ".vtx[0:999999999]"))
        pm.skinPercent(SkinCluster, tmw=[Joint[0], Joint[1]])
        pm.select(Model, r=1)



