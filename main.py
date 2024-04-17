from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_address, abi=abi)

print(contract.address)

print(f"Баланс смарт-контракта: {w3.eth.get_balance(contract.address)}")
print(f"Баланс первого аккаунта: {w3.eth.get_balance('0x8538984DDDd639867306Dad1E11b59c5f5AF0E6E')}")
print(f"Баланс второго аккаунта: {w3.eth.get_balance('0x4B9D076A0Dbf113C0Da1f6Aa3A65A1A151BE6826')}")
print(f"Баланс третьего аккаунта: {w3.eth.get_balance('0xcFAF0395Ce3154A30dd7F8D283E992419bb702A4')}")
print(f"Баланс четвертого аккаунта: {w3.eth.get_balance('0x745C4De7eA31bDBFDF5b324c52838D6CB7430774')}")
print(f"Баланс пятого аккаунта: {w3.eth.get_balance('0x177A70e61C26DbF8A108FD80d8cfC550Fa3E75b2')}")
