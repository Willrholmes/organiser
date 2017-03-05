from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def test_homepage(self):
        self.browser.get("http://localhost:8000")
        self.assertIn('Calendar', self.browser.title)

    def tearDown(self):
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
