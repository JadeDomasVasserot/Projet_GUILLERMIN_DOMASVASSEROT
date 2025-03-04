import streamlit as st
from PIL import Image, ImageOps
import io
from services.predictService import predictService
from utils.utils import setup_folders, setup_style, to_card

setup_folders()
setup_style()

st.title("Avec la Caméra !")

camera_image = st.camera_input("Prenez une photo de l'objet")

if camera_image:
    cam_image = Image.open(camera_image)

    buffer = io.BytesIO()
    cam_image.save(buffer, format="PNG")
    buffer.seek(0)

    predicted = predictService.predict(buffer)
    if predicted is None:
        predicted = [
        {"label": "basket", "id": 0, "confidence": 0},
        {"label": "eye", "id": 1, "confidence": 0},
        {"label": "binoculars", "id": 2, "confidence": 0},
        {"label": "rabbit", "id": 3, "confidence": 0},
        {"label": "hand", "id": 4, "confidence": 0}
    ]
    for item in predicted:
        st.markdown(to_card(item), unsafe_allow_html=True)
