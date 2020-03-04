from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from application.sap.forms import (
    GroupStatisticsForm,
)


@login_required(login_url='/auth/signin/')
def index(request):
    return render(request, 'internal/statistics/index.html')


@login_required(login_url='/auth/signin/')
def commented(request):
    return render(request, 'internal/statistics/commented/index.html')


@login_required(login_url='/auth/signin/')
def estimated(request):
    return render(request, 'internal/statistics/estimated/index.html')


@login_required(login_url='/auth/signin/')
def estimated_groups(request):
    form = GroupStatisticsForm()

    return render(request, 
        'internal/statistics/estimated/groups.html', 
        {'form': form, 'user_id': request.user.id}
    )
