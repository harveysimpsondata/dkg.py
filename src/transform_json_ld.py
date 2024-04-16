import os
import json
from dotenv import load_dotenv
from openai import OpenAI


class JSONLDTransformer:
    def __init__(self):
        load_dotenv()
        nvidia_api = os.getenv('NVIDIA_API')
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nvidia_api
        )
        self.instruction_message = '''
        Your task is the following:

        Transform the structured output from PDF extraction into a JSON-LD object that adheres to a schema suitable for representing knowledge assets in the Decentralized Knowledge Graph (DKG). The schema should capture essential elements of the extracted content, such as titles, main text, authors, publication dates, and any associated metadata.
        '''

    def transform_to_jsonld(self, extracted_json):
        chat_history = [{"role": "system", "content": self.instruction_message}]
        user_instruction = f'''Based on the output from the PDF extraction process, create a JSON-LD object for each document, adhering to the provided schema. Consider each piece of extracted information, such as document titles, text bodies, metadata including author names, publication dates, and any identifiable publisher information, and map these to the appropriate JSON-LD structure.

        Extracted JSON: {extracted_json}
        '''

        completion = self.client.chat.completions.create(
            model="google/gemma-7b",
            messages=chat_history + [{"role": "user", "content": user_instruction}],
            temperature=0,
            top_p=1,
            max_tokens=1024
        )

        generated_json_ld = completion.choices[0].message.content
        return generated_json_ld

# Usage example
# transformer = JSONLDTransformer()
# extracted_json = '{"title": "Example Document", "author": "John Doe", "text": "This is an example text."}'
# json_ld_output = transformer.transform_to_jsonld(extracted_json)
# print(json_ld_output)
