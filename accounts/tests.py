from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import NewUserForm, AddFriendForm
from accounts.models import Account
from unittest.mock import patch, call
from cal.tests import LoggedInTestCase
import uuid

class UserTest(TestCase):

    def test_create_account(self):
        new_account = User.objects.create(
            email="test@test.com",
            password="password",
            username="Test User"
        )
        self.assertEqual(new_account.email, "test@test.com")
        self.assertEqual(new_account.password, "password")
        self.assertEqual(new_account.username, "Test User")

    def test_home_has_login_option(self):
        response = self.client.get("/cal/")
        html = response.content.decode('utf8')
        self.assertIn("login", html)
        self.assertIn("Create Account", html)

class CreateUserFormTest(TestCase):

    def test_create_account_page(self):
        response = self.client.get("/accounts/new-account/")
        html = response.content.decode('utf8')
        self.assertIn("Email*", html)
        self.assertIn("Password*", html)
        self.assertIn("Confirm Password*", html)
        self.assertIn("Username", html)

    def test_form_creates_model(self):
        form_data = {'username':'Test_User',
                    'email':"test@test.com",
                    'password':"awd",
                    'confirm_password':"awd"}
        form = NewUserForm(form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(email="test@test.com")
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.password, "awd")

    def test_password_and_confirm_password_match(self):
        form_data = {'email':"test@test.com",
                    'password':"awd",
                    'confirm_password':"wd"}
        form = NewUserForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Your Passwords Do Not Match!", form.errors['__all__'])

class loginTest(LoggedInTestCase):

    def test_wrong_password_login(self):
        response = self.client.login(username="Test_User", password="passwor")
        self.assertEqual(response, False)
        response = self.client.login(username="Anon User", password="password")
        self.assertEqual(response, False)
        response = self.client.login(username="Test_User", password="password")
        self.assertEqual(response, True)

    def test_user(self):
        user = User.objects.get(username="Test_User")
        Account_user = Account.objects.get(user=user)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.username, "Test_User")
        self.assertEqual(Account_user.user, user)

class multipleUserTest(LoggedInTestCase):

    def test_add_friend_form_page(self):
        response = self.client.get("/accounts/add-friend/")
        html = response.content.decode('utf8')
        self.assertIn('Username', html)

    def test_add_friend(self):
        user = User.objects.get(username="Test_User")
        account_user = Account.objects.get(user=user)
        user_2 = User.objects.create_user(
            email="test2@test.com",
            username="Test_User2",
            password="password2",
            )
        account_user2 = Account.objects.get(user=user_2)

        account_user2.friends.add(account_user)
        friend = list(account_user2.friends.all())[0]
        self.assertEqual(friend, account_user)
