# -*- coding: utf-8 -*-
import importlib

import maya.cmds as cmds
import maya.mel as mel
# 获取文件路径
import os
import sys
import inspect
import webbrowser
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version

# 库添加到系统路径
sys.path.append(library_path)

class BlendshapeEdit:
    # 按对应名称规范添加bs中间帧
    # ZKM_BsIntermediateFrame().ZKM_AsSpecificationsAddBSIntermediateFrame('face_bs', 'face_base', '_bt_')
    def ZKM_AsSpecificationsAddBSIntermediateFrame(self,BsName, BaseBsGrp, Specifications):
        # 查询按规范对应的bs(末尾必定要是数字)
        cmds.select(BaseBsGrp, hierarchy=1)
        BaseMD = cmds.ls(sl=1, type='mesh', long=1)
        AllBsName = cmds.listAttr((BsName + '.w'), k=True, m=True)
        for i in range(0, len(AllBsName)):
            # 烘焙出对应bs
            for BsNameIntermediateFrame in AllBsName:
                if (AllBsName[i] + Specifications) == BsNameIntermediateFrame[:len(AllBsName[i] + Specifications)]:
                    num = float(BsNameIntermediateFrame.split(Specifications)[1])
                    while num > 1:
                        num = num / 10.0
                    cmds.setAttr(BsName + '.' + BsNameIntermediateFrame, 1)
                    cmds.select(BaseBsGrp)
                    cmds.duplicate(rr=1)
                    cmds.rename(cmds.ls(sl=1), BsNameIntermediateFrame)
                    sel = cmds.ls(sl=1)
                    cmds.select(sel, hierarchy=1)
                    CopyMD = cmds.ls(sl=1, type='mesh', long=1)
                    # 添加Bs中间帧
                    for j in range(0, len(BaseMD)):
                        cmds.blendShape(BsName, ibt='absolute', ib=1, e=1, tc=True, t=(BaseMD[j], i, CopyMD[j], num))
                    cmds.setAttr(BsName + '.' + BsNameIntermediateFrame, 0)
                    cmds.delete(sel)

    # 清理Bs中间帧
    # ZKM_BsIntermediateFrame().ZKM_ClearBsIntermediateFrame('blendShape1')
    def ZKM_ClearBsIntermediateFrame(self,BsName):
        #AllBsName = cmds.listAttr((BsName + '.w'), k=True, m=True)
        # 获取所有主要bs的对应数字
        AllNum = cmds.listAttr(BsName+'.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsNum)):
            # 获取中间帧
            if cmds.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = cmds.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                if type(IntermediateFrameName) == list:
                    for name in IntermediateFrameName:
                        num = name.split('_')[1]
                        num = float(num) * 1000
                        cmds.mel.blendShapeDeleteInBetweenTarget(BsName, int(AllBsNum[i]), int(5000 + num))
                else:
                    num = IntermediateFrameName.split('_')[1]
                    num = float(num) * 1000
                    cmds.mel.blendShapeDeleteInBetweenTarget(BsName, int(AllBsNum[i]), int(5000 + num))

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
                cmds.connectAttr(Dictionary.get('soure'), Dictionary.get('oneself'), f=1)
            if Dictionary.get('target'):
                for t in Dictionary.get('target'):
                    cmds.connectAttr(Dictionary.get('oneself'), t, f=1)

    # 烘焙所有bs并返回出相关链接字典
    # print(ZKM_BsIntermediateFrame().ZKM_BakeBsBackDictionary('face_base', 'blendShape1'))
    def ZKM_BakeBsBackDictionary(self,Model, BsName):
        AllBsName = cmds.listAttr((BsName + '.w'), k=True, m=True)
        AllLinkDictionary = []  # 创建还原链接字典
        # 建立原链接源和目标的字典，并断开原本链接
        for Bs in AllBsName:
            Soure = cmds.connectionInfo((BsName + '.' + Bs), sfd=1)  # 获取源
            Target = cmds.connectionInfo((BsName + '.' + Bs), dfs=1)  # 获取目标
            dictionary = {'soure': Soure, 'oneself': (BsName + '.' + Bs), 'target': Target}
            AllLinkDictionary.append(dictionary)
            if Soure:
                cmds.disconnectAttr(str(Soure), (BsName + '.' + Bs))
            if Target:
                for T in Target:
                    cmds.disconnectAttr((BsName + '.' + Bs), str(T))
        # 清理所有bs
        cmds.setAttr((BsName + '.envelope'), 1)
        for Bs in AllBsName:
            cmds.setAttr((BsName + '.' + Bs), 0)
        # 创建bs组
        cmds.select(cl=1)
        cmds.group(n='ZKM_AllFaceBsCure_Grp')
        # 轮流烘焙文件并改名
        # 先烘焙基础部分
        for Bs in AllBsName:
            cmds.setAttr((BsName + '.' + Bs), 1)
            cmds.select(Model)
            cmds.duplicate(rr=1)
            sel = cmds.ls(sl=1)
            cmds.rename(sel, Bs)
            cmds.parent(sel, 'ZKM_AllFaceBsCure_Grp')
            cmds.setAttr((BsName + '.' + Bs), 0)
        # 再烘焙中间帧部分
        AllNum = cmds.listAttr(BsName + '.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsNum)):
            # 获取中间帧
            if cmds.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = cmds.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                '''if not type(IntermediateFrameName) == list:
                    a = str(IntermediateFrameName)
                    IntermediateFrameName = []
                    IntermediateFrameName.append(a)'''
                for name in IntermediateFrameName:
                    num = name.split('_')[-1]
                    num = float(num)
                    DictionnaireS = str(IntermediateFrameName[0].split('_')[0])
                    for i in range(1,len(IntermediateFrameName[0].split('_')[:-1])):
                        DictionnaireS = DictionnaireS + '_' + (IntermediateFrameName[0].split('_')[:-1])[i]
                    cmds.setAttr((BsName + '.' + DictionnaireS), num)
                    cmds.select(Model)
                    sel = cmds.duplicate(rr=1)
                    cmds.rename(sel, DictionnaireS + '_' + str(int(num * 1000)))
                    cmds.parent(sel, 'ZKM_AllFaceBsCure_Grp')
                    cmds.setAttr((BsName + '.'+DictionnaireS), 0)
        cmds.delete(BsName)
        BsModel = cmds.listRelatives('ZKM_AllFaceBsCure_Grp', c=1)
        cmds.select(BsModel)
        cmds.select(Model, add=1)
        NewBsName = cmds.blendShape(frontOfChain=1)
        cmds.rename(NewBsName, BsName)
        return AllLinkDictionary

    # 将中间帧转换为游戏规范(有中间帧的bs必须有链接)
    # ZKM_BsIntermediateFrame().ZKM_BSIntermediateFrameConversionSpecification('pCube1', 'blendShape1')
    def ZKM_BSIntermediateFrameConversionSpecification(self, Model, BsName):
        AllBsName = cmds.listAttr((BsName + '.w'), k=True, m=True)
        AllNum = cmds.listAttr(BsName + '.inputTarget[0].inputTargetGroup[*]', c=1)
        i = 0
        AllBsNum = []
        HaveBsIntermediateFrameDictionnaire = []
        while i < len(AllNum):
            AllBsNum.append(int(AllNum[i].split('[')[-1][:-1]))
            i = i + 12
        for i in range(0, len(AllBsName)):
            # 当中间帧存在
            if cmds.objExists(BsName + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName'):
                IntermediateFrameName = cmds.mel.eval('getAttr \"' + str(BsName) + '.inbetweenInfoGroup[' + str(AllBsNum[i]) + '].inbetweenInfo[*].inbetweenTargetName\" ;')
                '''if not type(IntermediateFrameName) == list:
                    a = str(IntermediateFrameName)
                    IntermediateFrameName = []
                    IntermediateFrameName.append(a)'''
                # 轮流记录中间帧所在位置
                num = []
                num.append(0)
                for j in range(0, len(IntermediateFrameName)):
                    n = IntermediateFrameName[j].split('_')[-1]

                    n = float(n)
                    num.append(n)
                num.append(1)
                DictionnaireS = str(IntermediateFrameName[0].split('_')[0])
                for i in range(1, len(IntermediateFrameName[0].split('_')[:-1])):
                    DictionnaireS = DictionnaireS + '_' + (IntermediateFrameName[0].split('_')[:-1])[i]
                Dictionnaire = {'soure': DictionnaireS, 'IntermediateFrame': num}
                HaveBsIntermediateFrameDictionnaire.append(Dictionnaire)
        # 烘焙所有bs并返回出相关链接字典
        AllLinkDictionary = self.ZKM_BakeBsBackDictionary(Model, BsName)
        # 还原原链接
        for Dictionary in AllLinkDictionary:
            if Dictionary.get('soure'):
                cmds.connectAttr(Dictionary.get('soure'), Dictionary.get('oneself'), f=1)
            if Dictionary.get('target'):
                for t in Dictionary.get('target'):
                    cmds.connectAttr(Dictionary.get('oneself'), t, f=1)
        # 按字典进行创建过渡
        # 创建代理源
        cmds.shadingNode('plusMinusAverage', asUtility=1, n='LS_ProxyLink')
        # 添加代理属性
        cmds.addAttr('LS_ProxyLink', ln='AgentProperties', dv=0, at='double')
        cmds.setAttr('LS_ProxyLink.AgentProperties', e=1, keyable=True)
        for Dic in HaveBsIntermediateFrameDictionnaire:
            # 断开原本链接并保存源
            Soure = cmds.connectionInfo((BsName + '.' + Dic.get('soure')), sfd=1)
            if Soure:
                cmds.disconnectAttr(Soure, (BsName + '.' + Dic.get('soure')))
            # 按字典里所含关键帧的数字进行添加关键帧
            # 先对为0时进行k帧
            cmds.setAttr('LS_ProxyLink.AgentProperties', 0)
            cmds.setAttr((BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0))), 0)
            cmds.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0))),
                currentDriver='LS_ProxyLink.AgentProperties')
            cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[1])
            cmds.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0)), 1)
            cmds.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[1] * 1000.0))),
                currentDriver='LS_ProxyLink.AgentProperties')
            if Dic.get('IntermediateFrame')[2] == 1:
                cmds.setAttr('LS_ProxyLink.AgentProperties', 1)
                cmds.setAttr((BsName + '.' + Dic.get('soure')), 0)
                cmds.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure')),
                    currentDriver='LS_ProxyLink.AgentProperties')
            else:
                cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[2])
                cmds.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[2] * 1000.0)),
                           0)
                cmds.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[2] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
            # 再对中间帧进行k帧
            for i in range(1, (len(Dic.get('IntermediateFrame')) - 1)):
                cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[i - 1])
                cmds.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0)),
                           0)
                cmds.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
                cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[i])
                cmds.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0)),
                           1)
                cmds.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
                cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[i + 1])
                cmds.setAttr((BsName + '.' + Dic.get('soure')) + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0)),
                           0)
                cmds.setDrivenKeyframe(
                    (BsName + '.' + Dic.get('soure') + '_' + str(int(Dic.get('IntermediateFrame')[i] * 1000.0))),
                    currentDriver='LS_ProxyLink.AgentProperties')
            # 为1时进行k帧
            cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[-2])
            cmds.setAttr((BsName + '.' + Dic.get('soure')), 0)
            cmds.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure')),
                currentDriver='LS_ProxyLink.AgentProperties')
            cmds.setAttr('LS_ProxyLink.AgentProperties', Dic.get('IntermediateFrame')[-1])
            cmds.setAttr((BsName + '.' + Dic.get('soure')), 1)
            cmds.setDrivenKeyframe(
                (BsName + '.' + Dic.get('soure')),
                currentDriver='LS_ProxyLink.AgentProperties')
            # 转移代理
            if Soure:
                Target = cmds.connectionInfo('LS_ProxyLink.AgentProperties', dfs=1)
                for t in Target:
                    cmds.disconnectAttr('LS_ProxyLink.AgentProperties', t)
                    cmds.connectAttr(Soure, t, f=1)
        # 删除代理链接
        cmds.delete('LS_ProxyLink')

    # 不同拓补传递BS
    def transfer_different_topologies_bs(self, transmit_source, transmit_target, intermediate_state):
        cmds.undoInfo(ock=1)
        cmds.select(intermediate_state, transmit_source)
        cmds.CreateLattice()
        lattice = cmds.ls(sl=1)

        cmds.select(intermediate_state, transmit_source)
        cmds.Morph()
        cmds.select(intermediate_state, transmit_source, d=1)
        morph = cmds.ls(sl=1)

        shape = cmds.listRelatives(transmit_source,type = 'mesh')

        cmds.connectAttr((shape[1]+ '.outMesh'),(morph[0] + '.originalMorphTarget[0]'),force=1)
        cmds.setAttr(morph[0] + '.morphMode', 3)
        cmds.setAttr(morph[0] + '.neighborLevel', 10)
        cmds.delete(lattice)

        cmds.select(transmit_target, r=1)
        cmds.duplicate(rr=1)
        cmds.rename(cmds.ls(sl=1), transmit_target + "_Copy")
        cmds.transferAttributes(intermediate_state, (transmit_target + "_Copy"), flipUVs=0, transferPositions=1,
                                transferUVs=0, sourceUvSpace="map1", searchMethod=3,
                                transferNormals=1, transferColors=0, targetUvSpace="map1", colorBorders=1,
                                sampleSpace=3)
        cmds.select((transmit_target + "_Copy"), r=1)
        cmds.duplicate(rr=1)
        cmds.rename(cmds.ls(sl=1), transmit_target + "_CopySecond")
        cmds.blendShape((transmit_target + "_Copy"), (transmit_target + "_CopySecond"), transmit_target,
                        n="SecondPass_BS")
        cmds.setAttr(("SecondPass_BS." + transmit_target + "_Copy"), 1)
        cmds.setAttr(("SecondPass_BS." + transmit_target + "_CopySecond"), -1)
        cmds.delete(transmit_target + "_CopySecond")
        cmds.setAttr((transmit_source + ".visibility"), 0)
        cmds.setAttr((intermediate_state + ".visibility"), 0)
        cmds.setAttr((transmit_target + "_Copy.visibility"), 0)
        cmds.undoInfo(cck=1)

    # 加载的bs自动k帧
    def bs_auto_k_frame(self,bs_name,num):
        cmds.undoInfo(ock=1)
        # 查询动画的最后一帧
        all = cmds.ls()
        keyframes = cmds.keyframe(all, q=True)
        if keyframes:
            end_frames = max(keyframes)
        else:
            start = cmds.playbackOptions(q=True, min=True)
            end_frames = start
        # 开始k帧
        for bs in bs_name:
            bs = bs.split('.')
            cmds.setKeyframe(bs[0], t=(end_frames - 1.0), v=0, at=bs[1])
            cmds.setKeyframe(bs[0], t=end_frames, v=num, at=bs[1])
            cmds.setKeyframe(bs[0], t=(end_frames + 1.0), v=0, at=bs[1])
            end_frames = end_frames + 1
        cmds.undoInfo(cck=1)

    # 烘焙当前范围帧
    def back_frame(self,model):
        cmds.undoInfo(ock=1)
        start_time = cmds.playbackOptions(query=True, minTime=True)
        end_time = cmds.playbackOptions(query=True, maxTime=True)
        all = cmds.ls()
        keyframes = cmds.keyframe(all, q=True)
        frames_list = []
        for x in keyframes:
            if x not in frames_list:
                frames_list.append(x)
        print(frames_list)
        for frames in frames_list:
            if frames >= start_time and frames <= end_time:
                cmds.currentTime(frames)
                cmds.duplicate(model, n=model + '_' + str(frames))
            if frames > end_time:
                break
        cmds.undoInfo(cck=1)

    # 分解BS
    def split_bs(self, source, bs, reference):
        decomposere_ference_shapes = cmds.listRelatives(reference, shapes=1)
        cmds.select((decomposere_ference_shapes[0] + ".vtx[*]"), r=1)
        decomposere_ference_vtx = cmds.ls(fl=1, sl=1)
        decompose_bs = bs[0].split(".")
        # 清理BS属性
        cmds.setAttr((decompose_bs[0] + ".envelope"), 1)
        decompose_bs_welght = cmds.listAttr((decompose_bs[0] + ".weight"), k=1, m=1)
        for i in range(0, len(decompose_bs_welght)):
            cmds.setAttr((decompose_bs[0] + "." + decompose_bs_welght[i]), 0)
        # 开始轮流bs分解
        for i in range(0, len(bs)):
            cmds.select(reference)
            cmds.duplicate(rr=1,n=(reference + '_' + bs[i].split(".")[1] + "_X"))
            cmds.duplicate(rr=1,n=(reference + '_' + bs[i].split(".")[1] + "_Y"))
            cmds.duplicate(rr=1,n=(reference + '_' + bs[i].split(".")[1] + "_Z"))
            cmds.setAttr(bs[i], 1)
            cmds.select(source, r=1)
            cmds.duplicate(rr=1)
            Copy = cmds.ls(sl=1)
            cmds.select((Copy[0] + ".vtx[*]"), r=1)
            decompose_source_vtx = cmds.ls(fl=1, sl=1)
            cmds.setAttr(bs[i], 0)
            for j in range(0, len(decompose_source_vtx)):
                DecomposeSourceNum = cmds.xform(decompose_source_vtx[j], q=1, ws=1, t=1)
                DecomposereFerenceNum = cmds.xform(decomposere_ference_vtx[j], q=1, ws=1, t=1)
                cmds.setAttr((reference + '_' + bs[i].split(".")[1] + "_XShape" + ".pnts[" + str(j) + "].pntx"),
                             (DecomposeSourceNum[0] - DecomposereFerenceNum[0]))
                cmds.setAttr((reference + '_' + bs[i].split(".")[1] + "_YShape" + ".pnts[" + str(j) + "].pnty"),
                             (DecomposeSourceNum[1] - DecomposereFerenceNum[1]))
                cmds.setAttr((reference + '_' + bs[i].split(".")[1] + "_ZShape" + ".pnts[" + str(j) + "].pntz"),
                             (DecomposeSourceNum[2] - DecomposereFerenceNum[2]))
            cmds.move(0, 0, 0,
                      (reference + '_' + bs[i].split(".")[1] + "_X.vtx[0]"),
                      (reference + '_' + bs[i].split(".")[1] + "_Y.vtx[0]"),
                      (reference + '_' + bs[i].split(".")[1] + "_Z.vtx[0]"),
                      absolute=True)
            cmds.delete(Copy)
        cmds.refresh(f=1)