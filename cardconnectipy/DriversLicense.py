class DriversLicense(object):
	def __init__(self, **kwargs):
		self.number = None
		self.state = None
		self.__dict__.update(**kwargs)
	def serialize(self):
		data = {
			'license':"%s:%s" % (self.state, self.number) if self.state and self.number else None
		}
		return dict((k, v) for k, v in data.iteritems() if v)
