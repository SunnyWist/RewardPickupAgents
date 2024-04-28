class MAP_STATE:
    OBSTACLE = "#"
    PASS_POINT = "."
    AGENT = "a"
    VAULT = "v"
    REWARD = "★"


# エージェントが一度に保持できる報酬の最大値
MAXIMUM_REWARDS_CAPACITY = 3

# 障害物の情報を持つcsvファイルのパス
OBSTACLE_CSV_FILE_PATH = "obstacle_data/obstacle1.csv"
# 報酬が出現する確率を持つcsvファイルのパス
REWARD_CSV_FILE_PATH = "reward_probability_data/reward1.csv"
# シミュレーションを行うステップ数
SIMULATION_TIMESTEP = 100
# ターミナルにマップを表示するかどうか
PRINT_MAP_IN_TEMINAL = False
