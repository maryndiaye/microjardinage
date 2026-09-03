import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import LocateControl
import streamlit_folium

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Carte des microjardins",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Carte interactive des microjardins de Dakar")


# ==================================================
# CORRECTION ENCODAGE
# ==================================================

def corriger_encodage(texte):

    if not isinstance(texte, str):
        return texte

    corrections = {
        "Ã©": "é",
        "Ã¨": "è",
        "Ãª": "ê",
        "Ã«": "ë",
        "Ã ": "à",
        "Ã¢": "â",
        "Ã®": "î",
        "Ã¯": "ï",
        "Ã´": "ô",
        "Ã¶": "ö",
        "Ã»": "û",
        "Ã¼": "ü",
        "Ã¹": "ù",
        "Ã§": "ç",
        "Ã‰": "É",
        "Ã€": "À",
        "Ã‚": "Â",
        "ÃŽ": "Î",
        "Ã”": "Ô",
        "Ã›": "Û",
        "Ã‡": "Ç",
        "dâ": "d’",
        "dâ€™": "d’"
    }

    for ancien, nouveau in corrections.items():
        texte = texte.replace(ancien, nouveau)

    return texte


# ==================================================
# CHARGEMENT DES MICROJARDINS
# ==================================================

try:

    jardins = gpd.read_file("sites.shp")

except Exception as e:

    st.error(
        f"❌ Impossible de charger sites.shp : {e}"
    )

    st.stop()


# Correction des textes

for colonne in jardins.columns:

    if jardins[colonne].dtype == "object":

        jardins[colonne] = jardins[colonne].apply(
            corriger_encodage
        )


# CRS

if jardins.crs is None:

    jardins = jardins.set_crs(
        epsg=32628
    )

jardins = jardins.to_crs(
    epsg=4326
)


# ==================================================
# CHARGEMENT DES COMMUNES
# ==================================================

try:

    communes = gpd.read_file(
        "Com_Dakar.shp"
    )

except Exception as e:

    st.error(
        f"❌ Impossible de charger Com_Dakar.shp : {e}"
    )

    st.stop()


# Correction des textes

for colonne in communes.columns:

    if communes[colonne].dtype == "object":

        communes[colonne] = communes[colonne].apply(
            corriger_encodage
        )


# CRS

if communes.crs is None:

    communes = communes.set_crs(
        epsg=32628
    )

communes = communes.to_crs(
    epsg=4326
)


# ==================================================
# INFORMATIONS
# ==================================================

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"🌱 {len(jardins)} microjardins"
    )

with col2:

    st.info(
        f"🏘️ {len(communes)} communes"
    )


# ==================================================
# CARTE
# ==================================================

carte = folium.Map(

    location=[
        14.7167,
        -17.4677
    ],

    zoom_start=11,

    control_scale=True
)


# ==================================================
# 📍 POSITION DE L'UTILISATEUR
# ==================================================

LocateControl(

    auto_start=False,

    strings={
        "title": "Afficher ma position",
        "popup": "Vous êtes ici"
    }

).add_to(carte)


# ==================================================
# FONDS DE CARTE
# ==================================================

folium.TileLayer(

    "OpenStreetMap",

    name="OpenStreetMap"

).add_to(carte)


folium.TileLayer(

    "CartoDB positron",

    name="Carte claire"

).add_to(carte)


folium.TileLayer(

    "CartoDB dark_matter",

    name="Carte sombre"

).add_to(carte)


# Satellite

folium.TileLayer(

    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",

    attr="Esri",

    name="🛰️ Satellite",

    overlay=False,

    control=True

).add_to(carte)


# ==================================================
# LIMITES COMMUNALES
# ==================================================

communes_layer = folium.FeatureGroup(

    name="🏘️ Limites communales",

    show=True

)


# On utilise NAME_4

if "NAME_4" in communes.columns:

    colonne_nom = "NAME_4"

else:

    colonne_nom = None


for _, commune in communes.iterrows():

    if colonne_nom:

        nom_commune = str(
            commune[colonne_nom]
        )

    else:

        nom_commune = "Commune"


    popup = f"""

    <div style="width:200px">

        <h4>🏘️ {nom_commune}</h4>

    </div>

    """


    folium.GeoJson(

        commune.geometry,

        style_function=lambda feature: {

            "fillColor": "transparent",

            "color": "black",

            "weight": 2,

            "fillOpacity": 0

        },

        tooltip=nom_commune,

        popup=folium.Popup(

            popup,

            max_width=250

        )

    ).add_to(communes_layer)


communes_layer.add_to(carte)


# ==================================================
# MICROJARDINS
# ==================================================

jardins_layer = folium.FeatureGroup(

    name="🌱 Microjardins",

    show=True

)


# Recherche automatique du champ culture

colonne_culture = None

for colonne in jardins.columns:

    if "Vari" in colonne:

        colonne_culture = colonne

        break


# Ajout des marqueurs

for _, jardin in jardins.iterrows():

    point = jardin.geometry


    nom = jardin.get(

        "position",

        "Microjardin"

    )


    responsable = jardin.get(

        "Responsabl",

        "Non renseigné"

    )


    if colonne_culture:

        varietes = jardin.get(

            colonne_culture,

            "Non renseignées"

        )

    else:

        varietes = "Non renseignées"


    commentaire = jardin.get(

        "commentair",

        "Aucun commentaire"

    )


    # Gestion des valeurs vides

    if str(responsable) == "nan":

        responsable = "Non renseigné"


    if str(varietes) == "nan":

        varietes = "Non renseignées"


    if str(commentaire) == "nan":

        commentaire = "Aucun commentaire"


    popup = f"""

    <div style="width:300px">

        <h4>🌱 {nom}</h4>

        <b>👤 Responsable :</b><br>

        {responsable}

        <br><br>

        <b>🌿 Variétés :</b><br>

        {varietes}

        <br><br>

        <b>📝 Commentaire :</b><br>

        {commentaire}

    </div>

    """


    folium.Marker(

        location=[

            point.y,

            point.x

        ],

        tooltip=f"🌱 {nom}",

        popup=folium.Popup(

            popup,

            max_width=350

        ),

        icon=folium.Icon(

            color="green",

            icon="leaf",

            prefix="fa"

        )

    ).add_to(jardins_layer)


jardins_layer.add_to(carte)


# ==================================================
# CONTRÔLE DES COUCHES
# ==================================================

folium.LayerControl(

    collapsed=False

).add_to(carte)


# ==================================================
# AFFICHAGE
# ==================================================

st_folium(

    carte,

    width=None,

    height=650

)


# ==================================================
# MESSAGE
# ==================================================

st.success(

    f"✅ {len(jardins)} microjardins affichés."

)
