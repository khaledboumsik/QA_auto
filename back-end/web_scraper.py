import requests
from typing import Dict, List
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = self._fetch_and_parse()
    
    def _fetch_and_parse(self) -> BeautifulSoup:
        response = requests.get(self.url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    
    def extract_elements(self) -> List[Dict]:
        elements = []
        for tag in self.soup.find_all(True):
            elements.append({
                "tag": tag.name,
                "text": tag.get_text(strip=True),
                "aria_label": tag.get("aria-label"),
                "aria_expanded": tag.get("aria-expanded"),
                "aria_hidden": tag.get("aria-hidden"),
                "tabindex": tag.get("tabindex"),
                "class": tag.get("class"),
                "href": tag.get("href"),
                "style": tag.get("style"),
                "id": tag.get("id"),
                "alt": tag.get("alt"),
                "name": tag.get("name"),
            })
        return elements