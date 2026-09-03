import streamlit as st
import geopandas as gpd
import pandas as pd


st.set_page_config(
    page_title="Cultures",
    page_icon="🌿",
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

st.title("🌿 Cultures des microjardins")


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


# =========================================================
# CORRECTION ENCODAGE
# =========================================================

for colonne in jardins.columns:

    if jardins[colonne].dtype == "object":

        jardins[colonne] = jardins[colonne].apply(
            corriger_encodage
        )


# =========================================================
# RECHERCHE DU CHAMP CULTURE
# =========================================================

colonne_culture = None


if "VariÃ©tÃ©" in jardins.columns:

    colonne_culture = "VariÃ©tÃ©"

else:

    for colonne in jardins.columns:

        if "Vari" in str(colonne):

            colonne_culture = colonne
            break


if colonne_culture is None:

    st.error(
        "❌ Le champ contenant les cultures n'a pas été trouvé."
    )

    st.write(
        "Champs disponibles :"
    )

    st.write(
        list(jardins.columns)
    )

    st.stop()


# =========================================================
# PREPARATION DES CULTURES
# =========================================================

cultures_par_site = []


for _, ligne in jardins.iterrows():

    site = ligne.get(
        "position",
        "Site inconnu"
    )


    valeur = ligne.get(
        colonne_culture,
        ""
    )


    if pd.notna(valeur):

        cultures = str(valeur).split(",")


        for culture in cultures:

            culture = culture.strip()


            if culture:

                # Correction supplémentaire
                culture = corriger_encodage(
                    culture
                )


                cultures_par_site.append({

                    "Site": site,

                    "Culture": culture

                })


# =========================================================
# DATAFRAME
# =========================================================

df_cultures = pd.DataFrame(
    cultures_par_site
)


if df_cultures.empty:

    st.warning(
        "⚠️ Aucune culture disponible dans les données."
    )

    st.stop()


# =========================================================
# FILTRES
# =========================================================

st.sidebar.title("🔎 Filtres")


# ---------------------------------------------------------
# CULTURES
# ---------------------------------------------------------

liste_cultures = sorted(

    df_cultures["Culture"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()

)


culture_selection = st.sidebar.multiselect(

    "🌿 Culture",

    liste_cultures,

    placeholder="Choisissez une culture"

)


# ---------------------------------------------------------
# SITES
# ---------------------------------------------------------

liste_sites = sorted(

    df_cultures["Site"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()

)


site_selection = st.sidebar.multiselect(

    "📍 Site",

    liste_sites,

    placeholder="Choisissez un site"

)


# =========================================================
# APPLICATION DES FILTRES
# =========================================================

df_filtre = df_cultures.copy()


if culture_selection:

    df_filtre = df_filtre[
        df_filtre["Culture"]
        .isin(culture_selection)
    ]


if site_selection:

    df_filtre = df_filtre[
        df_filtre["Site"]
        .isin(site_selection)
    ]


# =========================================================
# VERIFICATION
# =========================================================

if df_filtre.empty:

    st.warning(
        "⚠️ Aucun résultat pour les filtres sélectionnés."
    )

    st.stop()


# =========================================================
# INDICATEURS
# =========================================================

nombre_cultures = (
    df_filtre["Culture"]
    .nunique()
)


nombre_sites = (
    df_filtre["Site"]
    .nunique()
)


nombre_enregistrements = len(
    df_filtre
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🌿 Cultures",
        nombre_cultures
    )


with col2:

    st.metric(
        "📍 Sites",
        nombre_sites
    )


with col3:

    st.metric(
        "📋 Enregistrements",
        nombre_enregistrements
    )


# =========================================================
# CULTURES RECENSEES
# =========================================================

st.subheader(
    "🌿 Cultures recensées"
)


df_comptage = (

    df_filtre["Culture"]

    .value_counts()

    .reset_index()

)


df_comptage.columns = [

    "Culture",

    "Nombre de sites"

]


st.dataframe(

    df_comptage,

    use_container_width=True,

    hide_index=True

)


# =========================================================
# GRAPHIQUE
# =========================================================

st.subheader(
    "📊 Répartition des cultures"
)


graphique = df_comptage.set_index(
    "Culture"
)


st.bar_chart(
    graphique
)


# =========================================================
# CULTURES PAR SITE
# =========================================================

st.subheader(
    "📍 Cultures par site"
)


for site in sorted(
    df_filtre["Site"].unique()
):

    cultures_site = (

        df_filtre[
            df_filtre["Site"] == site
        ]["Culture"]

        .drop_duplicates()

        .tolist()

    )


    st.markdown(
        f"### 🌱 {site}"
    )


    st.write(
        ", ".join(cultures_site)
    )


# =========================================================
# DONNEES DETAILLEES
# =========================================================

st.subheader(
    "📋 Données détaillées"
)


st.dataframe(

    df_filtre.sort_values(
        ["Site", "Culture"]
    ),

    use_container_width=True,

    hide_index=True

)


# =========================================================
# MESSAGE FINAL
# =========================================================

st.markdown("---")


st.success(

    f"✅ {nombre_cultures} culture(s) "
    f"sur {nombre_sites} site(s) après filtrage."

)