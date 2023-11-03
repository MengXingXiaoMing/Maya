#coding=gbk
import pymel.core as pm
import maya.cmds as cmds
class ZKM_DriveAnimationConversionWindowClass:
    def WindowPLXGDH(self):
        if pm.window('DriveAnimationConversionWindow', ex=1):
            pm.deleteUI('DriveAnimationConversionWindow')
        pm.window('DriveAnimationConversionWindow', t='批量修改动画')
        pm.columnLayout(w=325)
        pm.rowColumnLayout(nc=1, adj=4)
        pm.button(l='打开图形编辑器', c='cmds.GraphEditor()',bgc=(0.2,0.5,0.7))
        pm.rowColumnLayout(nc=1, adj=1,w=10)
        pm.textFieldButtonGrp('JZDHJD', bl='加载驱动/动画节点', text='', cw3=(70, 145,  0), l=('驱动/动画节点'),bc='ZKM_DriveAnimationConversionWindowClass().jztxt(\'JZDHJD\')')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=2)
        pm.rowColumnLayout(nc=2, adj=2)
        pm.textFieldGrp('PYSLTransverse', text='0', cw2=(50, 40), l=('横向偏移:'))
        pm.textFieldButtonGrp(bl='添加', text='90',l=(''), cw3=(0, 80, 0),bc='ZKM_DriveAnimationConversionWindowClass().AddNumbers(\'PYSLTransverse\', \'AddNumbersTransverseText\')')
        pm.textFieldGrp('PYSLPortrait', text='0', cw2=(50, 40), l=('纵向偏移:'))
        pm.textFieldButtonGrp('AddNumbersPortraitText', bl='添加', text='90',l=(''), cw3=(0, 80, 0),bc='ZKM_DriveAnimationConversionWindowClass().AddNumbers(\'PYSLPortrait\', \'AddNumbersPortraitText\')')
        pm.setParent('..')
        pm.button(c='ZKM_DriveAnimationConversionWindowClass().DriveAnimationDeviation()', l='偏移')
        pm.setParent('..')
        pm.separator(style="in", height=10)
        pm.button(c='ZKM_DriveAnimationConversionWindowClass().DriveAnimationDeviationTransformation()', l='》》驱动节点《《——替换——》》动画节点《《')
        pm.separator(style="in", height=10)
        pm.button(c='ZKM_DriveAnimationConversionWindowClass().CopyAndLinkTarget()', l='驱动/动画节点转移链接(源空则保留,目标有则覆盖)')
        pm.textFieldButtonGrp('JZLJY', bl='加载', text='', cw3=(50, 230, 60), l=('链接源:'), bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJY\')')
        pm.textFieldButtonGrp('JZLJMB', bl='加载', text='', cw3=(50, 230, 60), l=('链接目标:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.separator(style="in", height=10)
        pm.rowColumnLayout(nc=1, adj=1)
        pm.text(l='驱动镜像')
        pm.rowColumnLayout(nc=3, adj=1)

        pm.rowColumnLayout(nc=1, adj=1)
        pm.textFieldButtonGrp('JZLJMBsd', bl='加载', text='', cw3=(35, 55, 0), l=('控制源:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.textFieldButtonGrp('JZLJMB', bl='加载', text='', cw3=(35, 55, 0), l=('驱动源:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
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
        pm.textFieldButtonGrp('JZLJMBsd', bl='加载', text='', cw3=(50, 55, 0), l=('源转移到:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
        pm.textFieldButtonGrp('JZLJMB', bl='加载', text='', cw3=(50, 55, 0), l=('复制目标:'),bc='ZKM_DriveAnimationConversionWindowClass().jzsx(\'JZLJMB\')')
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
        pm.text(l='倍率',h=25)
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
        #加载文本
    def jztxt(self,TextName):
        Select = pm.ls(sl=1)
        for i in range(0, len(Select) - 1):
            Select[i] = (Select[i] + ',')
        for i in range(1, len(Select)):
            Select[0] = (Select[0] + Select[i])
        pm.textFieldButtonGrp(TextName, e=1, tx=Select[0])
    #加载属性
    def jzsx(self,TextName):
        QvDongYvan = pm.ls(sl=1)#获取控制源
        LianJieYvan = pm.channelBox('mainChannelBox', q=1, sma=1)#获取控制轴向
        pm.textFieldButtonGrp(TextName, e=1, tx=(QvDongYvan[0] + '.' + LianJieYvan[0]))
    #增减数值
    def AddNumbers(self,Soure, Text):
        OldNumber = float(pm.textFieldGrp(Soure, q=1, text=1))
        NewNumber = float(pm.textField(Text, q=1, text=1))
        pm.textFieldGrp(Soure, text=(OldNumber + NewNumber), e=1)

    #读取驱动或动画节点对应数值的各项数值（包括指针）#此命令仅用于测试
    #ReadDriveAnimationNum(Source, SourceNumber)
    def ReadDriveAnimationNum(self,Source, SourceNumber):
        floatChange = pm.keyframe(Source, q=1, floatChange=1)
        valueChange = pm.keyframe(Source, q=1, valueChange=1)
        inAngle = pm.keyTangent(Source, q=1, inAngle=1)
        inWeight = pm.keyTangent(Source, q=1, inWeight=1)
        outAngle = pm.keyTangent(Source, q=1, outAngle=1)
        outWeight = pm.keyTangent(Source, q=1, outWeight=1)
        print valueChange
    #驱动与动画偏移
    def DriveAnimationDeviation(self):
        TextFieldJZDHJD = str(pm.textFieldButtonGrp('JZDHJD', q=1, text=1))#获取文本
        TextFieldData = []
        numTokens = TextFieldData = TextFieldJZDHJD.split(',')#获取节点
        TextFieldPYSLTransverse = float(pm.textFieldGrp('PYSLTransverse', q=1, text=1))#获取横向偏移数值
        TextFieldPYSLPortrait = float(pm.textFieldGrp('PYSLPortrait', q=1, text=1))#获取纵向偏移数值
        pm.keyTangent(lock=False)#解除指针锁定
        pm.keyTangent(edit=1, weightedTangents=True)#解除指针权重锁定
        for i in TextFieldData:
            #读取指针
            AnimationNodeType = []
            AnimationNodeTRSV = ['TL', 'TA', 'TU']
            for TRSA in range(0, len(AnimationNodeTRSV)):
                AnimationNodeTRSVLS = pm.ls(i, type=('animCurve' + AnimationNodeTRSV[TRSA]))
                Str = ''
                Str = AnimationNodeTRSVLS[0]
                AnimationNodeType[0] = AnimationNodeTRSVLS[0]
                if len(Str) >= 1:
                    break
            DriveNodeType = pm.ls(i, type='animCurveUL')#获取驱动节点
            #查询关键帧
            AorD = 0
            if len(AnimationNodeType) >= 1:
                AorD = 1
            if len(DriveNodeType) >= 1:
                AorD = 1
            if AorD == 0:
                pm.mel.error('请加载驱动或者动画节点')
            if len(AnimationNodeType) >= 1:
                pm.keyframe(i, valueChange=TextFieldPYSLPortrait, timeChange=TextFieldPYSLTransverse, r=1)
            if len(DriveNodeType) >= 1:
                pm.keyframe(i, valueChange=TextFieldPYSLPortrait, floatChange=TextFieldPYSLTransverse, r=1)
    #驱动或者动画互相转换
    def DriveAnimationDeviationTransformation(self):
            TextFieldJZDHJD = str(pm.textFieldButtonGrp('JZDHJD', q=1, text=1))#获取文本
            TextFieldData = []
            numTokens = TextFieldData = TextFieldJZDHJD.split(',')#获取节点i=0
            pm.keyTangent(lock=False)#解除指针锁定
            pm.keyTangent(edit=1, weightedTangents=True)#解除指针权重锁定
            for i in TextFieldData:#i=TextFieldData
                #读取指针
                AnimationNodeType = []
                AnimationNodeTRSV = ['TL', 'TA', 'TU']
                for TRSA in range(0, len(AnimationNodeTRSV)):
                    AnimationNodeTRSVLS = pm.ls(i, type=('animCurve' + AnimationNodeTRSV[TRSA]))
                    Str = ''
                    Str = AnimationNodeTRSVLS[0]
                    AnimationNodeType[0] = AnimationNodeTRSVLS[0]
                    if len(Str) >= 1:
                        break
                DriveNodeType = pm.ls(i, type='animCurveUL')#获取驱动节点
                #查询关键帧
                timeChange = []
                valueChange = []
                floatChange = []
                AorD = 0
                if len(AnimationNodeType) >= 1:
                    timeChangeLS = pm.keyframe(i, q=1, timeChange=1)#获取时间轴
                    timeChange = timeChangeLS
                    valueChangeLS = pm.keyframe(i, q=1, valueChange=1)#获取逐个时间轴上的数值
                    valueChange = valueChangeLS
                    AorD = 1
                if len(DriveNodeType) >= 1:
                    floatChangeLS = pm.keyframe(i, q=1, fc=1)#获取时间轴
                    floatChange = floatChangeLS
                    valueChangeLS = pm.keyframe(i, q=1, vc=1)#获取逐个时间轴上的数值
                    valueChange = valueChangeLS
                    AorD = 1
                if AorD == 0:
                    pm.mel.error('请加载驱动或者动画节点')
                inAngle = pm.keyTangent(i, q=1, inAngle=1)#获取逐个时间轴前指针位置
                inWeight = pm.keyTangent(i, q=1, inWeight=1)#获取逐个时间轴前指针权重
                outAngle = pm.keyTangent(i, q=1, outAngle=1)#获取逐个时间轴后指针位置
                outWeight = pm.keyTangent(i, q=1, outWeight=1)#获取逐个时间轴后指针权重
                Source = str(pm.connectionInfo((i + '.input'),sfd=1))#获取源
                Target = pm.connectionInfo((i + '.output'),dfs=1)#获取目标
                if len(AnimationNodeType) >= 1:
                    # 查询目标，判断创建节点类型
                    AttributeName=Target.split('.')
                    if (AttributeName[1]=='translate'):
                        pm.createNode('animCurveTL',n=(i+'_'+AttributeName[-1]))
                    if (AttributeName[1]=='rotate'):
                        pm.createNode('animCurveTA',n='aaa')
                    if (AttributeName[1]!='translate' and AttributeName[1]!='rotate'):
                        pm.createNode('animCurveTU',n='aaa')
                    #创建关键帧代理链接
                    pm.shadingNode('plusMinusAverage', asUtility=1, n='DriveKeyframeLinkProxy')
                    pm.addAttr('DriveKeyframeLinkProxy', ln='Soure', dv=0, at='double')
                    pm.setAttr('DriveKeyframeLinkProxy.Soure', e=1, keyable=True)
                    pm.addAttr('DriveKeyframeLinkProxy', ln='Target', dv=0, at='double')
                    pm.setAttr('DriveKeyframeLinkProxy.Target', e=1, keyable=True)
                    pm.createNode('animCurveUL', n=(i + '_CopyNode'))
                    pm.connectAttr('DriveKeyframeLinkProxy.Soure',(i + '_CopyNode.input'),f=1)
                    pm.connectAttr((i + '_CopyNode.output'),'DriveKeyframeLinkProxy.Target', f=1)
                    #创建关键帧
                    for k in range(0, len(timeChange)):
                        pm.setAttr('DriveKeyframeLinkProxy.Soure', timeChange[k])
                        pm.setDrivenKeyframe('DriveKeyframeLinkProxy.Target', currentDriver='DriveKeyframeLinkProxy.Soure')
                    #调整指针
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


    #拷贝驱动节点与动画节点复制并链接到目标
    def CopyAndLinkTarget(self):
        pass
ZKM_DriveAnimationConversionWindowClass().WindowPLXGDH()