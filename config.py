import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MONGO_URI = 'mongodb://admin:admin@ds011268.mlab.com:11268'
DB_NAME = 'analytics-hydrobase'


PUBNUB_PUBLISH_KEY = 'pub-c-e7fbaa01-b0a2-47d3-8409-e0328d166df0'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-8493a7ba-e4aa-11e5-a4f2-0619f8945a4f'
PUBNUB_SECRET_KEY = 'sec-c-MTk4YjhlYzAtM2JhYS00MWYxLWE5NzQtMTBhZjAwMjVlODIw'