import random
import pymel.core as pm
notes = ''
for i in range(0,32):
    j = str(random.randrange(0, 10,1))
    notes = notes + j
import pymel.core as pm
n = pm.selected()[0]
if not n.hasAttr('notes'):
    n.addAttr('notes', type='string')
n.attr('notes').set(notes)
#print (pm.getAttr(pm.ls(sl=1)[0]+'.notes'))