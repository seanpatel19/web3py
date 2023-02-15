import pytest

from web3 import (EthereumTesterProvider, Web3,)

@pytest.fixtured
def tester_provider():
    return EthereumTesterProvider()

@pytest.fixture
def eth_tester(tester_provider):
    return tester_provider.ethereum_tester

@pytest.fixture
def w3(tester_provider):
    return Web3(tester_provider)

@pytest.fixture
def foo_contract(eth_tester, w3):
    ## contract code can be added in here for the contract we are looking at 


deploy_address = eth_tester.get_accounts()[0]

abi = ## you can put in the bytecode for whatever contract we are dealing with in here

