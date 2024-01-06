import time

from absl import app
from eth_account import Account
from web3 import Web3
from web3.types import Wei

from client.endpoints import make_mainnet_provider
from client.web3_client import Web3Client

# This script can be used to 'disrupt' a bot that tries to automatically transfer out gas fees.
# It does so by transferring in gas, and then immediately submitting a transaction at the same nonce that the
# bot is expected to use to transfer out the gas. If the bot is dumb, it will fail this tx, and then give up.
#
# This gives you space to do other kinds of complex transactions like transferring contract ownership. But make
# sure none of your tx transfer in funds, or the bot will probably wake up and try to drain you.
#
# Not guaranteed to work; some bots might be smart enough to retry with a higher nonce. Test with a small amount of
# funds first. You can always do something more complicated, see rescue_wavax.py for an example.


def main(_: list[str]):
    print('Loading rescue')

    w3 = make_mainnet_provider()
    money_pk = '< FILL ME IN WITH THE PRIVATE KEY OF THE ACCOUNT THAT WILL FUND THE ACCOUNT NEEDING RESCUE >'
    rescue_pk = '< FILL ME IN WITH THE PRIVATE KEY OF THE ACCOUNT TO BE RESCUED >'
    new_owner = Web3.to_checksum_address('< THIS CAN BE ANY ACCOUNT EXCEPT THE ACCOUNT BEING RESCUED >')

    money_account = Account.from_key(money_pk)
    rescue_account = Account.from_key(rescue_pk)

    money_client = Web3Client(w3, money_account)
    rescue_client = Web3Client(w3, rescue_account)
    rescue_client.gas_limit = 50_000
    rescue_client.max_gas_in_gwei = 60
    rescue_client.max_priority_fee_gwei = 20
    rescue_start_nonce = rescue_client.next_nonce()

    # You might want to increase or decrease the amount you fund the rescued account with
    rescue_funding_avax = .1

    print('sending money')
    money_client.send_value(rescue_account.address, rescue_funding_avax)
    time.sleep(1)

    for i in range(20):
        print('loop', i)
        rescue_client.fixed_nonce = rescue_start_nonce
        try:
            tx_hash = rescue_client.send_value_wei(new_owner, Wei(1))
            print('sent', tx_hash)
        except Exception as ex:
            print('failed to send:', ex)
        time.sleep(.2)


if __name__ == '__main__':
    app.run(main)
