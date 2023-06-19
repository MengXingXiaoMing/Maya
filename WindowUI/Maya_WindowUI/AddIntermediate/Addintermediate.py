#coding=gbk
import maya.cmds as cmds
import pymel.core as pm

def Window():#����
    if cmds.window('PresetTemplate', ex=1,cc='CleanWindow()'):
        cmds.deleteUI('PresetTemplate')
    cmds.window('PresetTemplate', t="���淶�Զ������м�֡")
    cmds.rowColumnLayout(nc=1, adj=5)
    cmds.textFieldButtonGrp('LoadNameA',bl='����Դ������ߵ���ģ�ͣ�',bc='ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadNameA\')')
    cmds.textFieldButtonGrp('LoadNameB',bl='����BS����',bc='ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadNameB\')')
    cmds.textFieldButtonGrp('LoadNameC',bl='��д������������',bc='ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadNameC\')')
    cmds.button(l='��ʼ����', command='Create()')
    cmds.showWindow()
def Create():
    A = cmds.textFieldButtonGrp('LoadNameA', q=1, text=1)
    B = cmds.textFieldButtonGrp('LoadNameB', q=1, text=1)
    C = cmds.textFieldButtonGrp('LoadNameC', q=1, text=1)
    ZKM_AsSpecificationsAddBSIntermediateFrame(B, A, C)
def ZKM_AsSpecificationsAddBSIntermediateFrame(BsName, BaseBsGrp, Specifications):
    # ��ѯ���淶��Ӧ��bs(ĩβ����Ϊ000����999������0����0.999��bs������ֵ)
    pm.select(BaseBsGrp, hierarchy=1)
    BaseMD = pm.ls(sl=1, type='mesh', long=1)
    AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
    for i in range(0, len(AllBsName)):
        # �決����Ӧbs
        for BsNameIntermediateFrame in AllBsName:
            if (AllBsName[i] + Specifications) == BsNameIntermediateFrame[:len(AllBsName[i] + Specifications)]:
                num = float(BsNameIntermediateFrame[len(AllBsName[i] + Specifications):])
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
def ZKM_LoadText(Type,Name):
    sel=pm.ls(sl=1)
    Sel=pm.channelBox('mainChannelBox', q=1, sma=1)
    AllAttributeSel=[]
    AllSel=[]
    if Sel:
        for i in range(0,len(Sel)):
            AttributeSel=sel[0]+'.'+Sel[i]
            AllAttributeSel.append(AttributeSel)
        print (AllAttributeSel)
        AllSel=AllAttributeSel[0]
        for i in range(1,len(AllAttributeSel)):
            AllSel=AllSel+','+AllAttributeSel[i]
    if not Sel:
        if Type == 'textFieldButtonGrp':
            cmds.textFieldButtonGrp(Name,e=1, text=str(sel[0]))
    else:
        if Type == 'textFieldButtonGrp':
            cmds.textFieldButtonGrp(Name,e=1, text=str(AllSel))
if __name__ =='__main__':
    Window()

#ɾ����Ӱ������
