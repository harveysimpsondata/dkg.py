import os
from dotenv import load_dotenv
import requests
import json
import unicodedata

# Load environment variables from .env file
load_dotenv()

# Retrieve API URL and API KEY from environment variables
API_URL = os.getenv('UNSTRUCTURED_URL')
API_KEY = os.getenv('UNSTRUCTURED_API')

# The path to the file you want to send
pdf_path = os.path.join(os.path.dirname(__file__), '..', 'pdfs', 'uap.pdf')

# Make sure the file exists
if not os.path.exists(pdf_path):
    print(f"The file {pdf_path} does not exist.")
    exit(1)

# Open the PDF file and send it in the request
with open(pdf_path, 'rb') as f:
    files = {'files': f}
    headers = {
        'accept': 'application/json',
        'unstructured-api-key': API_KEY
    }
    response = requests.post(API_URL, headers=headers, files=files)

# Assuming response is JSON, parse it
data = json.loads(response.text)

def normalize_text(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'text' and isinstance(value, str):
                normalized_value = unicodedata.normalize('NFKC', value)
                # Replace specific Unicode characters with their desired representation
                replaced_value = normalized_value.replace('\u2248', '≈')
                # Example: Replace \u00b1 with "±"
                replaced_value = replaced_value.replace('\u00b1', '±')
                # Example for additional replacements: Replace \u2019 with a straight apostrophe
                replaced_value = replaced_value.replace('\u2019', "'")
                data[key] = replaced_value
            else:
                normalize_text(value)
    elif isinstance(data, list):
        for item in data:
            normalize_text(item)

# Normalize the text in the response
normalize_text(data)

# Print the normalized data
print(json.dumps(data, indent=4))
