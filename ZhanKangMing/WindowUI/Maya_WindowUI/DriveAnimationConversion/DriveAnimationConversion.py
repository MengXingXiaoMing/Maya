#coding=gbk
import pymel.core as pm
import maya.cmds as cmds
class ZKM_DriveAnimationConversionWindowClass:
    def WindowPLXGDH(self):
        if pm.window('DriveAnimationConversionWindow', ex=1):
            pm.deleteUI('DriveAnimationConversionWindow')
        pm.window('DriveAnimationConversionWindow', t='�����޸Ķ���')
        pm.columnLayout(w=325)
        pm.rowColumnLayout(nc=1, adj=4)
        pm.button(l='��ͼ�α༭��', c='cmds.GraphEditor()',bgc=(0.2,0.5,0.7))
        pm.rowColumnLayout(nc=1, adj=1,w=10)
        pm.textFieldButtonGrp('JZDHJD', bl='��������/�����ڵ�', text='', cw3=(70, 145,  0), l=('����/�����ڵ�'),bc='ZKM_DriveAnimationConversionWindowClass().jztxt(\'JZDHJD\')')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=2)
        pm.rowColumnLayout(nc=2, adj=2)
        pm.textFieldGrp('PYSLTransverse', text='0', cw2=(50, 40), l=('����ƫ��:'))
        pm.textFieldButtonGrp(bl='���', text='90',l=(''), cw3=(0, 80, 0),bc='ZKM_DriveAnimationConversionWindowClass().AddNumbers(\'PYSLTransverse\', \'AddNumbersTransverseText\')')
        pm.textFieldGrp('PYSLPortrait', text='0', cw2=(50, 40), l=('����ƫ��:'))
        pm.textFieldButtonGrp('AddNumbersPortraitText', bl='���', text='90',l=(''), cw3=(0, 80, 0),bc='ZKM_DriveAnimationConversionWindowClass().AddNumbers(\'PYSLPortrait\', \'AddNumbersPortraitText\')')
        pm.setParent('..')
        pm.button(c='ZKM_DriveAnimationConversionWindowClass().DriveAnimationDeviation()', l='ƫ��')
        pm.setParent('..')
        pm.separator(style="in", height=10)
        pm.button(c='ZKM_DriveAnimationConversionWindowClass().DriveAnimationDeviationTransformation()', l='���������ڵ㡶�������滻�������������ڵ㡶��')
        pm.separator(style="in", height=10)
        pm.button(c='ZKM_DriveAnimationConversionWindowClass().CopyAndLinkTarget()', l='����/�����ڵ�ת������(Դ������,Ŀ�����򸲸�)')
        pm.textFieldButtonGrp('JZLJY', bl='����', text='', cw3=(50, 230, 60), l=('����Դ:'), bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJY\')')
        pm.textFieldButtonGrp('JZLJMB', bl='����', text='', cw3=(50, 230, 60), l=('����Ŀ��:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.separator(style="in", height=10)
        pm.rowColumnLayout(nc=1, adj=1)
        pm.text(l='��������')
        pm.rowColumnLayout(nc=3, adj=1)

        pm.rowColumnLayout(nc=1, adj=1)
        pm.textFieldButtonGrp('JZLJMBsd', bl='����', text='', cw3=(35, 55, 0), l=('����Դ:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.textFieldButtonGrp('JZLJMB', bl='����', text='', cw3=(35, 55, 0), l=('����Դ:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.optionMenu()
        pm.menuItem(label="tx")
        pm.menuItem(label="ty")
        pm.menuItem(label="tz")
        pm.menuItem(label="rx")
        pm.menuItem(label="ry")
        pm.menuItem(label="rz")
        pm.menuItem(label="sx")
        pm.menuItem(label="sy")
        pm.menuItem(label="sz")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=2)
        pm.textFieldButtonGrp('JZLJMBsd', bl='����', text='', cw3=(50, 55, 0), l=('Դת�Ƶ�:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.textFieldButtonGrp('JZLJMB', bl='����', text='', cw3=(50, 55, 0), l=('����Ŀ��:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.optionMenu()
        pm.menuItem(label="tx")
        pm.menuItem(label="ty")
        pm.menuItem(label="tz")
        pm.menuItem(label="rx")
        pm.menuItem(label="ry")
        pm.menuItem(label="rz")
        pm.menuItem(label="sx")
        pm.menuItem(label="sy")
        pm.menuItem(label="sz")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=2)
        pm.text(l='����',h=25)
        pm.textFieldGrp(text='1', cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20,cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))
        pm.textFieldGrp(text='1', h=20, cw2=(0, 30), l=(''))

        pm.setParent('..')
        pm.setParent('..')

        pm.setParent('..')
        pm.showWindow()
        #�����ı�
    def jztxt(self,TextName):
        Select = pm.ls(sl=1)
        for i in range(0, len(Select) - 1):
            Select[i] = (Select[i] + ',')
        for i in range(1, len(Select)):
            Select[0] = (Select[0] + Select[i])
        pm.textFieldButtonGrp(TextName, e=1, tx=Select[0])
    #��������
    def jzsx(self,TextName):
        QvDongYvan = pm.ls(sl=1)#��ȡ����Դ
        LianJieYvan = pm.channelBox('mainChannelBox', q=1, sma=1)#��ȡ��������
        pm.textFieldButtonGrp(TextName, e=1, tx=(QvDongYvan[0] + '.' + LianJieYvan[0]))
    #������ֵ
    def AddNumbers(self,Soure, Text):
        OldNumber = float(pm.textFieldGrp(Soure, q=1, text=1))
        NewNumber = float(pm.textField(Text, q=1, text=1))
        pm.textFieldGrp(Soure, text=(OldNumber + NewNumber), e=1)

    #��ȡ�����򶯻��ڵ��Ӧ��ֵ�ĸ�����ֵ������ָ�룩#����������ڲ���
    #ReadDriveAnimationNum(Source, SourceNumber)
    def ReadDriveAnimationNum(self,Source, SourceNumber):
        floatChange = pm.keyframe(Source, q=1, floatChange=1)
        valueChange = pm.keyframe(Source, q=1, valueChange=1)
        inAngle = pm.keyTangent(Source, q=1, inAngle=1)
        inWeight = pm.keyTangent(Source, q=1, inWeight=1)
        outAngle = pm.keyTangent(Source, q=1, outAngle=1)
        outWeight = pm.keyTangent(Source, q=1, outWeight=1)
        print valueChange
    #�����붯��ƫ��
    def DriveAnimationDeviation(self):
        TextFieldJZDHJD = str(pm.textFieldButtonGrp('JZDHJD', q=1, text=1))#��ȡ�ı�
        TextFieldData = []
        numTokens = TextFieldData = TextFieldJZDHJD.split(',')#��ȡ�ڵ�
        TextFieldPYSLTransverse = float(pm.textFieldGrp('PYSLTransverse', q=1, text=1))#��ȡ����ƫ����ֵ
        TextFieldPYSLPortrait = float(pm.textFieldGrp('PYSLPortrait', q=1, text=1))#��ȡ����ƫ����ֵ
        pm.keyTangent(lock=False)#���ָ������
        pm.keyTangent(edit=1, weightedTangents=True)#���ָ��Ȩ������
        for i in TextFieldData:
            #��ȡָ��
            AnimationNodeType = []
            AnimationNodeTRSV = ['TL', 'TA', 'TU']
            for TRSA in range(0, len(AnimationNodeTRSV)):
                AnimationNodeTRSVLS = pm.ls(i, type=('animCurve' + AnimationNodeTRSV[TRSA]))
                Str = ''
                Str = AnimationNodeTRSVLS[0]
                AnimationNodeType[0] = AnimationNodeTRSVLS[0]
                if len(Str) >= 1:
                    break
            DriveNodeType = pm.ls(i, type='animCurveUL')#��ȡ�����ڵ�
            #��ѯ�ؼ�֡
            AorD = 0
            if len(AnimationNodeType) >= 1:
                AorD = 1
            if len(DriveNodeType) >= 1:
                AorD = 1
            if AorD == 0:
                pm.mel.error('������������߶����ڵ�')
            if len(AnimationNodeType) >= 1:
                pm.keyframe(i, valueChange=TextFieldPYSLPortrait, timeChange=TextFieldPYSLTransverse, r=1)
            if len(DriveNodeType) >= 1:
                pm.keyframe(i, valueChange=TextFieldPYSLPortrait, floatChange=TextFieldPYSLTransverse, r=1)
    #�������߶�������ת��
    def DriveAnimationDeviationTransformation(self):
            TextFieldJZDHJD = str(pm.textFieldButtonGrp('JZDHJD', q=1, text=1))#��ȡ�ı�
            TextFieldData = []
            numTokens = TextFieldData = TextFieldJZDHJD.split(',')#��ȡ�ڵ�i=0
            pm.keyTangent(lock=False)#���ָ������
            pm.keyTangent(edit=1, weightedTangents=True)#���ָ��Ȩ������
            for i in TextFieldData:#i=TextFieldData
                #��ȡָ��
                AnimationNodeType = []
                AnimationNodeTRSV = ['TL', 'TA', 'TU']
                for TRSA in range(0, len(AnimationNodeTRSV)):
                    AnimationNodeTRSVLS = pm.ls(i, type=('animCurve' + AnimationNodeTRSV[TRSA]))
                    Str = ''
                    Str = AnimationNodeTRSVLS[0]
                    AnimationNodeType[0] = AnimationNodeTRSVLS[0]
                    if len(Str) >= 1:
                        break
                DriveNodeType = pm.ls(i, type='animCurveUL')#��ȡ�����ڵ�
                #��ѯ�ؼ�֡
                timeChange = []
                valueChange = []
                floatChange = []
                AorD = 0
                if len(AnimationNodeType) >= 1:
                    timeChangeLS = pm.keyframe(i, q=1, timeChange=1)#��ȡʱ����
                    timeChange = timeChangeLS
                    valueChangeLS = pm.keyframe(i, q=1, valueChange=1)#��ȡ���ʱ�����ϵ���ֵ
                    valueChange = valueChangeLS
                    AorD = 1
                if len(DriveNodeType) >= 1:
                    floatChangeLS = pm.keyframe(i, q=1, fc=1)#��ȡʱ����
                    floatChange = floatChangeLS
                    valueChangeLS = pm.keyframe(i, q=1, vc=1)#��ȡ���ʱ�����ϵ���ֵ
                    valueChange = valueChangeLS
                    AorD = 1
                if AorD == 0:
                    pm.mel.error('������������߶����ڵ�')
                inAngle = pm.keyTangent(i, q=1, inAngle=1)#��ȡ���ʱ����ǰָ��λ��
                inWeight = pm.keyTangent(i, q=1, inWeight=1)#��ȡ���ʱ����ǰָ��Ȩ��
                outAngle = pm.keyTangent(i, q=1, outAngle=1)#��ȡ���ʱ�����ָ��λ��
                outWeight = pm.keyTangent(i, q=1, outWeight=1)#��ȡ���ʱ�����ָ��Ȩ��
                Source = str(pm.connectionInfo((i + '.input'),sfd=1))#��ȡԴ
                Target = pm.connectionInfo((i + '.output'),dfs=1)#��ȡĿ��
                if len(AnimationNodeType) >= 1:
                    # ��ѯĿ�꣬�жϴ����ڵ�����
                    AttributeName=Target.split('.')
                    if (AttributeName[1]=='translate'):
                        pm.createNode('animCurveTL',n=(i+'_'+AttributeName[-1]))
                    if (AttributeName[1]=='rotate'):
                        pm.createNode('animCurveTA',n='aaa')
                    if (AttributeName[1]!='translate' and AttributeName[1]!='rotate'):
                        pm.createNode('animCurveTU',n='aaa')
                    #�����ؼ�֡��������
                    pm.shadingNode('plusMinusAverage', asUtility=1, n='DriveKeyframeLinkProxy')
                    pm.addAttr('DriveKeyframeLinkProxy', ln='Soure', dv=0, at='double')
                    pm.setAttr('DriveKeyframeLinkProxy.Soure', e=1, keyable=True)
                    pm.addAttr('DriveKeyframeLinkProxy', ln='Target', dv=0, at='double')
                    pm.setAttr('DriveKeyframeLinkProxy.Target', e=1, keyable=True)
                    pm.createNode('animCurveUL', n=(i + '_CopyNode'))
                    pm.connectAttr('DriveKeyframeLinkProxy.Soure',(i + '_CopyNode.input'),f=1)
                    pm.connectAttr((i + '_CopyNode.output'),'DriveKeyframeLinkProxy.Target', f=1)
                    #�����ؼ�֡
                    for k in range(0, len(timeChange)):
                        pm.setAttr('DriveKeyframeLinkProxy.Soure', timeChange[k])
                        pm.setDrivenKeyframe('DriveKeyframeLinkProxy.Target', currentDriver='DriveKeyframeLinkProxy.Soure')
                    #����ָ��
                    for j in range(0, len(timeChange)):
                        value = valueChange[j]
                        pm.keyframe((i + '_CopyNode'),
                                    index=j, vc=value, e=1)
                        pm.keyTangent((i+ '_CopyNode'),
                                      a=1, index=j, e=1, outWeight=outWeight[j], inWeight=inWeight[j], inAngle=inAngle[j],
                                      outAngle=outAngle[j])
                    pm.connectAttr((i + "_CopyNode.output"),Target, f=1)
                    if len(Source) > 0:
                        pm.connectAttr(Source,(i + "_CopyNode.input"),f=1)
                    else:
                        pm.connectAttr("time1.outTime",(i + "_CopyNode.input"),f=1)
                    pm.delete("DriveKeyframeLinkProxy")
                    pm.delete(i)


    #���������ڵ��붯���ڵ㸴�Ʋ����ӵ�Ŀ��
    def CopyAndLinkTarget(self):
        pass
ZKM_DriveAnimationConversionWindowClass().WindowPLXGDH()