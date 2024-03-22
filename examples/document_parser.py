import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve API URL and API KEY from environment variables
API_URL = os.getenv('UNSTRUCTURED_URL')
API_KEY = os.getenv('UNSTRUCTURED_API')

# The path to the file you want to send
file_path = 'pdfs/recipe.pdf'

# Make sure the file exists
if not os.path.exists(file_path):
    print(f"The file {file_path} does not exist.")
    exit(1)

files = {'files': open(file_path, 'rb')}

headers = {
    'accept': 'application/json',
    'unstructured-api-key': API_KEY
}

response = requests.post(API_URL, headers=headers, files=files)

# Print the response from the server
print(response.text)