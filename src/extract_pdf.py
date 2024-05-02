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

    def save_json_to_folder(self, json_data, folder_path):
        os.makedirs(folder_path, exist_ok=True)
        base_filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
        file_path = os.path.join(folder_path, f"{base_filename}.json")
        with open(file_path, "w") as json_file:
            json_file.write(json_data)


# extractor = UnstructuredPDFExtractor('path/to/your/pdf')
# json_output = extractor.process_pdf()
# folder_path = "path/to/save/json"  # Specify your desired folder path
# extractor.save_json_to_folder(json_output, folder_path)
# print(f"JSON output saved successfully to {folder_path}")
