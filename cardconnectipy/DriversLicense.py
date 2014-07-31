class DriversLicense(object):
	def __init__(self, **kwargs):
		self.number = None
		self.state = None
		self.__dict__.update(**kwargs)
