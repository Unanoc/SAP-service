from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from application.sap.forms import (
    GroupAverageStatisticsForm,
    GroupDayInfoStatisticsForm,
    CommentedStatisticsForm,
)


@login_required(login_url='/auth/signin/')
def index(request):
    return render(request, 'internal/statistics/index.html')


@login_required(login_url='/auth/signin/')
def commented(request):
    form = CommentedStatisticsForm() 

    return render(request, 
        'internal/statistics/commented/index.html',
        {'form': form, 'user_id': request.user.id}
    )


@login_required(login_url='/auth/signin/')
def estimated(request):
    return render(request, 'internal/statistics/estimated/index.html')


@login_required(login_url='/auth/signin/')
def estimated_by_group(request):
    form = GroupAverageStatisticsForm()

    return render(request, 
        'internal/statistics/estimated/bygroup.html', 
        {'form': form, 'user_id': request.user.id}
    )


@login_required(login_url='/auth/signin/')
def estimated_by_day(request):
    form = GroupDayInfoStatisticsForm()

    return render(request, 
        'internal/statistics/estimated/byday.html', 
        {'form': form, 'user_id': request.user.id}
    )
