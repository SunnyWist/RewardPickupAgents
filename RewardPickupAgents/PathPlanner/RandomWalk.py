# エージェントがランダムウォークを行うプログラム
import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union

from ..World import Node, Agent, World
from .PathPlannerAbstract import PathPlannerAbstract
from .util import *


class RandomWalk(PathPlannerAbstract):
    def __init__(self):
        pass

    def get_next_actions_for_agents(self, world: World) -> Dict[int, Node]:
        return_dict: Dict[int, Node] = {}  # agent_id: Node
        agents = world.get_agents_list()
        for agent in agents:
            # エージェントが取れる行動を取得
            valid_actions = world.get_valid_next_actions_for_agents(agent)
            # 取れる行動の中からランダムに1つ選択
            selected_action = random.choice(valid_actions)
            return_dict[agent.get_id()] = selected_action

        return return_dict
