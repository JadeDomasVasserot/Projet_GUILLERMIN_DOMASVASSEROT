import streamlit as st
import requests
from services.modelsService import modelsService

# Configurer la page
st.set_page_config(
    page_title="Configurations",
    page_icon="💶",
    layout="wide",
)

# Ajouter un titre et une image dans la barre latérale
st.title("Configurations des models")

def select_model(name, version):
   modelsService.model_change(name, version)
            
current = modelsService.get_current()
st.success(f'Actuel : {current['name']} (v{current['versions'][0]['version']})')

st.title("Sélecteur de Modèle") 

models = modelsService.search_all()
for model in models:
    with st.container():
        st.subheader(model["name"])
        for version in model["versions"]:
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f'Version: {version["version"]}')
            col2.write(f'Statut: {version["status"]}')
            col3.button("Sélectionner", key=f'{model["name"]}_{version["version"]}', on_click=select_model, args=(model["name"], version["version"]))