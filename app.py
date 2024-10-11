import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_serp(keyword, lang, country):
    # Fonction de scraping pour récupérer les URLs du SERP
    url = f"https://www.google.com/search?q={keyword}&hl={lang}&gl={country}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')['href']
        results.append(link)
    return results[:10]

st.title("Analyse de Similarité SERP")

# Entrée des mots-clés
keyword1 = st.text_input("Entrez le mot-clé 1")
keyword2 = st.text_input("Entrez le mot-clé 2")
lang1 = st.selectbox("Langue du mot-clé 1", options=["fr", "en", "es", "de", "it"], index=0)
lang2 = st.selectbox("Langue du mot-clé 2", options=["fr", "en", "es", "de", "it"], index=0)

if st.button("Analyser"):
    # Scraping des SERPs
    urls1 = scrape_serp(keyword1, lang1, "FR")
    urls2 = scrape_serp(keyword2, lang2, "FR")

    # Calcul du taux de similarité
    common_urls = list(set(urls1) & set(urls2))
    similarity_rate = len(common_urls) / 10 * 100  # Sur 10 URLs

    # Affichage des résultats
    st.subheader("Résultats de l'analyse")
    st.write(f"Taux de similarité : {similarity_rate:.2f}%")
    st.write(f"URLs communes : {len(common_urls)}")

    # Affichage des URLs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"URLs pour le mot-clé 1 : {keyword1}")
        for url in urls1:
            st.write(url)
    
    with col2:
        st.subheader(f"URLs pour le mot-clé 2 : {keyword2}")
        for url in urls2:
            st.write(url)
    
    # Affichage des URLs communes
    st.subheader("URLs communes")
    for url in common_urls:
        st.write(url)

    # Comparaison visuelle
    st.subheader("Comparaison des SERPs")
    for url in urls1:
        if url in urls2:
            st.write(f"🔄 {url} (Commun)")
        else:
            st.write(f"⬇️ {url} (Non trouvé dans {keyword2})")

    for url in urls2:
        if url not in urls1:
            st.write(f"⬆️ {url} (Non trouvé dans {keyword1})")
