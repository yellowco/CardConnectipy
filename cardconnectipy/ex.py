from PaymentMethod import PaymentMethod
from CreditCard import CreditCard
from BankAccount import BankAccount
from pprint import pprint

pprint(CreditCard(account='5461160000875487', expiry='1116').verify())
pprint(BankAccount(account='12321321321', bankaba='122100024').verify())
