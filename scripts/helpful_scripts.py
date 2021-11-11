from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
)
from web3 import Web3

Decimals = 8
Starting_Price = 200000000000

Local_Blockchain_Environments = ["development", "ganache-local"]
Forked_Environments = ["mainnet-fork"]


def getAccount(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)  # Select specific account based on its id or index
    if (
        network.show_active()
        in Local_Blockchain_Environments  # If using local chain, use the first address provided from that chain
        or network.show_active() in Forked_Environments
    ):
        return accounts[0]
    return accounts.add(  # Otherwise, use wallet associated with current network
        config["wallets"]["from_key"]
    )


contract_to_mock = {  # Map inputs to mock contracts
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def deploy_mocks():  # Deploy mock versions of contracts
    MockV3Aggregator.deploy(Decimals, Starting_Price, {"from": getAccount()})
    _link_token = LinkToken.deploy({"from": getAccount()})
    VRFCoordinatorMock.deploy(_link_token.address, {"from": getAccount()})
    print("Mocks Deployed!")


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    # Map input to contract
    if network.show_active() in Local_Blockchain_Environments:
        # Deploy mock contracts if on local network and if there haven't been any deployed yet
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:  # If not on local network...
        contract_address = config["networks"][network.show_active()][contract_name]
        # Find address of contract for current network
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # Find and return contract info from abi
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else getAccount()
    # if there's an account input use that, if not run getAccount
    link_token = link_token if link_token else get_contract("link_token")
    # if there's a link token input use that if not run get_contract
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # transfer link from our current account to lottery contract
    tx.wait(1)
    print("Contract funded!")
    return tx
