import os
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
import json
from unidecode import unidecode
import fitz  # PyMuPDF
import base64


load_dotenv()
API_KEY = os.getenv('UNSTRUCTURED_API')
UNSTRUCTURED_URL = os.getenv('UNSTRUCTURED_URL')

s = UnstructuredClient(api_key_auth=API_KEY, server_url=UNSTRUCTURED_URL)

filename = os.path.join(os.path.dirname(__file__), '..', 'data/pdfs', 'Verifiable_Internet_for_Artificial_Intelligence_whitepaper.pdf')

with open(filename, "rb") as f:

    # Note that this currently only supports a single file
    files = shared.Files(
        content=f.read(),
        file_name=filename,
    )

req = shared.PartitionParameters(
    files=files,
    include_page_breaks=False,
    # Other partition params
    #chunking_strategy='by_title',
    strategy='hi_res',
    languages=["eng"],
    extract_image_block_types=["Image", "Table"],
    hi_res_model_name='yolox',
    pdf_infer_table_structure=True
)

try:
    resp = s.general.partition(req)
    normalized_elements = resp.elements  # Assume resp.elements is a list of dictionaries

    # Remove filename, filetype, and languages from each element's metadata
    for element in normalized_elements:
        if 'metadata' in element:
            element['metadata'].pop('filename', None)  # Remove filename if exists
            element['metadata'].pop('filetype', None)  # Remove filetype if exists
            element['metadata'].pop('languages', None)  # Remove languages if exists

    # If you want to print the entire response
    print(json.dumps(normalized_elements, indent=4))
except SDKError as e:
    print(e)


