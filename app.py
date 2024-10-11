import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_serp(keyword, language, country):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des résultats.")
        return [], []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    titles = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        title = g.find('h3')
        if link and title:
            results.append(link['href'])  # Stocke seulement l'URL
            titles.append(title.get_text())  # Stocke le title

    return results, titles  # Retourne seulement les résultats et les titles

def calculate_keyword_presence(titles, keyword1, keyword2):
    presence_count = sum(1 for title in titles if keyword1.lower() in title.lower() and keyword2.lower() in title.lower())
    return presence_count

def calculate_similarity(results1, results2, titles1, titles2, keyword1, keyword2):
    urls1 = set(results1)
    urls2 = set(results2)

    common_urls = urls1.intersection(urls2)
    unique_urls1 = urls1 - urls2
    unique_urls2 = urls2 - urls1

    total_urls = len(urls1.union(urls2))

    # Calculer les taux
    common_count = len(common_urls)
    non_common_count = len(urls1) + len(urls2) - common_count

    common_keyword_presence = calculate_keyword_presence([titles1[results1.index(url)] for url in common_urls], keyword1, keyword2)
    non_common_keyword_presence = (
        calculate_keyword_presence([titles1[results1.index(url)] for url in unique_urls1], keyword1, keyword2) +
        calculate_keyword_presence([titles2[results2.index(url)] for url in unique_urls2], keyword1, keyword2)
    )

    common_percentage = (common_keyword_presence / common_count * 100) if common_count > 0 else 0
    non_common_percentage = (non_common_keyword_presence / non_common_count * 100) if non_common_count > 0 else 0

    return list(common_urls), common_percentage, list(unique_urls1), list(unique_urls2), non_common_percentage

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
        results_keyword1, titles_keyword1 = scrape_serp(keyword1, language1, country1)
        results_keyword2, titles_keyword2 = scrape_serp(keyword2, language2, country2)

        # Calculer la similarité
        common_urls, common_percentage, unique_urls1, unique_urls2, non_common_percentage = calculate_similarity(
            results_keyword1, results_keyword2, titles_keyword1, titles_keyword2, keyword1, keyword2
        )

        # Affichage des résultats
        st.write(f"**Taux d'URLs communes contenant les deux mots-clés : {common_percentage:.2f}%**")
        st.write(f"**Taux d'URLs non communes contenant les deux mots-clés : {non_common_percentage:.2f}%**")

        # Affichage des résultats de SERP sous forme d'accordéon
        with st.expander("Afficher SERP pour le Mot-clé 1"):
            st.write("**SERP pour le Mot-clé 1**")
            for url in results_keyword1:
                st.write(url)

        with st.expander("Afficher SERP pour le Mot-clé 2"):
            st.write("**SERP pour le Mot-clé 2**")
            for url in results_keyword2:
                st.write(url)

        # Affichage des URLs communes
        st.write("**URLs communes**")
        for url in common_urls:
            st.write(url)

        # Affichage des URLs uniques pour chaque mot-clé
        with st.expander("URLs uniquement présentes pour le Mot-clé 1"):
            for url in unique_urls1:
                st.write(url)

        with st.expander("URLs uniquement présentes pour le Mot-clé 2"):
            for url in unique_urls2:
                st.write(url)

    else:
        st.error("Veuillez entrer les deux mots-clés.")
