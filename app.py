import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.metrics import jaccard_score
import numpy as np

# Function to scrape Google SERPs
def scrape_serp(query, lang="en", location="us"):
    # Adjusted Google search URL
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

    # Google uses different classes for results. We attempt multiple classes to ensure we extract them correctly.
    for g in soup.find_all('div', class_='g'):
        title_element = g.find('h3')
        link_element = g.find('a')

        # Ensure the title and link exist
        if title_element and link_element:
            title = title_element.text
            link = link_element['href']
            results.append((title, link))
    
    if not results:
        return "No results found or blocked by Google."

    return results

# Function to calculate the similarity score
def calculate_similarity(serp1, serp2):
    links1 = [link for _, link in serp1]
    links2 = [link for _, link in serp2]
    
    all_links = list(set(links1 + links2))
    vec1 = [1 if link in links1 else 0 for link in all_links]
    vec2 = [1 if link in links2 else 0 for link in all_links]
    
    return jaccard_score(vec1, vec2)

# Streamlit app interface
st.title('SERP Similarity Tool')

# Inputs for two keywords
keyword1 = st.text_input("Enter the first
