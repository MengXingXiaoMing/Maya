#coding=gbk
import maya.cmds as cmds
import pymel.core as pm
#�����ı�
class ZKM_SliderClass:
    # ��������
    def ZKM_Slider(self,SliderLine, Window, From, Num):
        num = pm.floatScrollBar(SliderLine, q=1, v=1)
        pm.formLayout(From, edit=1, attachPosition=(Window, "top", (num * Num), 0), attachForm=(Window, "left", 0))
