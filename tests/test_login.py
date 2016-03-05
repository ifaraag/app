import unittest

from app import app


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post('/login',
                             data=dict(username=username,
                                       password=password),
                             follow_redirects=True)

    def test_login_200(self):
        r = self.app.get('/login')
        self.assertEquals(200, r.status_code)

    def test_login_title(self):
        r = self.app.get('/login')
        self.assertIn(b'Hydrobase Login', r.data)

    def test_login_index_link(self):
        r = self.app.get('/login')
        self.assertIn(b'<a href="/index">Hydrobase</a>', r.data)

    def test_login(self):
        r = self.login('admin', 'admin')
        self.assertEquals(200, r.status_code)
        r = self.login('admin', 'wrong-password')
        self.assertIn(b'Invalid credentials. Please try again.', r.data)


if __name__ == '__main__':
    unittest.main()
