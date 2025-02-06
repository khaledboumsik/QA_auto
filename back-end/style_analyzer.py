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
