class Address(object):
	def __init__(self, **kwargs):
		self.first_name = None
		self.last_name = None
		self.street1 = None
		self.street2 = None
		self.city = None
		self.state = None
		self.postal = None
		self.country = 'US'
		self.phone = None
		self.__dict__.update(**kwargs)

