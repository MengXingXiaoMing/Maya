#coding=gbk
import os
#加载文本

class ZKM_FileNameProcessingClass:
    # 返回加载文件夹内相关后缀的文件名称（取返回值）
    def ZKM_LoadFileNameOfTheCorrespondingSuffix(self, file_path, HaveSuffix, *Allsuffix):
        files = os.listdir(file_path)  # 获取文件夹下所有文件名称
        Out = []
        for suffix in Allsuffix:
            for file in files:
                if not os.path.splitext(file)[1]:
                    continue
                if file == '__init__.py':
                    continue
                if os.path.splitext(file)[1] in suffix:  # 找到指定后缀的文件
                    if (HaveSuffix > 0):
                        Out.append(file)  # 将元素添加到列表最后
                    else:
                        Out.append(os.path.splitext(file)[0])  # 将元素添加到列表最后
        return (Out)

