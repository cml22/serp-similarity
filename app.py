import streamlit as st
import requests
from bs4 import BeautifulSoup

# Fonction pour scraper les résultats de recherche Google
def scrape_serp(query, lang="fr", region="FR"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}&hl={lang}&gl={region}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.find_all('h3'):
        parent = item.find_parent('a')
        if parent:
            results.append((item.get_text(), parent['href']))
    
    return results[:10]  # Limiter aux 10 premiers résultats

# Titre de l'application
st.title("Outil d'analyse de SERP")

# Colonne pour le mot-clé 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mot-clé 1")
    keyword1 = st.text_input("Entrez le mot-clé 1", value="exemple mot-clé 1")  # Valeur par défaut pour test
    lang1 = st.selectbox("Langue (Mot-clé 1)", options=["fr", "en", "es", "de", "it"], index=0)
    country1 = st.selectbox("Pays (Mot-clé 1)", options=["FR", "US", "GB", "DE", "IT"], index=0)

# Colonne pour le mot-clé 2
with col2:
    st.subheader("Mot-clé 2")
    keyword2 = st.text_input("Entrez le mot-clé 2", value="exemple mot-clé 2")  # Valeur par défaut pour test
    lang2 = st.selectbox("Langue (Mot-clé 2)", options=["fr", "en", "es", "de", "it"], index=0)
    country2 = st.selectbox("Pays (Mot-clé 2)", options=["FR", "US", "GB", "DE", "IT"], index=0)

# Bouton pour lancer l'analyse
if st.button("Analyser"):
    if keyword1 and keyword2:
        # Scraper les résultats pour les deux mots-clés
        results1 = scrape_serp(keyword1, lang1, country1)
        results2 = scrape_serp(keyword2, lang2, country2)

        # Extraire les URLs
        urls1 = [result[1] for result in results1]
        urls2 = [result[1] for result in results2]

        # Calculer le taux de similarité
        common_urls = set(urls1) & set(urls2)
        total_urls = len(set(urls1) | set(urls2))
        similarity_rate = len(common_urls) / total_urls * 100 if total_urls > 0 else 0

        # Afficher les résultats
        st.subheader("Résultats de l'analyse")
        st.write(f"Taux de similarité : {similarity_rate:.2f}%")
        st.write(f"URLs communes : {len(common_urls)}")
        
        # Afficher les URLs des résultats
        st.subheader("Top 10 Mot-clé 1")
        for title, url in results1:
            st.write(f"[{title}]({url})")

        st.subheader("Top 10 Mot-clé 2")
        for title, url in results2:
            st.write(f"[{title}]({url})")

        st.subheader("URLs communes")
        for url in common_urls:
            st.write(f"[{url}]({url})")
    else:
        st.warning("Veuillez entrer les deux mots-clés.")
