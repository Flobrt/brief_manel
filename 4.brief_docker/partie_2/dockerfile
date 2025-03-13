# Utiliser une image Python de base
FROM python:3.9

# Installer curl
RUN apt update && apt install -y curl

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "app.py"]
