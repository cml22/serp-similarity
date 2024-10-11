import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry
import langcodes

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

# Obtenir les noms complets des langues et des pays
languages = [(lang.alpha_2, lang.name) for lang in langcodes.Language]
countries = [(country.alpha_2, country.name) for country in pycountry.countries]

st.title("Analyse de Similarité SERP")

# Entrée des mots-clés
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Entrez le mot-clé 1", "")
    lang1 = st.selectbox("Langue du mot-clé 1", options=[name for _, name in languages])
    country1 = st.selectbox("Pays du mot-clé 1", options=[name for _, name in countries])

with col2:
    keyword2 = st.text_input("Entrez le mot-clé 2", "")
    lang2 = st.selectbox("Langue du mot-clé 2", options=[name for _, name in languages])
    country2 = st.selectbox("Pays du mot-clé 2", options=[name for _, name in countries])

# Bouton pour lancer l'analyse
if st.button("Analyser la similarité"):
    if keyword1 and keyword2:
        # Convertir les noms de langue et pays en codes
        lang1_code = [code for code, name in languages if name == lang1][0]
        lang2_code = [code for code, name in languages if name == lang2][0]
        country1_code = [code for code, name in countries if name == country1][0]
        country2_code = [code for code, name in countries if name == country2][0]

        # Scraper les SERPs
        results1 = scrape_serp(keyword1, lang1_code, country1_code)
        results2 = scrape_serp(keyword2, lang2_code, country2_code)

        # Comparer les résultats
        common_urls = set(results1) & set(results2)
        unique_to_keyword1 = set(results1) - set(results2)
        unique_to_keyword2 = set(results2) - set(results1)

        # Afficher les résultats
        st.write("### Résultats pour le mot-clé 1")
        st.write(results1)
        
        st.write("### Résultats pour le mot-clé 2")
        st.write(results2)

        st.write("### URLs communes")
        st.write(list(common_urls))

        st.write("### URLs uniques à mot-clé 1")
        st.write(list(unique_to_keyword1))

        st.write("### URLs uniques à mot-clé 2")
        st.write(list(unique_to_keyword2))
    else:
        st.error("Veuillez entrer les deux mots-clés.")
