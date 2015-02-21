import os
import application
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, application.app.config['DATABASE'] = tempfile.mkstemp()
		application.app.config['TESTING'] = True
		self.app = application.app.test_client()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(application.app.config['DATABASE'])

	def test_app_urls(self):
		rv = self.app.get('/')
		self.assertEqual(200, rv.status_code)

if __name__ == '__main__':
    unittest.main()