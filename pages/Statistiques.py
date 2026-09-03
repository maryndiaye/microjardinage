import streamlit as st
import geopandas as gpd
import pandas as pd


st.set_page_config(
    page_title="Statistiques",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CORRECTION ENCODAGE
# =========================================================

def corriger_encodage(valeur):

    if not isinstance(valeur, str):
        return valeur

    try:
        return valeur.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return valeur


# =========================================================
# TITRE
# =========================================================

st.title("📊 Statistiques des microjardins")


# =========================================================
# CHARGEMENT
# =========================================================

try:

    jardins = gpd.read_file("sites.shp")

except Exception as e:

    st.error(
        f"❌ Impossible de charger sites.shp : {e}"
    )

    st.stop()


# Correction encodage
for colonne in jardins.columns:

    if jardins[colonne].dtype == "object":

        jardins[colonne] = jardins[colonne].apply(
            corriger_encodage
        )


# =========================================================
# FILTRES
# =========================================================

st.sidebar.title("🔎 Filtres")


# ---------------------------------------------------------
# SITE
# ---------------------------------------------------------

if "position" in jardins.columns:

    liste_sites = sorted(
        jardins["position"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    liste_sites = []


site_selection = st.sidebar.multiselect(
    "📍 Site",
    liste_sites,
    placeholder="Choisissez un site"
)


# ---------------------------------------------------------
# RESPONSABLE
# ---------------------------------------------------------

if "Responsabl" in jardins.columns:

    liste_responsables = sorted(
        jardins["Responsabl"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    liste_responsables = []


responsable_selection = st.sidebar.multiselect(
    "👤 Responsable",
    liste_responsables,
    placeholder="Choisissez un responsable"
)


# ---------------------------------------------------------
# SITUATION
# ---------------------------------------------------------

if "Contenan_R" in jardins.columns:

    liste_situations = sorted(
        jardins["Contenan_R"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    liste_situations = []


situation_selection = st.sidebar.multiselect(
    "🏗️ Situation de l'espace",
    liste_situations,
    placeholder="Choisissez une situation"
)


# =========================================================
# APPLICATION DES FILTRES
# =========================================================

jardins_filtres = jardins.copy()


if site_selection:

    jardins_filtres = jardins_filtres[
        jardins_filtres["position"]
        .astype(str)
        .isin(site_selection)
    ]


if responsable_selection:

    jardins_filtres = jardins_filtres[
        jardins_filtres["Responsabl"]
        .astype(str)
        .isin(responsable_selection)
    ]


if situation_selection:

    jardins_filtres = jardins_filtres[
        jardins_filtres["Contenan_R"]
        .astype(str)
        .isin(situation_selection)
    ]


# =========================================================
# VERIFICATION
# =========================================================

if jardins_filtres.empty:

    st.warning(
        "⚠️ Aucun microjardin ne correspond aux filtres sélectionnés."
    )

    st.stop()


# =========================================================
# INDICATEURS
# =========================================================

nombre_jardins = len(jardins_filtres)


if "position" in jardins_filtres.columns:

    nombre_sites = (
        jardins_filtres["position"]
        .dropna()
        .astype(str)
        .nunique()
    )

else:

    nombre_sites = 0


if "Responsabl" in jardins_filtres.columns:

    nombre_responsables = (
        jardins_filtres["Responsabl"]
        .dropna()
        .astype(str)
        .nunique()
    )

else:

    nombre_responsables = 0


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🌱 Microjardins",
        nombre_jardins
    )


with col2:

    st.metric(
        "📍 Sites",
        nombre_sites
    )


with col3:

    st.metric(
        "👤 Responsables",
        nombre_responsables
    )


# =========================================================
# SITUATION DES ESPACES
# =========================================================

st.subheader("🏗️ Situation des espaces")


if "Contenan_R" in jardins_filtres.columns:

    df_situation = (

        jardins_filtres["Contenan_R"]

        .fillna("Non renseignée")

        .astype(str)

        .value_counts()

        .reset_index()

    )


    df_situation.columns = [
        "Situation",
        "Nombre"
    ]


    st.dataframe(
        df_situation,
        use_container_width=True,
        hide_index=True
    )


    st.bar_chart(
        df_situation.set_index(
            "Situation"
        )
    )

else:

    st.info(
        "Aucune information sur la situation des espaces."
    )


# =========================================================
# BESOINS
# =========================================================

st.subheader("🛠️ Besoins des microjardins")


if "Exp_Besoin" in jardins_filtres.columns:

    df_besoins = jardins_filtres[
        ["position", "Exp_Besoin"]
    ].copy()


    df_besoins.columns = [
        "Site",
        "Besoins"
    ]


    df_besoins["Besoins"] = (
        df_besoins["Besoins"]
        .fillna("Non renseigné")
        .astype(str)
    )


    st.dataframe(
        df_besoins,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Aucune information sur les besoins."
    )


# =========================================================
# MATERIELS
# =========================================================

st.subheader("🧰 Matériels et contenants")


if "Nombre_T_P" in jardins_filtres.columns:

    df_materiels = jardins_filtres[
        ["position", "Nombre_T_P"]
    ].copy()


    df_materiels.columns = [
        "Site",
        "Matériels / contenants"
    ]


    df_materiels[
        "Matériels / contenants"
    ] = (

        df_materiels[
            "Matériels / contenants"
        ]

        .fillna("Non renseigné")

        .astype(str)

    )


    st.dataframe(
        df_materiels,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Aucune information sur les matériels."
    )


# =========================================================
# CULTURES
# =========================================================

st.subheader("🌿 Cultures")


champ_variete = None


if "VariÃ©tÃ©" in jardins_filtres.columns:

    champ_variete = "VariÃ©tÃ©"

else:

    for colonne in jardins_filtres.columns:

        if "Vari" in str(colonne):

            champ_variete = colonne
            break


if champ_variete:

    df_cultures = jardins_filtres[
        ["position", champ_variete]
    ].copy()


    df_cultures.columns = [
        "Site",
        "Cultures"
    ]


    df_cultures["Cultures"] = (
        df_cultures["Cultures"]
        .fillna("Non renseignées")
        .astype(str)
    )


    st.dataframe(
        df_cultures,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Aucune information sur les cultures."
    )


# =========================================================
# DETAIL
# =========================================================

st.subheader("🌱 Détail des microjardins")


colonnes_affichage = []


if "position" in jardins_filtres.columns:
    colonnes_affichage.append("position")


if "Responsabl" in jardins_filtres.columns:
    colonnes_affichage.append("Responsabl")


if "Contenan_R" in jardins_filtres.columns:
    colonnes_affichage.append("Contenan_R")


if "Exp_Besoin" in jardins_filtres.columns:
    colonnes_affichage.append("Exp_Besoin")


if champ_variete:
    colonnes_affichage.append(champ_variete)


if "commentair" in jardins_filtres.columns:
    colonnes_affichage.append("commentair")


if colonnes_affichage:

    tableau = jardins_filtres[
        colonnes_affichage
    ].copy()


    noms = {

        "position": "Site",

        "Responsabl": "Responsable",

        "Contenan_R": "Situation",

        "Exp_Besoin": "Besoins",

        "commentair": "Commentaire"

    }


    if champ_variete:

        noms[champ_variete] = "Cultures"


    tableau = tableau.rename(
        columns=noms
    )


    st.dataframe(
        tableau,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# MESSAGE FINAL
# =========================================================

st.markdown("---")


st.success(
    f"✅ {nombre_jardins} microjardin(s) correspondant aux filtres sélectionnés."
)