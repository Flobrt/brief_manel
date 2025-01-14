from flask import Flask, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# Configuration de la connexion à la base de données MariaDB
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# Route pour tester la connexion à la base de données
@app.route('/', methods=['GET'])
def get_data():
    try:
        # Connexion à MariaDB
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=3306
        )
        cursor = conn.cursor()
        
        # Exécution d'une requête SQL
        cursor.execute("SELECT * FROM clients;")
        rows = cursor.fetchall()
        
        # Fermeture de la connexion
        cursor.close()
        conn.close()

        # Retourner les données sous forme de JSON
        return render_template('index.html', rows=rows)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

