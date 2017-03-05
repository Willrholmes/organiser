from django.test import TestCase
from cal.views import home

class HomepageTestCase(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
