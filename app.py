import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# -------------------------------------------------------------------
# 1. CONFIGURATION DE LA PAGE
# -------------------------------------------------------------------
st.set_page_config(page_title="PALM-INTELLIGENCE PRO", page_icon="🌴", layout="wide")

# CSS pour cacher les éléments standards et ajuster le design
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Ajustement pour que l'image prenne bien toute la largeur disponible */
            .stImage > img {
                width: 100%;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. CONFIGURATION DE L'API GEMINI
# -------------------------------------------------------------------
try:
    # On reste sur l'alias le plus stable pour la PRO
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except KeyError:
    st.error("⚠️ Clé API manquante dans les secrets.")
    st.stop()

# -------------------------------------------------------------------
# 3. LE PROMPT SYSTÈME (CONSEILLER TECHNIQUE #iCorporation)
# -------------------------------------------------------------------
prompt_systeme = """
Tu es l'IA "PALM-INTELLIGENCE PRO". Tu analyses des images de drones (Blocs de 2ha).
Ta mission : rédiger un rapport d'expertise chirurgical pour PALMCI.

DIRECTIVES DE RÉDACTION :
1. Examine les couronnes de tous les palmiers visibles (environ 280-300 par bloc).
2. Détecte les carences (potassium, azote) ou maladies débutantes. Explique biologiquement les symptômes.
3. Applique le PALM-CIRCULAR (engrais organique de rafles) UNIQUEMENT si la pathologie peut être corrigée par cet apport de matière organique.

STRUCTURE DU RAPPORT EXIGÉE :
---
### 🌿 IDENTIFICATION DU BLOC (2ha)
**Statut Global :** [🟢 SAIN | 🔴 INTERVENTION | ⚠️ SURVEILLANCE]

### 🔍 DIAGNOSTIC DE PRÉCISION (Expertise #iCorporation)
[Rédige un paragraphe de haute volée technique analysant l'état sanitaire du bloc.]

### 🛠️ PROTOCOLE D'INTERVENTION
* **Recommandation :** [Solution technique]
* **PALM-CIRCULAR (Apport Organique) :** [Recommandé / Non recommandé + Justification chimique]
* **Dosage & Zone :** [ex: kg/arbre, application en couronne]
---
"""

# -------------------------------------------------------------------
# 4. INTERFACE UTILISATEUR (Z0NE D'ACTION - HAUT)
# -------------------------------------------------------------------
# Nous avons enlevé le titre d'ici. L'application commence directement par l'action.
col_intro1, col_intro2 = st.columns([1, 4])
with col_intro1:
    st.image("https://i.imgur.com/KOTY4yX.png", width=100) # Remplace par ton logo si besoin

with col_intro2:
    st.markdown("#### Système autonome de diagnostic agronomique")
    st.caption("Module de traitement par lots de Blocs Visuels")

uploaded_files = st.file_uploader(
    "Transférez les images des blocs survolés (Sélection multiple)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

# -------------------------------------------------------------------
# 5. MOTEUR D'ANALYSE (DESIGN STACKÉ : Image GÉANTE d'abord)
# -------------------------------------------------------------------
if uploaded_files:
    st.write("---")
    if st.button("🚀 LANCER L'EXPERTISE DU DOMAINE", use_container_width=True):
        
        for i, file in enumerate(uploaded_files):
            # Expander ouvert par défaut pour le premier rapport
            is_expanded = (i == 0)
            
            with st.expander(f"📄 BLOC VISUEL VISUEL #{i+1} - Fichier : {file.name}", expanded=is_expanded):
                
                image = Image.open(file)
                
                # --- Changement Majeur de Design ---
                # Plus de colonnes. L'image occupe toute la largeur de l'expander.
                st.image(
                    image, 
                    caption=f"Aperçu Drone du Bloc #{i+1} (Détail 2,5cm/px)", 
                    use_column_width=True
                )
                
                # L'analyse vient se placer proprement en dessous
                st.write("#### Analyse de l'IA #iCorporation")
                with st.spinner("Moteur Pro en cours d'analyse..."):
                    try:
                        # Utilisation du prompt d'expertise
                        response = model.generate_content([prompt_systeme, image])
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Une erreur technique s'est produite : {e}")
            
            # --- LE FREIN ANTI-CRASH (Modèle Pro gratuit) ---
            # NOTE : Si tu as activé la facturation Google, tu peux supprimer ces 2 lignes
            # pour une vitesse d'analyse fulgurante.
            if i < len(uploaded_files) - 1:
                with st.spinner("Respect du quota API Pro (32s)..."):
                    time.sleep(32)

# -------------------------------------------------------------------
# 6. NOM DE LA PAGE (BAS DE PAGE)
# -------------------------------------------------------------------
st.write("") # Espace
st.write("---")
col_title1, col_title2 = st.columns([4, 1])
with col_title1:
    # Le nom de la page est maintenant en bas, grand et pro.
    st.title("🌴 PALM-INTELLIGENCE V2 : Expertise Pro")
with col_title2:
    st.markdown("### **#iCorporation**")
    st.caption("© 2026 - Solutions Souveraines")

