HOSTNAME = 'fts.prinpay.com'
PORT = '6443'
MERCHANT_ID = '496160873888'
USERNAME = 'testing'
PASSWORD = 'testing123'

BASE_URL = 'https://%s:%s/cardconnect/rest' % (HOSTNAME, PORT)
# python request headers
HEADERS = {'json' : {'Content-type': 'application/json'}}


"""
HOSTNAME = None
PORT = None
MERCHANT_ID = None
USERNAME = None
PASSWORD = None
"""

def config(hostname, port, merchant_id, username, password):
	HOSTNAME = hostname
	PORT = port
	MERCHANT_ID = merchant_id
	USERNAME = username
	PASSWORD = password
