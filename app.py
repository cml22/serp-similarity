import requests
from bs4 import BeautifulSoup

def scrape_serp(query, lang="en", location="us"):
    # Ajustement de l'URL de recherche Google
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

    # Google utilise différentes classes CSS pour les résultats. On essaye avec plusieurs.
    for g in soup.find_all('div', class_='g'):
        title_element = g.find('h3')
        link_element = g.find('a')

        # On vérifie que le titre et le lien existent
        if title_element and link_element:
            title = title_element.text
            link = link_element['href']
            results.append((title, link))
    
    if not results:
        return "No results found or blocked by Google."

    return results
