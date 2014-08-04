from PaymentMethod import PaymentMethod

class BankAccount(PaymentMethod):
	CHECKING = 1
	SAVINGS = 2
	def __init__(self, **kwargs):
		self.bankaba = None				# routing number -- self.account is now the banking account number instead
		PaymentMethod.__init__(self, **kwargs)

	@staticmethod
	def create(**kwargs):
		return BankAccount(**kwargs)

	# base AUTHORIZATION request
	def auth(amount=None, bankaba=None, **kwargs):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return super(BankAccount, self).auth(amount=amount, bankaba=bankaba, **kwargs)

	def capture(amount=None, bankaba=None, **kwargs):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return super(BankAccount, self).capture(amount=amount, bankaba=bankaba, **kwargs)

	# amount to be gained by the company
	def sale(amount=None, bankaba=None):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return self.capture(amount=amount, bankaba=bankaba)

	# amount to be sent back to user -- amount is therefore treated as NEGATIVE in AUTH request
	# input as a POSITIVE number
	def credit(amount=None, bankaba=None):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return self.capture(amount=-amount, bankaba=bankaba)

	# shorthand for auth(0, bankaba)
	def verify(bankaba=None):
		if(bankaba == None):
			bankaba = getattr(self, 'bankaba', None)
		return super(BankAccount, self).verify(amount=amount, bankaba=bankaba)
