#coding=gbk
#获取文件路径
import os
import inspect
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_path = os.path.join(cur_dir)  # 获取文件路径
cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_pathA = os.path.join(cur_dirA)  # 获取文件路径A
import pymel.core as pm
from binascii import hexlify
from maya import cmds
# pm.textCurves(t="a", f="Times-Roman")
# ZKM_AttributeVisualizationClass().AttributeVisualizationWindow()
class ZKM_AttributeVisualizationClass:
    def __init__(self):
        global Attribute
    '''def AttributeName():#修改文本
            cmds.setAttr('type1.textInput',
                ''.join([hexlify(x.encode('utf-16 be'))
                    for x in u'中文ABC！']),
                typ="string")
            #for item in student_old:
            '''
    def AttributeVisualizationWindow(self):#窗口
        if cmds.window('AttributeVisualizationWindow', ex=1):
            cmds.deleteUI('AttributeVisualizationWindow')
        cmds.window('AttributeVisualizationWindow',t="属性可视化")
        cmds.rowColumnLayout()
        # 创建按钮
        cmds.button('ReadAndCreateButton',w=300,l='选择并加载属性',c='CreateAttributeCrossReference()')
        cmds.button(w=300,l='重置',c='AttributeVisualizationWindow()')
        pm.rowColumnLayout(columnWidth=[(1, 150), (2, 1),(1, 150)], numberOfColumns=3)
        pm.text(l="属性名称", w=150)
        pm.separator(style="single")
        pm.text(l="属性变成样条后的名称", w=150)
        pm.setParent('..')
        pm.separator(style="out")
        cmds.text('SourceText',l='请选择独立控制器', bgc=(1, 1, 1))
        pm.rowColumnLayout('AttributeText')
        cmds.showWindow()
    def CreateAttributeCrossReference(self):#修改文本
        Source = cmds.ls(selection=True)
        global Attribute
        Attribute = pm.channelBox('mainChannelBox', q=1, sma=1)
        #创建对照表
        for i in Attribute:
            pm.textFieldGrp(i,cw2=(145, 145), l=i, tx=i ,parent='AttributeText')
            pm.separator(parent='AttributeText')
        cmds.button('ReadAndCreateButton',e=1,bgc=(1,1,1),l='按对应名称创建控制器',c='CreateAttributeController()')
        cmds.text('SourceText',e=1,l=Source[0])
        cmds.warning('属性对照生成完成')
    def CreateAttributeController(self):#创建控制器
        self.CreateControllerPath()#创建控制器
        self.CreateControllerTxt()#创建字符串
        self.Arrangement()#整理
    ###############################################
    def CreateControllerTxt(self):#创建控制器
        global Attribute
        self.CreateTxtCurve(Attribute)
    def CreateTxtCurve(self,TextSource):#创建文本样条
        sel = pm.textCurves(n='first', f='Courier', t='Show Controller')
        print sel

        '''for Text in TextSource:
            # 创建所需文本
            oldNodes = pm.ls()
            pm.mel.eval("CreatePolygonType;")  # 创建文本模型
            SetScale = cmds.ls(sl=1)
            pm.setAttr((SetScale[0] + '.scaleZ'), 0.08)
            pm.setAttr((SetScale[0] + '.scaleX'), 0.08)
            pm.setAttr((SetScale[0] + '.scaleY'), 0.08)
            newNodes = pm.ls()
            addNodes = [x for x in newNodes if x not in oldNodes]  # 筛选出新增的节点
            typeNode = ()
            for n in addNodes:  # 加载文本模型节点
                TextNode = pm.ls(n, type='type')
                if (not TextNode):
                    continue
                else:
                    typeNode = TextNode
                    break
                    # print(typeNode)
            # pm.select(addNodes)
            textFieldGrpOld = str(pm.textFieldGrp(Text, q=1, l=1))
            textFieldGrpNew = str(pm.textFieldGrp(Text, q=1, text=1))
            # print(textFieldGrpOld,textFieldGrpNew)
            cmds.setAttr((typeNode[0] + '.textInput'),
                         ' '.join([hexlify(x.encode('utf-16 be'))
                                   for x in (textFieldGrpNew)]),
                         typ="string")
            pm.select(SetScale[0], r=1)
            pm.mel.convertTypeCapsToCurves()  # 根据模型创建样条
            CurveTopGrp = pm.ls(sl=1)  # 开始清理生成的样条
            pm.mel.eval("SelectHierarchy;")
            CurveNode = pm.ls(sl=1, type='nurbsCurve')
            # print(CurveNode)
            pm.select(CurveNode)
            pm.pickWalk(d='up')
            CurveNodeGrp = pm.ls(sl=1)
            # print(CurveNodeGrp)
            pm.select(cl=1)
            for curve in CurveNode:
                pm.select(curve, add=1)
            pm.select(CurveTopGrp, add=1)
            pm.parent(add=1, s=1)
            pm.select(CurveNodeGrp[0])
            # pm.parent(w=1)
            pm.delete(CurveNodeGrp)
            Source = str(pm.text('SourceText', q=1, l=1))
            pm.select(CurveTopGrp)
            pm.rename(CurveTopGrp, (Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew))
            for CurveNodeName in CurveNode:  # 修改样条节点名称
                pm.rename(CurveNodeName, (Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew + 'Shape'))
            # 以上完成生成样条

            # 清理多余
            meshNode = pm.ls(addNodes, type='mesh')
            # print(meshNode)
            displayPointsNode = pm.ls(addNodes, type='displayPoints')
            # print(displayPointsNode)
            pm.select(meshNode, displayPointsNode)
            pm.pickWalk(d='up')
            deleteNode = pm.ls(sl=1)
            pm.delete(deleteNode)'''
    ####################################################
    def EnumCreateTxtCurve(self,TextSource,textFieldGrpOld):#创建Em文本样条
        # 创建所需文本
        oldNodes = pm.ls()
        pm.mel.eval("CreatePolygonType;")  # 创建文本模型
        newNodes = pm.ls()
        SetScale = cmds.ls(sl=1)
        pm.setAttr((SetScale[0] + '.scaleZ'), 0.08)
        pm.setAttr((SetScale[0] + '.scaleX'), 0.08)
        pm.setAttr((SetScale[0] + '.scaleY'), 0.08)
        addNodes = [x for x in newNodes if x not in oldNodes]  # 筛选出新增的节点
        typeNode = pm.ls(addNodes, type="type")
        cmds.setAttr((typeNode[0] + '.textInput'),
                     ' '.join([hexlify(x.encode('utf-16 be'))
                               for x in (TextSource)]),
                     typ="string")
        pm.select(SetScale[0], r=1)
        pm.mel.convertTypeCapsToCurves()  # 根据模型创建样条
        CurveTopGrp = pm.ls(sl=1)  # 开始清理生成的样条
        pm.mel.eval("SelectHierarchy;")
        CurveNode = pm.ls(sl=1, type='nurbsCurve')
        # print(CurveNode)
        pm.select(CurveNode)
        pm.pickWalk(d='up')
        CurveNodeGrp = pm.ls(sl=1)
        # print(CurveNodeGrp)
        pm.select(cl=1)
        for curve in CurveNode:
            pm.select(curve, add=1)
        pm.select(CurveTopGrp, add=1)
        pm.parent(add=1, s=1)
        pm.select(CurveNodeGrp[0])
        # pm.parent(w=1)
        pm.delete(CurveNodeGrp)
        Source = str(pm.text('SourceText', q=1, l=1))
        pm.select(CurveTopGrp)
        pm.rename(CurveTopGrp, (Source + '_' + 'Enum_' +textFieldGrpOld+ TextSource))
        for CurveNodeName in CurveNode:  # 修改样条节点名称
            pm.rename(CurveNodeName, (Source + '_' + 'Enum_' +textFieldGrpOld+ TextSource + 'Shape'))
        # 以上完成生成样条
        # 清理多余
        pm.delete(addNodes)
    def CreateControllerPath (self):#创建路径和控制器
        global Attribute
        for Text in Attribute:#Text=Attribute[0]
            oldNodes = pm.ls()
            pm.mel.performFileSilentImportAction(file_pathA + "/AttributeVisualizationNodeTemplate.mb")  # 导入文件
            newNodes = pm.ls()
            addNodes = [x for x in newNodes if x not in oldNodes]  # 筛选出新增的节点
            Source = str(pm.text('SourceText', q=1, l=1))#获取源
            textFieldGrpOld = str(pm.textFieldGrp(Text, q=1, l=1))#获取属性
            AttributeDefault = pm.attributeQuery(textFieldGrpOld, node=Source, ld=1) #获取默认值
            AttributeType = pm.attributeQuery(textFieldGrpOld, node=Source, attributeType=1)  # 获取属性类型
            AttributeMin = pm.attributeQuery(textFieldGrpOld, node=Source, minExists=1)  # 查询属性是否具有最小值
            AttributeMax = pm.attributeQuery(textFieldGrpOld, node=Source, maxExists=1)  # 查询属性是否具有最大值
            if (AttributeMin == 1):
                AttributeMin = 1
                GetAttributeMin = pm.attributeQuery(textFieldGrpOld, node=Source, min=1)  # 获取属性最大值
                GetAttributeMin =GetAttributeMin[0]
            else:
                AttributeMin = 0
                GetAttributeMin = 0
            if (AttributeMax == 1):
                AttributeMax = 1
                GetAttributeMax = pm.attributeQuery(textFieldGrpOld, node=Source, max=1)  # 获取属性最大值
                GetAttributeMax=GetAttributeMax[0]
            else:
                AttributeMax = 0
                GetAttributeMax =0

            pm.curve(p=[(-6.847494044e-16, -3.398130212e-17, 1.000234865), (-6.847494044e-16, 0.5001174326, 0.8662283992),
                        (-6.847494044e-16, 0.8662283992, 0.5001174326), (-6.847494044e-16, 1.000234865, -1.581002666e-16),
                        (-6.847494044e-16, 0.8662283992, -0.5001174326), (-6.847494044e-16, 0.5001174326, -0.8662283992),
                        (-6.847494044e-16, -3.398130212e-17, -1.000234865),
                        (-6.847494044e-16, -0.5001174326, -0.8662283992), (-6.847494044e-16, -0.8662283992, -0.5001174326),
                        (-6.847494044e-16, -1.000234865, -1.581002666e-16), (-6.847494044e-16, -0.8662283992, 0.5001174326),
                        (-6.847494044e-16, -0.5001174326, 0.8662283992), (-6.847494044e-16, -3.398130212e-17, 1.000234865),
                        (0.7072730748, -3.398130212e-17, 0.7072730748), (1.000234865, -3.398130212e-17, -1.581002666e-16),
                        (0.7072730748, -3.398130212e-17, -0.7072730748), (-6.847494044e-16, -3.398130212e-17, -1.000234865),
                        (-0.7072730748, -3.398130212e-17, -0.7072730748),
                        (-1.000234865, -3.398130212e-17, -1.581002666e-16), (-0.8662283992, 0.5001174326, -1.581002666e-16),
                        (-0.5001174326, 0.8662283992, -1.581002666e-16), (-6.847494044e-16, 1.000234865, -1.581002666e-16),
                        (0.5001174326, 0.8662283992, -1.581002666e-16), (0.8662283992, 0.5001174326, -1.581002666e-16),
                        (1.000234865, -3.398130212e-17, -1.581002666e-16), (0.8662283992, -0.5001174326, -1.581002666e-16),
                        (0.5001174326, -0.8662283992, -1.581002666e-16), (-6.847494044e-16, -1.000234865, -1.581002666e-16),
                        (-0.5001174326, -0.8662283992, -1.581002666e-16), (-0.8662283992, -0.5001174326, -1.581002666e-16),
                        (-1.000234865, -3.398130212e-17, -1.581002666e-16), (-0.7072730748, -3.398130212e-17, 0.7072730748),
                        (-6.847494044e-16, -3.398130212e-17, 1.000234865)],
                     d=1, n=(Source + '_' + textFieldGrpOld + '_Curve'))
            pm.group(n=(Source + '_' + textFieldGrpOld + '_Curve_Grp'))

            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.ty'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.tz'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.rx'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.ry'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.rz'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.sx'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.sy'),
                       lock=True, channelBox=False, keyable=False)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.sz'),
                       lock=True, channelBox=False, keyable=False)
            pm.connectAttr((Source + '_' + textFieldGrpOld + '_Curve.tx'),
                           'name_decomposeMatrix_Main.Translate', f=1)
            pm.connectAttr((Source + '_' + textFieldGrpOld + '_Curve.inverseMatrix'),
                           'name_decomposeMatrix_Main.inputMatrix', f=1)
            pm.connectAttr('name_decomposeMatrix_Main.OutTranslate',
                           (Source + '_' + textFieldGrpOld + '_Curve_Grp.tx'),
                           f=1)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.translateX'), 0)#设置默认值
            pm.mel.eval("transformLimits -tx"+" "+str(AttributeMin)+" "+str(AttributeMax)+" -etx "+str(GetAttributeMin)+" "+str(GetAttributeMax)+" "+(Source + '_' + textFieldGrpOld + '_Curve')+";")
            pm.transformLimits((Source + '_' + textFieldGrpOld + '_Curve'), etx=(AttributeMin, AttributeMax),
                               tx=(GetAttributeMin, GetAttributeMax))  # 设置最大最小值
            pm.connectAttr((Source + '_' + textFieldGrpOld + '_Curve.translateX'), (Source + '.' + textFieldGrpOld), f=1)
            Normal = pm.getAttr((Source + '.' + textFieldGrpOld), 1)  # 获取默认值
            '''if AttributeMin == 1:
                pm.disconnectAttr('name_Negative_direction_range.output1D', 'name_Negative_direction_condition.colorIfTrueR')
            if AttributeMax == 1:
                pm.disconnectAttr('name_Positive_direction_condition.outColorR', 'name_Negative_direction_condition.colorIfFalseR')'''
            # 对对应控制器进行对应的修改pm.setAttr('name_Negative_direction_condition.colorIfFalseR', 0)
            #print(AttributeType)
            #print(textFieldGrpOld+'AttributeType')

            if (AttributeType == 'double'):#浮点
                pm.group((Source + '_' + textFieldGrpOld + '_Curve_Grp'),
                         n=(Source + '_' + textFieldGrpOld + '_Curve_AllGrp'))
            if (AttributeType == 'long' or AttributeType == 'bool' or AttributeType == 'enum'):#整形#布尔#字符
                if(AttributeMin==0):
                    GetAttributeMin=-10
                if (AttributeMax == 0):
                    GetAttributeMax = 10
                pm.transformLimits((Source + '_' + textFieldGrpOld + '_Curve_Grp'), etx=(1, 1), tx=(GetAttributeMin, GetAttributeMax))

                pm.connectAttr('name_decomposeMatrix_Main.Int', (Source + '_' + textFieldGrpOld + '_Curve_Grp.translateX'), f=1)#链接到整数
                pm.select((Source + '_' + textFieldGrpOld + '_Curve'))
                pm.group(n=(Source + '_' + textFieldGrpOld + '_Curve_IntGrp'))
                pm.connectAttr('name_decomposeMatrix_Main.outputTranslateX', (Source + '_' + textFieldGrpOld + '_Curve_IntGrp.translateX'), f=1)#链接到创建的int组
                pm.addAttr((Source + '_' + textFieldGrpOld + '_Curve'), ln="int", dv=0, at='long')
                pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.int'), e=1, keyable=True)
                pm.connectAttr('name_decomposeMatrix_Main.Int', (Source + '_' + textFieldGrpOld + '_Curve.int'), f=1)#添加属性并链接
                pm.group((Source + '_' + textFieldGrpOld + '_Curve_Grp'),
                         n=(Source + '_' + textFieldGrpOld + '_Curve_AllGrp'))

            if (AttributeType == 'enum'):#字符
                EnumStr = pm.attributeQuery(textFieldGrpOld, node=Source, listEnum=1)
                EnumStr=EnumStr[0]
                pm.select(cl=1)
                pm.group(em=1,n=(Source + '_EnumText'+textFieldGrpOld+ '_Curve_Grp'))
                EnumStr = EnumStr.split(":")  # 文件名称
                for EnumText in EnumStr:
                    self.EnumCreateTxtCurve(EnumText,textFieldGrpOld)
                    pm.parent((Source + '_Enum_' +textFieldGrpOld+ EnumText), (Source + '_EnumText'+textFieldGrpOld+ '_Curve_Grp'))
                TextLong = 0
                for TrX in range(1, len(EnumStr)):
                    #trX = (trX + len(EnumStr[TrX-1]))
                    TextLong=(TextLong+len(str(EnumStr[TrX-1])))
                    pm.setAttr((Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'.translateX'), (TextLong*0.8))#设置大小
                for TrX in range(0, len(EnumStr)):
                    #调整颜色
                    pm.setAttr((Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'.overrideEnabled'), 1)#打开对应的颜色属性
                    pm.shadingNode('condition', asUtility=1, n=(Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'_condition'))#建立条件
                    pm.setAttr((Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'_condition.colorIfFalseR'), 2)#设置颜色显示
                    pm.setAttr((Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'_condition.secondTerm'), TrX)#设置值为多少时显示
                    pm.connectAttr('name_decomposeMatrix_Main.Int', (Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'_condition.firstTerm'), f=1)#链接整形
                    pm.connectAttr((Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'_condition.outColorR'), (Source + '_Enum_' +textFieldGrpOld+ EnumStr[TrX]+'.overrideDisplayType'), force=1)#链接到颜色
                pm.setAttr((Source + '_EnumText'+textFieldGrpOld+ '_Curve_Grp.translateY'), 1.5)
                pm.parent((Source + '_EnumText' +textFieldGrpOld+ '_Curve_Grp'),(Source + '_' + textFieldGrpOld + '_Curve_AllGrp'))#把额外生成的补进组里
            for rename in addNodes:
                pm.select(rename, r=1)
                pm.mel.searchReplaceNames('name', (Source + '_' + textFieldGrpOld), 'selected')
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve.translateX'), AttributeDefault[0])  # 设置默认值

        RouteMax = ()
        RouteMin = ()
        '''if (AttributeMin == 1):
            RouteMin = GetAttributeMin
        else:
            RouteMin = AttributeDefault
        if (AttributeMax == 1):
            RouteMax = GetAttributeMax
        else:
            RouteMax = AttributeDefault
        if (AttributeMin == 0 and AttributeMax == 1):#判断模式开始创建从默认值到最大值的曲线
            print('asd')
        if (AttributeMin == 1 and AttributeMax == 0):#判断模式开始创建从最小值到默认值的曲线
            print('asd')
        pm.curve(p=[(RouteMin, 0, 0), (RouteMax, 0, 0)], d=1)'''
    def Arrangement(self):  #整理
        global Attribute
        Source = str(pm.text('SourceText', q=1, l=1))  # 获取源
        for Text in Attribute:  # Text=Attribute[0]
            textFieldGrpOld = str(pm.textFieldGrp(Text, q=1, l=1))  # 获取属性
            textFieldGrpNew = str(pm.textFieldGrp(Text, q=1, text=1))
            pm.parent((Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew),(Source + '_' + textFieldGrpOld + '_Curve'))
            pm.setAttr((Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew + '.translateX'), -1)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew + '.translateY'), -2)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew + '.overrideEnabled'), 1)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew + '.overrideDisplayType'), 2)
            pm.setAttr((Source + '_' + textFieldGrpOld + '_revise_' + textFieldGrpNew + '.overrideDisplayType'), 2)
        pm.group(em=1, n=(Source + '_AttributeVisualization'))
        Ty=0
        for Text in Attribute:
            Source = str(pm.text('SourceText', q=1, l=1))  # 获取源
            textFieldGrpOld = str(pm.textFieldGrp(Text, q=1, l=1))  # 获取属性
            pm.parent((Source + '_' + textFieldGrpOld + '_Curve_AllGrp'),(Source + '_AttributeVisualization'))
            pm.setAttr((Source + '_' + textFieldGrpOld + '_Curve_AllGrp.translateY'), Ty)
            Ty = Ty+3

    #根据属性类型和范围创建控制器
    #print('A')#测试是否运行

    #for i in Attribute:
    #    pm.textFieldGrp(i,e=1,h=30)




