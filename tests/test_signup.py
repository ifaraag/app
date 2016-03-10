import unittest

from app import app


class TestSignup(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.r = self.app.get('/signup')

    def tearDown(self):
        pass

    def signup(self, username, email, password):
        return self.app.post('/signup',
                             data=dict(username=username,
                                       email=email,
                                       password=password,
                                       confirm=password),
                             follow_redirects=False)

    def test_signup_200(self):
        self.assertEquals(200, self.r.status_code)

    def test_signup_title(self):
        self.assertIn(b'<title>Sign Up for Hydrobase</title>', self.r.data)


if __name__ == '__main__':
    unittest.main()
