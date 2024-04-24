# マルチエージェント報酬運搬問題（仮）
## 1. 目的
- エージェント全体が協力して、2次元グリッド空間上にランダムに配置される報酬をなるべく多く保管庫まで運ぶことを目的とする。
## 2. 環境
- まず事前に2次元グリッド空間上に障害物、およびエージェントが配置される。
- 2次元グリッド空間上のそれぞれのノードは、各時刻において事前に決められた確率に従って報酬が配置されるかどうかが決定される。
- エージェントは報酬を運ぶことができる。
- エージェントは複数の報酬を運ぶことができるが、一度に運べる報酬の数には制限がある。
- エージェントは保管庫に到達すると報酬を保管庫に納めることができる。
## 