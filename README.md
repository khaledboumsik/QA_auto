# Website Testing Tool

## Overview

This project is a **website testing tool** that analyzes a website using only its URL, without requiring access to the source code. It performs the following tests:

- **Broken Link Detection**: Uses web scraping and HTTP request codes to detect broken links.
- **Performance Testing**: Utilizes the Lighthouse API to evaluate website performance.
- **Readability & Typography Analysis**: Uses web scraping and natural language processing to assess readability and typography.
- **Accessibility Testing**: Checks website accessibility through web scraping.
- **AI-Powered Reports**: Integrates OpenAI to generate detailed test reports and provides an AI agent for interactive discussions.

## Prerequisites

- **Backend Requirements:**
  - Python 3.8+
  - Virtual Environment (`venv`)
  - OpenAI API Key
  - Google PageSpeed Insights API Key

- **Frontend Requirements:**
  - Node.js (v18+)
  - Next.js
  - React

## Installation

### Backend Setup (Python & Flask)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/khaledboumsik/QA_auto.git
   cd QA_auto/backend
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup API Keys in a `.env` File:**
   Create a `.env` file in the `backend` directory with the following content:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_PAGESPEED_API_KEY=your_google_pagespeed_api_key
   ```

5. **Run the Backend Server:**
   ```bash
   python main.py
   ```

   The backend should now be running on `http://127.0.0.1:5000`.
### Backend file breakdown:

**link_detector Directory:**

1- link_checker: verifies the status code of a given URL  
2- link_fetcher: collects all the URLs inside a given URL based on href  
3- report_generator: generates a report based on the URL and its status and the way it is constructed  

**readability Directory:**

1- readability_analyzer: utilizes the textstat library to get metrics like (Flesch Reading Ease / Number of Words / Number of Sentences)  
2- typography_analyzer: responsible for the detection of the font size and analysis of the contrast  

**Main Directory:**

1- broken_link_detector: utilizes all the logic inside the link_detector directory to generate a general report about link validation  
2- html_bug_detector: responsible for detecting missing alt tags in images and links; it also detects missing name tags in various other types of elements  
3- performance: utilizes the PAGE_SPEED_INSIGHTS_API to run Lighthouse on the provided website to detect scores relevant to the performance of the website like  
(Performance Score / Accessibility Score / SEO Score) and many more  
4- style_analyzer: similar to the typography_analyzer but focuses only on color contrast using a different method to ensure the problem is caught  
5- test_options: contains the options that the system can have when running the analysis  
6- web_page_analyzer: utilizes the files inside the readability directory to generate a report  
7- web_scraper: responsible for the extraction of HTML pages from the website and the filtering of relevant information  
8- openai_api: integrates with the OpenAI API to prompt the model to generate a detailed report and has the capability of generating a Word document for the client to download  
9- main: this is our API endpoint; you run the program from here  

**API Documentation:**  
Currently, there is only 1 API for the generation of the response.  
The input should be the website URL with the list of the options that need analysis. For example:  

**Input:**  
```json
{
  "url": "website_example.com",
  "tests": {
    "Broken Link Detection": true,
    "Performance Testing": true,
    "Readability & Typography Analysis": false,
    "Accessibility Testing": false
  }
}

### Frontend Setup (Next.js & React)

1. **Navigate to the Frontend Directory:**
   ```bash
   cd ../frontend
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Run the Development Server:**
   ```bash
   npm run dev
   ```

   The frontend should now be running on `http://localhost:3000`.

## Using Environment Variables in Python

In the Python backend, the `.env` file is used to store API keys securely. The project reads these keys using `os.getenv`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access API keys
openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_PAGESPEED_API_KEY")

print(f"OpenAI Key: {openai_key}")  # Should print the key if loaded correctly
### API Documentation
Endpoint:
POST /start-test

Description:
This endpoint accepts a website URL and a list of selected tests to perform. It generates a report based on the selected tests and returns a downloadable Word document.

Request Body:
```

{
  "url": "https://example.com",
  "tests": {
    "Broken Link Detection": true,
    "Performance Testing": false,
    "Readability & Typography Analysis": true,
    "Accessibility Testing": false
  }
}
```
## Features & Future Improvements

- **Current Features:**
  - Website analysis through URL input
  - AI-powered reports
  - Interactive AI agent (still needs memory integration)

- **Planned Improvements:**
  - Expanded accessibility testing
  - More advanced link validation
  - UI/UX enhancements
  - Integrating memory based on the report generated
## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
