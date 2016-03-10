import unittest

from app import app


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.r = self.app.get('/index')

    def tearDown(self):
        pass

    def test_index_200(self):
        self.assertEquals(200, self.r.status_code)

    def test_index_title(self):
        self.assertIn(b'<title>Welcome to Hydrobase</title>', self.r.data)

    def test_index_bootstrap_cdn(self):
        self.assertIn(b'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css',
                      self.r.data)

    def test_index_index_link(self):
        self.assertIn(b'<a href="/index">Hydrobase</a>', self.r.data)

    def test_index_login_link(self):
        self.assertIn(b'<a href="/login">Log In</a>', self.r.data)

    def test_index_signup_link(self):
        self.assertIn(b'<a href="/signup">Sign Up</a>', self.r.data)


if __name__ == '__main__':
    unittest.main()
