import unittest

from app import app


class TestLogout(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.r = self.app.get('/logout')

    def tearDown(self):
        pass

    def test_logout_to_login_not_logged_in_returns_302(self):
        self.assertEquals(302, self.r.status_code)

    def test_logout_to_login_not_logged_in_redirecting(self):
        self.assertIn(b'Redirecting', self.r.data)


if __name__ == '__main__':
    unittest.main()
