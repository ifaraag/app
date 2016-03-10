import unittest

from app import app


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.r = self.app.get('/login')

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post('/login',
                             data=dict(username=username,
                                       password=password),
                             follow_redirects=True)

    def test_login_200(self):
        self.assertEquals(200, self.r.status_code)

    def test_login_title(self):
        self.assertIn(b'<title>Login to Hydrobase</title>', self.r.data)

    def test_login_index_link(self):
        self.assertIn(b'<a href="/index">Hydrobase</a>', self.r.data)

    def test_login(self):
        r = self.login('admin', 'wrong-password')
        self.assertIn(b'Invalid credentials. Please try again.', r.data)
        r = self.login('admin', 'admin')
        self.assertEquals(200, r.status_code)


if __name__ == '__main__':
    unittest.main()
