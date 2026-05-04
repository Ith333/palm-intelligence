import streamlit as st
import google.generativeai as genai
from PIL import Image

# -------------------------------------------------------------------
# 1. CONFIGURATION DE LA PAGE
# -------------------------------------------------------------------
st.set_page_config(page_title="R&D - PALM-INTELLIGENCE V2", page_icon="🌴", layout="wide")

# Masquer le menu Streamlit pour l'interface de test
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. CONFIGURATION DE L'API GEMINI
# -------------------------------------------------------------------
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("⚠️ Clé API introuvable. Veuillez configurer vos secrets Streamlit.")
    st.stop()

# Initialisation du modèle Flash (optimisé pour la rapidité sur plusieurs images)
model = genai.GenerativeModel('gemini-2.5-flash')

# -------------------------------------------------------------------
# 3. LE PROMPT SYSTÈME (MOTEUR D'ANALYSE STRICT)
# -------------------------------------------------------------------
prompt_systeme = """
Tu es le moteur d'Intelligence Artificielle "PALM-INTELLIGENCE", un expert agronome spécialisé dans la culture du palmier à huile en Afrique de l'Ouest.
Ton rôle est d'analyser des images aériennes (prises par drone) de palmiers et de fournir un diagnostic immédiat et structuré.

RÈGLES D'ANALYSE STRICTES :
1. Observe la coloration des folioles (jaunissement, nécrose, taches), la structure de la couronne et le cœur du palmier.
2. Détermine catégoriquement si le palmier est [SAIN], s'il présente une [CARENCE DÉTECTÉE] ou une [MALADIE].
3. Si le palmier est SAIN, ne propose pas de traitement. Recommande la poursuite du cycle normal.
4. Si une anomalie est détectée, donne la priorité absolue à une solution basée sur l'économie circulaire (utilisation de rafles de palmiers, compost organique, cendres) selon le protocole PALM-CIRCULAR, avant toute recommandation d'intrant chimique.

FORMAT DE RÉPONSE EXIGÉ :
Tu dois STRICTEMENT répondre selon la structure exacte ci-dessous. Ne génère aucun texte d'introduction ou de conclusion.

**STATUT :** [Indique uniquement : 🟢 SAIN ou 🔴 CARENCE DÉTECTÉE ou ⚠️ MALADIE]
**OBSERVATION VISUELLE :** [Décris en une phrase claire l'anomalie ou l'état normal des feuilles/tronc]
**DIAGNOSTIC PROBABLE :** [Nom exact du problème. Ex: Carence en Magnésium, Attaque de nuisibles, ou Aucune anomalie]
**PROTOCOLE PALM-CIRCULAR :** [Prescription précise utilisant la biomasse locale/rafles, ou "Maintien de la surveillance" si le statut est sain]
"""

# -------------------------------------------------------------------
# 4. INTERFACE UTILISATEUR (UI)
# -------------------------------------------------------------------
st.title("🌴 Laboratoire R&D : Analyse Multimédia")
st.markdown("**Projet #iCorporation** - Test de traitement par lots pour le diagnostic de masse.")

st.write("---")

# Uploader autorisant plusieurs fichiers (accept_multiple_files=True)
uploaded_files = st.file_uploader(
    "Chargez un lot d'images (Sélectionnez plusieurs fichiers simultanément)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

# -------------------------------------------------------------------
# 5. MOTEUR D'ANALYSE PAR LOTS
# -------------------------------------------------------------------
if uploaded_files:
    st.info(f"📂 {len(uploaded_files)} image(s) détectée(s). Prêt pour le diagnostic.")
    
    if st.button("🚀 Lancer l'Analyse Globale", use_container_width=True):
        
        for i, file in enumerate(uploaded_files):
            
            # Le premier rapport est ouvert par défaut, les autres sont fermés
            is_expanded = True if i == 0 else False
            
            with st.expander(f"📋 Rapport de Parcelle #{i+1} - {file.name}", expanded=is_expanded):
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    image = Image.open(file)
                    st.image(image, caption=f"Aperçu Drone #{i+1}", use_column_width=True)
                    
                with col2:
                    with st.spinner("Analyse phytosanitaire en cours..."):
                        try:
                            # Appel de l'API avec le prompt strict et l'image
                            response = model.generate_content([prompt_systeme, image])
                            
                            st.markdown("### 🧬 Diagnostic IA")
                            st.markdown(response.text)
                            
                        except Exception as e:
                            st.error(f"Erreur d'analyse pour cette image : {e}")

st.write("---")
st.caption("Environnement de Staging - Confidentiel")
