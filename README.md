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
   git clone https://github.com/your-username/website-testing-tool.git
   cd website-testing-tool/backend
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
   flask run
   ```

   The backend should now be running on `http://127.0.0.1:5000`.

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
```

## Features & Future Improvements

- **Current Features:**
  - Website analysis through URL input
  - AI-powered reports
  - Interactive AI agent

- **Planned Improvements:**
  - Expanded accessibility testing
  - More advanced link validation
  - UI/UX enhancements

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
