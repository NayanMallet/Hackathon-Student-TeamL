from __future__ import annotations
import pandas as pd


def read_csv_safely(path: str, sep: str = ",", nrows: int | None = None) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=sep,
        dtype=str,
        keep_default_na=False
    )
    if nrows is not None:
        df = df.head(nrows)

    # Interpréter <unset> comme NA (insensible à la casse)
    df = df.replace(to_replace=r"(?i)^\s*<unset>\s*$", value=pd.NA, regex=True)

    # Flag ligne incomplète si >40% des colonnes sont NA
    na_ratio = df.replace("", pd.NA).isna().mean(axis=1)
    df["row_incomplete"] = (na_ratio > 0.4)

    return df
