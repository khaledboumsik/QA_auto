import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BrokenLinkDetector:
    def __init__(self, url: str):
        self.url = url
        self.report = ""
    
    def _get_links(self) -> List[str]:
        """Extracts all links from the page."""
        try:
            # Send a request to fetch the page content
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all anchor tags and their href attributes
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return links
        except requests.exceptions.RequestException as e:
            self.report += f"Error fetching the page: {e}\n"
            return []
    
    def _check_link(self, link: str) -> str:
        """Checks the status code of a link and categorizes it."""
        try:
            # Resolve relative URLs to absolute URLs
            full_link = urljoin(self.url, link)
            
            # Skip JavaScript links or anchor links
            if link.startswith("#") or link.startswith("javascript"):
                return "local"
            
            # Send a request to check the link status
            response = requests.get(full_link)
            status_code = response.status_code
            
            # Categorize based on status codes
            if 200 <= status_code < 300:
                return "valid"
            elif 300 <= status_code < 400:
                return "redirect"
            elif 400 <= status_code < 500:
                if status_code == 401:
                    return "authentication_required"
                elif status_code == 403:
                    return "forbidden"
                elif status_code == 404:
                    return "invalid"
                return "client_error"
            elif 500 <= status_code < 600:
                return "server_error"
            else:
                return "unknown"
        except requests.exceptions.RequestException:
            return "invalid"
    
    def generate_report(self) -> str:
        """Generates a report on the link status for the page."""
        links = self._get_links()
        if not links:
            return "No links found or error fetching page."
        
        valid_links = []
        redirect_links = []
        local_links = []
        js_links = []
        invalid_links = []
        authentication_required = []
        forbidden_links = []
        client_error_links = []
        server_error_links = []
        unknown_links = []

        self.report += f"Broken Link Detection Report for {self.url}:\n"
        
        # Categorize links
        for link in links:
            full_link = urljoin(self.url, link)  # Convert to full URL
            link_status = self._check_link(link)
            
            if link_status == "valid":
                valid_links.append(full_link)
            elif link_status == "redirect":
                redirect_links.append(full_link)
            elif link_status == "local":
                local_links.append(full_link)
            elif link_status == "authentication_required":
                authentication_required.append(full_link)
            elif link_status == "forbidden":
                forbidden_links.append(full_link)
            elif link_status == "invalid":
                invalid_links.append(full_link)
            elif link_status == "client_error":
                client_error_links.append(full_link)
            elif link_status == "server_error":
                server_error_links.append(full_link)
            else:
                unknown_links.append(full_link)
        
        # Report results by groups
        if valid_links:
            self.report += "\n✅ Valid Links (2xx):\n"
            for link in valid_links:
                self.report += f"  {link}\n"
        
        if redirect_links:
            self.report += "\n🔁 Redirect Links (3xx):\n"
            for link in redirect_links:
                self.report += f"  {link}\n"
        
        if local_links:
            self.report += "\n📍 Local Links (within the same page):\n"
            for link in local_links:
                self.report += f"  {link}\n"
        
        if js_links:
            self.report += "\n🔧 JavaScript Links:\n"
            for link in js_links:
                self.report += f"  {link}\n"
        
        if invalid_links:
            self.report += "\n❌ Invalid Links (404 or request failed):\n"
            for link in invalid_links:
                self.report += f"  {link}\n"
        
        if authentication_required:
            self.report += "\n🔒 Authentication Required (401 Unauthorized):\n"
            for link in authentication_required:
                self.report += f"  {link}\n"
        
        if forbidden_links:
            self.report += "\n🚫 Forbidden Links (403 Forbidden):\n"
            for link in forbidden_links:
                self.report += f"  {link}\n"
        
        if client_error_links:
            self.report += "\n⚠️ Client Error Links (4xx):\n"
            for link in client_error_links:
                self.report += f"  {link}\n"
        
        if server_error_links:
            self.report += "\n💥 Server Error Links (5xx):\n"
            for link in server_error_links:
                self.report += f"  {link}\n"
        
        if unknown_links:
            self.report += "\n❓ Unknown Links (Other codes):\n"
            for link in unknown_links:
                self.report += f"  {link}\n"
        
        return self.report


if __name__ == "__main__":
    url = "https://www.art.yale.edu/"
    detector = BrokenLinkDetector(url)
    report = detector.generate_report()
    print(report)
