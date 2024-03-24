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
nvidia_api=os.getenv('NVIDIA_API')


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
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = nvidia_api
)

instruction_message = '''
Your task is the following:

Construct a JSON object following the Product JSON-LD schema based on the provided information by the user.
The user will provide the name, description, tags, category and deployer of the product, as well as the URL which you will use as the '@id'.

Here's an example of an Product that corresponds to the mentioned JSON-LD schema.:
{
  "@context": "http://schema.org",
  "@type": "Product",
  "@id": "https://build.nvidia.com/nvidia/ai-weather-forecasting",
  "name": "ai-weather-forecasting",
  "description": "AI-based weather prediction pipeline with global models and downscaling models.",
  "tags": [
    "ai weather prediction",
    "climate science"
  ],
  "category": "Industrial",
  "deployer": "nvidia"
}

Follow the provided JSON-LD schema, using the provided properties and DO NOT add or remove any one of them.
Output the JSON as a string, between ```json and ```.
'''

chat_history = [{"role":"system","content":instruction_message}]


user_instruction = '''I want to create a product (model) with name 'rerank-qa-mistral-4b', which is a GPU-accelerated model optimized for providing a probability score
that a given passage contains the information to answer a question. It's in category Retrieval and deployed by nvidia.
It's used for ranking and retrieval augmented generation. You can reach it at https://build.nvidia.com/nvidia/rerank-qa-mistral-4b. Give me the schema JSON LD object.'''


completion = client.chat.completions.create(
  model="google/gemma-7b",
  messages=chat_history + [{"role":"user","content":user_instruction}],
  temperature=0,
  top_p=1,
  max_tokens=1024,
)

generated_json = completion.choices[0].message.content
print(generated_json)


def clean_json_string(input_string):
    if input_string.startswith("```json") and input_string.endswith("```"):
        cleaned_query = input_string[7:-3].strip()
        return cleaned_query
    elif input_string.startswith("```") and input_string.endswith("```"):
        cleaned_query = input_string[3:-3].strip()
    else:
        return input_string

product = json.loads(clean_json_string(generated_json))

content = {"public": product}
create_asset_result = dkg.asset.create(content, 2)
print('Asset created!')
print(json.dumps(create_asset_result, indent=4))
print(create_asset_result["UAL"])

get_asset_result = dkg.asset.get(create_asset_result["UAL"])
print(json.dumps(get_asset_result, indent=4))



all_categories = ["Biology", "Gaming", "Visual Design", "Industrial", "Reasoning", "Retrieval", "Speech"];
all_tags = ["3d-generation", "automatic speech recognition", "chat", "digital humans", "docking", "drug discovery", "embeddings", "gaming", "healthcare", "image generation", "image modification", "image understanding", "language generation", "molecule generation", "nvidia nim", "protein folding", "ranking", "retrieval augmented generation", "route optimization", "text-to-3d", "advanced reasoning", "ai weather prediction", "climate science"];

instruction_message = '''
You have access to data connected to the new NVIDIA Build platform and the products available there.
You have a schema in JSON-LD format that outlines the structure and relationships of the data you are dealing with.
Based on this schema, you need to construct a SPARQL query to retrieve specific information from the NVIDIA products dataset that follows this schema.

The schema is focused on AI products and includes various properties such as name, description, category, deployer, URL and tags related to the product.
My goal with the SPARQL queries is to retrieve data from the graph about the products, based on the natural language question that the user posed.

Here's an example of a query to find products from category "AI Weather Prediction":
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?product ?name ?description ?ual

WHERE { ?product a schema:Product ;
GRAPH ?g
{ ?product schema:tags "ai weather prediction" ; schema:name ?name ; schema:description ?description }

?ual schema:assertion ?g
FILTER(CONTAINS(str(?ual), "20430")) }```

Pay attention to retrieving the UAL, this is a mandatory step of all your queries. After getting the product with '?product a schema:Product ;' you should wrap the next conditions around GRAPH ?g { }, and later use the graph retrieved (g) to get the UAL like in the example above.

Make sure you ALWAYS retrieve the UAL no matter what the user asks for and filter whether it contains "2043".
Make sure you always retrieve the NAME and the DESCRIPTION of the products.

Only return the SPARQL query wrapped in ```sparql ``` and DO NOT return anything extra.
'''

limitations_instruction = '''\nThe existing categories are: {}. The existing tags are: {}'''.format(all_categories, all_tags)
user_instruction = '''Give me all NVIDIA tools which I can use for use cases related to biology.'''

chat_history = [{"role":"system","content":instruction_message + limitations_instruction}, {"role":"user","content":user_instruction}]

limitations_instruction = '''\nThe existing categories are: {}. The existing tags are: {}'''.format(all_categories, all_tags)
user_instruction = '''Give me all NVIDIA tools which I can use for use cases related to biology.'''

chat_history = [{"role":"system","content":instruction_message + limitations_instruction}, {"role":"user","content":user_instruction}]

completion = client.chat.completions.create(
  model="meta/llama2-70b", # NVIDIA lets you choose any LLM from the platform
  messages=chat_history,
  temperature=0,
  top_p=1,
  max_tokens=1024,
)

answer = completion.choices[0].message.content
print(answer)


def clean_sparql_query(input_string):
    start_index = input_string.find("```sparql")
    end_index = input_string.find("```", start_index + 1)
    if start_index != -1 and end_index != -1:
        cleaned_query = input_string[start_index + 9:end_index].strip()
        return cleaned_query
    else:
        return input_string

query = clean_sparql_query(answer)
print(query)

