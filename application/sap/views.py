from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden as Http403, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from application.sap.forms import (
    UserRegistrationForm, 
    UserLoginForm,
    UserSettingsForm,
)
from application.sap.models import User


@login_required(login_url='/signin/')
def index(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
        logout(request)
    return render(request, 'signup.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserLoginForm()
        logout(request)
    return render(request, 'signin.html', {'form': form})


def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'profile.html', {'profile': user})
    else:
        raise Http404


@login_required(login_url='/signin/')
def settings(request):
	user = get_object_or_404(User, username=request.user)

	if request.method == 'POST':
		form = UserSettingsForm(
            instance=user,
            data=request.POST,
            files=request.FILES
        )

		if form.is_valid():
			form.save()
			return profile(request, user.username)
	else:
		form = UserSettingsForm(instance=user)

	return render(request, 'settings.html', {'form': form})


@login_required(login_url='/signin/')
def create_poll(request):
    return render(request, 'create_poll.html')


@login_required(login_url='/signin/')
def statistics(request):
    return render(request, 'statistics.html')
