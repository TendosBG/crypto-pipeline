# Crypto Analytics Pipeline

Projet de Data Engineering pour apprendre les concepts fondamentaux du domaine via un pipeline crypto end-to-end.

## Objectif

Construire un pipeline complet qui ingère des données de marché crypto depuis CoinGecko, les transforme en couches Bronze/Silver/Gold, et les expose dans un dashboard Streamlit — orchestré par Prefect.

## Stack technique

| Couche | Outil | Rôle |
|---|---|---|
| Ingestion | Python + requests | Appels API CoinGecko |
| Stockage | Parquet + DuckDB | Fichiers bruts + requêtes SQL |
| Transformation | dbt | Modèles Silver et Gold |
| Orchestration | Prefect | Scheduling + monitoring |
| Visualisation | Streamlit | Dashboard métriques |
| Conteneurisation | Docker (phase finale) | Déploiement |

## Architecture des données

```
CoinGecko API (gratuit, sans clé)
        ↓
  Ingestion Python
        ↓
  Bronze — données brutes (Parquet)
        ↓
  Silver — nettoyage + typage (dbt)
        ↓
  Gold — métriques agrégées (dbt)
        ↓
  Dashboard Streamlit
```

### Métriques Gold prévues
- Volatilité 7j / 30j par coin
- Corrélation BTC vs altcoins
- Évolution de la market cap dominance
- Détection de pumps (variation > seuil en 24h)

## Structure du projet

```
DE/
├── CLAUDE.md
├── ingestion/          # Scripts Python d'appel API
├── data/
│   ├── bronze/         # Données brutes (Parquet)
│   ├── silver/         # Données nettoyées
│   └── gold/           # Métriques finales
├── dbt/                # Modèles de transformation SQL
├── orchestration/      # Flows Prefect
├── dashboard/          # App Streamlit
├── docker/             # Dockerfiles (phase finale)
└── requirements.txt
```

## Phases du projet

- [ ] **Phase 1** — Ingestion : appeler CoinGecko, sauvegarder en Parquet
- [ ] **Phase 2** — Stockage : structurer Bronze/Silver/Gold avec DuckDB
- [ ] **Phase 3** — Transformation : modèles dbt (Silver + Gold)
- [ ] **Phase 4** — Orchestration : Prefect flows + scheduling
- [ ] **Phase 5** — Visualisation : dashboard Streamlit
- [ ] **Phase 6** — Conteneurisation Docker (bonus portfolio)

## Profil développeur

- Langage principal : Python (niveau avancé)
- SQL : expérience significative
- Data Engineering : débutant, apprend au fur et à mesure
- Approche : une techno nouvelle par phase, le reste en Python/SQL connu
