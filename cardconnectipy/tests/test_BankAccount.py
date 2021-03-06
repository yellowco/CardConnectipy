from .. import Config
from ..Client import Client
from ..BankAccount import BankAccount
import unittest
import datetime

class PaymentMethodTest(unittest.TestCase):
	def setUp(self):
		Config.config(hostname='fts.prinpay.com',
			port='6443',
			merchant_id='496160873888',
			username='testing',
			password='testing123')

	def test_bindable(self):
		client = Client.create()
		client.billing_address.first_name = 'Kevin'
		client.billing_address.last_name = 'Wang'
		account = BankAccount.create(
			account_holder='John Customer', # fyi this is ignored
			account_number='1234567845390',
			routing_number='122100024',
			type=BankAccount.CHECKING)
		account.random_data = 'yes'
		client.add_payment_method(account)
		id = client.save().id
		n = Client.retrieve(id=id)
		self.assertIsNotNone(n)
		self.assertEqual(len(n.payment_methods), 1)
		self.assertEqual(type(n.payment_methods[0]), BankAccount)
		self.assertEqual(n.payment_methods[0].account_holder, 'Kevin Wang')

	def test_unbindable(self):
		client = Client.create()
		client.billing_address.first_name = 'Kevin'
		client.billing_address.last_name = 'Wang'
		client.add_payment_method(BankAccount.create(
			account_holder='John Customer',
			account_number='1234567845390',
			routing_number='122100024',
			type=BankAccount.CHECKING,
			random_data='yes',
			note='test'))
		id = client.save().id
		n = Client.retrieve(id=id)
		self.assertIsNotNone(n)
		self.assertRaises(AttributeError, lambda: n.random_data)
		# self.assertEqual(n.payment_methods[0].note, 'test', "Note did not save correctly")

if __name__ == '__main__':
	unittest.main()
