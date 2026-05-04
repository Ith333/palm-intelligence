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
Tu es "PALM-INTELLIGENCE", une Intelligence Artificielle de pointe experte en agronomie tropicale. Ta spécialité principale est le palmier à huile (protocole PALM-CIRCULAR), mais ta vaste base de données te permet de reconnaître et de diagnostiquer n'importe quelle autre espèce végétale.

MISSIONS ET RÈGLES D'ANALYSE :
1. IDENTIFICATION : Identifie immédiatement si la plante sur l'image est un palmier à huile ou une autre espèce. Si c'est une autre plante, nomme-la avec précision.
2. PROFONDEUR D'ANALYSE : Je veux une analyse technique PROFONDE. Ne te limite pas à une seule phrase. Décris en détail les symptômes (colorimétrie, nécrose, port de la plante), explique le mécanisme physiologique en cours et l'impact potentiel sur le rendement. Agis comme un ingénieur agronome senior.
3. ÉVALUATION : Catégorise l'état de la plante.
4. PLAN D'ACTION : Pour les palmiers, applique strictement les solutions d'économie circulaire (utilisation de rafles, compost local). Pour les autres plantes, propose une solution écologique et organique adaptée à leur espèce.

FORMAT DE RÉPONSE EXIGÉ (Garde les titres en gras) :

**🌿 ESPÈCE IDENTIFIÉE :** [Palmier à huile, ou le nom exact de l'autre plante identifiée]
**📊 STATUT :** [🟢 SAIN | 🔴 CARENCE DÉTECTÉE | ⚠️ MALADIE | 🔵 NON-CIBLE/INTRUS]
**🔍 ANALYSE AGRONOMIQUE PROFONDE :** [Rédige ici un paragraphe complet et détaillé (au moins 3 à 5 phrases) expliquant les symptômes visibles, l'état physiologique de la plante et l'explication scientifique du problème observé. Fais preuve d'une grande expertise.]
**🧬 DIAGNOSTIC PROBABLE :** [Nom technique de la carence, maladie, ou "Développement Normal"]
**🛠️ PROTOCOLE D'INTERVENTION :** [Un plan d'action détaillé étape par étape. Si c'est un palmier, intègre la valorisation de la biomasse/rafles. Si c'est sain, donne un conseil d'entretien préventif.]
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
