import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_serp(keyword, language, country):
    query = urllib.parse.quote(keyword)
    
    # Update the country code for the UK
    if country == "gb":
        country = "co.uk"
        
    url = f"https://www.google.{country}/search?q={query}&hl={language}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, Gecko) Chrome/116.0.5845.96 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error while fetching results.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='g'):
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

# Example usage of the tool
if __name__ == "__main__":
    keyword1 = input("Enter Keyword 1: ")
    language1 = input("Enter Language for Keyword 1 (e.g., en, fr): ")
    country1 = input("Enter Country for Keyword 1 (e.g., us, co.uk): ")
    
    keyword2 = input("Enter Keyword 2: ")
    language2 = input("Enter Language for Keyword 2 (e.g., en, fr): ")
    country2 = input("Enter Country for Keyword 2 (e.g., us, co.uk): ")
    
    # Scrape results for both keywords
    results_keyword1 = scrape_serp(keyword1, language1, country1)
    results_keyword2 = scrape_serp(keyword2, language2, country2)

    # Calculate similarity
    common_urls, urls1, urls2, similarity_rate_url = calculate_similarity(results_keyword1, results_keyword2)

    # Analyze titles
    counts = analyze_titles((results_keyword1, results_keyword2), keyword1, keyword2)

    # Display similarity results
    print(f"Similarity Rate URL: {similarity_rate_url:.2f}%")

    if counts['common_both'] > 0:
        print("Both keywords seem to contribute to being a common URL in the title.")
    elif counts['common_keyword1'] > counts['common_keyword2']:
        print(f"It would be better to include {keyword1} in your title to optimize your ranking.")
    elif counts['common_keyword2'] > counts['common_keyword1']:
        print(f"It would be better to include {keyword2} in your title to optimize your ranking.")
    else:
        print("Neither keyword seems effective alone. Consider other optimizations.")

    # Display SERP details
    print(f"\nCommon URLs between {keyword1} and {keyword2}:")
    for url in common_urls:
        print(url)

    # Unique URLs for each keyword
    unique_urls1 = set(urls1.keys()) - common_urls
    unique_urls2 = set(urls2.keys()) - common_urls

    print(f"\nUnique URLs for {keyword1}:")
    for url in unique_urls1:
        print(url)

    print(f"\nUnique URLs for {keyword2}:")
    for url in unique_urls2:
        print(url)
