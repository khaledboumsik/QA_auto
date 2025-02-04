import requests
from urllib.parse import urljoin
from typing import Tuple


class LinkChecker:
    @staticmethod
    def check_link(base_url: str, link: str) -> Tuple[str, str, bool]:
        """Checks the status code of a link and categorizes it."""
        try:
            full_link = urljoin(base_url, link)

            # Skip JavaScript or local anchor links
            if link.startswith("#") or link.startswith("javascript"):
                return "local", full_link, False

            response = requests.get(full_link)
            status_code = response.status_code

            if 200 <= status_code < 300:
                return "valid", full_link, link != full_link
            elif 300 <= status_code < 400:
                return "redirect", full_link, link != full_link
            elif status_code == 401:
                return "authentication_required", full_link, link != full_link
            elif status_code == 403:
                return "forbidden", full_link, link != full_link
            elif status_code == 404:
                return "invalid", full_link, link != full_link
            elif 400 <= status_code < 500:
                return "client_error", full_link, link != full_link
            elif 500 <= status_code < 600:
                return "server_error", full_link, link != full_link
            else:
                return "unknown", full_link, link != full_link
        except requests.exceptions.RequestException:
            return "invalid", "", False
