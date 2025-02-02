from web_accesability.style_and_accesability_checkers import StyleAnalyzer,AccessibilityChecker
from typing import Dict, List
from web_scraper import WebScraper



class AccessibilityReport:
    def __init__(self, elements: List[Dict], default_bg_color: str = "#FFFFFF"):
        self.elements = elements
        self.default_bg_color = default_bg_color  # Default background color (e.g., body)
        self.report = ""

    def find_nearest_background_color(self, element) -> str:
        # Try to get the background color from the element's inline style first
        style = element.get('style', '')
        colors = StyleAnalyzer.extract_colors(style)
        if "background-color" in colors:
            return colors["background-color"]
        
        # If no background color found, check the parent element's background color
        parent = element.find_parent()  # Assuming you're using a method to get the parent
        while parent:
            style = parent.get('style', '')
            colors = StyleAnalyzer.extract_colors(style)
            if "background-color" in colors:
                return colors["background-color"]
            parent = parent.find_parent()
        
        # Return a default background color if none found
        return "#ffffff"  # Default to white

    def generate(self) -> str:
        for element in self.elements:
            self.report += f"Tag: {element['tag']}\n"
            self.report += f"Text: {element['text']}\n"
            self.report += f"ARIA Label: {element['aria_label']}\n"
            self.report += f"ARIA Expanded: {element['aria_expanded']}\n"
            self.report += f"ARIA Hidden: {element['aria_hidden']}\n"
            self.report += f"Tabindex: {element['tabindex']}\n"
            self.report += f"Class: {element['class']}\n"
            self.report += f"Href: {element['href']}\n"
            
            colors = StyleAnalyzer.extract_colors(element["style"])
            if colors:
                self.report += "Colors:\n"
                for key, value in colors.items():
                    self.report += f"  {key}: {value}\n"
                    if key == "color":
                        bg_color = self.find_nearest_background_color(element)  # Get closest background color
                        contrast_ratio = StyleAnalyzer.calculate_contrast(value, bg_color)
                        if contrast_ratio:
                            self.report += f"  Contrast Ratio: {contrast_ratio:.2f}\n"
                            self.report += "  ✅ Meets WCAG 2.1 AA standard.\n" if contrast_ratio >= 4.5 else "  ❌ Does not meet WCAG 2.1 AA standard.\n"
            
            keyboard_issues = AccessibilityChecker.check_keyboard_accessibility(element)
            if keyboard_issues:
                self.report += "\n⚠️ Keyboard Accessibility Issues Found:\n" + "\n".join(f"  - {issue}" for issue in keyboard_issues)
            
            self.report += "\n"
        return self.report



if __name__ == "__main__":
    url = "https://www.art.yale.edu/"
    scraper = WebScraper(url)
    elements = scraper.extract_elements()
    report = AccessibilityReport(elements).generate()
    print(report)
