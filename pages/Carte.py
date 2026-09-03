import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Carte des microjardins",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Carte interactive des microjardins de Dakar")


# ==================================================
# CORRECTION DE L'ENCODAGE
# ==================================================

def corriger_encodage(texte):

    if not isinstance(texte, str):
        return texte

    corrections = {
        "dâ": "d’",
        "dâ€™": "d’",
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
        "Ã‡": "Ç"
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


# ==================================================
# CORRECTION ENCODAGE DES MICROJARDINS
# ==================================================

for colonne in jardins.columns:

    if jardins[colonne].dtype == "object":

        jardins[colonne] = jardins[colonne].apply(
            corriger_encodage
        )


# ==================================================
# CRS DES MICROJARDINS
# ==================================================

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


# ==================================================
# CORRECTION ENCODAGE DES COMMUNES
# ==================================================

for colonne in communes.columns:

    if communes[colonne].dtype == "object":

        communes[colonne] = communes[colonne].apply(
            corriger_encodage
        )


# ==================================================
# CRS DES COMMUNES
# ==================================================

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
# FONDS DE CARTE
# ==================================================

folium.TileLayer(

    "OpenStreetMap",

    name="🗺️ OpenStreetMap",

    overlay=False,

    control=True

).add_to(carte)


folium.TileLayer(

    "CartoDB positron",

    name="⚪ Carte claire",

    overlay=False,

    control=True

).add_to(carte)


folium.TileLayer(

    "CartoDB dark_matter",

    name="⚫ Carte sombre",

    overlay=False,

    control=True

).add_to(carte)


# ==================================================
# FOND SATELLITAIRE
# ==================================================

folium.TileLayer(

    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",

    attr="Google Satellite",

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


# ==================================================
# RECHERCHE AUTOMATIQUE DU NOM DE COMMUNE
# ==================================================

colonnes_nom = [

    "NAME_4",
    "nom",
    "NOM",
    "Nom",
    "NAME",
    "Name",
    "COMMUNE",
    "Commune"

]


colonne_nom = None


for colonne in colonnes_nom:

    if colonne in communes.columns:

        colonne_nom = colonne

        break


# ==================================================
# AJOUT DES COMMUNES
# ==================================================

for _, commune in communes.iterrows():

    if colonne_nom:

        nom_commune = str(
            commune[colonne_nom]
        )

    else:

        nom_commune = "Commune"


    # Correction finale du nom
    nom_commune = corriger_encodage(
        nom_commune
    )


    popup = f"""

    <div style="
        width:200px;
        font-family:Arial;
    ">

        <h4>
            🏘️ {nom_commune}
        </h4>

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

    ).add_to(
        communes_layer
    )


communes_layer.add_to(
    carte
)


# ==================================================
# MICROJARDINS
# ==================================================

jardins_layer = folium.FeatureGroup(

    name="🌱 Microjardins",

    show=True

)


# ==================================================
# RECHERCHE DU CHAMP DES VARIÉTÉS
# ==================================================

champ_variete = None


if "VariÃ©tÃ©" in jardins.columns:

    champ_variete = "VariÃ©tÃ©"

else:

    for colonne in jardins.columns:

        if "Vari" in str(colonne):

            champ_variete = colonne

            break


# ==================================================
# AJOUT DES MICROJARDINS
# ==================================================

for _, jardin in jardins.iterrows():

    point = jardin.geometry


    # ----------------------------------------------
    # Nom du site
    # ----------------------------------------------

    nom = jardin.get(

        "position",

        "Microjardin"

    )


    # ----------------------------------------------
    # Responsable
    # ----------------------------------------------

    responsable = jardin.get(

        "Responsabl",

        "Non renseigné"

    )


    # ----------------------------------------------
    # Variétés
    # ----------------------------------------------

    if champ_variete:

        varietes = jardin.get(

            champ_variete,

            "Non renseignées"

        )

    else:

        varietes = "Non renseignées"


    # ----------------------------------------------
    # Commentaire
    # ----------------------------------------------

    commentaire = jardin.get(

        "commentair",

        "Aucun commentaire"

    )


    # ----------------------------------------------
    # Valeurs manquantes
    # ----------------------------------------------

    if str(nom).lower() == "nan":

        nom = "Microjardin"


    if str(responsable).lower() == "nan":

        responsable = "Non renseigné"


    if str(varietes).lower() == "nan":

        varietes = "Non renseignées"


    if str(commentaire).lower() == "nan":

        commentaire = "Aucun commentaire"


    # ----------------------------------------------
    # Correction encodage
    # ----------------------------------------------

    nom = corriger_encodage(
        str(nom)
    )

    responsable = corriger_encodage(
        str(responsable)
    )

    varietes = corriger_encodage(
        str(varietes)
    )

    commentaire = corriger_encodage(
        str(commentaire)
    )


    # ==================================================
    # POPUP
    # ==================================================

    popup = f"""

    <div style="
        width:300px;
        font-family:Arial;
    ">

        <h4 style="
            color:green;
        ">
            🌱 {nom}
        </h4>


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


    # ==================================================
    # MARKER
    # ==================================================

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

    ).add_to(
        jardins_layer
    )


jardins_layer.add_to(
    carte
)


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

    f"✅ {len(jardins)} microjardins affichés "
    f"dans les limites des communes."

)

