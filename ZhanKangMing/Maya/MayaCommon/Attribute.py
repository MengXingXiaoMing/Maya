#coding=gbk
import pymel.core as pm
class ZKM_AttributeClass:
    #�������
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
        #AddAttributes('nurbsCircle1','double','A',1,0,0,0,0)#long������
    #����Ĭ�����Է�Χ
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
    #��������
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
    #������������������
    def ZKM_HideUselessAttributes(self,Sel):
        OwnAttributes = pm.listAttr(Sel, ud=1)
        OwnAttributes.append(u'v')
        LockNormalAttributes=[]
        for Attributes in ['translate', 'rotate', 'scale']:
            SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), s=1 ,d=0)#�ж������Ƿ�������
            if SoureAndTarget:#���������
                for Axial in ['X', 'Y', 'Z']:#��ӵ��б�
                    LockNormalAttributes.append((Attributes + Axial))
            else:#���û������
                SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), p=1, c=1)  # ��ȡ�������Ե��������
                if not SoureAndTarget:#������������
                    for Axial in ['X','Y','Z']:#��ʼ�ж��²���û������������
                        SoureAndTarget = pm.listConnections((Sel + '.' + Attributes + Axial), s=1, d=0)  # �ж������Ƿ�������
                        if SoureAndTarget:
                            LockNormalAttributes.append((Attributes + Axial))
                        else:
                            SoureAndTarget = pm.listConnections((Sel + '.' + Attributes + Axial), p=1, c=1)#��ȡ�������Ե��������
                            if not SoureAndTarget:#���û�����(�Ѿ�û��������)
                                LockNormalAttributes.append((Attributes + Axial))
        for Attributes in OwnAttributes:
            SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), s=1 ,d=0)#�ж������Ƿ�������
            if SoureAndTarget:
                LockNormalAttributes.append(Attributes)
            else:
                SoureAndTarget = pm.listConnections((Sel + '.' + Attributes), p=1, c=1)  # ��ȡ�������Ե��������
                if not SoureAndTarget:  # ���û�����(�Ѿ�û��������)
                    LockNormalAttributes.append(Attributes)
        for Attributes in LockNormalAttributes:
            pm.setAttr((Sel + '.' + Attributes), lock=True, channelBox=False, keyable=False)
    #����������ѡ��Ŀ�������������
    def ZKM_SelHideUselessAttributes(self):
        Sel = pm.ls(sl=1)
        if str(type(Sel)) == '<type \'list\'>':
            for sel in Sel:
                ZKM_AttributeClass().ZKM_HideUselessAttributes(sel)
        else:
            ZKM_AttributeClass().ZKM_HideUselessAttributes(str(Sel).split('\'')[1])
    #��ʾѡ�����������������
    def ZKM_ShowSelectAllAttributes(self):
        Sel= pm.ls(sl=1)
        if str(type(Sel)) == '<type \'list\'>':
            for sel in Sel:
                ZKM_AttributeClass().ZKM_ShowAllAttributes(sel)
        else:
            ZKM_AttributeClass().ZKM_ShowAllAttributes(str(Sel).split('\'')[1])
    #��ʾ��������
    def ZKM_ShowAllAttributes(self,Sel):
        OwnAttributes = pm.listAttr(Sel, ud=1)
        for x in ['translateX','translateY','translateZ', 'rotateX','rotateY','rotateZ', 'scaleX', 'scaleY', 'scaleZ']:
            OwnAttributes.append(x)
        for Attributes in OwnAttributes:
            pm.setAttr((Sel+'.'+str(Attributes)), k=True)