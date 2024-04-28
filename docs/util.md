- `get_adjacent_nodes`関数
    ```python 
    def get_adjacent_nodes(self, node: Node) -> List[Node]:
    ```
   
    - 指定したノードの隣接するノードのリストを取得するメソッド
    - Args(引数):
        - `node (Node)`: 対象となるノード
    - Returns(戻り値):
        - `List[Node]`: 指定したノードの隣接するノードのリスト

- `get_manhattan_distance`関数
    ```python 
    def get_manhattan_distance(node1: Node, node2: Node) -> int:
    ```
   
    - 2ノード間のマンハッタン距離を計算する関数
    - Args(引数):
        - `node1 (Node)`: ノード1
        - `node2 (Node)`: ノード2
    - Returns(戻り値):
        - `int`: マンハッタン距離

- `get_euclidean_distance`関数
    ```python 
    def get_euclidean_distance(node1: Node, node2: Node) -> float:
    ```
   
    - 2ノード間のユークリッド距離を計算する関数
    - Args(引数):
        - `node1 (Node)`: ノード1
        - `node2 (Node)`: ノード2
    - Returns(戻り値):
        - `float`: ユークリッド距離

- `get_astar_path`関数
    ```python 
    def get_astar_path(world: World, node1: Node, node2: Node) -> Union[List[Node], None]:
    ```
   
    - 2ノード間の最短経路を返す関数
    - Args(引数):
        - `world (World)`: ワールドインスタンス
        - `node1 (Node)`: ノード1
        - `node2 (Node)`: ノード2
    - Returns(戻り値):
        - `List[Node]`: 経路、経路が存在しない場合はNone

- `get_astar_distance`関数
    ```python 
    def get_astar_distance(world: World, node1: Node, node2: Node) -> int:
    ```
   
    - 2ノード間の最短距離をA*探索で計算する関数
    - Args(引数):
        - `world (World)`: ワールドインスタンス
        - `node1 (Node)`: ノード1
        - `node2 (Node)`: ノード2
    - Returns(戻り値):
        - `int`: 最短距離、経路が存在しない場合は-1



