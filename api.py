
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

load_dotenv()

app = FastAPI(
    title="Tennis Sports Analytics API",
    version="1.0.0"
)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT", "5432")),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE", "defaultdb"),
        sslmode=os.getenv("PG_SSLMODE", "require"),
        connect_timeout=15
    )


def fetch_data(query, params=()):
    connection = None
    try:
        connection = get_connection()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()


@app.get("/")
def home():
    return {
        "message": "Tennis Sports Analytics API",
        "status": "running"
    }


@app.get("/health")
def health():
    try:
        fetch_data("SELECT 1 AS database_status")
        return {"api": "running", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/competitors")
def competitors():
    return fetch_data(
        """SELECT competitor_id, name, country,
        country_code, abbreviation
        FROM competitors ORDER BY name"""
    )


@app.get("/rankings")
def rankings(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    return fetch_data(
        """SELECT competitor_id, competitor_name, country,
        country_code, rank, movement, points,
        competitions_played, ranking_date
        FROM competitor_rankings
        ORDER BY rank ASC
        LIMIT %s OFFSET %s""",
        (limit, offset)
    )


@app.get("/categories")
def categories():
    return fetch_data(
        "SELECT * FROM categories ORDER BY category_name"
    )


@app.get("/competitions")
def competitions():
    return fetch_data(
        """SELECT c.*, cat.category_name
        FROM competitions c
        LEFT JOIN categories cat
        ON c.category_id = cat.category_id
        ORDER BY c.competition_name"""
    )


@app.get("/venues")
def venues():
    return fetch_data(
        """SELECT v.*, cx.complex_name
        FROM venues v
        LEFT JOIN complexes cx
        ON v.complex_id = cx.complex_id
        ORDER BY v.venue_name"""
    )


@app.get("/analytics/{query_id}")
def run_analytics(query_id: int):
    sql_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sql", "analytics_queries.sql"
    )

    try:
        with open(sql_path, encoding="utf-8") as f:
            sql = f.read()

        sql = "\n".join(
            line for line in sql.splitlines()
            if not line.strip().startswith("--")
        )

        queries = [q.strip() for q in sql.split(";") if q.strip()]

        if query_id < 1 or query_id > len(queries):
            raise HTTPException(
                status_code=404,
                detail="Invalid query ID"
            )

        rows = fetch_data(queries[query_id - 1])

        return {
            "query_id": query_id,
            "total_records": len(rows),
            "data": rows
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
