import streamlit as st
import geopandas as gpd


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Microjardinage Dakar",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #218739;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f8f5;
    text-align: center;
    border: 1px solid #e1e8e1;
}

.card-title {
    font-size: 16px;
    color: #555;
}

.card-value {
    font-size: 30px;
    font-weight: bold;
    color: #218739;
}

.section-title {
    color: #218739;
    font-size: 25px;
    font-weight: bold;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CHARGEMENT DES DONNÉES
# =========================================================

try:

    jardins = gpd.read_file("sites.shp")

    nombre_jardins = len(jardins)

    if "position" in jardins.columns:
        nombre_sites = jardins["position"].dropna().nunique()
    else:
        nombre_sites = nombre_jardins

except Exception as e:

    st.error(f"❌ Impossible de charger les données : {e}")
    st.stop()


# =========================================================
# TITRE
# =========================================================

st.markdown(
    '<div class="main-title">🌱 Plateforme de microjardinage à Dakar</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Visualisation et analyse des sites de microjardinage
    dans le Département de Dakar
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STATISTIQUES PRINCIPALES
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">🌱 Microjardins recensés</div>
            <div class="card-value">{nombre_jardins}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">📍 Sites</div>
            <div class="card-value">{nombre_sites}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">📌 Zone d'étude</div>
            <div class="card-value">Dakar</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PRESENTATION
# =========================================================

st.markdown(
    '<div class="section-title">🌿 À propos du projet</div>',
    unsafe_allow_html=True
)

st.write(
    """
    Cette plateforme permet de consulter les informations relatives
    aux microjardins recensés dans le Département de Dakar.

    Elle permet notamment de visualiser la localisation des sites,
    consulter les cultures présentes et analyser les différentes
    informations collectées sur les microjardins.
    """
)


# =========================================================
# LES FONCTIONNALITES
# =========================================================

st.markdown(
    '<div class="section-title">🗺️ Fonctionnalités</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        ### 🗺️ Carte

        Visualisez les microjardins sur une carte interactive.

        Les communes sont délimitées et leurs noms sont affichés.
        Cliquez sur une commune pour voir son contour en vert.
        """
    )


with col2:

    st.markdown(
        """
        ### 📊 Statistiques

        Analysez les données des microjardins à l'aide de tableaux,
        indicateurs et graphiques.
        """
    )


with col3:

    st.markdown(
        """
        ### 🌿 Cultures

        Consultez les différentes cultures présentes dans les
        microjardins et filtrez les résultats par site ou par culture.
        """
    )


# =========================================================
# MESSAGE DE NAVIGATION
# =========================================================

st.markdown("---")

st.success(
    "👉 Utilisez le menu à gauche pour accéder à la Carte, "
    "aux Statistiques et aux Cultures."
)


# =========================================================
# PIED DE PAGE
# =========================================================

st.markdown("---")

st.caption(
    "🌱 Plateforme de microjardinage — Département de Dakar"
)