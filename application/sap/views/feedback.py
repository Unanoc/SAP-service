import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError

from application.sap.forms import (
    CommentedFeedbackForm,
    FeedbackSettingsForm,
)
from application.sap.models import (
    CommentedFeedback,
    EstimatedFeedback,
    FeedbackSettings,
    User,
)


@login_required(login_url='/auth/signin/')
def create_commented_feedback(request):
    if request.method == 'POST':
        form = FeedbackSettingsForm(request.POST)
        if form.is_valid():
            user = User.objects.by_username(username=request.user)
            existing = FeedbackSettings.objects.get_where(
                group_name=form.cleaned_data['group_name'].upper(),
                subject=form.cleaned_data['subject'],
                user=user,
                base_url="{}/feedback/get/commented".format(request.META['HTTP_HOST']),
                date=datetime.date(datetime.now())
            )
            if existing is None:
                hash_url = uuid.uuid4()
                fs = FeedbackSettings.objects.create(
                    group_name=form.cleaned_data['group_name'].upper(),
                    telegram_channel=form.cleaned_data['telegram_channel'],
                    subject=form.cleaned_data['subject'],
                    hash_url=hash_url,
                    base_url = "{}/feedback/get/commented".format(request.META['HTTP_HOST']),
                    user=user,
                )
                fs.save()

                base_url = fs.base_url
                _hash = fs.hash_url
            else:
                base_url = existing.base_url
                _hash = existing.hash_url

            return render(request, 'internal/feedback/generated_link.html', 
                {
                    'message': "Commented feedback link",
                    'base_url': base_url,
                    'hash': _hash,
                }
            )
    else:
        form = FeedbackSettingsForm()

    return render(request, 'internal/feedback/create_commented_feedback.html', {'form': form})


def get_commented_feedback(request, hash):
    fs = FeedbackSettings.objects.get_by_hash(hash=hash)

    if request.method == 'POST':
        form = CommentedFeedbackForm(request.POST)
        if form.is_valid():

            cf = CommentedFeedback.objects.create(
                text=form.cleaned_data['text'],
                group_name=fs.group_name,
                user=fs.user,
                date=fs.date,
            )
            cf.save()

            return render(request, 'external/response_message.html', 
                {'message': "Thank you!"}
            )
    else:
        form = CommentedFeedbackForm()

    return render(request, 'external/feedback/get_commented_feedback.html', 
        {
            'form': form,
            'group_name': fs.group_name,
            'subject': fs.subject,
            'hash_url': fs.hash_url,
        }
    )


@login_required(login_url='/auth/signin/')
def create_estimated_feedback(request):
    if request.method == 'POST':
        form = FeedbackSettingsForm(request.POST)
        if form.is_valid():
            user = User.objects.by_username(username=request.user)
            existing = FeedbackSettings.objects.get_where(
                group_name=form.cleaned_data['group_name'].upper(),
                subject=form.cleaned_data['subject'],
                user=user,
                base_url="{}/feedback/get/estimated".format(request.META['HTTP_HOST']),
                date=datetime.date(datetime.now())
            )
            if existing is None:
                hash_url = uuid.uuid4()
                fs = FeedbackSettings.objects.create(
                    group_name=form.cleaned_data['group_name'].upper(),
                    telegram_channel=form.cleaned_data['telegram_channel'],
                    subject=form.cleaned_data['subject'],
                    hash_url=hash_url,
                    base_url = "{}/feedback/get/estimated".format(request.META['HTTP_HOST']),
                    user=user,
                )
                fs.save()

                base_url = fs.base_url
                _hash = fs.hash_url
            else:
                base_url = existing.base_url
                _hash = existing.hash_url

            return render(request, 'internal/feedback/generated_link.html', 
                {
                    'message': "Estimated feedback link",
                    'base_url': base_url,
                    'hash': _hash,
                }
            )
    else:
        form = FeedbackSettingsForm()

    return render(request, 'internal/feedback/create_estimated_feedback.html', {'form': form})


def get_estimated_feedback(request, hash):
    fs = FeedbackSettings.objects.get_by_hash(hash=hash)

    if request.method == 'POST':
        try:
            cf = EstimatedFeedback.objects.create(
                rating=request.POST['rating'],
                comment=request.POST['comment'],
                group_name=fs.group_name,
                user=fs.user,
                date=fs.date,
            )
            cf.save()
        except MultiValueDictKeyError:
            pass

        return render(request, 'external/response_message.html', 
            {'message': "Thank you!"}
        )
    else:
        return render(request, 'external/feedback/get_estimated_feedback.html', 
            {
                'group_name': fs.group_name,
                'subject': fs.subject,
                'hash_url': fs.hash_url,
                'RATING_CHOICES': EstimatedFeedback.RATING_CHOICES,
            }
        )
