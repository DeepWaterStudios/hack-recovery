from web3 import Web3
from web3.middleware import geth_poa_middleware

AVAX_NODE = 'https://api.avax.network/ext/bc/C/rpc'


def make_provider(node_uri: str) -> Web3:
    if node_uri.startswith('http'):
        return Web3(Web3.HTTPProvider(node_uri))
    elif node_uri.startswith('ws'):
        return Web3(Web3.WebsocketProvider(node_uri))
    else:
        raise Exception(f'node_uri not valid: {node_uri}')


def make_avax_provider(node_uri: str) -> Web3:
    provider = make_provider(node_uri)
    # Inject the POA middleware
    provider.middleware_onion.inject(geth_poa_middleware, layer=0)
    return provider


def make_mainnet_provider() -> Web3:
    return make_avax_provider(AVAX_NODE)
