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

# Entrée des mots-clés sans pré-remplissage
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Entrez le mot-clé 1", "")
    lang1 = st.selectbox("Langue du mot-clé 1", options=["fr", "en", "es", "de", "it"], index=0)
    country1 = st.selectbox("Pays du mot-clé 1", options=["FR", "US", "ES", "DE", "IT"], index=0)

with col2:
    keyword2 = st.text_input("Entrez le mot-clé 2", "")
    lang2 = st.selectbox("Langue du mot-clé 2", options=["fr", "en", "es", "de", "it"], index=0)
    country2 = st.selectbox("Pays du mot-clé 2", options=["FR", "US", "ES", "DE", "IT"], index=0)

if st.button("Analyser"):
    # Scraping des SERPs
    urls1 = scrape_serp(keyword1, lang1, country1)
    urls2 = scrape_serp(keyword2, lang2, country2)

    # Calcul du taux de similarité
    common_urls = list(set(urls1) & set(urls2))
    similarity_rate = len(common_urls) / 10 * 100  # Sur 10 URLs

    # Affichage des résultats
    st.subheader("Résultats de l'analyse")
    st.write(f"Taux de similarité : {similarity_rate:.2f}%")
    st.write(f"URLs communes : {len(common_urls)}")

    # Affichage des URLs dans deux colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"URLs pour le mot-clé 1 : {keyword1}")
        for url in urls1:
            st.markdown(f"[{url}]({url})")  # Affichage des URLs en tant que liens cliquables
    
    with col2:
        st.subheader(f"URLs pour le mot-clé 2 : {keyword2}")
        for url in urls2:
            st.markdown(f"[{url}]({url})")  # Affichage des URLs en tant que liens cliquables
    
    # Affichage des URLs communes
    st.subheader("URLs communes")
    for url in common_urls:
        st.write(url)

    # Comparaison visuelle
    st.subheader("Comparaison des SERPs")
    comparison_df = pd.DataFrame({
        'URL': list(set(urls1 + urls2)),
        'Position Mot-clé 1': [urls1.inde
