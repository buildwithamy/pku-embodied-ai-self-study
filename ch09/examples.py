"""策略梯度与专家似然的二元动作演算；不实现作业3的五个学生TODO。"""
import numpy as np

p = 0.3  # Bernoulli 策略，参数是 logit
actions = np.array([0.0, 1.0])
probabilities = np.array([1 - p, p])
scores = actions - p  # d log pi(a) / d logit
constant_return_pg = np.sum(probabilities * scores)
expert_mle = 1 - p  # 专家演示动作均为1
reward_pg = np.sum(probabilities * scores * actions)
assert np.isclose(constant_return_pg, 0)
assert np.isclose(expert_mle, 0.7)
assert np.isclose(reward_pg, 0.21)
print("恒回报 on-policy PG 梯度:", round(float(constant_return_pg), 6))
print("专家 a=1 的 BC 梯度:", expert_mle)
print("奖励 r=a 的 PG 梯度:", reward_pg)
