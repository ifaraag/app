import unittest

from app import app


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index_200(self):
        r = self.app.get('/index')
        self.assertEquals(200, r.status_code)

    def test_index_title(self):
        r = self.app.get('/index')
        self.assertIn(b'Welcome to Hydrobase', r.data)

    def test_index_index_link(self):
        r = self.app.get('/index')
        self.assertIn(b'<a href="/index">Hydrobase</a>', r.data)

    def test_index_login_link(self):
        r = self.app.get('/index')
        self.assertIn(b'<a href="login">Login</a>', r.data)


if __name__ == '__main__':
    unittest.main()
