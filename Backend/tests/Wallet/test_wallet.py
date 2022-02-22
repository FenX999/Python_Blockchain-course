from Backend.Wallet.wallet import Wallet
from Backend.Wallet.transaction import Transaction
from Backend.Blockchain.blockchain import Blockchain
from Backend.config import STARTING_BALANCE

def test_verify_valid_signature():
	data = {'foo': 'test_data'}
	wallet = Wallet()
	signature = wallet.sign(data)
	
	assert Wallet.verify(wallet.public_key, data, signature)
	
def test_verify_invalid_signature():
	data = {'foo': 'test_data'}
	wallet = Wallet()
	signature = wallet.sign(data)
	
	assert not Wallet.verify(Wallet().public_key, data, signature)
	
def test_calculate_balance():
	blockchain = Blockchain()
	wallet = Wallet()
	
	assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE
	
	amount = 50 
	transaction = Transaction(wallet, 'recipient', amount)
	blockchain.add_block([transaction.to_json()])
	
	assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount
	
	recieved_amount_1 = 25
	recieved_transaction_1 = Transaction(Wallet(), wallet.address, recieved_amount_1)
	recieved_amount_2 = 43
	recieved_transaction_2 = Transaction(Wallet(), wallet.address, recieved_amount_2)
	
	blockchain.add_block([recieved_transaction_1.to_json(), recieved_transaction_2.to_json()])
	assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount + recieved_amount_1 + recieved_amount_2
