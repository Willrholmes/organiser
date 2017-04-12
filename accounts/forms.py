from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Password*")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm Password*")

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        labels = {'email':"Email*"}

    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Your Passwords Do Not Match!")
        return cleaned_data

class AddFriendForm(forms.Form):
    username = forms.CharField()
