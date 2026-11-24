\# Project Documentation

\## Game Analytics: Unlocking Tennis Data with SportRadar API



\*\*Project:\*\* Tennis Sports Analytics  

\*\*Database:\*\* MySQL 8.0  

\*\*Backend:\*\* FastAPI  

\*\*Frontend:\*\* Streamlit  

\*\*Data Provider:\*\* SportRadar Tennis API  

\*\*Language:\*\* Python



\---



\## 1. Project Objective



The objective is to develop a database-powered Tennis Sports Analytics platform that collects tennis reference data through SportRadar APIs, transforms JSON responses into relational database records, and provides analytical insights through SQL queries and an interactive dashboard.



The application focuses on competition structures, venue information, complexes, competitors and doubles competitor rankings.



\## 2. System Architecture



The project follows a layered architecture:



1\. \*\*Data Source:\*\* SportRadar Tennis API.

2\. \*\*Extraction:\*\* Python Requests library retrieves API responses.

3\. \*\*Transformation:\*\* JSON fields are mapped into relational records.

4\. \*\*Storage:\*\* MySQL stores structured data.

5\. \*\*Backend:\*\* FastAPI exposes database information through REST endpoints.

6\. \*\*Presentation:\*\* Streamlit displays metrics, tables, charts and analytics.



\### Data Flow



SportRadar API → Python Extraction Scripts → JSON Processing → MySQL → FastAPI → Streamlit Dashboard



\## 3. SportRadar API Integration



The application integrates the following feeds:



\### 3.1 Competitions API



Endpoint:

`competitions.json`



Purpose:

\- Retrieve tennis competitions.

\- Extract competition identifiers and names.

\- Capture competition type and gender.

\- Extract category information.

\- Maintain parent-child competition relationships.



\### 3.2 Complexes API



Endpoint:

`complexes.json`



Purpose:

\- Retrieve sports complexes.

\- Extract venue information.

\- Store venue names and identifiers.

\- Capture city, country, country code and timezone.

\- Connect venues with their complexes.



\### 3.3 Doubles Competitor Rankings API



Endpoint:

`double\_competitors\_rankings.json`



Purpose:

\- Retrieve ATP and WTA doubles rankings.

\- Extract competitor names and identifiers.

\- Store ranking positions and points.

\- Capture ranking movement and competitions played.

\- Maintain ranking dates.



\### Authentication



SportRadar API authentication is performed using the `x-api-key` HTTP header.



The API key is stored in `.env` and loaded through python-dotenv. It is not stored in source code.



\### Error Handling



The integration handles:

\- HTTP request failures.

\- Authentication errors.

\- API rate limits.

\- Request timeouts.

\- Database transaction failures.



\## 4. Data Synchronization



Implementation file: `scripts/sync\_sportradar.py`



Workflow:



1\. Load environment configuration.

2\. Establish API authentication.

3\. Fetch all three API feeds.

4\. Validate and process the returned JSON.

5\. Synchronize categories.

6\. Synchronize competitions.

7\. Synchronize complexes and venues.

8\. Synchronize competitors and rankings.

9\. Commit successful database transactions.

10\. Roll back changes if an error occurs.



The synchronization uses database upsert operations where appropriate to avoid unnecessary duplicate reference records.



\## 5. Database Implementation



Database name: `tennis\_analytics`



Six relational tables are implemented:



\- categories

\- competitions

\- complexes

\- venues

\- competitors

\- competitor\_rankings



Primary keys identify records, while foreign keys maintain relationships between related entities.



Detailed table structures and relationships are documented in `DATABASE\_SCHEMA.md`.



\## 6. FastAPI Backend



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

| `/analytics/{query\_id}` | SQL analytics |



The backend connects to MySQL using PyMySQL and exposes database information as JSON responses.



\## 7. Streamlit Dashboard



Implementation file: `dashboard.py`



Dashboard URL:

`http://127.0.0.1:8501`



Dashboard capabilities:



\- Database and API connection status.

\- Competitor summary metrics.

\- Ranking summary metrics.

\- Competition and venue statistics.

\- Top player rankings.

\- Ranking points charts.

\- Competitor information.

\- Competition browsing.

\- Venue browsing.

\- SQL analytics.



The dashboard retrieves information through the FastAPI backend.



\## 8. SQL Analytics



Implementation file: `sql/analytics\_queries.sql`



Analytical areas include:



\### Competition Analysis

\- List competitions with category.

\- Count competitions by category.

\- Filter competitions by category.

\- Identify doubles competitions.

\- Analyze parent and sub-competitions.

\- Group competition types.



\### Venue Analysis

\- List venues and associated complexes.

\- Count venues by complex.

\- Analyze venues by country.

\- Group venues by country.

\- Identify complexes containing multiple venues.

\- Review venue timezones.



\### Ranking Analysis

\- List competitors with rank and points.

\- Retrieve top-ranked competitors.

\- Analyze ranking movement.

\- Calculate points by country.

\- Count ranked competitors by country.

\- Identify highest ranking points.



\## 9. Data Verification



Verified database snapshot on November 24, 2026:



| Table | Records |

|---|---:|

| Categories | 18 |

| Competitions | 6,743 |

| Complexes | 789 |

| Venues | 4,200 |

| Competitors | 1,000 |

| Competitor Rankings | 1,000 |

| \*\*Total\*\* | \*\*13,750\*\* |



The sample records were removed after verifying the corresponding identifiers against SportRadar API feeds.



These counts represent the verified snapshot and may change after future synchronization.



\## 10. Backup and Recovery



Before cleanup, a JSON backup of all six database tables was created.



Backup location:



`backup\_analytics\_20261123\_234828/before\_sportradar\_20261124\_120033.json`



The cleanup script uses database transactions and rolls back changes if an error occurs.



\## 11. Challenges and Solutions



\### API Connectivity

\*\*Challenge:\*\* API connectivity was initially unavailable on the previous network.



\*\*Solution:\*\* API access was verified using a working mobile hotspot connection.



\### API Authentication

\*\*Challenge:\*\* Securely configuring API authentication.



\*\*Solution:\*\* The API key was stored in `.env` and supplied through the required HTTP header.



\### Database Integration

\*\*Challenge:\*\* Mapping nested JSON records into relational tables.



\*\*Solution:\*\* Separate synchronization functions were implemented for categories, competitions, complexes, venues, competitors and rankings.



\### Python Module Resolution

\*\*Challenge:\*\* The synchronization script initially could not locate the root-level `api.py` module.



\*\*Solution:\*\* The project root was added to `PYTHONPATH` when executing the script.



\### Sample Data Removal

\*\*Challenge:\*\* The initial database contained sample records.



\*\*Solution:\*\* A cleanup script verified the SportRadar identifiers and removed non-API records while preserving the database schema.



\## 12. Security Considerations



\- Store API credentials in `.env`.

\- Never commit `.env` to GitHub.

\- Use `.env.example` for configuration guidance.

\- Keep database credentials outside source code.

\- Create backups before destructive database operations.

\- Use transaction rollback for failed synchronization.



\## 13. Future Enhancements



\- Scheduled API synchronization.

\- Historical ranking tracking.

\- Match and tournament data integration.

\- Advanced competitor comparison.

\- Automated testing.

\- Docker-based deployment.

\- Cloud hosting and CI/CD pipeline.



\## 14. Conclusion



The project successfully integrates SportRadar tennis reference and ranking feeds with a relational MySQL database, a FastAPI backend and an interactive Streamlit dashboard.



The implementation demonstrates API integration, JSON processing, database design, SQL analytics, backend development and dashboard visualization.

