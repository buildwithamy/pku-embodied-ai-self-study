# 本章可运行演示，按页面顺序执行；不含学生TODO解答。

# HTML L880
import numpy as np

def unit_quat(q):
    q = np.array(q, dtype=float, copy=True)
    if q.shape != (4,) or not np.all(np.isfinite(q)):
        raise ValueError("四元数必须包含四个有限分量")
    norm = np.linalg.norm(q)
    if norm == 0:
        raise ValueError("零四元数不能表示旋转")
    return q / norm

def slerp(q1, q2, t):
    q1, q2 = unit_quat(q1), unit_quat(q2)
    dot = float(q1 @ q2)
    if dot < 0:
        q2, dot = -q2, -dot
    dot = np.clip(dot, 0.0, 1.0)
    if dot > 1 - 1e-8:
        return unit_quat((1-t)*q1 + t*q2)
    theta = np.arccos(dot)
    return unit_quat((np.sin((1-t)*theta)*q1 + np.sin(t*theta)*q2)
                     / np.sin(theta))

def nlerp(q1, q2, t):
    q1, q2 = unit_quat(q1), unit_quat(q2)
    if q1 @ q2 < 0:
        q2 = -q2
    return unit_quat((1-t)*q1 + t*q2)

# 两个相差 120° 的旋转（绕 z 轴）
q1 = np.array([np.cos(0), 0, 0, np.sin(0)])
q2 = np.array([np.cos(np.pi/3), 0, 0, np.sin(np.pi/3)])   # θ/2 = 60°

ts = np.linspace(0, 1, 11)
angles_slerp = [2*np.arccos(np.clip(np.abs(slerp(q1,q2,t) @ q1), -1, 1)) for t in ts]
angles_nlerp = [2*np.arccos(np.clip(np.abs(nlerp(q1,q2,t) @ q1), -1, 1)) for t in ts]
diff_s = np.diff(angles_slerp); diff_n = np.diff(angles_nlerp)
print("Slerp 相邻间隔:", np.round(diff_s, 4))   # 均匀！
print("Nlerp 相邻间隔:", np.round(diff_n, 4))   # 中间大两头小

# HTML L908
# q 与 -q 表示同一旋转：相对角度应为 0
q = np.array([np.cos(np.pi/6), np.sin(np.pi/6), 0, 0])   # 绕 x 转 60°
rel = 2*np.arccos(np.clip(np.abs(q @ (-q)), -1, 1))
print("q 与 -q 的旋转距离:", np.round(rel, 6), "（期望 0）")
assert rel < 1e-6

# 用 rotation.py 的 quat_to_mat 验证：R(q) == R(-q)
def quat_to_mat(q):
    w, x, y, z = q
    return np.array([
        [1-2*y*y-2*z*z, 2*x*y-2*w*z, 2*w*y+2*x*z],
        [2*x*y+2*w*z, 1-2*x*x-2*z*z, 2*y*z-2*w*x],
        [2*x*z-2*w*y, 2*w*x+2*y*z, 1-2*x*x-2*y*y]])
assert np.allclose(quat_to_mat(q), quat_to_mat(-q))
print("✓ R(q) 与 R(-q) 完全相同")

# HTML L928
samples = np.random.randn(10000, 4)
samples /= np.linalg.norm(samples, axis=1, keepdims=True)
axes = samples[:, 1:] / np.linalg.norm(samples[:, 1:], axis=1, keepdims=True)
mean = axes.mean(axis=0)
print("旋转轴均值（期望 ≈ 0 向量）:", np.round(mean, 4))
