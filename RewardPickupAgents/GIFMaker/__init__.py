import numpy as np
from copy import deepcopy
from typing import List, Dict, Union, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


COLORS_CYCLE = ["red", "blue", "green", "purple", "orange", "cyan", "magenta", "lime", "pink"]

fig, ax = plt.subplots(figsize=(6, 6))


class GIFMaker:
    def __init__(self, obstacle_data: np.ndarray, agents_count: int, vaults_count: int):
        self.obstacle_data = obstacle_data
        self.agents_count = agents_count
        self.vaults_count = vaults_count
        self.plt_frames: List = []
        x = np.arange(obstacle_data.shape[1])
        y = np.arange(obstacle_data.shape[0])
        self.X_array, self.Y_array = np.meshgrid(x, y)
        ax.xaxis.tick_top()
        ax.invert_yaxis()

    def update(
        self, step: int, score: int, reward_data: np.ndarray, agents: Dict[int, List[int]], vaults: Dict[int, List[int]]
    ):
        ax_list = []
        ax_list.append(
            ax.pcolormesh(self.X_array, self.Y_array, self.obstacle_data, cmap="Greys", edgecolors="black", linewidth=1)
        )
        for r in range(reward_data.shape[1]):
            for c in range(reward_data.shape[0]):
                if reward_data[c, r] > 0:
                    ax_list.append(
                        ax.text(
                            c,
                            r,
                            "★",
                            fontsize=32,
                            color="orange",
                            ha="center",
                            va="center",
                        )
                    )
        for i in range(self.agents_count):
            agent_pos = agents[i]
            ax_list.append(
                ax.add_patch(
                    patches.Circle(
                        (agent_pos[0], agent_pos[1]),
                        0.45,
                        color=COLORS_CYCLE[i % len(COLORS_CYCLE)],
                        fill=True,
                        zorder=3,
                    )
                )
            )
        for i in range(self.vaults_count):
            vault_pos = vaults[i]
            ax_list.append(
                ax.add_patch(
                    patches.Polygon(
                        [
                            (vault_pos[0], vault_pos[1] + 0.5),
                            (vault_pos[0] + 0.5, vault_pos[1]),
                            (vault_pos[0], vault_pos[1] - 0.5),
                            (vault_pos[0] - 0.5, vault_pos[1]),
                        ],
                        color="black",
                        fill=True,
                        zorder=2,
                    )
                )
            )
        # 現在のステップを書く
        ax_list.append(
            ax.text(
                0.5,
                1.1,
                "Step: {}, Score: {}".format(step, score),
                fontsize=20,
                transform=ax.transAxes,
                ha="center",
                va="center",
            )
        )
        self.plt_frames.append([*ax_list])

    def save_gif(self, gif_path: str):
        ani = animation.ArtistAnimation(fig, self.plt_frames, interval=1000, repeat=False, blit=False)
        ani.save(gif_path, writer="pillow")
        plt.close()
        print("GIF file is saved at: ", gif_path)
