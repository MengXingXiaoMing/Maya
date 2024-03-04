#coding=gbk
import pymel.core as pm
from os import listdir
# 获取文件路径
import os
import inspect
import sys

ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))

# 加载文本
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *

class NewExpression:
    def __init__(self):
        cur_dir = '\\'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        cur_dirA = '/'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
        # 通过self向新建的对象中初始化属性
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
    def ZKM_Window(self):
        if pm.window('new_expression', ex=1):
            pm.deleteUI('new_expression')
        pm.window('new_expression', t='轮胎处理')
        pm.columnLayout()
        pm.rowColumnLayout(nc=1, adj=1)
        pm.button(c='NewExpression().modify_the_ADV_wheel_expression()', l='自动修改adv轮胎表达式(以6.220作为基准，其他版本可能会生成失败)')
        pm.textFieldButtonGrp('new_expression_Load_general_controller', cw2=(150, 10), bl='加载总控制器',text='',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'new_expression_Load_general_controller\')')
        pm.textFieldButtonGrp('new_expression_Load_tire_controller', cw2=(150, 10), bl='加载轮胎控制器',text='',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'new_expression_Load_tire_controller\')')
        pm.textFieldButtonGrp('new_expression_Load_tire_perimeter', cw2=(150, 10), bl='加载轮胎周长样条',text='',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'new_expression_Load_tire_perimeter\')')
        pm.textFieldButtonGrp('new_expression_Load_output_joint', cw2=(150, 10), bl='加载输出骨骼(生成后会替换其旋转关联)',text='',
                                bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\' , \'new_expression_Load_output_joint\')')
        pm.button(c='NewExpression().create_tire()', l='按加载内容创建表达式')
        pm.setParent('..')
        pm.showWindow()
    def modify_the_ADV_wheel_expression(self):
        # 获取总控制器
        general_controller = pm.ls(sl=1)
        # 获取所有表达式
        expression = pm.ls(type='expression')
        # 获取所有疑似车轮表达式的对象
        wheel = pm.ls('*WheelExpression*')
        # 筛选出轮胎表达式
        wheel_expression = list(set(expression) & set(wheel))
        # 获取表达式输出骨骼
        joint = pm.listConnections(wheel_expression,d=1,type='joint')
        # 删除adv轮胎表达式
        pm.delete(wheel_expression)
        # 获取adv其他部分的属性和对象
        # 给总样条添加属性
        pm.addAttr(general_controller, ln='tire', at='bool')
        pm.setAttr((general_controller[0]+'.tire'), e=1, channelBox=True, lock=True)
        pm.addAttr(general_controller, ln='baking_wheels', at='bool')
        pm.setAttr((general_controller[0]+'.baking_wheels'), e=1, channelBox=True)
        pm.addAttr(general_controller, ln='start_frame', dv=101, at='long')
        pm.setAttr((general_controller[0]+'.start_frame'), e=1, channelBox=True)
        pm.addAttr(general_controller, ln='expression_type', en="tradition:baking:", at="enum")
        pm.setAttr((general_controller[0]+'.expression_type'), e=1, channelBox=True)

        for j in joint:
            # 拆解出adv源骨骼的名称
            base_joint_name = j[3:]
            # 给样条添加属性
            pm.addAttr(('FK'+base_joint_name), ln='axial', en='x:y:z:', at='enum')
            pm.setAttr(('FK'+base_joint_name + '.axial'), e=1, channelBox=True)
            pm.addAttr(('FK'+base_joint_name), ln='start_num', dv=0, at='double')
            pm.setAttr(('FK'+base_joint_name + '.start_num'), e=1, keyable=True)
            pm.addAttr(('FK'+base_joint_name), ln='baking_num', dv=0, at='double')
            pm.setAttr(('FK'+base_joint_name + '.baking_num'), e=1, keyable=True)
            # 给骨骼添加属性
            pm.addAttr(('FKX'+base_joint_name), ln='tire', at='bool')
            pm.setAttr(('FKX'+base_joint_name + '.tire'), e=1, channelBox=True)
            pm.addAttr(('FKX'+base_joint_name), ln='calculate_tire_num', dv=0, at='double')
            pm.setAttr(('FKX' + base_joint_name + '.calculate_tire_num'), e=1, keyable=True)
            # 添加骨骼属性代理(代码里给此属性k帧)
            pm.addAttr(j, proxy=('FK'+base_joint_name+'.baking_num'), longName='baking_wheel')
            # 添加总控制器属性代理
            pm.addAttr(general_controller, proxy=('FK'+base_joint_name+'.baking_num'), longName=base_joint_name)
            # 建立节点关系
            pm.connectAttr((general_controller[0]+'.tire'), ('FKX'+base_joint_name+'.tire'), f=1)
            choice_node = pm.shadingNode('choice', asUtility=1)
            pm.connectAttr((general_controller[0]+'.expression_type'), (choice_node + '.selector'), f=1)
            pm.connectAttr(('FKX' + base_joint_name + '.calculate_tire_num'), (choice_node + '.input[0]'), f=1)
            pm.connectAttr(('FK'+base_joint_name+'.baking_num'), (choice_node + '.input[1]'), f=1)
            for i,axial in zip(range(0,3),['X','Y','Z']):
                plusMinusAverage_condition = pm.shadingNode('condition', asUtility=1)
                pm.connectAttr(('FK'+base_joint_name + '.axial'), (plusMinusAverage_condition + '.firstTerm'), f=1)
                pm.setAttr((plusMinusAverage_condition+'.secondTerm'),i)
                pm.setAttr((plusMinusAverage_condition + '.colorIfFalseR'), 0)
                pm.connectAttr((choice_node + '.output'), (plusMinusAverage_condition + '.colorIfTrueR'), f=1)
                pm.connectAttr((plusMinusAverage_condition + '.outColorR'), (j + '.rotate'+axial), f=1)
            # 添加表达式
            pm.expression(s='if('+general_controller[0]+'.baking_wheels=='+general_controller[0]+'.expression_type){\n'
                            '    int $start=1;\n'
                            '    int $start_frame='+general_controller[0]+'.start_frame'+';\n'
                            '    if(frame <= $start_frame)$start=0;\n'
                            '    float $start_num = FK'+base_joint_name+'.start_num;\n'
                            '    if(frame > $start_frame)$start_num=0;\n'
                            
                            '    float $diameter = FK'+base_joint_name+'.diameter;\n'
                            '    float $autoRoll = FK'+base_joint_name+'.autoRoll;\n'
                            '    float $sideAngle=prevPosAngler'+base_joint_name+'.rotateX;\n'
                            '    float $scale = MainScaleMultiplyDivide.input1Y;\n'
                            '    float $prevPosX=FK'+base_joint_name+'.prevPosX;\n'
                            '    float $prevPosY=FK'+base_joint_name+'.prevPosY;\n'
                            '    float $prevPosZ=FK'+base_joint_name+'.prevPosZ;\n'
                            '    prevPosOffset'+base_joint_name+'.translateX=$prevPosX;\n'
                            '    prevPosOffset'+base_joint_name+'.translateY=$prevPosY;\n'
                            '    prevPosOffset'+base_joint_name+'.translateZ=$prevPosZ;\n'
                            '    float $nowPosX=nowPos'+base_joint_name+'.translateX;\n'
                            '    float $nowPosY=nowPos'+base_joint_name+'.translateY;\n'
                            '    float $nowPosZ=nowPos'+base_joint_name+'.translateZ;\n'
                            '    float $distance=`mag<<$nowPosX-$prevPosX,$nowPosY-$prevPosY,$nowPosZ-$prevPosZ>>`;\n'
                            '    float $curRotX=FKX'+base_joint_name+'.calculate_tire_num;\n'
                            '    float $piD = 3.14 * $diameter;\n'
                            '    FKX'+base_joint_name+'.calculate_tire_num=$start_num+$start*($curRotX+($distance/$piD)*360 * $autoRoll * 1 * sin(deg_to_rad($sideAngle)) / $scale);\n'
                            '    FK'+base_joint_name+'.prevPosX=$nowPosX;\n'
                            '    FK'+base_joint_name+'.prevPosY=$nowPosY;\n'
                            '    FK'+base_joint_name+'.prevPosZ=$nowPosZ;\n'
                            '}',
                          ae=1, uc='all', o='', n=(base_joint_name+'_WheelExpression'))

        # 添加表达式
        pm.expression(s='if('+general_controller[0]+'.baking_wheels==1 && '+general_controller[0]+'.expression_type==1){\n'
                        '    int $start=1;\n'
                        '    string $car[]=`ls "*.baking_wheels"`;\n'
                        '    int $end_frame = `playbackOptions -q -max`;\n'
                        '    int $now_frame = `currentTime -q`;\n'
                        '    for($i=0;$i<size($car);$i++){\n'
                        '        int $open=`getAttr $car[$i]`;\n'
                        '        if($open==1){\n'
                        '            string $soure[];\n'
                        '            int $numTok=`tokenize $car[$i] "." $soure`;\n'
                        '            float $start_frame=`getAttr ($soure[0]+".start_frame")`;\n'
                        '            if(frame>=$start_frame){\n'
                        '                string $tire[]=`ls ($soure[0]+".tire")`;\n'
                        '                string $tires[]=`listConnections -d 1 $tire[0]`;\n'
                        '                for($j=0;$j<size($tires);$j++){\n'
                        '                    float $tire_num=`getAttr ($tires[$j]+".calculate_tire_num")`;\n'
                        '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
                        '                    setAttr ($tires[$j]+".baking_wheel") $tire_num;\n'
                        '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
                        '                }\n'
                        '            }\n'
                        '        }\n'
                        '    }\n'
                        '    if($end_frame==$now_frame){\n'
                        '        for($i=0;$i<size($car);$i++){\n'
                        '            setAttr $car[$i] 0;\n'
                        '        }\n'
                        '    }\n'
                        '}\n',
                      ae=1, uc='all', o='', n=('BakingWheelExpression'))

    def create_tire(self):
        # 加载总控制器
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'new_expression_Load_general_controller')
        tire_parent_controller = pm.ls(sl=1)
        # 加载轮子控制器
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'new_expression_Load_tire_controller')
        tire_controller = pm.ls(sl=1)
        # 加载轮子长度
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'new_expression_Load_tire_perimeter')
        tire_perimeter = pm.ls(sl=1)
        # 加载输出骨骼
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'new_expression_Load_output_joint')
        tire_joint = pm.ls(sl=1)

        grp = pm.group(em=1,n='All_Tire_Grp')

        # 给总样条添加属性
        pm.addAttr(tire_parent_controller, ln='tire', at='bool')
        # pm.setAttr((tire_parent_controller[0]+'.tire'), e=1, channelBox=True, lock=True)
        pm.addAttr(tire_parent_controller, ln='baking_wheels', at='bool')
        pm.setAttr((tire_parent_controller[0]+'.baking_wheels'), e=1, channelBox=True)
        pm.addAttr(tire_parent_controller, ln='start_frame', dv=101, at='long')
        pm.setAttr((tire_parent_controller[0]+'.start_frame'), e=1, channelBox=True)
        pm.addAttr(tire_parent_controller, ln='expression_type', en="tradition:baking:", at="enum")
        pm.setAttr((tire_parent_controller[0]+'.expression_type'), e=1, channelBox=True)

        ########################################################################################################################
        for i in range(0,len(tire_controller)):
            # 创建烘焙骨骼
            baking_bones = pm.joint(p=(0, 0, 0),n=(tire_controller[i]+'_baking_joint'))
            pm.parent(baking_bones,tire_controller[i])
            pm.setAttr(baking_bones+'.jointOrientX', 0)
            pm.setAttr(baking_bones+'.jointOrientY', 0)
            pm.setAttr(baking_bones+'.jointOrientZ', 0)
            pm.delete(pm.parentConstraint(tire_controller[i],baking_bones,w=1))
            # 创建
            prePosA = pm.spaceLocator(p=(0,0,0),n=(tire_controller[i]+'_car_bl_prePosLocA'))
            nowPos = pm.spaceLocator(p=(0, 0, 0), n=(tire_controller[i]+'_car_bl_nowPosLoc'))
            prePos = pm.spaceLocator(p=(0, 0, 0), n=(tire_controller[i]+'_car_bl_prePosLoc'))
            move_grp = pm.group(n=(tire_controller[i]+'_Tire'))
            pm.setAttr(tire_controller[i]+'_car_bl_prePosLoc.visibility', 0)
            pm.select(nowPos,prePosA)
            Group1 = pm.group(n=(tire_controller[i]+'_car_bl_locGrp'))
            pm.setAttr(tire_controller[i]+'_car_bl_locGrp.visibility',0)

            pm.addAttr((tire_controller[i]), ln='prePosX', dv=0, at='double')
            # pm.setAttr((tire_controller[i]+'.prePosX'), e=1, keyable=True)
            pm.addAttr((tire_controller[i]), ln='prePosY', dv=0, at='double')
            # pm.setAttr((tire_controller[i]+'.prePosY'), e=1, keyable=True)
            pm.addAttr((tire_controller[i]), ln='prePosZ', dv=0, at='double')
            # pm.setAttr((tire_controller[i]+'.prePosZ'), e=1, keyable=True)

            pm.addAttr((tire_controller[i]), ln='direction_num', dv=0, at='double')
            # pm.setAttr((tire_controller[i]+'.direction_num'), e=1, keyable=True)

            pm.select(Group1,move_grp)
            top_grp = pm.group(n=(tire_controller[i]+'Tire_Grp'))
            pm.parent(top_grp,grp)

            pm.pointConstraint(prePosA, prePos, weight=1)
            pm.pointConstraint(move_grp,nowPos,weight=1)
            pm.delete(pm.pointConstraint(tire_controller[i],top_grp,weight=1))
            curveInfo = pm.shadingNode('curveInfo', asUtility=1)
            pm.connectAttr((tire_perimeter[i] + '.worldSpace[0]'), (curveInfo + '.inputCurve'),f=1)

            # 给样条添加属性
            pm.addAttr(tire_controller[i], ln='running_direction', en='x:y:z:', at='enum')
            pm.setAttr((tire_controller[i] + '.running_direction'), e=1, channelBox=True)
            pm.setAttr((tire_controller[i] + '.running_direction'),2)
            pm.addAttr(tire_controller[i], ln='axial', en='x:y:z:', at='enum')
            pm.setAttr((tire_controller[i] + '.axial'), e=1, channelBox=True)
            pm.addAttr(tire_controller[i], ln='start_num', dv=0, at='double')
            pm.setAttr((tire_controller[i] + '.start_num'), e=1, keyable=True)
            pm.addAttr(tire_controller[i], ln='baking_num', dv=0, at='double')
            pm.setAttr((tire_controller[i] + '.baking_num'), e=1, keyable=True)
            pm.addAttr(tire_controller[i], ln='magnification', dv=1, at='double')
            pm.setAttr((tire_controller[i] + '.magnification'), e=1, keyable=True)
            # 给骨骼添加属性
            pm.addAttr(baking_bones, ln='tire', at='bool')
            # pm.setAttr((baking_bones + '.tire'), e=1, channelBox=True)
            pm.addAttr(baking_bones, ln='calculate_tire_num', dv=0, at='double')
            pm.setAttr((baking_bones + '.calculate_tire_num'), e=1, keyable=True)
            # 添加骨骼属性代理(代码里给此属性k帧)
            pm.addAttr(baking_bones, proxy=(tire_controller[i]+'.baking_num'), longName='baking_wheel')
            # 添加总控制器属性代理
            pm.addAttr(tire_parent_controller, proxy=(tire_controller[i]+'.baking_num'), longName=baking_bones)
            # 建立节点关系
            pm.connectAttr((tire_parent_controller[0]+'.tire'), (baking_bones+'.tire'), f=1)
            choice_node = pm.shadingNode('choice', asUtility=1)
            pm.connectAttr((tire_parent_controller[0]+'.expression_type'), (choice_node + '.selector'), f=1)
            pm.connectAttr((baking_bones + '.calculate_tire_num'), (choice_node + '.input[0]'), f=1)
            pm.connectAttr((tire_controller[i]+'.baking_num'), (choice_node + '.input[1]'), f=1)
            for j,axial in zip(range(0,3),['X','Y','Z']):
                plusMinusAverage_condition = pm.shadingNode('condition', asUtility=1)
                pm.connectAttr((tire_controller[i] + '.axial'), (plusMinusAverage_condition + '.firstTerm'), f=1)
                pm.setAttr((plusMinusAverage_condition+'.secondTerm'),j)
                pm.setAttr((plusMinusAverage_condition + '.colorIfFalseR'), 0)
                pm.connectAttr((choice_node + '.output'), (plusMinusAverage_condition + '.colorIfTrueR'), f=1)
                pm.connectAttr((plusMinusAverage_condition + '.outColorR'), (baking_bones + '.rotate'+axial), f=1)
            choice_node = pm.shadingNode('choice', asUtility=1)
            pm.connectAttr((tire_controller[i]+'.running_direction'), (choice_node+'.selector'), f=1)
            pm.connectAttr((tire_controller[i]+'_car_bl_prePosLoc.translateX'), (choice_node+'.input[0]'), f=1)
            pm.connectAttr((tire_controller[i]+'_car_bl_prePosLoc.translateY'), (choice_node+'.input[1]'), f=1)
            pm.connectAttr((tire_controller[i]+'_car_bl_prePosLoc.translateZ'), (choice_node+'.input[2]'), f=1)
            pm.connectAttr((choice_node+'.output'), (tire_controller[i]+'.direction_num'))

            pm.expression(s=('if('+tire_parent_controller[0]+'.baking_wheels=='+tire_parent_controller[0]+'.expression_type){\n'
                            '   int $start=1;\n'
                            '   int $start_frame='+tire_parent_controller[0]+'.start_frame;\n'
                            '   if(frame <= $start_frame)$start=0;\n'
                            '   float $start_num = '+tire_controller[i]+'.start_num;\n'
                            '   if(frame > $start_frame)$start_num=0;\n'
                            '   float $autoRoll=' + tire_controller[i] + '.magnification;\n'
                            '   float $prePosX=' + tire_controller[i] + '.prePosX;\n'
                            '   float $prePosY=' + tire_controller[i] + '.prePosY;\n'
                            '   float $prePosZ=' + tire_controller[i] + '.prePosZ;\n'
                            '   float $nowPosX=' + tire_controller[i] + '_car_bl_nowPosLoc.translateX;\n'
                            '   float $nowPosY=' + tire_controller[i] + '_car_bl_nowPosLoc.translateY;\n'
                            '   float $nowPosZ=' + tire_controller[i] + '_car_bl_nowPosLoc.translateZ;\n'
                            '   float $dis=`mag(<<$nowPosX,$nowPosY,$nowPosZ>>-<<$prePosX,$prePosY,$prePosZ>>)`;\n'
                            '   ' + tire_controller[i] + '_car_bl_prePosLocA.translateX=$prePosX;\n'
                            '   ' + tire_controller[i] + '_car_bl_prePosLocA.translateY=$prePosY;\n'
                            '   ' + tire_controller[i] + '_car_bl_prePosLocA.translateZ=$prePosZ;\n'
                            '   ' + tire_controller[i] + '.prePosX=$nowPosX;\n'
                            '   ' + tire_controller[i]+ '.prePosY=$nowPosY;\n'
                            '   ' + tire_controller[i] + '.prePosZ=$nowPosZ;\n'
                            '   float $dirPreZ=' + tire_controller[i]+'.direction_num;\n'
                            '   int $dir=1;\n'
                            '   if($dirPreZ<0)$dir=-1;\n'
                            '   float $perimeter=' + curveInfo + '.arcLength;\n'
                            '   float $curRoll=' + baking_bones + '.calculate_tire_num;\n'
                            '   ' + baking_bones + '.calculate_tire_num=$start_num+$start*($curRoll+($dis/$perimeter)*360*$autoRoll*$dir);\n'
                            '}'),
                            ae=1, uc='all', o='', n=(tire_joint[i]+'_WheelExpression'))
            pm.delete(pm.pointConstraint(tire_controller[i],move_grp,w=1))
            pm.parentConstraint(tire_controller[i],move_grp,w=1,mo=1)


            rotateX = pm.listConnections((tire_joint[i]+'.rotateX'),p=1)
            if rotateX:
                pm.disconnectAttr(rotateX[0], (tire_joint[i]+'.rotateX'))
            rotateY = pm.listConnections((tire_joint[i]+'.rotateY'),p=1)
            if rotateY:
                pm.disconnectAttr(rotateY[0], (tire_joint[i]+'.rotateY'))
            rotateZ = pm.listConnections((tire_joint[i]+'.rotateZ'),p=1)
            if rotateZ:
                pm.disconnectAttr(rotateZ[0], (tire_joint[i]+'.rotateZ'))

            pm.orientConstraint(baking_bones,tire_joint[i],mo=1, weight=1)

            pm.parent(tire_perimeter[i],grp)
            pm.setAttr((tire_perimeter[i]+'.visibility'), 0)
            pm.parentConstraint(tire_controller[i],tire_perimeter[i],w=1)
            pm.scaleConstraint(tire_controller[i], tire_perimeter[i], w=1)

        # 添加表达式
        pm.expression(s='if('+tire_parent_controller[0]+'.baking_wheels==1 && '+tire_parent_controller[0]+'.expression_type==1){\n'
                        '    int $start=1;\n'
                        '    string $car[]=`ls "*.baking_wheels"`;\n'
                        '    int $end_frame = `playbackOptions -q -max`;\n'
                        '    int $now_frame = `currentTime -q`;\n'
                        '    for($i=0;$i<size($car);$i++){\n'
                        '        int $open=`getAttr $car[$i]`;\n'
                        '        if($open==1){\n'
                        '            string $soure[];\n'
                        '            int $numTok=`tokenize $car[$i] "." $soure`;\n'
                        '            float $start_frame=`getAttr ($soure[0]+".start_frame")`;\n'
                        '            if(frame>=$start_frame){\n'
                        '                string $tire[]=`ls ($soure[0]+".tire")`;\n'
                        '                string $tires[]=`listConnections -d 1 $tire[0]`;\n'
                        '                for($j=0;$j<size($tires);$j++){\n'
                        '                    float $tire_num=`getAttr ($tires[$j]+".calculate_tire_num")`;\n'
                        '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
                        '                    setAttr ($tires[$j]+".baking_wheel") $tire_num;\n'
                        '                    setKeyframe ($tires[$j]+".baking_wheel");\n'
                        '                }\n'
                        '            }\n'
                        '        }\n'
                        '    }\n'
                        '    if($end_frame==$now_frame){\n'
                        '        for($i=0;$i<size($car);$i++){\n'
                        '            setAttr $car[$i] 0;\n'
                        '        }\n'
                        '    }\n'
                        '}\n',
                      ae=1, uc='all', o='', n=('BakingWheelExpression'))

    # 删除轮胎
    def PresetTemplateDeleteTire(self):
        pass
ShowWindow = NewExpression()
if __name__ == '__main__':
    ShowWindow.ZKM_Window()












