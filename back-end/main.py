from flask import Flask, request, jsonify
from flask_cors import CORS
from test_options import TestOptions
from reporter import create_report
from flask import send_file
import os
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/start-test', methods=['POST'])
def start_test():
    data = request.json
    url = data.get("url")
    selected_tests = data.get("tests", {})

    test_results = {test: selected_tests.get(test, False) for test in TestOptions.OPTIONS}

    try:
        # Create the report (Word document)
        doc_buffer = create_report(url, test_results)

        # Return the Word document first
        return send_file(
            doc_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'{url.replace("://", "_").replace("/", "_")}_report.docx'
        )
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to generate report"
        }), 500


@app.route('/download-qa-report', methods=['GET'])
def download_qa_report():
    qa_report_path = os.path.join(os.getcwd(), 'QA_report.txt')
    
    if not os.path.exists(qa_report_path):
        return jsonify({"error": "QA_report.txt not found"}), 404

    try:
        return send_file(
            qa_report_path,
            mimetype='text/plain',
            as_attachment=True,
            download_name='QA_report.txt'
        )
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to download QA_report.txt"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
