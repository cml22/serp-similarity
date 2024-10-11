import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to fetch SERP data
def fetch_serp_data(keyword, num_results):
    # Modify the search URL as needed, e.g., with "&num={num_results}"
    url = f"https://www.google.com/search?q={keyword}&num={num_results}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    urls = {}
    for item in soup.find_all('h3'):
        a_tag = item.find_parent('a')
        if a_tag:
            title = item.get_text()
            link = a_tag['href']
            rank = len(urls) + 1  # Assign a rank based on the order of appearance
            urls[link] = (title, rank)
    
    return urls

# Streamlit app layout
st.title("SERP Similarity Analysis Tool")

# Input fields for keywords
keyword1 = st.text_input("Enter the first keyword:")
keyword2 = st.text_input("Enter the second keyword:")
num_results = st.slider("Select the number of URLs to scrape (between 10 and 100)", 10, 100, 10)

if st.button("Fetch SERP Data"):
    if keyword1 and keyword2:
        # Fetch data
        urls1 = fetch_serp_data(keyword1, num_results)
        urls2 = fetch_serp_data(keyword2, num_results)

        # Prepare data for common URLs
        common_urls = set(urls1.keys()) & set(urls2.keys())
        common_urls_data = []

        for url in common_urls:
            title1, rank1 = urls1[url]
            title2, rank2 = urls2[url]
            common_urls_data.append({"URL": url, f"Rank in '{keyword1}'": rank1, f"Rank in '{keyword2}'": rank2})

        # Create DataFrame for common URLs
        df_common = pd.DataFrame(common_urls_data)

        # Display the number of common URLs
        st.write(f"### Common URLs Found: {len(common_urls)}")

        # Display the Common URLs and Rankings table
        st.write("### Common URLs and Rankings")
        st.dataframe(df_common)

        # Download button for common URLs
        st.download_button(
            label="Download Common URLs and Rankings as CSV",
            data=df_common.to_csv(index=False).encode('utf-8'),
            file_name='common_urls_rankings.csv',
            mime='text/csv',
        )

        # Unique URLs
        unique_urls_keyword1 = set(urls1.keys()) - set(urls2.keys())
        unique_urls_keyword2 = set(urls2.keys()) - set(urls1.keys())

        # Prepare data for unique URLs
        unique_urls_data1 = [{"URL": url, "Title": urls1[url][0]} for url in unique_urls_keyword1]
        unique_urls_data2 = [{"URL": url, "Title": urls2[url][0]} for url in unique_urls_keyword2]

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
        with st.expander(f"Unique URLs for '{keyword1}'"):
            if unique_urls_data1:
                st.write(f"**Unique URLs for '{keyword1}'**")
                for entry in unique_urls_data1:
                    st.markdown(f"- [{entry['Title']}]({entry['URL']})")
            else:
                st.write("No unique URLs found.")

        with st.expander(f"Unique URLs for '{keyword2}'"):
            if unique_urls_data2:
                st.write(f"**Unique URLs for '{keyword2}'**")
                for entry in unique_urls_data2:
                    st.markdown(f"- [{entry['Title']}]({entry['URL']})")
            else:
                st.write("No unique URLs found.")

        st.markdown("---")

# Include any necessary footer or additional information
st.write("Thank you for using the SERP Similarity Analysis Tool! If you have any feedback or suggestions, feel free to contact us.")
