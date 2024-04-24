import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union
from time import sleep

from .World import World
from .parameter import *

""" 以下を変更してください """
from .NextNodesSelector.AStarPath import AStarPath as NextNodesSelector

""" 以上を変更してください """


def main():
    world = World(OBSTACLE_CSV_FILE_PATH, REWARD_CSV_FILE_PATH)
    print(world.environment.get_environment_size())
    world.print_map_state()
    next_nodes_selector = NextNodesSelector()

    step = 0
    agents_owned_reward = 0
    stored_reward = 0
    collision_count = 0

    while step < MAX_TIMESTEP:
        world.update_reward()
        # エージェントの移動
        new_node_dict = next_nodes_selector.get_next_nodes(world)
        for i in range(len(world.agents)):
            if not world.environment.check_valid_node(new_node_dict[i]):
                raise ValueError("エージェントが範囲外もしくは障害物に移動しようとしています。")
            if world.get_agent_with_node(new_node_dict[i]):
                collision_count += 1
                continue
            world.agents[i].set_node(new_node_dict[i])

        # 報酬の取得
        for agent in world.agents:
            world.earn_reward(agent)

        # 報酬の保管
        for agent in world.agents:
            store_point = world.get_store_point_with_node(agent.get_node())
            if store_point:
                store_point.store_reward(agent.owned_reward)
                agent.owned_reward = 0

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
