class TypographyAnalyzer:
    """Extracts font sizes and contrast issues from webpage styles."""

    @staticmethod
    def analyze_fonts(soup):
        """Checks for inline styles defining small font sizes and returns location details."""
        issues = []
        
        for tag in soup.find_all(style=True):
            style = tag["style"]
            if "font-size" in style and "px" in style:
                try:
                    font_size = int(style.split("font-size:")[1].split("px")[0].strip())
                    if font_size < 12:
                        issues.append({
                            "Tag": tag.name,
                            "Class": tag.get("class", "N/A"),
                            "Style": style,
                            "Issue": f"Font size too small ({font_size}px, should be at least 12px)"
                        })
                except ValueError:
                    continue  # Skip if font size parsing fails

        return {"Small Font Issues": issues, "Total Small Fonts": len(issues)}

    @staticmethod
    def analyze_contrast(soup):
        """Detects potential low contrast text (text with background color)."""
        issues = []
        
        for tag in soup.find_all(style=True):
            style = tag["style"]
            if "color" in style and "background-color" in style:
                issues.append({
                    "Tag": tag.name,
                    "Class": tag.get("class", "N/A"),
                    "Style": style,
                    "Issue": "Potential low contrast text detected"
                })

        return {"Contrast Issues": issues, "Total Contrast Issues": len(issues)}