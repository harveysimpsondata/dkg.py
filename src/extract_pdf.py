import os
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
import json
class UnstructuredPDFExtractor:
    def __init__(self, pdf_path):

        self.pdf_path = pdf_path
        load_dotenv()
        self.API_KEY = os.getenv('UNSTRUCTURED_API')
        self.UNSTRUCTURED_URL = os.getenv('UNSTRUCTURED_URL')
        self.client = UnstructuredClient(api_key_auth=self.api_key, server_url=self.unstructured_url)
    def process_pdf(self):

        with open(self.pdf_path, "rb") as f:
            files = shared.Files(
                content=f.read(),
                file_name=self.pdf_path,
            )

        req = shared.PartitionParameters(
            files=files,
            strategy='hi_res',
            languages=["eng"],
            extract_image_block_types=["image", "table"],
            hi_res_model_name='yolox',
            pdf_infer_table_structure=True
        )
