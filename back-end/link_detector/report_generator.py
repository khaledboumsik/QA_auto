from typing import Dict, List, Tuple


class ReportGenerator:
    @staticmethod
    def generate_report(url: str, categorized_links: Dict[str, List[Tuple[str, str]]]) -> str:
        """Generates a formatted report from categorized links."""
        report = f"Broken Link Detection Report for {url}:\n"

        category_titles = {
            "valid": "✅ Valid Links",
            "redirect": "🔁 Redirect Links",
            "local": "📍 Local Links",
            "authentication_required": "🔒 Authentication Required (401 Unauthorized)",
            "forbidden": "🚫 Forbidden Links (403 Forbidden)",
            "invalid": "❌ Invalid Links (404 or request failed)",
            "client_error": "⚠️ Client Error Links (4xx)",
            "server_error": "💥 Server Error Links (5xx)",
            "unknown": "❓ Unknown Links (Other codes)",
        }

        for category, links in categorized_links.items():
            if links:
                report += f"\n{category_titles.get(category, category)}:\n"
                for link, indicator in links:
                    report += f"  {indicator} {link}\n"

        return report