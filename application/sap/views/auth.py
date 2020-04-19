from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.translation import get_language

from application.sap.forms import UserRegistrationForm, UserLoginForm
from application.sap.models import User


def signup(request):
    if request.user.is_authenticated:
        return redirect('/{}/'.format(get_language()))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/{}/'.format(get_language()))
    else:
        form = UserRegistrationForm()
        logout(request)
    return render(request, 'internal/auth/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/{}/'.format(get_language()))
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/{}/'.format(get_language()))
    else:
        form = UserLoginForm()
        logout(request)
    return render(request, 'internal/auth/signin.html', {'form': form})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/{}/'.format(get_language()))
