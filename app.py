import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry
import langcodes

# Fonction pour scraper les SERP en fonction de la langue et la localisation
def scrape_serp(query, lang="en", country="us"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": f"{lang}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    
    url = f"https://www.google.com/search?q={query}&hl={lang}&gl={country}&num=100"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        for g in soup.find_all('div', class_='g'):
            link = g.find('a')['href']
            results.append(link)
        
        return results
    
    except requests.RequestException as e:
        st.error(f"Erreur lors du scraping pour '{query}': {e}")
        return []

# Récupérer toutes les langues et tous les pays
lang_options = {langcodes.get(i).language_name(): i for i in langcodes.LANGUAGES}
country_options = {country.name: country.alpha_2 for country in pycountry.countries}

# Interface utilisateur en deux colonnes
st.title("SERP Similarity Analysis")

col1, col2 = st.columns(2)

# Colonne de gauche pour le mot-clé 1
with col1:
    st.header("Mot-clé 1")
    keyword1 = st.text_input("Mot-clé 1", key="keyword1")
    lang1 = st.selectbox("Langue pour le premier mot-clé", options=list(lang_options.keys()), key="lang1")
    country1 = st.selectbox("Pays pour le premier mot-clé", options=list(country_options.keys()), key="country1")

# Colonne de droite pour le mot-clé 2
with col2:
    st.header("Mot-clé 2")
    keyword2 = st.text_input("Mot-clé 2", key="keyword2")
    lang2 = st.selectbox("Langue pour le deuxième mot-clé", options=list(lang_options.keys()), key="lang2")
    country2 = st.selectbox("Pays pour le deuxième mot-clé", options=list(country_options.keys()), key="country2")

# Bouton pour lancer l'analyse
if st.button("Analyser"):
    if keyword1 and keyword2:
        results1 = scrape_serp(keyword1, lang=lang_options[lang1], country=country_options[country1])
        results2 = scrape_serp(keyword2, lang=lang_options[lang2], country=country_options[country2])
        
        # Calcul des métriques
        common_urls = set(results1) & set(results2)
        similarity_rate = (len(common_urls) / min(len(results1), len(results2))) * 100 if min(len(results1), len(results2)) > 0 else 0
        num_declined = len(set(results1) - common_urls)
        num_new = len(set(results2) - common_urls)
        
        # Afficher les résultats
        st.subheader("Résultats")
        st.write(f"Nombre d'URLs communes: {len(common_urls)}")
        st.write(f"Taux de similarité: {similarity_rate:.2f}%")
        st.write(f"Nouvelles URLs: {num_new}")
        st.write(f"URLs déclinées: {num_declined}")

        # Créer un DataFrame pour les résultats
        df_results = pd.DataFrame({
            "URL": list(common_urls),
            "Mot-clé 1 Rank": [results1.index(url) + 1 if url in results1 else None for url in common_urls],
            "Mot-clé 2 Rank": [results2.index(url) + 1 if url in results2 else None for url in common_urls],
        })

        # Afficher les résultats dans un tableau
        st.dataframe(df_results)

# Ajouter une section d'explications ou d'aide si nécessaire
st.sidebar.info("Entrez deux mots-clés, sélectionnez les langues et pays, puis cliquez sur 'Analyser' pour obtenir les résultats.")
