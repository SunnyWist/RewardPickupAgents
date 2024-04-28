- `get_environment_size`メソッド
    ```python 
    def get_environment_size(self) -> tuple[int, int]:
    ```
   
    - 環境の横幅と縦幅を取得するメソッド
    - Returns(戻り値):
        - `tuple[int, int]`: 環境の横幅と縦幅

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

- `check_valid_node`メソッド
    ```python 
    def check_valid_node(self, node: Node) -> bool:
    ```
   
    - 指定したノードが有効であるか(環境内にあり、障害物でない)を判定するメソッド
    - Args(引数):
        - `node (Node)`: 判定するノード
    - Returns(戻り値):
        - `bool`: 指定したノードが環境内にあり、障害物でない場合は`True`, それ以外は`False`

- `get_agents_list`メソッド
    ```python 
    def get_agents_list(self) -> List[Agent]:
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

- `get_store_points_list`メソッド
    ```python 
    def get_store_points_list(self) -> List[StorePoint]:
    ```
   
    - 報酬を保管する場所のリストを取得するメソッド
    - Returns(戻り値):
        - `List[StorePoint]`: 報酬を保管する場所のリスト

- `get_store_points_count`メソッド
    ```python 
    def get_store_points_count(self) -> int:
    ```
   
    - 報酬を保管する場所の総数を取得するメソッド
    - Returns(戻り値):
        - `int`: 報酬を保管する場所の総数

- `get_agent_with_node`メソッド
    ```python 
    def get_agent_with_node(self, node: Node) -> Union[Agent, None]:
    ```
   
    - 指定したノードにいるエージェントを取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `Union[Agent, None]`: 指定したノードにいるエージェントが存在する場合はそのエージェント, それ以外は`None`

- `get_store_point_with_node`メソッド
    ```python 
    def get_store_point_with_node(self, node: Node) -> Union[StorePoint, None]:
    ```
   
    - 指定したノードにある報酬を保管する場所を取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `Union[StorePoint, None]`: 指定したノードにある報酬を保管する場所が存在する場合はその場所, それ以外は`None`

- `get_nearest_reward_node`メソッド
    ```python 
    def get_nearest_reward_node(self, node: Node) -> Union[Node, None]:
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

- `get_agent_valid_next_nodes`メソッド
    ```python 
    def get_agent_valid_next_nodes(self, agent: Agent) -> List[Node]:
    ```
   
    - エージェントが次に移動できる有効なノードのリストを取得するメソッド
    - Args(引数):
        - `agent (Agent)`: 対象となるエージェント
    - Returns(戻り値):
        - `List[Node]`: エージェントが次に移動できる有効なノードのリスト



