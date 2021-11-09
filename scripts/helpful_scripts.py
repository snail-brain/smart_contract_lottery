from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

Decimals = 8
Starting_Price = 200000000000

Local_Blockchain_Environments = ["development", "ganache-local"]
Forked_Environments = ["mainnet-fork"]


def getAccount():
    if (
        network.show_active() in Local_Blockchain_Environments
        or network.show_active() in Forked_Environments
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active netork is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        mock_aggregator = MockV3Aggregator.deploy(
            Decimals, Starting_Price, {"from": getAccount()}
        )
    print("Mocks Deployed!")
