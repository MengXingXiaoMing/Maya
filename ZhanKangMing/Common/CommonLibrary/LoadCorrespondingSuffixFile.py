#coding=gbk
import os
#�����ı�

class ZKM_FileNameProcessingClass:
    # ���ؼ����ļ�������غ�׺���ļ����ƣ�ȡ����ֵ��
    def ZKM_LoadFileNameOfTheCorrespondingSuffix(self, file_path, HaveSuffix, *Allsuffix):
        files = os.listdir(file_path)  # ��ȡ�ļ����������ļ�����
        Out = []
        for suffix in Allsuffix:
            for file in files:
                if not os.path.splitext(file)[1]:
                    continue
                if file == '__init__.py':
                    continue
                if os.path.splitext(file)[1] in suffix:  # �ҵ�ָ����׺���ļ�
                    if (HaveSuffix > 0):
                        Out.append(file)  # ��Ԫ����ӵ��б����
                    else:
                        Out.append(os.path.splitext(file)[0])  # ��Ԫ����ӵ��б����
        return (Out)

