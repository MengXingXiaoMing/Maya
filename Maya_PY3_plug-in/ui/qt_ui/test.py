#coding=gbk
import maya.api.OpenMaya as om
selLis = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selLis)
result = [om.MDagPath()] * selLis.length()
selLis.getDagPath(0, result[0])
node = result[0].node()
node.hasFn(om.MFn.kMesh)
# ����MFnMesh�����Է�����������
mesh_fn = om.MFnMesh(node)
def get_mesh_vertex_uv(mesh_name, vertex_index):
    selection_list = om.MSelectionList()
    selection_list.add(mesh_name)
    dag_path = [om.MDagPath()] * selLis.length()
    selection_list.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path[0])

    # ȷ��������������Ч��Χ��
    if vertex_index < 0 or vertex_index >= mesh_fn.numVertices():
        raise IndexError("Vertex index out of range")

        # ��ȡ����� UV ����
    uv_coords = om.MFloatArray(2)  # ���ڴ洢 UV ���������
    mesh_fn.getUV(vertex_index, uv_coords)

    # ��ȡ UV ����
    u = uv_coords[0]
    v = uv_coords[1]

    return u, v


# ʹ�ú���
mesh_name = "pCube1"
vertex_index = 0
u, v = get_mesh_vertex_uv(mesh_name, vertex_index)
print(f"Vertex {vertex_index} UV: ({u}, {v})")