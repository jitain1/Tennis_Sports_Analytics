
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

        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if connection:
            connection.close()


@app.get("/")
def home():
    return {
        "message": "Tennis Sports Analytics API",
        "status": "running",
        "database": "PostgreSQL"
    }


@app.get("/health")
def health():
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return {
            "api": "running",
            "database": "connected"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if connection:
            connection.close()


@app.get("/competitors")
def get_competitors(
    limit: int = Query(default=1000, ge=1, le=10000)
):
    return fetch_data(
        "SELECT * FROM competitors LIMIT %s",
        (limit,)
    )


@app.get("/rankings")
def get_rankings(
    limit: int = Query(default=1000, ge=1, le=10000)
):
    return fetch_data(
        'SELECT * FROM competitor_rankings ORDER BY "rank" ASC LIMIT %s',
        (limit,)
    )


@app.get("/categories")
def get_categories():
    return fetch_data(
        "SELECT * FROM categories"
    )


@app.get("/competitions")
def get_competitions():
    return fetch_data(
        "SELECT * FROM competitions"
    )


@app.get("/venues")
def get_venues():
    return fetch_data(
        "SELECT * FROM venues"
    )


@app.get("/analytics/{query_id}")
def run_analytics(query_id: int):

    sql_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sql",
        "analytics_queries.sql"
    )

    try:
        with open(sql_path, encoding="utf-8-sig") as f:
            sql = f.read()

        sql = "\n".join(
            line for line in sql.splitlines()
            if not line.strip().startswith("--")
        )

        queries = [
            q.strip()
            for q in sql.split(";")
            if q.strip()
            and q.strip().upper() != "USE TENNIS_ANALYTICS"
        ]

        if query_id < 1 or query_id > len(queries):
            raise HTTPException(
                status_code=404,
                detail="Invalid query ID"
            )

        rows = fetch_data(
            queries[query_id - 1]
        )

        return {
            "query_id": query_id,
            "total_records": len(rows),
            "data": rows
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
