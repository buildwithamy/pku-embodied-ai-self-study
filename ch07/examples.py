# 本章可运行演示，按页面顺序执行；不含学生TODO解答。

# HTML L741
import numpy as np

def friction_cone_check(normals, mu=0.8):
    """判断一组接触法向的摩擦锥能否平衡任意二维平移力；忽略力矩。
    normals: (C,2) 接触点法向。每根法线张成的锥 = 法线 ± arctan(mu) 的扇形。"""
    alpha = np.arctan(mu)
    C = normals.shape[0]
    wrenches = []
    for n in normals:
        n = n / np.linalg.norm(n)
        # 锥的两个边界方向（2D 中锥退化为扇形）
        R = np.array([[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha), np.cos(alpha)]])
        wrenches.append(R @ n); wrenches.append(R.T @ n)
    F = np.column_stack(wrenches)               # (2,2C) 平移力方向矩阵；不含力矩
    rank_ok = np.linalg.matrix_rank(F) == 2
    # 条件2：严格正系数零组合 ⟺ 原点在凸包内部（用线性规划或采样判定）
    from scipy.spatial import ConvexHull
    pts = F.T
    if np.linalg.matrix_rank(pts - pts.mean(0)) < 2:
        return False
    hull = ConvexHull(pts)
    interior = bool(np.all(hull.equations[:, -1] < -1e-10))
    return rank_ok and interior

# 测试：对称的两根法线（左右夹）在 mu>0 时可平衡二维平移力
print(friction_cone_check(np.array([[1.,0],[-1,0]])))    # True
print(friction_cone_check(np.array([[1.,0],[0.7,0.7]])))  # False（同侧）

# HTML L773
def graspness_heuristic(pts, k=20, r=0.03):
    """对每个点，找 r 邻域内的点做 PCA：最小特征值对应法线方向；
    邻域越扁平，平面性分数越高；这不是完整 graspness，也不包含夹爪碰撞和接触稳定性。返回 (N,) 分数。"""
    from scipy.spatial import cKDTree
    tree = cKDTree(pts)
    scores = np.zeros(len(pts))
    for i, p in enumerate(pts):
        idx = tree.query_ball_point(p, r)
        if len(idx) < 8: continue
        nb = pts[idx] - p
        # PCA：协方差特征值 λ1≥λ2≥λ3；扁平 ⟺ λ3 远小于 λ1+λ2
        lambdas = np.linalg.eigvalsh(nb.T @ nb / len(nb))[::-1]
        flatness = 1 - lambdas[2] / (lambdas[0] + lambdas[1] + 1e-9)
        scores[i] = flatness
    return np.clip(scores, 0, 1)

# 相同点数和表面积量级的球面 / 平面表面采样；固定邻域半径
np.random.seed(42)
pts_sphere = np.random.randn(2000, 3)
pts_sphere *= 0.1 / np.linalg.norm(pts_sphere, axis=1, keepdims=True)
span = 0.1 * np.sqrt(np.pi)
pts_plane = np.column_stack([np.random.uniform(-span, span, (2000, 2)), np.zeros(2000)])
print("球面局部平面性均值:", np.round(graspness_heuristic(pts_sphere).mean(), 4))
print("平面局部平面性均值:", np.round(graspness_heuristic(pts_plane).mean(), 4))
