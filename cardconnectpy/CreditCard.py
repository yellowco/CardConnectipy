from Client import Client
import Config
import requests

class CreditCard(object):
	def __init__(self, **kwargs):
		self.profileid = None
		self.acctid = None
		self.account = None	# tokenized card number
		self.accttype = None	# oneof PPAL, PAID, GIFT, PDEBIT in PUT, oneof VISA, MC, DISC, ECHK in GET
		self.expiry = None	# MMYY
		self.defaultacct = None
		self.__dict__.update(kwargs)

	def serialize(self):
		return {
			'defaultacct':self.defaultacct,
			'profile':self.id(),
			'account':self.account,
			'accttype':self.accttype,
			'expiry':self.expiry
		}

	def deserialize(self):
		for key, value in data.items():
			setattr(self, key, value)
	@property
	def client(self):
		Client.retrieve(self.profileid)

	@property
	def id(self):
		return "%s/%s" % (self.profileid, self.acctid)

	def delete(self):
		if(self.acctid != None):
			requests.delete("https://%s:%s/cardconnect/rest/profile/%s/%s" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID))

	def save(self):
		self.profile.save()
		if(self.acctid == None):
			# account numbers must be tokens
			payload = {
				"merchid":Config.MERCHANT_ID,
				"account":self.account,
				"tokenize":"Y"
			}
			data = requests.put("https://%s:%s/cardconnect/auth" % (Config.HOSTNAME, Config.PORT, self.id, Config.MERCHANT_ID), data=payload).json()
			self.account = data['token']
		self.deserialize(requests.put("https://%s:%s/cardconnect/rest/profile" % (Config.HOSTNAME, Config.PORT), self.serialize()).json())

	@staticmethod
	def retrieve(id):
		return CreditCard(requests.get("%s/profile/%s/%s/" % (Config.BASE_URL, id, Config.MERCHANT_ID)).json())

	@staticmethod
	def create(**kwargs):
		return CreditCard(**kwargs)
