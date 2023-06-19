#coding=gbk
import pymel.core as pm
class ZKM_CleanMayaFilesClass:
    # ɾ����Ӱ������
    # ZKM_CleanMayaFilesClass().ZKM_DeleteNoImpactDrive()
    def ZKM_DeleteNoImpactDrive(self):
        for Type in ['animCurveUL','animCurveUA','animCurveUU']:
            Sel = pm.ls(type=Type)
            for sel in Sel:
                DeleteUL = 0
                floatChangeLS = pm.keyframe(sel, q=1, fc=1)  # �����ȡʱ����
                valueChangeLS = pm.keyframe(sel, q=1, vc=1)  # �����ȡʱ�����ϵ���ֵ
                inAngle = pm.keyTangent(sel, q=1, inAngle=1)  # �����ȡǰָ��λ��
                outAngle = pm.keyTangent(sel, q=1, outAngle=1)  # �����ȡ��ָ��λ��
                inWeight = pm.keyTangent(sel, q=1, inWeight=1)  # �����ȡǰָ��Ȩ��
                outWeight = pm.keyTangent(sel, q=1, outWeight=1)  # �����ȡ��ָ��Ȩ��
                if len(floatChangeLS) > 1:  # �ж��Ƿ�������������
                    for Num in valueChangeLS:
                        VAL = valueChangeLS
                        VAL.remove(Num)  # �˴��Ƴ�����ֱ�Ӹı�ԭ����Ԫ��
                        for num in VAL:  # �ж�ÿһ���������������Ƿ��в�ͬ
                            if Num == num:
                                DeleteUL = 1
                            else:
                                DeleteUL = 0
                                break
                        if DeleteUL == 1:  # ������ж���ͬ�Ļ����ж�ָ���Ƿ�������
                            AllAngle = inAngle + outAngle
                            AllWeight = inWeight + outWeight
                            for i in range(0, len(AllAngle)):  # �ж����Ƿ�Ϊ�㣬ֱ���и���Ϊ������
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

    # ɾ����Ӱ���м�֡�������Ͷ����ڵ㶼�ɣ�����д�����ͣ�
    # ZKM_CleanMayaFilesClass().ZKM_ClearDriveInvalidIntermediateFrame(['animCurveUU','animCurveTU'])
    def ZKM_ClearDriveInvalidIntermediateFrame(self, Type):
        for type in Type:
            Sel = pm.ls(type=type)
            for sel in Sel:
                floatChangeLS = []
                if type in ['animCurveUL', 'animCurveUU']:
                    floatChangeLS = pm.keyframe(sel, q=1, fc=1)  # �����ȡʱ����
                if type in ['animCurveTL', 'animCurveTA', 'animCurveTU']:
                    floatChangeLS = pm.keyframe(sel, q=1, timeChange=1)
                valueChangeLS = pm.keyframe(sel, q=1, vc=1)  # �����ȡʱ�����ϵ���ֵ
                inAngle = pm.keyTangent(sel, q=1, inAngle=1)  # �����ȡǰָ��λ��
                outAngle = pm.keyTangent(sel, q=1, outAngle=1)  # �����ȡ��ָ��λ��
                inWeight = pm.keyTangent(sel, q=1, inWeight=1)  # �����ȡǰָ��Ȩ��
                outWeight = pm.keyTangent(sel, q=1, outWeight=1)  # �����ȡ��ָ��Ȩ��
                # �������б�����ص�ת��Ϊ�ֵ���ӵ��б���
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
                # ��ʼɾ����Ч�м�֡
                if len(AllDictionaryGrp) > 2:
                    for j in range(1, (len(AllDictionaryGrp) - 1)):
                        # ��ʼѭ���ж��Ƿ����������㹹����������
                        # �ȴ���һ����������
                        pm.select(sel)
                        pm.duplicate(rr=1)
                        CopySel = pm.ls(sl=1)
                        # ��ȡ��Ҫ�����λ��
                        FloatChangeLSNum = AllDictionaryGrp[j].get('floatChangeLS')
                        if type in ['animCurveUL', 'animCurveUU']:
                            # ���е���Ҫ�����ĵ�
                            pm.mel.eval('cutKey - float \"' + str(AllDictionaryGrp[j].get('floatChangeLS')) + ':' + str(
                                AllDictionaryGrp[j].get('floatChangeLS')) + '\" - clear;')
                            # ������Ҫ�����ĵ�
                            pm.mel.eval(
                                'setKeyframe -insert -breakdown true -float ' + str(FloatChangeLSNum) + ' ' + CopySel[
                                    0] + ' ;')
                        if type in ['animCurveTL', 'animCurveTA', 'animCurveTU']:
                            # ���е���Ҫ�����ĵ�
                            pm.mel.eval('cutKey - time \"' + str(AllDictionaryGrp[j].get('floatChangeLS')) + ':' + str(
                                AllDictionaryGrp[j].get('floatChangeLS')) + '\" - clear;')
                            # ������Ҫ�����ĵ�
                            pm.mel.eval(
                                'setKeyframe -insert -breakdown true -time ' + str(FloatChangeLSNum) + ' ' + CopySel[
                                    0] + ' ;')
                        # ��ѯ�������м�֡��������
                        CopySelvalueChangeLS = pm.keyframe(CopySel, q=1, vc=1)  # �����ȡʱ�����ϵ���ֵ
                        CopySelinAngle = pm.keyTangent(CopySel, q=1, inAngle=1)  # �����ȡǰָ��λ��
                        CopySeloutAngle = pm.keyTangent(CopySel, q=1, outAngle=1)  # �����ȡ��ָ��λ��
                        CopySelinWeight = pm.keyTangent(CopySel, q=1, inWeight=1)  # �����ȡǰָ��Ȩ��
                        CopySeloutWeight = pm.keyTangent(CopySel, q=1, outWeight=1)  # �����ȡ��ָ��Ȩ��
                        # ���������ݷ����ֵ��У�Ȼ���ԭ�������Ա�
                        CopySelDictionary = {'CopySelvalueChangeLS': CopySelvalueChangeLS[j],
                                             'CopySelinAngle': CopySelinAngle[j],
                                             'CopySeloutAngle': CopySeloutAngle[j],
                                             'CopySelinWeight': CopySelinWeight[j],
                                             'CopySeloutWeight': CopySeloutWeight[j]}
                        # ��ʼ�Ա�������ֵ�Ƿ�һ��
                        if abs(AllDictionaryGrp[j].get('valueChangeLS') - CopySelDictionary.get(
                                'CopySelvalueChangeLS')) < 0.001:
                            # ��ʼ�Ա�ǰָ����ֵ�Ƿ�һ��
                            if abs(AllDictionaryGrp[j].get('inAngle') - CopySelDictionary.get(
                                    'CopySelinAngle')) < 0.001:
                                # ��ʼ�ԱȺ�ָ���Ƿ�һ��
                                if abs(AllDictionaryGrp[j].get('outAngle') - CopySelDictionary.get(
                                        'CopySeloutAngle')) < 0.001:
                                    # ��ʼ�ж�ǰָ��Ȩ���Ƿ�һ��
                                    if abs(AllDictionaryGrp[j].get('inWeight') - CopySelDictionary.get(
                                            'CopySelinWeight')) < 0.001:
                                        # ��ʼ�жϺ�ָ��Ȩ���Ƿ�һ��
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