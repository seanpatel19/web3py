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

logger = logging.getLogger(__name__)

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

        self.logger = logger
        self.contract = contract 
        self.web3 = web3
        self.state = state
        self.events = events
        self.filters = filters 

        self.min_scan_chunk_size = 10
        self.max_scan_chunk_size = max_chunk_scan_size
        self.max_request_retries = max_request_retries
        self.request_retry_seconds = request_retry_seconds
        self.chunk_size_decrease = 0.5
        self.chunk_size_increase = 2.0 

    def address(self):
        return self.token_address
    def get_block_timestampl(self,block_num) -> datetime.datetime:

        try:
            block_info = self.web3.eth.getBlcok(block_num)
        except BlockNotFound:
            return None 
        last_time = block_info["timestamp"]
        return datetime.datetime.utcfromtimestamp(last_time)
    def get_suggested_scan_start_block(self):
        end_block = self.get_last_scanned_block()
        if end_block:
            return max(1,end_block - self.NUM_BLOCKS_RESCAN_FOR_FORKS)
        return 1 
    def get_suggested_scan_end_block(self):
        return self.web3.eth.blockNumber -1 
    
    def get_last_scanned_block(self) -> int:
        return self.state.get_last_scanned_block()
    def delete_potentially_forked_block_data(self, after_block: int):
        self.state.delete_data(after_block)
    def scan_chunk(self, start_block, end_block) -> Tuple[int, datetime.datetime, list]:

        block_timestamps = {}
        get_block_timestamp = self.get_block_timestampl

        def get_block_when(block_num):
            if block_num not in block_timestamps:
                block_timestamps[block_num] = get_block_timestamp(block_num)
            return block_timestamps[block_num]

        all_processed = []

        for event_type in self.events:
            def _fetch_events(_start_block, _end_block):
                return _fetch_events_for_all_contracts(self.web3,
                event_type, self.filters, from_blocks = _start_block, to_block= _end_block)

            end_block, events = _retry_web3_call(
                _fetch_events,
                start_block = start_block,
                end_block = end_block,
                retries = self.max_request_retries,
                delay = self.request_retry_seconds
            )
            for evt in events:
                idx = evt["logIndex"]  

                assert idx is not None, "Somehow tried to scan a pending block"

                block_number = evt["blockNumber"]

                block_when = get_block_when(block_number)

                logger.debug("Processing event %s, block %d", evt["event"], evt["blockNumber"])
                processed = self.state.process_event(block_when, evt)
                all_processed.append(processed)
        end_block_timestamp = get_block_when(end_block)
        return end_block , end_block_timestamp, all_processed 
    def estimate_next_chunk_size(self, churrent_chunk_size: int, event_found_count: int):


