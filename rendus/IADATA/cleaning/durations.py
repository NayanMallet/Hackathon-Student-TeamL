from __future__ import annotations

import re
import pandas as pd

from cleaning.text_utils import safe_float, safe_int


def _hms_to_seconds(text: str) -> int | None:
    if not text or ":" not in text:
        return None
    parts = text.split(":")
    try:
        parts = [int(p) for p in parts]
    except Exception:
        return None
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = 0, parts[0], parts[1]
    else:
        return None
    return h * 3600 + m * 60 + s


def parse_duration_to_seconds(s: str | None) -> int | None:
    if not s:
        return None
    s = str(s).strip().lower()

    hms = _hms_to_seconds(s)
    if hms is not None:
        return int(hms)

    m = re.match(r"^\s*(\d+(?:[\.,]\d+)?)\s*min(?:ute|utes)?\s*$", s)
    if m:
        minutes = float(m.group(1).replace(",", "."))
        return int(round(minutes * 60.0))

    f = safe_float(s)
    if f is not None:
        return int(round(f * 60.0))

    return None


def parse_time_to_seconds(s: str | None) -> int | None:
    if not s:
        return None
    s0 = str(s).strip().lower()

    hms = _hms_to_seconds(s0)
    if hms is not None:
        return int(hms)

    m = re.match(r"^\s*(\d+(?:[\.,]\d+)?)\s*min(?:ute|utes)?\s*$", s0)
    if m:
        minutes = float(m.group(1).replace(",", "."))
        return int(round(minutes * 60.0))

    iv = safe_int(s0)
    if iv is not None:
        return int(iv)

    fv = safe_float(s0)
    if fv is not None:
        return int(round(fv * 60.0))

    return None


def normalize_game_duration(df: pd.DataFrame) -> pd.DataFrame:
    df["game_duration_seconds"] = (
        df.get("game_duration", "").apply(parse_duration_to_seconds).astype("Int64")
    )
    return df


def normalize_possession_time(df: pd.DataFrame) -> pd.DataFrame:
    df["possession_time_seconds"] = (
        df.get("possession_time", "").apply(parse_time_to_seconds).astype("Int64")
    )
    return df
