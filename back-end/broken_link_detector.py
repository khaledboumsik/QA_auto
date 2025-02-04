from typing import Dict, List, Tuple
from link_detector.link_fetcher import LinkFetcher
from link_detector.link_checker import LinkChecker
from link_detector.report_generator import ReportGenerator

class BrokenLinkDetector:
    def __init__(self, url: str):
        self.url = url
        self.link_fetcher = LinkFetcher(url)

    def generate_report(self) -> str:
        """Generates a complete broken link report for the page."""
        links = self.link_fetcher.get_links()
        if not links:
            return "No links found or error fetching page."

        categorized_links: Dict[str, List[Tuple[str, str]]] = {
            "valid": [],
            "redirect": [],
            "local": [],
            "authentication_required": [],
            "forbidden": [],
            "invalid": [],
            "client_error": [],
            "server_error": [],
            "unknown": []
        }

        for link in links:
            category, full_link, is_reconstructed = LinkChecker.check_link(self.url, link)
            indicator = "✔️" if not is_reconstructed else "🔄"
            categorized_links[category].append((full_link, indicator))

        return ReportGenerator.generate_report(self.url, categorized_links)
