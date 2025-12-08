import requests
from bs4 import BeautifulSoup

URL = "https://www.unr.edu/engineering/student-resources/clubs"

def scrape_clubs(url=URL):
    resp = requests.get(url, timeout=10)

    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    clubs = []

    for h2 in soup.find_all("h2"):
        name = h2.get_text(strip=True)
        description_parts = []
        for sib in h2.find_next_siblings():
            if sib.name == "h2":
                break
            if sib.name == "p":
                description_parts.append(sib.get_text(strip=True))
        description = "\n".join(description_parts).strip() if description_parts else None
        if name:
            clubs.append({"name": name, "description": description})

    return clubs

if __name__ == "__main__":
    clubs = scrape_clubs()
    for c in clubs:
        print(c["name"])
