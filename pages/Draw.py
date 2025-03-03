import streamlit as st
import requests
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps
import numpy as np
import io
from datetime import datetime
import os


image_folder = "./images/draw"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    
st.title("Dessinez un objet et prédisez-le")
st.header("Paramètres du Canvas")

drawing_mode = st.radio(
    "Mode de dessin :", ("freedraw", "line", "rect", "circle", "transform")
)
stroke_width = st.slider("Épaisseur du trait :", 1, 25, 3)
stroke_color = st.color_picker("Couleur du trait :", "#000000")
realtime_update = st.checkbox("Mise à jour en temps réel ?", True)
# Créer un canvas pour dessiner
# Création du canvas
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

# Affichage des résultats
if canvas_result.image_data is not None:
    st.subheader("Aperçu de l'image générée :")
    st.image(canvas_result.image_data)

    # Conversion en format PNG pour traitement ou envoi
    img = Image.fromarray((canvas_result.image_data).astype("uint8"))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Bouton pour simuler l'envoi au backend
    if st.button("Prédire"):
         # Générer un nom unique pour l'image (timestamp)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_folder}/image_{timestamp}.png"
        
        # Sauvegarder l'image localement dans le dossier /images
        img.save(image_filename)
        st.info(f"L'image a été sauvegardée sous `{image_filename}`.")
        response = requests.post(
            "https://api-cloud-g4-0bc391d2f0c3.herokuapp.com/models/predict",
            files={"file": buffer}
        )
        if response.status_code == 200:
            result = response.json()
            #label = result.get("label", "N/A")
            
            # Afficher le résultat à l'utilisateur
            st.success(f"Résultat : {result}")

            # Enregistrer les résultats dans un fichier CSV
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "timestamp": [timestamp],
#                "label": [label],
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
