import maya.cmds as cmds
import math


def distance_func_u(curve, center, u):
    pt = cmds.pointOnCurve(curve, parameter=u, position=True)
    dx = pt[0] - center[0]
    dy = pt[1] - center[1]
    dz = pt[2] - center[2]
    return dx * dx + dy * dy + dz * dz - 1.0


def newton_root(curve, center, u_guess, tol=1e-8, max_iter=20):
    u = u_guess
    for _ in range(max_iter):
        pt = cmds.pointOnCurve(curve, parameter=u, position=True)
        dx = pt[0] - center[0]
        dy = pt[1] - center[1]
        dz = pt[2] - center[2]
        f_val = dx * dx + dy * dy + dz * dz - 1.0
        if abs(f_val) < tol:
            return u
        # 使用 -tangent 获取单位切向量
        tangent = cmds.pointOnCurve(curve, parameter=u, tangent=True)
        df_val = 2 * (dx * tangent[0] + dy * tangent[1] + dz * tangent[2])
        if abs(df_val) < 1e-12:
            break
        u = u - f_val / df_val
        u = max(0.0, min(1.0, u))
    return None


def find_intersections(curve, center, samples=2000):
    u_list = [i / float(samples) for i in range(samples + 1)]
    f_list = [distance_func_u(curve, center, u) for u in u_list]
    intersections = []
    # 检查采样点本身
    for i, u in enumerate(u_list):
        if abs(f_list[i]) < 1e-6:
            pos = cmds.pointOnCurve(curve, parameter=u, position=True)
            intersections.append((u, pos))
    # 扫描符号变化区间
    for i in range(samples):
        if f_list[i] * f_list[i + 1] <= 0:
            u_mid = (u_list[i] + u_list[i + 1]) * 0.5
            u_root = newton_root(curve, center, u_mid)
            if u_root is not None:
                pos = cmds.pointOnCurve(curve, parameter=u_root, position=True)
                intersections.append((u_root, pos))
    # 去重
    if not intersections:
        return []
    intersections.sort(key=lambda x: x[0])
    merged = []
    last_u = -1.0
    for u, pos in intersections:
        if abs(u - last_u) > 1e-6:
            merged.append((u, pos))
            last_u = u
    return merged


def main():
    sel = cmds.ls(selection=True, type='nurbsCurve')
    if not sel:
        cmds.warning("请选择一条NURBS曲线")
        return
    curve = sel[0]

    result = cmds.promptDialog(title='输入u值', message='u值 (0~1):', button=['确定', '取消'])
    if result != '确定': return
    u_val = float(cmds.promptDialog(query=True, text=True))
    if not 0 <= u_val <= 1:
        cmds.warning("u值必须在0~1之间")
        return

    center = cmds.pointOnCurve(curve, parameter=u_val, position=True)
    sphere = cmds.polySphere(radius=1, name='temp_sphere')[0]
    cmds.move(center[0], center[1], center[2], sphere)

    intersections = find_intersections(curve, center, samples=3000)  # 提高采样
    if not intersections:
        cmds.warning("未找到交点，尝试增大samples参数")
        return

    max_u, max_pos = max(intersections, key=lambda x: x[0])
    loc = cmds.spaceLocator(name='contact_locator')[0]
    cmds.move(max_pos[0], max_pos[1], max_pos[2], loc)

    print("=" * 50)
    print("球心u值: {:.6f}".format(u_val))
    print("交点数量: {}".format(len(intersections)))
    print("所有u值: {}".format([round(u, 6) for u, _ in intersections]))
    print("最大u值: u={:.6f}, 位置={}".format(max_u, max_pos))
    print("=" * 50)


if __name__ == "__main__":
    main()