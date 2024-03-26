import json
from dotenv import load_dotenv
import os
from dkg import DKG
from dkg.providers import BlockchainProvider, NodeHTTPProvider
from openai import OpenAI



load_dotenv()

node_hostname = os.getenv('NODE_HOSTNAME')
node_port = os.getenv('NODE_PORT')
rpc_uri = os.getenv('GNOSIS_URI')
private_key = os.getenv('PRIVATE_KEY')
nvidia_api = os.getenv('NVIDIA_API')


node_provider = NodeHTTPProvider(f"http://{node_hostname}:{node_port}")
blockchain_provider = BlockchainProvider(
    "mainnet",
    "gnosis",
    rpc_uri=rpc_uri,
    private_key=private_key,
)

dkg = DKG(node_provider, blockchain_provider)
info_result = dkg.node.info


def print_json(json_dict: dict):
    print(json.dumps(json_dict, indent=4))


print("======================== NODE INFO RECEIVED")
print_json(info_result)

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key=nvidia_api
)

instruction_message = '''
Your task is the following:

Transform the structured output from PDF extraction into a JSON-LD object that adheres to a schema suitable for representing knowledge assets in the Decentralized Knowledge Graph (DKG). The schema should capture essential elements of the extracted content, such as titles, main text, authors, publication dates, and any associated metadata.

Here's an example schema for a knowledge asset extracted from a PDF document:
{
  "@context": "http://schema.org",
  "@type": "Article",
  "@id": "Unique_Identifier_URL",
  "name": "Title of the Article",
  "author": {
    "@type": "Person",
    "name": "Author's Name"
  },
  "datePublished": "Publication Date",
  "description": "Short description or abstract of the article",
  "articleBody": "Main text content of the article",
  "publisher": {
    "@type": "Organization",
    "name": "Publisher's Name"
  }
}

Ensure to accurately map the extracted content to the corresponding properties in the JSON-LD schema. Each property is crucial for representing the knowledge asset within the DKG. DO NOT omit any property from the schema, and ensure all textual content is well-formatted and normalized.
'''

chat_history = [{"role":"system","content":instruction_message}]

user_instruction = '''Based on the output from the PDF extraction process, create a JSON-LD object for each document, adhering to the provided schema. Consider each piece of extracted information, such as document titles, text bodies, metadata including author names, publication dates, and any identifiable publisher information, and map these to the appropriate JSON-LD structure.

For example, if processing a whitepaper on "Artificial Intelligence Trends" authored by "Jane Doe" and published in "2023", your task is to fill the schema with this information, ensuring a clear, accurate representation of the knowledge asset. The '@id' should be a unique identifier that could be constructed from the document's metadata or a URL where the document or its representation is stored.

Remember to normalize the text content to maintain consistency in formatting, and replace any special Unicode characters with their closest ASCII equivalents if necessary. This ensures the JSON-LD object is cleanly formatted and universally readable.
'''

completion = client.chat.completions.create(
  model="google/gemma-7b",
  messages=chat_history + [{"role":"user","content":user_instruction}],
  temperature=0,
  top_p=1,
  max_tokens=1024,
)

generated_json = completion.choices[0].message.content
print(generated_json)
