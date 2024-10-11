import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_serp(query, lang="fr", region="fr"):
    # Construction de l'URL de recherche
    url = f"https://www.google.{region}/search?q={query}&hl={lang}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Extraction des URLs des résultats de recherche
    for item in soup.find_all('h3'):
        parent = item.find_parent("a")
        if parent and 'href' in parent.attrs:
            results.append(parent['href'])

    return results[:10]  # Retourne seulement les 10 premiers résultats

st.title("Outil d'analyse de SERP")

# Configuration pour le mot-clé 1
st.header("Mot-clé 1")
query1 = st.text_input("Entrez le mot-clé 1")
lang1 = st.selectbox("Langue", options=["fr", "en"], index=0)
region1 = st.selectbox("Pays", options=["fr", "us", "uk"], index=0)

# Configuration pour le mot-clé 2
st.header("Mot-clé 2")
query2 = st.text_input("Entrez le mot-clé 2")
lang2 = st.selectbox("Langue", options=["fr", "en"], index=0)
region2 = st.selectbox("Pays", options=["fr", "us", "uk"], index=0)

# Bouton pour effectuer l'analyse
if st.button("Analyser"):
    if query1 and query2:
        # Scraping des SERP
        results1 = scrape_serp(query1, lang=lang1, region=region1)
        results2 = scrape_serp(query2, lang=lang2, region=region2)

        # Calcul des URLs communes
        set_results1 = set(results1)
        set_results2 = set(results2)
        common_urls = set_results1 & set_results2
        total_urls = len(set_results1 | set_results2)
        similarity_rate = (len(common_urls) / 10 * 100) if total_urls > 0 else 0  # Taux de similarité sur les top 10

        # Affichage des résultats
        st.subheader(f"Résultats pour '{query1}' (Top 10)")
        st.write(pd.DataFrame(results1, columns=["URLs"]))

        st.subheader(f"Résultats pour '{query2}' (Top 10)")
        st.write(pd.DataFrame(results2, columns=["URLs"]))

        st.subheader("Taux d'URLs communes")
        st.write(f"Taux de similarité : {similarity_rate:.2f}%")
        
        # Affichage des URLs communes
        if common_urls:
            st.subheader("URLs communes")
            st.write(pd.DataFrame(list(common_urls), columns=["URLs"]))
        else:
            st.write("Aucune URL co
