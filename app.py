import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_serp(keyword, lang, country):
    # Remplacez ceci par l'URL de votre moteur de recherche et les paramètres appropriés
    url = f"https://www.google.com/search?q={keyword}&hl={lang}&gl={country}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Ici, nous supposons que les résultats SERP sont dans des balises <h3>
    results = soup.find_all("h3")
    return [result.get_text() for result in results]

def main():
    st.title("Analyse de Similarité SERP")
    
    # Entrée pour les mots-clés
    keyword1 = st.text_input("Entrez le mot-clé 1")
    keyword2 = st.text_input("Entrez le mot-clé 2")

    # Sélection des langues
    languages = [
        ('fr', 'Français'),
        ('en', 'Anglais'),
        ('es', 'Espagnol'),
        ('de', 'Allemand'),
        ('it', 'Italien'),
        ('pt', 'Portugais'),
        ('ru', 'Russe'),
        ('ja', 'Japonais'),
        ('zh', 'Chinois'),
        # Ajoutez d'autres langues selon vos besoins
    ]
    
    selected_lang1 = st.selectbox("Langue du mot-clé 1", options=languages, format_func=lambda x: x[1])
    selected_lang2 = st.selectbox("Langue du mot-clé 2", options=languages, format_func=lambda x: x[1])

    # Sélection des pays
    countries = [
        ('FR', 'France'),
        ('US', 'États-Unis'),
        ('ES', 'Espagne'),
        ('DE', 'Allemagne'),
        ('IT', 'Italie'),
        ('PT', 'Portugal'),
        ('RU', 'Russie'),
        ('JP', 'Japon'),
        ('CN', 'Chine'),
        # Ajoutez d'autres pays selon vos besoins
    ]
    
    selected_country1 = st.selectbox("Pays du mot-clé 1", options=countries, format_func=lambda x: x[1])
    selected_country2 = st.selectbox("Pays du mot-clé 2", options=countries, format_func=lambda x: x[1])

    if st.button("Analyser"):
        if keyword1 and keyword2:
            # Récupération des résultats SERP
            serp1 = fetch_serp(keyword1, selected_lang1[0], selected_country1[0])
            serp2 = fetch_serp(keyword2, selected_lang2[0], selected_country2[0])

            # Comparaison des résultats
            common_urls = set(serp1).intersection(set(serp2))
            similarity_rate = len(common_urls) / max(len(serp1), len(serp2)) * 100 if max(len(serp1), len(serp2)) > 0 else 0
            
            st.write(f"Taux de similarité : {similarity_rate:.2f}%")
            st.write(f"URLs communes : {len(common_urls)}")
            
            st.subheader(f"Top résultats pour '{keyword1}'")
            for url in serp1:
                st.write(url)
                
            st.subheader(f"Top résultats pour '{keyword2}'")
            for url in serp2:
                st.write(url)

            st.subheader("URLs communes")
            for url in common_urls:
                st.write(url)
        else:
            st.error("Veuillez entrer les deux mots-clés pour l'analyse.")

if __name__ == "__main__":
    main()
