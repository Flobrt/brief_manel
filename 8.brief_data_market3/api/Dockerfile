# 1️⃣ Image de base
FROM python:3.11-slim

# 2️⃣ Variables d'environnement pour éviter les messages inutiles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Crée le dossier de l'app
WORKDIR /app

# 4️⃣ Copie le fichier requirements
COPY requirements.txt .

# 5️⃣ Installe les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6️⃣ Copie le reste du code
COPY . .

# 7️⃣ Expose le port Flask
EXPOSE 5000

# 8️⃣ Commande par défaut pour lancer l'API
CMD ["python", "app.py"]
