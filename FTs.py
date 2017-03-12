from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import datetime
import time
import unittest

MAX_WAIT = 5

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def wait_for(self, output):
        start_time = time.time()
        while True:
            try:
                return output()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
            time.sleep(0.1)

    def test_homepage_is_calendar(self):
        self.browser.get("http://localhost:8000")
        self.assertIn('Calendar', self.browser.title)

        month = datetime.datetime.now().strftime("%B")
        home_month = self.browser.find_element_by_name('month')
        self.assertEqual(month, home_month)

    def test_create_new_event(self):
        self.browser.get("http://localhost:8000")

        # Open new event setup
        self.browser.find_element_by_id("new_event").click()
        wait_for(
            lambda: self.browser.find_element_by_id("event_start")
        )

        # Input details
        self.browser.find_element_by_id("event_start").send_keys("25/06/2017")
        self.browser.find_element_by_id("event_end").send_keys("29/06/2017")
        self.browser.find_element_by_id("event_name").send_keys("Glasto 2017")
        self.browser.find_element_by_id("confirm").click()

        # Find event
        self.assertEqual(1+1, 3, "Complete FT!!!")


    def tearDown(self):
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
