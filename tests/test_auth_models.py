import unittest

from app import app
from app.auth.models import User

class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_is_authenticated(self):
        user=User('anubhav')
        self.assertEquals(user.is_authenticated(), 'True')

    def test_is_active(self):
        user=User('anubhav')
        self.assertEquals(user.is_active(), 'True')	

    def test_is_anonyous(self):
        user=User('anubhav')
        self.assertEquals(user.is_anonymous(), 'False')

    def test_get_id(self):
        user=User('anubhav')
        self.assertEquals(user.get_id(), 'anubhav')	

if __name__ == '__main__':
	unittest.main()
