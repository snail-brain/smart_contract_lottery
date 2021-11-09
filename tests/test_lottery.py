from brownie import Lottery, accounts, config
from scripts.helpful_scripts import (
    Forked_Environments,
    getAccount,
    Local_Blockchain_Environments,
)


def test_get_entrance_fee():
    account = getAccount()
    lottery = Lottery.deploy({"from": account})
