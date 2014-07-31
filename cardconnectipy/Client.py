from Address import Address
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
			'address':"%s %s" % (self.address.street1, self.address.street2),
			'region':self.address.state,
			'phone':self.address.phone,
			'postal':self.address.postal,
			'ssnl4':self.ssn[-4:],
			'email':self.email,
			'license':"%s:%s" % (self.drivers_license.state, self.drivers_license.number),
			'name':"%s %s" % (self.address.first_name, self.address.last_name),
			'country':self.address.country,
			'city':self.address.city,
			'profileid':self.profileid
		}
	
	def deserialize(self, data):
		for key, value in data.items():
			setattr(self, key, value)

	@property
	def id(self):
		return self.profileid + '/'

	@property
	def payment_methods(self):
		# remember to check for acctid != 1
		return map(lambda record: CreditCard(record) if 'expiry' in record else BankAccount(record),
			requests.get("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json())

	def delete(self):
		requests.delete("https://%s:%s/cardconnect/rest/profile/%s//%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD))

	def save(self):
		self.deserialize(requests.put("https://%s:%s/cardconnect/rest/profile" % (Config.HOSTNAME, Config.PORT), self.serialize(), auth=(Config.USERNAME, Config.PASSWORD)).json())

	@staticmethod
	def retrieve(id):
		# profile/{id}/{merchid} returns 404 -- must specify account number (numbering scheme starts at 1)
		# profile/{id}/{acctid}/{merchid} returns a LIST of accounts
		return Client(requests.get("https://%s:%s/cardconnect/rest/profile/%s/1/%s" % (Config.HOSTNAME, Config.PORT, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()[0])

	@staticmethod
	def create(**kwargs):
		return Client(**kwargs)
