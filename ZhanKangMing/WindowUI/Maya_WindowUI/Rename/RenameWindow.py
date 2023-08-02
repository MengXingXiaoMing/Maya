#coding=gbk
import maya.cmds as cmds
import pymel.core as pm
import os
import sys
import inspect
#根目录
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
# 加载文本
from LoadText import *
class ZKM_RenameWindowClass():
    def __init__(self):
        # 通过self向新建的对象中初始化属性
        cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.file_path = os.path.join(cur_dir)  # 获取文件路径
        # print(self.file_path)
        cur_dirA = '/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
    def ZKM_Window(self):#窗口
        if pm.window('RenameWindow',ex=1):
            pm.deleteUI('RenameWindow')
        pm.window('RenameWindow', t="改名",cc='ZKM_RenameWindowClass().SaveUIWindow()')
        pm.rowColumnLayout(nc=1, adj=2)
        pm.rowColumnLayout(nc=6, adj=6)
        pm.checkBox('RenameWindow_AutomaticallySaveSettings',label='自动保存设置',cc='ZKM_RenameWindowClass().SaveUI()')
        pm.iconTextButton(i='duplicateReference.png',c='ZKM_RenameWindowClass().SelectDuplicateNameObject()')
        pm.textField('RenameWindow_SelectObjectTextField')
        pm.button(l='选择对象', c='ZKM_RenameWindowClass().SelectTxt()')
        pm.iconTextButton(i='deleteRenderPass.png', c='ZKM_RenameWindowClass().detectionOfTheSameNameMain()')
        pm.button(l='数字→字母', c='ZKM_RenameWindowClass().ConvertNumToCharacters()')
        pm.setParent('..')
        pm.separator(style="in", height=1)
        pm.rowColumnLayout(nc=2, adj=1)
        pm.rowColumnLayout(nc=1, adj=2)
        pm.radioCollection('RenameWindow_IncludeSubsets')
        pm.radioButton('SELF', label="修改当前选择")
        pm.radioButton('Subsets', label="修改所有子集")
        pm.radioCollection('RenameWindow_IncludeSubsets', edit=1, select='SELF')
        pm.checkBox('RenameWindow_RunPrint',label="运行且打印")
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=3)
        pm.textFieldButtonGrp('RenameWindow_AddPrefix', bl='添加前缀',bc='ZKM_RenameWindowClass().AddPrefix()')
        pm.separator(style="in", height=1)
        pm.textFieldButtonGrp('RenameWindow_AddSuffix', bl='添加后缀',bc='ZKM_RenameWindowClass().AddSuffix()')
        pm.separator(style="in", height=1)
        pm.rowColumnLayout(nc=3, adj=2)
        pm.textFieldGrp('RenameWindow_SubstituteCharacterSoure',cw1=100)
        pm.text(l='>>>')
        pm.textFieldButtonGrp('RenameWindow_SubstituteCharacterTarget', cw2=(109,0),bl='替换字符',bc='ZKM_RenameWindowClass().SubstituteCharacter()')
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.separator(style="in", height=1)
        pm.rowColumnLayout(nc=1, adj=2)
        pm.rowColumnLayout('RenameWindow_CompletelyRenamerowColumnLayout',nc=6, adj=6)
        pm.textFieldGrp('RenameWindow_CompletelyRenamePrefix', l='前缀',cw2=(30,60))
        pm.rowColumnLayout('rowColumnLayout_name_front',nc=1, adj=1)
        pm.setParent('..')
        pm.textFieldGrp('RenameWindow_CompletelyRenameName', l='名称',cw2=(30,90))
        pm.rowColumnLayout('rowColumnLayout_suffix_front',nc=1, adj=1)
        pm.setParent('..')
        pm.textFieldGrp('RenameWindow_CompletelyRenameSuffix', l='后缀',cw2=(30,60))
        pm.rowColumnLayout('rowColumnLayout_suffix_back',nc=4, adj=1)
        pm.optionMenu('RenameWindow_binary_optionMenu',w=60)
        pm.menuItem(label="2进制")
        pm.menuItem(label="8进制")
        pm.menuItem(label="10进制")
        pm.menuItem(label="16进制")
        pm.menuItem(label="26进制")
        pm.optionMenu('RenameWindow_binary_optionMenu', e=1,sl=3)
        pm.setParent('..')
        pm.setParent('..')
        pm.intScrollBar('RenameWindow_MoveUI_intScrollBar',min=1,max=3, step=1, largeStep=1, value=3,cc='ZKM_RenameWindowClass().MoveUI()')
        pm.rowColumnLayout(nc=10, adj=9)
        pm.text(l='改名命令')
        pm.separator(style="single")
        pm.iconTextButton(i='nodeGrapherArrowDown.png',c='ZKM_RenameWindowClass().CompletelyRename()')
        pm.iconTextButton(i='play_S.png',c='pm.cmdScrollFieldExecuter(\'RenameWindow_cmdScrollFieldExecuter\',e=1,exc=1)')
        pm.iconTextButton(i='executeAll.png',c='pm.cmdScrollFieldExecuter(\'RenameWindow_cmdScrollFieldExecuter\',e=1,exa=1)')
        pm.iconTextButton(i='clearInput.png',c='pm.cmdScrollFieldExecuter(\'RenameWindow_cmdScrollFieldExecuter\',e=1,clr=1)')
        pm.iconTextButton(i='nodeGrapherDockBack.png',c='ZKM_RenameWindowClass().SaveToSelectNote()')
        pm.separator(style="single")
        pm.textFieldButtonGrp('RenameWindow_QueryCharacters',cw2=(195,0),bl='查询',bc='ZKM_RenameWindowClass().QueryCharacters()')
        pm.setParent('..')
        pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter',sln=1,sw=1,st='mel')
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        self.KeepUI()
        pm.showWindow()
    def MoveUI(self):
        num = pm.intScrollBar('RenameWindow_MoveUI_intScrollBar',q=1, value=1)
        if num==1:
            pm.optionMenu('RenameWindow_binary_optionMenu',e=1,p='rowColumnLayout_name_front')
            pm.rowColumnLayout('RenameWindow_CompletelyRenamerowColumnLayout', e=1, adj=2)
        if num==2:
            pm.optionMenu('RenameWindow_binary_optionMenu',e=1,p='rowColumnLayout_suffix_front')
            pm.rowColumnLayout('RenameWindow_CompletelyRenamerowColumnLayout', e=1, adj=4)
        if num==3:
            pm.optionMenu('RenameWindow_binary_optionMenu',e=1,p='rowColumnLayout_suffix_back')
            pm.rowColumnLayout('RenameWindow_CompletelyRenamerowColumnLayout', e=1, adj=6)

    def KeepUI(self):
        f = open(((self.file_pathReversion+'/UI_Set.txt')))  # 返回一个文件对象
        line = f.readlines()
        f.close()
        pm.checkBox('RenameWindow_AutomaticallySaveSettings',e=1,v=int(line[0]))
        pm.textField('RenameWindow_SelectObjectTextField', e=1, text=line[1][:-1])
        pm.radioCollection('RenameWindow_IncludeSubsets', e=1, select=line[2][:-1])
        pm.textFieldButtonGrp('RenameWindow_AddPrefix', e=1, text=line[3][:-1])
        pm.textFieldButtonGrp('RenameWindow_AddSuffix', e=1, text=line[4][:-1])
        pm.checkBox('RenameWindow_RunPrint', e=1, v=int(line[5]))
        pm.textFieldGrp('RenameWindow_SubstituteCharacterSoure',e=1, text=line[6][:-1])
        pm.textFieldButtonGrp('RenameWindow_SubstituteCharacterTarget',e=1, text=line[7][:-1])
        pm.textFieldGrp('RenameWindow_CompletelyRenamePrefix',e=1, text=line[8][:-1])
        pm.textFieldGrp('RenameWindow_CompletelyRenameName',e=1, text=line[9][:-1])
        pm.textFieldGrp('RenameWindow_CompletelyRenameSuffix',e=1, text=line[10][:-1])
        pm.optionMenu('RenameWindow_binary_optionMenu',e=1, sl=int(line[11]))
        pm.intScrollBar('RenameWindow_MoveUI_intScrollBar',e=1, value=int(line[12]))
        self.MoveUI()
        pm.textFieldButtonGrp('RenameWindow_QueryCharacters',e=1, text=line[13])

    def SaveUIWindow(self):
        if int(pm.checkBox('RenameWindow_AutomaticallySaveSettings', q=1, v=1)) == 1:
            self.SaveUI()
    def SaveUI(self):
        file = open((self.file_pathReversion+'/UI_Set.txt'), 'w')
        a0 = str(int(pm.checkBox('RenameWindow_AutomaticallySaveSettings',q=1,v=1)))
        a1 = pm.textField('RenameWindow_SelectObjectTextField', q=1, text=1)
        a2 = pm.radioCollection('RenameWindow_IncludeSubsets', q=1, select=1)
        a3 = pm.textFieldButtonGrp('RenameWindow_AddPrefix', q=1, text=1)
        a4 = pm.textFieldButtonGrp('RenameWindow_AddSuffix', q=1, text=1)
        a5 = str(int(pm.checkBox('RenameWindow_RunPrint', q=1, v=1)))
        a6 = pm.textFieldGrp('RenameWindow_SubstituteCharacterSoure',q=1, text=1)
        a7 = pm.textFieldButtonGrp('RenameWindow_SubstituteCharacterTarget',q=1, text=1)
        a8 = pm.textFieldGrp('RenameWindow_CompletelyRenamePrefix',q=1, text=1)
        a9 = pm.textFieldGrp('RenameWindow_CompletelyRenameName',q=1, text=1)
        a10 = pm.textFieldGrp('RenameWindow_CompletelyRenameSuffix',q=1, text=1)
        a11 = pm.optionMenu('RenameWindow_binary_optionMenu',q=1, sl=1)
        a12 = pm.intScrollBar('RenameWindow_MoveUI_intScrollBar',q=1, value=1)
        a13 = pm.textFieldButtonGrp('RenameWindow_QueryCharacters',q=1, text=1)
        w = (str(a0) + '\n' + str(a1) + '\n' + str(a2) + '\n' + str(a3) + '\n' + str(a4) + '\n' + str(a5) + '\n' + str(a6) + '\n' + str(
            a7) + '\n' + str(a8) + '\n' + str(a9) + '\n' + a10 + '\n' + str(a11) + '\n' + str(a12) + '\n' + str(a13))
        file.write(w)

    #ZKM_RenameWindowClass().SaveUI()
    def SelectDuplicateNameObject(self):
        sel = pm.ls()
        sel = list(filter(lambda x: x.find('|') >= 0, sel))
        pm.select(sel)
    def detectionOfTheSameNameMain(self):
        ZKM_RootDirectory = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        print '别人写的，这种我就不重新写了'
        pm.mel.eval('source \"'+ZKM_RootDirectory+'/Outside/去除重复的物体名.mel\";')

    def ConvertNumToCharacters(self):
        sel = pm.ls()
        lockSel = pm.ls(ln=1)
        sel = [x for x in sel if x not in lockSel]
        AZ = ['A','B','C','D','E','F','G','H','I','J','K']
        NUM = ['0','1','2','3','4','5','6','7','8','9']
        for s in sel:
            Text = ''
            name = str(s.split('|')[-1])
            for N in name:
                for i in range(0,len(NUM)):
                    if N == NUM[i]:
                        N = AZ[i]
                        break
                Text = Text+N
            try:
                pm.rename(s,Text)
            except:
                pass

    def AddPrefix(self):
        sel = pm.radioCollection('RenameWindow_IncludeSubsets', q=1, select=1)
        RunPrint = int(pm.checkBox('RenameWindow_RunPrint',q=1,v=1))
        if sel == 'SELF':
            level = 0
        else:
            level = 1
        self.ZKM_AddPrefix(level,RunPrint)
    def ZKM_AddPrefix(self,level,RunPrint):
        if level == 1:
            pm.mel.SelectHierarchy()
        sel = pm.ls(sl=1,type='transform')
        Prefix = pm.textFieldButtonGrp('RenameWindow_AddPrefix', q=1,text=1)
        Prefix = Prefix.encode('utf-8') # 字符码转为字符串
        for i in range(0,len(sel)):
            Text = self.Rename(sel[i], Prefix, sel[i].split('|')[-1], '', ['',''], [1,''])
            if RunPrint == 1:
                print Text
    def AddSuffix(self):
        sel = pm.radioCollection('RenameWindow_IncludeSubsets', q=1, select=1)
        RunPrint = int(pm.checkBox('RenameWindow_RunPrint', q=1, v=1))
        if sel == 'SELF':
            level = 0
        else:
            level = 1
        self.ZKM_AddSuffix(level,RunPrint)
    def ZKM_AddSuffix(self,level,RunPrint):
        if level == 1:
            pm.mel.SelectHierarchy()
        sel = pm.ls(sl=1,type='transform')
        Suffix = pm.textFieldButtonGrp('RenameWindow_AddSuffix', q=1,text=1)
        Suffix = Suffix.encode('utf-8') # 字符码转为字符串
        for i in range(0,len(sel)):
            Text = self.Rename(sel[i], '', sel[i].split('|')[-1], Suffix, ['',''], [1,''])
            if RunPrint == 1:
                print Text
    def SubstituteCharacter(self):
        sel = pm.radioCollection('RenameWindow_IncludeSubsets', q=1, select=1)
        RunPrint = int(pm.checkBox('RenameWindow_RunPrint', q=1, v=1))
        if sel == 'SELF':
            level = 0
        else:
            level = 1
        self.ZKM_SubstituteCharacter(level,RunPrint)
    def ZKM_SubstituteCharacter(self,level,RunPrint):
        if level == 1:
            pm.mel.SelectHierarchy()
        sel = pm.ls(sl=1,type='transform')
        Soure = pm.textFieldGrp('RenameWindow_SubstituteCharacterSoure', q=1,text=1)
        Target = pm.textFieldButtonGrp('RenameWindow_SubstituteCharacterTarget', q=1, text=1)
        Soure = Soure.encode('utf-8') # 字符码转为字符串
        Target = Target.encode('utf-8')  # 字符码转为字符串
        for i in range(0,len(sel)):
            Text = self.Rename(sel[i], '', sel[i], '', [Soure,Target], [1,''])
            if RunPrint == 1:
                print Text
    def CompletelyRename(self):
        sel = pm.radioCollection('RenameWindow_IncludeSubsets', q=1, select=1)
        RunPrint = int(pm.checkBox('RenameWindow_RunPrint', q=1, v=1))
        if sel == 'SELF':
            level = 0
        else:
            level = 1
        self.ZKM_CompletelyRename(level)
    def ZKM_CompletelyRename(self,level):
        if level == 1:
            pm.mel.SelectHierarchy()
        sel = pm.ls(sl=1,type='transform')
        Prefix = pm.textFieldGrp('RenameWindow_CompletelyRenamePrefix', q=1, text=1)
        Name = pm.textFieldGrp('RenameWindow_CompletelyRenameName', q=1, text=1)
        Suffix = pm.textFieldGrp('RenameWindow_CompletelyRenameSuffix', q=1, text=1)
        Prefix = Prefix.encode('utf-8')  # 字符码转为字符串
        Name = Name.encode('utf-8')  # 字符码转为字符串
        Suffix = Suffix.encode('utf-8')  # 字符码转为字符串
        Binary = pm.optionMenu('RenameWindow_binary_optionMenu', q=1,sl=1)
        NumPosition = pm.intScrollBar('RenameWindow_MoveUI_intScrollBar', q=1, value=1)
        Num = 0
        if Binary == 5:
            Num =26
        if Binary == 4:
            Num =16
        if Binary == 3:
            Num =10
        if Binary == 2:
            Num =8
        if Binary == 1:
            Num =2
        for i in range(0, len(sel)):
            j=i+1
            n = self.DecimalConversion(10, Num, j)
            C = self.Rename(sel[i], Prefix, Name, Suffix, ['', ''], [NumPosition, n])
            pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter', e=1, at=C)
    def Rename(self,Soure,Prefix,Name,Suffix,SubstituteCharacter,Num):
        Target = ''
        if Num[0] == 1:
            Target = Prefix+Num[1]+Name+Suffix
        if Num[0] == 2:
            Target = Prefix+Name+Num[1]+Suffix
        if Num[0] == 3:
            Target = Prefix+Name+Suffix+Num[1]
        Target = Target.replace(SubstituteCharacter[0], SubstituteCharacter[1])
        S = str(Soure)
        pm.rename(Soure,Target)
        return 'rename '+ S +' '+Target+';\n'
    def DecimalConversion(self, Soure, Target, num):
        Ten = 0
        if Soure < 10:
            Ten = str(self.DecimalConversion_ToTen(Target,num))
        if Soure > 10:
            Ten = str(self.DecimalConversion_ToTen(Target,num))
        if Soure == 10:
            Ten = str(num)
        if Target == 10:
            return Ten
        else:
            return str(self.DecimalConversion_TenTo(Target, int(Ten)))

    def DecimalConversion_ToTen(self, Soure,num):
        if Soure == 2:
            # 2 to 10
            return(int(str(num), 2))
        if Soure == 8:
            # 8 to 10
            return(int(str(num), 8))
        if Soure == 16:
            # 16 to 10
            return((int(str(num), 16)))
        if Soure == 26:
            # 26 to 10
            Num = ''
            STR = str(num)
            for i in range(0, len(STR) - 1):
                AddNum = str((ord(STR[i]) - 64) * 26)
                Num = Num + AddNum
            AddNum = (ord(STR[-1]) - 64)
            Num = int(Num) + AddNum
            return Num
    def DecimalConversion_TenTo(self, Target,num):
        if Target == 2:
            # 10 to 2
            return (bin(num))[2:]
        if Target == 8:
            # 10 to 8
            return int(oct(num))
        if Target == 16:
            # 10 to 16
            return (hex(num))[2:]
        if Target == 26:
            # 10 to 26
            AZ = ''
            while num > 26:
                r = num % 26
                AZ = str(chr(64 + r)) + AZ
                num = num // 26
            AZ = str(chr(64 + num)) + AZ
            return AZ

    def SaveToSelectNote(self):
        sel = pm.ls(sl=1)
        if not sel[0].hasAttr('notes'):
            sel[0].addAttr('notes', type='string')
        pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter', e=1, sla=1)
        pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter', e=1, slt=1)
        Txt = pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter', q=1, slt=1)
        sel[0].attr('notes').set(Txt)
    def QueryCharacters(self):
        Str = str(pm.textFieldButtonGrp('RenameWindow_QueryCharacters', q=1, text=1))
        pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter', e=1, ss=Str)
        pm.cmdScrollFieldExecuter('RenameWindow_cmdScrollFieldExecuter',q=1, sas=1)

    def SelectTxt(self):
        text = pm.textField('RenameWindow_SelectObjectTextField',q=1,tx=1)
        text = text.encode('utf-8')
        pm.select(text)
ShowWindow = ZKM_RenameWindowClass()
if __name__ =='__main__':
    ShowWindow.ZKM_Window()
#还差自动保存和数字替换成字母
