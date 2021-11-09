from brownie import lottery, accounts, config, network
from scripts.helpful_scripts import (
    Forked_Environments,
    getAccount,
    Local_Blockchain_Environments,
)
from web3 import Web3

#
def test_get_entrance_fee():
    account = getAccount()
    lottery_test = lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
    )
    assert lottery_test.getEntranceFee() > Web3.toWei(0.0104, "ether")
    assert lottery_test.getEntranceFee() < Web3.toWei(0.012, "ether")
