from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from test_options import TestOptions

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/start-test', methods=['POST'])
def start_test():
    data = request.json
    url = data.get("url")
    selected_tests = data.get("tests", {})
    
    test_results = {test: selected_tests.get(test, False) for test in TestOptions.OPTIONS}
    print(test_results)
    return jsonify({"url": url, "test_results": test_results})

if __name__ == '__main__':
    app.run(debug=True)
