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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des résultats.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraction des URLs des résultats de recherche et des titres
    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Titre non trouvé"
            results.append((link['href'], title))

    return results

def analyze_titles(results, keyword1, keyword2):
    # Compter les occurrences des mots-clés dans les titres
    count_keyword1 = 0
    count_keyword2 = 0
    count_both_keywords = 0

    for _, title in results:
        if keyword1.lower() in title.lower():
            count_keyword1 += 1
        if keyword2.lower() in title.lower():
            count_keyword2 += 1
        if keyword1.lower() in title.lower() and keyword2.lower() in title.lower():
            count_both_keywords += 1

    return count_keyword1, count_keyword2, count_both_keywords

def calculate_similarity(results1, results2):
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    non_common_urls1 = set(urls1.keys()) - common_urls
    non_common_urls2 = set(urls2.keys()) - common_urls
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    similarity_rate = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0
    
    return common_urls, non_common_urls1, non_common_urls2, similarity_rate, urls1, urls2

# Interface utilisateur avec Streamlit
st.title("Analyse de Similarité SERP")

# Entrée des mots-clés
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Mot-clé 1 :")
    language1 = st.selectbox("Langue (Mot-clé 1) :", ["fr", "en", "es", "de", "it", "pt"])
    country1 = st.selectbox("Pays (Mot-clé 1) :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

with col2:
    keyword2 = st.text_input("Mot-clé 2 :")
    language2 = st.selectbox("Langue (Mot-clé 2) :", ["fr", "en", "es", "de", "it", "pt"])
    country2 = st.selectbox("Pays (Mot-clé 2) :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

if st.button("Analyser"):
    if keyword1 and keyword2:
        # Scraper les résultats pour les deux mots-clés
        results_keyword1 = scrape_serp(keyword1, language1, country1)
        results_keyword2 = scrape_serp(keyword2, language2, country2)

        # Calculer la similarité
        common_urls, non_common_urls1, non_common_urls2, similarity_rate, urls1, urls2 = calculate_similarity(results_keyword1, results_keyword2)

        # Analyser les titres
        count_keyword1, count_keyword2, count_both_keywords = analyze_titles(results_keyword1 + results_keyword2, keyword1, keyword2)

        # Affichage des résultats
        st.write(f"**Taux de similarité : {similarity_rate:.2f}%**")
        st.write(f"**Mot-clé 1 dans les titres : {count_keyword1} occurrences**")
        st.write(f"**Mot-clé 2 dans les titres : {count_keyword2} occurrences**")
        st.write(f"**Les deux mots-clés dans les titres : {count_both_keywords} occurrences**")

        # Affichage des résultats de SERP
        with st.expander("Afficher SERP pour le Mot-clé 1"):
            st.write("**SERP pour le Mot-clé 1**")
            for url, title in results_keyword1:
                st.write(f"{url} - {title}")

        with st.expander("Afficher SERP pour le Mot-clé 2"):
            st.write("**SERP pour le Mot-clé 2**")
            for url, title in results_keyword2:
                st.write(f"{url} - {title}")

        # Affichage des URLs communes
        st.write("**URLs communes**")
        for url in common_urls:
            st.write(url)

        # Affichage des URLs uniquement présentes pour le Mot-clé 1
        with st.expander("URLs uniquement pour le Mot-clé 1"):
            for url in non_common_urls1:
                st.write(url)

        # Affichage des URLs uniquement présentes pour le Mot-clé 2
        with st.expander("URLs uniquement pour le Mot-clé 2"):
            for url in non_common_urls2:
                st.write(url)

    else:
        st.error("Veuillez entrer les deux mots-clés.")
