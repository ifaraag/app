import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'This string will be replaced with a proper key in production.'

MONGO_URI = 'mongodb://admin:admin@ds011268.mlab.com:11268/analytics-hydrobase'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "somethingimpossibletoguess"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}

PUBNUB_PUBLISH_KEY = 'pub-c-e7fbaa01-b0a2-47d3-8409-e0328d166df0'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-8493a7ba-e4aa-11e5-a4f2-0619f8945a4f'
PUBNUB_SECRET_KEY = 'sec-c-MTk4YjhlYzAtM2JhYS00MWYxLWE5NzQtMTBhZjAwMjVlODIw'