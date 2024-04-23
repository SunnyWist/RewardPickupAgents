import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union

from World import Node, Agent, World
from util import *


def get_all_agent_nodes(world: World) -> Dict[int, Node]:
    return_dict: Dict[int, Node] = {}  # agent_id: Node
    action_list: List[Node] = [
        Node(0, 1),
        Node(0, -1),
        Node(1, 0),
        Node(-1, 0),
        Node(0, 0),
    ]  # エージェントは上下左右に移動するか、その場に留まる
    for agent in world.agents:
        selected_action = random.choice(action_list)
        return_dict[agent.agent_id] = agent.node + selected_action
    return return_dict
