# Hackathon - Ynov Toulouse 2025 : Babyfoot du futur — FullStack

## Équipe

- Dev FullStack 1 : MALLET Nayan
- Dev FullStack 2 : REGUIA Dalyll
- Dev FullStack 3 : JEAN LOUIS Pablo

> Ce fichier résume la partie FullStack selon les attentes du sujet. Les requis détaillés sont dans SPECIFICATIONS.md.

---

## Vision produit

**BabyQueue** modernise l’usage des babyfoots au Souk via une file d’attente virtuelle, réservations rapides, suivi de parties et panneau d’admin. Cible : ~1000 étudiants. Objectif : expérience fluide, robuste, temps réel.

---

## Stack et choix techniques

- **Backend** : AdonisJS 6 (TypeScript), Lucid ORM, validation type zod, Auth sessions + rôles.
- **Frontend** : Inertia + Vue 3 + Vite, Tailwind.
- **DB** : SQLite en dev, Postgres prêt en prod.
- **API** : REST + docs Swagger (route /docs).
- **Tests** : Vitest sur services et routes critiques.
- **Pourquoi** : Adonis + Inertia accélère un monorepo cohérent, DX forte, auth/ORM intégrés, livraison rapide pour hackathon.

---

## Modèle de données (MVP)

- `users` : id, email, password_hash, display_name, role ∈ {user, admin}.
- `tables` : id, name, status ∈ {available, playing, maintenance}.
- `queues` : id, table_id, is_open, max_party_duration_min.
- `queue_entries` : id, queue_id, user_id, status ∈ {waiting, called, missed, done}, position.
- `matches` : id, table_id, started_at, ended_at, blue_score, red_score.
- `match_players` : match_id, user_id, team ∈ {blue, red}, role ∈ {attack, defense}.

Raisons : entités minimales pour réserver, attendre, jouer, tracer.

---

## Fonctionnalités livrées

### Public / Utilisateurs
- Page d’accueil claire et incitative.
- Inscription / Connexion, mot de passe hashé, remember optionnel.
- Tableau de bord “Étudiant” :
    - Rejoindre / quitter une file.
    - Notification visuelle “à vous de jouer” quand appelé.

### Admin
- Vue d’ensemble : liste des tables, statut, files ouvertes, parties en cours.
- CRUD **Tables** (create/read/update/delete). Requis CRUD rempli.
- Gestion utilisateurs : changer rôle, désactiver un compte.
- Forcer fin de partie, basculer une table en maintenance.

### API REST (extrait)
- `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`.
- `GET /tables`, `POST /tables`, `PATCH /tables/:id`, `DELETE /tables/:id`.
- `GET /queues/:tableId`, `POST /queues/:tableId/join`, `POST /queues/:tableId/leave`.
- `POST /matches/:tableId/start`, `POST /matches/:id/score`, `POST /matches/:id/end`.
- Codes HTTP conformes (200/201/400/401/403/404/409/422/500).
- **Docs** Swagger générées à l’adresse `/docs`.

### UX
- Design responsive.
- États chargement/erreur, toasts simples.
- Accessibilité de base : contraste et libellés.

---

## Rôles et autorisations

- **user** : rejoindre/quitter une file, voir les tables, lancer une partie appelée par le système.
- **admin** : CRUD tables, gérer files, forcer fin de match, éditer rôles.

---

## Règles métier clés

- Une **file** par table ouverte.
- Un **user** ne peut être *waiting* que dans une seule file à la fois.
- Appel des deux prochains joueurs. Délai de grâce configurable avant *missed* puis passage au suivant.
- Durée max d’une partie configurable par table ; dépassement déclenche un flag sur le dashboard.
- Score final verrouille la partie et libère la table.

---

## Intégrations et collaboration inter-équipes

- **Data** : export CSV des matchs et files (pour EDA “heures de pointe”, “tables les plus utilisées”). Hooks prêts pour webhooks temps réel. Alimente les sections “stats d’utilisation”.
- **IoT/Embarké** : webhooks `POST /iot/events` pour capteurs de but et état de table (playing/available). Schéma d’événement documenté.
- **Cloud/Infra** : envs `.env`, image Docker simple, healthcheck `/health`. Déploiement cible Render/Railway ou VPS. Requis “simplicité de déploiement” adressé côté app.

---

## Qualité, lisibilité, maintenabilité

- Modules par domaine : `app/controllers`, `app/services`, `app/validators`, `app/repositories`.
- Nommage explicite, schémas de validation partagés, commentaires uniquement où nécessaire.
- Tests :
    - Services de queue : insertion, re-order, missed → next.
    - Routes tables : 200/201/404/409.

Conforme aux attentes de lisibilité/bonnes pratiques.

---

## Sécurité

- Sessions serveur, cookies `HttpOnly`, `SameSite`, `Secure` en prod.
- Rate-limit sur auth et `/iot/events`.
- Validation stricte DTO, 401/403 systématiques.

---

## Documentation

- Swagger `/docs` (schémas, exemples, codes retour).
- README racine pour run local, variables d’env, scripts, et “how-to”.
- Ce `FULLSTACK.md` complète SPECIFICATIONS.md comme demandé.

---

## Scripts et démarrage

- `pnpm i`
- `pnpm dev` pour lancer Adonis + Vite.
- `node ace migration:run` pour provisionner la DB.
- `pnpm test` pour les tests unitaires.

---

## Difficultés et arbitrages

- Temps court : focus “file d’attente + CRUD tables + auth” plutôt que tournois.
- Choix Inertia pour éviter un backend/API séparés complexifiant la livraison.
- Gestion *missed* pragmatique : délai fixe + bouton “J’arrive” pour MVP.

---

## Backlog court terme

- WebSockets pour push “à vous de jouer”.
- Rôles par équipe et composition auto d’un match depuis deux entrées de queue.
- Page “Statistiques” globale (parties/jour, occupation par table).
- Intégration capteurs IoT en réel.
- Tests e2e Playwright.

---

## Couverture des requis du sujet

- Accueil attractive, Auth + rôles, Dashboard admin, API CRUD documentée, code propre. ✔️
- Bonus démarrés : responsive, tests unitaires, export data pour Data, hooks IoT. ✔️
