"""
このプログラムはデッドロックを起こします。その解決がヒントになるかもしれません。
"""

import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union

from ..World import Node, Agent, World
from .PathPlannerAbstract import PathPlannerAbstract
from .util import *


class AStarPath(PathPlannerAbstract):
    def __init__(self):
        # エージェントが向かうノードを格納するdict
        self.agent_forward_nodes: Dict[int, Union[Node, None]] = {}  # get_id(): Node

    def get_next_actions_for_agents(self, world: World) -> Dict[int, Node]:
        return_dict: Dict[int, Node] = {}  # get_id(): Node

        agents = world.get_agents_list()

        # エージェントが向かうノードを格納するdictを初期化
        if len(self.agent_forward_nodes) == 0:
            for agent in agents:
                self.agent_forward_nodes[agent.get_id()] = None

        # エージェントの現在位置と向かうノードが同じの場合、向かうノードを未定義にする
        for agent in agents:
            if self.agent_forward_nodes[agent.get_id()] is None:
                continue
            if agent.get_node() == self.agent_forward_nodes[agent.get_id()]:
                self.agent_forward_nodes[agent.get_id()] = None

        # エージェントが向かうノードが未定義の場合、持っている報酬が最大ならば報酬を保管するノードに向かう
        # そうでない場合は最寄りの報酬のあるノードに向かう
        for agent in agents:
            if self.agent_forward_nodes[agent.get_id()] is None:
                if agent.get_owned_reward() == agent.get_maximum_reward():
                    store_points = world.store_points
                    store_point_nodes = [store_point.node for store_point in store_points]
                    store_point_nodes.sort
                    self.agent_forward_nodes[agent.get_id()] = store_point_nodes[0]
                else:
                    nearest_reward_node = world.get_nearest_reward_node(agent.get_node())
                    self.agent_forward_nodes[agent.get_id()] = nearest_reward_node

        # それぞれのエージェントに対してA*探索を行い、次の行動を選択
        for agent in agents:
            agent_forward_node = self.agent_forward_nodes[agent.get_id()]
            if agent_forward_node is None:
                return_dict[agent.get_id()] = Node(0, 0)
                continue
            best_path = get_astar_path(world, agent.get_node(), agent_forward_node)
            if best_path is None:
                raise ValueError
            next_node = best_path[1]
            return_dict[agent.get_id()] = next_node - agent.get_node()

        return return_dict
