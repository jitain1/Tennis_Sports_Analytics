
import os
import requests
import api
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("SPORTRADAR_API_KEY")
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/"

if not API_KEY:
    raise RuntimeError("SportRadar API key missing from .env")

session = requests.Session()
session.headers.update({"x-api-key": API_KEY})


def fetch(feed):
    response = session.get(BASE_URL + feed + ".json", timeout=60)
    response.raise_for_status()
    return response.json()


def placeholders(values):
    return ",".join(["%s"] * len(values))


print("Fetching and verifying original SportRadar records...")

competitions_data = fetch("competitions")
complexes_data = fetch("complexes")
rankings_data = fetch("double_competitors_rankings")

competitions = competitions_data.get("competitions", [])
complexes = complexes_data.get("complexes", [])
ranking_groups = rankings_data.get("rankings", [])

competition_ids = {
    item["id"] for item in competitions if item.get("id")
}

category_ids = {
    item["category"]["id"]
    for item in competitions
    if isinstance(item.get("category"), dict)
    and item["category"].get("id")
}

complex_ids = {
    item["id"] for item in complexes if item.get("id")
}

venue_ids = {
    venue["id"]
    for item in complexes
    for venue in item.get("venues", [])
    if venue.get("id")
}

competitor_ids = set()

for group in ranking_groups:
    for item in group.get("competitor_rankings", []):
        competitor = item.get("competitor", {})
        if competitor.get("id"):
            competitor_ids.add(competitor["id"])

generated_at = rankings_data.get("generated_at")

if not generated_at:
    raise RuntimeError("Ranking feed date missing. Cleanup cancelled.")

ranking_date = datetime.fromisoformat(
    generated_at.replace("Z", "+00:00")
).date()

# Safety checks: abort if API data is incomplete.
if (
    len(competition_ids) < 6000
    or len(category_ids) < 10
    or len(complex_ids) < 500
    or len(venue_ids) < 3000
    or len(competitor_ids) < 500
):
    raise RuntimeError(
        "API record counts are unexpectedly low. No data was deleted."
    )

print("Verified API records:")
print("Categories:", len(category_ids))
print("Competitions:", len(competition_ids))
print("Complexes:", len(complex_ids))
print("Venues:", len(venue_ids))
print("Competitors:", len(competitor_ids))
print("Ranking date:", ranking_date)

connection = api.get_connection()
cursor = connection.cursor()

try:
    cursor.execute("START TRANSACTION")

    # Delete sample rankings first, preserving current API rankings.
    cursor.execute(
        """
        DELETE FROM competitor_rankings
        WHERE ranking_date IS NULL
           OR ranking_date <> %s
           OR competitor_id NOT IN (%s)
        """.replace("NOT IN (%s)", "NOT IN (" + placeholders(competitor_ids) + ")"),
        [ranking_date] + list(competitor_ids)
    )

    # Remove competitors not present in the API feed.
    cursor.execute(
        "DELETE FROM competitors WHERE competitor_id NOT IN ("
        + placeholders(competitor_ids) + ")",
        list(competitor_ids)
    )

    # Remove sample venues before complexes.
    cursor.execute(
        "DELETE FROM venues WHERE venue_id NOT IN ("
        + placeholders(venue_ids) + ")",
        list(venue_ids)
    )

    cursor.execute(
        "DELETE FROM complexes WHERE complex_id NOT IN ("
        + placeholders(complex_ids) + ")",
        list(complex_ids)
    )

    # Remove sample competitions before categories.
    cursor.execute(
        "DELETE FROM competitions WHERE competition_id NOT IN ("
        + placeholders(competition_ids) + ")",
        list(competition_ids)
    )

    cursor.execute(
        "DELETE FROM categories WHERE category_id NOT IN ("
        + placeholders(category_ids) + ")",
        list(category_ids)
    )

    connection.commit()
    print("\nSUCCESS: Sample data cleanup completed.")

except Exception:
    connection.rollback()
    print("\nERROR: Cleanup rolled back. Database changes were not committed.")
    raise

finally:
    cursor.close()
    connection.close()

# Verify final table counts.
connection = api.get_connection()
cursor = connection.cursor()

print("\nFINAL DATABASE COUNTS:")

for table in [
    "categories",
    "competitions",
    "complexes",
    "venues",
    "competitors",
    "competitor_rankings"
]:
    cursor.execute("SELECT COUNT(*) AS total FROM " + table)
    print(table + ":", cursor.fetchone()["total"])

cursor.close()
connection.close()
