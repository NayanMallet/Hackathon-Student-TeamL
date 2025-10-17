#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"figure.figsize": (8, 5), "axes.grid": True})

NUM_COLS_GAME = [
    "final_score_red","final_score_blue",
    "game_duration_seconds","attendance_count_value",
    "possession_time_seconds","rating_1to5",
    "ping_ms_value","player_age_years",
]
GROUP_DIMS = [
    ("season_final", "Season"),
    ("location", "Location"),
    ("table_condition_norm", "TableCondition"),
    ("ball_type_norm", "BallType"),
]

def ensure_numeric(df, cols):
    out = {}
    for c in cols:
        if c in df.columns:
            out[c] = pd.to_numeric(df[c], errors="coerce")
    return pd.DataFrame(out)

def save_fig(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()

def normalize_winner_text(s: pd.Series) -> pd.Series:
    wr = s.astype(str).str.strip().str.lower().replace({
        "bleu":"blue","blu":"blue","b":"blue",
        "rouge":"red","r":"red"
    })
    wr = wr.where(wr.isin(["red","blue"]), "")
    return wr

def derive_winner_from_scores(df: pd.DataFrame) -> pd.Series:
    fr = pd.to_numeric(df.get("final_score_red"), errors="coerce")
    fb = pd.to_numeric(df.get("final_score_blue"), errors="coerce")
    out = pd.Series([""]*len(df), index=df.index, dtype="string")
    both = fr.notna() & fb.notna()
    out = out.mask(both & (fr > fb), "red")
    out = out.mask(both & (fr < fb), "blue")
    out = out.mask(both & (fr == fb), "draw")
    return out

def compute_winner_final(game_df: pd.DataFrame) -> pd.Series:
    base_col = "winner_final" if "winner_final" in game_df.columns else ("winner_norm" if "winner_norm" in game_df.columns else "winner")
    wr_text = normalize_winner_text(game_df[base_col]) if base_col in game_df.columns else pd.Series([""]*len(game_df), index=game_df.index, dtype="string")
    wr_scores = derive_winner_from_scores(game_df)
    wr = wr_text.where(wr_text.isin(["red","blue"]), wr_scores)
    return wr.where(wr.isin(["red","blue","draw"]), "")

def to_bool_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true","1","yes"])

def make_game_level(df: pd.DataFrame) -> pd.DataFrame:
    if "game_id_norm" not in df.columns: raise KeyError("game_id_norm missing")
    cols = [
        "final_score_red","final_score_blue",
        "winner_final","winner_norm","winner",
        "game_duration_seconds","attendance_count_value",
        "possession_time_seconds","rating_1to5","ping_ms_value",
        "player_age_years","season_final","location","table_condition_norm",
        "ball_type_norm","game_date_date","game_date_ts","created_at_ts",
        "row_incomplete","duration_suspicious","scores_missing","winner_conflict"
    ]
    agg_map = {c:"first" for c in cols if c in df.columns}
    return df.groupby("game_id_norm", as_index=False).agg(agg_map)

def group_kpis(game_df: pd.DataFrame, dim: str, wr_final: pd.Series) -> pd.DataFrame:
    out = pd.DataFrame()
    out["games"] = game_df.groupby(dim).size()
    if {"final_score_red","final_score_blue"}.issubset(game_df.columns):
        fsr = pd.to_numeric(game_df["final_score_red"], errors="coerce")
        fsb = pd.to_numeric(game_df["final_score_blue"], errors="coerce")
        out["avg_total_score"] = (fsr + fsb).groupby(game_df[dim]).mean()
    if "game_duration_seconds" in game_df.columns:
        gds = pd.to_numeric(game_df["game_duration_seconds"], errors="coerce")
        out["avg_duration_s"] = gds.groupby(game_df[dim]).mean()
    valid = wr_final.isin(["red","blue","draw"])
    denom = valid.groupby(game_df[dim]).sum().replace(0, np.nan)
    out["pct_blue_win"] = (wr_final.eq("blue").groupby(game_df[dim]).sum() / denom) * 100
    out["pct_red_win"]  = (wr_final.eq("red").groupby(game_df[dim]).sum() / denom) * 100
    out["pct_draw"]     = (wr_final.eq("draw").groupby(game_df[dim]).sum() / denom) * 100
    return out.sort_values("games", ascending=False)

def eda(csv_path: str, out_dir: str, fig_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True); os.makedirs(fig_dir, exist_ok=True)
    df = pd.read_csv(csv_path, dtype=str, encoding="utf-8")
    game_df = make_game_level(df)
    wr_final = compute_winner_final(game_df)

    missing_game = game_df.isna() | game_df.map(lambda x: str(x).strip() == "")
    missing_game.mean().sort_values(ascending=False).to_frame(name="missing_pct").to_csv(os.path.join(out_dir, "missingness_game.csv"))

    num_game = ensure_numeric(game_df, NUM_COLS_GAME)
    num_game.describe().T.to_csv(os.path.join(out_dir, "num_summary_game.csv"))

    wr_valid = wr_final[wr_final.isin(["red","blue","draw"])]
    if not wr_valid.empty:
        wr_valid.value_counts(normalize=True).to_csv(os.path.join(out_dir, "win_rate.csv"))

    if not num_game.empty:
        corr = num_game.corr(numeric_only=True)
        corr.to_csv(os.path.join(out_dir, "correlations_game.csv"))
        fig, ax = plt.subplots()
        cax = ax.imshow(corr.values, aspect="auto")
        ax.set_xticks(range(len(corr.columns))); ax.set_yticks(range(len(corr.index)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right"); ax.set_yticklabels(corr.index)
        fig.colorbar(cax); save_fig(os.path.join(fig_dir, "corr_heatmap_game.png"))

    for col in num_game.columns:
        x = pd.to_numeric(game_df[col], errors="coerce").dropna()
        if x.empty: continue
        plt.figure(); plt.hist(x, bins=20)
        plt.title(f"Distribution of {col} (match-level, n={len(x)})")
        plt.xlabel(col); plt.ylabel("Count")
        save_fig(os.path.join(fig_dir, f"hist_game_{col}.png"))

    if {"game_duration_seconds","final_score_red","final_score_blue"}.issubset(num_game.columns):
        dur = num_game["game_duration_seconds"]
        total_score = num_game["final_score_red"].fillna(0) + num_game["final_score_blue"].fillna(0)
        plt.figure(); plt.scatter(dur, total_score, alpha=0.6)
        plt.xlabel("game_duration_seconds"); plt.ylabel("total_score")
        plt.title("Total score vs game duration (match-level)")
        save_fig(os.path.join(fig_dir, "scatter_game_duration_total_score.png"))

    for dim, label in GROUP_DIMS:
        if dim in game_df.columns:
            kpis = group_kpis(game_df, dim, wr_final)
            kpis.to_csv(os.path.join(out_dir, f"group_kpis_game_{label}.csv"))
            top = kpis["games"].head(15)
            if not top.empty:
                plt.figure(); top.plot(kind="bar")
                plt.title(f"Games per {label} (match-level, top 15)")
                plt.ylabel("games")
                save_fig(os.path.join(fig_dir, f"bar_game_by_{label}.png"))

    flags = []
    for flag in ["row_incomplete","duration_suspicious","scores_missing","winner_conflict"]:
        if flag in game_df.columns:
            val = to_bool_series(game_df[flag]).mean()
            flags.append((flag, round(100*val, 2)))

    md = []
    md.append("# EDA Report — babyfoot_dataset_out.csv\n")
    md.append("- Missingness (match-level): `outputs/missingness_game.csv`\n")
    md.append("- Numeric summary (match-level): `outputs/num_summary_game.csv`\n")
    if not wr_valid.empty:
        md.append("- Win rate (red/blue/draw): `outputs/win_rate.csv`\n")
    md.append("- Correlation heatmap: `figures/corr_heatmap_game.png`\n")
    md.append("- Histograms: `figures/hist_game_*.png`\n")
    md.append("- Group KPIs: `outputs/group_kpis_game_*.csv`\n")
    md.append("- Scatter: `figures/scatter_game_duration_total_score.png`\n")
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="babyfoot_dataset_out.csv")
    ap.add_argument("--outdir", default=os.path.join("eda","outputs"))
    ap.add_argument("--figdir", default=os.path.join("eda","figures"))
    args = ap.parse_args()
    if not os.path.exists(args.csv):
        print(f"[ERR] CSV not found: {args.csv}", file=sys.stderr); sys.exit(1)
    os.makedirs(args.outdir, exist_ok=True); os.makedirs(args.figdir, exist_ok=True)
    eda(args.csv, args.outdir, args.figdir)

if __name__ == "__main__":
    main()


