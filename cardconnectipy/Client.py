from Address import Address
from PaymentMethod import PaymentMethod
from CreditCard import CreditCard
from BankAccount import BankAccount
from DriversLicense import DriversLicense
import Config
import requests
import json

class Client(object):
	def __init__(self, **kwargs):
		self.billing_address = Address()
		self.drivers_license = DriversLicense()
		self.ssn = None
		self.email = None
		self.profileid = None
		self.__dict__.update(kwargs)

	def serialize(self):
		data = {
			'ssnl4':self.ssn[-4:] if self.ssn else None,
			'email':self.email,
			'merchid':Config.MERCHANT_ID,
			'defaultacct':'Y',
			'profileupdate':'Y'
		}
		data.update(self.billing_address.serialize())
		data.update(self.drivers_license.serialize())
		return dict((k, v) for k, v in data.iteritems() if v)
	
	def deserialize(self, data):
		for key, value in data.items():
			setattr(self, key, value)
		return self

	@property
	def id(self):
		return self.profileid

	@property
	def payment_methods(self):
		response = requests.get("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
		out = []
		for account in response:
			if 'expiry' in account:
				out.append(CreditCard(**account))
			if 'bankaba' in account:
				out.append(BankAccount(**account))
		return out

	def delete(self):
		requests.delete("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD))

	def save(self):
		return self.deserialize(requests.put("https://%s:%s/cardconnect/rest/profile" % (Config.HOSTNAME, Config.PORT), data=json.dumps(self.serialize()), auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json())

	@staticmethod
	def retrieve(id):
		response = requests.get("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
		print(response)
		for account in response:
			if account['defaultacct'] == 'Y':
				return Client(**account)
		return None

	@staticmethod
	def create(**kwargs):
		return Client(**kwargs)
