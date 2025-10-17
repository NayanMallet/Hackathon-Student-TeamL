from __future__ import annotations

import pandas as pd
from cleaning.text_utils import to_lower_ascii, normalize_space


def normalize_colors_and_winner(df: pd.DataFrame) -> pd.DataFrame:
    norm = {
        "r": "red", "red": "red", "🔴": "red", "rouge": "red",
        "b": "blue", "blue": "blue", "bleu": "blue",
    }

    def colormap(x: str | None) -> str | None:
        if not x:
            return None
        v = to_lower_ascii(x)
        return norm.get(v)

    for c in ["winner", "team_color"]:
        if c in df.columns:
            df[c + "_norm"] = df[c].apply(colormap)

    return df


def normalize_roles(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "attack": "attack", "attck": "attack", "attacking": "attack", "att": "attack",
        "def": "defense", "defence": "defense", "defense": "defense",
        "defender": "defense", "attackk": "attack",
        "attack ": "attack", "defence ": "defense", "def ": "defense",
        "🔴": None,
    }

    def norm_role(x: str | None) -> str | None:
        if not x:
            return None
        v = to_lower_ascii(x)
        return mapping.get(v, v)

    df["player_role_norm"] = df.get("player_role", "").apply(norm_role)
    return df


def normalize_ball_type(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "classic": "classic",
        "white hard": "white-hard",
        "orange soft": "orange-soft",
        "mini ball": "mini-ball",
        "trainer ball": "trainer-ball",
        "3-ball set": "set-3-balls",
        "old worn": "old-worn",
        "": None,
        None: None
    }

    def norm_ball(x: str | None) -> str | None:
        if x is None:
            return None
        v = x.strip().lower()
        return mapping.get(v, v)

    df["ball_type_norm"] = df.get("ball_type", "").apply(norm_ball)
    return df


def normalize_table_condition(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "new": "new",
        "worn": "worn",
        "scratched": "scratched",
        "missing screw": "missing-screw",
        "out of alignment": "out-of-alignment",
        "sticky handles": "sticky-handles",
        "needs cleaning": "needs-cleaning",
        "broken leg": "broken-leg",
        "beer stains": "beer stains",  # laissé tel quel si non mappé
    }

    def norm_cond(x: str | None) -> str | None:
        if not x:
            return None
        v = x.strip().lower()
        return mapping.get(v, v)

    df["table_condition_norm"] = df.get("table_condition", "").apply(norm_cond)
    return df


def normalize_music_fields(df: pd.DataFrame) -> pd.DataFrame:
    def parse_music(s: str | None):
        if not s:
            return (None, None)
        v = normalize_space(str(s))
        vlow = v.lower()
        if vlow in {"", "none", "silence"}:
            return ("silence", None)
        if vlow.startswith("spotify:"):
            return ("spotify", v.split(":", 1)[1].strip())
        if vlow.startswith("radio "):
            return ("radio", v)
        if "playlist" in vlow:
            return ("playlist", v)
        return ("other", v)

    src, lbl = zip(*df.get("music_playing", "").apply(parse_music))
    df["music_source"] = list(src)
    df["music_label"] = list(lbl)
    return df


def normalize_recorded_by(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "discord bot": "discord-bot",
        "discord-bot": "discord-bot",
        "player phone": "player-phone",
        "player-phone": "player-phone",
        "auto_recorder": "auto-recorder",
        "auto-recorder": "auto-recorder",
        "gopro": "gopro",
        "camera": "camera",
        "phone": "phone",
        "admin": "admin",
        "referee": "referee",
        "player": "player-phone",
    }

    def norm(x: str | None) -> str | None:
        if not x:
            return None
        key = to_lower_ascii(str(x)).replace("_", "-")
        return mapping.get(key, key)

    df["recorded_by_norm"] = df.get("recorded_by", "").apply(norm)
    return df
