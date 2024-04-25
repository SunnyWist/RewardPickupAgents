class MAP_STATE:
    OBSTACLE = "#"
    PASS_POINT = "."
    AGENT = "a"
    STORE_POINT = "s"
    REWARD = "★"


MAXIMUM_REWARD = 3

# 障害物の情報を持つcsvファイルのパス
OBSTACLE_CSV_FILE_PATH = "obstacle_data/obstacle1.csv"
# 報酬が出現する確率を持つcsvファイルのパス
REWARD_CSV_FILE_PATH = "reward_probability_data/reward1.csv"
# シミュレーションを行うステップ数
MAX_TIMESTEP = 100
# ターミナルにマップを表示するかどうか
PRINT_MAP_IN_TEMINAL = True
