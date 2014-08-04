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
		super(CreditCard, self).__init__(**kwargs)

	@staticmethod
	def create(**kwargs):
		return CreditCard(**kwargs)

	def serialize(self):
		dict = super(CreditCard, self).serialize()
		dict.update({
			'expiry':'' if self.expiry == None else self.expiry
		})
		return dict

	# base AUTHORIZATION request
	def auth(self, amount=None, cvv=None, **kwargs):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).auth(amount=amount, cvv2=cvv, **kwargs)

	def capture(self, amount=None, cvv=None, **kwargs):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).capture(amount=amount, cvv2=cvv, **kwargs)

	# amount to be gained by the company
	def sale(self, amount=None, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return self.capture(amount=amount, cvv=cvv)

	# amount to be sent back to user -- amount is therefore treated as NEGATIVE in AUTH request
	# input as a POSITIVE number
	def credit(self, amount=None, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return self.capture(amount=-amount, cvv=cvv)

	# shorthand for auth(0, cvv)
	def verify(self, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).verify(cvv2=cvv)
