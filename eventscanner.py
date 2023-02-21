import datetime
import time 
import logging 
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Callable, List, Iterable

from web3 import Web3 
from web3.contract import Contract
from web3.datastructures import AttributeDict
from web3.exceptions import BlockNotFound
from eth_abi.codec import ABICodec

from web3._utils.filters import construct_event_filter_params
from web3._utils.events import get_event_data 

loger = logging.getLogger(__name__)

class EventScannerState(ABC):
    @abstractmethod
    def get_last_scanned_block(self) -> int:

    @abstractmethod
    def start_chunk(self, block_number: int):
    
    @abstractmethod
    def process_event(self,block_when: datetime.datetime, event: AttributeDict) -> object 
    ## function takes raw events from web3 and turns them into te apps internal format and saves them as a db 

    ## param block_when: when it was mined
    ## param event: Symbolic dictionary of event data 

    ## retrun internal state structure as a result of event transfomr 

    def delete_data(self, since_block: int) -> int:
        ## delete any data since this block was scanned 


class EventScanner:
    ## can be used for real time scans it looks for minor chain reorganisation and rescans  can get events from multiple contracts such as all the transfers from all the tokens 
    ## You *should* disable the default `http_retry_request_middleware` on your provider for Web3, because it cannot correctly throttle and decrease the `eth_getLogs` block number range.
    def __init__(self,web3:Web3, contract:Contract, state:EventScannerState, events:List, filters:{},
    max_chunk_scan_size: int = 10000, max_request_retries: int = 30, request_rety_seconds: float = 3.0):
    ## param contract:Contract param events: List of web3 events that we are scanning param filters: Filters we passed to getLogs
    ## param max_chunk_scan_size JSON-RPC API limit in the number of blocks we query recommend 10k for main 500k for test
    ## param max_request_retries for many times we retry the call
    ## param request_rety_seconds delay between failed requests 