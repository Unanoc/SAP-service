from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/auth/signin/')
def index(request):
    return render(request, 'internal/root/index.html')
