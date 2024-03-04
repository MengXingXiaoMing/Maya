'''import numpy as np
import matplotlib.pyplot as plt


def line_intersection(A, B, C, D):
    a1 = B[1] - A[1]
    b1 = A[0] - B[0]
    c1 = a1 * A[0] + b1 * A[1]

    a2 = D[1] - C[1]
    b2 = C[0] - D[0]
    c2 = a2 * C[0] + b2 * C[1]

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        return None  # lines are parallel

    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant

    return (x, y)


A = (1, 1)
B = (5, 5)
C = (3, 0)
D = (0, 3)

intersection = line_intersection(A, B, C, D)
if intersection:
    x, y = intersection
    print(f'Intersection at ({x:.1f}, {y:.1f})')
else:
    print('Lines do not intersect.')

# Plotting the lines
fig, ax = plt.subplots()
ax.plot([A[0], B[0]], [A[1], B[1]], 'r', label='Line AB')
ax.plot([C[0], D[0]], [C[1], D[1]], 'b', label='Line CD')
if intersection:
    ax.plot(x, y, 'go', label='Intersection')
ax.legend()
plt.show()





'''













import pymel.core as pm




ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_grp')
face_bs_grp = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face')
face = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'tongue')
tongue = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'upper_teeth')
upper_teeth = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'lower_teeth')
lower_teethe = pm.ls(sl=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'controller')
controller = pm.ls(sl=1)
bs_name = pm.optionMenu('bs_convert_drver_window_bs_name_OptionMenu',q=1,v=1)
ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'face_bs_name')
face_bs_name = pm.ls(sl=1)


# 开始修改上下牙和舌头的位置
# 修改舌头位置
all_tongue = pm.ls(sl=1)
shape = pm.listRelatives(all_tongue[0], s=1)
pm.createNode('closestPointOnMesh', n=('cpom'))
pm.connectAttr((shape[0] + '.outMesh'), ('cpom' + '.inMesh'), f=1)
pm.setAttr(('cpom.inPositionX'), 0)
pm.setAttr(('cpom.inPositionY'), 0)
pm.setAttr(('cpom.inPositionZ'), 0)
u = float(pm.getAttr('cpom.parameterU'))
v = float(pm.getAttr('cpom.parameterV'))
pm.delete('cpom')
for i in range(0,len(all_tongue)):
    shape = pm.listRelatives(all_tongue[i], s=1)
    pm.createNode('follicle', n=('tongue_follicleShape'+str(i)))
    pm.connectAttr((shape[0] + '.outMesh'), ('tongue_follicleShape'+str(i)+'.inputMesh'), f=1)
    pm.connectAttr((shape[0] + '.worldMatrix[0]'), ('tongue_follicleShape'+str(i)+'.inputWorldMatrix'),f=1)
    pm.connectAttr(('tongue_follicleShape'+str(i)+'.outTranslate'), ('tongue_follicle'+str(i)+'.translate'), f=1)
    pm.connectAttr(('tongue_follicleShape'+str(i)+'.outRotate'), ('tongue_follicle'+str(i)+'.rotate'), f=1)
    pm.setAttr(('tongue_follicleShape'+str(i)+'.parameterU'), u)
    pm.setAttr(('tongue_follicleShape'+str(i)+'.parameterV'), v)
    pm.spaceLocator(p=(0, 0, 0), n=('tongue'+str(i)+'_Loc'))
    pm.delete(pm.parentConstraint('tongue_follicle'+str(i), 'tongue'+str(i)+'_Loc', w=1))
    pm.delete('tongue_follicle'+str(i))
pm.spaceLocator(p=(0, 0, 0), n=('Tongue0_M_Loc'))
pm.delete(pm.parentConstraint('Tongue0_M','Tongue0_M_Loc',w=1))
pm.parentConstraint('tongue0_Loc','Tongue0_M_Loc',w=1,mo=1)
parentConstraint_1 = pm.parentConstraint('Tongue0_M_Loc','Tongue0_M',w=1,mo=1)
pm.parentConstraint('tongue1_Loc','tongue0_Loc',w=1)
pm.delete(parentConstraint_1)
pm.delete('tongue0_Loc','tongue1_Loc','Tongue0_M_Loc')



