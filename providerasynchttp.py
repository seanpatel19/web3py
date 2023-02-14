from aiohttp import ClientSession
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet
from web3.geth import Geth, AsyncGethTxPool
w3= Web3(
    AsyncHTTPProvider(endpoint_uri),
    modules = {'eth': (AsyncEth),
        'net': (AsyncNet,),
        'geth': (Geth, {
            'txpool': (AsyncGethTxPool,),
            'personal': (AsyncGethPersonal,),
            'admin': (AsyncGethAdmin,)
        })},
    middleswares = []
)
custom_sesson = ClientSesson()
await w3.provider.cache_async_sesson(customer_sesson)