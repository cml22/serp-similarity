import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Set up page configuration
st.set_page_config(page_title="SERP Similarity Analysis", layout="centered")

def scrape_serp(keyword, language, country):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Error retrieving results.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Title not found"
            results.append((link['href'], title))

    return results

def analyze_titles(results, keyword1, keyword2):
    counts = {
        "common_keyword1": 0,
        "common_keyword2": 0,
        "common_both": 0,
    }

    urls_common = {url: title for url, title in results[0]}  # SERP 1
    urls_non_common = {url: title for url, title in results[1]}  # SERP 2

    for url, title in urls_common.items():
        if keyword1.lower() in title.lower() and keyword2.lower() in title.lower():
            counts["common_both"] += 1
        elif keyword1.lower() in title.lower():
            counts["common_keyword1"] += 1
        elif keyword2.lower() in title.lower():
            counts["common_keyword2"] += 1

    return counts

def calculate_similarity(results1, results2):
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    non_common_urls1 = set(urls1.keys()) - common
