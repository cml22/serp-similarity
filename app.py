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
keyword1 = st.text_input("Entrez le mot-clé 1", "")  # Champ vide par défaut
keyword2 = st.text_input("Entrez le mot-clé 2", "")  # Champ vide par défaut
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
        'URL': urls1 + urls2,
        'Position Mot-clé 1': [1 + urls1.index(url) if url in urls1 else None for url in urls1 + urls2],
        'Position Mot-clé 2': [1 + urls2.index(url) if url in urls2 else None for url in urls1 + urls2]
    }).dropna()

    for index, row in comparison_df.iterrows():
        if row['Position Mot-clé 1'] == row['Position Mot-clé 2']:
            st.write(f"🔄 {row['URL']} (Stable)")
        elif row['Position Mot-clé 1'] < row['Position Mot-clé 2']:
            st.write(f"⬆️ {row['URL']} (Améliorée de {row['Position Mot-clé 1']} à {row['Position Mot-clé 2']})")
        else:
            st.write(f"⬇️ {row['URL']} (Diminution de {row['Position Mot-clé 1']} à {row['Position Mot-clé 2']})")
