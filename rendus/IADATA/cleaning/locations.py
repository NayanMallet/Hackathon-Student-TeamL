from __future__ import annotations
import re
import pandas as pd


def normalize_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise quelques variantes récurrentes :
      - 'Ynov tls', 'Ynov Tls' → 'Ynov Toulouse'
    """
    mapping = {
        "ynov toulouse": "Ynov Toulouse",
        "ynov tls": "Ynov Toulouse",
    }

    def norm(x: str | None) -> str | None:
        if not x:
            return None
        key = re.sub(r"\s+", " ", str(x)).strip().lower()
        return mapping.get(key, str(x).strip())

    df["location"] = df.get("location", "").apply(norm)
    return df
