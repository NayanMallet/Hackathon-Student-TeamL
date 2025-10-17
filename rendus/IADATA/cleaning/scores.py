from __future__ import annotations
import re
import pandas as pd


def _to_int(x):
    try:
        return int(float(str(x).replace(",", ".").strip()))
    except Exception:
        return None


def split_merged_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Si final_score_red OU final_score_blue contient 'A - B' (ou 'A:B') et l'autre est vide,
    on éclate proprement.
    """

    def parse_pair(s: str | None) -> tuple[int | None, int | None]:
        if not s:
            return (None, None)
        m = re.match(r"^\s*(\d+)\s*[-:]\s*(\d+)\s*$", str(s))
        if not m:
            return (None, None)
        return int(m.group(1)), int(m.group(2))

    new_red = []
    new_blue = []
    for r, b in zip(df.get("final_score_red"), df.get("final_score_blue")):
        r_int, b_int = _to_int(r), _to_int(b)
        if r_int is None and b_int is None:
            pr = parse_pair(r)
            pb = parse_pair(b)
            if pr != (None, None):
                new_red.append(pr[0]); new_blue.append(pr[1])
            elif pb != (None, None):
                new_red.append(pb[0]); new_blue.append(pb[1])
            else:
                new_red.append(None); new_blue.append(None)
        elif r_int is None and b_int is not None:
            pr = parse_pair(r)
            if pr != (None, None):
                new_red.append(pr[0]); new_blue.append(pr[1])
            else:
                new_red.append(None); new_blue.append(b_int)
        elif r_int is not None and b_int is None:
            pb = parse_pair(b)
            if pb != (None, None):
                new_red.append(pb[0]); new_blue.append(pb[1])
            else:
                new_red.append(r_int); new_blue.append(None)
        else:
            new_red.append(r_int); new_blue.append(b_int)

    df["final_score_red"] = pd.Series(new_red, index=df.index).astype("Int64")
    df["final_score_blue"] = pd.Series(new_blue, index=df.index).astype("Int64")
    return df


def reconcile_scores_and_winner(df: pd.DataFrame) -> pd.DataFrame:
    r = df.get("final_score_red")
    b = df.get("final_score_blue")

    df["winner_from_scores"] = None
    mask = r.notna() & b.notna()
    df.loc[mask & (r > b), "winner_from_scores"] = "red"
    df.loc[mask & (b > r), "winner_from_scores"] = "blue"

    if "winner_norm" not in df.columns:
        df["winner_norm"] = df.get("winner")

    df["winner_conflict"] = (
            df["winner_norm"].notna()
            & pd.Series(df["winner_from_scores"]).notna()
            & (df["winner_norm"] != df["winner_from_scores"])
    )

    df["winner_final"] = df["winner_from_scores"].where(
        pd.Series(df["winner_from_scores"]).notna(), df["winner_norm"]
    )

    return df
