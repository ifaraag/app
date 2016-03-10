import unittest

from app import app
from app.auth.models import User

class TestAuthModels(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.user = User('admin')

    def tearDown(self):
        pass

    def test_is_authenticated(self):
        self.assertEquals(True, self.user.is_authenticated())

    def test_is_active(self):
        self.assertEquals(True, self.user.is_active())

    def test_is_anonyous(self):
        self.assertEquals(False, self.user.is_anonymous())

    def test_get_id(self):
        self.assertEquals('admin', self.user.get_id())


if __name__ == '__main__':
	unittest.main()
