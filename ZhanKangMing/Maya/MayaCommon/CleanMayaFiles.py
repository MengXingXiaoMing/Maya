#coding=gbk
import pymel.core as pm
class ZKM_CleanMayaFilesClass:
    # 删除无影响驱动
    # ZKM_CleanMayaFilesClass().ZKM_DeleteNoImpactDrive()
    def ZKM_DeleteNoImpactDrive(self):
        for Type in ['animCurveUL','animCurveUA','animCurveUU']:
            Sel = pm.ls(type=Type)
            for sel in Sel:
                DeleteUL = 0
                floatChangeLS = pm.keyframe(sel, q=1, fc=1)  # 逐个获取时间轴
                valueChangeLS = pm.keyframe(sel, q=1, vc=1)  # 逐个获取时间轴上的数值
                inAngle = pm.keyTangent(sel, q=1, inAngle=1)  # 逐个获取前指针位置
                outAngle = pm.keyTangent(sel, q=1, outAngle=1)  # 逐个获取后指针位置
                inWeight = pm.keyTangent(sel, q=1, inWeight=1)  # 逐个获取前指针权重
                outWeight = pm.keyTangent(sel, q=1, outWeight=1)  # 逐个获取后指针权重
                if len(floatChangeLS) > 1:  # 判断是否至少有两个数
                    for Num in valueChangeLS:
                        VAL = valueChangeLS
                        VAL.remove(Num)  # 此次移除后是直接改变原来的元组
                        for num in VAL:  # 判断每一个数在其他数中是否有不同
                            if Num == num:
                                DeleteUL = 1
                            else:
                                DeleteUL = 0
                                break
                        if DeleteUL == 1:  # 如果所有都相同的话再判断指针是否有区别
                            AllAngle = inAngle + outAngle
                            AllWeight = inWeight + outWeight
                            for i in range(0, len(AllAngle)):  # 判断数是否为零，直到有个不为零跳出
                                if AllAngle[i] == 0 or AllWeight[i] == 0:
                                    continue
                                else:
                                    DeleteUL = 0
                                    break
                        if DeleteUL == 1:
                            break
                    if DeleteUL == 1:
                        pm.delete(sel)
                else:
                    pm.delete(sel)

    # 删除无影响中间帧（驱动和动画节点都可，看填写的类型）
    # ZKM_CleanMayaFilesClass().ZKM_ClearDriveInvalidIntermediateFrame(['animCurveUU','animCurveTU'])
    def ZKM_ClearDriveInvalidIntermediateFrame(self, Type):
        for type in Type:
            Sel = pm.ls(type=type)
            for sel in Sel:
                floatChangeLS = []
                if type in ['animCurveUL', 'animCurveUU']:
                    floatChangeLS = pm.keyframe(sel, q=1, fc=1)  # 逐个获取时间轴
                if type in ['animCurveTL', 'animCurveTA', 'animCurveTU']:
                    floatChangeLS = pm.keyframe(sel, q=1, timeChange=1)
                valueChangeLS = pm.keyframe(sel, q=1, vc=1)  # 逐个获取时间轴上的数值
                inAngle = pm.keyTangent(sel, q=1, inAngle=1)  # 逐个获取前指针位置
                outAngle = pm.keyTangent(sel, q=1, outAngle=1)  # 逐个获取后指针位置
                inWeight = pm.keyTangent(sel, q=1, inWeight=1)  # 逐个获取前指针权重
                outWeight = pm.keyTangent(sel, q=1, outWeight=1)  # 逐个获取后指针权重
                # 创建空列表，将相关的转换为字典添加到列表中
                AllDictionaryGrp = []
                if len(floatChangeLS) > 1:
                    for i in range(0, len(floatChangeLS)):
                        Dictionary = {'floatChangeLS': floatChangeLS[i],
                                      'valueChangeLS': valueChangeLS[i],
                                      'inAngle': inAngle[i],
                                      'outAngle': outAngle[i],
                                      'inWeight': inWeight[i],
                                      'outWeight': outWeight[i]}
                        AllDictionaryGrp.append(Dictionary)
                else:
                    pm.delete(sel)
                DEL = []
                # 开始删除无效中间帧
                if len(AllDictionaryGrp) > 2:
                    for j in range(1, (len(AllDictionaryGrp) - 1)):
                        # 开始循环判断是否再相邻两点构建的切线上
                        # 先创建一个驱动代理
                        pm.select(sel)
                        pm.duplicate(rr=1)
                        CopySel = pm.ls(sl=1)
                        # 获取需要处理的位置
                        FloatChangeLSNum = AllDictionaryGrp[j].get('floatChangeLS')
                        if type in ['animCurveUL', 'animCurveUU']:
                            # 剪切掉需要测量的点
                            pm.mel.eval('cutKey - float \"' + str(AllDictionaryGrp[j].get('floatChangeLS')) + ':' + str(
                                AllDictionaryGrp[j].get('floatChangeLS')) + '\" - clear;')
                            # 创建需要测量的点
                            pm.mel.eval(
                                'setKeyframe -insert -breakdown true -float ' + str(FloatChangeLSNum) + ' ' + CopySel[
                                    0] + ' ;')
                        if type in ['animCurveTL', 'animCurveTA', 'animCurveTU']:
                            # 剪切掉需要测量的点
                            pm.mel.eval('cutKey - time \"' + str(AllDictionaryGrp[j].get('floatChangeLS')) + ':' + str(
                                AllDictionaryGrp[j].get('floatChangeLS')) + '\" - clear;')
                            # 创建需要测量的点
                            pm.mel.eval(
                                'setKeyframe -insert -breakdown true -time ' + str(FloatChangeLSNum) + ' ' + CopySel[
                                    0] + ' ;')
                        # 查询创建的中间帧所有数据
                        CopySelvalueChangeLS = pm.keyframe(CopySel, q=1, vc=1)  # 逐个获取时间轴上的数值
                        CopySelinAngle = pm.keyTangent(CopySel, q=1, inAngle=1)  # 逐个获取前指针位置
                        CopySeloutAngle = pm.keyTangent(CopySel, q=1, outAngle=1)  # 逐个获取后指针位置
                        CopySelinWeight = pm.keyTangent(CopySel, q=1, inWeight=1)  # 逐个获取前指针权重
                        CopySeloutWeight = pm.keyTangent(CopySel, q=1, outWeight=1)  # 逐个获取后指针权重
                        # 将所有数据放入字典中，然后和原来的做对比
                        CopySelDictionary = {'CopySelvalueChangeLS': CopySelvalueChangeLS[j],
                                             'CopySelinAngle': CopySelinAngle[j],
                                             'CopySeloutAngle': CopySeloutAngle[j],
                                             'CopySelinWeight': CopySelinWeight[j],
                                             'CopySeloutWeight': CopySeloutWeight[j]}
                        # 开始对比纵向数值是否一致
                        if abs(AllDictionaryGrp[j].get('valueChangeLS') - CopySelDictionary.get(
                                'CopySelvalueChangeLS')) < 0.001:
                            # 开始对比前指针数值是否一致
                            if abs(AllDictionaryGrp[j].get('inAngle') - CopySelDictionary.get(
                                    'CopySelinAngle')) < 0.001:
                                # 开始对比后指针是否一致
                                if abs(AllDictionaryGrp[j].get('outAngle') - CopySelDictionary.get(
                                        'CopySeloutAngle')) < 0.001:
                                    # 开始判断前指针权重是否一致
                                    if abs(AllDictionaryGrp[j].get('inWeight') - CopySelDictionary.get(
                                            'CopySelinWeight')) < 0.001:
                                        # 开始判断后指针权重是否一致
                                        if abs(AllDictionaryGrp[j].get('outWeight') - CopySelDictionary.get(
                                                'CopySeloutWeight')) < 0.001:
                                            N = str(AllDictionaryGrp[j].get('floatChangeLS'))
                                            DEL.append(N)
                        pm.delete(CopySel)
                    for N in DEL:
                        pm.select(sel)
                        if type in ['animCurveUL', 'animCurveUU']:
                            pm.mel.eval('cutKey - float \"' + N + ':' + N + '\" - clear;')
                        if type in ['animCurveTL', 'animCurveTA', 'animCurveTU']:
                            pm.mel.eval('cutKey - time \"' + N + ':' + N + '\" - clear;')
#end