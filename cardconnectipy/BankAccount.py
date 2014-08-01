from PaymentMethod import PaymentMethod

class BankAccount(PaymentMethod):
	CHECKING = 1
	SAVINGS = 2
	def __init__(self, **kwargs):
		raise NotImplementedError
