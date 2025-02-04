import requests
from bs4 import BeautifulSoup
from readability.readability_analyzer import ReadabilityAnalyzer
from readability.typography_anaylzer import TypographyAnalyzer
class WebpageAnalyzer:
    """Combines Readability & Typography Analysis with location references."""

    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None

    def fetch_content(self):
        """Fetch webpage content."""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.html = response.text
            self.soup = BeautifulSoup(self.html, "html.parser")
            return True
        except requests.RequestException as e:
            print(f"Error fetching website: {e}")
            return False

    def analyze(self):
        """Performs readability & typography analysis with issue locations."""
        if not self.soup:
            return {"error": "No HTML content to analyze."}

        # Extract visible text
        text = " ".join([p.get_text() for p in self.soup.find_all("p")])

        return {
            "Readability": ReadabilityAnalyzer.get_text_statistics(text),
            "Typography": TypographyAnalyzer.analyze_fonts(self.soup),
            "Contrast": TypographyAnalyzer.analyze_contrast(self.soup),
        }

def readability_performance(url):
    analyzer = WebpageAnalyzer(url)

    if analyzer.fetch_content():
        results = analyzer.analyze()
        return str(results)
    else:
        return "no readablitiy issues"
