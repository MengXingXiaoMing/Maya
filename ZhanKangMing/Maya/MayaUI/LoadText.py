#coding=gbk
import maya.cmds as cmds
import pymel.core as pm
#加载文本
class ZKM_LoadTextClass:
    def ZKM_LoadText(self, Type, Name):
        sel = pm.ls(sl=1, fl=1)
        Sel = pm.channelBox('mainChannelBox', q=1, sma=1)
        if sel or Sel:
            # 建立具体的文本
            if Sel:
                AllAttributeSel = []
                for i in range(0, len(Sel)):
                    AttributeSel = str(sel[0]) + '.' + str(Sel[i])
                    AllAttributeSel.append(AttributeSel)
                AllSel = AllAttributeSel[0]
                for i in range(1, len(AllAttributeSel)):
                    AllSel = AllSel + ',' + AllAttributeSel[i]
            else:
                AllSel = sel[0]
                for i in range(1, len(sel)):
                    AllSel = AllSel + ',' + sel[i]
            # 有属性加载物体属性，没属性加载物体
            if Sel:
                if Type == 'textFieldButtonGrp':
                    cmds.textFieldButtonGrp(Name, e=1, text=str(AllSel))
                if Type == 'textField':
                    cmds.textField(Name, e=1, text=str(AllSel))
                if Type == 'textFieldGrp':
                    cmds.textFieldGrp(Name, e=1, text=str(AllSel))
            else:
                if Type == 'textFieldButtonGrp':
                    cmds.textFieldButtonGrp(Name, e=1, text=str(AllSel))
                if Type == 'textField':
                    cmds.textField(Name, e=1, text=str(AllSel))
                if Type == 'textFieldGrp':
                    cmds.textFieldGrp(Name, e=1, text=str(AllSel))
        else:
            pm.error('请选择物体或者属性')
#选择文本的内容
class ZKM_ReadTextClass:
    def ZKM_ReadLoadText(self, Type, Name):
        if Type == 'textFieldButtonGrp':
            Text = cmds.textFieldButtonGrp(Name, q=1, text=1)
            AllText = Text.split(',')
            pm.select(AllText)
        if Type == 'textField':
            Text = pm.select(cmds.textField(Name, q=1, text=1))
            AllText = Text.split(',')
            pm.select(AllText)
        if Type == 'textFieldGrp':
            Text = pm.select(cmds.textFieldGrp(Name, q=1, text=1))
            AllText = Text.split(',')
            pm.select(AllText)
