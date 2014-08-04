from PaymentMethod import PaymentMethod

class BankAccount(PaymentMethod):
	CHECKING = 1
	SAVINGS = 2
	def __init__(self, **kwargs):
		# bank routing number -- self.account is now the banking account number instead
		self.bankaba = None
		super(BankAccount, self).__init__(**kwargs)

	@staticmethod
	def create(**kwargs):
		return BankAccount(**kwargs)

	def serialize(self):
		dict = super(BankAccount, self).serialize()
		dict.update({
			'bankaba':'' if self.bankaba == None else self.bankaba
		})
		return dict

	def auth(self, amount=None, bankaba=None, **kwargs):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return super(BankAccount, self).auth(amount=amount, bankaba=bankaba, **kwargs)

	def capture(self, amount=None, bankaba=None, **kwargs):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return super(BankAccount, self).capture(amount=amount, bankaba=bankaba, **kwargs)

	# amount to be gained by the company
	def sale(self, amount=None, bankaba=None):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return self.capture(amount=amount, bankaba=bankaba)

	# amount to be sent back to user -- amount is therefore treated as NEGATIVE in AUTH request
	# input as a POSITIVE number
	def credit(self, amount=None, bankaba=None):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return self.capture(amount=-amount, bankaba=bankaba)

	# shorthand for auth(0, bankaba)
	def verify(self, bankaba=None):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return super(BankAccount, self).verify(bankaba=bankaba)
