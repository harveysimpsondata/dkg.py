import os
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
import json
import unicodedata


def normalize_text(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'text' and isinstance(value, str):

                normalized_value = unicodedata.normalize('NFKC', value)

                # Replace specific Unicode characters with their desired representation
                replaced_value = (
                    normalized_value.replace('\u2248', '≈')
                                    .replace('\u00b1', '±')
                                    .replace('\u2019', "'")
                )
                data[key] = replaced_value
            else:
                normalize_text(value)
    elif isinstance(data, list):
        for item in data:
            normalize_text(item)


load_dotenv()
API_KEY = os.getenv('UNSTRUCTURED_API')
UNSTRUCTURED_URL = os.getenv('UNSTRUCTURED_URL')

s = UnstructuredClient(api_key_auth=API_KEY, server_url=UNSTRUCTURED_URL)

filename = os.path.join(os.path.dirname(__file__), '..', 'pdfs', 'uap.pdf')
with open(filename, "rb") as f:

    # Note that this currently only supports a single file
    files = shared.Files(
        content=f.read(),
        file_name=filename,
    )

req = shared.PartitionParameters(
    files=files,
    # Other partition params
    #chunking_strategy='by_title',
    strategy='hi_res',
    languages=["eng"],
    extract_image_block_types=["image", "table"],
    hi_res_model_name='yolox',
    pdf_infer_table_structure=True
)

try:
    resp = s.general.partition(req)
    # Directly serialize resp.elements if it's already in the correct format
    normalized_elements = resp.elements  # Assume resp.elements is a list of dictionaries
    normalize_text(normalized_elements)
    for element in normalized_elements:
        if 'metadata' in element and 'text_as_html' in element['metadata']:
            print("HTML Table Content for element_id", element['element_id'], ":", element['metadata']['text_as_html'])
        else:
            pass

        # If you want to print the entire response
    print(json.dumps(normalized_elements, indent=4))
except SDKError as e:
    print(e)
