import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import langcodes
import pycountry
import matplotlib.pyplot as plt

# Fonction pour récupérer les résultats du SERP
def scrape_serp(query, lang="en", region="us"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = f"https://www.google.{region}/search?q={query}&hl={lang}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')  # Modifier en fonction de la structure HTML de Google
        urls = [result.find('a')['href'] for result in results if result.find('a')]
        return urls
    else:
        return []

# Interface utilisateur Streamlit
st.title("Analyse de SERP Similarity")
st.write("Entrez deux mots-clés pour analyser leur similarité dans les résultats de recherche.")

# Options de langue et de pays
lang_options = {langcodes.get(i).language_name(): i for i in langcodes.LANGUAGES.keys()}
country_options = {country.name: country.alpha_2 for country in pycountry.countries}

# Colonne de gauche pour le premier mot-clé
st.header("Mot-clé 1")
keyword1 = st.text_input("Entrez le premier mot-clé")
lang1 = st.selectbox("Langue", options=list(lang_options.keys()), index=list(lang_options.keys()).index("French"))
country1 = st.selectbox("Pays", options=list(country_options.keys()), index=list(country_options.keys()).index("France"))

# Colonne de droite pour le deuxième mot-clé
st.header("Mot-clé 2")
keyword2 = st.text_input("Entrez le deuxième mot-clé")
lang2 = st.selectbox("Langue", options=list(lang_options.keys()), index=list(lang_options.keys()).index("French"))
country2 = st.selectbox("Pays", options=list(country_options.keys()), index=list(country_options.keys()).index("France"))

if st.button("Analyser"):
    # Récupérer les résultats SERP pour chaque mot-clé
    region1 = country_options[country1]
    region2 = country_options[country2]

    results1 = scrape_serp(keyword1, lang=lang_options[lang1], region=region1)
    results2 = scrape_serp(keyword2, lang=lang_options[lang2], region=region2)

    # Analyser les résultats
    common_urls = set(results1) & set(results2)
    unique_urls1 = set(results1) - set(results2)
    unique_urls2 = set(results2) - set(results1)

    # Calculer les métriques
    similarity_rate = (len(common_urls) / min(len(results1), len(results2))) * 100 if min(len(results1), len(results2)) > 0 else 0
    declined_urls = len(unique_urls1)
    new_urls = len(unique_urls2)

    # Afficher les résultats
    st.write(f"Taux d'URLs communes : {similarity_rate:.2f}%")
    st.write(f"URLs déclinées pour le mot-clé 1 : {declined_urls}")
    st.write(f"Nouvelles URLs pour le mot-clé 2 : {new_urls}")

    # Graphique des évolutions entre les SERPs
    if len(results1) > 0 and len(results2) > 0:
        st.write("Graphique des évolutions entre les SERPs (à venir)...")
        # Code pour créer un graphique avec Matplotlib ici

