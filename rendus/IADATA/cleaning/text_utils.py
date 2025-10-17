from __future__ import annotations

import re
import unicodedata
from typing import Iterable


_LEET_MAP = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t"
})


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def to_lower_ascii(s: str) -> str:
    s = strip_accents(s)
    return normalize_space(s).lower()


def replace_ordinal_suffixes(s: str) -> str:
    # Supprime 1st/2nd/3rd/4th/etc.
    return re.sub(r"(\d+)(st|nd|rd|th)", r"\1", s, flags=re.I)


def wordnum_to_int(s: str) -> int | None:
    if not s:
        return None
    base = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    }
    s_norm = to_lower_ascii(s)
    return base.get(s_norm)


def safe_int(s: str) -> int | None:
    if s is None or s == "":
        return None
    s2 = str(s).strip()
    s2 = re.sub(r"[^\d\-]+", "", s2)
    if s2 in {"", "-", "—"}:
        return None
    try:
        return int(s2)
    except ValueError:
        try:
            return int(float(s2.replace(",", ".")))
        except Exception:
            return None


def safe_float(s: str) -> float | None:
    if s is None or s == "":
        return None
    s2 = str(s).strip().replace(",", ".")
    s2 = re.sub(r"[^0-9\.\-]", "", s2)
    if s2 in {"", ".", "-", "—"}:
        return None
    try:
        return float(s2)
    except Exception:
        return None


def de_leet(s: str) -> str:
    if not s:
        return s
    return s.translate(_LEET_MAP)


def pick_first_nonempty(values: Iterable[str | None]) -> str | None:
    for v in values:
        if v is not None and str(v).strip() != "":
            return str(v).strip()
    return None
