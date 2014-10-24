from .. import Config
from ..Client import Client
from ..CreditCard import CreditCard
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
		account = CreditCard.create(
			account_holder='John Customer',
			card_number='4111111111111111',
			expiration_date=datetime.datetime(month=1, day=1, year=2017),
			type=CreditCard.VISA)
		account.random_data = 'yes'
		client.add_payment_method(account)
		id = client.save().id
		n = Client.retrieve(id=id)
		self.assertIsNotNone(n)
		self.assertEqual(len(n.payment_methods), 1)
		self.assertEqual(type(n.payment_methods[0]), CreditCard)
		self.assertEqual(n.payment_methods[0].account_holder, 'Kevin Wang')
		# self.assertEqual(n.payment_methods[0].random_data, 'yes', "The arbitrary data did not save correctly")

	def test_unbindable(self):
		client = Client.create()
		client.billing_address.first_name = 'Kevin'
		client.billing_address.last_name = 'Wang'
		client.add_payment_method(CreditCard.create(
			account_holder='John Customer',
			card_number='4111111111111111',
			expiration_date=datetime.datetime(month=1, day=1, year=2017),
			type=CreditCard.VISA,
			random_data='yes',
			note='test'))
		id = client.save().id
		n = Client.retrieve(id=id)
		self.assertRaises(AttributeError, lambda: n.random_data)
		# self.assertEqual(n.payment_methods[0].note, 'test', "Note did not save correctly")

if __name__ == '__main__':
	unittest.main()
