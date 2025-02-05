
# Utiliser une image Python comme base
FROM python:3.9
LABEL authors="jadedomas-vasserot"
# Définir le répertoire de travail
WORKDIR /home/app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application dans le conteneur
COPY . .

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Commande pour lancer l'application Streamlit
CMD streamlit run Dashboard.py --server.port=$PORT --server.address="0.0.0.0"
