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

	def serialize(self):
		data = {
			'address':"%s %s" % (self.street1, self.street2) if self.street1 and self.street2 else None,
			'region':self.state,
			'phone':self.phone,
			'postal':self.postal,
			'name':"%s %s" % (self.first_name, self.last_name) if self.first_name and self.last_name else None,
			'country':self.country,
			'city':self.city
		}	
		return dict((k, v) for k, v in data.iteritems() if v)
