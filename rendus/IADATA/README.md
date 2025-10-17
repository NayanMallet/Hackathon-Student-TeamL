# Hackathon - Ynov Toulouse 2025 : Babyfoot du futur - IA & Data

## Equipe

- IA & Data 1 : ANDRIEUX Rodolphe
- IA & Data 2 : PUJOL Ariel
- IA & Data 3 : BELSANY Salma



## 1. Nettoyage et préparation des données

On a pris le CSV “babyfoot” tel quel, avec ses formats hétérogènes, et on l’a transformé en un tableau propre, cohérent et exploitable.
Les dates sont interprétées malgré leurs variantes, les durées et temps de possession sont convertis en secondes entières,
les scores éventuels écrits “6 - 9” sont éclatés correctement et le vainqueur est recalculé à partir des scores pour signaler toute contradiction.
Les identifiants de match sont remis au format G######, les lieux épurés (“Ynov tls” devient “Ynov Toulouse”),
la source d’enregistrement est ramenée à un petit vocabulaire stable, et la saison est reconstruite depuis la date selon une logique simple
(année sportive d’août à juillet). Côté joueur, on conserve le nom saisi tel quel et on ajoute une version canonique lisible
(correction du leet uniquement pour les joueurs, jamais pour l’arbitre). Les champs ambigus comme yes/no/maybe deviennent de vrais booléens,
les notations hétérogènes sont ramenées sur 1–5, et les valeurs du type <unset>/null sont remplacées proprement en fin de chaîne.

Des indicateurs de qualité repèrent les durées aberrantes, les scores manquants et les désaccords sur le gagnant,
sans supprimer l’information d’origine. Le pipeline est modulaire (un fichier par thème), main.py lit babyfoot_dataset.csv et 
écrit babyfoot_dataset_out.csv, prêt à être intégré ou rejoué dès que de nouvelles données arrivent.

> 🧠 Le nettoyage final a produit `babyfoot_dataset_out.csv`, un fichier cohérent, typé, et exploitable.

---

## 2. Analyse exploratoire des données (EDA)

Réalisation d’une EDA complète avec le script `eda/run_eda.py`.  
L’analyse est faite **au niveau du match** (et non du joueur), avec détection automatique des matchs nuls (`draw` = scores égaux et winner vide).

### Analyses effectuées :
- Distribution des scores, durées et présences
- Corrélations entre métriques de performance (`duration ↔ total_score`, `ping ↔ rating`)
- KPI par dimension :
  - **Season** → répartition temporelle des matchs
  - **Location** → lieux les plus utilisés
  - **Ball type** → types de balles les plus performants
  - **Table condition** → impact de l’état du matériel sur le score
- Calcul des taux de victoire

Les fichiers de sortie se trouvent dans :
- `eda/outputs/` → CSV de KPIs, statistiques, et corrélations
- `eda/figures/` → graphiques automatiques (heatmaps, bar charts, histograms)

---

### Défi Data Science

### Top 10 des buteurs
- Basé sur la somme de `player_goals` par `player_canonical_norm`.
- Les joueurs les plus prolifiques sont souvent liés à la position `ATTACK`.

### Top 5 des meilleurs défenseurs
- Basé sur la moyenne et la somme de `player_saves` par joueur.
- Les joueurs `DEFENSE` affichent une régularité plus forte que les `ATTACK` (ce qui parait coherent)

### Influence du camp (red/blue)
- Analyse des taux de victoire sur l’ensemble des matchs :
  - **Blue wins ≈ 52%**
  - **Red wins ≈ 45%**
  - **Draws ≈ 3%**
- Aucune corrélation significative entre la couleur d’équipe et le score final : **l’avantage du camp n’est pas statistiquement prouvé.**

---

## 3. Participation à la base de données du projet

### Objectif
Concevoir un schéma de base cohérent avec la structure réelle des données, afin de permettre son utilisation 
par l’application des devs.

### Réalisations
- Schéma **Mermaid** complet (`schema/er_diagram.mmd`)
- Modélisation des relations entre entités :  
  `PLAYER`, `GAME`, `MATCH_PARTICIPATION`, `VENUE`, `FOOS_TABLE`, `REFEREE`, `MUSIC`, `RECORDED_BY`, `SEASON`
- Ajustements : déplacement du champ `referee_present` de `REFEREE` vers `GAME` pour coller à la structure logique du dataset.

On pourra par la suite y ajouter les tables et colonnes relative a l'Application (Logins, Elo, rank, etc.) qui ne sont pas present dans le dataset initial.
Par manque de temps. cette partie n'a pas pu etre traitée durant le hackathon.

