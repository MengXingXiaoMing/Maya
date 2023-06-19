#coding=gbk
import maya.cmds as cmds
import pymel.core as pm
#加载文本
class ZKM_AutomaticModificationUIRangeClass:
    # 自动调整滑块范围
    def ZKM_FloatSlider_Max_Edit_Controller(self,floatSlider):
        ShuLiang = float(pm.floatSliderGrp(floatSlider, q=1, v=1))
        ShuLiangMax = float(pm.floatSliderGrp(floatSlider, q=1, max=1))
        ShuLiangMaxA = 0.0
        ShuLiangMaxA = ShuLiangMax / 4.0
        if ShuLiang < ShuLiangMaxA:
            pm.floatSliderGrp(floatSlider, max=(ShuLiangMaxA * 2), e=1, fmx=9999999)
        ShuLiangMaxB = 0.0
        ShuLiangMaxB = ShuLiangMax / 4.0 * 3.0
        if ShuLiang > ShuLiangMaxB:
            pm.floatSliderGrp(floatSlider, max=(ShuLiangMaxB * 2), e=1, fmx=9999999)

    def ZKM_IntSlider_Max_Edit_Controller(self,intSlider):
        ShuLiang = int(pm.intSliderGrp(intSlider, q=1, v=1))
        ShuLiangMax = int(pm.intSliderGrp(intSlider, q=1, max=1))
        ShuLiangMaxA = 0
        ShuLiangMaxA = ShuLiangMax / 4
        if ShuLiang < ShuLiangMaxA:
            pm.intSliderGrp(intSlider, max=(ShuLiangMaxA * 2), e=1, fmx=9999999)
        ShuLiangMaxB = 0
        ShuLiangMaxB = ShuLiangMax / 4 * 3
        if ShuLiang > ShuLiangMaxB:
            pm.intSliderGrp(intSlider, max=(ShuLiangMaxB * 2), e=1, fmx=9999999)

