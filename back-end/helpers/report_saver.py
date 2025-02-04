def save_report(report, filename: str = "accessibility_report.txt") -> None:
        """Replaces print with writing the report to a file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)
        print(f"✅ Report saved to {filename}")