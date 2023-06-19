#coding=gbk
import maya.cmds as cmds
import pymel.core as pm

def Window():#窗口
    if cmds.window('PresetTemplate', ex=1,cc='CleanWindow()'):
        cmds.deleteUI('PresetTemplate')
    cmds.window('PresetTemplate', t="按规范自动创建中间帧")
    cmds.rowColumnLayout(nc=1, adj=5)
    cmds.textFieldButtonGrp('LoadNameA',bl='加载源（组或者单个模型）',bc='ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadNameA\')')
    cmds.textFieldButtonGrp('LoadNameB',bl='加载BS名称',bc='ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadNameB\')')
    cmds.textFieldButtonGrp('LoadNameC',bl='填写除数字外区别',bc='ZKM_LoadText(\'textFieldButtonGrp\' , \'LoadNameC\')')
    cmds.button(l='开始生成', command='Create()')
    cmds.showWindow()
def Create():
    A = cmds.textFieldButtonGrp('LoadNameA', q=1, text=1)
    B = cmds.textFieldButtonGrp('LoadNameB', q=1, text=1)
    C = cmds.textFieldButtonGrp('LoadNameC', q=1, text=1)
    ZKM_AsSpecificationsAddBSIntermediateFrame(B, A, C)
def ZKM_AsSpecificationsAddBSIntermediateFrame(BsName, BaseBsGrp, Specifications):
    # 查询按规范对应的bs(末尾数字为000——999，代表0——0.999的bs具体数值)
    pm.select(BaseBsGrp, hierarchy=1)
    BaseMD = pm.ls(sl=1, type='mesh', long=1)
    AllBsName = pm.listAttr((BsName + '.w'), k=True, m=True)
    for i in range(0, len(AllBsName)):
        # 烘焙出对应bs
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
                # 添加Bs中间帧
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

#删除无影响驱动
