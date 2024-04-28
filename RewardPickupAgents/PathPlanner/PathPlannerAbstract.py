import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union
from abc import ABCMeta, abstractmethod

from ..World import Node, Agent, World


class PathPlannerAbstract(metaclass=ABCMeta):
    """次の行動を選択するためのメソッド(get_next_actions_for_agents)を持つ抽象クラス

    Args:
        metaclass (ABCMeta): 抽象クラスを作成するためのメタクラス
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_next_actions_for_agents(self, world: World) -> Dict[int, Node]:
        """エージェントが次に起こす行動(Node)をDictで返すメソッド

        エージェントは隣接するノードを選択するか、その場に留まるかを選択する

        ※行動としてNode(0,0), Node(0,1), Node(0,-1), Node(1,0), Node(-1,0)の5つのノードのいずれかを選択することになる

        Args:
            world (World): ワールドクラス

        Returns:
            Dict[int, Node]: エージェントIDをキーとしてエージェントが次に起こす行動(Node)を値とするDict
        """
        raise NotImplementedError("get_next_actionsメソッドを実装してください")
