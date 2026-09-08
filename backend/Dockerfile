FROM python:3.13-slim

WORKDIR /app

# Installation des dépendances système nécessaires pour psycopg2 / PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copie et installation des paquets Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code source du dossier backend
COPY . .

EXPOSE 8000

# Commande par défaut pour lancer l'API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]