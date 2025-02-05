import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import os
import io

# Créer un dossier pour stocker les images si nécessaire
image_folder = "./images/upload"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

st.title("Application de prédiction d'images")

# Upload d'image
uploaded_file = st.file_uploader("Téléchargez une image", type=["png", "jpg", "jpeg"])

# Affichage des résultats
if uploaded_file is not None:
    st.subheader("Aperçu de l'image :")
    
    # Charger l'image avec PIL
    img = Image.open(uploaded_file)
    st.image(img, caption="Image téléversée")

    # Bouton pour simuler l'envoi au backend
    if st.button("Prédire"):
        # Générer un nom unique pour l'image (timestamp)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_folder}/image_{timestamp}.png"
        
        # Sauvegarder l'image localement dans le dossier /images
        img.save(image_filename)
        st.info(f"L'image a été sauvegardée sous `{image_filename}`.")
        
        # Convertir l'image en bytes pour l'envoi au backend
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Envoi au backend (remplacez l'URL par celle de votre backend)
        response = requests.post(
            "http://localhost:8000/predict",
            files={"file": buffer}
        )
        
        if response.status_code == 200:
            result = response.json()
            label = result.get("label", "N/A")
            
            # Afficher le résultat à l'utilisateur
            st.success(f"Résultat : {label}")

            # Enregistrer les résultats dans un fichier CSV
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "timestamp": [timestamp],
                "label": [label],
                "image_path": [image_filename]
            }

            # Charger ou créer le fichier CSV
            csv_file = "predictions.csv"
            try:
                df = pd.read_csv(csv_file)
                df_new = pd.DataFrame(data)
                df = pd.concat([df, df_new], ignore_index=True)
            except FileNotFoundError:
                df = pd.DataFrame(data)
            
            # Sauvegarder le DataFrame dans le fichier CSV
            df.to_csv(csv_file, index=False)
            st.info(f"Prédiction enregistrée dans `{csv_file}`.")
        else:
            st.error("Erreur lors de l'envoi au backend.")
