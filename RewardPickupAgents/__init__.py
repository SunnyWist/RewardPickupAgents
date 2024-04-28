# Description: シミュレーションを実行するためのスクリプトです。
import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union
from time import sleep

from .World import World, Node
from .parameter import *

""" 以下を変更してください """
from .PathPlanner.RandomWalk import RandomWalk as PathPlanner

""" 以上を変更してください """


def main():
    world = World(OBSTACLE_CSV_FILE_PATH, REWARD_CSV_FILE_PATH)
    print("(width, height) = ", world.environment.get_environment_size())
    if PRINT_MAP_IN_TEMINAL:
        world.print_map_state()
    next_nodes_selector = PathPlanner()

    step: int = 0
    agents_owned_reward: int = 0
    stored_reward: int = 0
    collision_count: int = 0

    AGENTS_COUNT = world.get_agents_count()
    ACTIONS_LIST = [Node(0, 1), Node(0, -1), Node(1, 0), Node(-1, 0), Node(0, 0)]

    while step < MAX_TIMESTEP:
        # 報酬を出現させる
        world.update_reward()
        # エージェントの移動
        new_acitons = next_nodes_selector.get_next_actions_for_agents(world)
        for i in range(AGENTS_COUNT):
            if not new_acitons[i] in ACTIONS_LIST:
                raise ValueError(
                    "エージェントが取れない行動を選択しようとしています。 Agent ID: {}, Node: {}".format(
                        i, new_acitons[i]
                    )
                )
            new_node = world.agents[i].get_node() + new_acitons[i]
            if not world.is_valid_node(new_node):
                raise ValueError(
                    "エージェントが範囲外もしくは障害物に移動しようとしています。 Agent ID: {}, Node: {}".format(
                        i, new_node
                    )
                )
            if world.get_agent_with_node(new_node):
                collision_count += 1
                continue
            world.agents[i].set_node(new_node)

        # 報酬の取得
        for agent in world.agents:
            world.earn_reward(agent)

        # 報酬の保管
        for agent in world.agents:
            store_point = world.get_store_point_with_node(agent.get_node())
            if store_point:
                store_point.store_reward(agent.owned_reward)
                agent.owned_reward = 0

        # 後処理
        step += 1
        agents_owned_reward = sum([agent.owned_reward for agent in world.agents])
        stored_reward = sum([store_point.stored_reward for store_point in world.store_points])

        if PRINT_MAP_IN_TEMINAL:
            print("Step", step)
            print("Agents Owned Reward", agents_owned_reward)
            print("Stored Reward", stored_reward)
            print("Collision Count", collision_count)
            world.print_map_state()
            sleep(1)

    print("Final Step", step)
    print("Final Agents Owned Reward", agents_owned_reward)
    print("Final Stored Reward", stored_reward)
    print("Final Collision Count", collision_count)


if __name__ == "__main__":
    main()
