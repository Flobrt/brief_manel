FROM python:3.11-slim

# Installer dépendances système pour MariaDB
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["python", "main.py"]
# CMD ["tail", "-f", "/dev/null"]