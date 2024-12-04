import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_option_menu import option_menu
from streamlit_image_comparison import image_comparison
from st_on_hover_tabs import on_hover_tabs
import base64
import requests
from PIL import Image
import numpy as np
import io

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

# Ajout de styles CSS pour changer l'image de fond
def add_bg_from_local(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Ajout de l'image de fond

add_bg_from_local("DALL·E 2024-12-03 11.43.31 - A dark and subtle abstract background suitable for a website offering AI solutions for crack detection in concrete. The design features a minimalist s.webp")



def set_global_backdrop(image_url):
    st.markdown(
        f"""
        <style>
        /* Style pour l'application globale */
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: rgba(0, 0, 0, 0.5); /* Couche sombre */
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
        }}

        /* Style pour le conteneur principal */
        .global-backdrop {{
            background: rgba(255, 255, 255, 0.2); /* Couleur blanche semi-transparente */
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: auto;
            max-width: 900px; /* Largeur limitée et centrée */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


with st.sidebar:
    selected2 = on_hover_tabs(tabName=["Home", "Prediction", "Resultats",],
                         iconName=['dashboard', 'search', 'check'], default_choice=0,
                         styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       },
                             key="1")


def array_to_image(array):
    """Convertir une liste 2D en une image PIL."""
    return Image.fromarray(np.array(array, dtype=np.uint8))

# Contenus des sections
if selected2 == "Home":
    # Titre principal
    st.title("🔍 Détection de fissures dans le béton")

    # Description
    st.markdown('''
    Bienvenue sur notre plateforme dédiée à l'inspection et au diagnostic des structures en béton.
    Nous utilisons des technologies avancées d'intelligence artificielle pour offrir des analyses rapides, fiables et automatisées.

    ### 🌟 Pourquoi choisir notre technologie ?
    - **Rapidité et précision** : Identification et catégorisation des fissures en temps réel.
    - **Fiabilité** : Détection automatisée réduisant les erreurs humaines.
    - **Durabilité** : Une maintenance proactive pour préserver la longévité des infrastructures.

    Nos outils s’adressent aux professionnels de la construction, gestionnaires d’infrastructures et experts en ingénierie.
    🚀 **Explorez notre solution et transformez la manière dont vous surveillez vos structures en béton !**
    ''')
    # Ajout d'une image ou logo (facultatif)
    st.image("jes-nov2020-img-scaled.webp", caption="Inspection des fissures dans le béton", use_container_width=True)

# Bouton d'exploration
# if st.button("Commencer l'exploration"):
#     st.write("➡️ Naviguez dans notre solution pour découvrir ses fonctionnalités !")


# Section "Prediction"
elif selected2 == "Prediction":
    st.title("Prediction des fissures à partir d'une photo")

    # Charger un fichier
# Charger un fichier
# Charger un fichier
    uploaded_file = st.file_uploader(
        "Choisissez un fichier",
        accept_multiple_files=False,
        type=["PNG", "JPG"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Image chargée.", use_container_width=True)

        # Bouton pour effectuer la prédiction
        if st.button("Faire la prédiction"):
            classification_url = "https://crackapi-798025987909.europe-west1.run.app/classification/"
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

            try:
                response = requests.post(classification_url, files=files)
                if response.status_code == 200:
                    prediction = response.json()
                    fissure_class = prediction.get("Classe de la fissure", "")

                    # Stocker la classe de fissure dans st.session_state
                    st.session_state["fissure_class"] = fissure_class


                else:
                    st.error(f"Erreur API classification : {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

        # Afficher le message de fissure_class (s'il existe) après l'action
        if "fissure_class" in st.session_state:
            fissure_class = st.session_state["fissure_class"]
            if fissure_class == "Aucune fissure detectée":
                st.success("✅ Aucune fissure détectée.")
            else:
                st.warning(f"⚠️ Fissure détectée : {fissure_class}.")

        # Bouton pour vérifier avec la segmentation
        if st.button("Vérifier avec la segmentation"):
            segmentation_url = "https://crackapi-798025987909.europe-west1.run.app/segmentation"
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

            try:
                response_seg = requests.post(segmentation_url, files=files)
                if response_seg.status_code == 200:
                    seg_data = response_seg.json()
                    image_array = seg_data.get("image", [])
                    if image_array:
                        image = array_to_image(image_array)
                        uploaded_image = Image.open(uploaded_file)
                        image_comparison(
                            img1=uploaded_image,
                            img2=image,
                            label1="Originale",
                            label2="Avec Segmentation"
                        )
                    else:
                        st.error("Erreur : L'API segmentation n'a pas retourné d'image.")
                else:
                    st.error(f"Erreur API segmentation : {response_seg.status_code} - {response_seg.text}")

            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

    # if uploaded_file:
    #     st.success(f"Le fichier '{uploaded_file.name}' a été prédit avec succès !")
    #     # set page config
    #     image_comparison(
    #         img1="05538.jpg",
    #         img2="05538pred.jpg",
    #     )


elif selected2 == "Resultats":
    st.title("Interprétation des résultats")
     # Description
    st.markdown('''
     ### 🧠 **Interprétation des résultats**
    Notre solution utilise deux modèles complémentaires pour garantir une détection et une classification précises :

    1. **Classification des fissures avec un modèle CNN :**
       - Les fissures sont classées en 4 catégories :
         - **Negative :** Aucune fissure détectée.
         - **Light :** Fissures légères.
         - **Moderate :** Fissures modérées.
         - **Severe :** Fissures sévères nécessitant une intervention urgente.
       - Si aucune fissure n’est détectée par le CNN, le modèle YOLO n'est pas déclenché.

    2. **Détection et segmentation avec YOLO :**
       - Si le CNN détecte une fissure, le modèle YOLO est activé pour :
         - **Segmenter précisément les fissures sur l'image.**
         - **Confirmer la classification initiale.**

    3. **Comparaison des résultats :**
       - Les classifications des deux modèles sont comparées :
         - En cas de concordance, la classe est validée.
         - En cas de divergence, des heuristiques ou un retour utilisateur peuvent être utilisés pour ajuster les résultats.

    Cette combinaison garantit une analyse robuste et fiable, minimisant les erreurs de classification et maximisant la précision des détections.
    ''')
    # Ajout d'une image ou logo (facultatif)
    st.image("maxresdefault.jpg", caption="Inspection des fissures dans le béton", use_container_width=True)
