import os

from web3 import Web3


def load_web3_file(filename: str) -> str:
    dirname = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dirname, 'files', filename)
    with open(path, 'r') as f:
        return f.read()


def erc20_abi():
    return load_web3_file('erc20.abi')


WAVAX_ADDRESS = Web3.to_checksum_address('0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7')
