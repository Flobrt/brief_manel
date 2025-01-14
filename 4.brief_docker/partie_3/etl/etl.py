import pandas as pd 
import os
import sqlalchemy

df_clients = pd.read_csv('csv/clients.csv')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_PORT = os.getenv('DB_PORT', '3306')

connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = sqlalchemy.create_engine(connection_string)
print("Création de la base de donnée : ")

try:
    df_clients.to_sql('clients', con=engine, if_exists='replace', index=False)
    print('Création de la table clients réussie')
except Exception as e:
    print('Erreur lors de la création de la table clients')
    print(e)
    
print("Fin de la création de la base de donnée")