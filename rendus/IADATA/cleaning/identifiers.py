from __future__ import annotations
import re
import pandas as pd


def normalize_game_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise game_id en 'G' + 6 chiffres.
    - Supprime suffixes '_1', '-a', etc.
    - Met en majuscules.
    - Remplit à gauche si < 6 chiffres.
    Ajoute:
      - game_id_norm
      - game_id_was_fixed (bool)
    """
    def fix(gid: str | None) -> tuple[str | None, bool]:
        if not gid:
            return None, False
        s = str(gid).strip()
        s = s.split()[0]
        s = re.sub(r"[_\-].*$", "", s)
        s = s.upper()
        # Extraire la partie numérique, avec ou sans 'G' initial
        m = re.match(r"^G\s*(\d+)$", s) or re.match(r"^(\d+)$", s.replace("G", "", 1))
        if not m:
            return s, (s != gid)  # valeur atypique
        num = m.group(1).zfill(6)[:6]
        norm = f"G{num}"
        return norm, (norm != gid)

    fixed = df.get("game_id", "").apply(fix)
    df["game_id_norm"] = fixed.apply(lambda x: x[0])
    df["game_id_was_fixed"] = fixed.apply(lambda x: x[1])
    return df
