from __future__ import annotations
import pandas as pd


def flag_suspicions(df: pd.DataFrame) -> pd.DataFrame:
    df["duration_suspicious"] = (
            df["game_duration_seconds"].isna()
            | (df["game_duration_seconds"] <= 0)
            | (df["game_duration_seconds"] > 3 * 3600)
    )

    df["scores_missing"] = df["final_score_red"].isna() | df["final_score_blue"].isna()

    declared = df.get("winner_norm")
    deduced = df.get("winner_from_scores")
    df["winner_conflict"] = declared.notna() & deduced.notna() & (declared != deduced)

    return df


def final_column_order(df: pd.DataFrame) -> pd.DataFrame:
    preferred_order = [
        # Clés & dates
        "game_id_norm", "game_id_was_fixed",
        "game_id", "game_date", "game_date_ts", "game_date_date",
        "created_at", "created_at_ts",
        # Scores & gagnant
        "final_score_red", "final_score_blue", "winner", "winner_norm",
        "winner_from_scores", "winner_final",
        # Durées
        "game_duration", "game_duration_seconds",
        # Joueur (garde brut + canonique lisible)
        "player_id",
        "player_name",
        "player_canonical_norm",
        # Stats/joueur
        "player_age", "player_age_years", "player_role", "player_role_norm",
        "player_goals", "player_own_goals", "player_assists", "player_saves",
        # Possession
        "possession_time", "possession_time_seconds",
        # Contexte
        "team_color", "team_color_norm",
        "location", "table_id",
        "table_condition", "table_condition_norm",
        "ball_type", "ball_type_norm",
        "music_playing", "music_source", "music_label",
        "referee", "referee_present", "referee_name", "referee_name_norm",
        "attendance_count", "attendance_count_value",
        # Saison
        "season", "season_from_date", "season_final",
        # Source
        "recorded_by", "recorded_by_norm",
        # Divers num/flags
        "rating_raw", "rating_1to5",
        "is_substitute", "is_substitute_normalized",
        "duplicate_flag", "duplicate_flag_normalized",
        "ping_ms", "ping_ms_value",
        "row_incomplete",
        # Qualité
        "duration_suspicious", "scores_missing", "winner_conflict",
        # Texte
        "mood", "player_comment", "misc", "notes",
    ]
    cols = [c for c in preferred_order if c in df.columns]
    tail = [c for c in df.columns if c not in cols]

    # S'assurer que notes_normalized soit tout à la fin
    if "notes_normalized" in df.columns and "notes_normalized" not in tail:
        tail.append("notes_normalized")

    return df[cols + tail]
