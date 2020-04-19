import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import get_language

from application.sap.forms import FeedbackSettingsForm
from application.sap.models import (
    EstimatedFeedback,
    FeedbackSettings,
    User,
)


@login_required(login_url='/auth/signin/')
def index(request):
    feedback_list = FeedbackSettings.objects.get_all(user_id=request.user)

    return render(
        request, 
        'internal/feedback/index.html', 
        {'feedback_list': feedback_list},
    )


@login_required(login_url='/auth/signin/')
def create(request):
    if request.method == 'POST':
        form = FeedbackSettingsForm(request.POST)
        url, tg_chan = None, None
        
        if form.is_valid():
            user = User.objects.by_username(username=request.user)
            existing = FeedbackSettings.objects.get_where(
                group_name=form.cleaned_data['group_name'].upper(),
                subject=form.cleaned_data['subject'],
                class_type=form.cleaned_data['class_type'],
                telegram_channel=form.cleaned_data['telegram_channel'],
                feedback_type=form.cleaned_data['feedback_type'],
                user=user,
                date=request.POST['date']
            )
            if existing is None:
                _hash = uuid.uuid4()
                url = "/feedback/get/{}/{}".format(
                    form.cleaned_data['feedback_type'], 
                    _hash,
                )
                tg_chan = form.cleaned_data['telegram_channel']

                fs = FeedbackSettings.objects.create(
                    group_name=form.cleaned_data['group_name'].upper(),
                    subject=form.cleaned_data['subject'],
                    class_type=form.cleaned_data['class_type'],
                    telegram_channel=form.cleaned_data['telegram_channel'],
                    feedback_type=form.cleaned_data['feedback_type'],
                    url=url,
                    _hash=_hash,
                    user=user,
                    date=request.POST['date'],
                )
                fs.save()
            else:
                url = existing.url
                tg_chan = existing.telegram_channel

            result_url = request.META['HTTP_HOST'] + url
            return render(
                request, 
                'internal/feedback/generated_link.html', 
                {'url': result_url, 'telegram_channel': tg_chan},
            )
    else:
        form = FeedbackSettingsForm()

    return render(request, 'internal/feedback/create.html', {'form': form})


@login_required(login_url='/auth/signin/')
def delete(request):
    if request.method == 'POST':
        feedback_id = int(request.POST.get('id'))
        feedback = FeedbackSettings.objects.get_by_id(id=feedback_id)
        if feedback.user.id != request.user.id:
            raise Http403
        feedback.delete()
        return redirect('/{}/feedback/'.format(get_language()))
    else:
        raise Http404


def get(request, feedback_type, hash):
    fs = FeedbackSettings.objects.get_by_hash(_hash=hash)
    user = User.objects.by_username(username=fs.user)
    print(user.first_name)

    if feedback_type == 'commented':
        return render(request, 'external/feedback/get_commented_feedback.html', 
            {
                'group_name': fs.group_name,
                'subject': fs.subject,
                'professor': user,
                'class_type': fs.class_type,
                'settings': fs.id,
            }
    )
    if feedback_type == 'estimated':
        return render(request, 'external/feedback/get_estimated_feedback.html', 
            {
                'group_name': fs.group_name,
                'subject': fs.subject,
                'professor': user,
                'class_type': fs.class_type,
                'settings': fs.id,
                'RATING_CHOICES': EstimatedFeedback.RATING_CHOICES,
            }
    )

    raise Http404 
