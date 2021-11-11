from _pytest.config import exceptions
from brownie import lottery, accounts, config, network, exceptions
from scripts.helpful_scripts import (
    Forked_Environments,
    fund_with_link,
    get_contract,
    getAccount,
    Local_Blockchain_Environments,
)
from scripts.deploy_lottery import deploy_lottery, end_lottery
from web3 import Web3
import pytest

#
def test_get_entrance_fee():
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    excepted_entrance_fee = Web3.toWei(0.025, "ether")
    # Assert
    assert excepted_entrance_fee == entrance_fee


def test_cant_enter_unless_starter():
    # Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": getAccount(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    _lottery = deploy_lottery()

    # Act
    _lottery.startLottery({"from": getAccount()})
    _lottery.enter({"from": getAccount(), "value": _lottery.getEntranceFee()})

    # Assert
    assert _lottery.balance() == _lottery.getEntranceFee()


def test_end_lottery():
    # Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    _lottery = deploy_lottery()
    account = getAccount()

    # Act
    _lottery.startLottery({"from": account})
    _lottery.enter({"from": account, "value": _lottery.getEntranceFee()})
    fund_with_link(_lottery)
    _lottery.endLottery({"from": account})
    # Assert
    assert _lottery.lottery_state() == 2


def test_choose_winner_correctly():
    # Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    _lottery = deploy_lottery()
    account = getAccount()

    _lottery.startLottery({"from": account})
    _lottery.enter({"from": account, "value": _lottery.getEntranceFee()})
    _lottery.enter({"from": getAccount(index=1), "value": _lottery.getEntranceFee()})
    _lottery.enter({"from": getAccount(index=2), "value": _lottery.getEntranceFee()})

    fund_with_link(_lottery)
    tx = _lottery.endLottery({"from": account})
    request_id = tx.events["RequestedRandomness"]["requestId"]

    static_rng = 777
    starting_balance = account.balance()
    balance_of_lottery = _lottery.balance()

    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, static_rng, _lottery.address, {"from": account}
    )

    assert _lottery.recentWinner() == account
    assert _lottery.balance() == 0
    assert account.balance() == starting_balance + balance_of_lottery
