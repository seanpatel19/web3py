from web3 import Web3

# from web3.auto import w3  // this will check common locations for a node connection

#IPCProvider::
# w3= Web3(Web3.IPCProvider('./path/to/geth.ipc'))

#HTTPProvider:
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# WebsocketProvider:

w3 = Web3(Web3.WebsocketProvider('wss://127.0.0.1:8546'))

w3.isConnected()
True


# after connection is established

w3.eth.get_block('latest')