from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import (
    Forked_Environments,
    getAccount,
    Local_Blockchain_Environments,
)


def test_get_entrance_fee():
    account = getAccount()
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
