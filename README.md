# 🎾 Tennis Sports Analytics

A database-powered Tennis Sports Analytics platform built using the SportRadar Tennis API, Python, MySQL, FastAPI and Streamlit.

The application collects tennis reference data and doubles competitor rankings from SportRadar, stores the structured data in MySQL, exposes it through REST APIs, and presents analytics through an interactive dashboard.

## Project Overview

The platform integrates three SportRadar API feeds:

- Competitions API
- Complexes API
- Doubles Competitor Rankings API

The extracted JSON data is transformed and stored in a relational MySQL database.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Source | SportRadar Tennis API |
| Database | MySQL 8.0 |
| Backend | FastAPI |
| Dashboard | Streamlit |
| Data Processing | Requests, Pandas |
| Visualization | Plotly |
| Database Connectivity | PyMySQL |
| Environment Configuration | python-dotenv |

## Architecture

SportRadar API → Python Data Synchronization → MySQL Database → FastAPI → Streamlit Dashboard

## Database Overview

The database is named `tennis_analytics` and contains six tables:

| Table | Records |
|---|---:|
| categories | 18 |
| competitions | 6,743 |
| complexes | 789 |
| venues | 4,200 |
| competitors | 1,000 |
| competitor_rankings | 1,000 |
| **Total** | **13,750** |

These counts represent the verified database snapshot on November 24, 2026. Future API synchronization may change them.

## Project Structure

```text

Tennis_Sports_Analytics/

│

├── api.py

├── dashboard.py

├── requirements.txt

├── .env.example

├── .gitignore

├── Dockerfile

├── .dockerignore

│

├── scripts/

│   ├── sync_sportradar.py

│   └── cleanup_sample_data.py

│

├── sql/

│   ├── schema.sql

│   ├── analytics_queries.sql

│   └── load_sample_data.sql

│

├── docs/

│   ├── PROJECT_DOCUMENTATION.md

│   └── DATABASE_SCHEMA.md

│

├── assets/

├── data/

└── backup_analytics_<timestamp>/

```

## Features

### SportRadar Data Integration

- Fetches competition information.
- Extracts complexes and associated venues.
- Retrieves ATP and WTA doubles competitor rankings.
- Uses API key authentication through an environment variable.
- Handles HTTP errors and API rate limits.
- Synchronizes records into MySQL.

### Database

- Six relational tables.
- Primary and foreign key relationships.
- Indexed columns for frequently used queries.
- Structured competitor ranking information.

### FastAPI Backend

Base URL: `http://127.0.0.1:8000`

Swagger documentation: `http://127.0.0.1:8000/docs`

Available endpoints:

- `/`
- `/health`
- `/competitors`
- `/rankings`
- `/categories`
- `/competitions`
- `/venues`
- `/analytics/{query_id}`

### Streamlit Dashboard

Dashboard URL: `http://127.0.0.1:8501`

The dashboard provides:

- API and MySQL connection status with summary metrics.
- Top 10 player rankings and ranking-points visualization.
- Player ranking search by player name or country.
- Competitor directory with search by name or country.
- Individual competitor profile with country, abbreviation, rank, points, movement, competitions played and ranking date when available.
- Competition Explorer with filters for competition type, category, gender and hierarchy level (top-level or sub-competition).
- Venue directory.
- Interactive execution of 22 SQL business analytics queries with tabular results and charts.
- Refresh Data control to clear cached API responses and reload dashboard data.

## Installation and Setup

### 1. Clone the Repository

```bash

git clone https://github.com/jitain1/Tennis_Sports_Analytics.git

cd Tennis_Sports_Analytics

```

### 2. Create a Virtual Environment

```bash

py -m venv .venv

```

Activate it on Windows PowerShell:

```powershell

.\.venv\Scripts\Activate.ps1

```

### 3. Install Dependencies

```bash

py -m pip install -r requirements.txt

```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Configure your own values:

```env

SPORTRADAR_API_KEY=your_api_key

DB_HOST=localhost

DB_USER=root

DB_PASSWORD=your_mysql_password

DB_NAME=tennis_analytics

```

Never commit `.env` or expose your API key or database password.

### 5. Create the Database

Create the MySQL database:

```sql

CREATE DATABASE tennis_analytics;

```

Execute the schema file using your MySQL client or a database management tool:

```sql

SOURCE path/to/sql/schema.sql;

```

### 6. Synchronize SportRadar Data

Run from the project root:

```powershell

$env:PYTHONPATH = (Get-Location).Path

py scripts/sync_sportradar.py

```

The synchronization script fetches the configured SportRadar feeds and inserts or updates database records.

### 7. Start FastAPI

Open a terminal:

```powershell

py -m uvicorn api:app --host 127.0.0.1 --port 8000

```

### 8. Start Streamlit

Open a second terminal:

```powershell

py -m streamlit run dashboard.py --server.address 127.0.0.1 --server.port 8501

```

Open `http://127.0.0.1:8501` in your browser. If port 8501 is already in use, start Streamlit on another port (for example, `--server.port 8502`) and open the matching local URL.

## SQL Analytics

The `sql/analytics_queries.sql` file contains 22 business analytics queries. The dashboard exposes them through `/analytics/{query_id}`:

1. Top 10 Competitors
2. Complete Player Rankings
3. Country-wise Competitor Count
4. Country-wise Average Ranking Points
5. Country-wise Total Ranking Points
6. Best Ranking by Country
7. Ranking Movement Analysis
8. Ranking Distribution
9. Competitor Country Details
10. Competitions by Category
11. Competitions by Gender
12. Competitions by Event Type
13. Complete Competition Details
14. Venues by Country
15. Venues by City
16. Venues by Complex
17. Complexes Without Venues
18. Rankings by Ranking Date
19. Top 3 Competitors Per Country
20. Competitors Without Ranking Records
21. Ranking Records Without Competitor Master Record
22. Overall Database KPI Summary

The analytics cover competition hierarchy and type, venue geography and complex relationships, player rankings and movement, country-level ranking points, data-quality checks and overall database KPIs.

## Data Cleanup

The `scripts/cleanup_sample_data.py` script verifies IDs against the SportRadar feeds and removes records not present in the verified API snapshot.

A database backup should always be taken before running cleanup operations.

**Important:** `sql/load_sample_data.sql` is intended for sample-data setup and should not be executed when maintaining the API-only dataset.

## Documentation

- `docs/PROJECT_DOCUMENTATION.md` — implementation workflow, architecture, API integration, dashboard features, SQL analytics and verified data findings.
- `docs/DATABASE_SCHEMA.md` — database tables, keys, indexes and entity relationships.

Dashboard screenshots can be stored in `assets/` and linked here after capture.

## Error Handling and Reliability

- API authentication and HTTP response validation.
- Request timeouts and retry handling for rate limits.
- Database transaction handling.
- Rollback on synchronization failures.
- Environment-based credential management.
- Database backup before cleanup.

## Future Improvements

- Automated scheduled data synchronization.
- Historical ranking snapshots.
- Match-level and tournament-level analytics.
- Advanced player comparison.
- Deployment with Docker and a cloud platform.
- Automated testing and CI/CD.

## Repository

GitHub: https://github.com/jitain1/Tennis_Sports_Analytics

## Project Status

Core API integration, MySQL data synchronization, FastAPI backend, 22 SQL analytics queries and the Streamlit dashboard (including competition filters and competitor profiles) have been implemented and tested locally.

Database snapshot verified on November 24, 2026.
