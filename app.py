import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

# Fonction pour scraper les SERP en fonction de la langue et la localisation
def scrape_serp(query, lang="en", country="us"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    url = f"https://www.google.com/search?q={query}&hl={lang}&gl={country}&num=100"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')['href']
        results.append(link)
    return results

# Interface utilisateur avec des clés uniques pour éviter les erreurs
st.title("SERP Similarity Analysis")

# Input des mots-clés
keyword1 = st.text_input("Mot-clé 1", key="keyword1")
keyword2 = st.text_input("Mot-clé 2", key="keyword2")

# Sélection des options de langue et de localisation
lang1 = st.selectbox("Langue pour le premier mot-clé", options=["fr", "en", "es", "de", "it"], key="lang1")
country1 = st.selectbox("Pays pour le premier mot-clé", options=["us", "fr", "es", "de", "it"], key="country1")

lang2 = st.selectbox("Langue pour le deuxième mot-clé", options=["fr", "en", "es", "de", "it"], key="lang2")
country2 = st.selectbox("Pays pour le deuxième mot-clé", options=["us", "fr", "es", "de", "it"], key="country2")

# Validation de la saisie
if keyword1 and keyword2:
    st.write(f"Scraping des résultats pour '{keyword1}' en {lang1}-{country1}...")
    results1 = scrape_serp(keyword1, lang=lang1, country=country1)
    
    st.write(f"Scraping des résultats pour '{keyword2}' en {lang2}-{country2}...")
    results2 = scrape_serp(keyword2, lang=lang2, country=country2)
    
    # Affichage des résultats
    st.write(f"Top 100 SERP pour {keyword1} en {lang1}-{country1} :")
    st.write(results1)
    
    st.write(f"Top 100 SERP pour {keyword2} en {lang2}-{country2} :")
    st.write(results2)
    
    # Calcul des URL et des domaines en commun
    common_urls = set(results1) & set(results2)
    common_domains = set([url.split('/')[2] for url in results1]) & set([url.split('/')[2] for url in results2])
    
    st.write(f"Nombre d'URLs en commun : {len(common_urls)}")
    st.write(f"Nombre de domaines en commun : {len(common_domains)}")
    
    # Graphique des changements et similarité
    # ... ici on peut ajouter la logique de comparaison entre SERPs et l'affichage avec Plotly
    
    # Exemple de calcul du taux de similarité
    similarity_rate = len(common_urls) / min(len(results1), len(results2)) * 100
    st.write(f"Taux de similarité entre les SERPs : {similarity_rate:.2f}%")
