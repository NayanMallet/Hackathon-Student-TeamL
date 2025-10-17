from __future__ import annotations

import pandas as pd

from cleaning import read_csv_safely
from cleaning.identifiers import normalize_game_id
from cleaning.dates import normalize_game_date, normalize_created_at
from cleaning.scores import split_merged_scores, reconcile_scores_and_winner
from cleaning.durations import normalize_game_duration, normalize_possession_time
from cleaning.booleans import normalize_yes_no_maybe_flags
from cleaning import (
    normalize_integers,
    normalize_ping_ms,
    normalize_attendance_count,
    normalize_rating,
    normalize_player_age,
)
from cleaning.categories import (
    normalize_colors_and_winner,
    normalize_roles,
    normalize_ball_type,
    normalize_table_condition,
    normalize_music_fields,
    normalize_recorded_by,
)
from cleaning.locations import normalize_location
from cleaning import normalize_people_names
from cleaning.seasons import normalize_season
from cleaning.text_fields import normalize_notes
from cleaning.quality import flag_suspicions, final_column_order


INPUT_PATH = "./babyfoot_dataset.csv"
OUTPUT_PATH = "./babyfoot_dataset_out.csv"
CSV_SEP = ","


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # Identifiants
    df = normalize_game_id(df)

    # Dates & timestamps
    df = normalize_game_date(df)
    df = normalize_created_at(df)

    # Scores fusionnés -> éclatement
    df = split_merged_scores(df)

    # Durées & temps (entiers)
    df = normalize_game_duration(df)
    df = normalize_possession_time(df)

    # Booléens stricts
    df = normalize_yes_no_maybe_flags(df)

    # Numériques
    df = normalize_integers(df)
    df = normalize_ping_ms(df)
    df = normalize_attendance_count(df)
    df = normalize_rating(df)
    df = normalize_player_age(df)

    # Catégories & champs textuels
    df = normalize_colors_and_winner(df)
    df = normalize_roles(df)
    df = normalize_ball_type(df)
    df = normalize_table_condition(df)
    df = normalize_music_fields(df)
    df = normalize_recorded_by(df)

    # Lieux
    df = normalize_location(df)

    # Noms (ne conserver que player_name + player_canonical_norm)
    df = normalize_people_names(df)

    # Saison depuis la date (vérité métier)
    df = normalize_season(df)

    # Cohérence scores ↔ gagnant
    df = reconcile_scores_and_winner(df)

    # Notes
    df = normalize_notes(df)

    # Qualité & ordre des colonnes
    df = flag_suspicions(df)
    df = final_column_order(df)

    # Supprimer colonnes nom joueur superflues si présentes
    drop_cols = [
        "player_name_norm",
        "player_canonical_name",
        "player_canonical_form",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    return df


def main() -> None:
    df = read_csv_safely(INPUT_PATH, sep=CSV_SEP)
    cleaned = run_pipeline(df)
    cleaned.to_csv(OUTPUT_PATH, index=False)

    print(f"Entrée : {INPUT_PATH}")
    print(f"Sortie : {OUTPUT_PATH}")
    print(f"Lignes: {len(cleaned)}, Colonnes: {len(cleaned.columns)}")


if __name__ == "__main__":
    main()
