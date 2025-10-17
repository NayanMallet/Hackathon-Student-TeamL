from __future__ import annotations
import re
import pandas as pd
from cleaning.text_utils import normalize_space, de_leet


def _titlecase_name(s: str | None) -> str | None:
    if not s:
        return None
    s = normalize_space(s)
    parts = []
    for token in s.split(" "):
        if re.match(r"^[A-Za-z]\.$", token):
            parts.append(token.upper())
        else:
            parts.append(token.capitalize())
    return " ".join(parts)


def normalize_people_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Conserver seulement:
      - player_name (brut, colonne existante)
      - player_canonical_norm (lisible, propre) : priorité à player_canonical_name sinon player_name.
    """
    def norm_readable(s: str | None) -> str | None:
        if not s:
            return None
        return _titlecase_name(de_leet(s))

    df["player_canonical_norm"] = df.apply(
        lambda r: norm_readable(r.get("player_canonical_name")) or norm_readable(r.get("player_name")),
        axis=1,
    )

    # Arbitre lisible (on garde la colonne pour usage)
    if "referee_name" in df.columns:
        df["referee_name_norm"] = df["referee_name"].apply(norm_readable)
    else:
        df["referee_name_norm"] = df.get("referee", "").apply(norm_readable)

    return df
