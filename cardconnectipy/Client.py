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
		self._payment_methods = []

	def serialize(self):
		data = {
			'profile':"%s/%s" % (self.profileid, self.acctid) if self.profileid and self.acctid else None,
			'ssnl4':self.ssn[-4:] if self.ssn else None,
			'email':self.email,
			'merchid':Config.MERCHANT_ID,
			'defaultacct':'Y',
			'profileupdate':'Y'
		}
		data.update(self.billing_address.serialize())
		data.update(self.drivers_license.serialize())
		return data
	
	def deserialize(self, data):
		for key, value in data.items():
			setattr(self, key, value)
		return self

	@property
	def id(self):
		return self.profileid

	@property
	def payment_methods(self):
		if len(self._payment_methods) == 0:
			response = requests.get("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
			out = []
			for account in response:
				if 'expiry' in account:
					out.append(CreditCard(**account))
				if 'bankaba' in account:
					out.append(BankAccount(**account))
			self._payment_methods = out
		return self._payment_methods
	
	def add_payment_method(self, method):
		method.client = self
		self._payment_methods.append(method)		

	def delete(self):
		requests.delete("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD))

	def save(self):
		# need to get own profileid to pass onto payment_methods
		resp = self.deserialize(requests.put("https://%s:%s/cardconnect/rest/profile" % (Config.HOSTNAME, Config.PORT), data=json.dumps(self.serialize()), auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json())
		for payment_method in self.payment_methods:
			if not payment_method.acctid:
				payment_method.save() # this isn't quite right, doesn't track modified cards.
		return resp

	@staticmethod
	def retrieve(id):
		response = requests.get("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
		for account in response:
			if account.get('defaultacct') == 'Y':
				return Client(**account)
		return None

	@staticmethod
	def create(**kwargs):
		return Client(**kwargs)
