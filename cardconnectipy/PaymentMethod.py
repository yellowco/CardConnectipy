import Config
import requests
import json

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
			'defaultacct':'' if self.defaultacct == None else self.defaultacct,
			'profile':'' if self.client == None else self.id(),
			'account':'' if self.account == None else self.account,
			'accttype':'' if self.accttype == None else self.accttype
		}

	@property
	def profileid(self):
		return self.client.id

	def deserialize(self, data):
		for key, value in data.items():
			setattr(self, key, value)
		return self

	@property
	def id(self):
		return '%s/%s' % (self.profileid, self.acctid)

	def delete(self):
		if(self.acctid != None):
			requests.delete('%s/profile/%s/%s' % (Config.BASE_URL, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD))

	def save(self):
		for key in self.__dict__:
			if self.__dict__[key] == None:
				raise ValueError('all payment method fields are required')

		self.client.save()
		if(self.acctid == None):
			# account numbers must be tokens
			self.account = self.tokenize()
		self.deserialize(requests.put('%s/profile' % (Config.BASE_URL), self.serialize(), auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json())

	@staticmethod
	def retrieve(id):
		# id of form "<profileid>/<acctid>"
		return PaymentMethod(requests.get('%s/profile/%s/%s/' % (Config.BASE_URL, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()[0])

	@staticmethod
	def create(**kwargs):
		return PaymentMethod(**kwargs)

	# base AUTHORIZATION request
	# cf. http://bit.ly/1ohnJEb for 3DSecure support
	def auth(self, amount=None, **kwargs):
		payload = {
			'merchid':Config.MERCHANT_ID,
			'amount':str(amount),
		}
		if(self.client != None):
			payload = dict(payload.items() + self.client.serialize().items())
		# cvv, etc. in here as well
		payload = dict(payload.items() + kwargs.items() + self.serialize().items())
		resp = requests.put('%s/auth' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD), data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		return (resp['respstat'] == 'A', resp['retref'], resp)

	# shorthand for auth(0)
	def verify(self):
		return self.auth(amount='0')

	def tokenize(self):
		if(self.account != None):
			return(self.auth(amount='0', tokenize='Y'))[2]['token']

	# utilize AUTHORIZE-CAPTURE request feature
	# cf. http://bit.ly/1qzs8p1 for additional fields to present to the AUTHORIZATION request payload
	def capture(self, amount=None, **kwargs):
		return self.auth(amount, capture='Y', **kwargs)

	# TX stuff here
	@staticmethod
	def void(retref=None, amount=None):
		payload = {
			'merchid':Config.MERCHANT_ID,
			'amount':str(amount),
			'retref':str(retref)
		}
		resp = requests.put('%s/void' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD), data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		return (resp['respstat'] == 'A', resp['retref'], resp)

	# REFUND request
	@staticmethod
	def refund(retref=None, amount=None):
		payload = {
			'merchid':Config.MERCHANT_ID,
			'amount':str(amount),
			'retref':str(retref)
		}
		resp = requests.put('%s/refund' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD), data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		return (resp['respstat'] == 'A', resp['retref'], resp)

	@staticmethod
	def inquire(retref=None):
		resp = requests.get('%s/inquire/%s/%s' % (Config.BASE_URL, retref, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
		return(resp['respstat'] == 'A', resp['retref'], resp)

	@staticmethod
	def deposit(**kwargs):
		url = '%s/deposit?merchid=%s&' % (Config.BASE_URL, Config.MERCHANT_ID) + '&'.join([str(k) + '=' + str(v) for k, v in kwargs.items()])
		return requests.get(url, auth=(Config.USERNAME, Config.PASSWORD)).json()

	@staticmethod
	def settlement_status(**kwargs):
		url = '%s/settlestat?merchid=%s&' % (Config.BASE_URL, Config.MERCHANT_ID) + '&'.join([str(k) + '=' + str(v) for k, v in kwargs.items()])
		return requests.get(url, auth=(Config.USERNAME, Config.PASSWORD)).json()
