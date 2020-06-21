import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MONGO_URI = 'mongodb+srv://admin:admin@cluster0-4w9h4.gcp.mongodb.net/hydrosmart?retryWrites=true&w=majority'
DB_NAME = 'hydrosmart'


PUBNUB_PUBLISH_KEY = 'pub-c-d820df08-5466-4cfc-a868-704d857db647'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-942b13b6-b313-11ea-875a-ceb74ea8e96a'
PUBNUB_SECRET_KEY = 'sec-c-OTAyOTY0NWUtNzRhZS00Nzg4LWJmNmItOWMyYjQwYWFkZWYy'
PUBNUB_AUTH_KEY = 'auth-me-not'
PUBNUB_CHANNEL_GRP = "hydrosmart"