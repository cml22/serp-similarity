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
            results.append(link['href'])

    return results

def calculate_similarity(results1, results2):
    # Calcul des URLs communes
    common_urls = set(results1).intersection(set(results2))
    total_urls = len(set(results1).union(set(results2)))

    # Taux de similarité
    similarity_rate = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0
    
    return list(common_urls), similarity_rate, len(common_urls)

# Interface utilisateur avec Streamlit
st.title("Analyse de Similarité SERP")

# Entrée des mots-clés
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Mot-clé 1 :")
    
with col2:
    keyword2 = st.text_input("Mot-clé 2 :")

# Sélection de la langue et du pays
language = st.selectbox("Langue :", ["fr", "en", "es", "de", "it", "pt"])
country = st.selectbox("Pays :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt"])

if st.button("Analyser"):
    if keyword1 and keyword2:
        # Scraper les résultats pour les deux mots-clés
        results_keyword1 = scrape_serp(keyword1, language, country)
        results_keyword2 = scrape_serp(keyword2, language, country)

        # Calculer la similarité
        common_urls, similarity_rate, common_count = calculate_similarity(results_keyword1, results_keyword2)

        # Affichage du taux de similarité avec le nombre d'URLs communes
        st.write(f"**Taux de similarité : {similarity_rate:.2f}% ({common_count} URLs communes)**")

        # Affichage des résultats de SERP sous forme d'accordéon
        with st.expander("Afficher SERP pour le Mot-clé 1"):
            st.write("**SERP pour le Mot-clé 1**")
            for result in results_keyword1:
                st.write(result)

        with st.expander("Afficher SERP pour le Mot-clé 2"):
            st.write("**SERP pour le Mot-clé 2**")
            for result in results_keyword2:
                st.write(result)

        # Affichage des URLs communes
        st.write("**URLs communes**")
        for url in common_urls:
            st.write(url)

    else:
        st.error("Veuillez entrer les deux mots-clés.")
