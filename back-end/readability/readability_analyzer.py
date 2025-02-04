import textstat

class ReadabilityAnalyzer:
    """Analyzes the readability of webpage text."""

    @staticmethod
    def get_readability_score(text):
        """Returns the Flesch-Kincaid readability score."""
        if len(text.split()) < 50:  # Avoid incorrect calculations on short text
            return "Not enough text to analyze"
        return textstat.flesch_reading_ease(text)

    @staticmethod
    def get_text_statistics(text):
        """Returns basic readability statistics."""
        return {
            "Flesch Reading Ease": ReadabilityAnalyzer.get_readability_score(text),
            "Number of Words": textstat.lexicon_count(text),
            "Number of Sentences": textstat.sentence_count(text),
        }
