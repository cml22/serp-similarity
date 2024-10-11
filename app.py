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
    non_common_urls1 = set(urls1.keys()) - common_urls
    non_common_urls2 = set(urls2.keys()) - common_urls
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    similarity_rate = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0
    
    return common_urls, non_common_urls1, non_common_urls2, similarity_rate

# User interface with Streamlit
st.title("SERP Similarity Analysis")
st.markdown("---")  # Separator

# Purpose of the tool
st.subheader("Purpose of the Tool")
st.write("This tool analyzes the similarity of search engine results pages (SERPs) for two keywords and provides insights on how to optimize titles effectively.")

# Disclaimer
st.markdown("**Disclaimer:** Optimizing the title alone may not be sufficient for improving rankings. Consider other SEO factors for best results.")
st.write("Tool made with love by [Charles Migaud](https://charles-migaud.fr).")  # Backlink

# Input for keywords
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Enter Keyword 1:", placeholder="E.g., digital marketing")
    language1 = st.selectbox("Language (Keyword 1):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country1 = st.selectbox("Country (Keyword 1):", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

with col2:
    keyword2 = st.text_input("Enter Keyword 2:", placeholder="E.g., SEO")
    language2 = st.selectbox("Language (Keyword 2):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country2 = st.selectbox("Country (Keyword 2):", ["fr", "gb", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

st.markdown("---")  # Separator

if st.button("Analyze"):
    if keyword1 and keyword2:
        # Scrape results for both keywords
        results_keyword1 = scrape_serp(keyword1, language1, country1)
        results_keyword2 = scrape_serp(keyword2, language2, country2)

        st.write(f"Results for Keyword 1: {len(results_keyword1)} results found.")
        st.write(f"Results for Keyword 2: {len(results_keyword2)} results found.")

        # Calculate similarity
        common_urls, non_common_urls1, non_common_urls2, similarity_rate = calculate_similarity(results_keyword1, results_keyword2)

        # Analyze titles
        counts = analyze_titles((results_keyword1, results_keyword2), keyword1, keyword2)

        # Display results
        st.write(f"**Similarity Rate: {similarity_rate:.2f}%**")
        
        # Summary on keyword usage
        if counts['common_both'] > 0:
            st.success("Both keywords in the title appear to contribute to a common URL.")
        elif counts['common_keyword1'] > counts['common_keyword2']:
            st.warning(f"It would be beneficial to include **{keyword1}** in your title to optimize your ranking.")
        elif counts['common_keyword2'] > counts['common_keyword1']:
            st.warning(f"It would be beneficial to include **{keyword2}** in your title to optimize your ranking.")
        else:
            st.info("Neither keyword seems effective on its own. Consider other optimizations.")

        st.markdown("---")  # Separator
        st.subheader("SERP Results")
        
        # Display search links with encoding
        encoded_keyword1 = urllib.parse.quote(keyword1)
        encoded_keyword2 = urllib.parse.quote(keyword2)
        st.markdown(f"[View SERP for Keyword: {keyword1}](https://www.google.com/search?q={encoded_keyword1})")
        st.markdown(f"[View SERP for Keyword: {keyword2}](https://www.google.com/search?q={encoded_keyword2})")

        # Display SERP results
        with st.expander(f"SERP Details for Keyword: {keyword1}"):
            st.write(f"**SERP for Keyword: {keyword1}**")
            for url, title in results_keyword1:
                st.markdown(f"- [{title}]({url})")  # Clickable link

        with st.expander(f"SERP Details for Keyword: {keyword2}"):
            st.write(f"**SERP for Keyword: {keyword2}**")
            for url, title in results_keyword2:
                st.markdown(f"- [{title}]({url})")  # Clickable link

        st.markdown("---")  # Separator
        st.subheader("Common URLs")
        for url in common_urls:
            st.write(url)

        # Display URLs only present for Keyword 1
        with st.expander(f"URLs Only for Keyword: {keyword1}"):
            for url in non_common_urls1:
                st.write(url)

        # Display URLs only present for Keyword 2
        with st.expander(f"URLs Only for Keyword: {keyword2}"):
            for url in non_common_urls2:
                st.write(url)

    else:
        st.error("Please enter both keywords.")

# Final separator
st.markdown("---")  # Separator
