from dotenv import load_dotenv
import os
import json
from dkg import DKG
from dkg.providers import BlockchainProvider, NodeHTTPProvider
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

load_dotenv()

node_hostname = os.getenv('NODE_HOSTNAME')
node_port = os.getenv('NODE_PORT')
rpc_uri = os.getenv('GNOSIS_URI')
private_key = os.getenv('PRIVATE_KEY')


node_provider = NodeHTTPProvider(f"http://{node_hostname}:{node_port}")
blockchain_provider = BlockchainProvider(
    "mainnet",
    "gnosis",
    rpc_uri=rpc_uri,
    private_key=private_key,
)

dkg = DKG(node_provider, blockchain_provider)

ual = "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/32000"
ual = "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/38957"
ual = "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/38955"
ual = "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/33175"
ual = "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/82904"

# Explicitly setting the output format to 'JSON-LD'
get_asset_result = dkg.asset.get(ual, output_format="JSON-LD")

#print(json.dumps(get_asset_result, indent=4))

get_asset_result = get_asset_result['public']['assertion']


def convert_turtle_to_jsonld(turtle_data):
    g = Graph()
    g.parse(data=turtle_data, format='turtle')

    # Serialize the graph to JSON-LD
    jsonld_data = g.serialize(format='json-ld', indent=4)
    return jsonld_data


jsonld_output = convert_turtle_to_jsonld(get_asset_result)
print(jsonld_output)