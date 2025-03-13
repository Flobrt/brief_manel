from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Configuration de la connexion à la base de données MariaDB
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# Route pour tester la connexion à la base de données
@app.route('/data', methods=['GET'])
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
        cursor.execute("SELECT * FROM employees;")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "name": row[1],
                "position": row[2],
                "salary": row[3]    
            })
        
        # Fermeture de la connexion
        cursor.close()
        conn.close()

        # Retourner les données sous forme de JSON
        return jsonify(rows)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

