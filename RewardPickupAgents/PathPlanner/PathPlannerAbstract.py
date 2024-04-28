import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union
from abc import ABCMeta, abstractmethod

from ..World import Node, Agent, World


class PathPlanner(metaclass=ABCMeta):
    """次のノードを選ぶためのメソッド(get_next_nodes)を持つ抽象クラス

    Args:
        metaclass (ABCMeta): 抽象クラスを作成するためのメタクラス
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_next_nodes(self, world: World) -> Dict[int, Node]:
        """各々のエージェントが次に向かうノードをエージェントのIDに対するノードの辞書で返すメソッド

        Args:
            world (World): エージェントと環境を持つクラス

        Returns:
            Dict[int, Node]: エージェントIDをキーとしてエージェントが次に向かうノードを値とする辞書
        """
        raise NotImplementedError("get_next_nodesメソッドを実装してください")
