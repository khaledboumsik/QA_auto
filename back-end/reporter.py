from typing import Dict, List
from style_analyzer import StyleAnalyzer
from web_scraper import WebScraper
from html_bug_detector import HTMLBugChecker
from broken_link_detector import BrokenLinkDetector
from helpers.report_saver import save_report
from performance import output_performance
from web_page_analyzer import readability_performance
from openai_api import generate_text,create_word_document
class IReport:
    """Interface for all report generators"""
    def generate(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

class AccessibilityReport(IReport):
    """Generates an accessibility report based on extracted elements."""
    def __init__(self, elements: List[Dict], default_bg_color: str = "#FFFFFF"):
        self.elements = elements
        self.default_bg_color = default_bg_color

    def find_nearest_background_color(self, element) -> str:
        style = element.get('style', '')
        colors = StyleAnalyzer.extract_colors(style)
        return colors.get("background-color", self.default_bg_color)

    def generate(self) -> str:
        report = "=== ACCESSIBILITY REPORT ===\n\n"
        
        # HTML Validation
        html_checker = HTMLBugChecker(self.elements)
        html_issues = html_checker.detect_html_issues()
        if html_issues:
            report += "=== HTML VALIDATION ISSUES ===\n\n"
            report += "\n".join(f"⚠️ {issue}" for issue in html_issues)
        else:
            report += "=== HTML VALIDATION ===\n\n✅ No HTML issues found\n"

        return report

class BrokenLinkReport(IReport):
    """Generates a report on broken links in a website."""
    def __init__(self, url: str):
        self.url = url

    def generate(self) -> str:
        detector = BrokenLinkDetector(self.url)
        report = detector.generate_report()
        return "\nHTML links health: note that 🔄 means the link is reconstructed, and ✔️ indicates a valid link.\n" + report

class PerformanceReport(IReport):
    """Generates a performance report for a website."""
    def __init__(self, url: str):
        self.url = url

    def generate(self) -> str:
        lighthouse_report = output_performance(self.url)
        return f"\nThis is a report of the website's performance:\n{lighthouse_report}"

class ReadabilityReport(IReport):
    """Generates a readability and typography analysis report."""
    def __init__(self, url: str):
        self.url = url

    def generate(self) -> str:
        return readability_performance(self.url)

class ReportGenerator:
    """Handles generating multiple reports based on test results."""
    def __init__(self, url: str, test_results: Dict[str, bool]):
        self.url = url
        self.test_results = test_results
        self.reports: List[IReport] = []
        self.scrapper=WebScraper(self.url)
        self.content=self.scrapper.soup
    def collect_reports(self):
        if self.test_results.get("Accessibility Testing"):
            elements = self.scrapper.extract_elements()
            self.reports.append(AccessibilityReport(elements))
        
        if self.test_results.get("Broken Link Detection"):
            self.reports.append(BrokenLinkReport(self.url))

        if self.test_results.get("Performance Testing"):
            self.reports.append(PerformanceReport(self.url))

        if self.test_results.get("Readability & Typography Analysis"):
            self.reports.append(ReadabilityReport(self.url))

    def generate_report(self) -> str:
        final_report = "\n".join(report.generate() for report in self.reports)
        save_report(final_report, "QA_report.txt")
        return final_report

def create_report(url: str, test_results: Dict[str, bool]):
    generator = ReportGenerator(url, test_results)
    generator.collect_reports()
    final_report = generator.generate_report()

    prompt = {
        "Context": "You are a senior QA consultant...",
        "Information": final_report + " " + str(generator.content),
        "Style": "Your response should be detailed..."
    }
    
    response = generate_text(str(prompt), 1000)
    return create_word_document(response)
