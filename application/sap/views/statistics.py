from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/auth/signin/')
def index(request):
    return render(request, 'internal/statistics/index.html')


@login_required(login_url='/auth/signin/')
def commented(request):
    return render(request, 'internal/statistics/commented.html')


@login_required(login_url='/auth/signin/')
def estimated(request):
    return render(request, 'internal/statistics/estimated.html')