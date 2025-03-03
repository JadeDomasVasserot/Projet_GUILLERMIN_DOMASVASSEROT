import streamlit as st
from PIL import Image
import pandas as pd
import requests
from datetime import datetime
import os
import io

# Créer un dossier pour stocker les images capturées si nécessaire
image_folder = "./images/mimic"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

st.title("Capturez un objet et obtenez une prédiction")

# Capture d'image via la caméra
camera_image = st.camera_input("Prenez une photo de l'objet")
if camera_image:
    # Charger l'image capturée avec Pillow (PIL)
    cam_image = Image.open(camera_image)
    st.image(cam_image, caption="Image capturée")

    # Bouton pour envoyer au backend
    if st.button("Prédire"):
        # Générer un nom unique pour l'image (timestamp)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_folder}/image_{timestamp}.png"
        
        # Sauvegarder localement
        cam_image.save(image_filename)
        st.info(f"L'image a été sauvegardée sous `{image_filename}`.")

        # Convertir l'image en bytes pour l'envoi
        buffer = io.BytesIO()
        cam_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Envoi au backend (remplacez l'URL par votre endpoint)
        url = "https://api-cloud-g4-0bc391d2f0c3.herokuapp.com/models/predict"
        files = {"data": buffer}  # Vérifie que ton API attend "file" et pas "data"

        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Lève une erreur HTTP si problème

            if response.status_code == 200:
                result = response.json()

                # Sauvegarder les résultats dans un fichier CSV
                csv_file = "predictions.csv"
                data = {
                    "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "image_path": [image_filename]
                }
                                # Afficher le résultat
                st.success(f"Résultat : {result}")

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
                st.error(response.text)  # Voir le message d'erreur exact

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")
