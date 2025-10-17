from __future__ import annotations

from datetime import datetime
import pandas as pd

from cleaning.text_utils import replace_ordinal_suffixes, normalize_space


# Formats testés explicitement (US, EU, ISO, pointés, noms de mois)
_DATE_TRY_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%d-%m-%Y",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%d %b %y",
    "%d %b %Y",
    "%b %d %Y",
    "%b %d %y",
    "%d %B %Y",
    "%B %d %Y",
]


def _preclean_date_str(s: str | None) -> str | None:
    if not s:
        return None
    s = replace_ordinal_suffixes(str(s))
    s = normalize_space(s)
    s = s.replace("Sept", "Sep")
    return s


def _try_parse_strptime(s: str) -> pd.Timestamp | None:
    for fmt in _DATE_TRY_FORMATS:
        try:
            return pd.to_datetime(datetime.strptime(s, fmt), utc=True)
        except Exception:
            continue
    return None


def _try_parse(s: str | None) -> pd.Timestamp | None:
    if not s:
        return None
    s2 = _preclean_date_str(s)
    if not s2:
        return None

    # 1) essais explicites
    ts = _try_parse_strptime(s2)
    if ts is not None:
        return ts

    # 2) repli pandas (sans dayfirst=True pour éviter warnings)
    try:
        return pd.to_datetime(s2, utc=True, errors="coerce")
    except Exception:
        return None


def normalize_game_date(df: pd.DataFrame) -> pd.DataFrame:
    parsed = df.get("game_date", "").apply(_try_parse)
    df["game_date_ts"] = parsed
    df["game_date_date"] = df["game_date_ts"].dt.date.astype("string")
    return df


def normalize_created_at(df: pd.DataFrame) -> pd.DataFrame:
    df["created_at_ts"] = pd.to_datetime(
        df.get("created_at", None), utc=True, errors="coerce"
    )
    return df
