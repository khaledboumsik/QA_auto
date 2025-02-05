from flask import Flask, request, send_file
from io import BytesIO
import openai
import os
from dotenv import load_dotenv
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from abc import ABC, abstractmethod

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dependency Injection for OpenAI Service
class TextGenerator(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int) -> str:
        pass

class OpenAITextGenerator(TextGenerator):
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

# Document creation service
class DocumentCreator:
    def create_document(self, content: str) -> BytesIO:
        doc = Document()
        sections = content.split("\n\n")
        
        for section in sections:
            self._add_section_to_document(doc, section)
        
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
    
    def _add_section_to_document(self, doc: Document, section: str):
        if section.startswith("# "):
            doc.add_heading(section[2:], level=1)
        elif section.startswith("## "):
            doc.add_heading(section[3:], level=2)
        elif "|" in section:
            self._add_table(doc, section)
        else:
            doc.add_paragraph(section)
    
    def _add_table(self, doc: Document, section: str):
        rows = section.strip().split("\n")
        num_columns = len(rows[0].split("|")) - 2
        table = doc.add_table(rows=1, cols=num_columns)
        table.style = "Table Grid"

        hdr_cells = table.rows[0].cells
        headers = rows[0].split("|")[1:-1]
        for i, header in enumerate(headers):
            hdr_cells[i].text = header.strip()

        for row in rows[2:]:
            cells = row.split("|")[1:-1]
            row_cells = table.add_row().cells
            for i, cell in enumerate(cells):
                row_cells[i].text = cell.strip()

# Flask Application Setup
app = Flask(__name__)
text_generator = OpenAITextGenerator()
document_creator = DocumentCreator()

@app.route('/start-test', methods=['POST'])
def handle_test():
    data = request.get_json()
    url = data.get('url')
    tests = data.get('tests', {})
    
    if not url or not isinstance(tests, dict):
        return {"error": "Invalid input."}, 400
    
    active_tests = [test for test, selected in tests.items() if selected]
    if not active_tests:
        return {"error": "No tests selected."}, 400
    
    prompt = f"Generate comprehensive website analysis report for {url} covering: {', '.join(active_tests)}. Include detailed findings and recommendations."
    content = text_generator.generate_text(prompt)
    doc_buffer = document_creator.create_document(content)
    
    return send_file(
        doc_buffer,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='website_analysis_report.docx'
    )
