from __future__ import annotations
import pandas as pd

YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
MAYBE = {"maybe", "perhaps", "?"}


def _to_bool_or_none(val: str | None) -> bool | None:
    if val is None:
        return None
    v = str(val).strip().lower()
    if v in YES:
        return True
    if v in NO:
        return False
    if v in {"", "-", "—", "null", "n/a"}:
        return None
    return None


def normalize_yes_no_maybe_flags(df: pd.DataFrame) -> pd.DataFrame:
    # Colonnes réellement booléennes
    for col in ["is_substitute", "duplicate_flag"]:
        if col in df.columns:
            df[col + "_normalized"] = df[col].apply(_to_bool_or_none)

    # 'referee' : présence booléenne + nom séparé
    if "referee" in df.columns:
        low = df["referee"].astype(str).str.strip().str.lower()
        df["referee_present"] = low.isin(YES | NO).map({True: True, False: None})
        df["referee_name"] = df["referee"].where(~low.isin(YES | NO), None)

    return df
