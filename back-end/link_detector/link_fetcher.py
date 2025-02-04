import requests
from bs4 import BeautifulSoup
from typing import List


class LinkFetcher:
    def __init__(self, url: str):
        self.url = url

    def get_links(self) -> List[str]:
        """Fetches and extracts all links from the webpage."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return [a['href'] for a in soup.find_all('a', href=True)]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return []