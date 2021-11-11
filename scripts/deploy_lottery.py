from scripts.helpful_scripts import getAccount
import time
from brownie import network, lottery, config
from scripts.helpful_scripts import getAccount, get_contract, fund_with_link


def deploy_lottery():
    account = getAccount()
    _lottery = lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery!")
    return _lottery


def start_lottery():
    account = getAccount()
    _lottery = lottery[-1]
    starting_tx = _lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery Started!")


def enter_lottery():
    account = getAccount()
    _lottery = lottery[-1]
    value = _lottery.getEntranceFee() + 1000000
    tx = _lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You're in")


def end_lottery():
    account = getAccount()
    _lottery = lottery[-1]
    tx = fund_with_link(_lottery.address)
    tx.wait(1)
    # fund the contract with Link
    ending_tx = _lottery.endLottery({"from": account})
    ending_tx.wait(1)
    # end the lottery
    time.sleep(60)
    print(f"{_lottery.recentWinner()} is the winner!")


def testing():
    account = getAccount()
    _lottery = lottery[-1]
    print(_lottery.Lottery_State)


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    testing()
