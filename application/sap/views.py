import telebot
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden as Http403, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from application.sap.forms import (
    CommentedFeedbackSettingsForm,
    CommentedFeedbackForm,
    UserRegistrationForm, 
    UserLoginForm,
    UserSettingsForm,
)
from application.sap.models import (
    CommentedFeedback,
    CommentedFeedbackSettings,
    User,
)
from application.settings import CONFIG


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
def statistics(request):
    return render(request, 'statistics.html')


@login_required(login_url='/signin/')
def sending_to_telegram(request, hash):
    cfs = CommentedFeedbackSettings.objects.get_by_hash(hash=hash)
    url = "{}/{}".format(
        cfs.base_url, 
        cfs.hash_url,
    )

    try:
        bot = telebot.TeleBot(CONFIG['token'])
        bot.send_message(cfs.telegram_channel, text=url)
    except telebot.apihelper.ApiException as e:
        return render(request, 'response_message.html', 
            {'message': "Bot is not a member of the channel chat or this channel chat does not exist."}
        )
    except Exception as e:
        return render(request, 'response_message.html', 
            {'message': "Something bad happend... Bot has not send this link. Please, try again."}
        )

    return redirect('/')


@login_required(login_url='/signin/')
def creating_commented_feedback_settings(request):
    if request.method == 'POST':
        form = CommentedFeedbackSettingsForm(request.POST)
        if form.is_valid():
            hash_url = uuid.uuid4()
            user = User.objects.by_username(username=request.user)
            cfs = CommentedFeedbackSettings.objects.create(
                group_name=form.cleaned_data['group_name'],
                telegram_channel=form.cleaned_data['telegram_channel'],
                subject=form.cleaned_data['subject'],
                hash_url=hash_url,
                base_url = "{}/feedback/comment".format(request.META['HTTP_HOST']),
                user=user,
            )
            cfs.save()

            return render(request, 'generated_link.html', 
                {
                    'message': "Commented feedback link",
                    'base_link': cfs.base_url,
                    'hash_url': cfs.hash_url,
                }
            )
    else:
        form = CommentedFeedbackSettingsForm()

    return render(request, 'creating_commented_feedback.html', {'form': form})


def getting_commented_feedback(request, hash):
    cfs = CommentedFeedbackSettings.objects.get_by_hash(hash=hash)

    if request.method == 'POST':
        form = CommentedFeedbackForm(request.POST)
        if form.is_valid():

            cf = CommentedFeedback.objects.create(
                text=form.cleaned_data['text'],
                group_name=cfs.group_name,
                user=cfs.user,
            )
            cf.save()

            return render(request, 'response_message_student.html', 
                {'message': "Thank you!"}
            )
    else:
        form = CommentedFeedbackForm()

    return render(request, 'commented_feedback.html', 
        {
            'form': form,
            'group_name': cfs.group_name,
            'subject': cfs.subject,
            'hash_url': cfs.hash_url,
        }
    )
