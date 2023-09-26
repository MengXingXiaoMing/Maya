#coding=gbk

import pymel.core as pm
class ZKM_BsIntermediateFrame:
    # ����Ӧ���ƹ淶���bs�м�֡
    # ZKM_BsIntermediateFrame().ZKM_AsSpecificationsAddBSIntermediateFrame('face_bs', 'face_base', '_bt_')
    def ZKM_AsSpecificationsAddBSIntermediateFrame(self,BsName, BaseBsGrp, Specifications):
        # ��ѯ���淶��Ӧ��bs(ĩβ�ض�Ҫ������)
        pm.select(BaseBsGrp, hierarchy=1)
        BaseMD = pm.ls(sl=1, type='mesh', long=1)
        AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        for i in range(0, len(AllBsName)):
            # �決����Ӧbs
            for BsNameIntermediateFrame in AllBsName:
                if (AllBsName[i] + Specifications) == BsNameIntermediateFrame[:len(AllBsName[i] + Specifications)]:
                    num = float(BsNameIntermediateFrame.split(Specifications)[1])
                    while num > 1:
                        num = num / 10.0
                    pm.setAttr(BsName + '.' + BsNameIntermediateFrame, 1)
                    pm.select(BaseBsGrp)
                    pm.duplicate(rr=1)
                    pm.rename(pm.ls(sl=1), BsNameIntermediateFrame)
                    sel = pm.ls(sl=1)
                    pm.select(sel, hierarchy=1)
                    CopyMD = pm.ls(sl=1, type='mesh', long=1)
                    # ���Bs�м�֡
                    for j in range(0, len(BaseMD)):
                        pm.blendShape(BsName, ibt='absolute', ib=1, e=1, tc=True, t=(BaseMD[j], i, CopyMD[j], num))
                    pm.setAttr(BsName + '.' + BsNameIntermediateFrame, 0)
                    pm.delete(sel)
    # ����Bs�м�֡
    # ZKM_BsIntermediateFrame().ZKM_ClearBsIntermediateFrame('blendShape1')
    def ZKM_ClearBsIntermediateFrame(self,BsName):
        #AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        # ��ȡ������Ҫbs�Ķ�Ӧ����
        AllNum = pm.listAttr(BsName+'.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsNum)):
            # ��ȡ�м�֡
            if pm.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = pm.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                if type(IntermediateFrameName) == list:
                    for name in IntermediateFrameName:
                        num = name.split('_')[1]
                        num = float(num) * 1000
                        pm.mel.blendShapeDeleteInBetweenTarget(BsName, int(AllBsNum[i]), int(5000 + num))
                else:
                    num = IntermediateFrameName.split('_')[1]
                    num = float(num) * 1000
                    pm.mel.blendShapeDeleteInBetweenTarget(BsName, int(AllBsNum[i]), int(5000 + num))
    # ���������ؽ�����Bs�������м�֡��
    # ZKM_BsIntermediateFrame().ZKM_KeepLinkRebuildBs('bace_bs_Mesh', 'blendShape1', 1)
    def ZKM_KeepLinkRebuildBs(self,Model, BsName, AddIntermediateFrame):
        AllLinkDictionary = self.ZKM_BakeBsBackDictionary( Model, BsName)
        # �Զ�����м�֡
        if AddIntermediateFrame == 1:
            self.ZKM_AsSpecificationsAddBSIntermediateFrame(BsName, Model, '_')
        # ��ԭԭ����
        for Dictionary in AllLinkDictionary:
            if Dictionary.get('soure'):
                pm.connectAttr(Dictionary.get('soure'), Dictionary.get('oneself'), f=1)
            if Dictionary.get('target'):
                for t in Dictionary.get('target'):
                    pm.connectAttr(Dictionary.get('oneself'), t, f=1)
    # �決����bs�����س���������ֵ�
    # print(ZKM_BsIntermediateFrame().ZKM_BakeBsBackDictionary('bace_bs_Mesh', 'blendShape1'))
    def ZKM_BakeBsBackDictionary(self,Model, BsName):
        AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        AllLinkDictionary = []  # ������ԭ�����ֵ�
        # ����ԭ����Դ��Ŀ����ֵ䣬���Ͽ�ԭ������
        for Bs in AllBsName:
            Soure = pm.connectionInfo((BsName + '.' + Bs), sfd=1)  # ��ȡԴ
            Target = pm.connectionInfo((BsName + '.' + Bs), dfs=1)  # ��ȡĿ��
            dictionary = {'soure': Soure, 'oneself': (BsName + '.' + Bs), 'target': Target}
            AllLinkDictionary.append(dictionary)
            if Soure:
                pm.disconnectAttr(str(Soure), (BsName + '.' + Bs))
            if Target:
                for T in Target:
                    pm.disconnectAttr((BsName + '.' + Bs), str(T))
        # ��������bs
        pm.setAttr((BsName + '.envelope'), 1)
        for Bs in AllBsName:
            pm.setAttr((BsName + '.' + Bs), 0)
        # ����bs��
        pm.select(cl=1)
        pm.group(n='ZKM_AllFaceBsCure_Grp')
        # �����決�ļ�������
        # �Ⱥ決��������
        for Bs in AllBsName:
            pm.setAttr((BsName + '.' + Bs), 1)
            pm.select(Model)
            pm.duplicate(rr=1)
            sel = pm.ls(sl=1)
            pm.rename(sel, Bs)
            pm.parent(sel, 'ZKM_AllFaceBsCure_Grp')
            pm.setAttr((BsName + '.' + Bs), 0)
        # �ٺ決�м�֡����
        AllNum = pm.listAttr(BsName + '.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsNum)):
            # ��ȡ�м�֡
            if pm.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = pm.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                '''if not type(IntermediateFrameName) == list:
                    a = str(IntermediateFrameName)
                    IntermediateFrameName = []
                    IntermediateFrameName.append(a)'''
                for name in IntermediateFrameName:
                    num = name.split('_')[1]
                    num = float(num)
                    pm.setAttr((BsName + '.' + name.split('_')[0]), num)

                    pm.select(Model)
                    sel = pm.duplicate(rr=1)
                    pm.rename(sel, name.split('_')[0] + '_' + str(int(num * 1000)))
                    pm.parent(sel, 'ZKM_AllFaceBsCure_Grp')
                    pm.setAttr((BsName + '.' + name.split('_')[0]), 0)
        pm.delete(BsName)
        BsModel = pm.listRelatives('ZKM_AllFaceBsCure_Grp', c=1)
        pm.select(BsModel)
        pm.select(Model, add=1)
        NewBsName = pm.blendShape(frontOfChain=1)
        pm.rename(NewBsName, BsName)
        return AllLinkDictionary
    # ���м�֡ת��Ϊ��Ϸ�淶(���м�֡��bs����������)
    # ZKM_BsIntermediateFrame().ZKM_BSIntermediateFrameConversionSpecification('pCube1', 'blendShape1')
    def ZKM_BSIntermediateFrameConversionSpecification(self, Model, BsName):
        AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        AllNum = pm.listAttr(BsName + '.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        HaveBsIntermediateFrameDictionnaire = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsName)):
            # ���м�֡����
            if pm.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = pm.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                '''if not type(IntermediateFrameName) == list:
                    a = str(IntermediateFrameName)
                    IntermediateFrameName = []
                    IntermediateFrameName.append(a)'''
                # ������¼�м�֡����λ��
                num = []
                num.append(0)
                for j in range(0, len(IntermediateFrameName)):
                    n = IntermediateFrameName[j].split('_')[1]
                    n = float(n)
                    num.append(n)
                num.append(1)
                Dictionnaire = {'soure': str(IntermediateFrameName[0].split('_')[0]), 'IntermediateFrame': num}
                HaveBsIntermediateFrameDictionnaire.append(Dictionnaire)
        # �決����bs�����س���������ֵ�
        AllLinkDictionary = self.ZKM_BakeBsBackDictionary(Model, BsName)
        # ��ԭԭ����
        for Dictionary in AllLinkDictionary:
            if Dictionary.get('soure'):
                pm.connectAttr(Dictionary.get('soure'), Dictionary.get('oneself'), f=1)
            if Dictionary.get('target'):
                for t in Dictionary.get('target'):
                    pm.connectAttr(Dictionary.get('oneself'), t, f=1)
        # ���ֵ���д�������
        # ��������Դ
        pm.shadingNode('plusMinusAverage', asUtility=1, n='LS_ProxyLink')
        # ��Ӵ�������
        pm.addAttr('LS_ProxyLink', ln='AgentProperties', dv=0, at='double')
        pm.setAttr('LS_ProxyLink.AgentProperties', e=1, keyable=True)
        for Dic in HaveBsIntermediateFrameDictionnaire:
            # �Ͽ�ԭ�����Ӳ�����Դ
            Soure = pm.connectionInfo((BsName + '.' + Dic.get('soure')), sfd=1)
            if Soure:
                pm.disconnectAttr(Soure, (BsName + '.' + Dic.get('soure')))
            # ���ֵ��������ؼ�֡�����ֽ�����ӹؼ�֡
            # �ȶ�Ϊ0ʱ����k֡
            pm.setAttr('LS_ProxyLink.AgentProperties', 0)
            pm.setAttr((BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0))), 0)
            pm.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0))),
                currentDriver='LS_ProxyLink.AgentProperties')
            pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[1])
            pm.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0)), 1)
            pm.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0))),
                currentDriver='LS_ProxyLink.AgentProperties')
            if Dic.get('IntermediateFrame')[2] == 1:
                pm.setAttr('LS_ProxyLink.AgentProperties', 1)
                pm.setAttr((BsName + '.' + Dic.get('soure')), 0)
                pm.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure')),
                    currentDriver='LS_ProxyLink.AgentProperties')
            else:
                pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[2])
                pm.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[2] * 1000.0)),
                           0)
                pm.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[2] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
            # �ٶ��м�֡����k֡
            for i in range(1, (len(Dic.get('IntermediateFrame')) - 1)):
                pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[i - 1])
                pm.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0)),
                           0)
                pm.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
                pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[i])
                pm.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0)),
                           1)
                pm.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
                pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[i + 1])
                pm.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0)),
                           0)
                pm.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
            # Ϊ1ʱ����k֡
            pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[-2])
            pm.setAttr((BsName + '.' + Dic.get('soure')), 0)
            pm.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure')),
                currentDriver='LS_ProxyLink.AgentProperties')
            pm.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[-1])
            pm.setAttr((BsName + '.' + Dic.get('soure')), 1)
            pm.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure')),
                currentDriver='LS_ProxyLink.AgentProperties')
            # ת�ƴ���
            if Soure:
                Target = pm.connectionInfo('LS_ProxyLink.AgentProperties', dfs=1)
                for t in Target:
                    pm.disconnectAttr('LS_ProxyLink.AgentProperties', t)
                    pm.connectAttr(Soure, t, f=1)
        # ɾ����������
        pm.delete('LS_ProxyLink')
#end