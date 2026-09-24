import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def draw_heatmap(readings, filename):
    xs = [r["x"] for r in readings]
    ys = [r["y"] for r in readings]
    vals = [r["signal_dbm"] for r in readings]

    grid_x, grid_y = np.mgrid[0:5:100j, 0:5:100j]
    grid_z = griddata((xs, ys), vals, (grid_x, grid_y), method="cubic")

    plt.figure(figsize=(6, 5))
    plt.contourf(grid_x, grid_y, grid_z, levels=20, cmap="viridis")
    plt.colorbar(label="Signal (dBm)")
    plt.scatter(xs, ys, c="white", edgecolors="black", s=40)
    plt.title("Wi-Fi Signal Heatmap")
    plt.xlabel("metres")
    plt.ylabel("metres")
    plt.savefig(filename, dpi=100)
    plt.close()


if __name__ == "__main__":
    with open("survey.json") as f:
        readings = json.load(f)

    draw_heatmap(readings, "heatmap.png")
    print("Saved heatmap.png - open it to see your Wi-Fi coverage")