import requests as re
import mysql.connector
import pandas as pd
import json

def resquet_name(product_name: str, langue: str = '*', page_size: int = 10) -> pd.DataFrame:
    '''
        Function to request product data from Open Food Facts based on product name and language.
        Parameters:
            - product_name (str): The name of the product to search for.
            - langue (str): The language code for the product data. Default is '*', which means all languages.
            - page_size (int): The number of products to return per page. Default is 10.
        Returns:
            - pd.DataFrame: A DataFrame containing the product data with columns for product name, language, brands, nutrition grades, and ecoscore grade.
    '''
    
    if langue == '*':
        product_name = product_name.lower()
        url = f"https://search.openfoodfacts.org/search?q={product_name}&page_size={page_size}&page=1&fields=product_name%2Clang%2Cbrands%2Cnutrition_grades%2Cecoscore_grade"
        df = pd.DataFrame(re.get(url).json().get('hits'))
    
    else: 
        product_name = product_name.lower()
        url = f"https://search.openfoodfacts.org/search?langs={langue}&q={product_name}&page_size={page_size}&page=1&fields=product_name%2Clang%2Cbrands%2Cnutrition_grades%2Cecoscore_grade"
        df = pd.DataFrame(re.get(url).json().get('hits'))
        
    return df

# Connexion à MariaDB
def get_connection():
    return mysql.connector.connect(
        host="mariadb",   # nom du service Docker
        user="user",
        password="password",
        database="produitsdb"
    )

# Insérer utilisateur
def insert_user(nom, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO utilisateurs (nom, email) VALUES (%s, %s)", (nom, email))
    conn.commit()
    conn.close()

# Récupérer ID utilisateur
def get_user_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nom, id FROM utilisateurs")
    result = cursor.fetchall()
    conn.close()
    return result

# Insérer produits
def insert_products(df, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO produits (utilisateur_id, brands, lang, nutrition_grades, ecoscore_grade, product_name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            json.dumps(row.get("brands", None)) if isinstance(row.get("brands", None), list) else row.get("brands", None),
            row.get("lang", None),
            row.get("nutrition_grades", None),
            row.get("ecoscore_grade", None),
            row.get("product_name", None)
        ))
    conn.commit()
    conn.close()