from ..Config import config
from ..Client import Client
import unittest
import datetime

class ClientTest(unittest.TestCase):
	def setUp(self):
		config(hostname='fts.prinpay.com',
			port='6443',
			merchant_id='496160873888',
			username='testing',
			password='testing123')

	def test_client(self):
		client = Client.create()
		client.billing_address.first_name = 'Kevin'
		client.billing_address.last_name = 'Wang'
		client.email = 'kevmo314@gmail.com'
		client.save()
		self.assertIsNotNone(client.id, "Client did not save properly on the server")
		self.assertIsNotNone(Client.retrieve(client.id), "Could not retrieve the client from the server")
		self.assertEqual(Client.retrieve(client.id).email, client.email, "Email attribute not retrieved from the server")
		self.assertIsNone(Client.retrieve(-1), "An invalid client was returned from the server")
		self.assertRaises(Exception, Client.all)
		id = client.id
		client.email = 'newemail@mail.com'
		self.assertEqual(client.save().id, id, "The server created a new id instead of updating the existing one")
		self.assertEqual(Client.retrieve(id).email, client.email, "Email attribute was not updated")
		client.delete()
		self.assertIsNone(Client.retrieve(id), "Client was not deleted from the server")


if __name__ == '__main__':
	unittest.main()
