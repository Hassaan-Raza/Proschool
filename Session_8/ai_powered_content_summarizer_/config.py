```python
# config.py

import os
import logging
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up AI model and summarization pipeline
model_name = os.getenv('MODEL_NAME', 't5-base')
summarizer = pipeline('summarization', model=model_name)

# Set up export options
export_formats = ['txt', 'pdf', 'docx']
export_path = os.getenv('EXPORT_PATH', './summaries')

# Set up URL input
url_input = os.getenv('URL_INPUT', '')

# Set up text extraction
text_extraction = os.getenv('TEXT_EXTRACTION', 'html')

# Set up AI summarization settings
max_length = int(os.getenv('MAX_LENGTH', 500))
min_length = int(os.getenv('MIN_LENGTH', 100))
do_sample = os.getenv('DO_SAMPLE', 'False').lower() == 'true'
num_beams = int(os.getenv('NUM_BEAMS', 4))
no_repeat_ngram_size = int(os.getenv('NO_REPEAT_NGRAM_SIZE', 2))

# Set up error handling
try:
    # Check if model name is valid
    if model_name not in ['t5-base', 't5-large', 't5-3b', 't5-11b']:
        raise ValueError('Invalid model name')
except ValueError as e:
    logger.error(f'Error: {e}')
    exit(1)

try:
    # Check if export path exists
    if not os.path.exists(export_path):
        os.makedirs(export_path)
except OSError as e:
    logger.error(f'Error: {e}')
    exit(1)
```