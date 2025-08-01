# src/main.py

from dotenv import load_dotenv
import os

def main():
    # .env laden
    load_dotenv()

    # Beispiel: API-Key auslesen
    api_football_key = os.getenv("API_FOOTBALL_KEY")
    print("Loaded API_FOOTBALL_KEY:", api_football_key)

    # TODO: Hier kommen später dein ETL-, Modell- und Agenten-Code hin

if __name__ == "__main__":
    main()
