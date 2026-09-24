# -*- coding: gbk -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import numpy as np
import os
import subprocess
import time

# ================= 配置区 (必须准确) =================
# 1. 请在 PyCharm 终端输入: where python  然后把显示的路径贴到这里
# 2. 或者在 PyCharm 右下角 Interpreter 设置里找到路径
# 注意：一定要带上 r 前缀
EXTERNAL_PYTHON = r"C:\Users\YourName\PycharmProjects\ProjectName\venv\Scripts\python.exe"

# 临时数据存放 (确保你有权写入这个目录)
TEMP_DATA = os.path.join(os.environ["TEMP"], "ssdr_temp_data.npz").replace("\\", "/")
TEMP_WEIGHTS = os.path.join(os.environ["TEMP"], "ssdr_temp_weights.npy").replace("\\", "/")


# =====================================================

def run_integrated_ssdr(mesh_name, start_frame, end_frame, max_inf=6):
    # --- 0. 环境预检 ---
    if not os.path.exists(EXTERNAL_PYTHON):
        cmds.error(f"找不到 Python 解释器，请检查路径: {EXTERNAL_PYTHON}")
        return

    start_t = time.time()

    # --- 1. Maya 导出数据 ---
    print("Step 1: 正在导出 Maya 几何数据...")
    history = cmds.listHistory(mesh_name)
    sc_list = cmds.ls(history, type="skinCluster")
    if not sc_list:
        cmds.error("未找到 skinCluster")
        return
    sc = sc_list[0]
    joints = cmds.skinCluster(sc, q=True, influence=True)
    num_j = len(joints)

    mesh_dag = om.MGlobal.getSelectionListByName(mesh_name).getDagPath(0)
    mesh_fn = om.MFnMesh(mesh_dag)
    num_v = mesh_fn.numVertices

    bind_invs = [np.array(om.MMatrix(cmds.getAttr(f"{sc}.bindPreMatrix[{i}]"))).reshape(4, 4) for i in range(num_j)]

    frames = list(range(start_frame, end_frame + 1))
    all_v_pos = []
    all_j_mats = []

    curr_f = cmds.currentTime(q=True)
    for f in frames:
        cmds.currentTime(f)
        all_v_pos.append(np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3])
        all_j_mats.append([np.array(om.MMatrix(cmds.getAttr(f"{jnt}.worldMatrix[0]"))).reshape(4, 4) for jnt in joints])
    cmds.currentTime(curr_f)

    np.savez(TEMP_DATA, v_pos=np.array(all_v_pos), j_mats=np.array(all_j_mats),
             bind_invs=np.array(bind_invs), num_v=num_v, num_j=num_j)

    # --- 2. 外部解算 (静默) ---
    print("Step 2: 正在调用外部引擎解算 (请稍候)...")

    # 将逻辑写入独立脚本运行，避免命令行过长
    compute_script_content = f"""
import numpy as np
from scipy.optimize import nnls
try:
    data = np.load(r'{TEMP_DATA}')
    v_pos, j_mats, b_inv = data['v_pos'], data['j_mats'], data['bind_invs']
    num_v, num_j, num_f = int(data['num_v']), int(data['num_j']), v_pos.shape[0]

    eff = np.array([j_mats[f, j] @ b_inv[j] for f in range(num_f) for j in range(num_j)]).reshape(num_f, num_j, 4, 4)
    final_w = np.zeros((num_v, num_j))
    ref_h = np.ones((num_v, 4))
    ref_h[:, :3] = v_pos[0]

    for v in range(num_v):
        p_ref = ref_h[v]
        A = np.zeros((num_f * 3, num_j))
        for j in range(num_j):
            A[:, j] = (eff[:, j] @ p_ref)[:, :3].flatten()
        B = v_pos[:, v, :].flatten()

        # 数据中心化 (核心优化)
        Ac = A - np.mean(A, axis=0)
        Bc = B - np.mean(B)

        w, _ = nnls(Ac, Bc)
        if np.count_nonzero(w) > {max_inf}:
            w[np.argsort(w)[:-{max_inf}]] = 0
        if w.sum() > 1e-8: w /= w.sum()
        final_w[v] = w

    np.save(r'{TEMP_WEIGHTS}', final_w)
except Exception as e:
    with open(r'{TEMP_WEIGHTS}.log', 'w') as f:
        f.write(str(e))
"""
    # 使用 subprocess 运行
    # shell=True 可以增加兼容性，但在某些环境下需要 False
    proc = subprocess.Popen([EXTERNAL_PYTHON, "-c", compute_script_content],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    # --- 3. 错误检查与应用 ---
    if os.path.exists(TEMP_WEIGHTS + ".log"):
        with open(TEMP_WEIGHTS + ".log", 'r') as f:
            cmds.error("外部解算逻辑错误: " + f.read())
        return

    if not os.path.exists(TEMP_WEIGHTS):
        cmds.error("外部 Python 运行失败，未生成权重文件。错误信息: " + stderr.decode('gbk', 'ignore'))
        return

    print("Step 3: 应用权重...")
    weights = np.load(TEMP_WEIGHTS).flatten()
    sc_obj = om.MGlobal.getSelectionListByName(sc).getDependNode(0)
    sc_fn = oma.MFnSkinCluster(sc_obj)
    v_comp = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
    om.MFnSingleIndexedComponent(v_comp).addElements(om.MIntArray(range(num_v)))
    sc_fn.setWeights(mesh_dag, v_comp, om.MIntArray(range(num_j)), om.MDoubleArray(weights), normalize=True)

    print(f"解算成功！总用时: {time.time() - start_t:.2f}s")


# 运行
run_integrated_ssdr("bace_bs_Mesh1", 1, 35, max_inf=6)