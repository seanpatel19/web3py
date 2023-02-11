from web3 import Web3

from web3.auto import w3 

ExampleContract = w3.eth.contract(abi=abi, bytecode=bytecode)  ## this would have to be filled in with a real active contract 

tx_hash = ExampleContract.consturctor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
tx_receipt.contractAddress        ## this needs to be changed to an actual contract address

deployed_contract = w3.eth.contract(address = tx_receipt, contractAddress, abi=abi)  ## again this will referene an actual contract address
deployed_contract.functions.myFunction(42).transact()

deployed_contract.functions.getMyValue().call()  ## since the number put in  the myFunction line 14 was 42 should be the output of these two functios
deployed_contract.caller().getMyValue()

## once contract has been retrieved we can filter specific events

new_filter = web3.eth.filter('latest')
new_filter = deployed_contract.events.MyEvent.createFilter(fromBlock='latest')

new_filter.get_all_entries()
new_filter.get_new_entries()


# web3.eth.filter()
# web3.eth.get_filter_changes()
# web3.eth.get_filter_logs()
# web3.eth.uninstall_filter()
# web3.eth.get_logs()
# Contract.events.your_event_name.createFilter()
# Contract.events.your_event_name.build_filter()
# Filter.get_new_entries()
# Filter.get_all_entries()
# Filter.format_entry()
# Filter.is_valid_entry()


# also web3.net has some properties as well 

# web3.net.listening
# web3.net.peer_count
# web3.net.version


