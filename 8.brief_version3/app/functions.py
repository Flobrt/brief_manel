import psycopg2
import pandas as pd

# Connexion à PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="postgres-1",  # nom du service Docker
        user="airflow",
        password="airflow",
        dbname="airflow",
        port=5432
    )

# Insérer utilisateur
def insert_game(game, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (urlgame, game) VALUES (%s, %s)", (url, game))
    conn.commit()
    conn.close()


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


def get_merged_data():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        g.game AS Game,
        p_current.dateprice AS CurrentPriceDate,
        p_current.price AS CurrentPrice,
        p_min.min_price AS LowestPriceEver
    FROM games g
    LEFT JOIN (
        -- prix actuel = dernière date
        SELECT p1.game_id, p1.price, p1.dateprice
        FROM prices p1
        INNER JOIN (
            SELECT game_id, MAX(dateprice) AS max_date
            FROM prices
            GROUP BY game_id
        ) p2 ON p1.game_id = p2.game_id AND p1.dateprice = p2.max_date
    ) AS p_current ON g.id = p_current.game_id
    LEFT JOIN (
        -- prix le plus bas jamais obtenu
        SELECT game_id, MIN(price) AS min_price
        FROM prices
        GROUP BY game_id
    ) AS p_min ON g.id = p_min.game_id
    ORDER BY g.id;
    """

    cursor.execute(query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()

    df = pd.DataFrame(result, columns=columns)
    return df
