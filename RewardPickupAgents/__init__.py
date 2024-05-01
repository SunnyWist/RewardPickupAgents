# Description: シミュレーションを実行するためのスクリプトです。
import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union
from time import sleep

from .World import World, Node
from .parameter import *
from .GIFMaker import GIFMaker

""" 以下を変更してください """
from .PathPlanner.RandomWalk import RandomWalk as PathPlanner

""" 以上を変更してください """


def main():
    world = World(MAP_WIDTH, MAP_HEIGHT, OBSTACLE_CSV_FILE_PATH, REWARD_CSV_FILE_PATH)
    print("(width, height) = ", world.get_environment_size())
    if PRINT_MAP_IN_TEMINAL:
        world.print_map_state()
    next_nodes_selector = PathPlanner()

    step: int = 0
    agents_owned_rewards: int = 0
    stored_rewards: int = 0
    collision_count: int = 0
    if CREATE_GIF:
        gif_maker = GIFMaker(world.get_obstacle_data(), world.get_agents_count(), world.get_vaults_count())
        gif_maker.update(
            step, stored_rewards, world.get_reward_array(), world.get_agents_pos_dict(), world.get_vaults_pos_dict()
        )

    AGENTS_COUNT = world.get_agents_count()
    ACTIONS_LIST = [Node(0, 1), Node(0, -1), Node(1, 0), Node(-1, 0), Node(0, 0)]

    while step < SIMULATION_TIMESTEP:
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
            vault = world.get_vault_with_node(agent.get_node())
            if vault:
                vault.store_rewards(agent.owned_reward)
                agent.owned_reward = 0

        # 後処理
        step += 1
        agents_owned_rewards = sum([agent.owned_reward for agent in world.agents])
        stored_rewards = sum([vault.stored_rewards for vault in world.vaults])
        if CREATE_GIF:
            gif_maker.update(
                step, stored_rewards, world.get_reward_array(), world.get_agents_pos_dict(), world.get_vaults_pos_dict()
            )

        if PRINT_MAP_IN_TEMINAL:
            print("Step", step)
            print("Agents Owned Reward", agents_owned_rewards)
            print("Stored Reward", stored_rewards)
            print("Collision Count", collision_count)
            world.print_map_state()
            sleep(1)

    print("Final Step", step)
    print("Final Agents Owned Reward", agents_owned_rewards)
    print("Final Stored Reward", stored_rewards)
    print("Final Collision Count", collision_count)
    if CREATE_GIF:
        gif_maker.save_gif(GIF_SAVE_PATH)


if __name__ == "__main__":
    main()
