from django.shortcuts import render, HttpResponse, redirect
from accounts.forms import NewUserForm
from django.contrib.auth.models import User
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
            return redirect('cal:home')
        else:
            print(form.errors)
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
            return redirect('/cal/')
            #return render(request, 'home.html', calendar(_date, title, username))
    return redirect('/cal/')

def logout_view(request):
    logout(request)
    return redirect('cal:home')
