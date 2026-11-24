# Project Documentation

## Game Analytics: Unlocking Tennis Data with SportRadar API

**Project:** Tennis Sports Analytics

**Database:** MySQL 8.0

**Backend:** FastAPI

**Frontend:** Streamlit

**Data Provider:** SportRadar Tennis API

**Language:** Python

---

## 1. Project Objective

The objective is to develop a database-powered Tennis Sports Analytics platform that collects tennis reference data through SportRadar APIs, transforms JSON responses into relational database records, and provides analytical insights through SQL queries and an interactive dashboard.

The application focuses on competition structures, venue information, complexes, competitors and doubles competitor rankings.

## 2. System Architecture

The project follows a layered architecture:

1. **Data Source:** SportRadar Tennis API.
2. **Extraction:** Python Requests library retrieves API responses.
3. **Transformation:** JSON fields are mapped into relational records.
4. **Storage:** MySQL stores structured data.
5. **Backend:** FastAPI exposes database information through REST endpoints.
6. **Presentation:** Streamlit displays metrics, tables, charts and analytics.

### Data Flow

SportRadar API → Python Extraction Scripts → JSON Processing → MySQL → FastAPI → Streamlit Dashboard

## 3. SportRadar API Integration

The application integrates the following feeds:

### 3.1 Competitions API

Endpoint:

`competitions.json`

Purpose:

- Retrieve tennis competitions.
- Extract competition identifiers and names.
- Capture competition type and gender.
- Extract category information.
- Maintain parent-child competition relationships.

### 3.2 Complexes API

Endpoint:

`complexes.json`

Purpose:

- Retrieve sports complexes.
- Extract venue information.
- Store venue names and identifiers.
- Capture city, country, country code and timezone.
- Connect venues with their complexes.

### 3.3 Doubles Competitor Rankings API

Endpoint:

`double_competitors_rankings.json`

Purpose:

- Retrieve ATP and WTA doubles rankings.
- Extract competitor names and identifiers.
- Store ranking positions and points.
- Capture ranking movement and competitions played.
- Maintain ranking dates.

### Authentication

SportRadar API authentication is performed using the `x-api-key` HTTP header.

The API key is stored in `.env` and loaded through python-dotenv. It is not stored in source code.

### Error Handling

The integration handles:

- HTTP request failures.
- Authentication errors.
- API rate limits.
- Request timeouts.
- Database transaction failures.

## 4. Data Synchronization

Implementation file: `scripts/sync_sportradar.py`

Workflow:

1. Load environment configuration.
2. Establish API authentication.
3. Fetch all three API feeds.
4. Validate and process the returned JSON.
5. Synchronize categories.
6. Synchronize competitions.
7. Synchronize complexes and venues.
8. Synchronize competitors and rankings.
9. Commit successful database transactions.
10. Roll back changes if an error occurs.

The synchronization uses database upsert operations where appropriate to avoid unnecessary duplicate reference records.

## 5. Database Implementation

Database name: `tennis_analytics`

Six relational tables are implemented:

- categories
- competitions
- complexes
- venues
- competitors
- competitor_rankings

Primary keys identify records, while foreign keys maintain relationships between related entities.

Detailed table structures and relationships are documented in `DATABASE_SCHEMA.md`.

## 6. FastAPI Backend

Implementation file: `api.py`

Base URL:

`http://127.0.0.1:8000`

Swagger UI:

`http://127.0.0.1:8000/docs`

Implemented endpoints:

| Endpoint | Purpose |
|---|---|
| `/` | API root |
| `/health` | Health check |
| `/competitors` | Competitor information |
| `/rankings` | Competitor rankings |
| `/categories` | Competition categories |
| `/competitions` | Competition information |
| `/venues` | Venue information |
| `/analytics/{query_id}` | SQL analytics |

The backend connects to MySQL using PyMySQL and exposes database information as JSON responses.

## 7. Streamlit Dashboard

Implementation file: `dashboard.py`

Dashboard URL: `http://127.0.0.1:8501`

Dashboard capabilities:

- Database and API connection status.
- Summary metrics for competitors, rankings, competitions and venues.
- Top 10 player rankings and ranking-points chart.
- Player ranking search by player name or country.
- Competitor directory with search by name or country.
- Individual competitor profile showing competitor ID, country, country code and abbreviation.
- Ranking details for the selected competitor when a ranking record is available: current rank, points, movement, competitions played and ranking date.
- Competition Explorer with filters for event type, category, gender and competition hierarchy level.
- The hierarchy level is derived from `parent_id`: a missing parent indicates a top-level competition; a populated parent indicates a sub-competition.
- Venue directory.
- SQL Analytics page with 22 selectable business queries, result counts, tables and numeric chart options.
- Sidebar refresh control to clear cached API data and reload the dashboard.

The dashboard retrieves data through the FastAPI backend. If port 8501 is occupied, Streamlit can be started on another port such as 8502.

## 8. SQL Analytics

Implementation file: `sql/analytics_queries.sql`

The SQL file contains 22 queries, all of which were executed successfully during local validation. The dashboard maps the query list to the `/analytics/{query_id}` endpoint.

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

The queries cover:

### Competition Analysis

- Competition lists and counts by category.
- Competition filters by category, gender and event type.
- Doubles competitions and parent/sub-competition hierarchy.

### Venue Analysis

- Venues with their complexes.
- Venue counts by complex, country and city.
- Complexes with multiple venues or without venues.
- Venue timezone analysis.

### Ranking and Data Quality Analysis

- Complete and top-ranked competitor rankings.
- Ranking movement and distribution.
- Country-wise competitor counts and ranking points.
- Best-ranked competitors by country and top competitors per country.
- Competitors without ranking records and ranking records without a competitor master record.
- Overall database KPI summary.

## 9. Data Verification

Verified database snapshot on November 24, 2026:

| Table | Records |
|---|---:|
| Categories | 18 |
| Competitions | 6,743 |
| Complexes | 789 |
| Venues | 4,200 |
| Competitors | 1,000 |
| Competitor Rankings | 1,000 |
| **Total** | **13,750** |

The sample records were removed after verifying the corresponding identifiers against SportRadar API feeds.

These counts represent the verified snapshot and may change after future synchronization. The snapshot contains 6,743 competitions across 18 categories, 4,200 venues associated with 789 complexes, and 1,000 competitor master records matched to 1,000 ranking records. The ranking feed included 500 ATP and 500 WTA doubles competitor entries at the time of extraction.

### Analytical Findings and Use Cases

The available data supports analysis of competition distribution by category, gender and event type; separation of top-level competitions from child competitions; venue distribution by country, city and complex; ranking-position and points comparisons; ranking movement; country-level ranking-point summaries; and data-quality checks for unmatched competitor and ranking records. Exact leaders and country totals should be taken from the SQL query results rather than inferred from record counts alone.

## 10. Backup and Recovery

Before cleanup, a JSON backup of all six database tables was created.

Backup location:

`backup_analytics_20261123_234828/before_sportradar_20261124_120033.json`

The cleanup script uses database transactions and rolls back changes if an error occurs.

## 11. Challenges and Solutions

### API Connectivity

**Challenge:** API connectivity was initially unavailable on the previous network.

**Solution:** API access was verified using a working mobile hotspot connection.

### API Authentication

**Challenge:** Securely configuring API authentication.

**Solution:** The API key was stored in `.env` and supplied through the required HTTP header.

### Database Integration

**Challenge:** Mapping nested JSON records into relational tables.

**Solution:** Separate synchronization functions were implemented for categories, competitions, complexes, venues, competitors and rankings.

### Python Module Resolution

**Challenge:** The synchronization script initially could not locate the root-level `api.py` module.

**Solution:** The project root was added to `PYTHONPATH` when executing the script.

### Sample Data Removal

**Challenge:** The initial database contained sample records.

**Solution:** A cleanup script verified the SportRadar identifiers and removed non-API records while preserving the database schema.

## 12. Security Considerations

- Store API credentials in `.env`.
- Never commit `.env` to GitHub.
- Use `.env.example` for configuration guidance.
- Keep database credentials outside source code.
- Create backups before destructive database operations.
- Use transaction rollback for failed synchronization.

## 13. Future Enhancements

- Scheduled API synchronization.
- Historical ranking tracking.
- Match and tournament data integration.
- Advanced competitor comparison.
- Automated testing.
- Docker-based deployment.
- Cloud hosting and CI/CD pipeline.

## 14. Dashboard Evidence and Screenshots

For the final submission, capture and place the following screenshots in the repository's `assets/` folder:

- `dashboard_overview.png` — connection status, KPI cards and top 10 ranking chart.
- `dashboard_competitions.png` — competition filters and filtered results.
- `dashboard_competitor_profile.png` — selected competitor profile and ranking details.
- `dashboard_sql_analytics.png` — a representative SQL analytics result and chart.
- `api_swagger.png` — FastAPI Swagger UI showing the implemented endpoints.

Only add screenshots that have actually been captured from the running application.

## 15. Conclusion

The project successfully integrates SportRadar tennis reference and ranking feeds with a relational MySQL database, a FastAPI backend and an interactive Streamlit dashboard.

The implementation demonstrates API integration, JSON processing, relational database design, 22 SQL analytics queries, REST backend development and interactive dashboard visualization. The verified local snapshot contains 13,750 records across the six required tables.
