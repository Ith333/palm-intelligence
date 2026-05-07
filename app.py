import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# -------------------------------------------------------------------
# 1. CONFIGURATION TECHNIQUE ET VISUELLE
# -------------------------------------------------------------------
st.set_page_config(page_title="PALM-INTELLIGENCE PRO", page_icon="🌴", layout="wide")

# CSS pour le design épuré et l'image géante
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stImage > img {
        width: 100% !important;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        color: #1E1E1E;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. INITIALISATION DE L'IA (Correction de l'Erreur 404)
# -------------------------------------------------------------------
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    model = genai.GenerativeModel('gemini-3.1-pro') 

# -------------------------------------------------------------------
# 3. INTERFACE DE CHARGEMENT (HAUT DE PAGE)
# -------------------------------------------------------------------
st.markdown("### 🛰️ Système autonome de diagnostic agronomique")
st.caption("Module de traitement par lots - Haute Résolution")

uploaded_files = st.file_uploader(
    "Transférez les images des blocs survolés (Sélection multiple)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

# -------------------------------------------------------------------
# 4. ANALYSE ET AFFICHAGE (L'IMAGE EST REINE)
# -------------------------------------------------------------------
if uploaded_files:
    if st.button("🚀 LANCER L'EXPERTISE PRO", use_container_width=True):
        for i, file in enumerate(uploaded_files):
            # Affichage du rapport dans un conteneur large
            st.write("---")
            st.subheader(f"📄 ANALYSE DU BLOC #{i+1}")
            
            image = Image.open(file)
            
            # AFFICHAGE DE L'IMAGE EN TRÈS GRAND
            st.image(image, use_column_width=True)
            
            # ANALYSE EN DESSOUS
            with st.spinner(f"Analyse approfondie du bloc #{i+1} en cours..."):
                try:
                    # Le prompt d'expertise
                    prompt = "Analyse cette image de palmier à huile. Identifie précisément les carences ou maladies et propose le dosage PALM-CIRCULAR (rafles) adapté."
                    response = model.generate_content([prompt, image])
                    st.markdown(f"#### Rapport d'Expertise #iCorporation\n{response.text}")
                except Exception as e:
                    # Si le modèle Pro échoue encore, on bascule automatiquement sur Flash pour ne pas bloquer la démo
                    st.warning("Bascule automatique sur le moteur secondaire pour continuité de service...")
                    backup_model = genai.GenerativeModel('gemini-1.5-flash')
                    response = backup_model.generate_content([prompt, image])
                    st.markdown(response.text)
            
            # Temporisation pour le quota (Uniquement si plusieurs fichiers)
            if i < len(uploaded_files) - 1:
                time.sleep(32)

# -------------------------------------------------------------------
# 5. TITRE ET IDENTITÉ (BAS DE PAGE)
# -------------------------------------------------------------------
st.write("---")
st.markdown('<h1 class="main-title">🌴 PALM-INTELLIGENCE V2 : Expertise Pro</h1>', unsafe_allow_html=True)
st.markdown("## **#iCorporation**")
st.caption("© 2026 - Solutions Souveraines pour PALMCI")
