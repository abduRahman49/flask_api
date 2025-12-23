import requests


def get_quote_of_the_day():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Données reçues", data)
        return data
    return None


def get_google_search_result(cle):
    url = "https://www.google.com/search"
    params = {"q": cle}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Résultats recherche", response.text)
        return response.text
    return None

get_google_search_result("animaux")