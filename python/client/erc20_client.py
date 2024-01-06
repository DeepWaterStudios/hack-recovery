from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress, HexStr
from web3 import Web3
from web3.types import Wei

from client.web3_client import Web3Client
from deployment.contracts import erc20_abi


class ERC20Client(Web3Client):
    def __init__(self, provider: Web3, account: LocalAccount, address: ChecksumAddress):
        super().__init__(provider, account)
        self.contract = self.w3.eth.contract(address=address, abi=erc20_abi())

    def balance_of(self, account: ChecksumAddress) -> Wei:
        return self.contract.functions.balanceOf(account).call()

    def approve(self, spender: ChecksumAddress, amount: Wei) -> HexStr:
        cf = self.contract.functions.approve(spender, amount)
        cf.call({'from': self.account.address})
        tx = self.build_contract_tx(cf)
        return self.sign_and_send_tx(tx)

    def transfer(self, recipient: ChecksumAddress, amount: Wei) -> HexStr:
        cf = self.contract.functions.transfer(recipient, amount)
        # cf.call({'from': self.account.address})
        tx = self.build_contract_tx(cf)
        return self.sign_and_send_tx(tx)
