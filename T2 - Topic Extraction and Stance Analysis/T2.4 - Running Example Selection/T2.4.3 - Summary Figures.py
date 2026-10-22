"""Summary figures and the party table for the T2.4 memo (README.md in this folder).

Three figures: the selection flowchart, and one compact 2 x 2 figure per step for
the four topics that reached Step 2. The Step 1 panels use the model's
support/concern labels on every record placed on a topic; the Step 2 panels use
the audited direction codes from the same records. One table: audited direction
by administration and speaker party, which needs the hearing membership file
under the data root. Everything else reads only files that T2.4.1 and T2.4.2
wrote under output/. No model is run.
"""

import argparse
import importlib.util
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("select", HERE / "T2.4.1 - Step 1 - Topic Screening.py")
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

STEP1 = HERE / "output" / "T2.4.1 - Step 1 - Topic Screening"
AUDIT = HERE / "output" / "T2.4.2 - Step 2 - Stance Audit and Angle Coding" / "audit"
OUT = HERE / "output" / Path(__file__).stem
S.OUT = OUT  # S.finish() saves next to this script's other outputs

FINALISTS = [78, 26, 68, 21]
TITLES = {78: "EPA air and water regulations", 26: "Renewable energy technologies and storage",
          68: "Consumer data privacy legislation", 21: "Nuclear energy research and development"}
MIN_DIR_ADMIN = 20   # directional records an administration needs for its mean to be drawn
ADMIN_EDGES = [lo - 0.5 for _, lo, _ in S.ADMIN_YEARS] + [S.ADMIN_YEARS[-1][2] + 0.5]
ADMIN_TEXT = "Bush 2001-2008, Obama 2009-2016, Trump 2017-2020, Biden 2021-2024, Trump 2025"


# ----------------------------------------------------------------- data --
def load_audit(t):
    d = pd.read_csv(AUDIT / f"audit_topic_{t}.csv")
    assert d.hyear.between(S.YEAR_MIN, S.YEAR_MAX).all()
    d["sup"] = d.stance.eq("support")
    d["admin"] = pd.cut(d.hyear, ADMIN_EDGES, labels=S.ADMIN_ORDER)
    return d


def direction_yearly(d):
    y = (d.groupby("hyear").agg(pro=("direction", lambda v: v.eq("pro").sum()), anti=("direction", lambda v: v.eq("anti").sum()))
         .reindex(range(S.YEAR_MIN, S.YEAR_MAX + 1), fill_value=0))
    y["n"] = y.pro + y.anti
    y["net"] = (y.pro - y.anti) / y.n.replace(0, np.nan)
    return y


def direction_admin(d):
    a = d.groupby("admin", observed=False).agg(pro=("direction", lambda v: v.eq("pro").sum()), anti=("direction", lambda v: v.eq("anti").sum()))
    a["n"] = a.pro + a.anti
    a["net"] = (a.pro - a.anti) / a.n.replace(0, np.nan)
    return a


# -------------------------------------------------------------- panels --
def top_labels(ax, years, min_span=3):
    """Administration names above a small panel; spans shorter than min_span years get no label."""
    top = ax.secondary_xaxis("top")
    top.spines["top"].set_visible(False)
    spans = [(n, lo, hi) for n, lo, hi in S.admin_spans(years) if hi - lo + 1 >= min_span]
    top.set_xticks([(lo + hi) / 2 for _, lo, hi in spans])
    top.set_xticklabels([S.ADMIN_SHORT[n] for n, _, _ in spans], fontsize=8.5)
    top.tick_params(length=0, pad=2)


def panel(ax, years, line, admin, min_admin, ref=None):
    ax.axhline(0, color=S.RED, lw=0.8, ls=(0, (3, 2)))
    for name, lo, hi in S.admin_spans(years):
        if admin.loc[name, "n"] >= min_admin:
            ax.plot([lo - 0.5, hi + 0.5], [admin.loc[name, "net"]] * 2, color=S.GREEN, lw=2.6, solid_capstyle="butt", zorder=2)
    if ref is not None:
        ax.plot(ref.index, ref.values, color=S.NAVY_LIGHT, lw=0.9, zorder=2)
    ax.plot(line.index, line.values, color=S.NAVY, lw=0.9, marker="o", ms=3.4, mec="white", mew=0.4, zorder=3)
    S.admin_boundaries(ax, years)
    top_labels(ax, years)
    ax.set_ylim(-1.05, 1.05)
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xlim(S.YEAR_MIN - 0.7, S.YEAR_MAX + 0.7)
    ax.set_xticks([2001, 2009, 2017, 2021, 2025])
    ax.tick_params(axis="x", labelsize=8)
    ax.yaxis.grid(True, color=S.GRID, lw=0.6)
    ax.set_axisbelow(True)


def grid(stem, ylabel, note, handles, labels, draw):
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.6), sharey=True, gridspec_kw={"hspace": 0.62, "wspace": 0.10})
    for ax, t in zip(axes.flat, FINALISTS):
        draw(ax, t)
    for ax in axes[:, 0]:
        ax.set_ylabel(ylabel)
    for ax in axes[1]:
        ax.set_xlabel("Hearing year")
    S.finish(fig, stem, note, axes[1, 0], right_ax=axes[1, 1], bottom_ax=axes[1, 0], handles=handles, labels=labels, ncol=1)


def fig_step1(data, metrics):
    def draw(ax, t):
        d = data[t]
        y, a = S.yearly(d), S.by_admin(d)
        panel(ax, list(y.index), y.net[y.n >= S.MIN_CELL_YEAR], a, S.MIN_CELL_ADMIN)
        m = metrics.loc[t]
        ax.set_title(f"Topic {t}: {TITLES[t]}\n{m.n:,} records, support share {m.support_share:.2f}, break year {int(m.break_year)}",
                     loc="left", fontsize=9, pad=14)
    handles = [Line2D([], [], color=S.NAVY, lw=0.9, marker="o", ms=3.4, mec="white"), Line2D([], [], color=S.GREEN, lw=2.6),
               Line2D([], [], color=S.RED, lw=0.8, ls=(0, (3, 2)))]
    labels = [f"Yearly net stance from the model's labels (years with at least {S.MIN_CELL_YEAR} records)",
              f"Administration mean (at least {S.MIN_CELL_ADMIN} records)", "Balanced (net stance = 0)"]
    grid("fig_step1_finalists", "Net stance\n(support - concern) / records",
         "Note: Step 1 measure for the four topics that went on to Step 2. All legislator stance records placed on each topic "
         f"(codebook v1.0), House Science and Senate Commerce hearings held {S.YEAR_MIN}-{S.YEAR_MAX}, with the model's support or "
         f"concern label and no audit. Administrations are calendar-year blocks ({ADMIN_TEXT}); vertical lines mark the changes. "
         "The break year is the year that best splits the topic's records into a before and an after period.",
         handles, labels, draw)


def fig_step2(data):
    def draw(ax, t):
        d = data[t]
        y, a = direction_yearly(d), direction_admin(d)
        ref = S.yearly(d)
        panel(ax, list(y.index), y.net[y.n >= S.MIN_CELL_YEAR], a, MIN_DIR_ADMIN, ref=ref.net[ref.n >= S.MIN_CELL_YEAR])
        pro, anti = int(d.direction.eq("pro").sum()), int(d.direction.eq("anti").sum())
        ax.set_title(f"Topic {t}: {TITLES[t]}\n{pro} records favor more, {anti} favor less, {int(d.verdict.eq('offtopic').sum())} off-topic",
                     loc="left", fontsize=9, pad=14)
    handles = [Line2D([], [], color=S.NAVY, lw=0.9, marker="o", ms=3.4, mec="white"), Line2D([], [], color=S.GREEN, lw=2.6),
               Line2D([], [], color=S.NAVY_LIGHT, lw=0.9), Line2D([], [], color=S.RED, lw=0.8, ls=(0, (3, 2)))]
    labels = [f"Yearly net direction from the audit (years with at least {S.MIN_CELL_YEAR} directional records)",
              f"Administration mean (at least {MIN_DIR_ADMIN} directional records)",
              "Yearly net stance from the model's labels (Step 1 figure, for comparison)", "Balanced (net direction = 0)"]
    grid("fig_step2_finalists", "Net direction\n(more - less) / records",
         "Note: Step 2 measure for the same four topics and the same records. Every record was read against its cited sentences "
         "and coded for direction, whether it favors more or less of the topic's policy object (stronger environmental regulation or a "
         "stronger EPA; more support for renewable energy; stronger privacy protection; expanding nuclear energy), in a single assistant "
         "coding pass (Claude, 2026-10-22) with no human review yet. Net direction = (records favoring more - records favoring less) / "
         "records with a direction; records with no stance, no clear direction, or off-topic are left out. "
         f"Administrations are calendar-year blocks ({ADMIN_TEXT}); vertical lines mark the changes.",
         handles, labels, draw)


# ------------------------------------------------------------ flowchart --
# (heading, body, what leaves the box along the arrow below it)
FLOW = [
    ("Stage 3 output", "29,971 legislator stance records (one member position: cited sentences, an issue, support or concern) "
                       "placed on the 111 codebook topics; House Science and Senate Commerce hearings held 1999-2025", None),
    ("Candidate pool", "The 30 topics with the most records (374 to 1,369 records each)", "30 topics"),
    ("Step 1: screen", "Three numeric criteria on every topic: enough records, enough support and concern, a clean shift across "
                       "administrations or around an event", "13 of 30 pass"),
    ("Step 1: read", "40 sampled source sentences per passing topic: is it one topic, and does \"concern\" mean concern about a harm "
                     "or opposition to a rule?", "4 candidates: 78, 26, 68, 21 (plus 65, a sibling of 68)"),
    ("Step 2: audit", "Every record of each candidate read and coded by hand: is the label right, which angle of the topic, and "
                      "which direction (favoring more or less of the policy)", "2,589 records coded"),
    ("Best cases", "Direction shifts over time: 78 EPA regulations, 26 renewable energy. Direction constant, only the angle shifts: "
                   "68 consumer privacy, 21 nuclear R&D", None),
]


def fig_flow():
    fig = plt.figure(figsize=(7.4, 6.0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    W = fig.bbox.width
    x0, x1, head_w = 2, 98, 15              # box spans x0..x1 in axis units; heading column width
    box_h, gap = 12.4, 4.4                  # 6 boxes and 5 gaps fill the height
    body_px = (x1 - x0 - head_w - 3) / 100 * W
    y_top = 99
    bottoms = []
    for i, (head, body, _) in enumerate(FLOW):
        yt = y_top - i * (box_h + gap)
        step = head.startswith("Step")
        ax.add_patch(FancyBboxPatch((x0, yt - box_h), x1 - x0, box_h, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc="#EEF2F5" if step else "white", ec=S.NAVY, lw=1.4 if i == len(FLOW) - 1 else 1.0))
        ax.text(x0 + 1.6, yt - box_h / 2, head, ha="left", va="center", fontsize=10, fontweight="bold", color=S.CHARCOAL)
        ax.text(x0 + head_w + 1.0, yt - box_h / 2, S.wrap_to_px(fig, ren, body, body_px, fontsize=9), ha="left", va="center",
                fontsize=9, color=S.CHARCOAL, linespacing=1.25)
        bottoms.append(yt - box_h)
    x_arrow = x0 + head_w / 2
    for i, (_, _, count) in enumerate(FLOW[:-1]):
        y_from, y_to = bottoms[i], bottoms[i] - gap
        ax.add_patch(FancyArrowPatch((x_arrow, y_from), (x_arrow, y_to + 0.2), arrowstyle="-|>", mutation_scale=11,
                                     color=S.CHARCOAL, lw=0.9, shrinkA=0, shrinkB=0))
        if count:
            ax.text(x_arrow + 2.2, (y_from + y_to) / 2, count, ha="left", va="center", fontsize=9, color=S.CHARCOAL)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"fig_flowchart.{ext}", bbox_inches="tight", dpi=200, facecolor="white", pad_inches=0.04)
    plt.close(fig)
    print("saved fig_flowchart.pdf/.svg/.png")


# ---------------------------------------------------------- party table --
def party_table(data, data_root):
    """Audited direction by administration and speaker party for each finalist."""
    members = (pd.read_parquet(data_root / "interim/govinfo/hearing_members.parquet", columns=["packageId", "bioGuideId", "party"])
               .drop_duplicates(["packageId", "bioGuideId"]))
    rows = []
    for t in FINALISTS:
        d = data[t].merge(members, on=["packageId", "bioGuideId"], how="left", validate="m:1")
        x = d[d.direction.isin(["pro", "anti"])]
        tab = pd.crosstab([x.admin, x.party.fillna("unknown")], x.direction).reindex(columns=["pro", "anti"], fill_value=0)
        tab = tab[tab.sum(axis=1) > 0].reset_index()
        tab.insert(0, "topic_id", t)
        tab["party_missing_records"] = int(d.party.isna().sum())
        rows.append(tab)
    out = pd.concat(rows, ignore_index=True).rename(columns={"pro": "favor_more", "anti": "favor_less"})
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT / "direction_by_party.csv", index=False)
    print(out[out.topic_id == 78].to_string(index=False))


def main(data_root):
    S.style()
    metrics = pd.read_csv(STEP1 / "topic_selection_metrics.csv").set_index("topic_id")
    data = {t: load_audit(t) for t in FINALISTS}
    for t in FINALISTS:
        assert len(data[t]) == metrics.loc[t, "n"], f"topic {t}: audit file has {len(data[t])} records, screen counted {metrics.loc[t, 'n']}"
    fig_flow()
    fig_step1(data, metrics)
    fig_step2(data)
    party_table(data, data_root)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-root", type=Path, default=S.DEFAULT_DATA, help="only the hearing membership file is read from here")
    main(p.parse_args().data_root)
