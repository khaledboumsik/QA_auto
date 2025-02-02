from typing import Dict, List
from web_scraper import WebScraper
class HTMLBugChecker:
    def __init__(self, elements: List[Dict]):
        self.elements = elements

    def detect_html_issues(self) -> List[str]:
        issues = []
        ids = set()

        for element in self.elements:
            tag_name = element.get("tag")
            element_id = element.get("id")  # Use .get() to avoid KeyError

            # 1. Check for duplicate IDs
            if element_id:
                if element_id in ids:
                    issues.append(f"Duplicate ID found: {element_id}")
                else:
                    ids.add(element_id)

            # 2. Check for empty <a> tags without href
            if tag_name == "a" and not element.get("href"):
                issues.append(f"Empty <a> tag without href found: {element}")

            # 3. Check for <img> tags without alt attributes
            if tag_name == "img" and not element.get("alt"):
                issues.append(f"Missing alt attribute in <img>: {element}")

            # 4. Check for deprecated attributes (example: name on non-form elements)
            if element.get("name") and tag_name not in ["input", "textarea", "select", "form"]:
                issues.append(f"Deprecated 'name' attribute found on <{tag_name}>: {element}")

            # 5. Detect incorrectly nested tags
            if tag_name in ["p", "span"] and any(child in ["div", "section"] for child in element.get("children", [])):
                issues.append(f"Incorrect nesting inside <{tag_name}>: {element}")

        return issues



# Example usage:
if __name__ == "__main__":
    url = "https://www.art.yale.edu/"  # Replace with the target URL
    scraper = WebScraper(url)
    
    # Extract elements
    elements = scraper.extract_elements()
    
    # Check for HTML bugs
    bug_checker = HTMLBugChecker(elements)
    issues = bug_checker.detect_html_issues()
    
    print("Detected Issues:")
    for issue in issues:
        print("-", issue)