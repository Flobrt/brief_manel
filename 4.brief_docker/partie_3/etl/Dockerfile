# Utiliser l'image Python 3.9 comme base
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances et le script ETL dans le conteneur
COPY requirements.txt requirements.txt
COPY etl.py etl.py
COPY csv/ csv/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Ajouter un délai d'exécution par défaut (peut être modifié via docker-compose)
CMD ["sh", "-c", "sleep 30 && python /app/etl.py"]
