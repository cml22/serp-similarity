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
    language1 = st.selectbox("Langue (Mot-clé 1) :", ["fr", "en", "es", "de", "it", "pt", "nl", "da", "fi", "no", "sv", "ru", "pl", "ja", "zh", "tr"])
    country1 = st.selectbox("Pays (Mot-clé 1) :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn", "be", "ch", "at", "nl", "dk", "fi", "no", "se", "jp", "cn", "hk", "sg", "in", "br", "au"])

with col2:
    keyword2 = st.text_input("Mot-clé 2 :")
    language2 = st.selectbox("Langue (Mot-clé 2) :", ["fr", "en", "es", "de", "it", "pt", "nl", "da", "fi", "no", "sv", "ru", "pl", "ja", "zh", "tr"])
    country2 = st.selectbox("Pays (Mot-clé 2) :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn", "be", "ch", "at", "nl", "dk", "fi", "no", "se", "jp", "cn", "hk", "sg", "in", "br", "au"])

if st.button("Analyser"):
    if keyword1 and keyword2:
        # Scraper les résultats pour les deux mots-clés
        url1, results_keyword1 = scrape_serp(keyword1, language1, country1)
        url2, results_keyword2 = scrape_serp(keyword2, language2, country2)

        # Calculer la similarité
        common_urls, similarity_rate, common_count, urls1, urls2 = calculate_similarity(results_keyword1, results_keyword2)

        # Affichage du taux de similarité avec le nombre d'URLs communes
        st.write(f"**Taux de similarité : {similarity_rate:.2f}% ({common_count} URLs communes)**")

        # Affichage des URLs de recherche
        st.write(f"**URL de recherche pour le Mot-clé 1 :** [{url1}]({url1})")
        st.write(f"**URL de recherche pour le Mot-clé 2 :** [{url2}]({url2})")

        # Affichage des résultats de SERP sous forme d'accordéon
        with st.expander("Afficher SERP pour le Mot-clé 1"):
            st.write("**SERP pour le Mot-clé 1**")
            for url, title in results_keyword1:
                st.write(f"[{title}]({url})")

        with st.expander("Afficher SERP pour le Mot-clé 2"):
            st.write("**SERP pour le Mot-clé 2**")
            for url, title in results_keyword2:
                st.write(f"[{title}]({url})")

        # Affichage des URLs communes
        st.write("**URLs communes**")
        for url in common_urls:
     
