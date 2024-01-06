from eth_account.datastructures import SignedTransaction
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from eth_typing.encoding import HexStr
from web3 import Web3
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import Nonce, TxParams, TxReceipt, Wei


class Web3Client(object):
    """Generic Web3 client."""

    def __init__(self, provider: Web3, account: LocalAccount):
        self.w3 = provider
        self.account = account

        self.chain_id = self.w3.eth.chain_id
        self.max_gas_in_gwei = 100
        self.max_priority_fee_gwei = 1
        self.gas_limit = 300_000

        self.fixed_nonce = None

    ####################
    # Build Tx
    ####################

    def build_base_tx(self) -> TxParams:
        """Build a basic EIP-1559 transaction."""
        tx: TxParams = {
            'type': 0x2,
            'chainId': self.chain_id,
            'gas': self.gas_limit,
            'maxFeePerGas': Web3.to_wei(self.max_gas_in_gwei, 'gwei'),
            'maxPriorityFeePerGas': Web3.to_wei(self.max_priority_fee_gwei, 'gwei'),
            'nonce': self.next_nonce(),
        }
        return tx

    def build_send_value_tx(self, to: ChecksumAddress, value: Wei) -> TxParams:
        """Build a tx to transfer the blockchain token to an address."""
        tx = self.build_base_tx()
        tx_value: TxParams = {'to': to, 'value': value}
        return tx | tx_value

    def build_contract_tx(self, contract_function: ContractFunction) -> TxParams:
        """Build a transaction that involves a deployment interation."""
        base_tx = self.build_base_tx()
        return contract_function.build_transaction(base_tx)

    def build_contract_tx_value(self, contract_function: ContractFunction, value: Wei) -> TxParams:
        """Build a transaction that involves a deployment interation."""
        base_tx = self.build_base_tx()
        tx_value: TxParams = {'value': value}
        return contract_function.build_transaction(base_tx | tx_value)

    ####################
    # Sign & send Tx
    ####################

    def sign_tx(self, tx: TxParams) -> SignedTransaction:
        """Sign the given transaction."""
        return self.w3.eth.account.sign_transaction(tx, self.account.key)

    def send_signed_tx(self, signed_tx: SignedTransaction) -> HexStr:
        """Send a signed transaction and return the tx hash."""
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def sign_and_send_tx(self, tx: TxParams) -> HexStr:
        """Sign a transaction and send it.

        Just a convenience wrap around the sign_tx/send_signed_tx functions.
        """
        signed_tx = self.sign_tx(tx)
        return self.send_signed_tx(signed_tx)

    ####################
    # Utils
    ####################

    def next_nonce(self) -> Nonce:
        """Requests the next nonce from the server."""
        return self.fixed_nonce or self.w3.eth.get_transaction_count(self.account.address)

    def get_receipt_by_hash(self, tx_hash: HexStr) -> TxReceipt:
        """Given a transaction hash, wait for the blockchain to confirm it and return the tx receipt."""
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_balance(self) -> float:
        """Get the avax balance in avax."""
        return float(Web3.from_wei(self.get_balance_wei(), 'ether'))

    def get_balance_wei(self) -> int:
        """Get the avax balance in wei."""
        return self.w3.eth.get_balance(self.account.address)

    def contract(self, address: ChecksumAddress, abi: str) -> Contract:
        """Generate a contract helper from the address and abi."""
        return self.w3.eth.contract(address=address, abi=abi)

    def send_value(self, to_address: ChecksumAddress, amount: float) -> HexStr:
        """Send avax, in avax."""
        return self.send_value_wei(to_address, Web3.to_wei(amount, 'ether'))

    def send_value_wei(self, to_address: ChecksumAddress, amount: Wei) -> HexStr:
        """Send avax, in wei."""
        raw_tx = self.build_send_value_tx(to_address, amount)
        return self.sign_and_send_tx(raw_tx)
