from libs.mudpy.Mud import Mud
import Client
import Config
import requests
import json

class PaymentMethod(Mud):
	def __init__(self, **kwargs):
		self.client = None
		self.acctid = None
		self.account = None	# tokenized card / bank account number
		self.accttype = None	# oneof PPAL, PAID, GIFT, PDEBIT in PUT, oneof VISA, MC, DISC, ECHK in GET
		self.defaultacct = None

		# fields to ensure the tests pass
		self.note = None
		self.random_data = None

		super(PaymentMethod, self).__init__(**kwargs)

	###
	# API calls
	###

	@property
	def type(self):
		return self.accttype
        
	@type.setter
	def type(self, value):
		self.accttype = value

	@property
	def account_holder(self):
		return self.client.name

	@account_holder.setter
	def account_holder(self, v):
		# if this is implemented, then we will need to save client upon PaymentMethod.save
		#	this will lead to circular saving unless Client also inherits MudPy
		raise NotImplemented

	@property
	def can_debit(self):
		if not 'respstat' in self.__dict__:
			self.deserialize(self.verify()[2])
		return(self.respstat == 'A')

	###
	# housekeeping functions
	###

	def serialize(self):
		return {
			'defaultacct':'' if self.defaultacct == None else self.defaultacct,
			'profile':'' if self.client == None else self.client.id + '/',
			'account':'' if self.account == None else self.account,
			'accttype':'' if self.accttype == None else self.accttype,
		}

	# the profileid is NOT saved upon a profile GET request
	@property
	def profileid(self):
		return self.client.id

	# returns if the account number is a token or plaintext
	@property
	def is_token(self):
		return self.acctid != None

	def deserialize(self, data):
		for key, value in data.items():
			try:
				setattr(self, key, value)
			except AttributeError:
				pass
		return self

	@property
	def id(self):
		return '%s/%s' % (self.profileid, self.acctid)

	def delete(self):
		if(self.acctid != None):
			requests.delete('%s/profile/%s/%s' % (Config.BASE_URL, self.id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD))

	def save(self):
		if (not self.is_dirty) and (self.acctid != None):
			return
		# do we need to call client.save () if client calls payment_method.save()
		# self.client.save()
		if(self.acctid == None):
			# account numbers must be tokens
			self.account = self.tokenize()
		payload = {
			'merchid':Config.MERCHANT_ID,
		}
		payload.update(self.serialize())
		response = requests.put('%s/profile' % (Config.BASE_URL), data=json.dumps(payload), auth=(Config.USERNAME, Config.PASSWORD), headers=Config.HEADERS['json']).json()
		self.deserialize(response)
		super(PaymentMethod, self).save()

	# CAVEAT -- PM.retrieve does not get the associated client
	@staticmethod
	def retrieve(id):
		# id of form "<profileid>/<acctid>"
		resp = requests.get('%s/profile/%s/%s/' % (Config.BASE_URL, id, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()[0]
		c = Client.retrieve(resp.pop('profileid'))
		p.client = c
		return p

	@staticmethod
	def create(**kwargs):
		return PaymentMethod(**kwargs)

	# base AUTHORIZATION request
	# cf. http://bit.ly/1ohnJEb for 3DSecure support
	def auth(self, amount=None, currency=None, **kwargs):
		payload = {
			'merchid':Config.MERCHANT_ID,
			'amount':'' if amount == None else str(amount),
			'currency':'USD' if currency == None else currency
		}
		if(self.client != None):
			payload.update(self.client.serialize())
		# cvv, etc. in here as well
		payload.update(kwargs)
		payload.update(self.serialize())
		resp = requests.put('%s/auth' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD), data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		resp['amount'] = str(int(float(resp['amount']))  * 100)
		# custom filtering of response codes would be preferred to further rule out suspicious transactions
		# suggested filter (by the app) by cvvresp, authcode, etc.
		return (resp['respstat'] == 'A', resp['retref'], resp)

	# shorthand for auth(0) -- sees if the payment method is in good standing
	def verify(self, **kwargs):
		return PaymentMethod.auth(self, amount='0', **kwargs)

	# tokenize the account number
	def tokenize(self):
		if(self.account != None):
			resp = PaymentMethod.auth(self, amount='0', tokenize='Y')
			# there was a problem with authorizing a zero-value card -- this indicates an invalid card number
			if 'token' not in resp[2]:
				raise AttributeError("invalid account / routing number")
			return resp[2]['token']

	# utilize AUTHORIZE-CAPTURE request feature
	# cf. http://bit.ly/1qzs8p1 for additional fields to present to the AUTHORIZATION request payload
	def sale(self, amount=None, **kwargs):
		return PaymentMethod.auth(self, amount=amount, capture='Y', **kwargs)

	# money to be handed back to the end-user -- given in POSITIVE amount
	def credit(self, amount=None, **kwargs):
		return PaymentMethod.auth(self, amount=-amount, capture='Y', **kwargs)

	# given an AUTH id, confirm the transaction and move to settlement
	def capture(self, amount=None):
		if 'retref' not in self.__dict__:
			raise AttributeError("payment method retref not set")
		Transaction.retrieve(id=self.retref).capture(amount=amount)

	# given an AUTH id, decide to void all or part of the transaction
	def void(self, amount=None):
		if 'retref' not in self.__dict__:
			raise AttributeError("payment method retref not set")
		Transaction.retrieve(id=self.retref).void(amount=amount)
