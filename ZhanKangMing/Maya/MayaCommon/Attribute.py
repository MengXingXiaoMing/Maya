#coding=gbk
import pymel.core as pm
class ZKM_AttributeClass:
    #添加属性
    def ZKM_AddAttributes(self,Curve,Type,AttributesName,HaveMin,min,HaveMax,max,Aefault):
        pm.select(Curve)
        if HaveMin == 0:
            min = Aefault
        if HaveMax == 0:
            max = Aefault
        pm.addAttr(Curve, ln=AttributesName, max=max, dv=Aefault, at=Type, min=min)
        pm.setAttr((Curve+'.'+AttributesName), e=1, keyable=True)
        if HaveMin == 0:
            pm.mel.dynRenameMinCheckChanged(False, ('.'+AttributesName))
        if HaveMax == 0:
            pm.mel.dynRenameMaxCheckChanged(False, ('.'+AttributesName))
        #AddAttributes('nurbsCircle1','double','A',1,0,0,0,0)#long是整型
    #设置默认属性范围
    def ZKM_SetDefaultAttributeRange(self,Curve,AttributesName,HaveMin,min,HaveMax,max):
        if AttributesName == 'tx':
            pm.transformLimits(Curve, etx=(HaveMin, HaveMax), tx=(min, max))
        if AttributesName == 'ty':
            pm.transformLimits(Curve, ety=(HaveMin, HaveMax), ty=(min, max))
        if AttributesName == 'tz':
            pm.transformLimits(Curve, etz=(HaveMin, HaveMax), tz=(min, max))
        if AttributesName == 'rx':
            pm.transformLimits(Curve, erx=(HaveMin, HaveMax), rx=(min, max))
        if AttributesName == 'ry':
            pm.transformLimits(Curve, ery=(HaveMin, HaveMax), ry=(min, max))
        if AttributesName == 'rz':
            pm.transformLimits(Curve, erz=(HaveMin, HaveMax), rz=(min, max))
        if AttributesName == 'sx':
            pm.transformLimits(Curve, esx=(HaveMin, HaveMax), sx=(min, max))
        if AttributesName == 'sy':
            pm.transformLimits(Curve, esy=(HaveMin, HaveMax), sy=(min, max))
        if AttributesName == 'sz':
            pm.transformLimits(Curve, esz=(HaveMin, HaveMax), sz=(min, max))
        #SetDefaultAttributeRange('nurbsCircle1','tx',1,1,1,2)
    #链接属性
    def ZKM_LinkAttributes(self,Soure,Target,NodeType,Multiplier,SoureMappingMin,SoureMappingMax,TargetMappingMin,TargetMappingMax):
        if NodeType == 'multiplyDivide':
            pm.shadingNode('multiplyDivide', asUtility=1 ,n=(Soure.split('.')[0]+'_multiplyDivide_'+Target.split('.')[0]))
            pm.connectAttr(Soure, (Soure.split('.')[0]+'_multiplyDivide_'+Target.split('.')[0]+'.input1X'), f=1)
            pm.setAttr((Soure.split('.')[0]+'_multiplyDivide_'+Target.split('.')[0]+'.input2X'), Multiplier)
            pm.connectAttr((Soure.split('.')[0]+'_multiplyDivide_'+Target.split('.')[0]+'.outputX'), Target, f=1)
        if NodeType == 'setRange':
            pm.shadingNode('setRange', asUtility=1 ,n=(Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]))
            pm.connectAttr(Soure, (Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]+'.valueX'), f=1)
            pm.setAttr((Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]+'.minX'), SoureMappingMin)
            pm.setAttr((Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]+'.maxX'), SoureMappingMax)
            pm.setAttr((Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]+'.oldMinX'), TargetMappingMin)
            pm.setAttr((Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]+'.oldMaxX'), TargetMappingMax)
            pm.connectAttr((Soure.split('.')[0]+'_setRange_'+Target.split('.')[0]+'.outValueX'), Target, f=1)
    #锁定并隐藏无用属性
    def ZKM_HideUselessAttributes(self,Sel):
        OwnAttributes = pm.listAttr(Sel, ud=1)
        OwnAttributes.append(u'v')
        LockNormalAttributes=[]
        for Attributes in ['translate', 'rotate', 'scale']:
            SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), s=1 ,d=0)#判断属性是否有输入
            if SoureAndTarget:#如果有输入
                for Axial in ['X', 'Y', 'Z']:#添加到列表
                    LockNormalAttributes.append((Attributes + Axial))
            else:#如果没有输入
                SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), p=1, c=1)  # 获取具体属性的输入输出
                if not SoureAndTarget:#如果输出不存在
                    for Axial in ['X','Y','Z']:#开始判断下层有没有输入或者输出
                        SoureAndTarget = pm.listConnections((Sel + '.' + Attributes + Axial), s=1, d=0)  # 判断属性是否有输入
                        if SoureAndTarget:
                            LockNormalAttributes.append((Attributes + Axial))
                        else:
                            SoureAndTarget = pm.listConnections((Sel + '.' + Attributes + Axial), p=1, c=1)#获取具体属性的输入输出
                            if not SoureAndTarget:#如果没有输出(已经没有输入了)
                                LockNormalAttributes.append((Attributes + Axial))
        for Attributes in OwnAttributes:
            SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), s=1 ,d=0)#判断属性是否有输入
            if SoureAndTarget:
                LockNormalAttributes.append(Attributes)
            else:
                SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), p=1, c=1)  # 获取具体属性的输入输出
                if not SoureAndTarget:  # 如果没有输出(已经没有输入了)
                    LockNormalAttributes.append(Attributes)
        for Attributes in LockNormalAttributes:
            pm.setAttr((Sel + '.' + Attributes), lock=True, channelBox=False, keyable=False)
    #锁定并隐藏选择的控制器无用属性
    def ZKM_SelHideUselessAttributes(self):
        Sel = pm.ls(sl=1)
        if str(type(Sel)) == '<type \'list\'>':
            for sel in Sel:
                ZKM_AttributeClass().ZKM_HideUselessAttributes(sel)
        else:
            ZKM_AttributeClass().ZKM_HideUselessAttributes(str(Sel).split('\'')[1])
    #显示选择控制器的所有属性
    def ZKM_ShowSelectAllAttributes(self):
        Sel= pm.ls(sl=1)
        if str(type(Sel)) == '<type \'list\'>':
            for sel in Sel:
                ZKM_AttributeClass().ZKM_ShowAllAttributes(sel)
        else:
            ZKM_AttributeClass().ZKM_ShowAllAttributes(str(Sel).split('\'')[1])
    #显示所有属性
    def ZKM_ShowAllAttributes(self,Sel):
        OwnAttributes = pm.listAttr(Sel, ud=1)
        for x in ['translateX','translateY','translateZ', 'rotateX','rotateY','rotateZ', 'scaleX', 'scaleY', 'scaleZ']:
            OwnAttributes.append(x)
        for Attributes in OwnAttributes:
            pm.setAttr((Sel+'.'+str(Attributes)), k=True)