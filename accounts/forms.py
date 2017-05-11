from django.forms import ModelForm
from accounts.models import Account
from django.contrib.auth.models import User
from django import forms

#Form for adding new user taken from Django authentication (User) model
class NewUserForm(ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':"form-control", 'placeholder':"Password*"}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':"form-control", 'placeholder':"Confirm Password*"}))

    #Meta class allows specification of which model fields required in form
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        labels = {'email':"Email*"}
        #Widgets allows us to add attributes to HTML for form. Used for styling
        widgets = {'email':forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Email'}),
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Username"
            }),
        }

    # Clean data function added to check passwords match
    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()

        #Pull passwords from cleaned data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        #Check passwords match
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Your Passwords Do Not Match!")
        return cleaned_data


class AddFriendForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':"form-control",
            'placeholder':"Username",
        }))


    #Clean data function added to check username added exists
    def clean(self):
        cleaned_data = super(AddFriendForm, self).clean()

        #Pull username from cleaned data
        username = cleaned_data.get('username')

        #Check username in Account model
        if not Account.objects.filter(username=username).exists():
            raise forms.ValidationError("This account does not exist!")
        return cleaned_data
