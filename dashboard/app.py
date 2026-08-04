import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="GetAround", layout="wide")
st.title("GetAround, delai minimum entre deux locations")

@st.cache_data
def charger_donnees():
    chaines = pd.read_csv("chaines_clean.csv")
    delay = pd.read_csv("delay_clean.csv")
    return chaines, delay

chaines, delay = charger_donnees()

attentes = chaines[chaines["attente_conducteur"] > 0]

col1, col2, col3 = st.columns(3)
col1.metric("Enchainements analysés", len(chaines))
col2.metric("Conducteurs ayant attendu", len(attentes))
col3.metric("Attente mediane", f"{attentes['attente_conducteur'].median():.0f} min")

st.divider()
st.subheader("Simulateur de délai minimum")

col_seuil, col_scope = st.columns([3, 1])
seuil = col_seuil.slider("Délai minimum (minutes)", 0, 240, 60, step=15)
scope = col_scope.radio("Périmètre", ["all", "connect"])

def impact(seuil, scope="all"):
    base = chaines if scope == "all" else chaines[chaines["checkin_type"] == "connect"]

    bloquees = base["time_delta_with_previous_rental_in_minutes"] < seuil
    attente = base["attente_conducteur"] > 0
    PRIX_MOYEN_JOUR = 121.21

    return {
        "locations_bloquees": int(bloquees.sum()),
        "part_bloquee_pct": round(bloquees.mean() * 100, 1),
        "cas_resolus": int((bloquees & attente).sum()),
        "part_resolue_pct": round((bloquees & attente).sum() / attente.sum() * 100, 1),
        "ca_perdu_eur": round(bloquees.sum() * PRIX_MOYEN_JOUR),
    }


res = impact(seuil, scope)

c1, c2, c3 = st.columns(3)
c1.metric("Locations bloquees", res["locations_bloquees"], f"{res['part_bloquee_pct']} %")
c2.metric("Cas resolus", res["cas_resolus"], f"{res['part_resolue_pct']} %")
c3.metric("CA potentiel perdu", f"{res['ca_perdu_eur']:,} EUR".replace(",", " "))


st.divider()
st.subheader("Visualisation de l'impact du seuil")

grille = pd.DataFrame([
    {"seuil": s, **impact(s, scope)}
    for s in range(0, 241, 15)
])

fig = px.line(
    grille,
    x="seuil",
    y=["part_bloquee_pct", "part_resolue_pct"],
    markers=True,
    labels={"seuil": "Delai minimum (min)", "value": "%", "variable": ""},
)
fig.add_vline(x=seuil, line_dash="dash", line_color="grey")
st.plotly_chart(fig, use_container_width=True)