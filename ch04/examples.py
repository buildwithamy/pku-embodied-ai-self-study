# 本章可运行演示，按页面顺序执行；不含学生TODO解答。

import numpy as np
import matplotlib.pyplot as plt

obstacles = [((30, 40), 8), ((60, 65), 10), ((75, 25), 7)]   # (圆心, 半径)

def in_collision(p):
    return any(np.linalg.norm(p - np.array(c)) <= r for c, r in obstacles)

def edge_free(a, b):
    d = b - a
    length2 = np.dot(d, d)
    for center, radius in obstacles:
        u = 0.0 if length2 == 0 else np.clip(np.dot(np.array(center)-a, d) / length2, 0, 1)
        if np.linalg.norm(a + u*d - np.array(center)) <= radius:
            return False
    return True

q_start, q_goal = np.array([5., 5.]), np.array([95., 95.])
V = [q_start]; parent = [-1]; eps = 4; beta = 0.1
np.random.seed(42)

for i in range(2000):
    q_target = q_goal if np.random.rand() < beta else np.random.rand(2)*100
    idx = min(range(len(V)), key=lambda j: np.linalg.norm(V[j]-q_target))
    d = q_target - V[idx]; distance = np.linalg.norm(d)
    if distance < 1e-12: continue
    q_new = V[idx] + min(eps, distance) * d / distance
    if np.any(q_new < 0) or np.any(q_new > 100): continue
    if not in_collision(q_new) and edge_free(V[idx], q_new):
        V.append(q_new); parent.append(idx)
        if np.linalg.norm(q_new - q_goal) < eps and edge_free(q_new, q_goal):
            V.append(q_goal.copy()); parent.append(len(V)-2)
            print("已验证并连接目标！"); break

# 回溯路径并可视化（略：画障碍圆、树边、最终路径）

import numpy as np

dt, T = 0.01, 10.0
ts = np.arange(0, T, dt)
theta = 0.0; theta_d = 0.0
Kp, Ki = 8.0, 12.0

errs_p, errs_pi = [], []
theta_p = theta_pi = 0.0
integral = 0.0
for t in ts:
    theta_d = 1.0 * t          # 目标以恒速 1 移动
    # P 控制：theta_dot = Kp * err
    theta_p += Kp * (theta_d - theta_p) * dt
    errs_p.append(1.0 * (t + dt) - theta_p)
    # PI 控制：theta_dot = Kp*err + Ki*∫err
    e = theta_d - theta_pi
    integral += e * dt
    theta_pi += (Kp * e + Ki * integral) * dt
    errs_pi.append(1.0 * (t + dt) - theta_pi)

print("P  稳态误差:", np.round(errs_p[-1], 4))
print("PI 稳态误差:", np.round(errs_pi[-1], 4))   # 应趋近 0
