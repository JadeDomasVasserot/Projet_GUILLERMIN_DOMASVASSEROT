from datetime import datetime
import os
import pandas as pd
import streamlit as st
from azure.storage.blob import BlobServiceClient

AZURE_CONNECTION_URL = "DefaultEndpointsProtocol=https;AccountName=jdvpgniacloudproject;AccountKey=2edSn5N29xK38a8tXgp+XKoQw3/KqfPVe1hL5jCHHWTRpa4a2RBaRAvLoQc1wMltLtwfh6MJUlrS+AStH7RzkQ==;EndpointSuffix=core.windows.net"
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_CONNECTION_URL)
CONTAINER_BLOB_NAME = "quickdrawjdvpgn"

DRAW_FOLDER = "./images/draw"
MIMIC_FOLDER = "./images/mimic"
UPLOAD_FOLDER = "./images/upload"

def setup_folders():
    for folder in [DRAW_FOLDER, MIMIC_FOLDER, UPLOAD_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            
def setup_style():
    st.markdown("""
        <style>
            .card {
                background-color: #fff;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
            .confidence-bar {
                height: 10px;
                border-radius: 5px;
                background-color: #ddd;
                margin-top: 5px;
                position: relative;
            }
            .confidence-bar-fill {
                height: 100%;
                border-radius: 5px;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                transition: all 1s ease-out;
            }
            .label {
                font-weight: bold;
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)
    
def to_card(predicted):
    confidence_percent = int(predicted["confidence"] * 100)
    return f"""
        <div class="card">
            <div class="label">{predicted["label"].capitalize()}</div>
            <div class="confidence-bar">
                <div class="confidence-bar-fill" style="width: {confidence_percent}%;"></div>
            </div>
            <p>Confiance: {confidence_percent}%</p>
        </div>
    """

def save(folder, img, label, confidence):
    file_name = f"image_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png"
    image_filename = f"{folder}/{file_name}"
    img.save(image_filename)
    
    csv_file = "predictions.csv"
    data = {"timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "image_path": [image_filename], "label": label, "confidence" : confidence}
    try:
        df = pd.read_csv(csv_file)
        df_new = pd.DataFrame(data)
        df = pd.concat([df, df_new], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    
    blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container=CONTAINER_BLOB_NAME, blob=file_name)
    with open(image_filename, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    st.info(f"Image et données enregistrées dans Azure.")