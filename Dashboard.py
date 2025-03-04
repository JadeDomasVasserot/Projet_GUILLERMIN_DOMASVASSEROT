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

st.title("Quick Draw Prediction")
st.sidebar.image("https://quickdraw.withgoogle.com/static/shareimg.png", width=300)
st.sidebar.title("Pacôme GUILLERMIN")
st.sidebar.title("Jade DOMAS-VASSEROT")

csv_file = "predictions.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    st.warning(f"Le fichier `{csv_file}` n'existe pas encore. Veuillez effectuer des prédictions pour générer des données.")
    df = pd.DataFrame(columns=["timestamp", "label", "image_path"])

st.subheader("Données des prédictions")
edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor")

if st.button("Sauvegarder les modifications"):
    edited_df.to_csv(csv_file, index=False)
    st.success("Les modifications ont été sauvegardées avec succès !")
    
st.subheader("Visualisation des données")

col1, col2 = st.columns(2)

with col1:
    if not df.empty:
        # Distribution des labels
        st.markdown("### Répartition des labels prédits")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x="label", ax=ax, palette="viridis")
        ax.set_title("Distribution des Labels Prédits")
        ax.set_xlabel("Labels")
        ax.set_ylabel("Nombre de prédictions")
        st.pyplot(fig)
        
        # Camembert de répartition des labels
        st.markdown("### Répartition des labels (Camembert)")
        fig, ax = plt.subplots(figsize=(8, 8))
        df["label"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax, cmap="viridis")
        ax.set_ylabel('')
        ax.set_title("Répartition des Labels")
        st.pyplot(fig)
    else:
        st.info("Aucune donnée disponible pour la visualisation.")

with col2:
    if not df.empty:
        # Timeline des prédictions regroupée par intervalle de 15 minutes
        st.markdown("### Timeline des prédictions")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["time_group"] = df["timestamp"].dt.floor("15T")
        df_grouped = df.groupby("time_group").size().reset_index(name="count")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df_grouped, x="time_group", y="count", marker="o", ax=ax)
        ax.set_title("Évolution des prédictions dans le temps (par 15 min)")
        ax.set_xlabel("Temps")
        ax.set_ylabel("Nombre de prédictions")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Confiance moyenne par label
        st.markdown("### Confiance moyenne par label")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x="label", y="confidence", ax=ax, palette="viridis")
        ax.set_title("Confiance Moyenne par Label")
        ax.set_xlabel("Labels")
        ax.set_ylabel("Confiance Moyenne")
        st.pyplot(fig)
    else:
        st.info("Aucune donnée disponible pour la visualisation.")