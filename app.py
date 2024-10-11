import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Liste des User Agents incluant Chrome et d'autres navigateurs
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL Build/PQ3A.190801.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]

# Fonction pour obtenir les URLs SERP
def get_serp_urls(query, language, country, user_agent):
    headers = {
        "User-Agent": user_agent
    }
    url = f"https://www.google.{country}/search?q={query}&hl={language}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('h3')  # Extraction des titres des résultats
    urls = [result.find_parent('a')['href'] for result in results if result.find_parent('a')]
    return urls

# Fonction pour calculer le taux de similarité
def calculate_similarity(urls1, urls2):
    set1 = set(urls1)
    set2 = set(urls2)
    common_urls = set1.intersection(set2)
    similarity = (len(common_urls) / ((len(set1) + len(set2)) / 2)) * 100 if (len(set1) + len(set2)) > 0 else 0
    return round(similarity, 2), len(common_urls), list(common_urls)

# Interface Streamlit
st.title("Outil de Comparaison des SERP")
st.sidebar.header("Options de recherche")

# Saisie des mots-clés
keyword1 = st.sidebar.text_input("Mot-clé 1")
keyword2 = st.sidebar.text_input("Mot-clé 2")

# Choix de la langue, du pays et du User Agent
languages = ["fr", "en", "de", "es", "it"]
countries = ["com", "fr", "de", "es", "co.uk"]

selected_language = st.sidebar.selectbox("Langue", languages)
selected_country = st.sidebar.selectbox("Pays", countries)
selected_user_agent = st.sidebar.selectbox("User Agent", USER_AGENTS)

if st.sidebar.button("Comparer les SERP"):
    # Obtenir les URLs des SERP
    urls1 = get_serp_urls(keyword1, selected_language, selected_country, selected_user_agent)
    urls2 = get_serp_urls(keyword2, selected_language, selected_country, selected_user_agent)

    # Calculer le taux de similarité
    similarity, common_count, common_urls = calculate_similarity(urls1, urls2)

    # Affichage des résultats
    st.subheader(f"Taux de similarité : {similarity}% (Nombre d'URLs communes : {common_count})")

    # Accordéons pour afficher les SERP
    with st.expander("Afficher SERP 1"):
        st.write(urls1)
    
    with st.expander("Afficher SERP 2"):
        st.write(urls2)
    
    # Lister les URLs communes
    st.subheader("URLs communes")
    st.write(common_urls)

