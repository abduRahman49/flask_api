import os
import requests
from dotenv import load_dotenv

# chargement de toutes les variables d'environnement
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_first_five_quotes():
    url = "https://zenquotes.io/api/quotes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # liste de cinquante citations
        print("Données reçues", data)
        try:
            return data[:5]
        except IndexError:
            return None
    return None


def get_quote_of_the_day():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return {"q": data[0].get("q"), "a": data[0].get("a")}
        except IndexError:
            return None
    return None


def get_google_search_result(cle):
    url = "https://www.google.com/search"
    params = {"q": cle}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Résultats recherche", response.text)
        return response.text
    return None

def prompt_gemini_api_2_5_flash():
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
        {
            "parts": [
            {
                "text": "Explain how AI works in a few words"
            }
            ]
        }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Réponse retournée par l'API Gemini 2.5 flash ", response.text)

prompt_gemini_api_2_5_flash()