import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry

# Fonction pour scraper les SERPs
def scrape_serp(query, lang="fr", region="FR"):
    url = f"https://www.google.{region}/search?q={query}&hl={lang}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a')
        if title and link:
            results.append({
                'title': title.text,
                'url': link['href']
            })
    
    return results

# Fonction pour analyser les SERPs
def analyze_serps(results1, results2):
    urls1 = {result['url'] for result in results1}
    urls2 = {result['url'] for result in results2}
    
    common_urls = urls1.intersection(urls2)
    common_domains = {url.split('/')[2] for url in common_urls}
    
    similarity_rate = (len(common_urls) / min(len(urls1), len(urls2))) * 100 if min(len(urls1), len(urls2)) > 0 else 0
    
    metrics = {
        'new': len(urls2 - urls1),
        'improved': len(common_urls - urls1),
        'declined': len(urls1 - urls2),
        'lost': len(urls1 - common_urls)
    }
    
    return {
        'common_urls': common_urls,
        'common_domains': common_domains,
        'similarity_rate': similarity_rate,
        'metrics': metrics
    }

# Obtenir toutes les langues et pays disponibles
lang_options = {
    'Afar': 'aa', 'Abkhazian': 'ab', 'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am',
    'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Azerbaijani': 'az', 'Bashkir': 'ba',
    'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg',
    'Catalan': 'ca', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl',
    'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Faroese': 'fo', 'Fijian': 'fj',
    'Finnish': 'fi', 'French': 'fr', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de',
    'Greek': 'el', 'Guarani': 'gn', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha',
    'Hebrew': 'iw', 'Hindi': 'hi', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig',
    'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv',
    'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Korean': 'ko', 'Kurdish (Kurmanji)': 'ku',
    'Kyrgyz': 'ky', 'Lao': 'lo', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb',
    'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt',
    'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Norwegian': 'no',
    'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa',
    'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr',
    'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk',
    'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw',
    'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te',
    'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz',
    'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo',
    'Zulu': 'zu'
}

country_options = {country.name: country.alpha_2 for country in pycountry.countries}

# Pré-sélectionner "fr" pour le pays du premier mot-clé
default_country = "FR"

# Interface utilisateur
st.title("Outil d'analyse de SERP")
col1, col2 = st.columns(2)

with col1:
    st.header("Mot-clé 1")
    keyword1 = st.text_input("Entrez le mot-clé 1")
    lang1 = st.selectbox("Langue", options=list(lang_options.keys()), index=list(lang_options.keys()).index("French"))
    country1 = st.selectbox("Pays", options=list(country_options.keys()), index=list(country_options.values()).index(default_country))

with col2:
    st.header("Mot-clé 2")
    keyword2 = st.text_input("Entrez le mot-clé 2")
    lang2 = st.selectbox("Langue", options=list(lang_options.keys()))
    country2 = st.selectbox("Pays", options=list(country_options.keys()))

if st.button("Analyser"):
    if keyword1 and keyword2:
        results1 = scrape_serp(keyword1, lang=lang_options[lang1], region=country_options[country1])
        results2 = scrape_serp(keyword2, lang=lang_options[lang2], region=country_options[country2])
        
        if results1 and results2:
            analysis = analyze_serps(results1, results2)
            
            st.subheader("Résultats de l'analyse")
            st.write(f"Taux de similarité : {analysis['similarity_rate']:.2f}%")
            st.write(f"URLs communes : {len(analysis['common_urls'])}")
            st.write(f"Domaines communs : {len(analysis['common_domains'])}")
            st.write(f"Nouvelles URLs : {analysis['metrics']['new']}")
            st.write(f"URLs améliorées : {analysis['metrics']['improved']}")
            st.write(f"URLs déclinées : {analysis['metrics']['declined']}")
            st.write(f"URLs perdues : {analysis['metrics']['lost']}")
            
            # Graphique de la comparaison des SERPs (à implémenter)
            st.write("Graphique des évolutions entre les SERPs (à venir)...")
        else:
            st.error("Aucun résultat trouvé pour l'un des mots-clés.")
    else:
        st.warning("Veuillez entrer les deux mots-clés.")

