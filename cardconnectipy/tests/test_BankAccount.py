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
			account_holder='John Customer',
			account_number='1234567845390',
			routing_number='253271806',
			type=BankAccount.CHECKING)
		account.random_data = 'yes'
		client.add_payment_method(account)
		id = client.save().id
		n = Client.retrieve(id=id)
		self.assertEqual(n.payment_methods[0].random_data, 'yes', "The arbitrary data did not save correctly")

	def test_unbindable(self):
		client = Client.create()
		client.billing_address.first_name = 'Kevin'
		client.billing_address.last_name = 'Wang'
		client.add_payment_method(BankAccount.create(
			account_holder='John Customer',
			account_number='1234567845390',
			routing_number='253271806',
			type=BankAccount.CHECKING,
			random_data='yes',
			note='test'))
		id = client.save().id
		n = Client.retrieve(id=id)
		self.assertRaises(AttributeError, lambda: n.random_data)
		self.assertEqual(n.payment_methods[0].note, 'test', "Note did not save correctly")

if __name__ == '__main__':
	unittest.main()
