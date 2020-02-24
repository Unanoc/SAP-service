from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from application.sap.forms import UserSettingsForm
from application.sap.models import User


def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'internal/user/profile.html', {'profile': user})
    else:
        raise Http404


@login_required(login_url='/auth/signin/')
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

	return render(request, 'internal/user/settings.html', {'form': form})
