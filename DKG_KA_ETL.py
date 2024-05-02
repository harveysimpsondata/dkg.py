
from src.extract_pdf import *
from src.transform_json_ld import *
from src.upload_dkg import *


# EXTRACT text from PDF file

extractor = UnstructuredPDFExtractor('data/pdfs/Verifiable_Internet_for_Artificial_Intelligence_whitepaper.pdf')
json_output = extractor.process_pdf()
print(json_output)

folder_path = "data/jsons/"  # Specify your desired folder path
extractor.save_json_to_folder(json_output, folder_path)
print(f"JSON output saved successfully to {folder_path}")