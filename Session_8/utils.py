```python
# utils.py

import os
import uuid
import logging
from flask import current_app
from werkzeug.utils import secure_filename
from flask import request
from flask import jsonify
from werkzeug.exceptions import BadRequest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """
    Check if the file is allowed to be uploaded.
    
    Args:
    filename (str): The name of the file to check.
    
    Returns:
    bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def upload_file(file):
    """
    Upload a file to the server.
    
    Args:
    file (file): The file to upload.
    
    Returns:
    str: The uploaded file's filename.
    """
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        raise BadRequest('Invalid file')

def generate_uuid():
    """
    Generate a unique identifier.
    
    Returns:
    str: A unique identifier.
    """
    return str(uuid.uuid4())

def get_request_json():
    """
    Get the JSON data from the request.
    
    Returns:
    dict: The JSON data.
    """
    return request.get_json()

def get_request_args():
    """
    Get the arguments from the request.
    
    Returns:
    dict: The arguments.
    """
    return request.args

def jsonify_response(data, status_code=200):
    """
    Create a JSON response.
    
    Args:
    data (dict): The data to include in the response.
    status_code (int): The status code of the response. Defaults to 200.
    
    Returns:
    Response: The JSON response.
    """
    return jsonify(data), status_code
```