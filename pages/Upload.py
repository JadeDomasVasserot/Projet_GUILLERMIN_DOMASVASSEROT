import streamlit as st
from PIL import Image
from services.predictService import predictService
from utils.utils import UPLOAD_FOLDER, save, setup_folders, setup_style, to_card
import io

setup_folders()
setup_style()

st.title("Prediction par Upload de fichier")

col1, col2 = st.columns(2)
uploaded_file = col1.file_uploader("Téléchargez une image", type=["png", "jpg", "jpeg"])

predicted = None
if uploaded_file is not None:
    img = Image.open(uploaded_file)
       
    col2.subheader("Aperçu de l'image :")
    col2.image(img, caption="Image téléversée")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
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

if uploaded_file is not None:
    if st.button("Sauvegarder l'image"):
        best = max(predicted, key=lambda x: x["confidence"])
        save(UPLOAD_FOLDER, img, best["label"], best["confidence"])
