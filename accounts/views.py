from django.shortcuts import render, redirect, HttpResponse
from accounts.forms import NewUserForm, AddFriendForm
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Account
from django.contrib.auth import authenticate, login, logout
from cal.views import home
from cal.backend import monthdict, calendar
from datetime import date, datetime

def NewUser(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        #Pull data from form for creation
        username = form.data['username']
        email = form.data['email']
        password = form.data['password']
        if form.is_valid():
            #Django authentication works best when called via API instead of
            #submitting form as if it were a normal (user created) model
            user = User.objects.create_user(username, email, password)
            user.save()
            #Log user in after creation
            login(request, user)
            return redirect('cal:home')
    else:
        form = NewUserForm()
    return render(request, 'newaccount.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Use Django's built in authenticate function
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/cal/')
        else:
            #If authentication fails an error message will be displayed
            messages.error(
                request,
                "Your username and password didn't match. Please try again.",
                extra_tags='login-error'
                )
            return redirect('/cal/')
    return redirect('/cal/')

def logout_view(request):
    #Use Django's built in logout function
    logout(request)
    return redirect('cal:home')

def AddFriend(request):
    #Users can only add friends if they are authenticated
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = AddFriendForm(request.POST)
            username = form.data['username']
            if form.is_valid():
                #Need to pull User model to be able to pull Account model.
                user = User.objects.get(username=request.user)
                account = Account.objects.get(user=user)
                friend = User.objects.get(username=username)
                friend_account = Account.objects.get(user=friend)
                #Again user model API to carryout request
                account.friends.add(friend_account)
                return redirect('cal:home')
        else:
            form = AddFriendForm()
        return render(request, 'addfriend.html', {'form':form})
    return redirect('cal:home')
