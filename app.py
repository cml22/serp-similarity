import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_serp(keyword, language, country):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.{country}/search?q={query}&hl={language}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
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
            results.append((link['href'], link.get_text()))

    return results

def calculate_similarity(results1, results2):
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    similarity_rate = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0

    return list(common_urls), similarity_rate, len(common_urls), urls1, urls2

def analyze_titles(results1, results2, keyword1, keyword2):
    titles1 = [result[1] for result in results1]
    titles2 = [result[1] for result in results2]

    count_keyword1 = sum(keyword1.lower() in title.lower() for title in titles1)
    count_keyword2 = sum(keyword2.lower() in title.lower() for title in titles1)
    count_both_keywords = sum(keyword1.lower() in title.lower() and keyword2.lower() in title.lower() for title in titles1)

    return count_keyword1, count_keyword2, count_both_keywords

st.title("SERP Similarity Analysis Tool")

col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Keyword 1:")
    language1 = st.selectbox("Language (Keyword 1):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country1 = st.selectbox("Country (Keyword 1):", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

with col2:
    keyword2 = st.text_input("Keyword 2:")
    language2 = st.selectbox("Language (Keyword 2):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country2 = st.selectbox("Country (Keyword 2):", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

if st.button("Analyze"):
    if keyword1 and keyword2:
        results_keyword1 = scrape_serp(keyword1, language1, country1)
        results_keyword2 = scrape_serp(keyword2, language2, country2)

        common_urls, similarity_rate, common_count, urls1, urls2 = calculate_similarity(results_keyword1, results_keyword2)
        
        # Title Analysis
        count_keyword1, count_keyword2, count_both_keywords = analyze_titles(results_keyword1, results_keyword2, keyword1, keyword2)

        # Display results
        st.write(f"**Similarity Rate: {similarity_rate:.2f}% ({common_count} common URLs)**")
        
        # Title recommendation
        st.write(f"**Recommendation for Title:** To increase your chances of being a common URL, consider using **both keywords** in your title, if possible.")
        
        # Display SERP links
        st.write(f"**Search URL for Keyword 1:** [View SERP for {keyword1}](https://www.google.com/search?q={urllib.parse.quote(keyword1)})")
        st.write(f"**Search URL for Keyword 2:** [View SERP for {keyword2}](https://www.google.com/search?q={urllib.parse.quote(keyword2)})")

        # SERP Results
        with st.expander(f"View SERP for Keyword 1: {keyword1}"):
            for url, title in results_keyword1:
                st.write(f"[{title}]({url})")

        with st.expander(f"View SERP for Keyword 2: {keyword2}"):
            for url, title in results_keyword2:
                st.write(f"[{title}]({url})")

        # Common URLs
        st.write("**Common URLs**")
        for url in common_urls:
            st.write(url)

        # Unique URLs
        unique_urls_keyword1 = set(urls1.keys()) - set(urls2.keys())
        unique_urls_keyword2 = set(urls2.keys()) - set(urls1.keys())

        with st.expander(f"URLs only present for Keyword 1: {keyword1}"):
            for url in unique_urls_keyword1:
                st.write(url)

        with st.expander(f"URLs only present for Keyword 2: {keyword2}"):
            for url in unique_urls_keyword2:
                st.write(url)

        # Title occurrences
        st.write(f"{keyword1} in titles: {count_keyword1} occurrences")
        st.write(f"{keyword2} in titles: {count_keyword2} occurrences")
        st.write(f"Both keywords in titles: {count_both_keywords} occurrences")

        # Disclaimer
        st.write("**Disclaimer:** This tool provides an analysis of SERP similarity and title occurrences. However, having keywords in your title alone is not a sufficient element for ranking. Consider other SEO factors as well.")

        # Backlink
        st.write("Tool made with love by [Charles Migaud](https://charles-migaud.fr/)")

    else:
        st.error("Please enter both keywords.")
