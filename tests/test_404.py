import unittest

from app import app


class Test404(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_not_found(self):
		r = self.app.get('/404')
		self.assertIn(b'Redirecting', r.data)	

if __name__ == '__main__':
	unittest.main()
