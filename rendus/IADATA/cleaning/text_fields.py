from __future__ import annotations
import re
import pandas as pd


def normalize_notes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie 'notes' et ajoute 'notes_normalized'.
    """
    def norm(x: str | None) -> str | None:
        if not x:
            return None
        s = re.sub(r"\s+", " ", str(x)).strip()
        s = s.replace("—", "-")
        return s if s else None

    df["notes_normalized"] = df.get("notes", "").apply(norm)
    return df
