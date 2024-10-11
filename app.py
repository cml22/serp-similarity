import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Liste des User Agents pour faire un roulement
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Liste des langues et des pays
langues_pays = {
    "fr": "Français (France)",
    "fr-ca": "Français (Canada)",
    "fr-ma": "Français (Maroc)",
    "fr-sn": "Français (Sénégal)",
    "fr-tn": "Français (Tunisie)",
    "en-gb": "Anglais (Royaume-Uni)",
    "en-us": "Anglais (États-Unis)",
    "en-ca": "Anglais (Canada)",
    "en-ie": "Anglais (Irlande)",
    "en-sg": "Anglais (Singapour)",
    "en-au": "Anglais (Australie)",
    "en-nz": "Anglais (Nouvelle-Zélande)",
    "en-in": "Anglais (Inde)",
    "en-pk": "Anglais (Pakistan)",
    "en-hk": "Anglais (Hong Kong)",
    "es-es": "Espagnol (Espagne)",
    "es-mx": "Espagnol (Mexique)",
    "es-ar": "Espagnol (Argentine)",
    "es-co": "Espagnol (Colombie)",
    "es-cl": "Espagnol (Chili)",
    "es-pe": "Espagnol (Pérou)",
    "de": "Allemand (Allemagne)",
    "de-at": "Allemand (Autriche)",
    "de-ch": "Allemand (Suisse)",
    "it": "Italien (Italie)",
    "it-ch": "Italien (Suisse)",
    "nl": "Néerlandais (Pays-Bas)",
    "nl-be": "Néerlandais (Belgique)",
    "pt": "Portugais (Portugal)",
    "pt-br": "Portugais (Brésil)",
    "pl": "Polonais (Pologne)",
    "ru": "Russe (Russie)",
    "be": "Russe (Biélorussie)",
    "zh-cn": "Chinois (Chine)",
    "zh-hk": "Chinois (Hong Kong)",
    "zh-tw": "Chinois (Taïwan)",
    "ja": "Japonais (Japon)",
    "ar-sa": "Arabe (Arabie Saoudite)",
    "ar-ae": "Arabe (Émirats Arabes Unis)",
    "tr": "Turc (Turquie)",
    "ko": "Coréen (Corée du Sud)",
    "hi": "Hindi (Inde)"
}

def fetch_serp(keyword, lang_country):
    url = f"https://www.google.{lang_country}/search?q={keyword}"
    headers = {
        "User-Agent": USER_AGENTS[hash(keyword) % len(USER_AGENTS)]
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for g in soup.find_all('div', class_='g'):
        link = g.find('a')['href']
        results.append(link)

    return results

def calculate_similarity(serp1, serp2):
    common_urls = set(serp1) & set(serp2)
    total_urls = set(serp1) | set(serp2)
    similarity_rate = (len(common_urls) / len(total_urls)) * 100 if total_urls else 0
    return similarity_rate, common_urls

# Interface Streamlit
st.title("Outil de Similarité SERP")

# Saisie des mots-clés et sélection des langues/pays
keyword1 = st.text_input("Mot-clé 1")
keyword2 = st.text_input("Mot-clé 2")
lang_country = st.selectbox("Sélectionnez la langue/pays", list(langues_pays.keys()), format_func=lambda x: langues_pays[x])

if st.button("Analyser"):
    serp1 = fetch_serp(keyword1, lang_country)
    serp2 = fetch_serp(keyword2, lang_country)
    
    # Calcul du taux de similarité
    similarity_rate, common_urls = calculate_similarity(serp1, serp2)

    # Affichage des résultats
    st.markdown(f"**Taux de similarité : {similarity_rate:.2f}% avec {len(common_urls)} URL(s) commune(s)**")
    
    # Affichage des URLs communes
    if common_urls:
        st.subheader("URLs communes")
        for url in common_urls:
            st.markdown(f"- {url}")

    # Affichage des SERPs dans des accordéons
    with st.expander("SERP pour Mot-clé 1"):
        for url in serp1:
            st.markdown(f"- {url}")
    
    with st.expander("SERP pour Mot-clé 2"):
        for url in serp2:
            st.markdown(f"- {url}")
