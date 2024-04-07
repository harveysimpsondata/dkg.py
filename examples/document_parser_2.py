import os
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.partition.pdf import partition_pdf
import json
import unicodedata
import fitz  # PyMuPDF
import base64


#Unstructured API
load_dotenv()
API_KEY = os.getenv('UNSTRUCTURED_API')
UNSTRUCTURED_URL = os.getenv('UNSTRUCTURED_URL')

s = UnstructuredClient(api_key_auth=API_KEY, server_url=UNSTRUCTURED_URL)


filename = os.path.join(os.path.dirname(__file__), '..', 'pdfs', 'Verifiable_Internet_for_Artificial_Intelligence_whitepaper.pdf')

with open(filename, "rb") as f:

    files = shared.Files(
        content=f.read(),
        file_name=filename,
    )

# req = shared.PartitionParameters(
#
#     files=files,
#     # Other partition params
#     #chunking_strategy='by_title',
#     strategy='hi_res',
#     languages=["eng"],
#     extract_image_block_types=["image", "table"],
#     hi_res_model_name='yolox',
#     pdf_infer_table_structure=True
#
# )

partition_pdf(
    filename=filename,                  # mandatory
    strategy="hi_res",                                     # mandatory to use ``hi_res`` strategy
    extract_images_in_pdf=True,                            # mandatory to set as ``True``
    extract_image_block_types=["Image", "Table"],          # optional
    extract_image_block_to_payload=True,                  # optional
    #extract_image_block_output_dir="path/to/save/images",  # optional - only works when ``extract_image_block_to_payload=False``
    )