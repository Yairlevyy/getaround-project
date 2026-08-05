import json
from pathlib import Path

import requests
import streamlit as st

API_URL = "https://getaround-project-api.onrender.com/predict"
DOSSIER = Path(__file__).parent

st.set_page_config(page_title="Estimateur GetAround", page_icon="🚗")


@st.cache_data
def charger_options():
    with open(DOSSIER / "options.json") as f:
        return json.load(f)


options = charger_options()

st.title("Estimez le prix de location de votre voiture")
st.caption("Prix suggere par un modele de machine learning, a partir de 4 843 vehicules du parc GetAround.")

col1, col2 = st.columns(2)

model_key = col1.selectbox("Marque", options["model_key"])
car_type = col2.selectbox("Type de vehicule", options["car_type"])
fuel = col1.selectbox("Carburant", options["fuel"])
paint_color = col2.selectbox("Couleur", options["paint_color"])

mileage = st.slider("Kilometrage", 0, 400_000, 140_000, step=5_000)
engine_power = st.slider("Puissance (ch)", 50, 350, 120, step=5)

st.subheader("Equipements")

c1, c2, c3 = st.columns(3)
has_gps = c1.checkbox("GPS", value=True)
has_air_conditioning = c2.checkbox("Climatisation", value=True)
automatic_car = c3.checkbox("Boite automatique")
has_getaround_connect = c1.checkbox("GetAround Connect", value=True)
has_speed_regulator = c2.checkbox("Regulateur de vitesse", value=True)
winter_tires = c3.checkbox("Pneus hiver", value=True)
private_parking_available = c1.checkbox("Parking prive")

duree = st.number_input("Duree de location (jours)", min_value=1, max_value=30, value=3)

if st.button("Estimer le prix", type="primary"):
    voiture = [
        model_key, mileage, engine_power, fuel, paint_color, car_type,
        private_parking_available, has_gps, has_air_conditioning,
        automatic_car, has_getaround_connect, has_speed_regulator, winter_tires,
    ]

    with st.spinner("Appel de l'API..."):
        reponse = requests.post(API_URL, json={"input": [voiture]}, timeout=90)

    prix_jour = reponse.json()["prediction"][0]

    col_a, col_b = st.columns(2)
    col_a.metric("Prix suggere par jour", f"{prix_jour:.2f} EUR")
    col_b.metric(f"Total sur {duree} jours", f"{prix_jour * duree:.2f} EUR")