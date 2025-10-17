from __future__ import annotations
import pandas as pd


def _season_from_date(ts: pd.Timestamp | None) -> str | None:
    """
    Saison du 1er août (inclus) au 31 juillet (inclus).
    Ex.: 2024-08-01 → '2024-2025' ; 2025-05-31 → '2024-2025'.
    """
    if ts is None or pd.isna(ts):
        return None
    dt = ts.tz_convert("UTC") if ts.tzinfo else pd.Timestamp(ts).tz_localize("UTC")
    y = dt.year
    if dt.month >= 8:
        return f"{y}-{y+1}"
    else:
        return f"{y-1}-{y}"


def normalize_season(df: pd.DataFrame) -> pd.DataFrame:
    df["season_from_date"] = df.get("game_date_ts").apply(_season_from_date)
    df["season_final"] = df["season_from_date"].where(df["season_from_date"].notna(), df.get("season"))
    return df
