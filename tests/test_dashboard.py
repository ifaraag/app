import unittest

from app import app


class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.r = self.app.get('/dashboard')

    def tearDown(self):
        pass

    def test_dashboard_302(self):
        self.assertEquals(302, self.r.status_code)

    def test_dashboard_title(self):
        self.assertIn(b'</h1>\n<p>You should be redirected automatically to target URL: <a href="/login">/login</a>', self.r.data)


if __name__ == '__main__':
    unittest.main()
