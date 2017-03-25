from django.test import TestCase
from cal.views import home
from cal.models import Events
from datetime import datetime, date

class HomepageTestCase(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'calendar.html')

    def test_home_is_calendar(self):
        response = self.client.get('/')

        month = datetime.now().strftime("%B")
        year = datetime.now().strftime("%Y")

        html = response.content.decode('utf8')
        self.assertIn(month, html)
        self.assertIn(year, html)
        self.assertIn("Create New Event", html)

        for day in range(1, 28):
            self.assertIn(str(day), html)

class EventsTestCase(TestCase):

    def test_for_events(self):
        _date = date.today()
        new_event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing...")

        self.assertEqual(new_event.title, "Event 1")
        self.assertEqual(new_event.start_date, date.today())
        self.assertEqual(new_event.description, "Testing...")

    def test_create_event_page(self):
        response = self.client.get('/newevent/')
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Title", html)
        self.assertIn("Start date", html)
        self.assertIn("Private?", html)
        self.assertIn("Create", html)

    def test_events_show_in_calendar(self):
        _date = date.today()
        new_event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing...")
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertIn(new_event.title, html)

class navigationTestCase(TestCase):

    def testMonth(self):
        response = self.client.get('/2/2017')
        html = response.content.decode('utf8')
        self.assertIn('February, 2017', html)
