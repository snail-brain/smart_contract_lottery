from brownie import network
import pytest
import time
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    Local_Blockchain_Environments,
    fund_with_link,
    getAccount,
)


def test_pick_winner():
    if network.show_active() in Local_Blockchain_Environments:
        pytest.skip()
    _lottery = deploy_lottery()
    account = getAccount()
    _lottery.startLottery({"from": account})
    print("lottery started")
    _lottery.enter({"from": account, "value": _lottery.getEntranceFee()})
    _lottery.enter({"from": account, "value": _lottery.getEntranceFee()})
    print("Both Entered")
    fund_with_link(_lottery)
    _lottery.endLottery({"from": account})
    print("lottery ended")
    time.sleep(60)
    assert _lottery.recentWinner() == account
    assert _lottery.balance() == 0
