from dotenv import load_dotenv
import os
import json
from dkg import DKG
from dkg.providers import BlockchainProvider, NodeHTTPProvider

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

info_result = dkg.node.info


def print_json(json_dict: dict):
    print(json.dumps(json_dict, indent=4))


ual = "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/38385"
ual_list = [
    "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/38385",
    "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/38250",
    "did:dkg:gnosis:100/0xf81a8c0008de2dcdb73366cf78f2b178616d11dd/38246"
]

get_asset_result = dkg.asset.get(ual)

print(get_asset_result)