import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MONGO_URI = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
DB_NAME = 'XXXXXXXXXXXXXX'


PUBNUB_PUBLISH_KEY = 'publish-me-not'
PUBNUB_SUBSCRIBE_KEY = 'ssubscribe-me-not'
PUBNUB_SECRET_KEY = 'secret-me-not'
PUBNUB_AUTH_KEY = 'auth-me-not'
PUBNUB_CHANNEL_GRP = "hydrobase"