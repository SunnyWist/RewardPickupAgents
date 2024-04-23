import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union

from World import Node, Agent, World
from util import *

# エージェントが向かうノードを格納するdict
agent_forward_nodes: Dict[int, Union[Node, None]] = {}  # agent_id: Node


def get_all_agent_nodes(world: World) -> Dict[int, Node]:
    return_dict: Dict[int, Node] = {}  # agent_id: Node
    action_list: List[Node] = [
        Node(0, 1),
        Node(0, -1),
        Node(1, 0),
        Node(-1, 0),
        Node(0, 0),
    ]  # エージェントは上下左右に移動するか、その場に留まる

    # エージェントが向かうノードを格納するdictを初期化
    for agent in world.agents:
        agent_forward_nodes[agent.agent_id] = None

    # エージェントの現在位置と向かうノードが同じの場合、向かうノードを未定義にする
    for agent in world.agents:
        if agent_forward_nodes[agent.agent_id] is None:
            continue
        if agent.node == agent_forward_nodes[agent.agent_id]:
            agent_forward_nodes[agent.agent_id] = None

    # エージェントが向かうノードが未定義の場合、持っている報酬が最大ならば報酬を保管するノードに向かう
    # そうでない場合は最寄りの報酬のあるノードに向かう
    for agent in world.agents:
        if agent_forward_nodes[agent.agent_id] is None:
            if agent.owned_reward == agent.maximum_reward:
                store_points = world.store_points
                store_point_nodes = [store_point.node for store_point in store_points]
                store_point_nodes.sort
                agent_forward_nodes[agent.agent_id] = store_point_nodes[0]
            else:
                nearest_reward_node = world.get_nearest_reward_node(agent.node)
                agent_forward_nodes[agent.agent_id] = nearest_reward_node

    # それぞれのエージェントに対してA*探索を行い、次のノードを取得
    for agent in world.agents:
        agent_forward_node = agent_forward_nodes[agent.agent_id]
        if agent_forward_node is None:
            continue
        best_path = get_astar_path(world.environment.obstacle_array, agent.node, agent_forward_node)
        if best_path is None:
            continue
        return_dict[agent.agent_id] = best_path[1]

    return return_dict
