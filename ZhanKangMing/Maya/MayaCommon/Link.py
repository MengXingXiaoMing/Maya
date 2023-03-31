#coding=gbk
import pymel.core as pm
class LinkClass:
    # 断开链接
    def BreakLink(self,Attribute):
        Soure = pm.connectionInfo(Attribute, sfd=1)  # 获取源
        Target = pm.connectionInfo(Attribute, dfs=1)  # 获取目标
        if Soure:
            pm.disconnectAttr(str(Soure), Attribute)
        if Target:
            for T in Target:
                print(T)
                pm.disconnectAttr(Attribute, str(T))
