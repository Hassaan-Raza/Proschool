```markdown
# AI-Powered Content Summarizer

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Features](#features)
* [Dependencies](#dependencies)
* [Code](#code)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

## Features

* URL input
* Text extraction
* AI summarization
* Export options

## Dependencies

* `flask` for web development
* `beautifulsoup4` for HTML parsing
* `nltk` for natural language processing
* `transformers` for AI summarization
* `pandas` for data manipulation

## Code

```python
import os
import sys
import json
import time
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from transformers import pipeline
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load dependencies
nltk.download('punkt')
nlp = pipeline('summarization')

# Define routes
@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get URL from request
        url = request.json['url']
        
        # Extract text from URL
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        text = soup.get_text()
        
        # Tokenize text
        tokens = word_tokenize(text)
        
        # Summarize text using AI
        summary = nlp(tokens, max_length=100)
        
        # Return summary as JSON
        return jsonify({'summary': summary})
    
    except Exception as e:
        # Handle errors
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export():
    try:
        # Get summary from request
        summary = request.json['summary']
        
        # Save summary to file
        with open('summary.txt', 'w') as f:
            f.write(summary)
        
        # Return success message
        return jsonify({'message': 'Summary exported successfully'})
    
    except Exception as e:
        # Handle errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

```python
# requirements.txt
flask
beautifulsoup4
nltk
transformers
pandas
requests
```

```python
# app.py
import os
import sys
import json
import time
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from transformers import pipeline
import pandas as pd
```

```python
# summary.txt
This is a sample summary.
```

```bash
# Run the app
python app.py
```

```bash
# Test the API
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.example.com"}' http://localhost:5000/summarize
```

```bash
# Export the summary
curl -X POST -H "Content-Type: application/json" -d '{"summary": "This is a sample summary."}' http://localhost:5000/export
```