import time

from pubnub.pubnub import PubNub
from pubnub.pubnub import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from Backend.Blockchain.block import Block
from Backend.Wallet.transaction import Transaction
from Backend.config import PUBSUB_SUBSCRIBE_KEY, PUBSUB_PUBLISH_KEY

"""
you need to inform your pubsub credentials to utilize that module and the python blockchain as its all!
refere to BAckend/config.py file 
"""

subscribe_key = PUBSUB_SUBSCRIBE_KEY
publish_key = PUBSUB_PUBLISH_KEY

pnconfig = PNConfiguration()

pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key

CHANNELS = {
	'TEST': 'TEST',
	'BLOCK': 'BLOCK',
	'TRANSACTION': 'TRANSACTION'
}

class Listener(SubscribeCallback):
	def __init__(self, blockchain, transaction_pool):
		self.blockchain = blockchain
		self.transaction_pool = transaction_pool

	def message (self, pubnub, message_object):
		print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
		if message_object.channel == CHANNELS['BLOCK']:
			block = Block.from_json(message_object.message)
			potential_chain = self.blockchain.chain[:]
			potential_chain.append(block)
			try:
				self.blockchain.replace_chain(potential_chain)
				self.transaction_pool.clear_blockchain_transactions(self.blockchain)
				print(f'\n Succesfully replaced the local chain')
			except Exception as e:
				print(f'\n --Did not replace_chain: {e}')
		elif message_object.channel == CHANNELS['TRANSACTION']:
			transaction = Transaction.from_json(message_object.message)
			self.transaction_pool.set_transaction(transaction)
			print(f'\n -- Set the new transaction in the transaction pool')


class PubSub():
#	handle the publish/subscribe layer of the application.
#	provide communication between the nodes of the blockchain network.
	def __init__(self, blockchain, transaction_pool):
		self.pubnub = PubNub(pnconfig)
		self.pubnub.subscribe().channels(CHANNELS.values()).execute()
		self.pubnub.add_listener(Listener(blockchain, transaction_pool))
		
	def publish(self, channel, message):
#		publish the message object to the channel
		self.pubnub.publish().channel(channel).message(message).sync()

	def broadcast_block(self, block):
#		Broadcast a block to all nodes.
		self.publish(CHANNELS['BLOCK'], block.to_json())

	def broadcast_transaction(self, transaction):
#		Broadcast a transaction to all nodes.
		self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

def main():
	pubsub = PubSub()
	time.sleep(1)
	pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})
	
if __name__=='__main__':
	main()
