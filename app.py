import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity

# Fonction pour scraper les résultats SERP
def scrape_serp(query, lang, location):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    url = f"https://www.google.com/search?q={query}&hl={lang}&gl={location}&num=100"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    results = []
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        results.append(g.text)

    return results

# Fonction pour comparer les SERPs
def compare_serps(serp1, serp2):
    common_urls = set(serp1) & set(serp2)
    common_domains = set([url.split('/')[2] for url in serp1]) & set([url.split('/')[2] for url in serp2])
    
    # Calcul des metrics (nouvelles, améliorées, perdues)
    improved = set(serp2) - set(serp1)
    lost = set(serp1) - set(serp2)
    new_urls = improved
    declined_urls = lost
    
    return {
        'common_urls': len(common_urls),
        'common_domains': len(common_domains),
        'new': len(new_urls),
        'improved': len(improved),
        'lost': len(lost),
        'declined': len(declined_urls)
    }

# Fonction pour visualiser avec des flèches
def plot_evolution(serp1, serp2):
    fig = go.Figure()
    
    for i, url in enumerate(serp1[:10]):
        if url in serp2[:10]:
            j = serp2.index(url)
            fig.add_trace(go.Scatter(x=[0, 1], y=[i, j], mode='lines', line=dict(color='green', width=2), name=url))

    fig.update_layout(
        title='SERP Evolution (Top 10)',
        xaxis_title="SERP 1",
        yaxis_title="SERP 2",
        showlegend=False
    )
    return fig

# Interface Streamlit
st.title("SERP Similarity Tool")

col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Mot-clé 1")
    lang1 = st.selectbox("Langue", options=["fr", "en", "es", "de", "it"])
    location1 = st.text_input("Location", value="FR")
    
with col2:
    keyword2 = st.text_input("Mot-clé 2")
    lang2 = st.selectbox("Langue", options=["fr", "en", "es", "de", "it"])
    location2 = st.text_input("Location", value="FR")

if st.button("Analyser"):
    serp1 = scrape_serp(keyword1, lang1, location1)
    serp2 = scrape_serp(keyword2, lang2, location2)
    
    # Comparaison des SERPs
    result = compare_serps(serp1, serp2)
    
    st.write(f"Nombre d'URLs en commun : {result['common_urls']}")
    st.write(f"Nombre de domaines en commun : {result['common_domains']}")
    st.write(f"URLs nouvelles : {result['new']}")
    st.write(f"URLs améliorées : {result['improved']}")
    st.write(f"URLs perdues : {result['lost']}")
    st.write(f"URLs déclinées : {result['declined']}")
    
    # Visualisation graphique des flèches
    st.plotly_chart(plot_evolution(serp1, serp2))
