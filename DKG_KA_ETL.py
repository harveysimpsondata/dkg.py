
from src.extract_pdf import *
from src.transform_json_ld import *
from src.upload_dkg import *


extractor = UnstructuredPDFExtractor('data/pdfs/Verifiable_Internet_for_Artificial_Intelligence_whitepaper.pdf')
json_output = extractor.process_pdf()
print(json_output)