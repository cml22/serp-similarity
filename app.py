import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd

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
    # Adding num={num_results} parameter to scrape the specified number of results
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
    for g in soup.find_all('div', class_='g')[:num_results]:  # Limit the number of results
        link = g.find('a', href=True)
        if link:
            title = g.find('h3').get_text() if g.find('h3') else "Title not found"
            results.append((link['href'], title))

    return results

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
    
    return common_urls, urls1, urls2, similarity_rate_url

# User Interface with Streamlit
st.title("SERP Similarity Analysis")
st.markdown("---")

# Input fields for keywords
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Enter Keyword 1:", placeholder="Ex: digital marketing")
    language1 = st.selectbox("Language (Keyword 1):", ["fr", "en", "es", "de", "it", "pt", "pl"])
    country1 = st.selectbox("Country (Keyword 1):", ["FR", "GB", "US", "CA", "ES", "DE", "IT", "PT", "PL", "MA", "SN", "TN"])

with col2:
    keyword2 = st.text_input("Enter Keyword 2:", placeholder="Ex: SEO")
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

        # Calculate similarity
        common_urls, urls1, urls2, similarity_rate_url = calculate_similarity(results_keyword1, results_keyword2)

        # Analyze titles
        counts = analyze_titles((results_keyword1, results_keyword2), keyword1, keyword2)

        # Display results
        st.write(f"**Similarity Rate URL: {similarity_rate_url:.2f}%**")
        
        # Summary on keyword usage
        if counts['common_both'] > 0:
            st.success("Both keywords seem to contribute to being a common URL in the title.")
        elif counts['common_keyword1'] > counts['common_keyword2']:
            st.warning(f"It would be better to include **{keyword1}** in your title to optimize your ranking.")
        elif counts['common_keyword2'] > counts['common_keyword1']:
            st.warning(f"It would be better to include **{keyword2}** in your title to optimize your ranking.")
        else:
            st.info("Neither keyword seems effective alone. Consider other optimizations.")

        st.markdown("---")
        st.subheader("SERP Results")
        
        # Display search links with encoded keywords and the correct language/country
        encoded_keyword1 = urllib.parse.quote(keyword1)
        encoded_keyword2 = urllib.parse.quote(keyword2)

        # Generate SERP links with language and country parameters
        serp_url1 = f"https://www.google.com/search?q={encoded_keyword1}&hl={language1}&gl={country1}&num={num_urls}"
        serp_url2 = f"https://www.google.com/search?q={encoded_keyword2}&hl={language2}&gl={country2}&num={num_urls}"

        # Display the clickable links for the SERPs
        st.markdown(f"[View SERP for Keyword: {keyword1}]({serp_url1})")
        st.markdown(f"[View SERP for Keyword: {keyword2}]({serp_url2})")

        # Display SERP results
        with st.expander(f"Details for Keyword: {keyword1}"):
            st.write(f"**SERP for Keyword: {keyword1}**")
            for rank, (url, title) in enumerate(results_keyword1, start=1):
                st.markdown(f"{rank}. [{title}]({url})")

        with st.expander(f"Details for Keyword: {keyword2}"):
            st.write(f"**SERP for Keyword: {keyword2}**")
            for rank, (url, title) in enumerate(results_keyword2, start=1):
                st.markdown(f"{rank}. [{title}]({url})")

        st.markdown("---")
        st.subheader("Common URLs and Rankings")

        # Prepare data for the table
        common_urls_data = []
        for url in common_urls:
            rank_keyword1 = next((i + 1 for i, (u, _) in enumerate(results_keyword1) if u == url), "Not Found")
            rank_keyword2 = next((i + 1 for i, (u, _) in enumerate(results_keyword2) if u == url), "Not Found")
            common_urls_data.append({"URL": url, f"Rank in '{keyword1}'": rank_keyword1, f"Rank in '{keyword2}'": rank_keyword2})

        # Display number of common URLs
        st.write(f"**Number of Common URLs: {len(common_urls)}**")

        # Create a DataFrame for exporting to CSV
        df_common = pd.DataFrame(common_urls_data)

        # Button to download the common data as CSV
        st.download_button(
            label="Download Common URLs CSV",
            data=df_common.to_csv(index=False).encode('utf-8'),
            file_name='common_urls.csv',
            mime='text/csv',
        )

        # Display common URLs in a table
        st.dataframe(df_common)

        st.markdown("---")
        st.subheader("Unique URLs in Each SERP")

        # Unique URLs
        unique_urls_keyword1 = set(urls1.keys()) - set(urls2.keys())
        unique_urls_keyword2 = set(urls2.keys()) - set(urls1.keys())

        # Prepare data for unique URLs
        unique_urls_data1 = [{"URL": url, "Title": urls1[url]} for url in unique_urls_keyword1]
        unique_urls_data2 = [{"URL": url, "Title": urls2[url]} for url in unique_urls_keyword2]

        # Create DataFrames for exporting to CSV
        df_unique1 = pd.DataFrame(unique_urls_data1)
        df_unique2 = pd.DataFrame(unique_urls_data2)

        # Button to download unique URLs as CSV
        st.download_button(
            label="Download Unique URLs for Keyword 1 CSV",
            data=df_unique1.to_csv(index=False).encode('utf-8'),
            file_name='unique_urls_keyword1.csv',
            mime='text/csv',
        )

        st.download_button(
            label="Download Unique URLs for Keyword 2 CSV",
            data=df_unique2.to_csv(index=False).encode('utf-8'),
            file_name='unique_urls_keyword2.csv',
            mime='text/csv',
        )

        # Display unique URLs in accordions
        with st.expander(f"Unique URLs for Keyword: {keyword1}"):
            if unique_urls_data1:
                st.write(f"**Unique URLs for Keyword: {keyword1}**")
                for entry in unique_urls_data1:
                    st.markdown(f"- [{entry['Title']}]({entry['URL']})")
            else:
                st.write("No unique URLs found.")

        with st.expander(f"Unique URLs for Keyword: {keyword2}"):
            if unique_urls_data2:
                st.write(f"**Unique URLs for Keyword: {keyword2}**")
                for entry in unique_urls_data2:
                    st.markdown(f"- [{entry['Title']}]({entry['URL']})")
            else:
                st.write("No unique URLs found.")

        st.markdown("---")

# Include any necessary footer or additional information
st.write("Thank you for using the SERP Similarity Analysis Tool! If you have any feedback or suggestions, feel free to contact us.")

