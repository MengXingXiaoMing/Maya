#coding=gbk
import pymel.core as pm
class ZKM_Bs:
    #将bs转化为附着的控制器驱动
    def ZKM_BsConvertControllerDrive(self,Controller, LoadBsName):
        # 获取bs节点所有bs属性
        BS = LoadBsName[0].split('.')[0]
        AllBsName = pm.listAttr((BS + '.w'), k=True, m=True)
        # 开始清理所有bs
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

            # 创建字典
            SATs = {'S': Soure, 'A': (BS + '.' + Attribute), 'T': Target}
            AllSAT.append(SATs)
            # 将字典添加到列表，为后面重新链接回去做准备
            pm.setAttr((BS + '.' + Attribute), 0)
        for Attribute in LoadBsName:
            # 获取属性在bs中的位置
            num = []
            for i in range(0, len(AllBsName)):
                if (BS + '.' + AllBsName[i]) in Attribute:
                    num.append(i)
            # 查询是否有中间帧
            BSIntermediateFrame = pm.ls(BS + '.inputTarget[0].inputTargetGroup' + str(num) + '.inputTargetItem[*]')
            BSIntermediateFrame = BSIntermediateFrame[:-1]
            # 定义要打到的数值
            AllKeyFrame = [0]
            if BSIntermediateFrame:
                # 开始获取bs中间帧的名称最后的数值
                for BsNameNum in BSIntermediateFrame:
                    n = float(str(BsNameNum)[-4:-1]) / 1000.0
                    AllKeyFrame.append(n)
            AllKeyFrame.append(1)
            # 计算出所有关键帧的驱动并关联
            # 轮流创建控制器对应驱动
            for c in Controller:  # 创建所有的位置获取
                pm.select(cl=1)
                pm.group(n=(c + '_DriveTarget_Grp2'))  # 创建设置关键帧目标
                pm.group(n=(c + '_DriveTarget_Grp1'))  # 创建设置关键帧目标
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
                # 添加当前bs属性驱动源
                pm.addAttr((c + '_DriveTarget_Grp2'), ln="Soure", dv=0, at='double')
                pm.setAttr((c + '_DriveTarget_Grp2.Soure'), e=1, keyable=True)
                # 对控制器位移和旋转创建加节点进行混合
                for tr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    if not pm.objExists((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr)):
                        pm.shadingNode('plusMinusAverage', asUtility=1,
                                       n=(c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr))
                        pm.connectAttr((c.split('_')[0] + '_Drive_Grp' + c[-1:] + '_' + tr + '.output1D'),
                                       (c.split('_')[0] + '_Drive_Grp' + c[-1:] + '.' + tr), f=1)
                # 获取具体数值开始赋予
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
        # 还原链接
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