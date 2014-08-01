from PaymentMethod import PaymentMethod

class CreditCard(PaymentMethod):
	VISA = None
	MASTERCARD = None
	DISCOVER = None
	AMERICAN_EXPRESS = None
	DINERS_CLUB = None
	JCB = None
	def __init__(self, **kwargs):
		self.expiry = None
		PaymentMethod.__init__(self, **kwargs)

	@staticmethod
	def create(**kwargs):
		return CreditCard(**kwargs)

	# base AUTHORIZATION request
	def auth(amount=None, cvv=None, **kwargs):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return(super(CreditCard, self).auth(amount=amount, cvv2=cvv, **kwargs))

	def capture(amount=None, cvv=None, **kwargs):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return(super(CreditCard, self).capture(amount=amount, cvv2=cvv, **kwargs))

	# amount to be gained by the company
	def sale(amount=None, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return(self.capture(amount=amount, cvv=cvv))

	# amount to be sent back to user -- amount is therefore treated as NEGATIVE in AUTH request
	# input as a POSITIVE number
	def credit(amount=None, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return(self.capture(amount=-amount, cvv=cvv))

	# shorthand for auth(0, cvv)
	def verify(cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return self.auth(0, cvv=cvv)
