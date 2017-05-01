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
        username = form.data['username']
        email = form.data['email']
        password = form.data['password']
        if form.is_valid():
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect('cal:home')
    else:
        form = NewUserForm()
    return render(request, 'newaccount.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/cal/')
        else:
            messages.error(request,
                "Your username and password didn't match. Please try again.",
                extra_tags='login-error')
            return redirect('/cal/')
            #return render(request, 'home.html', calendar(_date, title, username))
    return redirect('/cal/')

def logout_view(request):
    logout(request)
    return redirect('cal:home')

def AddFriend(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = AddFriendForm(request.POST)
            username = form.data['username']
            if form.is_valid():
                user = User.objects.get(username=request.user)
                account = Account.objects.get(user=user)
                friend = User.objects.get(username=username)
                friend_account = Account.objects.get(user=friend)
                account.friends.add(friend_account)
                return redirect('cal:home')
        else:
            form = AddFriendForm()
        return render(request, 'addfriend.html', {'form':form})
    else:
        messages.error(request, "Please login to add a friend!",
                        extra_tags="add-friend-error")
    return redirect('cal:home')
