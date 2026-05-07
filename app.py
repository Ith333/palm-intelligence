import streamlit as st
import google.generativeai as genai
from PIL import Image

# -------------------------------------------------------------------
# 1. CONFIGURATION DE LA PAGE
# -------------------------------------------------------------------
st.set_page_config(page_title="PALM-INTELLIGENCE V2 PRO", layout="narrow")
st.set_page_config(page_icon= "🌴", layout="wide")
# Masquer le menu Streamlit pour garder une interface propre
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
    st.error("⚠️ Erreur : Clé API manquante dans les secrets Streamlit.")
    st.stop()

# Initialisation du modèle (Gemini 1.5 Pro pour l'expertise profonde)
model = genai.GenerativeModel('gemini-2.5-flash')

# -------------------------------------------------------------------
# 3. LE PROMPT SYSTÈME (EXPERT CONSULTANT & PALM-CIRCULAR)
# -------------------------------------------------------------------
prompt_systeme = """
Tu es l'IA "PALM-INTELLIGENCE PRO", l'expert agronome en chef de #iCorporation. 
Ta mission est de délivrer un rapport technique d'une profondeur absolue pour chaque image analysée.

DIRECTIVES DE RÉDACTION :
1. IDENTIFICATION : Identifie l'espèce. Si ce n'est pas un palmier, traite-la avec la même rigueur scientifique.
2. ANALYSE PHYSIOLOGIQUE : Ne décris pas seulement ce que tu vois, explique POURQUOI cela arrive (mécanismes biologiques, stress hydrique, attaques pathogènes).
3. SOLUTION OPTIMALE : Propose la solution biologique, organique ou de lutte intégrée la plus efficace au monde pour ce problème précis.
4. CONDITION PALM-CIRCULAR : Évalue les besoins nutritifs de la plante et du sol. Le protocole "PALM-CIRCULAR" est défini strictement comme la valorisation des résidus de récoltes (rafles de palmiers) transformés en engrais organique. Recommande ce protocole UNIQUEMENT si la carence identifiée (ex: Potassium, besoin en matière organique, paillage) peut être efficacement corrigée par cet apport en résidus. Si la pathologie exige un traitement foliaire, un fongicide ou un apport minéral que les rafles ne peuvent pas combler, prescris la solution technique adéquate sans forcer le PALM-CIRCULAR.

STRUCTURE DU RAPPORT EXIGÉE (Respecte strictement les titres) :

---
### 🌿 IDENTIFICATION DE L'UNITÉ
**Espèce :** [Nom précis] | **Statut :** [🟢 SAIN | 🔴 CARENCE | ⚠️ MALADIE | 🔵 INTRUS]

### 🔍 DIAGNOSTIC TECHNIQUE APPROFONDI
[Rédige ici un paragraphe d'expertise de haut niveau. Analyse la chlorose, la nécrose, l'angle des frondes ou l'état du stipe. Explique l'impact sur le rendement futur en tonnes de régimes/ha si rien n'est fait.]

### 🛠️ PLAN D'INTERVENTION CHIRURGICAL
**1. Solution recommandée :** [Nom de la méthode]
**2. Mise en œuvre :** [Étapes précises de l'application sur le terrain]
**3. Dosage & Quantité :** [Donne des chiffres précis : ex: kg/arbre, tonnes/ha]
**4. Localisation précise :** [Où appliquer ? En couronne autour du pied, dans l'inter-ligne d'andainage ?]
**5. Calendrier d'application :** [Période précise et fréquence]

### 📈 PROTOCOLE DE SURVEILLANCE
[Fréquence des prochains passages de drones et indicateurs visuels à surveiller pour valider la guérison.]

### ♻️ INITIATIVE PALM-CIRCULAR
[Indique explicitement si la valorisation des résidus de récolte (PALM-CIRCULAR) est recommandée. S'il l'est, explique chimiquement pourquoi cet engrais organique précis couvre le besoin. S'il ne l'est pas, explique pourquoi l'apport en résidus n'était pas la solution adaptée pour ce symptôme spécifique.]
---
"""

# -------------------------------------------------------------------
# 4. INTERFACE UTILISATEUR (UI)
# -------------------------------------------------------------------
st.title("🌴 PALM-INTELLIGENCE V2 : Expertise Pro")
st.markdown("Système de diagnostic industriel par lots - Propriété de **#iCorporation**")

st.write("---")

# Uploader autorisant plusieurs fichiers
uploaded_files = st.file_uploader(
    "Transférez les données de survol (Sélection multiple autorisée)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

# -------------------------------------------------------------------
# 5. MOTEUR D'ANALYSE PAR LOTS
# -------------------------------------------------------------------
if uploaded_files:
    st.info(f"📂 {len(uploaded_files)} image(s) détectée(s). Prêt pour le diagnostic.")
    
    if st.button("🚀 GÉNÉRER LES RAPPORTS D'EXPERTISE", use_container_width=True):
        
        for i, file in enumerate(uploaded_files):
            
            # Ouverture du premier rapport par défaut, les autres fermés
            is_expanded = True if i == 0 else False
            
            with st.expander(f"📄 RAPPORT D'EXPERTISE #{i+1} - Fichier : {file.name}", expanded=is_expanded):
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    image = Image.open(file)
                    st.image(image, caption=f"Aperçu Drone #{i+1}", use_column_width=True)
                    
                with col2:
                    with st.spinner("Analyse en cours par le moteur Pro..."):
                        try:
                            # Appel de l'API avec le prompt strict et l'image
                            response = model.generate_content([prompt_systeme, image])
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Une erreur technique s'est produite lors de l'analyse : {e}")

st.write("---")
st.caption("© 2026 #iCorporation - Solutions Agronomiques Souveraines")
