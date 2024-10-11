import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_serp(keyword, language, country):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des résultats.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Titre non trouvé"
            results.append((link['href'], title))

    return results

def analyze_titles(results, keyword1, keyword2):
    counts = {
        "common_keyword1": 0,
        "common_keyword2": 0,
        "common_both": 0,
    }

    urls_common = {url: title for url, title in results[0]}  # SERP 1
    urls_non_common = {url: title for url, title in results[1]}  # SERP 2

    for url, title in urls_common.items():
        if keyword1.lower() in title.lower() and keyword2.lower() in title.lower():
            counts["common_both"] += 1
        elif keyword1.lower() in title.lower():
            counts["common_keyword1"] += 1
        elif keyword2.lower() in title.lower():
            counts["common_keyword2"] += 1

    return counts

def calculate_similarity(results1, results2):
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    non_common_urls1 = set(urls1.keys()) - common_urls
    non_common_urls2 = set(urls2.keys()) - common_urls
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    similarity_rate = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0
    
    return common_urls, non_common_urls1, non_common_urls2, similarity_rate

# Interface utilisateur avec Streamlit
st.set_page_config(page_title="Analyse de Similarité SERP", layout="centered")
st.title("Analyse de Similarité SERP")
st.markdown("---")  # Ligne de séparation

# Entrée des mots-clés
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Entrer le Mot-clé 1 :", placeholder="Ex: marketing digital")
    language1 = st.selectbox("Langue (Mot-clé 1) :", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country1 = st.selectbox("Pays (Mot-clé 1) :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

with col2:
    keyword2 = st.text_input("Entrer le Mot-clé 2 :", placeholder="Ex: SEO")
    language2 = st.selectbox("Langue (Mot-clé 2) :", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country2 = st.selectbox("Pays (Mot-clé 2) :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

st.markdown("---")  # Ligne de séparation

if st.button("Analyser"):
    if keyword1 and keyword2:
        # Scraper les résultats pour les deux mots-clés
        results_keyword1 = scrape_serp(keyword1, language1, country1)
        results_keyword2 = scrape_serp(keyword2, language2, country2)

        # Calculer la similarité
        common_urls, non_common_urls1, non_common_urls2, similarity_rate = calculate_similarity(results_keyword1, results_keyword2)

        # Analyser les titres
        counts = analyze_titles((results_keyword1, results_keyword2), keyword1, keyword2)

        # Affichage des résultats
        st.write(f"**Taux de similarité : {similarity_rate:.2f}%**")
        
        # Résumé sur l'utilisation des mots-clés
        if counts['common_both'] > 0:
            st.success("Les deux mots-clés sont présents dans les titres de plusieurs résultats.")
        else:
            st.warning("Les deux mots-clés ne sont pas présents dans les titres de résultats communs.")

# Backlink en bas de la page
st.markdown("---")  # Ligne de séparation
st.markdown("[Développé par Charles Migaud](https://charles-migaud.fr)")
