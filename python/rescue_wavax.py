import time

from absl import app
from eth_account import Account
from web3 import Web3
from web3.types import Wei

from client.endpoints import make_mainnet_provider
from client.erc20_client import ERC20Client
from deployment.contracts import WAVAX_ADDRESS


# I used this script to retrieve funds from the Hyperspace airdrop that would otherwise have been lost.
#
# First I prefunded the account using rescue_avax.py
# Then I started up this script, which will fetch the latest nonce and then pause.
# I submitted a TX using the hyperspace website and then immediately hit enter to start this script.
#
# This script immediately disrupts the bot by sending out a bit of avax to adjust the nonce, and then subsequently
# transfers out the expected amount of WAVAX.
#
# It worked, but the transfer out of WAVAX woke up the bot and it subsequently drained the remaining gas in the account.
# Could have added a third tx to transfer out the gas, didn't think of it at the time.

def main(_: list[str]):
    print('Loading rescue')

    w3 = make_mainnet_provider()
    rescue_pk = '< FILL ME IN WITH THE PRIVATE KEY OF THE ACCOUNT TO BE RESCUED >'
    new_owner = Web3.to_checksum_address('< FILL ME IN WITH THE DESTINATION THAT YOU WANT TO SEND WAVAX TO >')
    rescue_amount_wei = Web3.to_wei(4.06, 'ether')

    rescue_account = Account.from_key(rescue_pk)

    rescue_client = ERC20Client(w3, rescue_account, WAVAX_ADDRESS)
    rescue_client.gas_limit = 100_000
    rescue_client.max_gas_in_gwei = 60
    rescue_client.max_priority_fee_gwei = 20
    rescue_start_nonce = rescue_client.next_nonce()

    input("ready?")

    for i in range(200):
        print('loop', i)
        rescue_client.fixed_nonce = rescue_start_nonce + 1
        try:
            tx_hash = rescue_client.send_value_wei(new_owner, Wei(1))
            print('sent', tx_hash)
        except Exception as ex:
            print('failed to send:', ex)

        rescue_client.fixed_nonce = rescue_start_nonce + 2
        try:
            tx_hash = rescue_client.transfer(new_owner, rescue_amount_wei)
            print('sent', tx_hash)
        except Exception as ex:
            print('failed to send:', ex)

        time.sleep(.2)


if __name__ == '__main__':
    app.run(main)
