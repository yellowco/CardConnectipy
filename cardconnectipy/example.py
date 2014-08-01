# things

from Config import HOSTNAME
from CreditCard import CreditCard

if __name__ == "__main__":
	# Config.config('fts.prinpay.com', '6443', '496160873888', 'testing', 'testing123')
	a = CreditCard(profileid='19092801181681761301/')
	print a.__dict__
	a.save()

