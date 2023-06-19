#coding=gbk
import pymel.core as pm
class ZKM_LinkClass:
    # 断开链接
    def ZKM_BreakLink(self,Attribute):
        for Att in Attribute:
            Soure = pm.connectionInfo(Att, sfd=1)  # 获取源
            Target = pm.connectionInfo(Att, dfs=1)  # 获取目标
            if Soure:
                pm.disconnectAttr(str(Soure), Att)
            if Target:
                for T in Target:
                    pm.disconnectAttr(Att, str(T))
    # ZKM_LinkClass().ZKM_BreakLink(['nurbsCircle1.translateY','nurbsCircle1.translateZ'])