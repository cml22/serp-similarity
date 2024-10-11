import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_serp(keyword, language, country):
    # Construction de l'URL de recherche
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"

    # En-têtes pour simuler un navigateur Chrome
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des résultats.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraction des URLs des résultats de recherche
    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        if link:
            results.append((link['href'], link.get_text()))

    return url, results  # Retourne également l'URL de recherche

def calculate_similarity(results1, results2):
    # Calcul des URLs communes
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    # Taux de similarité
    similarity_rate = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0
    
    return list(common_urls), similarity_rate, len(common_urls), urls1, urls2

# Interface utilisateur avec Streamlit
st.title("Analyse de Similarité SERP")

# Entrée des mots-clés
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Mot-clé 1 :")
    language1 = st.selectbox("Langue (Mot-clé 1) :", ["fr", "en", "es", "de", "it", "pt"])
    country1 = s
