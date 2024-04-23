import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union

OBSTACLE = 1
PASS_POINT = 0

AGENT_STR = "a"
STORE_POINT_STR = "s"

MAXIMUM_REWARD = 3


@dataclass
class Node:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Node(self.x + other.x, self.y + other.y)


def get_adjacent_nodes(node: Node) -> List[Node]:
    """ノードの上下左右の隣接ノードを取得する関数

    Args:
        node (Node): 基準となるノード

    Returns:
        List[Node]: 隣接ノードのリスト
    """
    return [Node(node.x + d[0], node.y + d[1]) for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]]


class Agent:
    def __init__(self, agent_id: int, maximum_reward: int, node: Node):
        self.agent_id = agent_id
        self.maximum_reward = maximum_reward
        self.node = node
        self.owned_reward = 0

    def set_node(self, node: Node):
        self.node = node

    def get_id(self) -> int:
        return self.agent_id

    def get_maximum_reward(self) -> int:
        return self.maximum_reward

    def get_node(self) -> Node:
        return self.node


class StorePoint:
    def __init__(self, node: Node):
        self.node = node
        self.stored_reward = 0

    def store_reward(self, reward: int):
        self.stored_reward += reward

    def get_node(self) -> Node:
        return self.node

    def get_stored_reward(self) -> int:
        return self.stored_reward


class Environment:
    """事前に決められた環境を表す静的なクラス"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.obstacle_array: np.ndarray = np.zeros((width, height))
        self.reward_probability_array: np.ndarray = np.zeros((width, height))

    def set_obstacle_array(self, obstacle_array: np.ndarray):
        self.obstacle_array = obstacle_array

    def set_reward_probability_array(self, reward_probability_array: np.ndarray):
        self.reward_probability_array = reward_probability_array

    def get_environment_size(self):
        return self.width, self.height

    def is_obstacle(self, node: Node):
        return self.obstacle_array[node.x, node.y] == OBSTACLE

    def check_valid_node(self, node: Node) -> bool:
        if not (0 <= node.x < self.width) or not (0 <= node.y < self.height):
            return False
        if self.is_obstacle(node):
            return False
        return True

    def print_raw_map(self):
        for r in range(self.width):
            for c in range(self.height):
                print_str = ""
                if self.is_obstacle(Node(r, c)):
                    print_str = "■"
                else:
                    print_str = "□"
                print(print_str.rjust(2), end=" ")
            print()


class World:
    def __init__(self, obstacle_file: str, reward_probability_file: str):
        self.environment: Environment
        self.agents: List[Agent] = []
        self.agents_count = 0
        self.store_points: List[StorePoint] = []
        self.store_points_count = 0
        self.reward_array: np.ndarray
        self.load_maps(obstacle_file, reward_probability_file)

    def load_maps(self, obstacle_file: str, reward_probability_file: str):
        with open(obstacle_file, "r") as f:
            first_line = f.readline()
            width, height = map(int, first_line.strip().split(","))
            self.environment = Environment(width, height)
            obstacle_array = np.zeros((width, height))
            for i in range(width):
                line = f.readline()
                row_list = line.strip().split(",")
                for j, value in enumerate(row_list):
                    if value == str(PASS_POINT):
                        obstacle_array[i, j] = int(value)
                    elif value == str(OBSTACLE):
                        obstacle_array[i, j] = int(value)
                    elif value == AGENT_STR:
                        self.agents.append(Agent(self.agents_count, MAXIMUM_REWARD, Node(i, j)))
                        self.agents_count += 1
                    elif value == STORE_POINT_STR:
                        self.store_points.append(StorePoint(Node(i, j)))
                        self.store_points_count += 1
            self.environment.set_obstacle_array(obstacle_array)

        with open(reward_probability_file, "r") as f:
            first_line = f.readline()
            width, height = map(int, first_line.strip().split(","))
            if width != self.environment.width or height != self.environment.height:
                raise ValueError("Map size is different")
            reward_probability_array = np.zeros((width, height))
            for i in range(width):
                line = f.readline()
                row_list = line.strip().split(",")
                for j, value in enumerate(row_list):
                    reward_probability_array[i, j] = float(value)
            self.environment.set_reward_probability_array(reward_probability_array)
        self.reward_array = np.zeros((width, height))

    def update_reward(self):
        for r in range(self.environment.width):
            for c in range(self.environment.height):
                node = Node(r, c)
                # エージェントがいる場所には報酬を生成しない
                if self.get_agent_with_node(node):
                    continue
                prob = self.environment.reward_probability_array[r, c]
                if random.random() < prob:
                    self.reward_array[r, c] = 1

    def earn_reward(self, agent: Agent):
        reward = self.reward_array[agent.get_node().x, agent.get_node().y]
        if agent.get_maximum_reward() - agent.owned_reward < reward:
            reward = agent.get_maximum_reward() - agent.owned_reward
        agent.owned_reward += reward
        self.reward_array[agent.get_node().x, agent.get_node().y] -= reward
        return reward

    def get_agent_with_node(self, node: Node) -> Union[Agent, None]:
        for agent in self.agents:
            if agent.get_node() == node:
                return agent
        return None

    def get_store_point_with_node(self, node: Node) -> Union[StorePoint, None]:
        for store_point in self.store_points:
            if store_point.get_node() == node:
                return store_point
        return None

    def get_nearest_reward_node(self, node: Node) -> Union[Node, None]:
        min_distance = 10000
        nearest_node = None
        for r in range(self.environment.width):
            for c in range(self.environment.height):
                if self.reward_array[r, c] > 0:
                    reward_node = Node(r, c)
                    distance = abs(node.x - reward_node.x) + abs(node.y - reward_node.y)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_node = reward_node
        return nearest_node

    def print_map_state(self):
        width, height = self.environment.get_environment_size()
        for r in range(width):
            for c in range(height):
                print_str = ""
                agent = self.get_agent_with_node(Node(r, c))
                store_point = self.get_store_point_with_node(Node(r, c))
                color_start_str = ""
                color_end_str = ""
                if agent:
                    print_str = AGENT_STR
                    color_start_str = "\033[32m"
                    color_end_str = "\033[0m"
                elif store_point:
                    print_str = "s"
                    color_start_str = "\033[34m"
                    color_end_str = "\033[0m"
                elif self.environment.is_obstacle(Node(r, c)):
                    print_str = "■"
                elif self.reward_array[r, c] > 0:
                    print_str = "★"
                    color_start_str = "\033[33m"
                    color_end_str = "\033[0m"
                else:
                    print_str = "□"
                print(color_start_str + print_str.rjust(2) + color_end_str, end=" ")
            print()
