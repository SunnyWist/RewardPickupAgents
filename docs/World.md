- `get_environment_size`メソッド
    ```python
    def get_environment_size(self) -> Tuple[int, int]:
    ```

    - 環境の横幅と縦幅を取得するメソッド
    - Returns(戻り値):
        - `Tuple[int, int]`: 環境の横幅と縦幅

- `get_obstacle_data`メソッド
    ```python
    def get_obstacle_data(self) -> np.ndarray:
    ```

    - 障害物のデータを取得するメソッド
    - Returns(戻り値):
        - `np.ndarray`: 障害物のデータ

- `is_obstacle`メソッド
    ```python
    def is_obstacle(self, node: Node) -> bool:
    ```

    - 指定したノードが障害物かどうかを判定するメソッド
    - Args(引数):
        - `node (Node)`: 判定するノード
    - Returns(戻り値):
        - `bool`: 指定したノードが障害物の場合は`True`, それ以外は`False`

- `is_in_environment`メソッド
    ```python
    def is_in_environment(self, node: Node) -> bool:
    ```

    - 指定したノードが環境内にあるかどうかを判定するメソッド
    - Args(引数):
        - `node (Node)`: 判定するノード
    - Returns(戻り値):
        - `bool`: 指定したノードが環境内にある場合は`True`, それ以外は`False`

- `is_valid_node`メソッド
    ```python
    def is_valid_node(self, node: Node) -> bool:
    ```

    - 指定したノードが有効であるか(環境内にあり、障害物でない)を判定するメソッド
    - Args(引数):
        - `node (Node)`: 判定するノード
    - Returns(戻り値):
        - `bool`: 指定したノードが環境内にあり、障害物でない場合は`True`, それ以外は`False`

- `get_agents`メソッド
    ```python
    def get_agents(self) -> List[Agent]:
    ```

    - エージェントのリストを取得するメソッド
    - Returns(戻り値):
        - `List[Agent]`: エージェントのリスト

- `get_agents_count`メソッド
    ```python
    def get_agents_count(self) -> int:
    ```

    - エージェントの総数を取得するメソッド
    - Returns(戻り値):
        - `int`: エージェントの総数

- `get_vaults`メソッド
    ```python
    def get_vaults(self) -> List[Vault]:
    ```

    - 保管庫のリストを取得するメソッド
    - Returns(戻り値):
        - `List[Vault]`: 保管庫のリスト

- `get_vaults_count`メソッド
    ```python
    def get_vaults_count(self) -> int:
    ```

    - 保管庫の総数を取得するメソッド

    - Returns(戻り値):
        - `int`: 保管庫の総数

- `get_agent_with_node`メソッド
    ```python
    def get_agent_with_node(self, node: Node) -> Union[Agent, None]:
    ```

    - 指定したノードにいるエージェントを取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `Union[Agent, None]`: 指定したノードにいるエージェントが存在する場合はそのエージェント, それ以外は`None`

- `get_vault_with_node`メソッド
    ```python
    def get_vault_with_node(self, node: Node) -> Union[Vault, None]:
    ```

    - 指定したノード上の保管庫を取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `Union[Vault, None]`: 指定したノードに保管庫が存在する場合はその保管庫, それ以外は`None`

- `get_reward_array`メソッド
    ```python
    def get_reward_array(self) -> np.ndarray:
    ```

    - 現在の報酬が配置されているノードを記録した配列を取得するメソッド
    - Returns(戻り値):
        - `np.ndarray`: 報酬の配列

- `has_reward`メソッド
    ```python
    def has_reward(self, node: Node) -> bool:
    ```

    - 指定したノードに報酬があるかどうかを判定するメソッド
    - Args(引数):
        - `node (Node)`: 判定するノード
    - Returns(戻り値):
        - `bool`: 指定したノードに報酬がある場合は`True`, それ以外は`False`

- `get_agents_pos_dict`メソッド
    ```python
    def get_agents_pos_dict(self) -> Dict[int, List[int]]:
    ```
    
    - エージェントの位置情報を辞書形式で取得するメソッド
    - Returns(戻り値):
        - `Dict[int, List[int]]`: エージェントの位置情報

- `get_vaults_pos_dict`メソッド
    ```python
    def get_vaults_pos_dict(self) -> Dict[int, List[int]]:
    ```

    - 保管庫の位置情報を辞書形式で取得するメソッド
    - Returns(戻り値):
        - `Dict[int, List[int]]`: 保管庫の位置情報

- `get_nearest_node_has_reward`メソッド
    ```python
    def get_nearest_node_has_reward(self, node: Node) -> Union[Node, None]:
    ```

    - 指定したノードに最も近い報酬があるノードを取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `Union[Node, None]`: 指定したノードに最も近い報酬があるノードが存在する場合はそのノード, それ以外は`None`

- `get_adjacent_nodes`メソッド
    ```python
    def get_adjacent_nodes(self, node: Node) -> List[Node]:
    ```

    - 指定したノードの隣接するノードのリストを取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `List[Node]`: 指定したノードの隣接するノードのリスト

- `get_valid_next_actions_for_agents`メソッド
    ```python
    def get_valid_next_actions_for_agents(self, agent: Agent) -> List[Node]:
    ```

    - エージェントが次に選択できる有効な行動(Node)のリストを取得するメソッド
    - Args(引数):
        - `agent (Agent)`: 対象となるエージェント
    - Returns(戻り値):
        - `List[Node]`: エージェントが次に選択できる有効な行動(Node)のリスト
