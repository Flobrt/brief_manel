import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="mariadb",   # nom du service Docker
        user="root",
        password="rootpassword",
        database="pricedb"
    )

# Récupérer ID utilisateur
def get_games():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM games")
    result = cursor.fetchall()  # récupère toutes les lignes
    columns = [desc[0] for desc in cursor.description]  # récupère les noms des colonnes
    
    conn.close()
    
    # Créer un DataFrame
    df = pd.DataFrame(result, columns=columns)
    return df

# Charger les jeux de la db
def load_to_db(df):
    conn = get_connection()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO prices (game_id, price, dateprice)
            VALUES (%s, %s, %s)
        """, (
            row['id'], 
            row['prix'], 
            row['logdate']
        ))
    conn.commit()
    conn.close()
