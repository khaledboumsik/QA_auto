from typing import Dict, List
class HTMLBugChecker:
    def __init__(self, elements: List[Dict]):
        self.elements = elements

    def detect_html_issues(self) -> List[str]:
        issues = []
        ids = set()

        for element in self.elements:
            tag_name = element.get("tag")
            element_id = element.get("id")

            if element_id:
                if element_id in ids:
                    issues.append(f"Duplicate ID found: {element_id}")
                else:
                    ids.add(element_id)

            if tag_name == "a" and not element.get("href"):
                issues.append(f"Empty <a> tag without href found: {element}")

            if tag_name == "img" and not element.get("alt"):
                issues.append(f"Missing alt attribute in <img>: {element}")

            if element.get("name") and tag_name not in ["input", "textarea", "select", "form"]:
                issues.append(f"Deprecated 'name' attribute found on <{tag_name}>: {element}")

        return issues
