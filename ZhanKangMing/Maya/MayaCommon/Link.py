#coding=gbk
import pymel.core as pm
class LinkClass:
    # �Ͽ�����
    def BreakLink(self,Attribute):
        Soure = pm.connectionInfo(Attribute, sfd=1)  # ��ȡԴ
        Target = pm.connectionInfo(Attribute, dfs=1)  # ��ȡĿ��
        if Soure:
            pm.disconnectAttr(str(Soure), Attribute)
        if Target:
            for T in Target:
                print(T)
                pm.disconnectAttr(Attribute, str(T))
