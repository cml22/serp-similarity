import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from collections import Counter
import spacy

# Load the spaCy model (only needed once)
nlp = spacy.load("en_core_web_sm")

# Must be the first Streamlit command
st.set_page_config(page_title="SERP Similarity Analysis", layout="centered")

# Purpose of the tool
st.write("## Purpose")
st.write("This tool compares the similarity of SERPs (Search Engine Results Pages) for two different keywords. It helps determine whether a new page should be created or if an existing page should be optimized based on the overlap of search results.")

# Disclaimer
st.info("**Disclaimer:** Optimizing titles alone is not enough for SEO. Ensure you're addressing other key factors like content quality, backlinks, and user experience.")

# Backlink to Charles Migaud's site
st.markdown('Tool made with ❤️ by [Charles Migaud](https://charles-migaud.fr)')

def scrape_serp(keyword, language, country, num_urls):
    query = urllib.parse.quote(keyword)
    
    # Update the country code for the UK
    if country == "gb":
        country = "co.uk"
        
    url = f"https://www.google.{country}/search?q={query}&hl={language}&gl={country}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Error while fetching results.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Title not found"
            results.append((link['href'], title))

    return results[:num_urls]

def extract_domain(url):
    """Extract domain name from URL."""
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc

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
    # Extract full URLs
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    # Calculate similarity for URLs
    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    total_urls = len(set(urls1.keys()).union(set(urls2.keys())))

    similarity_rate_url = (len(common_urls) / total_urls) * 100 if total_urls > 0 else 0

    # Calculate similarity for domains
    domains1 = {extract_domain(url) for url in urls1.keys()}
    domains2 = {extract_domain(url) for url in urls2.keys()}
    
    common_domains = domains1.intersection(domains2)
    total_domains = domains1.union(domains2)
    
    similarity_rate_domain = (len(common_domains) / len(total_domains)) * 100 if total_domains else 0
    
    return common_urls, urls1, urls2, similarity_rate_url, similarity_rate_domain

def extract_content(url):
    """Scrape content from a URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title and headings
        title = soup.title.string if soup.title else "No Title"
        headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
        
        # Extract main content
        content = ' '.join(p.get_text() for p in soup.find_all('p'))
        
        return title, headings, content
    except Exception as e:
        st.warning(f"Could not fetch content from {url}: {e}")
        return None, None, None

def generate_ngrams(text, n):
    """Generate n-grams from text using spaCy."""
    doc = nlp(text)
    ngrams_list = [tuple(doc[i:i+n].text for i in range(len(doc)-n+1)) for n in range(1, n+1)]
    return [ng for ngram in ngrams_list for ng in ngram]

def analyze_ngrams(common_urls, keyword1, keyword2, n):
    """Analyze n-grams from titles, headings, and content of common URLs."""
    all_ngrams = []
    
    for url in common_urls:
        title, headings, content = extract_content(url)
        all_ngrams.extend(generate_ngrams(title, n))
        for heading in headings:
            all_ngrams.extend(generate_ngrams(heading, n))
        all_ngrams.extend(generate_ngrams(content, n))
    
    ngram_counts = Counter(all_ngrams)
    most_common_ngram, freq = ngram_counts.most_common(1)[0] if ngram_counts else (None, 0)
    
    keyword1_ngram = tuple(keyword1.lower().split())
    keyword2_ngram = tuple(keyword2.lower().split())

    is_keyword1 = most_common_ngram == keyword1_ngram
    is_keyword2 = most_common_ngram == keyword2_ngram
    
    return most_common_ngram, freq, is_keyword1, is_keyword2

# User Interface with Streamlit
st.title("SERP Similarity Analysis")
st.markdown("---")

# Input fields for keywords
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Enter Keyword 1:", placeholder="Ex: digital marketing")
    language1 = st.selectbox("Language (Keyword 1):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country1 = st.selectbox("Country (Keyword 1):", ["fr", "co.uk", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

with col2:
    keyword2 = st.text_input("Enter Keyword 2:", placeholder="Ex: SEO")
    language2 = st.selectbox("Language (Keyword 2):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country2 = st.selectbox("Country (Keyword 2):", ["fr", "co.uk", "us", "ca", "es", "de", "it", "pt", "pl", "ma", "sn", "tn"])

# Slider for the number of URLs to scrape
num_urls = st.slider("Number of URLs to Scrape:", min_value=10, max_value=100, value=10, step=10)

st.markdown("---")

if st.button("Analyze"):
    if keyword1 and keyword2:
        # Scrape the results for both keywords
        results_keyword1 = scrape_serp(keyword1, language1, country1, num_urls)
        results_keyword2 = scrape_serp(keyword2, language2, country2, num_urls)

        # Calculate similarity
        common_urls, urls1, urls2, similarity_rate_url, similarity_rate_domain = calculate_similarity(results_keyword1, results_keyword2)

        # Analyze titles
        counts = analyze_titles((results_keyword1, results_keyword2), keyword1, keyword2)

        # Analyze n-grams
        n = 2  # Change this to set n-gram size (e.g., 2 for bigrams)
        most_common_ngram, freq, is_keyword1, is_keyword2 = analyze_ngrams(common_urls, keyword1, keyword2, n)

        # Display results
        st.write(f"**Most Common N-gram:** {most_common_ngram} (Frequency: {freq})")
        
        if is_keyword1:
            st.success(f"The most representative n-gram matches **Keyword 1: {keyword1}**.")
        elif is_keyword2:
            st.success(f"The most representative n-gram matches **Keyword 2: {keyword2}**.")
        else:
            st.warning("The most common n-gram does not match either keyword.")

        # Display similarity rates
        st.write(f"**Similarity Rate (URLs):** {similarity_rate_url:.2f}%")
        st.write(f"**Similarity Rate (Domains):** {similarity_rate_domain:.2f}%")

        # Display common URLs
        # Display common URLs
        st.write("### Common URLs:")
        if common_urls:
            for url in common_urls:
                st.write(url)
        else:
            st.write("No common URLs found.")

        # Display the results for each keyword's SERP
        st.write("### SERP Results for Keyword 1:")
        for url, title in results_keyword1:
            st.write(f"- **{title}**: [Link]({url})")

        st.write("### SERP Results for Keyword 2:")
        for url, title in results_keyword2:
            st.write(f"- **{title}**: [Link]({url})")

    else:
        st.warning("Please enter both keywords to proceed.")

# Optionally, you can add a footer
st.markdown("---")
st.write("**Note:** This tool is in development, and results may vary based on changes in Google SERP structures.")

