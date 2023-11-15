import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
import random
import sys
# 设置字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
def simulate_synthesis_dynamic_with_recording(start_a, start_b, target_a, target_b, target_c, iterations=1000):
    total_a, total_b, total_c = [], [], []

    for _ in range(iterations):
        a, b, c = start_a, start_b, 0
        strategy = 'a'  # 初始策略为策略a

        # A转B，动态调整策略
        while a >= 3 and a - 3 >= target_a:
            if b >= target_b:  # 当B接近需求量时考虑切换到策略b
                strategy = 'b'
            a -= 3
            b += 1
            if strategy == 'a' and random.random() < 0.25:
                a += 1
            elif strategy == 'b' and random.random() < 0.10:
                b += 1

        # B转C，策略同上
        while b >= 3 and b - 3 >= target_b and c < target_c:
            b -= 3
            c += 1
            if strategy == 'a' and random.random() < 0.25:
                b += 1
            elif strategy == 'b' and random.random() < 0.10:
                c += 1

        total_a.append(a)
        total_b.append(b)
        total_c.append(c)

    return total_a, total_b, total_c
def simulate_synthesis_strict_with_recording(start_a, start_b, target_a, target_b, target_c, strategy, iterations=1000):
    total_a, total_b, total_c = [], [], []

    for _ in range(iterations):
        a, b, c = start_a, start_b, 0

        # A转B
        while a >= 3 and a - 3 >= target_a and (b < target_b or (b % 3 != 0 or target_b % 3 == 0 or target_b == 0)):
            a -= 3
            b += 1
            if strategy == 'a' and random.random() < 0.25:
                a += 1
            elif strategy == 'b' and random.random() < 0.10:
                b += 1

        # B转C
        while b >= 3 and b - 3 >= target_b and c < target_c:
            b -= 3
            c += 1
            if strategy == 'a' and random.random() < 0.25:
                b += 1
            elif strategy == 'b' and random.random() < 0.10:
                c += 1

        total_a.append(a)
        total_b.append(b)
        total_c.append(c)

    return total_a, total_b, total_c
# 用户输入
userinput = False
if userinput:
    print("ABC最大数量为9999且ABC等级依次升高\n")
    start_a, start_b, start_c = int(input("初始A:")), int(input("初始B:")), int(input("初始C（其实没用）:"))  # 初始数量
    target_a, target_b, target_c = int(input("期望A:")), int(input("期望B:")), int(input("期望C(9999为尽可能大）:"))
else:
    start_a, start_b, start_c = 330, 150, 0  # 初始数量
    target_a, target_b, target_c = 0, 66, 9999  # 期望数量（C如希望尽可能多输入9999）

# 模拟三种策略
record_a_a, record_b_a, record_c_a = simulate_synthesis_strict_with_recording(start_a, start_b, target_a, target_b, target_c, 'a')
record_a_b, record_b_b, record_c_b = simulate_synthesis_strict_with_recording(start_a, start_b, target_a, target_b, target_c, 'b')
record_a_d, record_b_d, record_c_d = simulate_synthesis_dynamic_with_recording(start_a, start_b, target_a, target_b, target_c)

# 计算平均值
avg_a_a, avg_b_a, avg_c_a = sum(record_a_a) / len(record_a_a), sum(record_b_a) / len(record_b_a), sum(record_c_a) / len(record_c_a)
avg_a_b, avg_b_b, avg_c_b = sum(record_a_b) / len(record_a_b), sum(record_b_b) / len(record_b_b), sum(record_c_b) / len(record_c_b)
avg_a_d, avg_b_d, avg_c_d = sum(record_a_d) / len(record_a_d), sum(record_b_d) / len(record_b_d), sum(record_c_d) / len(record_c_d)


#控制台输出
print("方法A (25%返还):")
print(f"A均值: {avg_a_a}, B均值: {avg_b_a}, C均值: {avg_c_a}")
print("\n方法B (10%双倍产出):")
print(f"A均值: {avg_a_b}, B均值: {avg_b_b}, C均值: {avg_c_b}")
print("\n方法D (动态算法):")
print(f"A均值: {avg_a_d}, B均值: {avg_b_d}, C均值: {avg_c_d}")

# 折线图绘制
iterations_range = range(1, 1001)
# 绘制图表
plt.figure(figsize=(5, 15))

# A材料剩余
plt.subplot(3, 1, 1)
plt.plot(iterations_range, record_a_a, label='策略A', color='blue', alpha=0.5)
plt.plot(iterations_range, record_a_b, label='策略B', color='red', alpha=0.5)
plt.plot(iterations_range, record_a_d, label='动态策略', color='green', alpha=0.5)
plt.axhline(y=avg_a_a, color='blue', linestyle='--')
plt.axhline(y=avg_a_b, color='red', linestyle='--')
plt.axhline(y=avg_a_d, color='green', linestyle='--')
plt.title('A材料剩余')
plt.xlabel('迭代次数')
plt.ylabel('数量')
plt.legend()

# B材料剩余
plt.subplot(3, 1, 2)
plt.plot(iterations_range, record_b_a, label='策略A', color='blue', alpha=0.5)
plt.plot(iterations_range, record_b_b, label='策略B', color='red', alpha=0.5)
plt.plot(iterations_range, record_b_d, label='动态策略', color='green', alpha=0.5)
plt.axhline(y=avg_b_a, color='blue', linestyle='--')
plt.axhline(y=avg_b_b, color='red', linestyle='--')
plt.axhline(y=avg_b_d, color='green', linestyle='--')
plt.title('B材料剩余')
plt.xlabel('迭代次数')
plt.ylabel('数量')
plt.legend()

# C材料产出
plt.subplot(3, 1, 3)
plt.plot(iterations_range, record_c_a, label='策略A', color='blue', alpha=0.5)
plt.plot(iterations_range, record_c_b, label='策略B', color='red', alpha=0.5)
plt.plot(iterations_range, record_c_d, label='动态策略', color='green', alpha=0.5)
plt.axhline(y=avg_c_a, color='blue', linestyle='--')
plt.axhline(y=avg_c_b, color='red', linestyle='--')
plt.axhline(y=avg_c_d, color='green', linestyle='--')
plt.title('C材料产出')
plt.xlabel('迭代次数')
plt.ylabel('数量')
plt.legend()

plt.tight_layout()
plt.show()

# 版权声明:
# 版权所有 (c) 2023 azzbm
# 此代码为公共领域作品，任何人均可自由复制、修改、分发和使用，无论是商业还是非商业目的。无需请求许可。
