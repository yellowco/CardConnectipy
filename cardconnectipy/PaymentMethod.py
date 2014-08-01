import Config
import requests

class PaymentMethod(object):
	def __init__(self, **kwargs):
		self.client = None
		self.acctid = None
		self.account = None	# tokenized card / bank account number
		self.accttype = None	# oneof PPAL, PAID, GIFT, PDEBIT in PUT, oneof VISA, MC, DISC, ECHK in GET
		self.defaultacct = None
		self.__dict__.update(kwargs)

	def serialize(self):
		return {
			'defaultacct':self.defaultacct,
			'profile':self.id(),
			'account':self.account,
			'accttype':self.accttype,
		}

	@property
	def profileid(self):
		return self.client.id

	def deserialize(self, data):
		for key, value in data.items():
			setattr(self, key, value)

	@property
	def id(self):
		return "%s/%s" % (self.profileid, self.acctid)

	def delete(self):
		if(self.acctid != None):
			requests.delete("%s/profile/%s/%s" % (Config.BASE_URL, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD))

	def save(self):
		self.client.save()
		if(self.acctid == None):
			# account numbers must be tokens
			payload = {
				"merchid":Config.MERCHANT_ID,
				"account":self.account,
				"tokenize":"Y"
			}
			data = requests.put("%s/auth" % (Config.BASE_URL), data=payload, auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json()
			self.account = data['token']
		self.deserialize(requests.put("%s/profile" % (Config.BASE_URL), self.serialize(), auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json())

	@staticmethod
	def retrieve(id):
		# if of form "<profileid>/<acctid>"
		return PaymentMethod(requests.get("%s/profile/%s/%s/" % (Config.BASE_URL, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()[0])

	@staticmethod
	def create(**kwargs):
		return PaymentMethod(**kwargs)

	# base AUTHORIZATION request
	def auth(amount, cvv):
		raise NotImplementedError

	# utilize AUTHORIZE-CAPTURE request feature
	def capture(amount, cvv):
		raise NotImplementedError

	def void(amount, retref):
		raise NotImplementedError

	# REFUND request
	def refund(amount, cvv):
		raise NotImplementedError

	# shorthand for auth(0, cvv)
	def verify(cvv):
		raise NotImplementedError
