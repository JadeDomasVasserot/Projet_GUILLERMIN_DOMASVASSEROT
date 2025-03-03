import streamlit as st
import requests
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps
import numpy as np
import io
from datetime import datetime
import os
import pandas as pd  # Manquait dans ton code

# Dossier de stockage des images
image_folder = "./images/draw"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

st.title("Dessinez un objet et prédisez-le")
st.header("Paramètres du Canvas")

drawing_mode = st.radio("Mode de dessin :", ("freedraw", "line", "rect", "circle", "transform"))
stroke_width = st.slider("Épaisseur du trait :", 1, 25, 3)
stroke_color = st.color_picker("Couleur du trait :", "#000000")
realtime_update = st.checkbox("Mise à jour en temps réel ?", True)

# Création du canvas pour dessiner
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Couleur de remplissage par défaut
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    update_streamlit=realtime_update,
    height=400,
    width=600,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Vérifier si l'utilisateur a dessiné quelque chose
if canvas_result.image_data is not None:
    st.subheader("Aperçu de l'image générée :")
    img = Image.fromarray((canvas_result.image_data).astype("uint8"))

    # Convertir en niveau de gris ou en RGB si nécessaire
    img = img.convert("RGB")  # Ou "L" pour grayscale si besoin

    st.image(img)

    # Sauvegarde en mémoire (buffer)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Bouton pour envoyer l'image à l'API
    if st.button("Prédire"):
        # Générer un nom unique pour l'image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_folder}/image_{timestamp}.png"

        # Sauvegarde locale
        img.save(image_filename)
        st.info(f"L'image a été sauvegardée sous `{image_filename}`.")

        # Envoi au backend
        url = "https://api-cloud-g4-0bc391d2f0c3.herokuapp.com/models/predict"
        files = {"file": buffer}  # Assure-toi que l'API attend "file" et pas "data"

        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Lève une erreur en cas de problème HTTP

            if response.status_code == 200:
                result = response.json()
                st.success(f"Résultat : {result}")

                # Enregistrer la prédiction dans un fichier CSV
                csv_file = "predictions.csv"
                data = {"timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "image_path": [image_filename]}

                try:
                    df = pd.read_csv(csv_file)
                    df_new = pd.DataFrame(data)
                    df = pd.concat([df, df_new], ignore_index=True)
                except FileNotFoundError:
                    df = pd.DataFrame(data)

                df.to_csv(csv_file, index=False)
                st.info(f"Prédiction enregistrée dans `{csv_file}`.")

            else:
                st.error(f"Erreur de l'API : {response.status_code}")
                st.error(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")
