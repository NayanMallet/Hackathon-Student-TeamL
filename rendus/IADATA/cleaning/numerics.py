from __future__ import annotations

import re
import pandas as pd
from cleaning.text_utils import safe_int, safe_float, wordnum_to_int


def normalize_integers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit quelques colonnes numériques usuelles en Int64 quand applicable.
    """
    for c in [
        "final_score_red",
        "final_score_blue",
        "player_goals",
        "player_own_goals",
        "player_assists",
        "player_saves",
        "mood",
    ]:
        if c in df.columns:
            df[c] = df[c].apply(safe_int).astype("Int64")
    return df


def normalize_ping_ms(df: pd.DataFrame) -> pd.DataFrame:
    if "ping_ms" in df.columns:
        df["ping_ms_value"] = df["ping_ms"].apply(lambda x: None if x in (None, "") else safe_int(str(x)))
        df["ping_ms_value"] = df["ping_ms_value"].astype("Int64")
    return df


def normalize_attendance_count(df: pd.DataFrame) -> pd.DataFrame:
    if "attendance_count" in df.columns:
        def parse_att(x: str | None) -> int | None:
            if not x:
                return None
            m = re.search(r"(\d+)", str(x))
            return int(m.group(1)) if m else None
        df["attendance_count_value"] = df["attendance_count"].apply(parse_att).astype("Int64")
    return df


def normalize_rating(df: pd.DataFrame) -> pd.DataFrame:
    mapping_emojis = {"👍": 4, "😡": 1, "🙂": 3, "😂": 3}
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

    def to_rating(x: str | None) -> int | None:
        if not x:
            return None
        s = str(x).strip()
        if "⭐" in s:
            n = s.count("⭐")
            return max(1, min(5, n))
        for k, v in mapping_emojis.items():
            if k in s:
                return v
        lw = s.lower()
        if lw in words:
            return words[lw]
        valf = safe_float(s)
        if valf is not None:
            n = int(round(valf))
            return max(1, min(5, n))
        return None

    df["rating_1to5"] = df.get("rating_raw", "").apply(to_rating).astype("Int64")
    return df


def normalize_player_age(df: pd.DataFrame) -> pd.DataFrame:
    def to_age(x: str | None) -> int | None:
        if not x:
            return None
        iv = safe_int(x)
        if iv is not None:
            return iv
        m = re.search(r"(\d+)", str(x))
        if m:
            try:
                return int(m.group(1))
            except Exception:
                pass
        w = wordnum_to_int(str(x))
        return w
    df["player_age_years"] = df.get("player_age", "").apply(to_age).astype("Int64")
    return df
