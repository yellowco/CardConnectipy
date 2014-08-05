from PaymentMethod import PaymentMethod

class BankAccount(PaymentMethod):
	CHECKING = 1
	SAVINGS = 2
	def __init__(self, **kwargs):
		self.bankaba = None
		super(BankAccount, self).__init__(**kwargs)

	###
	# API calls
	###

	@staticmethod
	def create(**kwargs):
		return BankAccount(**kwargs)

	@property
	def account_number(self):
		return self.account

	@account_number.setter
	def account_number(self, value):
		self.account = value

	@property
	def routing_number(self):
		return self.bankaba

	@routing_number.setter
	def routing_number(self, value):
		self.bankaba = value

	@property
	def type(self):
		return self.accttype

	@type.setter
	def type(self, value):
		self.accttype = value

	@property
	def data(self):
		raise NotImplementedError

	def sale(self, amount):
		return super(BankAccount, self).sale(amount=amount)

	def authorization(self, amount):
		return super(BankAccount, self).auth(amount=amount)

	# force transaction
	def force(self, amount):
		raise NotImplementedError

	def capture(self, amount):
		return super(BankAccount, self).capture(amount=amount)

	def credit(self, amount):
		return super(BankAccount, self).credit(amount=amount)

	###
	# housekeeping functions
	###

	def serialize(self):
		dict = super(BankAccount, self).serialize()
		dict.update({
			'bankaba':'' if self.bankaba == None else self.bankaba
		})
		return dict
