import os
import datetime


class MAP_STATE:
    OBSTACLE = "#"
    PASS_POINT = "."
    AGENT = "a"
    VAULT = "v"
    REWARD = "★"


# エージェントが一度に保持できる報酬の最大値
MAXIMUM_REWARDS_CAPACITY = 3

# マップの縦横の長さ
MAP_WIDTH = 9
MAP_HEIGHT = 9
# 障害物の情報を持つcsvファイルのパス
OBSTACLE_CSV_FILE_PATH = "obstacle_data/obstacle1.csv"
# 報酬が出現する確率を持つcsvファイルのパス
REWARD_CSV_FILE_PATH = "reward_probability_data/randomized.csv"
# シミュレーションを行うステップ数
SIMULATION_TIMESTEP = 100
# ターミナルにマップを表示するかどうか
PRINT_MAP_IN_TEMINAL = False
# GIFアニメーションを作成するかどうか
CREATE_GIF = True
# GIFアニメーションの保存先, 現在時刻
GIF_SAVE_PATH = os.path.join("GIFs", datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".gif")
