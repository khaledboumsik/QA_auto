from typing import Dict, List, Optional
from webcolors import name_to_rgb
from wcag_contrast_ratio import rgb, contrast
class StyleAnalyzer:
    @staticmethod
    def extract_colors(style: Optional[str], computed_styles: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        colors = {}
        
        # First, try extracting colors from inline styles
        if style:
            for prop in style.split(";"):
                if ":" in prop:
                    key, value = prop.split(":", 1)
                    key, value = key.strip().lower(), value.strip().lower()
                    if key in ["color", "background-color", "background"]:
                        colors[key] = value
        
        # If no inline style was provided, try extracting from computed styles
        if not colors and computed_styles:
            for key in ["color", "background-color", "background"]:
                if key in computed_styles:
                    colors[key] = computed_styles[key]
        
        return colors
    
    @staticmethod
    def calculate_contrast(color1: str, color2: str) -> Optional[float]:
        try:
            rgb1 = name_to_rgb(color1)
            rgb2 = name_to_rgb(color2)
            return contrast(rgb(*rgb1), rgb(*rgb2))
        except ValueError:
            return None

class AccessibilityChecker:
    INTERACTIVE_TAGS = {"a", "button", "input", "textarea", "select", "details"}
    NON_FOCUSABLE_TAGS = {"div", "span", "p", "section"}
    
    @staticmethod
    def check_keyboard_accessibility(element: Dict) -> List[str]:
        issues = []
        if element["tag"] in AccessibilityChecker.INTERACTIVE_TAGS:
            if element["aria_hidden"] == "true":
                issues.append("❌ `aria-hidden='true'` on an interactive element: Prevents keyboard access.")
            if element["tabindex"] and element["tabindex"].isdigit() and int(element["tabindex"]) < 0:
                issues.append("❌ `tabindex='-1'`: Removes from keyboard navigation.")
        if element["tag"] in AccessibilityChecker.NON_FOCUSABLE_TAGS and element["tabindex"] is None:
            issues.append("⚠️ Consider adding `tabindex='0'` for keyboard accessibility.")
        if element["style"] and "outline: none" in element["style"].replace(" ", ""):
            issues.append("❌ Focus indicator removed (`outline: none`). Hinders keyboard navigation.")
        return issues