import os
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
import json


class UnstructuredPDFExtractor:
    def __init__(self, pdf_path):
        load_dotenv()
        self.pdf_path = pdf_path
        self.API_KEY = os.getenv('UNSTRUCTURED_API')
        self.UNSTRUCTURED_URL = os.getenv('UNSTRUCTURED_URL')
        self.client = UnstructuredClient(api_key_auth=self.API_KEY, server_url=self.UNSTRUCTURED_URL)

    def process_pdf(self):
        try:
            with open(self.pdf_path, "rb") as f:
                files = shared.Files(
                    content=f.read(),
                    file_name=self.pdf_path,
                )

            req = shared.PartitionParameters(
                files=files,
                strategy='hi_res',
                languages=["eng"],
                extract_image_block_types=["Image", "Table"],
                hi_res_model_name='yolox',
                pdf_infer_table_structure=True
            )

            resp = self.client.general.partition(req)
            normalized_elements = resp.elements  # Assume resp.elements is a list of dictionaries

            # Remove unwanted metadata from each element
            for element in normalized_elements:
                if 'metadata' in element:
                    element['metadata'].pop('filename', None)
                    element['metadata'].pop('filetype', None)
                    element['metadata'].pop('languages', None)

            # Convert the cleaned data to JSON
            return json.dumps(normalized_elements, indent=4)
        except SDKError as e:
            return json.dumps({'error': str(e)})

# Usage example
# extractor = UnstructuredPDFExtractor('path/to/your/pdf')
# json_output = extractor.process_pdf()
# print(json_output)
