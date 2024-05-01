# obstacle_dataをもとに報酬の出現確率をランダムに決定する
import csv
import numpy as np

# 障害物の情報を持つcsvファイルのパス
OBSTACLE_DATA_PATH = "obstacle_data/obstacle1.csv"
# 報酬が出現する確率を持つcsvファイルのパス
REWARD_PROBABILITY_DATA_PATH = "reward_probability_data/randomized.csv"
# 報酬が出現する確率の最大値
PROB_MAX = 0.04
# 報酬が出現する確率の最小値
PROB_MIN = 0.001

obstacle_data = []
with open(OBSTACLE_DATA_PATH, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        obstacle_data.append(row)

prob_array = np.random.rand(len(obstacle_data), len(obstacle_data[0])) * (PROB_MAX - PROB_MIN) + PROB_MIN

for i in range(len(obstacle_data)):
    for j in range(len(obstacle_data[i])):
        if obstacle_data[i][j] != ".":
            prob_array[i, j] = 0


with open(REWARD_PROBABILITY_DATA_PATH, "w") as f:
    writer = csv.writer(f)
    writer.writerows(prob_array)
