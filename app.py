import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry

# Fonction pour obtenir les résultats de recherche
def get_serp_results(keyword, lang, country):
    url = f"https://www.google.com/search?q={keyword}&hl={lang}&gl={country}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # Modifier le sélecteur selon la structure de Google SERP
    for item in soup.select('.BVG0Nb'):
        link = item.find('a', href=True)
        if link:
            results.append(link['href'])

    return results

# Titre de l'application
st.title("Analyse de Similarité SERP")

# Saisies des mots-clés
keyword1 = st.text_input("Entrez le mot-clé 1", "")
keyword2 = st.text_input("Entrez le mot-clé 2", "")

# Sélecteurs de langue et pays
languages = [(lang.alpha_2, lang.name) for lang in pycountry.languages]
countries = [(country.alpha_2, country.name) for country in pycountry.countries]

selected_lang1 = st.selectbox("Langue du mot-clé 1", options=[lang[1] for lang in languages])
selected_country1 = st.selectbox("Pays du mot-clé 1", options=[country[1] for country in countries])

selected_lang2 = st.selectbox("Langue du mot-clé 2", options=[lang[1] for lang in languages])
selected_country2 = st.selectbox("Pays du mot-clé 2", options=[country[1] for country in countries])

# Traitement des résultats
if st.button("Analyser"):
    lang1_code = next(lang[0] for lang in languages if lang[1] == selected_lang1)
    country1_code = next(country[0] for country in countries if country[1] == selected_country1)
    
    lang2_code = next(lang[0] for lang in languages if lang[1] == selected_lang2)
    country2_code = next(country[0] for country in countries if country[1] == selected_country2)
    
    results1 = get_serp_results(keyword1, lang1_code, country1_code)
    results2 = get_serp_results(keyword2, lang2_code, country2_code)

    if results1 is None or results2 is None:
        st.error("Erreur lors de la récupération des résultats.")
    else:
        # Affichage des résultats
        st.subheader("Résultats de l'analyse")
        
        similarity_count = len(set(results1) & set(results2))
        total_count = max(len(results1), len(results2))

        st.write(f"Taux de similarité : {similarity_count / total_count * 100:.2f}%")
        st.write(f"URLs communes : {similarity_count}")

        # Affichage des résultats
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Top 10 Mot-clé 1: {keyword1}")
            for url in results1[:10]:
                st.markdown(f"[{url}]({url})")

        with col2:
            st.subheader(f"Top 10 Mot-clé 2: {keyword2}")
            for url in results2[:10]:
                st.markdown(f"[{url}]({url})")

        # Affichage des URLs communes
        common_urls = set(results1) & set(results2)
        st.subheader("URLs communes")
        for url in common_urls:
            st.markdown(f"[{url}]({url})")
