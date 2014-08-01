from Address import Address
from PaymentMethod import PaymentMethod
from CreditCard import CreditCard
from BankAccount import BankAccount
from DriversLicense import DriversLicense
import Config
import requests

class Client(object):
	def __init__(self, **kwargs):
		self.billing_address = Address()
		self.drivers_license = DriversLicense()
		self.ssn = None
		self.email = None
		self.profileid = None
		self.__dict__.update(kwargs)

	def serialize(self):
		return {
			'address':"%s %s" % (self.billing_address.street1, self.billing_address.street2),
			'region':self.billing_address.state,
			'phone':self.billing_address.phone,
			'postal':self.billing_address.postal,
			'ssnl4':self.ssn[-4:] if self.ssn != None else None,
			'email':self.email,
			'license':"%s:%s" % (self.drivers_license.state, self.drivers_license.number),
			'name':"%s %s" % (self.billing_address.first_name, self.billing_address.last_name),
			'country':self.billing_address.country,
			'city':self.billing_address.city,
			'profileid':self.profileid,
			'defaultacct':'Y'
		}
	
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
		return self.deserialize(requests.put("https://%s:%s/cardconnect/rest/profile" % (Config.HOSTNAME, Config.PORT), self.serialize(), auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json())

	@staticmethod
	def retrieve(id):
		response = requests.get("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
		for account in response:
			if account['defaultacct'] == 'Y':
				return Client(**account)
		return None

	@staticmethod
	def create(**kwargs):
		return Client(**kwargs)
