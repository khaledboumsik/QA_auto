from flask import Flask, request, jsonify
from flask_cors import CORS
from test_options import TestOptions
from reporter import create_report
from flask import send_file
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
from flask import make_response

@app.route('/start-test', methods=['POST'])
def start_test():
    try:
        data = request.get_json()
        url = data.get("url")
        selected_tests = data.get("tests", {})
        
        test_results = {test: selected_tests.get(test, False) 
                      for test in TestOptions.OPTIONS}
        
        doc_buffer = create_report(url, test_results)
        
        response = make_response(doc_buffer.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response.headers['Content-Disposition'] = \
            f'attachment; filename={url.replace("://", "_").replace("/", "_")}_report.docx'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        
        return response
        
    except Exception as e:
        app.logger.error(f"Error generating report: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
