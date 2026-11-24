
import os
import time
from datetime import datetime
from pathlib import Path

import requests
import api
from dotenv import load_dotenv


# Project configuration
BASE_URL = (
    "https://api.sportradar.com/"
    "tennis/trial/v3/en/"
)

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("SPORTRADAR_API_KEY")

if not API_KEY:
    raise RuntimeError("SPORTRADAR_API_KEY is missing from .env")

HEADERS = {
    "x-api-key": API_KEY,
    "accept": "application/json",
}


def fetch_feed(feed_name):
    """Fetch one SportRadar API feed."""
    url = BASE_URL + feed_name

    for attempt in range(3):
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=60,
        )

        if response.status_code == 429 and attempt < 2:
            time.sleep(5 * (attempt + 1))
            continue

        response.raise_for_status()
        return response.json()

    raise RuntimeError(f"Unable to fetch {feed_name}")


def sync_categories(cursor, competitions):
    """Insert or update competition categories."""
    categories = {}

    for item in competitions:
        category = item.get("category") or {}
        category_id = category.get("id")

        if category_id:
            categories[category_id] = category.get("name") or "Unknown"

    query = """
        INSERT INTO categories (category_id, category_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        category_name = VALUES(category_name)
    """

    cursor.executemany(query, list(categories.items()))
    print("Categories synced:", len(categories))


def sync_competitions(cursor, competitions):
    """Insert or update competitions."""
    query = """
        INSERT INTO competitions
        (competition_id, competition_name, parent_id,
         type, gender, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        competition_name = VALUES(competition_name),
        parent_id = VALUES(parent_id),
        type = VALUES(type),
        gender = VALUES(gender),
        category_id = VALUES(category_id)
    """

    rows = []

    for item in competitions:
        category = item.get("category") or {}

        rows.append((
            item["id"],
            (item.get("name") or "Unknown")[:100],
            item.get("parent_id"),
            (item.get("type") or "unknown")[:20],
            (item.get("gender") or "unknown")[:10],
            category.get("id"),
        ))

    cursor.executemany(query, rows)
    print("Competitions synced:", len(rows))


def sync_complexes(cursor, complexes):
    """Insert or update complexes and their venues."""
    complex_query = """
        INSERT INTO complexes (complex_id, complex_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        complex_name = VALUES(complex_name)
    """

    venue_query = """
        INSERT INTO venues
        (venue_id, venue_name, city_name, country_name,
         country_code, timezone, complex_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        venue_name = VALUES(venue_name),
        city_name = VALUES(city_name),
        country_name = VALUES(country_name),
        country_code = VALUES(country_code),
        timezone = VALUES(timezone),
        complex_id = VALUES(complex_id)
    """

    complex_rows = []
    venue_rows = []

    for item in complexes:
        complex_id = item["id"]

        complex_rows.append((
            complex_id,
            (item.get("name") or "Unknown")[:100],
        ))

        for venue in item.get("venues", []):
            if not venue.get("id"):
                continue

            venue_rows.append((
                venue["id"],
                (venue.get("name") or "Unknown")[:100],
                (venue.get("city_name") or "Unknown")[:100],
                (venue.get("country_name") or "Unknown")[:100],
                (venue.get("country_code") or "UNK")[:3],
                (venue.get("timezone") or "Unknown")[:100],
                complex_id,
            ))

    cursor.executemany(complex_query, complex_rows)

    if venue_rows:
        cursor.executemany(venue_query, venue_rows)

    print("Complexes synced:", len(complex_rows))
    print("Venues synced:", len(venue_rows))


def sync_rankings(cursor, ranking_data):
    """Insert or update competitors and doubles rankings."""
    generated_at = ranking_data.get("generated_at")

    if generated_at:
        ranking_date = datetime.fromisoformat(
            generated_at.replace("Z", "+00:00")
        ).date()
    else:
        ranking_date = datetime.now().date()

    competitor_query = """
        INSERT INTO competitors
        (competitor_id, name, country, country_code, abbreviation)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        country = VALUES(country),
        country_code = VALUES(country_code),
        abbreviation = VALUES(abbreviation)
    """

    ranking_insert = """
        INSERT INTO competitor_rankings
        (competitor_id, competitor_name, country, country_code,
         `rank`, movement, points, competitions_played, ranking_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    ranking_update = """
        UPDATE competitor_rankings
        SET competitor_name = %s,
            country = %s,
            country_code = %s,
            `rank` = %s,
            movement = %s,
            points = %s,
            competitions_played = %s
        WHERE rank_id = %s
    """

    competitor_count = 0
    ranking_count = 0

    for group in ranking_data.get("rankings", []):
        for entry in group.get("competitor_rankings", []):
            competitor = entry.get("competitor") or {}
            competitor_id = competitor.get("id")

            if not competitor_id:
                continue

            name = (competitor.get("name") or "Unknown")[:150]
            country = competitor.get("country")
            country_code = competitor.get("country_code")
            abbreviation = competitor.get("abbreviation")

            cursor.execute(
                competitor_query,
                (
                    competitor_id,
                    name,
                    country,
                    country_code,
                    abbreviation,
                ),
            )
            competitor_count += 1

            rank = int(entry.get("rank") or 0)
            movement = int(entry.get("movement") or 0)
            points = int(entry.get("points") or 0)
            played = int(entry.get("competitions_played") or 0)

            values = (
                name,
                country,
                country_code,
                rank,
                movement,
                points,
                played,
            )

            cursor.execute(
                """
                SELECT rank_id
                FROM competitor_rankings
                WHERE competitor_id = %s
                  AND ranking_date = %s
                ORDER BY rank_id
                LIMIT 1
                """,
                (competitor_id, ranking_date),
            )

            existing = cursor.fetchone()

            if existing:
                cursor.execute(
                    ranking_update,
                    values + (existing["rank_id"],),
                )
            else:
                cursor.execute(
                    ranking_insert,
                    (
                        competitor_id,
                        name,
                        country,
                        country_code,
                        rank,
                        movement,
                        points,
                        played,
                        ranking_date,
                    ),
                )

            ranking_count += 1

    print("Competitors synced:", competitor_count)
    print("Ranking records synced:", ranking_count)
    print("Ranking date:", ranking_date)


def main():
    print("Fetching SportRadar feeds...")

    competitions_data = fetch_feed("competitions.json")
    complexes_data = fetch_feed("complexes.json")
    rankings_data = fetch_feed(
        "double_competitors_rankings.json"
    )

    competitions = competitions_data.get("competitions", [])
    complexes = complexes_data.get("complexes", [])

    print("Competitions received:", len(competitions))
    print("Complexes received:", len(complexes))

    conn = api.get_connection()

    try:
        conn.begin()

        cursor = conn.cursor()

        sync_categories(cursor, competitions)
        sync_competitions(cursor, competitions)
        sync_complexes(cursor, complexes)
        sync_rankings(cursor, rankings_data)

        conn.commit()

        print("\nSUCCESS: SportRadar data imported into MySQL.")

    except Exception:
        conn.rollback()
        print("\nERROR: Import failed. Database changes rolled back.")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
