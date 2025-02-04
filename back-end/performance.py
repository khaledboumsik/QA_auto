import requests
import os
PAGE_SPEED_INSIGHTS_API_KEY=os.getenv("PAGE_SPEED_INSIGHTS_API_KEY") 

class LighthouseAPI:
    """Handles API calls to Google PageSpeed Insights for Lighthouse data."""
    
    BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_lighthouse_data(self, url):
        """Fetch performance metrics from Google PageSpeed Insights API."""
        api_url = f"{self.BASE_URL}?url={url}&key={self.api_key}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data.get("lighthouseResult", {})
        
        return {"error": "Failed to fetch Lighthouse data"}


class LighthouseService:
    """Processes and extracts relevant Lighthouse metrics."""
    
    def __init__(self, api_client):
        self.api_client = api_client

    @staticmethod
    def safe_get(data, key, default="N/A"):
        """Safely extract a metric from Lighthouse audits and clean up Unicode spaces."""
        value = data.get(key, {}).get("displayValue", default)
        return value.replace("\u00a0", " ") if isinstance(value, str) else value

    def process_results(self, lighthouse_data):
        """Extracts useful metrics from Lighthouse API response."""
        if "error" in lighthouse_data:
            return lighthouse_data  # Return error message if API call failed

        categories = lighthouse_data.get("categories", {})
        audits = lighthouse_data.get("audits", {})

        return {
            "Performance Score": categories.get("performance", {}).get("score", 0) * 100,
            "Accessibility Score": categories.get("accessibility", {}).get("score", 0) * 100,
            "Best Practices Score": categories.get("best-practices", {}).get("score", 0) * 100,
            "SEO Score": categories.get("seo", {}).get("score", 0) * 100,
            "PWA Score": categories.get("pwa", {}).get("score", "N/A"),

            # Performance metrics
            "First Contentful Paint": self.safe_get(audits, "first-contentful-paint"),
            "Largest Contentful Paint": self.safe_get(audits, "largest-contentful-paint"),
            "Cumulative Layout Shift": self.safe_get(audits, "cumulative-layout-shift"),
            "Speed Index": self.safe_get(audits, "speed-index"),
            "Time to Interactive": self.safe_get(audits, "interactive"),
            "Total Blocking Time": self.safe_get(audits, "total-blocking-time"),

            # Accessibility details
            "Color Contrast Issues": audits.get("color-contrast", {}).get("score", "N/A"),
            "Image Alt Attributes": audits.get("image-alt", {}).get("score", "N/A"),

            # Best Practices
            "Uses HTTPS": audits.get("is-on-https", {}).get("score", "N/A"),
            "No Vulnerable Libraries": audits.get("no-vulnerable-libraries", {}).get("score", "N/A"),

            # SEO details
            "Mobile Friendly": audits.get("viewport", {}).get("score", "N/A"),
            "Title Element": audits.get("document-title", {}).get("score", "N/A"),

            # PWA checks (if applicable)
            "Service Worker": audits.get("service-worker", {}).get("score", "N/A"),
            "Offline Support": audits.get("works-offline", {}).get("score", "N/A")
        }


def output_performance(url):
    """Main function to fetch and display Lighthouse metrics."""
    print(f"\n🔍 Fetching full Lighthouse report for {url}...\n")
    
    api_client = LighthouseAPI(PAGE_SPEED_INSIGHTS_API_KEY)
    service = LighthouseService(api_client)

    raw_data = api_client.fetch_lighthouse_data(url)
    results = service.process_results(raw_data)

    return results

