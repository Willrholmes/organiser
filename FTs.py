from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from datetime import datetime, date, timedelta
import time
import unittest

MAX_WAIT = 15

def wait_for(output):
    start_time = time.time()
    while True:
        try:
            return output()
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
        time.sleep(0.1)

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(FunctionalTest, cls).tearDownClass()

    def test_homepage_is_calendar(self):
        self.browser.get('%s%s' % (self.live_server_url, "/"))
        self.assertIn('Calendar', self.browser.title)

        month = datetime.now().strftime("%B")
        home_month = self.browser.find_element_by_class_name('welcome').text
        self.assertIn(month, home_month)

    def test_create_new_event(self):
        self.browser.get('%s%s' % (self.live_server_url, "/"))

        # Open new event setup
        self.browser.find_element_by_class_name("new_event").click()
        wait_for(
            lambda: self.browser.find_element_by_class_name("new-event-form")
        )

        _today = date.today()
        date_1 = _today + timedelta(+1)

        # Input details
        self.browser.find_element_by_id("id_end_date").send_keys(str(date_1))
        self.browser.find_element_by_id("id_title").send_keys("Event 1")
        self.browser.find_element_by_id("submit").click()

        # Find event
        wait_for(
            lambda: self.browser.find_element_by_id("calendarify")
        )

        self.browser.find_element_by_xpath("//a[@href='/Event 1/']")

    def test_next_month(self):
        self.browser.get('%s%s' % (self.live_server_url, "/"))
        self.browser.find_element_by_class_name("next_month").click()

        wait_for(
            lambda: self.browser.find_element_by_id("calendarify")
        )

        month_year = self.browser.find_element_by_class_name("welcome").text
        month_int = int(date.today().strftime("%m")) + 1
        if month_int == 'January':
            year_int = int(date.today().strftime("%y")) + 1
        else:
            year_int = int(date.today().strftime("%y"))
        _date = date.today().replace(year=year_int, month=month_int)
        _month = _date.strftime("%B")
        _year = _date.strftime("%y")
        self.assertIn(_month, month_year)
        self.assertIn(_year, month_year)

    def test_last_month(self):
        self.browser.get('%s%s' % (self.live_server_url, "/"))
        self.browser.find_element_by_class_name("last_month").click()

        wait_for(
            lambda: self.browser.find_element_by_id("calendarify")
        )

        month_year = self.browser.find_element_by_class_name("welcome").text
        month_int = int(date.today().strftime("%m")) - 1
        if month_int == 'December':
            year_int = int(date.today().strftime("%y")) - 1
        else:
            year_int = int(date.today().strftime("%y"))
        _date = date.today().replace(year=year_int, month=month_int)
        _month = _date.strftime("%B")
        _year = _date.strftime("%y")
        self.assertIn(_month, month_year)
        self.assertIn(_year, month_year)

if __name__ == "__main__":
    unittest.main()
