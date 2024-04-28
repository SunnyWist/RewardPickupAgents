# Description: 経路計画プログラムに役立つ関数をまとめたモジュール
import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union

from ..World import Node, Environment, World


def get_adjacent_nodes(node: Node) -> List[Node]:
    """ノードの上下左右の隣接ノードを取得する関数

    Args:
        node (Node): 基準となるノード

    Returns:
        List[Node]: 隣接ノードのリスト
    """
    return [Node(node.x + d[0], node.y + d[1]) for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]]


def get_manhattan_distance(node1: Node, node2: Node) -> int:
    """2ノード間のマンハッタン距離を計算する関数

    Args:
        node1 (Node): ノード1
        node2 (Node): ノード2

    Returns:
        int: マンハッタン距離
    """
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


def get_euclidean_distance(node1: Node, node2: Node) -> float:
    """2ノード間のユークリッド距離を計算する関数

    Args:
        node1 (Node): ノード1
        node2 (Node): ノード2

    Returns:
        float: ユークリッド距離
    """
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5


def get_astar_path(world: World, node1: Node, node2: Node) -> Union[List[Node], None]:
    """2ノード間の最短経路を返す関数

    Args:
        world (World): ワールドインスタンス
        node1 (Node): ノード1
        node2 (Node): ノード2

    Returns:
        List[Node]: 経路、経路が存在しない場合はNone
    """

    class AStarNode:
        def __init__(self, node: Node, g: int, h: float, trajectory: List[Node] = []):
            self.node = node
            self.g = g
            self.h = h
            self.trajectory: List[Node] = trajectory

        def get_f(self):
            return self.g + self.h

        def __eq__(self, other):
            return self.node == other.node

        def __lt__(self, other):
            return self.get_f() < other.get_f()

    env: Environment = world.environment

    if env.is_obstacle(node1) or env.is_obstacle(node2):
        return None

    new_node1 = AStarNode(node1, 0, get_manhattan_distance(node1, node2))

    open_list: List[AStarNode] = [new_node1]
    close_list: List[AStarNode] = []
    while len(open_list) > 0:
        current_node = open_list.pop(0)
        close_list.append(current_node)
        if current_node.node == node2:
            return [*current_node.trajectory, node2]
        for new_node in get_adjacent_nodes(current_node.node):
            next_node = AStarNode(
                new_node,
                current_node.g + 1,
                get_manhattan_distance(new_node, node2),
                [*current_node.trajectory, current_node.node],
            )
            if not env.check_valid_node(next_node.node):
                continue
            if next_node in close_list:
                index = close_list.index(next_node)
                if close_list[index] > next_node:
                    close_list.pop(index)
                    open_list.append(next_node)
                else:
                    continue
            if next_node in open_list:
                index = open_list.index(next_node)
                if open_list[index] > next_node:
                    open_list[index] = next_node
            else:
                open_list.append(next_node)
        open_list.sort()
    return None


def get_astar_distance(world: World, node1: Node, node2: Node) -> int:
    """2ノード間の最短距離をA*探索で計算する関数

    Args:
        world (World): ワールドインスタンス
        node1 (Node): ノード1
        node2 (Node): ノード2

    Returns:
        int: 最短距離、経路が存在しない場合は-1
    """
    path = get_astar_path(world, node1, node2)
    if path is None:
        return -1
    return len(path) - 1
