import requests
from bs4 import BeautifulSoup
from pipeline.pouet import *
from datetime import datetime



def extract():
    df = get_games()

    prix_list = []

    for url in df["urlgame"]:
        try:
            headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/131.0.0.0 Safari/537.36"
                    }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                div_total = soup.find("div", class_="total")

                if div_total:
                    texte_prix = div_total.get_text(strip=True)
                    propre = texte_prix.replace("€", "").replace(",", ".").strip()
                    try:
                        prix = float(propre)
                    except ValueError:
                        prix = None
                else:
                    prix = None
            else:
                prix = None

        except Exception as e:
            print(f"Erreur avec {url} : {e}")
            prix = None

        prix_list.append(prix)

    # Ajouter la colonne au DataFrame
    df["prix"] = prix_list
    df["logdate"] = datetime.now()
    
    # Garder les colonnes prix, date et id 
    df_final = df[["id", "prix", "logdate"]]
    
    load_to_db(df_final)