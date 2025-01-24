#coding=gbk
import os
import inspect
import sys

print('这是一个py测试')
file_path = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
print(file_path)

