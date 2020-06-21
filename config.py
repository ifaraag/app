import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
HOST="0.0.0.0"
PORT=int("80")

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MONGO_URI = "mongodb+srv://admin:admin@cluster0-4w9h4.gcp.mongodb.net/hydrosmart?retryWrites=true&w=majority"
DB_NAME = 'hydrosmart'


PUBNUB_PUBLISH_KEY = 'pub-c-662a8ff6-793e-497d-9793-1e870410e1c2'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-825013ca-afef-11ea-af7b-9a67fd50bac3'
PUBNUB_SECRET_KEY = 'sec-c-NTc2ZjI4OGEtZjFlNy00Yzc3LWEwYTgtMWMzMjgwZWYwNDcy'
PUBNUB_AUTH_KEY = 'auth-me-not'
PUBNUB_CHANNEL_GRP = "hydrosmart"