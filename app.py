import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_serp(keyword, language, country):
    # Construction de l'URL de recherche
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"
    
    # En-têtes pour simuler un navigateur
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
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
            results.append(link['href'])
    
    return results

# Interface utilisateur avec Streamlit
st.title("Analyse de Similarité SERP")

# Entrée des mots-clés
keyword1 = st.text_input("Mot-clé 1 :")
keyword2 = st.text_input("Mot-clé 2 :")

# Sélection de la langue et du pays
language = st.selectbox("Langue :", ["fr", "en", "es", "de", "it", "pt"])
country = st.selectbox("Pays :", ["fr", "gb", "us", "ca", "es", "de", "it", "pt"])

if st.button("Analyser"):
    if keyword1 and keyword2:
        st.write(f"**Résultats de l'analyse SERP**")
        st.write(f"Mot-clé 1 : {keyword1}")
        st.write(f"Mot-clé 2 : {keyword2}")
        st.write(f"Langue/Pays : {language}/{country}")
        
        # Scraper les résultats pour les deux mots-clés
        results_keyword1 = scrape_serp(keyword1, language, country)
        results_keyword2 = scrape_serp(keyword2, language, country)
        
        st.write("**SERP pour le Mot-clé 1**")
        for result in results_keyword1:
            st.write(result)
        
        st.write("**SERP pour le Mot-clé 2**")
        for result in results_keyword2:
            st.write(result)
    else:
        st.error("Veuillez entrer les deux mots-clés.")
