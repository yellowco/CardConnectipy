import datetime
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

	###
	# API calls
	###

	@staticmethod
	def create(**kwargs):
		return CreditCard(**kwargs)

	@property
	def card_number(self):
		return self.account

	@card_number.setter
	def card_number(self, value):
		self.account = value

	@property
	def expiration_date(self):
		return datetime.datetime.strptime(self.expiry, "%m%y")

	@expiration_date.setter
	def expiration_date(self, value):
		self.expiry = value.strftime('%m%y')

	@property
	def card_type(self):
		raise NotImplementedError

	@card_type.setter
	def card_type(self, value):
		raise NotImplementedError

	@property
	def is_procurement_card(self):
		raise NotImplementedError

	@is_procurement_card.setter
	def is_procurement_card(self, value):
		raise NotImplementedError

	@property
	def data(self):
		raise NotImplementedError

	# amount to be gained by the company
	def sale(self, amount, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).sale(amount=amount, cvv2=cvv)

	def authorization(self, amount, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).auth(amount=amount, cvv2=cvv)

	# force transaction
	def preauthorization(self, amount, cvv=None):
		raise NotImplementedError

	def capture(self, amount, cvv=None):
		return super(CreditCard, self).capture(amount=amount, cvv2=cvv)

	def credit(self, amount, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).credit(amount=amount, cvv=cvv)

	def balance_inquiry(self, amount, cvv=None):
		raise NotImplementedError

	###
	# housekeeping functions
	###

	def serialize(self):
		dict = super(CreditCard, self).serialize()
		dict.update({
			'expiry':'' if self.expiry == None else self.expiry
		})
		return dict

	# shorthand for auth(0, cvv)
	def verify(self, cvv=None):
		if(cvv == None):
			cvv = getattr(self, 'cvv', None)
		return super(CreditCard, self).verify(cvv2=cvv)
