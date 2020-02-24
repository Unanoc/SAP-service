from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from application.sap.views import (
    auth,
    feedback, 
    home,
    statistics,
    telegram,
    user,
)


urlpatterns = [
    path('', home.index, name='index'),

    path('auth/signup/', auth.signup, name='auth-signup'),
    path('auth/signin/', auth.signin, name='auth-signin'),
    path('auth/signout/', auth.signout, name='auth-signout'),

    path('user/profile/<username>/', user.profile, name='user-profile'),
    path('user/settings/', user.settings, name='user-settings'),

    path('statistics/', statistics.index, name='statistics-index'),
    path('statistics/commented/', statistics.commented, name='statistics-commented'),
    path('statistics/estimated/', statistics.estimated, name='statistics-estimated'),

    path('feedback/create/commented/feedback/', feedback.create_commented_feedback, name='feedback-create_commented_feedback'),
    path('feedback/create/estimated/feedback/', feedback.create_estimated_feedback, name='feedback-create_estimated_feedback'),
    path('feedback/get/commented/<hash>/', feedback.get_commented_feedback, name='feedback-get_commented_feedback'),
    path('feedback/get/estimated/<hash>/', feedback.get_estimated_feedback, name='feedback-get_estimated_feedback'),

    path('api/telegrambot/send/<hash>/', telegram.telegrambot_send_to_telegram, name='api-telegrambot_send_to_telegram'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
