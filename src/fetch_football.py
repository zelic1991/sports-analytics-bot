# src/fetch_football.py
import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus dem Projekt-Root
project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / ".env")

# API-Konfiguration
API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = os.getenv("API_FOOTBALL_URL", "").rstrip("/")

if not API_KEY or not BASE_URL:
    raise RuntimeError("Fehlende API_FOOTBALL_KEY oder API_FOOTBALL_URL in .env")

HEADERS = {"x-apisports-key": API_KEY}


def fetch_fixtures(date_from: str, date_to: str) -> dict:
    """
    Holt alle Fixtures zwischen date_from und date_to.
    Datum im Format 'YYYY-MM-DD'.
    """
    url = f"{BASE_URL}/fixtures"
    params = {"date_from": date_from, "date_to": date_to}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_injuries(season: int) -> dict:
    """
    Holt die Injury-Reports für die angegebene Saison.
    """
    url = f"{BASE_URL}/injuries"
    params = {"season": season}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_lineups(fixture_id: int) -> dict:
    """
    Holt die Aufstellungen (Lineups) für ein spezifisches Fixture.
    """
    url = f"{BASE_URL}/fixtures/lineups"
    params = {"fixture": fixture_id}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def save_raw(data: dict, name: str):
    """
    Speichert die Rohdaten als JSON unter data/raw mit Datums-Suffix.
    """
    today = datetime.now().strftime("%Y%m%d")
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{name}_{today}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {name} to {path}")


if __name__ == "__main__":
    # Daten der letzten 2 Tage
    today = datetime.today().date()
    two_days_ago = today - timedelta(days=2)

    fixtures = fetch_fixtures(str(two_days_ago), str(today))
    save_raw(fixtures, "fixtures")

    current_season = today.year
    injuries = fetch_injuries(current_season)
    save_raw(injuries, "injuries")

    # Lineups für das erste gefundene Spiel
    resp = fixtures.get("response")
    if resp:
        first_id = resp[0]["fixture"]["id"]
        lineups = fetch_lineups(first_id)
        save_raw(lineups, f"lineups_{first_id}")
