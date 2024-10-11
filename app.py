import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import langcodes
import pycountry

# Fonction pour scraper le SERP
def scrape_serp(query, lang="en", region="us"):
    url = f"https://www.google.{region}/search?q={query}&hl={lang}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')
        if link:
            results.append(link['href'])
    return results

# Récupération des langues et pays
lang_options = {langcodes.get(i).language_name(): i for i in langcodes.LANGUAGES.keys()}
country_options = {country.name: country.alpha_2 for country in pycountry.countries}

# Interface utilisateur
st.title("Outil d'analyse de SERP")

# Colonne pour le mot-clé 1
col1, col2 = st.columns(2)

with col1:
    st.header("Mot-clé 1")
    keyword1 = st.text_input("Entrez le mot-clé 1")
    lang1 = st.selectbox("Langue", options=list(lang_options.keys()), index=list(lang_options.keys()).index("French"))
    country1 = st.selectbox("Pays", options=list(country_options.keys()), index=list(country_options.keys()).index("France"))

# Colonne pour le mot-clé 2
with col2:
    st.header("Mot-clé 2")
    keyword2 = st.text_input("Entrez le mot-clé 2")
    lang2 = st.selectbox("Langue", options=list(lang_options.keys()), index=list(lang_options.keys()).index("French"))
    country2 = st.selectbox("Pays", options=list(country_options.keys()), index=list(country_options.keys()).index("France"))

if st.button("Analyser"):
    # Scraper les SERPs
    results1 = scrape_serp(keyword1, lang=lang_options[lang1], region=country_options[country1])
    results2 = scrape_serp(keyword2, lang=lang_options[lang2], region=country_options[country2])

    # Analyser les résultats
    common_urls = set(results1) & set(results2)
    total_urls1 = len(results1)
    total_urls2 = len(results2)

    if total_urls1 > 0 and total_urls2 > 0:
        similarity_rate = len(common_urls) / min(total_urls1, total_urls2) * 100
    else:
        similarity_rate = 0

    st.write(f"URLs communes : {len(common_urls)}")
    st.write(f"Taux de similarité : {similarity_rate:.2f}%")
    
    # Graphique des évolutions entre les SERPs
    if len(results1) > 0 and len(results2) > 0:
        fig, ax = plt.subplots()
        ax.barh(range(len(results1)), [1]*len(results1), color='blue', label=keyword1)
        ax.barh(range(len(results2)), [1]*len(results2), color='orange', label=keyword2)
        ax.set_yticks(range(max(len(results1), len(results2))))
        ax.set_yticklabels(results1 + results2)
        ax.legend()
        plt.title("Graphique des SERPs")
        st.pyplot(fig)
    else:
        st.write("Pas de résultats à afficher.")
