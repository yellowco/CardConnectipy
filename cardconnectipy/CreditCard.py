from PaymentMethod import PaymentMethod

class CreditCard(PaymentMethod):
	def __init__(self, **kwargs):
		self.expiry = None
		PaymentMethod.__init__(self, **kwargs)

	@staticmethod
	def create(**kwargs):
		return CreditCard(**kwargs)

	# base AUTHORIZATION request
	def auth(amount, cvv):
		raise NotImplementedError

	# CAPTURE request -- will call authorize first
	def sale(amount, cvv):
		raise NotImplementedError

	def void(amount, retref):
		raise NotImplementedError

	# REFUND request
	def credit(amount, cvv):
		raise NotImplementedError

	# shorthand for auth(0, cvv)
	def verify(cvv):
		raise NotImplementedError
