import unittest

from app import app
from app.auth.views import load_user


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

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_200(self):
        self.assertEquals(200, self.r.status_code)

    def test_login_title(self):
        self.assertIn(b'<title>Log In to Hydrobase</title>', self.r.data)

    def test_login_index_link(self):
        self.assertIn(b'<a href="/index">Hydrobase</a>', self.r.data)

    def test_login_and_logout(self):
        r = self.login('admin', 'wrong-password')
        self.assertIn(b'Invalid credentials. Please try again.', r.data)
        r = self.login('admin', 'admin')
        self.assertEquals(200, r.status_code)
        out = self.logout()
        self.assertIn(b'<title>Log In to Hydrobase</title>', out.data)

    def test_load_user_Wolfeschlegelsteinhausenbergerdorff_is_None(self):
        self.assertEquals(None, load_user('Wolfeschlegelsteinhausenbergerdorff'))


if __name__ == '__main__':
    unittest.main()
