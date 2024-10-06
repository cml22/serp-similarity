def scrape_serp(query, lang="en", location="us"):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=10&hl={lang}&gl={location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)

    # Ajouter un délai pour éviter le blocage
    time.sleep(2)  # Délai de 2 secondes

    if response.status_code != 200:
        return f"Error: Unable to fetch data from Google (status code: {response.status_code})"
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for g in soup.find_all('div', class_='g'):
        title_element = g.find('h3')
        link_element = g.find('a')

        if title_element and link_element:
            title = title_element.text
            link = link_element['href']
            results.append((title, link))
    
    if not results:
        return "No results found or blocked by Google."

    return results
