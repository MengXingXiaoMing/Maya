#coding=gbk

import pymel.core as pm
class ZKM_BsIntermediateFrame:
    # 按对应名称规范添加bs中间帧
    # ZKM_BsIntermediateFrame().ZKM_AsSpecificationsAddBSIntermediateFrame('face_bs', 'face_base', '_bt_')
    def ZKM_AsSpecificationsAddBSIntermediateFrame(self,BsName, BaseBsGrp, Specifications):
        # 查询按规范对应的bs(末尾必定要是数字)
        pm.select(BaseBsGrp, hierarchy=1)
        BaseMD = pm.ls(sl=1, type='mesh', long=1)
        AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        for i in range(0, len(AllBsName)):
            # 烘焙出对应bs
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
                    # 添加Bs中间帧
                    for j in range(0, len(BaseMD)):
                        pm.blendShape(BsName, ibt='absolute', ib=1, e=1, tc=True, t=(BaseMD[j], i, CopyMD[j], num))
                    pm.setAttr(BsName + '.' + BsNameIntermediateFrame, 0)
                    pm.delete(sel)
    # 清理Bs中间帧
    # ZKM_BsIntermediateFrame().ZKM_ClearBsIntermediateFrame('blendShape1')
    def ZKM_ClearBsIntermediateFrame(self,BsName):
        #AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        # 获取所有主要bs的对应数字
        AllNum = pm.listAttr(BsName+'.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsNum)):
            # 获取中间帧
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
    # 保持链接重建基础Bs（包括中间帧）
    # ZKM_BsIntermediateFrame().ZKM_KeepLinkRebuildBs('bace_bs_Mesh', 'blendShape1', 1)
    def ZKM_KeepLinkRebuildBs(self,Model, BsName, AddIntermediateFrame):
        AllLinkDictionary = self.ZKM_BakeBsBackDictionary( Model, BsName)
        # 自动添加中间帧
        if AddIntermediateFrame == 1:
            self.ZKM_AsSpecificationsAddBSIntermediateFrame(BsName, Model, '_')
        # 还原原链接
        for Dictionary in AllLinkDictionary:
            if Dictionary.get('soure'):
                pm.connectAttr(Dictionary.get('soure'), Dictionary.get('oneself'), f=1)
            if Dictionary.get('target'):
                for t in Dictionary.get('target'):
                    pm.connectAttr(Dictionary.get('oneself'), t, f=1)
    # 烘焙所有bs并返回出相关链接字典
    # print(ZKM_BsIntermediateFrame().ZKM_BakeBsBackDictionary('bace_bs_Mesh', 'blendShape1'))
    def ZKM_BakeBsBackDictionary(self,Model, BsName):
        AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
        AllLinkDictionary = []  # 创建还原链接字典
        # 建立原链接源和目标的字典，并断开原本链接
        for Bs in AllBsName:
            Soure = pm.connectionInfo((BsName + '.' + Bs), sfd=1)  # 获取源
            Target = pm.connectionInfo((BsName + '.' + Bs), dfs=1)  # 获取目标
            dictionary = {'soure': Soure, 'oneself': (BsName + '.' + Bs), 'target': Target}
            AllLinkDictionary.append(dictionary)
            if Soure:
                pm.disconnectAttr(str(Soure), (BsName + '.' + Bs))
            if Target:
                for T in Target:
                    pm.disconnectAttr((BsName + '.' + Bs), str(T))
        # 清理所有bs
        pm.setAttr((BsName + '.envelope'), 1)
        for Bs in AllBsName:
            pm.setAttr((BsName + '.' + Bs), 0)
        # 创建bs组
        pm.select(cl=1)
        pm.group(n='ZKM_AllFaceBsCure_Grp')
        # 轮流烘焙文件并改名
        # 先烘焙基础部分
        for Bs in AllBsName:
            pm.setAttr((BsName + '.' + Bs), 1)
            pm.select(Model)
            pm.duplicate(rr=1)
            sel = pm.ls(sl=1)
            pm.rename(sel, Bs)
            pm.parent(sel, 'ZKM_AllFaceBsCure_Grp')
            pm.setAttr((BsName + '.' + Bs), 0)
        # 再烘焙中间帧部分
        AllNum = pm.listAttr(BsName + '.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsNum)):
            # 获取中间帧
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
    # 将中间帧转换为游戏规范(有中间帧的bs必须有链接)
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
            # 当中间帧存在
            if pm.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = pm.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                '''if not type(IntermediateFrameName) == list:
                    a = str(IntermediateFrameName)
                    IntermediateFrameName = []
                    IntermediateFrameName.append(a)'''
                # 轮流记录中间帧所在位置
                num = []
                num.append(0)
                for j in range(0, len(IntermediateFrameName)):
                    n = IntermediateFrameName[j].split('_')[1]
                    n = float(n)
                    num.append(n)
                num.append(1)
                Dictionnaire = {'soure': str(IntermediateFrameName[0].split('_')[0]), 'IntermediateFrame': num}
                HaveBsIntermediateFrameDictionnaire.append(Dictionnaire)
        # 烘焙所有bs并返回出相关链接字典
        AllLinkDictionary = self.ZKM_BakeBsBackDictionary(Model, BsName)
        # 还原原链接
        for Dictionary in AllLinkDictionary:
            if Dictionary.get('soure'):
                pm.connectAttr(Dictionary.get('soure'), Dictionary.get('oneself'), f=1)
            if Dictionary.get('target'):
                for t in Dictionary.get('target'):
                    pm.connectAttr(Dictionary.get('oneself'), t, f=1)
        # 按字典进行创建过渡
        # 创建代理源
        pm.shadingNode('plusMinusAverage', asUtility=1, n='LS_ProxyLink')
        # 添加代理属性
        pm.addAttr('LS_ProxyLink', ln='AgentProperties', dv=0, at='double')
        pm.setAttr('LS_ProxyLink.AgentProperties', e=1, keyable=True)
        for Dic in HaveBsIntermediateFrameDictionnaire:
            # 断开原本链接并保存源
            Soure = pm.connectionInfo((BsName + '.' + Dic.get('soure')), sfd=1)
            if Soure:
                pm.disconnectAttr(Soure, (BsName + '.' + Dic.get('soure')))
            # 按字典里所含关键帧的数字进行添加关键帧
            # 先对为0时进行k帧
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
            # 再对中间帧进行k帧
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
            # 为1时进行k帧
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
            # 转移代理
            if Soure:
                Target = pm.connectionInfo('LS_ProxyLink.AgentProperties', dfs=1)
                for t in Target:
                    pm.disconnectAttr('LS_ProxyLink.AgentProperties', t)
                    pm.connectAttr(Soure, t, f=1)
        # 删除代理链接
        pm.delete('LS_ProxyLink')
#end