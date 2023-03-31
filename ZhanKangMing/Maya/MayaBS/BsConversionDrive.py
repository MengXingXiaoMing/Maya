#coding=gbk
import pymel.core as pm
class ZKM_Bs:
    #��bsת��Ϊ���ŵĿ���������
    def ZKM_BsConvertControllerDrive(self,Controller, LoadBsName):
        # ��ȡbs�ڵ�����bs����
        BS = LoadBsName[0].split('.')[0]
        AllBsName = pm.listAttr((BS + '.w'), k=True, m=True)
        # ��ʼ��������bs
        pm.setAttr((BS + '.envelope'), 1)
        AllSAT = []
        for Attribute in AllBsName:
            Soure = pm.connectionInfo((BS + '.' + Attribute), sfd=1)
            Target = pm.connectionInfo((BS + '.' + Attribute), dfs=1)

            if Soure:
                pm.disconnectAttr(str(Soure), (BS + '.' + Attribute))
            if Target:
                for T in Target:
                    pm.disconnectAttr((BS + '.' + Attribute), str(T))

            # �����ֵ�
            SATs = {'S': Soure, 'A': (BS + '.' + Attribute), 'T': Target}
            AllSAT.append(SATs)
            # ���ֵ���ӵ��б�Ϊ�����������ӻ�ȥ��׼��
            pm.setAttr((BS + '.' + Attribute), 0)
        for Attribute in LoadBsName:
            # ��ȡ������bs�е�λ��
            num = []
            for i in range(0, len(AllBsName)):
                if (BS + '.' + AllBsName[i]) in Attribute:
                    num.append(i)
            # ��ѯ�Ƿ����м�֡
            BSIntermediateFrame = pm.ls(BS + '.inputTarget[0].inputTargetGroup' + str(num) + '.inputTargetItem[*]')
            BSIntermediateFrame = BSIntermediateFrame[:-1]
            # ����Ҫ�򵽵���ֵ
            AllKeyFrame = [0]
            if BSIntermediateFrame:
                # ��ʼ��ȡbs�м�֡������������ֵ
                for BsNameNum in BSIntermediateFrame:
                    n = float(str(BsNameNum)[-4:-1]) / 1000.0
                    AllKeyFrame.append(n)
            AllKeyFrame.append(1)
            # ��������йؼ�֡������������
            # ����������������Ӧ����
            for c in Controller:  # �������е�λ�û�ȡ
                pm.select(cl=1)
                pm.group(n=(c + '_DriveTarget_Grp2'))  # �������ùؼ�֡Ŀ��
                pm.group(n=(c + '_DriveTarget_Grp1'))  # �������ùؼ�֡Ŀ��
                pm.parent((c + '_DriveTarget_Grp1'), 'Face_Grp')
                pm.delete(pm.parentConstraint(c, (c + '_DriveTarget_Grp1'), weight=1))
                pm.delete(pm.scaleConstraint(c, (c + '_DriveTarget_Grp1'), weight=1))
                pm.select(c)
                pm.pickWalk(d='down')
                '''pm.select(c[:-2] + '2' + c[-1:])'''
                if not (pm.objExists(c.split('_')[0] + '_Drive_Grp' + c[-1:])):
                    pm.group(n=(c.split('_')[0] + '_Drive_Grp' + c[-1:]))
                if not (pm.objExists(c.split('_')[0] + '_Constraint_Grp' + c[-1:])):
                    pm.group(n=(c.split('_')[0] + '_Constraint_Grp' + c[-1:]))
                pm.parentConstraint((c.split('_')[0] + '_Constraint_Grp' + c[-1:]), (c + '_DriveTarget_Grp2'), weight=1,mo=1)
                # ��ӵ�ǰbs��������Դ
                pm.addAttr((c + '_DriveTarget_Grp2'), ln="Soure", dv=0, at='double')
                pm.setAttr((c + '_DriveTarget_Grp2.Soure'), e=1, keyable=True)
                # �Կ�����λ�ƺ���ת�����ӽڵ���л��
                for tr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    if not pm.objExists((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr)):
                        pm.shadingNode('plusMinusAverage', asUtility=1,
                                       n=(c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr))
                        pm.connectAttr((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr + '.output1D'),
                                       (c.split('_')[0] + '_Drive_Grp' + c[-1:] + '.' + tr), f=1)
                # ��ȡ������ֵ��ʼ����
                for n in AllKeyFrame:
                    pm.setAttr(Attribute, n)
                    pm.setAttr((c + '_DriveTarget_Grp2.Soure'), n)
                    for tr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                        H = len(pm.listAttr((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr), k=1, m=1))
                        if n > 0:
                            H = H - 1
                        TR = pm.getAttr((c + '_DriveTarget_Grp2.' + tr))
                        pm.setAttr((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr + '.input1D[' + str(H) + ']'),TR)
                        pm.setDrivenKeyframe((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr + '.input1D[' + str(H) + ']'),currentDriver=(c + '_DriveTarget_Grp2.Soure'))

                target = pm.connectionInfo((c + '_DriveTarget_Grp2.Soure'), dfs=1)
                for t in target:
                    pm.connectAttr(AllSAT[num[0]]['S'], t, f=1)
                    if AllSAT[num[0]]['T']:
                        pm.connectAttr(AllSAT[num[0]]['S'], AllSAT[num[0]]['T'], f=1)

                pm.setAttr(Attribute, 0)
                '''pm.select((c.split('_')[0]+'_Drive_Grp'+c[-1:]))
                pm.keyTangent('graphEditor1FromOutliner', itt='linear', animation='objects', ott='linear')'''
                pm.setAttr((c + '_DriveTarget_Grp2.Soure'), 0)
                pm.delete((c + '_DriveTarget_Grp1'))
        for c in Controller:
            if (pm.objExists(c + '_parentConstraint1')):
                pm.delete(c + '_parentConstraint1')
        # ��ԭ����
        for i in range(0, len(AllBsName)):
            for Attribute in LoadBsName:
                if (BS + '.' + AllBsName[i]) not in Attribute:
                    if AllSAT[i]['S']:
                        pm.connectAttr(AllSAT[i]['S'], AllSAT[i]['A'], f=1)
                    if AllSAT[i]['T']:
                        for t in AllSAT[i]['T']:
                            pm.connectAttr(AllSAT[i]['S'], AllSAT[i]['T'], f=1)
                else:
                    pm.connectAttr(AllSAT[i]['S'], AllSAT[i]['A'], f=1)
        pm.select(cl=1)