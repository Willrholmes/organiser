from django.test import TestCase
from cal.views import home
import datetime

class HomepageTestCase(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_is_calendar(self):
        response = self.client.get('/')

        month = datetime.datetime.now().strftime("%B")
        year = datetime.datetime.now().strftime("%Y")

        html = response.content.decode('utf8')
        self.assertIn(month, html)
        self.assertIn(year, html)

        for day in range(1, 28):
            self.assertIn(str(day), html)
