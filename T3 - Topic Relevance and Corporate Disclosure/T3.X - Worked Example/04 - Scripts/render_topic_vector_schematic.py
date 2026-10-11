"""Schematic for Section 5.2, procedure 2: how the topic side is anchored.

Run: python "render_topic_vector_schematic.py" [output folder]
Writes fig_topic_vector_schematic.svg/.pdf/.png. Uses no data; every position is drawn.

Left panel: the sentences of the first set, laid out as a list, with the few
that qualify as evidence picked out. Qualification is a Step #2 judgment, not a
position in space. Right panel: a hypothetical two-dimensional embedding space
in which the qualifying sentences and the definition are averaged into the
topic vector. Positions are drawn, not data.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import ConnectionPatch

# Output folder: the T3 figures directory by default, or a folder given as the first argument.
REPO = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "R - Results" / "figures" / "T3 - Topic Relevance and Corporate Disclosure"
OUT.mkdir(parents=True, exist_ok=True)
NAVY, RED, GRAY, LIGHT, GRID, INK = "#003049", "#9b2226", "#8c8c8c", "#c9c9c9", "#d0d0d0", "#222222"
plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 10})
rng = np.random.default_rng(11)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 4.6), gridspec_kw={"width_ratios": [1, 1.25]})

# ---- left: the sentences of the first set, as a list -------------------------
rows, cols = 12, 6
xs, ys = np.meshgrid(np.arange(cols), np.arange(rows)[::-1])
xs, ys = xs.ravel().astype(float), ys.ravel().astype(float)
n = len(xs)
state = np.zeros(n, dtype=int)                 # 0 no stance record
cited_other = rng.choice(n, 9, replace=False)   # 1 cited, placed elsewhere or in other
state[cited_other] = 1
pool = np.setdiff1d(np.arange(n), cited_other)
cited_a = rng.choice(pool, 7, replace=False)    # 2 cited, placed under topic A
state[cited_a] = 2

axL.scatter(xs[state == 0], ys[state == 0], s=22, c=LIGHT, zorder=2)
axL.scatter(xs[state == 1], ys[state == 1], s=46, facecolors="white", edgecolors=NAVY, linewidths=1.2, zorder=3)
axL.scatter(xs[state == 2], ys[state == 2], s=52, c=NAVY, zorder=3)
axL.set_xlim(-0.8, cols - 0.2)
axL.set_ylim(-1.0, rows - 0.3)
axL.set_xticks([]); axL.set_yticks([])
for side in axL.spines.values():
    side.set_color(GRID)
axL.set_title("Step #2 decides which sentences qualify", fontsize=10, color=INK, pad=8)
axL.text(-0.6, -0.75, "sentences of the first set, in document order", fontsize=8.5, color=GRAY)

# ---- right: embedding space ---------------------------------------------------
A = np.array([0.0, 0.0])
ang = rng.uniform(0, 2 * np.pi, 7)
rad = 1.3 * np.sqrt(rng.uniform(0.1, 1.0, 7))
ev = A + np.c_[rad * np.cos(ang), rad * np.sin(ang)]
defn = A + np.array([0.35, -0.6])
axR.set_aspect("equal")
for p in ev:
    axR.plot([A[0], p[0]], [A[1], p[1]], color=NAVY, lw=0.6, alpha=0.5, zorder=2)
axR.plot([A[0], defn[0]], [A[1], defn[1]], color=NAVY, lw=0.6, alpha=0.5, zorder=2)
axR.scatter(*ev.T, s=52, c=NAVY, zorder=3)
axR.scatter(*defn, marker="s", s=60, c=NAVY, zorder=3)
axR.scatter(*A, marker="*", s=320, c=RED, zorder=5, edgecolors="white", linewidths=0.6)
axR.annotate("topic vector  $\\mathbf{v}_k$\nnormalized mean of the definition\nand the evidence sentences", A,
             xytext=(-2.6, -2.55), fontsize=9, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
axR.annotate("definition", defn, xytext=(1.25, -1.9), fontsize=9, color=INK,
             arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
axR.annotate("evidence sentences", ev[np.argmax(ev[:, 1])], xytext=(0.6, 2.0), fontsize=9, color=INK,
             arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
axR.set_xlim(-2.9, 2.9)
axR.set_ylim(-2.9, 2.6)
axR.set_xticks([]); axR.set_yticks([])
for side in axR.spines.values():
    side.set_color(GRID)
axR.set_title("Step #3 averages them into the topic vector", fontsize=10, color=INK, pad=8)

# ---- arrow from the qualifying sentences to the right panel -------------------
con = ConnectionPatch(xyA=(cols - 0.35, rows / 2 - 0.5), coordsA=axL.transData,
                      xyB=(-2.75, 0.3), coordsB=axR.transData,
                      arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=12)
fig.add_artist(con)
fig.text(0.468, 0.60, "embed", fontsize=9, color=INK, ha="center")

handles = [
    Line2D([], [], marker="o", color="none", markerfacecolor=LIGHT, markersize=5, label="sentence with no stance record"),
    Line2D([], [], marker="o", color="none", markerfacecolor="white", markeredgecolor=NAVY, markersize=7, label="cited by a stance record placed under another topic or in “other”"),
    Line2D([], [], marker="o", color="none", markerfacecolor=NAVY, markersize=7, label="cited by a stance record placed under topic $k$: evidence sentence"),
    Line2D([], [], marker="s", color="none", markerfacecolor=NAVY, markersize=7, label="codebook definition"),
    Line2D([], [], marker="*", color="none", markerfacecolor=RED, markersize=13, label="topic vector"),
]
fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.14), frameon=False,
           fontsize=8.5, ncol=2, handletextpad=0.4, columnspacing=1.5)

fig.tight_layout()
for ext in ("svg", "pdf", "png"):
    fig.savefig(OUT / f"fig_topic_vector_schematic.{ext}", bbox_inches="tight", dpi=200)
print("saved")
