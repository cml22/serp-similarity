import streamlit as st
import requests
from urllib.parse import urlparse

# Configure the page
st.set_page_config(page_title="SERP Similarity Analysis", layout="centered")

# Function to extract the domain from a URL
def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

# Function to scrape a SERP (dummy scraper here, but you can add actual scraping logic)
def scrape_serp(keyword, language, country):
    # Example fake results (replace with your actual scraping logic)
    if keyword == "test":
        return [
            ("https://example.com/page1", "Example Title 1"),
            ("https://example.com/page2", "Example Title 2"),
            ("https://different.com/page3", "Different Title 1")
        ]
    else:
        return [
            ("https://example.com/page2", "Example Title 2"),
            ("https://example.com/page4", "Example Title 3"),
            ("https://another.com/page5", "Another Title 1")
        ]

# Function to calculate similarities
def calculate_similarity(results1, results2):
    # Extract URLs
    urls1 = {result[0]: result[1] for result in results1}
    urls2 = {result[0]: result[1] for result in results2}

    # Extract domains
    domains1 = {extract_domain(url): title for url, title in results1}
    domains2 = {extract_domain(url): title for url, title in results2}

    # Calculate URL similarity
    common_urls = set(urls1.keys()).intersection(set(urls2.keys()))
    url_similarity_rate = len(common_urls) / len(set(urls1.keys()).union(set(urls2.keys()))) * 100 if urls1 or urls2 else 0

    # Calculate Domain similarity with different URLs
    common_domains = set(domains1.keys()).intersection(set(domains2.keys()))
    domain_similarity_rate = len(common_domains) / len(set(domains1.keys()).union(set(domains2.keys()))) * 100 if domains1 or domains2 else 0

    return url_similarity_rate, domain_similarity_rate

# Input fields for keywords, language, and country
st.title("SERP Similarity Analysis")
keyword1 = st.text_input("Enter first keyword:", "")
keyword2 = st.text_input("Enter second keyword:", "")
language1 = st.selectbox("Select language for first keyword:", ["en", "fr"])
language2 = st.selectbox("Select language for second keyword:", ["en", "fr"])
country1 = st.selectbox("Select country for first keyword:", ["us", "gb", "fr"])
country2 = st.selectbox("Select country for second keyword:", ["us", "gb", "fr"])

if st.button("Analyze"):
    # Scrape SERPs
    results_keyword1 = scrape_serp(keyword1, language1, country1)
    results_keyword2 = scrape_serp(keyword2, language2, country2)

    # Calculate similarities
    url_similarity_rate, domain_similarity_rate = calculate_similarity(results_keyword1, results_keyword2)

    # Display results
    st.subheader("Results")
    st.write(f"Similarity Rate URL: {url_similarity_rate:.2f}%")
    st.write(f"Domain Similarity Rate (with different URLs): {domain_similarity_rate:.2f}%")

    # Show results
    st.write("Results for first keyword:")
    for url, title in results_keyword1:
        st.write(f"- [{title}]({url})")
    
    st.write("Results for second keyword:")
    for url, title in results_keyword2:
        st.write(f"- [{title}]({url})")

# Disclaimer
st.write("Disclaimer: This tool is for educational purposes only. Actual SERP results may vary.")
st.write("For more information, visit [your website](https://yourwebsite.com).")
