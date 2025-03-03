import streamlit as st
from PIL import Image
import pandas as pd
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

# Vérifier si un fichier a été uploadé
if uploaded_file is not None:
    st.subheader("Aperçu de l'image :")
    
    # Charger l'image avec PIL
    img = Image.open(uploaded_file)
    st.image(img, caption="Image téléversée")

    # Bouton pour envoyer l'image au backend
    if st.button("Prédire"):
        # Générer un nom unique pour l'image (timestamp)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_folder}/image_{timestamp}.png"

        # Sauvegarder l'image localement
        img.save(image_filename)
        st.info(f"L'image a été sauvegardée sous `{image_filename}`.")

        # Convertir l'image en bytes pour l'envoi
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Envoi au backend
        url = "https://api-cloud-g4-0bc391d2f0c3.herokuapp.com/models/predict"
        files = {"file": buffer}  # Assure-toi que ton API attend "file" et pas "data"

        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Lève une erreur HTTP si problème

            if response.status_code == 200:
                result = response.json()
                st.success("Prédiction réussie !")
                st.json(result)  # Affichage correct du JSON

                # Enregistrer les résultats dans un fichier CSV
                csv_file = "predictions.csv"
                data = {
                    "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "image_path": [image_filename]
                }

                try:
                    df = pd.read_csv(csv_file)
                    df_new = pd.DataFrame(data)
                    df = pd.concat([df, df_new], ignore_index=True)
                except FileNotFoundError:
                    df = pd.DataFrame(data)

                df.to_csv(csv_file, index=False)
                st.info(f"Prédiction enregistrée dans `{csv_file}`.")

            else:
                st.error(f"Erreur HTTP {response.status_code}")
                st.error(response.text)  # Affiche l'erreur exacte

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")
