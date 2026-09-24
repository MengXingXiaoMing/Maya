import codecs
path = r'z:\1.Private folder\Rig\zhankangming\ZhanKangMing\Maya_PY3_plug-in_2025\2023\node\meshToSurface.py'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()
with codecs.open(path, 'w', 'gbk') as f:
    f.write(content)
print('GBK conversion done')
