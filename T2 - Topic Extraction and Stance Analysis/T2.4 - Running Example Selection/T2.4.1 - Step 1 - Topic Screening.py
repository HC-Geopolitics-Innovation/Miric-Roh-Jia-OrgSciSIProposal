"""Screen the 30 largest stance topics as candidates for the Section 6 running example.

Reads the saved Stage-3 stance records placed on the frozen codebook, attaches each
record to the year its hearing was held, and aggregates by year and by presidential
administration. For each topic it reports volume, the balance of support and
concern, and the size, timing, and cleanness of any shift over time. Writes one
metrics table, five figure sets, sampled stance sentences for the shortlisted
topics, and a Markdown table for the memo. No model is run and no record is
relabeled.
"""

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import findfont
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = Path("/project2/mmiric_1435/acroh/llm_method/data")
OUT = Path(__file__).resolve().parent / "output" / Path(__file__).stem

# Analysis choices, stated once. Years are hearing held years; the one 1996 hearing
# and its 8 records sit alone before a three-year gap and are left out.
YEAR_MIN, YEAR_MAX = 1999, 2025
TOP_N = 30
MIN_CELL_YEAR = 5        # a yearly net stance is shown only with this many records
MIN_CELL_ADMIN = 30      # an administration enters the shift tests with this many
MIN_SIDE_BREAK = 50      # records required on each side of a candidate break year
BALANCE_BAND = (0.30, 0.70)   # support share counted as "enough of both"
SHIFT_RANGE = 0.40       # administration net-stance range counted as a clear shift
SHIFT_P = 0.01
SEED = 1089
# Administrations are calendar-year blocks, so that a January transition hearing
# (for example the 2017 nomination hearings) counts with the incoming administration.
ADMIN_YEARS = [("Clinton", 1993, 2000), ("Bush", 2001, 2008), ("Obama", 2009, 2016),
               ("Trump I", 2017, 2020), ("Biden", 2021, 2024), ("Trump II", 2025, 2028)]
ADMIN_ORDER = [a for a, _, _ in ADMIN_YEARS]
ADMIN_SHORT = {"Clinton": "Clinton", "Bush": "Bush", "Obama": "Obama", "Trump I": "Trump", "Biden": "Biden", "Trump II": "Trump"}
ADMIN_PARTY = {"Clinton": "D", "Bush": "R", "Obama": "D", "Trump I": "R", "Biden": "D", "Trump II": "R"}
# Chamber majorities by Congress. The 107th Senate changed hands in June 2001 and is
# coded Democratic for the whole Congress.
HOUSE_DEM = {110, 111, 116, 117}
SENATE_DEM = {107, 110, 111, 112, 113, 117, 118}

NAVY, RED, GREEN = "#003049", "#A30006", "#7C9885"
NAVY_LIGHT = "#8FA6B5"
CHARCOAL, GRID, INK = "#36454F", "#D0D0D0", "0.35"
DIVERGE = LinearSegmentedColormap.from_list("stance", [RED, "#f4f2ef", NAVY])
CM_IN = 1 / 2.54


# ----------------------------------------------------------------- data --
def load_records(data_root):
    tax = data_root / "interim/topics/taxonomy"
    rec = pd.read_parquet(tax / "track2_assigned.parquet")
    codebook = pd.read_parquet(tax / "codebook_v1.parquet").set_index("topic_id")
    hearings = pd.read_parquet(data_root / "interim/repo_data/raw/02_hearings/hearings_sst.parquet",
                               columns=["packageId", "heldDate_first", "congress"])
    assert hearings.packageId.is_unique
    n_all = len(rec)
    rec = rec[rec.topic_id >= 0].copy()
    print(f"records placed on a codebook topic: {len(rec):,} of {n_all:,}")
    rec = rec.merge(hearings, on="packageId", how="left", validate="m:1")
    assert rec.heldDate_first.notna().all()
    rec["hyear"] = pd.to_datetime(rec.heldDate_first).dt.year
    rec["cong"] = rec.congress.astype(int)
    edges = [ADMIN_YEARS[0][1] - 1] + [hi for _, _, hi in ADMIN_YEARS]
    rec["admin"] = pd.cut(rec.hyear, edges, labels=ADMIN_ORDER)
    rec["pres_party"] = rec.admin.map(ADMIN_PARTY).astype(str)
    house = rec.chamber.eq("HOUSE")
    rec["majority"] = np.where(house, np.where(rec.cong.isin(HOUSE_DEM), "D", "R"),
                               np.where(rec.cong.isin(SENATE_DEM), "D", "R"))
    rec["sup"] = rec.stance.eq("support").astype(int)
    assert rec.stance.isin(["support", "concern"]).all()
    before = len(rec)
    rec = rec[rec.hyear.between(YEAR_MIN, YEAR_MAX)].copy()
    print(f"records in hearings held {YEAR_MIN}-{YEAR_MAX}: {len(rec):,} (dropped {before - len(rec)})")
    rec["theme"] = rec.topic_id.map(codebook.theme_label)
    return rec, codebook


def wilson(k, n, z=1.96):
    """Wilson interval for a share; returned as (low, high)."""
    k, n = np.asarray(k, float), np.asarray(n, float)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return center - half, center + half


def yearly(r):
    y = r.groupby("hyear").agg(n=("sup", "size"), support=("sup", "sum")).reindex(range(YEAR_MIN, YEAR_MAX + 1), fill_value=0)
    y["concern"] = y.n - y.support
    y["net"] = np.where(y.n > 0, (y.support - y.concern) / y.n.replace(0, np.nan), np.nan)
    lo, hi = wilson(y.support.where(y.n > 0), y.n.where(y.n > 0))
    y["net_lo"], y["net_hi"] = 2 * lo - 1, 2 * hi - 1
    return y


def by_admin(r):
    a = r.groupby("admin", observed=False).agg(n=("sup", "size"), support=("sup", "sum"))
    a["concern"] = a.n - a.support
    a["net"] = (a.support - a.concern) / a.n.replace(0, np.nan)
    return a


def weighted_r2(values, fitted, weights):
    m = np.average(values, weights=weights)
    ss_tot = np.sum(weights * (values - m) ** 2)
    ss_res = np.sum(weights * (values - fitted) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else np.nan


def shift_metrics(r):
    """Administration contrast, best single break year, and how much of the yearly
    movement the two-regime description explains."""
    a = by_admin(r)
    big = a[a.n >= MIN_CELL_ADMIN]
    if len(big) >= 2:
        chi2, p_admin, _, _ = stats.chi2_contingency(np.c_[big.support, big.concern])
    else:
        chi2, p_admin = np.nan, np.nan
    out = {"admin_cells": len(big), "admin_range": big.net.max() - big.net.min() if len(big) else np.nan,
           "p_admin": p_admin}
    for name in ADMIN_ORDER:
        out[f"n_{name}"] = int(a.loc[name, "n"])
        out[f"net_{name}"] = a.loc[name, "net"] if a.loc[name, "n"] >= MIN_CELL_ADMIN else np.nan
    best = None
    for b in range(YEAR_MIN + 1, YEAR_MAX + 1):
        pre, post = r[r.hyear < b], r[r.hyear >= b]
        if len(pre) < MIN_SIDE_BREAK or len(post) < MIN_SIDE_BREAK:
            continue
        d = post.sup.mean() - pre.sup.mean()
        if best is None or abs(d) > abs(best[1]):
            best = (b, d, pre, post)
    if best is None:
        out.update(break_year=np.nan, net_before=np.nan, net_after=np.nan, delta_net=np.nan, p_break=np.nan, r2_break=np.nan)
    else:
        b, d, pre, post = best
        p_break = stats.ttest_ind(post.sup, pre.sup, equal_var=False).pvalue
        y = yearly(r)
        shown = y[y.n >= MIN_CELL_YEAR]
        fitted = np.where(shown.index < b, 2 * pre.sup.mean() - 1, 2 * post.sup.mean() - 1)
        out.update(break_year=b, net_before=2 * pre.sup.mean() - 1, net_after=2 * post.sup.mean() - 1,
                   delta_net=2 * d, p_break=p_break, r2_break=weighted_r2(shown.net.to_numpy(), fitted, shown.n.to_numpy()))
    maj = pd.crosstab(r.majority, r.sup).reindex(index=["R", "D"], columns=[0, 1], fill_value=0)
    out["net_majority_R"] = (maj.loc["R", 1] - maj.loc["R", 0]) / maj.loc["R"].sum() if maj.loc["R"].sum() else np.nan
    out["net_majority_D"] = (maj.loc["D", 1] - maj.loc["D", 0]) / maj.loc["D"].sum() if maj.loc["D"].sum() else np.nan
    out["p_majority"] = stats.chi2_contingency(maj.to_numpy())[1] if (maj.sum(axis=1) > 0).all() else np.nan
    return out


def firm_exposure_proxy(data_root, topic_ids):
    """Share of 10-K filings whose raw top-5 cosine to the topic exceeds the pooled
    95th percentile. Raw cosines favor topics worded like filing language, so this
    is a rough indicator and is not used for ranking."""
    s = pd.read_parquet(data_root / "interim/relevance/scores/firm_topic_scores.parquet", columns=["gvkey", "topic_id", "score"])
    thr = s.score.quantile(0.95)
    high = s[s.score >= thr]
    out = pd.DataFrame({"filings_share_high_similarity": s.groupby("topic_id").score.apply(lambda x: (x >= thr).mean()),
                        "firms_high_similarity": high.groupby("topic_id").gvkey.nunique()}).fillna({"firms_high_similarity": 0})
    out["firms_high_similarity"] = out.firms_high_similarity.astype(int)
    return out.reindex(topic_ids)


def build_metrics(rec, codebook, data_root):
    tot = rec.groupby("topic_id").agg(n=("sup", "size"), support=("sup", "sum"), n_hearings=("packageId", "nunique"),
                                      n_legislators=("bioGuideId", "nunique"), first_year=("hyear", "min"), last_year=("hyear", "max"))
    tot["concern"] = tot.n - tot.support
    tot["support_share"] = tot.support / tot.n
    top = tot.nlargest(TOP_N, "n").copy()
    top.insert(0, "label", codebook.label.reindex(top.index))
    top.insert(1, "theme", codebook.theme_label.reindex(top.index))
    rows = {}
    for t in top.index:
        r = rec[rec.topic_id == t]
        y = yearly(r)
        m = shift_metrics(r)
        m["years_with_records"] = int((y.n > 0).sum())
        m[f"years_ge_{MIN_CELL_YEAR}"] = int((y.n >= MIN_CELL_YEAR).sum())
        rows[t] = m
    metrics = top.join(pd.DataFrame.from_dict(rows, orient="index"))
    metrics = metrics.join(firm_exposure_proxy(data_root, metrics.index))
    metrics["balanced"] = metrics.support_share.between(*BALANCE_BAND)
    metrics["clear_shift"] = (metrics.p_admin < SHIFT_P) & (metrics.admin_range >= SHIFT_RANGE) & (metrics.admin_cells >= 3)
    metrics["shortlist"] = metrics.balanced & metrics.clear_shift
    assert metrics.n.sum() == rec[rec.topic_id.isin(metrics.index)].shape[0]
    return metrics.reset_index()


# -------------------------------------------------------------- figures --
def style():
    findfont("Times New Roman", fallback_to_default=False)
    plt.rcParams.update({"font.family": "Times New Roman", "font.size": 10, "axes.labelsize": 10.5,
                         "xtick.labelsize": 9, "ytick.labelsize": 9, "svg.fonttype": "none", "pdf.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": CHARCOAL,
                         "xtick.color": CHARCOAL, "ytick.color": CHARCOAL, "text.color": CHARCOAL,
                         "axes.labelcolor": CHARCOAL, "figure.facecolor": "white", "axes.facecolor": "white"})


def wrap_to_px(fig, ren, text, width_px, fontsize=8):
    probe = fig.text(0, 0, "", fontsize=fontsize)
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        probe.set_text(trial)
        if probe.get_window_extent(ren).width <= width_px or not line:
            line = trial
        else:
            out.append(line)
            line = word
    out.append(line)
    probe.remove()
    return "\n".join(out)


def finish(fig, stem, note, left_ax, right_ax=None, bottom_ax=None, handles=None, labels=None, ncol=0, top_px=None):
    """House layout: legend one row under the x-title, left-aligned to the y-title;
    note 0.3 cm below, wrapped to the measured figure width."""
    right_ax = right_ax or left_ax
    bottom_ax = bottom_ax or left_ax
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    dpi, W, H = fig.dpi, fig.bbox.width, fig.bbox.height
    gap = 0.3 * CM_IN * dpi
    ylab = left_ax.yaxis.label
    x0 = ylab.get_window_extent(ren).x0 if ylab.get_text() else min(t.get_window_extent(ren).x0 for t in left_ax.get_yticklabels()) if left_ax.get_yticklabels() else left_ax.get_window_extent(ren).x0
    x1 = right_ax.get_window_extent(ren).x1
    xlab = bottom_ax.xaxis.label
    y_top = top_px if top_px is not None else (xlab.get_window_extent(ren).y0 if xlab.get_text() else bottom_ax.get_window_extent(ren).y0)
    if ncol:
        leg = fig.legend(handles, labels, frameon=False, loc="upper left", bbox_to_anchor=(x0 / W, (y_top - gap) / H),
                         bbox_transform=fig.transFigure, ncol=ncol, fontsize=9, handlelength=1.8, columnspacing=1.4)
        fig.canvas.draw()
        y_top = leg.get_window_extent(ren).y0 - gap
    else:
        y_top = y_top - gap
    fig.text(x0 / W, y_top / H, wrap_to_px(fig, ren, note, x1 - x0), ha="left", va="top", fontsize=8, color=INK, linespacing=1.4)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", dpi=200, facecolor="white", pad_inches=0.04)
    plt.close(fig)
    print(f"saved {stem}.pdf/.svg/.png")


def admin_spans(years):
    """(name, first year, last year) for each administration inside the plotted years."""
    return [(n, max(lo, years[0]), min(hi, years[-1])) for n, lo, hi in ADMIN_YEARS if lo <= years[-1] and hi >= years[0]]


def admin_boundaries(ax, years, lw=0.7):
    for _, lo, _ in admin_spans(years)[1:]:
        ax.axvline(lo - 0.5, color=CHARCOAL, lw=lw, alpha=0.6)


def admin_top_labels(ax, years):
    top = ax.secondary_xaxis("top")
    top.spines["top"].set_visible(False)
    spans = admin_spans(years)
    top.set_xticks([(lo + hi) / 2 for _, lo, hi in spans])
    top.set_xticklabels([ADMIN_SHORT[n] for n, _, _ in spans], fontsize=8.5)
    top.tick_params(length=0, pad=2)
    return top


def short(label, limit):
    """Truncate at a word boundary with an ellipsis."""
    if len(label) <= limit:
        return label
    cut = label[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",;:") + "…"


def sample_note(rec):
    return (f"Note: {len(rec):,} legislator stance records (prompt stance-extraction-0.3-dev) placed on codebook v1.0, "
            f"House Science and Senate Commerce hearings held {YEAR_MIN}-{YEAR_MAX}. A record is one member position: "
            "cited sentences, an issue, and support or concern. Years are hearing held years; administrations are "
            "calendar-year blocks (Bush 2001-2008, Obama 2009-2016, Trump 2017-2020, Biden 2021-2024, Trump 2025).")


def fig_volume(metrics, rec):
    m = metrics.sort_values("n")
    fig, ax = plt.subplots(figsize=(7.4, 8.6))
    y = np.arange(len(m))
    ax.barh(y, m.support, height=0.62, color=NAVY, label="Support records")
    ax.barh(y, -m.concern, height=0.62, color=RED, label="Concern records")
    ax.axvline(0, color=CHARCOAL, lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([short(l, 50) for l in m.label], fontsize=8.5)
    ax.set_ylabel("Topic (codebook v1.0), most records at top")
    ax.set_xlabel("Stance records per topic (concern ← 0 → support)")
    lim = max(m.support.max(), m.concern.max()) * 1.06
    ax.set_xlim(-lim, lim)
    ticks = np.arange(-int(lim // 200) * 200, int(lim // 200) * 200 + 1, 200)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{abs(v):,}" for v in ticks])
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_ylim(-0.6, len(m) - 0.4)
    right = ax.twinx()
    right.set_ylim(ax.get_ylim())
    right.set_yticks(y)
    right.set_yticklabels([f"{s:.2f}" for s in m.support_share], fontsize=8.5)
    right.tick_params(length=0, pad=4)
    right.spines["right"].set_visible(False)
    right.set_ylabel("Support share", rotation=270, labelpad=14)
    h, l = ax.get_legend_handles_labels()
    finish(fig, "fig_select_volume_balance", sample_note(rec) + f" The {TOP_N} topics with the most records. Bar length is the "
           "record count on each side of zero; the right margin gives support records as a share of all records on the topic.",
           ax, right_ax=right, handles=h, labels=l, ncol=2)


def heat_grid(metrics, rec, value, stem, cmap, vmin, vmax, cbar_label, note_tail, mask_below=0):
    order = metrics.sort_values("delta_net", key=lambda s: -s.abs())
    years = list(range(YEAR_MIN, YEAR_MAX + 1))
    grid = np.full((len(order), len(years)), np.nan)
    for i, t in enumerate(order.topic_id):
        y = yearly(rec[rec.topic_id == t])
        vals = y[value].to_numpy(float)
        if mask_below:
            vals = np.where(y.n >= mask_below, vals, np.nan)
        grid[i] = vals
    fig, ax = plt.subplots(figsize=(7.8, 8.4))
    im = ax.imshow(grid, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest",
                   extent=(years[0] - 0.5, years[-1] + 0.5, len(order) - 0.5, -0.5))
    ax.set_facecolor("white")
    for i in range(len(order) + 1):
        ax.axhline(i - 0.5, color="white", lw=0.5)
    for yv in years:
        ax.axvline(yv - 0.5, color="white", lw=0.5)
    admin_boundaries(ax, years, lw=0.9)
    admin_top_labels(ax, years)
    ax.set_xticks(years)
    ax.set_xticklabels([str(v) if v % 2 else "" for v in years], fontsize=7.5, rotation=90)
    ax.tick_params(axis="x", length=2)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{short(l, 46)}  (n = {n:,})" for l, n in zip(order.label, order.n)], fontsize=8)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Hearing year; vertical lines mark changes of administration")
    ax.set_ylabel("Topic, largest shift at the best break year at top")
    for s in ax.spines.values():
        s.set_visible(False)
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    dpi, W, H = fig.dpi, fig.bbox.width, fig.bbox.height
    gap = 0.3 * CM_IN * dpi
    x0 = ax.yaxis.label.get_window_extent(ren).x0
    xlab_bot = ax.xaxis.label.get_window_extent(ren).y0
    cb_h = 0.014 * H
    cax = fig.add_axes([x0 / W, (xlab_bot - gap - cb_h) / H, 0.34, cb_h / H])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label(cbar_label, size=8.5)
    cax.tick_params(labelsize=8)
    cax.xaxis.label.set_horizontalalignment("left")
    cax.xaxis.label.set_position((0.0, 0))
    fig.canvas.draw()
    cb_bot = min(cax.get_window_extent(ren).y0, cax.xaxis.label.get_window_extent(ren).y0)
    finish(fig, stem, sample_note(rec) + " " + note_tail, ax, top_px=cb_bot)


def fig_small_multiples(metrics, rec):
    order = metrics.sort_values("delta_net", key=lambda s: -s.abs()).reset_index(drop=True)
    years = np.arange(YEAR_MIN, YEAR_MAX + 1)
    ncol, nrow = 5, 6
    fig, axes = plt.subplots(nrow, ncol, figsize=(8.2, 9.4), sharex=True, sharey=True)
    for ax, (_, m) in zip(axes.ravel(), order.iterrows()):
        r = rec[rec.topic_id == m.topic_id]
        y = yearly(r)
        a = by_admin(r)
        shown = y.net.where(y.n >= MIN_CELL_YEAR)
        ax.axhline(0, color=RED, lw=0.7, ls=(0, (3, 2)))
        for name, lo, hi in admin_spans(list(years)):
            if a.loc[name, "n"] >= MIN_CELL_ADMIN:
                ax.plot([lo - 0.5, hi + 0.5], [a.loc[name, "net"]] * 2, color=GREEN, lw=2.2, solid_capstyle="butt")
        ax.plot(years, shown, color=NAVY, lw=0.9, marker="o", ms=2.6, mec="white", mew=0.4)
        admin_boundaries(ax, list(years), lw=0.5)
        ax.set_ylim(-1.08, 1.08)
        ax.set_yticks([-1, 0, 1])
        ax.set_xlim(YEAR_MIN - 0.8, YEAR_MAX + 0.8)
        ax.set_xticks([2001, 2009, 2017, 2021])
        ax.set_xticklabels(["'01", "'09", "'17", "'21"], fontsize=7.5)
        ax.tick_params(length=2, labelsize=7.5)
        ax.yaxis.grid(True, color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        ax.set_title(f"{short(m.label, 31)}\nn = {m.n:,}, Δ = {m.delta_net:+.2f} at {int(m.break_year)}", fontsize=7.6, loc="left", pad=3)
    for ax in axes[-1]:
        ax.set_xlabel("Hearing year", fontsize=9)
    for ax in axes[:, 0]:
        ax.set_ylabel("Net stance", fontsize=9)
    fig.subplots_adjust(hspace=0.62, wspace=0.18, left=0.07, right=0.99, top=0.96, bottom=0.12)
    handles = [Line2D([], [], color=NAVY, lw=0.9, marker="o", ms=3.5, mec="white"), Line2D([], [], color=GREEN, lw=2.2),
               Line2D([], [], color=RED, lw=0.8, ls=(0, (3, 2))), Line2D([], [], color=CHARCOAL, lw=0.6, alpha=0.6)]
    labels = [f"Yearly net stance (years with at least {MIN_CELL_YEAR} records)", f"Administration mean (at least {MIN_CELL_ADMIN} records)",
              "Balanced (net stance = 0)", "Change of administration"]
    finish(fig, "fig_select_small_multiples", sample_note(rec) + " Net stance = (support - concern) / records. Panels are ordered by the "
           "absolute change in net stance at each topic's best single break year, which the panel title reports; x ticks mark "
           "inauguration years.", axes[-1, 0], right_ax=axes[-1, -1], bottom_ax=axes[-1, 0], handles=handles, labels=labels, ncol=2)


def fig_break_dumbbell(metrics, rec):
    m = metrics.sort_values("delta_net", key=lambda s: s.abs())
    fig, ax = plt.subplots(figsize=(7.4, 8.6))
    y = np.arange(len(m))
    for i, (_, row) in enumerate(m.iterrows()):
        ax.plot([row.net_before, row.net_after], [i, i], color=NAVY, lw=1.1, zorder=2)
    ax.scatter(m.net_before, y, s=34, facecolor="white", edgecolor=NAVY, lw=1.1, zorder=3, label="Net stance before the break year")
    ax.scatter(m.net_after, y, s=34, color=NAVY, zorder=4, label="Net stance from the break year on")
    ax.axvline(0, color=RED, lw=0.8, ls=(0, (3, 2)))
    ax.set_yticks(y)
    ax.set_yticklabels([short(l, 50) for l in m.label], fontsize=8.5)
    ax.set_ylabel("Topic, largest change at top")
    ax.set_xlabel("Net stance = (support - concern) / records")
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_ylim(-0.6, len(m) - 0.4)
    right = ax.twinx()
    right.set_ylim(ax.get_ylim())
    right.set_yticks(y)
    right.set_yticklabels([f"{int(b)}   {d:+.2f}{'' if p < SHIFT_P else '  (p = %.2f)' % p}" for b, d, p in zip(m.break_year, m.delta_net, m.p_break)], fontsize=8.5)
    right.tick_params(length=0, pad=4)
    right.spines["right"].set_visible(False)
    right.set_ylabel("Break year and change in net stance", rotation=270, labelpad=14)
    h, l = ax.get_legend_handles_labels()
    finish(fig, "fig_select_break_shift", sample_note(rec) + f" For each topic the break year is the year that maximizes the change in support "
           f"share between all records before it and all records from it on, with at least {MIN_SIDE_BREAK} records on each side. "
           f"The right margin gives that year and the change in net stance; a p-value is printed only when a Welch test does not "
           f"reject equal support shares at {SHIFT_P}.", ax, right_ax=right, handles=h, labels=l, ncol=1)


def fig_candidate(rec, metrics_row, stem):
    r = rec[rec.topic_id == metrics_row.topic_id]
    y = yearly(r)
    a = by_admin(r)
    years = y.index.to_numpy()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 6.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.25], "hspace": 0.1})
    ax1.bar(years, y.support, width=0.72, color=NAVY, label="Support records")
    ax1.bar(years, -y.concern, width=0.72, color=RED, label="Concern records")
    ax1.axhline(0, color=CHARCOAL, lw=0.8)
    lim = max(y.support.max(), y.concern.max()) * 1.15
    ax1.set_ylim(-lim, lim)
    ax1.set_yticks([t for t in ax1.get_yticks() if abs(t) <= lim])
    ax1.set_yticklabels([f"{abs(int(t))}" for t in ax1.get_yticks()])
    ax1.set_ylabel("Records per year\n(concern below, support above)")
    ax1.yaxis.grid(True, color=GRID, lw=0.6)
    ax1.set_axisbelow(True)
    admin_boundaries(ax1, list(years))
    admin_top_labels(ax1, list(years))
    shown = y[y.n >= MIN_CELL_YEAR]
    ax2.axhline(0, color=RED, lw=0.8, ls=(0, (3, 2)))
    for name, lo, hi in admin_spans(list(years)):
        if a.loc[name, "n"] >= MIN_CELL_ADMIN:
            ax2.plot([lo - 0.5, hi + 0.5], [a.loc[name, "net"]] * 2, color=GREEN, lw=2.6, solid_capstyle="butt", zorder=2)
    ax2.errorbar(shown.index, shown.net, yerr=[shown.net - shown.net_lo, shown.net_hi - shown.net], fmt="o", color=NAVY, ms=4.2,
                 mec="white", mew=0.5, lw=0.9, capsize=0, zorder=3)
    ax2.plot(shown.index, shown.net, color=NAVY, lw=0.8, zorder=2)
    admin_boundaries(ax2, list(years))
    ax2.set_ylim(-1.05, 1.05)
    ax2.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax2.set_ylabel("Net stance\n(support - concern) / records")
    ax2.set_xlabel("Hearing year; vertical lines mark changes of administration")
    ax2.set_xticks(years)
    ax2.set_xticklabels([str(v) if v % 2 else "" for v in years], rotation=90, fontsize=8)
    ax2.yaxis.grid(True, color=GRID, lw=0.6)
    ax2.set_axisbelow(True)
    ax2.set_xlim(YEAR_MIN - 0.7, YEAR_MAX + 0.7)
    handles = [Patch(color=NAVY), Patch(color=RED), Line2D([], [], color=NAVY, lw=0.8, marker="o", ms=4, mec="white"),
               Line2D([], [], color=GREEN, lw=2.6), Line2D([], [], color=RED, lw=0.8, ls=(0, (3, 2)))]
    labels = ["Support records", "Concern records", f"Yearly net stance with 95% Wilson interval (at least {MIN_CELL_YEAR} records)",
              f"Administration mean (at least {MIN_CELL_ADMIN} records)", "Balanced (net stance = 0)"]
    m = metrics_row
    finish(fig, stem, sample_note(rec) + f" Topic {m.topic_id}, {m.label}: {m.n:,} records from {m.n_hearings:,} hearings and "
           f"{m.n_legislators:,} legislators; support share {m.support_share:.2f}. Best single break year {int(m.break_year)}: net stance "
           f"{m.net_before:+.2f} before, {m.net_after:+.2f} after.", ax2, bottom_ax=ax2, handles=handles, labels=labels, ncol=2)


# ------------------------------------------------------------ sentences --
def write_sentences(rec, metrics, data_root, topic_ids):
    """Seeded sample of cited sentences for each shortlisted topic, split at the break
    year and by stance, so that the labels can be read against their sources."""
    turns = pd.read_parquet(data_root / "interim/topics/track2/member_turns.parquet", columns=["packageId", "turn_idx", "sentences"],
                            filters=[("packageId", "in", sorted(rec[rec.topic_id.isin(topic_ids)].packageId.unique()))])
    turns = turns.rename(columns={"sentences": "turn_sentences"})
    rng = np.random.default_rng(SEED)
    for t in topic_ids:
        m = metrics.set_index("topic_id").loc[t]
        r = rec[rec.topic_id == t].merge(turns, on=["packageId", "turn_idx"], how="left", validate="m:1")
        assert r.turn_sentences.notna().all()
        r["text"] = [" ".join(ts[i - 1] for i in idx) for ts, idx in zip(r.turn_sentences, r.sentences)]
        b = int(m.break_year)
        lines = [f"# Topic {t}: {m.label}", "", f"Theme: {m.theme}. Records {m.n:,}; support share {m.support_share:.2f}; "
                 f"best break year {b} (net {m.net_before:+.2f} before, {m.net_after:+.2f} from {b} on).", "",
                 "Each block is a seeded random sample of records. Text is the cited sentence(s) from the cleaned legislator turn; "
                 "the issue phrase is the model's own wording before placement on the codebook.", ""]
        for period, mask in [(f"Before {b}", r.hyear < b), (f"From {b} on", r.hyear >= b)]:
            for stance in ["support", "concern"]:
                sub = r[mask & r.stance.eq(stance)]
                k = min(10, len(sub))
                lines += [f"## {period}: {stance} ({len(sub):,} records, {k} shown)", ""]
                for _, row in sub.iloc[rng.choice(len(sub), k, replace=False)].sort_values("hyear").iterrows() if k else []:
                    who = f"{row.honorific} {row.surname}".strip() if row.surname else "The Chair"
                    lines.append(f"- **{row.hyear}, {who} ({row.chamber.title()})**, issue \"{row.topic}\" (sim {row.sim:.2f}): {row.text}")
                lines.append("")
        (OUT / f"stance_sentences_topic_{t}.md").write_text("\n".join(lines))
        print(f"saved stance_sentences_topic_{t}.md ({len(r):,} records)")


def write_table(metrics):
    cols = ["topic_id", "label", "n", "support_share", "n_hearings", f"years_ge_{MIN_CELL_YEAR}", "admin_range", "p_admin",
            "break_year", "net_before", "net_after", "delta_net", "p_break", "r2_break", "net_majority_R", "net_majority_D", "p_majority",
            "firms_high_similarity", "balanced", "clear_shift", "shortlist"]
    t = metrics[cols].copy()
    for c in ["support_share", "admin_range", "net_before", "net_after", "delta_net", "r2_break", "net_majority_R", "net_majority_D"]:
        t[c] = t[c].map(lambda v: "" if pd.isna(v) else f"{v:.2f}")
    for c in ["p_admin", "p_break", "p_majority"]:
        t[c] = t[c].map(lambda v: "" if pd.isna(v) else ("<0.001" if v < 0.001 else f"{v:.3f}"))
    t["break_year"] = t.break_year.map(lambda v: "" if pd.isna(v) else str(int(v)))
    for c in ["balanced", "clear_shift", "shortlist"]:
        t[c] = t[c].map({True: "yes", False: ""})
    header = "| " + " | ".join(cols) + " |\n|" + "|".join(["---"] * len(cols)) + "|\n"
    body = "\n".join("| " + " | ".join(str(v) for v in row) + " |" for row in t.itertuples(index=False))
    (OUT / "topic_selection_table.md").write_text(header + body + "\n")


def main(data_root, figures=True):
    style()
    rec, codebook = load_records(data_root)
    metrics = build_metrics(rec, codebook, data_root)
    OUT.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUT / "topic_selection_metrics.csv", index=False)
    write_table(metrics)
    shortlist = metrics[metrics.shortlist].sort_values("delta_net", key=lambda s: -s.abs())
    summary = {"records_in_window": int(len(rec)), "topics_screened": int(len(metrics)),
               "shortlist": shortlist[["topic_id", "label", "n", "support_share", "break_year", "delta_net", "p_admin"]].round(3).to_dict("records"),
               "rules": {"balance_band": BALANCE_BAND, "shift_range": SHIFT_RANGE, "shift_p": SHIFT_P, "min_cell_admin": MIN_CELL_ADMIN,
                         "min_cell_year": MIN_CELL_YEAR, "min_side_break": MIN_SIDE_BREAK, "years": [YEAR_MIN, YEAR_MAX]}}
    (OUT / "topic_selection_summary.json").write_text(json.dumps(summary, indent=2, default=float) + "\n")
    print(metrics[["topic_id", "label", "n", "support_share", "admin_range", "p_admin", "break_year", "delta_net", "r2_break", "shortlist"]]
          .round(3).to_string(index=False))
    print(f"\nshortlist ({len(shortlist)}): {shortlist.topic_id.tolist()}")
    review_ids = shortlist.topic_id.tolist() + [t for t in [68] if t not in shortlist.topic_id.tolist() and t in metrics.topic_id.tolist()]
    write_sentences(rec, metrics, data_root, review_ids)
    if figures:
        fig_volume(metrics, rec)
        heat_grid(metrics, rec, "n", "fig_select_attention_by_year", "Blues", 0, np.nanquantile(np.r_[[yearly(rec[rec.topic_id == t]).n for t in metrics.topic_id]], 0.98),
                  "Stance records in the cell (count)", "Color depth is the number of records a topic drew in a hearing year; the darkest shade is capped at the 98th percentile of cells.")
        heat_grid(metrics, rec, "net", "fig_select_net_by_year", DIVERGE, -1, 1, "Net stance: (support - concern) / records",
                  f"Red = concern-dominant, navy = support-dominant, gray = balanced; cells with fewer than {MIN_CELL_YEAR} records are blank.", mask_below=MIN_CELL_YEAR)
        fig_small_multiples(metrics, rec)
        fig_break_dumbbell(metrics, rec)
        for t in review_ids:
            fig_candidate(rec, metrics[metrics.topic_id == t].iloc[0], f"fig_select_topic_{t}")
    return metrics


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-root", type=Path, default=DEFAULT_DATA)
    p.add_argument("--no-figures", action="store_true")
    a = p.parse_args()
    main(a.data_root, not a.no_figures)
