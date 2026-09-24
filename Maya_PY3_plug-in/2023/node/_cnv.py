import codecs, sys
path = sys.argv[1]
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()
with codecs.open(path, 'w', 'gbk') as f:
    f.write(content)
print('GBK conversion done')
