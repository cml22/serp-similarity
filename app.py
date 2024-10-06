import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.metrics import jaccard_score
import numpy as np

# Function to scrape Google SERPs
def scrape_serp(query, lang="en", location="us"):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=10&hl={lang}&gl={location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Error: Unable to fetch data from Google (status code: {response.status_code})"
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for g in soup.find_all('div', class_='g'):
        title_element = g.find('h3')
        link_element = g.find('a')

        if title_element and link_element:
            title = title_element.text
            link = link_element['href']
            results.append((title, link))
    
    if not results:
        return "No results found or blocked by Google."

    return results

def calculate_similarity(serp1, serp2):
    links1 = [link for _, link in serp1]
    links2 = [link for _, link in serp2]
    
    all_links = list(set(links1 + links2))
    vec1 = [1 if link in links1 else 0 for link in all_links]
    vec2 = [1 if link in links2 else 0 for link in all_links]
    
    return jaccard_score(vec1, vec2)

st.title('SERP Similarity Tool')

# Inputs for two keywords
keyword1 = st.text_input("Enter the first keyword:")
keyword2 = st.text_input("Enter the second keyword:")

# Inputs for language and location (for each keyword)
lang1 = st.selectbox("Select language for keyword 1", ["en", "fr", "es", "de"])
location1 = st.selectbox("Select location for keyword 1", ["us", "fr", "es", "de"])

lang2 = st.selectbox("Select language for keyword 2", ["en", "fr", "es", "de"])
location2 = st.selectbox("Select location for keyword 2", ["us", "fr", "es", "de"])

if st.button('Compare SERPs'):
    if keyword1 and keyword2:
        st.write(f"Scraping SERPs for '{keyword1}' and '{keyword2}'...")

        serp1 = scrape_serp(keyword1, lang=lang1, location=location1)
        serp2 = scrape_serp(keyword2, lang=lang2, location=location2)
        
        if isinstance(serp1, str):
            st.write(f"Error for keyword 1: {serp1}")
        elif isinstance(serp2, str):
            st.write(f"Error for keyword 2: {serp2}")
        else:
            similarity_score = calculate_similarity(serp1, serp2)
            st.write(f"Similarity Score: {similarity_score * 100:.2f}/100")

            st.subheader(f"Results for {keyword1}")
            for title, link in serp1:
                st.write(f"- {title}: {link}")
            
            st.subheader(f"Results for {keyword2}")
            for title, link in serp2:
                st.write(f"- {title}: {link}")
    else:
        st.write("Please enter both keywords.")
