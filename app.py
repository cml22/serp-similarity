import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import langcodes

def scrape_serp(query, lang="en", region="fr"):
    # Construction de l'URL de recherche
    url = f"https://www.google.{region}/search?q={query}&hl={lang}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Extraction des URLs des résultats de recherche
    for item in soup.find_all('h3'):
        parent = item.find_parent("a")
        if parent and 'href' in parent.attrs:
            results.append(parent['href'])

    return results

st.title("Outil d'analyse de SERP")

# Configuration pour le mot-clé 1
st.header("Mot-clé 1")
query1 = st.text_input("Entrez le mot-clé 1")
lang1 = st.selectbox("Langue", options=list(langcodes.LANGUAGES.values()), index=list(langcodes.LANGUAGES.values()).index("french"))
region1 = st.selectbox("Pays", options=["fr", "us", "uk", "de", "es"], index=0)

# Configuration pour le mot-clé 2
st.header("Mot-clé 2")
query2 = st.text_input("Entrez le mot-clé 2")
lang2 = st.selectbox("Langue", options=list(langcodes.LANGUAGES.values()), index=list(langcodes.LANGUAGES.values()).index("french"))
region2 = st.selectbox("Pays", options=["fr", "us", "uk", "de", "es"], index=0)

# Bouton pour effectuer l'analyse
if st.button("Analyser"):
    if query1 and query2:
        # Scraping des SERP
        results1 = scrape_serp(query1, lang=lang1, region=region1)
        results2 = scrape_serp(query2, lang=lang2, region=region2)

        # Calcul des URLs communes
        set_results1 = set(results1)
        set_results2 = set(results2)
        common_urls = set_results1 & set_results2
        total_urls = len(set_results1 | set_results2)
        similarity_rate = (len(common_urls) / total_urls * 100) if total_urls > 0 else 0

        # Affichage des résultats
        st.subheader(f"Résultats pour '{query1}'")
        st.write(pd.DataFrame(results1, columns=["URLs"]))

        st.subheader(f"Résultats pour '{query2}'")
        st.write(pd.DataFrame(results2, columns=["URLs"]))

        st.subheader("Taux d'URLs communes")
        st.write(f"Nombre d'URLs communes: {len(common_urls)}")
        st.write(f"Taux de similarité: {similarity_rate:.2f}%")

        # Affichage des URLs communes
        if common_urls:
            st.subheader("URLs communes")
            st.write(pd.DataFrame(list(common_urls), columns=["URLs"]))
        else:
            st.write("Aucune URL commune trouvée.")

        # Compte des domaines
        domain_counts = Counter(url.split('/')[2] for url in results1 + results2)
        common_domains = set(domain for domain, count in domain_counts.items() if count > 1)
        st.write(f"Domaines communs : {len(common_domains)}")
        st.write(pd.DataFrame(list(common_domains), columns=["Domaines"]))

        # Nouvelles URLs, URLs améliorées, URLs déclinées, URLs perdues
        new_urls = set_results2 - set_results1
        improved_urls = {url for url in results2 if url in set_results1 and results2.index(url) < results1.index(url)}
        declined_urls = {url for url in results1 if url in set_results2 and results1.index(url) < results2.index(url)}
        lost_urls = set_results1 - set_results2

        st.write(f"Nouvelles URLs : {len(new_urls)}")
        st.write(f"URLs améliorées : {len(improved_urls)}")
        st.write(f"URLs déclinées : {len(declined_urls)}")
        st.write(f"URLs perdues : {len(lost_urls)}")
    else:
        st.warning("Veuillez entrer les deux mots-clés pour effectuer l'analyse.")
