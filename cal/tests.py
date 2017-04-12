from django.test import TestCase
from cal import views
from cal.models import Events
from cal.models import Account
from django.contrib.auth.models import User
from cal.forms import EventForm
from datetime import datetime, date
from django.shortcuts import render

_date = date.today()
whole_date = "%s/%s/%s" % (
    _date.strftime('%d'), _date.strftime('%m'), _date.strftime('%Y'))

class LoggedInTestCase(TestCase):

    def setUp(self):
        new_user = User.objects.create_user(
            email="test@test.com", username="Test_User", password="password"
            )
        user = self.client.login(username="Test_User", password="password")

class HomepageTestCase(LoggedInTestCase):

    def test_home(self):
        response = self.client.get('/cal/')
        self.assertTemplateUsed(response, 'calendar.html')

    def test_home_is_calendar(self):
        response = self.client.get('/cal/')

        month = _date.strftime("%B")
        year = _date.strftime("%Y")

        html = response.content.decode('utf8')
        self.assertIn(month, html)
        self.assertIn(year, html)
        self.assertIn("Create New Event", html)

        # Check all days for given month in calendar
        days = int(_date.strftime("%d"))
        for day in range(1, days):
            self.assertIn(str(day), html)

class EventsTestCase(LoggedInTestCase):

    def test_for_events(self):
        new_event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing..."
            )

        self.assertEqual(new_event.title, "Event 1")
        self.assertEqual(new_event.start_date, _date)
        self.assertEqual(new_event.description, "Testing...")

    def test_create_event_page(self):
        response = self.client.get('/cal/newevent/')
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Title", html)
        self.assertIn("Start date", html)
        self.assertIn("submit", html)

    def test_events_show_in_calendar(self):
        new_event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing..."
            )
        response = self.client.get('/cal/')
        html = response.content.decode('utf8')
        self.assertIn(new_event.title, html)

    def test_event_view(self):
        new_event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing..."
            )
        response = self.client.get('/cal/events/1/')
        html = response.content.decode('utf8')
        self.assertIn("Event 1", html)
        self.assertIn("Testing...", html)

    def test_cannot_view_non_related_user_event(self):
        new_event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing..."
            )
        new_user = User.objects.create_user(
            email="test2@test.com", username="Test_User2", password='password'
            )
        user = self.client.login(username="Test_User2", password="password")
        response = self.client.get('/cal/events/1/')
        html = response.content.decode('utf8')
        self.assertEqual('', html)

class CalFormTest(LoggedInTestCase):

    def test_initial_date(self):
        response = self.client.get('/cal/newevent/?')
        html = response.content.decode('utf8')
        self.assertIn(str(whole_date), html)

    def test_edit_form_test(self):
        event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing..."
            )
        instance = Events.objects.get(id=1)
        form = EventForm(instance=instance)
        self.assertIn("Event 1", form.as_p())
        self.assertIn(str(whole_date), form.as_p())
        self.assertIn("Testing...", form.as_p())

class NavigationTestCase(LoggedInTestCase):

    def test_month(self):
        response = self.client.get('/cal/2/2017?')
        html = response.content.decode('utf8')
        self.assertIn('February 2017', html)

class NotLoggedInTests(TestCase):

    def test_no_events_on_home(self):
        event = Events.objects.create(
            title="Event 1", start_date=_date, description="Testing..."
            )
        response = self.client.get('/cal/')
        html = response.content.decode('utf8')
        self.assertNotIn('<li><a id="event"', html)

class InviteOtherUsersTest(LoggedInTestCase):

    def test_create_event_with_other_users(self):
        user_2 = User.objects.create_user(
            email="test2@test.com",
            username="Test_User2",
            password="password2",
        )
        user_2.save()
        account_2 = Account.objects.get(user=user_2)
        event = Events.objects.create(
            title="Event 1",
            start_date=_date,
            description="Testing...",
            )
        event.attendees.add(account_2)
        user = self.client.login(username="Test_User2", password="password2")
        response = self.client.get("/cal/")
        html = response.content.decode('utf8')
        self.assertIn("Event 1", html)
