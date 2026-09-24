# coding=utf-8
import maya.api.OpenMaya as om
import math


def maya_useNewAPI():
    pass


class TrueSplineIKNode(om.MPxNode):
    kNodeId = om.MTypeId(0x00141482+203)
    kNodeName = "trueSplineIK"

    # --- 属性定义 ---
    aInCurve = om.MObject()
    aCtrlMatrix = om.MObject()
    aRootParentInvMatrix = om.MObject()
    aBoneTranslates = om.MObject()
    aBoneOrients = om.MObject()
    aOutRootTranslate = om.MObject()
    aOutRotates = om.MObject()

    def __init__(self):
        super(TrueSplineIKNode, self).__init__()

    @classmethod
    def creator(cls):
        return TrueSplineIKNode()

    @classmethod
    def initialize(cls):
        nAttr = om.MFnNumericAttribute()
        mAttr = om.MFnMatrixAttribute()
        tAttr = om.MFnTypedAttribute()

        # 输入：样条曲线数据
        cls.aInCurve = tAttr.create("inCurve", "ic", om.MFnData.kNurbsCurve)
        # 输入：控制器的世界矩阵
        cls.aCtrlMatrix = mAttr.create("ctrlMatrix", "cmat")
        # 输入：根骨骼父级的世界逆矩阵（用于转回局部空间）
        cls.aRootParentInvMatrix = mAttr.create("rootParentInvMatrix", "rpim")

        # 输入数组：骨骼的原始 Translate 值（主要用到长度）
        cls.aBoneTranslates = nAttr.createPoint("boneTranslates", "bt")
        nAttr.array = True
        # 输入数组：骨骼的原始 Joint Orient（用于逆向抵消）
        cls.aBoneOrients = nAttr.createPoint("boneOrients", "bo")
        nAttr.array = True

        # 输出：根骨骼的局部位移
        cls.aOutRootTranslate = nAttr.createPoint("outRootTranslate", "ort")
        # 输出数组：每一节骨骼计算后的 Rotate 值
        cls.aOutRotates = nAttr.createPoint("outRotates", "orot")
        nAttr.array = True
        nAttr.usesArrayDataBuilder = True

        # 添加属性并设置影响关系
        attrs = [cls.aInCurve, cls.aCtrlMatrix, cls.aRootParentInvMatrix,
                 cls.aBoneTranslates, cls.aBoneOrients, cls.aOutRootTranslate, cls.aOutRotates]
        for a in attrs: cls.addAttribute(a)
        for src in attrs[:-2]:
            cls.attributeAffects(src, cls.aOutRootTranslate)
            cls.attributeAffects(src, cls.aOutRotates)

    # --------------------------------------------------------------------------
    # 核心函数 1：寻找下一个骨骼的 U 值 (球体与曲线求交)
    # --------------------------------------------------------------------------
    def find_next_u(self, curveFn, center_pos, u_start, radius):
        """
        逻辑：以 center_pos 为球心，radius 为半径，寻找在 u_start 之后的曲线交点。
        算法：1. 线性采样锁定符号变化区间； 2. 牛顿迭代法精确求根。
        """
        u_min, u_max = curveFn.knotDomain
        # 预采样：将剩余曲线分为 100 段，寻找交点所在的区间
        samples = 100
        du = (u_max - u_start) / float(samples)

        target_u = u_max  # 默认值（如果没找到则停在末尾）

        for i in range(samples):
            u1 = u_start + i * du
            u2 = u1 + du

            # 计算两采样点到球心的距离差（f(u) = distance - radius）
            p1 = curveFn.getPointAtParam(u1, om.MSpace.kWorld)
            p2 = curveFn.getPointAtParam(u2, om.MSpace.kWorld)
            f1 = (om.MVector(p1) - center_pos).length() - radius
            f2 = (om.MVector(p2) - center_pos).length() - radius

            # 如果符号发生变化，说明 f(u)=0 的根就在 u1 和 u2 之间
            if f1 * f2 <= 0:
                # 使用牛顿迭代法精确定位 (Newton-Raphson)
                u_refined = (u1 + u2) * 0.5
                for _ in range(10):  # 10次迭代足以达到极高精度
                    pt = curveFn.getPointAtParam(u_refined, om.MSpace.kWorld)
                    diff = om.MVector(pt) - center_pos
                    # 我们令 F(u) = |P(u) - C|^2 - R^2 = 0
                    f_val = diff.length() ** 2 - radius ** 2
                    if abs(f_val) < 1e-7: break

                    # 数值求导：F'(u)
                    delta = 1e-5
                    u_d = u_refined + delta if u_refined + delta <= u_max else u_refined - delta
                    pt_d = curveFn.getPointAtParam(u_d, om.MSpace.kWorld)
                    derivative = (om.MVector(pt_d) - om.MVector(pt)) / (u_d - u_refined)
                    df_val = 2.0 * (diff.x * derivative.x + diff.y * derivative.y + diff.z * derivative.z)

                    if abs(df_val) > 1e-10:
                        u_refined = u_refined - f_val / df_val

                target_u = max(u_min, min(u_max, u_refined))
                return target_u

        return target_u  # 若无交点，返回最大值

    # --------------------------------------------------------------------------
    # 核心函数 2：计算骨骼的世界旋转矩阵
    # --------------------------------------------------------------------------
    def compute_bone_rotation(self, p_curr, p_next, up_hint, bone_vec):
        """
        逻辑：根据当前点和下一点计算 Aim 矩阵，并适配骨骼自身的本地坐标轴。
        p_curr: 当前骨骼位置, p_next: 下一节骨骼位置, up_hint: Up 向量参考
        bone_vec: 骨骼本地的位移向量（决定了骨骼该朝哪个轴指向子节点）
        """
        # 1. 确定前向轴 (Forward)
        forward = (p_next - p_curr).normal()

        # 2. 构建正交基 (Gram-Schmidt)
        right = (up_hint ^ forward).normal()  # 叉乘得到右向量
        up = (forward ^ right).normal()  # 再次叉乘得到校准后的上向量

        # 3. 创建基础 Aim 矩阵 (默认 X 指向 Forward)
        # 注意：这里构造的是标准坐标系 [F, U, R]
        m_list = [forward.x, forward.y, forward.z, 0,
                  up.x, up.y, up.z, 0,
                  right.x, right.y, right.z, 0,
                  0, 0, 0, 1]
        m_aim = om.MMatrix(m_list)

        # 4. 骨骼轴向适配：如果骨骼的 Translate 不是 X 轴，需要补偿
        # 我们计算一个四元数，将骨骼原始位移方向 (bone_vec) 旋转到世界 Forward 方向
        local_dir = bone_vec.normal()
        # 默认假设 Aim 矩阵让世界 X轴 对齐 Forward，所以我们将 local_dir 转到 X轴 (1,0,0)
        q_align = om.MQuaternion(local_dir, om.MVector(1, 0, 0))

        # 最终矩阵 = 适配旋转 * 目标朝向矩阵
        final_mat = q_align.asMatrix() * m_aim
        return final_mat

    def compute(self, plug, dataBlock):
        if plug != self.aOutRootTranslate and plug != self.aOutRotates and plug.parent() != self.aOutRotates:
            return om.kUnknownParameter

        # --- 数据提取 ---
        curveHandle = dataBlock.inputValue(self.aInCurve)
        if curveHandle.data().isNull(): return
        curveFn = om.MFnNurbsCurve(curveHandle.asNurbsCurve())

        ctrlMat = dataBlock.inputValue(self.aCtrlMatrix).asMatrix()
        rootParentInvMat = dataBlock.inputValue(self.aRootParentInvMatrix).asMatrix()
        ctrlPos = om.MPoint(ctrlMat[12], ctrlMat[13], ctrlMat[14])

        hTrans = dataBlock.inputArrayValue(self.aBoneTranslates)
        hOrients = dataBlock.inputArrayValue(self.aBoneOrients)
        num_joints = len(hTrans)

        # --- 1. 计算根部起点 ---
        _, u_root = curveFn.closestPoint(ctrlPos, om.MSpace.kWorld)
        p_curr_vec = om.MVector(curveFn.getPointAtParam(u_root, om.MSpace.kWorld))
        u_curr = u_root

        # 输出根骨骼位移
        p_root_local = om.MPoint(p_curr_vec) * rootParentInvMat
        dataBlock.outputValue(self.aOutRootTranslate).set3Float(p_root_local.x, p_root_local.y, p_root_local.z)

        # --- 2. 链式迭代计算 ---
        world_matrices = []
        outBuilder = om.MArrayDataBuilder(dataBlock, self.aOutRotates, num_joints)

        # 初始 Up 向量参考
        current_up = om.MVector(rootParentInvMat.inverse()[4:7]).normal()

        for i in range(num_joints):
            # 获取当前骨骼到子骨骼的位移（确定长度和主轴）
            bone_vec = om.MVector(0, 0, 0)
            if i < num_joints - 1:
                hTrans.jumpToLogicalElement(i + 1)
                bone_vec = om.MVector(hTrans.inputValue().asFloatVector())

            length = bone_vec.length()

            # 如果没有长度或到末尾了，保持上一节的朝向
            if length < 0.001:
                m_w = world_matrices[-1] if world_matrices else om.MMatrix()
            else:
                # A. 调用函数：寻找下一个交点 U 值
                u_next = self.find_next_u(curveFn, p_curr_vec, u_curr, length)
                p_next_vec = om.MVector(curveFn.getPointAtParam(u_next, om.MSpace.kWorld))

                # B. 调用函数：计算朝向矩阵
                m_w = self.compute_bone_rotation(p_curr_vec, p_next_vec, current_up, bone_vec)

                # 更新迭代变量
                p_curr_vec = p_next_vec
                u_curr = u_next
                # 更新 Up 向量，防止骨骼在极弯曲处翻转（Parallel Transport 简化版）
                current_up = om.MVector(m_w[4], m_w[5], m_w[6])

            # 存储世界矩阵（需带上位置信息）
            m_final_list = list(m_w)
            m_final_list[12:15] = [p_curr_vec.x, p_curr_vec.y, p_curr_vec.z]
            world_matrices.append(om.MMatrix(m_final_list))

        # --- 3. 转换回局部 Rotate 并输出 ---
        for i in range(num_joints):
            m_world = world_matrices[i]
            # 计算局部矩阵：M_local = M_world * Parent_World_Inv
            m_parent_inv = rootParentInvMat if i == 0 else world_matrices[i - 1].inverse()
            m_local = m_world * m_parent_inv

            # 提取旋转：这里需要剔除 JointOrient 和 Translate 的影响
            hTrans.jumpToLogicalElement(i)
            t_vec = om.MVector(hTrans.inputValue().asFloatVector())
            hOrients.jumpToLogicalElement(i)
            jo_vec = om.MVector(hOrients.inputValue().asFloatVector())

            inv_t = om.MMatrix();
            inv_t[12], inv_t[13], inv_t[14] = -t_vec.x, -t_vec.y, -t_vec.z
            jo_mat = om.MEulerRotation(jo_vec.x, jo_vec.y, jo_vec.z).asMatrix()

            # 最终旋转矩阵 R = M_local * T^-1 * JO^-1
            r_mat = m_local * inv_t * jo_mat.inverse()
            euler = om.MTransformationMatrix(r_mat).rotation(asQuaternion=False)

            outBuilder.addElement(i).set3Float(euler.x, euler.y, euler.z)

        dataBlock.outputArrayValue(self.aOutRotates).set(outBuilder)
        dataBlock.setClean(plug)


def initializePlugin(plugin):
    om.MFnPlugin(plugin, "TechAnim", "4.0").registerNode(
        TrueSplineIKNode.kNodeName, TrueSplineIKNode.kNodeId,
        TrueSplineIKNode.creator, TrueSplineIKNode.initialize
    )


def uninitializePlugin(plugin):
    om.MFnPlugin(plugin).deregisterNode(TrueSplineIKNode.kNodeId)