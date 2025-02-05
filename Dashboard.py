import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurer la page
st.set_page_config(
    page_title="My Dashboard",
    page_icon="💶",
    layout="wide",
)

# Ajouter un titre et une image dans la barre latérale
st.title("Quick Draw Prediction")
st.sidebar.image("https://quickdraw.withgoogle.com/static/shareimg.png", width=300)
st.sidebar.title("Pacôme GUILLERMIN")
st.sidebar.title("Jade DOMAS-VASSEROT")

# Charger le fichier CSV
csv_file = "predictions.csv"

# Vérifier si le fichier existe
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    st.warning(f"Le fichier `{csv_file}` n'existe pas encore. Veuillez effectuer des prédictions pour générer des données.")
    df = pd.DataFrame(columns=["timestamp", "label", "image_path"])

# Afficher les données du fichier CSV
st.subheader("Données des prédictions")
edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor")

# Sauvegarder les modifications dans le fichier CSV
if st.button("Sauvegarder les modifications"):
    edited_df.to_csv(csv_file, index=False)
    st.success("Les modifications ont été sauvegardées avec succès !")

# Visualisation des données avec Seaborn
st.subheader("Visualisation des données")

if not df.empty:
    # Graphique de répartition des labels prédits
    st.markdown("### Répartition des labels prédits")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x="label", ax=ax, palette="viridis")
    ax.set_title("Distribution des Labels Prédits")
    ax.set_xlabel("Labels")
    ax.set_ylabel("Nombre de prédictions")
    st.pyplot(fig)
else:
    st.info("Aucune donnée disponible pour la visualisation.")
