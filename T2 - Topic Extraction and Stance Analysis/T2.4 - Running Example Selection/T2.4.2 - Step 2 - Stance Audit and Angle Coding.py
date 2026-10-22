"""Audit every stance record of the candidate topics and code its angle and direction.

`export` writes one readable line per record (year, speaker, model label, issue
phrase, cited sentences) for each topic, plus a key file. The records are then read
one by one and coded by hand into `audit/codes_topic_<id>.csv` with four fields:
record number, verdict on the model's label, angle, and policy direction. The codes
are data, not model output; the coder and pass are recorded in the file header.

`aggregate` joins the codes back to the records, refuses to run on incomplete
coverage, and writes the label-agreement summary, angle-by-year and direction-by-
year tables, and the figures. No model is run.
"""

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import importlib.util

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("select", HERE / "T2.4.1 - Step 1 - Topic Screening.py")
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

OUT = HERE / "output" / Path(__file__).stem
AUDIT = OUT / "audit"
TOPICS = [68, 78, 21]

VERDICTS = ["ok", "inverted", "nostance", "offtopic"]
DIRECTIONS = ["pro", "anti", "none"]
# Direction is defined per topic as favoring the policy object itself.
DIRECTION_MEANING = {68: ("stronger consumer privacy protection", "less privacy regulation"),
                     78: ("stronger environmental regulation or a stronger EPA", "less environmental regulation"),
                     21: ("expanding nuclear energy research and deployment", "restricting or scaling back nuclear energy"),
                     26: ("expanding renewable energy and storage (research, deployment, support)", "scaling back renewable energy support"),
                     65: ("stronger consumer privacy and anti-spam protection", "less privacy or anti-spam regulation")}
ANGLES = {
    68: {"LAW": "Federal or comprehensive privacy legislation", "HARM": "Privacy harms from commercial data collection and use",
         "CONTROL": "Consumer control: consent, opt-in/opt-out, transparency, access", "SECURITY": "Data security and breach rules",
         "ENFORCE": "Enforcement, agency authority and resources (FTC, FCC)", "BURDEN": "Regulatory burden, preemption, innovation cost",
         "SECTOR": "Sector- or technology-specific privacy (children, health, cars, drones, ISPs, AI)",
         "GOVT": "Government handling of personal data and surveillance", "OFF": "Not about consumer data privacy"},
    78: {"OVERREACH": "EPA rules as burdensome, costly, or overreaching", "SCIENCE": "EPA science, process, and advisory boards",
         "RULE": "A specific rule or standard (water, air, greenhouse gas, chemicals)", "HEALTH": "Pollution and public-health harms",
         "AGENCY": "EPA mission, budget, staffing, and leadership", "LIABILITY": "Enforcement, cleanup, and polluter liability",
         "STATE": "Federal-state roles and permitting", "OFF": "Not about EPA or environmental regulation"},
    21: {"GENERAL": "Nuclear power as an energy source, in general", "FUSION": "Fusion research (ITER, fusion programs)",
         "ADVANCED": "Advanced reactors, fuel cycle, demonstrations", "WASTE": "Nuclear waste, storage, and reprocessing",
         "SAFETY": "Safety, accidents, proliferation, and oversight", "FUNDING": "Program funding, budget cuts, DOE management, workforce",
         "COMPETE": "International competition, leadership, and supply chain", "ECON": "Economics, subsidies, and market viability",
         "OFF": "Not about nuclear energy"},
    26: {"RDFUND": "Federal R&D programs and funding for renewables and storage", "DEPLOY": "Deployment policy: incentives, mandates, tax credits, standards",
         "TECH": "Merits or limits of a specific technology (solar, wind, storage, hydrogen, EVs, biofuels)",
         "GRID": "Grid integration, reliability, intermittency, transmission", "COST": "Cost, energy prices, ratepayers, economic burden",
         "SUPPLY": "Supply chain, critical minerals, China dependence, domestic manufacturing",
         "SITING": "Environmental, land, wildlife, and siting impacts of renewables", "CLIMATE": "Climate and emissions rationale, or skepticism of it",
         "INDEP": "Energy independence and security rationale", "OFF": "Not about renewable energy or storage"},
    65: {"SPAM": "Spam, robocalls, telemarketing, junk fax, do-not-call", "PRIVACY": "Consumer data privacy in general",
         "CHILD": "Children's online privacy and protection", "FRAUD": "Scams, identity theft, deceptive practices",
         "SECURITY": "Data security and breaches", "ENFORCE": "FTC, FCC authority, penalties, enforcement",
         "BURDEN": "Regulatory burden, preemption, innovation cost", "GOVT": "Government handling of personal data and surveillance",
         "OFF": "Not about consumer privacy or spam"},
}


def load(topic_ids):
    rec, codebook = S.load_records(S.DEFAULT_DATA)
    rec = rec[rec.topic_id.isin(topic_ids)].copy()
    turns = pd.read_parquet(S.DEFAULT_DATA / "interim/topics/track2/member_turns.parquet", columns=["packageId", "turn_idx", "sentences"],
                            filters=[("packageId", "in", sorted(rec.packageId.unique()))]).rename(columns={"sentences": "turn_sentences"})
    rec = rec.merge(turns, on=["packageId", "turn_idx"], how="left", validate="m:1")
    assert rec.turn_sentences.notna().all()
    rec["text"] = [" ".join(ts[i - 1] for i in idx) for ts, idx in zip(rec.turn_sentences, rec.sentences)]
    rec["speaker"] = [f"{h} {s}".strip() if s else "The Chair" for h, s in zip(rec.honorific.fillna(""), rec.surname.fillna(""))]
    rec = rec.sort_values(["topic_id", "hyear", "packageId", "turn_idx", "record_idx"]).reset_index(drop=True)
    return rec, codebook


def export(topic_ids):
    AUDIT.mkdir(parents=True, exist_ok=True)
    rec, codebook = load(topic_ids)
    for t in topic_ids:
        r = rec[rec.topic_id == t].reset_index(drop=True)
        r.insert(0, "rid", np.arange(1, len(r) + 1))
        keys = r[["rid", "packageId", "turn_idx", "record_idx", "hyear", "chamber", "bioGuideId", "speaker", "topic", "stance", "sim", "text"]]
        keys.to_csv(AUDIT / f"records_topic_{t}.csv", index=False)
        lines = [f"R{row.rid} | {row.hyear} | {row.speaker} ({row.chamber.title()}) | {row.stance.upper()} | issue: {row.topic} | {row.text}"
                 for row in r.itertuples()]
        (AUDIT / f"records_topic_{t}.txt").write_text("\n".join(lines) + "\n")
        print(f"topic {t}: {len(r):,} records, {sum(len(l) for l in lines):,} characters -> records_topic_{t}.txt")


def read_codes(t):
    path = AUDIT / f"codes_topic_{t}.csv"
    codes = pd.read_csv(path, comment="#")
    codes.columns = [c.strip() for c in codes.columns]
    for c in ["verdict", "angle", "direction"]:
        codes[c] = codes[c].str.strip()
    assert codes.rid.is_unique, "duplicate record ids in codes"
    assert codes.verdict.isin(VERDICTS).all(), codes.loc[~codes.verdict.isin(VERDICTS)]
    assert codes.direction.isin(DIRECTIONS).all(), codes.loc[~codes.direction.isin(DIRECTIONS)]
    assert codes.angle.isin(ANGLES[t]).all(), codes.loc[~codes.angle.isin(ANGLES[t])]
    return codes


def aggregate(topic_ids, figures=True):
    S.style()
    summary = {}
    for t in topic_ids:
        keys = pd.read_csv(AUDIT / f"records_topic_{t}.csv")
        codes = read_codes(t)
        missing = sorted(set(keys.rid) - set(codes.rid))
        assert not missing, f"topic {t}: {len(missing)} records not coded, first {missing[:10]}"
        extra = sorted(set(codes.rid) - set(keys.rid))
        assert not extra, f"topic {t}: unknown record ids {extra[:10]}"
        d = keys.merge(codes, on="rid", validate="1:1")
        d["verified_stance"] = np.where(d.verdict.eq("ok"), d.stance, np.where(d.verdict.eq("inverted"), d.stance.map({"support": "concern", "concern": "support"}), "none"))
        d.to_csv(AUDIT / f"audit_topic_{t}.csv", index=False)
        usable = d[d.verdict.isin(["ok", "inverted"])]
        by_year = (d.groupby("hyear").agg(records=("rid", "size"), usable=("verdict", lambda v: v.isin(["ok", "inverted"]).sum()),
                                          pro=("direction", lambda v: v.eq("pro").sum()), anti=("direction", lambda v: v.eq("anti").sum()))
                   .reindex(range(S.YEAR_MIN, S.YEAR_MAX + 1), fill_value=0))
        by_year["net_direction"] = (by_year.pro - by_year.anti) / (by_year.pro + by_year.anti).replace(0, np.nan)
        by_year.to_csv(AUDIT / f"direction_year_topic_{t}.csv")
        angle_year = pd.crosstab([usable.hyear, usable.verified_stance], usable.angle).reindex(columns=list(ANGLES[t]), fill_value=0)
        angle_year.to_csv(AUDIT / f"angle_year_topic_{t}.csv")
        angle_stance = pd.crosstab(usable.angle, usable.verified_stance).reindex(index=list(ANGLES[t]), fill_value=0)
        angle_dir = pd.crosstab(d.angle, d.direction).reindex(index=list(ANGLES[t]), columns=DIRECTIONS, fill_value=0)
        confusion = pd.crosstab(d.stance, d.verified_stance)
        summary[t] = {"records": int(len(d)), "verdicts": d.verdict.value_counts().to_dict(),
                      "label_agreement_among_stance_records": float(d.verdict.eq("ok").sum() / d.verdict.isin(["ok", "inverted"]).sum()),
                      "label_agreement_all_records": float(d.verdict.eq("ok").mean()),
                      "confusion_model_rows_verified_columns": {str(k): v for k, v in confusion.to_dict(orient="index").items()},
                      "angle_by_verified_stance": {str(k): v for k, v in angle_stance.to_dict(orient="index").items()},
                      "angle_by_direction": {str(k): v for k, v in angle_dir.to_dict(orient="index").items()},
                      "direction_counts": d.direction.value_counts().to_dict(),
                      "direction_meaning": {"pro": DIRECTION_MEANING[t][0], "anti": DIRECTION_MEANING[t][1]}}
        print(f"\n=== topic {t}: {len(d):,} records ===")
        print("verdicts:", summary[t]["verdicts"])
        print(f"label agreement among stance records: {summary[t]['label_agreement_among_stance_records']:.3f}")
        print(confusion.to_string())
        print(angle_stance.to_string())
        print(angle_dir.to_string())
        if figures:
            fig_angles(t, d, usable)
            fig_direction(t, d, by_year)
    (AUDIT / "audit_summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def note_audit(t, d):
    return (f"Note: all {len(d):,} Track 2 stance records placed on topic {t} (codebook v1.0), House Science and "
            f"Senate Commerce hearings held {S.YEAR_MIN}-{S.YEAR_MAX}. Each record was read against its cited sentences in a single "
            "assistant coding pass (Claude, 2026-10-22) and given a verdict on the model's label, an angle, and a policy direction; "
            "no human review yet. Years are hearing held years.")


def fig_angles(t, d, usable):
    angles = [a for a in ANGLES[t] if a != "OFF"]
    years = np.arange(S.YEAR_MIN, S.YEAR_MAX + 1)
    ncol = 2
    nrow = int(np.ceil(len(angles) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(7.6, 1.55 * nrow + 1.2), sharex=True, sharey=True)
    axes = np.atleast_2d(axes)
    lim = 0
    panels = []
    for ax, a in zip(axes.ravel(), angles):
        sub = usable[usable.angle.eq(a)]
        sup = sub[sub.verified_stance.eq("support")].groupby("hyear").size().reindex(years, fill_value=0)
        con = sub[sub.verified_stance.eq("concern")].groupby("hyear").size().reindex(years, fill_value=0)
        ax.bar(years, sup, width=0.75, color=S.NAVY)
        ax.bar(years, -con, width=0.75, color=S.RED)
        ax.axhline(0, color=S.CHARCOAL, lw=0.6)
        S.admin_boundaries(ax, list(years), lw=0.5)
        ax.set_title(f"{S.short(ANGLES[t][a], 46)} (n = {len(sub):,})", fontsize=8, loc="left", pad=2)
        ax.yaxis.grid(True, color=S.GRID, lw=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(labelsize=7.5, length=2)
        lim = max(lim, sup.max(), con.max())
        panels.append(ax)
    for ax in axes.ravel()[len(angles):]:
        ax.set_visible(False)
    lim = lim * 1.1
    for ax in panels:
        ax.set_ylim(-lim, lim)
        ticks = [v for v in ax.get_yticks() if abs(v) <= lim]
        ax.set_yticks(ticks)
        ax.set_yticklabels([f"{abs(int(v))}" for v in ticks])
    for j in range(ncol):
        column = [ax for ax in axes[:, j] if ax.get_visible()]
        column[-1].set_xlabel("Hearing year", fontsize=9)
        column[-1].set_xticks([2001, 2009, 2017, 2021])
        column[-1].tick_params(labelbottom=True)
    for ax in axes[:, 0]:
        ax.set_ylabel("Records (concern below)", fontsize=8.5)
    fig.subplots_adjust(hspace=0.55, wspace=0.12, left=0.09, right=0.99, top=0.95, bottom=0.1)
    handles = [Patch(color=S.NAVY), Patch(color=S.RED), Line2D([], [], color=S.CHARCOAL, lw=0.6, alpha=0.6)]
    labels = ["Verified support records", "Verified concern records", "Change of administration"]
    S.OUT = OUT
    S.finish(fig, f"fig_audit_angles_topic_{t}", note_audit(t, d) + " Panels are the angles of the topic; records judged to carry no stance "
             "or to be off-topic are excluded. x ticks mark inauguration years.", axes[-1, 0], right_ax=axes[0, -1], bottom_ax=axes[-1, 0],
             handles=handles, labels=labels, ncol=3)


def fig_direction(t, d, by_year):
    years = by_year.index.to_numpy()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 6.0), sharex=True, gridspec_kw={"height_ratios": [1, 1.1], "hspace": 0.1})
    ax1.bar(years, by_year.pro, width=0.72, color=S.NAVY)
    ax1.bar(years, -by_year.anti, width=0.72, color=S.RED)
    ax1.axhline(0, color=S.CHARCOAL, lw=0.8)
    lim = max(by_year.pro.max(), by_year.anti.max()) * 1.15
    ax1.set_ylim(-lim, lim)
    ticks = [v for v in ax1.get_yticks() if abs(v) <= lim]
    ax1.set_yticks(ticks)
    ax1.set_yticklabels([f"{abs(int(v))}" for v in ticks])
    pro, anti = DIRECTION_MEANING[t]
    ax1.set_ylabel("Records per year by direction\n(favoring less below, more above)")
    ax1.yaxis.grid(True, color=S.GRID, lw=0.6)
    ax1.set_axisbelow(True)
    S.admin_boundaries(ax1, list(years))
    S.admin_top_labels(ax1, list(years))
    shown = by_year[(by_year.pro + by_year.anti) >= S.MIN_CELL_YEAR]
    lo, hi = S.wilson(shown.pro, shown.pro + shown.anti)
    ax2.axhline(0, color=S.RED, lw=0.8, ls=(0, (3, 2)))
    # Wilson bounds sit inside [-1, 1] even when a year is unanimous, so clip the bars at the point.
    err_lo = np.maximum(0, shown.net_direction - (2 * lo - 1))
    err_hi = np.maximum(0, (2 * hi - 1) - shown.net_direction)
    ax2.errorbar(shown.index, shown.net_direction, yerr=[err_lo, err_hi], fmt="o",
                 color=S.NAVY, ms=4.2, mec="white", mew=0.5, lw=0.9, capsize=0, zorder=3)
    ax2.plot(shown.index, shown.net_direction, color=S.NAVY, lw=0.8, zorder=2)
    S.admin_boundaries(ax2, list(years))
    ax2.set_ylim(-1.05, 1.05)
    ax2.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax2.set_ylabel("Net direction\n(more - less) / directional records")
    ax2.set_xlabel("Hearing year; vertical lines mark changes of administration")
    ax2.set_xticks(years)
    ax2.set_xticklabels([str(v) if v % 2 else "" for v in years], rotation=90, fontsize=8)
    ax2.yaxis.grid(True, color=S.GRID, lw=0.6)
    ax2.set_axisbelow(True)
    ax2.set_xlim(S.YEAR_MIN - 0.7, S.YEAR_MAX + 0.7)
    handles = [Patch(color=S.NAVY), Patch(color=S.RED), Line2D([], [], color=S.NAVY, lw=0.8, marker="o", ms=4, mec="white"),
               Line2D([], [], color=S.RED, lw=0.8, ls=(0, (3, 2)))]
    labels = [f"Favors {pro}", f"Favors {anti}", f"Yearly net direction with 95% Wilson interval (at least {S.MIN_CELL_YEAR} directional records)",
              "Balanced"]
    S.OUT = OUT
    S.finish(fig, f"fig_audit_direction_topic_{t}", note_audit(t, d) + " Direction resolves the polarity of support and concern: a record favors "
             f"{pro} or {anti}, or neither (shown in neither panel).", ax2, bottom_ax=ax2, handles=handles, labels=labels, ncol=1)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["export", "aggregate"])
    p.add_argument("--topics", type=int, nargs="*", default=TOPICS)
    p.add_argument("--no-figures", action="store_true")
    a = p.parse_args()
    if a.command == "export":
        export(a.topics)
    else:
        aggregate(a.topics, not a.no_figures)
