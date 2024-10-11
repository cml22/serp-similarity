import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from requests.exceptions import ConnectionError, Timeout

# Configurer la page Streamlit
st.set_page_config(page_title="SERP Similarity Analysis", layout="centered")

# Fonction pour scraper les résultats de Google SERP
def scrape_serp(keyword, language, country):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)  # Timeout after 10 seconds
        response.raise_for_status()  # Raise an exception for bad responses
    except ConnectionError:
        st.error("Erreur de connexion. Impossible d'accéder à Google.")
        return []
    except Timeout:
        st.error("Délai dépassé. Google a mis trop de temps à répondre.")
        return []
    except requests.HTTPError as e:
        st.error(f"Erreur HTTP : {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Titre non trouvé"
            results.append((link['href'], title))

    return results

# Interface Streamlit
st.title("SERP Similarity Tool")

# Inputs des mots-clés
keyword1 = st.text_input("Entrez le premier mot-clé", "digital marketing")
keyword2 = st.text_input("Entrez le second mot-clé", "online marketing")

# Sélection de la langue et du pays
language1 = st.selectbox("Langue pour le premier mot-clé", ["en", "fr", "de"])
language2 = st.selectbox("Langue pour le second mot-clé", ["en", "fr", "de"])
country1 = st.selectbox("Pays pour le premier mot-clé", ["com", "fr", "de", "co.uk"])
country2 = st.selectbox("Pays pour le second mot-clé", ["com", "fr", "de", "co.uk"])

# Scraping des SERP pour les deux mots-clés
if st.button("Analyser la similarité des SERP"):
    with st.spinner('Scraping des résultats...'):
        results_keyword1 = scrape_serp(keyword1, language1, country1)
        results_keyword2 = scrape_serp(keyword2, language2, country2)

    # Vérification des résultats
    if results_keyword1 and results_keyword2:
        st.success("Scraping terminé avec succès!")

        # Affichage des résultats
        st.subheader(f"Résultats pour : {keyword1}")
        for link, title in results_keyword1:
            st.write(f"[{title}]({link})")

        st.subheader(f"Résultats pour : {keyword2}")
        for link, title in results_keyword2:
            st.write(f"[{title}]({link})")

        # Comparaison des URLs communes
        urls_keyword1 = {link for link, _ in results_keyword1}
        urls_keyword2 = {link for link, _ in results_keyword2}

        common_urls = urls_keyword1.intersection(urls_keyword2)
        st.subheader("URLs communes entre les deux SERP")
        if common_urls:
            for url in common_urls:
                st.write(f"[{url}]({url})")
        else:
            st.write("Aucune URL commune trouvée.")
    else:
        st.error("Échec du scraping ou pas de résultats pour un ou les deux mots-clés.")

