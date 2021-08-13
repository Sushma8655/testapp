from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .decorators import allowed_users
from datetime import datetime, timedelta

# Create your views here.
x = datetime.now()


@login_required(login_url='login/')
def home(request):
    x1 = datetime.now()
    return render(request, 'index.html', {'time': x1, })


@allowed_users(allowed_roles=['Admin'])
def registerPage(request):
    x = datetime.now()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/login')
    context = {'form': form, 'time': x, }
    return render(request, 'signup.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)
    # return render(reverse('login'))


def logoutUser(request):
    logout(request)
    return redirect('/login')
