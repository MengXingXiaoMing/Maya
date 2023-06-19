#coding=gbk
import pymel.core as pm
class ZKM_FileProcessingClass:
    #���ж�Ӧ����,������Ϊ����·��
    def ZKM_RunCorrespondingCommand(self,FilePath):
        FileName = FilePath.split('/')
        Name = FileName[len(FileName)-1].split('.')
        if Name[1]=='mel':
            pm.mel.source(FilePath)
        if Name[1]=='py':
            import maya.app.general.executeDroppedPythonFile as myTempEDPF
            myTempEDPF.executeDroppedPythonFile(FilePath, "")
            del myTempEDPF

    # ���뵼���ļ�
    def ZKM_ImportFile(self,name, ImportAdditionalPath, ImpExpFile,Type):
        #name = pm.optionMenu(ImportFileName, q=1, value=1)
        suffix = ''
        if Type == 'mayaAscii':
            suffix = '.ma'
        if Type == 'mayaBinary':
            suffix = '.mb'
        if ImpExpFile == 1:  # ����
            pm.mel.performFileSilentImportAction(ImportAdditionalPath + '/' + name + suffix)
        else:  # mayaAscii#mayaBinary#����
            pm.cmds.file((ImportAdditionalPath + '/' + name + suffix), pr=1, typ=Type, force=1,
                         options="v=0;", es=1)