import requests
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
# from .functions import get_games, load_to_db

import psycopg2
import pandas as pd

def get_data():
    pg_hook = PostgresHook(postgres_conn_id='postgres_pg')
    conn = pg_hook.get_conn()
    # cursor = conn.cursor()
    df = pd.read_sql("SELECT * FROM games", conn)
    print(f"Nombre de jeux : {df.shape[0]}")
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


# Charger les jeux de la db
def load_to_db(df):
    conn = get_connection()
    cursor = conn.cursor()
    # Trasnformer la colonne logdate en datetime si ce n'est pas déjà le cas
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

# Définition des chemins des fichiers
INPUT_CSV = "/opt/airflow/dags/data/fact_resultats_epreuves.csv"

def init_pipline():
    df = get_games()
    print(f"Nombre de jeux : {df.shape[0]}")
    return df.to_json()


def request_api(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='init_pipline')  # récupère le JSON du task extract
    print(data)
    df = pd.read_json(StringIO(data))
    
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
    df["logdate"] = datetime.now().isoformat()
    
    # Garder les colonnes prix, date et id 
    df_final = df[["id", "prix", "logdate"]]
    return df_final.to_json()


def transform_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='request_api')  # récupère le JSON du task extract
    df = pd.read_json(data)
    return df.to_json()



# Fonction de chargement des données en base
def load_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='transform_data')
    df = pd.read_json(data)

    load_to_db(df)


# Définition du DAG
dag = DAG(
    'csv_etl_pipeline',
    description             = 'Pipeline ETL pour extraire et charger des données CSV dans une base de données PostgreSQL',
    schedule_interval='0 8,20 * * *',
    # schedule_interval       = '0 8 * 2,8 *',
    start_date              = datetime(2025, 10, 10),
    catchup                 = False,
    is_paused_upon_creation = False 
)


# check_year      = PythonOperator(task_id='check_even_year', python_callable=skip_if_not_even_year, provide_context=True, dag=dag)
get_data      = PythonOperator(task_id='get_data', python_callable=get_data, dag=dag)
init_pipline    = PythonOperator(task_id='init_pipline', python_callable=init_pipline, dag=dag)
request_api     = PythonOperator(task_id='request_api', python_callable=request_api, provide_context=True, dag=dag)
transform_data  = PythonOperator(task_id='transform_data', python_callable=transform_data, provide_context=True, dag=dag)
load_data       = PythonOperator(task_id='load_data', python_callable=load_data, provide_context=True, dag=dag)
soda_scan_1      = BashOperator(
                    task_id='soda_scan',
                    bash_command=(
                        "soda scan -d airflow_pg -c /opt/airflow/dags/soda/configuration.yml "
                        "/opt/airflow/dags/soda/checks.yml"
                    ),
                    dag=dag
                )
soda_scan_2       = BashOperator(
                    task_id='soda_scan_2',
                    bash_command=(
                        "soda scan -d airflow_pg -c /opt/airflow/dags/soda/configuration.yml "
                        "/opt/airflow/dags/soda/checks_2.yml"
                    ),
                    dag=dag
                )

# Définition de l'ordre des tâches
get_data >> init_pipline >> request_api  >> soda_scan_1 >> transform_data  >> load_data >> soda_scan_2

