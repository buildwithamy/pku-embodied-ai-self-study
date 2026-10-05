# 本章可运行演示，按页面顺序执行；不含学生TODO解答。

# HTML L778
import numpy as np

# 环境：x' = x + a（动作就是速度）
def expert_policy(x):
    return 1.0 if x < 10 else 0.0

# 只收集 [0,1] 内的单步专家标注；不采集完整轨迹
np.random.seed(0)
data = []
for _ in range(20):
    x = np.random.uniform(0, 1)
    data.append((x, expert_policy(x)))
xs = np.array([d[0] for d in data])[:, None]
ys = np.array([d[1] for d in data])

# BC：最小二乘拟合线性策略（专家数据只覆盖 x∈[0,1] 附近！）
W = np.linalg.lstsq(np.hstack([xs, np.ones_like(xs)]), ys, rcond=None)[0]
bc = lambda x: W[0]*x + W[1]

# 闭环执行：从 x=0.5 出发，观察轨迹
x = 0.5; traj = [x]
for t in range(15):
    x += bc(x); traj.append(x)
print("BC 闭环轨迹终点:", np.round(traj[-1], 2), "（起点0.5、15步：专家终点为10.5）")
print("轨迹:", np.round(traj, 2))
print("训练状态范围:", xs.min(), xs.max())
print("训练MSE:", np.mean((xs[:,0]*W[0]+W[1]-ys)**2))
x_expert = 0.5
for _ in range(15): x_expert += expert_policy(x_expert)
print("专家闭环终点:", x_expert)

# HTML L813
# 专家在 x=0 处：一半概率 a=-1（左绕），一半概率 a=+1（右绕）
np.random.seed(1)
N = 1000
a_true = np.where(np.random.rand(N) < 0.5, -1.0, 1.0)
# 用「最小 MSE 估计」拟合单一动作（等价于 BC 回归）
a_bc = a_true.mean()
print("专家的两个峰: {-1, +1}，BC 预测:", np.round(a_bc, 3), "→ 撞上障碍物！")
