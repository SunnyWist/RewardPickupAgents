import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Union, Tuple

from .parameter import *


@dataclass
class Node:
    """マップのノード(セル)を表す構造体

    等価比較(==)と加算(+)、減算(-)をサポートしている
    """

    x: int
    y: int

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other) -> "Node":
        if not isinstance(other, Node):
            raise ValueError("Addition is only supported for Node")
        return Node(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Node":
        if not isinstance(other, Node):
            raise ValueError("Subtraction is only supported for Node")
        return Node(self.x - other.x, self.y - other.y)


class Agent:
    """マップ上で移動するエージェントを表すクラス

    Args:
        agent_id (int): エージェントのID (0...n-1)
        maximum_reward (int): エージェントが運搬できる最大の報酬
        node (Node): エージェントの現在位置
    """

    def __init__(self, agent_id: int, maximum_reward: int, node: Node):
        self.agent_id = agent_id
        self.maximum_reward = maximum_reward
        self.node = node
        self.owned_reward = 0

    def set_node(self, node: Node):
        """エージェントの位置を更新するメソッド

        Args:
            node (Node): 新しいエージェントの位置
        """
        self.node = node

    def get_id(self) -> int:
        """エージェントのIDを取得するメソッド

        Returns:
            int: エージェントのID
        """
        return self.agent_id

    def get_maximum_rewards_capacity(self) -> int:
        """エージェントが運べる最大の報酬を取得するメソッド

        Returns:
            int: エージェントが運べる最大の報酬
        """
        return self.maximum_reward

    def get_node(self) -> Node:
        """エージェントの現在位置を取得するメソッド

        Returns:
            Node: エージェントの現在位置
        """
        return self.node

    def get_owned_rewards(self) -> int:
        """エージェントが保有している報酬を取得するメソッド

        Returns:
            int: エージェントが保有している報酬
        """
        return self.owned_reward


class Vault:
    """報酬の保管庫を表すクラス

    Args:
        node (Node): 報酬の保管庫の位置
    """

    def __init__(self, node: Node):
        self.node = node
        self.stored_rewards = 0

    def store_rewards(self, rewards: int):
        """報酬を保管庫に格納するメソッド

        Args:
            rewards (int): 保管する報酬
        """
        self.stored_rewards += rewards

    def get_node(self) -> Node:
        """保管庫のノードを取得するメソッド

        Returns:
            Node: 報酬を保管する場所の位置
        """
        return self.node

    def get_stored_rewards(self) -> int:
        """保管されている報酬を取得するメソッド

        Returns:
            int: 保管されている報酬
        """
        return self.stored_rewards


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

    def get_environment_size(self) -> tuple[int, int]:
        """環境の横幅と縦幅を取得するメソッド

        Returns:
            tuple[int, int]: 環境の横幅と縦幅
        """
        return self.width, self.height

    def is_obstacle(self, node: Node) -> bool:
        """指定したノードが障害物かどうかを判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードが障害物の場合はTrue, それ以外はFalse
        """
        return self.obstacle_array[node.x, node.y] == 1

    def is_in_environment(self, node: Node) -> bool:
        """指定したノードが環境内にあるかどうかを判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードが環境内にある場合はTrue, それ以外はFalse
        """
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def is_valid_node(self, node: Node) -> bool:
        """指定したノードが有効であるか(環境内にあり、障害物でない)を判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードが環境内にあり、障害物でない場合はTrue, それ以外はFalse
        """
        if not self.is_in_environment(node):
            return False
        if self.is_obstacle(node):
            return False
        return True

    def print_raw_map(self):
        for r in range(self.width):
            for c in range(self.height):
                print_str = ""
                if self.is_obstacle(Node(r, c)):
                    print_str = MAP_STATE.OBSTACLE
                else:
                    print_str = MAP_STATE.PASS_POINT
                print(print_str.rjust(2), end=" ")
            print()


class World:
    """エージェントと報酬の保管庫の情報、および環境の状況を保持するクラス"""

    def __init__(self, obstacle_file: str, reward_probability_file: str):
        self.environment: Environment
        self.agents: List[Agent] = []
        self.agents_count = 0
        self.vaults: List[Vault] = []
        self.vaults_count = 0
        self.reward_array: np.ndarray
        self.__load_maps(obstacle_file, reward_probability_file)

    def __load_maps(self, obstacle_file: str, reward_probability_file: str):
        with open(obstacle_file, "r") as f:
            first_line = f.readline()
            width, height = map(int, first_line.strip().split(","))
            self.environment = Environment(width, height)
            obstacle_array = np.zeros((width, height))
            for i in range(width):
                line = f.readline()
                row_list = line.strip().split(",")
                for j, value in enumerate(row_list):
                    if value == MAP_STATE.OBSTACLE:
                        obstacle_array[i, j] = 1
                    elif value == MAP_STATE.PASS_POINT:
                        obstacle_array[i, j] = 0
                    elif value == MAP_STATE.AGENT:
                        self.agents.append(Agent(self.agents_count, MAXIMUM_REWARDS_CAPACITY, Node(i, j)))
                        self.agents_count += 1
                    elif value == MAP_STATE.VAULT:
                        self.vaults.append(Vault(Node(i, j)))
                        self.vaults_count += 1
                    else:
                        raise ValueError("Invalid value in the map")
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
        """確率に応じてノードに報酬を生成するメソッド

        !!経路計画プログラムでの利用はしてはいけない
        """
        for r in range(self.environment.width):
            for c in range(self.environment.height):
                node = Node(r, c)
                # エージェントがいる場所には報酬を生成しない
                if self.get_agent_with_node(node):
                    continue
                prob = self.environment.reward_probability_array[r, c]
                if random.random() < prob:
                    self.reward_array[r, c] = 1

    def earn_reward(self, agent: Agent) -> int:
        """エージェントが報酬を獲得するメソッド

        !!経路計画プログラムでの利用はしてはいけない
        """

        reward = self.reward_array[agent.get_node().x, agent.get_node().y]
        if agent.get_maximum_rewards_capacity() - agent.owned_reward < reward:
            reward = agent.get_maximum_rewards_capacity() - agent.owned_reward
        agent.owned_reward += reward
        self.reward_array[agent.get_node().x, agent.get_node().y] -= reward
        return reward

    def get_environment_size(self) -> Tuple[int, int]:
        """環境の横幅と縦幅を取得するメソッド

        Returns:
            Tuple[int, int]: 環境の横幅と縦幅
        """
        return self.environment.get_environment_size()

    def is_obstacle(self, node: Node) -> bool:
        """指定したノードが障害物かどうかを判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードが障害物の場合はTrue, それ以外はFalse
        """
        return self.environment.is_obstacle(node)

    def is_in_environment(self, node: Node) -> bool:
        """指定したノードが環境内にあるかどうかを判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードが環境内にある場合はTrue, それ以外はFalse
        """
        return self.environment.is_in_environment(node)

    def is_valid_node(self, node: Node) -> bool:
        """指定したノードが有効であるか(環境内にあり、障害物でない)を判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードが環境内にあり、障害物でない場合はTrue, それ以外はFalse
        """
        return self.environment.is_valid_node(node)

    def get_agents(self) -> List[Agent]:
        """エージェントのリストを取得するメソッド

        Returns:
            List[Agent]: エージェントのリスト
        """
        return self.agents

    def get_agents_count(self) -> int:
        """エージェントの総数を取得するメソッド

        Returns:
            int: エージェントの総数
        """
        return self.agents_count

    def get_vaults(self) -> List[Vault]:
        """保管庫のリストを取得するメソッド

        Returns:
            List[Vault]: 保管庫のリスト
        """
        return self.vaults

    def get_vaults_count(self) -> int:
        """保管庫の総数を取得するメソッド

        Returns:
            int: 保管庫の総数
        """
        return self.vaults_count

    def get_agent_with_node(self, node: Node) -> Union[Agent, None]:
        """指定したノードにいるエージェントを取得するメソッド

        Args:
            node (Node): 対象となるノード

        Returns:
            Union[Agent, None]: 指定したノードにいるエージェントが存在する場合はそのエージェント, それ以外はNone
        """
        for agent in self.agents:
            if agent.get_node() == node:
                return agent
        return None

    def get_vault_with_node(self, node: Node) -> Union[Vault, None]:
        """指定したノード上の保管庫を取得するメソッド

        Args:
            node (Node): 対象となるノード

        Returns:
            Union[Vault, None]: 指定したノードに保管庫が存在する場合はその保管庫, それ以外はNone
        """
        for vault in self.vaults:
            if vault.get_node() == node:
                return vault
        return None

    def get_reward_array(self) -> np.ndarray:
        """現在の報酬が配置されているノードを記録した配列を取得するメソッド

        Returns:
            np.ndarray: 報酬の配列
        """
        return self.reward_array

    def has_reward(self, node: Node) -> bool:
        """指定したノードに報酬があるかどうかを判定するメソッド

        Args:
            node (Node): 判定するノード

        Returns:
            bool: 指定したノードに報酬がある場合はTrue, それ以外はFalse
        """
        return self.reward_array[node.x, node.y] > 0

    def get_nearest_node_has_reward(self, node: Node) -> Union[Node, None]:
        """指定したノードに最も近い報酬があるノードを取得するメソッド

        Args:
            node (Node): 対象となるノード

        Returns:
            Union[Node, None]: 指定したノードに最も近い報酬があるノードが存在する場合はそのノード, それ以外はNone
        """
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

    def get_adjacent_nodes(self, node: Node) -> List[Node]:
        """指定したノードの隣接するノードのリストを取得するメソッド

        Args:
            node (Node): 対象となるノード

        Returns:
            List[Node]: 指定したノードの隣接するノードのリスト
        """
        action_list: List[Node] = [
            Node(0, 1),
            Node(0, -1),
            Node(1, 0),
            Node(-1, 0),
        ]
        return [node + action for action in action_list]

    def get_valid_next_actions_for_agents(self, agent: Agent) -> List[Node]:
        """エージェントが次に選択できる有効な行動(Node)のリストを取得するメソッド

        Args:
            agent (Agent): 対象となるエージェント

        Returns:
            List[Node]: エージェントが次に選択できる有効な行動(Node)のリスト
        """
        current_node = agent.get_node()
        actions_list = [
            Node(0, 1),
            Node(0, -1),
            Node(1, 0),
            Node(-1, 0),
            Node(0, 0),
        ]
        valid_next_actions: List[Node] = []
        for action in actions_list:
            next_node = current_node + action
            if self.is_valid_node(next_node):
                valid_next_actions.append(action)
        return valid_next_actions

    def print_map_state(self):
        width, height = self.environment.get_environment_size()
        for r in range(width):
            for c in range(height):
                print_str = ""
                agent = self.get_agent_with_node(Node(r, c))
                vault = self.get_vault_with_node(Node(r, c))
                color_start_str = ""
                color_end_str = ""
                if agent:
                    print_str = MAP_STATE.AGENT
                    color_start_str = "\033[32m"
                    color_end_str = "\033[0m"
                elif vault:
                    print_str = MAP_STATE.VAULT
                    color_start_str = "\033[34m"
                    color_end_str = "\033[0m"
                elif self.environment.is_obstacle(Node(r, c)):
                    print_str = MAP_STATE.OBSTACLE
                elif self.reward_array[r, c] > 0:
                    print_str = "★"
                    color_start_str = "\033[33m"
                    color_end_str = "\033[0m"
                else:
                    print_str = MAP_STATE.PASS_POINT
                print(color_start_str + print_str.rjust(2) + color_end_str, end=" ")
            print()
