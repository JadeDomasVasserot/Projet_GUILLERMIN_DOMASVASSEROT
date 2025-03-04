import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageEnhance, ImageOps
import io
from services.predictService import predictService
from utils.utils import save, DRAW_FOLDER, setup_folders

setup_folders()

st.title("Dessinez un objet et prédissez-le")
st.header("Paramètres du Canvas")

param_col1, param_col2 = st.columns(2)
drawing_mode = param_col1.radio("Mode de dessin :", ("freedraw", "line", "rect", "circle", "transform"))
stroke_color = param_col2.color_picker("Couleur du trait :", "#000000")
stroke_width = st.slider("Épaisseur du trait :", 1, 25, 13)

col1, col2 = st.columns(2)
with col1:
    canvas_result = st_canvas(
        fill_color="#000000",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#FFFFFF",
        update_streamlit=True,
        height=500,
        width=500,
        drawing_mode=drawing_mode,
        key="canvas",
    )

with col2:
    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data).astype("uint8"))
        # Contraste
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(100)
        # Negatif
        img = img.convert("RGB")
        img = ImageOps.invert(img)
        img = img.resize((256,256), Image.LANCZOS)

        st.subheader("Aperçu de l'image générée :")
        st.image(img)

        # Sauvegarde en mémoire
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        predicted = predictService.predict_best(buffer)
        if predicted["confidence"] > st.slider("Niveau de confiance :", 0, 100, 80) / 100:
            st.success(f"Oh, It's a { predicted["label"]} !")
        else :
            st.info("Mmmmh...")
        
        if st.button("Sauvegarder l'image"):
            save(DRAW_FOLDER, img, predicted["label"], predicted["confidence"])
