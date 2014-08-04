import Config
import requests
import json

class Transaction(object):
	def __init__(self, **kwargs):
		self.retref = None
		self.amount = None
		self.authcode = None
		self.__dict__.update(kwargs)

	@property
	def tx_id(self):
		return self.retref

	@property
	def status(self):
		if 'setlstat' not in self.__dict__:
			self.deserialize(self.inquire()[2])
		return self.__dict__['setlstat']

	def deserialize(self, data):
		for key, value in data.items():
			setattr(self, key, value)
		return self

	@staticmethod
	def retrieve(id):
		return Transaction(Transaction.inquire(id)[2])

	# VOID request -- possible to issue partial voids
	def void(self, amount=None):
		payload = {
			'merchid':Config.MERCHANT_ID,
			'retref':self.retref
		}
		# full reversal implied when amount field is omitted
		if(amount != None):
			payload['amount'] = amount
		resp = requests.put('%s/void' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD), data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		if(('amount' in resp) and (resp['amount'] < 1.)):
			resp['amount'] = str(int(float(resp['amount']))  * 100)

		# update the amount remaining of the transaction
		self.deserialize(self.inquire())

		return (resp['respstat'] == 'A', resp['retref'], resp)

	# capture AUTH request for settlement
	def capture(self, amount=None):
		if self.authcode == None:
			self.deserialize(self.inquire()[2])

		payload = {
			'merchid':Config.MERCHANT_ID,
			'retref':self.retref,
			'authcode':self.authcode,
			'amount':self.amount if amount == None else amount,
		}
		resp = requests.put('%s/capture' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD0, data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		resp['amount'] = str(int(float(resp['amount']) * 100))
		return (True, resp['retref'], resp)

	# REFUND request -- possible to issue partial refunds
	def refund(self, amount=None):
		payload = {
			'merchid':Config.MERCHANT_ID,
			'retref':self.retref
		}
		# full reversal implied when amount field is omitted
		if(amount != None):
			payload['amount'] = amount
		resp = requests.put('%s/refund' % (Config.BASE_URL), auth=(Config.USERNAME, Config.PASSWORD), data=json.dumps(payload), headers=Config.HEADERS['json']).json()
		if(('amount' in resp) and (resp['amount'] < 1.)):
			resp['amount'] = str(int(float(resp['amount']))  * 100)

		# update the amount remaining of the transaction
		self.deserialize(self.inquire())

		return (resp['respstat'] == 'A', resp['retref'], resp)

	@staticmethod
	def inquire(retref=None):
		resp = requests.get('%s/inquire/%s/%s' % (Config.BASE_URL, retref, Config.MERCHANT_ID), auth=(Config.USERNAME, Config.PASSWORD)).json()
		if(('amount' in resp) and (resp['amount'] < 1.)):
			resp['amount'] = str(int(float(resp['amount']))  * 100)

		return(resp['respstat'] == 'A', resp['retref'], resp)

	def inquire(self):
		return(Transaction.inquire(self.retref))

	@staticmethod
	def deposit(**kwargs):
		url = '%s/deposit?merchid=%s&' % (Config.BASE_URL, Config.MERCHANT_ID) + '&'.join([str(k) + '=' + str(v) for k, v in kwargs.items()])
		resp = requests.get(url, auth=(Config.USERNAME, Config.PASSWORD)).json()
		# convert to minor USD units
		# cf. http://bit.ly/1zLWxGi
		for deposit in resp:
			deposit['amount'] = str(int(float(deposit['amount']))  * 100)
			deposit['cbackamnt'] = str(int(float(deposit['cbackamnt']))  * 100)
			deposit['feeamnt'] = str(int(float(deposit['feeamnt']))  * 100)
			for tx in deposit['txns']:
				tx['feeamnt'] = str(int(float(tx['feeamnt']))  * 100)
				tx['depamnt'] = str(int(float(tx['depamnt']))  * 100)
		return resp

	@staticmethod
	def settlement_status(**kwargs):
		url = '%s/settlestat?merchid=%s&' % (Config.BASE_URL, Config.MERCHANT_ID) + '&'.join([str(k) + '=' + str(v) for k, v in kwargs.items()])
		return requests.get(url, auth=(Config.USERNAME, Config.PASSWORD)).json()
