import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MONGO_URI = 'mongodb://admin:admin@ds011268.mlab.com:11268/analytics-hydrobase'
DB_NAME = 'analytics-hydrobase'


PUBNUB_PUBLISH_KEY = 'pub-c-93c6c384-e1a0-412f-87cf-e626aaab6a00'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-8ec9d89e-e4aa-11e5-a4f2-0619f8945a4f'
PUBNUB_SECRET_KEY = 'sec-c-YzQyMTU3NmYtMDNhMS00MzM5LTg3MTgtZjA2N2U0N2IyNGY3'
PUBNUB_AUTH_KEY = '40ed6434-1991-4f7a-8034-20a072abde43'
PUBNUB_CHANNEL_GRP = "hydrobase"