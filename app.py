import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
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
    
    # Pré-sélection des options pour le mot-clé 1
    lang1 = st.selectbox("Langue", options=list(lang_options.keys()), index=list(lang_options.keys()).index("French"))
    country1 = st.selectbox("Pays", options=list(country_options.keys()), index=list(country_options.keys()).index("France"))

# Colonne pour le mot-clé 2
with col2:
    st.header("Mot-clé 2")
    keyword2 = st.text_input("Entrez le mot-clé 2")
    
    # Pré-sélection des mêmes options pour le mot-clé 2
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

    # Affichage des résultats des SERPs
    st.subheader("Top 10 Résultats pour le Mot-clé 1")
    for i, url in enumerate(results1[:10]):
        st.markdown(f"{i + 1}. [Lien]({url})")

    st.subheader("Top 10 Résultats pour le Mot-clé 2")
    for i, url in enumerate(results2[:10]):
        st.markdown(f"{i + 1}. [Lien]({url})")

    # Préparation des données pour le graphique
    top_results1 = results1[:10]
    top_results2 = results2[:10]
    url_mappings = {url: i + 1 for i, url in enumerate(top_results1)}
    url_mappings.update({url: -(i + 1) for i, url in enumerate(top_results2)})

    fig = go.Figure()

    for url, position in url_mappings.items():
        if position > 0:  # URL dans le top 10 du mot-clé 1
            fig.add_trace(go.Scatter(
                x=[1], 
                y=[position], 
                mode='markers+text', 
                text=[url],
                textposition='top center',
                marker=dict(size=10, color='blue'),
                name=keyword1
            ))
        else:  # URL dans le top 10 du mot-clé 2
            fig.add_trace(go.Scatter(
                x=[2], 
                y=[-position], 
                mode='markers+text', 
                text=[url],
                textposition='top center',
                marker=dict(size=10, color='orange'),
                name=keyword2
            ))

    # Flèches pour indiquer les changements de position
    for url in common_urls:
        pos1 = url_mappings.get(url)
        if pos1 > 0:  # Position dans le mot-clé 1
            pos2 = url_mappings.get(url)
            fig.add_annotation(
                x=1.5,
                y=pos1,
                ax=1,
                ay=pos1,
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor='gray'
            )
        elif pos1 < 0:  # Position dans le mot-clé 2
            pos2 = url_mappings.get(url)
            fig.add_annotation(
                x=1.5,
                y=-pos2,
                ax=2,
                ay=-pos2,
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor='gray'
            )

    fig.update_layout(
        title="Comparaison des SERPs",
        xaxis=dict(
            tickvals=[1, 2],
            ticktext=[keyword1, keyword2]
        ),
        yaxis=dict(
            title="Position",
            tickvals=list(range(-10, 1)),
            ticktext=[str(-i) for i in range(10, 0, -1)] + [str(i) for i in range(1, 11)]
        ),
        showlegend=False
    )

    st.plotly_chart(fig)
