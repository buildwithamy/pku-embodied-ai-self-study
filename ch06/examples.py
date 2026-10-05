# 本章可运行演示，按页面顺序执行；不含学生TODO解答。

import numpy as np

def icp(P, Q, max_iter=50, tol=1e-6):
    """点云配准：P (3,n) 源点云 → 对齐 Q (3,m) 目标点云，返回 (R, t, P_aligned)"""
    P = P.copy()
    R_total, t_total = np.eye(3), np.zeros(3)
    for it in range(max_iter):
        # 1. 找最近邻对应（暴力版即可，点少）
        corr = []
        for p in P.T:
            j = np.argmin(np.linalg.norm(Q.T - p, axis=1))
            corr.append(Q[:, j])
        Q_corr = np.array(corr).T

        # 2. 中心化
        cP, cQ = P - P.mean(1, keepdims=True), Q_corr - Q_corr.mean(1, keepdims=True)

        # 3. 带约束 Procrustes（第 5 章公式）
        U, _, Vt = np.linalg.svd(cQ @ cP.T)
        D = np.diag([1, 1, np.linalg.det(U @ Vt)])
        R = U @ D @ Vt
        t = Q_corr.mean(1) - R @ P.mean(1)

        # 4. 更新并检查收敛
        P_new = R @ P + t[:, None]
        movement = np.linalg.norm(P_new - P)
        R_total, t_total = R @ R_total, R @ t_total + t
        P = P_new
        if movement < tol: break
    return R_total, t_total, P

# 生成测试：非对称点云与较小位姿扰动，验证局部精修
np.random.seed(0)
Q = np.random.randn(3, 300) * np.array([[1.0], [0.7], [0.3]])
angle = 0.03
R_true = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
t_true = np.array([0.01, -0.02, 0.01])
P = R_true @ Q + t_true[:, None]
R, t, P_align = icp(P, Q)
print("旋转误差:", np.round(np.linalg.norm(R - R_true.T), 6))
print("平移误差:", np.round(np.linalg.norm(t + R_true.T @ t_true), 6))   # 应接近 0

def umeyama(P, Q):
    """7DoF 相似变换：s*R*p + t = q（P、Q 已一一对应）"""
    cP, cQ = P - P.mean(1, keepdims=True), Q - Q.mean(1, keepdims=True)
    # 对应点最小二乘尺度；无噪声时也等于 RMS 比
    U, singular_values, Vt = np.linalg.svd(cQ @ cP.T)
    D = np.diag([1, 1, np.linalg.det(U @ Vt)])
    R = U @ D @ Vt
    s = np.sum(singular_values * np.diag(D)) / np.sum(cP**2)
    t = Q.mean(1) - s * R @ P.mean(1)
    return s, R, t

# 测试：随机 3D 点云 + 随机相似变换
P0 = np.random.rand(3, 100)
s_t, R_t, t_t = 1.5, np.eye(3), np.array([1., -2., 3.])
s, R, t = umeyama(P0, s_t * R_t @ P0 + t_t[:, None])
assert np.allclose(s, s_t, atol=1e-9) and np.allclose(R, R_t, atol=1e-9) and np.allclose(t, t_t, atol=1e-9)
print("✓ Umeyama 恢复的 (s, R, t) 与真值一致")

def force_closure_2d(normals):
    """normals: (C,2) 法向力；仅平移，原点严格在满维凸包内部"""
    from scipy.spatial import ConvexHull
    if len(normals) < 3 or np.linalg.matrix_rank(normals - normals.mean(0)) < 2:
        return False
    hull = ConvexHull(normals)
    # 半空间 n·x+b ≤ 0：x=0 严格在内部要求所有 b < 0
    return bool(np.all(hull.equations[:, -1] < -1e-10))

print(force_closure_2d(np.array([[1,0],[-0.5,0.866],[-0.5,-0.866]])))  # 120°分布 → True
print(force_closure_2d(np.array([[1,0],[1,0.1],[-0.5,0.2]])))    # 集中在同一侧 → False
