import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import matplotlib.pyplot as plt

# Must be the first Streamlit command
st.set_page_config(page_title="SERP Similarity Analysis", layout="centered")

# Purpose of the tool
st.write("## Purpose")
st.write("This tool compares the similarity of SERPs (Search Engine Results Pages) for two different keywords. It helps determine whether a new page should be created or if an existing page should be optimized based on the overlap of search results.")

# Disclaimer
st.info("**Disclaimer:** Optimizing titles alone is not enough for SEO. Ensure you're addressing other key factors like content quality, backlinks, and user experience.")

# Backlink to Charles Migaud's site
st.markdown('Tool made with ❤️ by [Charles Migaud](https://charles-migaud.fr)')

def scrape_serp(keyword, language, country, num_results):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.com/search?q={query}&hl={language}&gl={country}&num={num_results}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Error while fetching results.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g')[:num_results]:
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Title not found"
            results.append((link['href'], title))

    return results

def calculate_similarity(results1, results2):
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    # Initialize the similarity rates for different counts
    similarity_rates = {}
    for num_results in range(10, 101, 10):
        common_urls = set(list(urls1.keys())[:num_results]).intersection(set(list(urls2.keys())[:num_results]))
        total_urls = len(set(list(urls1.keys())[:num_results]).union(set(list(urls2.keys())[:num_results])))
        similarity_rate_url = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0
        similarity_rates[num_results] = similarity_rate_url

    return similarity_rates

# User Interface with Streamlit
st.title("SERP Similarity Analysis")
st.markdown("---")

# Input fields for keywords
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Enter Keyword 1:", placeholder="Ex: vps")
    language1 = st.selectbox("Language (Keyword 1):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country1 = st.selectbox("Country (Keyword 1):", ["FR", "GB", "US", "CA", "ES", "DE", "IT", "PT", "PL", "MA", "SN", "TN"])

with col2:
    keyword2 = st.text_input("Enter Keyword 2:", placeholder="Ex: virtual private server")
    language2 = st.selectbox("Language (Keyword 2):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country2 = st.selectbox("Country (Keyword 2):", ["FR", "GB", "US", "CA", "ES", "DE", "IT", "PT", "PL", "MA", "SN", "TN"])

# Slider to choose the number of URLs to scrape
num_urls = st.slider("Select the number of URLs to scrape (between 10 and 100):", min_value=10, max_value=100, value=10, step=10)

st.markdown("---")

if st.button("Analyze"):
    if keyword1 and keyword2:
        # Scrape the results for both keywords
        results_keyword1 = scrape_serp(keyword1, language1, country1, num_urls)
        results_keyword2 = scrape_serp(keyword2, language2, country2, num_urls)

        # Calculate similarity rates for different numbers of results
        similarity_rates = calculate_similarity(results_keyword1, results_keyword2)

        # Display results
        for num, rate in similarity_rates.items():
            st.write(f"**Similarity Rate for Top {num} URLs: {rate:.2f}%**")

        # Plot similarity rates
        fig, ax = plt.subplots()
        ax.plot(list(similarity_rates.keys()), list(similarity_rates.values()), marker='o')
        ax.set_xlabel("Number of URLs Scraped")
        ax.set_ylabel("Similarity Rate (%)")
        ax.set_title("SERP Similarity Rate by Number of URLs")
        ax.grid()
        st.pyplot(fig)

        # Further analysis can be added here...
    else:
        st.error("Please enter both keywords.")
