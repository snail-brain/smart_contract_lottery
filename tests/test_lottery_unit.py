from _pytest.config import exceptions
from brownie import lottery, accounts, config, network, exceptions
from scripts.helpful_scripts import (
    Forked_Environments,
    fund_with_link,
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
    assert _lottery.players(0) == getAccount()


def test_end_lottery():
    # Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    _lottery = deploy_lottery()

    # Act
    _lottery.startLottery({"from": getAccount()})
    _lottery.enter({"from": getAccount(), "value": _lottery.getEntranceFee()})
    fund_with_link(getAccount())
    _lottery.endLottery({"from": getAccount()})
    # Assert
    assert _lottery.Lottery_State() == 2
